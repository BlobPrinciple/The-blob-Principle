#!/usr/bin/env python3
"""X-25 ter, construction, essai 3 (pose des constituants un a un). Non concluant : voir x25ter_construction.out. A lancer depuis calculs/ : python3 x25ter_construction_essai3.py graine cible.     Claude, 23 novembre 2026."""
"""Construction par insertion : les constituants sont poses un a un (ordre de degenerescence inverse), chaque pose est suivie d'une minimisation de l'energie
en produits inversifs sur tout ce qui est deja pose. Essai."""
import sys, time, json, numpy as np
sys.path.insert(0, '.')
from scipy.optimize import minimize
import x25ter_construction as c
S = './'   # dossier de sortie des essais
graine, cible = int(sys.argv[1]), int(sys.argv[2]); M = 0.05
X0, liens, emp = c.etat(graine, cible); N = len(X0)
adj = [set() for _ in range(N)]
for a, b in liens: adj[a].add(b); adj[b].add(a)
# ordre de degenerescence
deg = [len(a) for a in adj]; vivant = [True] * N; ordre = []
for _ in range(N):
    v = min((u for u in range(N) if vivant[u]), key=lambda u: deg[u]); ordre.append(v); vivant[v] = False
    for w in adj[v]:
        if vivant[w]: deg[w] -= 1
ordre = ordre[::-1]; rang = {v: i for i, v in enumerate(ordre)}
arr = max(sum(1 for w in adj[v] if rang[w] < rang[v]) for v in ordre)
print('constituants', N, 'liens', len(liens), 'degenerescence', arr, flush=True)

def energie(z, k, I, J, A, B, mu):
    X = z[:3 * k].reshape(k, 3); r = np.exp(z[3 * k:])
    gX = np.zeros((k, 3)); gr = np.zeros(k); e = 0.0
    for a, b, lien in ((I, J, True), (A, B, False)):
        if len(a) == 0: continue
        D = X[a] - X[b]; d2 = (D * D).sum(1); ra, rb = r[a], r[b]
        p = (ra * ra + rb * rb - d2) / (2 * ra * rb)
        if lien: w = p + 1.0; kk = 1.0
        else:
            w = p + 1.0 + M; act = w > 0
            if not act.any(): continue
            a, b, D, d2, ra, rb, w = a[act], b[act], D[act], d2[act], ra[act], rb[act], w[act]; kk = mu
        e += kk * (w * w).sum(); f = 2 * kk * w
        cX = (-f / (ra * rb))[:, None] * D
        for q in range(3): gX[:, q] += np.bincount(a, cX[:, q], k) - np.bincount(b, cX[:, q], k)
        gr += np.bincount(a, f * (ra * ra - rb * rb + d2) / (2 * ra * rb), k) + np.bincount(b, f * (rb * rb - ra * ra + d2) / (2 * ra * rb), k)
    return e, np.r_[gX.ravel(), gr]

rng = np.random.default_rng(25)
X = np.zeros((N, 3)); rho = np.zeros(N); pos = {}                    # pos : constituant -> indice de pose
lie = np.zeros((N, N), bool)
I = []; J = []; t0 = time.time(); pire = 0.0; echecs = 0
for k, v in enumerate(ordre):
    vois = [pos[w] for w in adj[v] if w in pos]
    if not vois:
        X[k] = rng.normal(size=3) * 3 + (X[:k].mean(0) if k else 0) + np.array([40.0 * (1 + k % 7), 0, 0]) * (k > 0); rho[k] = 0.0
    else:
        cc = X[vois].mean(0); rm = np.exp(rho[vois]).min()
        X[k] = cc + rng.normal(size=3) * rm; rho[k] = np.log(0.3 * rm)
    pos[v] = k
    for w in vois: I.append(k); J.append(w); lie[k, w] = lie[w, k] = True
    kk = k + 1
    if kk < 2: continue
    Ia, Ja = np.array(I, int), np.array(J, int)
    A, B = np.triu_indices(kk, 1); g = ~lie[:kk, :kk][A, B]; A, B = A[g], B[g]
    z = np.r_[X[:kk].ravel(), rho[:kk]]
    for mu, it in ((10.0, 60), (100.0, 150), (1000.0, 400)):
        res = minimize(energie, z, args=(kk, Ia, Ja, A, B, mu), jac=True, method='L-BFGS-B', options=dict(maxiter=it, maxfun=3 * it, ftol=1e-30, gtol=1e-13, maxcor=30)); z = res.x
        if res.fun < 1e-16: break
    if res.fun > 1e-10:
        res = minimize(energie, z, args=(kk, Ia, Ja, A, B, 1000.0), jac=True, method='L-BFGS-B', options=dict(maxiter=3000, maxfun=6000, ftol=1e-30, gtol=1e-13, maxcor=40)); z = res.x
    X[:kk] = z[:3 * kk].reshape(kk, 3); rho[:kk] = z[3 * kk:]
    pire = max(pire, res.fun); echecs += res.fun > 1e-10
    if kk % 20 == 0 or kk == N or res.fun > 1e-10:
        print('poses', kk, '| liens', len(I), '| energie %.2e' % res.fun, '| pire %.2e' % pire, '| poses sans retour a zero', echecs, '| rayons %.3g a %.3g' % (np.exp(rho[:kk]).min(), np.exp(rho[:kk]).max()), '| %.0f s' % (time.time() - t0), flush=True)
    if echecs > 25: print('abandon : trop de poses sans retour a zero'); break
np.savez(S + 'z3_g%d_N%d.npz' % (graine, N), X=X, rho=rho, ordre=np.array(ordre), poses=kk)
