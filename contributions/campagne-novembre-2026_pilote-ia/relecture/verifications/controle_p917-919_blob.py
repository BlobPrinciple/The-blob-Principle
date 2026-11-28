#!/usr/bin/env python3
"""Contrôle du pilote pour les pages 917-919 du master V346 (« d_s ≈ 3 au plateau localisé », 28 mai).

Moteur : celui de l'auteur, tel qu'il est consigné dans le dépôt
(corpus/03_scripts/.../gap curl colab.py : build_initial, run_mcmc_canonical, BETA=0,30, TAU=0,50,
BURN_F=50, PROD_F=80, kappa=6,6). Seules ses définitions sont chargées ; rien n'y est modifié.
Mesure : la mienne (voir controle_p896-920.py) : d_s(t) = -2 d ln Tr exp(-tL) / d ln t, laplacien normalisé,
spectre complet ; « plateau » = fenêtre de largeur un facteur 2 en t, de variance minimale, dans t entre 3 et 30.
Le script heat-kernel du master (test_heat_plateau.py) n'est pas dans le dépôt : ses choix de fenêtre me sont inconnus.
Question posée : la même lecture, appliquée au graphe de départ (témoin) et au Blob après la dynamique, donne quoi ?
Usage : controle_p917-919_blob.py "<chemin de gap curl colab.py>"
"""
import sys, math
import numpy as np
import scipy.sparse as sp

src = open(sys.argv[1], encoding='utf-8').read()
moteur = src[:src.index('# --------------------- GAP CURL DE HODGE')]
espace = {}
exec(compile(moteur, 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical, count_triangles = espace['build_initial'], espace['run_mcmc_canonical'], espace['count_triangles']

TS = np.logspace(-1, 3, 801)
REPERES = [3, 5, 8, 12, 20, 30]

def lecture(adj, N):
    lig = [i for i in range(N) for j in adj[i]]; col = [j for i in range(N) for j in adj[i]]
    A = sp.coo_matrix((np.ones(len(lig)), (lig, col)), shape=(N, N)).tocsr()
    d = np.asarray(A.sum(1)).ravel()
    Dm = sp.diags(1 / np.sqrt(np.maximum(d, 1)))
    lam = np.clip(np.linalg.eigvalsh(np.eye(N) - (Dm @ A @ Dm).toarray()), 0, None)
    W = np.exp(-np.outer(TS, lam)); ds = 2 * TS * (W * lam).sum(1) / W.sum(1)
    w = int(round(np.log10(2.0) * 200)); best = None
    for i in range(len(TS) - w):
        if TS[i] < 3 or TS[i + w] > 30: continue
        v = ds[i:i + w + 1].var()
        if best is None or v < best[0]: best = (v, ds[i:i + w + 1].mean(), TS[i])
    rep = "  ".join(f"{ds[np.argmin(abs(TS - t))]:.2f}" for t in REPERES)
    return ds.max(), TS[ds.argmax()], rep, best[1], best[2], d.std() / d.mean()

print("repères t =", REPERES)
for N in (400, 600, 800, 1000):
    pl = {'depart': [], 'blob': []}; mx = {'depart': [], 'blob': []}
    for seed in (1, 2, 3):
        pts, adj0, pool, E0 = build_initial(N, seed, 6.6)
        adjB = run_mcmc_canonical(pts, adj0, pool, N, E0, seed)
        for nom, adj in (('depart', adj0), ('blob', adjB)):
            m, tm, rep, p, tp, D = lecture(adj, N)
            pl[nom].append(p); mx[nom].append(m)
            print(f"N={N:>4} graine {seed} {nom:<6} tri={count_triangles(adj, N):>5} D={D:.2f}  max={m:.2f} (t={tm:.1f})  d_s(t)= {rep}  plateau={p:.2f} (t={tp:.1f})")
    print(f"  -> N={N} : plateau départ {np.mean(pl['depart']):.2f} ± {np.std(pl['depart']):.2f} ; Blob {np.mean(pl['blob']):.2f} ± {np.std(pl['blob']):.2f} ; max départ {np.mean(mx['depart']):.2f} ; max Blob {np.mean(mx['blob']):.2f}")
