#!/usr/bin/env python3
"""BP-L1c -- recoupement exact de BP-L1 / ACT-1 par equation maitresse (Claude, 15 novembre 2026). Predictions : bpl1c_prediction.txt.
Etat : (n1 aretes labiles, n2 aretes consolidees, q quanta). Phase 1 (t <= 20) : expm de la matrice de taux. Phase 2 : formules fermees."""
import itertools, json, math
import numpy as np
from scipy.linalg import expm
W = 1.5; NU01, NU12, NUD = 0.15, 0.002, 0.12; T1, T2 = 20.0, 60.0
def taux(beta, eps):
    E0, E1, E2 = 0.0, -0.25 - eps, -2.25 - eps
    return dict(k01=NU01 * math.exp(-beta * (E1 - E0) / 2), k10=NU01 * math.exp(beta * (E1 - E0) / 2), k12=NU12 * math.exp(-beta * (E2 - E1) / 2), k21=NU12 * math.exp(beta * (E2 - E1) / 2),
                d12=NUD * math.exp(-beta * ((E2 - E1) - W) / 2), d21=NUD * math.exp(beta * ((E2 - E1) - W) / 2))
def phase1(beta, eps, q0, lecture, nud=True, nu12=True):
    k = taux(beta, eps)
    if not nu12: k['k12'] = k['k21'] = 0.0
    drive = nud and q0 > 0
    Q = q0 + 6 + 1; etats = [(n1, n2, q) for n1 in range(7) for n2 in range(7 - n1) for q in range(Q)]; ix = {s: i for i, s in enumerate(etats)}
    G = np.zeros((len(etats), len(etats)))
    def add(s, t, r):
        if r > 0 and t in ix: G[ix[t], ix[s]] += r; G[ix[s], ix[s]] -= r
    for (n1, n2, q) in etats:
        n0 = 6 - n1 - n2; s = (n1, n2, q)
        add(s, (n1 + 1, n2, q), n0 * k['k01']); add(s, (n1 - 1, n2, q), n1 * k['k10'])
        add(s, (n1 - 1, n2 + 1, q), n1 * k['k12']); add(s, (n1 + 1, n2 - 1, q), n2 * k['k21'])
        if drive:
            if q > 0: add(s, (n1 - 1, n2 + 1, q - 1), n1 * k['d12'])
            if lecture == 'b' or q > 0: add(s, (n1 + 1, n2 - 1, q + 1), n2 * k['d21'])
    p0 = np.zeros(len(etats)); p0[ix[(0, 0, q0)]] = 1.0
    p = expm(G * T1) @ p0
    return etats, p, k
def mesures(beta, eps, q0, lecture, **kw):
    etats, p, k = phase1(beta, eps, q0, lecture, **kw)
    six2 = sum(pp for (n1, n2, q), pp in zip(etats, p) if n2 == 6)
    six_presentes = sum(pp for (n1, n2, q), pp in zip(etats, p) if n1 + n2 == 6)
    n2moy = sum(pp * n2 for (n1, n2, q), pp in zip(etats, p)); n1moy = sum(pp * n1 for (n1, n2, q), pp in zip(etats, p)); qmoy = sum(pp * q for (n1, n2, q), pp in zip(etats, p))
    strict = six2 * math.exp(-6 * k['k21'] * (T2 - T1))
    # maintien des six presentes sur [20, 60] : aucune arete ne passe en 0. Par arete, chaine {1, 2} avec fuite 1 -> 0.
    A = np.array([[-(k['k10'] + k['k12']), k['k21']], [k['k12'], -k['k21']]]); S = expm(A * (T2 - T1)); s1, s2 = S[:, 0].sum(), S[:, 1].sum()
    maintien = sum(pp * s1 ** n1 * s2 ** n2 for (n1, n2, q), pp in zip(etats, p) if n1 + n2 == 6)
    return dict(six_consolidees_t20=float(six2), six_presentes_t20=float(six_presentes), persistance_stricte=float(strict), maintien_six_presentes=float(maintien),
                consolidees_moy_t20=float(n2moy), labiles_moy_t20=float(n1moy), quanta_moy_t20=float(qmoy), norme=float(p.sum()), p_min=float(p.min()))
out = {'grille': {}, 'temoins': {}}
for beta in (1.0, 0.5):
    for eps in (0.0, 0.8):
        for q0 in (0, 3, 6, 12):
            out['grille'][f'beta={beta},eps={eps},q0={q0}'] = {lec: mesures(beta, eps, q0, lec) for lec in ('a', 'b')}
# temoin analytique : une arete seule, sans bain
for beta in (1.0, 0.5):
    for eps in (0.0, 0.8):
        k = taux(beta, eps); A = np.array([[-k['k01'], k['k10'], 0], [k['k01'], -(k['k10'] + k['k12']), k['k21']], [0, k['k12'], -k['k21']]]); p = expm(A * T1) @ np.array([1.0, 0, 0])
        out['temoins'][f'une_arete,beta={beta},eps={eps}'] = dict(p2=float(p[2]), p2_puissance_6=float(p[2] ** 6), maitresse=out['grille'][f'beta={beta},eps={eps},q0=0']['a']['six_consolidees_t20'],
                                                                 six_presentes_exact=float((p[1] + p[2]) ** 6), six_presentes_maitresse=out['grille'][f'beta={beta},eps={eps},q0=0']['a']['six_presentes_t20'])
out['temoins']['A_nud=0,q0=12,eps=0'] = mesures(1.0, 0.0, 12, 'a', nud=False); out['temoins']['A_nud=0,q0=12,eps=0.8'] = mesures(1.0, 0.8, 12, 'a', nud=False)
out['temoins']['B_sans_canal_12'] = mesures(1.0, 0.8, 12, 'a', nud=False, nu12=False)
json.dump(out, open('bpl1c.json', 'w'), indent=1)
print('config | lecture a : six consolidees t20, persistance stricte (sur 4096) | lecture b')
for kk, v in out['grille'].items():
    a, b = v['a'], v['b']; print(kk, '| a %.5f %.5f (%.1f) | b %.5f %.5f (%.1f) | presentes %.4f maintien %.4f' % (a['six_consolidees_t20'], a['persistance_stricte'], 4096 * a['persistance_stricte'], b['six_consolidees_t20'], b['persistance_stricte'], 4096 * b['persistance_stricte'], a['six_presentes_t20'], a['maintien_six_presentes']))
for kk, v in out['temoins'].items(): print(kk, {x: (round(y, 12) if isinstance(y, float) else y) for x, y in v.items()})
