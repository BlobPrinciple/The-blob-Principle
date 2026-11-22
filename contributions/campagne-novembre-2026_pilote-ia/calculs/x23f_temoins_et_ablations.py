#!/usr/bin/env python3
"""X-23 F -- temoins et ablations du moteur complet de l'auteur (<< blob ablation labo colab.py >>, charge comme dans c204c.py).
Prediction scellee : x23f_temoins_et_ablations_prediction.txt. Claude, 22 novembre 2026."""
import json, sys
import numpy as np
from c204c import Blob
from x23_outils import analyse_exacte


def et(N, liens, d, rng):
    a = analyse_exacte(N, liens, d, rng)
    return {k: v for k, v in a.items() if not k.startswith('_')}


def liens_de(bl):
    return sorted((i, j) for i in range(bl.N) for j in bl.adj[i] if j > i)


def aleatoire(N, E, rng):
    s = set()
    while len(s) < E:
        a, b = int(rng.integers(N)), int(rng.integers(N))
        if a != b:
            s.add((min(a, b), max(a, b)))
    return sorted(s)


def degres_conserves(liens, rng, par_lien=10):
    L = [list(l) for l in liens]; ens = set(liens)
    for _ in range(par_lien * len(L)):
        i, j = int(rng.integers(len(L))), int(rng.integers(len(L)))
        if i == j:
            continue
        a, b = L[i]; c, d = L[j]
        if rng.random() < 0.5:
            c, d = d, c
        n1 = (min(a, d), max(a, d)); n2 = (min(c, b), max(c, b))
        if a == d or c == b or n1 in ens or n2 in ens:
            continue
        ens.discard((min(a, b), max(a, b))); ens.discard((min(L[j][0], L[j][1]), max(L[j][0], L[j][1])))
        ens.add(n1); ens.add(n2); L[i] = list(n1); L[j] = list(n2)
    return sorted(ens)


def terreau_des_points(pts, E):
    from scipy.spatial import cKDTree
    pts = np.asarray(pts); N = len(pts); r = 0.05
    while True:
        p = cKDTree(pts).query_pairs(r, output_type='ndarray')
        if len(p) >= E:
            break
        r *= 1.3
    d = np.linalg.norm(pts[p[:, 0]] - pts[p[:, 1]], axis=1)
    return sorted((int(min(a, b)), int(max(a, b))) for a, b in p[np.argsort(d)[:E]])


out = dict(temoins=[], ablations=[])
quoi = sys.argv[1:] or ['temoins', 'ablations']
if 'temoins' in quoi:
    for graine in (1, 2):
        bl = Blob(N0=300, seed=graine, forces=("grav", "em", "weak", "bord"))
        for cible in (600, 1000, 1500):
            while bl.N < cible:
                bl.step(0.12)
            N = bl.N; L = liens_de(bl); E = len(L)
            rng = np.random.default_rng([graine, N, 77])
            r = dict(graine=graine, N=N, liens=E, voisins_moyens=2 * E / N, moteur=et(N, L, 3, rng),
                     aleatoire=[et(N, aleatoire(N, E, rng), 3, rng) for _ in range(2)],
                     degres_conserves=[et(N, degres_conserves(L, rng), 3, rng) for _ in range(2)],
                     terreau_des_memes_points=et(N, terreau_des_points(bl.pts, E), 3, rng))
            out['temoins'].append(r)
            print(json.dumps(r), flush=True)
            json.dump(out, open('x23f_temoins_et_ablations.json', 'w'), indent=1)
if 'ablations' in quoi:
    toutes = ("grav", "em", "weak", "bord")
    for nom, forces in (('complet', toutes), ('sans_bord', ("grav", "em", "weak")), ('sans_grav', ("em", "weak", "bord")), ('sans_weak', ("grav", "em", "bord")),
                        ('sans_em', ("grav", "weak", "bord")), ('aucune_force', ())):
        for graine in (1, 2):
            bl = Blob(N0=300, seed=graine, forces=forces)
            while bl.N < 600:
                bl.step(0.12)
            N = bl.N; L = liens_de(bl); E = len(L)
            rng = np.random.default_rng([graine, N, 88])
            r = dict(config=nom, graine=graine, N=N, liens=E, voisins_moyens=2 * E / N, **{f'etage{d}': et(N, L, d, rng) for d in (2, 3, 4)})
            out['ablations'].append(r)
            print(json.dumps(r), flush=True)
            json.dump(out, open('x23f_temoins_et_ablations.json', 'w'), indent=1)
