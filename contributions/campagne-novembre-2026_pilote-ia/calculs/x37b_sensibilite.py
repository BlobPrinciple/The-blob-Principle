#!/usr/bin/env python3
"""X-37 bis -- sensibilite de la composition du regime mixte aux trois taux poses de l'operateur << mitose_cycle.py >> de l'auteur (BlobCosmogonie,
charge sans modification). Prediction scellee : x37b_prediction.txt. Claude (pilote IA), 28 novembre 2026.
Usage : x37b_sensibilite.py <dossier des scripts de l'auteur> > x37b_sensibilite.jsonl"""
import sys, json
from x37_deux_horloges import charger, simplexes

GRILLE = [(0.3, 0.12, 0.06), (0.3, 0.06, 0.06), (0.3, 0.24, 0.06), (0.3, 0.12, 0.03), (0.3, 0.12, 0.12), (0.15, 0.12, 0.06), (0.6, 0.12, 0.06)]
natif, cycle = charger(sys.argv[1]); Cls = cycle['BlobCosmogonie']
for (pm, pt, pd) in GRILLE:
    for graine in range(4):
        bm = Cls(n_init=40, seed=graine); N0 = None
        while len(bm.adj) < 4000 and bm.t < 200:
            N0 = len(bm.adj); bm.step(p_mitose=pm, p_triangle=pt, p_dissip=pd)
        E, pures, tri, k4 = simplexes(bm.adj); N = len(bm.adj)
        dans_k4 = set()
        for q in k4:
            for i in range(4):
                for j in range(i + 1, 4): dans_k4.add((q[i], q[j]))
        print(json.dumps(dict(p_mitose=pm, p_triangle=pt, p_dissip=pd, graine=graine, pas=bm.t, N=N, liens=E, part_liens_purs=pures / E, part_liens_de_k4=len(dans_k4) / E,
                              part_liens_de_triangles_hors_k4=(E - pures - len(dans_k4)) / E, purs_par_sommet=pures / N, triangles_par_sommet=len(tri) / N, k4_par_sommet=len(k4) / N,
                              croissance_du_dernier_pas=N / N0 - 1)), flush=True)
