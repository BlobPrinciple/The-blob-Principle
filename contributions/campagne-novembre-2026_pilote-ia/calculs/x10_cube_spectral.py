#!/usr/bin/env python3
"""X-10 [EXPLORATOIRE, non aveugle] -- controle d'un temoin de PHYS-3 (ChatGPT) : dimension spectrale d'un cube n^3 a bords libres, laplacien de graphe non pondere,
d_s(tau) = -2 d ln P / d ln tau, P(tau) = moyenne de la probabilite de retour = (1/n^3) Somme exp(-lambda tau). Calcul exact par le spectre du chemin (Claude, 16 novembre 2026)."""
import json
import numpy as np
out = {}
for n in (12, 24, 48, 96):
    lam = 2 - 2 * np.cos(np.pi * np.arange(n) / n); r = {}
    for tau in (4, 8, 16):
        p = np.exp(-lam * tau).sum() / n; dp = -(lam * np.exp(-lam * tau)).sum() / n; r[tau] = float(3 * (-2 * tau * dp / p))   # cube = produit de trois chemins : d_s = 3 x celle du chemin
    out[n] = r; print(n, r)
json.dump(out, open('x10_cube_spectral.json', 'w'), indent=1)
