#!/usr/bin/env python3
"""Contrôle du pilote pour les pages 1178 à 1183 du master V346 (annexes du 21 juin) : le moteur que le master déclare
canonique à partir de cette date, blob_colab_verrouillage.canonical (réservoir de volume 2,6 fois la boule de Rips, soit
un rayon 2,6^(1/3) = 1,375 r ; arêtes de départ tirées au hasard dans le réservoir), et le « théorème de signe de la parité ».
Mesures, N = 1 500, graines 1 à 3, avec les fonctions de l'auteur (canonical, edges_tris, parity_face) :
  - triangles par sommet et dispersion des degrés : état de départ (aucun pas), Blob, graphe géométrique de même degré ;
  - P = part des paires de tétraèdres partageant une face dont les apex ont le même signe de volume (même côté de la face) ;
  - la même mesure après réflexion des coordonnées (x -> 1 - x) : une quantité qui viole la parité doit changer ;
  - distance apex-apex selon le côté ; nombre de tétraèdres portés par une face.
Usage : controle_p1178-1183_moteur_de_juin.py "<chemin de blob colab verrouillage.py>"
"""
import sys
import numpy as np
from scipy.spatial import cKDTree
src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# ============================== SECTION A')], 'moteur_de_l_auteur', 'exec'), espace)
canonical, edges_tris, parity_face = espace['canonical'], espace['edges_tris'], espace['parity_face']

def decrit(A, X, N):
    edges, eidx, tris = edges_tris(A, N)
    deg = np.array([len(s) for s in A], float)
    P, tot, chi = parity_face(A, X, tris)
    return dict(tri=len(tris) / N, cv=deg.std() / deg.mean(), P=P, paires=tot, chi=chi, tris=tris)

def geometrique(X, N, E0):
    arbre = cKDTree(X)
    r = (6.6 / (N * 4.18879)) ** (1 / 3.0)
    paires = arbre.query_pairs(1.3 * r, output_type='ndarray')
    d = np.linalg.norm(X[paires[:, 0]] - X[paires[:, 1]], axis=1)
    A = [set() for _ in range(N)]
    for k in np.argsort(d)[:E0]:
        a, b = int(paires[k, 0]), int(paires[k, 1]); A[a].add(b); A[b].add(a)
    return A

N = 1500
print(f"rayon du réservoir / rayon de Rips = {2.6 ** (1/3):.3f} (moteur de juin) ; 1,6 (moteur du 30 mai)")
cumul = {'meme': [], 'oppose': []}
for seed in (1, 2, 3):
    A0, X0, h = canonical(N, seed, nsw_per_N=0)
    d0 = decrit(A0, X0, N)
    A, X, h = canonical(N, seed)
    d1 = decrit(A, X, N)
    G = geometrique(X, N, int(round(N * 6.6 / 2.0)))
    dg = decrit(G, X, N)
    Xm = X.copy(); Xm[:, 0] = 1.0 - Xm[:, 0]
    dm = decrit(A, Xm, N)
    # distances apex-apex et multiplicité des faces
    mult = []
    for (i, j, k) in d1['tris']:
        apex = list(A[i] & A[j] & A[k])
        mult.append(len(apex))
        if len(apex) >= 2:
            n = np.cross(X[j] - X[i], X[k] - X[i])
            s = [np.sign(np.dot(X[l] - X[i], n)) for l in apex]
            for a in range(len(apex)):
                for b in range(a + 1, len(apex)):
                    cumul['meme' if s[a] == s[b] else 'oppose'].append(np.linalg.norm(X[apex[a]] - X[apex[b]]))
    mult = np.array(mult); portees = mult[mult >= 1]
    print(f"graine {seed} :")
    print(f"   départ (aucun pas)       triangles/sommet {d0['tri']:.2f} ; dispersion des degrés {d0['cv']:.3f} ; P = {d0['P']:.4f} sur {d0['paires']} paires")
    print(f"   graphe géométrique       triangles/sommet {dg['tri']:.2f} ; dispersion des degrés {dg['cv']:.3f} ; P = {dg['P']:.4f} sur {dg['paires']} paires")
    print(f"   Blob (80 N pas)          triangles/sommet {d1['tri']:.2f} ; dispersion des degrés {d1['cv']:.3f} ; P = {d1['P']:.4f} sur {d1['paires']} paires ; <chi> = {d1['chi']:+.4f}")
    print(f"   Blob vu dans un miroir   P = {dm['P']:.4f} ; <chi> = {dm['chi']:+.4f}")
    print(f"   faces du Blob : {100*np.mean(mult == 0):.0f} % sans tétraèdre ; parmi les autres, médiane {np.median(portees):.0f} tétraèdres par face, "
          f"{100*np.mean(portees <= 2):.0f} % en portent deux au plus, maximum {portees.max()}")
print(f"distance apex-apex, trois graines : même côté {np.mean(cumul['meme']):.4f} ({len(cumul['meme'])} paires) ; "
      f"côtés opposés {np.mean(cumul['oppose']):.4f} ({len(cumul['oppose'])} paires) ; part du même côté {len(cumul['meme'])/(len(cumul['meme'])+len(cumul['oppose'])):.4f}")
