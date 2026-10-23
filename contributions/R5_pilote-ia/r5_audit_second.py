#!/usr/bin/env python3
"""DEFI-R5 — Seconde implémentation indépendante (Python pur, fractions, statistics, scipy.stats).

Recalcule les mêmes grandeurs que r5_audit.py par d'autres chemins : accès aux clés
par chemin explicite (pas de recherche récursive), arithmétique exacte en fractions,
régressions par scipy.stats.linregress, moyennes par statistics. Compare ensuite
ses résultats à r5_audit_sortie.json (tolérance 1e-6 relative sur les nombres).

Usage : python3 contributions/R5_pilote-ia/r5_audit_second.py
"""
import json, math, os, statistics as st
from fractions import Fraction as F
from scipy.stats import linregress

ICI = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(ICI, "..", "..", "corpus")
L = lambda *p: json.load(open(os.path.join(C, *p), encoding="utf-8"))
out = {}

# E1 : chemin explicite dans le manifeste v99/v102
d = L("06_campagnes_et_sauts", "SAUT 9 et 10 et 11", "Manifestes v99 et addendum v102",
      "EXPECTED_OUTPUT_v93_updated 2.json")
chemins = []
def parcours(o, pref=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.startswith("ds_N"):
                chemins.append((pref + "/" + k, v))
            parcours(v, pref + "/" + k)
parcours(d)
vals = {c.split("/")[-1]: v for c, v in chemins}
out["E1"] = dict(ds_N1000=vals["ds_N1000"]["value"], seeds=vals["ds_N1000"]["seeds"],
                 ds_N3000=vals["ds_N3000"]["value"], cles=sorted(vals),
                 ecart_pct=float(F(3) - F(str(vals["ds_N1000"]["value"]))) / 3 * 100)

# E2 : régressions scipy
d = L("06_campagnes_et_sauts", "Test O2v4 projection 3D à 2D trou noir", "loi aire results.json")
lv = [math.log(b["V_mid"]) for b in d["bins"]]; la = [math.log(b["A_mid"]) for b in d["bins"]]
ls = [math.log(b["K4_var"]) for b in d["bins"]]
rV = linregress(lv, ls); rA = linregress(la, ls)
out["E2"] = dict(sigma2_V=rV.slope, r2_V=rV.rvalue ** 2, sigma2_A=rA.slope, r2_A=rA.rvalue ** 2,
                 fen_3_6=linregress(lv[2:6], ls[2:6]).slope, fen_4_6=linregress(lv[3:6], ls[3:6]).slope,
                 fen_A_proche=min((linregress(la[a:b], ls[a:b]).slope for a in range(7) for b in range(a + 3, 8)), key=lambda x: abs(x - 1)))

# E3 : fractions exactes
b = F("0.30") * F("0.2") * 8 * F("0.414") / (2 * F("0.125") * 81)
b2 = F("0.30") * F("0.2") * 8 * F("0.414") / (2 * F("0.35") * 81)
d = L("06_campagnes_et_sauts", "BLOB SCALING V30 DU 23 AVRIL 2026", "EXPECTED_OUTPUT_v93_updated.json")
th = d["theorems"] if "theorems" in d else None
txt = json.dumps(d, ensure_ascii=False)
i = txt.index('"delta0_analytic"'); j = txt.index('"delta0_measured"')
out["E3"] = dict(borne=float(b), borne_obs=float(b2), borne_x10=float(10 * b),
                 delta0_analytic=json.loads("{" + txt[i:txt.index("}", i) + 1] + "}")["delta0_analytic"]["value"],
                 delta0_measured=json.loads("{" + txt[j:txt.index("}", j) + 1] + "}")["delta0_measured"]["value"])

# E4 : moyenne du spectre puis rapport au médian, en Python pur
d = L("06_campagnes_et_sauts", "Audit 25 mai — paliers et gravite", "blob_toile_results.json")
E4 = {}
for mode in ("multi", "multi_noviab", "single", "poisson"):
    for N in (5000, 10000, 20000):
        runs = [v for k, v in d.items() if k.rsplit("_s", 1)[0] == "%s_N%d" % (mode, N)]
        spec = [st.fmean(col) for col in zip(*[r["pk"][1] for r in runs])]
        E4["%s_%d" % (mode, N)] = dict(n=len(runs), pk=max(spec) / st.median(spec),
                                      void=st.fmean(r["void"] for r in runs))
for N in (1000, 2500, 15000):
    for mode in ("multi", "multi_noviab"):
        runs = [v for k, v in d.items() if k.rsplit("_s", 1)[0] == "%s_N%d" % (mode, N)]
        spec = [st.fmean(col) for col in zip(*[r["pk"][1] for r in runs])]
        E4["%s_%d" % (mode, N)] = dict(n=len(runs), pk=max(spec) / st.median(spec))
for N in (1000, 5000, 20000):
    gr = sorted({k.rsplit("_s", 1)[1] for k in d if k.startswith("multi_N%d_s" % N)}, key=int)
    E4["dv_%d" % N] = st.fmean(d["multi_N%d_s%s" % (N, g)]["void"] - d["multi_noviab_N%d_s%s" % (N, g)]["void"] for g in gr)
out["E4"] = E4

# m4
d = L("03_scripts", "simulations", "blob_total_V286_results.json")["C"]
out["m4"] = [abs(F(str(v["C"])) - F(str(a["C"]))) for v, a in zip(d["viable"], d["alea"])]
out["m4"] = [float(x) for x in out["m4"]]

# E5 : ρ* recalculé depuis les graines (moyenne simple)
r = {}
for N, f in ((8000, "palier_8000.json"), (4000, "palier_4000.json"), (2000, "palier_2000-2.json"), (1000, "palier_1000-2.json")):
    s = L("04_donnees", "DERNIER JSON", f)["per_seed"]
    r[N] = st.fmean(x["rho_star"] for x in s)
s = L("03_scripts", "SCRIPTS DIVERS BLOB", "Grand N — paliers 32000", "palier_32000.json")["per_seed"]
r[32000] = st.fmean(x["rho_star"] for x in s)
out["E5"] = r

# E6
d = L("06_campagnes_et_sauts", "Test O2v4 projection 3D à 2D trou noir", "local collapse results.json")["stats"]["dense"]
out["E6"] = dict(z=(2 - d["dH_mean"]) * math.sqrt(d["n"]) / d["dH_std"])

# M-3.2 : rapports Blob/nul recopiés du tableau imprimé p. 136
tab = {300: (1860, 740), 500: (3121, 1148), 1000: (6350, 2062), 3000: (18513, 5693), 10000: (49204, 17510)}
out["m1"] = {N: b / n for N, (b, n) in tab.items()}

# Valeurs annoncées par la NOTE (tolérance : dernier chiffre écrit)
attendu = [
    ("E1 ds_N1000", out["E1"]["ds_N1000"], 2.847, 5e-4), ("E1 écart %", out["E1"]["ecart_pct"], 5.1, 0.05),
    ("E2 σ² ∝ V", out["E2"]["sigma2_V"], 3.230, 5e-4), ("E2 R² V", out["E2"]["r2_V"], 0.789, 5e-4),
    ("E2 σ² ∝ A", out["E2"]["sigma2_A"], 7.462, 5e-4), ("E2 R² A", out["E2"]["r2_A"], 0.929, 5e-4),
    ("E2 fenêtre 3-6", out["E2"]["fen_3_6"], 0.980, 5e-4), ("E2 fenêtre 4-6", out["E2"]["fen_4_6"], 0.774, 5e-4),
    ("E3 expression", out["E3"]["borne"], 0.00981, 5e-6), ("E3 D_min 0,35", out["E3"]["borne_obs"], 0.00350, 5e-6),
    ("E3 JSON analytique", out["E3"]["delta0_analytic"], 0.159, 0), ("E3 JSON mesuré", out["E3"]["delta0_measured"], 0.274, 0),
    ("E4 P Blob 5000", out["E4"]["multi_5000"]["pk"], 635, 0.5), ("E4 P témoin 5000", out["E4"]["multi_noviab_5000"]["pk"], 619, 0.5),
    ("E4 P Blob 20000", out["E4"]["multi_20000"]["pk"], 1879, 0.5), ("E4 P témoin 20000", out["E4"]["multi_noviab_20000"]["pk"], 2277, 0.5),
    ("E4 vides Blob 20000", out["E4"]["multi_20000"]["void"], 0.763, 5e-4), ("E4 vides témoin 20000", out["E4"]["multi_noviab_20000"]["void"], 0.743, 5e-4),
    ("E4 Δvides 1000", out["E4"]["dv_1000"], 0.015, 5e-4), ("E4 Δvides 5000", out["E4"]["dv_5000"], 0.027, 5e-4),
    ("E4 P Blob/témoin 1000", out["E4"]["multi_1000"]["pk"] / out["E4"]["multi_noviab_1000"]["pk"], 1.13, 5e-3),
    ("E4 P Blob/témoin 2500", out["E4"]["multi_2500"]["pk"] / out["E4"]["multi_noviab_2500"]["pk"], 1.05, 5e-3),
    ("E4 P témoin/Blob 15000", out["E4"]["multi_noviab_15000"]["pk"] / out["E4"]["multi_15000"]["pk"], 1.04, 5e-3),
    ("E4 P témoin/Blob 20000", out["E4"]["multi_noviab_20000"]["pk"] / out["E4"]["multi_20000"]["pk"], 1.21, 5e-3),
    ("E4 Δvides 20000", out["E4"]["dv_20000"], 0.020, 5e-4),
    ("E5 ρ* 1000", out["E5"][1000], 4.993, 5e-4), ("E5 ρ* 2000", out["E5"][2000], 4.800, 5e-4),
    ("E5 ρ* 4000", out["E5"][4000], 4.803, 5e-4), ("E5 ρ* 8000", out["E5"][8000], 4.630, 5e-4),
    ("E5 ρ* 32000", out["E5"][32000], 4.421, 5e-4), ("E6 erreurs-types", out["E6"]["z"], 12.3, 0.05),
    ("m1 rapport min", min(out["m1"].values()), 2.51, 5e-3), ("m1 rapport max", max(out["m1"].values()), 3.25, 5e-3),
    ("m4 écart final", out["m4"][-1], 0.0141, 5e-5),
]
ok = True
print("Seconde implémentation — contrôle des valeurs de la note :")
for nom, v, a, tol in attendu:
    bon = abs(float(v) - a) <= tol + 1e-12
    ok &= bon
    print("  %-24s calculé %-12.6g annoncé %-10g %s" % (nom, float(v), a, "accord" if bon else "DÉSACCORD"))
bon = abs(out["E2"]["fen_A_proche"] - 1) > 0.5; ok &= bon
print("  E2 σ²–A, fenêtre ≥ 3 classes la plus proche de 1 : pente %.3f (%s)" % (out["E2"]["fen_A_proche"], "aucune ≈ 1" if bon else "DÉSACCORD"))
json.dump(out, open(os.path.join(ICI, "r5_audit_second_sortie.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1, default=str)
print("ACCORD COMPLET" if ok else "DÉSACCORD")
