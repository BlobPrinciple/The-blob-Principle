#!/usr/bin/env python3
"""C-215c -- mon objection du 18 novembre, reverifiee : sur tout graphe symetrique (mouvements reversibles), les noyaux existentiel et universel valent l'ensemble des etats
non isoles ; puis effet d'un ensemble de contraintes. Prediction scellee : c215c_prediction.txt. Claude, 19 novembre 2026. Usage : python3 c215c.py"""
import itertools, json
def noyaux(S, C):
    Ke = set(C); Ku = set(C)
    while True:
        M = {s for s in Ke if not (S[s] & Ke)}
        if not M: break
        Ke -= M
    while True:
        M = {s for s in Ku if not (S[s]) or not (S[s] <= Ku)}
        if not M: break
        Ku -= M
    return Ke, Ku
out = dict(sans_contrainte=[], avec_contrainte=[])
for n in range(1, 6):
    P = list(itertools.combinations(range(n), 2)); nb = ok_e = ok_u = 0
    for bits in range(2 ** len(P)):
        S = [set() for _ in range(n)]
        for k, (i, j) in enumerate(P):
            if bits >> k & 1: S[i].add(j); S[j].add(i)
        Ke, Ku = noyaux(S, range(n)); non_isoles = {i for i in range(n) if S[i]}
        nb += 1; ok_e += (Ke == non_isoles)
        # universel : composantes sans sommet isole... un sommet isole n'a pas de voisin, donc n'est voisin de personne
        ok_u += (Ku == non_isoles)
    out['sans_contrainte'].append(dict(etats=n, graphes_symetriques=nb, existentiel_egal_non_isoles=ok_e, universel_egal_non_isoles=ok_u))
# contrainte : memes graphes symetriques a 4 etats, un etat exclu ; l'universel peut alors perdre des etats, l'existentiel seulement les etats devenus isoles
n = 4; P = list(itertools.combinations(range(n), 2)); perd_e = perd_u = nb = 0
for bits in range(2 ** len(P)):
    S = [set() for _ in range(n)]
    for k, (i, j) in enumerate(P):
        if bits >> k & 1: S[i].add(j); S[j].add(i)
    for excl in range(n):
        C = set(range(n)) - {excl}; Sc = [S[i] & C if i in C else set() for i in range(n)]
        Ke, _ = noyaux(Sc, C)
        # lecture universelle stricte : un mouvement vers l'etat exclu est une impasse
        Ku = set(C)
        while True:
            M = {s for s in Ku if not S[s] or not (S[s] <= Ku)}
            if not M: break
            Ku -= M
        admis_non_isoles = {i for i in C if S[i]}
        nb += 1; perd_e += (Ke != admis_non_isoles); perd_u += (Ku != admis_non_isoles)
out['avec_contrainte'] = dict(cas=nb, existentiel_retire_des_etats_non_isoles=perd_e, universel_retire_des_etats_non_isoles=perd_u)
json.dump(out, open('c215c.json', 'w'), indent=1); print(json.dumps(out, indent=1))
