#!/usr/bin/env python3
"""X-14 [APRES COUP, non aveugle : fait apres lecture du C-189 de ChatGPT] -- controle de son complement : le minimum tabule de Lennard-Jones a 19 atomes (double icosaedre, symetrie D5h),
construit ici independamment (trois couronnes pentagonales, la mediane tournee de 36 degres, quatre atomes sur l'axe), relaxe, puis mesure avec le detecteur de c189c.py (Claude, 16 novembre 2026).
Usage : python3 x14_lj19_double_icosaedre.py -> x14_lj19_double_icosaedre.json"""
import json, math
import numpy as np
from c189c import relaxe, mesure
X = [[0, 0, z] for z in (-1.5, -0.5, 0.5, 1.5)]
for z, dec in ((-1.0, 0.0), (0.0, math.pi / 5), (1.0, 0.0)): X += [[0.85 * math.cos(2 * math.pi * k / 5 + dec), 0.85 * math.sin(2 * math.pi * k / 5 + dec), z] for k in range(5)]
Y, E, g, dmin = relaxe(np.array(X)); out = dict(E=E, reference=-72.659782, ecart=E + 72.659782, gradient=g, dmin=dmin, mesures=[mesure(Y, s) for s in (1.30, 1.25, 1.35)])
json.dump(out, open('x14_lj19_double_icosaedre.json', 'w'), indent=1); print('E %.9f' % E, 'ecart %.1e' % out['ecart'], 'grad %.1e' % g, [(m['seuil'], m['tetraedres'], m['distribution'], m['faces_surchargees']) for m in out['mesures']])
