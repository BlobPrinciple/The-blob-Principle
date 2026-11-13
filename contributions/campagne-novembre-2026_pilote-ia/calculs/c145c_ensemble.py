#!/usr/bin/env python3
"""C-145 / PR-3 -- contre-audit du differend K4, arret A1, source S (Claude, 13 novembre 2026).

Prediction : c145c_ensemble_prediction.txt. Utilise c145c.py inchange (RK4, pas T0/1024).
Usage : python3 c145c_ensemble.py   (c145c.py doit etre dans le meme repertoire ou dans le repertoire parent)
"""
import json
import math
import pathlib
import sys
from collections import Counter
from multiprocessing import Pool

import numpy as np

ICI = pathlib.Path(__file__).resolve().parent
sys.path[:0] = [str(ICI), str(ICI.parent)]
import c145c  # noqa: E402

BASE = dict(top='K4', src='S', stop='A1', a=0.75, D=1.0, g0=0.0)
COUPLES = [(0.25, '1/2'), (0.25, '1'), (0.5, '1/2'), (0.5, '1')]


def une(arg):
    P, cad, x0, etiq = arg
    o = c145c.run3(P=P, cad=cad, g=0, solver='rk', sub=1, x0=x0, **BASE)
    return dict(P=P, cad=cad, etiq=etiq, statut=o['statut'], t1=o['t1'], ncol=o['ncol'], chocs=o['chocs'])


def brut(j):
    return np.array([[math.sin(2 * math.pi * j * (3 * i + k + 1) / 17) for k in range(3)] for i in range(4)])


if __name__ == '__main__':
    P0 = c145c.geometrie('K4', 0)
    taches = []
    for P, cad in COUPLES:
        for g in range(1, 9):
            sg, j = (1 if g % 2 == 1 else -1), (g + 1) // 2
            taches.append((P, cad, c145c.geometrie('K4', g), f'protocole g={g}'))
            d = brut(j)
            taches.append((P, cad, P0 + sg * 1e-8 * d / np.linalg.norm(d), f'sans centrage g={g}'))
            taches.append((P, cad, P0 + sg * 1e-8 * (d - d.mean(0)), f'sans normalisation g={g}'))
            taches.append((P, cad, P0 + sg * 1e-8 * d, f'ni centrage ni normalisation g={g}'))
    rng = np.random.default_rng(20261113)
    for P, cad in COUPLES:
        for q in range(100):
            d = rng.normal(size=(4, 3))
            d -= d.mean(0)
            taches.append((P, cad, P0 + 1e-8 * d / np.linalg.norm(d), 'ensemble'))
    with Pool(2) as pool:
        res = pool.map(une, taches, chunksize=4)
    bilan = dict(trajectoires=len(res))
    for P, cad in COUPLES:
        r = [x for x in res if x['P'] == P and x['cad'] == cad]
        ens = [x for x in r if x['etiq'] == 'ensemble']
        paquets = Counter(round(x['t1'] / 0.02) * 0.02 if x['t1'] is not None else None for x in ens).most_common()
        bilan[f'P={P},c={cad}'] = dict(
            protocole={x['etiq'][-3:]: (x['statut'], None if x['t1'] is None else round(x['t1'], 4)) for x in r if x['etiq'].startswith('protocole')},
            sans_centrage={x['etiq'][-3:]: (x['statut'], None if x['t1'] is None else round(x['t1'], 4)) for x in r if x['etiq'].startswith('sans centrage')},
            sans_normalisation={x['etiq'][-3:]: (x['statut'], None if x['t1'] is None else round(x['t1'], 4)) for x in r if x['etiq'].startswith('sans normalisation')},
            ni_l_un_ni_l_autre={x['etiq'][-3:]: (x['statut'], None if x['t1'] is None else round(x['t1'], 4)) for x in r if x['etiq'].startswith('ni centrage')},
            ensemble=dict(n=len(ens), statuts=dict(Counter(x['statut'] for x in ens)),
                          paquets_t1=[(None if k is None else round(k, 2), v) for k, v in paquets[:14]],
                          n_paquets_pour_90_pourcent=next(i + 1 for i in range(len(paquets)) if sum(v for _, v in paquets[:i + 1]) >= 0.9 * len(ens))))
    tot = [x for x in res if x['etiq'] == 'ensemble']
    bilan['ensemble_total'] = dict(n=len(tot), statuts=dict(Counter(x['statut'] for x in tot)))
    (ICI / 'c145c_ensemble.json').write_text(json.dumps(bilan, indent=1, ensure_ascii=False, default=str))
    print(json.dumps(bilan, indent=1, ensure_ascii=False, default=str))
