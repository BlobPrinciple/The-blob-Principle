#!/usr/bin/env python3
"""C-156c -- controle d'equilibre des 93 etats exportes de C-155A (Claude, 15 novembre 2026). Predictions : c156c_prediction.txt.
Pour chaque etat : multiplicateurs positifs sur les contraintes actives (volume, degagement) equilibrant la force des ressorts, par
moindres carres positifs ; residu = plus grande composante de force non equilibree. Usage : python3 c156c.py"""
import itertools, json, sys
import numpy as np, scipy.optimize as so
from c155a import degagement, MARGE, EPSV, MARGEV

def analyse(ex):
    ids = ex['sommets']; pos = {v: i for i, v in enumerate(ids)}; X = np.array(ex['X']); T = np.array([[pos[v] for v in t] for t in ex['cellules']])
    VR = np.array(ex['Vref']); I = np.array([pos[a] for a, b in ex['fils']]); J = np.array([pos[b] for a, b in ex['fils']]); R = np.array(ex['repos'])
    D = X[I] - X[J]; L = np.linalg.norm(D, axis=1); G = np.zeros_like(X); w = ((L - R) / L)[:, None] * D; np.add.at(G, I, w); np.add.at(G, J, -w)
    a, b, c, d = (X[T[:, i]] for i in range(4)); V = np.einsum('ij,ij->i', b - a, np.cross(c - a, d - a)) / 6
    cols = []; noms = []
    for t in np.nonzero(V < EPSV * VR * (1 + MARGEV) * 1.01)[0]:
        g = np.zeros_like(X); gb = np.cross(c[t] - a[t], d[t] - a[t]) / 6; gc = np.cross(d[t] - a[t], b[t] - a[t]) / 6; gd = np.cross(b[t] - a[t], c[t] - a[t]) / 6
        g[T[t, 1]] += gb; g[T[t, 2]] += gc; g[T[t, 3]] += gd; g[T[t, 0]] -= gb + gc + gd; cols.append(g.ravel()); noms.append('volume')
    clmin = np.inf; h = 1e-7
    for k in (0, 1, 2):
        P = []
        for i, j in itertools.combinations(range(len(T)), 2):
            com = [v for v in T[i] if v in T[j]]
            if len(com) == k: P.append(com + [v for v in T[i] if v not in com] + com + [v for v in T[j] if v not in com])
        if not P: continue
        P = np.array(P); cl = degagement(X[P], k); clmin = min(clmin, float(cl.min()))
        for q in np.nonzero(cl < 3 * MARGE)[0]:
            g = np.zeros_like(X); base = X[P[q]]
            for co in range(24):
                if 12 <= co < 12 + 3 * k: continue
                pp = np.repeat(base[None], 2, axis=0); pp[0, co // 3, co % 3] += h; pp[1, co // 3, co % 3] -= h
                if co < 3 * k: pp[0, 4 + co // 3, co % 3] += h; pp[1, 4 + co // 3, co % 3] -= h
                v = degagement(pp, k); g[P[q][co // 3], co % 3] += (v[0] - v[1]) / (2 * h)
            cols.append(g.ravel()); noms.append(f'degagement{k}')
    if cols:
        A = np.array(cols).T; mu, _ = so.nnls(A, G.ravel(), maxiter=200 * A.shape[1] + 2000); res = G.ravel() - A @ mu
    else:
        mu = np.zeros(0); res = G.ravel()
    return dict(residu=float(np.abs(res).max()), force_ressorts_max=float(np.abs(G).max()), contraintes_actives=len(cols), volumes_actifs=noms.count('volume'),
                contacts_actifs=len(noms) - noms.count('volume'), multiplicateur_max=float(mu.max()) if len(mu) else 0.0,
                multiplicateurs_contact=[round(float(m), 6) for m, nm in zip(mu, noms) if nm != 'volume' and m > 1e-12][:6], degagement_min=clmin if np.isfinite(clmin) else None,
                E=float(0.5 * ((L - R) ** 2).sum()), V_sur_Vref_min=float((V / VR).min()))

out = {}
for sd in (1320, 1321, 1322):
    o = json.load(open(f'c155a_{sd}_etats.json')); ref = json.load(open(f'c155a_{sd}.json'))
    rows = []
    for r, r0 in zip(o['U']['etats'], ref['U']['etats']):
        k = analyse(r['export']); k.update(n=r['n'], methode=r['methode'], ecart_energie_au_premier_calcul=abs(r['E'] - r0['E']), verifie=bool(k['residu'] < 1e-5)); rows.append(k)
    out[str(sd)] = rows
    print(sd, 'verifies', sum(x['verifie'] for x in rows), '/', len(rows), '| origine', sum(x['verifie'] for x in rows if x['methode'] == 'origine'), '/', sum(x['methode'] == 'origine' for x in rows),
          '| contrainte', sum(x['verifie'] for x in rows if x['methode'] == 'contrainte'), '/', sum(x['methode'] == 'contrainte' for x in rows), '| ecart rejeu max', max(x['ecart_energie_au_premier_calcul'] for x in rows), flush=True)
    for x in rows: print('  ', x['n'], x['methode'][:8], 'residu %.2e' % x['residu'], 'force %.3f' % x['force_ressorts_max'], 'actives', x['volumes_actifs'], x['contacts_actifs'], 'mult', x['multiplicateurs_contact'][:3])
json.dump(out, open('c156c.json', 'w'), indent=1)
