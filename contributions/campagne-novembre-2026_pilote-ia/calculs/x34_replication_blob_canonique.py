#!/usr/bin/env python3
"""X-34. Deux contrôles écrits à partir des seuls textes de l'auteur, sans son code.
R1 : réplication du « Blob canonique » d'après le Dossier de réplication indépendante v1.0 (4 juillet 2026, master V277 p. 1127-1131).
R2 : témoin de définition pour le couplage courbure-matière (tome de campagne V277, Partie R, 17 juillet 2026).
Usage : x34_replication_blob_canonique.py R1|R2 graine [N]
"""
import sys, math, json, itertools
import numpy as np
from scipy.spatial import cKDTree

def construire(N, kappa, graine, tore=False, rho=None):
    rng = np.random.default_rng(graine)
    if tore:
        L = (N / rho) ** (1 / 3); pts = rng.random((N, 3)) * L
        r = (3 * kappa / (4 * math.pi * rho)) ** (1 / 3)
        arbre = cKDTree(pts, boxsize=L)
    else:
        L = None; pts = rng.random((N, 3)); r = (3 * kappa / (4 * math.pi * N)) ** (1 / 3)
        arbre = cKDTree(pts)
    pool = [tuple(p) for p in arbre.query_pairs(1.6 * r, output_type='ndarray')]
    return rng, pts, L, r, arbre, pool

def distance(pts, L, i, j):
    d = pts[i] - pts[j]
    if L is not None: d -= L * np.round(d / L)
    return d

class Graphe:
    def __init__(self, N, pool, rng):
        self.N, self.pool, self.rng = N, pool, rng
        self.adj = [set() for _ in range(N)]
        self.present = {}            # arête -> indice dans self.liste
        self.liste = []
        self.absent = {}; self.labs = []
        self.ntri = 0; self.sd2 = 0
    def _voisins_communs(self, a, b): return len(self.adj[a] & self.adj[b])
    def ajouter(self, e):
        a, b = e
        self.ntri += self._voisins_communs(a, b)
        self.sd2 += 2 * len(self.adj[a]) + 1 + 2 * len(self.adj[b]) + 1
        self.adj[a].add(b); self.adj[b].add(a)
        self.present[e] = len(self.liste); self.liste.append(e)
        if e in self.absent:
            i = self.absent.pop(e); d = self.labs.pop()
            if i < len(self.labs): self.labs[i] = d; self.absent[d] = i
    def retirer(self, e):
        a, b = e
        self.adj[a].discard(b); self.adj[b].discard(a)
        self.ntri -= self._voisins_communs(a, b)
        self.sd2 -= 2 * len(self.adj[a]) + 1 + 2 * len(self.adj[b]) + 1
        i = self.present.pop(e); d = self.liste.pop()
        if i < len(self.liste): self.liste[i] = d; self.present[d] = i
        self.absent[e] = len(self.labs); self.labs.append(e)
    def cv(self):
        E = len(self.liste); mu = 2 * E / self.N
        return math.sqrt(max(self.sd2 / self.N - mu * mu, 0.0)) / mu
    def S(self, beta): return math.log(1 + self.ntri) - beta * self.cv()
    def relies(self, u, v):
        vus = {u}; pile = [u]
        while pile:
            x = pile.pop()
            for y in self.adj[x]:
                if y == v: return True
                if y not in vus: vus.add(y); pile.append(y)
        return False

def initialiser(g, aretes_init, E0, garde):
    for e in g.pool: g.absent[e] = len(g.labs); g.labs.append(e)
    for e in aretes_init: g.ajouter(e)
    while len(g.liste) < E0: g.ajouter(g.labs[int(g.rng.integers(len(g.labs)))])
    essais = 0
    while len(g.liste) > E0 and essais < 50 * E0:
        essais += 1
        e = g.liste[int(g.rng.integers(len(g.liste)))]
        g.retirer(e)
        if garde and not g.relies(*e): g.ajouter(e)

def balayages(g, n, beta, facteur, garde):
    acc = 0
    for _ in range(n * g.N):
        e = g.liste[int(g.rng.integers(len(g.liste)))]
        f = g.labs[int(g.rng.integers(len(g.labs)))]
        u, v = e
        verifier = garde and (len(g.adj[u]) <= 2 or len(g.adj[v]) <= 2)
        S0 = g.S(beta)
        g.retirer(e)
        if verifier and not g.relies(u, v): g.ajouter(e); continue
        g.ajouter(f)
        dS = g.S(beta) - S0
        if dS >= 0 or g.rng.random() < math.exp(dS * facteur): acc += 1
        else: g.retirer(f); g.ajouter(e)
    return acc / (n * g.N)

def cliques4(g):
    """Renvoie la liste des K4 (u<v<w<x)."""
    K = []
    for u in range(g.N):
        Nu = [w for w in g.adj[u] if w > u]
        for v in Nu:
            C = [w for w in (g.adj[u] & g.adj[v]) if w > v]
            for i, w in enumerate(C):
                for x in C[i + 1:]:
                    if x in g.adj[w]: K.append((u, v, w, x) if w < x else (u, v, x, w))
    return K

def observables_R1(g):
    N = g.N; deg = np.array([len(a) for a in g.adj])
    wedges = int((deg * (deg - 1) // 2).sum())
    K = cliques4(g)
    dans_k4 = np.zeros(N, bool)
    for q in K: dans_k4[list(q)] = True
    dans_tri = np.zeros(N, bool); mult = {}
    for q in K:
        for t in itertools.combinations(q, 3): mult[t] = mult.get(t, 0) + 1
    bandes = {'0-8': [], '8-12': [], '12-18': [], '18+': []}
    for (a, b) in g.liste:
        for c in g.adj[a] & g.adj[b]:
            if c > b and a < b:
                t = (a, b, c); dans_tri[[a, b, c]] = True
                m = mult.get(t, 0); d = (deg[a] + deg[b] + deg[c]) / 3
                bandes['0-8' if d < 8 else '8-12' if d < 12 else '12-18' if d < 18 else '18+'].append(m)
    return {'tri_par_N': g.ntri / N, 'transitivite': 3 * g.ntri / wedges, 'cv_degres': g.cv(), 'k4_par_N': len(K) / N,
            'multiplicite': 4 * len(K) / max(g.ntri, 1), 'f_baryon': float(dans_k4.mean()),
            'f_dm': float((dans_tri & ~dans_k4).mean()), 'f_de': float((~dans_tri).mean()),
            'strat': {k: (float(np.mean(v)) if v else None) for k, v in bandes.items()},
            'strat_n': {k: len(v) for k, v in bandes.items()}}

def R1(graine, N=2000):
    rng, pts, L, r, arbre, pool = construire(N, 6.6, graine)
    g = Graphe(N, [tuple(sorted(e)) for e in pool], rng)
    init = [tuple(sorted(p)) for p in arbre.query_pairs(r, output_type='ndarray')]
    initialiser(g, init, int(round(3.3 * N)), garde=True)
    out = {'controle': 'R1', 'graine': graine, 'N': N, 'aretes': len(g.liste), 'degre_pool': 2 * len(pool) / N}
    acc = balayages(g, 40, 0.30, N / 0.5, True); out['acceptation_40'] = acc
    out['a_40'] = observables_R1(g)
    balayages(g, 8, 0.30, N / 0.5, True); out['a_48'] = observables_R1(g)
    return out

def diedre(pu, pv, pw, px):
    e = pv - pu; e = e / np.linalg.norm(e)
    a = pw - pu; a = a - a.dot(e) * e; b = px - pu; b = b - b.dot(e) * e
    c = a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return math.acos(max(-1.0, min(1.0, c)))

def mesures_R2(g, pts, L):
    K = cliques4(g); k4v = np.zeros(g.N)
    par_arete = {}
    for q in K:
        for s in q: k4v[s] += 1
        for (a, b) in itertools.combinations(q, 2):
            autres = [s for s in q if s != a and s != b]
            par_arete.setdefault((a, b), []).append(autres)
    X = []
    for (a, b), lst in par_arete.items():
        m = len(lst)
        if m < 2: continue
        pa = pts[a]; pb = pa + distance(pts, L, b, a)
        som = 0.0
        for (w, x) in lst:
            som += diedre(pa, pb, pa + distance(pts, L, w, a), pa + distance(pts, L, x, a))
        X.append((abs(2 * math.pi - som), m, (k4v[a] + k4v[b]) / 2, (k4v[a] + k4v[b] - 2 * m) / 2, (len(g.adj[a]) + len(g.adj[b])) / 2))
    X = np.array(X)
    def r(i, j): return float(np.corrcoef(X[:, i], X[:, j])[0, 1])
    def partielle(i, j, k):
        a, b, c = r(i, j), r(i, k), r(j, k); return (a - b * c) / math.sqrt((1 - b * b) * (1 - c * c))
    return {'aretes_m>=2': len(X), 'aretes_total': len(g.liste), 'k4_par_N': len(K) / g.N, 'm_moyen': float(X[:, 1].mean()),
            'r_deficit_m': r(0, 1), 'r_deficit_rho_sommets': r(0, 2), 'r_deficit_rho_externe': r(0, 3), 'r_deficit_degre': r(0, 4),
            'partielle_rho_sommets_sachant_m': partielle(0, 2, 1), 'partielle_rho_externe_sachant_m': partielle(0, 3, 1),
            'part_arêtes_m>=6': float((X[:, 1] >= 6).mean())}

def R2(graine, N=6000):
    rng, pts, L, r, arbre, pool = construire(N, 10.0, graine, tore=True, rho=200.0)
    g = Graphe(N, [tuple(sorted(e)) for e in pool], rng)
    choix = rng.choice(len(g.pool), size=5 * N, replace=False)
    initialiser(g, [g.pool[i] for i in choix], 5 * N, garde=False)
    out = {'controle': 'R2', 'graine': graine, 'N': N, 'aretes': len(g.liste), 'degre_pool': 2 * len(pool) / N}
    out['aleatoire'] = mesures_R2(g, pts, L)
    out['acceptation'] = balayages(g, 30, 2.0, N / 0.5, False)
    out['tri_par_N'] = g.ntri / N; out['cv'] = g.cv()
    out['equilibre'] = mesures_R2(g, pts, L)
    return out

if __name__ == '__main__':
    quoi, graine = sys.argv[1], int(sys.argv[2])
    N = int(sys.argv[3]) if len(sys.argv) > 3 else None
    res = (R1(graine, N or 2000) if quoi == 'R1' else R2(graine, N or 6000))
    print(json.dumps(res, ensure_ascii=False))
