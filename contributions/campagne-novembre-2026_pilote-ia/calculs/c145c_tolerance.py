#!/usr/bin/env python3
"""C-145 / PR-3 -- differend K4, A1, S : effet de la tolerance de regroupement des contacts (Claude, 13 novembre 2026).
Prediction : c145c_tolerance_prediction.txt. c145c.py inchange, sauf la tolerance de simultaneite de reflect3."""
import json
import pathlib
import sys
from multiprocessing import Pool

import numpy as np

ICI = pathlib.Path(__file__).resolve().parent
sys.path[:0] = [str(ICI), str(ICI.parent)]
import c145c  # noqa: E402

TOL = 1e-9


def reflect3_tol(s, acore, n, PI, PJ, facteur=2.0):
    m = 3 * n
    x = s[:m].reshape(n, 3)
    v = s[m:2 * m].reshape(n, 3)
    d = x[PJ] - x[PI]
    r = np.sqrt((d * d).sum(1))
    nrm = d / r[:, None]
    u = ((v[PJ] - v[PI]) * nrm).sum(1)
    near = [z for z in range(len(PI)) if r[z] <= acore + TOL]
    con = [z for z in near if u[z] < 0]
    if not con:
        return [], False, 0.0
    A = np.zeros((len(con), m))
    for q, z in enumerate(con):
        A[q, 3 * PI[z]:3 * PI[z] + 3] = -nrm[z]
        A[q, 3 * PJ[z]:3 * PJ[z] + 3] = nrm[z]
    vf = v.ravel().copy()
    vn = vf - facteur * A.T @ (np.linalg.pinv(A @ A.T, rcond=1e-10) @ (A @ vf))
    k0 = .5 * float(vf @ vf)
    s[m:2 * m] = vn
    v2 = vn.reshape(n, 3)
    u2 = ((v2[PJ] - v2[PI]) * nrm).sum(1)
    ok = all(u2[z] >= -1e-12 for z in near)
    return con, ok, .5 * float(vn @ vn) - k0


def fmt(x, nd):
    return ('aucune' if x['t1'] is None else f"{x['t1']:.{nd}f}") + {'PANY': 'P', 'RECAPT': 'r', 'LIE': 'l'}[x['statut']]


def une(arg):
    global TOL
    tol, P, cad, g = arg
    TOL = tol
    c145c.reflect3 = reflect3_tol
    o = c145c.run3(top='K4', src='S', stop='A1', a=0.75, D=1.0, g0=0.0, P=P, cad=cad, g=g, solver='rk', sub=1)
    return dict(tol=tol, P=P, cad=cad, g=g, statut=o['statut'], t1=o['t1'], ncol=o['ncol'], nsimul=o['nsimul'], rmin=o['rmin'],
                residu=o['residu_abs'], ambigu=o['ambigu'])


if __name__ == '__main__':
    taches = [(tol, P, cad, g) for tol in (1e-9, 1e-7, 1e-6, 1e-5) for P in (0.25, 0.5) for cad in ('1/2', '1') for g in range(0, 9)]
    with Pool(2) as pool:
        res = pool.map(une, taches, chunksize=2)
    (ICI / 'c145c_tolerance.json').write_text(json.dumps(res, indent=0, default=str))
    cg = {1: 7.1356, 2: 7.1040, 3: 5.1392, 4: 5.7091, 5: 7.4639, 6: 7.4639, 7: 7.4639, 8: 7.4639}
    for tol in (1e-9, 1e-7, 1e-6, 1e-5):
        r = [x for x in res if x['tol'] == tol]
        dur = sum(x['statut'] == 'PANY' for x in r if x['g'] > 0)
        dur0 = sum(x['statut'] == 'PANY' for x in r if x['g'] == 0)
        sel = sorted((x for x in r if x['P'] == 0.5 and x['cad'] == '1' and x['g'] > 0), key=lambda x: x['g'])
        proches = sum(1 for x in sel if x['t1'] is not None and abs(x['t1'] - cg[x['g']]) < 0.1)
        print(f"tol={tol:g} durables perturbes {dur}/32, exacts {dur0}/4 ; P=1/2 c=1 : proches de ChatGPT {proches}/8 ; t1 = "
              + ' '.join(fmt(x, 4) for x in sel)
              + f" ; rmin/a min {min(x['rmin'] for x in r) / 0.75:.9f} ; residu max {max(x['residu'] for x in r):.1e} ; ambigus {sum(x['ambigu'] is not None for x in r)}")
        for (P, cad) in ((0.25, '1/2'), (0.25, '1'), (0.5, '1/2')):
            s2 = sorted((x for x in r if x['P'] == P and x['cad'] == cad), key=lambda x: x['g'])
            print(f"     P={P} c={cad} : " + ' '.join(fmt(x, 3) for x in s2))
