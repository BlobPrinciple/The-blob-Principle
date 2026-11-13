# C-145 / PR-2 — CŒUR DUR, TRAVERSEES, ARRET CAUSAL APRES RECAPTURE, ENSEMBLES DE PERTURBATIONS
# Protocole FIGE par ChatGPT (12 nov. 2026) ; sha256 f16dcbc17cba802619885e19c57eb6a08f22629efa0abf0ac3fc8381e00ecc2d, 14 699 octets, recalculée par Claude
# sur le contenu brut du fichier. Prédiction de Claude enregistrée avant tout calcul : c145pr2_prediction.txt (23 h 33 UTC).
# Matériau, sources et chocs : ceux de C-145 / PR-1 (repris de c145.py, sans changement). Nouveautés :
#   - cœur dur : quand un lien descend à r = a, collision élastique v+ = v- - 2 A^T (A A^T)^+ A v- sur les contacts entrants (un contact : échange des vitesses normales) ;
#   - arrêt A1 : fin de la source au premier lien sorti (r >= r_c) ; arrêt A2 : un choc n'est donné que si les six liens sont liés à l'instant de la tentative ;
#     fin définitive dès qu'un même lien est resté continûment sorti pendant T0 ; les chocs sautés restent dans la réserve ; la phase j mod 4 du demandeur est conservée ;
#   - 9 géométries : tétraèdre exact et +/- 1e-8 selon quatre directions delta_j[i,k] = sin(2 pi j (3i+k+1)/17), centrées, de norme de Frobenius 1 ;
#   - P_first : un lien du premier groupe sorti reste sorti sur tout [24, 28] T0 ; P_any : un lien quelconque ;
#   - campagnes : principale 1 296 (a = 1/2 ; P 1/8, 1/4, 1/2 ; 4 cadences ; S, C, F ; B0, Bg ; A1, A2) ; modes internes 432 ; rayon du cœur 288 (a = 1/4, 3/4) ;
#     témoin de traversée 144 (cœur mou, premier passage sous r = 1/2 relevé) : 2 160 trajectoires ; témoins d'étiquetage et comparateur à précision accrue en plus.
# PRECISIONS D'EXECUTION (Claude, déclarées avant calcul ; voir c145pr2_declaration.txt) :
#  - contact : lien à moins de 1e-9 de r = a ; contact entrant : vitesse normale négative ; après réflexion, si un lien au contact rentre encore (vitesse normale < -1e-12),
#    ou si un contact est détecté sans vitesse entrante, ou si plus de 4 000 collisions se suivent : trajectoire INDETERMINEE (collision ambiguë ou cascade), arrêtée là ;
#  - accord des solveurs exigé sur : existence d'une sortie, groupe de première sortie (à 1e-5 T0), P_first, P_any, existence d'un rebond et liens du premier contact ;
#  - lecture stricte : bilan sous 1e-6 (absolu et relatif) pour les trois intégrations ; référence : bilan de DOP853 ; classement brut de chaque solveur conservé ;
#  - témoins d'étiquetage : permutations (0 1) et (0 1 2 3), huit configurations B0 (4 couples, S et C), règles A1 et A2, DOP853, géométrie exacte ;
#  - comparateur à précision accrue : mêmes huit configurations, A1 et A2, DOP853 rtol 1e-12, atol 1e-13, pas maximal T0/128.
import numpy as np, math, json, sys, time
from numba import njit
from scipy.integrate import DOP853
from scipy.optimize import brentq
from c145 import EDGE, EI, EJ, P0, T0, R0, RC, TOL, REG, CAD, NIMP, TSIM, rhs_nb, lens, rk4, Model, kick, Sampler
CHECKB = (1, 4, 24, 28)

class Ambigu(Exception): pass

@njit(cache=True)
def rk_seg2(s, t, tm, hmax, side, ev, nev, rmin, acore, cmode, m, w2, alpha, nu, gam):
    """RK4 de t à tm (pas égaux <= hmax, coupés à r0, r_c et au cœur). Renvoie (instant atteint, nev, code) : 0 = tm atteint ; 1 = contact de cœur ; 9 = garde dépassée.
       ev : (instant, lien, sens, frontière) ; frontière 1 = r_c, 2 = cœur (témoin de traversée seulement)."""
    n = s.shape[0]; sn = np.empty(n); st = np.empty(n); k1 = np.empty(n); k2 = np.empty(n); k3 = np.empty(n); k4 = np.empty(n); tmp = np.empty(n)
    rp = np.empty(6); rn = np.empty(6); rt = np.empty(6); nst = int(math.ceil((tm - t) / hmax - 1e-9)); nk = 3 if cmode > 0 else 2
    if nst < 1: nst = 1
    h = (tm - t) / nst; lens(s, rp)
    for i in range(nst):
        tc = t + i * h; rem = h; guard = 0
        while rem > 1e-14 * h:
            guard += 1
            if guard > 400: return tc, nev, 9
            rk4(s, rem, sn, k1, k2, k3, k4, tmp, m, w2, alpha, nu, gam); lens(sn, rn); best = 2.0; bz = -1; bk = -1
            for kk in range(nk):
                c = R0 if kk == 0 else (RC if kk == 1 else acore)
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
                    else:
                        if kk == 2 and cmode == 1: return tc, nev, 1            # déjà au contact et rentrant
                        side[kk, z] = sg
                        if kk >= 1 and nev < ev.shape[0]: ev[nev, 0] = tc; ev[nev, 1] = z; ev[nev, 2] = sg; ev[nev, 3] = kk; nev += 1
            if bz < 0:
                for q in range(n): s[q] = sn[q]
                for z in range(6):
                    rp[z] = rn[z]
                    if rn[z] < rmin[z]: rmin[z] = rn[z]
                tc += rem; rem = 0.0
            elif best * rem < 1e-13:
                if bk == 2 and cmode == 1: return tc, nev, 1
                c = R0 if bk == 0 else (RC if bk == 1 else acore); sg = 1 if rn[bz] - c > 0 else -1; side[bk, bz] = sg
                if bk >= 1 and nev < ev.shape[0]: ev[nev, 0] = tc; ev[nev, 1] = bz; ev[nev, 2] = sg; ev[nev, 3] = bk; nev += 1
            else:
                rk4(s, best * rem, sn, k1, k2, k3, k4, tmp, m, w2, alpha, nu, gam); lens(sn, rn)
                for q in range(n): s[q] = sn[q]
                for z in range(6):
                    rp[z] = rn[z]
                    if rn[z] < rmin[z]: rmin[z] = rn[z]
                tc += best * rem; rem -= best * rem
                if bk == 2 and cmode == 1: return tc, nev, 1
                sg = -side[bk, bz]; side[bk, bz] = sg
                if bk >= 1 and nev < ev.shape[0]: ev[nev, 0] = tc; ev[nev, 1] = bz; ev[nev, 2] = sg; ev[nev, 3] = bk; nev += 1
    return tm, nev, 0

def reflect(s, acore, facteur=2.0):
    """collision élastique sur les contacts entrants ; renvoie (liens au contact entrant, ok, variation d'énergie cinétique)"""
    x = s[:12].reshape(4, 3); v = s[12:24].reshape(4, 3); d = x[EJ] - x[EI]; r = np.sqrt((d * d).sum(1)); nrm = d / r[:, None]; u = ((v[EJ] - v[EI]) * nrm).sum(1)
    near = [z for z in range(6) if r[z] <= acore + 1e-9]; con = [z for z in near if u[z] < 0]
    if not con: return [], False, 0.0
    A = np.zeros((len(con), 12))
    for q, z in enumerate(con): A[q, 3 * EI[z]:3 * EI[z] + 3] = -nrm[z]; A[q, 3 * EJ[z]:3 * EJ[z] + 3] = nrm[z]
    vf = v.ravel().copy(); vn = vf - facteur * A.T @ (np.linalg.pinv(A @ A.T, rcond=1e-10) @ (A @ vf)); k0 = .5 * float(vf @ vf); s[12:24] = vn
    v2 = vn.reshape(4, 3); u2 = ((v2[EJ] - v2[EI]) * nrm).sum(1); ok = all(u2[z] >= -1e-12 for z in near)
    return con, ok, .5 * float(vn @ vn) - k0

def a2_state(ev, tnow):
    """ev : passages de r_c (instant, lien, sens). Renvoie (les six liens sont liés à tnow, instant de l'arrêt définitif ou None)"""
    out = {}; fin = None
    for te, z, sg in sorted(ev):
        if te > tnow: break
        if sg > 0: out[z] = te
        elif z in out:
            if te - out[z] >= T0: fin = out[z] + T0 if fin is None else min(fin, out[z] + T0)
            del out[z]
    for z, t0 in out.items():
        if tnow - t0 >= T0: fin = t0 + T0 if fin is None else min(fin, t0 + T0)
    return len(out) == 0, fin

def dop_seg2(md, s, t, tm, side, ev, samp, rmin, acore, cmode, colls, rtol=1e-11, atol=1e-12, hmaxi=T0 / 32, facteur=2.0):
    C = (R0, RC, acore); r = np.empty(6); nloop = 0; nk = 3 if cmode else 2
    def one(y, z): lens(y, r); return r[z]
    while tm - t > 1e-13:
        nloop += 1
        if nloop > 100000: raise Ambigu('boucle')
        sol = DOP853(md.fun, t, s, tm, rtol=rtol, atol=atol, max_step=hmaxi); cut = False
        while sol.status == 'running':
            sol.step()
            if sol.status == 'failed': raise Ambigu('DOP853 en échec')
            ta = sol.t_old; tb = sol.t; dense = sol.dense_output(); tprev = ta
            for th in (1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6, 1.0):
                tq = tb if th == 1.0 else ta + th * (tb - ta); yq = sol.y if th == 1.0 else dense(tq); lens(yq, r); cand = []; rq = r.copy()
                for kk in range(nk):
                    for z in range(6):
                        b = r[z] - C[kk]
                        if abs(b) > TOL and (1 if b > 0 else -1) != side[kk, z]: cand.append((kk, z, b))
                if cand:
                    roots = []
                    for kk, z, b in cand:
                        f = (lambda tt, kk=kk, z=z: one(dense(tt), z) - C[kk]); fa = f(tprev)
                        roots.append((brentq(f, tprev, tq, xtol=1e-15, rtol=8.9e-16) if fa * b < 0 else tprev, kk, z, b))
                    te0 = min(q[0] for q in roots); coll = False
                    for te, kk, z, b in roots:
                        if te <= te0 + 1e-12:
                            if kk == 2 and cmode == 1: coll = True; continue
                            sg = 1 if b > 0 else -1; side[kk, z] = sg
                            if kk >= 1:
                                ev.append((float(te), z, sg, kk))
                                if kk == 1 and sg > 0 and samp is not None and samp.t1 is None: samp.t1 = float(te)
                    if samp is not None: samp(ta, te0, dense)
                    if te0 - ta > 1e-12:
                        s2 = DOP853(md.fun, ta, sol.y_old, te0, rtol=rtol, atol=atol, first_step=te0 - ta)
                        while s2.status == 'running': s2.step()
                        if s2.status == 'failed': raise Ambigu('DOP853 en échec (reprise)')
                        s = s2.y.copy()
                    else: s = sol.y_old.copy()
                    t = te0; cut = True; lens(s, r); np.minimum(rmin, r, out=rmin)          # distance minimale : seuls comptent les points de la trajectoire retenue
                    if coll:
                        con, ok, dk = reflect(s, acore, facteur); colls.append((float(t), con, dk))
                        if not con: raise Ambigu('contact sans vitesse entrante')
                        if not ok: raise Ambigu('collision ambiguë')
                        if len(colls) > 4000: raise Ambigu('cascade')
                    break
                np.minimum(rmin, rq, out=rmin); tprev = tq
            if cut: break
            if samp is not None: samp(ta, tb, dense)
        if not cut: s = sol.y.copy(); t = tm
    return s

def rk_adv(md, s, t, tm, sub, side, ev, rmin, acore, cmode, colls, facteur=2.0):
    evb = np.zeros((2048, 4))
    while tm - t > 1e-13:
        tr, nev, code = rk_seg2(s, t, tm, T0 / (1024 * sub), side, evb, 0, rmin, acore, cmode, *md.par)
        for q in range(nev): ev.append((float(evb[q, 0]), int(evb[q, 1]), int(evb[q, 2]), int(evb[q, 3])))
        t = tr
        if code == 9: raise Ambigu('garde')
        if code == 1:
            con, ok, dk = reflect(s, acore, facteur); colls.append((float(t), con, dk))
            if not con: raise Ambigu('contact sans vitesse entrante')
            if not ok: raise Ambigu('collision ambiguë')
            if len(colls) > 4000: raise Ambigu('cascade')
    return s

def delta(j):
    d = np.array([[math.sin(2 * math.pi * j * (3 * i + k + 1) / 17) for k in range(3)] for i in range(4)]); d -= d.mean(0); return d / np.linalg.norm(d)
def geometrie(g):
    """g = 0 : tétraèdre exact ; g = 1..8 : +1e-8 delta_1, -1e-8 delta_1, +1e-8 delta_2, ..."""
    if g == 0: return P0.copy()
    return P0 + (1 if g % 2 == 1 else -1) * 1e-8 * delta((g + 1) // 2)

def run2(reg, src, P, cad, stop='A1', a=0.5, cmode=1, g=0, solver='dop', sub=1, perm=None, rtol=1e-11, atol=1e-12, hmaxi=T0 / 32, sabotage=False, facteur=2.0, x0=None, v0=None, tend=28):
    md = Model(reg); c = CAD[cad]; N = NIMP[cad]; W = P * c; s = np.zeros(md.n); pm = list(range(4)) if perm is None else list(perm)
    xi = geometrie(g) if x0 is None else np.array(x0, float); xx = np.zeros((4, 3)); vv = np.zeros((4, 3))
    for i in range(4):
        xx[pm[i]] = xi[i]
        if v0 is not None: vv[pm[i]] = v0[i]
    s[:12] = xx.ravel(); s[12:24] = vv.ravel(); E0 = 24 * P + .5 * float((vv * vv).sum()); res = 24 * P; trav = 0.0; nk = 0; nsaut = 0; dem = None
    raw = sorted([(j * c * T0, 'k', j) for j in range(N) if j * c < tend] + [(float(k) * T0, 'c', k) for k in CHECKB if k <= tend]); marks = []; flags = []
    for tm_, f_, j_ in raw:
        if marks and abs(tm_ - marks[-1]) < 1e-9: flags[-1][f_] = j_
        else: marks.append(tm_); flags.append({f_: j_})
    r = np.empty(6); lens(s, r); side = np.ones((3, 6), np.int64); side[0] = np.where(r >= R0, 1, -1); side[1] = np.where(r >= RC, 1, -1)
    ev = []; colls = []; rmin = r.copy(); samp = Sampler(md) if solver == 'dop' else None; pts = {}; resid = 0.0; qm = 0.0; lm = 0.0; t = 0.0; amb = None; parchoc = []
    def tot(s): e = md.energies(s); return res + e['cin'] + e['coh'] + e['interne'] + (0.0 if sabotage else e['ext']), e
    try:
        for k, tm in enumerate(marks):
            if tm > t + 1e-12:
                nc0 = len(colls)
                if solver == 'dop': s = dop_seg2(md, s, t, tm, side, ev, samp, rmin, a, cmode, colls, rtol, atol, hmaxi, facteur)
                else: s = rk_adv(md, s, t, tm, sub, side, ev, rmin, a, cmode, colls, facteur)
                t = tm
            e_, en = tot(s); resid = max(resid, abs(e_ - E0)); qm = max(qm, en['qmv']); lm = max(lm, en['mcin'])
            if 'c' in flags[k]:
                en['source'] = res; en['travail'] = trav; en['chocs'] = nk
                if samp is not None: en['cumul'] = samp.snap()
                del en['U']; pts[int(flags[k]['c'])] = en
            if 'k' in flags[k] and P > 0:
                rc_ev = [(q[0], q[1], q[2]) for q in ev if q[3] == 1]
                if stop == 'A1': go = not any(q[2] > 0 for q in rc_ev)
                else: lie, fin = a2_state(rc_ev, tm); go = lie and fin is None
                if go:
                    j = flags[k]['k']
                    if samp is not None and samp.t1 is None: parchoc.append((tm / T0, trav, [float(q) for q in samp.I]))
                    if src == 'F': w = kick(s, W, edge=(pm[0], pm[1])); dem = 'arête'
                    else: v = pm[0] if src == 'S' else pm[j % 4]; w = kick(s, W, v=v); dem = v
                    res -= w; trav += w; nk += 1; e_, en = tot(s); resid = max(resid, abs(e_ - E0)); qm = max(qm, en['qmv']); lm = max(lm, en['mcin'])
                else: nsaut += 1
    except Ambigu as ex: amb = str(ex)
    rc_ev = [(q[0], q[1], q[2]) for q in ev if q[3] == 1]; co_ev = [(q[0], q[1], q[2]) for q in ev if q[3] == 2]
    out_t = [[q[0] for q in rc_ev if q[1] == z and q[2] > 0] for z in range(6)]; in_t = [[q[0] for q in rc_ev if q[1] == z and q[2] < 0] for z in range(6)]
    lens(s, r); tf = 24 * T0; te_ = 28 * T0; first = [min(o) if o else None for o in out_t]; t1 = min([q for q in first if q is not None], default=None)
    grp = sorted(z for z in range(6) if first[z] is not None and first[z] <= t1 + TSIM * T0) if t1 is not None else []
    pers = [z for z in range(6) if r[z] >= RC and out_t[z] and not any(q >= tf for q in in_t[z]) and not any(q > tf for q in out_t[z])] if amb is None else []
    inter = []                                                # intervalles de sortie de chaque lien, pour la fraction de fenêtre et les durées d'excursion
    for z in range(6):
        evz = sorted([(q, 1) for q in out_t[z]] + [(q, -1) for q in in_t[z]]); t0 = None
        for q, sg in evz:
            if sg > 0 and t0 is None: t0 = q
            elif sg < 0 and t0 is not None: inter.append((t0, q, z, True)); t0 = None
        if t0 is not None: inter.append((t0, te_, z, False))
    pts_w = sorted([(max(a_, tf), 1) for a_, b_, z, f in inter if b_ > tf] + [(min(b_, te_), -1) for a_, b_, z, f in inter if b_ > tf]); cov = 0.0; lvl = 0; tl = tf
    for q, sg in pts_w:
        if lvl > 0: cov += q - tl
        lvl += sg; tl = q
    exc = [b_ - a_ for a_, b_, z, f in inter if f]; _, fin = a2_state(rc_ev, te_)
    inv = {pm[i]: i for i in range(4)}; lab = lambda z: tuple(sorted((inv[EDGE[z][0]], inv[EDGE[z][1]])))
    tco = min([q[0] for q in co_ev if q[2] < 0], default=None)
    o = dict(statut=('LIE' if t1 is None else ('PANY' if pers else 'RECAPT')), t1=(t1 / T0 if t1 is not None else None), groupe=sorted(lab(z) for z in grp), liens=sorted(lab(z) for z in pers),
             Pany=bool(pers), Pfirst=bool(set(pers) & set(grp)), chocs=nk, sautes=nsaut, travail=trav, reserve=res, frac=cov / (4 * T0),
             retour=[(min(i_) / T0 if i_ else None) for i_ in in_t], nexc=len(exc), excmax=(max(exc) / T0 if exc else 0.0), excmoy=(float(np.mean(exc)) / T0 if exc else 0.0),
             ncol=len(colls), col1=(None if not colls else [colls[0][0] / T0, sorted(lab(z) for z in colls[0][1])]), nsimul=sum(len(q[1]) > 1 for q in colls),
             dkcol=max([abs(q[2]) for q in colls], default=0.0), ambigu=amb, rmin=[float(q) for q in rmin], tstop=(fin / T0 if fin is not None else None),
             tcoeur=(tco / T0 if tco is not None else None), r_fin=[float(q) for q in r], residu_abs=resid, residu_rel=resid / (E0 if E0 > 0 else 1.0), qmv=qm, mcin=lm,
             demandeur=(inv[dem] if isinstance(dem, int) else dem) if t1 is not None else None)
    if solver == 'dop':
        o['points'] = pts; o['parchoc'] = parchoc
        o['avant'] = samp.pre if samp.pre is not None else dict(t=samp.tl / T0, I=[float(q) for q in samp.I], mx=[float(q) for q in samp.mx])
    return o

def key2(d): return (d['t1'] is not None, tuple(tuple(q) for q in d['groupe']), d['Pfirst'], d['Pany'], d['ncol'] > 0, None if d['col1'] is None else tuple(tuple(q) for q in d['col1'][1]), d['ambigu'] is None)

def traj2(job):
    t0 = time.time(); o = dict(job)
    kw = dict(stop=job['stop'], a=job['a'], cmode=job['cmode'], g=job['g'])
    if job['camp'] in ('etiq', 'fin'):
        ex = dict(perm=job['perm']) if job['camp'] == 'etiq' else dict(rtol=1e-12, atol=1e-13, hmaxi=T0 / 128)
        o['dop'] = run2(job['reg'], job['src'], job['P'], job['cad'], solver='dop', **kw, **ex)
    else:
        o['dop'] = run2(job['reg'], job['src'], job['P'], job['cad'], solver='dop', **kw); o['rk1'] = run2(job['reg'], job['src'], job['P'], job['cad'], solver='rk', sub=1, **kw)
        o['rk2'] = run2(job['reg'], job['src'], job['P'], job['cad'], solver='rk', sub=2, **kw); sol = [o['dop'], o['rk1'], o['rk2']]
        o['accord'] = len(set(key2(q) for q in sol)) == 1 and all(q['ambigu'] is None for q in sol)
        o['bilan_ok'] = all(q['residu_abs'] <= 1e-6 and q['residu_rel'] <= 1e-6 for q in sol); o['bilan_dop'] = o['dop']['residu_abs'] <= 1e-6 and o['dop']['residu_rel'] <= 1e-6
        o['verdict'] = o['dop']['statut'] if (o['accord'] and o['bilan_ok']) else 'INDETERMINE'; o['verdict_ref'] = o['dop']['statut'] if (o['accord'] and o['bilan_dop']) else 'INDETERMINE'
        tt = [q['t1'] for q in sol if q['t1'] is not None]; o['dt1'] = (max(tt) - min(tt)) if tt else 0.0
    o['duree'] = round(time.time() - t0, 2); return o

COUPLES = ((1 / 4, '1/2'), (1 / 4, '1'), (1 / 2, '1/2'), (1 / 2, '4/5'))
def jobs():
    J = []
    for P in (1 / 8, 1 / 4, 1 / 2):
        for c in ('1/2', '4/5', '1', '6/5'):
            for src in 'SCF':
                for reg in ('B0', 'Bg'):
                    for stop in ('A1', 'A2'):
                        for g in range(9): J.append(dict(camp='princ', reg=reg, src=src, P=P, cad=c, stop=stop, a=0.5, cmode=1, g=g))
    for P, c in COUPLES:
        for src in 'SCF':
            for reg in ('H3', 'X3'):
                for stop in ('A1', 'A2'):
                    for g in range(9): J.append(dict(camp='modes', reg=reg, src=src, P=P, cad=c, stop=stop, a=0.5, cmode=1, g=g))
    for P, c in COUPLES:
        for src in 'SC':
            for stop in ('A1', 'A2'):
                for a in (0.25, 0.75):
                    for g in range(9): J.append(dict(camp='coeur', reg='B0', src=src, P=P, cad=c, stop=stop, a=a, cmode=1, g=g))
    for P, c in COUPLES:
        for src in 'SC':
            for stop in ('A1', 'A2'):
                for g in range(9): J.append(dict(camp='trav', reg='B0', src=src, P=P, cad=c, stop=stop, a=0.5, cmode=2, g=g))
    for P, c in COUPLES:
        for src in 'SC':
            for stop in ('A1', 'A2'):
                for pm in ((1, 0, 2, 3), (1, 2, 3, 0)): J.append(dict(camp='etiq', reg='B0', src=src, P=P, cad=c, stop=stop, a=0.5, cmode=1, g=0, perm=pm))
                J.append(dict(camp='fin', reg='B0', src=src, P=P, cad=c, stop=stop, a=0.5, cmode=1, g=0))
    return J

if __name__ == '__main__':
    from multiprocessing import Pool
    run2('H3', 'C', 0.3, '4/5', solver='rk', tend=2); run2('Bg', 'S', 0.3, '4/5', solver='rk', tend=2)             # compilation avant la bifurcation des processus
    J = jobs(); res = []; t0 = time.time(); print(len(J), 'calculs :', {k: sum(j['camp'] == k for j in J) for k in ('princ', 'modes', 'coeur', 'trav', 'etiq', 'fin')}, flush=True)
    with Pool(2) as pool:
        for o in pool.imap(traj2, J, chunksize=4):
            res.append(o); d = o['dop']
            if len(res) % 200 == 0: json.dump(res, open('c145b.json', 'w'))
            ex = (f"rk={o['rk1']['statut']},{o['rk2']['statut']} accord={o['accord']} résidu={max(d['residu_abs'], o['rk1']['residu_abs'], o['rk2']['residu_abs']):.0e} -> {o['verdict']}/{o['verdict_ref']}") if 'rk1' in o else ''
            print(f"{o['camp']:<5} P={o['P']:<6.4f} c={o['cad']:<4} {o['reg']:<2} {o['src']} {o['stop']} a={o['a']} g={o['g']} dop={d['statut']:<6} t1={None if d['t1'] is None else round(d['t1'], 3)} gr={d['groupe']} "
                  f"chocs={d['chocs']}/{d['sautes']} W={d['travail']:.2f} liens={d['liens']} col={d['ncol']} amb={d['ambigu']} rmin={min(d['rmin']):.3f} {ex} ({time.time() - t0:.0f} s)", flush=True)
    json.dump(res, open('c145b.json', 'w')); print('TERMINE', len(res))
