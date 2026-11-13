# C-145 / PR-3 — NAISSANCE NON CHEVAUCHANTE, RESISTANCE DU LIANT ET DISSIPATION, PUIS TISSU REDONDANT
# Protocole FIGE par ChatGPT (13 nov. 2026, nouvelle conversation) ; sha256 b58619d250c9fb5349a2a6053585720a6db70b2aac771fa504b00adea70125a3, 15 188 octets,
# recalculée par Claude sur le contenu brut du fichier. Notes de lecture : c145pr3_spec.txt. Prédiction enregistrée avant tout calcul : c145pr3_prediction.txt (4 h 25 UTC).
# Code général à n porteurs (4 ou 5) : liens cohésifs U_D, frein radial gamma_D = gamma0 sqrt(D) sur les liens, cœur dur élastique à r = a sur TOUTES les paires,
# chocs de travail exact sur le K4 primaire, arrêts A1 / A2 lus sur les six arêtes primaires, T0(D) = 2 pi / sqrt(2D).
# PRECISIONS D'EXECUTION (Claude, déclarées avant calcul ; voir c145pr3_declaration.txt) : mêmes conventions que PR-2 (contact à 1e-9 ; ambigu => INDETERMINE ;
# accord des solveurs sur sortie, groupe à 1e-5 T0, P_first, P_any, rebond ; lectures stricte et de référence). a = 1 : BLOQUE (voir déclaration).
# Tissu : x4 = image de x3 (perturbé) par le plan z = 0 ; chevauchement des deux tétraèdres = volumes orientés (0,1,2,3) et (0,1,2,4) de même signe.
import numpy as np, math, json, sys, time, itertools
from numba import njit
from scipy.integrate import DOP853
from scipy.optimize import brentq
P0 = np.array([[0, 0, 0], [1, 0, 0], [.5, math.sqrt(3) / 2, 0], [.5, math.sqrt(3) / 6, math.sqrt(2 / 3)]], float)
R0 = 1.0; LL = math.sqrt(3.0); RC = R0 + LL; TOL = 1e-10; TSIM = 1e-5
PRIM = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
TOPO = {'K4': (4, PRIM), 'T5': (5, PRIM + [(0, 4), (1, 4), (2, 4)])}
def arrays(top):
    n, links = TOPO[top]; pairs = list(itertools.combinations(range(n), 2))
    return n, np.array([a for a, b in links]), np.array([b for a, b in links]), np.array([a for a, b in pairs]), np.array([b for a, b in pairs]), links, pairs
class Ambigu(Exception): pass

@njit(cache=True)
def potD(r, D):
    if r < R0: return D * (r - R0) ** 2, 2 * D * (r - R0)
    if r < RC:
        u = (r - R0) / LL; return D * (3 * u * u - 2 * u * u * u), D * (6 * u - 6 * u * u) / LL
    return D, 0.0

@njit(cache=True)
def rhs3(s, out, n, BI, BJ, D, gam):
    m = 3 * n; qd = 0.0
    for k in range(m): out[k] = s[m + k]; out[m + k] = 0.0
    for z in range(BI.shape[0]):
        i = BI[z]; j = BJ[z]; dx = s[3 * j] - s[3 * i]; dy = s[3 * j + 1] - s[3 * i + 1]; dz = s[3 * j + 2] - s[3 * i + 2]
        r = math.sqrt(dx * dx + dy * dy + dz * dz); U, f = potD(r, D)
        if gam != 0.0:
            rd = ((s[m + 3 * j] - s[m + 3 * i]) * dx + (s[m + 3 * j + 1] - s[m + 3 * i + 1]) * dy + (s[m + 3 * j + 2] - s[m + 3 * i + 2]) * dz) / r
            f += gam * rd; qd += gam * rd * rd
        f /= r
        out[m + 3 * i] += f * dx; out[m + 3 * i + 1] += f * dy; out[m + 3 * i + 2] += f * dz
        out[m + 3 * j] -= f * dx; out[m + 3 * j + 1] -= f * dy; out[m + 3 * j + 2] -= f * dz
    out[2 * m] = qd

@njit(cache=True)
def lensg(s, I, J, r):
    for z in range(I.shape[0]):
        i = I[z]; j = J[z]; dx = s[3 * j] - s[3 * i]; dy = s[3 * j + 1] - s[3 * i + 1]; dz = s[3 * j + 2] - s[3 * i + 2]; r[z] = math.sqrt(dx * dx + dy * dy + dz * dz)

@njit(cache=True)
def vols(s):
    """volumes orientés (0,1,2,3) et (0,1,2,4) ; les deux tétraèdres se chevauchent quand ils ont le même signe"""
    ax = s[3] - s[0]; ay = s[4] - s[1]; az = s[5] - s[2]; bx = s[6] - s[0]; by = s[7] - s[1]; bz = s[8] - s[2]
    nx = ay * bz - az * by; ny = az * bx - ax * bz; nz = ax * by - ay * bx
    return nx * (s[9] - s[0]) + ny * (s[10] - s[1]) + nz * (s[11] - s[2]), nx * (s[12] - s[0]) + ny * (s[13] - s[1]) + nz * (s[14] - s[2])

@njit(cache=True)
def rk4g(s, h, sn, k1, k2, k3, k4, tmp, n, BI, BJ, D, gam):
    N = s.shape[0]; rhs3(s, k1, n, BI, BJ, D, gam)
    for q in range(N): tmp[q] = s[q] + .5 * h * k1[q]
    rhs3(tmp, k2, n, BI, BJ, D, gam)
    for q in range(N): tmp[q] = s[q] + .5 * h * k2[q]
    rhs3(tmp, k3, n, BI, BJ, D, gam)
    for q in range(N): tmp[q] = s[q] + h * k3[q]
    rhs3(tmp, k4, n, BI, BJ, D, gam)
    for q in range(N): sn[q] = s[q] + h / 6 * (k1[q] + 2 * k2[q] + 2 * k3[q] + k4[q])

@njit(cache=True)
def rk_seg3(s, t, tm, hmax, side, ev, nev, rmin, ovl, acore, n, BI, BJ, PI, PJ, D, gam):
    """RK4 de t à tm, pas coupés à r0 et r_c (liens) et au cœur (toutes paires). Renvoie (instant, nev, code) : 0 = tm ; 1 = contact de cœur ; 9 = garde.
       ev : (instant, lien, sens) des passages de r_c ; ovl[0] : premier instant de chevauchement des deux tétraèdres (tissu), -1 sinon."""
    N = s.shape[0]; nb = BI.shape[0]; npair = PI.shape[0]; sn = np.empty(N); st = np.empty(N); k1 = np.empty(N); k2 = np.empty(N); k3 = np.empty(N); k4 = np.empty(N); tmp = np.empty(N)
    rp = np.empty(nb); rn = np.empty(nb); rt = np.empty(nb); pp = np.empty(npair); pn = np.empty(npair); pt = np.empty(npair)
    nst = int(math.ceil((tm - t) / hmax - 1e-9))
    if nst < 1: nst = 1
    h = (tm - t) / nst; lensg(s, BI, BJ, rp); lensg(s, PI, PJ, pp)
    for i in range(nst):
        tc = t + i * h; rem = h; guard = 0
        while rem > 1e-14 * h:
            guard += 1
            if guard > 400: return tc, nev, 9
            rk4g(s, rem, sn, k1, k2, k3, k4, tmp, n, BI, BJ, D, gam); lensg(sn, BI, BJ, rn); lensg(sn, PI, PJ, pn); best = 2.0; bz = -1; bk = -1
            for kk in range(3):
                nz_ = npair if kk == 2 else nb
                for z in range(nz_):
                    if kk == 2: b = pn[z] - acore; a = pp[z] - acore
                    else:
                        c = R0 if kk == 0 else RC; b = rn[z] - c; a = rp[z] - c
                    if abs(b) <= TOL: continue
                    sg = 1 if b > 0 else -1
                    if sg == side[kk, z]: continue
                    if a * b < 0.0:
                        lo = 0.0; hi = 1.0; flo = a; fhi = b; th = 0.5
                        for it in range(100):
                            th = lo - flo * (hi - lo) / (fhi - flo)
                            if it % 3 == 2 or th <= lo or th >= hi: th = .5 * (lo + hi)
                            rk4g(s, th * rem, st, k1, k2, k3, k4, tmp, n, BI, BJ, D, gam)
                            if kk == 2: lensg(st, PI, PJ, pt); f = pt[z] - acore
                            else: lensg(st, BI, BJ, rt); f = rt[z] - (R0 if kk == 0 else RC)
                            if abs(f) < 1e-14 or (hi - lo) < 1e-15: break
                            if f * flo < 0.0: hi = th; fhi = f
                            else: lo = th; flo = f
                        if th < best: best = th; bz = z; bk = kk
                    else:
                        if kk == 2: return tc, nev, 1
                        side[kk, z] = sg
                        if kk == 1 and nev < ev.shape[0]: ev[nev, 0] = tc; ev[nev, 1] = z; ev[nev, 2] = sg; nev += 1
            if bz >= 0 and best * rem < 1e-13:
                if bk == 2: return tc, nev, 1
                c = R0 if bk == 0 else RC; sg = 1 if rn[bz] - c > 0 else -1; side[bk, bz] = sg
                if bk == 1 and nev < ev.shape[0]: ev[nev, 0] = tc; ev[nev, 1] = bz; ev[nev, 2] = sg; nev += 1
                continue
            dt = rem if bz < 0 else best * rem
            if bz >= 0: rk4g(s, dt, sn, k1, k2, k3, k4, tmp, n, BI, BJ, D, gam); lensg(sn, BI, BJ, rn); lensg(sn, PI, PJ, pn)
            for q in range(N): s[q] = sn[q]
            for z in range(nb): rp[z] = rn[z]
            for z in range(npair):
                pp[z] = pn[z]
                if pn[z] < rmin[z]: rmin[z] = pn[z]
            tc += dt; rem -= dt
            if bz < 0: rem = 0.0
            if n == 5 and ovl[0] < 0:
                v3, v4 = vols(s)
                if v3 * v4 > 0: ovl[0] = tc
            if bz >= 0:
                if bk == 2: return tc, nev, 1
                sg = -side[bk, bz]; side[bk, bz] = sg
                if bk == 1 and nev < ev.shape[0]: ev[nev, 0] = tc; ev[nev, 1] = bz; ev[nev, 2] = sg; nev += 1
    return tm, nev, 0

def reflect3(s, acore, n, PI, PJ, facteur=2.0):
    m = 3 * n; x = s[:m].reshape(n, 3); v = s[m:2 * m].reshape(n, 3); d = x[PJ] - x[PI]; r = np.sqrt((d * d).sum(1)); nrm = d / r[:, None]; u = ((v[PJ] - v[PI]) * nrm).sum(1)
    near = [z for z in range(len(PI)) if r[z] <= acore + 1e-9]; con = [z for z in near if u[z] < 0]
    if not con: return [], False, 0.0
    A = np.zeros((len(con), m))
    for q, z in enumerate(con): A[q, 3 * PI[z]:3 * PI[z] + 3] = -nrm[z]; A[q, 3 * PJ[z]:3 * PJ[z] + 3] = nrm[z]
    vf = v.ravel().copy(); vn = vf - facteur * A.T @ (np.linalg.pinv(A @ A.T, rcond=1e-10) @ (A @ vf)); k0 = .5 * float(vf @ vf); s[m:2 * m] = vn
    v2 = vn.reshape(n, 3); u2 = ((v2[PJ] - v2[PI]) * nrm).sum(1); ok = all(u2[z] >= -1e-12 for z in near)
    return con, ok, .5 * float(vn @ vn) - k0

def a2_state(ev, tnow, T0D):
    out = {}; fin = None
    for te, z, sg in sorted(ev):
        if te > tnow: break
        if sg > 0: out[z] = te
        elif z in out:
            if te - out[z] >= T0D: fin = out[z] + T0D if fin is None else min(fin, out[z] + T0D)
            del out[z]
    for z, t0 in out.items():
        if tnow - t0 >= T0D: fin = t0 + T0D if fin is None else min(fin, t0 + T0D)
    return len(out) == 0, fin

class Ctx:
    def __init__(self, top, D, g0, a):
        self.n, self.BI, self.BJ, self.PI, self.PJ, self.links, self.pairs = arrays(top); self.D = D; self.gam = g0 * math.sqrt(D); self.a = a; self.T0 = 2 * math.pi / math.sqrt(2 * D)
        self.N = 6 * self.n + 1; self.par = (self.n, self.BI, self.BJ, D, self.gam)
    def fun(self, t, y):
        out = np.empty_like(y); rhs3(y, out, *self.par); return out
    def energies(self, s):
        n = self.n; m = 3 * n; x = s[:m].reshape(n, 3); v = s[m:2 * m].reshape(n, 3); d = x[self.BJ] - x[self.BI]; r = np.sqrt((d * d).sum(1)); u = (r - R0) / LL
        U = self.D * np.where(r < R0, (r - R0) ** 2, np.where(r < RC, 3 * u * u - 2 * u ** 3, 1.0)); xc = x - x.mean(0)
        return dict(cin=.5 * float((v * v).sum()), coh=float(U.sum()), ext=float(s[-1]), r=[float(k) for k in r], qmv=float(np.abs(v.sum(0)).max()), mcin=float(np.abs(np.cross(xc, v).sum(0)).max()),
                    FU=(float(U.max() / U.sum()) if U.sum() > 1e-20 * self.D else 0.0))

def kick3(s, W, n, v=None, edge=None):
    m = 3 * n; x = s[:m].reshape(n, 3); vel = s[m:2 * m].reshape(n, 3); g = np.zeros((n, 3))
    if edge is None:
        for j in range(4):
            if j != v: u = x[j] - x[v]; u = u / np.linalg.norm(u); g[j] += u; g[v] -= u
    else:
        a, b = edge; u = x[b] - x[a]; u = u / np.linalg.norm(u); g[a] = -u; g[b] = u
    A = float((vel * g).sum()); B = float((g * g).sum()); lam = (-A + math.sqrt(A * A + 2 * B * W)) / B; vn = vel + lam * g
    w = .5 * float((vn * vn).sum() - (vel * vel).sum()); s[m:2 * m] = vn.ravel(); return w

def dop_seg3(cx, s, t, tm, side, ev, st, colls, rtol=1e-11, atol=1e-12, facteur=2.0):
    """st : dict d'état de mesure (rmin, ovl, grille de F_U)"""
    nb = len(cx.BI); npair = len(cx.PI); r = np.empty(nb); p = np.empty(npair); nloop = 0; hmaxi = cx.T0 / 32
    def val(y, kk, z):
        if kk == 2: lensg(y, cx.PI, cx.PJ, p); return p[z] - cx.a
        lensg(y, cx.BI, cx.BJ, r); return r[z] - (R0 if kk == 0 else RC)
    def sample(ta, tb, dense):
        dt = cx.T0 / 32
        while st['k'] * dt <= tb + 1e-12:
            tg = st['k'] * dt; y = dense(min(max(tg, ta), tb)); lensg(y, cx.BI, cx.BJ, r); u = (r - R0) / LL
            U = np.where(r < R0, (r - R0) ** 2, np.where(r < RC, 3 * u * u - 2 * u ** 3, 1.0)); su = float(U.sum()); f = float(U.max()) / su if su > 1e-20 else 0.0
            if st['fprev'] is not None: st['IFU'] += .5 * dt * (f + st['fprev'])
            st['fprev'] = f; st['k'] += 1
    while tm - t > 1e-13:
        nloop += 1
        if nloop > 100000: raise Ambigu('boucle')
        sol = DOP853(cx.fun, t, s, tm, rtol=rtol, atol=atol, max_step=hmaxi); cut = False
        while sol.status == 'running':
            sol.step()
            if sol.status == 'failed': raise Ambigu('DOP853 en échec')
            ta = sol.t_old; tb = sol.t; dense = sol.dense_output(); tprev = ta
            for th in (1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6, 1.0):
                tq = tb if th == 1.0 else ta + th * (tb - ta); yq = sol.y if th == 1.0 else dense(tq); lensg(yq, cx.BI, cx.BJ, r); lensg(yq, cx.PI, cx.PJ, p); cand = []; pq = p.copy()
                for kk in range(3):
                    arr = p - cx.a if kk == 2 else r - (R0 if kk == 0 else RC)
                    for z in range(len(arr)):
                        b = arr[z]
                        if abs(b) > TOL and (1 if b > 0 else -1) != side[kk, z]: cand.append((kk, z, float(b)))
                if cand:
                    roots = []
                    for kk, z, b in cand:
                        f = (lambda tt, kk=kk, z=z: val(dense(tt), kk, z)); fa = f(tprev)
                        roots.append((brentq(f, tprev, tq, xtol=1e-15, rtol=8.9e-16) if fa * b < 0 else tprev, kk, z, b))
                    te0 = min(q[0] for q in roots); coll = False
                    for te, kk, z, b in roots:
                        if te <= te0 + 1e-12:
                            if kk == 2: coll = True; continue
                            sg = 1 if b > 0 else -1; side[kk, z] = sg
                            if kk == 1: ev.append((float(te), z, sg))
                    sample(ta, te0, dense)
                    if te0 - ta > 1e-12:
                        s2 = DOP853(cx.fun, ta, sol.y_old, te0, rtol=rtol, atol=atol, first_step=te0 - ta)
                        while s2.status == 'running': s2.step()
                        if s2.status == 'failed': raise Ambigu('DOP853 en échec (reprise)')
                        s = s2.y.copy()
                    else: s = sol.y_old.copy()
                    t = te0; cut = True; lensg(s, cx.PI, cx.PJ, p); np.minimum(st['rmin'], p, out=st['rmin'])
                    if coll:
                        con, ok, dk = reflect3(s, cx.a, cx.n, cx.PI, cx.PJ, facteur); colls.append((float(t), con, dk))
                        if not con: raise Ambigu('contact sans vitesse entrante')
                        if not ok: raise Ambigu('collision ambiguë')
                        if len(colls) > 6000: raise Ambigu('cascade')
                    break
                np.minimum(st['rmin'], pq, out=st['rmin'])
                if cx.n == 5 and st['ovl'] < 0:
                    v3, v4 = vols(yq)
                    if v3 * v4 > 0: st['ovl'] = float(tq)
                tprev = tq
            if cut: break
            sample(ta, tb, dense)
        if not cut: s = sol.y.copy(); t = tm
    return s

def rk_adv3(cx, s, t, tm, sub, side, ev, st, colls, facteur=2.0):
    evb = np.zeros((2048, 3)); ov = np.array([st['ovl']])
    while tm - t > 1e-13:
        tr, nev, code = rk_seg3(s, t, tm, cx.T0 / (1024 * sub), side, evb, 0, st['rmin'], ov, cx.a, cx.n, cx.BI, cx.BJ, cx.PI, cx.PJ, cx.D, cx.gam)
        for q in range(nev): ev.append((float(evb[q, 0]), int(evb[q, 1]), int(evb[q, 2])))
        t = tr; st['ovl'] = float(ov[0])
        if code == 9: raise Ambigu('garde')
        if code == 1:
            con, ok, dk = reflect3(s, cx.a, cx.n, cx.PI, cx.PJ, facteur); colls.append((float(t), con, dk))
            if not con: raise Ambigu('contact sans vitesse entrante')
            if not ok: raise Ambigu('collision ambiguë')
            if len(colls) > 6000: raise Ambigu('cascade')
    return s

def delta(j):
    d = np.array([[math.sin(2 * math.pi * j * (3 * i + k + 1) / 17) for k in range(3)] for i in range(4)]); d -= d.mean(0); return d / np.linalg.norm(d)
def geometrie(top, g):
    x = P0.copy() if g == 0 else P0 + (1 if g % 2 == 1 else -1) * 1e-8 * delta((g + 1) // 2)
    if top == 'T5': x = np.vstack([x, [x[3, 0], x[3, 1], -x[3, 2]]])
    return x

def connexe(n, links, dehors):
    adj = {i: set() for i in range(n)}
    for z, (a, b) in enumerate(links):
        if z not in dehors: adj[a].add(b); adj[b].add(a)
    seen = {0}; pile = [0]
    while pile:
        q = pile.pop()
        for w in adj[q]:
            if w not in seen: seen.add(w); pile.append(w)
    return len(seen) == n

def run3(top, src, P, cad, stop, a, D, g0, g, solver='dop', sub=1, sabotage=False, facteur=2.0, x0=None, v0=None, tend=28, rtol=1e-11, atol=1e-12):
    if a >= 1.0: return dict(bloque='a = 1 : contact initial et contacts permanents non traités (voir déclaration)')
    cx = Ctx(top, D, g0, a); n = cx.n; m = 3 * n; c = {'1/2': 0.5, '1': 1.0}[cad]; N = int(round(24 / c)); W = P * c; T0 = cx.T0
    s = np.zeros(cx.N); s[:m] = (geometrie(top, g) if x0 is None else np.array(x0, float)).ravel()
    if v0 is not None: s[m:2 * m] = np.array(v0, float).ravel()
    E0 = 24 * P + .5 * float((s[m:2 * m] ** 2).sum()); res = 24 * P; trav = 0.0; nk = 0; nsaut = 0
    raw = sorted([(j * c * T0, 'k', j) for j in range(N) if j * c < tend] + [(float(k) * T0, 'c', k) for k in (24, 28) if k <= tend] + ([(float(tend) * T0, 'c', tend)] if tend not in (24, 28) else []))
    marks = []; flags = []
    for tm_, f_, j_ in raw:
        if marks and abs(tm_ - marks[-1]) < 1e-9: flags[-1][f_] = j_
        else: marks.append(tm_); flags.append({f_: j_})
    nb = len(cx.BI); npair = len(cx.PI); r = np.empty(nb); p = np.empty(npair); lensg(s, cx.BI, cx.BJ, r); lensg(s, cx.PI, cx.PJ, p)
    side = np.ones((3, 10), np.int64); side[0, :nb] = np.where(r >= R0, 1, -1); side[1, :nb] = np.where(r >= RC, 1, -1)
    ev = []; colls = []; st = dict(rmin=p.copy(), ovl=-1.0, k=0, fprev=None, IFU=0.0); pts = {}; resid = 0.0; qm = 0.0; lm = 0.0; t = 0.0; amb = None; parchoc = []
    def tot(s): e = cx.energies(s); return res + e['cin'] + e['coh'] + (0.0 if sabotage else e['ext']), e
    prim = lambda: [q for q in ev if q[1] < 6]
    try:
        for k, tm in enumerate(marks):
            if tm > t + 1e-12:
                if solver == 'dop': s = dop_seg3(cx, s, t, tm, side, ev, st, colls, rtol, atol, facteur)
                else: s = rk_adv3(cx, s, t, tm, sub, side, ev, st, colls, facteur)
                t = tm
            e_, en = tot(s); resid = max(resid, abs(e_ - E0)); qm = max(qm, en['qmv']); lm = max(lm, en['mcin'])
            if 'c' in flags[k]: en['source'] = res; en['travail'] = trav; pts[int(flags[k]['c'])] = en
            if 'k' in flags[k] and P > 0:
                pe = prim()
                if stop == 'A1': go = not any(q[2] > 0 for q in pe)
                else: lie, fin = a2_state(pe, tm, T0); go = lie and fin is None
                if go:
                    j = flags[k]['k']
                    if solver == 'dop' and not any(q[2] > 0 for q in pe): parchoc.append((tm / T0, trav, st['IFU']))
                    w = kick3(s, W, n, edge=(0, 1)) if src == 'F' else kick3(s, W, n, v=(0 if src == 'S' else j % 4))
                    res -= w; trav += w; nk += 1; e_, en = tot(s); resid = max(resid, abs(e_ - E0)); qm = max(qm, en['qmv']); lm = max(lm, en['mcin'])
                else: nsaut += 1
    except Ambigu as ex: amb = str(ex)
    out_t = [[q[0] for q in ev if q[1] == z and q[2] > 0] for z in range(nb)]; in_t = [[q[0] for q in ev if q[1] == z and q[2] < 0] for z in range(nb)]
    lensg(s, cx.BI, cx.BJ, r); tf = 24 * T0; te_ = 28 * T0; first = [min(o) if o else None for o in out_t[:6]]; t1 = min([q for q in first if q is not None], default=None)
    grp = sorted(z for z in range(6) if first[z] is not None and first[z] <= t1 + TSIM * T0) if t1 is not None else []
    persall = [z for z in range(nb) if r[z] >= RC and out_t[z] and not any(q >= tf for q in in_t[z]) and not any(q > tf for q in out_t[z])] if amb is None else []
    pers = [z for z in persall if z < 6]; _, fin = a2_state(prim(), te_, T0)
    # tissu : connexité du graphe des liens à portée, à tout instant et sur la fenêtre ; porteur de degré zéro pendant toute la fenêtre
    dehors = set(); cx_tjrs = True; cx_fen = True
    for te, z, sg in sorted(ev):
        if sg > 0: dehors.add(z)
        else: dehors.discard(z)
        if not connexe(n, cx.links, dehors):
            cx_tjrs = False
            if te >= tf: cx_fen = False
    dehors_tf = set()
    for te, z, sg in sorted(ev):
        if te > tf: break
        if sg > 0: dehors_tf.add(z)
        else: dehors_tf.discard(z)
    if not connexe(n, cx.links, dehors_tf): cx_fen = False
    deg0 = [v for v in range(n) if all((z in persall) for z, (a_, b_) in enumerate(cx.links) if v in (a_, b_))]
    o = dict(statut=('LIE' if t1 is None else ('PANY' if pers else 'RECAPT')), t1=(t1 / T0 if t1 is not None else None), groupe=[list(cx.links[z]) for z in grp], liens=[list(cx.links[z]) for z in pers],
             liens_tous=[list(cx.links[z]) for z in persall], Pany=bool(pers), Pfirst=bool(set(pers) & set(grp)), chocs=nk, sautes=nsaut, travail=trav, reserve=res,
             ncol=len(colls), col1=(None if not colls else [colls[0][0] / T0, [list(cx.pairs[z]) for z in colls[0][1]]]), nsimul=sum(len(q[1]) > 1 for q in colls),
             dkcol=max([abs(q[2]) for q in colls], default=0.0), ambigu=amb, rmin=float(st['rmin'].min()), tstop=(fin / T0 if fin is not None else None), ovl=(st['ovl'] / T0 if st['ovl'] >= 0 else None),
             connexe_toujours=cx_tjrs, connexe_fenetre=cx_fen, deg0=deg0, nexc=sum(len(q) for q in in_t), residu_abs=resid, residu_rel=resid / (E0 if E0 > 0 else 1.0), qmv=qm, mcin=lm,
             chaleur=float(s[-1]), r_fin=[float(q) for q in r])
    if solver == 'dop': o['parchoc'] = parchoc; o['points'] = {k: dict(cin=v['cin'], coh=v['coh'], ext=v['ext'], travail=v['travail']) for k, v in pts.items()}
    return o

def key3(d): return (d['t1'] is not None, tuple(tuple(q) for q in d['groupe']), d['Pfirst'], d['Pany'], d['ncol'] > 0, None if d['col1'] is None else tuple(tuple(q) for q in d['col1'][1]), d['ambigu'] is None, d['connexe_fenetre'])

def traj3(job):
    t0 = time.time(); o = dict(job); kw = dict(top=job['top'], src=job['src'], P=job['P'], cad=job['cad'], stop=job['stop'], a=job['a'], D=job['D'], g0=job['g0'], g=job['g'])
    o['dop'] = run3(solver='dop', **kw)
    if 'bloque' in o['dop']: o['verdict'] = o['verdict_ref'] = 'BLOQUE'; o['duree'] = 0.0; return o
    o['rk1'] = run3(solver='rk', sub=1, **kw); o['rk2'] = run3(solver='rk', sub=2, **kw); sol = [o['dop'], o['rk1'], o['rk2']]
    o['accord'] = len(set(key3(q) for q in sol)) == 1 and all(q['ambigu'] is None for q in sol)
    o['bilan_ok'] = all(q['residu_abs'] <= 1e-6 and q['residu_rel'] <= 1e-6 for q in sol); o['bilan_dop'] = o['dop']['residu_abs'] <= 1e-6 and o['dop']['residu_rel'] <= 1e-6
    o['verdict'] = o['dop']['statut'] if (o['accord'] and o['bilan_ok']) else 'INDETERMINE'; o['verdict_ref'] = o['dop']['statut'] if (o['accord'] and o['bilan_dop']) else 'INDETERMINE'
    o['duree'] = round(time.time() - t0, 2); return o

def jobs():
    J = []
    for P in (1 / 128, 1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1.0):
        for D in (0.5, 1.0, 2.0):
            for g0 in (0.0, 0.04):
                for c in ('1/2', '1'):
                    for src in 'SCF':
                        for g in range(9): J.append(dict(camp='A', top='K4', src=src, P=P, cad=c, stop='A2', a=0.5, D=D, g0=g0, g=g))
    for a in (0.25, 0.5, 0.75, 1.0):
        for P in (1 / 4, 1 / 2):
            for c in ('1/2', '1'):
                for src in 'SC':
                    for stop in ('A1', 'A2'):
                        for g in range(9): J.append(dict(camp='B', top='K4', src=src, P=P, cad=c, stop=stop, a=a, D=1.0, g0=0.0, g=g))
    for top in ('K4', 'T5'):
        for P in (1 / 4, 1 / 2):
            for c in ('1/2', '1'):
                for src in 'SC':
                    for stop in ('A1', 'A2'):
                        for g in range(9): J.append(dict(camp='C', top=top, src=src, P=P, cad=c, stop=stop, a=0.75, D=1.0, g0=0.0, g=g))
    return J

if __name__ == '__main__':
    from multiprocessing import Pool
    run3('T5', 'C', 0.3, '1', 'A2', 0.75, 1.0, 0.0, 1, solver='rk', tend=2); run3('K4', 'S', 0.3, '1', 'A2', 0.5, 2.0, 0.04, 0, solver='rk', tend=2)
    J = jobs(); res = []; t0 = time.time(); print(len(J), 'trajectoires :', {k: sum(j['camp'] == k for j in J) for k in 'ABC'}, flush=True)
    with Pool(2) as pool:
        for o in pool.imap(traj3, J, chunksize=4):
            res.append(o); d = o['dop']
            if len(res) % 300 == 0: json.dump(res, open('c145c.json', 'w'))
            if 'bloque' in d: print(f"{o['camp']} a={o['a']} BLOQUE", flush=True); continue
            print(f"{o['camp']} {o['top']} P={o['P']:<8.5f} D={o['D']} g0={o['g0']} c={o['cad']:<3} {o['src']} {o['stop']} a={o['a']} g={o['g']} dop={d['statut']:<6} t1={None if d['t1'] is None else round(d['t1'], 3)} gr={d['groupe']} "
                  f"chocs={d['chocs']}/{d['sautes']} W={d['travail']:.2f} liens={d['liens']} col={d['ncol']} amb={d['ambigu']} cx={d['connexe_fenetre']} ovl={d['ovl'] and round(d['ovl'], 2)} rk={o['rk1']['statut']},{o['rk2']['statut']} "
                  f"accord={o['accord']} résidu={max(d['residu_abs'], o['rk1']['residu_abs'], o['rk2']['residu_abs']):.0e} -> {o['verdict']}/{o['verdict_ref']} ({time.time() - t0:.0f} s)", flush=True)
    json.dump(res, open('c145c.json', 'w')); print('TERMINE', len(res))
