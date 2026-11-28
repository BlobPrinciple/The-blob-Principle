#!/usr/bin/env python3
"""Contrôle indépendant des pages 1886 (V341, « FK-LOCAL-FLAT ») et 1875 (V338, théorème E/T).

Phase de Frank–Kasper A15 (type Cr3Si, groupe Pm-3n), positions idéales :
  2a : (0,0,0), (1/2,1/2,1/2)
  6c : (1/4,0,1/2), (3/4,0,1/2), (1/2,1/4,0), (1/2,3/4,0), (0,1/2,1/4), (0,1/2,3/4)
On construit la triangulation de Delaunay périodique du revêtement m x m x m (m = 3 puis 4),
sans aucune donnée du corpus, et l'on compte : sommets, arêtes, triangles, tétraèdres,
caractéristique d'Euler, degrés d'arêtes (nombre de tétraèdres autour de chaque arête),
non-dégénérescence (aucun cinquième point sur une sphère circonscrite),
puis les deux énergies du théorème V338 : avec q = degré - 1 et, par tétraèdre,
ses trois paires d'arêtes opposées (e, e'),
  T = somme (q_e - q_e')^2,  E = somme (s_i - moyenne(s))^2 où s_i = q_e + q_e',
et l'anisotropie delta = 1/2 - (3/4) E/T.
Valeurs écrites par le master pour m = 3 : N0 = 216, N1 = 1458, N2 = 2484, N3 = 1242,
degrés {5 : 1296, 6 : 162}, E = 864, T = 648, E/T = 4/3, delta = -1/2.
"""
import itertools
from collections import Counter
from fractions import Fraction
import numpy as np
from scipy.spatial import Delaunay, cKDTree

BASE = np.array([(0, 0, 0), (.5, .5, .5),
                 (.25, 0, .5), (.75, 0, .5), (.5, .25, 0), (.5, .75, 0), (0, .5, .25), (0, .5, .75)])
DECAL = np.array(list(itertools.product((-1.0, 0.0, 1.0), repeat=3)))

def a15(m):
    cells = np.array(list(itertools.product(range(m), repeat=3)), dtype=float)
    return (cells[:, None, :] + BASE[None, :, :]).reshape(-1, 3)

def triangulation(p, m):
    n = len(p)
    tous = (p[None, :, :] + m * DECAL[:, None, :]).reshape(-1, 3)
    d = Delaunay(tous)
    bary = tous[d.simplices].mean(axis=1)
    dedans = np.all((bary >= -1e-9) & (bary < m - 1e-9), axis=1)
    tets = {tuple(sorted(int(v) % n for v in s)) for s in d.simplices[dedans]}
    # non-dégénérescence : aucun autre point sur la sphère circonscrite
    x = tous[d.simplices[dedans]]
    a = 2.0 * (x[:, 1:, :] - x[:, 0:1, :]); b = (x[:, 1:, :] ** 2).sum(2) - (x[:, 0:1, :] ** 2).sum(2)
    cc = np.linalg.solve(a, b[..., None])[..., 0]
    r = np.linalg.norm(cc - x[:, 0, :], axis=1)
    arbre = cKDTree(tous)
    sur_sphere = [len(arbre.query_ball_point(c, rr + 1e-7)) for c, rr in zip(cc, r)]
    return sorted(tets), Counter(sur_sphere), (r.min(), r.max())

def bilan(m):
    p = a15(m)
    tets, sph, (rmin, rmax) = triangulation(p, m)
    aretes, faces = Counter(), Counter()
    for t in tets:
        for e in itertools.combinations(t, 2): aretes[e] += 1
        for f in itertools.combinations(t, 3): faces[f] += 1
    n0, n1, n2, n3 = len(p), len(aretes), len(faces), len(tets)
    print(f"m = {m} : N0 = {n0}, N1 = {n1}, N2 = {n2}, N3 = {n3}, Euler = {n0 - n1 + n2 - n3}")
    print(f"   N1 = N0 + N3 : {n1 == n0 + n3} ; N2 = 2 N3 : {n2 == 2 * n3} ; triangles dans exactement 2 tétraèdres : {sum(v == 2 for v in faces.values())}/{n2}")
    print(f"   points sur chaque sphère circonscrite (4 = non dégénéré) : {dict(sph)} ; rayons de {rmin:.6f} à {rmax:.6f}")
    print(f"   degrés d'arêtes : {dict(sorted(Counter(aretes.values()).items()))} ; coordination moyenne = {Fraction(6 * n3, n1)} = {6 * n3 / n1:.6f}")
    # bilan par sommet : somme des (6 - degré) sur les arêtes d'un sommet (« GAUSS-12 »)
    charge = Counter()
    for (u, v), d in aretes.items():
        charge[u] += 6 - d; charge[v] += 6 - d
    print(f"   somme par sommet de (6 - degré) : {dict(Counter(charge.values()))}")
    voisins = Counter()
    for (u, v) in aretes: voisins[u] += 1; voisins[v] += 1
    print(f"   nombre de voisins par sommet : {dict(sorted(Counter(voisins.values()).items()))}")
    E = T = Fraction(0); types = Counter()
    for t in tets:
        a, b, c, d = t
        paires = [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]
        q = [(aretes[tuple(sorted(e))] - 1, aretes[tuple(sorted(f))] - 1) for e, f in paires]
        s = [Fraction(x + y) for x, y in q]; sm = sum(s) / 3
        T += sum((x - y) ** 2 for x, y in q); E += sum((si - sm) ** 2 for si in s)
        k = sum(aretes[e] == 6 for e in itertools.combinations(t, 2))
        opp = any(x == 5 and y == 5 for x, y in q)
        types[(k, 'opposées' if opp else '-')] += 1
    print(f"   tétraèdres par nombre d'arêtes de degré 6 : {dict(sorted(types.items()))}")
    print(f"   E = {E}, T = {T}, E/T = {E / T}, delta = 1/2 - (3/4) E/T = {Fraction(1, 2) - Fraction(3, 4) * E / T}")
    x56 = sum((6 - d) * (6 - d - 1) for d in aretes.values())
    print(f"   X56 = somme c(c-1) avec c = 6 - degré : {x56}")

if __name__ == "__main__":
    for m in (3, 4):
        bilan(m)
    import math
    ds = 2 * math.pi / math.acos(1 / 3)
    print(f"cible plate d* = 2 pi / arccos(1/3) = {ds:.6f} ; A15 : 138/27 = {138/27:.6f} ; écart relatif {138/27/ds - 1:+.4%}")
