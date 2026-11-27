# Regle a la lettre au rang 3 par force brute (cliques de 4 + cotes geometriques), paliers 0..6,
# temoin de la descente contre un parcours en largeur des tuiles, puis A1, A3, T23, T25, T26, (g).
import sys, time, pickle, itertools, json
import numpy as np
from noyau import *

t0 = time.time()
G5 = germe(5)
GT = frozenset(G5)
def P(*a):
    print(*a, flush=True)

# ---------- temoin : parcours en largeur des tuiles ----------
D = 7
prof = {GT: 0}
front = [GT]
for d in range(1, D + 1):
    nf = []
    for T in front:
        L = list(T)
        for i in range(5):
            w = retourne(L, i)
            U = frozenset(L[:i] + [w] + L[i + 1:])
            if U not in prof:
                prof[U] = d; nf.append(U)
    front = nf
P("BFS tuiles par profondeur:", [sum(1 for v in prof.values() if v == d) for d in range(D + 1)])
# critere : retourner v diminue la profondeur <=> somme du retourne < somme de v (tuiles de profondeur <= D-1)
bad = 0; nchk = 0; egal = 0
for T, d in prof.items():
    if d > D - 1: continue
    L = list(T)
    for i in range(5):
        w = retourne(L, i)
        U = frozenset(L[:i] + [w] + L[i + 1:])
        dd = prof[U]
        nchk += 1
        if sum(w) == sum(L[i]): egal += 1
        if (dd < d) != (sum(w) < sum(L[i])) or abs(dd - d) != 1: bad += 1
P("temoin critere de descente: controles", nchk, "desaccords", bad, "egalites de somme", egal)
# tuile-porte par BFS (tuile de profondeur min contenant u) vs descente, pour u dont toutes les tuiles proches sont vues
best = {}
for T, d in prof.items():
    for u in T:
        if u not in best or d < best[u][0]:
            best[u] = (d, [T])
        elif d == best[u][0]:
            best[u][1].append(T)
bad2 = 0; n2 = 0; nonuniq = 0
for u, (d, Ts) in best.items():
    if d > D - 2: continue   # sa vraie porte est forcement de profondeur <= d, vue
    n2 += 1
    if len(Ts) > 1: nonuniq += 1
    if descente(list(Ts[0]), {u}) != Ts[0]: bad2 += 1
P("temoin tuile-porte: constituants", n2, "porte par descente != porte BFS:", bad2, "portes non uniques:", nonuniq)
# paire : T0(p,q) par BFS vs descente
bad3 = 0; n3 = 0
bestp = {}
for T, d in prof.items():
    for p, q in itertools.combinations(sorted(T), 2):
        k = (p, q)
        if k not in bestp or d < bestp[k][0]:
            bestp[k] = (d, T)
for (p, q), (d, T) in bestp.items():
    if d > D - 2: continue
    n3 += 1
    if descente(list(T), {p, q}) != T: bad3 += 1
P("temoin tuile de paire: paires", n3, "desaccords:", bad3)
del prof, best, bestp

# ---------- regle a la lettre, force brute ----------
def cliques4(nodes, adj):
    idx = {u: i for i, u in enumerate(nodes)}
    out = []
    for a in nodes:
        Na = {b for b in adj[a] if idx[b] > idx[a]}
        for b in Na:
            Nab = {c for c in adj[b] if c in Na and idx[c] > idx[b]}
            for c in Nab:
                for d in adj[c]:
                    if d in Nab and idx[d] > idx[c]:
                        out.append((a, b, c, d))
    return out

def adjacence(nodes):
    Y = np.array(nodes, dtype=np.int64)
    s = Y.sum(1)
    Gm = 2 * Y @ Y.T - np.outer(s, s)
    adj = {u: set() for u in nodes}
    I, J = np.nonzero(Gm == -1)
    for i, j in zip(I, J):
        adj[nodes[i]].add(nodes[j])
    over = int(((Gm > -1) & (~np.eye(len(nodes), dtype=bool))).sum())
    return adj, over

palier = {u: 0 for u in G5}
tuile_de = {u: GT for u in G5}
S = list(G5)
tailles = [len(S)]
cells_par_n = {}
for n in range(0, 6):
    adj, over = adjacence(S)
    cells = cliques4(S, adj)
    cells_par_n[n] = cells
    nouveaux = []
    sans_cote = 0; cote_seul_loin = 0
    for c in cells:
        u, v = cotes(list(c))
        nu, nv = (u in palier), (v in palier)
        if not nu and not nv: sans_cote += 1
        if nu != nv:
            ne = u if nu else v; autre = v if nu else u
            if sum(ne) > sum(autre): cote_seul_loin += 1
        for w in (u, v):
            if w not in palier:
                palier[w] = n + 1; tuile_de[w] = frozenset(c + (w,)); nouveaux.append(w)
    S = S + nouveaux
    tailles.append(len(S))
    P(f"S({n}) : {len(S)-len(nouveaux)} constituants, chevauchements {over}, cellules nees {len(cells)}, sans cote ne {sans_cote}, cote ne seul cote loin {cote_seul_loin}")
P("tailles S(0..6):", tailles, "  temps", round(time.time() - t0, 1))
memb = sum(1 for u in palier if appartient(u)); P("constituants reconnus par reduction du germe:", memb, "/", len(palier))

# portes et parents
porte = {}
for u in palier:
    porte[u] = GT if u in GT else descente(list(tuile_de[u]), {u})
parents = {u: (frozenset() if u in GT else porte[u] - {u}) for u in palier}
# T7 (controle) : palier = 1 + max palier parents
t7 = sum(1 for u in palier if u not in GT and palier[u] != 1 + max(palier.get(q, 99) for q in parents[u]))
P("controle T7 (palier = 1 + max palier des parents) : ecarts", t7, "parents hors S(6):", sum(1 for u in palier for q in parents[u] if q not in palier))

def T0(p, x, T):
    return descente(list(T), {p, x})

# ---------- A1 : T20 sous la regle a la lettre ----------
Sall = list(palier)
Y6 = np.array(Sall, dtype=np.int64); s6 = Y6.sum(1)
pal_arr = np.array([palier[u] for u in Sall])
def tuile_contenant(p, x):
    # une tuile contenant p et x : la porte de x si p y est, sinon on remonte la descente de x en gardant p
    for T in (porte[x], porte[p], tuile_de[x], tuile_de[p]):
        if p in T and x in T: return T
    # sinon : parcours dans le residu de x jusqu'a trouver p
    seen = {porte[x]}; fr = [porte[x]]
    for _ in range(8):
        nf = []
        for T in fr:
            L = list(T)
            for i in range(5):
                if L[i] == x: continue
                w = retourne(L, i); U = frozenset(L[:i] + [w] + L[i + 1:])
                if U in seen: continue
                if p in U: return U
                seen.add(U); nf.append(U)
        fr = nf
    return None

res_A1 = {}
for n in (2, 3, 4):
    born = {u for u in Sall if palier[u] <= n}
    idxP = np.nonzero(pal_arr <= n)[0]; idxX = np.nonzero((pal_arr > n) & (pal_arr <= n + 2))[0]
    Gm = 2 * Y6[idxP] @ Y6[idxX].T - np.outer(s6[idxP], s6[idxX])
    I, J = np.nonzero(Gm == -1)
    cnt = {"paires": 0, "parent": 0, "cousin": 0, "exception": 0, "les_deux": 0, "sans_tuile": 0}
    for i, j in zip(I, J):
        p = Sall[idxP[i]]; x = Sall[idxX[j]]
        cnt["paires"] += 1
        isp = p in parents[x]
        T = tuile_contenant(p, x)
        isc = False
        if T is None:
            cnt["sans_tuile"] += 1
        else:
            T0px = T0(p, x, T); abc = T0px - {p, x}
            if all(a in born for a in abc):
                xp = tuple(a - b for a, b in zip(add(p, *abc), x))
                if xp in born and parents[p] == frozenset(abc | {xp}):
                    isc = True
        if isp and isc: cnt["les_deux"] += 1
        if isp: cnt["parent"] += 1
        elif isc: cnt["cousin"] += 1
        else: cnt["exception"] += 1
    res_A1[n] = cnt
    P(f"A1 n={n}:", json.dumps(cnt))

# ---------- T23 : nombre de voisins deja nes d'un nouveau-ne ----------
for k in range(1, 7):
    born_prev = np.nonzero(pal_arr < k)[0]; newk = np.nonzero(pal_arr == k)[0]
    Gm = 2 * Y6[newk] @ Y6[born_prev].T - np.outer(s6[newk], s6[born_prev])
    deg = (Gm == -1).sum(1)
    Gs = 2 * Y6[newk] @ Y6[newk].T - np.outer(s6[newk], s6[newk])
    degs = (Gs == -1).sum(1)
    P(f"T23 palier {k}: nouveau-nes {len(newk)}; voisins nes avant (min,max) = ({deg.min()},{deg.max()}); nombre avec >4 : {(deg>4).sum()}; voisins nes au meme palier (max) {degs.max()}")

# ---------- T26 / B4 ----------
for k in range(1, 7):
    idx = np.nonzero(pal_arr == k)[0]
    Gs = 2 * Y6[idx] @ Y6[idx].T - np.outer(s6[idx], s6[idx])
    I, J = np.nonzero(np.triu(Gs == -1, 1))
    cous = 0; autres = 0
    for i, j in zip(I, J):
        p = Sall[idx[i]]; q = Sall[idx[j]]
        if p not in parents[q] and q not in parents[p] and len(parents[p] & parents[q]) == 3: cous += 1
        else: autres += 1
    P(f"T26 palier {k}: paires liees de meme palier {len(I)}, cousines {cous}, autres {autres}")

# ---------- (g) voisins d'un constituant du germe ----------
for i in range(5):
    e = G5[i]
    g = 2 * Y6 @ np.array(e) - s6 * 1
    cum = [int(((g == -1) & (pal_arr <= k)).sum()) for k in range(7)]
    P(f"(g) voisins nes de e{i+1} aux paliers 0..6 (cumules):", cum)

# ---------- T25 : voisins communs des dix fils du germe ----------
toutes_ok = True
for i, j in itertools.combinations(range(5), 2):
    gi = 2 * Y6[:, i] - s6; gj = 2 * Y6[:, j] - s6
    idx = np.nonzero((gi == -1) & (gj == -1))[0]
    cum = [int((pal_arr[idx] <= k).sum()) for k in range(7)]
    oth = [k for k in range(5) if k not in (i, j)]
    ecarts = 0; somme_pas_1 = 0; liens_faux = 0
    pts = []
    for t in idx:
        u = Sall[t]; tr = tuple(u[k] for k in oth)
        if sum(tr) != 1: somme_pas_1 += 1
        if palier[u] != max(tr) - min(tr) - 1: ecarts += 1
        pts.append((u, tr))
    for (u, a), (v, b) in itertools.combinations(pts, 2):
        d = sorted(x - y for x, y in zip(a, b))
        lie = (ip(u, v) == -1)
        if lie != (d == [-1, 0, 1]): liens_faux += 1
    if ecarts or somme_pas_1 or liens_faux: toutes_ok = False
    P(f"T25 fil (e{i+1},e{j+1}): cumules paliers 0..6 {cum}; triplet=coord. des 3 autres: somme!=1 {somme_pas_1}, palier!=etendue-1 {ecarts}, liens mal decrits {liens_faux}")
P("T25 tout conforme:", toutes_ok)

pickle.dump({"palier": palier, "tuile_de": tuile_de}, open("/home/claude/audit_x31/rang3_S6.pkl", "wb"))
P("temps total", round(time.time() - t0, 1), "s")
