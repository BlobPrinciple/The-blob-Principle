#!/usr/bin/env python3
"""X-12 [EXPLORATOIRE] -- le moteur canonique de l'auteur, TEL QUEL (fonction canonical() de corpus/03_scripts/SCRIPTS DIVERS BLOB/blob colab verrouillage.py, importee sans
modification : kappa = 6,6, beta = 0,30, tau = 0,50, cand_factor = 2,6), en fonction du nombre de balayages nsw_per_N (valeur de l'auteur : 80). Question : le nombre de
tetraedres par arete et la taille des amas se stabilisent-ils, ou le graphe se condense-t-il quand on laisse tourner ? (Claude, 16 novembre 2026).
Usage : python3 x12_moteur_canonique.py <N> <graine> <nsw> -> x12_<N>_<graine>_<nsw>.json"""
import importlib.util, json, os, sys, time
import numpy as np
from c179c import G

chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB', 'blob colab verrouillage.py')
src = open(chemin).read().split('def edges_tris')[0]; src = src[src.index('BETA, TAU'):]   # seulement les constantes BETA, TAU et la fonction canonical(), texte inchange
ns = {}; exec('import numpy as np, os\nfrom scipy.spatial import cKDTree\n' + src, ns)
N, seed, nsw = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); t0 = time.time()
A, X, h = ns['canonical'](N, seed, nsw_per_N=nsw); g = G(N)
for a in range(N):
    for b in A[a]:
        if a < b: g.ajoute(a, b)
m = g.mesure(); deg = np.array([len(x) for x in A]); vu = set(); comps = []
for a in range(N):
    if a in vu: continue
    c = {a}; pile = [a]
    while pile:
        x = pile.pop()
        for y in A[x]:
            if y not in c: c.add(y); pile.append(y)
    vu |= c; comps.append(len(c))
m.update(nsw=nsw, graine=seed, triangles_par_sommet=m['triangles'] / N, composantes=len(comps), plus_grande_composante=max(comps), sommets_isoles=int((deg == 0).sum()), dispersion_degres=float(deg.std() / deg.mean()), secondes=time.time() - t0)
json.dump(m, open(f'x12_{N}_{seed}_{nsw}.json', 'w')); print({k: m[k] for k in ('nsw', 'graine', 'triangles_par_sommet', 'tetraedres_par_sommet', 'plus_grande_clique', 'n_e_mediane', 'n_e_moyenne', 'n_e_max', 'degre_max', 'composantes', 'plus_grande_composante', 'sommets_isoles', 'dispersion_degres', 'secondes')}, flush=True)
