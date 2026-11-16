#!/usr/bin/env python3
"""C-178c -- RO-24, option economique de l'armature : mitose (un sommet engendre un sommet) + echange d'aretes de A_Gibbs a nombre d'aretes fixe, version abstraite
(Claude, 16 novembre 2026). Predictions : c178c_prediction.txt (ecrites avant). Usage : python3 c178c.py <tau> <graine debut> <graine fin> <etiquette>"""
import itertools, json, math, sys
import numpy as np

BETA = 0.30; NMAX = 30


def S_sim(A):
    deg = A.sum(1); ntri = int(round(np.trace(A @ A @ A) / 6)); m = deg.mean(); D = deg.std() / m if m > 0 else 0.0
    return math.log(1 + ntri) - BETA * D, ntri


def composantes(A):
    n = len(A); vu = [False] * n; c = 0
    for s in range(n):
        if vu[s]: continue
        c += 1; pile = [s]; vu[s] = True
        while pile:
            x = pile.pop()
            for y in np.nonzero(A[x])[0]:
                if not vu[y]: vu[y] = True; pile.append(y)
    return c


def mesure(A):
    n = len(A); E = int(A.sum() // 2); c = composantes(A); ntri = int(round(np.trace(A @ A @ A) / 6)); K4 = [q for q in itertools.combinations(range(n), 4) if all(A[a, b] for a, b in itertools.combinations(q, 2))]
    ne = {}
    for q in K4:
        for e in itertools.combinations(q, 2): ne[e] = ne.get(e, 0) + 1
    cl = 0; deg = A.sum(1)
    for k in range(min(n, 12), 1, -1):
        if any(all(A[a, b] for a, b in itertools.combinations(q, 2)) for q in itertools.combinations([v for v in range(n) if deg[v] >= k - 1], k)): cl = k; break
    return dict(N=n, aretes=E, composantes=c, b1=E - n + c, triangles=ntri, tetraedres=len(K4), isoles=int((deg == 0).sum()), n_e=sorted(ne.values()), plus_grande_clique=cl, identite=bool(E == n - 1 and E - n + c == c - 1))


def trajectoire(seed, tau):
    rng = np.random.Generator(np.random.PCG64(seed)); A = np.zeros((1, 1), int); L = []
    while len(A) < NMAX:
        n = len(A); v0 = int(rng.integers(n)); B = np.zeros((n + 1, n + 1), int); B[:n, :n] = A; B[v0, n] = B[n, v0] = 1; A = B; n += 1
        s, _ = S_sim(A)
        for _ in range(200 * n):
            ed = np.argwhere(np.triu(A, 1)); ne_ = np.argwhere(np.triu(1 - A, 1))
            if len(ed) == 0 or len(ne_) == 0: break
            a, b = ed[rng.integers(len(ed))]; c, d = ne_[rng.integers(len(ne_))]
            A[a, b] = A[b, a] = 0; A[c, d] = A[d, c] = 1; s2, _ = S_sim(A)
            if math.log(rng.random()) < n * (s2 - s) / tau: s = s2
            else: A[a, b] = A[b, a] = 1; A[c, d] = A[d, c] = 0
        L.append(mesure(A))
    return L


if __name__ == '__main__':
    tau, a, b, lab = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]; out = {}
    for seed in range(a, b):
        out[seed] = trajectoire(seed, tau); f = out[seed][-1]; json.dump(out, open(f'c178c_{lab}_{a}.json', 'w'))
        print(seed, 'N', f['N'], 'comp', f['composantes'], 'b1', f['b1'], 'tri', f['triangles'], 'tetra', f['tetraedres'], 'isoles', f['isoles'], 'clique', f['plus_grande_clique'], 'n_e med', (np.median(f['n_e']) if f['n_e'] else None), flush=True)
