#!/usr/bin/env python3
"""Contrôle du pilote pour la page 1053 du master V346 (Partie CIII, portes C et G, 7 juin).
Le master : « la preuve robuste de d = 3 reste la dégénérescence x3 du premier triplet » du laplacien de graphe
(rapports attendus pour le cube, conditions de Neumann : 1, 1, 1, 2, 2, 2, 3).
Question : ce triplet distingue-t-il le Blob de son graphe de départ, et que lit-on si les points sont posés
dans une boîte qui n'est pas un cube ? Moteur de l'auteur (gap curl colab.py), dynamique inchangée ; pour la boîte
allongée, seule la forme du domaine change (points uniformes dans [0;2]x[0;1]x[0;0,5], même volume).
Usage : controle_p1053_triplet.py "<chemin de gap curl colab.py>"
"""
import sys, math
import numpy as np
import scipy.sparse as sp
from scipy.spatial import KDTree

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical, lcc_size, E0_target, rips_radius = (espace[k] for k in ('build_initial', 'run_mcmc_canonical', 'lcc_size', 'E0_target', 'rips_radius'))

def rapports(adj, N):
    # plus grande composante connexe seulement (sinon plusieurs valeurs propres nulles faussent les rapports)
    vu = [-1] * N; comps = []
    for s0 in range(N):
        if vu[s0] < 0:
            c = [s0]; vu[s0] = len(comps); q = [s0]
            while q:
                x = q.pop()
                for y in adj[x]:
                    if vu[y] < 0: vu[y] = len(comps); c.append(y); q.append(y)
            comps.append(c)
    comp = max(comps, key=len); pos = {v: i for i, v in enumerate(comp)}; n = len(comp)
    lig = [pos[i] for i in comp for j in adj[i]]; col = [pos[j] for i in comp for j in adj[i]]
    A = sp.coo_matrix((np.ones(len(lig)), (lig, col)), shape=(n, n)).tocsr()
    d = np.asarray(A.sum(1)).ravel()
    lam = np.linalg.eigvalsh(np.diag(d) - A.toarray())[1:8]
    return f"(composante {n}/{N})  " + "  ".join(f"{x:.2f}" for x in lam / lam[0])

def depart_boite(N, seed, kappa, cotes, pool_mult=1.6):
    r = rips_radius(N, kappa); E0 = E0_target(N, kappa)       # volume de la boîte = 1, même rayon
    rng = np.random.default_rng(seed); pts = rng.uniform(0.0, 1.0, (N, 3)) * np.array(cotes)
    tree = KDTree(pts); adj = [set() for _ in range(N)]
    for i, j in tree.query_pairs(r): adj[i].add(j); adj[j].add(i)
    pool = list(tree.query_pairs(pool_mult * r)); rng2 = np.random.default_rng(seed + 50_000)
    K = sum(len(a) for a in adj) // 2; att = 0
    while K != E0 and att < 10 * abs(E0 - K) + 5000:
        att += 1
        if K < E0:
            u, v = pool[rng2.integers(len(pool))]
            if v not in adj[u]: adj[u].add(v); adj[v].add(u); K += 1
        else:
            edges = [(i, j) for i in range(N) for j in adj[i] if j > i]
            u, v = edges[rng2.integers(len(edges))]
            adj[u].discard(v); adj[v].discard(u)
            if lcc_size(adj, N) == N: K -= 1
            else: adj[u].add(v); adj[v].add(u)
    return pts, adj, pool, E0

print("rapports des sept premières valeurs propres non nulles à la première (cube de Neumann : 1 1 1 2 2 2 3)")
N = 1500
for seed in (1, 2):
    pts, adj0, pool, E0 = build_initial(N, seed, 6.6)
    print(f"cube, graine {seed}, départ : {rapports(adj0, N)}")
    print(f"cube, graine {seed}, Blob   : {rapports(run_mcmc_canonical(pts, adj0, pool, N, E0, seed), N)}")
pts, adj0, pool, E0 = depart_boite(N, 1, 6.6, (2.0, 1.0, 0.5))
print(f"boîte 2 x 1 x 0,5, départ : {rapports(adj0, N)}     (Neumann attendu : 1 4 4 5 8 9 13 ...)")
print(f"boîte 2 x 1 x 0,5, Blob   : {rapports(run_mcmc_canonical(pts, adj0, pool, N, E0, 1), N)}")
