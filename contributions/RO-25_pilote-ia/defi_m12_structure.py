#!/usr/bin/env python3
"""DEFI-M12 — anatomie de l'aristocratie à l'équilibre (réglage c2 : M = 2n, lam = n / tau).

Pilote IA du laboratoire (Claude, Anthropic), 27 octobre 2026.
Instantanés d'équilibre (moteur de defi_m12_lenteur.py, rodage de 400 balayages au moins et
au moins 10 fois Delta·20) : plus grande clique (networkx), plus grand k-cœur non vide
(k_max et sa taille), T_v maximal, part des triangles portée par les sommets de la plus
grande clique. Sert à tester une lecture [H] : la barrière croît comme la taille du noyau.
Usage : python3 defi_m12_structure.py -> defi_m12_structure.json
"""
import json
import pathlib

import networkx as nx
import numpy as np

import defi_m12_lenteur as L

ICI = pathlib.Path(__file__).resolve().parent


def main():
    out = []
    for n in (17, 25, 33, 49, 65, 97, 129, 193):
        m = 2 * n
        lam = n / L.TAU
        delta = L.delta_pour(n, "c2")
        rng = np.random.default_rng(99 + n)
        L.graine_numba(99 + n)
        adj, ar, deg, etat = L.depart(n, m, rng, False)
        L.balayer(adj, ar, deg, etat, n, max(400, 200 * delta) * m, lam)
        lignes = []
        tv = np.zeros(n, dtype=np.int64)
        for s in range(40):
            L.balayer(adj, ar, deg, etat, n, max(1, delta * 20) * m, lam)
            G = nx.from_numpy_array(adj.astype(int))
            cl = max(nx.find_cliques(G), key=len)
            core = nx.core_number(G)
            kmax = max(core.values())
            L.tri_tous(adj, n, tv)
            lignes.append((len(cl), kmax, sum(1 for v in core.values() if v == kmax), int(tv.max()),
                           float(sum(tv[v] for v in cl) / tv.sum())))
        a = np.array(lignes, float)
        r = {"n": n, "clique_max": float(a[:, 0].mean()), "k_max": float(a[:, 1].mean()),
             "taille_k_coeur": float(a[:, 2].mean()), "Tv_max": float(a[:, 3].mean()),
             "part_Tv_clique": float(a[:, 4].mean()), "T_dernier_instantane": float(etat[0])}
        out.append(r)
        print({k: round(v, 2) for k, v in r.items()}, flush=True)
    ns = np.array([r["n"] for r in out], float)
    exposants = {}
    for cle in ("clique_max", "taille_k_coeur", "Tv_max"):
        y = np.array([r[cle] for r in out])
        a = np.polyfit(np.log(ns[2:]), np.log(y[2:]), 1)[0]
        print("exposant de", cle, "(n ≥ 33) :", round(a, 2))
        exposants[cle] = float(a)
    (ICI / "defi_m12_structure.json").write_text(json.dumps({"instantanes": out, "exposants_n_ge_33": exposants},
                                                            ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
