#!/usr/bin/env python3
"""C-205c -- contre-calcul du C-205 de ChatGPT : distances de resistance d'un arbre de naissances (et variantes), rang de la metrique, volumes de quadruplets et quintuplets, signatures spectrales.
Choix d'AUDITEUR ; theoremes classiques. (Claude, 18 novembre 2026.) Predictions : c205c_prediction.txt. Usage : python3 c205c.py -> c205c.json"""
import itertools, json
import numpy as np

def gram(D2, idx):
    S = D2[np.ix_(idx, idx)]; return -0.5 * (S[1:, 1:] - S[1:, [0]] - S[[0], 1:])   # produits scalaires vus du premier point
def rang(M): w = np.linalg.eigvalsh(M); return int((w > max(1e-9, w.max() * 1e-8)).sum())
def detn(G): d = len(G); return float(np.linalg.det(G) / (np.trace(G) / d) ** d)
def resistance(L):
    N = len(L); U = np.ones((N, N)) / N; P = np.linalg.inv(L + U) - U; d = np.diag(P); return d[:, None] + d[None] - 2 * P, P   # pseudo-inverse exacte d'un laplacien connexe

out = {}
# D1 : etoile
L = np.zeros((5, 5)); 
for i in range(1, 5): L[0, 0] += 1; L[i, i] += 1; L[0, i] -= 1; L[i, 0] -= 1
R, P = resistance(L); G = gram(R, [0, 1, 2, 3, 4]); out['etoile'] = dict(R_centre_feuille=float(R[0, 1]), R_feuille_feuille=float(R[1, 2]), gram_identite=bool(np.allclose(G, np.eye(4))), volume4=float(np.sqrt(np.linalg.det(G)) / 24)); print('D1', out['etoile'])
res = []
for N in (64, 128):
    for s in range(205000, 205008):
        rng = np.random.default_rng(s); par = [None] + [int(rng.integers(0, v)) for v in range(1, N)]; om = rng.uniform(0, 1, N); X = np.zeros((N, 3))
        for v in range(1, N): u = rng.normal(size=3); X[v] = X[par[v]] + u / np.linalg.norm(u)
        def lap(poids, extra=()):
            L = np.zeros((N, N))
            for v in range(1, N):
                c = poids(v, par[v]); L[v, v] += c; L[par[v], par[v]] += c; L[v, par[v]] -= c; L[par[v], v] -= c
            for a, b in extra: L[a, a] += 1; L[b, b] += 1; L[a, b] -= 1; L[b, a] -= 1
            return L
        ex = set(); enf = [[] for _ in range(N)]
        for v in range(1, N):
            enf[par[v]].append(v)
            if rng.random() < 0.4:
                cand = [(a, par[par[a]]) for a in range(1, v + 1) if par[a] != 0 or False] ; cand = [(a, g) for a, g in cand if g is not None] + [(a, c) for a in range(1, v + 1) for c in enf[par[a]] if c < a]
                if cand:
                    a, b = cand[int(rng.integers(len(cand)))]; ex.add((min(a, b), max(a, b)))
        bras = dict(A=lap(lambda a, b: 1.0), B=lap(lambda a, b: float(np.exp(-abs(om[a] - om[b])))), C=lap(lambda a, b: 1.0, ex)); r = dict(N=N, graine=s, liens_ajoutes_C=len(ex)); q5 = [sorted(rng.choice(N, 5, replace=False).tolist()) for _ in range(100)]; q4 = [sorted(rng.choice(N, 4, replace=False).tolist()) for _ in range(100)]
        for nom, L in bras.items():
            R, P = resistance(L); J = np.eye(N) - 1 / N; B = -0.5 * J @ R @ J
            r[nom] = dict(rang=rang(B), B_egale_pinv=float(abs(B - P).max()), det5_min=min(detn(gram(R, q)) for q in q5), det4_min=min(detn(gram(R, q)) for q in q4))
        D2 = ((X[:, None] - X[None]) ** 2).sum(2); J = np.eye(N) - 1 / N; r['D'] = dict(rang=rang(-0.5 * J @ D2 @ J), det5_max=max(abs(detn(gram(D2, q))) for q in q5), det4_min=min(detn(gram(D2, q)) for q in q4))
        w, U = np.linalg.eigh(bras['A']); r['lambda4_sur_lambda3'] = float(w[4] / w[3]); r['spectral'] = {}
        for k in (2, 3, 4):
            Y = U[:, 1:k + 1]; S2 = ((Y[:, None] - Y[None]) ** 2).sum(2); J = np.eye(N) - 1 / N
            r['spectral'][k] = dict(rang=rang(-0.5 * J @ S2 @ J), det4_max=max(abs(detn(gram(S2, q))) for q in q4), det4_min=min(abs(detn(gram(S2, q))) for q in q4), det5_max=max(abs(detn(gram(S2, q))) for q in q5))
        res.append(r)
out['cas'] = res
for nom in 'ABC': print(nom, '| rang = N-1 :', sum(r[nom]['rang'] == r['N'] - 1 for r in res), '/ 16 | ecart max a la pseudo-inverse %.1e' % max(r[nom]['B_egale_pinv'] for r in res), '| plus petit det de quintuplet %.2e' % min(r[nom]['det5_min'] for r in res), '| plus petit det de quadruplet %.2e' % min(r[nom]['det4_min'] for r in res))
print('D | rang 3 :', sum(r['D']['rang'] == 3 for r in res), '/ 16 | plus grand |det| de quintuplet %.1e' % max(r['D']['det5_max'] for r in res), '| plus petit det de quadruplet %.2e' % min(r['D']['det4_min'] for r in res))
for k in (2, 3, 4): print('signatures k =', k, '| rang k :', sum(r['spectral'][str(k)]['rang'] == k if str(k) in r['spectral'] else r['spectral'][k]['rang'] == k for r in res), '/ 16 | det4 max %.1e, min %.1e | det5 max %.1e' % (max(r['spectral'][k]['det4_max'] for r in res), min(r['spectral'][k]['det4_min'] for r in res), max(r['spectral'][k]['det5_max'] for r in res)))
lam = [r['lambda4_sur_lambda3'] for r in res]; print('lambda4/lambda3 : mediane %.3f, max %.3f, au-dessus de 5 :' % (np.median(lam), max(lam)), sum(x > 5 for x in lam), '/ 16')
json.dump(out, open('c205c.json', 'w'), indent=1)
