#!/usr/bin/env python3
"""X-9 bis [EXPLORATOIRE] -- comptages de PHYS-2 (cellules N, faces exterieures B, cycles C du graphe des cellules voisines par une face) sur les croissances
archivees du laboratoire (c163c_*_A.json[.gz]) : la croissance canonique est-elle une chaine ? (Claude, 16 novembre 2026). Topologie seule, rejouee depuis la suite des fils."""
import json, glob, itertools, gzip
from c120 import Mesh, SEEDS
res = []
for f in sorted(glob.glob('c163c_*_A.json*')):
    d = json.load(gzip.open(f) if f.endswith('.gz') else open(f)); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); degs = []
    for r in d['etats']:
        E = m.inc(); e = tuple(r['fil_canonique']); degs.append(len(E[e])); m.bisect(e, m=3 + r['n'], E=E)
    F = {}
    for t in m.T:
        for fc in itertools.combinations(sorted(t), 3): F.setdefault(fc, []).append(t)
    B = sum(len(v) == 1 for v in F.values()); N = len(m.T); C = (len(F) - B) - N + 1; E = m.inc(); bord = set(e for fc, v in F.items() if len(v) == 1 for e in itertools.combinations(fc, 2))
    res.append(dict(f=f, naissances=len(d['etats']), N=N, B=B, C=C, fils_int=len(set(E) - bord), propres=sum(x == 1 for x in degs), partages=sum(x > 1 for x in degs))); print(res[-1])
json.dump(res, open('x9_topologie_croissances.json', 'w'), indent=1)
