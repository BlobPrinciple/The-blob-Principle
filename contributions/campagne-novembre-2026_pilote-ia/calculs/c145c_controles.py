# CONTROLES AVANT EXECUTION de C-145 / PR-3 — aucune trajectoire de la grille (hors grille : P/D = 0,3 et 0,6 ; D = 4 ; cadences de la grille).
import numpy as np, math, time, sys
from c145c import *
import c145 as m1, c145b as m2
rng = np.random.default_rng(1453); ok = True
def chk(name, cond, info=''):
    global ok; ok = ok and bool(cond); print(('  OK   ' if cond else '  ECHEC'), name, info, flush=True)

print('A. second membre général contre celui de PR-1 / PR-2 (4 porteurs, D = 1), puis gradient de l\'énergie pour le tissu à 5 porteurs')
for g0, reg in ((0.0, 'B0'), (0.04, 'Bg')):
    cx = Ctx('K4', 1.0, g0, 0.5); md = m1.Model(reg); w = 0.0
    for _ in range(300):
        s = np.zeros(25); s[:12] = (P0 * rng.uniform(.6, 3.2) + rng.normal(0, .3, (4, 3))).ravel(); s[12:] = rng.normal(0, 1, 13); w = max(w, float(np.abs(cx.fun(0, s) - md.fun(0, s)).max()))
    chk(f'{reg} : écart maximal sur 300 états', w < 1e-12, f'{w:.0e}')
cx = Ctx('T5', 2.0, 0.0, 0.75); s = np.zeros(cx.N); s[:15] = (geometrie('T5', 0) * 1.6 + rng.normal(0, .2, (5, 3))).ravel(); f = cx.fun(0, s); w = 0.0
for q in range(15):
    sp = s.copy(); sm = s.copy(); sp[q] += 1e-6; sm[q] -= 1e-6; w = max(w, abs((cx.energies(sp)['coh'] - cx.energies(sm)['coh']) / 2e-6 + f[15 + q]))
chk('tissu, D = 2 : force + gradient', w < 1e-8, f'{w:.0e}')

print('B. contrôle analytique : respiration rentrante, D = 2, énergie 6 : six contacts à t = pi/16, état retourné à 2 t')
cen = P0.mean(0); e = P0 - cen; e = e / np.linalg.norm(e, axis=1)[:, None]; ta = math.pi / 16; wv = math.sqrt(3.0)
for name, sub in (('dop', 0), ('rk', 1), ('rk', 2)):
    cx = Ctx('K4', 2.0, 0.0, 0.5); s = np.zeros(25); s[:12] = P0.ravel(); s[12:24] = (-wv * e).ravel(); side = np.ones((3, 10), np.int64); side[1] = -1; colls = []; ev = []; st = dict(rmin=np.ones(6), ovl=-1.0, k=0, fprev=None, IFU=0.0)
    s = dop_seg3(cx, s, 0.0, 2 * ta, side, ev, st, colls) if name == 'dop' else rk_adv3(cx, s, 0.0, 2 * ta, sub, side, ev, st, colls)
    good = len(colls) == 1 and len(colls[0][1]) == 6 and abs(colls[0][0] - ta) < 1e-9 and np.abs(s[:12] - P0.ravel()).max() < 1e-9 and np.abs(s[12:24] - (wv * e).ravel()).max() < 1e-9 and st['rmin'].min() > 0.5 - 1e-9
    chk(f'{name}{sub or ""}', good, f"contacts {len(colls[0][1]) if colls else 0}, écart d'instant {abs(colls[0][0]-ta) if colls else float('nan'):.0e}, retour {np.abs(s[:12]-P0.ravel()).max():.0e}, r minimal {st['rmin'].min():.12f}")

print('C. le nouveau code redonne PR-2 (mêmes paramètres hors grille : P = 0,3 ; D = 1 ; a = 1/2)')
w = 0.0; n = 0; same = 0
for src in 'SCF':
    for stop in ('A1', 'A2'):
        for c in ('1/2', '1'):
            for g in (0, 3):
                a = run3('K4', src, 0.3, c, stop, 0.5, 1.0, 0.0, g); b = m2.run2('B0', src, 0.3, c, stop=stop, g=g); n += 1
                eq = (a['t1'] is None) == (b['t1'] is None) and a['Pany'] == b['Pany'] and a['chocs'] == b['chocs'] and a['ncol'] == b['ncol']; same += eq
                if a['t1'] is not None and b['t1'] is not None: w = max(w, abs(a['t1'] - b['t1']))
chk('24 trajectoires : mêmes sorties, mêmes séparations durables, mêmes nombres de chocs et de collisions', same == n, f'{same}/{n} ; écart maximal de première sortie {w:.0e} T0')

print('D. théorème d\'échelle [T-2] : D = 4, P = 1,2 contre D = 1, P = 0,3 (facteur 4 exact en machine), avec et sans friction, K4 et tissu')
n = 0; same = 0; w = 0.0
for top, a_ in (('K4', 0.5), ('T5', 0.75)):
    for g0 in (0.0, 0.04):
        for src in 'SC':
            a = run3(top, src, 0.3, '1', 'A2', a_, 1.0, g0, 3); b = run3(top, src, 1.2, '1', 'A2', a_, 4.0, g0, 3); n += 1
            eq = key3(a) == key3(b) and a['chocs'] == b['chocs'] and a['ncol'] == b['ncol']; same += eq
            if a['t1'] is not None and b['t1'] is not None: w = max(w, abs(a['t1'] - b['t1']))
            w = max(w, abs(a['travail'] * 4 - b['travail']) / 4, abs(a['chaleur'] * 4 - b['chaleur']) / 4)
chk('8 paires : mêmes événements en temps réduit, travail et chaleur multipliés par 4', same == n and w < 1e-9, f'{same}/{n} ; écart {w:.0e}')

print('E. trajectoires hors grille : bilans, cœur respecté sur toutes les paires, accord des trois intégrations')
t0 = time.time(); worst = {'dop': 0.0, 'rk1': 0.0, 'rk2': 0.0}; agree = 0; tot = 0; rmn = 9.; amb = 0; dk = 0.0; arel = 9.
for top, a_, D, g0 in (('K4', 0.5, 2.0, 0.0), ('K4', 0.5, 0.5, 0.04), ('K4', 0.25, 1.0, 0.0), ('K4', 0.75, 1.0, 0.0), ('T5', 0.75, 1.0, 0.0)):
    for src in 'SC':
        for stop in ('A1', 'A2'):
            for PD in (0.3, 0.6):
                o = traj3(dict(camp='x', top=top, src=src, P=PD * D, cad='1', stop=stop, a=a_, D=D, g0=g0, g=5)); d = o['dop']; tot += 1; agree += o['accord']
                for k in worst: worst[k] = max(worst[k], o[k]['residu_abs'], o[k]['residu_rel'])
                rmn = min(rmn, min(o[k]['rmin'] for k in worst) / a_); amb += any(o[k]['ambigu'] for k in worst); dk = max(dk, max(o[k]['dkcol'] for k in worst))
                if top == 'T5': print(f"     tissu {src} {stop} P/D={PD} : {d['statut']:<6} t1={d['t1'] and round(d['t1'],3)} liens primaires durables {d['liens']} tous {d['liens_tous']} connexe fenêtre {d['connexe_fenetre']} degré zéro {d['deg0']} chevauchement à {d['ovl'] and round(d['ovl'],2)} col {d['ncol']} | rk {o['rk1']['statut']},{o['rk2']['statut']} accord {o['accord']} ({o['duree']} s)", flush=True)
print(f'     {tot} triplets en {time.time()-t0:.0f} s ; accord {agree}/{tot} ; ambigus {amb}')
for k in worst: chk(f'{k} : bilan sous 1e-6', worst[k] <= 1e-6, f'{worst[k]:.1e}')
chk('aucune paire sous r = a (rapport minimal r / a)', rmn >= 1 - 2e-9, f'{rmn:.12f}'); chk('collisions sans variation d\'énergie', dk < 1e-12, f'{dk:.0e}')

print('F. témoins négatifs et tests unitaires')
d = run3('K4', 'S', 0.6, '1', 'A2', 0.5, 0.5, 0.04, 0, sabotage=True); chk('bilan saboté (chaleur oubliée) détecté', d['residu_abs'] > 1e-3, f"{d['residu_abs']:.1e}")
d = run3('T5', 'C', 0.3, '1', 'A2', 0.75, 1.0, 0.0, 0, facteur=1.0); chk('collision rendue inélastique détectée', d['residu_abs'] > 1e-3 or d['ambigu'] is not None, f"{d['residu_abs']:.1e} {d['ambigu']}")
d = run3('K4', 'S', 0.01, '1', 'A2', 0.5, 1.0, 0.0, 2); chk('[T-1] énergie 0,24 < D : aucune sortie', d['t1'] is None)
x = geometrie('T5', 0); s = np.zeros(31); s[:15] = x.ravel(); v3, v4 = vols(s); x2 = x.copy(); x2[4, 2] = +0.3; s2 = np.zeros(31); s2[:15] = x2.ravel(); w3, w4 = vols(s2)
chk('détecteur de chevauchement : tétraèdres de part et d\'autre de la face (non), du même côté (oui)', v3 * v4 < 0 and w3 * w4 > 0, f'{v3:.3f} {v4:.3f} / {w3:.3f} {w4:.3f}')
L = TOPO['T5'][1]; chk('connexité : tissu entier (oui) ; porteur 3 détaché (non) ; porteur 0 privé de ses liens primaires mais tenu par 4 (oui)', connexe(5, L, set()) and not connexe(5, L, {2, 4, 5}) and connexe(5, L, {0, 1, 2}))
chk('a = 1 : renvoyé BLOQUE, sans calcul', 'bloque' in run3('K4', 'S', 0.25, '1', 'A1', 1.0, 1.0, 0.0, 0))
xg = geometrie('K4', 3); chk('a = 1, géométrie perturbée : des liens partent sous le rayon', (np.sqrt(((xg[[b for a_, b in PRIM]] - xg[[a_ for a_, b in PRIM]]) ** 2).sum(1)) < 1 - 1e-9).any(), str(np.round((np.sqrt(((xg[[b for a_, b in PRIM]] - xg[[a_ for a_, b in PRIM]]) ** 2).sum(1)) - 1) * 1e8, 2)) + ' e-8')
print('TOUS LES CONTROLES PASSENT' if ok else 'AU MOINS UN CONTROLE ECHOUE')
