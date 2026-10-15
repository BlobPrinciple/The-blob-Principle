#!/usr/bin/env python3
"""RO-25 / RO-24 — pont croissance -> Gibbs : calculs exacts sur petits graphes.

Contribution du pilote IA du laboratoire (Claude, Anthropic), 15 octobre 2026.
Tout est exact (énumération complète) sauf la partie A (tirages aléatoires,
graine fixe) ; aucune approximation de Monte-Carlo dans B, C, D.

Cadre (déclaré, voir RAPPORT.md, hypothèse H-abs) : graphes simples étiquetés
abstraits, sans la contrainte géométrique Rips du moteur historique A_Gibbs.
  S_sim(C) = log(1 + n_tri(C)) - beta * D(C),  D = std(deg)/mean(deg)
  pi_{N,M}(C) ∝ exp(N * S_sim(C) / tau)   (armature V347.1, A3-A4)
  beta = 0.30, tau = 0.50                  (valeurs ARCHIVE / PRODUCTION)
std = écart-type de population (numpy.std, ddof=0), comme le script historique.

Usage :  python3 pont_croissance_gibbs.py            (environ 1 à 3 minutes)
         python3 pont_croissance_gibbs.py --rapide   (sans N = 7 en partie D)
Sortie : resultats.json (même dossier) + résumé à l'écran.
"""
import itertools
import json
import math
import pathlib
import sys

import numpy as np
import scipy.sparse as sp

BETA, TAU = 0.30, 0.50
ICI = pathlib.Path(__file__).resolve().parent


# ---------------------------------------------------------------- outils
def paires(n):
    return list(itertools.combinations(range(n), 2))


def s_sim(n, aretes):
    deg = np.zeros(n)
    adj = [set() for _ in range(n)]
    for u, v in aretes:
        deg[u] += 1
        deg[v] += 1
        adj[u].add(v)
        adj[v].add(u)
    m = deg.mean()
    if m == 0:
        return None  # D non défini en degré moyen nul (RO-02)
    ntri = sum(len(adj[u] & adj[v]) for u, v in aretes) // 3
    return math.log(1 + ntri) - BETA * deg.std() / m


def composantes(n, aretes):
    p = list(range(n))

    def f(x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x
    for u, v in aretes:
        p[f(u)] = f(v)
    return len({f(x) for x in range(n)})


def ntri_k4(n, aretes):
    a = set(aretes)
    e = lambda x, y: (min(x, y), max(x, y)) in a
    t = sum(1 for x, y, z in itertools.combinations(range(n), 3) if e(x, y) and e(y, z) and e(x, z))
    k4 = sum(1 for q in itertools.combinations(range(n), 4)
             if all(e(x, y) for x, y in itertools.combinations(q, 2)))
    return t, k4


def secteur(n, m):
    """Tous les graphes étiquetés à n sommets et m arêtes, et pi_{n,m}."""
    P = paires(n)
    etats = [tuple(c) for c in itertools.combinations(P, m)]
    S = np.array([s_sim(n, c) for c in etats], dtype=float)
    lw = n * S / TAU
    w = np.exp(lw - lw.max())
    return P, etats, w / w.sum()


def tv(p, q):
    return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())


# ---------------------------------------------------------------- A
def partie_a(graine=20261015, trajets=200, pas=400):
    """Invariant M - N sous mitose, collapse de feuille et échanges à |E| fixé."""
    rng = np.random.default_rng(graine)
    violations = 0
    nmax = 0
    for _ in range(trajets):
        n, E = 1, set()  # Omega^0
        for _ in range(pas):
            r = rng.random()
            if r < 0.5:  # mitose mu : nouvelle feuille
                v = int(rng.integers(n))
                E.add((v, n))
                n += 1
            elif r < 0.65:  # mu^{-1} : collapse d'une feuille (sommet de degré 1)
                deg = [0] * n
                for u, w in E:
                    deg[u] += 1
                    deg[w] += 1
                feuilles = [x for x in range(n) if deg[x] == 1]
                if feuilles and n > 2:
                    x = feuilles[int(rng.integers(len(feuilles)))]
                    E = {(a - (a > x), b - (b > x)) for a, b in E if x not in (a, b)}
                    n -= 1
            else:  # échange d'arêtes à |E| fixé (retire une arête, ajoute une non-arête)
                non = [p for p in itertools.combinations(range(n), 2) if p not in E]
                if E and non:
                    E.remove(sorted(E)[int(rng.integers(len(E)))])
                    E.add(non[int(rng.integers(len(non)))])
            nmax = max(nmax, n)
            if len(E) - n != -1:
                violations += 1
    return {"trajets": trajets, "pas_par_trajet": pas, "graine": graine,
            "N_max_atteint": nmax, "violations_de_M_moins_N_egal_moins_1": violations}


# ---------------------------------------------------------------- B
def partie_b(Ns=(4, 5, 6, 7)):
    """Secteur M = N - 1 : triangles et K4 imposent la fragmentation ; poids de Gibbs."""
    out = []
    for n in Ns:
        P, etats, pi = secteur(n, n - 1)
        viol_tri = viol_k4 = 0
        p_conn = p_tri = p_frag = 0.0
        e_ntri = 0.0
        for c, w in zip(etats, pi):
            k = composantes(n, c)
            t, k4 = ntri_k4(n, c)
            if t >= 1 and k < 2:
                viol_tri += 1
            if k4 >= 1 and k < 4:
                viol_k4 += 1
            p_conn += w * (k == 1)
            p_tri += w * (t >= 1)
            e_ntri += w * t
        out.append({"N": n, "M": n - 1, "graphes": len(etats),
                    "graphes_avec_triangle_et_connexes": viol_tri,
                    "graphes_avec_K4_et_moins_de_4_composantes": viol_k4,
                    "pi_P_connexe": p_conn, "pi_P_au_moins_un_triangle": p_tri,
                    "pi_E_n_tri": e_ntri})
    return out


# ---------------------------------------------------------------- C
def partie_c(cas=((4, 3), (4, 4), (5, 5), (5, 7), (6, 9))):
    """Obstruction généalogique : TV(pi_{N,M}, R#pi_{N+1,M+k}) minimisée sur k.

    R = restriction (sous-graphe induit sur les N premiers sommets). Pour tout noyau
    généalogique G (qui ne recâble aucune arête ancienne), R#(pi_{N,M} G) = pi_{N,M},
    donc TV(pi_{N,M} G, pi_{N+1,M'}) >= TV(pi_{N,M}, R#pi_{N+1,M'}).
    """
    out = []
    for n, m in cas:
        P, etats, pi = secteur(n, m)
        idx = {c: i for i, c in enumerate(etats)}
        meilleur = None
        Pn1 = paires(n + 1)
        for k in range(1, n + 1):
            m2 = m + k
            if m2 > len(Pn1):
                break
            _, etats2, pi2 = secteur(n + 1, m2)
            marg = np.zeros(len(etats))
            hors = 0.0  # masse dont la restriction n'a pas m arêtes
            for c2, w in zip(etats2, pi2):
                r = tuple(e for e in c2 if e[1] < n)
                if len(r) == m:
                    marg[idx[r]] += w
                else:
                    hors += w
            borne = 0.5 * (np.abs(pi - marg).sum() + hors)
            item = {"k_aretes_du_nouveau_sommet": k, "M_prime": m2,
                    "borne_inf_TV": float(borne),
                    "P_deg_nouveau_sommet_egal_k": float(1 - hors)}
            if meilleur is None or borne < meilleur["borne_inf_TV"]:
                meilleur = item
        out.append({"N": n, "M": m, "meilleur_k": meilleur})
    return out


# ---------------------------------------------------------------- D
def noyau_echange(n, P, etats, pi):
    """Noyau de Metropolis à |E| fixé : retire une arête et ajoute une non-arête,
    proposition uniforme (symétrique), acceptation min(1, pi'/pi)."""
    idx = {c: i for i, c in enumerate(etats)}
    m = len(etats[0])
    nprop = m * (len(P) - m)
    lig, col, val = [], [], []
    for i, c in enumerate(etats):
        cs = set(c)
        non = [p for p in P if p not in cs]
        reste = 1.0
        for e in c:
            base = cs - {e}
            for f in non:
                j = idx[tuple(sorted(base | {f}))]
                a = min(1.0, pi[j] / pi[i]) / nprop
                lig.append(i); col.append(j); val.append(a)
                reste -= a
        lig.append(i); col.append(i); val.append(reste)
    return sp.csr_matrix((val, (lig, col)), shape=(len(etats), len(etats)))


def croissance(n, m, k, etats, pi, etats2):
    """Mitose + fermeture : le sommet n naît relié à k anciens sommets distincts,
    choisis uniformément (k = 1 : mitose mu seule ; k >= 2 : k - 1 arêtes de fermeture)."""
    idx2 = {c: i for i, c in enumerate(etats2)}
    nu = np.zeros(len(etats2))
    choix = list(itertools.combinations(range(n), k))
    for c, w in zip(etats, pi):
        for S in choix:
            nu[idx2[tuple(sorted(c + tuple((s, n) for s in S)))]] += w / len(choix)
    return nu


def partie_d(cas=((4, 5, 2), (5, 8, 3), (6, 11, 3)), t_max=4000):
    out = []
    for n, m, k in cas:
        P, etats, pi = secteur(n, m)
        P2, etats2, pi2 = secteur(n + 1, m + k)
        nu = croissance(n, m, k, etats, pi, etats2)
        K = noyau_echange(n + 1, P2, etats2, pi2)
        KT = K.T.tocsr()
        # contrôles : stochasticité et invariance de pi
        sto = float(np.abs(np.asarray(K.sum(axis=1)).ravel() - 1).max())
        inv = float(np.abs(KT @ pi2 - pi2).max())
        courbe = {}
        t = 0
        x = nu.copy()
        cibles = {0.1: None, 0.01: None, 0.001: None}
        while t <= t_max:
            d = tv(x, pi2)
            if t in (0, 1, 10, 100, 1000) or t == t_max:
                courbe[t] = d
            for eps in cibles:
                if cibles[eps] is None and d <= eps:
                    cibles[eps] = t
            if all(v is not None for v in cibles.values()):
                courbe[t] = d
                break
            x = KT @ x
            t += 1
        out.append({"N_avant": n, "M_avant": m, "k": k, "N": n + 1, "M": m + k,
                    "etats": len(etats2), "controle_stochastique": sto,
                    "controle_invariance_pi": inv,
                    "TV_apres_t_echanges": {str(a): b for a, b in courbe.items()},
                    "echanges_pour_TV_inf_eps": {str(a): b for a, b in cibles.items()},
                    "echanges_par_arete_pour_TV_0_01": (cibles[0.01] / (m + k)) if cibles[0.01] is not None else None})
    return out


def main():
    rapide = "--rapide" in sys.argv
    res = {"cadre": {"beta": BETA, "tau": TAU, "poids": "exp(N*S_sim/tau)",
                     "hypothese": "H-abs : graphes abstraits, sans contrainte Rips"}}
    print("A. invariant M - N …"); res["A_invariant"] = partie_a(); print("  ", res["A_invariant"])
    print("B. secteur M = N - 1 …"); res["B_secteur_arbre"] = partie_b()
    for r in res["B_secteur_arbre"]:
        print("  ", r)
    print("C. obstruction généalogique …"); res["C_obstruction"] = partie_c()
    for r in res["C_obstruction"]:
        print("  ", r)
    cas = ((4, 5, 2), (5, 8, 3)) if rapide else ((4, 5, 2), (5, 8, 3), (6, 11, 3))
    print("D. croissance puis relaxation …"); res["D_relaxation"] = partie_d(cas)
    for r in res["D_relaxation"]:
        print("  ", r)
    (ICI / ("resultats_rapide.json" if rapide else "resultats.json")).write_text(
        json.dumps(res, ensure_ascii=False, indent=1))
    print("écrit :", "resultats_rapide.json" if rapide else "resultats.json")


if __name__ == "__main__":
    main()
