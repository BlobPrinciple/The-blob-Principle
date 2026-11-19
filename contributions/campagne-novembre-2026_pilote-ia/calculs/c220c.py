#!/usr/bin/env python3
"""C-219c, C-220c, C-221c -- contre-calculs des notes C-219 (bipyramide : deux decoupages), C-220 (orientation des tetraedres, developpement de l'operateur) et
C-221 (ordre de naissance) de ChatGPT. Prediction scellee avant calcul : c220c_prediction.txt. Ecrit sans ouvrir ses programmes. Claude, 19 novembre 2026."""
import itertools, json, math
from fractions import Fraction as F
import numpy as np
from scipy.spatial import Delaunay
out = {}
r3 = math.sqrt(3)
Tp = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]; Tm = [tuple(-x for x in v) for v in Tp]
R = lambda v: (-v[1], v[0], v[2])
img = [R(v) for v in Tp]; perm = [Tp.index(tuple(-x for x in w)) for w in img]      # -R : T+ -> T+
def signe(p):
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]: s = -s
    return s
def det3(a, b, c): return a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])
def D(V): return det3(*[tuple(V[i][k] - V[0][k] for k in range(3)) for i in (1, 2, 3)])
cov = lambda T: [[F(sum(v[i] * v[j] for v in T), 3) for j in range(3)] for i in range(3)]
out['C220'] = dict(R_envoie_Tplus_sur_Tmoins=sorted(img) == sorted(Tm), permutation_de_moins_R=perm, signature=signe(perm),
                   somme_vvT_Tplus=[[str(x) for x in l] for l in cov(Tp)], somme_vvT_Tmoins=[[str(x) for x in l] for l in cov(Tm)],
                   D_Tplus=D(Tp), D_Tmoins=D(Tm), D_apres_echange_de_deux_etiquettes=D([Tp[1], Tp[0], Tp[2], Tp[3]]))
U = np.array(Tp, float) / r3
def symbole(k, h, eps): return complex((3 / (2 * h * h)) * sum((1 + eps) / 2 * np.exp(1j * h * (v @ k)) + (1 - eps) / 2 * np.exp(-1j * h * (v @ k)) - 1 for v in U))
lig = []
for eps in (0.0, 0.3, 1.0):
    for h in (0.4, 0.2, 0.1, 0.05, 0.025):
        ld = symbole(np.ones(3) / r3, h, eps); la = symbole(np.array([1., 0, 0]), h, eps)
        lig.append(dict(eps=eps, h=h, reel_diag_moins_axe_sur_h2=(ld.real - la.real) / h ** 2, imag_diag_sur_h=ld.imag / h, imag_axe=la.imag, reel_axe_plus_1_sur_h2=(la.real + 1) / h ** 2))
out['C220']['symboles'] = lig; out['C220']['attendus'] = dict(un_sur_27=1 / 27, moins_2_eps_sur_9='-(2/9) eps', un_sur_36=1 / 36)
# C-221
dets = [D([Tp[i] for i in p]) for p in itertools.permutations(range(4))]
out['C221'] = dict(ordres=len(dets), positifs=sum(d > 0 for d in dets), negatifs=sum(d < 0 for d in dets), valeurs_absolues=sorted(set(abs(d) for d in dets)), signe_egal_signature=all((d > 0) == (signe(p) * dets[0] > 0) for d, p in zip(dets, itertools.permutations(range(4)))),
                   p_couple_fort=1 - math.exp(-2), p_couple_faible=1 - math.exp(-0.5))
# C-219
def vol6(P): return abs(det3(*[tuple(P[i][k] - P[0][k] for k in range(3)) for i in (1, 2, 3)]))
c, d, e = (F(1), F(0), F(0)), (F(-1, 2), F(1), F(0)), (F(-1, 2), F(-1), F(0))
res = []
for za, zb in ((F(1), F(-1)), (F(1), F(-3)), (F(1, 2), F(-1, 3))):
    a, b = (F(0), F(0), za), (F(0), F(0), zb)
    v2 = vol6([a, c, d, e]) + vol6([b, c, d, e]); v3 = vol6([a, b, c, d]) + vol6([a, b, d, e]) + vol6([a, b, e, c])
    pts = np.array([[float(x) for x in p] for p in (a, b, c, d, e)]); nt = len(Delaunay(pts, qhull_options='QJ').simplices)
    res.append(dict(za=str(za), zb=str(zb), six_fois_volume_decoupage_en_2=str(v2), six_fois_volume_decoupage_en_3=str(v3), egaux=(v2 == v3), cellules_retenues_par_Delaunay=nt))
out['C219'] = dict(cas=res, liens_du_decoupage_en_2=9, liens_du_decoupage_en_3=10)
json.dump(out, open('c220c.json', 'w'), indent=1); print(json.dumps(out))
