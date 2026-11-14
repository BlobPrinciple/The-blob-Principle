#!/usr/bin/env python3
"""C-148c bis -- complements APRES COUP (non preenregistres), declares comme tels.  (Claude, 13 novembre 2026)
(a) amplitude ajustee A(B) = sigma8 implicite aujourd'hui ; (b) incertitude sur r_d ; (c) identite de l'histoire d'ensemble pour toute loi B ;
(d) indice de croissance a B = 1/3 ; (e) densite d'equilibre frein = moteur.
Usage : python3 c148c_bis.py   (ecrit c148c_bis.json)
"""
import json, math, pathlib, sys
import numpy as np
from scipy.integrate import solve_ivp
ICI = pathlib.Path(__file__).resolve().parent
src = (ICI / 'c148c.py').read_text().split("(ICI / 'c148c.json').write_text")[0]
_stdout = sys.stdout
exec(src)                                   # reprend donnees, fonctions et resultats de c148c.py, sans reecrire son fichier
b = {}
# (a)
b['a_amplitude_sigma8_implicite'] = {f'{B:.3f}': dict(amplitude=chi2_croissance(B)[1], chi2=chi2_croissance(B)[0]) for B in (0.0, 0.25, 1 / 3, 0.375, 0.45, 0.49)}
# (b) r_d a n = 2 : erreurs sur H0 (chronometres) et alpha (DESI), a w fixe puis w libre (profil combine)
def rd_de(w):
    return C / (chi2_bao(E_frein(w, 2))[1] * chi2_cc(E_frein(w, 2))[1])
ws = np.linspace(0.25, 0.35, 201)
tot = np.array([chi2_bao(E_frein(w, 2))[0] + chi2_cc(E_frein(w, 2))[0] for w in ws])
F = E_frein(wt, 2)(zc)
sH0 = 1 / math.sqrt((wc * F * F).sum())
g = forme_bao(E_frein(wt, 2))
sal = 1 / math.sqrt(float(g @ W @ g))
H0b, alb = chi2_cc(E_frein(wt, 2))[1], chi2_bao(E_frein(wt, 2))[1]
ok = ws[tot - tot.min() <= 1]
b['b_r_d'] = dict(r_d=rd_de(wt), H0=H0b, sigma_H0_a_w_fixe=sH0, alpha=alb, sigma_alpha_a_w_fixe=sal,
                  sigma_r_d_a_w_fixe=rd_de(wt) * math.hypot(sH0 / H0b, sal / alb), r_d_aux_bornes_de_w=[rd_de(ok[0]), rd_de(ok[-1])],
                  reference_Planck_2018='147,09 +/- 0,26 Mpc (non reverifiee ce jour)')
# (c) meme histoire d'ensemble pour toute loi B : integration de la loi locale sur le fond, de z = 3 a z = 0
c0 = 1.0
cinf2 = (1 - OM) * c0 * c0
K_rho0 = OM * c0 * c0 / 2                    # platitude : c^2 = c_inf^2 + 2 K rho, K = 12 pi G
ident = {}
for B in (0.0, 0.2, 1 / 3, 0.45, 0.5):
    def droite(x, y, B=B):                   # x = ln(1+z) ; dN/N = -3 dx ; dc/dx = -3 (dc/dt)/c
        c = y[0]
        rho = K_rho0 * math.exp(3 * x)
        return [-3 * (B * (cinf2 - c * c) - (1 - 2 * B) * rho) / c]
    x3 = math.log(4.0)
    cz3 = math.sqrt(cinf2 + 2 * K_rho0 * 64)
    sol = solve_ivp(droite, (x3, 0.0), [cz3], rtol=1e-12, atol=1e-14, method='DOP853')
    ident[f'{B:.3f}'] = abs(sol.y[0, -1] / c0 - 1)
b['c_ecart_relatif_de_la_cadence_a_z0_pour_les_lois_B'] = ident
# (d)
f0 = croissance(1 / 3)[2]
b['d_indice_de_croissance_B_un_tiers'] = dict(f_aujourdhui=f0, gamma=math.log(f0) / math.log(OM), relativite_generale=0.55)
# (e)
Lam = cinf ** 2 / 3
rho_eq = Lam / (4 * math.pi * G)
b['e_equilibre'] = dict(Lambda_s2=Lam, densite_d_equilibre_kg_m3=rho_eq, atomes_d_hydrogene_par_m3=rho_eq / 1.6735e-27,
                        densite_critique_kg_m3=3 * H0s ** 2 / (8 * math.pi * G), densite_de_matiere_aujourdhui_kg_m3=OM * 3 * H0s ** 2 / (8 * math.pi * G))
(ICI / 'c148c_bis.json').write_text(json.dumps(b, indent=1, ensure_ascii=False, default=float))
print('\n=== COMPLEMENTS APRES COUP ===')
print(json.dumps(b, indent=1, ensure_ascii=False, default=float))
