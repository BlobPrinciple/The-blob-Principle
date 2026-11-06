#!/usr/bin/env python3
"""DEFI-M14 — temps de séjour dans l'aristocratie à n = 225, 257 et 289 (et contrôle à n = 193).

Pilote IA du laboratoire (Claude, Anthropic), 6 novembre 2026.
Cadre de DEFI-M12 et DEFI-M13 : graphes abstraits étiquetés, M = 2n (degré moyen 4),
pi ∝ exp(lam · S_sim), lam = n / tau (mesure de l'armature), beta = 0,30, tau = 0,50,
échanges de Metropolis à |E| fixé (une arête, une non-arête, proposition uniforme).

Grandeur mesurée : celle de defi_m13_sorties.py, inchangée. Tous les Delta balayages,
T_v de tous les sommets ; un sommet devient « aristocrate » quand T_v ≥ T_haut, « roturier »
quand T_v ≤ T_bas = 2, et garde son état entre les deux (hystérésis) ; T_haut = moitié du
T du minimum aristocratique du profil de DEFI-M13 (n = 257 : t_ari = 136 et 135, moyenne
arrondie 136, T_haut = 68 ; n = 225 : interpolé, voir T_ARI). Séjour moyen = temps total
passé aristocrate (sommets × balayages) / nombre de sorties aristocrate → roturier.
Delta = t½ prévu par la loi de DEFI-M12 / 40, comme dans DEFI-M13.
En plus : autocorrélation poolée de T_v (tous les sommets, moyenne commune) et son t½.

Deux moteurs sans code commun pour le noyau :
  A : noyau de defi_m12_lenteur.balayer (matrice booléenne, générateur numba), départ
      « noyau planté » de defi_m12_lenteur.depart ;
  B : noyau de defi_m12_second_moteur.avancer_compte (mots de 64 bits, popcount, PCG64),
      départ planté construit ici, T_v par la diagonale de A³, autocorrélation par somme
      directe, sans FFT.
Les chaînes écrivent un état partiel tous les 25 enregistrements (reprise après coupure
non prévue : on relance la chaîne entière ; le partiel sert de témoin).

Usage : python3 defi_m14_sejour.py --moteur A|B --points 257:1,257:2 [--balayages 2e7]
        [--rodage 1e6] [--delta-facteur 1] [--depart plante|aleatoire (B)] [--processus 2] --sortie defi_m14_sejour_A.json
        (point = n:graine)
"""
import json
import math
import pathlib
import sys
import time
from multiprocessing import Pool

import numpy as np

import defi_m12_lenteur as L
import defi_m12_second_moteur as S

ICI = pathlib.Path(__file__).resolve().parent
# T du minimum aristocratique (profils de DEFI-M13) ; 225 : interpolation linéaire 193 → 257
T_ARI = {193: 112, 257: 136}
T_ARI[225] = int(round(T_ARI[193] + (T_ARI[257] - T_ARI[193]) * (225 - 193) / (257 - 193)))
# 289 : extrapolation linéaire (même pente), aucun profil mesuré à cette taille
T_ARI[289] = int(round(T_ARI[257] + (T_ARI[257] - T_ARI[193]) * (289 - 257) / (257 - 193)))


def t_demi_m12(n):
    return math.exp(0.964 * math.sqrt(n) - 1.77)


class Compteur:
    def __init__(self, n, t_haut, t_bas, tv0):
        self.t_haut, self.t_bas = t_haut, t_bas
        self.etat = (tv0 >= t_haut).astype(np.int64)
        self.sorties = 0
        self.entrees = 0
        self.temps_ari = 0
        self.balayages = 0
        self.ari_trace = []
        self.sorties_trace = []

    def pas(self, tv, delta):
        nouveau = self.etat.copy()
        nouveau[tv >= self.t_haut] = 1
        nouveau[tv <= self.t_bas] = 0
        k = int(((self.etat == 1) & (nouveau == 0)).sum())
        self.sorties += k
        self.sorties_trace.append(k)
        self.entrees += int(((self.etat == 0) & (nouveau == 1)).sum())
        self.temps_ari += int(nouveau.sum()) * delta
        self.balayages += delta
        self.ari_trace.append(int(nouveau.sum()))
        self.etat = nouveau


def acf_fft(X):
    return L.acf_poolee(X)


def acf_directe(X, kmax):
    Y = X - X.mean()
    var = (Y * Y).mean()
    Lr = X.shape[0]
    C = np.empty(min(kmax, Lr))
    for k in range(len(C)):
        C[k] = (Y[: Lr - k] * Y[k:]).mean() / var
    return C


def seuil(C, s, delta):
    for i in range(1, len(C)):
        if C[i] <= s:
            c0, c1 = C[i - 1], C[i]
            return (i - 1 + ((c0 - s) / (c0 - c1) if c0 != c1 else 1.0)) * delta
    return None


def chaine_A(n, graine, nrec, delta, rodage, partiel):
    m = 2 * n
    lam = n / L.TAU
    rng = np.random.default_rng(graine)
    L.graine_numba(graine)
    adj, ar, deg, etat = L.depart(n, m, rng, True)
    L.balayer(adj, ar, deg, etat, n, rodage * m, lam)
    tv = np.zeros(n, dtype=np.int64)
    L.tri_tous(adj, n, tv)
    cpt = Compteur(n, max(3, T_ARI[n] // 2), 2, tv)
    X = np.zeros((nrec, n))
    for i in range(nrec):
        L.balayer(adj, ar, deg, etat, n, delta * m, lam)
        L.tri_tous(adj, n, tv)
        X[i] = tv
        cpt.pas(tv, delta)
        if (i + 1) % 25 == 0:
            partiel(cpt, i + 1)
    # contrôle exact en fin de chaîne
    A = adj.astype(np.int64)
    assert int(np.trace(A @ A @ A)) // 6 == int(etat[0]) == int(tv.sum()) // 3
    C = acf_fft(X)
    return cpt, X, C


def depart_B(n, M, g, plante=True):
    """Départ planté construit indépendamment : clique de q sommets (q maximal avec
    q(q−1)/2 ≤ M), puis arêtes restantes tirées uniformément hors clique.
    plante=False : toutes les arêtes tirées uniformément (contrôle du départ)."""
    q = 1
    while (q + 1) * q // 2 <= M:
        q += 1
    if not plante:
        q = 0
    noyau = np.sort(g.choice(n, size=q, replace=False))
    pris = set()
    for i in range(q):
        for j in range(i + 1, q):
            pris.add((int(noyau[i]), int(noyau[j])))
    while len(pris) < M:
        a, b = sorted(int(x) for x in g.choice(n, size=2, replace=False))
        pris.add((a, b))
    return np.array(sorted(pris), dtype=np.int64), q


def chaine_B(n, graine, nrec, delta, rodage, partiel, plante=True):
    M = 2 * n
    lam = n / S.TA
    g = np.random.Generator(np.random.PCG64(graine))
    E, q = depart_B(n, M, g, plante)
    W = (n + 63) // 64
    bits = np.zeros((n, W), dtype=np.uint64)
    dg = np.zeros(n, dtype=np.int64)
    for a, b in E:
        S.poser(bits, a, b, True)
        S.poser(bits, b, a, True)
        dg[a] += 1
        dg[b] += 1

    def tv():
        A = np.zeros((n, n), dtype=np.int64)
        A[E[:, 0], E[:, 1]] = 1
        A[E[:, 1], E[:, 0]] = 1
        return np.diag(A @ A @ A) // 2

    t = tv()
    st = np.array([t.sum() / 3.0, float((dg ** 2).sum())])

    def faire(k):
        r = k
        while r > 0:
            lot = min(r, 4_000_000)
            U = g.random((lot + 4096, 4))
            r -= S.avancer_compte(bits, E, dg, st, n, lam, U, lot)

    faire(rodage * M)
    cpt = Compteur(n, max(3, T_ARI[n] // 2), 2, tv())
    X = np.zeros((nrec, n))
    for i in range(nrec):
        faire(delta * M)
        t = tv()
        assert abs(t.sum() / 3.0 - st[0]) < 1e-9
        X[i] = t
        cpt.pas(t, delta)
        if (i + 1) % 25 == 0:
            partiel(cpt, i + 1)
    assert st[1] == float((dg ** 2).sum())
    C = acf_directe(X, nrec)
    return cpt, X, C


def une(args):
    moteur, n, graine, balayages, rodage, dfac, sortie, plante = args
    delta = max(1, int(round(t_demi_m12(n) / 40 * dfac)))
    nrec = int(round(balayages / delta))
    nom = ICI / f"{sortie}.partiel_{moteur}_{n}_{graine}.json"

    def partiel(cpt, i):
        nom.write_text(json.dumps({"n": n, "graine": graine, "enregistrements_faits": i, "sorties": cpt.sorties,
                                   "temps_ari": cpt.temps_ari, "balayages": cpt.balayages}))

    t0 = time.time()
    if moteur == "A":
        cpt, X, C = chaine_A(n, graine, nrec, delta, rodage, partiel)
    else:
        cpt, X, C = chaine_B(n, graine, nrec, delta, rodage, partiel, plante)
    ari = np.array(cpt.ari_trace)
    sor = np.array(cpt.sorties_trace)
    # huit blocs consécutifs : séjour par bloc (barre d'erreur par blocs)
    blocs = [(int(b.sum()), int(a.sum()) * delta) for b, a in zip(np.array_split(sor, 8), np.array_split(ari, 8))]
    return {"moteur": moteur, "n": n, "graine": graine, "depart": "plante" if plante else "aleatoire", "delta": delta, "enregistrements": nrec,
            "rodage_balayages": rodage, "balayages": cpt.balayages, "t_haut": cpt.t_haut, "t_bas": cpt.t_bas,
            "sorties": cpt.sorties, "entrees": cpt.entrees,
            "aristocrates_moyen": cpt.temps_ari / cpt.balayages,
            "aristocrates_moitie1": float(ari[: len(ari) // 2].mean()), "aristocrates_moitie2": float(ari[len(ari) // 2:].mean()),
            "blocs_sorties_temps_ari": blocs,
            "sejour_balayages": cpt.temps_ari / cpt.sorties if cpt.sorties else None,
            "t_demi": seuil(C, 0.5, delta), "t_1e": seuil(C, math.exp(-1), delta), "C_debut": C[:120].tolist(),
            "Tv_max_moyen": float(X.max(1).mean()), "duree_s": time.time() - t0}


def main():
    def opt(nom, defaut):
        return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut
    moteur = opt("--moteur", "A")
    sortie = opt("--sortie", f"defi_m14_sejour_{moteur}.json")
    pts = [tuple(int(v) for v in p.split(":")) for p in opt("--points", "257:1,257:2").split(",")]
    bal = int(float(opt("--balayages", "2e7")))
    rod = int(float(opt("--rodage", "1e6")))
    dfac = float(opt("--delta-facteur", "1"))
    plante = opt("--depart", "plante") == "plante"
    assert plante or moteur == "B", "départ aléatoire : moteur B seulement"
    taches = [(moteur, n, g, bal, rod, dfac, sortie, plante) for n, g in pts]
    res = []
    with Pool(int(opt("--processus", "2"))) as p:
        for r in p.imap_unordered(une, taches):
            res.append(r)
            print(r["moteur"], r["n"], r["graine"], "sorties", r["sorties"], "entrées", r["entrees"],
                  "aristocrates", round(r["aristocrates_moyen"], 2),
                  "séjour", None if r["sejour_balayages"] is None else round(r["sejour_balayages"]),
                  "t½", None if r["t_demi"] is None else round(r["t_demi"]), "%.0f s" % r["duree_s"], flush=True)
            (ICI / sortie).write_text(json.dumps({"cadre": __doc__.split("Usage")[0], "chaines": res},
                                                 ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
