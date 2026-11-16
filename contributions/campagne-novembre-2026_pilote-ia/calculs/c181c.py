#!/usr/bin/env python3
"""C-181c -- le terme en b de la couche B ajoute au moteur canonique de l'auteur lui-meme, << blob engine.py >> (Claude, 16 novembre 2026). Predictions : c181c_prediction.txt.
_mcmc est retranscrit a l'identique (memes tirages np.random, dans le meme ordre, memes blocs, memes graines de bloc) ; seul l'exposant recoit - b Somme (n_e - d*)^2.
Usage : python3 c181c.py <graine> <b> [temoin]   -> c181c_<graine>_<b>.json   (temoin : compare a build_blob de l'auteur, et controle le suivi incremental de n_e)"""
import importlib.util, itertools, json, math, os, sys
import numpy as np
from c180c import mesure

DS = 2 * math.pi / math.acos(1 / 3)
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(base, 'blob engine.py')); be = importlib.util.module_from_spec(spec); spec.loader.exec_module(be)


def cle(x, y): return (x, y) if x < y else (y, x)


def k4(A, x, y):
    com = sorted(A[x] & A[y]); return [(c, d) for c, d in itertools.combinations(com, 2) if d in A[c]]


def tous_ne(A, N):
    return {(i, j): len(k4(A, i, j)) for i in range(N) for j in A[i] if i < j}


def moteur(N, seed, b, suivi=False):
    pts, edges, pool = be._rips(N, seed, be.KAPPA, be.POOL_FAC)
    A = [set() for _ in range(N)]
    for u, v in edges: A[int(u)].add(int(v)); A[int(v)].add(int(u))
    eu = [int(x) for x in edges[:, 0]]; ev = [int(x) for x in edges[:, 1]]; pa = [int(x) for x in pool[:, 0]]; pb = [int(x) for x in pool[:, 1]]
    mean = 2.0 * len(edges) / N; steps = be.THERM_FAC * N; chunk = max(steps // be.N_CHUNKS, 1); cap = be.CAP; beta = be.BETA; tau_eff = be.TAU / N
    nt = sum(len(A[i] & A[j]) for i in range(N) for j in A[i] if i < j) // 3
    suivi = suivi or b > 0; ne = tous_ne(A, N) if suivi else None; E = len(eu); P = len(pa)
    for c in range(be.N_CHUNKS):
        np.random.seed(seed * 100 + 1 + c)
        sumsq = 0.0
        for i in range(N): sumsq += len(A[i]) * len(A[i])
        cv = math.sqrt(max(sumsq / N - mean * mean, 0.0)) / mean
        S = math.log(1.0 + nt) - beta * cv
        for _ in range(chunk):
            io = np.random.randint(0, E); u = eu[io]; v = ev[io]
            if len(A[u]) <= 2 or len(A[v]) <= 2: continue
            a = -1; b_ = -1; ok = False
            for _t in range(40):
                pi = np.random.randint(0, P); ca = pa[pi]; cb = pb[pi]
                if ca == u or ca == v or cb == u or cb == v: continue
                if len(A[ca]) >= cap or len(A[cb]) >= cap: continue
                if cb not in A[ca]: a = ca; b_ = cb; ok = True; break
            if not ok: continue
            tl = len(A[u] & A[v]); tg = len(A[a] & A[b_]); nt2 = nt - tl + tg
            du = len(A[u]); dv = len(A[v]); da = len(A[a]); db = len(A[b_])
            nss = sumsq + (-2 * du + 1) + (-2 * dv + 1) + (2 * da + 1) + (2 * db + 1)
            cv2 = math.sqrt(max(nss / N - mean * mean, 0.0)) / mean
            S2 = math.log(1.0 + nt2) - beta * cv2
            if suivi:
                delta = {}
                for x, y in k4(A, u, v):
                    for q in ((u, x), (u, y), (v, x), (v, y), (x, y)): delta[cle(*q)] = delta.get(cle(*q), 0) - 1
                A[u].discard(v); A[v].discard(u); A[a].add(b_); A[b_].add(a)
                nouv = k4(A, a, b_)
                for x, y in nouv:
                    for q in ((a, x), (a, y), (b_, x), (b_, y), (x, y)): delta[cle(*q)] = delta.get(cle(*q), 0) + 1
                A[a].discard(b_); A[b_].discard(a); A[u].add(v); A[v].add(u)
                dP = -(ne[cle(u, v)] - DS) ** 2 + (len(nouv) - DS) ** 2
                for q, dq in delta.items():
                    if dq: dP += (ne[q] + dq - DS) ** 2 - (ne[q] - DS) ** 2
                lw = (S2 - S) / tau_eff - b * dP
                acc = lw >= 0.0 or np.random.random() < math.exp(max(lw, -700.0))
            else:
                acc = (S2 - S) >= 0.0 or np.random.random() < math.exp((S2 - S) / tau_eff)
            if acc:
                A[u].discard(v); A[v].discard(u); A[a].add(b_); A[b_].add(a)
                nt = nt2; sumsq = nss; S = S2; eu[io] = a; ev[io] = b_
                if suivi:
                    del ne[cle(u, v)]; ne[cle(a, b_)] = len(nouv)
                    for q, dq in delta.items():
                        if dq: ne[q] += dq
    return A, ne, nt


def complement(A, N):
    T = set()
    for i in range(N):
        for j in A[i]:
            if i < j:
                for k in A[i] & A[j]:
                    if k > j: T.add((i, j, k))
    nb = [len(A[i] & A[j] & A[k]) for i, j, k in T]; nb = np.array(nb) if T else np.zeros(0)
    vu = [False] * N; comp = 0; plus = 0
    for s in range(N):
        if vu[s]: continue
        comp += 1; pile = [s]; vu[s] = True; t = 0
        while pile:
            x = pile.pop(); t += 1
            for y in A[x]:
                if not vu[y]: vu[y] = True; pile.append(y)
        plus = max(plus, t)
    d = np.array([len(x) for x in A], float)
    return dict(triangles_distincts=len(T), part_triangles_dans_plus_de_2_tetraedres=float((nb > 2).mean()) if len(nb) else None, part_triangles_dans_1_ou_2=float(((nb == 1) | (nb == 2)).mean()) if len(nb) else None,
                part_triangles_sans_tetraedre=float((nb == 0).mean()) if len(nb) else None, composantes=comp, plus_grande_composante=plus, CV_degres=float(d.std() / d.mean()), degre_moyen=float(d.mean()), degre_min=int(d.min()))


if __name__ == '__main__':
    seed, b = int(sys.argv[1]), float(sys.argv[2]); N = 1000; tem = len(sys.argv) > 3
    A, ne, nt = moteur(N, seed, b, suivi=tem); m = mesure(A, N); m.update(complement(A, N)); m.update(N=N, graine=seed, b=b, compteur_final=nt)
    if tem:
        pts, nbr, deg = be.build_blob(N, seed); A2 = [set(int(x) for x in nbr[u, :deg[u]]) for u in range(N)]
        m['temoin_identite'] = bool(all(A[i] == A2[i] for i in range(N))); m['temoin_suivi_n_e'] = bool(ne == tous_ne(A, N)); m['temoin_compteur'] = bool(nt == m['triangles'])
    json.dump(m, open(f'c181c_{seed}_{b}.json', 'w'))
    print(seed, 'b', b, 'tri/s %.2f' % m['triangles_par_sommet'], 'CV %.3f' % m['CV_degres'], 'n_e med', m['n_e_mediane'], 'moy %.1f' % m['n_e_moyenne'], 'max', m['n_e_max'], '456 %.2f' % (m['part_4_5_6'] or 0), 'sans %.2f' % m['part_aretes_sans_tetraedre'],
          'tri>2 %.3f' % (m['part_triangles_dans_plus_de_2_tetraedres'] or 0), 'isoles', m['sommets_isoles'], 'comp', m['composantes'], m.get('temoin_identite', ''), m.get('temoin_suivi_n_e', ''), m.get('temoin_compteur', ''), flush=True)
