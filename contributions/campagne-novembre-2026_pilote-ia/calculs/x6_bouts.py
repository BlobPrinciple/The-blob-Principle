#!/usr/bin/env python3
"""X-6 [EXPLORATOIRE] -- Claude, 15 novembre 2026. Sur mes arbres (croissance libre, x3_anneaux.arbre, graines 6000 a 6003, 60 naissances), compte des paires de sommets
non lies a moins de 0,25 selon la definition de ChatGPT (C-169R) : << les deux bouts d'un meme eventail ouvert >> = il existe un fil (u, v) dont les cellules forment
une chaine ouverte, la paire etant les deux sommets exterieurs des cellules du bout. Les autres paires sont dites hors eventail ; on releve leur distance, leurs voisins
communs, et la distance en nombre de cellules (graphe d'adjacence par faces) entre les cellules qui les portent."""
import itertools, json
from collections import Counter, deque
import numpy as np
from x3_anneaux import arbre
out = []
for seed in range(6000, 6004):
    m, Vref = arbre(seed, 60); ids = sorted(m.X); X = {v: m.X[v] for v in ids}; E = m.inc()
    vois = {v: set() for v in ids}
    for a, b in m.rest: vois[a].add(b); vois[b].add(a)
    bouts = {}
    for (u, v), cells in E.items():
        g = {}
        for t in cells:
            x, y = [w for w in t if w not in (u, v)]; g.setdefault(x, set()).add(y); g.setdefault(y, set()).add(x)
        ext = [w for w, s in g.items() if len(s) == 1]
        if len(ext) == 2 and len(g) == len(cells) + 1: bouts[frozenset(ext)] = len(cells)
    # graphe des cellules par faces
    cellules = list(m.T); faces = {}
    for i, t in enumerate(cellules):
        for f in itertools.combinations(sorted(t), 3): faces.setdefault(f, []).append(i)
    adj = {i: set() for i in range(len(cellules))}
    for f, l in faces.items():
        if len(l) == 2: adj[l[0]].add(l[1]); adj[l[1]].add(l[0])
    de = {v: [i for i, t in enumerate(cellules) if v in t] for v in ids}
    def dist_cellules(a, b):
        but = set(de[b]); vu = {i: 0 for i in de[a]}; q = deque(de[a])
        while q:
            i = q.popleft()
            if i in but: return vu[i]
            for j in adj[i]:
                if j not in vu: vu[j] = vu[i] + 1; q.append(j)
        return None
    ev = Counter(); hors = []
    for a, b in itertools.combinations(ids, 2):
        if b in vois[a]: continue
        d = float(np.linalg.norm(X[a] - X[b]))
        if d < 0.25:
            k = bouts.get(frozenset((a, b)))
            if k: ev[k] += 1
            else: hors.append(dict(d=round(d, 6), voisins_communs=len(vois[a] & vois[b]), cellules_entre=dist_cellules(a, b)))
    r = dict(graine=seed, cellules=len(m.T), bouts_d_eventail={str(k): v for k, v in sorted(ev.items())}, hors_eventail=len(hors), detail_hors=sorted(hors, key=lambda h: h['d']))
    out.append(r); print(seed, 'cellules', r['cellules'], '| bouts d eventail (cellules : nombre)', r['bouts_d_eventail'], '| hors eventail', r['hors_eventail']); [print('     ', h) for h in r['detail_hors']]
json.dump(out, open('x6_bouts.json', 'w'), indent=1)
