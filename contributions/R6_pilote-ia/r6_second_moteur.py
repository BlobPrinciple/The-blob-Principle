# -*- coding: utf-8 -*-
"""DEFI-R6 — seconde implémentation, sans code commun avec r6_mesures.py,
r6_campagne.py ni le moteur archivé.

Réécrit d'après sa spécification (V346 XXV.1–XXV.2 et la docstring de r6_mesures) :
- germes : 8 centres uniformes, âges U(0,2 ; 1), effectifs multinomiaux ∝ âge^3,
  nuages gaussiens d'écart-type 0,12·âge, rognés à [0,1]^3 ;
- mobilité : balayages × ⌊N/4⌋ propositions ; sommet tiré uniformément, ignoré s'il
  est isolé ; pas gaussien d'écart-type 0,3·r, rogné ; voisinage reconstruit
  (0 < d < r) ; acceptation de Metropolis sur la viabilité locale du seul sommet
  déplacé, S_v = ln(1 + triangles en v) − β·(écart-type/moyenne des degrés des
  voisins), à τ = 0,5 ; sans viabilité, acceptation à pile ou face ;
- mesures : vides par comptage d'indices de cellules uniques (20^3) ; P(k) par
  histogramdd + scipy.fft.fftn complet (64^3), coquilles round(|k|) ; amplitude
  exacte P(k)/N^2 sur les coquilles 1 et 2 par somme directe sur les points.
Générateur : PCG64 sur des graines disjointes de la partie B (flux 7 000 + g).
"""
import argparse, json, math, time
import numpy as np
import scipy.fft as sfft

KAPPA, BETA, TAU = 6.6, 0.30, 0.50


def rayon(N):
    return (KAPPA / ((N - 1) * 4.0 / 3.0 * math.pi)) ** (1 / 3)


def nuage(N, gen):
    ages = gen.uniform(0.2, 1.0, 8)
    c = gen.uniform(0, 1, (8, 3))
    n = gen.multinomial(N, ages**3 / np.sum(ages**3))
    blocs = [c[i] + 0.12 * ages[i] * gen.standard_normal((n[i], 3)) for i in range(8)]
    return np.minimum(np.maximum(np.vstack(blocs), 0.0), 1.0)


class Graphe:
    def __init__(self, X, r):
        self.X, self.r, self.N = X, r, len(X)
        self.v = [set() for _ in range(self.N)]
        cell = np.floor(X / r).astype(int)
        seau = {}
        for i, cc in enumerate(map(tuple, cell)):
            seau.setdefault(cc, []).append(i)
        for i in range(self.N):
            cx, cy, cz = cell[i]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        for j in seau.get((cx + dx, cy + dy, cz + dz), ()):
                            if j > i and np.sum((X[i] - X[j]) ** 2) < r * r:
                                self.v[i].add(j); self.v[j].add(i)

    def S(self, i):
        nb = self.v[i]
        if len(nb) < 2:
            return 0.0
        t = sum(len(self.v[a] & nb) for a in nb) // 2
        d = np.array([len(self.v[a]) for a in nb], float)
        m = d.mean()
        return math.log(1 + t) - BETA * (d.std() / m if m > 0 else 0.0)

    def placer(self, i, x):
        for a in self.v[i]:
            self.v[a].discard(i)
        self.X[i] = x
        d2 = np.einsum("ij,ij->i", self.X - x, self.X - x)
        nouv = set(np.nonzero((d2 < self.r * self.r) & (d2 > 0))[0].tolist())
        nouv.discard(i)
        self.v[i] = nouv
        for a in nouv:
            self.v[a].add(i)


def dynamique(X, N, balayages, viab, gen):
    r = rayon(N)
    G = Graphe(X.copy(), r)
    for _ in range(balayages * (N // 4)):
        i = int(gen.integers(N))
        if not G.v[i]:
            continue
        avant = G.S(i) if viab else 0.0
        xo = G.X[i].copy()
        vo = set(G.v[i])
        G.placer(i, np.minimum(np.maximum(xo + gen.normal(0, 0.3 * r, 3), 0.0), 1.0))
        if viab:
            dS = G.S(i) - avant
            ok = dS >= 0 or gen.random() < math.exp(dS / TAU)
        else:
            ok = gen.random() < 0.5
        if not ok:
            for a in G.v[i]:
                G.v[a].discard(i)
            G.X[i] = xo
            G.v[i] = vo
            for a in vo:
                G.v[a].add(i)
    return G.X


def mesures(X):
    N = len(X)
    idx = np.minimum((X * 20).astype(int), 19)
    cel = np.unique(idx[:, 0] * 400 + idx[:, 1] * 20 + idx[:, 2])
    vid = 1 - len(cel) / 8000
    H, _ = np.histogramdd(X, bins=64, range=[(0, 1)] * 3)
    P = np.abs(sfft.fftn(H)) ** 2
    f = sfft.fftfreq(64, 1 / 64)
    K = np.rint(np.sqrt(f[:, None, None] ** 2 + f[None, :, None] ** 2 + f[None, None, :] ** 2)).astype(int)
    sh = np.array([P[K == k].mean() for k in range(1, 32)])
    # somme directe, coquilles 1 et 2 (vecteurs entiers de norme arrondie 1 ou 2)
    vec = [(a, b, c) for a in range(-2, 3) for b in range(-2, 3) for c in range(-2, 3)
           if round(math.sqrt(a * a + b * b + c * c)) in (1, 2)]
    direct = {1: [], 2: []}
    for v in vec:
        ph = 2 * math.pi * (X @ np.array(v, float))
        direct[round(math.sqrt(sum(t * t for t in v)))].append(np.cos(ph).sum() ** 2 + np.sin(ph).sum() ** 2)
    return {"vides": float(vid), "Pmax_sur_mediane": float(sh.max() / np.median(sh)),
            "Pmax_sur_N2": float(sh.max() / N**2), "kmax": int(sh.argmax() + 1),
            "direct_k1_sur_N2": float(np.mean(direct[1]) / N**2),
            "direct_k2_sur_N2": float(np.mean(direct[2]) / N**2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--graines", default="0:8")
    ap.add_argument("--balayages", type=int, default=5)
    ap.add_argument("--uniforme", action="store_true", help="départ uniforme au lieu des germes")
    ap.add_argument("--sortie", required=True)
    a = ap.parse_args()
    g0, g1 = map(int, a.graines.split(":"))
    out = {"N": a.N, "balayages": a.balayages, "init": "poisson" if a.uniforme else "germes", "graines": {}}
    for g in range(g0, g1):
        t = time.time()
        gen = np.random.Generator(np.random.PCG64(7000 + g))
        X0 = gen.uniform(0, 1, (a.N, 3)) if a.uniforme else nuage(a.N, gen)
        e = {"fige": mesures(X0)}
        for nom, viab in (("mobile", False), ("viab", True)):
            X = dynamique(X0, a.N, a.balayages, viab, np.random.Generator(np.random.PCG64([7000 + g, int(viab)])))
            e[nom] = mesures(X)
        e["poisson"] = mesures(gen.uniform(0, 1, (a.N, 3)))
        out["graines"][str(g)] = e
        json.dump(out, open(a.sortie, "w"), indent=1)
        print(f"N={a.N} g={g} {time.time()-t:.0f}s amp {e['fige']['Pmax_sur_N2']:.4f} "
              f"{e['mobile']['Pmax_sur_N2']:.4f} {e['viab']['Pmax_sur_N2']:.4f} | vides "
              f"{e['fige']['vides']:.4f} {e['mobile']['vides']:.4f} {e['viab']['vides']:.4f}", flush=True)


if __name__ == "__main__":
    main()
