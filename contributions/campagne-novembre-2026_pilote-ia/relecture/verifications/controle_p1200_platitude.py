#!/usr/bin/env python3
"""Contrôle du pilote pour la page 1200 du master V346 (Partie CXXXII, §CXXXII.2, 25 juin) :
« la platitude globale est un équilibre, pas un héritage » : courbure d'Ollivier moyenne du Blob -0,031 ± 0,005,
du graphe géométrique (même nuage, même degré) +0,155 ± 0,004.
Question : cette valeur proche de zéro tient-elle quand on change le degré moyen kappa ou la température tau,
ou est-elle propre au point de travail (kappa = 6,6 ; tau = 0,50) ?
Convention du master : transport optimal exact, mesures uniformes sur les voisins (marche non paresseuse), distances 0 / 1 / 2.
Moteur de l'auteur déclaré canonique le 25 juin : blob_colab_verrouillage.canonical. N = 800, deux graines, 300 arêtes tirées au hasard.
Usage : controle_p1200_platitude.py "<chemin de blob colab verrouillage.py>"
"""
import sys
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import cKDTree
src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# ============================== SECTION A')], 'moteur_de_l_auteur', 'exec'), espace)
canonical = espace['canonical']

def ollivier(adj, x, y):
    A = sorted(adj[x]); B = sorted(adj[y]); na, nb = len(A), len(B)
    c = np.array([[0.0 if u == v else (1.0 if v in adj[u] else 2.0) for v in B] for u in A]).ravel()
    Aeq = np.zeros((na + nb, na * nb))
    for i in range(na): Aeq[i, i * nb:(i + 1) * nb] = 1
    for j in range(nb): Aeq[na + j, j::nb] = 1
    beq = np.concatenate([np.full(na, 1 / na), np.full(nb, 1 / nb)])
    return 1.0 - linprog(c, A_eq=Aeq, b_eq=beq, bounds=(0, None), method='highs').fun

def geometrique(X, N, E0, kappa):
    r = (kappa / (N * 4.18879)) ** (1 / 3.0)
    paires = cKDTree(X).query_pairs(1.3 * r, output_type='ndarray')
    d = np.linalg.norm(X[paires[:, 0]] - X[paires[:, 1]], axis=1)
    A = [set() for _ in range(N)]
    for k in np.argsort(d)[:E0]:
        a, b = int(paires[k, 0]), int(paires[k, 1]); A[a].add(b); A[b].add(a)
    return A

def moyenne(adj, N, rng):
    aretes = [(i, j) for i in range(N) for j in adj[i] if j > i]
    K = np.array([ollivier(adj, *aretes[k]) for k in rng.choice(len(aretes), size=min(300, len(aretes)), replace=False)])
    tri = sum(len(adj[i] & adj[j]) for (i, j) in aretes) / 3 / N
    return K.mean(), tri

N = 800
rng = np.random.default_rng(11)
print("Balayage en kappa (tau = 0,50)")
for kappa in (4.0, 5.0, 6.6, 8.0, 10.0, 12.0):
    b, g, tb, tg = [], [], [], []
    for seed in (1, 2):
        A, X, h = canonical(N, seed, kappa)
        m, t = moyenne(A, N, rng); b.append(m); tb.append(t)
        m, t = moyenne(geometrique(X, N, int(round(N * kappa / 2.0)), kappa), N, rng); g.append(m); tg.append(t)
    print(f"  kappa = {kappa:>4} : Blob {np.mean(b):+.3f} (graines {b[0]:+.3f}, {b[1]:+.3f}), {np.mean(tb):.2f} triangles par sommet ; "
          f"graphe géométrique {np.mean(g):+.3f}, {np.mean(tg):.2f} triangles par sommet")
print("Balayage en tau (kappa = 6,6)")
for tau in (0.15, 0.25, 0.50, 1.00, 2.00):
    espace['TAU'] = tau
    b, tb = [], []
    for seed in (1, 2):
        A, X, h = canonical(N, seed, 6.6)
        m, t = moyenne(A, N, rng); b.append(m); tb.append(t)
    print(f"  tau = {tau:>4} : Blob {np.mean(b):+.3f} (graines {b[0]:+.3f}, {b[1]:+.3f}), {np.mean(tb):.2f} triangles par sommet")
