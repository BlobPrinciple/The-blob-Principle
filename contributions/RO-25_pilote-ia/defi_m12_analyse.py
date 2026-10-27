#!/usr/bin/env python3
"""DEFI-M12 — analyse : forme de la croissance de t½(n), prédiction hors échantillon, recoupements.

Pilote IA du laboratoire (Claude, Anthropic), 27 octobre 2026.
Lit defi_m12_lenteur.json (méthode stationnaire), defi_m12_second_moteur*.json (seconde
implémentation), defi_m11_demi_temps.json et defi_m12_naissance.json (méthode naissance).
Trois formes ajustées par moindres carrés sur log t½, poids égaux, n ≥ 25 :
  puissance      log t = a·log n + b
  exponentielle  log t = a·n + b
  étirée         log t = a·sqrt(n) + b
Prédiction hors échantillon : ajustement sur n ≤ 97, prédiction à n = 129 et 193.
Usage : python3 defi_m12_analyse.py -> defi_m12_analyse.json
"""
import json
import math
import pathlib

import numpy as np

from defi_m12_lenteur import delta_pour

ICI = pathlib.Path(__file__).resolve().parent
FORMES = {"puissance": np.log, "exponentielle": lambda n: n, "etiree_racine": np.sqrt}


def ajuste(n, t, forme):
    x = FORMES[forme](np.asarray(n, float))
    y = np.log(t)
    a, b = np.polyfit(x, y, 1)
    res = y - (a * x + b)
    return a, b, float((res ** 2).sum()), float(np.abs(res).max())


def main():
    chaines = []
    for nom, reg in (("defi_m12_lenteur.json", "c2"), ("defi_m12_lenteur_c3_c2T.json", "c3"),
                     ("defi_m12_lenteur_c2T.json", "c2T")):
        chaines += [c for c in json.loads((ICI / nom).read_text())["chaines"] if c["reglage"] == reg]
    # on ne garde que les chaînes dont l'espacement est celui du code actuel (delta_pour)
    chaines = [c for c in chaines if c["delta"] == delta_pour(c["n"], c["reglage"])]
    R = {}
    for reg in ("c2", "c3", "c2T"):
        for n in sorted(set(c["n"] for c in chaines if c["reglage"] == reg)):
            C = [c for c in chaines if c["reglage"] == reg and c["n"] == n]
            v = [c["t_demi"] for c in C]
            R.setdefault(reg, {})[str(n)] = {
                "t_demi": [float(np.mean(v)), float(np.std(v, ddof=1) / math.sqrt(len(v))), len(v)],
                "t_1e": float(np.mean([c["t_1e"] for c in C])),
                "t_demi_sur_delta": float(np.mean(v)) / C[0]["delta"],
                "longueur_sur_t_demi": C[0]["L"] * C[0]["delta"] / float(np.mean(v)),
                "rodage_sur_t_demi": C[0]["rodage_balayages"] / float(np.mean(v)),
                "T_ecart_departs": float(np.mean([c["T_moy_moitie2"] for c in C if c["plante"]])
                                         - np.mean([c["T_moy_moitie2"] for c in C if not c["plante"]])),
                "T_sd": float(np.mean([c["T_sd"] for c in C])),
                "Tv_moy": float(np.mean([c["Tv_moy"] for c in C])),
                "part_Tv_sup6": float(np.mean([c["part_Tv_sup6"] for c in C]))}
    out_resume = R
    out = {"resume": out_resume, "stationnaire": {}}
    for reg in R:
        ns = sorted(int(x) for x in R[reg])
        t = [R[reg][str(n)]["t_demi"][0] for n in ns]
        e = [R[reg][str(n)]["t_demi"][1] for n in ns]
        bloc = {"n": ns, "t_demi": t, "erreur": e,
                "T_ecart_departs_plante_moins_aleatoire": [R[reg][str(n)]["T_ecart_departs"] for n in ns],
                "T_sd": [R[reg][str(n)]["T_sd"] for n in ns]}
        bloc["pentes_locales_loglog"] = [math.log(t[i + 1] / t[i]) / math.log(ns[i + 1] / ns[i]) for i in range(len(ns) - 1)]
        bloc["pentes_locales_log_t_par_racine_n"] = [math.log(t[i + 1] / t[i]) / (math.sqrt(ns[i + 1]) - math.sqrt(ns[i]))
                                                    for i in range(len(ns) - 1)]
        sel = [i for i, n in enumerate(ns) if n >= 25]
        if len(sel) >= 3:
            bloc["ajustements_n_ge_25"] = {}
            for f in FORMES:
                a, b, rss, mx = ajuste([ns[i] for i in sel], [t[i] for i in sel], f)
                bloc["ajustements_n_ge_25"][f] = {"a": a, "b": b, "somme_carres_residus_log": rss, "residu_max_log": mx}
            # exposant libre : log t = a·n^g + b (scipy.optimize.curve_fit), n ≥ 25 et n ≥ 49
            from scipy.optimize import curve_fit
            for nmin in ((25, 49) if reg != "c2T" else ()):
                ii = [i for i, n in enumerate(ns) if n >= nmin]
                if len(ii) >= 4:
                    xx = np.array([ns[i] for i in ii], float)
                    yy = np.log([t[i] for i in ii])
                    pp, cc = curve_fit(lambda x, a, g, b: a * x ** g + b, xx, yy, p0=(1.0, 0.5, 0.0), maxfev=20000)
                    bloc.setdefault("exposant_libre", {})["n_ge_%d" % nmin] = {
                        "a": pp[0], "gamma": pp[1], "gamma_erreur": float(np.sqrt(cc[1, 1])), "b": pp[2]}
                    print("  [%s] exposant libre (n ≥ %d) : log t½ = %.3f·n^%.3f (± %.3f) %+.2f" % (
                        reg, nmin, pp[0], pp[1], np.sqrt(cc[1, 1]), pp[2]))
            appr = [i for i in sel if ns[i] <= 97]
            test = [i for i, n in enumerate(ns) if n > 97]
            if len(appr) >= 3 and test:
                bloc["prediction_hors_echantillon"] = {}
                for f in FORMES:
                    a, b, _, _ = ajuste([ns[i] for i in appr], [t[i] for i in appr], f)
                    bloc["prediction_hors_echantillon"][f] = {
                        str(ns[i]): {"predit": float(math.exp(a * FORMES[f](float(ns[i])) + b)), "mesure": t[i],
                                     "rapport_mesure_sur_predit": t[i] / float(math.exp(a * FORMES[f](float(ns[i])) + b))}
                        for i in test}
        out["stationnaire"][reg] = bloc
        print("==", reg)
        for i, n in enumerate(ns):
            q = R[reg][str(n)]
            print("  n = %3d  t½ = %9.1f ± %6.1f  t½/Δ %5.1f  durée/t½ %5.0f  rodage/t½ %5.1f  ΔT(planté−aléat.) %+.2f (sd T %.1f)  part T_v>6 %.2f" % (
                n, t[i], e[i], q["t_demi_sur_delta"], q["longueur_sur_t_demi"], q["rodage_sur_t_demi"],
                bloc["T_ecart_departs_plante_moins_aleatoire"][i], bloc["T_sd"][i], q["part_Tv_sup6"]))
        print("  pentes log-log :", [round(x, 2) for x in bloc["pentes_locales_loglog"]])
        print("  pentes log t / sqrt n :", [round(x, 3) for x in bloc["pentes_locales_log_t_par_racine_n"]])
        for f, v in bloc.get("ajustements_n_ge_25", {}).items():
            print("  %-14s a = %.4f  RSS = %.4f  résidu max = %.3f" % (f, v["a"], v["somme_carres_residus_log"], v["residu_max_log"]))
        for f, v in bloc.get("prediction_hors_echantillon", {}).items():
            print("  prédiction (n ≤ 97) %-14s" % f, {k: (round(w["predit"]), round(w["rapport_mesure_sur_predit"], 2)) for k, w in v.items()})
    # recoupements
    rec = {}
    m11 = json.loads((ICI / "defi_m11_demi_temps.json").read_text())
    naiss = {}
    for l in m11["lignes"]:
        if l["theta"] == 0.0 and l["t_demi_balayages"]:
            naiss.setdefault(l["N"] + 1, []).append(l["t_demi_balayages"])
    for nom in ("defi_m12_naissance_96.json", "defi_m12_naissance_128.json"):
        p = ICI / nom
        if not p.exists():
            continue
        for l in json.loads(p.read_text()):
            naiss.setdefault(l["N"] + 1, []).append(l["t_demi_balayages"])
            rec.setdefault("naissance_IC90", {})[str(l["N"] + 1)] = l["t_demi_IC90"]
    rec["naissance_vs_stationnaire_c2"] = {str(n): {"naissance": v, "stationnaire": R["c2"].get(str(n), {}).get("t_demi", [None])[0]}
                                           for n, v in sorted(naiss.items())}
    sec = {}
    for nom in ("defi_m12_second_moteur.json", "defi_m12_second_moteur_c3.json"):
        q = ICI / nom
        if q.exists():
            for r in json.loads(q.read_text()):
                reg = "c3" if r["c"] == 3 else "c2"
                sec.setdefault(reg, {}).setdefault(str(r["n"]), []).append(r["t_demi"])
    rec["second_moteur"] = {reg: {n: {"second": float(np.mean(v)), "premier": R[reg][n]["t_demi"][0],
                                      "ecart_relatif": float(np.mean(v)) / R[reg][n]["t_demi"][0] - 1}
                                  for n, v in dd.items() if n in R[reg]} for reg, dd in sec.items()}
    out["recoupements"] = rec
    q = ICI / "defi_m12_structure.json"
    if q.exists():
        st = {r["n"]: r["clique_max"] for r in json.loads(q.read_text())["instantanes"]}
        ns = [n for n in sorted(st) if n >= 33 and str(n) in R["c2"]]
        x = np.array([st[n] for n in ns])
        y = np.log([R["c2"][str(n)]["t_demi"][0] for n in ns])
        a, b = np.polyfit(x, y, 1)
        r = y - (a * x + b)
        out["t_demi_c2_contre_clique_max"] = {"n": ns, "clique_max": x.tolist(), "pente": a, "ordonnee": b,
                                              "residu_max_log": float(np.abs(r).max())}
        print("log t½ (c2) = %.3f · clique_max %+.3f, résidu max %.3f (n ≥ 33)" % (a, b, np.abs(r).max()))
    print(json.dumps(rec, indent=1, ensure_ascii=False))
    (ICI / "defi_m12_analyse.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
