#!/usr/bin/env python3
"""BP-EQ2 (ChatGPT, 13 novembre 2026) -- contre-verification independante (Claude).
Coques fermees : ensembles de triangles sur n sommets etiquetes, chaque arete dans exactement deux triangles,
connexes, tous les sommets utilises, V - E + F = 2.
Attendu, ecrit avant execution : 0, 1, 10 pour n = 3, 4, 5 (ChatGPT) ; 195 pour n = 6 (15 octaedres + 180, prediction de Claude)."""
import itertools
import json
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
res = {}
for n in (3, 4, 5, 6):
    tris = list(itertools.combinations(range(n), 3))
    aretes = list(itertools.combinations(range(n), 2))
    ia = {e: k for k, e in enumerate(aretes)}
    te = [[ia[e] for e in itertools.combinations(t, 2)] for t in tris]
    compte = 0
    tailles = {}
    for masque in range(1, 1 << len(tris)):
        F = bin(masque).count('1')
        if F != 2 * n - 4:
            continue                                   # 3F = 2E et Euler imposent F = 2V - 4 quand tous les sommets servent
        deg = [0] * len(aretes)
        sommets = set()
        choisis = [t for b, t in enumerate(tris) if masque >> b & 1]
        ok = True
        for b, t in enumerate(tris):
            if masque >> b & 1:
                sommets.update(t)
                for e in te[b]:
                    deg[e] += 1
                    if deg[e] > 2:
                        ok = False
        if not ok or len(sommets) != n or any(d == 1 for d in deg):
            continue
        E = sum(1 for d in deg if d == 2)
        if n - E + F != 2:
            continue
        vus, pile = {choisis[0]}, [choisis[0]]         # connexite par aretes communes
        while pile:
            t = pile.pop()
            for u in choisis:
                if u not in vus and len(set(t) & set(u)) == 2:
                    vus.add(u)
                    pile.append(u)
        if len(vus) != F:
            continue
        compte += 1
    res[n] = compte
(ICI / 'bp_eq2_contre_audit.json').write_text(json.dumps(res))
print(res)
