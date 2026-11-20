#!/usr/bin/env python3
"""C-235c -- controle NON AVEUGLE (declare : l'enonce etait dans la passation lue) de la proposition C-235-T1 de ChatGPT : pour S = a * somme sur les liens de f(t_e)
- b * somme (deg - deg moyen)^2, avec a > 0, b >= 0, f croissante et f(n-2) > 0, le graphe complet est l'unique maximiseur. Enumeration de tous les graphes a n = 4, 5, 6
pour quatre fonctions f et deux valeurs de b. Argument : S <= a |E| f(n-2) <= a C(n,2) f(n-2), egalite seulement pour le graphe complet. Claude, 20 novembre 2026."""
import itertools, json
F = dict(t=lambda t: t, t_plus_1=lambda t: t + 1, t_carre_moins_1=lambda t: t * t - 1, constante=lambda t: 1)
out = []
for n in (4, 5, 6):
    P = list(itertools.combinations(range(n), 2)); m = len(P)
    for nom, f in F.items():
        if f(n - 2) <= 0: continue
        for b in (0.0, 0.5):
            best = None; ex = []
            for mask in range(1 << m):
                A = [0] * n
                for i, (u, v) in enumerate(P):
                    if mask >> i & 1: A[u] |= 1 << v; A[v] |= 1 << u
                s = sum(f(bin(A[u] & A[v]).count('1')) for i, (u, v) in enumerate(P) if mask >> i & 1)
                d = [bin(x).count('1') for x in A]; mo = sum(d) / n; s -= b * sum((x - mo) ** 2 for x in d)
                if best is None or s > best + 1e-12: best, ex = s, [mask]
                elif abs(s - best) <= 1e-12: ex.append(mask)
            r = dict(n=n, f=nom, b=b, graphes=1 << m, maximum=best, maximiseurs=len(ex), complet_seul=(ex == [(1 << m) - 1])); out.append(r); print(json.dumps(r), flush=True)
json.dump(out, open('c235c.json', 'w'), indent=1)
