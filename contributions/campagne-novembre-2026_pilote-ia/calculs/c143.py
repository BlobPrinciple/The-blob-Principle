# C-143 / PR-1 — MITOSE CONTRARIEE, CHALEUR RETENUE OU EVACUEE, DISSOCIATION DES LIANTS. Protocole FIGE par ChatGPT (12 nov. 2026, fil principal,
#   sha256 8f5964854d3b4f007e840614f878c2e68aa7f5d5d68f3b71dce2c82918b954ab, recalculée par Claude sur le texte collé), exécuté par Claude.
# Modèle : tétraèdre régulier, 4 masses 1, r0 = 1 ; liens U(r) = (k/2)(r - r0)^2, k = 2, cohésion D = 1 ; amortisseur gamma sur la vitesse radiale relative,
#   chaleur du lien qdot = gamma ((v_j - v_i).n)^2. Bras R : le lien se dissout si r >= r0 et U + Q_loc >= D (la chaleur paie D - U) ; bras E (chaleur évacuée)
#   et I (chaleur retenue, inerte) : si r >= r0 et U >= D. Liens franchissant ensemble le critère : rompus ensemble. E_frag reçoit D par lien.
#   Source : impulsions internes centrées sur le porteur 0 (comme C-142B), travail exact W = P * (dt/T0), aux instants j*dt ; T0 = 2 pi / sqrt 2 ; fenêtre 24 T0 ;
#   cadences dt/T0 = 1/2, 4/5, 1, 6/5 (48, 30, 24, 20 impulsions) ; P = 0, 1/4, 1/2, 1 ; gamma = 0, 0,04, 0,12 ; trois bras : 144 scénarios.
#   Après le premier événement : plus d'impulsion, plus de rupture ; relaxation jusqu'à 24 T0 pour contrôler le bilan.
#   Solveurs : RK4 aux pas T0/512, T0/1024, T0/2048, et DOP853 (rtol 1e-11, atol 1e-12) ; désaccord ou résidu relatif > 1e-6 : INDETERMINE.
# PRECISIONS D'EXECUTION (Claude, déclarées avant calcul) :
#  - RK4 : chaque intervalle entre impulsions est découpé en pas égaux, le plus petit nombre tel que le pas ne dépasse pas la cible (les cadences 4/5 et 6/5
#    ne tombent pas sur la grille T0/512) ;
#  - événement RK4 : premier pas où le critère devient vrai, puis dichotomie (50 itérations) sur la fraction de pas ; DOP853 : fonction d'événement
#    max_e min(U_e + Q_e - D, r_e - r0) (R) ou max_e min(U_e - D, r_e - r0) (E, I), racine montante ;
#  - groupe simultané : tous les liens intacts dont le critère est satisfait à 1e-7 près à l'instant de l'événement ;
#  - résidu relatif rapporté à l'énergie programmée 24 P (résidu absolu si P = 0) ; scénarios P = 0 : pas de base et DOP853 seulement (rien ne bouge).
import numpy as np, itertools, math, json, sys, time
from scipy.integrate import solve_ivp
EDGE = np.array(list(itertools.combinations(range(4), 2))); I, J = EDGE[:, 0], EDGE[:, 1]
M = np.zeros((4, 6))
for z, (i, j) in enumerate(EDGE): M[i, z] = 1.0; M[j, z] = -1.0
P0 = np.array([[0, 0, 0], [1, 0, 0], [.5, math.sqrt(3) / 2, 0], [.5, math.sqrt(3) / 6, math.sqrt(2 / 3)]], float)
T0 = 2 * math.pi / math.sqrt(2); KS = 2.0; D = 1.0; R0 = 1.0; TOL = 1e-7
CAD = {'1/2': 0.5, '4/5': 0.8, '1': 1.0, '6/5': 1.2}; NIMP = {'1/2': 48, '4/5': 30, '1': 24, '6/5': 20}

def rates(x, v, act, gamma):
    d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); s = ((v[J] - v[I]) * d).sum(1) / r
    f = np.where(act, KS * (r - R0) + gamma * s, 0.0)
    return M @ (d * (f / r)[:, None]), np.where(act, gamma * s * s, 0.0)

def rk4(x, v, q, act, gamma, h):
    a1, q1 = rates(x, v, act, gamma); v2 = v + .5 * h * a1
    a2, q2 = rates(x + .5 * h * v, v2, act, gamma); v3 = v + .5 * h * a2
    a3, q3 = rates(x + .5 * h * v2, v3, act, gamma); v4 = v + h * a3
    a4, q4 = rates(x + h * v3, v4, act, gamma)
    return x + h / 6 * (v + 2 * v2 + 2 * v3 + v4), v + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4), q + h / 6 * (q1 + 2 * q2 + 2 * q3 + q4)

def impulse(x, v, act, W):
    g = np.zeros((4, 3))
    for z in range(6):
        if act[z] and (I[z] == 0 or J[z] == 0):
            o = J[z] if I[z] == 0 else I[z]; u = x[o] - x[0]; u = u / np.linalg.norm(u); g[o] += u; g[0] -= u
    aa = (v * g).sum(); bb = (g * g).sum(); al = (-aa + math.sqrt(aa * aa + 2 * bb * W)) / bb; vn = v + al * g
    return vn, .5 * ((vn * vn).sum() - (v * v).sum())

def crit(x, q, act, arm, tol=0.0):
    d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); U = .5 * KS * (r - R0) ** 2; g = U + (q if arm == 'R' else 0.0) - D
    return act & (r >= R0 - tol) & (g >= -tol), r, U

def break_links(grp, r, U, q, arm, led):
    for z in grp:
        if arm == 'R': led['frag'] += D; led['conv'] += D - U[z]          # la chaleur locale paie D - U
        else: led['frag'] += U[z]                                           # U = D au franchissement

def energy(x, v, q, act, led):
    d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); U = np.where(act, .5 * KS * (r - R0) ** 2, 0.0)
    return led['src'] + .5 * float((v * v).sum()) + float(U.sum()) + float(q.sum()) - led['conv'] + led['frag']

def run_rk4(arm, gamma, P, cad, sub=1, sabotage=False):
    dti = CAD[cad] * T0; N = NIMP[cad]; W = P * CAD[cad]; nseg = math.ceil(dti / (T0 / (512 * sub)) - 1e-9); h = dti / nseg
    x = P0.copy(); v = np.zeros((4, 3)); q = np.zeros(6); act = np.ones(6, bool); led = dict(src=24 * P, frag=0.0, conv=0.0); E0 = 24 * P
    ev = None; nimp = 0; deliv = 0.0; res = 0.0; t = 0.0; qmono = True
    for j in range(N):
        if ev is None and P > 0:
            v, w = impulse(x, v, act, W); led['src'] -= w; deliv += w; nimp += 1
        for st in range(nseg):
            xn, vn, qn = rk4(x, v, q, act, gamma, h)
            if (qn < q - 1e-15).any(): qmono = False
            if ev is None:
                pr, r, U = crit(xn, qn, act, arm)
                if pr.any():
                    lo, hi = 0.0, h
                    for _ in range(50):
                        mid = .5 * (lo + hi); xm, vm, qm = rk4(x, v, q, act, gamma, mid)
                        if crit(xm, qm, act, arm)[0].any(): hi = mid
                        else: lo = mid
                    xe, ve, qe = rk4(x, v, q, act, gamma, hi); pr, r, U = crit(xe, qe, act, arm, TOL); grp = [int(z) for z in np.where(pr)[0]]
                    eb = energy(xe, ve, qe, act, led)
                    if not sabotage: break_links(grp, r, U, qe, arm, led)
                    act[grp] = False; ea = energy(xe, ve, qe, act, led)
                    ev = dict(t=t + hi, liens=[tuple(int(k) for k in EDGE[z]) for z in grp], r=[float(k) for k in r], U=[float(k) for k in U], Q=[float(k) for k in qe],
                              saut_bilan=ea - eb, impulsions=nimp, energie_fournie=deliv)
                    xn, vn, qn = rk4(xe, ve, qe, act, gamma, h - hi)
            x, v, q = xn, vn, qn; t += h
        res = max(res, abs(energy(x, v, q, act, led) - E0))
    d = x[J] - x[I]; r = np.sqrt((d * d).sum(1))
    return dict(rupture=ev is not None, ev=ev, impulsions=nimp, energie_fournie=deliv, source_restante=led['src'], Q=[float(k) for k in q], Qtot=float(q.sum()),
                Efrag=led['frag'], chaleur_convertie=led['conv'], Ecin=.5 * float((v * v).sum()), residu=res / (E0 if E0 > 0 else 1.0), q_monotone=qmono,
                sym=float(np.ptp(r[:3])) if ev is None else float(np.ptp(np.array(ev['r'])[:3])))

def run_dop(arm, gamma, P, cad):
    dti = CAD[cad] * T0; N = NIMP[cad]; W = P * CAD[cad]; act = np.ones(6, bool); led = dict(src=24 * P, frag=0.0, conv=0.0); E0 = 24 * P
    y = np.concatenate([P0.ravel(), np.zeros(12), np.zeros(6)]); ev = None; nimp = 0; deliv = 0.0; res = 0.0
    def rhs(t, y):
        a, qd = rates(y[:12].reshape(4, 3), y[12:24].reshape(4, 3), act, gamma); return np.concatenate([y[12:24], a.ravel(), qd])
    def evf(t, y):
        x = y[:12].reshape(4, 3); d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); g = .5 * KS * (r - R0) ** 2 + (y[24:] if arm == 'R' else 0.0) - D
        return float(np.where(act, np.minimum(g, r - R0), -1.0).max())
    evf.terminal = True; evf.direction = 1
    for j in range(N):
        t0, t1 = j * dti, (j + 1) * dti
        if ev is None and P > 0:
            vn, w = impulse(y[:12].reshape(4, 3), y[12:24].reshape(4, 3), act, W); y[12:24] = vn.ravel(); led['src'] -= w; deliv += w; nimp += 1
        if ev is None:
            sol = solve_ivp(rhs, (t0, t1), y, method='DOP853', rtol=1e-11, atol=1e-12, events=evf); y = sol.y[:, -1].copy()
            if sol.status == 1:
                te = float(sol.t[-1]); x = y[:12].reshape(4, 3); pr, r, U = crit(x, y[24:], act, arm, TOL); grp = [int(z) for z in np.where(pr)[0]]
                break_links(grp, r, U, y[24:], arm, led); act[grp] = False
                ev = dict(t=te, liens=[tuple(int(k) for k in EDGE[z]) for z in grp], r=[float(k) for k in r], U=[float(k) for k in U], Q=[float(k) for k in y[24:]],
                          impulsions=nimp, energie_fournie=deliv)
                if te < t1: sol = solve_ivp(rhs, (te, t1), y, method='DOP853', rtol=1e-11, atol=1e-12); y = sol.y[:, -1].copy()
        else:
            sol = solve_ivp(rhs, (t0, t1), y, method='DOP853', rtol=1e-11, atol=1e-12); y = sol.y[:, -1].copy()
        res = max(res, abs(energy(y[:12].reshape(4, 3), y[12:24].reshape(4, 3), y[24:], act, led) - E0))
    return dict(rupture=ev is not None, ev=ev, impulsions=nimp, energie_fournie=deliv, Qtot=float(y[24:].sum()), Q=[float(k) for k in y[24:]], Efrag=led['frag'],
                residu=res / (E0 if E0 > 0 else 1.0))

def scenario(a):
    arm, gamma, P, cad = a; t0 = time.time(); out = dict(bras=arm, gamma=gamma, P=P, cadence=cad)
    out['rk1'] = run_rk4(arm, gamma, P, cad, 1); out['dop'] = run_dop(arm, gamma, P, cad)
    if P > 0: out['rk2'] = run_rk4(arm, gamma, P, cad, 2); out['rk4'] = run_rk4(arm, gamma, P, cad, 4)
    sol = [out[k] for k in ('rk1', 'rk2', 'rk4', 'dop') if k in out]
    same = len(set(s['rupture'] for s in sol)) == 1 and len(set(tuple(sorted(tuple(l) for l in s['ev']['liens'])) if s['ev'] else () for s in sol)) == 1
    resmax = max(s['residu'] for s in sol)
    out['verdict'] = 'INDETERMINE' if (not same or resmax > 1e-6) else ('RUPTURE' if sol[0]['rupture'] else 'INTACT')
    out['accord_solveurs'] = same; out['residu_max'] = resmax; out['temps'] = [s['ev']['t'] if s['ev'] else None for s in sol]; out['duree_calcul'] = round(time.time() - t0, 1)
    return out

if __name__ == '__main__':
    from multiprocessing import Pool
    jobs = [(arm, g, P, c) for g in (0.0, 0.04, 0.12) for P in (0.0, 0.25, 0.5, 1.0) for c in ('1/2', '4/5', '1', '6/5') for arm in ('R', 'E', 'I')]
    res = []; t0 = time.time()
    with Pool(2) as pool:
        for o in pool.imap(scenario, jobs):
            res.append(o); json.dump(res, open('c143.json', 'w'))
            e = o['rk4']['ev'] if 'rk4' in o and o['rk4']['ev'] else (o['rk1']['ev'] if o['rk1']['ev'] else None)
            print(f"gamma={o['gamma']:<5} P={o['P']:<5} cad={o['cadence']:<4} bras={o['bras']} -> {o['verdict']:<11} t/T0={[round(x/T0,4) if x is not None else None for x in o['temps']]} "
                  f"liens={e['liens'] if e else None} imp={e['impulsions'] if e else o['rk1']['impulsions']} résidu={o['residu_max']:.1e} ({time.time()-t0:.0f} s)", flush=True)
    print('TERMINE', len(res))
