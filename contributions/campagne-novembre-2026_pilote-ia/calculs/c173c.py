#!/usr/bin/env python3
"""C-173c -- contre-calcul du C-173 de ChatGPT (Claude, 16 novembre 2026). NON a l'aveugle : voir c173c_prediction.txt (ecrit avant le calcul).
Usage : python3 c173c.py HET | UNI | DYN   -> c173c_<partie>.json"""
import itertools, json, math, sys
import numpy as np, scipy.optimize as so, scipy.integrate as si
from c120 import Mesh, SEEDS, vol6
from c155a import Tissu

VREG = 1 / (6 * math.sqrt(2))


# ---------- HET : couronne en toutes coordonnees, liens de ceinture de longueur naturelle 1 + delta
def couronne(n):
    h, r = 1.0, math.sqrt(3) / 2
    X = [[0, 0, h / 2], [0, 0, -h / 2]] + [[r * math.cos(2 * math.pi * j / n), r * math.sin(2 * math.pi * j / n), 0] for j in range(n)]
    L = [(0, 1, 0)] + [(p, 2 + j, 0) for p in (0, 1) for j in range(n)] + [(2 + j, 2 + (j + 1) % n, 1) for j in range(n)]
    return np.array(X, float), np.array([l[:2] for l in L]), np.array([l[2] for l in L])


def energie(z, I, R):
    X = z.reshape(-1, 3); d = X[I[:, 0]] - X[I[:, 1]]; L = np.linalg.norm(d, axis=1); g = np.zeros_like(X); f = ((L - R) / L)[:, None] * d
    np.add.at(g, I[:, 0], f); np.add.at(g, I[:, 1], -f); return 0.5 * ((L - R) ** 2).sum(), g.ravel()


def hess(X, I, R):
    n = len(X); H = np.zeros((3 * n, 3 * n))
    for (a, b), r in zip(I, R):
        d = X[a] - X[b]; L = np.linalg.norm(d); u = d / L; K = np.outer(u, u) + (1 - r / L) * (np.eye(3) - np.outer(u, u))
        H[3 * a:3 * a + 3, 3 * a:3 * a + 3] += K; H[3 * b:3 * b + 3, 3 * b:3 * b + 3] += K; H[3 * a:3 * a + 3, 3 * b:3 * b + 3] -= K; H[3 * b:3 * b + 3, 3 * a:3 * a + 3] -= K
    return np.linalg.eigvalsh(H)


def Emin(n, delta, detail=False):
    X, I, c = couronne(n); R = 1.0 + delta * c; rng = np.random.Generator(np.random.PCG64(1000 * n + 7)); z = (X + 1e-3 * rng.standard_normal(X.shape)).ravel()
    r = so.minimize(energie, z, args=(I, R), jac=True, method='BFGS', options=dict(gtol=1e-13, maxiter=20000))
    r = so.minimize(energie, r.x, args=(I, R), jac=True, method='L-BFGS-B', options=dict(gtol=1e-14, ftol=1e-18, maxiter=20000, maxcor=40))
    if not detail: return r.fun
    w = hess(r.x.reshape(-1, 3), I, R); X2 = r.x.reshape(-1, 3); vol = [abs(vol6(X2, (0, 1, 2 + j, 2 + (j + 1) % n))) / 6 / VREG for j in range(n)]
    return dict(n=n, delta=delta, E=float(r.fun), gradient=float(np.abs(r.jac).max()), vp_min=float(w[0]), directions_de_descente=int((w < -1e-7).sum()), modes_nuls=int((np.abs(w) < 1e-7).sum()),
                volume_min_sur_Vreg=float(min(vol)), ceinture=sorted(float(np.linalg.norm(X2[2 + j] - X2[2 + (j + 1) % n])) for j in range(n)))


def HET():
    out = dict(table=[], seuils={}, etats=[])
    for d in (-0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15):
        E = {n: Emin(n, d) for n in (3, 4, 5, 6, 7)}; out['table'].append(dict(delta=d, E=E, meilleur=min(E, key=E.get))); print('delta %+.2f' % d, ' '.join('E%d=%.9f' % (n, E[n]) for n in E), 'meilleur', out['table'][-1]['meilleur'], flush=True)
    s56 = so.brentq(lambda d: Emin(5, d) - Emin(6, d), -0.15, -0.01, xtol=1e-13); s45 = so.brentq(lambda d: Emin(4, d) - Emin(5, d), 0.05, 0.20, xtol=1e-13)
    out['seuils'] = dict(E5_egale_E6=s56, E4_egale_E5=s45, ecart_a_chatgpt=[abs(s56 + 0.0653221354369), abs(s45 - 0.108894144708)]); print('SEUILS', out['seuils'], flush=True)
    for d in (s56, 0.0, s45):
        for n in (4, 5, 6):
            r = Emin(n, d, True); out['etats'].append(r); print('etat', json.dumps(r), flush=True)
    for n, d in ((4, math.sqrt(1.5) - 1), (5, math.sqrt(3) * math.sin(math.pi / 5) - 1), (6, math.sqrt(3) / 2 - 1)): print('temoin energie nulle', n, d, Emin(n, d)); out.setdefault('temoins_nuls', []).append([n, d, Emin(n, d)])
    json.dump(out, open('c173c_HET.json', 'w'), indent=1)


# ---------- UNI : lois a sens unique
def UNI():
    out = []
    for n in range(3, 9):
        s, s2 = math.sin(math.pi / n), math.sin(2 * math.pi / n)
        # tension seule : energie nulle ssi h <= 1, q <= 1, b <= 1 ; on maximise le volume de cellule V = h r^2 sin(2 pi / n) / 6
        best = max(((h * min(1 - h * h / 4, 1 / (4 * s * s)) * s2 / 6 / VREG, h) for h in np.linspace(0.01, 1, 991)))
        h = best[1]; r = math.sqrt(min(1 - h * h / 4, 1 / (4 * s * s))); q = math.sqrt(r * r + h * h / 4); b = 2 * r * s
        Et = 0.5 * (max(h - 1, 0) ** 2 + 2 * n * max(q - 1, 0) ** 2 + n * max(b - 1, 0) ** 2)
        # compression seule : energie nulle ssi toutes les longueurs >= 1 ; exemple le plus serre : h = 1, r = max(sqrt(3)/2, 1/(2 sin(pi/n)))
        rc = max(math.sqrt(3) / 2, 1 / (2 * s)); qc = math.sqrt(rc * rc + 0.25); bc = 2 * rc * s
        Ec = 0.5 * (min(1 - 1, 0) ** 2 + 2 * n * min(qc - 1, 0) ** 2 + n * min(bc - 1, 0) ** 2)
        d = dict(n=n, tension=dict(h=h, r=r, q=q, b=b, E=Et, volume_sur_Vreg=best[0]), compression=dict(h=1.0, r=rc, q=qc, b=bc, E=Ec, volume_sur_Vreg=rc * rc * s2 / 6 / VREG)); out.append(d); print(json.dumps(d), flush=True)
    json.dump(out, open('c173c_UNI.json', 'w'), indent=1)


# ---------- DYN : descente libre apres deux divisions concurrentes de M30
def charge():
    d = json.load(open('c171r_etat_m30_chatgpt.json')); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F')
    m.X = {int(k): np.array(v) for k, v in d['vertices'].items()}; m.T = set(tuple(t) if vol6(m.X, tuple(t)) > 0 else (t[1], t[0], t[2], t[3]) for t in d['tetrahedra']); m.nv = max(m.X) + 1
    m.rest = {e: 1.0 for t in m.T for e in itertools.combinations(sorted(t), 2)}; return m


def branche(e):
    m = charge(); E0 = m.energy(); m.bisect(e); ts = Tissu(m); I = np.stack([ts.I, ts.J], axis=1); R = np.asarray(ts.R, float); z0 = ts.X0().ravel()
    f = lambda t, z: -energie(z, I, R)[1]
    sol = si.solve_ivp(f, (0, 300), z0, method='LSODA', rtol=1e-10, atol=1e-12, dense_output=True)
    En = lambda t: energie(sol.sol(t), I, R)[0]
    def chev(t):
        cl = ts.degagements(sol.sol(t).reshape(-1, 3)); return int(sum((v <= 1e-10).sum() for v in cl.values())), float(min(v.min() for v in cl.values() if len(v)))
    return dict(m=m, ts=ts, E0=E0, En=En, chev=chev, sol=sol)


def DYN():
    A, C = branche((0, 9)), branche((16, 19)); D = lambda t: A['En'](t) - C['En'](t)
    temps = [0, 0.01, 0.1, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 300]; out = dict(D=[[t, float(D(t))] for t in temps], E_M30=A['E0'])
    print('D', out['D'], flush=True)
    tc = so.brentq(D, 10, 20, xtol=1e-12); out['croisement'] = tc; out['ecart_a_chatgpt'] = abs(tc - 19.263714551297404); print('CROISEMENT', tc, out['ecart_a_chatgpt'], flush=True)
    grille = sorted(set([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 7, 10, 11, 12, 13, 14, 15, 18, 19, tc, 20, 25, 30, 50, 75, 100, 150, 200, 250, 300]))
    for nom, B in (('A', A), ('C2', C)):
        L = [(t, *B['chev'](t)) for t in grille]; bad = [t for t, c, _ in L if c > 0]
        # premier contact : dichotomie sur le degagement minimal entre le dernier instant sain avant le premier mauvais et celui-ci
        prem = None
        if bad:
            t1 = bad[0]; t0 = max([t for t in grille if t < t1], default=0.0)
            if B['chev'](t0)[0] == 0:
                for _ in range(50):
                    tm = (t0 + t1) / 2
                    if B['chev'](tm)[0] > 0: t1 = tm
                    else: t0 = tm
                prem = t1
        out[nom] = dict(cout_insertion=float(B['En'](0) - B['E0']), cout_a_300=float(B['En'](300) - B['E0']), chevauchements=[[t, c, dg] for t, c, dg in L], instants_mauvais=bad, au_croisement=B['chev'](tc)[0], a_300=B['chev'](300)[0],
                        premier_contact=prem, energie_au_premier_contact=(float(B['En'](prem)) if prem is not None else None),
                        volume_min_sur_Vreg=float(min(B['ts'].volumes(B['sol'].sol(t).reshape(-1, 3)).min() for t in grille) / VREG))
        print(nom, json.dumps({k: v for k, v in out[nom].items() if k != 'chevauchements'}), flush=True)
    json.dump(out, open('c173c_DYN.json', 'w'), indent=1)


if __name__ == '__main__':
    dict(HET=HET, UNI=UNI, DYN=DYN)[sys.argv[1]]()
