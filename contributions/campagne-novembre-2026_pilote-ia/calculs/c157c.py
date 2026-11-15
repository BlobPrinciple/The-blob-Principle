#!/usr/bin/env python3
"""C-157c -- la regle "les plus anciens d'abord" sur le tore de Kuhn 6x6x6 (Claude, 15 novembre 2026). Predictions : c157c_prediction.txt."""
import itertools, json, math, sys
TH = math.acos(1 / 3); C = 6 * TH - 2 * math.pi
def tore(n, idx):
    T = []
    for p in itertools.product(range(n), repeat=3):
        for perm in itertools.permutations(range(3)):
            q = list(p); t = [idx(*[c % n for c in q])]
            for a in perm:
                q[a] += 1; t.append(idx(*[c % n for c in q]))
            T.append(tuple(sorted(t)))
    return T
def run(idx, nmax=1600, points=(0, 100, 220, 420, 600, 1000, 1512, 1600)):
    n = 6; T = set(tore(n, idx)); age = {v: 0 for v in range(n ** 3)}; inc = {}
    for t in T:
        for e in itertools.combinations(t, 2): inc.setdefault(e, set()).add(t)
    res = {}; N0 = n ** 3; ages_divises = {}
    def releve(t):
        k = [len(v) for v in inc.values()]
        res[t] = dict(N0=N0, N1=len(inc), N3=len(T), rapport=len(T) / N0, somme_par_porteur=(2 * math.pi * N0 - C * len(T)) / N0, k_max=max(k), k_min=min(k),
                      deficit_min_deg=math.degrees(2 * math.pi - max(k) * TH))
    releve(0)
    for t in range(1, nmax + 1):
        e = min(inc, key=lambda x: (max(age[x[0]], age[x[1]]), min(age[x[0]], age[x[1]]), x[0], x[1]))
        key = (age[e[0]] == 0) + (age[e[1]] == 0); ages_divises[key] = ages_divises.get(key, 0) + 1
        a, b = e; m = N0; N0 += 1; age[m] = t
        for old in list(inc[e]):
            T.discard(old)
            for x in itertools.combinations(old, 2):
                inc[x].discard(old)
                if not inc[x]: del inc[x]
            for rep in (a, b):
                new = tuple(sorted(m if v == rep else v for v in old)); T.add(new)
                for x in itertools.combinations(new, 2): inc.setdefault(x, set()).add(new)
        if t in points: releve(t)
    res['fils_divises_selon_le_nombre_de_bouts_d_age_zero'] = ages_divises
    return res
out = {'x*36+y*6+z': run(lambda x, y, z: x * 36 + y * 6 + z), 'z*36+y*6+x': run(lambda x, y, z: z * 36 + y * 6 + x)}
json.dump(out, open('c157c.json', 'w'), indent=1)
for nom, r in out.items():
    print(nom)
    for t, v in r.items():
        print('  ', t, v if not isinstance(v, dict) or 'rapport' not in v else {k: (round(x, 6) if isinstance(x, float) else x) for k, x in v.items()})
