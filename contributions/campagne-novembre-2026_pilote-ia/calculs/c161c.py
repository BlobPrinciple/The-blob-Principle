#!/usr/bin/env python3
"""C-161c -- la croissance de C-158c refaite a marge decroissante (Claude, 15 novembre 2026). Predictions : c161c_prediction.txt.
Usage : python3 c161c.py <graine> <nmax> <marge de degagement> <marge de volume>. c155a.py et c158c.py sont inchanges ; seules les deux marges sont remplacees."""
import json, sys
import c155a
seed, nmax, mg, mv = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
c155a.MARGE = mg; c155a.MARGEV = mv
import c158c                                   # lit les marges deja remplacees
import numpy as np
src = open('c156c.py').read().split("out = {}")[0].replace("from c155a import degagement, MARGE, EPSV, MARGEV", "from c155a import degagement, EPSV"); MARGE, MARGEV = mg, mv; exec(src)
rowsU, seq, stU = c155a.trajectoire(seed, nmax, 'U'); out = []
for r in rowsU:
    k = analyse(r['export']); out.append(dict(n=r['n'], arete=r['arete'], methode=r['methode'], E=r['E'], residu=k['residu'], contacts_actifs=k['contacts_actifs'], volumes_actifs=k['volumes_actifs'],
                multiplicateurs_contact=k['multiplicateurs_contact'], multiplicateur_max=k['multiplicateur_max'], degagement_min=r['degagement_min_global'], V_sur_Vref_min=r['min_V_sur_Vref'],
                recouvrements=r['recouvrements_controle_independant'], rapport_volume=r['rapport_volume'], qmin=r['qmin'], admissible=r['admissible']))
json.dump(dict(graine=seed, marge=mg, marge_volume=mv, statut=stU, etats=out), open(f'c161c_{seed}_{mg:g}.json', 'w'), indent=1)
print('STATUT', seed, mg, stU)
