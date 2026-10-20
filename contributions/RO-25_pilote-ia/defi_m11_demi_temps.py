#!/usr/bin/env python3
"""DEFI-M11 — demi-temps de relaxation des triangles du nouveau-né, et loi d'échelle en N.

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
Lit defi_m11_monte_carlo.json et defi_m11_monte_carlo_long.json. Demi-temps t½ : premier
temps (interpolation log-linéaire sur la grille) où l'écart de la moyenne de T_v à
l'équilibre tombe sous la moitié de l'écart à la naissance ; exprimé en balayages
(échanges / (M + k)). Intervalle à 90 % par bootstrap sur les courbes moyennes
n'est pas disponible (courbes individuelles non sauvegardées) : on donne à la place
la dispersion entre theta et entre les deux campagnes. Ajustement t½ ∝ N^a par
moindres carrés en log-log.
Usage : python3 defi_m11_demi_temps.py  ->  defi_m11_demi_temps.json
"""
import json
import pathlib

import numpy as np

ICI = pathlib.Path(__file__).resolve().parent


def demi_temps(grille, courbe, eq):
    e = np.abs(np.array(courbe) - eq)
    cible = e[0] / 2
    for g in range(1, len(grille)):
        if e[g] <= cible:
            t0, t1 = max(grille[g - 1], 0.5), grille[g]
            e0, e1 = e[g - 1], e[g]
            f = (e0 - cible) / (e0 - e1) if e0 != e1 else 1.0
            return float(np.exp(np.log(t0) + f * (np.log(t1) - np.log(t0))))
    return None


def main():
    lignes = []
    for nom in ("defi_m11_monte_carlo.json", "defi_m11_monte_carlo_long.json"):
        d = json.loads((ICI / nom).read_text())
        for L in d["tailles"]:
            mk = L["M"] + L["k"]
            for th, v in L["par_theta"].items():
                c = [x[0] for x in v["courbe_moyenne"]]
                t = demi_temps(L["grille"], c, L["equilibre_moy"][0])
                lignes.append({"campagne": nom, "N": L["N"], "theta": float(th), "R": d["R_naissances_par_theta"],
                               "ecart_reduit_naissance": (c[0] - L["equilibre_moy"][0]) / L["equilibre_sd"][0],
                               "t_demi_balayages": None if t is None else t / mk})
    ok = [l for l in lignes if l["t_demi_balayages"]]
    N = np.array([l["N"] for l in ok], float)
    t = np.array([l["t_demi_balayages"] for l in ok])
    sel = N >= 12
    a, b = np.polyfit(np.log(N[sel]), np.log(t[sel]), 1)
    res = {"lignes": lignes, "ajustement_N_ge_12": {"exposant": a, "prefacteur": float(np.exp(b))}}
    for l in lignes:
        print(l["campagne"][9:], l["N"], l["theta"], "écart naissance", round(l["ecart_reduit_naissance"], 2),
              "t½ (balayages)", None if l["t_demi_balayages"] is None else round(l["t_demi_balayages"], 1))
    print("t½ ∝ N^%.2f (N ≥ 12, tous theta)" % a)
    for th in sorted(set(l["theta"] for l in ok)):
        s = [(l["N"], l["t_demi_balayages"]) for l in ok if l["theta"] == th and l["N"] >= 12
             and l["campagne"] == "defi_m11_monte_carlo.json"]
        if len(s) >= 3:
            aa = np.polyfit(np.log([x[0] for x in s]), np.log([x[1] for x in s]), 1)[0]
            res.setdefault("exposant_par_theta_campagne_principale", {})[str(th)] = aa
            print("  theta", th, "exposant", round(aa, 2))
    (ICI / "defi_m11_demi_temps.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
