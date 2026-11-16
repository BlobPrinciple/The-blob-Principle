#!/usr/bin/env python3
"""C-180c -- moteur canonique de l'auteur : certification de X-12 (partie I) et essai du terme en b (partie II) (Claude, 16 novembre 2026). Predictions : c180c_prediction.txt.
Usage : python3 c180c.py I <N> <graine> <nsw> <cand_factor>   -> c180c_I_<N>_<graine>_<nsw>_<cf>.json
        python3 c180c.py II <graine> <b> [cand_factor] [temoin] -> c180c_II_<graine>_<b>_<cf>.json"""
import importlib.util, itertools, json, math, os, sys
import numpy as np
from scipy.spatial import cKDTree
from c179c import G

DS = 2 * math.pi / math.acos(1 / 3); BETA, TAU = 0.30, 0.50
chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB', 'blob colab verrouillage.py')
src = open(chemin).read().split('def edges_tris')[0]; src = src[src.index('BETA, TAU'):]; ns = {}; exec('import numpy as np, os\nfrom scipy.spatial import cKDTree\n' + src, ns)


def mesure(A, N):
    g = G(N)
    for a in range(N):
        for b in A[a]:
            if a < b: g.ajoute(a, b)
    m = g.mesure(); ne = []
    for a, b in g.aretes():
        com = sorted(g.adj[a] & g.adj[b]); ne.append(sum(1 for c, d in itertools.combinations(com, 2) if d in g.adj[c]))
    ne = np.array(ne); pos = ne[ne > 0]
    m.update(triangles_par_sommet=m['triangles'] / N, part_aretes_sans_tetraedre=float((ne == 0).mean()), part_4_5_6=float(np.isin(pos, (4, 5, 6)).mean()) if len(pos) else None, sommets_isoles=int(sum(1 for x in A if not x)),
             histogramme_complet={int(k): int((ne == k).sum()) for k in sorted(set(ne.tolist()))})
    return m


def avec_b(N, seed, b, kappa=6.6, cand_factor=4.1, nsw_per_N=80):
    """Retranscription ligne a ligne de canonical() de l'auteur (memes tirages, dans le meme ordre), plus le terme -b Somme (n_e - d*)^2 dans l'exposant."""
    rng = np.random.default_rng(seed); X = rng.random((N, 3))
    r_cand = (kappa * cand_factor / (N * 4.18879)) ** (1 / 3.0)
    cand = cKDTree(X).query_pairs(r_cand, output_type='ndarray'); M = len(cand)
    E0 = min(int(round(N * kappa / 2.0)), M)
    sel = rng.choice(M, size=E0, replace=False)
    pres = np.zeros(M, bool); pres[sel] = True
    A = [set() for _ in range(N)]
    for k in sel:
        a, b_ = int(cand[k, 0]), int(cand[k, 1]); A[a].add(b_); A[b_].add(a)
    deg = np.array([len(s) for s in A], float)
    ntri = float(sum(len(A[i] & A[j]) for i in range(N) for j in A[i] if i < j))
    sumsq = float((deg ** 2).sum()); mean = 2.0 * E0 / N
    plist = list(sel); T = TAU / N
    ne = {}
    def cle(x, y): return (x, y) if x < y else (y, x)
    if b:
        for i in range(N):
            for j in A[i]:
                if i < j:
                    com = sorted(A[i] & A[j]); ne[(i, j)] = sum(1 for c, d in itertools.combinations(com, 2) if d in A[c])
    def k4(x, y):   # tetraedres contenant la paire (x, y), supposee liee : liste des paires (c, d)
        com = sorted(A[x] & A[y]); return [(c, d) for c, d in itertools.combinations(com, 2) if d in A[c]]
    for _ in range(nsw_per_N * N):
        ri = rng.integers(len(plist)); e = plist[ri]
        a, b_ = int(cand[e, 0]), int(cand[e, 1]); f = -1
        for _t in range(25):
            g = int(rng.integers(M))
            if not pres[g]:
                c, d = int(cand[g, 0]), int(cand[g, 1])
                if len({a, b_, c, d}) == 4: f = g; break
        if f < 0: continue
        c, d = int(cand[f, 0]), int(cand[f, 1])
        dn = -len(A[a] & A[b_]) + len(A[c] & A[d]); new_ntri = ntri + dn
        new_sumsq = sumsq + 2.0 * (deg[c] + deg[d] - deg[a] - deg[b_]) + 4.0
        cv0 = np.sqrt(max(sumsq / N - mean * mean, 0)) / mean
        cv1 = np.sqrt(max(new_sumsq / N - mean * mean, 0)) / mean
        dS = np.log1p(new_ntri) - np.log1p(ntri) - BETA * (cv1 - cv0)
        delta = None; dP = 0.0
        if b:
            delta = {}
            for x, y in k4(a, b_):          # tetraedres detruits par le retrait de (a, b)
                for q in ((a, x), (a, y), (b_, x), (b_, y), (x, y)): delta[cle(*q)] = delta.get(cle(*q), 0) - 1
            A[a].discard(b_); A[b_].discard(a); A[c].add(d); A[d].add(c)
            nouv = k4(c, d)                 # tetraedres crees par l'ajout de (c, d)
            for x, y in nouv:
                for q in ((c, x), (c, y), (d, x), (d, y), (x, y)): delta[cle(*q)] = delta.get(cle(*q), 0) + 1
            A[c].discard(d); A[d].discard(c); A[a].add(b_); A[b_].add(a)
            dP = -(ne[cle(a, b_)] - DS) ** 2 + (len(nouv) - DS) ** 2
            for q, dv in delta.items():
                if dv: dP += (ne[q] + dv - DS) ** 2 - (ne[q] - DS) ** 2
        u = rng.random() if not (dS >= 0 and not b) else None
        if b:
            lw = dS / T - b * dP; ok = lw >= 0 or u < math.exp(max(min(lw, 30), -700))
        else:
            ok = dS >= 0 or u < np.exp(min(dS / T, 30))
        if ok:
            A[a].discard(b_); A[b_].discard(a); A[c].add(d); A[d].add(c)
            deg[a] -= 1; deg[b_] -= 1; deg[c] += 1; deg[d] += 1
            ntri = new_ntri; sumsq = new_sumsq
            pres[e] = False; pres[f] = True; plist[ri] = f
            if b:
                del ne[cle(a, b_)]; ne[cle(c, d)] = len(nouv)
                for q, dv in delta.items():
                    if dv: ne[q] += dv
    return A, X


if __name__ == '__main__':
    if sys.argv[1] == 'I':
        N, seed, nsw, cf = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
        A, X, h = ns['canonical'](N, seed, cand_factor=cf, nsw_per_N=nsw); m = mesure(A, N); m.update(N=N, graine=seed, nsw=nsw, cand_factor=cf)
        json.dump(m, open(f'c180c_I_{N}_{seed}_{nsw}_{cf}.json', 'w')); print('I', N, seed, nsw, cf, 'tri/s %.2f' % m['triangles_par_sommet'], 'n_e med', m['n_e_mediane'], 'moy %.1f' % m['n_e_moyenne'], 'max', m['n_e_max'], flush=True)
    else:
        seed, b = int(sys.argv[2]), float(sys.argv[3]); cf = float(sys.argv[4]) if len(sys.argv) > 4 else 4.1; N = 1000
        A, X = avec_b(N, seed, b, cand_factor=cf); m = mesure(A, N); m.update(N=N, graine=seed, b=b, cand_factor=cf)
        if len(sys.argv) > 5:
            A2, X2, h = ns['canonical'](N, seed, cand_factor=cf, nsw_per_N=80); m['temoin_identite'] = bool(all(A[i] == A2[i] for i in range(N)))
        json.dump(m, open(f'c180c_II_{seed}_{b}_{cf}.json', 'w')); print('II', seed, 'b', b, 'cf', cf, 'tri/s %.2f' % m['triangles_par_sommet'], 'tet/s %.2f' % m['tetraedres_par_sommet'], 'n_e med', m['n_e_mediane'], 'moy %.1f' % m['n_e_moyenne'], 'max', m['n_e_max'], 'sans %.2f' % m['part_aretes_sans_tetraedre'], '456 %.2f' % (m['part_4_5_6'] or 0), m.get('temoin_identite', ''), flush=True)
