#!/usr/bin/env python3
"""DEFI-M11 — carte exacte : naître juste ou relaxer vite, sur tous les secteurs à N + 1 ≤ 7.

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
Pour chaque secteur de départ (N, M), N = 4, 5, 6, M ≥ 1, et chaque k avec
2 ≤ k ≤ N − 1 (k = 1 et k = N : une seule loi possible au sens de D1 ou une
seule partie), on compare les noyaux tempérés G_theta(A | C) ∝ pi'(C + v_A)^theta
(theta = −1, −0,5, 0 = uniforme, 0,5, 1 = Gibbs) :
  - TV à la naissance ;
  - nombre d'échanges de Metropolis pour TV ≤ 0,01 (propagation exacte).
Réutilise les fonctions exactes de defi_m8_attachement_gibbs.py (implémentation 1) ;
recoupement : defi_m11_carte_second_moteur.py (implémentation 2) pour N + 1 ≤ 6.

Usage : python3 defi_m11_carte_exacte.py [--nmax 6]  ->  defi_m11_carte.json
"""
import json
import math
import pathlib
import sys
import time

import numpy as np

import defi_m8_attachement_gibbs as m8

ICI = pathlib.Path(__file__).resolve().parent
THETAS = (-1.0, -0.5, 0.0, 0.5, 1.0)
EPS = 0.01
T_MAX = 50000


def cas(n, m, k):
    anc, P2 = m8.paires_ordonnees(n)
    La = len(anc)
    MA = m8.masques_secteur(La, m)
    S, _ = m8.s_sim_masques(n, anc, MA)
    pi = m8.gibbs(n, S)
    M2 = m8.masques_secteur(len(P2), m + k)
    S2, _ = m8.s_sim_masques(n + 1, P2, M2)
    pi2 = m8.gibbs(n + 1, S2)
    restr = M2 & ((1 << La) - 1)
    degv = np.array([bin(int(x)).count("1") for x in (M2 >> La)])
    bon = degv == k
    i = np.searchsorted(MA, restr[bon])
    assert np.all(MA[i] == restr[bon])
    K = m8.noyau_echange(len(P2), M2, pi2).T.tocsr()
    sortie = {"N": n, "M": m, "k": k, "etats_apres": int(len(M2))}
    for th in THETAS:
        w = pi2[bon] ** th
        z = np.bincount(i, weights=w, minlength=len(MA))
        x = np.zeros(len(M2))
        x[bon] = pi[i] * w / z[i]
        tv0 = m8.tv(x, pi2)
        t01 = None
        for t in range(T_MAX + 1):
            if m8.tv(x, pi2) <= EPS:
                t01 = t
                break
            x = K @ x
        sortie[f"theta={th}"] = {"TV_naissance": tv0, "t_TV_0_01": t01}
    return sortie


def main():
    nmax = int(sys.argv[sys.argv.index("--nmax") + 1]) if "--nmax" in sys.argv else 6
    t0 = time.time()
    out = {"thetas": THETAS, "eps": EPS, "cadre": "H-abs, beta = 0,30, tau = 0,50", "cas": []}
    for n in range(4, nmax + 1):
        L2 = (n + 1) * n // 2
        for m in range(1, n * (n - 1) // 2 + 1):
            for k in range(2, n):
                if m + k > L2 - 1:  # secteur d'arrivée trivial (au plus un état sans non-arête)
                    continue
                r = cas(n, m, k)
                out["cas"].append(r)
                print(json.dumps(r, ensure_ascii=False), flush=True)
                (ICI / "defi_m11_carte.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    out["duree_s"] = round(time.time() - t0, 1)
    (ICI / "defi_m11_carte.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("écrit : defi_m11_carte.json", out["duree_s"], "s")


if __name__ == "__main__":
    main()
