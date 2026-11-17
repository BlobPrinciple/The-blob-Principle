#!/usr/bin/env python3
"""C-203c -- temoin de Delaunay (auditeur) sur les positions de C-202c : volume certifie ? spectre des incidences ? (Claude, 17 novembre 2026.) Predictions : c203c_prediction.txt.
Usage : python3 c203c.py -> c203c.json"""
import itertools, json
from collections import Counter, defaultdict
import numpy as np
from scipy.spatial import Delaunay

def positions(seed, N=600):
    rng = np.random.default_rng(seed); X = np.zeros((N, 3))
    for c in range(1, N): p = int(rng.integers(0, c)); u = rng.normal(size=3); X[c] = X[p] + u / np.linalg.norm(u)
    return X

out = []
for s in range(202000, 202008):
    X = positions(s); T = [tuple(sorted(int(v) for v in t)) for t in Delaunay(X).simplices]; vol = [abs(np.linalg.det(X[list(t[1:])] - X[t[0]])) / 6 for t in T]
    F = Counter(f for t in T for f in itertools.combinations(t, 3)); par = defaultdict(list)
    for t in T:
        for e in itertools.combinations(t, 2): par[e].append(tuple(x for x in t if x not in e))
    V = len(set(v for t in T for v in t)); E = len(par); sp = Counter(); bord = 0
    for e, L in par.items():
        dg = Counter(x for p in L for x in p)
        if all(v == 2 for v in dg.values()): sp[len(L)] += 1
        else: bord += 1
    n = sum(sp.values()); L = np.array([np.linalg.norm(X[a] - X[b]) for a, b in par])
    r = dict(graine=s, V=V, E=E, F=len(F), T=len(T), euler=V - E + len(F) - len(T), faces_surchargees=sum(1 for v in F.values() if v > 2), volume_min=float(min(vol)), aretes_interieures=n, aretes_de_bord=bord,
             moyenne=float(sum(k * v for k, v in sp.items()) / n), spectre={int(k): v for k, v in sorted(sp.items())}, part_5_6=float((sp[5] + sp[6]) / n), part_3_4=float((sp[3] + sp[4]) / n), part_8_plus=float(sum(v for k, v in sp.items() if k >= 8) / n),
             part_aretes_courtes=float((L <= 1.30).mean()), longueur_mediane=float(np.median(L)))
    out.append(r); print(s, '| V E F T', V, E, len(F), len(T), 'Euler', r['euler'], '| surchargees', r['faces_surchargees'], '| vol min %.1e' % r['volume_min'], '| interieures', n, 'moyenne %.4f' % r['moyenne'], '| 5+6 %.3f' % r['part_5_6'], '| 3+4 %.3f' % r['part_3_4'], '| 8+ %.3f' % r['part_8_plus'], '| max', max(sp), '| aretes <= 1,30 : %.3f' % r['part_aretes_courtes'], flush=True)
json.dump(out, open('c203c.json', 'w'), indent=1)
