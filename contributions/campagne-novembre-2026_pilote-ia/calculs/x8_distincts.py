#!/usr/bin/env python3
"""X-8 [EXPLORATOIRE] -- Claude, 15 novembre 2026. Controle : les trois tissus S1 de c171c.py (graines 9000 a 9002) sont-ils reellement differents ?
Invariant d'isometrie : liste triee de toutes les distances entre sommets, avant et apres la fermeture de l'eventail. Et : les arbres different-ils des la croissance ?"""
import json
import numpy as np
import c132_audit as c132
from c169c import degagement_min, reunir
from x3_anneaux import arbre
from x7_moindre_cout import bouts
def sig(m):
    X = np.array([m.X[v] for v in sorted(m.X)]); i, j = np.triu_indices(len(X), 1); return np.sort(np.linalg.norm(X[i] - X[j], axis=1))
S = {}; out = {}
for seed in (9000, 9001, 9002):
    m, V = arbre(seed, 30); a = sig(m); nb = sum(1 for p, k in bouts(m).items() if k == 5)
    c = [(float(np.linalg.norm(m.X[x] - m.X[y])), x, y) for (x, y), k in ((tuple(p), k) for p, k in bouts(m).items()) if k == 5 and tuple(sorted((x, y))) not in m.rest]
    d, x, y = min(c); reunir(m, V, x, y); c132.relax(m, V); S[seed] = (a, sig(m)); E = m.inc()
    out[seed] = dict(cellules=len(m.T), eventails_de_cinq=nb, fils_propres=sum(1 for v in E.values() if len(v) == 1), rayon_giration_avant=float(np.sqrt(((np.array(list(m.X.values())) - np.array(list(m.X.values())).mean(0)) ** 2).sum(1).mean())))
    print(seed, out[seed])
for a, b in ((9000, 9001), (9000, 9002), (9001, 9002)):
    e0 = float(np.abs(S[a][0] - S[b][0]).max()); e1 = float(np.abs(S[a][1] - S[b][1]).max()) if len(S[a][1]) == len(S[b][1]) else None
    out[f'{a}-{b}'] = dict(ecart_arbres=e0, ecart_tissus_fermes=e1); print(a, b, 'ecart max des distances triees : arbres %.4f' % e0, '| tissus fermes', e1)
json.dump(out, open('x8_distincts.json', 'w'), indent=1)
