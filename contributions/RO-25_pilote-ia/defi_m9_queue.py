#!/usr/bin/env python3
"""DEFI-M9 — analyse de la queue supérieure, toutes tailles réunies (seconde lecture des sorties).

Lit defi_m9_resultats.json et calcule, par décalage :
- la part de nouveau-nés et de témoins dans le décile supérieur (u > 0,9), toutes tailles
  réunies, avec un test exact de Fisher (nouveau-nés contre témoins) et un test binomial
  contre 0,1 ;
- l'écart moyen de masse triangulaire nouveau-né − population, moyenne pondérée par
  l'inverse des variances sur les quatre tailles.
"""
import json, math, pathlib
import numpy as np
from scipy import stats
ICI = pathlib.Path(__file__).resolve().parent
R = json.loads((ICI / "defi_m9_resultats.json").read_text())["N"]
out = []
lags = R["250"]["lags_balayages"]
for j, t in enumerate(lags):
    kn = kc = n = 0; w = wm = 0.0
    for N, a in R.items():
        L = a["par_lag"][j]; m = a["n_naissances"]
        kn += round(L["nouveau_ne"]["part_u_sup_0.9"] * m); kc += round(L["temoin"]["part_u_sup_0.9"] * m); n += m
        ww = 1 / L["ecart_tri_et"] ** 2; w += ww; wm += ww * L["ecart_tri_moy"]
    fisher = stats.fisher_exact([[kn, n - kn], [kc, n - kc]])
    out.append({"t": t, "n": n, "nouveau_ne_haut_decile": round(kn / n, 4), "temoin_haut_decile": round(kc / n, 4),
                "binom_p_nouveau_ne_vs_0.1": float("%.3g" % stats.binomtest(kn, n, 0.1).pvalue),
                "fisher_p_nouveau_ne_vs_temoin": float("%.3g" % fisher.pvalue),
                "ecart_tri_pondere": round(wm / w, 3), "ecart_tri_pondere_et": round(1 / math.sqrt(w), 3)})
    print(out[-1])
(ICI / "defi_m9_queue.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
