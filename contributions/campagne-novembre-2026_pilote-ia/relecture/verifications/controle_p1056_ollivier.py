#!/usr/bin/env python3
"""Contrôle du pilote pour la page 1056 du master V346 (Partie CIV, 7 juin) : « loi courbure <-> matière, forme d'Einstein ».
Le master : courbure d'Ollivier-Ricci (transport optimal exact, mesures uniformes sur les voisins, métrique de sol 0/1/2)
corrélée à la densité de matière locale à +0,72 (N = 500, kappa = 6,6, 120 arêtes par graine).
Question : la même corrélation existe-t-elle dans le graphe géométrique de départ, sans dynamique de viabilité ?
Moteur de l'auteur (gap curl colab.py), inchangé. « Matière » : trois lectures (triangles sur l'arête ; triangles incidents
aux deux extrémités, c'est-à-dire la « calcification » ; tétraèdres contenant l'arête).
Usage : controle_p1056_ollivier.py "<chemin de gap curl colab.py>"
"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical = espace['build_initial'], espace['run_mcmc_canonical']

def ollivier(adj, x, y):
    A = sorted(adj[x]); B = sorted(adj[y]); na, nb = len(A), len(B)
    c = np.array([[0.0 if u == v else (1.0 if v in adj[u] else 2.0) for v in B] for u in A]).ravel()
    Aeq = np.zeros((na + nb, na * nb))
    for i in range(na): Aeq[i, i * nb:(i + 1) * nb] = 1
    for j in range(nb): Aeq[na + j, j::nb] = 1
    beq = np.concatenate([np.full(na, 1 / na), np.full(nb, 1 / nb)])
    r = linprog(c, A_eq=Aeq, b_eq=beq, bounds=(0, None), method='highs')
    return 1.0 - r.fun

def mesure(nom, adj, N, rng):
    tri_s = np.array([sum(len(adj[i] & adj[j]) for j in adj[i]) / 2 for i in range(N)])     # triangles incidents à chaque sommet
    aretes = [(i, j) for i in range(N) for j in adj[i] if j > i and len(adj[i]) > 1 and len(adj[j]) > 1]
    choix = [aretes[k] for k in rng.choice(len(aretes), size=min(200, len(aretes)), replace=False)]
    K, T, C, Q = [], [], [], []
    for (x, y) in choix:
        K.append(ollivier(adj, x, y)); cn = adj[x] & adj[y]
        T.append(len(cn)); C.append(tri_s[x] + tri_s[y]); Q.append(sum(1 for a, b in itertools.combinations(cn, 2) if b in adj[a]))
    K = np.array(K)
    def r(v): return np.corrcoef(K, np.array(v, float))[0, 1]
    print(f"{nom:<20} courbure moyenne {K.mean():+.3f} ; corr(courbure, triangles sur l'arête) = {r(T):+.2f} ; "
          f"corr(courbure, calcification des extrémités) = {r(C):+.2f} ; corr(courbure, tétraèdres sur l'arête) = {r(Q):+.2f}")

rng = np.random.default_rng(5)
for seed in (1, 2, 3):
    pts, adj0, pool, E0 = build_initial(500, seed, 6.6)
    mesure(f"départ (graine {seed})", adj0, 500, rng)
    mesure(f"Blob (graine {seed})", run_mcmc_canonical(pts, adj0, pool, 500, E0, seed), 500, rng)
