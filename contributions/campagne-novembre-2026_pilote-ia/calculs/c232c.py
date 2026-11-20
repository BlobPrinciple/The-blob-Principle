#!/usr/bin/env python3
"""C-232c -- contre-calcul independant de la note C-232 de ChatGPT : complexe simplicial aleatoire sans dimension maximale imposee ; la dimension la plus frequente depend-elle de
p et de N ? Prediction scellee : c232c_prediction.txt. Claude, 20 novembre 2026."""
import itertools, json, math
from collections import Counter
import numpy as np
def tirage(N, p, q, arbre, rng):
    T = {(i, i + 1) for i in range(N - 1)} if arbre == 'chemin' else {(0, i) for i in range(1, N)}
    niv = {e for e in itertools.combinations(range(N), 2) if rng.random() < (q if e in T else p)}; dim = 1 if niv else 0
    adj = [set() for _ in range(N)]
    for a, b in niv: adj[a].add(b)                       # voisins de numero superieur
    while niv:
        suiv = set()
        for s in niv:                                    # etendre s par un sommet plus grand que son dernier ; tout le bord doit etre present
            for v in adj[s[-1]]:
                t = s + (v,)
                if all(t[:i] + t[i + 1:] in niv for i in range(len(t) - 1)) and rng.random() < p: suiv.add(t)
        if not suiv: break
        niv = suiv; dim += 1
    return dim
out = dict(N12=[], N24=[], esperances={})
for p in (0.5, 0.65, 0.8, 0.95):
    for arbre in ('chemin', 'etoile'):
        for nom, q in (('passif', p), ('privilegie', 1.0)):
            rng = np.random.default_rng([232, int(p * 100), arbre == 'etoile', q == 1.0]); c = Counter(tirage(12, p, q, arbre, rng) for _ in range(2000))
            r = dict(p=p, arbre=arbre, q=nom, frequences={str(k): v / 2000 for k, v in sorted(c.items())}, dimension_la_plus_frequente=c.most_common(1)[0][0]); out['N12'].append(r); print(json.dumps(r), flush=True)
rng = np.random.default_rng([232, 24]); c = Counter(tirage(24, 0.65, 0.65, 'chemin', rng) for _ in range(1000))
out['N24'] = dict(p=0.65, frequences={str(k): v / 1000 for k, v in sorted(c.items())}); print(json.dumps(out['N24']), flush=True)
for N in (12, 24, 40, 100, 1000):                        # nombre moyen de k-simplexes pleins, q = p : C(N, k+1) p^(2^(k+1) - 1 - (k+1))
    out['esperances'][str(N)] = {str(p): {str(k): math.comb(N, k + 1) * p ** (2 ** (k + 1) - 2 - k) for k in range(2, 8)} for p in (0.5, 0.65, 0.8)}
print(json.dumps(out['esperances']['40']['0.65'])); print(json.dumps(out['esperances']['100']['0.65'])); print(json.dumps(out['esperances']['1000']['0.65']))
json.dump(out, open('c232c.json', 'w'), indent=1)
