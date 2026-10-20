#!/usr/bin/env python3
"""DEFI-M8 — seconde implémentation indépendante (networkx, dictionnaires, matrices denses).

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
Ne partage aucun code avec defi_m8_attachement_gibbs.py : graphes représentés
comme frozensets d'arêtes, triangles et degrés calculés par networkx, noyau
d'échange construit par énumération ensembliste, puissance de matrice dense.
Couvre les cas à au plus 6 sommets après naissance.

Usage : python3 defi_m8_second_moteur.py            ->  defi_m8_second_moteur.json
        python3 defi_m8_second_moteur.py --tempere  ->  defi_m8_second_moteur_tempere.json
"""
import itertools
import json
import math
import pathlib

import networkx as nx
import numpy as np

BETA, TAU = 0.30, 0.50
ICI = pathlib.Path(__file__).resolve().parent


def ssim(n, E):
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(E)
    d = np.array([g.degree(v) for v in range(n)], dtype=float)
    t = sum(nx.triangles(g).values()) // 3
    return math.log(1 + t) - BETA * float(np.std(d)) / float(np.mean(d))


def mesure(n, m):
    toutes = [frozenset(c) for c in itertools.combinations(itertools.combinations(range(n), 2), m)]
    lw = {c: n * ssim(n, c) / TAU for c in toutes}
    mx = max(lw.values())
    z = sum(math.exp(v - mx) for v in lw.values())
    return {c: math.exp(v - mx) / z for c, v in lw.items()}


def naissances(n, m, k):
    pi = mesure(n, m)
    pi2 = mesure(n + 1, m + k)
    choix = list(itertools.combinations(range(n), k))
    U, G = {}, {}
    for c, w in pi.items():
        enfants = [c | frozenset((a, n) for a in A) for A in choix]
        z = sum(pi2[e] for e in enfants)
        for e in enfants:
            U[e] = U.get(e, 0.0) + w / len(choix)
            G[e] = G.get(e, 0.0) + w * pi2[e] / z
    # restriction : borne de la proposition C
    marg = {}
    for e, w in pi2.items():
        r = frozenset(x for x in e if n not in x)
        marg[r] = marg.get(r, 0.0) + w
    borne = 0.5 * (sum(abs(pi[c] - marg.get(c, 0.0)) for c in pi)
                   + sum(w for r, w in marg.items() if r not in pi))
    return pi2, U, G, borne


def tv(nu, pi2):
    return 0.5 * sum(abs(nu.get(e, 0.0) - w) for e, w in pi2.items())


def kl(nu, pi2):
    return sum(p * math.log(p / pi2[e]) for e, p in nu.items() if p > 0)


def noyau(n, pi2):
    etats = sorted(pi2, key=lambda s: sorted(s))
    idx = {e: i for i, e in enumerate(etats)}
    P = set(itertools.combinations(range(n), 2))
    m = len(etats[0])
    nprop = m * (len(P) - m)
    K = np.zeros((len(etats), len(etats)))
    for e in etats:
        i = idx[e]
        for a in e:
            for b in P - e:
                f = (e - {a}) | {b}
                K[i, idx[f]] += min(1.0, pi2[f] / pi2[e]) / nprop
        K[i, i] = 1.0 - K[i].sum() + K[i, i]
    return etats, K


def tempere():
    """G_theta(A|C) ∝ pi2(C+A)^theta : t pour TV <= 0,01 (cas à 6 sommets au plus)."""
    out = []
    for n, m, k in [(4, 3, 3), (4, 4, 3), (5, 5, 4), (5, 7, 4)]:
        pi = mesure(n, m)
        pi2 = mesure(n + 1, m + k)
        etats, K = noyau(n + 1, pi2)
        p = np.array([pi2[e] for e in etats])
        idx = {e: i for i, e in enumerate(etats)}
        choix = list(itertools.combinations(range(n), k))
        ligne = {"N": n, "M": m, "k": k}
        for th in (-0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0):
            x = np.zeros(len(etats))
            for c, w in pi.items():
                enfants = [c | frozenset((a, n) for a in A) for A in choix]
                poids = [pi2[e] ** th for e in enfants]
                z = sum(poids)
                for e, q in zip(enfants, poids):
                    x[idx[e]] += w * q / z
            t01 = None
            for t in range(4001):
                if 0.5 * np.abs(x - p).sum() <= 0.01:
                    t01 = t
                    break
                x = x @ K
            ligne[f"theta={th}"] = t01
        out.append(ligne)
        print(ligne, flush=True)
    (ICI / "defi_m8_second_moteur_tempere.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


def main():
    out = {"implementation": "2 (networkx, frozensets, matrices denses)", "naissance": [], "relaxation": []}
    for n, m in [(4, 3), (4, 4), (4, 5), (5, 5), (5, 7), (5, 8)]:
        for k in range(1, n + 1):
            pi2, U, G, borne = naissances(n, m, k)
            r = {"N": n, "M": m, "k": k, "borne": borne, "TV_U": tv(U, pi2), "TV_G": tv(G, pi2),
                 "KL_U": kl(U, pi2), "KL_G": kl(G, pi2)}
            out["naissance"].append(r)
            print(r, flush=True)
    for n, m, k in [(4, 5, 2), (5, 8, 3), (4, 3, 3), (4, 4, 3), (5, 5, 4), (5, 7, 4)]:
        pi2, U, G, _ = naissances(n, m, k)
        etats, K = noyau(n + 1, pi2)
        p = np.array([pi2[e] for e in etats])
        res = {"N": n, "M": m, "k": k, "etats": len(etats),
               "ecart_stochastique": float(np.abs(K.sum(1) - 1).max()),
               "ecart_invariance": float(np.abs(p @ K - p).max())}
        courbes = {}
        for nom, nu in (("U", U), ("G", G)):
            x = np.array([nu.get(e, 0.0) for e in etats])
            tvs, kls, t01 = [], [], None
            for t in range(3000):
                d = 0.5 * np.abs(x - p).sum()
                s = x > 0
                tvs.append(d)
                kls.append(float((x[s] * np.log(x[s] / p[s])).sum()))
                if t01 is None and d <= 0.01:
                    t01 = t
                    break
                x = x @ K
            res["t_TV_0_01_" + nom] = t01
            courbes[nom] = (tvs, kls)
        T = min(len(courbes["U"][0]), len(courbes["G"][0]))
        res["premier_t_TV_G_sup_U"] = next((t for t in range(T) if courbes["G"][0][t] > courbes["U"][0][t] + 1e-15), None)
        res["premier_t_KL_G_sup_KL_U"] = next((t for t in range(T) if courbes["G"][1][t] > courbes["U"][1][t] + 1e-15), None)
        out["relaxation"].append(res)
        print(res, flush=True)
    (ICI / "defi_m8_second_moteur.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("écrit : defi_m8_second_moteur.json")


if __name__ == "__main__":
    import sys
    if "--tempere" in sys.argv:
        tempere()
    else:
        main()
