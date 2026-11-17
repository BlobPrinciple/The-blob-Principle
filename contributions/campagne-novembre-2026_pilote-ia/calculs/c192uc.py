#!/usr/bin/env python3
"""C-192Uc -- contre-calcul independant du C-192-U de ChatGPT (Claude, 17 novembre 2026) : naissance genealogique minimale (un porteur + un lien au parent, place a 1,04 dans une direction au hasard)
suivie d'une relaxation sous Lennard-Jones (bras LJ) ou sous sa seule partie repulsive (bras WCA, temoin), de 2 a 19 porteurs, graines 192000 a 192015. Ecrit d'apres son seul PROTOCOLE SCELLE.
La mise en espace, le choix du parent et le potentiel sont des choix d'AUDITEUR de ChatGPT, pas la mitose du master. Predictions : c192uc_prediction.txt. Usage : python3 c192uc.py -> c192uc.json"""
import json
import numpy as np, scipy.optimize as so
from c187c import lj
from c189c import mesure

def wca(z):
    X = z.reshape(-1, 3); n = len(X); iu = np.triu_indices(n, 1); d = X[iu[0]] - X[iu[1]]; r2 = (d * d).sum(1); m = r2 < 1; i6 = np.where(m, 1 / r2 ** 3, 0.0)
    e = np.where(m, i6 * i6 - 2 * i6 + 1, 0.0).sum(); f = np.where(m, -12 * (i6 * i6 - i6) / r2, 0.0)[:, None] * d; g = np.zeros_like(X); np.add.at(g, iu[0], f); np.add.at(g, iu[1], -f)
    return e, g.ravel()

def relaxe(V, X):
    r = so.minimize(V, X.ravel(), jac=True, method='L-BFGS-B', options=dict(maxiter=1500, gtol=1e-8, ftol=1e-12, maxls=40)); x, e = r.x, r.fun; secours = False
    if np.linalg.norm(V(x)[1]) > 1e-4:
        r2 = so.minimize(V, x, jac=True, method='BFGS', options=dict(gtol=1e-7, maxiter=1500)); secours = True
        if r2.fun < e: x, e = r2.x, r2.fun
    return x.reshape(-1, 3), float(e), float(np.linalg.norm(V(x)[1])), secours

def trajectoire(V, seed):
    rng = np.random.default_rng(seed); X = np.array([[-0.5, 0, 0], [0.5, 0, 0]]); gen = [(0, 1)]; out = dict(graine=seed, echec=None, etats={})
    for N in range(3, 20):
        p = int(rng.integers(0, N - 1)); ok = False
        for _ in range(128):
            u = rng.normal(size=3); c = X[p] + 1.04 * u / np.linalg.norm(u); d = np.linalg.norm(X - c, axis=1); d[p] = 9
            if d.min() >= 0.78: ok = True; break
        if not ok: out['echec'] = N; break
        gen.append((p, N - 1)); X, e, g, sec = relaxe(V, np.vstack([X, c])); m = mesure(X, 1.30 + 1e-12)
        D = np.linalg.norm(X[:, None] - X[None], axis=2); contacts = set((i, j) for i in range(N) for j in range(i + 1, N) if D[i, j] <= 1.30 + 1e-12)
        out['etats'][N] = dict(E=e, force=g, secours=sec, contacts=len(contacts), contacts_non_genealogiques=len(contacts - set(tuple(sorted(x)) for x in gen)), liens_genealogiques_rompus=len(set(tuple(sorted(x)) for x in gen) - contacts),
                               tetraedres=m['tetraedres'], distribution=m['distribution'], moyenne=m['moyenne'], faces_surchargees=m['faces_surchargees'],
                               icosaedre=bool(N == 13 and m['tetraedres'] == 20 and m['distribution'] == {5: 12} and m['faces_surchargees'] == 0))
    return out

if __name__ == '__main__':
    res = {}
    for nom, V in (('LJ', lj), ('WCA', wca)):
        R = [trajectoire(V, s) for s in range(192000, 192016)]; res[nom] = R
        for N in (7, 13, 19):
            L = [r['etats'][N] for r in R if N in r['etats']]; tous = [k for e in L for k, v in e['distribution'].items() for _ in range(v)]
            print(nom, 'N', N, '| avec lien entoure de 5 :', sum(1 for e in L if e['distribution'].get(5)), '/', len(L), '| toutes valences des liens entoures :', {k: tous.count(k) for k in sorted(set(tous))}, '| moyenne %.4f' % (np.mean(tous) if tous else float('nan')),
                  '| icosaedres :', sum(e['icosaedre'] for e in L), '| surcharges :', sum(1 for e in L if e['faces_surchargees']), '| contacts non genealogiques (min, mediane, max) :', (min(e['contacts_non_genealogiques'] for e in L), int(np.median([e['contacts_non_genealogiques'] for e in L])), max(e['contacts_non_genealogiques'] for e in L)),
                  '| E min %.6f' % min(e['E'] for e in L), '| force max %.1e' % max(e['force'] for e in L), '| secours', sum(e['secours'] for e in L), flush=True)
        print(nom, 'par graine a N=7 :', [(1 if r['etats'][7]['distribution'].get(5) else 0) if 7 in r['etats'] else None for r in R], ' a N=13 :', [r['etats'][13]['distribution'].get(5, 0) if 13 in r['etats'] else None for r in R], ' a N=19 :', [r['etats'][19]['distribution'].get(5, 0) if 19 in r['etats'] else None for r in R], 'echecs (graine, N) :', [(r['graine'], r['echec']) for r in R if r['echec']])
    json.dump(res, open('c192uc.json', 'w'))
