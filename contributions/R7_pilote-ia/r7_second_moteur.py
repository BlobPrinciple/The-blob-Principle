# -*- coding: utf-8 -*-
"""DEFI-R7 — seconde implémentation, sans code commun avec r7_periodique.py.

Python pur + numpy : distances d'image minimale par force brute (O(N) par sommet
interrogé), générateur PCG64 (numpy Generator) sur d'autres graines, et mesure
indépendante : facteur de structure exact S(k) = |Σ_j exp(2iπ n·x_j)|²/N sur tous
les vecteurs entiers n de la coquille round(|n|) = k (pas de grille, pas d'affectation).
Même règle que le moteur archivé (voir r7_periodique.py), boîte périodique.

Usage : python3 r7_second_moteur.py --N 2500 --graines 0:4 --instants 0,80,320 --sortie f.json
"""
import argparse, json, math, os, time
import numpy as np

K, B, T = 6.6, 0.30, 0.50


def voisins_de(P, x, r2):
    u = P - x
    u -= np.round(u)
    q = (u * u).sum(1)
    return np.nonzero((q < r2) & (q > 0))[0]


def s_loc(P, v, r2):
    nv = voisins_de(P, P[v], r2)
    if len(nv) < 2:
        return 0.0
    Q = P[nv]
    D = Q[:, None, :] - Q[None, :, :]
    D -= np.round(D)
    q = (D * D).sum(2)
    tri = int(((q < r2) & (q > 0)).sum()) // 2
    deg = np.array([len(voisins_de(P, P[u], r2)) for u in nv], float)
    return math.log(1 + tri) - B * (deg.std() / deg.mean())


def evoluer(P, n_bal, r, rng):
    r2 = r * r; N = len(P)
    for _ in range(n_bal):
        for _ in range(N // 4):
            v = int(rng.integers(N))
            if len(voisins_de(P, P[v], r2)) == 0:
                continue
            s0 = s_loc(P, v, r2)
            x0 = P[v].copy()
            P[v] = (x0 + rng.normal(0, 0.3 * r, 3)) % 1.0
            ds = s_loc(P, v, r2) - s0
            if not (ds >= 0 or rng.random() < math.exp(ds / T)):
                P[v] = x0


_N = {}


def vecteurs(kmax):
    if kmax not in _N:
        g = np.arange(-kmax - 1, kmax + 2)
        n = np.array(np.meshgrid(g, g, g, indexing="ij")).reshape(3, -1).T
        m = np.rint(np.sqrt((n * n).sum(1))).astype(int)
        keep = (m >= 1) & (m <= kmax)
        _N[kmax] = (n[keep], m[keep])
    return _N[kmax]


def S_exact(P, kmax=12):
    n, m = vecteurs(kmax)
    out = np.zeros(kmax)
    for a in range(0, len(n), 400):
        ph = np.exp(2j * np.pi * (P @ n[a:a + 400].T))
        s = np.abs(ph.sum(0)) ** 2 / len(P)
        np.add.at(out, m[a:a + 400] - 1, s)
    cnt = np.bincount(m - 1, minlength=kmax)
    return out / cnt


def mesure(P):
    S = S_exact(P)
    c = np.minimum((P * 20).astype(int), 19)
    vides = 1 - len(np.unique(c[:, 0] * 400 + c[:, 1] * 20 + c[:, 2])) / 8000
    return {"S": S.tolist(), "kmax": int(np.argmax(S) + 1), "Smax": float(S.max()), "vides": float(vides)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--graines", default="0:4")
    ap.add_argument("--instants", default="0,80,320")
    ap.add_argument("--sortie", required=True)
    a = ap.parse_args()
    r = (K / ((a.N - 1) * 4 / 3 * math.pi)) ** (1 / 3)
    res = json.load(open(a.sortie)) if os.path.exists(a.sortie) else {"N": a.N, "r_N": r, "graines": {}}
    g0, g1 = map(int, a.graines.split(":"))
    for g in range(g0, g1):
        if str(g) in res["graines"]:
            continue
        t = time.time()
        rng = np.random.default_rng([7, a.N, g])
        P = rng.uniform(0, 1, (a.N, 3))
        tr = {}; fait = 0
        for ti in map(int, a.instants.split(",")):
            evoluer(P, ti - fait, r, rng); fait = ti
            tr[str(ti)] = mesure(P)
        res["graines"][str(g)] = {"traj": tr, "secondes": time.time() - t}
        json.dump(res, open(a.sortie, "w"), indent=1)
        print(f"N={a.N} g={g} {time.time()-t:.0f}s " + " ".join(f"t={k}: vides {v['vides']:.3f} kmax {v['kmax']} Smax {v['Smax']:.2f}" for k, v in tr.items()), flush=True)


if __name__ == "__main__":
    main()
