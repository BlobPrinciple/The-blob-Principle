#!/usr/bin/env python3
"""C-196c -- contre-calcul independant du C-196 de ChatGPT (Claude, 17 novembre 2026), d'apres son seul PROTOCOLE : cycle R, X, M, A dans quatre poches non couplees ; puis un ajout :
reserve inepuisable (R constant), croissance exponentielle ou non ? Modele d'AUDITEUR, pas le moteur du Blob. Predictions : c196c_prediction.txt. Usage : python3 c196c.py -> c196c.json"""
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

BETA, K, A_, D_ = 4.0, 40.0, 0.25, 0.08; T = [0, 0.1, 0.5, 1, 2, 5, 10, 20, 50, 150, 500]
POCHES = [(0.75, 0.25, 0, 0), (0.40, 0.16, 0.10, 0.01), (0.30, 0.14, 0.04, 0.10), (0.15, 0.15, 0.10, 0.075)]
def f(t, y, k=K, r_const=False):
    R, X, M, A = y; return [0.0 if r_const else -BETA * R * X, BETA * R * X - 4 * k * X ** 4 + 4 * D_ * A, k * X ** 4 - A_ * M, A_ * M - D_ * A]

if __name__ == '__main__':
    out = {}
    xs = brentq(lambda x: x + 4 * (K / A_ + K / D_) * x ** 4 - 1, 0, 1); ms, as_ = K * xs ** 4 / A_, K * xs ** 4 / D_; g = 16 * K * xs ** 3; J = np.array([[-g - A_, -g], [A_, -D_]]); vp = np.linalg.eigvals(J)
    out['point_fixe'] = dict(X=xs, M=ms, A=as_, libres=xs, matiere=4 * ms, vieillis=4 * as_, valeurs_propres=[complex(v).real for v in vp], parties_imaginaires=[complex(v).imag for v in vp]); print('point fixe', out['point_fixe'])
    out['poches'] = []
    for i, y0 in enumerate(POCHES):
        s = solve_ivp(f, (0, 500), y0, method='DOP853', rtol=1e-10, atol=1e-12, t_eval=T, dense_output=True); R, X, M, A = s.y; N = X + 4 * (M + A); Q = R + N
        tt = np.concatenate([np.linspace(0, 20, 20001), np.linspace(20, 500, 48001)[1:]]); Y = s.sol(tt); dM = K * Y[1] ** 4 - A_ * Y[2]; sg = np.sign(dM[np.abs(dM) > 1e-9]); chg = int((sg[1:] != sg[:-1]).sum())
        Nd = Y[1] + 4 * (Y[2] + Y[3]); out['poches'].append(dict(poche=i, t=T, R=R.tolist(), X=X.tolist(), M=M.tolist(), A=A.tolist(), Q_ecart=float(abs(Q - 1).max()), N_non_decroissant=bool((np.diff(Nd) >= -1e-9).all()), changements_de_signe_dM=chg, M_max=float(Y[2].max()), t_M_max=float(tt[Y[2].argmax()])))
        print('poche', i, '| Q %.1e' % abs(Q - 1).max(), '| N monotone', out['poches'][-1]['N_non_decroissant'], '| R(500) %.1e' % R[-1], '| final X M A %.6f %.6f %.6f' % (X[-1], M[-1], A[-1]), '| changements de signe de dM/dt', chg, '| M max %.4f a t=%.2f' % (Y[2].max(), tt[Y[2].argmax()]), flush=True)
    P = out['poches']
    for v in 'XMA':
        e = [max(p[v][j] for p in P) - min(p[v][j] for p in P) for j in range(len(T))]; out['ecart_' + v] = e; print('ecart max-min de', v, 'aux temps', T, ':', ['%.2e' % x for x in e])
    out['P4'] = [bool(max(p['M'][:7]) > 0.01 and max(p['A'][:7]) > 0.01) for p in P]; print('M > 0,01 et A > 0,01 avant t = 10 :', out['P4'])
    s0 = solve_ivp(f, (0, 50), (1.0, 0, 0, 0), method='DOP853', rtol=1e-10, atol=1e-12); out['sans_germe'] = [float(x) for x in s0.y[:, -1]]; print('sans germe', out['sans_germe'])
    # ajout : reserve inepuisable
    te = np.array([1, 10, 100, 1000, 2000, 5000, 10000.]); s = solve_ivp(f, (0, 1e4), POCHES[0], method='LSODA', rtol=1e-10, atol=1e-12, t_eval=te, args=(K, True)); R, X, M, A = s.y; N = X + 4 * (M + A)
    pente = lambda Z, a, b: float(np.log(Z[b] / Z[a]) / np.log(te[b] / te[a]))
    out['reserve_inepuisable'] = dict(t=te.tolist(), N=N.tolist(), X=X.tolist(), pente_N_1000_10000=pente(N, 3, 6), pente_X_1000_10000=pente(X, 3, 6), pente_N_100_1000=pente(N, 2, 3), rapport_N_10000_5000=float(N[6] / N[5]), part_libre=(X / N).tolist())
    print('reserve inepuisable : N', ['%.4g' % x for x in N], '| X', ['%.4g' % x for x in X], '| pentes N %.4f (100-1000 : %.4f), X %.4f' % (out['reserve_inepuisable']['pente_N_1000_10000'], out['reserve_inepuisable']['pente_N_100_1000'], out['reserve_inepuisable']['pente_X_1000_10000']), '| N(1e4)/N(5e3) %.4f' % (N[6] / N[5]), '| part libre', ['%.3g' % x for x in X / N])
    s = solve_ivp(f, (0, 5), POCHES[0], method='DOP853', rtol=1e-12, atol=1e-14, t_eval=[1, 2, 5], args=(0.0, True)); N = s.y[1] + 4 * (s.y[2] + s.y[3]); ex = 0.25 * np.exp(3 * np.array([1, 2, 5.]))
    out['temoin_sans_assemblage'] = dict(N=N.tolist(), exact=ex.tolist(), ecart_relatif=float(abs(N / ex - 1).max())); print('temoin k = 0 :', out['temoin_sans_assemblage'])
    json.dump(out, open('c196c.json', 'w'), indent=1)
