#!/usr/bin/env python3
"""DEFI-M9 — recoupement du contrôle « deux chaînes » par la seconde implémentation
(defi_m9_second_moteur.py : matrice d'adjacence dense, sans le moteur du corpus).
Même protocole que defi_m9_deux_chaines.py : même nuage de points, départ A = paires les plus
courtes, départ B = paires du réservoir tirées au hasard, 120 N pas puis 4 096 balayages."""
import importlib.util, json, math, pathlib
import numpy as np
from scipy.spatial import cKDTree
ICI = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("m2", ICI / "defi_m9_second_moteur.py")
m2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m2)
T = 4096

def chaine(N, pool, edges, sd):
    A = np.zeros((N, N), np.bool_); A[edges[:, 0], edges[:, 1]] = True; A[edges[:, 1], edges[:, 0]] = True
    deg = A.sum(1).astype(np.int64); iu, iv = np.nonzero(np.triu(A)); iu = iu.astype(np.int64); iv = iv.astype(np.int64)
    pa, pb = pool[:, 0].copy(), pool[:, 1].copy(); mean = 2.0 * len(iu) / N
    m2.metropolis(A, deg, iu, iv, pa, pb, 120 * N, m2.BETA, m2.TAU / N, mean, sd)
    a0 = m2.masse(A)
    m2.metropolis(A, deg, iu, iv, pa, pb, T * len(iu), m2.BETA, m2.TAU / N, mean, sd + 1)
    return a0, m2.masse(A)

haut = lambda m: m >= np.quantile(m, 0.9)
out = []
for N, ng in [(500, 4)]:
    for g in range(ng):
        rng = np.random.default_rng(55_000 + g); pts = rng.random((N, 3))
        r = (m2.KAPPA / ((N - 1) * 4.0 / 3.0 * math.pi)) ** (1 / 3)
        pool = np.array(sorted(cKDTree(pts).query_pairs(m2.PF * r)), dtype=np.int64)
        L = np.linalg.norm(pts[pool[:, 0]] - pts[pool[:, 1]], axis=1); E0 = int(round(N * m2.KAPPA / 2))
        eA = pool[np.argsort(L, kind="stable")[:E0]]; eB = pool[rng.choice(len(pool), E0, replace=False)]
        a0, aT = chaine(N, pool, eA, 3_000 + 10 * g); _, bT = chaine(N, pool, eB, 7_000 + 10 * g)
        hA0, hAT, hBT = haut(a0), haut(aT), haut(bT)
        row = {"N": N, "graine_positions": 55_000 + g, "persistance_A": round(float((hA0 & hAT).sum() / hA0.sum()), 4),
               "recouvrement_A_B": round(float((hAT & hBT).sum() / hAT.sum()), 4)}
        out.append(row); print(row, flush=True)
(ICI / "defi_m9_deux_chaines_second_moteur.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
