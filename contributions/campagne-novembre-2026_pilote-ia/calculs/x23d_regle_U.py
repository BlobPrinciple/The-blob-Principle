#!/usr/bin/env python3
"""X-23 D -- exploratoire : sous la regle U (tous les liens de longueur naturelle 1), une coque fermee admet-elle une forme sans tension a l'etage d ?
Prediction scellee : x23d_regle_U_prediction.txt. Claude, 22 novembre 2026."""
import json, sys, time
import numpy as np
from scipy.optimize import least_squares
from x23_outils import liens_des_cellules
from x23_coques import bord_du_simplexe, mitose_arete, naissance_en_volume


def forme(n, liens, d, rng, departs=40):
    I = np.array([l[0] for l in liens]); J = np.array([l[1] for l in liens])
    meilleur = np.inf; confondus = None
    def res(x):
        p = x.reshape(n, d)
        return np.linalg.norm(p[I] - p[J], axis=1) - 1.0
    def jac(x):
        p = x.reshape(n, d); v = p[I] - p[J]; L = np.linalg.norm(v, axis=1)[:, None]; u = v / np.maximum(L, 1e-300)
        Jm = np.zeros((len(liens), n * d))
        for r in range(len(liens)):
            Jm[r, d * I[r]:d * I[r] + d] = u[r]; Jm[r, d * J[r]:d * J[r] + d] = -u[r]
        return Jm
    propre = np.inf                                          # meilleur ecart parmi les formes SANS sommets confondus (amendement declare : la premiere execution
    for t in range(departs):                                 # s'arretait a la premiere forme trouvee, souvent un pliage ou deux sommets non lies coincident)
        x0 = rng.standard_normal(n * d) * (0.6 + 0.6 * rng.random())
        s = least_squares(res, x0, jac=jac, method='lm' if len(liens) >= n * d else 'trf', xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
        e = float(np.abs(s.fun).max())
        p = s.x.reshape(n, d)
        D = np.linalg.norm(p[:, None, :] - p[None, :, :], axis=2) + np.eye(n) * 9
        meilleur = min(meilleur, e)
        if D.min() > 1e-3:
            propre = min(propre, e)
        if propre < 1e-11:
            break
    return meilleur, propre


if __name__ == '__main__':
    out = dict(rang2={}, rang3={})
    for V in (5, 6, 7, 8, 10, 12, 14, 16, 20):
        lignes = []
        for g in range(12):
            rng = np.random.default_rng(4000 + 100 * V + g)
            cel, n = bord_du_simplexe(2)
            while n < V:
                L = liens_des_cellules(cel); a, b = L[rng.integers(len(L))]
                cel = mitose_arete(cel, a, b, n); n += 1
            L = liens_des_cellules(cel)
            r = {}
            for d in (2, 3, 4):
                e, dmin = forme(n, L, d, rng)
                r[d] = (e, dmin)
            lignes.append(r)
        out['rang2'][V] = [[list(x[d]) for d in (2, 3, 4)] for x in lignes]
        print('rang 2, V =', V, '| forme a liens tous egaux trouvee (ecart < 1e-9) : etage 2 :', sum(x[2][0] < 1e-9 for x in lignes), '/ 12 ; etage 3 :', sum(x[3][0] < 1e-9 for x in lignes),
              '/ 12 (dont sans sommets confondus :', sum(x[3][1] < 1e-9 for x in lignes), ') ; etage 4 :', sum(x[4][0] < 1e-9 for x in lignes), '/ 12', flush=True)
    for V in (6, 8, 10, 12):
        for mode in ('empilee', 'mitose'):
            ok = 0; tot = 8; justes = 0
            for g in range(tot):
                rng = np.random.default_rng(6000 + 100 * V + g + (0 if mode == 'empilee' else 50))
                cel, n = bord_du_simplexe(3)
                while n < V:
                    if mode == 'empilee':
                        cel = naissance_en_volume(cel, int(rng.integers(len(cel))), n)
                    else:
                        L = liens_des_cellules(cel); a, b = L[rng.integers(len(L))]
                        cel = mitose_arete(cel, a, b, n)
                    n += 1
                L = liens_des_cellules(cel)
                justes += (len(L) == 4 * n - 10)
                e, dmin = forme(n, L, 4, rng)
                ok += e < 1e-9
            out['rang3'][f'{mode}_{V}'] = [ok, tot, justes]
            print('rang 3,', mode, 'V =', V, ': forme trouvee dans R^4 :', ok, '/', tot, '| coques justes (E = 4V - 10) :', justes, flush=True)
    json.dump(out, open('x23d_regle_U.json', 'w'), indent=1)
