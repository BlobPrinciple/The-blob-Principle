#!/usr/bin/env python3
"""C-179c -- RO-24, suite : source d'aretes kappa0, bras geometrique (moteur historique A_Gibbs du master) et bras abstrait local (Claude, 16 novembre 2026).
Predictions : c179c_prediction.txt (ecrites avant). Usage : python3 c179c.py G <graine> | L <graine>  -> c179c_<bras>_<graine>.json"""
import itertools, json, math, sys
import numpy as np

BETA, TAU, K0, POOL = 0.30, 0.50, 6.6, 1.6


class G:
    def __init__(s, n): s.adj = [set() for _ in range(n)]; s.ntri = 0; s.m = 0
    def n(s): return len(s.adj)
    def ajoute_sommet(s): s.adj.append(set()); return len(s.adj) - 1
    def ajoute(s, a, b): s.ntri += len(s.adj[a] & s.adj[b]); s.adj[a].add(b); s.adj[b].add(a); s.m += 1
    def retire(s, a, b): s.adj[a].discard(b); s.adj[b].discard(a); s.ntri -= len(s.adj[a] & s.adj[b]); s.m -= 1
    def S(s):
        d = np.array([len(x) for x in s.adj], float); mu = d.mean(); return math.log(1 + s.ntri) - BETA * (d.std() / mu if mu > 0 else 0.0)
    def relie(s, a, b):
        vu = {a}; pile = [a]
        while pile:
            x = pile.pop()
            for y in s.adj[x]:
                if y == b: return True
                if y not in vu: vu.add(y); pile.append(y)
        return False
    def aretes(s): return [(a, b) for a in range(len(s.adj)) for b in s.adj[a] if a < b]
    def mesure(s):
        n = len(s.adj); ne = {}; nk4 = 0
        for a, b in s.aretes():
            com = sorted(s.adj[a] & s.adj[b]); k = sum(1 for c, d in itertools.combinations(com, 2) if d in s.adj[c])
            if k: ne[(a, b)] = k
            nk4 += k
        nk4 //= 6; cl = 2 if s.m else 1
        for a in range(n):
            vois = sorted(s.adj[a])
            for k in range(min(len(vois), 9), cl - 1, -1):
                if any(all(y in s.adj[x] for x, y in itertools.combinations(q, 2)) for q in itertools.combinations(vois, k)): cl = max(cl, k + 1); break
        v = sorted(ne.values()); d = [len(x) for x in s.adj]
        return dict(N=n, aretes=s.m, degre_moyen=2 * s.m / n, triangles=s.ntri, tetraedres=nk4, tetraedres_par_sommet=nk4 / n, plus_grande_clique=cl, aretes_dans_un_tetraedre=len(v),
                    n_e_mediane=(float(np.median(v)) if v else None), n_e_moyenne=(float(np.mean(v)) if v else None), n_e_max=(v[-1] if v else None), histogramme_n_e={k: v.count(k) for k in sorted(set(v))}, degre_max=max(d), degre_min=min(d))


def metropolis(g, rng, nprop, entrant):
    s = g.S(); n = g.n(); acc = 0; suivi = []
    E = g.aretes()
    for it in range(nprop):
        i = int(rng.integers(len(E))); u, v = E[i]; ab = entrant()
        if ab is None: continue
        a, b = ab
        if a == b or b in g.adj[a] or (min(a, b), max(a, b)) == (u, v): continue
        g.retire(u, v); g.ajoute(a, b)
        ok = g.relie(u, v)
        if ok:
            s2 = g.S()
            if math.log(rng.random()) < n * (s2 - s) / TAU: s = s2; E[i] = (min(a, b), max(a, b)); acc += 1
            else: ok = False
        if not ok: g.retire(a, b); g.ajoute(u, v)
        if it % max(1, nprop // 30) == 0: suivi.append(g.ntri)
    return acc, suivi


def bras_G(seed):
    rng = np.random.Generator(np.random.PCG64(seed)); N = 300; X = rng.random((N, 3)); r = (K0 * 3 / (4 * math.pi * N)) ** (1 / 3)
    d = X[:, None] - X[None]; d -= np.round(d); D = np.linalg.norm(d, axis=2); g0 = G(N)
    for a, b in zip(*np.nonzero(np.triu(D < r, 1))): g0.ajoute(int(a), int(b))
    comp = []; vu = set()
    for a in range(N):
        if a in vu: continue
        c = {a}; pile = [a]
        while pile:
            x = pile.pop()
            for y in g0.adj[x]:
                if y not in c: c.add(y); pile.append(y)
        vu |= c; comp.append(c)
    big = sorted(max(comp, key=len)); idx = {v: i for i, v in enumerate(big)}; g = G(len(big))
    for a, b in g0.aretes():
        if a in idx and b in idx: g.ajoute(idx[a], idx[b])
    Dg = D[np.ix_(big, big)]; pool = [np.nonzero((Dg[i] < POOL * r) & (np.arange(len(big)) != i))[0] for i in range(len(big))]; ini = g.mesure()
    def entrant():
        a = int(rng.integers(g.n()))
        if len(pool[a]) == 0: return None
        return a, int(pool[a][rng.integers(len(pool[a]))])
    acc, suivi = metropolis(g, rng, 150 * g.m, entrant); fin = g.mesure()
    out = dict(bras='G', graine=seed, rayon=r, sommets_retenus=len(big), initial=ini, final=fin, acceptes=acc, propositions=150 * g.m, suivi_triangles=suivi, derive_dernier_tiers=(suivi[-1] - suivi[len(suivi) * 2 // 3]) / max(1, suivi[-1]))
    json.dump(out, open(f'c179c_G_{seed}.json', 'w')); print('G', seed, 'initial', {k: ini[k] for k in ('N', 'aretes', 'triangles', 'tetraedres', 'plus_grande_clique', 'n_e_mediane')}, 'final', {k: fin[k] for k in ('triangles', 'tetraedres', 'plus_grande_clique', 'n_e_mediane', 'n_e_moyenne', 'n_e_max')}, 'derive', out['derive_dernier_tiers'], flush=True)


def bras_L(seed):
    rng = np.random.Generator(np.random.PCG64(seed)); g = G(1); etapes = []
    def paire_locale():
        a = int(rng.integers(g.n()))
        if not g.adj[a]: return None
        c = list(g.adj[a])[int(rng.integers(len(g.adj[a])))]; lb = list(g.adj[c]); b = lb[int(rng.integers(len(lb)))]
        return (a, b) if b != a and b not in g.adj[a] else None
    while g.n() < 60:
        v0 = int(rng.integers(g.n())); v = g.ajoute_sommet(); g.ajoute(v0, v); n = g.n(); budget = int(n * K0 / 2); essais = 0
        while g.m < min(budget, n * (n - 1) // 2) and essais < 5000:
            essais += 1; p = paire_locale()
            if p: g.ajoute(*p)
        if g.m >= 2: metropolis(g, rng, 100 * n, paire_locale)
        if n in (10, 20, 30, 40, 50, 60): etapes.append(g.mesure())
    out = dict(bras='L', graine=seed, etapes=etapes, final=etapes[-1]); json.dump(out, open(f'c179c_L_{seed}.json', 'w'))
    print('L', seed, {k: etapes[-1][k] for k in ('N', 'aretes', 'triangles', 'tetraedres', 'plus_grande_clique', 'n_e_mediane', 'n_e_moyenne', 'n_e_max', 'degre_max')}, flush=True)


if __name__ == '__main__':
    (bras_G if sys.argv[1] == 'G' else bras_L)(int(sys.argv[2]))
