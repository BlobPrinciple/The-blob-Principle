# CONTROLES AVANT EXECUTION de C-145 / PR-2 — aucune trajectoire de la grille (puissances hors grille : 0,3 et 0,6).
import numpy as np, math, time, sys
from c145b import *
rng = np.random.default_rng(1452); ok = True
def chk(name, cond, info=''):
    global ok; ok = ok and bool(cond); print(('  OK   ' if cond else '  ECHEC'), name, info, flush=True)
def etat(x, v, n=25): s = np.zeros(n); s[:12] = x.ravel(); s[12:24] = v.ravel(); return s
def rdot(s):
    x = s[:12].reshape(4, 3); v = s[12:24].reshape(4, 3); d = x[EJ] - x[EI]; return ((v[EJ] - v[EI]) * d).sum(1) / np.sqrt((d * d).sum(1))

print('A. loi de collision')
w = [0, 0, 0, 0]
for _ in range(300):
    k = int(rng.integers(1, 4)); x = P0.copy() + rng.normal(0, .05, (4, 3)); zs = rng.choice(6, k, replace=False)
    for z in zs:                                              # amener les liens choisis exactement à r = 1/2 (un seul lien : exact ; plusieurs : itération)
        pass
    for it in range(200):
        for z in zs:
            i, j = EDGE[z]; d = x[j] - x[i]; r = np.linalg.norm(d); c = .5 * (r - .5) * d / r; x[i] += c; x[j] -= c
    v = rng.normal(0, 1, (4, 3)); s = etat(x, v); p0 = v.sum(0); l0 = np.cross(x, v).sum(0); u0 = rdot(s); con, good, dk = reflect(s, 0.5); v2 = s[12:24].reshape(4, 3); u2 = rdot(s)
    w[0] = max(w[0], abs(dk)); w[1] = max(w[1], np.abs(v2.sum(0) - p0).max()); w[2] = max(w[2], np.abs(np.cross(x, v2).sum(0) - l0).max())
    if len(con) == 1:
        z = con[0]; i, j = EDGE[z]; n = (x[j] - x[i]) / np.linalg.norm(x[j] - x[i]); u = u0[z]
        w[3] = max(w[3], np.abs(v2[i] - (v[i] + u * n)).max(), np.abs(v2[j] - (v[j] - u * n)).max(), abs(u2[z] + u0[z]))
chk('300 configurations (1 à 3 contacts) : énergie, quantité de mouvement, moment cinétique conservés', max(w[:3]) < 1e-12, str([f'{q:.0e}' for q in w[:3]]))
chk('un seul contact : formule du protocole (v_i + u n, v_j - u n), vitesse normale retournée', w[3] < 1e-12, f'{w[3]:.0e}')

print('B. contrôle analytique : respiration rentrante d\'énergie 3, six contacts simultanés à t = pi / (4 sqrt 8), retour à l\'état initial retourné à 2 t')
cen = P0.mean(0); e = P0 - cen; e = e / np.linalg.norm(e, axis=1)[:, None]; ta = math.pi / (4 * math.sqrt(8)); wv = math.sqrt(1.5)
for name, sub in (('dop', 0), ('rk', 1), ('rk', 2)):
    md = Model('B0'); s = etat(P0, -wv * e); r = np.empty(6); lens(s, r); side = np.ones((3, 6), np.int64); side[0] = np.where(r >= R0, 1, -1); side[1] = -1; colls = []; ev = []; rmin = r.copy()
    if name == 'dop': s = dop_seg2(md, s, 0.0, 2 * ta, side, ev, None, rmin, 0.5, 1, colls)
    else: s = rk_adv(md, s, 0.0, 2 * ta, sub, side, ev, rmin, 0.5, 1, colls)
    good = len(colls) == 1 and len(colls[0][1]) == 6 and abs(colls[0][0] - ta) < 1e-9 and np.abs(s[:12] - P0.ravel()).max() < 1e-9 and np.abs(s[12:24] - (wv * e).ravel()).max() < 1e-9 and rmin.min() > 0.5 - 1e-9
    chk(f'{name}{sub or ""}', good, f"collisions {len(colls)}, contacts {len(colls[0][1]) if colls else 0}, écart d'instant {abs(colls[0][0]-ta) if colls else None:.1e}, retour : positions {np.abs(s[:12]-P0.ravel()).max():.1e}, vitesses {np.abs(s[12:24]-(wv*e).ravel()).max():.1e}, r minimal {rmin.min():.12f}")

print('C. règle A2 sur une suite d\'événements fabriquée')
evs = [(10 * T0, 2, 1), (10.5 * T0, 2, -1), (12 * T0, 3, 1)]
c1 = a2_state(evs, 11 * T0) == (True, None); c2 = a2_state(evs, 12.5 * T0) == (False, None); r3 = a2_state(evs, 13.2 * T0); c3 = (r3[0] is False and abs(r3[1] - 13 * T0) < 1e-12)
r4 = a2_state(evs + [(13.5 * T0, 3, -1)], 14 * T0); c4 = (r4[0] is True and abs(r4[1] - 13 * T0) < 1e-12)
chk('lié / sorti / arrêt définitif après T0 hors portée / arrêt conservé après recapture', c1 and c2 and c3 and c4)

print('D. géométries')
ds = [delta(j) for j in (1, 2, 3, 4)]
chk('quatre directions centrées, de norme 1, distinctes', all(np.abs(d.mean(0)).max() < 1e-15 and abs(np.linalg.norm(d) - 1) < 1e-15 for d in ds) and min(np.linalg.norm(ds[a] - ds[b]) for a in range(4) for b in range(a)) > .1 and min(np.linalg.norm(ds[a] + ds[b]) for a in range(4) for b in range(a)) > .1)
chk('neuf géométries, écart de 1e-8 au tétraèdre exact', all(abs(np.linalg.norm(geometrie(g) - P0) - 1e-8) < 1e-12 for g in range(1, 9)) and np.linalg.norm(geometrie(1) + geometrie(2) - 2 * P0) < 1e-16)

print('E. trajectoires hors grille (P = 0,3 et 0,6 ; cadence 4/5 ; a = 1/2) : bilans, cœur respecté, accord des trois intégrations')
t0 = time.time(); worst = {'dop': 0.0, 'rk1': 0.0, 'rk2': 0.0}; agree = 0; tot = 0; rmn = 9.; ncolt = 0; amb = 0; dk = 0.0
for P in (0.3, 0.6):
    for reg in ('B0', 'Bg', 'H3', 'X3'):
        for src in 'SCF':
            for stop in ('A1', 'A2'):
                if P == 0.6 and reg in ('H3', 'X3') and stop == 'A1': continue
                o = traj2(dict(camp='x', reg=reg, src=src, P=P, cad='4/5', stop=stop, a=0.5, cmode=1, g=(3 if stop == 'A2' else 0))); d = o['dop']; tot += 1; agree += o['accord']
                for k in worst: worst[k] = max(worst[k], o[k]['residu_abs'], o[k]['residu_rel'])
                rmn = min(rmn, min(min(o[k]['rmin']) for k in worst)); ncolt += d['ncol']; amb += any(o[k]['ambigu'] for k in worst); dk = max(dk, max(o[k]['dkcol'] for k in worst))
                print(f"     P={P} {reg} {src} {stop} g={o['g']} : {d['statut']:<6} t1={None if d['t1'] is None else round(d['t1'],4)} gr={d['groupe']} chocs={d['chocs']}/{d['sautes']} liens={d['liens']} col={d['ncol']}(simult. {d['nsimul']}) "
                      f"arrêt={None if d['tstop'] is None else round(d['tstop'],2)} | rk {o['rk1']['statut']},{o['rk2']['statut']} | résidus {d['residu_abs']:.0e} {o['rk1']['residu_abs']:.0e} {o['rk2']['residu_abs']:.0e} | accord {o['accord']} amb={d['ambigu']},{o['rk1']['ambigu']},{o['rk2']['ambigu']} ({o['duree']} s)", flush=True)
print(f'     {tot} triplets en {time.time()-t0:.0f} s ; accord {agree}/{tot} ; collisions (DOP853) {ncolt} ; ambigus {amb}')
for k in worst: chk(f'{k} : bilan sous 1e-6', worst[k] <= 1e-6, f'{worst[k]:.1e}')
chk('aucun lien sous r = a (tolérance 1e-9)', rmn >= 0.5 - 1e-9, f'r minimal {rmn:.12f}'); chk('aucune collision ne change l\'énergie cinétique', dk < 1e-12, f'{dk:.0e}')

print('F. témoins négatifs')
d0 = run2('B0', 'F', 0.3, '4/5', cmode=0); chk('sans cœur, la même trajectoire descend sous r = 1/2 (le cœur agit)', min(d0['rmin']) < 0.5, f"r minimal {min(d0['rmin']):.2e}")
d1 = run2('B0', 'F', 0.3, '4/5', facteur=1.0); chk('collision sabotée (inélastique) détectée par le bilan', d1['residu_abs'] > 1e-3 or d1['ambigu'] is not None, f"résidu {d1['residu_abs']:.1e}, {d1['ambigu']}")
d2 = run2('Bg', 'S', 0.3, '4/5', sabotage=True); chk('bilan saboté (chaleur oubliée) détecté', d2['residu_abs'] > 1e-3, f"résidu {d2['residu_abs']:.1e}")
d3 = run2('B0', 'F', 0.3, '4/5', cmode=2); chk('témoin de traversée : premier passage sous r = 1/2 relevé', d3['tcoeur'] is not None and min(d3['rmin']) < 0.5, f"à {d3['tcoeur']} T0 ; première sortie {d3['t1']}")

print('G. permutation d\'étiquettes : covariance exacte aux premiers points de contrôle')
for pm in ((1, 0, 2, 3), (1, 2, 3, 0)):
    order = [EDGE.index(tuple(sorted((pm[a_], pm[b_])))) for a_, b_ in EDGE]
    for src in 'SC':
        a = run2('B0', src, 0.3, '4/5', stop='A2'); b = run2('B0', src, 0.3, '4/5', stop='A2', perm=pm)
        dv = {k: float(np.abs(np.array(a['points'][k]['r']) - np.array(b['points'][k]['r'])[order]).max()) for k in a['points'] if k in b['points']}
        chk(f'{src} {pm}', dv.get(1, 1) < 1e-9, ' ; '.join(f'{k} T0 : {v:.0e}' for k, v in dv.items()) + f" ; t1 {a['t1'] and round(a['t1'],4)} / {b['t1'] and round(b['t1'],4)}")
print('TOUS LES CONTROLES PASSENT' if ok else 'AU MOINS UN CONTROLE ECHOUE')
