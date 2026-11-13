# CONTROLES AVANT EXECUTION de C-145 / PR-1 — aucune trajectoire de la grille n'est calculée ici (puissances hors grille : 0,03 ; 0,3 ; 2).
import numpy as np, math, time, sys
import c145 as m5, c144 as m4
from c145 import *
from scipy.integrate import quad
rng = np.random.default_rng(145); ok = True
def chk(name, cond, info=''):
    global ok; ok = ok and bool(cond); print(('  OK   ' if cond else '  ECHEC'), name, info, flush=True)

print('A. second membre compilé contre une écriture numpy indépendante (celle de C-144, plus un amortisseur radial écrit à part)')
def rhs_np(reg, s):
    w, alpha, nu, gam = REG[reg]; mm = len(w); w2 = np.array(w) ** 2; x = s[:12].reshape(4, 3); v = s[12:24].reshape(4, 3); d = x[EJ] - x[EI]; r = np.sqrt((d * d).sum(1))
    U, dU, h, dh = m4.pot(r); f = dU.copy(); qd = 0.0; out = [v.ravel()]
    if mm:
        y = s[24:24 + 6 * mm].reshape(6, mm); yd = s[24 + 6 * mm:24 + 12 * mm].reshape(6, mm); dev = y - alpha * h[:, None]; f = f - alpha * (w2 * dev).sum(1) * dh
        ydd = -nu * yd - w2 * dev; qd += nu * float((yd * yd).sum())
    if gam: rd = ((v[EJ] - v[EI]) * d).sum(1) / r; f = f + gam * rd; qd += gam * float((rd * rd).sum())
    out.append((m4.M @ (d * (f / r)[:, None])).ravel())
    if mm: out += [yd.ravel(), ydd.ravel()]
    return np.concatenate(out + [[qd]])
for reg in REG:
    md = Model(reg); worst = 0.0
    for _ in range(300):
        s = np.zeros(md.n); s[:12] = (P0 * rng.uniform(.6, 3.2) + rng.normal(0, .3, (4, 3))).ravel(); s[12:] = rng.normal(0, 1, md.n - 12)
        worst = max(worst, float(np.abs(md.fun(0, s) - rhs_np(reg, s)).max()))
    chk(f'{reg} : écart maximal sur 300 états aléatoires', worst < 1e-12, f'{worst:.1e}')

print('B. les forces sont bien le gradient de l\'énergie (différences finies, H3)')
md = Model('H3'); s = np.zeros(md.n); s[:12] = (P0 * 1.7 + rng.normal(0, .2, (4, 3))).ravel(); s[24:24 + 18] = rng.normal(0, .3, 18)
def V(s): e = md.energies(s); return e['coh'] + e['interne'] - .5 * float((s[42:60] ** 2).sum())
f = md.fun(0, s); worst = 0.0
for q in list(range(12)) + list(range(24, 42)):
    sp = s.copy(); sm = s.copy(); sp[q] += 1e-6; sm[q] -= 1e-6; g = (V(sp) - V(sm)) / 2e-6; worst = max(worst, abs(g + f[12 + q if q < 12 else 18 + q]))
chk('écart force + gradient', worst < 1e-8, f'{worst:.1e}')

print('C. choc : théorème T-2, travail exact, quantité de mouvement et moment cinétique')
W = 0.37; md = Model('B0')
def rdot(s):
    x = s[:12].reshape(4, 3); v = s[12:24].reshape(4, 3); d = x[EJ] - x[EI]; return ((v[EJ] - v[EI]) * d).sum(1) / np.sqrt((d * d).sum(1))
s = np.zeros(md.n); s[:12] = P0.ravel(); w = kick(s, W, v=0); rd = rdot(s)
chk('S au repos : arêtes du porteur 0 à sqrt(2W), face opposée à sqrt(2W)/3', np.allclose(rd[:3], math.sqrt(2 * W), atol=1e-13) and np.allclose(rd[3:], math.sqrt(2 * W) / 3, atol=1e-13) and abs(w - W) < 1e-14, f'{rd[0]:.12f} contre {math.sqrt(2*W):.12f}')
s = np.zeros(md.n); s[:12] = P0.ravel(); w = kick(s, W, edge=(0, 1)); rd = rdot(s)
chk('F au repos : arête 0-1 à 2 sqrt(W), arêtes voisines à sqrt(W)/2, arête 2-3 à 0', abs(rd[0] - 2 * math.sqrt(W)) < 1e-13 and np.allclose(rd[1:5], math.sqrt(W) / 2, atol=1e-13) and abs(rd[5]) < 1e-13 and abs(w - W) < 1e-14, f'{rd[0]:.12f} contre {2*math.sqrt(W):.12f} ; rapport F/S = {2*math.sqrt(W)/math.sqrt(2*W):.6f}')
s = np.zeros(md.n); s[:12] = P0.ravel(); w = kick(s, W, v=2); rd = rdot(s); inc = [z for z in range(6) if 2 in EDGE[z]]
chk('demandeur 2 : ses trois arêtes à sqrt(2W)', np.allclose(rd[inc], math.sqrt(2 * W), atol=1e-13))
worst = [0.0, 0.0, 0.0]
for _ in range(200):
    s = np.zeros(md.n); x = P0 * rng.uniform(.7, 2) + rng.normal(0, .2, (4, 3)); v = rng.normal(0, 1, (4, 3)); s[:12] = x.ravel(); s[12:24] = v.ravel()
    p0 = v.sum(0); l0 = np.cross(x, v).sum(0); kw = dict(edge=(1, 3)) if rng.random() < .3 else dict(v=int(rng.integers(4))); w = kick(s, W, **kw); v2 = s[12:24].reshape(4, 3)
    worst = [max(worst[0], abs(w - W), abs(.5 * (v2 * v2).sum() - .5 * (v * v).sum() - W)), max(worst[1], np.abs(v2.sum(0) - p0).max()), max(worst[2], np.abs(np.cross(x, v2).sum(0) - l0).max())]
chk('200 états en mouvement : travail, quantité de mouvement, moment cinétique', max(worst) < 1e-12, str([f'{q:.1e}' for q in worst]))

print('D. contrôle analytique 1 : respiration de petite amplitude du liant nu, période 2 pi / sqrt(8)')
cen = P0.mean(0); e = (P0 - cen); e = e / np.linalg.norm(e, axis=1)[:, None]; T = 2 * math.pi / math.sqrt(8)
for name in ('dop', 'rk'):
    md = Model('B0'); s = np.zeros(md.n); s[:12] = P0.ravel(); s[12:24] = (1e-6 * e).ravel(); s0 = s.copy(); r = np.empty(6); lens(s, r); side = np.ones((2, 6), np.int64); side[0] = np.where(r >= R0, 1, -1); side[1] = -1
    if name == 'dop': s = dop_segment(md, s, 0.0, T, side, [], None)
    else: rk_segment(s, 0.0, T, T0 / 1024, side, np.zeros((64, 3)), 0, np.ones(6), *md.par)
    chk(f'{name} : retour à l\'état initial après une période', np.abs(s[:12] - s0[:12]).max() < 1e-11 and np.abs(s[12:24] - s0[12:24]).max() < 1e-11, f'positions {np.abs(s[:12]-s0[:12]).max():.1e}, vitesses {np.abs(s[12:24]-s0[12:24]).max():.1e} (amplitude 1e-6)')

print('E. contrôle analytique 2 : instant de sortie des six liens, respiration d\'énergie 8 (quadrature exacte du bilan)')
E = 8.0; tc = quad(lambda r: 1 / math.sqrt(4 / 3 * (E - 6 * float(m4.pot(np.array(r))[0]))), R0, RC, epsabs=1e-13, epsrel=1e-13)[0]
for name, sub in (('dop', 0), ('rk', 1), ('rk', 2)):
    md = Model('B0'); s = np.zeros(md.n); s[:12] = P0.ravel(); s[12:24] = (math.sqrt(E / 2) * e).ravel(); r = np.empty(6); lens(s, r); side = np.ones((2, 6), np.int64); side[0] = np.where(r >= R0, 1, -1); side[1] = -1
    if name == 'dop': ev = []; s = dop_segment(md, s, 0.0, 1.5, side, ev, None)
    else: evb = np.zeros((64, 3)); n = rk_segment(s, 0.0, 1.5, T0 / (1024 * sub), side, evb, 0, np.ones(6), *md.par); ev = [(evb[q, 0], int(evb[q, 1]), int(evb[q, 2])) for q in range(n)]
    ts = [q[0] for q in ev]; tol = 1e-9 if name == 'dop' else 1e-8
    chk(f'{name}{sub or ""} : six sorties à t = {tc:.10f}', len(ev) == 6 and all(q[2] > 0 for q in ev) and max(abs(q - tc) for q in ts) < tol, f'écart {max(abs(q-tc) for q in ts):.1e}' if ev else 'aucun événement')

print('F. bilans sur des trajectoires hors grille (P = 0,3 ; cadence 4/5), trois intégrations, quatre régimes, trois sources')
t0 = time.time(); worst = {'dop': [0, 0], 'rk1': [0, 0], 'rk2': [0, 0]}; agree = 0; tot = 0; ratios = []
for reg in REG:
    for src in 'SCF':
        a = run(reg, src, 0.3, '4/5', 'dop'); b = run(reg, src, 0.3, '4/5', 'rk', 1); c = run(reg, src, 0.3, '4/5', 'rk', 2); tot += 1; same = key(a) == key(b) == key(c); agree += same
        for nm, d in (('dop', a), ('rk1', b), ('rk2', c)): worst[nm] = [max(worst[nm][0], d['residu_abs']), max(worst[nm][1], d['residu_rel'])]
        ratios.append(b['residu_abs'] / max(c['residu_abs'], 1e-300))
        print(f"     {reg} {src} : {a['statut']:<11} t1={None if a['t1'] is None else round(a['t1'],5)} groupe={a['groupe']} chocs={a['chocs']} | rk1 t1={None if b['t1'] is None else round(b['t1'],5)} rk2 t1={None if c['t1'] is None else round(c['t1'],5)} "
              f"| résidus {a['residu_abs']:.1e} {b['residu_abs']:.1e} {c['residu_abs']:.1e} | accord {same} | qmv {a['qmv']:.1e} moment {a['mcin']:.1e} | rmin {min(a['rmin']):.1e}/{min(b['rmin']):.1e}", flush=True)
print(f'     durée {time.time()-t0:.0f} s pour {tot} triplets ; accord {agree}/{tot} ; rapport médian des résidus RK4 (pas / demi-pas) : {np.median(ratios):.1f}')
for nm in worst: chk(f'{nm} : résidu absolu et relatif sous 1e-6', worst[nm][0] <= 1e-6 and worst[nm][1] <= 1e-6, f'{worst[nm][0]:.1e} / {worst[nm][1]:.1e}')

print('G. témoins négatifs')
for reg in ('Bg', 'X3'):
    d = run(reg, 'S', 0.3, '4/5', 'dop', sabotage=True); chk(f'{reg} : bilan saboté (chaleur évacuée oubliée) détecté', d['residu_abs'] > 1e-3, f"résidu {d['residu_abs']:.2e}")
n = 0
for reg in REG:
    for src in 'SCF':
        d = run(reg, src, 0.03, '1', 'dop'); n += d['t1'] is None and d['statut'] == 'LIE'
chk('énergie totale 0,72 < D (P = 0,03 hors grille) : aucune sortie dans les 12 cas', n == 12, f'{n}/12')
d = run('B0', 'F', 2.0, '1', 'dop'); chk('P = 2 sous F, liant nu : une sortie est bien détectée', d['t1'] is not None, f"t1 = {d['t1']}, groupe {d['groupe']}, statut {d['statut']}")

print('H. permutation d\'étiquettes (hors grille, P = 0,3) : covariance exacte aux premiers points de contrôle, puis croissance de l\'écart (sensibilité)')
pm = (2, 0, 3, 1); inv = {pm[i]: i for i in range(4)}; order = [EDGE.index(tuple(sorted((pm[a_], pm[b_])))) for a_, b_ in EDGE]      # lien d'origine z -> indice du lien dans le calcul permuté
for reg, src in (('Bg', 'S'), ('Bg', 'C'), ('H3', 'S'), ('H3', 'C'), ('B0', 'C')):
    a = run(reg, src, 0.3, '4/5', 'dop'); b = run(reg, src, 0.3, '4/5', 'dop', perm=pm)
    dv = {k: float(np.abs(np.array(a['points'][k]['r']) - np.array(b['points'][k]['r'])[order]).max()) for k in a['points']}
    chk(f'{reg} {src} : distances identiques à 1 T0 et 4 T0 une fois les étiquettes rétablies', dv[1] < 1e-9 and dv[4] < 1e-7, ' ; '.join(f'{k} T0 : {v:.0e}' for k, v in dv.items()) + f" ; t1 {a['t1'] and round(a['t1'],3)} / {b['t1'] and round(b['t1'],3)}")
print('TOUS LES CONTROLES PASSENT' if ok else 'AU MOINS UN CONTROLE ECHOUE')
