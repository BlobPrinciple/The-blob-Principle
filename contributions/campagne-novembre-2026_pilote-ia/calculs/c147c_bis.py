#!/usr/bin/env python3
"""C-147c bis -- la loi en 1/r sur la VRAIE trame de palier du tissu regulier (Claude, 13 novembre 2026).

Le controle C0 de c147c.py a echoue : la trame de palier n'est pas le reseau de Kuhn. Ici les fils sont releves
sur les cellules produites par la regle genealogique de C-136c, puis etendus a un cube par la regle de parite.
Predictions : c147c_bis_prediction.txt (ecrit avant ce calcul).
Usage : python3 c147c_bis.py   (ecrit c147c_bis.json)
"""
import itertools
import json
import math
import pathlib
import sys

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import cg

ICI = pathlib.Path(__file__).resolve().parent
bilan = {}

# ------------------------------------------------------------------ la trame, par la regle genealogique (entiers)
K = 4                                   # paliers : generation 3K = 12, maille 1, cote 2^K = 16
S = 2 ** K
P = {0: (0, 0, 0), 1: (S, 0, 0), 2: (S, S, 0), 3: (S, S, S)}
mid = {}


def milieu(a, b):
    k = frozenset((a, b))
    if k not in mid:
        mid[k] = len(P)
        P[mid[k]] = tuple((P[a][i] + P[b][i]) // 2 for i in range(3))
    return mid[k]


cells = [((0, 1, 2, 3), 3)]
for _ in range(3 * K):
    new = []
    for x, d in cells:
        z = milieu(x[0], x[d])
        nd = d - 1 if d > 1 else 3
        new.append((x[:d] + (z,) + x[d + 1:], nd))
        new.append((x[1:d + 1] + (z,) + x[d + 1:], nd))
    cells = new
cells = [x for x, _ in cells]
fils = {frozenset(p) for x in cells for p in itertools.combinations(x, 2)}
vois = {}
for f in fils:
    a, b = tuple(f)
    vois.setdefault(a, set()).add(tuple(P[b][i] - P[a][i] for i in range(3)))
    vois.setdefault(b, set()).add(tuple(P[a][i] - P[b][i] for i in range(3)))


def interieur(p):
    x, y, z = p
    return z >= 2 and y - z >= 2 and x - y >= 2 and x <= S - 2


classes = {}
incoherent = 0
for v, p in P.items():
    if interieur(p):
        c = tuple(q % 2 for q in p)
        if c in classes and classes[c] != vois[v]:
            incoherent += 1
        classes.setdefault(c, vois[v])
recip = all(tuple(-x for x in d) in classes[tuple((c[i] + d[i]) % 2 for i in range(3))] for c, D in classes.items() for d in D)
bilan['B0_trame'] = dict(cellules=len(cells), porteurs=len(P), fils=len(fils), classes_trouvees=len(classes),
                         porteurs_incoherents=incoherent, reciprocite=recip,
                         fils_par_porteur={str(c): len(D) for c, D in sorted(classes.items())},
                         longueurs_au_carre={str(c): sorted({sum(x * x for x in d) for d in D}) for c, D in sorted(classes.items())})

# poids metriques releves sur les cellules reelles (elements finis P1 = formule des cotangentes)
poids = {}
for x in cells:
    V = np.array([P[v] for v in x], float)
    T = np.hstack([np.ones((4, 1)), V])
    G = np.linalg.inv(T)[1:, :].T
    vol = abs(np.linalg.det(T)) / 6
    for a, b in itertools.combinations(range(4), 2):
        k = frozenset((x[a], x[b]))
        poids[k] = poids.get(k, 0.0) - vol * float(G[a] @ G[b])
wm = {}
for f, w in poids.items():
    a, b = tuple(f)
    if interieur(P[a]) and interieur(P[b]):
        d2 = sum((P[a][i] - P[b][i]) ** 2 for i in range(3))
        wm.setdefault(d2, []).append(w)
bilan['B2_poids_metriques'] = {f'longueur_au_carre_{d2}': dict(n=len(v), min=min(v), max=max(v)) for d2, v in sorted(wm.items())}


# ------------------------------------------------------------------ extension au cube par la regle de parite
def aretes(n):
    grille = np.indices((n, n, n)).reshape(3, -1).T
    idx = np.arange(n ** 3).reshape((n, n, n))
    par = grille % 2
    A, B, D = [], [], []
    for c, dirs in classes.items():
        m = np.all(par == np.array(c), axis=1)
        for d in dirs:
            if d <= (0, 0, 0):
                continue                                    # chaque fil une seule fois
            dd = np.array(d)
            ok = m & np.all((grille + dd >= 0) & (grille + dd < n), axis=1)
            A.append(idx.reshape(-1)[ok])
            B.append(idx[tuple((grille[ok] + dd).T)])
            D.append(np.tile(dd, (ok.sum(), 1)))
    return np.concatenate(A), np.concatenate(B), np.concatenate(D), grille, idx


def resous(M, b):
    x, info = cg(M, b, rtol=1e-11, atol=0.0, M=sp.diags(1.0 / M.diagonal()), maxiter=40000)
    assert info == 0, info
    return x


def le_long(u, c, v, kmax):
    v = np.array(v)
    return np.array([u[tuple(c + k * v)] for k in range(0, kmax + 1)])


def estime(u, c, v):
    L = math.sqrt(sum(x * x for x in v))
    k = max(1, round(4 / L))
    k += k % 2                                             # pas pair : on compare des porteurs de meme classe
    s = le_long(u, c, v, 4 * k)
    return dict(r=k * L, exposant=math.log2((s[k] - s[2 * k]) / (s[2 * k] - s[4 * k])), amplitude=2 * k * L * (s[k] - s[2 * k]),
                amplitude_a_2r=4 * k * L * (s[2 * k] - s[4 * k]))


CINQ = {'axe (1,0,0)': (1, 0, 0), '(1,1,0)': (1, 1, 0), '(1,-1,0)': (1, -1, 0), '(1,1,1)': (1, 1, 1), '(1,-1,1)': (1, -1, 1)}

# B1 : transmission egale sur tous les fils
n = 65
a, b, d, grille, idx = aretes(n)
N = n ** 3
L = sp.coo_matrix((np.concatenate([-np.ones(len(a)), -np.ones(len(a))]), (np.concatenate([a, b]), np.concatenate([b, a]))), shape=(N, N)).tocsr()
deg = np.asarray(-L.sum(axis=1)).ravel()
L = L + sp.diags(deg)
dedans = np.all((grille > 0) & (grille < n - 1), axis=1)
Ld = L[dedans][:, dedans]
res = {}
for nom, centre in (('centre de classe (0,0,0)', 32), ('centre de classe (1,1,1)', 31)):
    rhs = np.zeros(N)
    rhs[idx[centre, centre, centre]] = 1.0
    u = np.zeros(N)
    u[dedans] = resous(Ld, rhs[dedans])
    u3 = u.reshape(n, n, n)
    dd = {k: estime(u3, centre, v) for k, v in CINQ.items()}
    ref = dd['(1,-1,0)']['amplitude']
    for k in dd:
        dd[k]['rapport_a_(1,-1,0)'] = dd[k]['amplitude'] / ref
    res[nom] = dict(fils_du_centre=int(deg[idx[centre, centre, centre]]), residu=float(np.abs(Ld @ u[dedans] - rhs[dedans]).max()), directions=dd)
bilan['B1_tous_les_fils_sans_metrique'] = res
bilan['B1_degres'] = {str(int(k)): int(v) for k, v in zip(*np.unique(deg[dedans], return_counts=True))}

# ---- AJOUTS APRES COUP (hors predictions ; declares) ----------------------------------------------------------
# (i) source sur un porteur a dix fils ; (ii) profil avec les poids metriques reels, qui ne sont PAS egaux
#     sur les fils d'axe (2/3, 1, 4/3) : la prediction B2 "reseau cubique simple" etait fausse sur ce point.
def estime_v(u3, cv, v):
    Lv = math.sqrt(sum(x * x for x in v))
    k = max(1, round(4 / Lv))
    k += k % 2
    cv, v = np.array(cv), np.array(v)
    sv = np.array([u3[tuple(cv + j * v)] for j in range(0, 4 * k + 1)])
    return dict(r=k * Lv, exposant=math.log2((sv[k] - sv[2 * k]) / (sv[2 * k] - sv[4 * k])), amplitude=2 * k * Lv * (sv[k] - sv[2 * k]),
                amplitude_a_2r=4 * k * Lv * (sv[2 * k] - sv[4 * k]))


def profils(Lmat, centre):
    rhs = np.zeros(N)
    rhs[idx[tuple(centre)]] = 1.0
    uu = np.zeros(N)
    uu[dedans] = resous(Lmat, rhs[dedans])
    u3 = uu.reshape(n, n, n)
    dd = {k: estime_v(u3, centre, v) for k, v in CINQ.items()}
    ref = dd['(1,-1,0)']['amplitude']
    for k in dd:
        dd[k]['rapport_a_(1,-1,0)'] = dd[k]['amplitude'] / ref
        dd[k]['quatre_pi_A'] = 4 * math.pi * dd[k]['amplitude']
    return dd


bilan['ajout_source_a_dix_fils'] = dict(fils_du_centre=int(deg[idx[33, 32, 32]]), directions=profils(Ld, (33, 32, 32)))
wk = {}
incoh = 0
for f, w in poids.items():
    pa, pb = (P[v] for v in tuple(f))
    if not (interieur(pa) and interieur(pb)):
        continue
    dv = tuple(pb[i] - pa[i] for i in range(3))
    if sum(x * x for x in dv) != 1:
        continue
    if dv < (0, 0, 0):
        pa, pb, dv = pb, pa, tuple(-x for x in dv)
    key = (tuple(q % 2 for q in pa), dv)
    if key in wk and abs(wk[key] - w) > 1e-12:
        incoh += 1
    wk[key] = w
A2, B2, W2 = [], [], []
par = grille % 2
for (c, dv), w in wk.items():
    dd_ = np.array(dv)
    ok = np.all(par == np.array(c), axis=1) & np.all((grille + dd_ >= 0) & (grille + dd_ < n), axis=1)
    A2.append(idx.reshape(-1)[ok])
    B2.append(idx[tuple((grille[ok] + dd_).T)])
    W2.append(np.full(ok.sum(), w))
A2, B2, W2 = np.concatenate(A2), np.concatenate(B2), np.concatenate(W2)
Lm = sp.coo_matrix((np.concatenate([-W2, -W2]), (np.concatenate([A2, B2]), np.concatenate([B2, A2]))), shape=(N, N)).tocsr()
Lm = (Lm + sp.diags(np.asarray(-Lm.sum(axis=1)).ravel()))[dedans][:, dedans]
bilan['ajout_poids_metriques_reels'] = dict(cles=len(wk), incoherences=incoh,
                                            valeurs={str(k): int(v) for k, v in zip(*np.unique(np.round(list(wk.values()), 6), return_counts=True))},
                                            centre_000=profils(Lm, (32, 32, 32)), centre_100=profils(Lm, (33, 32, 32)))

# B4 : ressorts egaux sur tous les fils, centre de dilatation
n = 41
a, b, d, grille, idx = aretes(n)
N = n ** 3
lig, col, val = [], [], []
nn = d[:, :, None] * d[:, None, :] / (d * d).sum(axis=1)[:, None, None]
for i in range(3):
    for j in range(3):
        w = nn[:, i, j]
        for (p, q, sg) in ((a, a, 1), (b, b, 1), (a, b, -1), (b, a, -1)):
            lig.append(3 * p + i)
            col.append(3 * q + j)
            val.append(sg * w)
Kmat = sp.coo_matrix((np.concatenate(val), (np.concatenate(lig), np.concatenate(col))), shape=(3 * N, 3 * N)).tocsr()
dedans = np.repeat(np.all((grille > 0) & (grille < n - 1), axis=1), 3)
c = 20                                                     # centre de classe (0,0,0)
F = np.zeros(3 * N)
for dv in classes[(0, 0, 0)]:
    q = idx[tuple(c + np.array(dv))]
    F[3 * q:3 * q + 3] += np.array(dv) / math.sqrt(sum(x * x for x in dv))
Kd = Kmat[dedans][:, dedans]
ue = np.zeros(3 * N)
ue[dedans] = resous(Kd, F[dedans])
ue3 = ue.reshape(n, n, n, 3)
ur = np.array([ue3[c + k, c, c, 0] for k in range(0, 17)])
al = ur[2:] - ur[:-2]                                      # allongement sur deux mailles, de k a k+2
bilan['B4_elastique'] = dict(residu=float(np.abs(Kd @ ue[dedans] - F[dedans]).max()), somme_des_forces=[float(x) for x in F.reshape(-1, 3).sum(axis=0)],
                             deplacement_axe={str(k): float(ur[k]) for k in (2, 4, 6, 8, 12)},
                             q_axe_4_8=math.log2(ur[4] / ur[8]), q_axe_6_12=math.log2(ur[6] / ur[12]),
                             allongement_axe={str(k): float(al[k]) for k in (2, 4, 6, 8)},
                             s_axe_4_8=math.log2(al[4] / al[8]), s_axe_2_4=math.log2(al[2] / al[4]))

(ICI / 'c147c_bis.json').write_text(json.dumps(bilan, indent=1, ensure_ascii=False, default=float))
json.dump(bilan, sys.stdout, indent=1, ensure_ascii=False, default=float)
print()
