#!/usr/bin/env python3
"""BP-S2c bis -- COMPLEMENT APRES COUP (declare) : F5 a epsilon = 4, chaines trois fois plus longues, deux departs, pour lever le
doute de convergence sur la fraction a neuf contacts (ecart de 2 points entre departs a R = 1,8 dans bps2c.json).
bps2c.py a recu apres coup une sortie de plus (erreur_deux_K4) ; la dynamique est inchangee."""
import json
from bps2c import moteur
out = {}
for R in (1.8, 2.3):
    for dep in ('aleatoire', 'compact'):
        r = moteur(5, R, depart=dep, pas=60000, rodage=20000, seed=500 + int(10 * R) + (dep == 'compact'))
        out[f'F5_R={R}_{dep}'] = r; print(R, dep, json.dumps(r['eps=4']), flush=True)
json.dump(out, open('bps2c_bis.json', 'w'), indent=1)
