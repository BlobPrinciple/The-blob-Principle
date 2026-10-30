#!/usr/bin/env python3
"""DEFI-M13 — analyse : barrière de P(T_v) contre la lenteur mesurée par DEFI-M12.

Pilote IA du laboratoire (Claude, Anthropic), 30 octobre 2026.
Lit defi_m13_profil_c2.json, defi_m13_profil_c2_grand.json, defi_m13_profil_lambda.json,
defi_m13_profil_c3.json, defi_m13_second_moteur.json, defi_m13_second_moteur_257.json,
defi_m13_sorties.json, defi_m12_analyse.json, defi_m12_arrhenius.json ; écrit
defi_m13_analyse.json.

Quatre estimateurs de la barrière de sortie de l'aristocratie, F = −log P :
  brut   : F(col) − F(minimum aristocratique) sur les valeurs entières de T ;
  k      : même chose après regroupement de T en classes [C(k,2), C(k+1,2)) (k = « degré
           de clique » équivalent) ;
  lissé  : même chose sur P lissé par une moyenne glissante de 5 cases ;
  mfpt   : log du temps moyen de premier passage d'une diffusion unité le long de T,
           du minimum aristocratique au minimum roturier : log Σ_x e^{F(x)} Σ_{y>x} e^{−F(y)}.
Ces estimateurs ne sont pas des temps : seule leur variation avec n (ou lam) se compare à
celle de log t½.
"""
import json
import pathlib

import numpy as np

ICI = pathlib.Path(__file__).resolve().parent


def charger(nom):
    return json.loads((ICI / nom).read_text())


def classes_k(logP):
    P = np.array([0.0 if x is None else np.exp(x) for x in logP])
    T = np.arange(len(P))
    k = np.floor((1 + np.sqrt(1 + 8 * T)) / 2).astype(int)
    Pk = np.bincount(k, weights=P)
    with np.errstate(divide="ignore"):
        return -np.log(np.where(Pk > 0, Pk, np.nan)), P


def barriere(F):
    ok = np.where(np.isfinite(F))[0]
    haut = ok[ok >= ok.max() // 2]
    ia = haut[np.nanargmin(F[haut])]
    bas = ok[ok <= ia // 3]
    ir = bas[np.nanargmin(F[bas])]
    mil = ok[(ok > ir) & (ok < ia)]
    if len(mil) == 0:
        return 0.0, int(ir), int(ia), int(ia)
    ic = mil[np.nanargmax(F[mil])]
    return float(F[ic] - F[ia]), int(ir), int(ic), int(ia)


def estimateurs(logP):
    Fraw = np.array([np.nan if x is None else -x for x in logP])
    Fk, P = classes_k(logP)
    with np.errstate(divide="ignore"):
        Fl = -np.log(np.convolve(P, np.ones(5) / 5, "same"))
    Fl[~np.isfinite(Fl)] = np.nan
    b_brut, ir, ic, ia = barriere(Fraw)
    tot = 0.0
    for x in range(ir, ia):
        if P[x] > 0:
            tot += P[x + 1:].sum() / P[x]
    return {"brut": b_brut, "k": barriere(Fk)[0], "lisse": barriere(Fl)[0], "mfpt": float(np.log(tot)),
            "T_rot": ir, "T_col": ic, "T_ari": ia, "k_ari": int(np.floor((1 + np.sqrt(1 + 8 * ia)) / 2))}


NOMS = ("brut", "k", "lisse", "mfpt")


def resumer(points, filtre):
    par = {}
    for r in points:
        if filtre(r):
            par.setdefault((r["reglage"], r["n"], r["lam"]), []).append(estimateurs(r["logP"]))
    out = {}
    for cle, L in sorted(par.items()):
        out[cle] = {nom: (float(np.mean([e[nom] for e in L])), float(np.std([e[nom] for e in L], ddof=1)) if len(L) > 1 else None)
                    for nom in NOMS}
        out[cle]["repetitions"] = len(L)
        out[cle]["T_ari"] = float(np.mean([e["T_ari"] for e in L]))
        out[cle]["k_ari"] = float(np.mean([e["k_ari"] for e in L]))
    return out


def ecart_profils(p1, p2):
    F2 = np.array([np.nan if x is None else -x for x in p2["logP"]])
    F1 = np.array([np.nan if x is None else -x for x in p1["logP"]])[:len(F2)]
    d = F1 - F2
    ok = np.isfinite(d) & (F1 < np.nanmin(F1) + 16)
    d = d - d[ok].mean()
    return float(np.sqrt((d[ok] ** 2).mean())), float(np.abs(d[ok]).max())


def main():
    m12 = charger("defi_m12_analyse.json")["resume"]
    arr = charger("defi_m12_arrhenius.json")["points"]
    c2 = charger("defi_m13_profil_c2.json")["points"] + charger("defi_m13_profil_c2_grand.json")["points"]
    c2 = [r for r in c2 if r["n"] != 385]  # n = 385 : production bloquée (voir rapport), exclu
    lam = charger("defi_m13_profil_lambda.json")["points"]
    c3 = charger("defi_m13_profil_c3.json")["points"]
    sec = charger("defi_m13_second_moteur.json")["points"] + charger("defi_m13_second_moteur_257.json")["points"]
    sor = charger("defi_m13_sorties.json")["chaines"]
    out = {}

    print("A. Degré moyen 4, mesure de l'armature (lam = 2n) : barrières (moyenne ± écart-type entre répétitions)")
    A = resumer(c2, lambda r: True)
    S = resumer(sec, lambda r: True)
    lignes = []
    print("   n  rép  ln t½   brut         k            lissé        mfpt         | second : brut   k     lissé  mfpt | k_ari | séjour  séjour/t½")
    for (reg, n, l), v in A.items():
        lt = float(np.log(m12["c2"][str(n)]["t_demi"][0])) if str(n) in m12["c2"] else None
        sj = [c["sejour_balayages"] for c in sor if c["n"] == n]
        sejour = float(np.mean(sj)) if sj else None
        s = S.get((reg, n, l))
        lignes.append({"n": n, "lam": l, "ln_t_demi_M12": lt, "premier": v, "second": s, "sejour": sejour,
                       "sejour_sur_t_demi": (sejour / np.exp(lt)) if (sejour and lt) else None})
        fmt = lambda x: "%5.2f ± %4.2f" % (x[0], x[1] if x[1] is not None else float("nan"))
        print("%4d  %d  %6s  %s  %s  %s  %s | %s | %5.1f | %s  %s" % (
            n, v["repetitions"], "%.2f" % lt if lt else "  —  ", fmt(v["brut"]), fmt(v["k"]), fmt(v["lisse"]), fmt(v["mfpt"]),
            " ".join("%5.2f" % s[nm][0] for nm in NOMS) if s else "—", v["k_ari"],
            "%.0f" % sejour if sejour else "—", "%.2f" % (sejour / np.exp(lt)) if (sejour and lt) else "—"))
    out["c2"] = lignes

    print("\nB. Écart entre les deux implémentations (profil F, après recentrage, cases à moins de 16 du minimum)")
    ec = []
    for s in sec:
        for r in [r for r in c2 if r["n"] == s["n"]]:
            ec.append({"n": s["n"], "rms": ecart_profils(r, s)[0], "max": ecart_profils(r, s)[1]})
    for n in sorted({e["n"] for e in ec}):
        E = [e for e in ec if e["n"] == n]
        print("   n = %d : rms %.2f à %.2f, écart maximal %.2f" % (n, min(e["rms"] for e in E), max(e["rms"] for e in E), max(e["max"] for e in E)))
    out["ecarts_implementations"] = ec

    print("\nB bis. Contrôle par histogramme direct non biaisé (premier moteur, n ≤ 65 ; cases à moins de 8 du minimum)")
    for r in c2:
        if r["n"] > 65:
            continue
        Hd = np.array(r["H_direct"], float)
        F1 = np.array([np.nan if x is None else -x for x in r["logP"]])
        with np.errstate(divide="ignore"):
            Fd = -np.log(np.where(Hd > 0, Hd, np.nan))
        d = F1 - Fd
        ok = np.isfinite(d) & (F1 < np.nanmin(F1) + 8)
        d = d - d[ok].mean()
        print("   n = %d, graine %d : rms %.2f, max %.2f" % (r["n"], r["graine"], np.sqrt((d[ok] ** 2).mean()), np.abs(d[ok]).max()))

    print("\nC. log t½ (DEFI-M12) contre B, n = 33 à 193 : ln t½ = a·B + b ; prédiction à n = 257")
    fit = [x for x in lignes if 33 <= x["n"] <= 193]
    y = np.array([x["ln_t_demi_M12"] for x in fit])
    l257 = [x for x in lignes if x["n"] == 257][0]
    pred = {}
    for nm in NOMS:
        xx = np.array([x["premier"][nm][0] for x in fit])
        a, b = np.polyfit(xx, y, 1)
        r = y - (a * xx + b)
        p1 = a * l257["premier"][nm][0] + b
        p2 = a * l257["second"][nm][0] + b
        pred[nm] = {"pente": float(a), "ordonnee": float(b), "residu_max": float(np.abs(r).max()),
                    "prediction_257_premier": float(p1), "prediction_257_second": float(p2)}
        print("   %-6s pente %.3f, résidu max %.2f ; ln t½(257) prédit %.2f (premier moteur), %.2f (second)" % (nm, a, np.abs(r).max(), p1, p2))
    ext = 0.964 * np.sqrt(257) - 1.77
    print("   loi de DEFI-M12, log t½ = 0,964·√n − 1,77, extrapolée : %.2f" % ext)
    # sensibilité au modèle de calibration (relecture hostile) : pente du dernier intervalle, quadratique
    print("   sensibilité au modèle de calibration (premier moteur) :")
    for nm in NOMS:
        xx = np.array([x["premier"][nm][0] for x in fit])
        a_loc = (y[-1] - y[-2]) / (xx[-1] - xx[-2])
        p_loc = y[-1] + a_loc * (l257["premier"][nm][0] - xx[-1])
        p_quad = float(np.polyval(np.polyfit(xx, y, 2), l257["premier"][nm][0]))
        pentes = np.diff(y) / np.diff(xx)
        pred[nm].update({"prediction_257_pente_locale": float(p_loc), "prediction_257_quadratique": p_quad,
                         "pentes_locales": pentes.tolist()})
        print("   %-6s pentes locales %s ; pente locale -> %.2f ; quadratique -> %.2f" % (
            nm, " ".join("%.2f" % v for v in pentes), p_loc, p_quad))
    out["prediction_257"] = {"estimateurs": pred, "loi_racine_M12": float(ext)}

    print("\nD. Croissance de B avec n (n = 33 à 257, premier moteur)")
    ns = np.array([x["n"] for x in lignes if x["n"] >= 33], float)
    formes = {}
    for nm in NOMS:
        yy = np.array([x["premier"][nm][0] for x in lignes if x["n"] >= 33])
        r1 = yy - np.polyval(np.polyfit(np.sqrt(ns), yy, 1), np.sqrt(ns))
        r2 = yy - np.polyval(np.polyfit(ns, yy, 1), ns)
        # exposant libre : B = a·n^g + b, balayage de g
        best = None
        for g in np.linspace(0.3, 1.5, 241):
            c = np.polyfit(ns ** g, yy, 1)
            s2 = float(((yy - np.polyval(c, ns ** g)) ** 2).sum())
            if best is None or s2 < best[1]:
                best = (float(g), s2)
        pente_rac = np.diff(yy) / np.diff(np.sqrt(ns))
        formes[nm] = {"ssr_racine": float((r1 ** 2).sum()), "ssr_lineaire": float((r2 ** 2).sum()), "exposant_libre": best[0],
                      "pentes_par_racine_n": pente_rac.tolist()}
        print("   %-6s SCR √n %.2f ; SCR n %.2f ; exposant libre %.2f ; ΔB/Δ√n : %s" % (
            nm, (r1 ** 2).sum(), (r2 ** 2).sum(), best[0], " ".join("%.2f" % p for p in pente_rac)))
    for bornes in ((65, 193), (33, 193)):
        sel_n = np.array([x["n"] for x in lignes if bornes[0] <= x["n"] <= bornes[1]], float)
        for nm in NOMS:
            yy = np.array([x["premier"][nm][0] for x in lignes if bornes[0] <= x["n"] <= bornes[1]])
            r1 = yy - np.polyval(np.polyfit(np.sqrt(sel_n), yy, 1), np.sqrt(sel_n))
            r2 = yy - np.polyval(np.polyfit(sel_n, yy, 1), sel_n)
            best = min(((float(((yy - np.polyval(np.polyfit(sel_n ** g, yy, 1), sel_n ** g)) ** 2).sum()), float(g))
                        for g in np.linspace(0.3, 1.5, 241)))
            formes[nm]["n_%d_%d" % bornes] = {"ssr_racine": float((r1 ** 2).sum()), "ssr_lineaire": float((r2 ** 2).sum()),
                                               "exposant_libre": best[1]}
            print("   n = %d à %d, %-6s SCR √n %.2f ; SCR n %.2f ; exposant libre %.2f" % (
                bornes[0], bornes[1], nm, (r1 ** 2).sum(), (r2 ** 2).sum(), best[1]))
    out["croissance_B"] = formes

    print("\nE. n = 65, lam variable (DEFI-M12, test à n fixé) : B contre ln t½")
    Lm = resumer(lam, lambda r: True)
    Lm[("c2", 65, 130.0)] = A[("c2", 65, 130.0)]
    tl = {66.0: float(np.log(m12["c2T"]["65"]["t_demi"][0])), 130.0: float(np.log(m12["c2"]["65"]["t_demi"][0]))}
    for p in arr:
        if p["n"] == 65:
            tl[p["lam"]] = float(np.log(p["t_demi"]))
    le = []
    for (reg, n, l), v in sorted(Lm.items(), key=lambda kv: kv[0][2]):
        le.append({"lam": l, "ln_t_demi_M12": tl[l], **{nm: v[nm][0] for nm in NOMS}, "k_ari": v["k_ari"]})
        print("   λ = %3.0f  ln t½ %.2f  brut %.2f  k %.2f  lissé %.2f  mfpt %.2f  k_ari %.1f" % (
            l, tl[l], v["brut"][0], v["k"][0], v["lisse"][0], v["mfpt"][0], v["k_ari"]))
    sel = [x for x in le if x["lam"] >= 98]
    for nm in NOMS:
        a = np.polyfit([x["lam"] for x in sel], [x[nm] for x in sel], 1)[0]
        print("   pente dB/dλ (λ ≥ 98) %-6s %.4f" % (nm, a))
    a = np.polyfit([x["lam"] for x in sel], [x["ln_t_demi_M12"] for x in sel], 1)[0]
    print("   pente d ln t½/dλ (λ ≥ 98)      %.4f" % a)
    out["lambda_n65"] = le

    print("\nF. Degré moyen 6 (M = 3n, lam = 2n)")
    C = resumer(c3, lambda r: True)
    lc = []
    for (reg, n, l), v in C.items():
        lt = float(np.log(m12["c3"][str(n)]["t_demi"][0]))
        lc.append({"n": n, "ln_t_demi_M12": lt, **{nm: v[nm][0] for nm in NOMS}, "k_ari": v["k_ari"]})
        print("   n = %3d  ln t½ %.2f  brut %.2f  k %.2f  lissé %.2f  mfpt %.2f  k_ari %.1f" % (
            n, lt, v["brut"][0], v["k"][0], v["lisse"][0], v["mfpt"][0], v["k_ari"]))
    out["c3"] = lc
    (ICI / "defi_m13_analyse.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
