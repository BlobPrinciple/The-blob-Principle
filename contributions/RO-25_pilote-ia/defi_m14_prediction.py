#!/usr/bin/env python3
"""DEFI-M14 — prédictions écrites AVANT toute mesure à n = 225 et 257 (préenregistrement).

Pilote IA du laboratoire (Claude, Anthropic), 6 novembre 2026.
Sources : séjours de defi_m13_sorties.json (n = 25 à 193), loi t½ de DEFI-M12
(ln t½ = 0,964·√n − 1,77), rapport séjour/t½ de DEFI-M13 § 3.2 (1,48 à 1,86 ; 1,63 à n = 193),
calibrations linéaires ln t½ ↔ B de DEFI-M13 § 3.4 (ln t½(257) = 15,1 à 15,9).
Critère de décision fixé ici : la loi en √n « survit » à n = 257 si le séjour mesuré
(deux moteurs) tombe dans [0,6 ; 1,7]·10⁶ balayages ; elle est « contredite par une
croissance plus rapide » s'il dépasse 3·10⁶ ; entre les deux, non tranché.
Usage : python3 defi_m14_prediction.py  (écrit defi_m14_prediction.json)
"""
import collections
import json
import math
import pathlib

import numpy as np

ICI = pathlib.Path(__file__).resolve().parent
d = json.loads((ICI / "defi_m13_sorties.json").read_text())["chaines"]
s = collections.defaultdict(list)
for c in d:
    s[c["n"]].append(c["sejour_balayages"])
ns = np.array(sorted(s))
y = np.array([math.log(np.mean(s[n])) for n in ns])
out = {"cadre": __doc__.split("Usage")[0], "sejours_m13": {int(n): float(np.mean(s[n])) for n in ns}, "predictions": {}}
for lo in (65, 97):
    sel = ns >= lo
    p = np.polyfit(np.sqrt(ns[sel]), y[sel], 1)
    q = np.polyfit(ns[sel], y[sel], 1)
    for n in (225, 257):
        out["predictions"][f"sejour_racine_n_depuis_{lo}_n{n}"] = float(math.exp(np.polyval(p, math.sqrt(n))))
        out["predictions"][f"sejour_lineaire_n_depuis_{lo}_n{n}"] = float(math.exp(np.polyval(q, n)))
for n in (225, 257):
    td = math.exp(0.964 * math.sqrt(n) - 1.77)
    out["predictions"][f"t_demi_loi_M12_n{n}"] = td
    out["predictions"][f"sejour_loi_M12_x1.63_n{n}"] = 1.63 * td
out["predictions"]["sejour_calibration_lineaire_M13_n257"] = [1.63 * math.exp(15.1), 1.63 * math.exp(15.9)]
out["critere"] = {"survit_si_dans": [6e5, 1.7e6], "contredite_si_au_dessus_de": 3e6}
(ICI / "defi_m14_prediction.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out["predictions"].items():
    print(k, v if isinstance(v, list) else "%.4g" % v)
