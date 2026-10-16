#!/usr/bin/env python3
"""DEFI-M9 — recoupement par une seconde implémentation du même noyau.

Recoupement de code, pas de modèle : même auteur, même spécification, mêmes particularités du
noyau de proposition.

Contribution du pilote IA du laboratoire (Claude, Anthropic), 16 octobre 2026.

Ce script n'importe pas le moteur du corpus. Il réécrit le modèle à partir de sa
spécification (en-tête de « blob engine.py ») : N points uniformes dans le cube unité,
r = (kappa / ((N - 1) 4 pi / 3))^(1/3), réservoir = paires à distance < 1,6 r, graphe
initial = les round(N kappa / 2) paires les plus courtes, Metropolis sur
S = log(1 + n_tri) - beta CV(degrés) (moyenne des degrés fixée à 2E/N), tau_eff = tau / N,
thermalisation 120 N pas. Noyau de proposition : une arête uniforme (u, v), refusée si un
des deux degrés vaut au plus 2 ; une paire du réservoir non arête, disjointe de {u, v},
tirée uniformément (au plus 40 essais) ; plafond de degré 96.
Différences d'implémentation voulues : matrice d'adjacence dense, triangles par produit
matriciel (diag(A^3)/2), variation de S recalculée à partir des seuls degrés et du nombre de
triangles, générateur aléatoire distinct.
La naissance suit la même loi [H-loc] que DEFI-M7 et DEFI-M9.
"""
import json, math, pathlib, sys, time
import numpy as np
from numba import njit
from scipy import stats
from scipy.spatial import cKDTree

ICI = pathlib.Path(__file__).resolve().parent
KAPPA, BETA, TAU, PF, CAP = 6.6, 0.30, 0.50, 1.6, 96
LAGS = [0, 256, 2048]
POINT = []


@njit(cache=True)
def metropolis(A, deg, E_u, E_v, P_a, P_b, nsteps, beta, tau_eff, mean, seed):
    np.random.seed(seed)
    N = A.shape[0]; E = E_u.shape[0]; P = P_a.shape[0]
    nt = 0
    for i in range(N):
        for j in range(i + 1, N):
            if A[i, j]:
                for k in range(j + 1, N):
                    if A[i, k] and A[j, k]:
                        nt += 1
    s2 = 0.0
    for i in range(N):
        s2 += deg[i] * deg[i]
    for _ in range(nsteps):
        e = np.random.randint(E); u = E_u[e]; v = E_v[e]
        if deg[u] <= 2 or deg[v] <= 2:
            continue
        a = -1; b = -1
        for _t in range(40):
            q = np.random.randint(P); x = P_a[q]; y = P_b[q]
            if x == u or x == v or y == u or y == v:
                continue
            if deg[x] >= CAP or deg[y] >= CAP:
                continue
            if not A[x, y]:
                a = x; b = y; break
        if a < 0:
            continue
        cl = 0; cg = 0
        for w in range(N):
            if A[u, w] and A[v, w]:
                cl += 1
            if A[a, w] and A[b, w]:
                cg += 1
        nt2 = nt - cl + cg
        s2n = s2 - deg[u] ** 2 - deg[v] ** 2 - deg[a] ** 2 - deg[b] ** 2 \
            + (deg[u] - 1) ** 2 + (deg[v] - 1) ** 2 + (deg[a] + 1) ** 2 + (deg[b] + 1) ** 2
        cv1 = math.sqrt(max(s2 / N - mean * mean, 0.0)) / mean
        cv2 = math.sqrt(max(s2n / N - mean * mean, 0.0)) / mean
        dS = (math.log(1.0 + nt2) - beta * cv2) - (math.log(1.0 + nt) - beta * cv1)
        if dS >= 0 or np.random.random() < math.exp(dS / tau_eff):
            A[u, v] = False; A[v, u] = False; A[a, b] = True; A[b, a] = True
            deg[u] -= 1; deg[v] -= 1; deg[a] += 1; deg[b] += 1
            E_u[e] = a; E_v[e] = b; nt = nt2; s2 = s2n
    return nt


def masse(A):
    M = A.astype(np.float64)
    return np.rint(np.diag(M @ M @ M) / 2).astype(np.int64)


def pit(x, autres, rng):
    return (np.count_nonzero(autres < x) + rng.random() * np.count_nonzero(autres == x)) / len(autres)


def une_graine(N0, seed, B):
    rng = np.random.default_rng(900_000 + seed)
    pts = rng.random((N0, 3))
    r = (KAPPA / ((N0 - 1) * 4.0 / 3.0 * math.pi)) ** (1 / 3)
    pool = np.array(sorted(cKDTree(pts).query_pairs(PF * r)), dtype=np.int64)
    L = np.linalg.norm(pts[pool[:, 0]] - pts[pool[:, 1]], axis=1)
    E0 = min(int(round(N0 * KAPPA / 2)), len(pool))
    init = pool[np.argsort(L, kind="stable")[:E0]]
    Nmax = N0 + B
    A = np.zeros((Nmax, Nmax), dtype=np.bool_)
    A[init[:, 0], init[:, 1]] = True; A[init[:, 1], init[:, 0]] = True
    N = N0
    def chaine(nsteps, sd):
        Au = A[:N, :N].copy(); dg = Au.sum(1).astype(np.int64)
        iu, iv = np.nonzero(np.triu(Au)); iu = iu.astype(np.int64); iv = iv.astype(np.int64)
        metropolis(Au, dg, iu, iv, pool[:, 0].copy(), pool[:, 1].copy(), nsteps, BETA, TAU / N,
                   2.0 * len(iu) / N, sd)
        A[:N, :N] = Au
        return len(iu)
    chaine(120 * N0, 31 * seed + 7)
    m0 = np.sort(masse(A[:N, :N]).astype(float)); c = np.arange(1, N + 1)
    POINT.append({"N": N0, "graine": seed, "n_tri_par_N": round(float(m0.sum() / 3 / N), 3),
                  "Gini_masse": round(float(2 * np.sum(c * m0) / (N * m0.sum()) - (N + 1) / N), 3)})
    out = []
    for b in range(B):
        E = int(np.triu(A[:N, :N]).sum())
        k = max(1, min(int(round(KAPPA * (N + 1) / 2)) - E, 8))
        p = rng.random(3); d = np.linalg.norm(pts - p, axis=1)
        for v in np.argsort(d)[:k]:
            A[v, N] = True; A[N, v] = True
        voisins_pool = np.where(d < PF * r)[0]
        pool = np.vstack([pool, np.stack([voisins_pool, np.full(len(voisins_pool), N)], 1)])
        pts = np.vstack([pts, p]); N += 1
        ctl = int(rng.integers(0, N0)); ligne = {"u_nb": [], "u_ctl": [], "d_tri": []}
        t_prev = 0
        for Lg in LAGS:
            if Lg > t_prev:
                E = int(np.triu(A[:N, :N]).sum())
                chaine((Lg - t_prev) * E, 10_007 * seed + 97 * b + Lg)
            t_prev = Lg
            m = masse(A[:N, :N]); nb = N - 1
            ligne["u_nb"].append(pit(m[nb], np.delete(m, nb), rng))
            ligne["u_ctl"].append(pit(m[ctl], np.delete(m, [ctl, nb]), rng))
            ligne["d_tri"].append(float(m[nb] - np.delete(m, nb).mean()))
        out.append(ligne)
    return out


def main():
    plan = [(250, 10, 12), (500, 6, 12)]
    if "--rapide" in sys.argv:
        plan = [(250, 1, 3)]
    res = {"lags_balayages": LAGS, "N": {}}
    for N0, ns, B in plan:
        t0 = time.time()
        rows = [x for s in range(ns) for x in une_graine(N0, s, B)]
        U = np.array([r["u_nb"] for r in rows]); C = np.array([r["u_ctl"] for r in rows])
        D = np.array([r["d_tri"] for r in rows]); n = len(rows)
        res["N"][str(N0)] = {"n_naissances": n, "secondes": round(time.time() - t0, 1), "par_lag": [
            {"t": Lg,
             "nouveau_ne_moy_u": round(float(U[:, j].mean()), 4),
             "nouveau_ne_et": round(float(U[:, j].std(ddof=1) / math.sqrt(n)), 4),
             "nouveau_ne_part_u_sup_0.9": round(float((U[:, j] > 0.9).mean()), 4),
             "temoin_moy_u": round(float(C[:, j].mean()), 4),
             "temoin_part_u_sup_0.9": round(float((C[:, j] > 0.9).mean()), 4),
             "KS_p_nouveau_ne": float("%.3g" % stats.kstest(U[:, j], "uniform").pvalue),
             "ecart_tri_moy": round(float(D[:, j].mean()), 3),
             "ecart_tri_et": round(float(D[:, j].std(ddof=1) / math.sqrt(n)), 3)}
            for j, Lg in enumerate(LAGS)]}
        print(N0, json.dumps(res["N"][str(N0)], ensure_ascii=False), flush=True)
    res["point_de_travail"] = POINT
    print("point de travail", POINT)
    if "--rapide" not in sys.argv:
        (ICI / "defi_m9_second_moteur.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
