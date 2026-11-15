#!/usr/bin/env python3
"""X-5 [EXPLORATOIRE] -- Claude, 15 novembre 2026. Regime d'exploration : pas de prediction prealable, rien ici n'est acquis.
Mise a l'epreuve, sur de vrais arbres, du theoreme conditionnel de ChatGPT (C-169-E) : << dans un eventail ideal, toute portee de fusion entre 1/9 et 1 selectionne
la cinquieme cellule comme premier contact >>. Dans les arbres de la croissance libre (x3_anneaux.arbre), quelles sont les distances entre sommets NON lies ?
Sont-elles toutes des ouvertures d'eventail de cinq (1/9), ou d'autres rapprochements existent-ils sous la portee ?
Controle analytique : d_k = racine(3) |sin(k theta / 2)|, theta = arccos(1/3)."""
import itertools, json, math, sys
from collections import Counter
import numpy as np
from x3_anneaux import arbre
th = math.acos(1 / 3); out = {'d_k': {k: math.sqrt(3) * abs(math.sin(k * th / 2)) for k in range(2, 8)}}
print('d_k', {k: round(v, 9) for k, v in out['d_k'].items()}, '| 1/9 =', 1 / 9, '| 5/3 =', 5 / 3, '| racine(8/3) =', math.sqrt(8 / 3))
out['arbres'] = []
for seed in range(6000, 6000 + int(sys.argv[1])):
    m, Vref = arbre(seed, int(sys.argv[2])); ids = sorted(m.X); X = np.array([m.X[v] for v in ids]); E = m.inc()
    vois = {v: set() for v in ids}
    for a, b in m.rest: vois[a].add(b); vois[b].add(a)
    paires = []
    for i, j in itertools.combinations(range(len(ids)), 2):
        a, b = ids[i], ids[j]
        if b in vois[a]: continue
        d = float(np.linalg.norm(X[i] - X[j]))
        if d < 1.2:
            com = vois[a] & vois[b]                       # sommets lies aux deux
            # ouverture d'eventail : un fil (u, v), u et v lies a a et b, entoure de k cellules en chaine dont a et b sont les deux bouts
            fan = max((len(E[tuple(sorted((u, v)))]) for u, v in itertools.combinations(sorted(com), 2) if tuple(sorted((u, v))) in E), default=0)
            paires.append((d, len(com), fan))
    cl = Counter()
    for d, nc, fan in paires:
        cl[('1/9' if abs(d - 1 / 9) < 1e-6 else '<0,25' if d < 0.25 else '0,25-0,5' if d < 0.5 else '0,5-1' if d < 1 else '1,0887' if abs(d - out['d_k'][4]) < 1e-6 else '1-1,2', f'voisins communs {nc}', f'plus grand eventail commun {fan}')] += 1
    r = dict(graine=seed, cellules=len(m.T), sommets=len(ids), classes={' | '.join(k): v for k, v in sorted(cl.items())}, plus_petite=min((p[0] for p in paires), default=None))
    out['arbres'].append(r); print(seed, 'cellules', len(m.T)); [print('   ', k, ':', v) for k, v in r['classes'].items()]
json.dump(out, open('x5_contacts.json', 'w'), indent=1)
