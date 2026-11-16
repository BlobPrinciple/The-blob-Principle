#!/usr/bin/env python3
"""C-185c -- ancrage sur une physique REELLE et connue (Claude, 16 novembre 2026) : amas de Lennard-Jones (interaction de paires des gaz rares), N = 4 a 13.
Aucun terme du Blob, aucune penalite sur le nombre de tetraedres : on minimise seulement V = somme 4 (r^-12 - r^-6) et on regarde quelles structures gagnent.
Reference : Cambridge Cluster Database (Wales, Doye et al.), table des minima globaux. Predictions : c185c_prediction.txt. Precalcul independant, fait avant de lire le C-185 de ChatGPT.
Usage : python3 c185c.py <N> -> c185c_<N>.json"""
import itertools, json, math, sys
import numpy as np, scipy.optimize as so

R0 = 2 ** (1 / 6); REF = {4: -6.0, 5: -9.103852, 6: -12.712062, 7: -16.505384, 8: -19.821489, 9: -24.113360, 10: -28.422532, 11: -32.765970, 12: -37.967600, 13: -44.326801}


def lj(z):
    X = z.reshape(-1, 3); n = len(X); iu = np.triu_indices(n, 1); d = X[iu[0]] - X[iu[1]]; r2 = (d * d).sum(1); i6 = 1 / r2 ** 3
    e = 4 * (i6 * i6 - i6).sum(); f = (-24 * (2 * i6 * i6 - i6) / r2)[:, None] * d; g = np.zeros_like(X); np.add.at(g, iu[0], f); np.add.at(g, iu[1], -f)
    return e, g.ravel()


def structure(X, seuil=1.3):
    n = len(X); D = np.linalg.norm(X[:, None] - X[None], axis=2); A = [set(j for j in range(n) if j != i and D[i, j] <= seuil * R0) for i in range(n)]
    B = [(i, j) for i in range(n) for j in A[i] if j > i]; T = [q for q in itertools.combinations(range(n), 4) if all(b in A[a] for a, b in itertools.combinations(q, 2))]
    tri = {}
    for q in T:
        for f in itertools.combinations(q, 3): tri[f] = tri.get(f, 0) + 1
    ne = {b: sum(1 for q in T if b[0] in q and b[1] in q) for b in B}
    ferme = [b for b in B if ne[b] >= 3 and all(tri[f] == 2 for f in tri if b[0] in f and b[1] in f)]
    L = np.array([D[i, j] for i, j in B]) / R0
    return dict(liens=len(B), tetraedres=len(T), n_e=sorted(ne.values()), liens_entoures=len(ferme), n_e_des_liens_entoures=sorted(ne[b] for b in ferme), longueurs_des_liens_entoures=sorted(float(D[b] / R0) for b in ferme),
                triangles_dans_plus_de_2_tetraedres=sum(1 for v in tri.values() if v > 2), longueur_min=float(L.min()), longueur_max=float(L.max()), longueur_moyenne=float(L.mean()),
                seconde_distance_min=float(min((D[i, j] for i in range(n) for j in range(i + 1, n) if j not in A[i]), default=float('nan')) / R0))


def cherche(N, departs=3000):
    rng = np.random.Generator(np.random.PCG64(185000 + N)); minima = {}
    for k in range(departs):
        z = rng.uniform(-1, 1, 3 * N) * (0.55 * N ** (1 / 3) * R0)
        r = so.minimize(lj, z, jac=True, method='L-BFGS-B', options=dict(maxiter=5000, gtol=1e-9, ftol=1e-15))
        if not np.isfinite(r.fun) or r.fun > -1: continue
        X = r.x.reshape(-1, 3); D = np.linalg.norm(X[:, None] - X[None], axis=2)
        if D.max() > 4 * N ** (1 / 3): continue   # amas eclate
        r = so.minimize(lj, r.x, jac=True, method='BFGS', options=dict(gtol=1e-10, maxiter=5000)); key = round(float(r.fun), 4)
        if key not in minima: minima[key] = [0, r.x.copy(), float(np.abs(r.jac).max())]
        minima[key][0] += 1
    return minima


if __name__ == '__main__':
    N = int(sys.argv[1]); m = cherche(N, 3000 if N <= 9 else 6000); E = sorted(m); z = m[E[0]][1]; X = z.reshape(-1, 3)
    # hessien numerique du minimum global : minimum vrai ? (6 modes nuls attendus)
    h = 1e-5; Hs = np.array([(lj(z + h * e)[1] - lj(z - h * e)[1]) / (2 * h) for e in np.eye(3 * N)]); w = np.linalg.eigvalsh((Hs + Hs.T) / 2)
    out = dict(N=N, energie=float(lj(z)[0]), reference=REF[N], ecart=float(lj(z)[0] - REF[N]), gradient=m[E[0]][2], vp_negatives=int((w < -1e-4).sum()), modes_nuls=int((abs(w) < 1e-4).sum()), minima_distincts=len(E),
               energies_des_minima=[[e, m[e][0]] for e in E[:8]], structure=structure(X), positions=X.tolist())
    json.dump(out, open(f'c185c_{N}.json', 'w')); s = out['structure']
    print(N, 'E %.6f' % out['energie'], 'ecart %.1e' % out['ecart'], 'minima', len(E), [e for e in E[:4]], 'liens', s['liens'], 'tetra', s['tetraedres'], 'entoures', s['liens_entoures'], s['n_e_des_liens_entoures'], ['%.4f' % x for x in s['longueurs_des_liens_entoures'][:3]],
          'tri>2', s['triangles_dans_plus_de_2_tetraedres'], 'L %.4f-%.4f' % (s['longueur_min'], s['longueur_max']), '2e %.3f' % s['seconde_distance_min'], 'vp-', out['vp_negatives'], 'nuls', out['modes_nuls'], flush=True)
