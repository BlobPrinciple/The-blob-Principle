#!/usr/bin/env python3
"""C-148c ter -- Contre-verification du contre-audit de ChatGPT ; second ordre des lois en lambda.  (Claude, 13 novembre 2026)

Attendus : c148c_ter_prediction.txt (ecrit avant execution).
Donnees officielles DESI DR2 : depot public CobayaSampler/bao_data (commit bb0c1c9), non redistribuees ici.
Usage : python3 -I c148c_ter.py /chemin/vers/bao_data/desi_bao_dr2      (ecrit c148c_ter.json)
"""
import hashlib
import json
import math
import pathlib
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

ICI = pathlib.Path(__file__).resolve().parent
src = (ICI / 'c148c.py').read_text().split("# ------------------------------------------------------------------ T1 : temoin publie")[0]
exec(src)                      # donnees arrondies, integrale(), E_frein(), profil_n(), intervalle() de c148c.py
b = {}

# ------------------------------------------------------------------ E1 : donnees officielles
rep = pathlib.Path(sys.argv[1])
fm, fc = rep / 'desi_gaussian_bao_ALL_GCcomb_mean.txt', rep / 'desi_gaussian_bao_ALL_GCcomb_cov.txt'
lignes = [l.split() for l in fm.read_text().splitlines() if l.strip() and not l.startswith('#')]
zo = np.array([float(l[0]) for l in lignes])
do = np.array([float(l[1]) for l in lignes])
qo = [l[2] for l in lignes]
Wo = np.linalg.inv(np.loadtxt(fc))


def forme_off(E):
    g = []
    for z, q in zip(zo, qo):
        if q == 'DV_over_rs':
            g.append((z * integrale(E, z) ** 2 / float(E(z))) ** (1 / 3))
        elif q == 'DM_over_rs':
            g.append(integrale(E, z))
        elif q == 'DH_over_rs':
            g.append(1 / float(E(z)))
        else:
            raise ValueError(q)
    return np.array(g)


def chi2_off(E):
    g = forme_off(E)
    al = float(g @ Wo @ do) / float(g @ Wo @ g)
    r = do - al * g
    return float(r @ Wo @ r)


r2 = minimize_scalar(lambda w: chi2_off(E_frein(w, 2)), bounds=(0.05, 0.8), method='bounded', options=dict(xatol=1e-12))
ns = np.round(np.arange(1.90, 2.2001, 0.005), 4)
po = profil_n(chi2_off, ns)
i = po[:, 2].argmin()
fin = minimize_scalar(lambda n: minimize_scalar(lambda w: chi2_off(E_frein(w, n)), bounds=(1e-6, 1.0), method='bounded',
                                                options=dict(xatol=1e-12)).fun, bounds=(po[i, 0] - 0.01, po[i, 0] + 0.01), method='bounded',
                      options=dict(xatol=1e-8))
po2 = po.copy()
po2[:, 2] = po2[:, 2] - fin.fun + po2[:, 2].min()          # profil rapporte au minimum continu
dx = po[:, 2] - fin.fun


def croise(seuil):
    out = []
    for j in range(len(ns) - 1):
        if (dx[j] - seuil) * (dx[j + 1] - seuil) < 0:
            out.append(float(ns[j] + (seuil - dx[j]) * (ns[j + 1] - ns[j]) / (dx[j + 1] - dx[j])))
    return out


b['E1_donnees_officielles'] = dict(
    fichiers=dict(moyenne=hashlib.sha256(fm.read_bytes()).hexdigest(), covariance=hashlib.sha256(fc.read_bytes()).hexdigest()),
    n2=dict(Omega_m=r2.x, chi2=r2.fun), n_libre=dict(n=fin.x, chi2=fin.fun, un_ecart_type=croise(1.0)),
    chatgpt=dict(Omega_m=0.29746182, chi2_n2=10.271041, n=2.04905749, chi2=9.831973, un_ecart_type=[1.975119, 2.123605]),
    ecart_max_donnees_arrondies=float(np.abs(np.sort(do) - np.sort(d)).max()))

# ------------------------------------------------------------------ E2 : Z a^(6B) constant
# unites : K = 12 pi G = 1 ; c_inf^2 = 0,7 c0^2 ; x = ln a ; d/dt = (c/3) d/dx
e2 = {}
for B in (0.1, 1 / 3, 0.45):
    for z0 in (0.2, -0.2):
        c0, cinf2 = 1.0, 0.7
        rho0 = (c0 * c0 - cinf2 - z0) / 2

        def droite(x, y, B=B):
            c, lr = y
            rho = math.exp(lr)
            return [3 * (B * (cinf2 - c * c) - (1 - 2 * B) * rho) / c, -3.0]
        sol = solve_ivp(droite, (0, math.log(10)), [c0, math.log(rho0)], t_eval=np.linspace(0, math.log(10), 9), rtol=1e-12, atol=1e-14, method='DOP853')
        Z = sol.y[0] ** 2 - cinf2 - 2 * np.exp(sol.y[1])
        inv = Z * np.exp(6 * B * sol.t)
        e2[f'B={B:.3f}, Z0={z0:+.1f}'] = float(np.abs(inv / z0 - 1).max())
b['E2_ecart_relatif_de_Z_a^6B'] = e2


# ------------------------------------------------------------------ E3, E4 : loi en lambda, ere de matiere, variables exactes (delta, g)
def droite_dg(x, y, B, lam):
    dl, g = y
    zz = 2 * g + g * g - dl
    return [-3 * g * (1 + dl), 1.5 * g + 3 * (-dl / 2 - B * zz + lam * zz * zz / (1 + g) ** 2)]


def nu_theorie(B, lam):
    p = 3 - 6 * B
    return (B * p * p / 3 + (p / 3) * (4.5 - 6 * B) - 3 * lam * (1 + 2 * p / 3) ** 2) / (p * (2.5 - 4 * B))


def nu_mesure(B, lam, eps=1e-6, a1=50.0, a2=100.0):
    p = 3 - 6 * B
    sol = solve_ivp(droite_dg, (0, math.log(a2)), [eps, -(p / 3) * eps], args=(B, lam), t_eval=[math.log(a1), math.log(a2)],
                    rtol=1e-13, atol=1e-22, method='DOP853')
    L1, L2 = sol.y[0, 0] / a1 ** p, sol.y[0, 1] / a2 ** p
    Cc = (L2 - L1) / (a2 ** p - a1 ** p)
    A = L1 - Cc * a1 ** p
    return Cc / (A * A)


e3 = {}
for lam in (-1.0, 0.0, 1.0):
    sol = solve_ivp(droite_dg, (0, math.log(100)), [1e-8, -(1 / 3) * 1e-8], args=(1 / 3, lam), t_eval=[math.log(10), math.log(100)],
                    rtol=1e-13, atol=1e-24, method='DOP853')
    e3[f'lambda={lam:+.0f}'] = dict(exposant_lineaire=float(math.log(sol.y[0, 1] / sol.y[0, 0]) / math.log(10)))
# fond : Z0 = 0 reste nul quel que soit lambda (delta = g = 0 est solution exacte) ; controle par integration a deux regions identiques
sol = solve_ivp(droite_dg, (0, math.log(100)), [0.0, 0.0], args=(1 / 3, 1.0), rtol=1e-13, atol=1e-24, method='DOP853')
e3['fond_inchange_ecart_max'] = float(np.abs(sol.y).max())
b['E3_premier_ordre'] = e3

e4 = {}
for B, lam in ((1 / 3, 0.0), (1 / 3, 0.02), (1 / 3, -0.05), (0.25, 0.0), (0.4, 0.01)):
    a2 = 100.0 if B > 0.3 else 30.0                        # delta ~ eps a^p : rester dans le regime faible
    th, me = nu_theorie(B, lam), nu_mesure(B, lam, a1=a2 / 2, a2=a2)
    e4[f'B={B:.4f}, lambda={lam:+.2f}'] = dict(theoreme=th, mesure=me, ecart_relatif=abs(me / th - 1))
b['E4_second_ordre'] = e4
b['E4_valeurs'] = dict(dix_sept_vingt_et_uniemes=17 / 21, pente_en_lambda_a_B_un_tiers=-50 / 7,
                       S3_relativite_generale=34 / 7, S3_pour_lambda_0_01=34 / 7 - 300 / 7 * 0.01,
                       nu_lambda_nul={f'{B:.3f}': nu_theorie(B, 0.0) for B in (0.0, 0.25, 0.3, 1 / 3, 0.375, 0.45)})

# ------------------------------------------------------------------ E5 : amplification si c_* = c_inf
OMo = r2.x
b['E5_amplification_c_sur_cinf_au_carre'] = {str(z): (OMo * (1 + z) ** 3 + 1 - OMo) / (1 - OMo) for z in (0, 0.5, 2.33, 1100)}

(ICI / 'c148c_ter.json').write_text(json.dumps(b, indent=1, ensure_ascii=False, default=float))
print(json.dumps(b, indent=1, ensure_ascii=False, default=float))
