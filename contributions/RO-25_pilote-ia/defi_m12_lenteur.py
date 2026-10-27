#!/usr/bin/env python3
"""DEFI-M12 — la lenteur aristocratique : puissance de N ou exponentielle ?

Pilote IA du laboratoire (Claude, Anthropic), 27 octobre 2026.

Cadre de DEFI-M8 et DEFI-M11 (H-abs : graphes abstraits étiquetés ; beta = 0,30 ;
tau = 0,50 ; pi_{n,M} ∝ exp(lam · S_sim), lam = n / tau pour la mesure de l'armature,
n = nombre de sommets ; D = écart-type de population des degrés / degré moyen ;
échanges de Metropolis à |E| fixé, proposition uniforme : une arête, une non-arête).

Méthode « stationnaire » (indépendante de la méthode « naissance » de DEFI-M11) :
dans une chaîne à l'équilibre, on enregistre T_v (triangles contenant v) pour tous les
sommets tous les Delta balayages (un balayage = M échanges). Autocorrélation poolée
C(t) = < (T_v(0) − m)(T_v(t) − m) > / < (T_v − m)² >, moyenne m commune à tous les
sommets (échangeabilité) : elle inclut donc la persistance du rang d'un sommet
(aristocrate ou roturier). Temps caractéristiques : t_1/2 (C = 1/2), t_1/e, t_0,1.

Réglages :
  « c2 »   : M = 2n (degré moyen 4), lam = n / tau (mesure de l'armature) ;
  « c3 »   : M = 3n (degré moyen 6), lam = n / tau ;
  « c2T »  : M = 2n, lam = 33 / tau fixé (température effective tenue constante) :
             teste le mécanisme [H] de DEFI-M11 (refroidissement de pi quand n grandit).
Quatre chaînes par point : deux départs aléatoires, deux départs « noyau planté »
(clique de taille maximale compatible avec M, reste aléatoire). Barres : écart-type
entre chaînes / 2.

Usage : python3 defi_m12_lenteur.py [--tailles 17,25,...] [--reglages c2,c3,c2T]
        [--L 3000] [--processus 2] [--sortie defi_m12_lenteur.json]
"""
import itertools
import json
import math
import pathlib
import sys
import time
from multiprocessing import Pool

import numpy as np
from numba import njit

BETA, TAU = 0.30, 0.50
ICI = pathlib.Path(__file__).resolve().parent


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
def balayer(adj, aretes, deg, etat, n, nsteps, lam):
    """Même noyau que defi_m11_monte_carlo.balayer, avec lam explicite (lam = n/TAU y est implicite)."""
    M = aretes.shape[0]
    acc = 0
    for s in range(nsteps):
        i = np.random.randint(M)
        u, v = aretes[i, 0], aretes[i, 1]
        while True:
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
        dS = lam * (ssim(ntri2, Q2, M, n) - ssim(etat[0], etat[1], M, n))
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
def tri_tous(adj, n, out):
    for v in range(n):
        out[v] = 0
    for a in range(n):
        for b in range(a + 1, n):
            if adj[a, b]:
                for c in range(b + 1, n):
                    if adj[a, c] and adj[b, c]:
                        out[a] += 1
                        out[b] += 1
                        out[c] += 1


def depart(n, m, rng, plante):
    paires = list(itertools.combinations(range(n), 2))
    adj = np.zeros((n, n), dtype=np.bool_)
    choisies = set()
    if plante:
        q = int((1 + math.isqrt(1 + 8 * m)) // 2)
        while q * (q - 1) // 2 > m:
            q -= 1
        noyau = rng.choice(n, size=q, replace=False)
        for a, b in itertools.combinations(sorted(noyau), 2):
            choisies.add((a, b))
    reste = [p for p in paires if p not in choisies]
    for j in rng.choice(len(reste), size=m - len(choisies), replace=False):
        choisies.add(reste[j])
    aretes = np.array(sorted(choisies), dtype=np.int64)
    for u, v in aretes:
        adj[u, v] = adj[v, u] = True
    deg = adj.sum(1).astype(np.int64)
    A = adj.astype(np.int64)
    etat = np.array([float(np.trace(A @ A @ A) // 6), float((deg ** 2).sum())])
    return adj, aretes, deg, etat


def acf_poolee(X):
    """X : (L, n). Autocorrélation poolée sur les sommets, moyenne commune."""
    L, n = X.shape
    Y = X - X.mean()
    var = (Y ** 2).mean()
    nfft = 1 << (2 * L - 1).bit_length()
    F = np.fft.rfft(Y, n=nfft, axis=0)
    ac = np.fft.irfft(F * np.conj(F), n=nfft, axis=0)[:L].sum(1)
    ac /= (np.arange(L, 0, -1) * n)
    return ac / var


def temps_seuil(C, seuil, delta):
    for i in range(1, len(C)):
        if C[i] <= seuil:
            c0, c1 = C[i - 1], C[i]
            f = (c0 - seuil) / (c0 - c1) if c0 != c1 else 1.0
            return (i - 1 + f) * delta
    return None


def delta_pour(n, reglage):
    """Espacement des enregistrements (balayages), environ t½ / 15 attendu.
    c2T : à température tenue fixe, t½ décroît avec n (passes précédentes : Delta trop
    grand dès n = 49, voir defi_m12_lenteur_premiere_passe_sortie.txt et
    defi_m12_lenteur_c3_c2T_sortie.txt) ; Delta = 1 balayage.
    c3 : t½ environ quatre fois plus court qu'en c2 ; base 0,15 au lieu de 0,6."""
    if reglage == "c2T":
        return 1
    base = 0.15 if reglage == "c3" else 0.6
    return max(1, int(round(base * (n / 16.0) ** 3)))


def une_chaine(args):
    n, reglage, L, graine, plante, delta = args
    c = 3 if reglage == "c3" else 2
    m = c * n
    lam = (33 / TAU) if reglage == "c2T" else (n / TAU)
    rng = np.random.default_rng(graine)
    graine_numba(graine)
    adj, ar, deg, etat = depart(n, m, rng, plante)
    t0 = time.time()
    rodage = max(400, 20 * delta * 10)  # balayages ; au moins 200 fois Delta / 10
    acc = balayer(adj, ar, deg, etat, n, rodage * m, lam)
    X = np.zeros((L, n))
    T = np.zeros(L)
    out = np.zeros(n, dtype=np.int64)
    acc = 0
    for i in range(L):
        acc += balayer(adj, ar, deg, etat, n, delta * m, lam)
        tri_tous(adj, n, out)
        X[i] = out
        T[i] = etat[0]
    C = acf_poolee(X)
    return {"n": n, "reglage": reglage, "graine": graine, "plante": plante, "delta": delta, "L": L,
            "rodage_balayages": rodage, "acceptation": acc / (L * delta * m),
            "T_moy_moitie1": float(T[:L // 2].mean()), "T_moy_moitie2": float(T[L // 2:].mean()),
            "T_sd": float(T.std()), "Tv_moy": float(X.mean()), "Tv_sd": float(X.std()),
            "part_Tv_sup6": float(X[X > 6].sum() / X.sum()),
            "t_demi": temps_seuil(C, 0.5, delta), "t_1e": temps_seuil(C, math.exp(-1), delta),
            "t_01": temps_seuil(C, 0.1, delta), "C_debut": C[:200].tolist(), "duree_s": time.time() - t0}


def main():
    def opt(nom, defaut):
        return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut
    tailles = [int(x) for x in opt("--tailles", "17,25,33,49,65,97,129").split(",")]
    reglages = opt("--reglages", "c2,c3,c2T").split(",")
    L = int(opt("--L", "3000"))
    sortie = opt("--sortie", "defi_m12_lenteur.json")
    taches = []
    for reg in reglages:
        for n in tailles:
            d = delta_pour(n, reg)
            for j in range(4):
                taches.append((n, reg, L, 20261027 + 1000 * n + 10 * j + {"c2": 0, "c3": 1, "c2T": 2}[reg] * 100000,
                               j >= 2, d))
    taches.sort(key=lambda t: t[0])
    res = []
    t0 = time.time()
    with Pool(int(opt("--processus", "2"))) as p:
        for r in p.imap_unordered(une_chaine, taches):
            res.append(r)
            print(r["reglage"], r["n"], "planté" if r["plante"] else "aléat.", "Δ", r["delta"],
                  "t½", None if r["t_demi"] is None else round(r["t_demi"], 1),
                  "t1/e", None if r["t_1e"] is None else round(r["t_1e"], 1),
                  "T", round(r["T_moy_moitie1"], 1), round(r["T_moy_moitie2"], 1),
                  "acc", round(r["acceptation"], 3), "%.0f s" % r["duree_s"], flush=True)
            (ICI / sortie).write_text(json.dumps({"chaines": res}, ensure_ascii=False))
    resume = {}
    for reg in reglages:
        for n in tailles:
            R = [r for r in res if r["reglage"] == reg and r["n"] == n]
            for cle in ("t_demi", "t_1e", "t_01"):
                v = [r[cle] for r in R if r[cle] is not None]
                resume.setdefault(reg, {}).setdefault(str(n), {})[cle] = (
                    [float(np.mean(v)), float(np.std(v, ddof=1) / math.sqrt(len(v))) if len(v) > 1 else None, len(v)])
            resume[reg][str(n)]["T_moy"] = float(np.mean([r["T_moy_moitie2"] for r in R]))
            resume[reg][str(n)]["T_ecart_departs"] = float(
                np.mean([r["T_moy_moitie2"] for r in R if r["plante"]]) - np.mean([r["T_moy_moitie2"] for r in R if not r["plante"]]))
            resume[reg][str(n)]["T_sd"] = float(np.mean([r["T_sd"] for r in R]))
    (ICI / sortie).write_text(json.dumps({"cadre": __doc__.split("Usage")[0], "resume": resume, "chaines": res,
                                          "duree_s": time.time() - t0}, ensure_ascii=False))
    print(json.dumps(resume, indent=1))


if __name__ == "__main__":
    main()
