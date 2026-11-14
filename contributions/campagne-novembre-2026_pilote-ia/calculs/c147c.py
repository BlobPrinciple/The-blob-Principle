#!/usr/bin/env python3
"""C-147c -- La loi en 1/r sort-elle de la trame ?  (Claude, 13 novembre 2026)

Protocole et predictions : c147c_prediction.txt (ecrit avant tout calcul).
Trame : etat de palier du tissu regulier de la mitose de l'arete = triangulation de Kuhn du reseau cubique.
Usage : python3 c147c.py   (ecrit c147c.json)
"""
import itertools
import json
import math
import pathlib
import sys
from fractions import Fraction as Fr

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import cg

ICI = pathlib.Path(__file__).resolve().parent
DIRS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]   # sept directions de Kuhn
bilan = {}


# ------------------------------------------------------------------ C0 : la regle genealogique donne bien cette trame
def controle_genealogique(generations=9):
    P = {0: (Fr(0), Fr(0), Fr(0)), 1: (Fr(1), Fr(0), Fr(0)), 2: (Fr(1), Fr(1), Fr(0)), 3: (Fr(1), Fr(1), Fr(1))}
    mid = {}

    def milieu(a, b):
        k = frozenset((a, b))
        if k not in mid:
            mid[k] = len(P)
            P[mid[k]] = tuple((P[a][i] + P[b][i]) / 2 for i in range(3))
        return mid[k]

    cells = [((0, 1, 2, 3), 3)]
    for _ in range(generations):
        new = []
        for x, d in cells:
            z = milieu(x[0], x[d])
            nd = d - 1 if d > 1 else 3
            new.append((x[:d] + (z,) + x[d + 1:], nd))
            new.append((x[1:d + 1] + (z,) + x[d + 1:], nd))
        cells = new
    h = Fr(1, 2 ** (generations // 3))
    permis = {tuple(s * c * h for c in d) for d in DIRS for s in (1, -1)}
    fils = {frozenset(p) for x, _ in cells for p in itertools.combinations(x, 2)}
    hors = sum(1 for f in fils for a, b in [tuple(f)] if tuple(P[b][i] - P[a][i] for i in range(3)) not in permis)
    return dict(generations=generations, cellules=len(cells), porteurs=len(P), fils=len(fils), fils_hors_des_sept_directions=hors)


bilan['C0'] = controle_genealogique()


# ------------------------------------------------------------------ outils de reseau
def laplacien(n, dirs, poids, mu=0.0):
    """Laplacien de graphe sur le cube n^3 (ou n^2 si dirs est plan), restreint a l'interieur (valeur nulle au bord)."""
    dim = len(dirs[0])
    grille = np.indices((n,) * dim).reshape(dim, -1).T
    idx = np.arange(n ** dim).reshape((n,) * dim)
    lig, col, val = [], [], []
    diag = np.zeros(n ** dim)
    for d, w in zip(dirs, poids):
        if w == 0:
            continue
        d = np.array(d)
        ok = np.all((grille + d >= 0) & (grille + d < n), axis=1)
        p = idx.reshape(-1)[ok]
        q = idx[tuple((grille[ok] + d).T)]
        lig += [p, q]
        col += [q, p]
        val += [np.full(len(p), -w), np.full(len(p), -w)]
        np.add.at(diag, p, w)
        np.add.at(diag, q, w)
    A = sp.coo_matrix((np.concatenate(val), (np.concatenate(lig), np.concatenate(col))), shape=(n ** dim,) * 2).tocsr()
    A = A + sp.diags(diag + mu)
    dedans = np.all((grille > 0) & (grille < n - 1), axis=1)
    return A[dedans][:, dedans], dedans, idx


def resous(A, b):
    M = sp.diags(1.0 / A.diagonal())
    x, info = cg(A, b, rtol=1e-11, atol=0.0, M=M, maxiter=20000)
    assert info == 0, info
    return x


def profil(n, dirs, poids, mu=0.0):
    dim = len(dirs[0])
    A, dedans, idx = laplacien(n, dirs, poids, mu)
    c = n // 2
    b = np.zeros(n ** dim)
    b[idx[(c,) * dim]] = 1.0
    u = np.zeros(n ** dim)
    u[dedans] = resous(A, b[dedans])
    res = np.abs(A @ u[dedans] - b[dedans]).max()
    return u.reshape((n,) * dim), c, res


def le_long(u, c, v, kmax):
    v = np.array(v)
    return np.array([u[tuple(c + k * v)] for k in range(0, kmax + 1)])


def estime(u, c, v):
    """Exposant p = log2[(u(r)-u(2r))/(u(2r)-u(4r))] et amplitude A = 2r(u(r)-u(2r)), r voisin de 4 a 6 mailles."""
    L = math.sqrt(sum(x * x for x in v))
    k = max(1, round(4 / L))
    s = le_long(u, c, v, 4 * k)
    p = math.log2((s[k] - s[2 * k]) / (s[2 * k] - s[4 * k]))
    amp = [2 * (j * L) * (s[j] - s[2 * j]) for j in range(k, 2 * k + 1)]
    return dict(r=k * L, exposant=p, amplitude=float(np.mean(amp)))


CINQ = {'axe (1,0,0)': (1, 0, 0), '(1,1,0)': (1, 1, 0), '(1,-1,0)': (1, -1, 0), '(1,1,1)': (1, 1, 1), '(1,-1,1)': (1, -1, 1)}
N = 65

# ------------------------------------------------------------------ CA : temoin analytique, reseau cubique simple
u7, c, res7 = profil(N, DIRS, [1, 1, 1, 0, 0, 0, 0])
bilan['CA_cubique_simple'] = dict(residu=res7, u0=float(u7[c, c, c]),
                                  quatre_pi_r_u={str(r): float(4 * math.pi * r * (u7[c + r, c, c] - u7[c + 2 * r, c, c]) * 2)
                                                 for r in (3, 4, 6, 8)},
                                  directions={k: estime(u7, c, v) for k, v in CINQ.items()})

# ------------------------------------------------------------------ P1 : quatorze fils, transmission egale
u14, c, res14 = profil(N, DIRS, [1] * 7)
d14 = {k: estime(u14, c, v) for k, v in CINQ.items()}
ref = d14['(1,-1,0)']['amplitude']
attendu = {'axe (1,0,0)': 1 / math.sqrt(0.75), '(1,1,0)': math.sqrt(2), '(1,-1,0)': 1.0, '(1,1,1)': 2.0, '(1,-1,1)': 1 / math.sqrt(11 / 12)}
for k in d14:
    d14[k]['rapport_a_(1,-1,0)'] = d14[k]['amplitude'] / ref
    d14[k]['rapport_attendu'] = attendu[k]
bilan['P1_quatorze_fils_sans_metrique'] = dict(residu=res14, directions=d14)

# ------------------------------------------------------------------ P2 : poids metriques (cotangentes, elements finis P1)
poids = {d: 0.0 for d in DIRS}
for perm in itertools.permutations(range(3)):
    V = [np.zeros(3)]
    for a in perm:
        e = np.zeros(3)
        e[a] = 1
        V.append(V[-1] + e)
    V = np.array(V)
    T = np.hstack([np.ones((4, 1)), V])
    G = np.linalg.inv(T)[1:, :].T              # gradients des coordonnees barycentriques
    vol = abs(np.linalg.det(T)) / 6
    for a, b in itertools.combinations(range(4), 2):
        d = tuple(int(round(x)) for x in V[b] - V[a])
        poids[d] += -vol * float(G[a] @ G[b])
bilan['P2_poids_metriques'] = {str(d): w for d, w in poids.items()}
um, c, resm = profil(N, DIRS, [poids[d] for d in DIRS])
dm = {k: estime(um, c, v) for k, v in CINQ.items()}
for k in dm:
    dm[k]['quatre_pi_A'] = 4 * math.pi * dm[k]['amplitude']
bilan['P2_profil_metrique'] = dict(residu=resm, directions=dm, ecart_max_au_cubique_simple=float(np.abs(um - u7).max()))

# ------------------------------------------------------------------ P3 : perte mu = 0,01 sur le reseau metrique
uy, c, resy = profil(N, DIRS, [poids[d] for d in DIRS], mu=0.01)
s = le_long(uy, c, (1, 0, 0), 24)
r = np.arange(6, 21)
pente = np.polyfit(r, np.log(r * s[6:21]), 1)[0]
bilan['P3_perte'] = dict(residu=resy, portee=-1 / pente, exposant_estime=estime(uy, c, (1, 0, 0))['exposant'])

# ------------------------------------------------------------------ CN : temoin negatif, trame plane triangulaire
u2, c2, res2 = profil(129, [(1, 0), (0, 1), (1, 1)], [1, 1, 1])
s2 = le_long(u2, c2, (1, 0), 16)
bilan['CN_plan'] = dict(residu=res2, exposant=math.log2((s2[4] - s2[8]) / (s2[8] - s2[16])),
                        difference_u4_u8=float(s2[4] - s2[8]), difference_u8_u16=float(s2[8] - s2[16]))

# ------------------------------------------------------------------ P4 : reseau de ressorts, centre de dilatation
def elastique(n):
    grille = np.indices((n, n, n)).reshape(3, -1).T
    idx = np.arange(n ** 3).reshape((n, n, n))
    lig, col, val = [], [], []
    for d in DIRS:
        d = np.array(d)
        nn = np.outer(d, d) / (d @ d)
        ok = np.all((grille + d >= 0) & (grille + d < n), axis=1)
        p = idx.reshape(-1)[ok]
        q = idx[tuple((grille[ok] + d).T)]
        for a in range(3):
            for b in range(3):
                w = nn[a, b]
                if w == 0:
                    continue
                for (i, j, sg) in ((p, p, 1), (q, q, 1), (p, q, -1), (q, p, -1)):
                    lig.append(3 * i + a)
                    col.append(3 * j + b)
                    val.append(np.full(len(i), sg * w))
    K = sp.coo_matrix((np.concatenate(val), (np.concatenate(lig), np.concatenate(col))), shape=(3 * n ** 3,) * 2).tocsr()
    dedans = np.repeat(np.all((grille > 0) & (grille < n - 1), axis=1), 3)
    c = n // 2
    F = np.zeros(3 * n ** 3)
    for d in DIRS:
        for sg in (1, -1):
            q = idx[tuple(c + sg * np.array(d))]
            F[3 * q:3 * q + 3] += sg * np.array(d) / math.sqrt(sum(x * x for x in d))     # poussee radiale, somme et moment nuls
    Kd = K[dedans][:, dedans]
    u = np.zeros(3 * n ** 3)
    u[dedans] = resous(Kd, F[dedans])
    res = np.abs(Kd @ u[dedans] - F[dedans]).max()
    return u.reshape(n, n, n, 3), c, res


ue, ce, rese = elastique(41)
ur = np.array([ue[ce + k, ce, ce, 0] for k in range(0, 17)])              # deplacement radial le long de l'axe
al = ur[1:] - ur[:-1]                                                    # allongement du fil radial entre k et k+1
ud = np.array([ue[ce + k, ce + k, ce + k] @ np.ones(3) / math.sqrt(3) for k in range(0, 9)])
bilan['P4_elastique'] = dict(residu=rese,
                             deplacement_axe={str(k): float(ur[k]) for k in (2, 3, 4, 6, 8, 12)},
                             q_axe_3_6=math.log2(ur[3] / ur[6]), q_axe_4_8=math.log2(ur[4] / ur[8]),
                             q_diagonale_2_4=math.log2(ud[2] / ud[4]),
                             allongement_axe={str(k): float(al[k]) for k in (2, 3, 4, 6, 8)},
                             s_axe_3_6=math.log2(al[3] / al[6]), s_axe_4_8=math.log2(al[4] / al[8]))

(ICI / 'c147c.json').write_text(json.dumps(bilan, indent=1, ensure_ascii=False, default=float))
json.dump(bilan, sys.stdout, indent=1, ensure_ascii=False, default=float)
print()
