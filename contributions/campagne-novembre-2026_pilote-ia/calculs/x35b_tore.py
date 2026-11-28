#!/usr/bin/env python3
"""X-35 bis. Ajout non prévu au plan scellé : les mêmes fractions à kappa0 = 4, mais dans une boîte périodique (sans bord).
But : dire si la lente dérive avec la taille observée dans X-35 est un effet de bord du cube, et quelle est la limite sans bord.
Écart déclaré avec le programme de l'auteur : la boîte est périodique ; si le graphe de rayon r a plus de E0 arêtes, on en retire au
hasard sans condition de connexité (la règle de l'auteur, « seulement si le graphe reste d'un seul tenant », ne peut pas s'appliquer à un
graphe qui ne l'est pas au départ).
Usage : x35b_tore.py N kappa graine
"""
import sys, math, json
import numpy as np
from scipy.spatial import cKDTree
from x34_replication_blob_canonique import Graphe, cliques4
from x35_fractions_kappa4 import composante_max, pas, classer, BURN, EVOL

def lancer(N, kappa, graine, beta=0.30, tau=0.50):
    r = (kappa / ((N - 1) * (4 / 3) * math.pi)) ** (1 / 3)
    E0 = max(N - 1, int(N * kappa / 2))
    pts = np.random.default_rng(graine).uniform(0.0, 1.0, (N, 3))
    arbre = cKDTree(pts, boxsize=1.0)
    pool = [tuple(sorted(map(int, p))) for p in arbre.query_pairs(1.6 * r, output_type='ndarray')]
    init = [tuple(sorted(map(int, p))) for p in arbre.query_pairs(r, output_type='ndarray')]
    g = Graphe(N, pool, np.random.default_rng(graine + 50_000))
    for e in g.pool: g.absent[e] = len(g.labs); g.labs.append(e)
    for e in init: g.ajouter(e)
    while len(g.liste) < E0: g.ajouter(g.labs[int(g.rng.integers(len(g.labs)))])
    while len(g.liste) > E0: g.retirer(g.liste[int(g.rng.integers(len(g.liste)))])
    out = {'N': N, 'kappa': kappa, 'graine': graine, 'bras': 'tore', 'E0': E0, 'aretes': len(g.liste), 'aretes_rayon': len(init),
           'degre_reserve': 2 * len(pool) / N, 'lcc_initiale': composante_max(g.adj, N) / N}
    acc, gardes = pas(g, BURN * N, beta, N / tau, np.random.default_rng(graine + 200_000), False)
    adj_eq = [set(a) for a in g.adj]; K4 = cliques4(g)
    out.update({'acceptation': acc, 'part_gardes': gardes, 'tri_par_N': g.ntri / N, 'k4_par_N': len(K4) / N, 'cv_degres': g.cv()})
    pas(g, EVOL * N, beta, N / tau, np.random.default_rng(graine + 210_000), False)
    out.update(classer(adj_eq, g.adj, N, K4, [0.338, 0.40, 0.45, 0.50, 0.55, 0.60]))
    return out

if __name__ == '__main__':
    print(json.dumps(lancer(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])), ensure_ascii=False))
