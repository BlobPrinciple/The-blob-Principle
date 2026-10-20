#!/usr/bin/env python3
"""DEFI-M11 — validation croisée du Monte-Carlo (numba) par le calcul exact.

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
Sur un secteur énumérable (N = 6, M = 10, k = 4 : M + k = 2(N + 1), comme dans
defi_m11_monte_carlo.py), on calcule exactement, pour chaque theta, l'espérance au
temps t des trois observables suivies par le Monte-Carlo (triangles du nouveau-né
T_v, triangles T, dispersion D), par propagation exacte de la loi (implémentation 1
de DEFI-M8). On fait tourner le Monte-Carlo de defi_m11_monte_carlo.py sur le même
secteur et on compare les courbes (écart en erreurs-types).

Usage : python3 defi_m11_validation.py  ->  defi_m11_validation.json
"""
import json
import pathlib

import numpy as np

import defi_m8_attachement_gibbs as m8
import defi_m11_monte_carlo as mc

ICI = pathlib.Path(__file__).resolve().parent
N, M, K = 6, 10, 4
GRILLE = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
R = 6000


def exact():
    anc, P2 = m8.paires_ordonnees(N)
    La = len(anc)
    MA = m8.masques_secteur(La, M)
    S, _ = m8.s_sim_masques(N, anc, MA)
    pi = m8.gibbs(N, S)
    M2 = m8.masques_secteur(len(P2), M + K)
    S2, ntri2 = m8.s_sim_masques(N + 1, P2, M2)
    pi2 = m8.gibbs(N + 1, S2)
    bits = ((M2[:, None] >> np.arange(len(P2))[None, :]) & 1).astype(np.int64)
    pos = {p: b for b, p in enumerate(P2)}
    deg = np.zeros((len(M2), N + 1))
    for b, (u, v) in enumerate(P2):
        deg[:, u] += bits[:, b]
        deg[:, v] += bits[:, b]
    D = deg.std(1) / deg.mean(1)
    tv_ = np.zeros(len(M2))  # triangles contenant le sommet N
    for a in range(N):
        for b in range(a + 1, N):
            tv_ += bits[:, pos[(a, N)]] & bits[:, pos[(b, N)]] & bits[:, pos[(a, b)]]
    obs = np.stack([tv_, ntri2.astype(float), D], 1)
    restr = M2 & ((1 << La) - 1)
    degv = np.array([bin(int(x)).count("1") for x in (M2 >> La)])
    bon = degv == K
    i = np.searchsorted(MA, restr[bon])
    KT = m8.noyau_echange(len(P2), M2, pi2).T.tocsr()
    res = {}
    for th in mc.THETAS:
        w = pi2[bon] ** th
        z = np.bincount(i, weights=w, minlength=len(MA))
        x = np.zeros(len(M2))
        x[bon] = pi[i] * w / z[i]
        courbe, t_prec = [], 0
        for t in GRILLE:
            for _ in range(t - t_prec):
                x = KT @ x
            t_prec = t
            courbe.append((x @ obs).tolist())
        res[th] = np.array(courbe)
    eq = pi2 @ obs
    sd = np.sqrt(pi2 @ obs ** 2 - eq ** 2)
    return res, eq, sd


def main():
    ex, eq, sd = exact()
    obs, eq_mc = mc.experience(N, M, K, R, GRILLE, rodage=4000, espacement=400, graine=7, n_eq=40000)
    out = {"secteur": [N, M, K], "R": R, "grille": GRILLE, "equilibre_exact": eq.tolist(),
           "equilibre_mc": eq_mc.mean(0).tolist(), "sd_exact": sd.tolist(), "par_theta": {}}
    pire = 0.0
    for th in mc.THETAS:
        moy = obs[th].mean(0)
        se = obs[th].std(0) / np.sqrt(R) + 1e-12
        z = (moy - ex[th]) / se
        pire = max(pire, float(np.abs(z).max()))
        out["par_theta"][str(th)] = {"exact": ex[th].tolist(), "mc": moy.tolist(), "z_max": float(np.abs(z).max())}
        print(th, "z max", round(float(np.abs(z).max()), 2), "T_v(0) exact", round(ex[th][0, 0], 3), "mc", round(moy[0, 0], 3))
    zeq = (eq_mc.mean(0) - eq) / (sd / np.sqrt(len(eq_mc)) * 3)  # chaîne corrélée : marge x3
    out["z_max_tous"] = pire
    out["equilibre_ecart_relatif"] = ((eq_mc.mean(0) - eq) / sd).tolist()
    print("pire z :", round(pire, 2), "; écart équilibre (en écarts-types) :", np.round((eq_mc.mean(0) - eq) / sd, 3))
    (ICI / "defi_m11_validation.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
