#!/usr/bin/env python3
"""DEFI-R5 — Chasse aux incohérences JSON ↔ master V346 (implémentation A, numpy).

Chaque contrôle lit un JSON du corpus, recalcule la grandeur que le master V346
cite, et la compare à la valeur imprimée (recopiée à la main du texte, page
indiquée). Sortie : r5_audit_sortie.json et un tableau texte.

Usage : python3 contributions/R5_pilote-ia/r5_audit.py   (depuis la racine du dépôt)
"""
import json, math, os, sys
import numpy as np

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
C = os.path.join(RACINE, "corpus")


def charge(*p):
    with open(os.path.join(C, *p), encoding="utf-8") as f:
        return json.load(f)


res = []


def note(code, objet, json_rel, cite, reel, verdict, detail=""):
    res.append(dict(code=code, objet=objet, json=json_rel, valeur_citee=cite,
                    valeur_json=reel, verdict=verdict, detail=detail))


# ---------------------------------------------------------------- E1
p = ("06_campagnes_et_sauts", "SAUT 9 et 10 et 11", "Manifestes v99 et addendum v102",
     "EXPECTED_OUTPUT_v93_updated 2.json")
d = charge(*p)


def cherche(o, cle):
    if isinstance(o, dict):
        if cle in o:
            return o[cle]
        for v in o.values():
            r = cherche(v, cle)
            if r is not None:
                return r
    return None


ds = {N: cherche(d, "ds_N%d" % N) for N in (300, 500, 1000, 3000)}
for N in (260, 400):
    assert cherche(d, "ds_N%d" % N) is None
v1000 = ds[1000]
ecart = abs(3 - v1000["value"]) / 3
note("E1", "M-7.1 (p. 173) : ligne N=1000 du tableau « convergence d_s → 3 »",
     "/".join(p), "N=1000 : 20 graines, 3.045 ± 0.026, écart 1.5 %",
     "ds_N1000 = %.3f ± %.3f, %d graines, écart à 3 = %.1f %% ; ds_N3000 = %.3f ± %.3f, %d graines ; "
     "aucune entrée N=260 ni N=400" % (v1000["value"], v1000["uncertainty"], v1000["seeds"], 100 * ecart,
                                      ds[3000]["value"], ds[3000]["uncertainty"], ds[3000]["seeds"]),
     "INCOHÉRENT",
     "La ligne N=1000 recopie la ligne N=3000. Série du JSON : %s." %
     ", ".join("N=%d : %.3f" % (N, ds[N]["value"]) for N in (300, 500, 1000, 3000)))
serie = [ds[N]["value"] for N in (300, 500, 1000)]
assert serie[0] > serie[1] > serie[2]  # décroissance de 300 à 1000

# ---------------------------------------------------------------- E2
p = ("06_campagnes_et_sauts", "Test O2v4 projection 3D à 2D trou noir", "loi aire results.json")
d = charge(*p)
B = d["bins"]
V = np.array([b["V_mid"] for b in B]); A = np.array([b["A_mid"] for b in B])
var = np.array([b["K4_var"] for b in B]); moy = np.array([b["K4_mean"] for b in B])


def fit(x, y):
    m = (x > 0) & (y > 0)
    pente, _ = np.polyfit(np.log(x[m]), np.log(y[m]), 1)
    r2 = np.corrcoef(np.log(x[m]), np.log(y[m]))[0, 1] ** 2
    return float(pente), float(r2)


aV, r2V = fit(V, var); aA, r2A = fit(A, var); m1, _ = fit(V, moy)
regle = "loi d'aire" if aV < 0.78 else ("super-extensif" if aV > 1.2 else "extensif/thermique standard")
locales = np.diff(np.log(var)) / np.diff(np.log(V))
fen = {}
for a_, b_ in ((2, 5), (2, 6), (2, 7), (3, 6)):
    fen["classes %d à %d" % (a_ + 1, b_)] = fit(V[a_:b_], var[a_:b_])[0]
note("E2", "III.5.1, test loi d'aire (p. 259-260) et tableau VII.1.3 (p. 329) : exposant de σ²(n_K4)",
     "/".join(p), "σ² ∝ V^≈1.0 « extensif, thermique standard » ; σ² vs A ≈ 1",
     "σ² ∝ V^%.3f (R² %.3f) ; σ² ∝ A^%.3f (R² %.3f) ; fits enregistrés %.4f / %.4f ; règle du script : %s"
     % (aV, r2V, aA, r2A, d["fits"]["sigma2_vs_V"]["exp"], d["fits"]["sigma2_vs_A"]["exp"], regle),
     "INCOHÉRENT",
     "Pentes locales : %s. Fenêtres non déclarées : %s. Le texte imprime lui-même le JSON (p. 322-323). "
     "Selon la fenêtre, l'exposant va de 0,77 à 3,23 (7 classes) : ni « extensif » ni l'absence de loi d'aire "
     "ne sont établis par ces données ; σ² ∝ A^≈1 n'est retrouvé par aucune fenêtre."
     % (", ".join("%.2f" % x for x in locales), ", ".join("%s : %.3f" % kv for kv in fen.items())))
assert abs(aV - d["fits"]["sigma2_vs_V"]["exp"]) < 1e-9 and abs(m1 - 1.9507) < 1e-3

# ---------------------------------------------------------------- E3
p = ("06_campagnes_et_sauts", "BLOB SCALING V30 DU 23 AVRIL 2026", "EXPECTED_OUTPUT_v93_updated.json")
d = charge(*p)
borne = 0.30 * 0.2 * 8 * 0.414 / (2 * 0.125 * 81)
borne_obs = 0.30 * 0.2 * 8 * 0.414 / (2 * 0.35 * 81)
a = cherche(d, "delta0_analytic"); m = cherche(d, "delta0_measured")
note("E3", "Annexe A1.5, cascades 2 et 3 (p. 560) : borne Nβ|ΔD| et gap δ₀",
     "/".join(p),
     "(0,30 × 0,2 × 8 × 0,414)/(2 × 0,125 × 81) = 0,0982 ; D_min^obs = 0,35 → 0,035 ; δ₀ ≥ 0,350 − 0,098 = 0,252, statut [T]",
     "l'expression imprimée vaut %.5f (et %.5f avec D_min = 0,35) ; JSON : delta0_analytic = %s [%s], delta0_measured = %s [%s]"
     % (borne, borne_obs, a["value"], a.get("label"), m["value"], m.get("label")),
     "INCOHÉRENT",
     "Les deux évaluations imprimées valent dix fois l'expression imprimée. Selon la lecture : δ₀ ≥ %.3f "
     "(expression imprimée), 0,252 (texte), %s (JSON, T*). Le signe δ₀ > 0 tient dans les trois cas ; "
     "la valeur et l'étiquette [T] ne concordent pas avec le JSON." % (0.350 - borne, a["value"]))

# ---------------------------------------------------------------- E4
p = ("06_campagnes_et_sauts", "Audit 25 mai — paliers et gravite", "blob_toile_results.json")
d = charge(*p)
tab = {}
for mode in ("multi", "single", "multi_noviab", "poisson"):
    for N in (1000, 2500, 5000, 10000, 15000, 20000):
        cles = [k for k in d if k.startswith("%s_N%d_s" % (mode, N))]
        P = np.mean([d[k]["pk"][1] for k in cles], axis=0)
        tab[(mode, N)] = dict(n=len(cles), pk=float(P.max() / np.median(P)),
                              void=float(np.mean([d[k]["void"] for k in cles])))
apparie = {}
for N in (1000, 2500, 5000, 10000, 15000, 20000):
    gr = sorted(k.rsplit("_s", 1)[1] for k in d if k.startswith("multi_N%d_s" % N))
    dv = [d["multi_N%d_s%s" % (N, g)]["void"] - d["multi_noviab_N%d_s%s" % (N, g)]["void"] for g in gr]
    apparie[N] = (float(np.mean(dv)), sum(x > 0 for x in dv), len(dv))
lig = []
for N in (5000, 10000, 20000):
    lig.append("N=%d : P_max/méd. Blob %.0f, sans viabilité %.0f, site unique %.0f, Poisson %.1f ; "
               "vides Blob %.3f, sans viabilité %.3f" % (
                   N, tab[("multi", N)]["pk"], tab[("multi_noviab", N)]["pk"], tab[("single", N)]["pk"],
                   tab[("poisson", N)]["pk"], tab[("multi", N)]["void"], tab[("multi_noviab", N)]["void"]))
note("E4", "XXV.2 (p. 644-645) : « structuration … propre à la viabilité », « vides … propres à la viabilité »",
     "/".join(p), "P_max/médiane ≈ 1900 (Blob) vs 1,2 (Poisson) ; vides 0,86/0,81/0,76 ; « propre à la viabilité »",
     " | ".join(lig), "INCOHÉRENT (portée de la conclusion)",
     "Les valeurs Blob et Poisson du texte concordent ; le témoin « mobilité sans viabilité », annoncé au protocole "
     "et présent dans le fichier, n'est pas rapporté. Excès de vides du Blob sur le témoin, graines appariées : %s. "
     "Graines : %s (texte : « jusqu'à 6 »)."
     % (", ".join("N=%d : %+.3f (%d/%d positifs)" % (N, *apparie[N]) for N in apparie),
        ", ".join("N=%d : %d" % (N, tab[("multi", N)]["n"]) for N in (1000, 2500, 5000, 10000, 15000, 20000))))

# ---------------------------------------------------------------- E5
p = ("03_scripts", "simulations", "blob_total_V286_results.json")
d = charge(*p)
ec = [abs(v["C"] - a_["C"]) for v, a_ in zip(d["C"]["viable"], d["C"]["alea"])]
note("m4", "Tome V292, volet C (PARTIE CCI, p. 5 du tome) : « Écart final : 0,004 »",
     "/".join(p), "0,004",
     "|⟨C⟩ viable − ⟨C⟩ aléa| par niveau : %s ; niveau final %.4f" % (", ".join("%.4f" % x for x in ec), ec[-1]),
     "INCOHÉRENT (intitulé)",
     "La table imprimée elle-même donne 0,331 et 0,345 au niveau 3, soit 0,014. 0,004 correspond à "
     "l'écart des moyennes des niveaux 1 à 3 (%.4f). Conclusion (convergence vers ≈ 0,34) inchangée."
     % abs(np.mean([v["C"] for v in d["C"]["viable"][1:]]) - np.mean([v["C"] for v in d["C"]["alea"][1:]])))

# ---------------------------------------------------------------- E6
rho = {}
for N, f in ((1000, "palier_1000-2.json"), (2000, "palier_2000-2.json"), (4000, "palier_4000.json"),
             (8000, "palier_8000.json")):
    e = charge("04_donnees", "DERNIER JSON", f)
    rho[N] = (e["palier"]["rho_star_mean"], [s["rho_star"] for s in e["per_seed"]])
e = charge("03_scripts", "SCRIPTS DIVERS BLOB", "Grand N — paliers 32000", "palier_32000.json")
rho[32000] = (e["palier"]["rho_star_mean"], [s["rho_star"] for s in e["per_seed"]])
note("E5", "CXL.7.2 (p. 1203) : « ρ* ≈ 4,8–5,0 stable », confirmations à N = 8000",
     "04_donnees/DERNIER JSON/palier_*.json ; 03_scripts/…/palier_32000.json", "ρ* ≈ 4,8–5,0 stable",
     "ρ* moyen : %s ; N=8000, graines : %s" % (", ".join("N=%d : %.3f" % (N, rho[N][0]) for N in sorted(rho)),
                                              ", ".join("%.3f" % x for x in rho[8000][1])),
     "INCOHÉRENT (mineur)",
     "À N = 8000 aucune graine n'atteint 4,8. Le master recale lui-même la constante sur ρ = 4,42 (p. 1213-1214, "
     "« le 5,8 … utilisait ρ = 4,9 : périmé »).")

# ---------------------------------------------------------------- E7
p = ("06_campagnes_et_sauts", "Test O2v4 projection 3D à 2D trou noir", "local collapse results.json")
d = charge(*p)["stats"]
de = d["dense"]
z_sem = (2 - de["dH_mean"]) / (de["dH_std"] / math.sqrt(de["n"]))
t = lambda a, b: (a["dH_mean"] - b["dH_mean"]) / math.sqrt(a["dH_std"] ** 2 / a["n"] + b["dH_std"] ** 2 / b["n"])
note("E6", "III.3.6 (p. 255) : « 1.87 ± 0.24, compatible avec 2 (barre d'erreur 1σ) » et « l'effet dépasse 40σ »",
     "/".join(p), "1.87 ± 0.24 compatible avec 2 à 1σ ; effet > 40σ",
     "dense : %.4f ± %.4f (écart-type), n = %d ; écart à 2 = %.1f erreurs-types ; t Welch dense−bulk %.2f, dense−void %.2f"
     % (de["dH_mean"], de["dH_std"], de["n"], z_sem, t(de, d["bulk"]), t(de, d["void"])),
     "INCOHÉRENT (convention)",
     "Les t de Welch (−25,33 et −44,37 au texte) utilisent l'erreur-type ; la compatibilité avec 2 utilise l'écart-type. "
     "À la même métrique, la classe dense est à ≈ 12 erreurs-types de 2. Les 515 sommets viennent de 5 graines : "
     "les erreurs-types par sommet sont des pseudo-répliques, et ni « compatible à 1σ » ni « 40σ » ne sont établis à l'échelle des graines.")

# ---------------------------------------------------------------- mineurs
p = ("06_campagnes_et_sauts", "BLOB SCALING V30 DU 23 AVRIL 2026", "EXPECTED_OUTPUT_v93_updated.json")
tr = cherche(charge(*p), "tri_ratio_N3000")
snr = [12820 / math.sqrt((690 ** 2 + 98 ** 2) / n) for n in (4, 5)]
note("m1", "M-3.2 (p. 136) : enrichissement en triangles à N = 3000", "/".join(p),
     "18 513 ± 690 / 5 693 ± 98, +225 %, 36.8σ ; « facteur 2.25× à 3.25× »",
     "tri_ratio_N3000 = %s, SNR = %s ; rapport %.3f ; SNR recalculé %.1f (n = 4) ou %.1f (n = 5)"
     % (tr["value"], tr.get("SNR"), 18513 / 5693, snr[0], snr[1]),
     "INCOHÉRENT (mineur)", "Rapports du tableau : 2,51 à 3,25 ; le « 2.25× » est le gain (+225 %) lu comme un rapport. 36,8σ ⇔ n = 4, "
     "SNR = 41 ⇔ n = 5 ; aucun n documenté." )
p3 = ("06_campagnes_et_sauts", "SAUT 9 et 10 et 11", "Manifestes v99 et addendum v102", "EXPECTED_OUTPUT_v93_updated 2.json")
t10 = cherche(charge(*p3), "tri_ratio_N10000")
note("m2", "M-3.2 (p. 136) : ligne N = 10000 (49 204 ± 5 050 / 17 510 ± 249, +181 %, 16.6σ, [M])", "/".join(p3),
     "ligne mesurée [M]", "tri_ratio_N10000 = %s (%s)" % (t10["value"], t10.get("note")), "INCOHÉRENT (mineur)",
     "Le manifeste tient cette mesure pour non faite ; aucun JSON du corpus ne donne 49 204.")
p = ("06_campagnes_et_sauts", "Test O2v4 projection 3D à 2D trou noir", "scout results.json")
s = charge(*p)
note("m3", "Test B, cascade triangle → tétraèdre (p. 261)", "/".join(p),
     "« 5 seeds × ~20 samples MCMC »",
     "params.seeds = %s, test_B.n_points = %s" % (s["params"]["seeds"], cherche(s, "n_points")),
     "INCOHÉRENT (mineur)", "Protocole décrit : ≈ 100 points ; fichier : 56 points (4 graines × 14). Le script imprimé (p. 305) a SEEDS = [0,1,2,3]. b et R² concordent.")

with open(os.path.join(os.path.dirname(__file__), "r5_audit_sortie.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
for r in res:
    print("[%s] %s\n   JSON : %s\n   cité : %s\n   réel : %s\n   %s — %s\n" % (
        r["code"], r["objet"], r["json"], r["valeur_citee"], r["valeur_json"], r["verdict"], r["detail"]))
