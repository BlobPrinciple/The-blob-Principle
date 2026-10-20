#!/usr/bin/env python3
"""DEFI-M11 — part de la moyenne d'équilibre de T_v portée par les sommets ayant plus de 6 triangles.

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026. Un nouveau-né à k = 4 arêtes
a au plus C(4, 2) = 6 triangles à la naissance ; cette part mesure ce qu'aucune loi
d'attachement à k = 4 ne peut lui donner d'emblée. Chaîne de Metropolis sur pi_{N+1, M+k}
(moteur de defi_m11_monte_carlo.py), M + k = 2(N + 1).
Usage : python3 defi_m11_queue_aristocratique.py -> defi_m11_queue_aristocratique.json
"""
import json
import pathlib

import numpy as np

import defi_m11_monte_carlo as mc

ICI = pathlib.Path(__file__).resolve().parent


def main():
    out = []
    for n in (8, 16, 24, 32, 48, 64):
        n1, m1 = n + 1, 2 * (n + 1)
        rng = np.random.default_rng(5 + n)
        mc.graine_numba(5 + n)
        adj, ar = mc.graphe_aleatoire(n1, m1, rng)
        deg, etat = mc.etat_de(adj)
        mc.balayer(adj, ar, deg, etat, n1, 500 * m1)
        tv = []
        for _ in range(2000):
            mc.balayer(adj, ar, deg, etat, n1, 5 * m1)
            tv.extend(mc.tri_sommet(adj, n1, v) for v in range(n1))
        tv = np.array(tv, float)
        part = float(tv[tv > 6].sum() / tv.sum())
        frac = float((tv > 6).mean())
        out.append({"N_plus_1": n1, "moyenne_T_v": float(tv.mean()), "part_de_la_moyenne_portee_par_T_v_sup_6": part,
                    "fraction_de_sommets_T_v_sup_6": frac})
        print(n1, round(tv.mean(), 2), "part", round(part, 3), "sommets", round(frac, 3), flush=True)
    (ICI / "defi_m11_queue_aristocratique.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
