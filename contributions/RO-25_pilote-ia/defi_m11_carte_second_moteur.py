#!/usr/bin/env python3
"""DEFI-M11 — recoupement de la carte exacte par l'implémentation 2 (networkx, matrices denses).

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
Mêmes cas que defi_m11_carte_exacte.py pour N = 4 et 5 (N + 1 ≤ 6), sans code commun
avec l'implémentation 1 : fonctions de defi_m8_second_moteur.py.

Usage : python3 defi_m11_carte_second_moteur.py  ->  defi_m11_carte_second_moteur.json
"""
import itertools
import json
import pathlib

import numpy as np

import defi_m8_second_moteur as s2

ICI = pathlib.Path(__file__).resolve().parent
THETAS = (-1.0, -0.5, 0.0, 0.5, 1.0)


def main():
    out = []
    for n in (4, 5):
        L2 = (n + 1) * n // 2
        for m in range(1, n * (n - 1) // 2 + 1):
            for k in range(2, n):
                if m + k > L2 - 1:
                    continue
                pi = s2.mesure(n, m)
                pi2 = s2.mesure(n + 1, m + k)
                etats, K = s2.noyau(n + 1, pi2)
                p = np.array([pi2[e] for e in etats])
                idx = {e: i for i, e in enumerate(etats)}
                choix = list(itertools.combinations(range(n), k))
                ligne = {"N": n, "M": m, "k": k}
                for th in THETAS:
                    x = np.zeros(len(etats))
                    for c, w in pi.items():
                        enfants = [c | frozenset((a, n) for a in A) for A in choix]
                        poids = [pi2[e] ** th for e in enfants]
                        z = sum(poids)
                        for e, q in zip(enfants, poids):
                            x[idx[e]] += w * q / z
                    tv0 = 0.5 * np.abs(x - p).sum()
                    t01 = None
                    for t in range(50001):
                        if 0.5 * np.abs(x - p).sum() <= 0.01:
                            t01 = t
                            break
                        x = x @ K
                    ligne[f"theta={th}"] = {"TV_naissance": tv0, "t_TV_0_01": t01}
                out.append(ligne)
                print(json.dumps(ligne), flush=True)
    (ICI / "defi_m11_carte_second_moteur.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
