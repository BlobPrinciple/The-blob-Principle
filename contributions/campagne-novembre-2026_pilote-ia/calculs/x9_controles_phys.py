#!/usr/bin/env python3
"""X-9 [EXPLORATOIRE, non aveugle] -- controles rapides de trois affirmations de ChatGPT (C-173R, PHYS-1, PHYS-2), 16 novembre 2026 (Claude).
1 seuil de flambement de la couronne plate de six quand la ceinture s'allonge ; 2 comptages de l'instantane M30 ; 3 bissections de fils propres seules => cellules en chaine."""
import itertools, json, random
import numpy as np, scipy.optimize as so
import c173c
from c120 import Mesh, SEEDS

out = {}
# 1 flambement : etat symetrique (minimise sans perturbation), plus petite valeur propre hors six modes rigides
def vp(d, n=6):
    X, I, c = c173c.couronne(n); R = 1 + d * c; r = so.minimize(c173c.energie, X.ravel(), args=(I, R), jac=True, method='L-BFGS-B', options=dict(gtol=1e-14, ftol=1e-18, maxiter=20000))
    w = c173c.hess(r.x.reshape(-1, 3), I, R); return sorted(w, key=abs)[6:] and min(sorted(w, key=abs)[6:])
s = so.brentq(vp, 0.05, 0.08, xtol=1e-13); out['flambement'] = dict(seuil=s, ecart_a_chatgpt=abs(s - 0.065154087757), vp_a_10=vp(0.10), directions_a_15=int((np.array(sorted(c173c.hess(so.minimize(c173c.energie, c173c.couronne(6)[0].ravel(), args=(c173c.couronne(6)[1], 1 + 0.15 * c173c.couronne(6)[2]), jac=True, method='L-BFGS-B', options=dict(gtol=1e-14, ftol=1e-18, maxiter=20000)).x.reshape(-1, 3), c173c.couronne(6)[1], 1 + 0.15 * c173c.couronne(6)[2]))) < -1e-7).sum()))
print('1', out['flambement'])
# 2 M30
m = c173c.charge(); E = m.inc(); F = {}
for t in m.T:
    for f in itertools.combinations(sorted(t), 3): F.setdefault(f, []).append(t)
B = sum(len(v) == 1 for v in F.values()); Fi = sum(len(v) == 2 for v in F.values()); N = len(m.T); bord = set(e for f, v in F.items() if len(v) == 1 for e in itertools.combinations(f, 2))
out['M30'] = dict(cellules=N, faces_exterieures=B, faces_interieures=Fi, cycles=Fi - N + 1, identite_B_2N_2_2C=bool(B == 2 * N + 2 - 2 * (Fi - N + 1)), fils_interieurs=[[list(e), len(v)] for e, v in E.items() if e not in bord],
                fils_de_bord_a_cinq_cellules=sum(1 for e, v in E.items() if e in bord and len(v) == 5), sommets_interieurs=len(set(m.X) - set(v for e in bord for v in e)))
print('2', out['M30'])
# 3 chaine : bissections de fils propres seules, sans relaxation
res = []
for seed in range(5):
    rng = random.Random(9300 + seed); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F')
    while len(m.T) < 512:
        E = m.inc(); m.bisect(rng.choice(sorted(e for e, v in E.items() if len(v) == 1)), E=E)
    F = {}
    for t in m.T:
        for f in itertools.combinations(sorted(t), 3): F.setdefault(f, []).append(t)
    deg = {t: 0 for t in m.T}
    for v in F.values():
        if len(v) == 2: deg[v[0]] += 1; deg[v[1]] += 1
    E = m.inc(); va = np.mean([len(set(t2 for e in itertools.combinations(sorted(t), 2) for t2 in E[e]) - {t}) for t in m.T])
    res.append(dict(graine=9300 + seed, cellules=len(m.T), voisins_par_face={k: sum(1 for d in deg.values() if d == k) for k in range(5)}, faces_exterieures=sum(len(v) == 1 for v in F.values()), voisins_par_fil_moyenne=float(va)))
    print('3', res[-1])
out['chaine'] = res; json.dump(out, open('x9_controles_phys.json', 'w'), indent=1)
# 4 temoin de Freudenthal : 7^3 cubes x 6 tetraedres (comptages de PHYS-1)
from collections import Counter
T = []
for c in itertools.product(range(7), repeat=3):
    for p in itertools.permutations(range(3)):
        v = list(c); t = [tuple(v)]
        for a in p: v[a] += 1; t.append(tuple(v))
        T.append(tuple(sorted(t)))
F = {}; E = {}
for t in T:
    for f in itertools.combinations(t, 3): F.setdefault(f, []).append(t)
    for e in itertools.combinations(t, 2): E.setdefault(e, []).append(t)
B = sum(len(v) == 1 for v in F.values()); Fi = len(F) - B; N = len(T); bv = set(x for f, v in F.items() if len(v) == 1 for x in f); be = set(e for f, v in F.items() if len(v) == 1 for e in itertools.combinations(f, 2)); deg = Counter()
for v in F.values():
    if len(v) == 2: deg[v[0]] += 1; deg[v[1]] += 1
out['freudenthal'] = dict(cellules=N, faces_exterieures=B, sommets_interieurs=len(set(x for t in T for x in t) - bv), fils_interieurs=len(set(E) - be), cycles=Fi - N + 1, cellules_a_quatre_voisins=sum(1 for t in T if deg[t] == 4), identite=bool(B == 2 * N + 2 - 2 * (Fi - N + 1)))
print('4', out['freudenthal']); json.dump(out, open('x9_controles_phys.json', 'w'), indent=1)
