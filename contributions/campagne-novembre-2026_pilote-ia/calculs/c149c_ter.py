#!/usr/bin/env python3
"""C-149c ter -- COMPLEMENT APRES COUP (declare) : les cellules de l'etat flambe sont-elles retournees ou ecrasees ?
Cellules = groupes de quatre porteurs tous lies (C-135c). Etat flambe recalcule (n = 4, graine 1490), comme dans c149c_bis.py."""
import itertools, json, math
import numpy as np, scipy.optimize as so
from c149c import classes_de_palier, reseau
cl = classes_de_palier(); n = 4; a = (3 + 3 * math.sqrt(2) + math.sqrt(3)) / 12
N, I, J, D = reseau(n, classes=cl); rng = np.random.default_rng(1490)
def Fm(h): return np.array([[h[0], h[3], h[4]], [h[3], h[1], h[5]], [h[4], h[5], h[2]]])
def fun(z):
    U = z[:3 * N].reshape(-1, 3); F = Fm(z[3 * N:])
    B = D @ F.T + U[J] - U[I]; L = np.linalg.norm(B, axis=1); f = L - 1; w = (f / L)[:, None] * B
    G = np.zeros_like(U); np.add.at(G, J, w); np.add.at(G, I, -w); GF = np.einsum('ea,eb->ab', w, D)
    return 0.5 * (f ** 2).sum(), np.concatenate([G.ravel(), [GF[0, 0], GF[1, 1], GF[2, 2], GF[0, 1] + GF[1, 0], GF[0, 2] + GF[2, 0], GF[1, 2] + GF[2, 1]]])
r = so.minimize(fun, np.concatenate([0.05 * rng.standard_normal(3 * N), [a, a, a, 0, 0, 0]]), jac=True, method='L-BFGS-B', options=dict(gtol=1e-12, ftol=1e-17, maxiter=200000, maxfun=400000, maxcor=40))
U = r.x[:3 * N].reshape(-1, 3); F = Fm(r.x[3 * N:])
idx = lambda p: (p[0] % n) * n * n + (p[1] % n) * n + (p[2] % n)
cells = set()
for p in itertools.product(range(n), repeat=3):
    Dp = sorted(cl[tuple(q % 2 for q in p)])
    for d1, d2, d3 in itertools.combinations(Dp, 3):
        q1, q2, q3 = (tuple(p[i] + d[i] for i in range(3)) for d in (d1, d2, d3))
        lie = lambda u, v: tuple(v[i] - u[i] for i in range(3)) in cl[tuple(c % 2 for c in u)]
        if lie(q1, q2) and lie(q1, q3) and lie(q2, q3):
            # forme canonique : translater pour que le plus petit sommet soit dans la boite
            S = sorted([p, q1, q2, q3]); o = tuple((S[0][i] // n) * n for i in range(3))
            cells.add(tuple(tuple(s[i] - o[i] for i in range(3)) for s in S))
def vol(c, flambe):
    X = [np.array(s, float) @ (F.T if flambe else a * np.eye(3)) + (U[idx(s)] if flambe else 0) for s in c]
    return np.dot(X[1] - X[0], np.cross(X[2] - X[0], X[3] - X[0])) / 6
v0 = np.array([vol(c, False) for c in cells]); v1 = np.array([vol(c, True) for c in cells]); rap = v1 / v0
out = dict(E_par_porteur=float(r.fun / N), cellules=len(cells), cellules_par_porteur=len(cells) / N, volume_regulier_min=float(abs(v0).min()), volume_regulier_max=float(abs(v0).max()),
           somme_volumes_reguliers_par_porteur=float(abs(v0).sum() / N), a_cube=a ** 3,
           retournees=int((rap <= 0).sum()), rapport_min=float(rap.min()), rapport_max=float(rap.max()), rapport_median=float(np.median(rap)),
           sous_20_pour_cent=int((rap < 0.2).sum()), somme_volumes_flambes_par_porteur=float(abs(v1).sum() / N), det_F=float(np.linalg.det(F)))
json.dump(out, open('c149c_ter.json', 'w'), indent=1); print(json.dumps(out, indent=1))
