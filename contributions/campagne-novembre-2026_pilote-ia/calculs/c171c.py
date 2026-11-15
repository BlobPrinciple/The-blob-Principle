#!/usr/bin/env python3
"""C-171c -- cout de chaque division possible autour d'un anneau ferme de cinq (Claude, 15 novembre 2026). Protocole et predictions : c171c_prediction.txt (ecrits avant)."""
import itertools, json, math
import numpy as np
import c132_audit as c132
from c120 import Mesh, SEEDS, vol6
from c169c import degagement_min, reunir
from x1_regles import hessien
from x3_anneaux import arbre
from x7_moindre_cout import bouts
out = []


def anneau_isole(n=5):
    m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); m.X = {0: np.array([0, 0, .5]), 1: np.array([0, 0, -.5])}
    for k in range(n): m.X[2 + k] = np.array([math.sqrt(3) / 2 * math.cos(2 * math.pi * k / n), math.sqrt(3) / 2 * math.sin(2 * math.pi * k / n), 0.0])
    T = [(0, 1, 2 + k, 2 + (k + 1) % n) for k in range(n)]
    m.T = set(t if vol6(m.X, t) > 0 else (t[1], t[0], t[2], t[3]) for t in T); m.nv = n + 2
    m.rest = {e: 1.0 for t in m.T for e in itertools.combinations(sorted(t), 2)}; Vref = {}; c132.relax(m, Vref); return m, Vref


def etudie(nom, m, Vref):
    E = m.inc(); bord = m._bedges(); inter = [f for f in E if f not in bord]; E0 = m.energy(); vp0 = float(hessien(m)[0][0])
    ring = set(t for f in inter for t in E[f]); faces = lambda t: set(itertools.combinations(sorted(t), 3)); fr = set(f for t in ring for f in faces(t))
    print(nom, '| cellules', len(m.T), '| fils interieurs', [(f, len(E[f])) for f in inter], '| E %.12f' % E0, '| vp min %.2e' % vp0, flush=True)
    for e in sorted(f for f, v in E.items() if len(v) == 1):
        t = E[e][0]; cat = 'A' if t in ring else ('C' if faces(t) & fr else 'D')
        m2 = m.copy(); V2 = dict(Vref); m2.bisect(e); c132.relax(m2, V2); E2 = m2.inc(); b2 = m2._bedges(); dg, chev = degagement_min(m2)
        r = dict(etat=nom, fil=list(e), categorie=cat, cout=float(m2.energy() - E0), admissible=bool(dg > 1e-9), degagement=dg, vp_min=float(hessien(m2)[0][0]),
                 anneaux_apres=sorted(len(v) for f, v in E2.items() if f not in b2))
        out.append(r); json.dump(out, open('c171c.json', 'w')); print('  ', nom, e, cat, 'cout %.9f' % r['cout'], 'adm', r['admissible'], 'vp %.2e' % r['vp_min'], 'anneaux', r['anneaux_apres'], flush=True)


m, V = anneau_isole(); etudie('S0', m, V)
seed = 9000; faits = 0
while faits < 3 and seed < 9030:
    m, V = arbre(seed, 30); c = [(float(np.linalg.norm(m.X[x] - m.X[y])), x, y) for (x, y), k in ((tuple(p), k) for p, k in bouts(m).items()) if k == 5 and tuple(sorted((x, y))) not in m.rest]
    if c:
        d, x, y = min(c); reunir(m, V, x, y); c132.relax(m, V)
        if degagement_min(m)[0] > 1e-9: etudie(f'S1_{seed}', m, V); faits += 1
        else: print('graine', seed, 'ecartee : chevauchement apres reunion', flush=True)
    else: print('graine', seed, 'ecartee : aucun eventail de cinq', flush=True)
    seed += 1
