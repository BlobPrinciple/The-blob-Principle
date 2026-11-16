#!/usr/bin/env python3
"""X-11 [EXPLORATOIRE] -- l'energie d'un tissu du laboratoire est-elle la somme, sur ses fils interieurs, de l'energie de couronne E(n_e) de C-176c ?
Autrement dit : le terme Somme_e f(n_e) de l'action du master decrit-il, sans parametre ajuste, l'energie relaxee sous la regle U ? (Claude, 16 novembre 2026).
Croissance c163c (mode A), graines 2100 a 2111 (celles de C-175c, rejouees pour garder la suite des fils), 16 naissances.
Usage : python3 x11_additivite.py G <debut> <fin> ; python3 x11_additivite.py S"""
import contextlib, glob, io, itertools, json, math, sys
import numpy as np, scipy.optimize as so
import c163c
from c120 import Mesh, SEEDS

DS = 2 * math.pi / math.acos(1 / 3); C2 = 0.0302174006


def Ecour(n):
    f = lambda z: 0.5 * (z[0] - 1) ** 2 + n * (math.sqrt(z[1] ** 2 + z[0] ** 2 / 4) - 1) ** 2 + n / 2 * (2 * z[1] * math.sin(math.pi / n) - 1) ** 2
    return so.minimize(f, [1.0, math.sqrt(3) / 2], method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-16, maxiter=4000)).fun


def croissance(a, b):
    out = {}
    for seed in range(a, b):
        with contextlib.redirect_stdout(io.StringIO()): rows, statut = c163c.trajectoire(seed, 16, 'A')
        m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); L = []
        for r in rows:
            E = m.inc(); e = tuple(r['fil_canonique']); m.bisect(e, m=3 + r['n'], E=E); E = m.inc(); F = {}
            for t in m.T:
                for f in itertools.combinations(sorted(t), 3): F.setdefault(f, []).append(t)
            bord = set(x for f, v in F.items() if len(v) == 1 for x in itertools.combinations(f, 2))
            L.append(dict(n=r['n'], fil=list(e), E=r['E'], methode=r['methode'], min_V=r['min_V_sur_Vref'], N=len(m.T), n_int=sorted(len(v) for x, v in E.items() if x not in bord), n_bord=sorted(len(v) for x, v in E.items() if x in bord)))
        out[seed] = dict(statut=statut, etats=L); json.dump(out, open(f'x11_G_{a}.json', 'w')); print(seed, statut, flush=True)


def synthese():
    H = {}
    for f in sorted(glob.glob('x11_G_*.json')): H.update(json.load(open(f)))
    ec = {n: Ecour(n) for n in range(3, 13)}; pts = []
    for s, d in H.items():
        for t in d['etats']:
            pts.append(dict(graine=s, n=t['n'], E=t['E'], somme_couronnes=sum(ec[k] for k in t['n_int']), somme_quadratique=sum(C2 * (k - DS) ** 2 for k in t['n_int']), fils_int=len(t['n_int']), libre=bool(t['min_V'] > 0.21), histo={k: t['n_int'].count(k) for k in sorted(set(t['n_int']))}))
    def stat(P, cle):
        x = np.array([p[cle] for p in P]); y = np.array([p['E'] for p in P]); ok = x > 0
        return dict(points=len(P), correlation=float(np.corrcoef(x, y)[0, 1]) if len(P) > 2 else None, pente_par_origine=float((x * y).sum() / (x * x).sum()), rapport_median=float(np.median(y[ok] / x[ok])) if ok.any() else None, ecart_abs_median=float(np.median(np.abs(y - x))))
    out = dict(E_couronne=ec, tous=dict(couronnes=stat(pts, 'somme_couronnes'), quadratique=stat(pts, 'somme_quadratique')), libres=dict(couronnes=stat([p for p in pts if p['libre']], 'somme_couronnes'), quadratique=stat([p for p in pts if p['libre']], 'somme_quadratique')),
               sans_fil_interieur=[(p['graine'], p['n'], p['E']) for p in pts if p['fils_int'] == 0][:40], histogramme_n_int=dict(sorted({k: sum(p['histo'].get(k, 0) for p in pts) for k in range(3, 13)}.items())), exemples=pts[::13][:16])
    print(json.dumps(out, indent=1)); json.dump(out, open('x11_synthese.json', 'w'), indent=1)


if __name__ == '__main__':
    croissance(int(sys.argv[2]), int(sys.argv[3])) if sys.argv[1] == 'G' else synthese()
