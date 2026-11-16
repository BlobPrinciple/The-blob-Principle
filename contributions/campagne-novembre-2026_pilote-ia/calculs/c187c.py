#!/usr/bin/env python3
"""C-187c et C-188c -- contre-calculs independants des C-187 et C-188 de ChatGPT (Claude, 16 novembre 2026). Physique reelle et connue : potentiel de Lennard-Jones de paires,
E = somme (r^-12 - 2 r^-6), r0 = 1, aucun terme du Blob. Ecrits d'apres ses seuls PROTOCOLES FIGES ; resultats non lus avant le scelle de c187c_c188c_prediction.txt.
 C-187 : croissance atome par atome de N = 2 a 13 (Q1 : une proposition par naissance ; Q4 : la meilleure de quatre), puis detection des liens entoures de 5 tetraedres.
 C-188 : icosaedre a 13 atomes compare au cuboctaedre ; complexe de 20 tetraedres ; stabilite.
Detecteur independant du sien (cliques et non Delaunay) : lien = paire dans [0,80 ; 1,25] ; tetraedre = 4 atomes tous lies, volume > 0,015 ; lien entoure = tous ses triangles dans exactement 2 tetraedres.
Usage : python3 c187c.py Q1 | Q4 | ICO   -> c187c_Q1.json, c187c_Q4.json, c188c.json"""
import itertools, json, math, sys
import numpy as np, scipy.optimize as so


def lj(z):
    X = z.reshape(-1, 3); n = len(X); iu = np.triu_indices(n, 1); d = X[iu[0]] - X[iu[1]]; r2 = (d * d).sum(1); i6 = 1 / r2 ** 3
    e = (i6 * i6 - 2 * i6).sum(); f = (-12 * (i6 * i6 - i6) / r2)[:, None] * d; g = np.zeros_like(X); np.add.at(g, iu[0], f); np.add.at(g, iu[1], -f)
    return e, g.ravel()


def detecte(X, lo=0.80, hi=1.25, vmin=0.015):
    n = len(X); D = np.linalg.norm(X[:, None] - X[None], axis=2); A = [set(j for j in range(n) if j != i and lo <= D[i, j] <= hi) for i in range(n)]
    T = [q for q in itertools.combinations(range(n), 4) if all(b in A[a] for a, b in itertools.combinations(q, 2)) and abs(np.dot(X[q[1]] - X[q[0]], np.cross(X[q[2]] - X[q[0]], X[q[3]] - X[q[0]]))) / 6 > vmin]
    tri = {}
    for q in T:
        for f in itertools.combinations(q, 3): tri[f] = tri.get(f, 0) + 1
    ne = {}
    for q in T:
        for e in itertools.combinations(q, 2): ne[e] = ne.get(e, 0) + 1
    ent = {e: k for e, k in ne.items() if k >= 3 and all(v == 2 for f, v in tri.items() if e[0] in f and e[1] in f)}
    return dict(tetraedres=len(T), liens_entoures=sorted(ent.values()), cinq=sum(1 for v in ent.values() if v == 5), faces_surchargees=sum(1 for v in tri.values() if v > 2), centre_icosaedrique=bool(any(len(a) == 12 for a in A)),
                dmin=float(D[np.triu_indices(n, 1)].min()))


def naissance(X, rng):
    for _ in range(500):
        p = int(rng.integers(len(X))); u = rng.standard_normal(3); u /= np.linalg.norm(u); r = rng.uniform(0.97, 1.24); c = X[p] + r * u
        if np.linalg.norm(X - c, axis=1).min() >= 0.82: break
    Y = np.vstack([X, c]); r = so.minimize(lj, Y.ravel(), jac=True, method='L-BFGS-B', options=dict(ftol=1e-12, gtol=1e-8, maxiter=1000)); Y = r.x.reshape(-1, 3)
    return Y - Y.mean(axis=0), float(r.fun), float(np.abs(r.jac).max())


def croissance(seed, k):
    rng = np.random.Generator(np.random.PCG64(seed)); X = np.array([[0., 0, 0], [1., 0, 0]]); out = dict(graine=seed, N={})
    for N in range(3, 14):
        X, E, g = min((naissance(X, rng) for _ in range(k)), key=lambda t: t[1]); d = detecte(X); d.update(E=E, gradient=g); out['N'][N] = d
    return out


def ICO():
    phi = (1 + math.sqrt(5)) / 2; V = []
    for a, b in itertools.product((1, -1), repeat=2): V += [(0, a, b * phi), (a, b * phi, 0), (a * phi, 0, b)]
    ico = np.array([(0, 0, 0)] + V, float); cubo = np.array([(0, 0, 0)] + [p for p in itertools.product((0, 1, -1), repeat=3) if sorted(map(abs, p)) == [0, 1, 1]], float); out = {}
    for nom, X0 in (('icosaedre', ico), ('cuboctaedre', cubo)):
        r = np.linalg.norm(X0[:, None] - X0[None], axis=2)[np.triu_indices(13, 1)]; A = (r ** -12.).sum(); B = (r ** -6.).sum(); s = (A / B) ** (1 / 6); out[nom] = dict(echelle=s, E=-B * B / A, E_par_paires=float(lj((s * X0).ravel())[0]))
    X = out['icosaedre']['echelle'] * ico; r = so.minimize(lj, X.ravel(), jac=True, method='L-BFGS-B', options=dict(ftol=1e-15, gtol=1e-12, maxiter=5000)); Xm = r.x.reshape(-1, 3); Em = float(r.fun)
    d = detecte(Xm); D = np.linalg.norm(Xm[:, None] - Xm[None], axis=2); c = int(np.argmin(np.linalg.norm(Xm - Xm.mean(0), axis=1))); rad = sorted(D[c, j] for j in range(13) if j != c); sur = sorted(D[i, j] for i in range(13) for j in range(i + 1, 13) if c not in (i, j) and D[i, j] < 1.25)
    # somme des diedres autour de chaque rayon, volumes
    T = [q for q in itertools.combinations(range(13), 4) if c in q and all(D[a, b] < 1.25 for a, b in itertools.combinations(q, 2))]
    def diedre(a, b, p, q):
        e = (Xm[b] - Xm[a]) / np.linalg.norm(Xm[b] - Xm[a]); u = Xm[p] - Xm[a]; u -= np.dot(u, e) * e; v = Xm[q] - Xm[a]; v -= np.dot(v, e) * e; return math.acos(np.clip(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v), -1, 1))
    sommes = []
    for j in range(13):
        if j == c: continue
        sommes.append(sum(diedre(c, j, *[x for x in t if x not in (c, j)]) for t in T if j in t))
    from scipy.spatial import ConvexHull
    vol = sum(abs(np.dot(Xm[t[1]] - Xm[t[0]], np.cross(Xm[t[2]] - Xm[t[0]], Xm[t[3]] - Xm[t[0]]))) / 6 for t in T)
    h = 1e-5; z = Xm.ravel(); Hs = np.array([(lj(z + h * e)[1] - lj(z - h * e)[1]) / (2 * h) for e in np.eye(39)]); w = np.linalg.eigvalsh((Hs + Hs.T) / 2)
    pert = []
    for seed in range(18800, 18812):
        Y = Xm + 0.025 * np.random.default_rng(seed).standard_normal((13, 3)); Y -= Y.mean(0); rr = so.minimize(lj, Y.ravel(), jac=True, method='L-BFGS-B', options=dict(ftol=1e-15, gtol=1e-10, maxiter=5000)); pert.append(float(rr.fun))
    U = 0.5 * (sum((x - 1) ** 2 for x in rad) + sum((x - 1) ** 2 for x in sur))
    out.update(E_minimum_libre=Em, detecteur=d, tetraedres_au_centre=len(T), rayon=[rad[0], rad[-1]], arete_de_surface=[sur[0], sur[-1]], nombre_aretes_de_surface=len(sur), rapport=rad[0] / sur[0], somme_diedres_ecart_max_a_2pi=float(max(abs(x - 2 * math.pi) for x in sommes)),
               volume_tetraedres=vol, volume_enveloppe=float(ConvexHull(Xm).volume), U_des_42_liens=U, modes_nuls=int((abs(w) < 1e-4).sum()), modes_positifs=int((w > 1e-4).sum()), plus_petite_vp_positive=float(w[w > 1e-4].min()),
               perturbations_revenues=sum(1 for e in pert if abs(e - Em) < 1e-6 * abs(Em)), energies_perturbations=pert)
    json.dump(out, open('c188c.json', 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'energies_perturbations'}))


if __name__ == '__main__':
    if sys.argv[1] == 'ICO': ICO()
    else:
        k = 1 if sys.argv[1] == 'Q1' else 4; graines = range(187000, 187064) if k == 1 else range(188000, 188024); R = [croissance(s, k) for s in graines]; json.dump(R, open(f'c187c_{sys.argv[1]}.json', 'w'))
        for N in (6, 7, 8, 10, 13):
            L = [r['N'][N] for r in R]; print(sys.argv[1], 'N', N, 'avec lien entoure de 5 :', sum(1 for d in L if d['cinq'] > 0), '/', len(L), '| entoures autres que 5 :', sum(1 for d in L if any(v != 5 for v in d['liens_entoures'])), '| centre icosaedrique :', sum(d['centre_icosaedrique'] for d in L),
                                         '| faces surchargees :', sum(d['faces_surchargees'] > 0 for d in L), '| E min %.6f max %.6f' % (min(d['E'] for d in L), max(d['E'] for d in L)), '| dmin %.3f' % min(d['dmin'] for d in L), '| grad max %.1e' % max(d['gradient'] for d in L), flush=True)
        print(sys.argv[1], 'N<=6 avec cinq :', sum(1 for r in R for N in range(3, 7) if r['N'][N]['cinq'] > 0), '| energies distinctes a N=7 :', sorted(set(round(r['N'][7]['E'], 3) for r in R)), '| a N=13, meilleures :', sorted(set(round(r['N'][13]['E'], 3) for r in R))[:4])
