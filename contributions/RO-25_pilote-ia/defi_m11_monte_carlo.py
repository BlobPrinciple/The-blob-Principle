#!/usr/bin/env python3
"""DEFI-M11 — naître juste ou relaxer vite, au-delà de l'énumération (Monte-Carlo, numba).

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.

Cadre identique à DEFI-M8 (H-abs : graphes abstraits étiquetés ; beta = 0,30 ;
tau = 0,50 ; pi_{N,M} ∝ exp(N S_sim / tau) ; D = écart-type de population / moyenne).
Pour chaque taille N (densité fixée : M = c·N, k arêtes pour le nouveau-né) :
  1. une chaîne de Metropolis à |E| fixé échantillonne pi_{N,M} (rodage puis
     espacement), d'où R graphes parents C ;
  2. pour chaque parent et chaque theta, le nouveau-né naît selon
     G_theta(A | C) ∝ pi_{N+1,M+k}(C + v_A)^theta (loi exacte sur les C(N, k) parties,
     calculée par la proposition E de DEFI-M8_RAPPORT.md), puis t échanges de Metropolis ;
  3. on suit trois observables : triangles incidents au nouveau-né (T_v), triangles
     totaux (T) et dispersion D ; la référence d'équilibre vient d'une chaîne longue
     sur pi_{N+1,M+k}.
Écart réduit (moyenne − équilibre) / écart-type d'équilibre aux repères 0, 0,5, 1, …, 300
balayages (un balayage = M + k échanges). Temps de relaxation d'une observable : premier t (sur une grille) où l'écart de la
moyenne à l'équilibre est ≤ 0,1 écart-type d'équilibre. Intervalle par bootstrap.
Les parents, le tirage de naissance et la graine de relaxation sont communs à tous
les theta (variables aléatoires communes).

Usage : python3 defi_m11_monte_carlo.py [--rapide]  ->  defi_m11_monte_carlo.json
        python3 defi_m11_monte_carlo.py --tailles 48,64 --thetas 0,1 --R 600 --balayages-max 2000 \
                --sortie defi_m11_monte_carlo_long.json
"""
import itertools
import json
import math
import pathlib
import sys
import time

import numpy as np
from numba import njit

BETA, TAU = 0.30, 0.50
ICI = pathlib.Path(__file__).resolve().parent
THETAS = (-1.0, -0.5, 0.0, 0.5, 1.0)


@njit(cache=True)
def ssim(ntri, Q, M, n):
    mu = 2.0 * M / n
    var = Q / n - mu * mu
    if var < 0.0:
        var = 0.0
    return math.log(1.0 + ntri) - BETA * math.sqrt(var) / mu


@njit(cache=True)
def communs(adj, n, u, v):
    c = 0
    for w in range(n):
        if adj[u, w] and adj[v, w]:
            c += 1
    return c


@njit(cache=True)
def graine_numba(g):
    np.random.seed(g)


@njit(cache=True)
def balayer(adj, aretes, deg, etat, n, nsteps):
    """nsteps échanges de Metropolis à |E| fixé (proposition uniforme : une arête,
    une non-arête ; acceptation min(1, pi'/pi)). etat = [ntri, Q] (float64)."""
    M = aretes.shape[0]
    acc = 0
    for s in range(nsteps):
        i = np.random.randint(M)
        u, v = aretes[i, 0], aretes[i, 1]
        while True:  # non-arête uniforme (la paire u, v est encore une arête : exclue)
            x = np.random.randint(n)
            y = np.random.randint(n)
            if x != y and not adj[x, y]:
                break
        if x > y:
            x, y = y, x
        cuv = communs(adj, n, u, v)
        adj[u, v] = False
        adj[v, u] = False
        cxy = communs(adj, n, x, y)
        ntri2 = etat[0] - cuv + cxy
        Q2 = etat[1]
        deg[u] -= 1
        Q2 += deg[u] ** 2 - (deg[u] + 1) ** 2
        deg[v] -= 1
        Q2 += deg[v] ** 2 - (deg[v] + 1) ** 2
        deg[x] += 1
        Q2 += deg[x] ** 2 - (deg[x] - 1) ** 2
        deg[y] += 1
        Q2 += deg[y] ** 2 - (deg[y] - 1) ** 2
        dS = n * (ssim(ntri2, Q2, M, n) - ssim(etat[0], etat[1], M, n)) / TAU
        if dS >= 0.0 or np.random.random() < math.exp(dS):
            adj[x, y] = True
            adj[y, x] = True
            aretes[i, 0] = x
            aretes[i, 1] = y
            etat[0] = ntri2
            etat[1] = Q2
            acc += 1
        else:
            adj[u, v] = True
            adj[v, u] = True
            deg[u] += 1
            deg[v] += 1
            deg[x] -= 1
            deg[y] -= 1
    return acc


@njit(cache=True)
def tri_sommet(adj, n, v):
    t = 0
    for a in range(n):
        if adj[v, a]:
            for b in range(a + 1, n):
                if adj[v, b] and adj[a, b]:
                    t += 1
    return t


def graphe_aleatoire(n, m, rng):
    L = list(itertools.combinations(range(n), 2))
    sel = rng.choice(len(L), size=m, replace=False)
    adj = np.zeros((n, n), dtype=np.bool_)
    aretes = np.array([L[i] for i in sel], dtype=np.int64)
    for u, v in aretes:
        adj[u, v] = adj[v, u] = True
    return adj, aretes


def etat_de(adj):
    n = adj.shape[0]
    deg = adj.sum(1).astype(np.int64)
    A = adj.astype(np.int64)
    ntri = int(np.trace(A @ A @ A) // 6)
    return deg, np.array([float(ntri), float((deg ** 2).sum())])


def poids_naissance(adj, deg, etat, n, m, k, parties, paires_idx):
    """log pi'(C + v_A) à constante près, pour toutes les parties A (proposition E).
    parties : tableau (P, k) ; paires_idx : couples de colonnes (a, b) de parties."""
    s = deg[parties].sum(1).astype(float)
    e = np.zeros(len(parties))
    for a, b in paires_idx:
        e += adj[parties[:, a], parties[:, b]]
    n2, m2 = n + 1, m + k
    mu = 2.0 * m2 / n2
    Q = etat[1] + 2 * s + k + k * k
    D = np.sqrt(np.maximum(Q / n2 - mu * mu, 0.0)) / mu
    return n2 * (np.log1p(etat[0] + e) - BETA * D) / TAU


def experience(n, m, k, R, grille, rodage, espacement, graine, n_eq):
    rng = np.random.default_rng(graine)
    graine_numba(graine)
    parties = np.array(list(itertools.combinations(range(n), k)), dtype=np.int64)
    paires_idx = list(itertools.combinations(range(k), 2))
    # 1. parents
    adj, aretes = graphe_aleatoire(n, m, rng)
    deg, etat = etat_de(adj)
    balayer(adj, aretes, deg, etat, n, rodage)
    tmax = grille[-1]
    obs = {th: np.zeros((R, len(grille), 3)) for th in THETAS}
    for r in range(R):
        balayer(adj, aretes, deg, etat, n, espacement)
        lw = poids_naissance(adj, deg, etat, n, m, k, parties, paires_idx)
        tirage = rng.random()
        graine_r = int(rng.integers(2**31))  # même graine de relaxation pour tous les theta
        for th in THETAS:
            w = np.exp(th * (lw - lw.max()))
            w /= w.sum()
            j = min(int(np.searchsorted(np.cumsum(w), tirage)), len(w) - 1)
            A = parties[j]
            adj2 = np.zeros((n + 1, n + 1), dtype=np.bool_)
            adj2[:n, :n] = adj
            for a in A:
                adj2[a, n] = adj2[n, a] = True
            ar2 = np.vstack([aretes, np.array([[a, n] for a in A], dtype=np.int64)])
            deg2, etat2 = etat_de(adj2)
            graine_numba(graine_r)
            t_prec = 0
            for g, t in enumerate(grille):
                if t > t_prec:
                    balayer(adj2, ar2, deg2, etat2, n + 1, t - t_prec)
                    t_prec = t
                mu = 2.0 * (m + k) / (n + 1)
                D = math.sqrt(max(etat2[1] / (n + 1) - mu * mu, 0.0)) / mu
                obs[th][r, g] = (tri_sommet(adj2, n + 1, n), etat2[0], D)
    # 3. équilibre de pi_{N+1, M+k} : chaîne longue, observable sur un sommet fixé (échangeable)
    adj, aretes = graphe_aleatoire(n + 1, m + k, rng)
    deg, etat = etat_de(adj)
    balayer(adj, aretes, deg, etat, n + 1, rodage)
    eq = np.zeros((n_eq, 3))
    pas = max(1, (m + k) // 2)
    for i in range(n_eq):
        balayer(adj, aretes, deg, etat, n + 1, pas)
        mu = 2.0 * (m + k) / (n + 1)
        D = math.sqrt(max(etat[1] / (n + 1) - mu * mu, 0.0)) / mu
        v = i % (n + 1)
        eq[i] = (tri_sommet(adj, n + 1, v), etat[0], D)
    return obs, eq


def temps_relax(courbe, moy_eq, sd_eq, grille, delta=0.1):
    ecart = np.abs(courbe - moy_eq) / sd_eq
    for g in range(len(grille)):
        if np.all(ecart[g:] <= delta):
            return grille[g]
    return None


def main():
    rapide = "--rapide" in sys.argv

    def opt(nom, defaut):
        return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut
    tailles = [8, 12] if rapide else [int(x) for x in opt("--tailles", "8,12,16,24,32,48").split(",")]
    R = 300 if rapide else int(opt("--R", "2000"))
    bal_max = float(opt("--balayages-max", "300"))
    global THETAS
    THETAS = tuple(float(x) for x in opt("--thetas", "-1,-0.5,0,0.5,1").split(","))
    nom_sortie = opt("--sortie", "defi_m11_monte_carlo_rapide.json" if rapide else "defi_m11_monte_carlo.json")
    k = 4  # le nouveau-né naît avec le degré moyen d'arrivée (≈ 4) : trois arêtes de fermeture
    t0 = time.time()
    out = {"cadre": "H-abs, beta = 0,30, tau = 0,50, M = 2N − 2, k = 4 (M + k = 2(N + 1))", "thetas": THETAS,
           "R_naissances_par_theta": R, "observables": ["T_v (triangles du nouveau-né)", "T (triangles)", "D"],
           "critere": "premier t de la grille au-delà duquel |moyenne − équilibre| ≤ 0,1 écart-type d'équilibre",
           "tailles": []}
    for n in tailles:
        m = 2 * n - 2
        reperes = tuple(x for x in (0.5, 1, 2, 4, 8, 16, 32, 64, 128, 300, 1000, 3000) if x <= bal_max)
        grille = sorted(set([0] + [int(round(x)) for x in np.geomspace(1, bal_max * (m + k), 50)]
                            + [int(round(x * (m + k))) for x in reperes]))
        obs, eq = experience(n, m, k, R, grille, rodage=200 * (m + k), espacement=20 * (m + k),
                             graine=20261020 + n, n_eq=20000)
        moy_eq, sd_eq = eq.mean(0), eq.std(0)
        ligne = {"N": n, "M": m, "k": k, "equilibre_moy": moy_eq.tolist(), "equilibre_sd": sd_eq.tolist(),
                 "grille": grille, "par_theta": {}}
        rng = np.random.default_rng(1)
        for th in THETAS:
            courbes = obs[th].mean(0)
            tau = [temps_relax(courbes[:, o], moy_eq[o], sd_eq[o], grille) for o in range(3)]
            boot = []
            for _ in range(200):
                ii = rng.integers(0, R, R)
                cb = obs[th][ii].mean(0)
                boot.append([temps_relax(cb[:, o], moy_eq[o], sd_eq[o], grille) for o in range(3)])
            boot = np.array([[x if x is not None else np.nan for x in b] for b in boot], dtype=float)
            ligne["par_theta"][str(th)] = {
                "T_v_naissance": float(courbes[0, 0]),
                "tau_obs": tau,
                "tau_obs_par_arete": [None if x is None else x / (m + k) for x in tau],
                "tau_IC90": [[float(np.nanpercentile(boot[:, o], 5)), float(np.nanpercentile(boot[:, o], 95))]
                             for o in range(3)],
                "ecart_reduit_aux_reperes": {str(x): ((courbes[grille.index(int(round(x * (m + k))))] - moy_eq) / sd_eq).tolist()
                                             for x in (0,) + reperes},
                "courbe_moyenne": courbes.tolist()}
        out["tailles"].append(ligne)
        print(n, {th: (round(v["T_v_naissance"], 2), v["tau_obs"]) for th, v in ligne["par_theta"].items()},
              "eq T_v", round(moy_eq[0], 2), flush=True)
        (ICI / nom_sortie).write_text(json.dumps(out, ensure_ascii=False))
    out["duree_s"] = round(time.time() - t0, 1)
    (ICI / nom_sortie).write_text(json.dumps(out, ensure_ascii=False))
    print("durée", out["duree_s"], "s")


if __name__ == "__main__":
    main()
