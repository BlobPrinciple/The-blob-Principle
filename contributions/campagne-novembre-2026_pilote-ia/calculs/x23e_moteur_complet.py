#!/usr/bin/env python3
"""X-23 E -- l'etage de rigidite du moteur complet de l'auteur (<< blob ablation labo colab.py >>, charge comme dans c204c.py) le long de sa croissance par mitose.
Prediction scellee : x23e_moteur_complet_prediction.txt. Claude, 22 novembre 2026."""
import json, time
import numpy as np
from c204c import Blob
from x23_outils import analyse_exacte


def releve(bl, graine, tours):
    N = bl.N
    liens = sorted((i, j) for i in range(N) for j in bl.adj[i] if j > i)
    r = dict(graine=graine, tours=tours, N=N, liens=len(liens), voisins_moyens=2 * len(liens) / N)
    for d in (2, 3, 4):
        rng = np.random.default_rng([graine, N, d])
        a = analyse_exacte(N, liens, d, rng)
        r[f'etage{d}'] = {k: v for k, v in a.items() if not k.startswith('_')}
    return r


out = []
for graine, cibles in ((1, (600, 1000, 1500)), (2, (600, 1000, 1500)), (3, (600,)), (4, (600,))):
    bl = Blob(N0=300, seed=graine, forces=("grav", "em", "weak", "bord")); tours = 0
    for cible in (0,) + cibles:
        while bl.N < cible:
            bl.step(0.12); tours += 1
        r = releve(bl, graine, tours); out.append(r)
        print(json.dumps(r), flush=True)
        json.dump(out, open('x23e_moteur_complet.json', 'w'), indent=1)
