#!/usr/bin/env python3
"""C-158c -- C-155A refait avec une etape SLSQP a contraintes explicites apres la penalite (Claude, 15 novembre 2026).
Predictions : c158c_prediction.txt. Tout le reste est c155a.py, inchange. Usage : python3 c158c.py <graine> [nmax]"""
import json, sys
import numpy as np, scipy.optimize as so
import c155a
from c155a import degagement, MARGE, EPSV, MARGEV

def polir(ts, VR):
    X0 = ts.X0(); z0 = X0.ravel(); N = len(X0); h = 1e-7
    cl0 = ts.degagements(X0); proches = {k: set(np.nonzero(v < 20 * MARGE)[0].tolist()) for k, v in cl0.items()}
    def E(z):
        X = z.reshape(-1, 3); D = X[ts.I] - X[ts.J]; L = np.linalg.norm(D, axis=1); G = np.zeros_like(X); w = ((L - ts.R) / L)[:, None] * D
        np.add.at(G, ts.I, w); np.add.at(G, ts.J, -w); return 0.5 * ((L - ts.R) ** 2).sum(), G.ravel()
    for tour in range(3):
        listes = {k: np.array(sorted(v), int) for k, v in proches.items()}
        def cons(z):
            X = z.reshape(-1, 3); out = [(ts.volumes(X) - EPSV * VR * (1 + MARGEV)) / VR]
            for k, idx in listes.items():
                if len(idx): out.append(degagement(X[ts.paires[k][idx]], k) - MARGE)
            return np.concatenate(out)
        def jac(z):
            X = z.reshape(-1, 3); a, b, c, d = (X[ts.T[:, i]] for i in range(4)); nt = len(ts.T); J = np.zeros((nt, N, 3)); r = np.arange(nt)
            gb = np.cross(c - a, d - a) / 6 / VR[:, None]; gc = np.cross(d - a, b - a) / 6 / VR[:, None]; gd = np.cross(b - a, c - a) / 6 / VR[:, None]
            J[r, ts.T[:, 1]] += gb; J[r, ts.T[:, 2]] += gc; J[r, ts.T[:, 3]] += gd; J[r, ts.T[:, 0]] -= gb + gc + gd
            rows = [J.reshape(nt, -1)]
            for k, idx in listes.items():
                if not len(idx): continue
                p = ts.paires[k][idx]; Pa = X[p]; pert = np.repeat(Pa[:, None], 48, axis=1)
                for q in range(24):
                    pert[:, 2 * q, q // 3, q % 3] += h; pert[:, 2 * q + 1, q // 3, q % 3] -= h
                for q in range(3 * k):
                    pert[:, 2 * q, 4 + q // 3, q % 3] += h; pert[:, 2 * q + 1, 4 + q // 3, q % 3] -= h
                val = degagement(pert.reshape(-1, 8, 3), k).reshape(len(idx), 48); dcl = (val[:, 0::2] - val[:, 1::2]) / (2 * h)
                Jc = np.zeros((len(idx), N, 3)); rr = np.arange(len(idx))
                for q in range(24):
                    if 12 <= q < 12 + 3 * k: continue
                    np.add.at(Jc, (rr, p[:, q // 3], q % 3), dcl[:, q])
                rows.append(Jc.reshape(len(idx), -1))
            return np.vstack(rows)
        try:
            r = so.minimize(lambda z: E(z)[0], z0, jac=lambda z: E(z)[1], method='SLSQP', constraints=[dict(type='ineq', fun=cons, jac=jac)], options=dict(ftol=1e-14, maxiter=400))
        except Exception as ex:
            return None, f'SLSQP erreur {type(ex).__name__}'
        X = r.x.reshape(-1, 3); cl = ts.degagements(X); ajout = False
        for k, v in cl.items():
            nouv = set(np.nonzero(v < MARGE - 1e-9)[0].tolist()) - proches[k]
            if nouv: proches[k] |= nouv; ajout = True
        if not ajout: break
    if not ts.admissible(X, VR): return None, 'poli non admissible'
    return X, f'SLSQP statut {r.status}, {r.nit} iterations, tour {tour + 1}'

_relaxe = c155a.Tissu.relaxe
def relaxe(self, VR, graine, n):
    X, g, essais = _relaxe(self, VR, graine, n)
    if X is None: return X, g, essais
    E0 = float(self.energie(X)); Xp, note = polir(self, VR)
    if Xp is not None and self.energie(Xp) <= E0 + 1e-5:
        for v in self.ids: self.m.X[v] = Xp[self.pos[v]]
        essais.append(dict(i='poli', statut='garde', E=float(self.energie(Xp)), E_avant=E0, note=note)); return Xp, 0.0, essais
    essais.append(dict(i='poli', statut='ecarte', E=None if Xp is None else float(self.energie(Xp)), E_avant=E0, note=note)); return X, g, essais
c155a.Tissu.relaxe = relaxe

if __name__ == '__main__':
    seed = int(sys.argv[1]); nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 31
    rowsU, seq, stU = c155a.trajectoire(seed, nmax, 'U'); rowsB, _, stB = c155a.trajectoire(seed, len(seq), 'B', replay=seq)
    json.dump(dict(graine=seed, U=dict(statut=stU, etats=rowsU), B=dict(statut=stB, etats=rowsB)), open(f'c158c_{seed}_etats.json', 'w'))
    print('STATUT', seed, 'U :', stU, '| B :', stB)
