#!/usr/bin/env python3
"""Contrôle du pilote pour les pages 930-933 du master V346 (Partie LXVII, « échelle intrinsèque », 3 juin).

Le master mesure, sur le profil d_s(t) du noyau de la chaleur (laplacien normalisé), le point d'inflexion de la montée,
t_infl ≈ 1,29, stable de N = 1 200 à 8 138, et la valeur ≈ 0,6 du côté des petites échelles (t = 0,3).
Question : ces deux nombres distinguent-ils le Blob ? Je calcule les mêmes grandeurs sur le graphe de départ, sur le Blob
(moteur de l'auteur, inchangé), sur un réseau cubique et sur des graphes réguliers aléatoires SANS géométrie.
Rappel analytique : la moyenne des valeurs propres du laplacien normalisé vaut 1 (graphe sans sommet isolé),
donc d_s(t) = 2 t <lambda>_t vaut 2t aux petits t, pour tout graphe.
Usage : controle_p930-933_echelle.py "<chemin de gap curl colab.py>"
"""
import sys
import numpy as np
import scipy.sparse as sp

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical = espace['build_initial'], espace['run_mcmc_canonical']
TS = np.logspace(np.log10(0.05), np.log10(60), 1201)

def depuis_adj(adj, N):
    lig = [i for i in range(N) for j in adj[i]]; col = [j for i in range(N) for j in adj[i]]
    return sp.coo_matrix((np.ones(len(lig)), (lig, col)), shape=(N, N)).tocsr()

def grille(n, dim=3):
    idx = np.arange(n ** dim).reshape((n,) * dim); lig, col = [], []
    for ax in range(dim):
        lig += list(np.take(idx, range(n - 1), axis=ax).ravel()); col += list(np.take(idx, range(1, n), axis=ax).ravel())
    A = sp.coo_matrix((np.ones(len(lig)), (lig, col)), shape=(n ** dim, n ** dim)); return (A + A.T).tocsr()

def regulier_aleatoire(N, d, rng):
    while True:
        bouts = np.repeat(np.arange(N), d); rng.shuffle(bouts)
        a, b = bouts[0::2], bouts[1::2]
        if (a == b).any(): continue
        paires = {(min(x, y), max(x, y)) for x, y in zip(a, b)}
        if len(paires) < len(a): continue
        lig = [p[0] for p in paires]; col = [p[1] for p in paires]
        A = sp.coo_matrix((np.ones(len(lig)), (lig, col)), shape=(N, N)); return (A + A.T).tocsr()

def mesure(nom, A):
    d = np.asarray(A.sum(1)).ravel(); Dm = sp.diags(1 / np.sqrt(np.maximum(d, 1)))
    lam = np.clip(np.linalg.eigvalsh(np.eye(A.shape[0]) - (Dm @ A @ Dm).toarray()), 0, None)
    W = np.exp(-np.outer(TS, lam)); ds = 2 * TS * (W * lam).sum(1) / W.sum(1)
    im = int(ds.argmax()); pente = np.gradient(ds[:im + 1], np.log(TS[:im + 1])); ii = int(pente.argmax())
    print(f"{nom:<44} N={A.shape[0]:>5} degré={d.mean():4.1f}  d_s(0,3)={ds[np.argmin(abs(TS - 0.3))]:.2f}  t_infl={TS[ii]:.2f}  max={ds.max():.2f} à t={TS[im]:.1f}")
    return TS[ii]

rng = np.random.default_rng(7)
for seed in (1, 2):
    pts, adj0, pool, E0 = build_initial(1000, seed, 6.6)
    mesure(f"graphe de départ (graine {seed})", depuis_adj(adj0, 1000))
    mesure(f"Blob, moteur canonique (graine {seed})", depuis_adj(run_mcmc_canonical(pts, adj0, pool, 1000, E0, seed), 1000))
mesure("réseau cubique 10^3", grille(10))
for d in (5, 6, 7, 9):
    mesure(f"graphe régulier aléatoire de degré {d} (sans géométrie)", regulier_aleatoire(1000, d, rng))
