#!/usr/bin/env python3
"""Contrôle du pilote pour la page 1165 du master V346 (chapitre « La résonance simpliciale », §7).
Le master donne la « rigidité de Hodge » moyenne des arêtes engagées dans un tétraèdre : Blob 12,8 ; graphe géométrique 5,8 ;
rapport 2,2 stable de N = 800 à 2 000 ; et aucune différence pour les arêtes engagées seulement dans des triangles.
Hypothèse testée : cette rigidité est le terme diagonal du laplacien de Hodge de degré 1 du complexe de drapeau,
(L1)_ee = 2 + nombre de triangles portés par l'arête e (deux sommets au bord, un triangle par voisin commun).
Moteur de l'auteur (gap curl colab.py), kappa = 6,6.
Usage : controle_p1165_rigidite_hodge.py "<chemin de gap curl colab.py>"
"""
import sys
import numpy as np
src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical = espace['build_initial'], espace['run_mcmc_canonical']

def classes(adj, N):
    A = [set(adj[v]) for v in range(N)]
    k4, tri, pur = [], [], 0
    for u in range(N):
        for v in A[u]:
            if v <= u:
                continue
            communs = A[u] & A[v]
            if not communs:
                pur += 1
                continue
            dans_k4 = any(A[w] & communs for w in communs)
            (k4 if dans_k4 else tri).append(2 + len(communs))
    return k4, tri, pur

for N, graines in ((800, (1, 2)), (2000, (1,))):
    for seed in graines:
        pts, adj0, pool, E0 = build_initial(N, seed, 6.6)
        lignes = {}
        for nom, adj in (("départ", adj0), ("Blob", run_mcmc_canonical(pts, adj0, pool, N, E0, seed))):
            k4, tri, pur = classes(adj, N)
            lignes[nom] = np.mean(k4)
            print(f"N={N} graine {seed} {nom:<6} arêtes dans un tétraèdre : {len(k4)}, diagonale moyenne {np.mean(k4):.2f} ; "
                  f"arêtes dans des triangles seulement : {len(tri)}, diagonale moyenne {np.mean(tri) if tri else float('nan'):.2f} ; arêtes pures : {pur}")
        print(f"   rapport Blob / départ sur les arêtes de tétraèdre : {lignes['Blob']/lignes['départ']:.2f}")
