#!/usr/bin/env python3
"""BP-R1, BP-EQ1, BP-IM1 (ChatGPT, 13 novembre 2026) -- contre-verification independante (Claude).

Tout est exact ou exhaustif ; aucun tirage aleatoire hors du controle d'optimisation (graine fixe).
Usage : python3 bp_r1_eq1_im1_contre_audit.py
"""
import itertools
import json
import math
import pathlib

import numpy as np
from scipy.optimize import minimize

ICI = pathlib.Path(__file__).resolve().parent
bilan = {}

# ------------------------------------------------------------------ BP-R1 : fermeture triadique
def composantes(n, adj):
    vus, comps = set(), []
    for s in range(n):
        if s in vus:
            continue
        pile, comp = [s], {s}
        while pile:
            u = pile.pop()
            for v in range(n):
                if adj[u] >> v & 1 and v not in comp:
                    comp.add(v)
                    pile.append(v)
        vus |= comp
        comps.append(comp)
    return comps


def ferme(n, adj):
    """Deux elements qui partagent un voisin deviennent relies ; les liens restent. Jusqu'au point fixe."""
    adj = list(adj)
    while True:
        nouv = list(adj)
        for u in range(n):
            for w in range(n):
                if adj[u] >> w & 1:
                    nouv[u] |= adj[w] & ~(1 << u)
        if nouv == adj:
            return adj
        adj = nouv


r1 = {}
for n in range(2, 7):
    paires = list(itertools.combinations(range(n), 2))
    total = connexes = connexes_complets = composantes_completes = 0
    for masque in range(1 << len(paires)):
        adj = [0] * n
        for b, (i, j) in enumerate(paires):
            if masque >> b & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
        total += 1
        comps = composantes(n, adj)
        fin = ferme(n, adj)
        ok = all(all(fin[u] == sum(1 << v for v in c if v != u) for u in c) for c in comps)
        composantes_completes += ok
        if len(comps) == 1:
            connexes += 1
            connexes_complets += ok
    r1[n] = dict(graphes=total, connexes=connexes, connexes_devenus_complets=connexes_complets,
                 toute_composante_devient_complete=composantes_completes)
bilan['BP-R1_fermeture'] = r1
# deux tetraedres collant par une face : f-vecteur et caracteristique d'Euler
tets = [(0, 1, 2, 3), (0, 1, 2, 4)]
aretes = {frozenset(p) for t in tets for p in itertools.combinations(t, 2)}
faces = {frozenset(p) for t in tets for p in itertools.combinations(t, 3)}
bilan['BP-R1_deux_tetraedres'] = dict(sommets=5, aretes=len(aretes), faces=len(faces), cellules=2,
                                      euler=5 - len(aretes) + len(faces) - 2)

# complements de la passation : P1 (diametre), P3 (plafond de degre 3), K4 avant K5, assemblage en arbre
def un_pas(n, adj):
    nouv = list(adj)
    for u in range(n):
        for w in range(n):
            if adj[u] >> w & 1:
                nouv[u] |= adj[w] & ~(1 << u)
    return nouv


def diametre(n, adj):
    dmax = 0
    for s in range(n):
        dist, front, d = {s: 0}, [s], 0
        while front:
            d += 1
            suiv = []
            for u in front:
                for v in range(n):
                    if adj[u] >> v & 1 and v not in dist:
                        dist[v] = d
                        suiv.append(v)
            front = suiv
        dmax = max(dmax, max(dist.values()))
    return dmax


def a_clique(n, adj, k):
    return any(all(adj[i] >> j & 1 for i, j in itertools.combinations(c, 2)) for c in itertools.combinations(range(n), k))


comp = {}
for n in (5, 6):
    paires = list(itertools.combinations(range(n), 2))
    p1_ok = p1_tot = cap = cap_k4 = avant = ensemble = 0
    for masque in range(1 << len(paires)):
        adj = [0] * n
        for bb, (i, j) in enumerate(paires):
            if masque >> bb & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
        if len(composantes(n, adj)) != 1:
            continue
        d = diametre(n, adj)
        pas, cur, t4, t5 = 0, list(adj), None, None
        complet = [((1 << n) - 1) & ~(1 << u) for u in range(n)]
        while True:
            if t4 is None and a_clique(n, cur, 4):
                t4 = pas
            if t5 is None and a_clique(n, cur, 5):
                t5 = pas
            if cur == complet:
                break
            cur = un_pas(n, cur)
            pas += 1
        p1_tot += 1
        p1_ok += (pas == (0 if d <= 1 else math.ceil(math.log2(d))))
        if max(bin(x).count('1') for x in adj) <= 3:
            cap += 1
            cap_k4 += a_clique(n, adj, 4)
        if n == 5:
            avant += (t4 < t5)
            ensemble += (t4 == t5)
    comp[n] = dict(connexes=p1_tot, P1_formule_verifiee=p1_ok, degre_max_3=cap, degre_max_3_avec_K4=cap_k4,
                   K4_avant_K5=avant, K4_avec_K5=ensemble)
bilan['BP-R1_complements'] = comp
arbre = {}
for m in range(1, 8):
    cells = [(0, 1, 2, 3)]
    for k in range(1, m):                      # chaine : chaque cellule neuve sur une face exposee de la precedente
        prec = cells[-1]
        cells.append((prec[1], prec[2], prec[3], 3 + k))
    E = {frozenset(p) for t in cells for p in itertools.combinations(t, 2)}
    Fc = {}
    for t in cells:
        for p in itertools.combinations(t, 3):
            Fc[frozenset(p)] = Fc.get(frozenset(p), 0) + 1
    V = len({v for t in cells for v in t})
    arbre[m] = dict(V=V, E=len(E), F=len(Fc), T=m, euler=V - len(E) + len(Fc) - m,
                    faces_frontiere=sum(1 for c in Fc.values() if c == 1),
                    conforme=(V == m + 3 and len(E) == 3 * m + 3 and len(Fc) == 3 * m + 1
                              and sum(1 for c in Fc.values() if c == 1) == 2 * m + 2))
bilan['BP-R1_assemblage_en_arbre'] = arbre

# ------------------------------------------------------------------ BP-EQ1 : coupes et cycles
bilan['BP-EQ1_Kn'] = {n: dict(desequilibre=n - 1, circulation=(n - 1) * (n - 2) // 2) for n in range(2, 8)}
bilan['BP-EQ1_egalite_pour_n'] = [n for n in range(2, 2001) if n - 1 == (n - 1) * (n - 2) // 2]
L = 4 * np.eye(4) - np.ones((4, 4))
bilan['BP-EQ1_spectre_K4'] = sorted(round(float(x), 12) for x in np.linalg.eigvalsh(L))
# l'egalite equivaut a E = 2(V-1) pour un graphe connexe : toutes les roues la satisfont
bilan['BP-EQ1_roues'] = {f'W{k}': dict(V=k + 1, E=2 * k, desequilibre=k, circulation=2 * k - (k + 1) + 1,
                                         egalite=(k == 2 * k - (k + 1) + 1)) for k in range(3, 9)}
# enumeration exhaustive : graphes connexes non complets a V sommets et 2(V-1) aretes, a isomorphisme pres
def classes(V):
    paires = list(itertools.combinations(range(V), 2))
    vus = set()
    for choix in itertools.combinations(range(len(paires)), 2 * (V - 1)):
        adj = [0] * V
        for b in choix:
            i, j = paires[b]
            adj[i] |= 1 << j
            adj[j] |= 1 << i
        if len(composantes(V, adj)) != 1:
            continue
        canon = min(tuple(sorted(tuple(sorted((p[i], p[j]))) for b in choix for i, j in [paires[b]]))
                    for p in itertools.permutations(range(V)))
        vus.add(canon)
    return len(vus)
bilan['BP-EQ1_contre_exemples_a_isomorphisme_pres'] = {V: classes(V) for V in (4, 5, 6)}

# ------------------------------------------------------------------ BP-IM1
faces4 = [frozenset(f) for f in itertools.combinations(range(4), 3)]
expo = {}
for k in range(1, 5):
    vals = set()
    for sous in itertools.combinations(faces4, k):
        compte = {}
        for f in sous:
            for e in itertools.combinations(sorted(f), 2):
                compte[e] = compte.get(e, 0) + 1
        vals.add(sum(1 for c in compte.values() if c == 1))
    expo[k] = sorted(vals)
bilan['BP-IM1_aretes_exposees'] = expo
# identite n * somme |x_i - xbar|^2 = somme_{i<j} |x_i - x_j|^2 et minimum sous distances >= a
rng = np.random.default_rng(20261113)
X = rng.normal(size=(4, 3))
g = 4 * ((X - X.mean(0)) ** 2).sum()
d = sum(((X[i] - X[j]) ** 2).sum() for i, j in itertools.combinations(range(4), 2))
bilan['BP-IM1_identite_ecart'] = abs(g - d)
def etal(x):
    P = x.reshape(4, 3)
    return ((P - P.mean(0)) ** 2).sum()
cons = [dict(type='ineq', fun=lambda x, i=i, j=j: np.linalg.norm(x.reshape(4, 3)[i] - x.reshape(4, 3)[j]) - 1.0)
        for i, j in itertools.combinations(range(4), 2)]
mins = []
for _ in range(40):
    res = minimize(etal, rng.normal(size=12) * 1.5, constraints=cons, method='SLSQP', options=dict(maxiter=500, ftol=1e-14))
    if res.success:
        mins.append(res.fun)
bilan['BP-IM1_minimum_numerique_R2'] = dict(min=min(mins), attendu=1.5, essais_reussis=len(mins))
# meme probleme dans le plan : carre et losange a egalite, 2 a^2
def etal2(x):
    P = x.reshape(4, 2)
    return ((P - P.mean(0)) ** 2).sum()
cons2 = [dict(type='ineq', fun=lambda x, i=i, j=j: np.linalg.norm(x.reshape(4, 2)[i] - x.reshape(4, 2)[j]) - 1.0)
         for i, j in itertools.combinations(range(4), 2)]
m2 = [r.fun for r in (minimize(etal2, rng.normal(size=8) * 1.5, constraints=cons2, method='SLSQP',
                               options=dict(maxiter=500, ftol=1e-14)) for _ in range(40)) if r.success]
bilan['BP-IM1_minimum_dans_le_plan'] = min(m2)
theta = math.degrees(math.acos(1 / 3))
bilan['BP-IM1_diedre'] = dict(theta=theta, cinq=5 * theta, defaut=360 - 5 * theta)

(ICI / 'bp_r1_eq1_im1_contre_audit.json').write_text(json.dumps(bilan, indent=1, ensure_ascii=False, default=float))
print(json.dumps(bilan, indent=1, ensure_ascii=False, default=float))
