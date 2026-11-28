#!/usr/bin/env python3
"""Contrôle du pilote pour les pages 987-989 du master V346 (Partie LXXXIV, « flèche du temps chirale », 5 juin).

Moteur : le moteur vivant de l'auteur (classe BlobVivant de « blob scaling colab.py »), inchangé. Dans ce moteur, le numéro
d'un sommet est son rang de naissance. « Chiralité » d'un tétraèdre = signe du volume orienté, sommets rangés par numéro.
Identité testée paire par paire (deux tétraèdres partageant une face a<b<c, d'apex d et e) :
    même chiralité  <=>  (d et e du même côté de la face)  XOR  (rangs d'insertion de d et e de parités différentes).
Si elle est exacte, P(même chiralité) est fixé par deux nombres : la part des paires dont les apex sont du même côté,
et la part des paires dont les rangs ont même parité, laquelle dépend de l'ordre des naissances.
Usage : controle_p987-989_fleche_chirale.py "<chemin de blob scaling colab.py>" [balayages]
"""
import sys, itertools
import numpy as np

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# ----------------------------- MESURE AUX PALIERS')], 'moteur_vivant_de_l_auteur', 'exec'), espace)
BlobVivant = espace['BlobVivant']
nb = int(sys.argv[2]) if len(sys.argv) > 2 else 26

def chir(P, t):
    a, b, c, d = sorted(t)
    return np.sign(np.linalg.det(np.array([P[b] - P[a], P[c] - P[a], P[d] - P[a]])))

def mesure(bl):
    N = bl.N; P = np.array(bl.pts); adj = bl.adj
    tot = ident = 0
    C = {k: [0, 0, 0] for k in ('apex tous deux plus jeunes que la face', 'autres, parités égales', 'parités différentes')}
    for i in range(N):
        for j in adj[i]:
            if j <= i: continue
            for k in adj[i] & adj[j]:
                if k <= j: continue
                apex = sorted(adj[i] & adj[j] & adj[k])
                if len(apex) < 2: continue
                nrm = np.cross(P[j] - P[i], P[k] - P[i])
                for d, e in itertools.combinations(apex, 2):
                    cote = np.sign(np.dot(nrm, P[d] - P[i])) == np.sign(np.dot(nrm, P[e] - P[i]))
                    chi = chir(P, (i, j, k, d)) == chir(P, (i, j, k, e))
                    rd = sum(x < d for x in (i, j, k)); re_ = sum(x < e for x in (i, j, k))
                    par = (rd - re_) % 2 == 0
                    tot += 1; ident += (chi == (cote == par))
                    cle = 'apex tous deux plus jeunes que la face' if rd == 3 and re_ == 3 else ('autres, parités égales' if par else 'parités différentes')
                    C[cle][0] += 1; C[cle][1] += cote; C[cle][2] += chi
    return tot, ident, C

cumul = {}
for seed in (1, 2, 3):
    bl = BlobVivant(N0=100, seed=seed)
    for s in range(1, nb + 1):
        bl.step()
        if s in (14, 20, nb):
            tot, ident, C = mesure(bl)
            c = cumul.setdefault(s, [0, 0, {k: [0, 0, 0] for k in C}, 0])
            c[0] += tot; c[1] += ident; c[3] += bl.N
            for k in C:
                for q in range(3): c[2][k][q] += C[k][q]
for s, (tot, ident, C, Ns) in sorted(cumul.items()):
    n_cote = sum(v[1] for v in C.values()); n_chi = sum(v[2] for v in C.values())
    print(f"balayage {s} (3 graines, N moyen {Ns//3}) : {tot} paires liées par une face ; identité vérifiée sur {ident} ({100*ident/max(tot,1):.1f} %)")
    print(f"    ensemble : P(même côté) = {n_cote/tot:.3f} ; P(même chiralité) = {n_chi/tot:.3f}")
    for k, (n, co, ch) in C.items():
        if n: print(f"    {k:<40} {100*n/tot:5.1f} % des paires ; P(même côté) = {co/n:.3f} ; P(même chiralité) = {ch/n:.3f}")
