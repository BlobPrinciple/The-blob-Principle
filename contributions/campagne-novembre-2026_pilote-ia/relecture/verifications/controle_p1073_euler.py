#!/usr/bin/env python3
"""Contrôle du pilote pour la page 1073 du master V346 (Partie CXIII.2, 8 juin) : caractéristique d'Euler du complexe de drapeau.
Le master corrige un calcul tronqué (sommets - arêtes + triangles - tétraèdres, très négatif) en écrivant que la somme alternée
COMPLÈTE, cliques de toutes tailles comprises, donne « le résultat correct chi = 0 ».
Calcul : dénombrement exact des cliques de chaque taille, moteur de l'auteur (gap curl colab.py), kappa = 6,6.
Usage : controle_p1073_euler.py "<chemin de gap curl colab.py>"
"""
import sys
src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical = espace['build_initial'], espace['run_mcmc_canonical']

def cliques_par_taille(adj, N):
    compte = {}
    def etend(taille, cand):
        compte[taille] = compte.get(taille, 0) + 1
        for v in sorted(cand):
            etend(taille + 1, {w for w in cand if w > v and w in adj[v]})
    for v in range(N):
        etend(1, {w for w in adj[v] if w > v})
    return compte

for N in (300, 600):
    for seed in (1, 2):
        pts, adj0, pool, E0 = build_initial(N, seed, 6.6)
        for nom, adj in (("départ", adj0), ("Blob", run_mcmc_canonical(pts, adj0, pool, N, E0, seed))):
            c = cliques_par_taille(adj, N); kmax = max(c)
            chi = sum((-1) ** (k - 1) * c[k] for k in c)
            chi4 = sum((-1) ** (k - 1) * c.get(k, 0) for k in range(1, 5))
            print(f"N={N} graine {seed} {nom:<6} cliques par taille {[c[k] for k in sorted(c)]} ; plus grande clique {kmax} ; "
                  f"chi tronqué aux tétraèdres = {chi4} ({chi4/N:+.2f} N) ; chi complet = {chi} ({chi/N:+.2f} N)")
