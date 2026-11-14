#!/usr/bin/env python3
"""C-149c -- Le tenseur des contraintes de la trame a ressorts (Claude, 14 novembre 2026).

Demande du dossier GR-3 de ChatGPT. Predictions : c149c_prediction.txt (ecrit avant ce programme).
Modele : ressorts de Hooke, K = 1, longueur naturelle commune l0 = 1 (regle U). Aucune hypothese ajoutee.
Usage : python3 c149c.py A   (trame periodique)   |   python3 c149c.py B   (tissu fini de C-132 bis, rejoue)
"""
import itertools
import json
import math
import sys

import numpy as np
import scipy.optimize as so
from scipy.stats import spearmanr

R2, R3 = math.sqrt(2), math.sqrt(3)
TOL = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-6     # tolerance du reperage des cellules au contact (COMPLEMENT : 1e-3, fichier c149c_B_tol.json)


# ------------------------------------------------------------------ la trame de palier, par la regle genealogique (comme C-147c bis)
def classes_de_palier(K=4):
    S = 2 ** K
    P = {0: (0, 0, 0), 1: (S, 0, 0), 2: (S, S, 0), 3: (S, S, S)}
    mid = {}

    def milieu(a, b):
        k = frozenset((a, b))
        if k not in mid:
            mid[k] = len(P)
            P[mid[k]] = tuple((P[a][i] + P[b][i]) // 2 for i in range(3))
        return mid[k]

    cells = [((0, 1, 2, 3), 3)]
    for _ in range(3 * K):
        new = []
        for x, d in cells:
            z = milieu(x[0], x[d])
            nd = d - 1 if d > 1 else 3
            new.append((x[:d] + (z,) + x[d + 1:], nd))
            new.append((x[1:d + 1] + (z,) + x[d + 1:], nd))
        cells = new
    fils = {frozenset(p) for x, _ in cells for p in itertools.combinations(x, 2)}
    vois = {}
    for f in fils:
        a, b = tuple(f)
        vois.setdefault(a, set()).add(tuple(P[b][i] - P[a][i] for i in range(3)))
        vois.setdefault(b, set()).add(tuple(P[a][i] - P[b][i] for i in range(3)))
    classes = {}
    for v, (x, y, z) in P.items():
        if z >= 2 and y - z >= 2 and x - y >= 2 and x <= S - 2:
            c = (x % 2, y % 2, z % 2)
            assert classes.get(c, vois[v]) == vois[v]
            classes[c] = vois[v]
    assert len(classes) == 8
    return classes


KUHN = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
CUBIQUE = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def reseau(n, classes=None, dirs=None):
    """Sites de (Z/n)^3 ; fils (i, j, d) avec d le deplacement entier de i vers j."""
    idx = lambda p: (p[0] % n) * n * n + (p[1] % n) * n + (p[2] % n)
    fils = set()
    for p in itertools.product(range(n), repeat=3):
        D = classes[tuple(q % 2 for q in p)] if classes else [d for d in dirs] + [tuple(-c for c in d) for d in dirs]
        for d in D:
            q = tuple(p[i] + d[i] for i in range(3))
            i, j = idx(p), idx(q)
            fils.add((i, j, d) if (i, d) < (j, tuple(-c for c in d)) else (j, i, tuple(-c for c in d)))
    fils = sorted(fils)
    I = np.array([f[0] for f in fils]); J = np.array([f[1] for f in fils]); D = np.array([f[2] for f in fils], float)
    return n ** 3, I, J, D


def etat(N, I, J, D, a, F=None, U=None, repos=None):
    F = np.eye(3) if F is None else F
    B = a * D @ F.T
    if U is not None:
        B = B + U[J] - U[I]
    L = np.linalg.norm(B, axis=1)
    R = np.ones(len(L)) if repos is None else repos
    f = L - R
    return B, L, f


def viriel(B, L, f):
    return np.einsum('e,ea,eb->ab', f / L, B, B)


def viriels_de_site(N, I, J, B, L, f):
    w = 0.5 * np.einsum('e,ea,eb->eab', f / L, B, B)
    W = np.zeros((N, 3, 3))
    np.add.at(W, I, w); np.add.at(W, J, w)
    return W


def hessien(N, I, J, B, L, f):
    H = np.zeros((3 * N, 3 * N))
    for e in range(len(L)):
        nvec = B[e] / L[e]
        k = np.outer(nvec, nvec) + (f[e] / L[e]) * (np.eye(3) - np.outer(nvec, nvec))
        i, j = I[e], J[e]
        H[3 * i:3 * i + 3, 3 * i:3 * i + 3] += k; H[3 * j:3 * j + 3, 3 * j:3 * j + 3] += k
        H[3 * i:3 * i + 3, 3 * j:3 * j + 3] -= k; H[3 * j:3 * j + 3, 3 * i:3 * i + 3] -= k
    return H


def energie_relaxee(N, I, J, D, a, F):
    def fun(z):
        U = z.reshape(-1, 3)
        B, L, f = etat(N, I, J, D, a, F, U)
        G = np.zeros_like(U); w = (f / L)[:, None] * B
        np.add.at(G, J, w); np.add.at(G, I, -w)
        return 0.5 * (f ** 2).sum(), G.ravel()
    r = so.minimize(fun, np.zeros(3 * N), jac=True, method='L-BFGS-B', options=dict(gtol=1e-13, ftol=1e-18, maxiter=5000))
    return r.fun, float(np.abs(r.x).max())


def constantes(N, I, J, D, a, h=1e-3):
    V = N * a ** 3
    def d2(M):
        E0, _ = energie_relaxee(N, I, J, D, a, np.eye(3))
        Ep, up = energie_relaxee(N, I, J, D, a, np.eye(3) + h * M)
        Em, um = energie_relaxee(N, I, J, D, a, np.eye(3) - h * M)
        return (Ep - 2 * E0 + Em) / h ** 2 / V, max(up, um)
    c11, u1 = d2(np.diag([1.0, 0, 0]))
    cb, u2 = d2(np.diag([1.0, 1.0, 0]))
    s = np.zeros((3, 3)); s[0, 1] = s[1, 0] = 0.5
    c44, u3 = d2(s)
    c12 = (cb - 2 * c11) / 2
    return dict(C11=c11, C12=c12, C44=c44, B=(c11 + 2 * c12) / 3, Zener=2 * c44 / (c11 - c12), deplacement_interne_max=max(u1, u2, u3))


def partie_A():
    out = {}
    cl = classes_de_palier()
    out['classes'] = {str(c): dict(fils=len(D), axes=sum(1 for d in D if sum(abs(x) for x in d) == 1),
                                   faces=sum(1 for d in D if sum(abs(x) for x in d) == 2), espace=sum(1 for d in D if sum(abs(x) for x in d) == 3),
                                   moments=[sum(d[i] ** 2 for d in D) for i in range(3)],
                                   centrosymetrique=all(tuple(-x for x in d) in D for d in D)) for c, D in sorted(cl.items())}
    n = 6
    N, I, J, D = reseau(n, classes=cl)
    lam = np.linalg.norm(D, axis=1)
    out['A1'] = dict(porteurs=N, fils=len(lam), par_porteur=dict(axes=float((abs(lam - 1) < 1e-9).sum() / N), faces=float((abs(lam - R2) < 1e-9).sum() / N),
                     espace=float((abs(lam - R3) < 1e-9).sum() / N)), somme_lambda=float(lam.sum() / N), somme_lambda2=float((lam ** 2).sum() / N))
    a = lam.sum() / (lam ** 2).sum()
    B, L, f = etat(N, I, J, D, a)
    E = 0.5 * (f ** 2).sum()
    # equilibre : force sur chaque porteur
    G = np.zeros((N, 3)); w = (f / L)[:, None] * B; np.add.at(G, J, w); np.add.at(G, I, -w)
    out['A2'] = dict(a_etoile=float(a), E_par_porteur=float(E / N), E_par_fil=float(E / len(L)), force_residuelle_max=float(np.abs(G).max()))
    V = N * a ** 3
    part = {}
    for nom, l in (('axes', 1.0), ('faces', R2), ('espace', R3)):
        m = abs(lam - l) < 1e-9
        part[nom] = dict(force=float(f[m][0]), fL=float((f[m] * L[m])[0]), pression_partielle=float(-(f[m] * L[m]).sum() / (3 * V)))
    out['A3'] = part
    sig = viriel(B, L, f) / V
    out['A4'] = dict(sigma_moyen=sig.round(15).tolist(), norme_max=float(np.abs(sig).max()))
    # controle par derivee de l'energie : pression = -dE/dV
    h = 1e-5
    Ea = lambda s: 0.5 * (etat(N, I, J, D, s)[2] ** 2).sum()
    out['A4']['dE_da_a_etoile'] = float((Ea(a + h) - Ea(a - h)) / (2 * h))
    W = viriels_de_site(N, I, J, B, L, f) / a ** 3
    sites = {}
    for p in itertools.product(range(2), repeat=3):
        i = p[0] * n * n + p[1] * n + p[2]
        sites[str(p)] = dict(fils=len(cl[p]), sigma_diag=np.diag(W[i]).round(6).tolist(), hors_diag_max=float(np.abs(W[i] - np.diag(np.diag(W[i]))).max()),
                             pression=float(-np.trace(W[i]) / 3))
    out['A5'] = dict(sites=sites, moyenne=np.mean(W, axis=0).round(14).tolist())
    # stabilite
    stab = {}
    for nn in (6, 8):
        N2, I2, J2, D2 = reseau(nn, classes=cl)
        B2, L2, f2 = etat(N2, I2, J2, D2, a)
        ev = np.linalg.eigvalsh(hessien(N2, I2, J2, B2, L2, f2))
        stab[f'n={nn}'] = dict(plus_petite=float(ev[0]), nulles=int((abs(ev) < 1e-9).sum()), premiere_positive=float(ev[abs(ev) >= 1e-9].min()) if ev[0] > -1e-9 else None,
                               negatives=int((ev < -1e-9).sum()), plus_grande=float(ev[-1]))
    out['A6'] = stab
    out['A7'] = constantes(N, I, J, D, a)
    # affine exacte : C_abcd = (l0 / V) Somme L n_a n_b n_c n_d
    nv = B / L[:, None]
    out['A7']['affine'] = dict(C11=float((L * nv[:, 0] ** 4).sum() / V), C12=float((L * nv[:, 0] ** 2 * nv[:, 1] ** 2).sum() / V),
                               C1112=float((L * nv[:, 0] ** 3 * nv[:, 1]).sum() / V))
    A8 = {}
    for nom, s in (('a*/2 (juste apres un palier)', a / 2), ('0,9 a*', 0.9 * a), ('1,1 a*', 1.1 * a), ('2 a*', 2 * a)):
        Bs, Ls, fs = etat(N, I, J, D, s)
        p = -np.trace(viriel(Bs, Ls, fs)) / (3 * N * s ** 3); eps = 0.5 * (fs ** 2).sum() / (N * s ** 3)
        A8[nom] = dict(pression=float(p), formule=float((lam.sum() / N - s * (lam ** 2).sum() / N) / (3 * s ** 2)), energie_par_volume=float(eps), rapport_p_sur_energie=float(p / eps),
                       cisaillement_max=float(np.abs(viriel(Bs, Ls, fs) - np.diag(np.diag(viriel(Bs, Ls, fs)))).max()))
    out['A8'] = A8
    # A9 temoin analytique : cubique simple
    Nc, Ic, Jc, Dc = reseau(6, dirs=CUBIQUE)
    Bc, Lc, fc = etat(Nc, Ic, Jc, Dc, 1.0)
    cc = constantes(Nc, Ic, Jc, Dc, 1.0)
    out['A9_cubique_simple'] = dict(E=float(0.5 * (fc ** 2).sum()), sigma_max=float(np.abs(viriel(Bc, Lc, fc)).max()), **cc)
    # A10 temoin de discrimination : Kuhn
    Nk, Ik, Jk, Dk = reseau(6, dirs=KUHN)
    lk = np.linalg.norm(Dk, axis=1); ak = lk.sum() / (lk ** 2).sum()
    Bk, Lk, fk = etat(Nk, Ik, Jk, Dk, ak)
    out['A10_Kuhn'] = dict(a_etoile=float(ak), E_par_porteur=float(0.5 * (fk ** 2).sum() / Nk), sigma=(viriel(Bk, Lk, fk) / (Nk * ak ** 3)).round(6).tolist())
    # A11 temoin negatif : regle B
    Bb, Lb, fb = etat(N, I, J, D, a, repos=L.copy())
    out['A11_regle_B'] = dict(E=float(0.5 * (fb ** 2).sum()), sigma_max=float(np.abs(viriel(Bb, Lb, fb)).max()))
    return out


# ------------------------------------------------------------------ partie B : tissu fini de C-132 bis, rejoue par le programme d'origine
def partie_B():
    import c132_audit as c
    from c120 import vol6
    prises = {}
    orig = c.relax
    etat_run = dict(n=0)

    def relax_espion(m, Vref):
        r = orig(m, Vref)
        etat_run['m'] = m; etat_run['Vref'] = Vref; etat_run['r'] = r
        return r
    c.relax = relax_espion

    def analyse(m, Vref):
        ids = sorted(m.X); pos = {v: i for i, v in enumerate(ids)}; X = np.array([m.X[v] for v in ids])
        ed = list(m.rest); I = np.array([pos[e[0]] for e in ed]); J = np.array([pos[e[1]] for e in ed]); R = np.array([m.rest[e] for e in ed])
        B = X[J] - X[I]; L = np.linalg.norm(B, axis=1); f = L - R
        G = np.zeros_like(X); w = (f / L)[:, None] * B; np.add.at(G, J, w); np.add.at(G, I, -w)      # G = gradient de l'energie des ressorts
        Wt = float((f * L).sum())
        TT = list(m.T); V = np.array([vol6(m.X, t) / 6 for t in TT]); VR = np.array([Vref[t] for t in TT])
        act = [k for k in range(len(TT)) if V[k] <= 0.2 * VR[k] * (1 + TOL)]
        res = dict(porteurs=len(ids), fils=len(ed), cellules=len(TT), E=float(0.5 * (f ** 2).sum()), W=Wt, W_sur_somme_L=float(Wt / L.sum()),
                   gradient_ressorts_max=float(np.abs(G).max()), au_contact=len(act), fils_comprimes=float((f < 0).mean()))
        if act:
            A = np.zeros((3 * len(ids), len(act)))
            for col, k in enumerate(act):
                t = TT[k]; a_, b_, c_, d_ = (X[pos[v]] for v in t)
                gb = np.cross(c_ - a_, d_ - a_) / 6; gc = np.cross(d_ - a_, b_ - a_) / 6; gd = np.cross(b_ - a_, c_ - a_) / 6
                for v, g in zip(t, (-(gb + gc + gd), gb, gc, gd)):
                    A[3 * pos[v]:3 * pos[v] + 3, col] += g
            mu, rn = so.nnls(A, G.ravel(), maxiter=50 * len(act) + 1000)
            res.update(residu_KKT=float(rn), mu_max=float(mu.max()), trois_somme_mu_V=float(3 * (mu * V[act]).sum()))
        # viriels de site
        ws = 0.5 * np.einsum('e,ea,eb->eab', f / L, B, B); W = np.zeros((len(ids), 3, 3)); np.add.at(W, I, ws); np.add.at(W, J, ws)
        tr = np.trace(W, axis1=1, axis2=2); deg = np.bincount(np.concatenate([I, J]), minlength=len(ids))
        vs = np.zeros(len(ids))
        for k, t in enumerate(TT):
            for v in t:
                vs[pos[v]] += V[k] / 4
        rad = np.linalg.norm(X - X.mean(0), axis=1); med = np.median(rad); inn = rad <= med
        rho = spearmanr(deg, tr)
        res.update(spearman_degre_trace=float(rho.statistic), p_value=float(rho.pvalue), degre_max=int(deg.max()),
                   pression_interieure=float(-tr[inn].sum() / (3 * vs[inn].sum())), pression_exterieure=float(-tr[~inn].sum() / (3 * vs[~inn].sum())),
                   trace_moyenne_interieure=float(tr[inn].mean()), trace_moyenne_exterieure=float(tr[~inn].mean()),
                   trace_moyenne_degre_haut=float(tr[deg >= np.percentile(deg, 75)].mean()), trace_moyenne_degre_bas=float(tr[deg <= np.percentile(deg, 25)].mean()),
                   volume=float(V.sum()), sigma_moyen=(np.einsum('e,ea,eb->ab', f / L, B, B) / V.sum()).round(5).tolist())
        return res

    out = {}
    for seed in (1320, 1321, 1322):
        releves = {}
        c.HOOK = lambda row: releves.__setitem__(row['n'], dict(E_programme=row['E'], nact_programme=row['nact'], **analyse(etat_run['m'], etat_run['Vref'])))
        c.CHECK = (1, 3, 7, 15, 31, 63, 127)
        rows, seq = c.run('L', seed, 127)
        out[str(seed)] = releves
        for n_, r in releves.items():
            print(seed, n_, json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items() if k != 'sigma_moyen'}), flush=True)
    return out


if __name__ == '__main__':
    part = sys.argv[1]
    res = partie_A() if part == 'A' else partie_B()
    json.dump(res, open(f'c149c_{part}.json' if len(sys.argv) <= 2 else f'c149c_{part}_tol.json', 'w'), indent=1, ensure_ascii=False)
    if part == 'A':
        print(json.dumps(res, indent=1, ensure_ascii=False))
