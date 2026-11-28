#!/usr/bin/env python3
"""Contrôles du pilote pour les pages 896-897 et 917-920 du master V346.

1. Grammaire des possibles : énumération des 2^6 et 2^10 graphes sur 4 et 5 sommets
   (nombres de triangles et de tétraèdres atteignables).
2. Étalonnage de la lecture « au plateau » de la dimension spectrale
   d_s(t) = -2 d ln Tr exp(-tL) / d ln t (laplacien normalisé, spectre complet)
   sur des témoins de dimension connue, aux tailles du master (N = 400 à 1 000).
   Ce n'est PAS le script du master (absent du dépôt) : c'est mon implémentation.
   Choix déclarés : fenêtre de largeur un facteur 2 en t, cherchée dans t entre 3 et 30
   (le master rapporte des plateaux entre t = 4,4 et t = 11,9), variance minimale.
"""
import itertools
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree


def spectres(n):
    aretes = list(itertools.combinations(range(n), 2))
    tris = list(itertools.combinations(range(n), 3))
    k4s = list(itertools.combinations(range(n), 4))
    st, sk = set(), set()
    for masque in range(1 << len(aretes)):
        E = {e for i, e in enumerate(aretes) if masque >> i & 1}
        st.add(sum(all(p in E for p in itertools.combinations(T, 2)) for T in tris))
        sk.add(sum(all(p in E for p in itertools.combinations(K, 2)) for K in k4s))
    return sorted(st), sorted(sk)


def rgg(N, kappa, dim, rng):
    P = rng.random((N, dim))
    arbre = cKDTree(P)
    bas, haut = 0.0, 0.7
    for _ in range(45):
        r = (bas + haut) / 2
        if 2 * len(arbre.query_pairs(r)) / N < kappa:
            bas = r
        else:
            haut = r
    pr = np.array(sorted(arbre.query_pairs(haut)))
    A = sp.coo_matrix((np.ones(len(pr)), (pr[:, 0], pr[:, 1])), shape=(N, N))
    return (A + A.T).tocsr()


def grille(n, dim):
    idx = np.arange(n ** dim).reshape((n,) * dim)
    lig, col = [], []
    for ax in range(dim):
        lig += list(np.take(idx, range(n - 1), axis=ax).ravel())
        col += list(np.take(idx, range(1, n), axis=ax).ravel())
    A = sp.coo_matrix((np.ones(len(lig)), (lig, col)), shape=(n ** dim, n ** dim))
    return (A + A.T).tocsr()


def composante(A):
    _, lab = connected_components(A, directed=False)
    garde = np.where(lab == np.bincount(lab).argmax())[0]
    return A[garde][:, garde]


def valeurs_propres(A):
    d = np.asarray(A.sum(1)).ravel()
    Dm = sp.diags(1 / np.sqrt(d))
    L = np.eye(A.shape[0]) - (Dm @ A @ Dm).toarray()
    return np.clip(np.linalg.eigvalsh(L), 0, None)


TS = np.logspace(-1, 3, 801)          # 200 points par décade
REPERES = [3, 5, 8, 12, 20, 30]


def profil(lam):
    W = np.exp(-np.outer(TS, lam))
    return 2 * TS * (W * lam).sum(1) / W.sum(1)


def lecture(ds, facteur=2.0, tmin=3.0, tmax=30.0):
    w = int(round(np.log10(facteur) * 200))
    meilleur = None
    for i in range(len(TS) - w):
        if TS[i] < tmin or TS[i + w] > tmax:
            continue
        v = ds[i:i + w + 1].var()
        if meilleur is None or v < meilleur[0]:
            meilleur = (v, ds[i:i + w + 1].mean(), TS[i], TS[i + w])
    return meilleur


def ligne(nom, A):
    A = composante(A)
    ds = profil(valeurs_propres(A))
    rep = "  ".join(f"{ds[np.argmin(abs(TS - t))]:.2f}" for t in REPERES)
    _, val, t0, t1 = lecture(ds)
    deg = A.sum() / A.shape[0]
    print(f"{nom:<26} N={A.shape[0]:>5} deg={deg:4.1f}  max={ds.max():.2f}  d_s(t)= {rep}   plateau={val:.2f} sur t=[{t0:.1f};{t1:.1f}]")
    return val


print("1. Grammaire des possibles")
for n in (4, 5):
    st, sk = spectres(n)
    print(f"   {n} sommets : triangles atteignables {st} ; tétraèdres atteignables {sk}")

print("\n2. Lecture au plateau de d_s(t) sur des témoins ; repères t =", REPERES)
rng = np.random.default_rng(20261128)
res = {}
for nom, fab in [
    ("réseau carré 20x20", lambda: grille(20, 2)),
    ("réseau carré 32x32", lambda: grille(32, 2)),
    ("réseau cubique 7^3", lambda: grille(7, 3)),
    ("réseau cubique 10^3", lambda: grille(10, 3)),
    ("réseau hypercubique 5^4", lambda: grille(5, 4)),
    ("réseau hypercubique 6^4", lambda: grille(6, 4)),
]:
    ligne(nom, fab())
for nom, N, kappa, dim in [
    ("graphe géom. 2D k=6,6", 1000, 6.6, 2),
    ("graphe géom. 3D k=6,6", 400, 6.6, 3),
    ("graphe géom. 3D k=6,6", 1000, 6.6, 3),
    ("graphe géom. 3D k=4", 1000, 4.0, 3),
    ("graphe géom. 4D k=6,6", 1000, 6.6, 4),
]:
    vals = [ligne(nom, rgg(N, kappa, dim, rng)) for _ in range(4)]
    print(f"   -> {nom}, N={N} : plateau moyen {np.mean(vals):.2f}, écart-type {np.std(vals):.2f} (4 tirages)")
