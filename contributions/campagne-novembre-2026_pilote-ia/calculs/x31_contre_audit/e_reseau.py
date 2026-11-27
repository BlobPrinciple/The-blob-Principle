# T25 : (1) regle sur le reseau triangulaire seul ; (2) decompte compare a (g+1)(g+2) + [3|g] ;
# (3) palier 7 de l'empilement par force brute (S(7)) pour prolonger la suite des voisins communs.
import itertools, time, pickle
import numpy as np
from noyau import *
t0 = time.time()
def P(*a): print(*a, flush=True)

# (1) reseau : points (i,j,k) de somme 1 ; voisins : differer d'une permutation de (1,-1,0)
R = 40
pts = [(i, j, 1 - i - j) for i in range(-R, R + 1) for j in range(-R, R + 1) if abs(1 - i - j) <= R]
ps = set(pts)
D = [d for d in itertools.permutations((1, -1, 0))]
def vois(x): return [tuple(a + b for a, b in zip(x, d)) for d in D]
# regle : un point nait au tour n+1 des que deux de ses voisins, lies entre eux, sont nes au tour n au plus
age = {(1, 0, 0): 0, (0, 1, 0): 0, (0, 0, 1): 0}
for n in range(0, 30):
    new = []
    for x in pts:
        if x in age: continue
        V = [y for y in vois(x) if y in age]
        if any(sorted(a - b for a, b in zip(u, v)) == [-1, 0, 1] for u, v in itertools.combinations(V, 2)):
            new.append(x)
    for x in new: age[x] = n + 1
ecarts = sum(1 for x, a in age.items() if a != max(x) - min(x) - 1)
P("reseau : points dates", len(age), "jusqu'au tour 30 ; age != etendue - 1 :", ecarts)
# (2) decompte
bad = []
for g in range(0, 301):
    E = g + 1
    # points de somme 1 et d'etendue <= E : min m >= -E, max <= m + E
    c = 0
    for m in range(-E - 1, 2):
        for i in range(m, m + E + 1):
            for j in range(m, m + E + 1):
                k = 1 - i - j
                if m <= k <= m + E and min(i, j, k) == m: c += 1
    f = (g + 1) * (g + 2) + (1 if g % 3 == 0 else 0)
    if c != f: bad.append((g, c, f))
    if g <= 9: P(f"g={g}: points d'etendue <= g+1 : {c} ; formule {f}")
P("g = 0..300 : ecarts a la formule :", bad)

# (3) S(7) par force brute
d = pickle.load(open("/home/claude/audit_x31/rang3_S6.pkl", "rb"))
palier = dict(d["palier"])
S6 = [u for u in palier]
Y = np.array(S6, dtype=np.int64); s = Y.sum(1)
adj = [set() for _ in S6]
for i0 in range(0, len(S6), 1000):
    G = 2 * Y[i0:i0+1000] @ Y.T - np.outer(s[i0:i0+1000], s)
    I, J = np.nonzero(G == -1)
    for i, j in zip(I, J): adj[i0 + i].add(j)
ncell = 0
for a in range(len(S6)):
    Na = {b for b in adj[a] if b > a}
    for b in Na:
        Nab = {c for c in adj[b] if c in Na and c > b}
        for c in Nab:
            for e in adj[c]:
                if e in Nab and e > c:
                    ncell += 1
                    for w in cotes([S6[a], S6[b], S6[c], S6[e]]):
                        if w not in palier: palier[w] = 7
P("S(6) : cellules nees", ncell, "; taille de S(7) :", len(palier), " temps", round(time.time() - t0, 1))
S7 = list(palier); Y7 = np.array(S7, dtype=np.int64); s7 = Y7.sum(1); pal = np.array([palier[u] for u in S7])
for i, j in itertools.combinations(range(5), 2):
    gi = 2 * Y7[:, i] - s7; gj = 2 * Y7[:, j] - s7
    idx = np.nonzero((gi == -1) & (gj == -1))[0]
    oth = [k for k in range(5) if k not in (i, j)]
    ec = sum(1 for t in idx if palier[S7[t]] != max(S7[t][k] for k in oth) - min(S7[t][k] for k in oth) - 1)
    P(f"fil (e{i+1},e{j+1}) : voisins communs nes aux paliers 0..7 (cumules) {[int((pal[idx] <= k).sum()) for k in range(8)]} ; palier != etendue-1 : {ec}")
g = 2 * Y7[:, 0] - s7
P("voisins nes de e1 aux paliers 0..7 (cumules):", [int(((g == -1) & (pal <= k)).sum()) for k in range(8)])
P("temps", round(time.time() - t0, 1), "s")
