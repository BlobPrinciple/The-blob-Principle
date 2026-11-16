#!/usr/bin/env python3
"""C-189c -- contre-calcul independant du C-189 de ChatGPT (Claude, 16 novembre 2026) : amas de Lennard-Jones a 13, 19, 38 et 55 atomes, departs deterministes de son protocole,
V = somme (r^-12 - 2 r^-6), aucun terme du Blob. Ecrit d'apres son seul PROTOCOLE SCELLE ; resultats non lus avant le scelle de c189c_prediction.txt.
Mesure : lien si distance <= seuil (1,30 ; sensibilites 1,25 et 1,35) ; tetraedre = clique de 4 ; lien ENTOURE si les sommets opposes forment un seul cycle (chacun de degre 2, connexe, au moins 3).
Usage : python3 c189c.py -> c189c.json"""
import itertools, json, math
import numpy as np, scipy.optimize as so
from c187c import lj

PHI = (1 + math.sqrt(5)) / 2; REF = {13: -44.326801419534, 19: -72.659782, 38: -173.928427, 55: -279.248470}


def departs():
    V = []
    for a, b in itertools.product((1, -1), repeat=2): V += [(0, a, b * PHI), (a, b * PHI, 0), (a * PHI, 0, b)]
    V = np.array(V, float); n13 = np.vstack([[0, 0, 0], V]) / 2
    paires = [(i, j) for i in range(12) for j in range(i + 1, 12) if abs(np.linalg.norm(V[i] - V[j]) - 2) < 1e-10]; assert len(paires) == 30
    ext = np.vstack([2 * V, [V[i] + V[j] for i, j in paires]]) / 2; n55 = np.vstack([n13, ext])
    o = sorted(range(42), key=lambda k: (-round(ext[k, 2], 9), -round(ext[k, 0], 9), -round(ext[k, 1], 9)))[:6]; n19 = np.vstack([n13, ext[o]])
    P = set()
    for s in itertools.product((1, -1), repeat=3):
        P.add((s[0], 0, 0)); P.add((0, s[0], 0)); P.add((0, 0, s[0])); P.add(s)
        for p in itertools.permutations((2, 1, 0)): P.add(tuple(p[k] * s[k] for k in range(3)))
    n38 = np.array(sorted(P), float) / math.sqrt(2); assert len(n38) == 38
    return {13: n13, 19: n19, 38: n38, 55: n55}


def relaxe(X):
    X = X - X.mean(0); r = np.linalg.norm(X[:, None] - X[None], axis=2)[np.triu_indices(len(X), 1)]; s = ((r ** -12.).sum() / (r ** -6.).sum()) ** (1 / 6)
    res = so.minimize(lj, (s * X).ravel(), jac=True, method='L-BFGS-B', options=dict(maxiter=3000, ftol=1e-14, gtol=1e-10, maxls=40))
    if np.abs(res.jac).max() > 1e-6: res = so.minimize(lj, res.x, jac=True, method='BFGS', options=dict(maxiter=600, gtol=1e-8))
    Y = res.x.reshape(-1, 3); D = np.linalg.norm(Y[:, None] - Y[None], axis=2)
    return Y, float(res.fun), float(np.abs(lj(res.x)[1]).max()), float(D[np.triu_indices(len(Y), 1)].min())


def mesure(X, seuil):
    n = len(X); D = np.linalg.norm(X[:, None] - X[None], axis=2); A = [set(j for j in range(n) if j != i and D[i, j] <= seuil) for i in range(n)]
    ent = {}; avec = {}; tri = {}; ntet = 0
    for i in range(n):
        for j in A[i]:
            if j < i: continue
            com = A[i] & A[j]; adj = {c: com & A[c] for c in com}; k = sum(len(v) for v in adj.values()) // 2
            if k: avec[(i, j)] = k
            if k >= 3 and all(len(adj[c]) == 2 for c in com if adj[c]) and all(adj[c] for c in com):
                c0 = next(iter(com)); vu = {c0}; pile = [c0]
                while pile:
                    x = pile.pop()
                    for y in adj[x]:
                        if y not in vu: vu.add(y); pile.append(y)
                if len(vu) == len(com): ent[(i, j)] = k
    for q in itertools.combinations(range(n), 4):
        if all(b in A[a] for a, b in itertools.combinations(q, 2)):
            ntet += 1
            for f in itertools.combinations(q, 3): tri[f] = tri.get(f, 0) + 1
    v = sorted(ent.values()); h = {int(k): v.count(k) for k in sorted(set(v))}
    return dict(seuil=seuil, liens=sum(len(a) for a in A) // 2, tetraedres=ntet, liens_entoures=len(v), distribution=h, moyenne=(float(np.mean(v)) if v else None), part_six=(v.count(6) / len(v) if v else None),
                n_e_de_tous_les_liens={int(k): list(avec.values()).count(k) for k in sorted(set(avec.values()))}, faces_surchargees=sum(1 for x in tri.values() if x > 2), longueurs_entoures=sorted(round(float(D[e]), 5) for e in ent)[:3] + sorted(round(float(D[e]), 5) for e in ent)[-3:])


if __name__ == '__main__':
    out = {}
    for N, X0 in departs().items():
        X, E, g, dmin = relaxe(X0); r = dict(N=N, E=E, reference=REF[N], ecart=E - REF[N], gradient=g, dmin=dmin, mesures=[mesure(X, s) for s in (1.30, 1.25, 1.35)], reprises=[])
        for k in range(4):
            rng = np.random.Generator(np.random.PCG64(189000 + N * 100 + k)); Y, E2, g2, d2 = relaxe(X + rng.normal(loc=0.0, scale=0.025, size=(N, 3))); m = mesure(Y, 1.30)
            r['reprises'].append(dict(k=k, E=E2, gradient=g2, meme_energie=bool(abs(E2 - E) < 1e-6 * abs(E)), liens_entoures=m['liens_entoures'], distribution=m['distribution']))
        D = np.linalg.norm(X[:, None] - X[None], axis=2)[np.triu_indices(N, 1)]; r['distances_entre_1_25_et_1_45'] = sorted(set(np.round(D[(D > 1.25) & (D < 1.45)], 3).tolist()))[:12]
        out[N] = r; m = r['mesures'][0]
        print(N, 'E %.6f' % E, 'ecart %.2e' % r['ecart'], 'grad %.1e' % g, '| 1,30 : tetra', m['tetraedres'], 'entoures', m['liens_entoures'], m['distribution'], 'moy', m['moyenne'], 'surch', m['faces_surchargees'], 'tous', m['n_e_de_tous_les_liens'],
              '| 1,25 :', r['mesures'][1]['liens_entoures'], r['mesures'][1]['distribution'], '| 1,35 :', r['mesures'][2]['liens_entoures'], r['mesures'][2]['distribution'], 'surch', r['mesures'][2]['faces_surchargees'],
              '| reprises', [(x['meme_energie'], x['liens_entoures']) for x in r['reprises']], '| d', r['distances_entre_1_25_et_1_45'][:6], flush=True)
    json.dump(out, open('c189c.json', 'w'), indent=1)
