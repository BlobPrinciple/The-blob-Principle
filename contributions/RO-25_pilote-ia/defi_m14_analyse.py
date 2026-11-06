#!/usr/bin/env python3
"""DEFI-M14 — analyse : séjour dans l'aristocratie de n = 25 à 257, contre les prédictions préenregistrées.

Pilote IA du laboratoire (Claude, Anthropic), 6 novembre 2026.
Entrées : defi_m13_sorties.json (n = 25 à 193, moteur A, DEFI-M13), defi_m14_sejour_A.json
(n = 257, moteur A), defi_m14_sejour_B_{193,225,257,289}.json (moteur B, départ planté),
defi_m14_sejour_B_257_aleatoire.json (moteur B, départ aléatoire : contrôle, hors série),
defi_m14_prediction.json.
Chaque ajustement est fait deux fois : moindres carrés numpy (polyfit) et formule fermée
écrite à la main (sommes) ; l'exposant libre par scipy.optimize.curve_fit et par balayage
de grille sur γ avec moindres carrés linéaires à γ fixé.
Usage : python3 defi_m14_analyse.py  (écrit defi_m14_analyse.json)
"""
import collections
import json
import math
import pathlib

import numpy as np
from scipy.optimize import curve_fit

ICI = pathlib.Path(__file__).resolve().parent
out = {"cadre": __doc__.split("Usage")[0]}


def charge(nom):
    p = ICI / nom
    return json.loads(p.read_text())["chaines"] if p.exists() else []


m13 = charge("defi_m13_sorties.json")
A = charge("defi_m14_sejour_A.json")
B = (charge("defi_m14_sejour_B_193.json") + charge("defi_m14_sejour_B_225.json") + charge("defi_m14_sejour_B_257.json")
     + charge("defi_m14_sejour_B_289.json"))
A289 = charge("defi_m14_sejour_A_289.json")  # contrôle moteur A à n = 289 (une chaîne courte), hors série
ALEA = charge("defi_m14_sejour_B_257_aleatoire.json")
pred = json.loads((ICI / "defi_m14_prediction.json").read_text())

# 1. séjours par point et par moteur ; estimateur poolé = Σ temps / Σ sorties
par = collections.defaultdict(list)
for c in m13:
    par[("A", c["n"])].append(c)
for c in A + B:
    par[(c["moteur"], c["n"])].append(c)


def temps(c):
    return c["sejour_balayages"] * c["sorties"]


print("1. Séjour moyen (balayages) : chaînes, poolé, barre par blocs (moteur B)")
tab = {}
for (mo, n) in sorted(par, key=lambda k: (k[1], k[0])):
    cs = par[(mo, n)]
    pool = sum(temps(c) for c in cs) / sum(c["sorties"] for c in cs)
    ind = [c["sejour_balayages"] for c in cs]
    ligne = {"chaines": ind, "poole": pool, "sorties": sum(c["sorties"] for c in cs)}
    blocs = [b for c in cs for b in c.get("blocs_sorties_temps_ari", [])]
    if blocs:
        s = [t / k for k, t in blocs if k > 0]
        ligne["blocs_n"] = len(s)
        ligne["erreur_type_blocs"] = float(np.std(s, ddof=1) / math.sqrt(len(s)))
    if "t_demi" in cs[0]:
        td = [c["t_demi"] for c in cs if c.get("t_demi")]
        if td:
            ligne["t_demi"] = td
            ligne["sejour_sur_t_demi"] = pool / np.mean(td)
            ligne["aristocrates"] = [round(c["aristocrates_moyen"], 2) for c in cs]
            ligne["aristo_moities"] = [(round(c["aristocrates_moitie1"], 2), round(c["aristocrates_moitie2"], 2)) for c in cs]
    tab[f"{mo}{n}"] = ligne
    print(f"  {mo} n={n:3d} chaînes {[round(x) for x in ind]} poolé {pool:.4g} sorties {ligne['sorties']}"
          + (f" ± {ligne['erreur_type_blocs']:.3g} (blocs)" if "erreur_type_blocs" in ligne else "")
          + (f" t½ {[round(x) for x in ligne['t_demi']]} séjour/t½ {ligne['sejour_sur_t_demi']:.2f}" if "t_demi" in ligne else ""))
out["tableau"] = tab

# 2. série combinée : moteur A jusqu'à 193 (DEFI-M13) et à 257 ; moteur B à 225 (seul) ; 257 moyenne A, B
serie = {}
for n in (25, 33, 49, 65, 97, 129, 193):
    serie[n] = tab[f"A{n}"]["poole"]
if "B225" in tab:
    serie[225] = tab["B225"]["poole"]
v257 = [tab[k]["poole"] for k in ("A257", "B257") if k in tab]
serie[257] = float(np.exp(np.mean(np.log(v257))))
if "B289" in tab:
    serie[289] = tab["B289"]["poole"]
if ALEA:
    pa = sum(temps(c) for c in ALEA) / sum(c["sorties"] for c in ALEA)
    out["controle_depart_aleatoire_257"] = {"chaines": [c["sejour_balayages"] for c in ALEA], "poole": pa,
                                            "sorties": sum(c["sorties"] for c in ALEA),
                                            "aristocrates": [c["aristocrates_moyen"] for c in ALEA],
                                            "rapport_au_plante": pa / serie[257]}
    print("\n   contrôle départ aléatoire n = 257 : chaînes", [round(c["sejour_balayages"]) for c in ALEA], "poolé %.4g" % pa,
          "sorties", sum(c["sorties"] for c in ALEA), "aristocrates", [round(c["aristocrates_moyen"], 2) for c in ALEA],
          "rapport au planté %.2f" % (pa / serie[257]))
out["serie"] = serie
print("\n2. Série retenue (ln séjour) :", {n: round(math.log(s), 3) for n, s in serie.items()})

# 3. confrontation aux prédictions écrites avant la mesure
P = pred["predictions"]
s257 = serie[257]
print("\n3. n = 257 : mesuré %.3g (A %s, B %s)" % (s257, "%.3g" % tab["A257"]["poole"] if "A257" in tab else "-",
                                                    "%.3g" % tab["B257"]["poole"] if "B257" in tab else "-"))
conf = {}
for k in ("sejour_racine_n_depuis_65_n257", "sejour_racine_n_depuis_97_n257", "sejour_loi_M12_x1.63_n257",
          "sejour_lineaire_n_depuis_65_n257", "sejour_lineaire_n_depuis_97_n257"):
    conf[k] = {"prevu": P[k], "mesure_sur_prevu": s257 / P[k]}
    print(f"  {k:36s} prévu {P[k]:.3g}  mesuré/prévu {s257 / P[k]:.2f}")
lo, hi = P["sejour_calibration_lineaire_M13_n257"]
conf["calibration_lineaire_M13"] = {"prevu": [lo, hi], "mesure_sur_prevu": [s257 / lo, s257 / hi]}
print(f"  calibration linéaire DEFI-M13         prévu {lo:.3g}–{hi:.3g}  mesuré/prévu {s257 / hi:.2f}–{s257 / lo:.2f}")
c = pred["critere"]
verdict = ("survit" if c["survit_si_dans"][0] <= s257 <= c["survit_si_dans"][1]
           else "contredite" if s257 > c["contredite_si_au_dessus_de"] else "non tranché")
print("  critère fixé d'avance :", verdict)
out["confrontation_257"] = conf
out["verdict_preenregistre"] = verdict
if 225 in serie:
    for k in ("sejour_racine_n_depuis_65_n225", "sejour_lineaire_n_depuis_65_n225", "sejour_loi_M12_x1.63_n225"):
        print(f"  n = 225 {k:34s} prévu {P[k]:.3g} mesuré/prévu {serie[225] / P[k]:.2f}")
        conf[k] = {"prevu": P[k], "mesure_sur_prevu": serie[225] / P[k]}

# 4. ajustements sur n ≥ 65 : √n, n, exposant libre ; deux implémentations
ns = np.array(sorted(n for n in serie if n >= 65), dtype=float)
y = np.array([math.log(serie[int(n)]) for n in ns])


def droite_main(x, y):
    k = len(x)
    sx, sy, sxx, sxy = sum(x), sum(y), sum(a * a for a in x), sum(a * b for a, b in zip(x, y))
    b = (k * sxy - sx * sy) / (k * sxx - sx * sx)
    a = (sy - b * sx) / k
    return a, b, sum((yy - a - b * xx) ** 2 for xx, yy in zip(x, y))


print("\n4. Ajustements de ln séjour sur n =", [int(n) for n in ns])
aj = {}
for nom, f in (("racine", np.sqrt), ("lineaire", lambda z: z)):
    x = f(ns)
    p = np.polyfit(x, y, 1)
    r1 = float(((y - np.polyval(p, x)) ** 2).sum())
    a2, b2, r2 = droite_main(list(x), list(y))
    aj[nom] = {"pente": float(p[0]), "ordonnee": float(p[1]), "sce": r1, "pente_main": b2, "sce_main": r2}
    print(f"  {nom:9s} pente {p[0]:.4f} (main {b2:.4f})  SCE {r1:.4f} (main {r2:.4f})")


def modele(n, a, b, g):
    return a + b * n ** g


po, pc = curve_fit(modele, ns, y, p0=(-1.5, 1.0, 0.5), maxfev=20000)
grille = np.linspace(0.2, 1.5, 1301)
sce_g = []
for g in grille:
    a, b, r = droite_main(list(ns ** g), list(y))
    sce_g.append(r)
gbest = float(grille[int(np.argmin(sce_g))])
# intervalle « ΔSCE ≤ SCE_min · F » grossier : on rapporte la plage où SCE ≤ 2 × SCE_min
plage = grille[np.array(sce_g) <= 2 * min(sce_g)]
aj["exposant_libre"] = {"curve_fit": [float(v) for v in po], "erreur_gamma": float(math.sqrt(pc[2, 2])),
                        "grille_gamma": gbest, "plage_sce_2x": [float(plage.min()), float(plage.max())]}
print(f"  exposant libre : γ = {po[2]:.3f} ± {math.sqrt(pc[2, 2]):.3f} (curve_fit) ; grille {gbest:.3f} ;"
      f" SCE ≤ 2·min pour γ ∈ [{plage.min():.2f}, {plage.max():.2f}]")
# ajustements pondérés : erreur de ln séjour = 1/√(sorties) (Poisson, sorties corrélées non comptées),
# suggérés par le relecteur ; les fits non pondérés à 3 paramètres sur 4 points n'ont pas de précision utile
sorties_n = {n: (tab[f"A{n}"]["sorties"] if f"A{n}" in tab and n != 257 else
                 sum(tab[k]["sorties"] for k in (f"A{n}", f"B{n}") if k in tab)) for n in serie}
print("  pondéré (σ = 1/√sorties) :")
aj["pondere"] = {}
for lo, hi in ((65, 193), (65, 225), (65, 257), (65, 289), (129, 289)):
    sel = (ns >= lo) & (ns <= hi)
    sg = np.array([1 / math.sqrt(sorties_n[int(n)]) for n in ns[sel]])
    try:
        pw, cw = curve_fit(modele, ns[sel], y[sel], p0=(-1.5, 1.0, 0.5), sigma=sg, absolute_sigma=True, maxfev=50000)
        chi2 = float((((y[sel] - modele(ns[sel], *pw)) / sg) ** 2).sum())
        ddl = int(sel.sum()) - 3
        aj["pondere"][f"{lo}-{hi}"] = {"gamma": float(pw[2]), "erreur": float(math.sqrt(cw[2, 2])), "chi2": chi2, "ddl": ddl}
        print(f"    n = {lo} à {hi} : γ = {pw[2]:.3f} ± {math.sqrt(cw[2, 2]):.3f} ; χ² = {chi2:.1f} pour {ddl} ddl")
    except RuntimeError as e:
        print(f"    n = {lo} à {hi} : échec ({e})")
# même ajustement non pondéré sans les grandes tailles (stabilité ; précision indicative seulement)
for exclus in ((289,), (257, 289), (225, 257, 289)):
    sel = ~np.isin(ns, exclus)
    po2, pc2 = curve_fit(modele, ns[sel], y[sel], p0=(-1.5, 1.0, 0.5), maxfev=20000)
    aj[f"exposant_libre_sans_{'_'.join(map(str, exclus))}"] = [float(v) for v in po2]
    print(f"  exposant libre sans {exclus} : γ = {po2[2]:.3f} ± {math.sqrt(pc2[2, 2]):.3f}")
out["ajustements"] = aj

# 5. pentes locales Δ ln séjour / Δ √n
nn = sorted(serie)
pl = {}
print("\n5. Pentes locales Δ ln séjour / Δ √n")
for a, b in zip(nn, nn[1:]):
    if a >= 49:
        s = (math.log(serie[b]) - math.log(serie[a])) / (math.sqrt(b) - math.sqrt(a))
        pl[f"{a}-{b}"] = s
        print(f"  {a:3d} → {b:3d} : {s:.3f}")
out["pentes_locales"] = pl

# 4 bis. exposant libre (non pondéré) sur la fin de plage (n ≥ 129), deux implémentations
sel = ns >= 129
po3, pc3 = curve_fit(modele, ns[sel], y[sel], p0=(-1.5, 1.0, 0.5), maxfev=20000)
sg = [droite_main(list(ns[sel] ** g), list(y[sel]))[2] for g in grille]
aj["exposant_libre_n129_289"] = {"curve_fit": [float(v) for v in po3], "erreur_gamma": float(math.sqrt(pc3[2, 2])),
                                 "grille_gamma": float(grille[int(np.argmin(sg))])}
print(f"\n4 bis. exposant libre non pondéré sur n ≥ 129 : γ = {po3[2]:.3f} ± {math.sqrt(pc3[2, 2]):.3f} (grille {grille[int(np.argmin(sg))]:.3f})")

if A289:
    c = A289[0]
    out["controle_moteur_A_289"] = {k: c[k] for k in ("sejour_balayages", "sorties", "aristocrates_moyen", "t_demi", "balayages")}
    print(f"\n   contrôle moteur A, n = 289 : séjour {c['sejour_balayages']:.4g} ({c['sorties']} sorties, "
          f"{c['balayages']:.3g} balayages), aristocrates {c['aristocrates_moyen']:.2f}, "
          f"t½ {c['t_demi']}, rapport au moteur B {c['sejour_balayages'] / tab['B289']['poole']:.2f}")

# 6. t½ à n = 257 (autocorrélation poolée) contre la loi de DEFI-M12 et la calibration de DEFI-M13
print("\n6. ln t½ par chaîne (autocorrélation poolée) contre la loi de DEFI-M12, ln t½ = 0,964·√n − 1,77")
lt = {}
for k in ("B193", "B225", "A257", "B257", "B289"):
    if k in tab and "t_demi" in tab[k]:
        n = int(k[1:])
        lt[k] = [math.log(x) for x in tab[k]["t_demi"]]
        print(f"  {k} : {[round(v, 3) for v in lt[k]]} ; loi M12 : {0.964 * math.sqrt(n) - 1.77:.2f}")
print("  calibration linéaire DEFI-M13 à n = 257 : 15,1–15,9")
out["ln_t_demi"] = lt
(ICI / "defi_m14_analyse.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
