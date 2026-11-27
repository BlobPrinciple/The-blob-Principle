#!/usr/bin/env python3
"""DEFI-M20, volet « κ ≥ 8 » — tableau des moyennes (4 graines) et verdict selon le critère déposé d'avance
(issue #56, commentaire 7213958737)."""
import json, pathlib
import numpy as np
ICI = pathlib.Path(__file__).resolve().parent
R = json.load(open(ICI / "m20_kappa.json"))
Q = ("V", "C1", "C2", "C3_aretes", "G", "A10", "Z", "ntri_par_N", "seuil_global", "deg_max")


def moy(mod, k, N, q):
    x = np.array([r[q] for r in R if r["modele"] == mod and r["kappa"] == k and r["N"] == N], float)
    return x.mean(), x.std(ddof=1) / np.sqrt(len(x)), len(x)


kap = sorted({r["kappa"] for r in R}); tailles = sorted({r["N"] for r in R})
print("κ      N     | BLOB  V      C1     C2     C3e    G      A10    Z      ntri/N (seuil) dmax | RGG  V      G      A10    Z")
verdict = {}
for k in kap:
    ari_g, ari_p, obs_s, obs_l, complet = True, None, True, None, True
    for N in tailles:
        b = {q: moy("blob", k, N, q) for q in Q}; g = {q: moy("rgg", k, N, q) for q in Q}
        if b["V"][2] < 4:
            complet = False; continue
        print(f"{k:<5}  {N:<5} | {b['V'][0]:.3f}  {b['C1'][0]:.3f}  {b['C2'][0]:.3f}  {b['C3_aretes'][0]:.3f}  "
              f"{b['G'][0]:.3f}  {b['A10'][0]:.3f}  {b['Z'][0]:.3f}  {b['ntri_par_N'][0]:.2f} ({b['seuil_global'][0]:.2f}) "
              f"{b['deg_max'][0]:.0f} | {g['V'][0]:.3f}  {g['G'][0]:.3f}  {g['A10'][0]:.3f}  {g['Z'][0]:.3f}")
        dG = b["G"][0] - g["G"][0]; dA = b["A10"][0] - g["A10"][0]
        ari_g &= (dG >= 0.10 and dA >= 0.10); obs_s &= b["V"][0] >= 0.50
        if N == max(tailles):
            ari_p = dG < 0.05 and dA < 0.05; obs_l = b["V"][0] < 0.10
    if not complet:
        verdict[k] = "incomplet"; continue
    a = "GARDÉE" if ari_g else ("PERDUE" if ari_p else "NON TRANCHÉ")
    o = "SUBSISTE" if obs_s else ("LEVÉ" if obs_l else "NON TRANCHÉ")
    verdict[k] = (a, o)
print()
for k, v in verdict.items():
    print(f"κ = {k} : aristocratie {v[0] if v != 'incomplet' else v} ; obstacle local {v[1] if v != 'incomplet' else ''}")
