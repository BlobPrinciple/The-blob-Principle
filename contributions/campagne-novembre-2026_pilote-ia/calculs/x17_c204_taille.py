#!/usr/bin/env python3
"""X-17 [APRES COUP] -- C-204c pousse plus loin en taille (graines 1 et 2, mesures a 660, 1000 et 1500 sommets environ) : le moteur de l'auteur finit-il par remplir le volume ?
(Claude, 17 novembre 2026.) Usage : python3 x17_c204_taille.py -> x17_c204_taille.json"""
import json, time
from c204c import Blob, mesure
out = []
for seed in (1, 2):
    bl = Blob(N0=300, seed=seed, forces=("grav", "em", "weak", "bord")); t0 = time.time(); tours = 0
    for cible in (600, 1000, 1500):
        while bl.N < cible: bl.step(0.12); tours += 1
        m = mesure(bl); m.update(graine=seed, tours=tours, secondes=round(time.time() - t0)); out.append(m)
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items() if k in ('graine', 'N', 'tours', 'voisins_moyens', 'cellules', 'groupes_de_5', 'part_exposee', 'part_surchargee', 'anneaux_fermes', 'part_5_6', 'secondes')}, flush=True)
        json.dump(out, open('x17_c204_taille.json', 'w'), indent=1)
