#!/usr/bin/env python3
"""BP-L1e-c -- controle des formules fermees de BP-L1e (Claude, 15 novembre 2026). Predictions : bpl1e_c_prediction.txt."""
import json, math
import numpy as np
from scipy.linalg import expm
from bpl1d_c import chaine, generateur, taux, W
ref = json.load(open('bpl1d_c.json')); out = {}
for beta in (1.0, 0.5):
    for eps in (0.0, 0.8):
        k = taux(beta, eps); a = np.exp(-beta * np.array([0.0, k['E1'], k['E2']])); a /= a.sum()
        r = ref[f'P3P4,beta={beta},eps={eps},b']
        etats, ix, R, _ = chaine(beta, eps, 42, 'b'); G = generateur(etats, ix, R); p0 = np.zeros(len(etats)); p0[ix[(0, 0, 12)]] = 1; p20 = expm(G * 20.0) @ p0
        e0, i0, R0, _ = chaine(beta, eps, 0, 'b', drive=False); G0 = generateur(e0, i0, R0); m = np.zeros(len(e0))
        for s, v in zip(etats, p20): m[i0[(s[0], s[1], 0)]] += v
        six20 = m[i0[(0, 6, 0)]]
        out[f'beta={beta},eps={eps}'] = dict(Q1_formule=float(a[2] ** 6), Q1_ecart=float(abs(a[2] ** 6 - r['six_consolidees_stationnaire'])), Q2_formule=1 / math.expm1(beta * W), Q2_ecart=abs(1 / math.expm1(beta * W) - r['q_moyen']),
                                             Q3_temps_survie_stricte=1 / (6 * k['k21']), six_t20=float(six20), stricte_t60=float(six20 * math.exp(-6 * k['k21'] * 40)),
                                             Q4_six_apres_retrait={str(t): float((expm(G0 * (t - 20)) @ m)[i0[(0, 6, 0)]]) for t in (60, 300, 1000, 3000)}, equilibre=float(a[2] ** 6))
json.dump(out, open('bpl1e_c.json', 'w'), indent=1)
for kk, v in out.items(): print(kk, json.dumps(v))
