#!/usr/bin/env python3
"""C-165c -- contre-calcul du C-165 de ChatGPT (Claude, 15 novembre 2026). Predictions : c165c_prediction.txt (ecrites avant)."""
import contextlib, gzip, io, itertools, json, math
import numpy as np
import c132_audit as c132, c164c, c163c_bis
from c155a import Tissu, EPSV
from c120 import Mesh, SEEDS, vol6
out = {}


def hessien(m):
    ids = sorted(m.X); pos = {v: i for i, v in enumerate(ids)}; n = len(ids); Hm = np.zeros((3 * n, 3 * n))
    for (a, b), R in m.rest.items():
        d = m.X[a] - m.X[b]; L = np.linalg.norm(d); u = d / L; K = np.outer(u, u) + (1 - R / L) * (np.eye(3) - np.outer(u, u)); i, j = 3 * pos[a], 3 * pos[b]
        Hm[i:i + 3, i:i + 3] += K; Hm[j:j + 3, j:j + 3] += K; Hm[i:i + 3, j:j + 3] -= K; Hm[j:j + 3, i:i + 3] -= K
    w, V = np.linalg.eigh(Hm); return w, V, ids


def spectre(m): w, V, ids = hessien(m); return [float(x) for x in w[:8]]


# U1, U2 : forme fermee
p = np.roots([144, -336, 270, -84, 7]); r = [x.real for x in p if abs(x.imag) < 1e-12 and abs(x.real - 0.94313066) < 1e-6][0]
a = r / (6 * r - 4); b = r / (math.sqrt(2) * (2 * r - 1)); Ef = 4 * (r - 1) ** 2 + 2 * (math.sqrt(2) * b - 1) ** 2 + 0.5 * (2 * a - 1) ** 2
Eref = 0.030574477178155993
out['U1'] = dict(racines=[complex(x).real if abs(x.imag) < 1e-12 else str(x) for x in p], r=r, a=a, b=b, coherence_r=abs(math.hypot(a, b) - r), E_formule=Ef, ecart_a_ma_valeur=abs(Ef - Eref))
out['U2'] = dict(polynome_en_E=3 * Eref ** 4 - 22 * Eref ** 3 + 39 * Eref ** 2 - 132 * Eref + 4, racines_E=[float(x.real) for x in np.roots([3, -22, 39, -132, 4]) if abs(x.imag) < 1e-12])
# U3, U4, U5 : triangulations de la branche E
E = json.load(gzip.open('c164c_E.json.gz', 'rt'))
def etat(m):
    Vref = {}; c132.relax(m, Vref); ts = Tissu(m); VR = np.array([Vref[t] for t in ts.TT]); X = ts.X0(); cl = ts.degagements(X); V = ts.volumes(X)
    return ts, VR, dict(E=float(ts.energie(X)), admissible=bool(ts.admissible(X, VR)), min_V_sur_Vref=float((V / VR).min()), degagement_min=float(min(v.min() for v in cl.values() if len(v))), spectre=spectre(m))
m, mid = c164c.rouge((0, 1)); ts, VR, d = etat(m); out['U4_rouge'] = d
for k, s in enumerate(E['suite']):
    m, mid = c164c.suite([tuple(e) for e in s['exemple']]); ts, VR, d = etat(m); d['ordres'] = s['ordres']; nom = 'U3_classe_D' if s['ordres'] == 144 else f'U4_suite_{k}'; out[nom] = d
    if s['ordres'] == 144:
        w, Vv, ids = hessien(m); X0 = np.array([m.X[v] for v in ids]); mode = Vv[:, 0].reshape(-1, 3); mode = mode / np.linalg.norm(mode)
        res = {}
        for sg in (1, -1):
            for v, x in zip(ids, X0 + sg * 0.003 * mode): m.X[v] = x
            Xp = ts.X0(); clp = ts.degagements(Xp)
            res[f'deplace_{sg:+d}'] = dict(E=float(ts.energie(Xp)), min_V_sur_Vref=float((ts.volumes(Xp) / VR).min()), degagement_min=float(min(v.min() for v in clp.values() if len(v))))
            r0 = c132.relax(m, {t: float(x) for t, x in zip(ts.TT, VR)}); X1 = ts.X0(); cl1 = ts.degagements(X1); adm = bool(ts.admissible(X1, VR)); methode = 'origine'
            E1 = float(ts.energie(X1)); dg = float(min(v.min() for v in cl1.values() if len(v)))
            if not adm:
                for v, x in zip(ids, X0 + sg * 0.003 * mode): m.X[v] = x
                X2, g, essais = ts.relaxe(VR, 165, sg + 2); methode = 'contrainte'
                if X2 is not None: X1 = ts.X0(); adm = bool(ts.admissible(X1, VR))
                else: methode = 'contrainte : aucun essai admissible'
            V1 = ts.volumes(ts.X0()); cl1 = ts.degagements(ts.X0())
            res[f'relaxe_{sg:+d}'] = dict(E_relaxation_origine=E1, degagement_min_relaxation_origine=dg, methode=methode, E=float(ts.energie(ts.X0())), admissible=adm, min_V_sur_Vref=float((V1 / VR).min()),
                                          degagement_min=float(min(v.min() for v in cl1.values() if len(v))), volumes_actifs=int((V1 < EPSV * VR * (1 + 2e-3)).sum()), spectre=spectre(m))
        out['U5'] = res
# U6, U8 : naissance 2
for nom, e2 in (('prive', (0, 2)), ('partage', (2, 3))):
    m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); m.bisect((0, 1)); c132.relax(m, {}); E0 = m.energy(); m.bisect(e2); Ei = m.energy(); c132.relax(m, {})
    out[f'U6_U8_{nom}'] = dict(E_avant=E0, cout_insertion=Ei - E0, E_final=m.energy(), cellules=len(m.T), spectre=spectre(m))
out['U8_formule'] = dict(prive=2 - math.sqrt(3), partage=0.25 + 1.5 * (math.sqrt(3) / 2 - 1) ** 2)
# U7 : trajectoire 1320
rel = []; orig = c163c_bis.mesures
def espion(m, ts, VR, f0, V0):
    r = orig(m, ts, VR, f0, V0); w = hessien(m)[0]
    if len(m.X) - 4 == 11:                      # complement apres coup (declare) : l'etat de la naissance 11 est-il un point-selle ? deplacement le long du mode negatif, puis relaxation
        wv, Vv, ids = hessien(m); mode = Vv[:, 0].reshape(-1, 3); c1 = {}
        for sg in (1, -1):
            m2 = m.copy()
            for v, x in zip(ids, mode): m2.X[v] = m2.X[v] + sg * 0.003 * x
            t2 = Tissu(m2); E_dep = float(t2.energie(t2.X0())); c132.relax(m2, {t: float(x) for t, x in zip(ts.TT, VR)}); X2 = t2.X0(); cl2 = t2.degagements(X2)
            c1[f'{sg:+d}'] = dict(E_depart=r['E'], E_deplace=E_dep, E_relaxe=float(t2.energie(X2)), admissible=bool(t2.admissible(X2, VR)), min_V_sur_Vref=float((t2.volumes(X2) / VR).min()),
                                  degagement_min=float(min(v.min() for v in cl2.values() if len(v))), vp_min=float(hessien(m2)[0][0]))
        out['C1_naissance_11'] = c1
    rel.append(dict(N0=len(m.X), vp_min=float(w[0]), nb_negatives=int((w < -1e-6).sum()), volumes_actifs=r['volumes_actifs'], paires_actives=r['paires_actives'], E=r['E'])); return r
c163c_bis.mesures = espion
with contextlib.redirect_stdout(io.StringIO()): c163c_bis.trajectoire(1320, 24, 'A')
import os; os.remove('c163c_bis_1320_A.json')
out['U7'] = dict(etats=rel, libres=sum(1 for x in rel if x['volumes_actifs'] == 0 and x['paires_actives'] == 0), libres_avec_vp_negative=[x['N0'] - 4 for x in rel if x['volumes_actifs'] == 0 and x['paires_actives'] == 0 and x['nb_negatives'] > 0],
                 contraints_avec_vp_negative=[x['N0'] - 4 for x in rel if (x['volumes_actifs'] or x['paires_actives']) and x['nb_negatives'] > 0])
json.dump(out, open('c165c.json', 'w'), indent=1)
for k, v in out.items():
    if k == 'U7': print('U7', json.dumps({x: y for x, y in v.items() if x != 'etats'})); [print('   n', x['N0'] - 4, 'vp_min %.6f' % x['vp_min'], 'neg', x['nb_negatives'], 'actifs', x['volumes_actifs'], x['paires_actives']) for x in v['etats']]
    else: print(k, json.dumps(v))
