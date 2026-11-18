#!/usr/bin/env python3
"""C-208c -- contre-calcul exact du << C-208 >> de ChatGPT (trois pieces logiques : chevauchement extrinseque, recollement intrinseque, non-unicite dynamique).
Prediction scellee avant calcul et avant lecture du rapport : c208c_prediction.txt. Claude, 18 novembre 2026. Usage : python3 c208c.py"""
import itertools, json, math
from fractions import Fraction as Fr
from collections import Counter
import numpy as np

def det3(a, b, c): return a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def vol6(P): return det3(sub(P[1], P[0]), sub(P[2], P[0]), sub(P[3], P[0]))
def bary(P, q):
    d = vol6(P); return [Fr(vol6([q if j == i else P[j] for j in range(4)]), d) for i in range(4)]
def compte(T):
    V = set(v for t in T for v in t); E = set(e for t in T for e in itertools.combinations(sorted(t), 2)); F = Counter(f for t in T for f in itertools.combinations(sorted(t), 3))
    return len(V), len(E), len(F), len(T), F

out = {}
# A
A, B = (Fr(0),)*3, (Fr(0), Fr(0), Fr(1)); xy = [(1,0),(0,1),(-1,0),(0,-1),(2,1),(-1,2),(-2,-1),(1,-2)]; p = [(Fr(x), Fr(y), Fr(0)) for x, y in xy]
pts = {'A': A, 'B': B, **{i: p[i] for i in range(8)}}; cells = [('A', 'B', i, (i+1) % 8) for i in range(8)]
dets = [vol6([pts[v] for v in c]) for c in cells]
ang = sum(math.atan2(xy[i][0]*xy[(i+1) % 8][1] - xy[i][1]*xy[(i+1) % 8][0], xy[i][0]*xy[(i+1) % 8][0] + xy[i][1]*xy[(i+1) % 8][1]) for i in range(8))
crois = [xy[i][0]*xy[(i+1) % 8][1] - xy[i][1]*xy[(i+1) % 8][0] for i in range(8)]
V, E, F, T, cf = compte([tuple(map(str, c)) for c in cells])
q = (Fr(1, 8), Fr(1, 8), Fr(1, 4)); dedans = [i for i, c in enumerate(cells) if all(b > 0 for b in bary([pts[v] for v in c], q))]
out['A'] = dict(determinants=[str(d) for d in dets], tous_positifs=all(d > 0 for d in dets), produits_croises_tous_positifs=all(c > 0 for c in crois), somme_angles_sur_pi=ang / math.pi,
                V=V, E=E, F=F, T=T, euler=V - E + F - T, faces_contenant_AB_toutes_doubles=all(n == 2 for f, n in cf.items() if 'A' in f and 'B' in f),
                cellules_contenant_q_strictement=dedans, barycentriques_q={i: [str(b) for b in bary([pts[v] for v in cells[i]], q)] for i in dedans})
# B
seq = [(0,1,2,3), (0,1,2,4), (0,1,3,4), (0,2,3,4)]; etapes = []
for k in range(1, 4):
    anc = set(f for t in seq[:k] for f in itertools.combinations(t, 3)); etapes.append(len(anc & set(itertools.combinations(seq[k], 3))))
V, E, F, T, cf = compte(seq); bord = sorted(f for f, n in cf.items() if n == 1)
ar_bord = set(e for f in bord for e in itertools.combinations(f, 2)); ar_int = sorted(set(e for t in seq for e in itertools.combinations(t, 2)) - ar_bord)
som_bord = set(v for f in bord for v in f)
G = np.array([[0.5 if i != j else 1.0 for j in range(4)] for i in range(4)])  # Gram des vecteurs issus d'un sommet, 5 points a distances mutuelles 1
out['B'] = dict(faces_communes_a_chaque_ajout=etapes, V=V, E=E, F=F, T=T, euler=V - E + F - T, faces_de_bord=bord, aretes_interieures=ar_int, sommets_interieurs=sorted(set(range(5)) - som_bord),
                graphe_complet_K5=(E == 10), quatre_simplexe_present=False, rang_Gram=int(np.linalg.matrix_rank(G)), det_Gram=float(np.linalg.det(G)),
                cellules_par_arete_interieure=[sum(1 for t in seq if set(e) <= set(t)) for e in ar_int], somme_diedres_degres=3 * math.degrees(math.acos(1 / 3)))
# C
def gen(a, b, c):
    Q = np.array([[-(a + b), a, b], [a, -(a + c), c], [b, c, -(b + c)]], float); return Q
r = {}
for nom, w in (('1_1_1', (1, 1, 1)), ('1_2_1', (1, 2, 1))):
    Q = gen(*w); pi = np.ones(3) / 3
    r[nom] = dict(symetrique=bool(np.allclose(Q, Q.T)), stationnaire=bool(np.allclose(pi @ Q, 0)), reversible=bool(np.allclose(pi[:, None] * Q, (pi[:, None] * Q).T)), spectre=sorted(np.linalg.eigvalsh(Q).round(12).tolist()))
out['C'] = r
json.dump(out, open('c208c.json', 'w'), indent=1); print(json.dumps(out, indent=1))
