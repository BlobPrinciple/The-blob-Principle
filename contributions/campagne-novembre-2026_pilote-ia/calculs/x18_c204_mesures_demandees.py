#!/usr/bin/env python3
"""X-18 [APRES COUP] -- mesures demandees par ChatGPT (passation C-206) sur l'etat du moteur de l'auteur de C-204c (660 sommets, graines 1 a 4) : sommets appartenant a au moins une cellule,
plus grande composante de cellules reliees par des faces, cellules de volume positif. (Claude, 18 novembre 2026.) Usage : python3 x18_c204_mesures_demandees.py"""
import json, itertools
from collections import defaultdict
import numpy as np
from c204c import Blob, M
out = []
for seed in (1, 2, 3, 4):
    bl = Blob(N0=300, seed=seed, forces=("grav", "em", "weak", "bord"))
    while bl.N < 600: bl.step(0.12)
    T = [tuple(sorted(t)) for t in M['find_all_K4'](bl.adj, bl.N)]; X = np.array(bl.pts); sv = set(v for t in T for v in t); F = defaultdict(list)
    for i, t in enumerate(T):
        for f in itertools.combinations(t, 3): F[f].append(i)
    par = list(range(len(T)))
    def r(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for L in F.values():
        for a in L[1:]: par[r(a)] = r(L[0])
    comp = defaultdict(int)
    for i in range(len(T)): comp[r(i)] += 1
    vol = [abs(np.linalg.det(X[list(t[1:])] - X[t[0]])) / 6 for t in T]
    out.append(dict(graine=seed, N=int(bl.N), cellules=len(T), sommets_dans_une_cellule=len(sv), part=len(sv) / bl.N, plus_grande_composante_par_faces=int(max(comp.values())), composantes=len(comp), cellules_volume_positif=int(sum(v > 1e-12 for v in vol)))); print(out[-1])
json.dump(out, open('x18_c204_mesures_demandees.json', 'w'), indent=1)
