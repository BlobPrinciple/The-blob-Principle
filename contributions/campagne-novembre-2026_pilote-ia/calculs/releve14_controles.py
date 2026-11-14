#!/usr/bin/env python3
"""Releve du 14 novembre -- controles rapides et exacts des treize dossiers de ChatGPT (13 et 14 novembre 2026).  (Claude)

Attendus : releve14_prediction.txt (ecrit avant tout programme). Ne recoupe PAS ses simulations : seulement ses enonces exacts.
Reprend les programmes du laboratoire c147c_bis.py (trame de palier) et c148c.py (croissance), cherches a cote de ce fichier.
Usage : python3 releve14_controles.py   (ecrit releve14_controles.json)
"""
import itertools
import json
import math
import pathlib
import random
import sys
from fractions import Fraction as Fr

import numpy as np

ICI = pathlib.Path(__file__).resolve().parent


def source(nom):
    for d in (ICI, ICI.parent / 'c147'):
        if (d / nom).exists():
            return (d / nom).read_text()
    raise FileNotFoundError(nom)


R = {}

# ------------------------------------------------------------------ K1 : deux tetraedres reguliers colles par une face
A, B, C = np.array([0, 0, 0.0]), np.array([1, 0, 0.0]), np.array([0.5, math.sqrt(3) / 2, 0])
G = (A + B + C) / 3
h = math.sqrt(1 - G @ G)
D, E = G + np.array([0, 0, h]), G - np.array([0, 0, h])
R['K1'] = dict(DE=float(np.linalg.norm(D - E)), racine_8_tiers=math.sqrt(8 / 3), aretes_unite=all(
    abs(np.linalg.norm(p - q) - 1) < 1e-12 for p in (D, E) for q in (A, B, C)), contacts_du_cinquieme=sum(
    np.linalg.norm(E - q) <= 1.15 for q in (A, B, C, D)))


# ------------------------------------------------------------------ K2 : division d'un sommet, heritage des voisins
def cycles(n, ar):
    return len(ar) - n + 1


def divisions(n, ar):
    """Toutes les divisions d'un graphe (sommets 0..n-1, aretes = frozenset de paires) : (probabilite en p, graphe, voisins partages)."""
    for v in range(n):
        vois = [u for u in range(n) if frozenset((u, v)) in ar]
        for choix in itertools.product((0, 1, 2), repeat=len(vois)):          # 0 : reste a v ; 1 : passe a la fille ; 2 : les deux
            new = set(a for a in ar if v not in a)
            new.add(frozenset((v, n)))
            for u, c in zip(vois, choix):
                if c in (0, 2):
                    new.add(frozenset((u, v)))
                if c in (1, 2):
                    new.add(frozenset((u, n)))
            s = sum(c == 2 for c in choix)
            yield v, len(vois), s, frozenset(new)


def classe(n, ar):
    return tuple(sorted(sum(1 for a in ar if v in a) for v in range(n))), len(ar)


exceptions, histoires = 0, 0
niveau = {frozenset([frozenset((0, 1))]): None}
atteints = {2: set(niveau)}
for n in (2, 3, 4):
    suiv = set()
    for ar in atteints[n]:
        for v, k, s, new in divisions(n, ar):
            histoires += 1
            if cycles(n + 1, new) != cycles(n, ar) + s:
                exceptions += 1
            suiv.add(new)
    atteints[n + 1] = suiv


def proba_K4(p):
    """Probabilite exacte d'obtenir K4 a N = 4 : sommet tire uniformement, chaque voisin partage avec probabilite p, sinon une fille (1/2, 1/2)."""
    etats = {frozenset([frozenset((0, 1))]): Fr(1)}
    for n in (2, 3):
        nouv = {}
        for ar, pr in etats.items():
            for v, k, s, new in divisions(n, ar):
                w = pr * Fr(1, n) * (p ** s) * (((1 - p) / 2) ** (k - s))
                nouv[new] = nouv.get(new, 0) + w
        etats = nouv
    assert sum(etats.values()) == 1
    return sum(pr for ar, pr in etats.items() if len(ar) == 6)


R['K2'] = dict(histoires_examinees=histoires, exceptions_a_la_loi_des_cycles=exceptions,
               graphes_etiquetes_atteints={str(n): len(v) for n, v in atteints.items()},
               classes_d_isomorphie_a_N4=len({classe(4, ar) for ar in atteints[4]}),
               P_K4={str(p): [str(proba_K4(p)), str(p ** 3)] for p in (Fr(1, 2), Fr(1, 3), Fr(7, 10))})

# ------------------------------------------------------------------ K3 : cube de Kuhn de cote 5, frontiere et cycles
L = 5
tets = []
for o in itertools.product(range(L), repeat=3):
    for perm in itertools.permutations(range(3)):
        v = [tuple(o)]
        for a in perm:
            w = list(v[-1])
            w[a] += 1
            v.append(tuple(w))
        tets.append(tuple(v))
faces = {}
for i, t in enumerate(tets):
    for f in itertools.combinations(t, 3):
        faces.setdefault(frozenset(f), []).append(i)
front = sum(1 for v in faces.values() if len(v) == 1)
internes = sum(1 for v in faces.values() if len(v) == 2)
r = internes - len(tets) + 1
R['K3'] = dict(tetraedres=len(tets), faces_de_frontiere=front, faces_partagees=internes, cycles_du_dual=r,
               formule=2 * len(tets) + 2 - 2 * r, faces_a_plus_de_deux=sum(1 for v in faces.values() if len(v) > 2))


# ------------------------------------------------------------------ K4 : six coupes d'un tetraedre colle a un voisin
def aire(tri):
    (a, b, c) = tri
    u = [b[i] - a[i] for i in range(3)]
    v = [c[i] - a[i] for i in range(3)]
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    return Fr(sum(x * x for x in n), 4)                       # carre de l'aire


def volume(t):
    a, b, c, d = t
    m = [[x[i] - a[i] for i in range(3)] for x in (b, c, d)]
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
           + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    return abs(Fr(det, 6))


P = dict(A=(Fr(0), Fr(0), Fr(0)), B=(Fr(1), Fr(0), Fr(0)), C=(Fr(0), Fr(1), Fr(0)), D=(Fr(0), Fr(0), Fr(1)))
k4 = {}
for x, y in itertools.combinations('ABCD', 2):
    M = tuple((P[x][i] + P[y][i]) / 2 for i in range(3))
    filles = [[P[s] for s in 'ABCD' if s != x] + [M], [P[s] for s in 'ABCD' if s != y] + [M]]
    contacts, aires = 1, []                                    # les deux filles se touchent par la face de coupe
    for f in filles:
        bas = [q for q in f if q[2] == 0]                      # face dans le plan de ABC, partagee avec le voisin ABCE
        if len(bas) == 3 and aire(bas) > 0:
            contacts += 1
            aires.append(str(aire(bas)))
    k4[x + y] = dict(contacts=contacts, cycles=contacts - 3 + 1, carres_des_aires_de_contact=aires, volumes=[str(volume(f)) for f in filles])
fam = {}
for m in range(1, 7):
    pts = [(Fr(i, m), Fr(0), Fr(0)) for i in range(m + 1)]
    cell = [(pts[i], pts[i + 1], P['C'], P['D']) for i in range(m)] + [(pts[i], pts[i + 1], P['C'], (Fr(0), Fr(0), Fr(-1))) for i in range(m)]
    fa = {}
    for i, t in enumerate(cell):
        for f in itertools.combinations(t, 3):
            fa.setdefault(frozenset(f), []).append(i)
    c = sum(1 for v in fa.values() if len(v) == 2)
    fam[str(m)] = dict(N=len(cell), contacts=c, cycles=c - len(cell) + 1, faces_exterieures=sum(1 for v in fa.values() if len(v) == 1),
                       volume=str(sum(volume(t) for t in cell)))
R['K4'] = dict(six_coupes=k4, famille=fam)

# ------------------------------------------------------------------ K5 : six orthoschemes de Kuhn ; defaut diedre
ortho = []
for perm in itertools.permutations(range(3)):
    v = [(Fr(0), Fr(0), Fr(0))]
    for a in perm:
        w = list(v[-1])
        w[a] += 1
        v.append(tuple(w))
    ortho.append(tuple(v))
fa = {}
for i, t in enumerate(ortho):
    for f in itertools.combinations(t, 3):
        fa.setdefault(frozenset(f), []).append(i)
adj = {i: set() for i in range(6)}
for v in fa.values():
    if len(v) == 2:
        adj[v[0]].add(v[1])
        adj[v[1]].add(v[0])
vu, pile = {0}, [0]
while pile:
    for j in adj[pile.pop()]:
        if j not in vu:
            vu.add(j)
            pile.append(j)
R['K5'] = dict(volumes=[str(volume(t)) for t in ortho], somme=str(sum(volume(t) for t in ortho)), degres=[len(adj[i]) for i in range(6)],
               connexe=len(vu) == 6, defaut_diedre_degres=360 - 5 * math.degrees(math.acos(1 / 3)))

# ------------------------------------------------------------------ K6 : genealogie par division
rng = random.Random(20261114)
parent, feuilles, suivant = {0: None}, [0], 1
while len(feuilles) < 2048:
    c = feuilles.pop(rng.randrange(len(feuilles)))
    for _ in range(2):
        parent[suivant] = c
        feuilles.append(suivant)
        suivant += 1


def lignee(x):
    out = []
    while x is not None:
        out.append(x)
        x = parent[x]
    return out


prof = {x: len(lignee(x)) - 1 for x in parent}
exc = 0
for _ in range(2000):
    d = rng.choice(feuilles)
    li = lignee(d)
    a = rng.choice(li)
    inter = li[:li.index(a) + 1]                               # tout x avec a <= x <= d est sur la lignee de d
    exc += any(not (x in lignee(y) or y in lignee(x)) for x in inter for y in inter)
n_ev = len(parent)
R['K6'] = dict(cellules=n_ev, feuilles=len(feuilles), intervalles_testes=2000, exceptions=exc,
               fraction_de_paires_comparables=sum(prof.values()) / (n_ev * (n_ev - 1) / 2))

# ------------------------------------------------------------------ K7, K8 : nombres
c_l, MPC = 299792458.0, 3.0856775814913673e22
H0 = 70e3 / MPC
saut = c_l / (3 * H0)


def moments(vecs):
    v = np.array(vecs, float)
    return dict(x4=float((v[:, 0] ** 4).sum()), x2y2=float((v[:, 0] ** 2 * v[:, 1] ** 2).sum()), x6=float((v[:, 0] ** 6).sum()),
                x4y2=float((v[:, 0] ** 4 * v[:, 1] ** 2).sum()), x2y2z2=float((v[:, 0] ** 2 * v[:, 1] ** 2 * v[:, 2] ** 2).sum()))


tous = [d for d in itertools.product((-1, 0, 1), repeat=3) if any(d)]
coq = {k: moments([d for d in tous if sum(x * x for x in d) == k]) for k in (1, 2, 3)}
# conditions d'isotropie : x4 = 3 x2y2 (ordre 4) ; x6 = 5 x4y2 et x4y2 = 3 x2y2z2 (ordre 6)
Mx = np.array([[coq[k]['x4'] - 3 * coq[k]['x2y2'] for k in (1, 2, 3)],
               [coq[k]['x6'] - 5 * coq[k]['x4y2'] for k in (1, 2, 3)],
               [coq[k]['x4y2'] - 3 * coq[k]['x2y2z2'] for k in (1, 2, 3)]])
iso18 = Mx @ np.array([2.0, 1.0, 0.0])
R['K7'] = dict(poisson_au_moins_8=1 - sum(math.exp(-1) / math.factorial(k) for k in range(8)), boule_carree_rayon_10=2 * 100 + 2 * 10 + 1,
               chemin_40_pas=2 * 40 + 1)
R['K8'] = dict(saut_m=saut, saut_Gpc=saut / MPC / 1e3, rapport_femtometre=saut / 1e-15, matrice=Mx.tolist(), determinant=float(np.linalg.det(Mx)),
               reseau_18_voisins=dict(ordre_4=float(iso18[0]), ordre_6=[float(iso18[1]), float(iso18[2])]))

# ------------------------------------------------------------------ K9 : identite de GR-1 sur ma propre integration (c148c.py)
exec(source('c148c.py').split('# ------------------------------------------------------------------ P6')[0], globals())
Bq = 0.375
f0 = croissance(Bq)[2]


def f_en(x, Bv):
    from scipy.integrate import solve_ivp as _s
    Om_a = lambda u: OM * math.exp(-3 * u) / (1 - OM + OM * math.exp(-3 * u))
    sol = _s(lambda u, y: [y[1], -y[1] * y[1] - (-1.5 * Om_a(u) + 6 * Bv) * y[1] + 4.5 * (1 - 2 * Bv) * Om_a(u)], (math.log(1e-3), x), [0.0, 3 - 6 * Bv],
             rtol=1e-11, atol=1e-13, method='DOP853')
    return float(sol.y[1, -1])


hh = 1e-3
fp = (f_en(hh, Bq) - f_en(-hh, Bq)) / (2 * hh)
gauche = fp + f0 * f0 + (2 - 1.5 * OM) * f0 - 1.5 * OM
R['K9'] = dict(Omega_m=OM, f_aujourdhui_B_0_375=f0, premier_membre=gauche, second_membre=(1 - 3 * Bq) * (2 * f0 + 3 * OM),
               f_aujourdhui_B_un_tiers=croissance(1 / 3)[2],
               rayonnement_sans_pression=1 - (8 + 4) / (8 + 8), kasner_sans_cisaillement=1 - (1 / 3) / 1)

# ------------------------------------------------------------------ K10, K11, K12 : la trame de C-147c (reconstruite par c147c_bis.py)
exec(source('c147c_bis.py').split('# B1 : transmission egale sur tous les fils')[0], globals())
cl = {}
S64 = np.zeros((3, 3))
m4 = dict(x4=0.0, x2y2=0.0)
for cpar, dirs in sorted(classes.items()):
    v = np.array(sorted(dirs), float)
    T = v.T @ v
    S64 += T
    m4['x4'] += float((v[:, 0] ** 4).sum())
    m4['x2y2'] += float((v[:, 0] ** 2 * v[:, 1] ** 2).sum())
    cl[str(cpar)] = dict(fils=len(dirs), moments=np.diag(T).tolist(), hors_diagonale=float(np.abs(T - np.diag(np.diag(T))).max()))
deg = sum(len(d) for d in classes.values()) / 8
GMs, Rs = 1.32712440018e20, 6.957e8
dev = 4 * GMs / (c_l ** 2 * Rs) * 180 / math.pi * 3600
R['K10'] = dict(classes=cl, somme_des_moments=np.diag(S64).tolist(), degre_moyen=deg, diffusivite_conductance_unite=float(S64[0, 0] / 8 / 2),
                diffusivite_marche_normalisee=float(S64[0, 0] / 8 / 2 / deg), deviation_solaire_gamma_1=dev, deviation_solaire_gamma_0=dev / 2)
R['K12'] = dict(somme_x4_par_porteur=m4['x4'] / 8, somme_x2y2_par_porteur=m4['x2y2'] / 8, rapport=m4['x4'] / m4['x2y2'], rapport_isotrope=3.0)

n = 6
ed = []
for o in itertools.product(range(n), repeat=3):
    for d in classes[tuple(q % 2 for q in o)]:
        if d > (0, 0, 0):
            ed.append(d)
ed = np.array(ed, float)
Nn = n ** 3
r2 = (ed ** 2).sum(1)


def energie(t, F):
    """Energie elastique par porteur sous deformation affine F, longueurs naturelles r0 = (1 - t) r."""
    rr = np.sqrt(((ed @ F.T) ** 2).sum(1))
    return float((0.5 * (rr - (1 - t) * np.sqrt(r2)) ** 2).sum() / Nn)


k11 = {}
for t in (-0.5, 0.0, 0.5):
    sig = t * (ed.T @ ed) / Nn                                  # viriel : force t r le long de chaque fil, volume 1 par porteur
    eps = 1e-6
    num = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Fp, Fm = np.eye(3), np.eye(3)
            Fp[i, j] += eps
            Fm[i, j] -= eps
            num[i, j] = (energie(t, Fp) - energie(t, Fm)) / (2 * eps)
    k11[str(t)] = dict(energie_par_porteur=energie(t, np.eye(3)), contrainte_viriel=np.diag(sig).tolist(), pression=float(-np.trace(sig) / 3),
                       ecart_a_la_derivee_de_l_energie=float(np.abs(num - sig).max()))
R['K11'] = dict(porteurs=Nn, fils=len(ed), somme_des_carres_par_porteur=float(r2.sum() / Nn), etats=k11)

(ICI / 'releve14_controles.json').write_text(json.dumps(R, indent=1, ensure_ascii=False, default=float))
print(json.dumps(R, indent=1, ensure_ascii=False, default=float))
