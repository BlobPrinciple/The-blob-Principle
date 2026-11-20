# -*- coding: utf-8 -*-
"""DEFI-R7 — tableau Markdown de la note, tiré de r7_analyse_sortie.json (aucun calcul nouveau)."""
import json, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(ICI, "r7_analyse_sortie.json")))["periodique"]
en = "--en" in sys.argv
f = (lambda x, n=2: f"{x:.{n}f}") if en else (lambda x, n=2: f"{x:.{n}f}".replace(".", ","))
print("| N (seeds) | sweeps | voids, viab | voids, mobile | L₁c/r_N | L₁/r_N | L_peak/r_N | S_max |" if en else
      "| N (graines) | balayages | vides viab | vides mobile | L₁c/r_N | L₁/r_N | L_pic/r_N | S_max |")
print("|---|---|---|---|---|---|---|---|")
for N, c in d.items():
    t = c["table"]
    for ts in ("20", "80", "320", "1280"):
        if ts not in t:
            continue
        a = t[ts]; b = t[ts + "_robustesse"]
        pm = lambda m: f"{f(m[0])} ± {f(m[1])}"
        print(f"| {N} ({c['graines']}) | {ts} | {f(a['vides_viab'][0],3)} ± {f(a['vides_viab'][1],3)} | {f(a['vides_mobile'][0],3)} | "
              f"{pm(b['L1c_sur_rN'])} | {pm(a['L1_sur_rN'])} | {pm(b['Lpic_sur_rN'])} | {f(a['Smax'][0],1)} ± {f(a['Smax'][1],1)} |")
    p = t.get("pente_lnL1_lnt"); q = t.get("pente_lnL1c_lnt")
    if p:
        print(f"| {N} | {'slope' if en else 'pente'} d ln L/d ln t, t = 80–1280 | | | {f(q['valeur'][0],3)} ± {f(q['valeur'][1],3)} | {f(p['valeur'][0],3)} ± {f(p['valeur'][1],3)} | | |")
