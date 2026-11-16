#!/usr/bin/env python3
"""C-174c -- classement des etats d'une croissance : minimum, point-selle, contraint (Claude, 16 novembre 2026). Predictions : c174c_prediction.txt (ecrites avant).
Usage : python3 c174c.py G <debut> <fin>  -> c174c_G_<debut>.jsonl ;  python3 c174c.py T (temoins) ;  python3 c174c.py S (synthese)"""
import contextlib, glob, io, itertools, json, math, sys
import numpy as np, scipy.optimize as so
import c163c, c132_audit as c132
from c155a import Tissu
from c120 import Mesh, SEEDS, vol6
from x1_regles import hessien, sortie_selle

NB = 12; TOL = 1e-6


def gradE(ts, X):
    d = X[ts.I] - X[ts.J]; L = np.linalg.norm(d, axis=1); g = np.zeros_like(X); f = ((L - ts.R) / L)[:, None] * d; np.add.at(g, ts.I, f); np.add.at(g, ts.J, -f); return g


def gradV(ts, X, k):
    a, b, c, d = (X[i] for i in ts.T[k]); g = np.zeros_like(X); gb = np.cross(c - a, d - a) / 6; gc = np.cross(d - a, b - a) / 6; gd = np.cross(b - a, c - a) / 6
    g[ts.T[k][1]] += gb; g[ts.T[k][2]] += gc; g[ts.T[k][3]] += gd; g[ts.T[k][0]] -= gb + gc + gd; return g.ravel()


def classe(m, Vref):
    ts = Tissu(m); X = ts.X0(); VR = np.array([Vref[t] for t in ts.TT]); V = ts.volumes(X); cl = ts.degagements(X)
    dg = min((float(v.min()) for v in cl.values() if len(v)), default=1.0); av = np.nonzero(V / VR < 0.2 + TOL)[0]; g = gradE(ts, X).ravel()
    r = dict(E=float(ts.energie(X)), gradient=float(np.abs(g).max()), min_V_sur_Vref=float((V / VR).min()), degagement_min=dg, planchers_actifs=int(len(av)), contact_actif=bool(dg < TOL))
    w = hessien(m)[0]; r['vp_min_libre'] = float(w[0])
    if r['contact_actif']: r['classe'] = 'contact : non tranche'
    elif len(av) == 0:
        r['directions'] = int((w < -TOL).sum()); r['classe'] = 'libre, selle' if r['directions'] else 'libre, minimum'
    else:
        A = np.array([-gradV(ts, X, k) for k in av]); lam, res = so.nnls(A.T, -g); r['multiplicateurs'] = [float(x) for x in lam]; r['residu_KKT'] = float(res)
        n = X.size; H = np.zeros((n, n)); ids = ts.ids; h = 1e-6
        for (a, b), R in m.rest.items():
            d = m.X[a] - m.X[b]; L = np.linalg.norm(d); u = d / L; K = np.outer(u, u) + (1 - R / L) * (np.eye(3) - np.outer(u, u)); i, j = 3 * ts.pos[a], 3 * ts.pos[b]
            H[i:i + 3, i:i + 3] += K; H[j:j + 3, j:j + 3] += K; H[i:i + 3, j:j + 3] -= K; H[j:j + 3, i:i + 3] -= K
        for k, l in zip(av, lam):
            if l <= 0: continue
            for q in range(n):
                e = np.zeros(n); e[q] = h; H[:, q] -= l * (gradV(ts, (X.ravel() + e).reshape(-1, 3), k) - gradV(ts, (X.ravel() - e).reshape(-1, 3), k)) / (2 * h)
        H = (H + H.T) / 2; u_, s_, vt = np.linalg.svd(A); rang = int((s_ > 1e-9).sum()); Z = vt[rang:].T; wr = np.linalg.eigvalsh(Z.T @ H @ Z)
        r['vp_min_reduite'] = float(wr[0]); r['directions'] = int((wr < -TOL).sum()); r['classe'] = 'plancher, selle' if r['directions'] else 'plancher, stationnaire stable'
        if res > 1e-5: r['classe'] = 'plancher, non stationnaire (residu %.1e)' % res
    return r


def croissance(a, b):
    f = open(f'c174c_G_{a}.jsonl', 'w')
    for seed in range(a, b):
        with contextlib.redirect_stdout(io.StringIO()): rows, statut = c163c.trajectoire(seed, NB, 'A')
        m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); Vref = {}
        for r in rows:
            n = r['n']; m.bisect(tuple(r['fil_canonique']), m=3 + n)
            for t in m.T:
                if t not in Vref: Vref[t] = vol6(m.X, t) / 6
            for t in list(Vref):
                if t not in m.T: del Vref[t]
            for v in m.X: m.X[v] = np.array(r['positions'][str(v)])
            c = classe(m, Vref); c.update(graine=seed, n=n, methode=r['methode'], admissible=r['admissible'], ecart_E=abs(c['E'] - r['E']), statut=statut)
            if c['classe'] == 'libre, selle':
                m2 = m.copy(); ns = sortie_selle(m2, dict(Vref)); c2 = classe(m2, {t: Vref[t] for t in m2.T}); c['sortie'] = dict(pas=ns, E=c2['E'], baisse=c['E'] - c2['E'], classe=c2['classe'], degagement_min=c2['degagement_min'], min_V_sur_Vref=c2['min_V_sur_Vref'])
            f.write(json.dumps(c) + '\n'); f.flush(); print(seed, n, c['classe'], 'E %.9f' % c['E'], 'vp %.2e' % c['vp_min_libre'], c.get('sortie', ''), flush=True)


def temoins():
    import c173c
    out = {}
    for nom, n in (('couronne de cinq', 5), ('couronne de sept', 7)):
        X, I, c = c173c.couronne(n); R = np.ones(len(I)); r = so.minimize(c173c.energie, X.ravel(), args=(I, R), jac=True, method='L-BFGS-B', options=dict(gtol=1e-14, ftol=1e-18, maxiter=20000))
        w = c173c.hess(r.x.reshape(-1, 3), I, R); out[nom] = dict(E=float(r.fun), directions=int((w < -TOL).sum()), modes_nuls=int((np.abs(w) < TOL).sum()))
    m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); w = hessien(m)[0]; out['tetraedre'] = dict(E=m.energy(), directions=int((w < -TOL).sum()), modes_nuls=int((np.abs(w) < TOL).sum()))
    print(json.dumps(out, indent=1)); json.dump(out, open('c174c_T.json', 'w'), indent=1)


def synthese():
    L = [json.loads(l) for f in sorted(glob.glob('c174c_G_*.jsonl')) for l in open(f)]; from collections import Counter
    out = dict(etats=len(L), graines=len(set(x['graine'] for x in L)), classes=dict(Counter(x['classe'].split(' (')[0] for x in L)), par_naissance={n: dict(Counter(x['classe'].split(' (')[0] for x in L if x['n'] == n)) for n in range(1, NB + 1)},
               planchers_actifs=sum(x['planchers_actifs'] > 0 for x in L), contacts_actifs=sum(x['contact_actif'] for x in L), ecart_E_max=max(x['ecart_E'] for x in L), gradient_max_libres=max((x['gradient'] for x in L if x['classe'].startswith('libre')), default=None),
               selles=[dict(graine=x['graine'], n=x['n'], vp=x['vp_min_libre'], directions=x['directions'], sortie=x.get('sortie')) for x in L if x['classe'] == 'libre, selle'],
               selles_plancher=[dict(graine=x['graine'], n=x['n'], vp=x['vp_min_reduite'], residu=x['residu_KKT']) for x in L if x['classe'] == 'plancher, selle'], statuts=dict(Counter(x['statut'] for x in L if x['n'] == max(y['n'] for y in L if y['graine'] == x['graine']))))
    print(json.dumps(out, indent=1)); json.dump(out, open('c174c_synthese.json', 'w'), indent=1)


if __name__ == '__main__':
    if sys.argv[1] == 'G': croissance(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == 'T': temoins()
    else: synthese()
