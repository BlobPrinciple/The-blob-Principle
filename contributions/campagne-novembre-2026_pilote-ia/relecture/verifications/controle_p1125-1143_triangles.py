#!/usr/bin/env python3
"""Contrôle du pilote pour les pages 1125, 1139 et 1142-1143 du master V346 : densité de triangles.
(1) Graphe géométrique 3D sans bord (cube périodique), degré moyen kappa : triangles par sommet, comparés à
    kappa^2 * (15/32) / 6 (chaque triangle compté une fois) et à kappa^2 * (15/32) / 2 (formule de LIT-2, p. 1143).
(2) Arithmétique sur les chiffres du master (p. 1111 et 1139) : tri/arête * kappa/2 = triangles par sommet ;
    fois 3 = triangles incidents à un sommet.
"""
import numpy as np
from math import pi
from scipy.spatial import cKDTree

def mesure(N, kappa, graine):
    rng = np.random.default_rng(graine)
    pts = rng.random((N, 3))
    r = (3 * kappa / (4 * pi * N)) ** (1 / 3)
    paires = cKDTree(pts, boxsize=1.0).query_pairs(r, output_type='ndarray')
    adj = [set() for _ in range(N)]
    for a, b in paires:
        adj[a].add(b); adj[b].add(a)
    tri = sum(len(adj[a] & adj[b]) for a, b in paires) // 3
    return 2 * len(paires) / N, tri / N

print("(1) Graphe géométrique 3D périodique, N = 20 000, trois graines")
for kappa in (6.6, 8.0):
    res = [mesure(20000, kappa, g) for g in (1, 2, 3)]
    deg = np.mean([x[0] for x in res]); t = [x[1] for x in res]
    print(f"  kappa visé {kappa} ; degré moyen mesuré {deg:.3f} ; triangles par sommet {np.mean(t):.3f} ± {np.std(t, ddof=1):.3f} ; "
          f"kappa²·(15/32)/6 = {kappa**2*15/32/6:.3f} ; kappa²·(15/32)/2 = {kappa**2*15/32/2:.3f}")

print("(2) Chiffres du master")
print(f"  tri/arête 1,549 (p. 1111) × kappa/2 = 3,3  ->  {1.549*3.3:.3f} triangles par sommet ; × 3 = {1.549*3.3*3:.2f} triangles incidents par sommet (le master écrit 15,33)")
print(f"  « tri/sommet » de la page 1139, mesuré dans le conteneur : 5,09 ; rapport 15,33 / 5,09 = {15.33/5.09:.2f}")
