#!/usr/bin/env python3
"""X-35 : vérification du classeur. Sur deux paires de graphes engendrées par la même recette des deux côtés (sommes de contrôle
identiques), mon classeur doit rendre les mêmes effectifs que classify_phases du programme de l'auteur (exécuté sur sa machine).
Effectifs de l'auteur, relevés le 28 novembre 2026 (graine : somme_eq, somme_ev, [(L, DM, b) pour theta = 0,338 ; 0,5 ; 0,6]) :"""
import numpy as np
from types import SimpleNamespace
from x34_replication_blob_canonique import cliques4
from x35_fractions_kappa4 import classer
AUTEUR = {7: (50632299, 50447171, [(214, 102, 84), (147, 193, 60), (100, 259, 41)]),
          8: (59765718, 58914788, [(230, 78, 92), (162, 179, 59), (122, 241, 37)])}
def gen(seed=7, N=400, r=0.17):
    rng = np.random.default_rng(seed)
    P = rng.random((N, 3))
    D = np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(-1))
    U = rng.random((N, N))
    a0 = [set() for _ in range(N)]; a1 = [set() for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            if D[i, j] < r:
                a0[i].add(j); a0[j].add(i)
                if U[i, j] < 0.7: a1[i].add(j); a1[j].add(i)
            elif D[i, j] < 1.3 * r and U[i, j] < 0.25:
                a1[i].add(j); a1[j].add(i)
    return a0, a1
def somme(a): return sum(i * j for i in range(len(a)) for j in a[i] if j > i)
ok = True
for seed, (s0, s1, ref) in AUTEUR.items():
    a0, a1 = gen(seed); N = len(a0)
    memes = (somme(a0), somme(a1)) == (s0, s1)
    K4 = cliques4(SimpleNamespace(N=N, adj=a0))
    c = classer(a0, a1, N, K4, [0.338, 0.5, 0.6])
    moi = [tuple(round(c['par_theta'][str(t)][k] * N) for k in ('f_L', 'f_DM', 'f_b')) for t in (0.338, 0.5, 0.6)]
    print(seed, 'graphes identiques :', memes, '| auteur', ref, '| moi', moi, '|', 'ACCORD' if moi == ref else 'ECART')
    ok &= memes and moi == ref
print('CLASSEUR FIDELE' if ok else 'CLASSEUR NON FIDELE')
