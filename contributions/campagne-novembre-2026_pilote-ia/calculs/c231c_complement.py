#!/usr/bin/env python3
"""C-231c, COMPLEMENT APRES COUP (declare) : apres lecture des resultats de ChatGPT, sa regle << derniere facette >> produit une bande (diametre 32 pour d = 2), la mienne un
eventail (diametre 2) : la consigne du protocole admet les deux. Je rejoue ici la bande (chaque nouveau sommet est colle sur les d sommets les plus recents) et les distances
moyennes, pour comparer aux chiffres de sa passation (d = 3, p = 0,4 : hasard 11,77 %, derniere 49,48 % ; distances moyennes 2,63 et 7,56). Claude, 20 novembre 2026."""
import itertools, json
import numpy as np, networkx as nx
N = 64; out = []
def bande(d):
    G = nx.complete_graph(d + 1); G.add_edges_from((v, u) for v in range(d + 1, N) for u in range(v - d, v)); return G
def hasard(d, rng):
    G = nx.complete_graph(d + 1); fac = [tuple(c) for c in itertools.combinations(range(d + 1), d)]
    for v in range(d + 1, N):
        f = fac.pop(rng.integers(len(fac))); G.add_edges_from((v, u) for u in f); fac.extend(tuple(x for x in f if x != u) + (v,) for u in f)
    return G
for d in (2, 3, 4, 6, 12):
    rng = np.random.default_rng([231, d]); G = bande(d); E = np.array(G.edges()); r = dict(d=d, M=G.number_of_edges(), lam=nx.edge_connectivity(G), diametre=nx.diameter(G),
        distance_moyenne_bande=nx.average_shortest_path_length(G), distance_moyenne_hasard=float(np.mean([nx.average_shortest_path_length(hasard(d, rng)) for _ in range(8)])), connexe_bande={})
    for p in (0.2, 0.4, 0.6):
        k = 0
        for _ in range(960):
            H = nx.Graph(); H.add_nodes_from(range(N)); H.add_edges_from(E[rng.random(len(E)) >= p]); k += nx.is_connected(H)
        r['connexe_bande'][str(p)] = k / 960
    out.append(r); print(json.dumps(r), flush=True)
json.dump(out, open('c231c_complement.json', 'w'), indent=1)
