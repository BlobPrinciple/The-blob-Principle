#!/usr/bin/env python3
"""DEFI-M12 — test direct du refroidissement : t½ à n fixé quand lam varie, et à lam fixé quand n varie.

Pilote IA du laboratoire (Claude, Anthropic), 27 octobre 2026. Test suggéré par la relecture hostile.
Moteur et estimateur de defi_m12_lenteur.py (M = 2n, autocorrélation poolée de T_v, quatre chaînes :
deux départs aléatoires, deux noyaux plantés). Delta choisi pour t½/Delta ≈ 10 à 15.
Usage : python3 defi_m12_arrhenius.py -> defi_m12_arrhenius.json
"""
import json
import math
import pathlib
from multiprocessing import Pool

import numpy as np

import defi_m12_lenteur as L

ICI = pathlib.Path(__file__).resolve().parent
POINTS = [  # (n, lam, Delta)
    (65, 98.0, 10), (65, 162.0, 80), (65, 194.0, 200),
    (49, 98.0, 10), (97, 194.0, 134),
]


def une(args):
    n, lam, delta, j = args
    m = 2 * n
    g = 31337 + 7 * n + int(lam) * 101 + j
    rng = np.random.default_rng(g)
    L.graine_numba(g)
    adj, ar, deg, etat = L.depart(n, m, rng, j >= 2)
    L.balayer(adj, ar, deg, etat, n, max(400, 200 * delta) * m, lam)
    X = np.zeros((3000, n))
    out = np.zeros(n, dtype=np.int64)
    for i in range(3000):
        L.balayer(adj, ar, deg, etat, n, delta * m, lam)
        L.tri_tous(adj, n, out)
        X[i] = out
    C = L.acf_poolee(X)
    return {"n": n, "lam": lam, "delta": delta, "chaine": j, "t_demi": L.temps_seuil(C, 0.5, delta),
            "part_Tv_sup6": float(X[X > 6].sum() / X.sum())}


def main():
    taches = [(n, lam, d, j) for n, lam, d in POINTS for j in range(4)]
    with Pool(2) as p:
        res = p.map(une, taches)
    resume = []
    for n, lam, d in POINTS:
        v = [r["t_demi"] for r in res if r["n"] == n and r["lam"] == lam]
        resume.append({"n": n, "lam": lam, "lam_sur_n": lam / n, "t_demi": float(np.mean(v)),
                       "erreur": float(np.std(v, ddof=1) / 2), "t_demi_sur_delta": float(np.mean(v)) / d,
                       "part_Tv_sup6": float(np.mean([r["part_Tv_sup6"] for r in res if r["n"] == n and r["lam"] == lam]))})
        print(resume[-1], flush=True)
    # à n = 65 : avec lam = 66 (c2T) et 130 (c2) de defi_m12_analyse.json
    a = json.loads((ICI / "defi_m12_analyse.json").read_text())["resume"]
    serie = [(66.0, a["c2T"]["65"]["t_demi"][0]), (130.0, a["c2"]["65"]["t_demi"][0])] + \
            [(r["lam"], r["t_demi"]) for r in resume if r["n"] == 65]
    serie.sort()
    x = np.array([s[0] for s in serie if s[0] >= 98])
    y = np.log([s[1] for s in serie if s[0] >= 98])
    pente, b = np.polyfit(x, y, 1)
    print("n = 65 :", [(l, round(t, 1)) for l, t in serie], "pente log t½ / lam (lam ≥ 98) = %.4f" % pente)
    json.dump({"points": resume, "chaines": res, "serie_n65": serie, "pente_log_t_par_lam_n65_lam_ge_98": pente},
              open(ICI / "defi_m12_arrhenius.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
