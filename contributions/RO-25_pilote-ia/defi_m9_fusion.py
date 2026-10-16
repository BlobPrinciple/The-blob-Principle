#!/usr/bin/env python3
"""DEFI-M9 — fusion des morceaux de calcul en defi_m9_resultats.json.

N = 250, 500, 1 000 : sortie imprimée par defi_m9_aristocratie.py (plan complet, journal
defi_m9_journal_partie1.txt ; le processus a été interrompu pendant N = 2 000).
N = 2 000 : graines 0 à 4 et 5 à 9 (defi_m9_N2000_a.json, defi_m9_N2000_b.json), réanalysées
ensemble à partir des données brutes. Figement : defi_m9_figement.json.
Les données brutes par naissance ne sont archivées que pour N = 2 000 (fichiers a et b) ;
pour N = 250 à 1 000, seuls les résumés imprimés ont été conservés.
"""
import json, pathlib, sys
ICI = pathlib.Path(__file__).resolve().parent
sys.argv = [sys.argv[0]]
import importlib.util
spec = importlib.util.spec_from_file_location("m9", ICI / "defi_m9_aristocratie.py")
m9 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m9)
res = {"protocole": "voir l'en-tête de defi_m9_aristocratie.py", "N": {}, "figement": {}}
for line in (ICI / "defi_m9_journal_partie1.txt").read_text().splitlines():
    if line[:1].isdigit():
        N, js = line.split(" ", 1); res["N"][N] = json.loads(js)
recs = []
for f in ("defi_m9_N2000_a.json", "defi_m9_N2000_b.json"):
    recs += json.loads((ICI / f).read_text())["brut"]["2000"]
a = m9.analyse(recs); a["graines"] = 10; a["naissances_par_graine"] = 20
a["secondes"] = "calcul en deux moitiés parallèles, environ 1 000 s chacune"
res["N"]["2000"] = a
fig = ICI / "defi_m9_figement.json"
if fig.exists():
    res["figement"] = json.loads(fig.read_text())["figement"]
(ICI / "defi_m9_resultats.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
print("N :", list(res["N"]), "| figement :", list(res["figement"]))
