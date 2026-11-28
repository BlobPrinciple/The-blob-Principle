#!/usr/bin/env python3
"""Suite du contrôle des pages 917-919 : la lecture « au plateau » suit-elle le substrat ou la fonctionnelle ?

Même dynamique (run_mcmc_canonical de l'auteur, inchangée) lancée sur des points uniformes en dimension 2, 3 et 4.
Seule la construction du graphe de départ est généralisée : rayon r = (kappa / ((N-1) V_d))^(1/d), V_d volume de la
boule unité ; réservoir à 1,6 r ; ajustement à E0 = N kappa / 2 arêtes par la même procédure que build_initial.
Mesure : identique à controle_p917-919_blob.py (fenêtre d'un facteur 2 en t, variance minimale, t entre 3 et 30).
Usage : controle_p917-919_substrat.py "<chemin de gap curl colab.py>"
"""
import sys, math
import numpy as np
import scipy.sparse as sp
from scipy.spatial import KDTree

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
run_mcmc_canonical, count_triangles, lcc_size, E0_target = (espace[k] for k in ('run_mcmc_canonical', 'count_triangles', 'lcc_size', 'E0_target'))
VOL = {2: math.pi, 3: 4 * math.pi / 3, 4: math.pi ** 2 / 2}

def depart(N, seed, kappa, dim, pool_mult=1.6):
    r = (kappa / ((N - 1) * VOL[dim])) ** (1 / dim); E0 = E0_target(N, kappa)
    rng = np.random.default_rng(seed); pts = rng.uniform(0.0, 1.0, (N, dim))
    tree = KDTree(pts); adj = [set() for _ in range(N)]
    for i, j in tree.query_pairs(r): adj[i].add(j); adj[j].add(i)
    pool = list(tree.query_pairs(pool_mult * r)); rng2 = np.random.default_rng(seed + 50_000)
    K = sum(len(a) for a in adj) // 2; att = 0; max_att = 10 * abs(E0 - K) + 5000
    while K != E0 and att < max_att:
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

TS = np.logspace(-1, 3, 801)
def lecture(adj, N):
    lig = [i for i in range(N) for j in adj[i]]; col = [j for i in range(N) for j in adj[i]]
    A = sp.coo_matrix((np.ones(len(lig)), (lig, col)), shape=(N, N)).tocsr()
    d = np.asarray(A.sum(1)).ravel(); Dm = sp.diags(1 / np.sqrt(np.maximum(d, 1)))
    lam = np.clip(np.linalg.eigvalsh(np.eye(N) - (Dm @ A @ Dm).toarray()), 0, None)
    W = np.exp(-np.outer(TS, lam)); ds = 2 * TS * (W * lam).sum(1) / W.sum(1)
    w = int(round(np.log10(2.0) * 200)); best = None
    for i in range(len(TS) - w):
        if TS[i] < 3 or TS[i + w] > 30: continue
        v = ds[i:i + w + 1].var()
        if best is None or v < best[0]: best = (v, ds[i:i + w + 1].mean(), TS[i])
    return ds.max(), best[1], best[2], d.std() / d.mean(), lcc_size(adj, N)

for dim in (2, 3, 4):
    for N in (600, 1000):
        P = {'depart': [], 'blob': []}; M = {'depart': [], 'blob': []}; T = {'depart': [], 'blob': []}
        for seed in (1, 2, 3):
            pts, adj0, pool, E0 = depart(N, seed, 6.6, dim)
            adjB = run_mcmc_canonical(pts, adj0, pool, N, E0, seed)
            for nom, adj in (('depart', adj0), ('blob', adjB)):
                m, p, tp, D, lc = lecture(adj, N)
                P[nom].append(p); M[nom].append(m); T[nom].append(count_triangles(adj, N))
                print(f"dim {dim} N={N:>4} graine {seed} {nom:<6} composante={lc:>4} tri={T[nom][-1]:>5} D={D:.2f} max={m:.2f} plateau={p:.2f} (t={tp:.1f})")
        print(f"  => substrat de dimension {dim}, N={N} : départ {np.mean(P['depart']):.2f} ± {np.std(P['depart']):.2f} ; Blob {np.mean(P['blob']):.2f} ± {np.std(P['blob']):.2f} ; "
              f"max {np.mean(M['depart']):.2f} -> {np.mean(M['blob']):.2f} ; triangles x{np.mean(T['blob'])/np.mean(T['depart']):.2f}")
