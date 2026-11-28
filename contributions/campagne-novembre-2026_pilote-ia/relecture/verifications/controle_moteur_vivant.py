#!/usr/bin/env python3
"""Contrôle du pilote : la géométrie du « moteur vivant » (Partie XLII, 1er juin), tel que l'auteur l'a consigné
dans corpus/03_scripts (« blob scaling colab.py », classe BlobVivant, « tout fidèle à la session »). Rien n'y est modifié.

Lecture du code : recâblage entre deux sommets quelconques distants de moins de 0,45 ; naissance d'un sommet à une
distance tirée selon N(0 ; 0,10) de son parent, relié aux 6 plus proches parmi le parent et ses voisins à moins de 0,32 ;
croissance de 12 % par balayage. Ces trois longueurs sont absolues : elles ne diminuent pas quand N augmente.
Question : à quoi ressemble l'espace produit ? Longueur des arêtes, part des arêtes pures, étendue du nuage.
Usage : controle_moteur_vivant.py "<chemin de blob scaling colab.py>" [balayages]
"""
import sys, math
import numpy as np

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# ----------------------------- MESURE AUX PALIERS')], 'moteur_vivant_de_l_auteur', 'exec'), espace)
BlobVivant, rips_radius, find_all_K4 = espace['BlobVivant'], espace['rips_radius'], espace['find_all_K4']
nb = int(sys.argv[2]) if len(sys.argv) > 2 else 24

for seed in (1, 2):
    bl = BlobVivant(N0=100, seed=seed)
    print(f"graine {seed} : départ N = 100, rayon de Rips = {rips_radius(100, 6.6):.3f}")
    for s in range(1, nb + 1):
        bl.step()
        if s in (6, 12, 18, nb):
            N = bl.N; P = np.array(bl.pts)
            L = []; pure = []; 
            for i in range(N):
                for j in bl.adj[i]:
                    if j > i:
                        L.append(np.linalg.norm(P[i] - P[j])); pure.append(len(bl.adj[i] & bl.adj[j]) == 0)
            L = np.array(L); pure = np.array(pure); deg = np.array([len(a) for a in bl.adj])
            k4 = len(find_all_K4(bl.adj, N))
            long_ = L > 0.20
            print(f"  balayage {s:>2} : N = {N:>5} ; degré moyen {deg.mean():5.2f} ; étendue du nuage (écart-type par axe) {P.std(0).mean():.2f} ; rayon de Rips qu'aurait un nuage de N points à densité 6,6 : {rips_radius(N, 6.6):.3f}")
            print(f"               longueur des arêtes : médiane {np.median(L):.3f}, 90e centile {np.quantile(L, 0.9):.3f}, maximum {L.max():.3f} ; arêtes de plus de 0,20 : {100*long_.mean():.0f} %")
            print(f"               arêtes pures : {100*pure.mean():.0f} % du total ; {100*pure[long_].mean() if long_.any() else float('nan'):.0f} % des longues, {100*pure[~long_].mean():.0f} % des courtes ; tétraèdres par sommet {k4/N:.1f}")
