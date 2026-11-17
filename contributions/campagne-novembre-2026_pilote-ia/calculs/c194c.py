#!/usr/bin/env python3
"""C-194c -- contre-calcul independant du C-194 de ChatGPT (Claude, 17 novembre 2026), d'apres son seul PROTOCOLE SCELLE : decompte d'Euler sur le tore, incidences 5 et 6,
nombre d'aretes par sommet qu'exige une moyenne d* ; recompte depuis mes positions cristallographiques (A15, C15, sigma). Predictions : c194c_prediction.txt. Usage : python3 c194c.py -> c194c.json"""
import itertools, json, math
from fractions import Fraction
import numpy as np
import c189dc, c190c
from c193bc import complexe

DS = 2 * math.pi / math.acos(1 / 3); out = dict(d_etoile=DS, alpha=6 / (6 - DS), coordination=12 / (6 - DS), surplus=6 / (6 - DS) - 1, part_fournie=(6 - DS) / 6, six_par_sommet=6 / (6 - DS) - 6, fraction_de_six=DS - 5)
print({k: round(v, 6) for k, v in out.items()})
out['cristaux'] = {}
for nom, m, V in (('A15', c189dc.mesure(c189dc.A15, 1.30), 8), ('C15', c189dc.mesure(c189dc.C15, 1.30), 24), ('sigma', c190c.mesure(1.30), 30)):
    E = m.get('liens_par_maille', m.get('liens')); T = m.get('tetraedres_par_maille', m.get('tetraedres')); h = {int(k): v for k, v in m['distribution'].items()}; n5, n6 = h.get(5, 0), h.get(6, 0)
    out['cristaux'][nom] = dict(V=V, E=E, T=T, n5=n5, n6=n6, autres={k: v for k, v in h.items() if k not in (5, 6)}, E_sur_V=E / V, six_par_sommet=n6 / V, euler=bool(E == V + T), n5_egal_6V=bool(n5 == 6 * V), n6_egal_E_moins_6V=bool(n6 == E - 6 * V),
                                somme=bool(5 * n5 + 6 * n6 == 6 * T), six_T=6 * T, exces_sur_arbre=E - (V - 1), moyenne=str(Fraction(6 * T, E)), moyenne_dec=6 * T / E, surchargees=m['faces_surchargees'])
    print(nom, out['cristaux'][nom])
ordre = sorted([('alpha(d*)', out['alpha'])] + [(k, v['E_sur_V']) for k, v in out['cristaux'].items()], key=lambda x: x[1]); out['ordre'] = ordre; print('ordre E/V :', ordre)
rng = np.random.default_rng(194); arbres = []
for n in (13, 100, 1000):
    E = [(int(rng.integers(0, v)), v) for v in range(1, n)]; T, F, tri = complexe(E, n); arbres.append(dict(n=n, aretes=len(E), triangles=tri, tetraedres=len(T)))
out['arbres'] = arbres; print('arbres', arbres)
K67 = [(i, 6 + j) for i in range(6) for j in range(7)]; T, F, tri = complexe(K67, 13); out['K_6_7'] = dict(aretes=len(K67), triangles=tri, tetraedres=len(T))
K13 = list(itertools.combinations(range(13), 2)); T, F, tri = complexe(K13, 13); out['K_13'] = dict(aretes=len(K13), triangles=tri, tetraedres=len(T), tetra_par_face=sorted(set(F.values())))
print('K6,7', out['K_6_7'], 'K13', out['K_13'])
json.dump(out, open('c194c.json', 'w'), indent=1)
