#!/usr/bin/env python3
"""Suite du contrôle des pages 917-919 : la lecture « au plateau » en fonction de kappa_0, substrat de dimension 3.
Moteur de l'auteur inchangé (build_initial, run_mcmc_canonical) ; mesure identique à controle_p917-919_blob.py.
Usage : controle_p917-919_kappa.py "<chemin de gap curl colab.py>"
"""
import sys
import numpy as np
import scipy.sparse as sp

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical, count_triangles = (espace[k] for k in ('build_initial', 'run_mcmc_canonical', 'count_triangles'))
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
    return ds.max(), best[1], best[2]
N = 600
for kappa in (4.0, 5.0, 6.0, 6.6, 7.0, 8.0, 10.0):
    P = {'depart': [], 'blob': []}; M = {'depart': [], 'blob': []}; T = {'depart': [], 'blob': []}; TP = []
    for seed in (1, 2, 3):
        pts, adj0, pool, E0 = build_initial(N, seed, kappa)
        adjB = run_mcmc_canonical(pts, adj0, pool, N, E0, seed)
        for nom, adj in (('depart', adj0), ('blob', adjB)):
            m, p, tp = lecture(adj, N); P[nom].append(p); M[nom].append(m); T[nom].append(count_triangles(adj, N))
            if nom == 'blob': TP.append(tp)
    print(f"kappa={kappa:>4} : plateau départ {np.mean(P['depart']):.2f} ± {np.std(P['depart']):.2f} ; Blob {np.mean(P['blob']):.2f} ± {np.std(P['blob']):.2f} (t={min(TP):.1f} à {max(TP):.1f}) ; "
          f"max {np.mean(M['depart']):.2f} -> {np.mean(M['blob']):.2f} ; triangles x{np.mean(T['blob'])/np.mean(T['depart']):.2f}")
