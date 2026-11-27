# Tissus clos par plancher construits au hasard (ajout un a un d'un constituant non ne dont les quatre parents sont nes),
# puis T20, T21 (places trouvees par resolution directe, sans (C*)), T22, et le nombre de cellules creees par une naissance (T23).
import sys, time, random, itertools, json
import numpy as np
from noyau import *

G5 = germe(5); GT = frozenset(G5)
GENMAX = 9
M = 2 * np.eye(5) - np.ones((5, 5))
_porte = {}
def porte(u, T):
    if u in GT: return GT
    if u not in _porte: _porte[u] = descente(list(T), {u})
    return _porte[u]
def parents(u, T=None):
    if u in GT: return frozenset()
    return porte(u, T) - {u}

def construit(N, rng, mode):
    born = list(G5); B = set(G5); gen = {u: 0 for u in G5}; tile = {u: GT for u in G5}
    adj = {u: set(G5) - {u} for u in G5}
    cells = set(frozenset(c) for c in itertools.combinations(G5, 4))
    sides = {}
    while len(born) < N:
        cand = {}
        for c in cells:
            if c not in sides: sides[c] = cotes(list(c))
            for w in sides[c]:
                if w in B or w in cand: continue
                T = frozenset(c | {w})
                if parents(w, T) <= B: cand[w] = T
        cl = sorted(cand)
        gg = {w: 1 + max(gen[q] for q in parents(w)) for w in cl}
        cl = [w for w in cl if gg[w] <= GENMAX]
        if mode == "profond" and rng.random() < 0.85:
            g = {w: 1 + max(gen[q] for q in parents(w)) for w in cl}
            g = {w: v for w, v in g.items() if v <= GENMAX}
            if g:
                mx = max(g.values()); cl = [w for w in cl if g.get(w) == mx]
        w = rng.choice(cl); T = cand[w]
        gen[w] = 1 + max(gen[q] for q in parents(w)); tile[w] = T
        nb = {b for b in born if ip(w, b) == -1}
        for b in nb: adj[b].add(w)
        adj[w] = nb
        for a, b, c in itertools.combinations(sorted(nb), 3):
            if b in adj[a] and c in adj[a] and c in adj[b]:
                cells.add(frozenset((w, a, b, c)))
        born.append(w); B.add(w)
    return born, B, gen, tile, adj, cells, sides

def places_directes(born, B, adj):
    Bar = np.array(born, dtype=np.float64)
    Bint = np.array(born, dtype=np.int64); sB = Bint.sum(1)
    ent = set(); nonent = 0; nonent_libre = []; dependants = 0; quads = 0
    for p in born:
        Nb = sorted(adj[p])
        if len(Nb) < 3: continue
        tr = list(itertools.combinations(range(len(Nb)), 3))
        quads += len(tr)
        Nar = np.array(Nb, dtype=np.float64)
        tri = np.array(tr)
        V = np.concatenate([np.broadcast_to(np.array(p, dtype=np.float64), (len(tr), 1, 5)), Nar[tri]], axis=1)
        A = V @ M
        U, Sg, Vt = np.linalg.svd(A)
        ind = Sg[:, 3] > 1e-9 * Sg[:, 0]
        dependants += int((~ind).sum())
        c = np.einsum('mij,i->mj', U, -np.ones(4)) / Sg
        x0 = np.einsum('mij,mi->mj', Vt[:, :4, :], c)
        k = Vt[:, 4, :]
        qa = np.einsum('mi,ij,mj->m', k, M, k); qb = 2 * np.einsum('mi,ij,mj->m', x0, M, k); qc = np.einsum('mi,ij,mj->m', x0, M, x0) - 1
        for m in np.nonzero(ind)[0]:
            a_, b_, c_ = qa[m], qb[m], qc[m]
            ts = []
            if abs(a_) > 1e-9:
                disc = b_ * b_ - 4 * a_ * c_
                if disc < -1e-7 * max(1, abs(b_ * b_)): continue
                sq = np.sqrt(max(disc, 0.0)); ts = [(-b_ + sq) / (2 * a_), (-b_ - sq) / (2 * a_)]
            elif abs(b_) > 1e-12:
                ts = [-c_ / b_]
            for t in ts:
                x = x0[m] + t * k[m]
                xi = tuple(int(round(v)) for v in x)
                quad = [p] + [Nb[i] for i in tr[m]]
                if np.max(np.abs(x - np.array(xi))) < 1e-6 and ip(xi, xi) == 1 and all(ip(xi, v) == -1 for v in quad):
                    g = 2 * Bint @ np.array(xi) - sB * sum(xi)
                    if (g > -1).sum() == 0:      # ne chevauche aucun ne (et n'est pas ne)
                        ent.add(xi)
                else:
                    nonent += 1
                    g = 2 * Bar @ x - Bar.sum(1) * x.sum()
                    if g.max() <= -1 + 1e-7:
                        nonent_libre.append([p, list(map(float, x))])
    return ent, nonent, nonent_libre, dependants, quads

def residu(p, T0p, r):
    seen = {T0p}; fr = [T0p]; out = {}
    for T in fr:
        for x in T:
            if x != p: out.setdefault(x, T)
    for _ in range(r):
        nf = []
        for T in fr:
            L = list(T)
            for i in range(5):
                if L[i] == p: continue
                w = retourne(L, i); Uu = frozenset(L[:i] + [w] + L[i + 1:])
                if Uu in seen: continue
                seen.add(Uu); nf.append(Uu); out.setdefault(w, Uu)
        fr = nf
    return out

def analyse(born, B, gen, tile, adj, cells, sides, rayon):
    r = {}
    r["clos_par_plancher"] = all(parents(u, tile[u]) <= B for u in born)
    r["generation_max"] = max(gen.values())
    # cellules nees, cotes
    Q = {}
    sans = 0; seul_loin = 0; deux = 0
    for c in cells:
        if c not in sides: sides[c] = cotes(list(c))
        u, v = sides[c]
        nu, nv = u in B, v in B
        if not nu and not nv: sans += 1
        if nu and nv: deux += 1
        if nu != nv:
            ne, au = (u, v) if nu else (v, u)
            if sum(ne) > sum(au): seul_loin += 1
            Q.setdefault(au, frozenset(c | {au}))
    r["cellules_nees"] = len(cells); r["T22_cellules_sans_cote_ne"] = sans; r["T22_cote_ne_seul_loin_du_germe"] = seul_loin
    ent, nonent, nonent_libre, dep, quads = places_directes(born, B, adj)
    r["quadruples"] = quads; r["quadruples_dependants"] = dep
    r["places_entieres"] = len(ent); r["boules_non_entieres_liees_a_un_quadruple"] = nonent
    r["places_non_entieres_libres"] = len(nonent_libre)
    r["places_hors_empilement_entieres"] = sum(1 for x in ent if not appartient(x))
    r["T21_places_egal_cotes_non_nes"] = (ent == set(Q))
    r["places_pas_cote"] = len(ent - set(Q)); r["cotes_pas_place"] = len(set(Q) - ent)
    # plancher incomplet ; nombre de cellules creees par chaque naissance possible (T23)
    pi = 0; ncel = {}
    for x in ent:
        T = Q.get(x)
        if T is not None and not parents(x, T) <= B: pi += 1
        nb = sorted(b for b in born if ip(x, b) == -1)
        k = 0
        for a, b, c in itertools.combinations(nb, 3):
            if b in adj[a] and c in adj[a] and c in adj[b]: k += 1
        ncel[k] = ncel.get(k, 0) + 1
    r["places_plancher_incomplet"] = pi
    r["T23_cellules_creees_par_place"] = {str(k): v for k, v in sorted(ncel.items())}
    # T20 sur reservoir : residu de p de rayon 'rayon' + cotes non nes + places
    cnt = {"paires": 0, "parent": 0, "cousin": 0, "exception": 0, "les_deux": 0}
    exemples = []
    for p in born:
        R = residu(p, porte(p, tile[p]), rayon)
        for x in list(Q) + list(ent):
            if ip(x, p) == -1 and x not in R:
                R[x] = None
        for x, T in R.items():
            if x in B: continue
            if T is None:
                T = Q.get(x)
                if T is None or p not in T:
                    # chercher une tuile contenant p et x dans le residu de p de rayon plus grand
                    RR = residu(p, porte(p, tile[p]), rayon + 3)
                    T = RR.get(x)
                    if T is None:
                        cnt.setdefault("sans_tuile", 0); cnt["sans_tuile"] += 1; continue
            cnt["paires"] += 1
            isp = p in parents(x, T)
            T0 = descente(list(T), {p, x}); abc = T0 - {p, x}
            isc = False
            if abc <= B:
                xp = tuple(a - b for a, b in zip(add(p, *abc), x))
                if xp in B and parents(p) == frozenset(abc | {xp}): isc = True
            if isp and isc: cnt["les_deux"] += 1
            if isp: cnt["parent"] += 1
            elif isc: cnt["cousin"] += 1
            else:
                cnt["exception"] += 1
                if len(exemples) < 3: exemples.append([p, x])
    r["T20"] = cnt; r["T20_exemples_exception"] = exemples
    return r

if __name__ == "__main__":
    g0, g1, rayon = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tot = {}
    t0 = time.time()
    for seed in range(g0, g1 + 1):
        rng = random.Random(seed)
        N = rng.randint(40, 150)
        mode = "profond" if seed % 2 == 0 else "uniforme"
        ts = time.time()
        data = construit(N, rng, mode)
        r = analyse(*data, rayon)
        r = {"graine": seed, "mode": mode, "constituants": N, **r, "duree_s": round(time.time() - ts, 1)}
        print(json.dumps(r), flush=True)
        for k, v in r.items():
            if isinstance(v, bool): tot[k] = tot.get(k, 0) + int(v)
            elif isinstance(v, int) and k not in ("graine",): tot[k] = tot.get(k, 0) + v
        for k, v in r["T20"].items(): tot["T20_" + k] = tot.get("T20_" + k, 0) + v
        for k, v in r["T23_cellules_creees_par_place"].items(): tot["T23_" + k] = tot.get("T23_" + k, 0) + v
        tot["generation_max_max"] = max(tot.get("generation_max_max", 0), r["generation_max"])
    tot["tissus"] = g1 - g0 + 1; tot["duree_totale_s"] = round(time.time() - t0, 1)
    print("BILAN", json.dumps(tot), flush=True)
