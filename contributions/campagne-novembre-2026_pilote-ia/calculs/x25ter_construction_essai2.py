#!/usr/bin/env python3
"""X-25 ter, construction, essai 2 (objectif en produits inversifs, rayons bornes). Non concluant : voir x25ter_construction.out. A lancer depuis calculs/ : python3 x25ter_construction_essai2.py graine cible.     Claude, 23 novembre 2026."""
import sys, time, json, numpy as np
sys.path.insert(0, '.')
from scipy.optimize import minimize
import x25ter_construction as c
S = './'   # dossier de sortie des essais
graine, cible = int(sys.argv[1]), int(sys.argv[2])
X0, liens, emp = c.etat(graine, cible); P = c.Probleme(X0, liens); N = P.N
def energie_p(z, mu, m):
    X = z[:3 * N].reshape(N, 3); r = np.exp(z[3 * N:])
    def bloc(a, b, lien):
        D = X[a] - X[b]; d2 = (D * D).sum(1); ra, rb = r[a], r[b]
        p = (ra * ra + rb * rb - d2) / (2 * ra * rb)
        if lien: w = p + 1.0; act = slice(None); k = 1.0
        else:
            w = p + 1.0 + m; act = w > 0; k = mu
            if not act.any(): return 0.0, None
            a, b, D, d2, ra, rb, w = a[act], b[act], D[act], d2[act], ra[act], rb[act], w[act]
        e = k * (w * w).sum(); f = 2 * k * w
        gX = np.zeros((N, 3)); gr = np.zeros(N)
        cX = (-f / (ra * rb))[:, None] * D
        for q in range(3): gX[:, q] += np.bincount(a, cX[:, q], N) - np.bincount(b, cX[:, q], N)
        gr += np.bincount(a, f * (ra * ra - rb * rb + d2) / (2 * ra * rb), N) + np.bincount(b, f * (rb * rb - ra * ra + d2) / (2 * ra * rb), N)
        return e, (gX, gr)
    e1, g1 = bloc(P.I, P.J, True); e2, g2 = bloc(P.A, P.B, False)
    gX, gr = g1
    if g2 is not None: gX = gX + g2[0]; gr = gr + g2[1]
    return e1 + e2, np.r_[gX.ravel(), gr]
z = P.depart()
# controle du gradient
rng = np.random.default_rng(0); v = rng.normal(size=z.size); h = 1e-6
e0, g0 = energie_p(z, 1.0, 0.05); ep, _ = energie_p(z + h * v, 1.0, 0.05); em, _ = energie_p(z - h * v, 1.0, 0.05)
print('gradient : analytique', float(g0 @ v), 'numerique', (ep - em) / (2 * h), flush=True)
bornes = [(None, None)] * (3 * N) + [(np.log(0.05), np.log(30.0))] * N
t0 = time.time()
for mu, it in ((0.1, 2000), (1.0, 3000), (10.0, 4000), (100.0, 6000), (1000.0, 8000)):
    t = time.time(); res = minimize(energie_p, z, args=(mu, 0.05), jac=True, method='L-BFGS-B', bounds=bornes, options=dict(maxiter=it, maxfun=2 * it, ftol=1e-30, gtol=1e-15, maxcor=40)); z = res.x
    m = P.mesures(z)
    print('mu', mu, 'energie %.3e' % res.fun, 'it', res.nit, '%.0f s' % (time.time() - t), '| residu liens %.2e | ecart min non lies %.2e | chevauchements %d | rayons %.3f a %.2f | p liens %.2e | p max non lies %.6f' % (
        m['residu_relatif_max_sur_les_liens'], m['ecart_relatif_min_des_paires_non_liees'], m['paires_non_liees_qui_se_chevauchent'], m['rayon_min'], m['rayon_max'], m['produit_inversif_des_liens_ecart_max_a_moins_un'], m['produit_inversif_max_des_paires_non_liees']), flush=True)
    np.save(S + 'z_p_g%d_N%d.npy' % (graine, N), z)
    if res.fun < 1e-18: break
print('total %.0f s' % (time.time() - t0))
