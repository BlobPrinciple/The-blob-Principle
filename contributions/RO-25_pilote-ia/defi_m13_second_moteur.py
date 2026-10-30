#!/usr/bin/env python3
"""DEFI-M13 — seconde implémentation indépendante du profil P(T_v).

Pilote IA du laboratoire (Claude, Anthropic), 30 octobre 2026.
Aucun code commun avec defi_m13_profil.py ni defi_m12_lenteur.py :
  - voisinages en mots de 64 bits, voisins communs par popcount ;
  - T_0 recalculé en entier après chaque échange proposé (somme sur les voisins de 0 des
    voisins communs, divisée par 2), sans mise à jour incrémentale ;
  - nombres aléatoires tirés par numpy.random.Generator (PCG64) en lots ;
  - autre algorithme de biais : variante « 1/t » de Wang–Landau (Belardinelli et Pereyra,
    2007), critère « toutes les cases visitées » au lieu d'un critère de platitude ;
    production à biais fixé, P ∝ H·exp(−w). (Une première version, récurrence
    multicanonique de Berg, ne convergeait pas à n ≥ 129 : cases intérieures vides.)
Même mesure : pi ∝ exp(lam · S_sim), S_sim = log(1 + n_tri) − 0,30 · D, lam = n / 0,50 par défaut,
D = écart-type de population des degrés / degré moyen ; même noyau d'échange en loi
(une arête uniforme, une non-arête uniforme) ; même support [0, tcap] que le premier moteur
(lu dans son JSON) pour comparer des lois conditionnelles identiques.
Usage : python3 defi_m13_second_moteur.py [--points c2:33,c2:65,...]
        [--source defi_m13_profil_c2.json] [--sortie defi_m13_second_moteur.json]
"""
import json
import math
import pathlib
import sys
import time

import numpy as np
from numba import njit

ICI = pathlib.Path(__file__).resolve().parent
BB, TT = 0.30, 0.50
F_FIN = 1e-5          # arrêt de l'algorithme 1/t
ETAPES_MAX = 2_000_000  # plafond, en balayages


@njit(cache=True)
def popc(x):
    x = x - ((x >> np.uint64(1)) & np.uint64(0x5555555555555555))
    x = (x & np.uint64(0x3333333333333333)) + ((x >> np.uint64(2)) & np.uint64(0x3333333333333333))
    x = (x + (x >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    return int((x * np.uint64(0x0101010101010101)) >> np.uint64(56))


@njit(cache=True)
def inter(bits, a, b):
    s = 0
    for k in range(bits.shape[1]):
        s += popc(bits[a, k] & bits[b, k])
    return s


@njit(cache=True)
def lien(bits, a, b):
    return ((bits[a, b >> 6] >> np.uint64(b & 63)) & np.uint64(1)) == np.uint64(1)


@njit(cache=True)
def regler(bits, a, b, val):
    msk = np.uint64(1) << np.uint64(b & 63)
    if val:
        bits[a, b >> 6] |= msk
        bits[b, a >> 6] |= np.uint64(1) << np.uint64(a & 63)
    else:
        bits[a, b >> 6] &= ~msk
        bits[b, a >> 6] &= ~(np.uint64(1) << np.uint64(a & 63))


@njit(cache=True)
def tri_sommet0(bits, n):
    s = 0
    for a in range(1, n):
        if lien(bits, 0, a):
            s += inter(bits, 0, a)
    return s // 2


@njit(cache=True)
def valeur(tri, sd2, n, M):
    moy = 2.0 * M / n
    var = sd2 / n - moy * moy
    return math.log(1.0 + tri) - BB * math.sqrt(max(var, 0.0)) / moy


@njit(cache=True)
def avancer(bits, E, dg, st, n, lam, w, tcap, U, hist, f):
    """st = [tri, Σd², T_0]. Une proposition par ligne de U (4 uniformes) ; les tirages
    (x, y) déjà reliés ou confondus sont refusés sur place (même loi que « retirer jusqu'à
    trouver une non-arête » : la proposition retenue est uniforme sur les non-arêtes)."""
    M = E.shape[0]
    fait = 0
    for j in range(U.shape[0]):
        e = min(int(U[j, 0] * M), M - 1)
        a, b = E[e, 0], E[e, 1]
        x = min(int(U[j, 1] * n), n - 1)
        y = min(int(U[j, 2] * n), n - 1)
        if x == y or lien(bits, x, y):
            continue  # nouveau tirage de (x, y) : ce n'est pas une proposition
        fait += 1
        cab = inter(bits, a, b)
        regler(bits, a, b, False)
        cxy = inter(bits, x, y)
        regler(bits, x, y, True)
        t0n = tri_sommet0(bits, n)
        trin = st[0] - cab + cxy
        d2 = st[1] + (-2 * dg[a] + 1) + (-2 * dg[b] + 1)
        dg[a] -= 1
        dg[b] -= 1
        d2 += 2 * dg[x] + 1 + 2 * dg[y] + 1
        dg[x] += 1
        dg[y] += 1
        acc = False
        if t0n <= tcap:
            ds = lam * (valeur(trin, d2, n, M) - valeur(st[0], st[1], n, M)) + w[t0n] - w[int(st[2])]
            acc = ds >= 0.0 or U[j, 3] < math.exp(ds)
        if acc:
            E[e, 0] = x
            E[e, 1] = y
            st[0] = trin
            st[1] = d2
            st[2] = t0n
        else:
            regler(bits, x, y, False)
            regler(bits, a, b, True)
            dg[x] -= 1
            dg[y] -= 1
            dg[a] += 1
            dg[b] += 1
        hist[int(st[2])] += 1
        if f > 0.0:
            w[int(st[2])] -= f
    return fait


class Chaine:
    def __init__(self, n, M, lam, tcap, graine):
        self.n, self.M, self.lam, self.tcap = n, M, lam, tcap
        self.g = np.random.Generator(np.random.PCG64(graine))
        g = self.g
        # départ : clique de taille q contenant le sommet 0, reste uniforme
        q = int((1 + math.isqrt(1 + 8 * M)) // 2)
        while q * (q - 1) // 2 > M:
            q -= 1
        q = max(3, int(0.6 * q))
        noyau = [0] + list(g.choice(np.arange(1, n), size=q - 1, replace=False))
        pris = set()
        for i in range(q):
            for j in range(i + 1, q):
                pris.add((min(noyau[i], noyau[j]), max(noyau[i], noyau[j])))
        while len(pris) < M:
            a, b = g.integers(0, n, 2)
            if a != b:
                pris.add((min(a, b), max(a, b)))
        self.E = np.array(sorted(pris), dtype=np.int64)
        self.bits = np.zeros((n, (n + 63) // 64), dtype=np.uint64)
        self.dg = np.zeros(n, dtype=np.int64)
        for a, b in self.E:
            regler(self.bits, a, b, True)
            self.dg[a] += 1
            self.dg[b] += 1
        A = np.zeros((n, n), dtype=np.int64)
        A[self.E[:, 0], self.E[:, 1]] = 1
        A[self.E[:, 1], self.E[:, 0]] = 1
        t0 = int(np.diag(A @ A @ A)[0] // 2)
        if t0 > tcap:
            raise RuntimeError("départ hors support")
        self.st = np.array([float(np.trace(A @ A @ A) // 6), float((self.dg ** 2).sum()), float(t0)])

    def courir(self, nprop, w, hist, f=0.0):
        reste = nprop
        while reste > 0:
            U = self.g.random((min(reste, 2_000_000) + 1000, 4))
            reste -= avancer(self.bits, self.E, self.dg, self.st, self.n, self.lam, w, self.tcap, U, hist, f)

    def verifier(self):
        n = self.n
        A = np.zeros((n, n), dtype=np.int64)
        A[self.E[:, 0], self.E[:, 1]] = 1
        A[self.E[:, 1], self.E[:, 0]] = 1
        A3 = np.diag(A @ A @ A)
        assert int(A3.sum() // 6) == int(self.st[0])
        assert int(A3[0] // 2) == int(self.st[2])
        assert float((A.sum(1) ** 2).sum()) == self.st[1]


def un_point(reg, n, lam, tcap, masque, graine):
    M = (3 if reg == "c3" else 2) * n
    ch = Chaine(n, M, lam, tcap, graine)
    t_deb = time.time()
    w = np.zeros(tcap + 1)
    h = np.zeros(tcap + 1)
    ch.courir(300 * M, w, h)
    # algorithme « 1/t » de Belardinelli et Pereyra (2007) : f divisé par 2 dès que toutes
    # les cases du support ont été visitées ; puis f = (nombre de cases) / t quand f < 1/t.
    f = 1.0
    nb = tcap + 1
    t = 0
    bloc = 20 * M
    while True:
        h = np.zeros(nb)
        while True:
            ch.courir(bloc, w, h, f)
            t += bloc
            if h[masque].min() > 0 or f <= nb / t:
                break
        if f <= nb / t:
            break
        f /= 2.0
    while f > F_FIN:
        h = np.zeros(nb)
        ch.courir(bloc, w, h, f)
        t += bloc
        f = nb / t
        if t > ETAPES_MAX * M:
            break
    w -= w.max()
    ch.verifier()
    blocs = []
    for b in range(8):
        h = np.zeros(tcap + 1)
        ch.courir(5000 * M, w, h)
        blocs.append(h)
    ch.verifier()
    Hs = np.sum(blocs, axis=0)
    lp = np.full(tcap + 1, np.nan)
    ok = Hs > 0
    lp[ok] = np.log(Hs[ok]) - w[ok]
    lp -= np.nanmax(lp)
    return {"reglage": reg, "n": n, "M": M, "lam": lam, "tcap": tcap, "graine": graine, "pas_1_sur_t": t, "f_final": f,
            "logP": [None if not np.isfinite(v) else float(v) for v in lp],
            "platitude_production": float(Hs.min() / Hs.mean()), "H_blocs": [b.tolist() for b in blocs],
            "w": w.tolist(), "duree_s": time.time() - t_deb}


def main():
    def opt(nom, defaut):
        return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut
    pts = opt("--points", "c2:33,c2:65,c2:97,c2:129").split(",")
    source = json.loads((ICI / opt("--source", "defi_m13_profil_c2.json")).read_text())
    sortie = opt("--sortie", "defi_m13_second_moteur.json")
    res = []
    for p in pts:
        ch = p.split(":")
        reg, n = ch[0], int(ch[1])
        lam = float(ch[2]) if len(ch) > 2 else n / TT
        tcaps = [r["tcap"] for r in source["points"] if r["reglage"] == reg and r["n"] == n and abs(r["lam"] - lam) < 1e-9]
        tcap = min(tcaps)
        # cases atteintes par le premier moteur (certaines sont inaccessibles, ex. T_v = 27 à n = 17)
        masque = np.zeros(tcap + 1, dtype=bool)
        for r0 in source["points"]:
            if r0["reglage"] == reg and r0["n"] == n and abs(r0["lam"] - lam) < 1e-9:
                masque |= np.array([x is not None for x in r0["logP"][:tcap + 1]])
        r = un_point(reg, n, lam, tcap, masque, 777 + 31 * n + int(lam))
        res.append(r)
        print(reg, n, "λ", lam, "tcap", tcap, "platitude", round(r["platitude_production"], 3), "%.0f s" % r["duree_s"], flush=True)
        (ICI / sortie).write_text(json.dumps({"cadre": __doc__.split("Usage")[0], "points": res}, ensure_ascii=False))


if __name__ == "__main__":
    main()
