#!/usr/bin/env python3
"""DEFI-M12 — prolongement de la méthode « naissance » de DEFI-M11 à N = 96 et 128 (theta = 0).

Pilote IA du laboratoire (Claude, Anthropic), 27 octobre 2026.
Réutilise sans modification defi_m11_monte_carlo.experience (attachement uniforme, k = 4,
M = 2N − 2, donc M + k = 2(N + 1)) et le demi-temps t½ de defi_m11_demi_temps.demi_temps.
Seuls changent : le rodage des parents (au moins 4 fois le t½ stationnaire attendu) et
l'espacement entre parents (balayages), pour réduire la corrélation entre naissances.
Erreur sur t½ : bootstrap sur les naissances (200 rééchantillonnages).
Usage : python3 defi_m12_naissance.py --tailles 96 --R 400 --sortie defi_m12_naissance_96.json
        python3 defi_m12_naissance.py --tailles 128 --R 200 --sortie defi_m12_naissance_128.json
"""
import json
import pathlib
import sys

import numpy as np

import defi_m11_monte_carlo as mc
from defi_m11_demi_temps import demi_temps

ICI = pathlib.Path(__file__).resolve().parent
PLAN = {  # N : (balayages max, rodage en balayages, espacement en balayages)
    64: (3000, 4000, 200),
    96: (20000, 12000, 1000),
    128: (40000, 40000, 3000),
}


def main():
    def opt(nom, d):
        return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else d
    tailles = [int(x) for x in opt("--tailles", "96,128").split(",")]
    R = int(opt("--R", "400"))
    sortie = opt("--sortie", "defi_m12_naissance.json")
    mc.THETAS = (0.0,)
    out = []
    for n in tailles:
        m, k = 2 * n - 2, 4
        mk = m + k
        bmax, rod, esp = PLAN[n]
        grille = sorted(set([0] + [int(round(x)) for x in np.geomspace(1, bmax * mk, 70)]))
        obs, eq = mc.experience(n, m, k, R, grille, rodage=rod * mk, espacement=esp * mk,
                                graine=20261027 + n, n_eq=20000)
        tv = obs[0.0][:, :, 0]
        moy_eq = float(eq[:, 0].mean())
        # référence d'équilibre exacte par échangeabilité : 3 T / (N + 1) moyen sur la chaîne d'équilibre
        moy_eq_T = float(3 * eq[:, 1].mean() / (n + 1))
        t = demi_temps(grille, tv.mean(0), moy_eq_T)
        rng = np.random.default_rng(1)
        boot = []
        for _ in range(200):
            ii = rng.integers(0, R, R)
            b = demi_temps(grille, tv[ii].mean(0), moy_eq_T)
            boot.append(np.nan if b is None else b / mk)
        ligne = {"N": n, "R": R, "rodage_balayages": rod, "espacement_balayages": esp, "balayages_max": bmax,
                 "Tv_eq_sommet_suivi": moy_eq, "Tv_eq_3T_sur_n": moy_eq_T, "Tv_naissance": float(tv[:, 0].mean()),
                 "Tv_fin": float(tv[:, -1].mean()),
                 "t_demi_balayages": None if t is None else t / mk,
                 "t_demi_IC90": [float(np.nanpercentile(boot, 5)), float(np.nanpercentile(boot, 95))],
                 "grille_balayages": [g / mk for g in grille], "courbe_Tv": tv.mean(0).tolist()}
        out.append(ligne)
        print(n, {x: ligne[x] for x in ("Tv_eq_3T_sur_n", "Tv_naissance", "Tv_fin", "t_demi_balayages", "t_demi_IC90")},
              flush=True)
        (ICI / sortie).write_text(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
