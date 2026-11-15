#!/usr/bin/env python3
"""BP-L1d-c -- contre-calcul du bilan detaille du bain fini (Claude, 15 novembre 2026). Predictions : bpl1d_c_prediction.txt.
Moteur : celui de bpl1c.py (taux), matrice reconstruite ici avec troncature parametrable."""
import json, math, sys
import numpy as np
from scipy.linalg import expm, null_space
sys.argv = sys.argv[:1]
W = 1.5; NU01, NU12, NUD = 0.15, 0.002, 0.12
def taux(beta, eps):
    E0, E1, E2 = 0.0, -0.25 - eps, -2.25 - eps
    return dict(E1=E1, E2=E2, k01=NU01 * math.exp(-beta * (E1 - E0) / 2), k10=NU01 * math.exp(beta * (E1 - E0) / 2), k12=NU12 * math.exp(-beta * (E2 - E1) / 2), k21=NU12 * math.exp(beta * (E2 - E1) / 2),
                d12=NUD * math.exp(-beta * ((E2 - E1) - W) / 2), d21=NUD * math.exp(beta * ((E2 - E1) - W) / 2))
def chaine(beta, eps, qmax, lecture, drive=True):
    k = taux(beta, eps)
    etats = [(n1, n2, q) for n1 in range(7) for n2 in range(7 - n1) for q in range(qmax + 1)]; ix = {s: i for i, s in enumerate(etats)}
    R = {}
    def add(s, t, r):
        if r > 0 and t in ix: R[(s, t)] = R.get((s, t), 0.0) + r
    for (n1, n2, q) in etats:
        n0 = 6 - n1 - n2; s = (n1, n2, q)
        add(s, (n1 + 1, n2, q), n0 * k['k01']); add(s, (n1 - 1, n2, q), n1 * k['k10'])
        add(s, (n1 - 1, n2 + 1, q), n1 * k['k12']); add(s, (n1 + 1, n2 - 1, q), n2 * k['k21'])
        if drive:
            if q > 0: add(s, (n1 - 1, n2 + 1, q - 1), n1 * k['d12'])
            if lecture == 'b' or q > 0: add(s, (n1 + 1, n2 - 1, q + 1), n2 * k['d21'])
    return etats, ix, R, k
def mesure(k, beta, w):
    return lambda s: math.factorial(6) / (math.factorial(6 - s[0] - s[1]) * math.factorial(s[0]) * math.factorial(s[1])) * math.exp(-beta * (s[0] * k['E1'] + s[1] * k['E2'] + w * s[2]))
def generateur(etats, ix, R):
    G = np.zeros((len(etats), len(etats)))
    for (s, t), r in R.items(): G[ix[t], ix[s]] += r; G[ix[s], ix[s]] -= r
    return G
def thermique(k, beta):
    pi = {}
    for n1 in range(7):
        for n2 in range(7 - n1): pi[(n1, n2)] = mesure(k, beta, 0.0)((n1, n2, 0))
    z = sum(pi.values()); return {s: v / z for s, v in pi.items()}
out = {}
# P1, P2, temoin negatif
for beta in (1.0, 0.5):
    for eps in (0.0, 0.8):
        for lec in ('a', 'b'):
            etats, ix, R, k = chaine(beta, eps, 12, lec)
            sans = [(s, t) for (s, t) in R if (t, s) not in R]
            pi = mesure(k, beta, W); faux = mesure(k, beta, 0.0)
            err = max(abs(pi(s) * r - pi(t) * R[(t, s)]) / max(pi(s) * r, pi(t) * R[(t, s)]) for (s, t), r in R.items() if (t, s) in R)
            errf = max(abs(faux(s) * r - faux(t) * R[(t, s)]) / max(faux(s) * r, faux(t) * R[(t, s)]) for (s, t), r in R.items() if (t, s) in R)
            out[f'P1P2,beta={beta},eps={eps},{lec}'] = dict(etats=len(etats), transitions=len(R), sans_inverse=len(sans), tous_sans_inverse_vers_q0=all(t[2] == 0 for s, t in sans), err_bilan=err, err_mesure_fausse=errf)
# P3, P4 : lois stationnaires
for beta in (1.0, 0.5):
    for eps in (0.0, 0.8):
        for lec in ('a', 'b'):
            etats, ix, R, k = chaine(beta, eps, 60, lec); G = generateur(etats, ix, R)
            if lec == 'b':
                ns = null_space(G, rcond=1e-11); assert ns.shape[1] == 1, ns.shape; p = ns[:, 0] / ns[:, 0].sum()
            else:                                    # la classe q = 0 est fermee : limite t -> infini depuis (0, 0, 6)
                sub = [s for s in etats if s[2] <= 6]; sx = {s: i for i, s in enumerate(sub)}
                Gs = np.zeros((len(sub), len(sub)))
                for (s, t), r in R.items():
                    if s in sx and t in sx: Gs[sx[t], sx[s]] += r; Gs[sx[s], sx[s]] -= r
                p0 = np.zeros(len(sub)); p0[sx[(0, 0, 6)]] = 1; ps = expm(Gs * 2e5) @ p0
                p = np.zeros(len(etats))
                for s, v in zip(sub, ps): p[ix[s]] = v
            th = thermique(k, beta); marg = {}
            for s, v in zip(etats, p): marg[s[:2]] = marg.get(s[:2], 0.0) + v
            out[f'P3P4,beta={beta},eps={eps},{lec}'] = dict(ecart_max_marginale_thermique=max(abs(marg[s] - th[s]) for s in th), q_moyen=float(sum(v * s[2] for s, v in zip(etats, p))), masse_q0=float(sum(v for s, v in zip(etats, p) if s[2] == 0)),
                                                         six_consolidees_stationnaire=float(marg[(0, 6)]), six_consolidees_thermique=float(th[(0, 6)]))
# P5 : troncature de BP-L1c
def strict(beta, eps, q0, lec, qmax):
    etats, ix, R, k = chaine(beta, eps, qmax, lec, drive=q0 > 0); G = generateur(etats, ix, R)
    p0 = np.zeros(len(etats)); p0[ix[(0, 0, q0)]] = 1; p = expm(G * 20.0) @ p0
    return 4096 * sum(v for s, v in zip(etats, p) if s[1] == 6) * math.exp(-6 * k['k21'] * 40.0)
for beta in (1.0, 0.5):
    for eps in (0.0, 0.8):
        for q0 in (6, 12):
            a, b = strict(beta, eps, q0, 'b', q0 + 6), strict(beta, eps, q0, 'b', q0 + 30)
            out[f'P5,beta={beta},eps={eps},q0={q0}'] = dict(q0_plus_6=a, q0_plus_30=b, ecart=b - a)
# P7 : sans bain, six consolidees en fonction du temps
for beta in (1.0, 0.5):
    for eps in (0.0, 0.8):
        etats, ix, R, k = chaine(beta, eps, 0, 'b', drive=False); G = generateur(etats, ix, R); p0 = np.zeros(len(etats)); p0[ix[(0, 0, 0)]] = 1
        vp = np.sort(np.linalg.eigvals(G).real)[::-1]
        out[f'P7,beta={beta},eps={eps}'] = dict(six_consolidees={str(t): float((expm(G * t) @ p0)[ix[(0, 6, 0)]]) for t in (20, 100, 300, 1000, 3000, 10000)}, temps_lent=float(-1 / vp[1]),
                                                avec_bain_12_t20=float(strict(beta, eps, 12, 'b', 42) / 4096 / math.exp(-6 * k['k21'] * 40.0)))
# Complement apres coup (declare) : le bain reste actif sous (b), depart 12 quanta -- la surconsolidation retombe-t-elle ?
for beta in (1.0, 0.5):
    for eps in (0.0, 0.8):
        etats, ix, R, k = chaine(beta, eps, 42, 'b'); G = generateur(etats, ix, R); p0 = np.zeros(len(etats)); p0[ix[(0, 0, 12)]] = 1
        out[f'C1,beta={beta},eps={eps}'] = {str(t): float(sum(v for s, v in zip(etats, expm(G * t) @ p0) if s[1] == 6)) for t in (5, 10, 20, 50, 100, 300, 1000, 3000)}
# P6 : course d'exponentielles
rng = np.random.default_rng(20261115); V = np.array([0.2, 0.3, 0.5]); n = 30000
g = np.argmin(rng.exponential(size=(n, 3)) / V, axis=1); f = np.bincount(g, minlength=3) / n
out['P6'] = dict(frequences=f.tolist(), ecarts_types=((f - V) / np.sqrt(V * (1 - V) / n)).tolist())
json.dump(out, open('bpl1d_c.json', 'w'), indent=1)
for kk, v in out.items(): print(kk, json.dumps(v))
