#!/usr/bin/env python3
"""X-13 bis [EXPLORATOIRE, complement declare apres coup de C-180c partie II] -- meme essai du terme en b (cand_factor = 4,1, N = 1000, graines 11 a 13), mais avec le compteur
de triangles CORRIGE (triangles distincts des l'initialisation), pour savoir si le resultat de C-180c tient sans l'anomalie de comptage de canonical() (Claude, 16 novembre 2026)."""
import json, sys
src = open('c180c.py').read(); ligne = "    ntri = float(sum(len(A[i] & A[j]) for i in range(N) for j in A[i] if i < j))"; assert src.count(ligne) == 1
src = src.split("if __name__ == '__main__':")[0].replace(ligne, ligne + " / 3.0"); ns = {'__file__': 'c180c.py', '__name__': 'c180c_corrige'}; exec(compile(src, 'c180c.py (compteur corrige)', 'exec'), ns)
seed, b = int(sys.argv[1]), float(sys.argv[2]); A, X = ns['avec_b'](1000, seed, b, cand_factor=4.1); m = ns['mesure'](A, 1000)
r = dict(graine=seed, b=b, triangles_par_sommet=m['triangles_par_sommet'], tetraedres_par_sommet=m['tetraedres_par_sommet'], n_e_mediane=m['n_e_mediane'], n_e_moyenne=m['n_e_moyenne'], n_e_max=m['n_e_max'], part_aretes_sans_tetraedre=m['part_aretes_sans_tetraedre'],
         part_4_5_6=m['part_4_5_6'], plus_grande_clique=m['plus_grande_clique'], sommets_isoles=m['sommets_isoles'])
json.dump(r, open(f'x13_bis_{seed}_{b}.json', 'w')); print(r, flush=True)
