# CONTRE-AUDIT DE C-142B / PR-1 (protocole figé et exécuté par ChatGPT, fil principal, 12 nov. 2026, empreinte 2e6f0bd9…).
# Réécriture indépendante (numpy vectorisé, sans numba) des règles du protocole :
#   tétraèdre régulier d'arête 1, 4 masses unité, 6 liens de Morse U(r) = (1 - exp(-(r-1)))^2 ; amortisseur gamma sur la vitesse radiale relative de chaque lien ;
#   tentative bloquée au porteur 0 : impulsion interne dv = alpha * g (g = vecteurs unitaires vers les trois voisins, opposé sur 0), alpha tel que le travail vaille W ;
#   RK4, dt = T0/512, T0 = 2 pi / sqrt 2 ; 24 tentatives au plus ; coupure du premier lien tel que r >= 1 + ln 20 avec vitesse sortante ; plus d'impulsion après ;
#   arrêt une période après la coupure ; grille : K4 et étoile, gamma 0 / 0,04 / 0,12, W 0 / 0,25 / 0,5, intervalles 256, 410, 512, 614 pas.
# PARTIE A : recoupement des 72 bras. PARTIE B : même dynamique intégrée par un autre schéma (DOP853, tolérance 1e-11) sur les bras K4 alimentés.
# PARTIE C (complément d'audit annoncé à ChatGPT AVANT calcul, 20 h 44 UTC) : contrôle à puissance moyenne égale (W proportionnel à l'intervalle, même durée,
#   même énergie totale). Prédiction enregistrée : les quatre cadences donnent le même verdict dans au moins cinq régimes sur six.
import numpy as np, itertools, math, json, sys, time
from multiprocessing import Pool
from scipy.integrate import solve_ivp
EDGE = np.array(list(itertools.combinations(range(4), 2))); I, J = EDGE[:, 0], EDGE[:, 1]
M = np.zeros((4, 6))
for z, (i, j) in enumerate(EDGE): M[i, z] = 1.0; M[j, z] = -1.0
P0 = np.array([[0, 0, 0], [1, 0, 0], [.5, math.sqrt(3) / 2, 0], [.5, math.sqrt(3) / 6, math.sqrt(2 / 3)]], float)
T0 = 2 * math.pi / math.sqrt(2); DT = T0 / 512; CUT = 1 + math.log(20.0)
STAR = np.array([0 in z for z in EDGE]); K4 = np.ones(6, bool)

def rates(x, v, act, gamma):
    d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); a = np.exp(-(r - 1)); s = ((v[J] - v[I]) * d).sum(1) / r
    f = np.where(act, 2 * (1 - a) * a + gamma * s, 0.0)
    return M @ (d * (f / r)[:, None]), np.where(act, gamma * s * s, 0.0)

def rk4(x, v, q, act, gamma, dt):
    a1, q1 = rates(x, v, act, gamma); v2 = v + .5 * dt * a1
    a2, q2 = rates(x + .5 * dt * v, v2, act, gamma); v3 = v + .5 * dt * a2
    a3, q3 = rates(x + .5 * dt * v2, v3, act, gamma); v4 = v + dt * a3
    a4, q4 = rates(x + dt * v3, v4, act, gamma)
    return x + dt / 6 * (v + 2 * v2 + 2 * v3 + v4), v + dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4), q + dt / 6 * (q1 + 2 * q2 + 2 * q3 + q4)

def impulse(x, v, act, W):
    g = np.zeros((4, 3))
    for z in range(6):
        if act[z] and (I[z] == 0 or J[z] == 0):
            o = J[z] if I[z] == 0 else I[z]; u = (x[o] - x[0]); u = u / np.linalg.norm(u); g[o] += u; g[0] -= u
    aa = (v * g).sum(); bb = (g * g).sum()
    if bb < 1e-20: return v, None
    al = (-aa + math.sqrt(aa * aa + 2 * bb * W)) / bb; vn = v + al * g
    return vn, .5 * ((vn * vn).sum() - (v * v).sum())

def potential(x, act):
    d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); return float(np.where(act, (1 - np.exp(-(r - 1))) ** 2, 0.0).sum())

def run(graph, gamma, W, steps, n_events=24, dt=DT, sub=1):
    """sub = raffinement du pas (dt/sub) ; les impulsions restent aux mêmes instants"""
    x = P0.copy(); v = np.zeros((4, 3)); act = (K4 if graph == 'K4' else STAR).copy(); q = np.zeros(6)
    src = n_events * W; frag = 0.0; E0 = src; nimp = 0; tcut = -1.0; ecut = -1; stop_at = None; t = 0.0
    h = dt / sub; per = steps * sub
    for st in range(per * n_events):
        if st % per == 0 and tcut < 0 and W > 0:
            vn, w = impulse(x, v, act, W)
            if w is not None: v = vn; src -= w; nimp += 1
        x, v, q = rk4(x, v, q, act, gamma, h); t = (st + 1) * h
        if tcut < 0:
            d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); out = ((v[J] - v[I]) * d).sum(1) > 0
            hit = np.where(act & (r >= CUT) & out)[0]
            if len(hit):
                z = int(hit[0]); frag += (1 - math.exp(-(r[z] - 1))) ** 2; act[z] = False; tcut = t; ecut = z; stop_at = st + 1 + per
        if stop_at is not None and st + 1 >= stop_at: break
    kin = .5 * float((v * v).sum()); pot = potential(x, act); rem = float(q[(I != 0) & (J != 0)].sum())
    return dict(graph=graph, gamma=gamma, W=W, steps=steps, cut=tcut >= 0, tcut=tcut, edge=tuple(int(k) for k in EDGE[ecut]) if ecut >= 0 else None, impulses=nimp, duree=t,
                Ekin=kin, Epot=pot, Q=float(q.sum()), Qdist=rem, part_dist=(rem / float(q.sum())) if q.sum() > 1e-15 else None, source=src, Efrag=frag,
                residu=src + kin + pot + float(q.sum()) + frag - E0, Qlien=[float(k) for k in q])

def run_dop(gamma, W, steps, n_events=24):
    """même règle, intégrateur DOP853 à tolérance serrée ; coupure détectée par événement"""
    act = K4.copy(); y = np.concatenate([P0.ravel(), np.zeros(12), np.zeros(6)]); nimp = 0; tcut = -1.0; ecut = None
    def rhs(t, y):
        x = y[:12].reshape(4, 3); v = y[12:24].reshape(4, 3); a, qd = rates(x, v, act, gamma); return np.concatenate([v.ravel(), a.ravel(), qd])
    def ev(t, y):
        x = y[:12].reshape(4, 3); d = x[J] - x[I]; return float((np.sqrt((d * d).sum(1)) - CUT).max())
    ev.terminal = True; ev.direction = 1
    for k in range(n_events):
        x = y[:12].reshape(4, 3); v = y[12:24].reshape(4, 3); vn, w = impulse(x, v, act, W); y[12:24] = vn.ravel(); nimp += 1
        sol = solve_ivp(rhs, (k * steps * DT, (k + 1) * steps * DT), y, method='DOP853', rtol=1e-11, atol=1e-13, events=ev)
        y = sol.y[:, -1].copy()
        if sol.status == 1:
            x = y[:12].reshape(4, 3); d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); z = int(np.argmax(r)); tcut = float(sol.t[-1]); ecut = tuple(int(q) for q in EDGE[z]); break
    return dict(gamma=gamma, W=W, steps=steps, cut=tcut >= 0, tcut=tcut, edge=ecut, impulses=nimp, Q=float(y[24:].sum()), Qdist=float(y[24:][(I != 0) & (J != 0)].sum()))

def job(a):
    kind = a[0]
    if kind == 'A': return ('A', run(*a[1:]))
    if kind == 'B': return ('B', run_dop(*a[1:]))
    if kind == 'C':
        _, gamma, P, steps = a; n = round(12288 / steps); W = P * steps / 512
        r = run('K4', gamma, W, steps, n_events=n); r['P'] = P; return ('C', r)
    if kind == 'D':                                   # convergence dt/2 et dt/4 sur les deux cas annoncés par le protocole
        _, W, sub = a; r = run('K4', .04, W, 512, sub=sub); r['sub'] = sub; return ('D', r)

if __name__ == '__main__':
    jobs = [('A', g, ga, W, s) for g in ('K4', 'star') for ga in (0., .04, .12) for W in (0., .25, .5) for s in (256, 410, 512, 614)]
    jobs += [('B', ga, W, s) for ga in (0., .04, .12) for W in (.25, .5) for s in (256, 410, 512, 614)]
    jobs += [('C', ga, P, s) for ga in (.04, .12) for P in (.25, .5, 1.0) for s in (256, 410, 512, 614)]
    jobs += [('D', W, sub) for W in (.25, .5) for sub in (2, 4)]
    out = {'A': [], 'B': [], 'C': [], 'D': []}; t0 = time.time()
    with Pool(2) as pool:
        for k, r in pool.imap(job, jobs):
            out[k].append(r); json.dump(out, open('c142b_audit.json', 'w'))
            print(k, {kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in r.items() if kk != 'Qlien'}, f'({time.time()-t0:.0f} s)', flush=True)
    print('TERMINE')
