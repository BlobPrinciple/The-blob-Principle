#!/usr/bin/env python3
"""DEFI-M11 — diagnostic : la chaîne d'équilibre de pi_{N+1, M+k} mélange-t-elle ?

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
Pour chaque taille du Monte-Carlo, quatre chaînes indépendantes (graines et graphes
de départ différents) ; on compare leurs moyennes de T_v (triangles d'un sommet),
T et D sur deux moitiés de leur trajectoire, et le taux d'acceptation.
Usage : python3 defi_m11_diagnostic_equilibre.py -> defi_m11_diagnostic_equilibre.json
"""
import json
import math
import pathlib

import numpy as np

import defi_m11_monte_carlo as mc

ICI = pathlib.Path(__file__).resolve().parent


def chaine(n1, m1, graine, rodage_bal, n_mes, pas_bal):
    rng = np.random.default_rng(graine)
    mc.graine_numba(graine)
    adj, aretes = mc.graphe_aleatoire(n1, m1, rng)
    deg, etat = mc.etat_de(adj)
    mc.balayer(adj, aretes, deg, etat, n1, rodage_bal * m1)
    obs = np.zeros((n_mes, 3))
    acc = 0
    for i in range(n_mes):
        acc += mc.balayer(adj, aretes, deg, etat, n1, pas_bal * m1)
        mu = 2.0 * m1 / n1
        D = math.sqrt(max(etat[1] / n1 - mu * mu, 0.0)) / mu
        obs[i] = (np.mean([mc.tri_sommet(adj, n1, v) for v in range(n1)]), etat[0], D)
    return obs, acc / (n_mes * pas_bal * m1)


def main():
    out = []
    for n in (8, 12, 16, 24, 32, 48):
        m, k = 2 * n - 2, 4
        n1, m1 = n + 1, m + k
        lignes = []
        for g in range(4):
            obs, acc = chaine(n1, m1, 1000 + 17 * g + n, rodage_bal=200, n_mes=2000, pas_bal=5)
            h = len(obs) // 2
            lignes.append({"graine": 1000 + 17 * g + n, "acceptation": acc,
                           "moy_moitie_1": obs[:h].mean(0).tolist(), "moy_moitie_2": obs[h:].mean(0).tolist(),
                           "sd": obs.std(0).tolist()})
        moy = np.array([l["moy_moitie_1"] + l["moy_moitie_2"] for l in lignes]).reshape(-1, 3)
        sd = np.array(lignes[0]["sd"])
        ecart = ((moy.max(0) - moy.min(0)) / np.where(sd > 0, sd, 1)).tolist()
        out.append({"N_plus_1": n1, "M_plus_k": m1, "chaines": lignes,
                    "etendue_des_8_demi_moyennes_en_sd": ecart})
        print(n1, "acc", [round(l["acceptation"], 4) for l in lignes], "étendue (T_v, T, D) en sd :", np.round(ecart, 3),
              "T_v", np.round(moy[:, 0], 2), flush=True)
    (ICI / "defi_m11_diagnostic_equilibre.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
