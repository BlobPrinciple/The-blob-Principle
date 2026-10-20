#!/usr/bin/env python3
"""DEFI-M11 — lecture de la carte exacte (defi_m11_carte.json).

Pour chaque cas : G* gagne-t-il à la naissance (TV(theta=1) < TV(theta=0) − 1e-9) ?
quel theta relaxe le plus vite (t pour TV ≤ 0,01) ? l'ordre est-il monotone en theta ?
Classement par densité d'arrivée (degré moyen 2(M + k)/(N + 1)).
Usage : python3 defi_m11_carte_analyse.py [fichier]  ->  defi_m11_carte_analyse.json
"""
import json
import pathlib
import sys
from collections import Counter

ICI = pathlib.Path(__file__).resolve().parent


def main():
    f = sys.argv[1] if len(sys.argv) > 1 else "defi_m11_carte.json"
    d = json.loads((ICI / f).read_text())
    cas = d["cas"] if isinstance(d, dict) else d
    TH = ["-1.0", "-0.5", "0.0", "0.5", "1.0"]
    lignes = []
    for c in cas:
        t = [c[f"theta={x}"]["t_TV_0_01"] for x in TH]
        tv = [c[f"theta={x}"]["TV_naissance"] for x in TH]
        gagne = tv[4] < tv[2] - 1e-9
        tmin = min(t)
        plus_rapides = [TH[i] for i in range(5) if t[i] == tmin]
        croissant = all(t[i] <= t[i + 1] for i in range(4))
        decroissant = all(t[i] >= t[i + 1] for i in range(4))
        kbar = 2 * (c["M"] + c["k"]) / (c["N"] + 1)
        lignes.append({"N": c["N"], "M": c["M"], "k": c["k"], "degre_moyen_arrivee": kbar, "t": t, "TV0": tv,
                       "G_gagne_naissance": gagne, "plus_rapides": plus_rapides,
                       "t_croissant_en_theta": croissant, "t_decroissant_en_theta": decroissant,
                       "rapport_t_G_sur_U": t[4] / t[2] if t[2] else None,
                       "rapport_t_antiG1_sur_U": t[0] / t[2] if t[2] else None})
    res = {"cas": lignes, "resume": {}}
    for nom, filtre in (("tous", lambda l: True), ("G* gagne à la naissance", lambda l: l["G_gagne_naissance"]),
                        ("G* gagne, degré moyen d'arrivée ≥ 2", lambda l: l["G_gagne_naissance"] and l["degre_moyen_arrivee"] >= 2),
                        ("G* gagne, degré moyen d'arrivée < 2", lambda l: l["G_gagne_naissance"] and l["degre_moyen_arrivee"] < 2)):
        L = [l for l in lignes if filtre(l)]
        if not L:
            continue
        r = {"n": len(L),
             "G_plus_lent_que_U": sum(1 for l in L if l["t"][4] > l["t"][2]),
             "G_egal_U": sum(1 for l in L if l["t"][4] == l["t"][2]),
             "G_plus_rapide_que_U": sum(1 for l in L if l["t"][4] < l["t"][2]),
             "antiG1_plus_rapide_que_U": sum(1 for l in L if l["t"][0] < l["t"][2]),
             "antiG1_plus_lent_que_U": sum(1 for l in L if l["t"][0] > l["t"][2]),
             "croissant_en_theta": sum(1 for l in L if l["t_croissant_en_theta"]),
             "decroissant_en_theta": sum(1 for l in L if l["t_decroissant_en_theta"]),
             "theta_le_plus_rapide": dict(Counter(x for l in L for x in l["plus_rapides"])),
             "rapport_t_G_sur_U_min_max": [min(l["rapport_t_G_sur_U"] for l in L), max(l["rapport_t_G_sur_U"] for l in L)]}
        res["resume"][nom] = r
        print(nom, json.dumps(r, ensure_ascii=False))
    (ICI / f.replace(".json", "_analyse.json")).write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
