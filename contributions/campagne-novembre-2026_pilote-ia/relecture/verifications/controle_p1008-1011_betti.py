#!/usr/bin/env python3
"""Contrôle du pilote pour les pages 1008-1011 du master V346 (Partie XC, 6 juin) : premier nombre de Betti du complexe de cliques.
Le master compare le Blob à un graphe d'Erdős–Rényi de même densité (« la viabilité supprime les boucles d'un facteur 5,9 »).
Question : et par rapport au graphe géométrique de départ, sans dynamique ? Moteur de l'auteur (gap curl colab.py), inchangé.
b1 = E - V + b0 - rang sur GF(2) de la matrice de bord triangles -> arêtes.
Usage : controle_p1008-1011_betti.py "<chemin de gap curl colab.py>"
"""
import sys
import numpy as np

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical, lcc_size = espace['build_initial'], espace['run_mcmc_canonical'], espace['lcc_size']

def betti1(adj, N):
    idx = {}; 
    for i in range(N):
        for j in adj[i]:
            if j > i: idx[(i, j)] = len(idx)
    E = len(idx); lignes = []
    for (i, j) in idx:
        for k in adj[i] & adj[j]:
            if k > j: lignes.append((1 << idx[(i, j)]) | (1 << idx[(j, k)]) | (1 << idx[(i, k)]))
    pivots = {}; rang = 0
    for r in lignes:
        while r:
            h = r.bit_length() - 1
            if h in pivots: r ^= pivots[h]
            else: pivots[h] = r; rang += 1; break
    # composantes
    vu = [False] * N; b0 = 0
    for s in range(N):
        if not vu[s]:
            b0 += 1; q = [s]; vu[s] = True
            while q:
                x = q.pop()
                for y in adj[x]:
                    if not vu[y]: vu[y] = True; q.append(y)
    return E - N + b0 - rang, E, len(lignes)

rng = np.random.default_rng(11)
for N in (600, 1000):
    for seed in (1, 2):
        pts, adj0, pool, E0 = build_initial(N, seed, 6.6)
        adjB = run_mcmc_canonical(pts, adj0, pool, N, E0, seed)
        er = [set() for _ in range(N)]; m = 0
        while m < E0:
            a, b = int(rng.integers(N)), int(rng.integers(N))
            if a != b and b not in er[a]: er[a].add(b); er[b].add(a); m += 1
        out = []
        for nom, adj in (("départ", adj0), ("Blob", adjB), ("Erdős–Rényi", er)):
            b1, E, T = betti1(adj, N); out.append(f"{nom} : b1 = {b1:>5}, b1/E = {b1/E:.3f}, triangles {T}")
        print(f"N={N} graine {seed} | " + " | ".join(out))
