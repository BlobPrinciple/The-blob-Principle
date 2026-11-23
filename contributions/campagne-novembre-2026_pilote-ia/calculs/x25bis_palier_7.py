#!/usr/bin/env python3
"""X-25 bis, ajout apres execution, non predit : un palier de plus (palier 7), comptes et controles de surface seulement (ni voisinages ni contacts, trop longs).
Usage : python3 x25bis_palier_7.py     Claude, 23 novembre 2026."""
import json, os, time
from x25bis_naissances_et_fermetures import Tissu
ICI = os.path.dirname(os.path.abspath(__file__))
t0 = time.time(); T = Tissu(3)
for g in range(1, 8): p = T.palier(g)
c = T.controle(complet=False)
r = dict(palier=7, constituants=c['constituants'], naissances=p['naissances'], accolements_du_palier=p['accolements'], liens=c['liens_de_surface'], cellules=c['cellules_de_surface'],
         faces_hors_de_deux_cellules=c['faces_hors_de_deux_cellules'], caracteristique_d_Euler=c['caracteristique_d_Euler'], comptes_attendus=c['comptes_attendus'],
         tetraedres_par_lien=c['tetraedres_par_lien'], fermetures_sur_naissances=c['fermetures_sur_naissances'], accolements_cumules={str(k): v for k, v in T.accole.items()})
print(json.dumps(r)); json.dump(r, open(os.path.join(ICI, 'x25bis_palier_7.json'), 'w'), indent=1)
