# Rang 2 : regle a la lettre par force brute (triangles + cotes geometriques), paliers 0..8 ; puis T24.
import time, itertools, json
import numpy as np
from noyau import *
t0 = time.time()
G4 = germe(4)
NMAX = 8
def P(*a): print(*a, flush=True)

def aretes(nodes):
    Y = np.array(nodes, dtype=np.int64); s = Y.sum(1)
    E = []; over = 0
    for i0 in range(0, len(nodes), 1500):
        G = 2 * Y[i0:i0+1500] @ Y.T - np.outer(s[i0:i0+1500], s)
        I, J = np.nonzero(G == -1)
        for i, j in zip(I, J):
            if i0 + i < j: E.append((i0 + i, j))
        G[np.arange(G.shape[0]), np.arange(i0, i0 + G.shape[0])] = -99
        over += int((G > -1).sum())
    return E, over

palier = {u: 0 for u in G4}
S = list(G4); tailles = [4]
for n in range(NMAX):
    E, over = aretes(S)
    adj = {i: set() for i in range(len(S))}
    for i, j in E: adj[i].add(j); adj[j].add(i)
    cells = [(a, b, c) for a in adj for b in adj[a] if b > a for c in adj[a] & adj[b] if c > b]
    new = []; sans = 0
    for (a, b, c) in cells:
        u, v = cotes([S[a], S[b], S[c]])
        if u not in palier and v not in palier: sans += 1
        for w in (u, v):
            if w not in palier:
                palier[w] = n + 1; new.append(w)
    P(f"S({n}): {len(S)} disques, chevauchements {over}, cellules nees {len(cells)}, sans cote ne {sans}")
    S = S + new; tailles.append(len(S))
P("tailles S(0..8):", tailles, " temps", round(time.time() - t0, 1))
P("reconnus par reduction du germe:", sum(1 for u in S if appartient(u)), "/", len(S))
E, over = aretes(S)
P("S(8): chevauchements entre disques distincts:", over, "; liens:", len(E))
idx = {u: i for i, u in enumerate(S)}
pal = [palier[u] for u in S]
adj = [set() for _ in S]
for i, j in E: adj[i].add(j); adj[j].add(i)

# liens entre disques du meme palier
same = {}
for i, j in E:
    if pal[i] == pal[j]: same[pal[i]] = same.get(pal[i], 0) + 1
P("liens entre disques du meme palier, par palier:", dict(sorted(same.items())))

# voisins par age, anneau, division des fils
couples = 0; ecarts = 0; naiss = 0; naiss_mauvaises = 0; anneau_mauvais = 0
voisins_meme_palier_lies = {"palier0": 0, "palier>=1": 0}
exemple_ecart = None
for p in range(len(S)):
    n0 = pal[p]
    Nb = adj[p]
    for g in range(0, NMAX - n0 + 1):
        c = sum(1 for q in Nb if pal[q] <= n0 + g)
        couples += 1
        if c != 3 * 2 ** g:
            ecarts += 1
            if exemple_ecart is None: exemple_ecart = (S[p], g, c)
    for q in Nb:
        for r in Nb:
            if q < r and pal[q] == pal[r] and r in adj[q]:
                voisins_meme_palier_lies["palier0" if pal[q] == 0 else "palier>=1"] += 1
    # pourtour
    init = [q for q in Nb if pal[q] <= n0]
    if len(init) != 3 or not all(b in adj[a] for a, b in itertools.combinations(init, 2)):
        anneau_mauvais += 1; continue
    cyc = init[:]
    for k in range(n0 + 1, NMAX + 1):
        nouveaux = [x for x in Nb if pal[x] == k]
        L = len(cyc)
        pos = {q: t for t, q in enumerate(cyc)}
        insert = {}
        for x in nouveaux:
            naiss += 1
            anc = [q for q in Nb if pal[q] < k and q in adj[x]]
            ok = len(anc) == 2 and anc[1] in adj[anc[0]]
            if ok:
                a, b = pos.get(anc[0]), pos.get(anc[1])
                ok = a is not None and b is not None and ((a - b) % L in (1, L - 1))
            if not ok:
                naiss_mauvaises += 1; continue
            e = (a, b) if (b - a) % L == 1 else (b, a)
            if e in insert: naiss_mauvaises += 1
            insert[e] = x
        if len(insert) != L:
            anneau_mauvais += 1; break
        nc = []
        for t in range(L):
            nc.append(cyc[t]); nc.append(insert[(t, (t + 1) % L)])
        cyc = nc
P(f"couples (disque, age) : {couples} ; ecarts a 3 x 2^g : {ecarts} ; exemple : {exemple_ecart}")
P(f"naissances de voisins (p, x) : {naiss} ; ne divisant pas exactement un fil du pourtour : {naiss_mauvaises} ; disques dont le pourtour ne double pas a chaque palier : {anneau_mauvais}")
P("paires de voisins d'un meme disque, liees, nees au meme palier :", voisins_meme_palier_lies)
P("temps", round(time.time() - t0, 1), "s")
