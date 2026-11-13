# C-145 / PR-1 — MITOSE CONTRARIEE, FOCALISATION MECANIQUE DES ARETES, DISSOCIATION SANS REGLE D'USURE
# Protocole FIGE par ChatGPT (12 nov. 2026, fil principal) ; sha256 9b1cd06bd67002df30ffbf1a01abebe30c4e3c812524e9f957c37f167cb14148, 11 368 octets,
# recalculée par Claude sur le texte du fichier. Prédiction de Claude enregistrée avant tout calcul : c145_prediction.txt (22 h 30 UTC).
# Modèle (inchangé depuis C-144) : tétraèdre régulier, 4 masses 1, r0 = 1, D = 1, k = 2, L = sqrt 3, r_c = 1 + L, u = (r - r0)/L.
#   U_c : k (r-r0)^2/2 (r < r0) ; D (3u^2 - 2u^3) (r0 <= r < r_c) ; D (r >= r_c).   h : r - r0 ; L u (1-u)^2 ; 0.   V_e = U_c + somme_a w_a^2 [y - h]^2 / 2.
#   Régimes : B0 (nu) ; Bg (nu + amortisseur radial gamma = 0,04, puissance gamma r'^2 vers Q_ext) ; H3 (w = 1, sqrt 2, 2 ; nu = 0) ; X3 (idem, nu = 0,04).
#   Sources : S (porteur 0 contre ses trois voisins à chaque choc) ; C (porteurs 0, 1, 2, 3, 0, 1... à tour de rôle) ; F (arête 0-1 seule : témoin construit).
#   Choc : A = somme v.g, B = somme |g|^2, lambda = [-A + sqrt(A^2 + 2 B W)]/B, v <- v + lambda g ; W = P c ; chocs aux instants j c T0, j = 0..N-1, N = 24/c.
#   L'injection S'ARRETE au premier franchissement sortant r_e >= r_c d'un lien quelconque (ou à 24 T0) ; évolution passive jusqu'à 28 T0 ; aucun lien effacé.
#   Grille : P = 0, 1/48, 1/16, 1/8, 1/4, 1/2 ; c = 1/2, 4/5, 1, 6/5 ; 4 régimes ; 3 sources : 288 trajectoires. Témoins perturbés : 48 ; permutation d'étiquettes : 8.
#   Solveurs : DOP853 (rtol 1e-11, atol 1e-12), RK4 à T0/1024 et T0/2048 ; pas subdivisés à r = r0, r = r_c, aux chocs et aux événements.
# PRECISIONS D'EXECUTION (Claude, déclarées avant calcul ; voir c145_declaration.txt) :
#  - l'amortisseur radial de Bg agit à toute distance (aucun lien n'est effacé ; le protocole ne le borne pas à r < r_c) ;
#  - les directions n_vj d'un choc sont celles des positions à l'instant du choc ; pour C, le j-ième choc programmé sollicite le porteur j mod 4 ;
#  - « simultanées » : sorties à moins de 1e-5 T0 de la première ; F_U = 0 si la somme des énergies de cohésion est inférieure à 1e-20 ;
#  - côté d'un lien par rapport à r0 et r_c tenu en mémoire (tolérance 1e-10) ; à chaque changement de côté, le pas est coupé exactement sur la frontière
#    (RK4 : recherche du point de passage ; DOP853 : racine sur la sortie dense, pas refait jusqu'à la racine, puis reprise) ;
#  - statut : LIE (aucune sortie), TRANSITOIRE (sortie sans séparation persistante), PERSISTANTE (au moins un lien au-delà de r_c pendant tout [24 T0, 28 T0]) ;
#  - accord des solveurs exigé sur : existence d'une première rupture, groupe des liens de première rupture, statut, liens persistants ;
#  - mesures de concentration : relevées sur DOP853, échantillonné tous les T0/32 par sa sortie dense ;
#  - « statut de première rupture » : existence, groupe des liens, nombre de chocs délivrés avant elle (il fixe le travail injecté) ;
#  - ECART DECLARE AVANT EXECUTION (c145_declaration.txt) : sous la source F, les porteurs 0 et 1 se traversent (r = 0), point anguleux du potentiel que le protocole
#    ne prévoit pas de subdiviser ; RK4 y perd sa précision. Exécution à la lettre, sans ajout ; deux lectures rapportées : « lettre stricte » (bilan exigé des trois
#    intégrations) et « référence » (bilan exigé de DOP853, accord exigé des trois) ; le classement brut de chaque solveur est conservé ; rmin relevé par lien.
import numpy as np, math, json, sys, time, itertools
from numba import njit
from scipy.integrate import DOP853
from scipy.optimize import brentq
EDGE = list(itertools.combinations(range(4), 2)); EI = np.array([e[0] for e in EDGE]); EJ = np.array([e[1] for e in EDGE])
P0 = np.array([[0, 0, 0], [1, 0, 0], [.5, math.sqrt(3) / 2, 0], [.5, math.sqrt(3) / 6, math.sqrt(2 / 3)]], float)
T0 = 2 * math.pi / math.sqrt(2); KS = 2.0; D = 1.0; R0 = 1.0; LL = math.sqrt(6 * D / KS); RC = R0 + LL; TOL = 1e-10; S2 = math.sqrt(2)
REG = {'B0': ((), 0.0, 0.0, 0.0), 'Bg': ((), 0.0, 0.0, 0.04), 'H3': ((1.0, S2, 2.0), 1.0, 0.0, 0.0), 'X3': ((1.0, S2, 2.0), 1.0, 0.04, 0.0)}   # (fréquences, alpha, nu, gamma)
CAD = {'1/2': 0.5, '4/5': 0.8, '1': 1.0, '6/5': 1.2}; NIMP = {'1/2': 48, '4/5': 30, '1': 24, '6/5': 20}
CHECK = (1, 4, 8, 12, 16, 20, 24, 28); PUIS = (0.0, 1 / 48, 1 / 16, 1 / 8, 1 / 4, 1 / 2); TSIM = 1e-5

@njit(cache=True)
def pot1(r):
    if r < R0: return .5 * KS * (r - R0) ** 2, KS * (r - R0), r - R0, 1.0
    if r < RC:
        u = (r - R0) / LL; return D * (3 * u * u - 2 * u * u * u), D * (6 * u - 6 * u * u) / LL, LL * u * (1 - u) ** 2, (1 - u) * (1 - 3 * u)
    return D, 0.0, 0.0, 0.0

@njit(cache=True)
def rhs_nb(s, out, m, w2, alpha, nu, gam):
    n = s.shape[0]; o1 = 24; o2 = 24 + 6 * m; qd = 0.0
    for k in range(12): out[k] = s[12 + k]; out[12 + k] = 0.0
    for z in range(6):
        i = EI[z]; j = EJ[z]; dx = s[3 * j] - s[3 * i]; dy = s[3 * j + 1] - s[3 * i + 1]; dz = s[3 * j + 2] - s[3 * i + 2]
        r = math.sqrt(dx * dx + dy * dy + dz * dz); U, dU, h, dh = pot1(r); f = dU
        if m > 0:
            acc = 0.0
            for a in range(m):
                dev = s[o1 + z * m + a] - alpha * h; yd = s[o2 + z * m + a]; acc += w2[a] * dev
                out[o1 + z * m + a] = yd; out[o2 + z * m + a] = -nu * yd - w2[a] * dev; qd += nu * yd * yd
            f -= alpha * acc * dh
        if gam != 0.0:
            rd = ((s[12 + 3 * j] - s[12 + 3 * i]) * dx + (s[13 + 3 * j] - s[13 + 3 * i]) * dy + (s[14 + 3 * j] - s[14 + 3 * i]) * dz) / r
            f += gam * rd; qd += gam * rd * rd
        f /= r
        out[12 + 3 * i] += f * dx; out[13 + 3 * i] += f * dy; out[14 + 3 * i] += f * dz
        out[12 + 3 * j] -= f * dx; out[13 + 3 * j] -= f * dy; out[14 + 3 * j] -= f * dz
    out[n - 1] = qd

@njit(cache=True)
def lens(s, r):
    for z in range(6):
        i = EI[z]; j = EJ[z]; dx = s[3 * j] - s[3 * i]; dy = s[3 * j + 1] - s[3 * i + 1]; dz = s[3 * j + 2] - s[3 * i + 2]; r[z] = math.sqrt(dx * dx + dy * dy + dz * dz)

@njit(cache=True)
def rk4(s, h, sn, k1, k2, k3, k4, tmp, m, w2, alpha, nu, gam):
    n = s.shape[0]; rhs_nb(s, k1, m, w2, alpha, nu, gam)
    for q in range(n): tmp[q] = s[q] + .5 * h * k1[q]
    rhs_nb(tmp, k2, m, w2, alpha, nu, gam)
    for q in range(n): tmp[q] = s[q] + .5 * h * k2[q]
    rhs_nb(tmp, k3, m, w2, alpha, nu, gam)
    for q in range(n): tmp[q] = s[q] + h * k3[q]
    rhs_nb(tmp, k4, m, w2, alpha, nu, gam)
    for q in range(n): sn[q] = s[q] + h / 6 * (k1[q] + 2 * k2[q] + 2 * k3[q] + k4[q])

@njit(cache=True)
def rk_segment(s, t, tm, hmax, side, ev, nev, rmin, m, w2, alpha, nu, gam):
    """RK4 de t à tm, pas égaux <= hmax, coupés exactement à r = r0 et r = r_c ; ev : (instant, lien, sens) des passages de r_c ; renvoie nev"""
    n = s.shape[0]; sn = np.empty(n); st = np.empty(n); k1 = np.empty(n); k2 = np.empty(n); k3 = np.empty(n); k4 = np.empty(n); tmp = np.empty(n)
    rp = np.empty(6); rn = np.empty(6); rt = np.empty(6); nst = int(math.ceil((tm - t) / hmax - 1e-9))
    if nst < 1: nst = 1
    h = (tm - t) / nst; lens(s, rp)
    for i in range(nst):
        tc = t + i * h; rem = h; guard = 0
        while rem > 1e-14 * h and guard < 400:
            guard += 1; rk4(s, rem, sn, k1, k2, k3, k4, tmp, m, w2, alpha, nu, gam); lens(sn, rn); best = 2.0; bz = -1; bk = -1
            for kk in range(2):
                c = R0 if kk == 0 else RC
                for z in range(6):
                    b = rn[z] - c
                    if abs(b) <= TOL: continue
                    sg = 1 if b > 0 else -1
                    if sg == side[kk, z]: continue
                    a = rp[z] - c
                    if a * b < 0.0:
                        lo = 0.0; hi = 1.0; flo = a; fhi = b; th = 0.5
                        for it in range(100):
                            th = lo - flo * (hi - lo) / (fhi - flo)
                            if it % 3 == 2 or th <= lo or th >= hi: th = .5 * (lo + hi)
                            rk4(s, th * rem, st, k1, k2, k3, k4, tmp, m, w2, alpha, nu, gam); lens(st, rt); f = rt[z] - c
                            if abs(f) < 1e-14 or (hi - lo) < 1e-15: break
                            if f * flo < 0.0: hi = th; fhi = f
                            else: lo = th; flo = f
                        if th < best: best = th; bz = z; bk = kk
                    else:                                    # déjà sur la frontière au début du sous-pas : changement de côté enregistré ici
                        side[kk, z] = sg
                        if kk == 1 and nev < ev.shape[0]: ev[nev, 0] = tc; ev[nev, 1] = z; ev[nev, 2] = sg; nev += 1
            if bz < 0:
                for q in range(n): s[q] = sn[q]
                for z in range(6):
                    rp[z] = rn[z]
                    if rn[z] < rmin[z]: rmin[z] = rn[z]
                tc += rem; rem = 0.0
            elif best * rem < 1e-13:
                c = R0 if bk == 0 else RC; sg = 1 if rn[bz] - c > 0 else -1; side[bk, bz] = sg
                if bk == 1 and nev < ev.shape[0]: ev[nev, 0] = tc; ev[nev, 1] = bz; ev[nev, 2] = sg; nev += 1
            else:
                rk4(s, best * rem, sn, k1, k2, k3, k4, tmp, m, w2, alpha, nu, gam); lens(sn, rn); sg = -side[bk, bz]; side[bk, bz] = sg
                if bk == 1 and nev < ev.shape[0]: ev[nev, 0] = tc + best * rem; ev[nev, 1] = bz; ev[nev, 2] = sg; nev += 1
                for q in range(n): s[q] = sn[q]
                for z in range(6): rp[z] = rn[z]
                tc += best * rem; rem -= best * rem
    return nev

def pot_np(r):                                               # version numpy indépendante (celle de C-144), pour les bilans et les contrôles
    u = (r - R0) / LL
    U = np.where(r < R0, .5 * KS * (r - R0) ** 2, np.where(r < RC, D * (3 * u * u - 2 * u ** 3), D))
    dU = np.where(r < R0, KS * (r - R0), np.where(r < RC, D * (6 * u - 6 * u * u) / LL, 0.0))
    h = np.where(r < R0, r - R0, np.where(r < RC, LL * u * (1 - u) ** 2, 0.0))
    return U, dU, h

class Model:
    def __init__(self, reg):
        w, self.alpha, self.nu, self.gam = REG[reg]; self.w2 = np.array(w, float) ** 2; self.m = len(w); self.n = 24 + 12 * self.m + 1
        self.par = (self.m, self.w2, self.alpha, self.nu, self.gam)
    def fun(self, t, y):
        out = np.empty_like(y); rhs_nb(y, out, *self.par); return out
    def energies(self, s):
        m = self.m; x = s[:12].reshape(4, 3); v = s[12:24].reshape(4, 3); d = x[EJ] - x[EI]; r = np.sqrt((d * d).sum(1)); U, dU, h = pot_np(r)
        if m:
            y = s[24:24 + 6 * m].reshape(6, m); yd = s[24 + 6 * m:24 + 12 * m].reshape(6, m); ein = .5 * yd * yd + .5 * self.w2 * (y - self.alpha * h[:, None]) ** 2
        else: ein = np.zeros((6, 0))
        su = float(U.sum()); xc = x - x.mean(0)
        return dict(cin=.5 * float((v * v).sum()), coh=su, interne=float(ein.sum()), ext=float(s[-1]), interne_freq=[float(k) for k in ein.sum(0)], r=[float(k) for k in r],
                    U=[float(k) for k in U], FU=(float(U.max()) / su if su > 1e-20 else 0.0), etir=float(np.maximum(r - R0, 0).max()), tens=float(np.maximum(dU, 0).max()),
                    plateau=int((r >= RC).sum()), qmv=float(np.abs(v.sum(0)).max()), mcin=float(np.abs(np.cross(xc, v).sum(0)).max()))

def kick(s, W, v=None, edge=None):
    """choc interne équilibré de travail exact W ; renvoie le travail réellement fourni (calculé avant d'écrire dans l'état)"""
    x = s[:12].reshape(4, 3); vel = s[12:24].reshape(4, 3); g = np.zeros((4, 3))
    if edge is None:
        for j in range(4):
            if j != v: u = x[j] - x[v]; u = u / np.linalg.norm(u); g[j] += u; g[v] -= u
    else:
        a, b = edge; u = x[b] - x[a]; u = u / np.linalg.norm(u); g[a] = -u; g[b] = u
    A = float((vel * g).sum()); B = float((g * g).sum()); lam = (-A + math.sqrt(A * A + 2 * B * W)) / B; vn = vel + lam * g
    w = .5 * float((vn * vn).sum() - (vel * vel).sum()); s[12:24] = vn.ravel(); return w

class Sampler:
    """mesures de concentration sur la grille T0/32 (DOP853) : intégrales de F_U, de max U et de somme U, maxima d'étirement, de force et d'énergie sur un lien"""
    def __init__(self, md): self.md = md; self.dt = T0 / 32; self.k = 0; self.prev = None; self.I = np.zeros(3); self.mx = np.zeros(3); self.t1 = None; self.pre = None; self.tl = 0.0
    def val(self, y):
        x = y[:12].reshape(4, 3); d = x[EJ] - x[EI]; r = np.sqrt((d * d).sum(1)); U, dU, h = pot_np(r); su = float(U.sum()); mu = float(U.max())
        return np.array([mu / su if su > 1e-20 else 0.0, mu, su]), np.array([mu, float(np.maximum(r - R0, 0).max()), float(np.maximum(dU, 0).max())])
    def __call__(self, ta, tb, dense):
        while self.k * self.dt <= tb + 1e-12:
            tg = self.k * self.dt; a, b = self.val(dense(min(max(tg, ta), tb)))
            if self.t1 is not None and self.pre is None and tg > self.t1: self.pre = dict(t=self.tl / T0, I=[float(q) for q in self.I], mx=[float(q) for q in self.mx])
            if self.prev is not None: self.I += .5 * self.dt * (a + self.prev)
            self.mx = np.maximum(self.mx, b); self.prev = a; self.tl = tg; self.k += 1
    def snap(self): return dict(I=[float(q) for q in self.I], mx=[float(q) for q in self.mx])

def dop_segment(md, s, t, tm, side, ev, samp, rmin=None):
    """DOP853 de t à tm ; à chaque changement de côté (r0 ou r_c) : racine sur la sortie dense, pas refait jusqu'à la racine, reprise"""
    C = (R0, RC); r = np.empty(6); nloop = 0
    def one(y, z): lens(y, r); return r[z]
    while tm - t > 1e-13:
        nloop += 1
        if nloop > 200000: raise RuntimeError('boucle')
        sol = DOP853(md.fun, t, s, tm, rtol=1e-11, atol=1e-12, max_step=T0 / 32); cut = False
        while sol.status == 'running':
            sol.step()
            if sol.status == 'failed': raise RuntimeError('DOP853 en échec')
            ta = sol.t_old; tb = sol.t; dense = sol.dense_output(); tprev = ta
            for th in (.25, .5, .75, 1.0):
                tq = tb if th == 1.0 else ta + th * (tb - ta); yq = sol.y if th == 1.0 else dense(tq); lens(yq, r); cand = []
                if rmin is not None: np.minimum(rmin, r, out=rmin)
                for kk in (0, 1):
                    for z in range(6):
                        b = r[z] - C[kk]
                        if abs(b) > TOL and (1 if b > 0 else -1) != side[kk, z]: cand.append((kk, z, b))
                if cand:
                    roots = []
                    for kk, z, b in cand:
                        f = (lambda tt, kk=kk, z=z: one(dense(tt), z) - C[kk]); fa = f(tprev)
                        roots.append((brentq(f, tprev, tq, xtol=1e-15, rtol=8.9e-16) if fa * b < 0 else tprev, kk, z, b))
                    te0 = min(q[0] for q in roots)
                    for te, kk, z, b in roots:
                        if te <= te0 + 1e-12:
                            sg = 1 if b > 0 else -1; side[kk, z] = sg
                            if kk == 1:
                                ev.append((float(te), z, sg))
                                if sg > 0 and samp is not None and samp.t1 is None: samp.t1 = float(te)
                    if samp is not None: samp(ta, te0, dense)
                    if te0 - ta > 1e-12:
                        s2 = DOP853(md.fun, ta, sol.y_old, te0, rtol=1e-11, atol=1e-12, first_step=te0 - ta)
                        while s2.status == 'running': s2.step()
                        if s2.status == 'failed': raise RuntimeError('DOP853 en échec (reprise)')
                        s = s2.y.copy()
                    else: s = sol.y_old.copy()
                    t = te0; cut = True; break
                tprev = tq
            if cut: break
            if samp is not None: samp(ta, tb, dense)
        if not cut: s = sol.y.copy(); t = tm
    return s

def run(reg, src, P, cad, solver='dop', sub=1, perturb=0.0, perm=None, sabotage=False, x0=None, v0=None, tend=28):
    """perm[i] = nouvelle étiquette de l'ancien porteur i (relabellisation exactement covariante) ; sub : RK4 au pas T0/(1024 sub)"""
    md = Model(reg); c = CAD[cad]; N = NIMP[cad]; W = P * c; s = np.zeros(md.n); pm = list(range(4)) if perm is None else list(perm)
    xi = P0.copy() if x0 is None else np.array(x0, float)
    if perturb: xi[1, 0] += perturb; xi -= xi.mean(0)
    xx = np.zeros((4, 3)); vv = np.zeros((4, 3))
    for i in range(4):
        xx[pm[i]] = xi[i]
        if v0 is not None: vv[pm[i]] = v0[i]
    s[:12] = xx.ravel(); s[12:24] = vv.ravel(); E0 = 24 * P + .5 * float((vv * vv).sum()); res = 24 * P; trav = 0.0; nk = 0; dem = None
    raw = sorted([(j * c * T0, 'k', j) for j in range(N) if j * c < tend] + [(float(k) * T0, 'c', k) for k in CHECK if k <= tend]); marks = []; flags = []
    for tm_, f_, j_ in raw:                                  # fusion des instants confondus (un choc et un point de contrôle au même instant)
        if marks and abs(tm_ - marks[-1]) < 1e-9: flags[-1][f_] = j_
        else: marks.append(tm_); flags.append({f_: j_})
    r = np.empty(6); lens(s, r); side = np.ones((2, 6), np.int64); side[0] = np.where(r >= R0, 1, -1); side[1] = np.where(r >= RC, 1, -1)
    ev = []; evb = np.zeros((4096, 3)); rmin = r.copy(); samp = Sampler(md) if solver == 'dop' else None; pts = {}; resid = 0.0; qm = 0.0; lm = 0.0; t = 0.0
    def tot(s): e = md.energies(s); return res + e['cin'] + e['coh'] + e['interne'] + (0.0 if sabotage else e['ext']), e
    for k, tm in enumerate(marks):
        if tm > t + 1e-12:
            if solver == 'dop': s = dop_segment(md, s, t, tm, side, ev, samp, rmin)
            else:
                nev = rk_segment(s, t, tm, T0 / (1024 * sub), side, evb, 0, rmin, *md.par)
                for q in range(nev): ev.append((float(evb[q, 0]), int(evb[q, 1]), int(evb[q, 2])))
            t = tm
        e_, en = tot(s); resid = max(resid, abs(e_ - E0)); qm = max(qm, en['qmv']); lm = max(lm, en['mcin'])
        if 'c' in flags[k]:
            en['source'] = res; en['travail'] = trav; en['chocs'] = nk
            if samp is not None: en['cumul'] = samp.snap()
            pts[int(flags[k]['c'])] = en
        if 'k' in flags[k] and P > 0 and not any(q[2] > 0 for q in ev):          # l'injection s'arrête au premier franchissement sortant
            j = flags[k]['k']
            if src == 'F': w = kick(s, W, edge=(pm[0], pm[1])); dem = 'arête'
            else: v = pm[0] if src == 'S' else pm[j % 4]; w = kick(s, W, v=v); dem = v
            res -= w; trav += w; nk += 1; e_, en = tot(s); resid = max(resid, abs(e_ - E0)); qm = max(qm, en['qmv']); lm = max(lm, en['mcin'])
    out_t = [[q[0] for q in ev if q[1] == z and q[2] > 0] for z in range(6)]; in_t = [[q[0] for q in ev if q[1] == z and q[2] < 0] for z in range(6)]
    lens(s, r); tf = 24 * T0; first = [min(o) if o else None for o in out_t]; t1 = min([q for q in first if q is not None], default=None)
    grp = sorted(z for z in range(6) if first[z] is not None and first[z] <= t1 + TSIM * T0) if t1 is not None else []
    pers = [z for z in range(6) if r[z] >= RC and out_t[z] and not any(te >= tf for te in in_t[z]) and not any(te > tf for te in out_t[z])]
    inv = {pm[i]: i for i in range(4)}; lab = lambda z: tuple(sorted((inv[EDGE[z][0]], inv[EDGE[z][1]])))          # liens rendus dans les étiquettes d'origine
    o = dict(statut='PERSISTANTE' if pers else ('TRANSITOIRE' if t1 is not None else 'LIE'), liens=sorted(lab(z) for z in pers), t1=(t1 / T0 if t1 is not None else None),
             groupe=sorted(lab(z) for z in grp), demandeur=(inv[dem] if isinstance(dem, int) and t1 is not None else (dem if t1 is not None else None)), chocs=nk, travail=trav,
             reserve=res, premier=[(q / T0 if q is not None else None) for q in first], sorties=[len(q) for q in out_t], recaptures=[len(q) for q in in_t],
             r_fin=[float(q) for q in r], rmin=[float(q) for q in rmin], points=pts, residu_abs=resid, residu_rel=resid / (E0 if E0 > 0 else 1.0), qmv=qm, mcin=lm)
    if samp is not None: o['avant'] = samp.pre if samp.pre is not None else dict(t=samp.tl / T0, I=[float(q) for q in samp.I], mx=[float(q) for q in samp.mx])
    return o

def key(d): return (d['t1'] is not None, tuple(tuple(q) for q in d['groupe']), d['chocs'], d['statut'], tuple(tuple(q) for q in d['liens']))

def traj(a):
    kind = a[0]; t0 = time.time()
    if kind == 'G':
        _, reg, src, P, cad = a; o = dict(type='G', regime=reg, source=src, P=P, cadence=cad)
        o['dop'] = run(reg, src, P, cad, 'dop'); o['rk1'] = run(reg, src, P, cad, 'rk', 1); o['rk2'] = run(reg, src, P, cad, 'rk', 2); sol = [o['dop'], o['rk1'], o['rk2']]
        o['accord'] = len(set(key(q) for q in sol)) == 1; o['bilan_ok'] = all(q['residu_abs'] <= 1e-6 and q['residu_rel'] <= 1e-6 for q in sol)
        o['verdict'] = o['dop']['statut'] if (o['accord'] and o['bilan_ok']) else 'INDETERMINE'                          # lettre stricte
        o['bilan_dop'] = o['dop']['residu_abs'] <= 1e-6 and o['dop']['residu_rel'] <= 1e-6
        o['verdict_ref'] = o['dop']['statut'] if (o['accord'] and o['bilan_dop']) else 'INDETERMINE'                      # lecture de référence
        tt = [q['t1'] for q in sol if q['t1'] is not None]; o['dt1'] = (max(tt) - min(tt)) if tt else 0.0
    elif kind == 'W':
        _, reg, src, P, cad, eps = a; o = dict(type='W', regime=reg, source=src, P=P, cadence=cad, eps=eps); o['dop'] = run(reg, src, P, cad, 'dop', perturb=eps)
    else:
        _, reg, src, P, cad, pm = a; o = dict(type='L', regime=reg, source=src, P=P, cadence=cad, perm=list(pm)); o['dop'] = run(reg, src, P, cad, 'dop', perm=pm)
    o['duree'] = round(time.time() - t0, 1); return o

if __name__ == '__main__':
    from multiprocessing import Pool
    run('H3', 'C', 0.25, '1', 'rk', 1, tend=1); run('Bg', 'S', 0.25, '1', 'rk', 1, tend=1)                                   # compilation avant la bifurcation des processus
    jobs = [('G', reg, src, P, c) for P in PUIS for c in ('1/2', '4/5', '1', '6/5') for reg in ('B0', 'Bg', 'H3', 'X3') for src in ('S', 'C', 'F')]
    jobs += [('W', reg, src, P, c, eps) for P in (1 / 8, 1 / 4) for c in ('4/5', '1') for src in ('S', 'C', 'F') for reg in ('Bg', 'H3') for eps in (1e-8, -1e-8)]
    jobs += [('L', reg, src, P, c, (2, 0, 3, 1)) for (P, c) in ((1 / 8, '4/5'), (1 / 4, '1')) for src in ('S', 'C') for reg in ('Bg', 'H3')]
    res = []; t0 = time.time()
    with Pool(2) as pool:
        for o in pool.imap(traj, jobs):
            res.append(o); d = o['dop']
            if len(res) % 8 == 0 or len(res) == len(jobs): json.dump(res, open('c145.json', 'w'))
            extra = (f"rk={o['rk1']['statut'][:5]},{o['rk2']['statut'][:5]} accord={o['accord']} résidu={max(d['residu_rel'], o['rk1']['residu_rel'], o['rk2']['residu_rel']):.1e}/"
                     f"{max(d['residu_abs'], o['rk1']['residu_abs'], o['rk2']['residu_abs']):.1e} -> {o['verdict']} / {o['verdict_ref']} rmin={min(d['rmin']):.1e}") if o['type'] == 'G' else (f"eps={o.get('eps')}" if o['type'] == 'W' else f"perm={o['perm']}")
            print(f"{o['type']} P={o['P']:<8.5f} cad={o['cadence']:<4} {o['regime']:<3} {o['source']} dop={d['statut']:<11} t1={None if d['t1'] is None else round(d['t1'], 4)} groupe={d['groupe']} "
                  f"chocs={d['chocs']} travail={d['travail']:.4f} liens={d['liens']} {extra} ({time.time() - t0:.0f} s)", flush=True)
    json.dump(res, open('c145.json', 'w')); print('TERMINE', len(res))
