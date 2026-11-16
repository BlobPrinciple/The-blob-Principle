#!/usr/bin/env python3
"""X-12 bis [EXPLORATOIRE] -- moteur canonique de l'auteur (canonical() importee telle quelle), N = 1000, nsw = 80, en faisant varier le seul facteur de volume du vivier
de paires candidates cand_factor (valeur de l'auteur : 2,6). Le nombre de tetraedres par arete depend-il du vivier ? (Claude, 16 novembre 2026)."""
import json, os, sys
import numpy as np
from c179c import G
chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB', 'blob colab verrouillage.py')
src = open(chemin).read().split('def edges_tris')[0]; src = src[src.index('BETA, TAU'):]; ns = {}; exec('import numpy as np, os\nfrom scipy.spatial import cKDTree\n' + src, ns)
out = []
for cf in (1.3, 1.6, 2.6, 4.1, 6.0):
    for seed in (1, 2, 3):
        A, X, h = ns['canonical'](1000, seed, cand_factor=cf, nsw_per_N=80); g = G(1000)
        for a in range(1000):
            for b in A[a]:
                if a < b: g.ajoute(a, b)
        m = g.mesure(); r = dict(cand_factor=cf, graine=seed, aretes=m['aretes'], triangles_par_sommet=m['triangles'] / 1000, tetraedres_par_sommet=m['tetraedres_par_sommet'], n_e_mediane=m['n_e_mediane'], n_e_moyenne=m['n_e_moyenne'], n_e_max=m['n_e_max'], plus_grande_clique=m['plus_grande_clique'], degre_max=m['degre_max'])
        out.append(r); print(r, flush=True); json.dump(out, open('x12_bis_pool.json', 'w'), indent=1)
