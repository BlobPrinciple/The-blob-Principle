#!/usr/bin/env python3
"""Témoin : nombre de triangles et de 4-cliques d'un graphe géométrique aléatoire dans le cube unité
(bords libres), N points uniformes, rayon r = (kappa0 / ((4 pi / 3) N))^(1/3).
Compare aux formules du livre annexe (Théorème 3.7 : N kappa0^2 K3 / 6, K3 = 15/32 ;
Théorème 4.2 : N kappa0^3 K4 / 24, K4 = 0,3798) et aux « null » de ses tableaux M-3.2 et M-4.1.
Usage : python3 -I temoin_triangles_rgg.py"""
import numpy as np
def compte(N, kappa0, graine):
    rng = np.random.default_rng(graine)
    X = rng.random((N, 3))
    r = (kappa0 / ((4 * np.pi / 3) * N)) ** (1 / 3)
    D2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
    A = (D2 <= r * r) & ~np.eye(N, dtype=bool)
    vois = [set(np.flatnonzero(A[i])) for i in range(N)]
    aretes = tri = k4 = 0
    for u in range(N):
        for v in vois[u]:
            if v <= u: continue
            aretes += 1
            commun = [w for w in vois[u] & vois[v]]
            tri += len(commun)                     # chaque triangle compté 3 fois (une par arête)
            c = set(commun)
            k4 += sum(len(vois[w] & c) for w in commun) // 2   # chaque 4-clique comptée 6 fois (une par arête)
    return aretes, tri // 3, k4 // 6
if __name__ == "__main__":
    for N in (300, 1000, 3000):
        for k in (8.0, 6.6):
            res = [compte(N, k, g) for g in range(5 if N < 3000 else 3)]
            e, t, q = (np.mean([x[i] for x in res]) for i in range(3))
            st, sq = np.std([x[1] for x in res]), np.std([x[2] for x in res])
            print(f"N={N:5d} kappa0={k:3.1f} : degré moyen {2*e/N:5.2f} ; triangles {t:7.0f} ± {st:4.0f} (formule {N*k*k*(15/32)/6:6.0f}) ; "
                  f"4-cliques {q:7.0f} ± {sq:4.0f} (formule {N*k**3*0.3798/24:6.0f})")
