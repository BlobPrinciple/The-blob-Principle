#!/usr/bin/env python3
"""DEFI-M8 — famille tempérée G_theta de part et d'autre de l'uniforme (theta = 0), jusqu'à G* (theta = 1).

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
G_theta(A | C) ∝ pi_{N+1,M+k}(C + v_A)^theta. Mesure exacte de la TV à la naissance
et du nombre d'échanges de Metropolis pour TV <= 0,01. Réutilise les fonctions de
defi_m8_attachement_gibbs.py (implémentation 1) ; le recoupement est fait par
defi_m8_second_moteur.py --tempere (implémentation 2).

Usage : python3 defi_m8_tempere.py   ->  defi_m8_tempere.json
"""
import json
import pathlib

import numpy as np

import defi_m8_attachement_gibbs as m8

ICI = pathlib.Path(__file__).resolve().parent
THETAS = (-0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0)


def lois_temperees(n, m, k):
    r, (P2, M2, pi2, nu_U, nu_G) = m8.cas_naissance(n, m, k)
    La = n * (n - 1) // 2
    restr = M2 & ((1 << La) - 1)
    degv = np.array([bin(int(x)).count("1") for x in (M2 >> La)])
    bon = degv == k
    MA = m8.masques_secteur(La, m)
    S, _ = m8.s_sim_masques(n, [p for p in P2 if p[1] < n], MA)
    pi = m8.gibbs(n, S)
    i = np.searchsorted(MA, restr[bon])
    lois = {}
    for th in THETAS:
        w = pi2[bon] ** th
        z = np.bincount(i, weights=w, minlength=len(MA))
        nu = np.zeros(len(M2))
        nu[bon] = pi[i] * w / z[i]
        lois[th] = nu
    assert np.allclose(lois[0.0], nu_U) and np.allclose(lois[1.0], nu_G)
    return P2, M2, pi2, lois


def main():
    out = []
    for n, m, k in [(4, 3, 3), (4, 4, 3), (5, 5, 4), (5, 7, 4), (6, 9, 4), (6, 11, 3)]:
        P2, M2, pi2, lois = lois_temperees(n, m, k)
        K = m8.noyau_echange(len(P2), M2, pi2).T.tocsr()
        ligne = {"N": n, "M": m, "k": k}
        for th, nu in lois.items():
            x, t01 = nu.copy(), None
            tv0 = m8.tv(nu, pi2)
            for t in range(4001):
                if m8.tv(x, pi2) <= 0.01:
                    t01 = t
                    break
                x = K @ x
            ligne[f"theta={th}"] = {"TV_naissance": tv0, "t_TV_0_01": t01}
        out.append(ligne)
        print(ligne, flush=True)
    (ICI / "defi_m8_tempere.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
