#!/usr/bin/env python3
"""X-13 [EXPLORATOIRE, non aveugle : fait apres lecture du C-180 de ChatGPT] -- (1) le second moteur historique de l'auteur, << blob engine.py >> (build_blob, importe sans
modification : kappa = 6,6, beta = 0,30, tau = 0,50, POOL_FAC = 1,6 sur le rayon, THERM_FAC = 120) : point de travail et nombre de tetraedres par arete ;
(2) controle de l'anomalie de comptage signalee par ChatGPT dans canonical() de << blob colab verrouillage.py >> (triangles comptes trois fois a l'initialisation, une fois
ensuite) et effet de sa correction (Claude, 16 novembre 2026). Usage : python3 x13_deux_moteurs.py"""
import importlib.util, itertools, json, os, sys
import numpy as np
from c180c import mesure

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(base, 'blob engine.py')); be = importlib.util.module_from_spec(spec); spec.loader.exec_module(be)
out = dict(numba=be.HAVE_NUMBA, moteur_engine=[], compteur=[])
for N, tf in ((1000, 120), (1000, 480), (2000, 120)):
    for seed in (0, 1, 2):
        pts, nbr, deg = be.build_blob(N, seed, therm_fac=tf); A = [set(int(x) for x in nbr[u, :deg[u]]) for u in range(N)]; m = mesure(A, N); d = np.array([len(x) for x in A], float)
        r = dict(N=N, graine=seed, therm_fac=tf, triangles_par_sommet=m['triangles_par_sommet'], CV_degres=float(d.std() / d.mean()), degre_moyen=float(d.mean()), tetraedres_par_sommet=m['tetraedres_par_sommet'], n_e_mediane=m['n_e_mediane'], n_e_moyenne=m['n_e_moyenne'],
                 n_e_max=m['n_e_max'], part_aretes_sans_tetraedre=m['part_aretes_sans_tetraedre'], part_4_5_6=m['part_4_5_6'], sommets_isoles=m['sommets_isoles'], degre_max=m['degre_max'])
        out['moteur_engine'].append(r); print('engine', r, flush=True); json.dump(out, open('x13_deux_moteurs.json', 'w'), indent=1)
# (2) compteur de canonical()
src = open(os.path.join(base, 'blob colab verrouillage.py')).read().split('def edges_tris')[0]; src = src[src.index('BETA, TAU'):]
ligne = "    ntri = float(sum(len(A[i] & A[j]) for i in range(N) for j in A[i] if i < j))"; assert src.count(ligne) == 1
ns0 = {}; exec('import numpy as np, os\nfrom scipy.spatial import cKDTree\n' + src, ns0)
ns1 = {}; exec('import numpy as np, os\nfrom scipy.spatial import cKDTree\n' + src.replace(ligne, ligne + " / 3.0"), ns1)
for seed in (1, 2, 3):
    A0, X, h = ns0['canonical'](1000, seed, nsw_per_N=0); T0 = mesure(A0, 1000)['triangles']; interne0 = sum(len(A0[i] & A0[j]) for i in range(1000) for j in A0[i] if i < j)
    A, X, h = ns0['canonical'](1000, seed); m = mesure(A, 1000); Ac, X, h = ns1['canonical'](1000, seed); mc = mesure(Ac, 1000)
    r = dict(graine=seed, triangles_distincts_initiaux=T0, compteur_initial_du_script=interne0, rapport=interne0 / T0, original=dict(triangles_par_sommet=m['triangles_par_sommet'], n_e_mediane=m['n_e_mediane'], n_e_moyenne=m['n_e_moyenne'], n_e_max=m['n_e_max']),
             corrige=dict(triangles_par_sommet=mc['triangles_par_sommet'], n_e_mediane=mc['n_e_mediane'], n_e_moyenne=mc['n_e_moyenne'], n_e_max=mc['n_e_max']))
    out['compteur'].append(r); print('compteur', r, flush=True); json.dump(out, open('x13_deux_moteurs.json', 'w'), indent=1)
