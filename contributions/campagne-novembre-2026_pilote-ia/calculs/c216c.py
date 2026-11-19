#!/usr/bin/env python3
"""C-215c (suite) et C-216c -- controles APRES LECTURE des passations de ChatGPT (declare) : (1) son contre-exemple reversible a trois etats (C-215) ;
(2) tetraedre creux contre tetraedre plein : memes bords d'ordre 1 et 2, nombres de Betti differents (C-216, T1) ; (3) sortie certaine de tout sous-ensemble propre
d'une chaine finie irreductible (C-216, T5), sur des chaines tirees au hasard. Claude, 19 novembre 2026. Usage : python3 c216c.py"""
import itertools, json
from fractions import Fraction as F
import numpy as np
out = {}
P = [[F(8, 10), F(2, 10), 0], [F(1, 10), F(7, 10), F(2, 10)], [0, F(1, 10), F(9, 10)]]; pi = [F(1, 7), F(2, 7), F(4, 7)]
surv = []
v = [F(1), F(0)]
for n in range(0, 6):
    surv.append([str(sum(v)), str(F(4, 3) * F(9, 10) ** n - F(1, 3) * F(6, 10) ** n)]); v = [v[0] * P[0][0] + v[1] * P[1][0], v[0] * P[0][1] + v[1] * P[1][1]]
# temps moyens de sortie de {A,B} : (I - Q) t = 1
a, b, c, d = 1 - P[0][0], -P[0][1], -P[1][0], 1 - P[1][1]; det = a * d - b * c; tA = (d - b) / det; tB = (a - c) / det
out['C215'] = dict(stationnaire=all(sum(pi[i] * P[i][j] for i in range(3)) == pi[j] for j in range(3)), balance_detaillee=all(pi[i] * P[i][j] == pi[j] * P[j][i] for i in range(3) for j in range(3)),
                   survie_calculee_et_formule=surv, temps_moyen_de_rupture_depuis_A=str(tA), depuis_B=str(tB))
# tetraedre creux / plein
V = range(4); E = list(itertools.combinations(V, 2)); T = list(itertools.combinations(V, 3))
d1 = np.zeros((4, 6), int); d2 = np.zeros((6, 4), int); d3 = np.zeros((4, 1), int)
for j, (u, w) in enumerate(E): d1[u, j] = -1; d1[w, j] = 1
for j, t in enumerate(T):
    for k in range(3):
        f = tuple(x for i, x in enumerate(t) if i != k); d2[E.index(f), j] = (-1) ** k
for k in range(4): d3[T.index(tuple(x for i, x in enumerate(V) if i != k)), 0] = (-1) ** k
rk = np.linalg.matrix_rank
out['C216_T1'] = dict(d1_d2_nul=bool((d1 @ d2 == 0).all()), d2_d3_nul=bool((d2 @ d3 == 0).all()), b2_creux=int(4 - rk(d2)), b2_plein=int(4 - rk(d2) - rk(d3)), euler_creux=4 - 6 + 4, euler_plein=4 - 6 + 4 - 1)
# sortie certaine
rng = np.random.default_rng(216); pire = 0.0; nb = 0
for _ in range(200):
    n = int(rng.integers(3, 7)); M = rng.random((n, n)) * (rng.random((n, n)) < 0.6); M += np.roll(np.eye(n), 1, axis=1) * 0.05; M /= M.sum(1, keepdims=True)
    for r in range(1, n):
        O = list(range(r)); pire = max(pire, float(np.abs(np.linalg.eigvals(M[np.ix_(O, O)])).max())); nb += 1
out['C216_T5'] = dict(sous_ensembles_testes=nb, plus_grand_rayon_spectral_de_la_chaine_restreinte=pire, toujours_inferieur_a_1=pire < 1)
json.dump(out, open('c216c.json', 'w'), indent=1); print(json.dumps(out))
