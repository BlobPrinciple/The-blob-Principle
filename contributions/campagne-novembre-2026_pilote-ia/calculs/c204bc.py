#!/usr/bin/env python3
"""C-204bc -- contre-calcul independant du C-204 de ChatGPT : selection des cellules de Delaunay de rayon circonscrit borne (complexe alpha), part de volume, spectre, et verification de localite
(reconstruction sommet par sommet dans un voisinage 2 rho). Temoin geometrique d'AUDITEUR. (Claude, 17 novembre 2026.) Predictions : c204bc_prediction.txt. Usage : python3 c204bc.py -> c204bc.json"""
import itertools, json
from collections import Counter, defaultdict
import numpy as np
from scipy.spatial import Delaunay, ConvexHull, cKDTree
from c203c import positions

def rayon(P):
    A = 2 * (P[1:] - P[0]); b = (P[1:] ** 2).sum(1) - (P[0] ** 2).sum(); c = np.linalg.solve(A, b); return float(np.linalg.norm(c - P[0]))
def cellules(X): return [tuple(sorted(int(v) for v in t)) for t in Delaunay(X).simplices if abs(np.linalg.det(X[t[1:]] - X[t[0]])) > 1e-12]
def spectre(T):
    par = defaultdict(list); F = Counter(f for t in T for f in itertools.combinations(t, 3))
    for t in T:
        for e in itertools.combinations(t, 2): par[e].append(tuple(x for x in t if x not in e))
    sp = Counter()
    for e, L in par.items():
        dg = Counter(x for p in L for x in p)
        if all(v == 2 for v in dg.values()) and len(dg) == len(L):
            adj = defaultdict(list)
            for a, b in L: adj[a].append(b); adj[b].append(a)
            vu = {L[0][0]}; pile = [L[0][0]]
            while pile:
                x = pile.pop()
                for y in adj[x]:
                    if y not in vu: vu.add(y); pile.append(y)
            if len(vu) == len(dg): sp[len(L)] += 1
    return sp, sum(1 for v in F.values() if v > 2)

RHO = (0.25, 0.50, 0.75, 1.00, 1.50); out = []
for s in range(202000, 202008):
    X = positions(s); T = cellules(X); R = np.array([rayon(X[list(t)]) for t in T]); vol = np.array([abs(np.linalg.det(X[list(t[1:])] - X[t[0]])) / 6 for t in T]); VH = ConvexHull(X).volume; r = dict(graine=s, cellules=len(T), volume_enveloppe=float(VH), somme_volumes=float(vol.sum()), par_rho={}); prec = set()
    for rho in RHO:
        sel = [t for t, x in zip(T, R) if x <= rho]; sp, sur = spectre(sel); n = sum(sp.values()); ss = set(sel)
        r['par_rho'][rho] = dict(retenues=len(sel), part_cellules=len(sel) / len(T), part_volume=float(vol[R <= rho].sum() / VH), volume_min=float(vol[R <= rho].min()) if len(sel) else None, faces_surchargees=sur, emboitee=bool(prec <= ss), aretes_interieures=n,
                                 part_5_6=((sp[5] + sp[6]) / n if n else None), part_six_parmi_5_6=(sp[6] / (sp[5] + sp[6]) if sp[5] + sp[6] else None), moyenne=(sum(k * v for k, v in sp.items()) / n if n else None)); prec = ss
    if s in (202000, 202001):
        tr = cKDTree(X); r['localite'] = {}
        for rho in (0.50, 0.75):
            glob = set(t for t, x in zip(T, R) if x <= rho); loc = set()
            for v in range(len(X)):
                idx = np.array(sorted(tr.query_ball_point(X[v], 2 * rho + 1e-12)))
                if len(idx) < 5: continue
                try: D = Delaunay(X[idx])
                except Exception: continue
                for t in D.simplices:
                    q = tuple(sorted(int(idx[i]) for i in t))
                    if v in q and abs(np.linalg.det(X[list(q[1:])] - X[q[0]])) > 1e-12 and rayon(X[list(q)]) <= rho: loc.add(q)
            r['localite'][rho] = dict(globale=len(glob), locale=len(loc), identiques=bool(glob == loc), seulement_globale=len(glob - loc), seulement_locale=len(loc - glob))
    out.append(r); print(s, '| cellules', len(T), '| par rho :', {k: (v['retenues'], round(v['part_volume'], 3), v['faces_surchargees'], v['aretes_interieures'], None if v['part_5_6'] is None else round(v['part_5_6'], 3)) for k, v in r['par_rho'].items()}, '| emboitees', all(v['emboitee'] for v in r['par_rho'].values()), '| localite', r.get('localite'), flush=True)
json.dump(out, open('c204bc.json', 'w'), indent=1)
