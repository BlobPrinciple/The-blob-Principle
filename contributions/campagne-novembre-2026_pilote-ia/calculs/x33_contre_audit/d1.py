"""D1 : regle a la lettre, palier n. Paires liees, cousins, T29 sur donnees."""
import json, sys, time
from alib import *

n = int(sys.argv[1])
t0 = time.time()
S = {u: 0 for u in GERM}
tile_of = {u: GERMSET for u in GERM}
sizes = [5]
for k in range(1, n + 1):
    L = sorted(S)
    _, over, adj = adjacency(L)
    assert over == 0
    new = {}
    for cl in cliques4(L, adj):
        C = [L[i] for i in cl]
        for u in cell_sides(C):
            if u not in S and u not in new:
                new[u] = frozenset(C) | {u}
    for u, T in new.items():
        S[u] = k
        tile_of[u] = T
    sizes.append(len(S))
P = Pack()
L = sorted(S, key=lambda u: S[u])
for u in L:
    if u not in GERMSET:
        P.gate_of(u, tile_of[u])
L = sorted(S)
links, over, adj = adjacency(L)
res = dict(partie='D1', palier=n, tailles=sizes, constituants=len(S), paires_liees=len(links), chevauchements=over,
           dans_le_germe=0, parent_et_enfant=0, cousins=0, cousins_hors_de_la_forme=0, cousins_mur_ne_separe_pas=0,
           cousins_de_paliers_differents=0, cousins_distances_portes_differentes=0)
isparent = lambda p, q: p in P.floor(q)
cous = {u: set() for u in L}
for i, j in links:
    p, q = L[i], L[j]
    if p in GERMSET and q in GERMSET:
        res['dans_le_germe'] += 1; continue
    if isparent(p, q) or isparent(q, p):
        res['parent_et_enfant'] += 1; continue
    res['cousins'] += 1
    cous[p].add(q); cous[q].add(p)
    if S[p] != S[q]:
        res['cousins_de_paliers_differents'] += 1
    if dist(P.T[p]) != dist(P.T[q]):
        res['cousins_distances_portes_differentes'] += 1
    for x, y in ((p, q), (q, p)):
        Tx = P.T[x]
        fs = [f for f in P.floor(x) if other(Tx, f) == y]
        if len(fs) != 1:
            res['cousins_hors_de_la_forme'] += 1; continue
        if not wall_separates(P.Tp(x), fs[0]):
            res['cousins_mur_ne_separe_pas'] += 1
# murs de T'(x) et mere propre
bywalls = {}
mismatch = dict(zero_mur_pas_palier1=0, un_mur_sans_mere_propre=0, un_mur_mere_pas_le_parent_oppose=0, deux_murs_avec_mere_propre=0,
                deux_murs_parents_opposes_non_cousins=0, plus_de_deux=0, annonce_non_liee=0, annonce_parent_ou_enfant=0,
                annonce_hors_tissu=0, cousin_donnees_non_annonce=0, annonces=0, mere_propre_non_unique=0)
palier1 = {other(GERMSET, v) for v in GERM}
for x in L:
    if x in GERMSET:
        if cous[x]:
            mismatch.setdefault('germe_avec_cousin', 0); mismatch['germe_avec_cousin'] += 1
        continue
    sep = P.separating_parents(x)
    k = len(sep)
    bywalls[k] = bywalls.get(k, 0) + 1
    # meres propres, par definition : f dont T(f) contient le plancher de x et f
    F = P.floor(x)
    moms = [f for f in F if F <= P.T[f] and f in F]
    if k == 0 and x not in palier1: mismatch['zero_mur_pas_palier1'] += 1
    if k == 1:
        if len(moms) == 0: mismatch['un_mur_sans_mere_propre'] += 1
        elif moms != sep: mismatch['un_mur_mere_pas_le_parent_oppose'] += 1
    if k == 2:
        if moms: mismatch['deux_murs_avec_mere_propre'] += 1
        if ip(sep[0], sep[1]) != -1 or isparent(sep[0], sep[1]) or isparent(sep[1], sep[0]):
            mismatch['deux_murs_parents_opposes_non_cousins'] += 1
    if k > 2: mismatch['plus_de_deux'] += 1
    if x not in palier1 and len(moms) > 1: mismatch['mere_propre_non_unique'] += 1
    ann = set()
    for f in sep:
        y = other(P.T[x], f)
        ann.add(y); mismatch['annonces'] += 1
        if ip(x, y) != -1: mismatch['annonce_non_liee'] += 1
        if y not in S:
            mismatch['annonce_hors_tissu'] += 1
            continue
        if isparent(x, y) or isparent(y, x): mismatch['annonce_parent_ou_enfant'] += 1
    for y in cous[x]:
        if y not in ann: mismatch['cousin_donnees_non_annonce'] += 1
res['par_nombre_de_murs_qui_separent'] = bywalls
res['T29'] = mismatch
res['duree_s'] = round(time.time() - t0, 1)
print(json.dumps(res))
