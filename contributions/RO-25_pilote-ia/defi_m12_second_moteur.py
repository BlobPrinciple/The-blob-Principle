#!/usr/bin/env python3
"""DEFI-M12 — seconde implémentation indépendante de la méthode stationnaire.

Pilote IA du laboratoire (Claude, Anthropic), 27 octobre 2026.
Aucun code commun avec defi_m12_lenteur.py ni defi_m11_monte_carlo.py :
  - voisinages en mots de 64 bits, voisins communs par popcount ;
  - S_sim recalculé à partir des degrés tenus dans un tableau propre, sans terme Q incrémental ;
  - nombres aléatoires tirés par numpy.random.Generator (PCG64) en lots, passés au noyau ;
  - T_v par la diagonale de A³ (numpy, entiers), autocorrélation par somme directe
    (pas de FFT), moyenne commune à tous les sommets.
Même mesure (lam = n / tau, beta = 0,30, tau = 0,50), même noyau d'échange en loi.
Usage : python3 defi_m12_second_moteur.py [--tailles 17,33,65,129] [--reglage c2|c3] [--L 3000]
        [--sortie defi_m12_second_moteur.json]
"""
import json
import math
import pathlib
import sys

import numpy as np
from numba import njit

ICI = pathlib.Path(__file__).resolve().parent
B, TA = 0.30, 0.50


@njit(cache=True)
def pc(x):
    x = x - ((x >> np.uint64(1)) & np.uint64(0x5555555555555555))
    x = (x & np.uint64(0x3333333333333333)) + ((x >> np.uint64(2)) & np.uint64(0x3333333333333333))
    x = (x + (x >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    return int((x * np.uint64(0x0101010101010101)) >> np.uint64(56))


@njit(cache=True)
def nb_communs(bits, a, b):
    s = 0
    for w in range(bits.shape[1]):
        s += pc(bits[a, w] & bits[b, w])
    return s


@njit(cache=True)
def a_lien(bits, a, b):
    return (bits[a, b >> 6] >> np.uint64(b & 63)) & np.uint64(1)


@njit(cache=True)
def poser(bits, a, b, val):
    m = np.uint64(1) << np.uint64(b & 63)
    if val:
        bits[a, b >> 6] |= m
    else:
        bits[a, b >> 6] &= ~m


@njit(cache=True)
def score(tri, sdeg2, n, M):
    moy = 2.0 * M / n
    v = sdeg2 / n - moy * moy
    return math.log(1.0 + tri) - B * math.sqrt(max(v, 0.0)) / moy


def chaine(n, c, L, delta, graine):
    M = c * n
    g = np.random.Generator(np.random.PCG64(graine))
    toutes = [(a, b) for a in range(n) for b in range(a + 1, n)]
    E = np.array([toutes[i] for i in g.permutation(len(toutes))[:M]], dtype=np.int64)
    W = (n + 63) // 64
    bits = np.zeros((n, W), dtype=np.uint64)
    dg = np.zeros(n, dtype=np.int64)
    for a, b in E:
        poser(bits, a, b, True)
        poser(bits, b, a, True)
        dg[a] += 1
        dg[b] += 1

    def tv():
        A = np.zeros((n, n), dtype=np.int64)
        for a, b in E:
            A[a, b] = A[b, a] = 1
        return np.diag(A @ A @ A) // 2
    t = tv()
    st = np.array([t.sum() / 3.0, float((dg ** 2).sum())])
    lam = n / TA

    def faire(nsteps):
        reste = nsteps
        while reste > 0:
            U = g.random((reste + 64, 4))
            fait = avancer_compte(bits, E, dg, st, n, lam, U, reste)
            reste -= fait
    faire(200 * delta * M)
    X = np.zeros((L, n))
    for i in range(L):
        faire(delta * M)
        X[i] = tv()
        assert abs(X[i].sum() / 3 - st[0]) < 1e-9
        assert st[1] == float((dg ** 2).sum()) and (np.bincount(E.ravel(), minlength=n) == dg).all()
    return X


@njit(cache=True)
def set_unique(a, b, x, y):
    r = np.array([a, b, x, y])
    for i in range(4):
        for j in range(i):
            if r[i] == r[j]:
                r[i] = -1
                break
    return r


@njit(cache=True)
def avancer_compte(bits, E, dg, st, n, lam, U, maxprop):
    """Exécute au plus maxprop propositions avec les lignes de U ; renvoie le nombre fait."""
    M = E.shape[0]
    K = U.shape[0]
    dg2 = np.zeros(n, dtype=np.int64)
    j = 0
    p = 0
    while p < maxprop and j < K:
        e = min(int(U[j, 0] * M), M - 1)
        a, b = E[e, 0], E[e, 1]
        x = min(int(U[j, 1] * n), n - 1)
        y = min(int(U[j, 2] * n), n - 1)
        u = U[j, 3]
        j += 1
        ok = True
        while x == y or a_lien(bits, x, y):
            if j >= K:
                ok = False
                break
            x = min(int(U[j, 1] * n), n - 1)
            y = min(int(U[j, 2] * n), n - 1)
            j += 1
        if not ok:
            break
        poser(bits, a, b, False)
        poser(bits, b, a, False)
        perte = nb_communs(bits, a, b)
        gain = nb_communs(bits, x, y)
        tri2 = st[0] - perte + gain
        # somme des carrés des degrés après l'échange, recalculée sur les sommets touchés
        # (x ou y peut coïncider avec a ou b : on agrège les variations par sommet)
        s2 = st[1]
        for w in (a, b, x, y):
            dg2[w] = dg[w]
        dg2[a] -= 1
        dg2[b] -= 1
        dg2[x] += 1
        dg2[y] += 1
        s2 = st[1]
        for w in set_unique(a, b, x, y):
            if w >= 0:
                s2 += dg2[w] ** 2 - dg[w] ** 2
        d = lam * (score(tri2, s2, n, M) - score(st[0], st[1], n, M))
        if d >= 0 or u < math.exp(d):
            poser(bits, x, y, True)
            poser(bits, y, x, True)
            dg[a] -= 1
            dg[b] -= 1
            dg[x] += 1
            dg[y] += 1
            E[e, 0] = x
            E[e, 1] = y
            st[0] = tri2
            st[1] = s2
        else:
            poser(bits, a, b, True)
            poser(bits, b, a, True)
        p += 1
    return p


def acf_directe(X, kmax):
    m = X.mean()
    Y = X - m
    v = (Y * Y).mean()
    L = len(Y)
    return np.array([(Y[:L - k] * Y[k:]).mean() / v for k in range(kmax)])


def premier_sous(C, s, delta):
    i = int(np.argmax(C <= s))
    if C[i] > s:
        return None
    return (i - 1 + (C[i - 1] - s) / (C[i - 1] - C[i])) * delta


def main():
    def opt(nom, d):
        return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else d
    tailles = [int(x) for x in opt("--tailles", "17,33,65,129").split(",")]
    c = 3 if opt("--reglage", "c2") == "c3" else 2
    L = int(opt("--L", "3000"))
    out = []
    for n in tailles:
        delta = max(1, int(round(0.6 * (n / 16.0) ** 3)))
        for j in range(2):
            X = chaine(n, c, L, delta, 777 + 31 * n + j)
            C = acf_directe(X, min(400, L // 3))
            r = {"n": n, "c": c, "delta": delta, "chaine": j, "Tv_moy": float(X.mean()),
                 "t_demi": premier_sous(C, 0.5, delta), "t_1e": premier_sous(C, math.exp(-1), delta),
                 "t_01": premier_sous(C, 0.1, delta)}
            out.append(r)
            print(r, flush=True)
            (ICI / opt("--sortie", "defi_m12_second_moteur.json")).write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
