#!/usr/bin/env python3
"""DEFI-M8 — loi d'attachement dérivée de S_sim : calculs exacts sur petits graphes.

Contribution du pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
Implémentation 1 (numpy, graphes codés en masques de bits). Tout est exact
(énumération complète des secteurs), aucune approximation de Monte-Carlo.

Cadre identique à RAPPORT.md (hypothèse H-abs) :
  S_sim(C) = log(1 + n_tri(C)) - beta * D(C),  D = std(deg)/mean(deg)  (ddof=0)
  pi_{N,M}(C) ∝ exp(N * S_sim(C) / tau),       beta = 0.30, tau = 0.50
Le nouveau sommet porte l'étiquette N ; il naît relié à un ensemble A de k
anciens sommets (k = 1 : mitose seule ; k >= 2 : k - 1 arêtes de fermeture).

Noyaux comparés (tous généalogiques : aucune arête ancienne n'est recâblée) :
  U  : A uniforme parmi les C(N, k) parties ;
  G* : attachement de Gibbs (bain thermique sur le voisinage du nouveau-né),
       G*(A | C) = pi_{N+1,M+k}(C + v_A) / somme_{|A'|=k} pi_{N+1,M+k}(C + v_A').
Mesures : TV(pi_{N,M} G, pi_{N+1,M+k}) ; borne de la proposition C (RAPPORT.md
§ 3.3) : TV(pi_{N,M}, R# pi_{N+1,M+k}) ; échanges de Metropolis nécessaires
ensuite pour TV <= 0,1 / 0,01 / 0,001.

Usage : python3 defi_m8_attachement_gibbs.py [--sans-relaxation-7]
Sortie : defi_m8_resultats.json (même dossier) + résumé à l'écran.
"""
import itertools
import json
import math
import pathlib
import sys
import time

import numpy as np
import scipy.sparse as sp

BETA, TAU = 0.30, 0.50
ICI = pathlib.Path(__file__).resolve().parent


def paires_ordonnees(n):
    """Paires de {0..n} : d'abord les paires anciennes (i<j<n), puis (i, n)."""
    anc = list(itertools.combinations(range(n), 2))
    return anc, anc + [(i, n) for i in range(n)]


def masques_secteur(L, m):
    """Tous les sous-ensembles à m éléments de {0..L-1}, en masques triés."""
    out = np.fromiter((sum(1 << b for b in c) for c in itertools.combinations(range(L), m)),
                      dtype=np.int64)
    out.sort()
    return out


def s_sim_masques(nsom, P, masques):
    """S_sim vectorisé pour des graphes à nsom sommets dont les arêtes sont codées
    par des bits selon la liste de paires P."""
    bits = ((masques[:, None] >> np.arange(len(P))[None, :]) & 1).astype(np.int64)
    deg = np.zeros((len(masques), nsom))
    for b, (u, v) in enumerate(P):
        deg[:, u] += bits[:, b]
        deg[:, v] += bits[:, b]
    pos = {p: b for b, p in enumerate(P)}
    ntri = np.zeros(len(masques), dtype=np.int64)
    for x, y, z in itertools.combinations(range(nsom), 3):
        ntri += bits[:, pos[(x, y)]] & bits[:, pos[(x, z)]] & bits[:, pos[(y, z)]]
    moy = deg.mean(axis=1)
    if np.any(moy == 0):
        raise ValueError("degré moyen nul : D non défini (RO-02)")
    return np.log1p(ntri) - BETA * deg.std(axis=1) / moy, ntri


def gibbs(nsom, S):
    lw = nsom * S / TAU
    w = np.exp(lw - lw.max())
    return w / w.sum()


def kl(p, q):
    s = p > 0
    return float((p[s] * np.log(p[s] / q[s])).sum())


def tv(p, q):
    return 0.5 * float(np.abs(p - q).sum())


def cas_naissance(n, m, k):
    """Lois à la naissance pour un passage (n, m) -> (n+1, m+k)."""
    anc, P2 = paires_ordonnees(n)
    La = len(anc)
    MA = masques_secteur(La, m)
    S, _ = s_sim_masques(n, anc, MA)
    pi = gibbs(n, S)
    M2 = masques_secteur(len(P2), m + k)
    S2, ntri2 = s_sim_masques(n + 1, P2, M2)
    pi2 = gibbs(n + 1, S2)
    # restriction aux anciens sommets et voisinage du nouveau-né
    restr = M2 & ((1 << La) - 1)
    voisin = M2 >> La
    degv = np.array([bin(int(x)).count("1") for x in voisin])
    bon = degv == k
    # indice de la restriction dans le secteur (n, m) (si elle a m arêtes)
    i_restr = np.searchsorted(MA, restr)
    i_restr[~bon] = 0
    assert np.all(MA[i_restr[bon]] == restr[bon])
    # borne de la proposition C : TV(pi, R# pi2)
    marg = np.bincount(i_restr[bon], weights=pi2[bon], minlength=len(MA))
    hors = float(pi2[~bon].sum())
    borne = 0.5 * (float(np.abs(pi - marg).sum()) + hors)
    # noyau uniforme
    nb = math.comb(n, k)
    nu_U = np.zeros(len(M2))
    nu_U[bon] = pi[i_restr[bon]] / nb
    # noyau de Gibbs : G*(A|C) = pi2(C+A) / Z_k(C), Z_k(C) = marg(C)
    nu_G = np.zeros(len(M2))
    nu_G[bon] = pi[i_restr[bon]] * pi2[bon] / marg[i_restr[bon]]
    for nom, nu in (("U", nu_U), ("G", nu_G)):
        assert abs(nu.sum() - 1) < 1e-12, (nom, nu.sum())
    # anatomie de G* : nombre d'arêtes entre les cibles (triangles fermés par la naissance)
    # e(A) = n_tri(C + A) - n_tri(C) ; on calcule la loi de e(A) sous U et G*
    _, ntri_anc = s_sim_masques(n, anc, MA)
    eA = ntri2[bon] - ntri_anc[i_restr[bon]]
    loi_e = {}
    for nom, nu in (("U", nu_U), ("G", nu_G)):
        loi_e[nom] = {int(e): float(nu[bon][eA == e].sum()) for e in np.unique(eA)}
    return {
        "N": n, "M": m, "k": k, "N_apres": n + 1, "M_apres": m + k,
        "etats_avant": int(len(MA)), "etats_apres": int(len(M2)),
        "P_pi_apres_deg_nouveau_egal_k": 1 - hors,
        "borne_prop_C": borne,
        "TV_naissance_uniforme": tv(nu_U, pi2),
        "TV_naissance_gibbs": tv(nu_G, pi2),
        "loi_e_A_aretes_entre_cibles": loi_e,
        "KL_naissance_uniforme": kl(nu_U, pi2),
        "KL_naissance_gibbs": kl(nu_G, pi2),
    }, (P2, M2, pi2, nu_U, nu_G)


def noyau_echange(L, M2, pi2):
    """Échange de Metropolis à |E| fixé, proposition uniforme (retirer une arête,
    ajouter une non-arête), acceptation min(1, pi'/pi). Renvoie la transposée."""
    m = bin(int(M2[0])).count("1")
    nprop = m * (L - m)
    n_et = len(M2)
    lig, col, val = [], [], []
    diag = np.ones(n_et)
    for e in range(L):
        a_e = ((M2 >> e) & 1) == 1
        for f in range(L):
            if f == e:
                continue
            sel = a_e & (((M2 >> f) & 1) == 0)
            i = np.nonzero(sel)[0]
            if len(i) == 0:
                continue
            j = np.searchsorted(M2, M2[i] ^ (1 << e) ^ (1 << f))
            p = np.minimum(1.0, pi2[j] / pi2[i]) / nprop
            lig.append(i); col.append(j); val.append(p)
            np.subtract.at(diag, i, p)
    lig = np.concatenate(lig + [np.arange(n_et)])
    col = np.concatenate(col + [np.arange(n_et)])
    val = np.concatenate(val + [diag])
    K = sp.csr_matrix((val, (lig, col)), shape=(n_et, n_et))
    return K


def relaxation(L, M2, pi2, departs, t_max=4000):
    K = noyau_echange(L, M2, pi2)
    sto = float(np.abs(np.asarray(K.sum(axis=1)).ravel() - 1).max())
    KT = K.T.tocsr()
    inv = float(np.abs(KT @ pi2 - pi2).max())
    out = {"controle_stochastique": sto, "controle_invariance_pi": inv}
    courbes = {}
    for nom, nu in departs.items():
        x = nu.copy()
        cibles = {0.1: None, 0.01: None, 0.001: None}
        courbe = []
        for t in range(t_max + 1):
            d = tv(x, pi2)
            courbe.append(d)
            for eps in cibles:
                if cibles[eps] is None and d <= eps:
                    cibles[eps] = t
            if all(v is not None for v in cibles.values()):
                break
            x = KT @ x
        out[nom] = {str(a): b for a, b in cibles.items()}
        out["KL_naissance_" + nom] = kl(nu, pi2)
        out["TV_t_" + nom] = {str(t): courbe[t] for t in (0, 1, 2, 5, 10, 20, 50, 100) if t < len(courbe)}
        courbes[nom] = courbe
    # premier t où la courbe de G* passe au-dessus de celle de U (croisement)
    u, g = courbes["U"], courbes["G"]
    croise = next((t for t in range(min(len(u), len(g))) if g[t] > u[t] + 1e-15), None)
    out["premier_t_TV_G_superieure_a_TV_U"] = croise
    return out


def main():
    sans7 = "--sans-relaxation-7" in sys.argv
    t0 = time.time()
    res = {"cadre": {"beta": BETA, "tau": TAU, "poids": "exp(N*S_sim/tau)",
                     "hypothese": "H-abs : graphes abstraits étiquetés, sans contrainte Rips",
                     "implementation": "1 (numpy, masques de bits)"},
           "naissance": [], "relaxation": []}
    # A. tous les k pour les secteurs de départ de RAPPORT.md (parties C et D)
    departs = [(4, 3), (4, 4), (4, 5), (5, 5), (5, 7), (5, 8), (6, 9), (6, 11)]
    for n, m in departs:
        for k in range(1, n + 1):
            if m + k > n * (n + 1) // 2:
                break
            r, _ = cas_naissance(n, m, k)
            res["naissance"].append(r)
            print(f"N={n} M={m} k={k} -> M'={m+k}: borne={r['borne_prop_C']:.6f} "
                  f"TV_U={r['TV_naissance_uniforme']:.6f} TV_G*={r['TV_naissance_gibbs']:.6f} "
                  f"P(deg=k)={r['P_pi_apres_deg_nouveau_egal_k']:.4f}", flush=True)
    # B. relaxation après naissance, mêmes cas que RAPPORT.md § 3.4
    # mêmes cas que RAPPORT.md § 3.4, puis les meilleurs k où G* gagne à la naissance
    cas_d = [(4, 5, 2), (5, 8, 3)] + ([] if sans7 else [(6, 11, 3)])
    cas_d += [(4, 3, 3), (4, 4, 3), (5, 5, 4), (5, 7, 4)] + ([] if sans7 else [(6, 9, 4)])
    for n, m, k in cas_d:
        r, (P2, M2, pi2, nu_U, nu_G) = cas_naissance(n, m, k)
        rel = relaxation(len(P2), M2, pi2, {"U": nu_U, "G": nu_G})
        rel.update({"N": n, "M": m, "k": k, "etats_apres": int(len(M2)),
                    "TV_naissance_uniforme": r["TV_naissance_uniforme"],
                    "TV_naissance_gibbs": r["TV_naissance_gibbs"]})
        res["relaxation"].append(rel)
        print("relaxation", rel, flush=True)
    res["duree_s"] = round(time.time() - t0, 1)
    (ICI / "defi_m8_resultats.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print("écrit : defi_m8_resultats.json", res["duree_s"], "s")


if __name__ == "__main__":
    main()
