#!/usr/bin/env python3
"""C-148c -- La cadence de la mitose face a l'expansion mesuree : niveau, frein, croissance.  (Claude, 13 novembre 2026)

Protocole et predictions : c148c_prediction.txt (ecrit avant tout calcul).
Donnees : DESI DR2 resultats II (arXiv:2503.14738, table IV) ; 31 chronometres cosmiques (A&A 683, A91, table 1) ;
          six valeurs de f sigma8 de la table finale SDSS (BAO + distorsions).
Usage : python3 c148c.py   (ecrit c148c.json)
"""
import json
import math
import pathlib
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

ICI = pathlib.Path(__file__).resolve().parent
C = 299792.458
bilan = {}

# ------------------------------------------------------------------ donnees
DV = (0.295, 7.942, 0.075)
COUPLES = [(0.510, 13.588, 0.167, 21.863, 0.425, -0.459), (0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
           (0.934, 21.576, 0.152, 17.641, 0.193, -0.416), (1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
           (1.484, 30.512, 0.760, 12.817, 0.516, -0.500), (2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
d = [DV[1]]
cov = np.zeros((13, 13))
cov[0, 0] = DV[2] ** 2
for i, (z, dm, sm, dh, sh, r) in enumerate(COUPLES):
    d += [dm, dh]
    a, b = 1 + 2 * i, 2 + 2 * i
    cov[a, a], cov[b, b], cov[a, b], cov[b, a] = sm ** 2, sh ** 2, r * sm * sh, r * sm * sh
d = np.array(d)
W = np.linalg.inv(cov)

CC = np.array([(0.09, 69, 12), (0.17, 83, 8), (0.27, 77, 14), (0.4, 95, 17), (0.9, 117, 23), (1.3, 168, 17), (1.43, 177, 18), (1.53, 140, 14),
               (1.75, 202, 40), (0.48, 97, 62), (0.88, 90, 40), (0.35, 82.1, 4.9), (0.179, 75, 4), (0.199, 75, 5), (0.352, 83, 14),
               (0.593, 104, 13), (0.68, 92, 8), (0.781, 105, 12), (0.875, 125, 17), (1.037, 154, 20), (0.07, 69, 19.6), (0.12, 68.6, 26.2),
               (0.2, 72.9, 29.6), (0.28, 88.8, 36.6), (1.363, 160, 33.6), (1.965, 186.5, 50.4), (0.3802, 83, 13.5), (0.4004, 77, 10.2),
               (0.4247, 87.1, 11.2), (0.4497, 92.8, 12.9), (0.4783, 80.9, 9)])
zc, Hc, sc = CC.T
wc = 1 / sc ** 2

FS8 = np.array([(0.15, 0.53, 0.16), (0.38, 0.497, 0.045), (0.51, 0.459, 0.038), (0.70, 0.473, 0.041), (0.85, 0.315, 0.095), (1.48, 0.462, 0.045)])

GLx, GLw = np.polynomial.legendre.leggauss(48)


def integrale(E, z):
    x = 0.5 * z * (GLx + 1)
    return 0.5 * z * float(np.sum(GLw / E(x)))


def forme_bao(E):
    """Vecteur des treize grandeurs pour alpha = c/(H0 r_d) = 1."""
    z0 = DV[0]
    g = [(z0 * integrale(E, z0) ** 2 / float(E(z0))) ** (1 / 3)]
    for (z, *_r) in COUPLES:
        g += [integrale(E, z), 1 / float(E(z))]
    return np.array(g)


def chi2_bao(E, alpha=None):
    g = forme_bao(E)
    if alpha is None:
        alpha = float(g @ W @ d) / float(g @ W @ g)
    r = d - alpha * g
    return float(r @ W @ r), alpha


def chi2_cc(E):
    F = E(zc)
    H0 = float((wc * Hc * F).sum() / (wc * F * F).sum())
    return float((wc * (Hc - H0 * F) ** 2).sum()), H0


def E_frein(w, n):
    return lambda z: (1 - w + w * (1 + np.asarray(z, dtype=float)) ** 3) ** (1 / n)


def E_niveau(m):
    return lambda z: (1 - m * (1 + np.asarray(z, dtype=float)) ** 3) / (1 - m)


def profil_n(chi2, ns):
    """Pour chaque n : minimum sur w dans [0, 1]."""
    out = []
    for n in ns:
        res = minimize_scalar(lambda w: chi2(E_frein(w, n)), bounds=(1e-6, 1.0), method='bounded', options=dict(xatol=1e-10))
        out.append((n, res.x, res.fun))
    return np.array(out)


def intervalle(p, seuil):
    """Bornes de n ou delta chi2 <= seuil (interpolation lineaire entre points de grille)."""
    dx = p[:, 2] - p[:, 2].min()
    ok = np.where(dx <= seuil)[0]
    lo, hi = ok[0], ok[-1]

    def borne(i, j):
        if j < 0 or j >= len(p):
            return float(p[i, 0])
        return float(p[i, 0] + (seuil - dx[i]) * (p[j, 0] - p[i, 0]) / (dx[j] - dx[i]))
    return borne(lo, lo - 1), borne(hi, hi + 1)


# ------------------------------------------------------------------ T1 : temoin publie, n = 2
res = minimize_scalar(lambda w: chi2_bao(E_frein(w, 2))[0], bounds=(0.05, 0.8), method='bounded', options=dict(xatol=1e-12))
w2 = res.x
c2, al2 = chi2_bao(E_frein(w2, 2))
f = lambda w, a: chi2_bao(E_frein(w, 2), a)[0]
hw, ha = 1e-4, 1e-3
Hss = np.array([[(f(w2 + hw, al2) - 2 * f(w2, al2) + f(w2 - hw, al2)) / hw ** 2,
                 (f(w2 + hw, al2 + ha) - f(w2 + hw, al2 - ha) - f(w2 - hw, al2 + ha) + f(w2 - hw, al2 - ha)) / (4 * hw * ha)],
                [0, (f(w2, al2 + ha) - 2 * f(w2, al2) + f(w2, al2 - ha)) / ha ** 2]])
Hss[1, 0] = Hss[0, 1]
cv = 2 * np.linalg.inv(Hss)
hrd = C / (100 * al2)
bilan['T1'] = dict(Omega_m=w2, sigma_Omega_m=math.sqrt(cv[0, 0]), h_rd=hrd, sigma_h_rd=hrd * math.sqrt(cv[1, 1]) / al2,
                   correlation=-cv[0, 1] / math.sqrt(cv[0, 0] * cv[1, 1]), chi2=c2, alpha=al2,
                   publie=dict(Omega_m=0.2975, sigma_Omega_m=0.0086, h_rd=101.54, sigma_h_rd=0.73, correlation=-0.92, chi2=10.2))

# ------------------------------------------------------------------ T2 : cadence constante sur DESI
bilan['T2_cadence_constante_DESI'] = chi2_bao(E_frein(0.0, 2))[0]

# ------------------------------------------------------------------ T3 : loi de frein integree contre la forme fermee
t3 = {}
for n in (1, 2, 3):
    w = 0.3
    sol = solve_ivp(lambda z, E: (3 * w / n) * E ** (1 - n) * (1 + z) ** 2, (0, 3), [1.0], rtol=1e-12, atol=1e-14, method='DOP853')
    t3[str(n)] = abs(sol.y[0, -1] / float(E_frein(w, n)(3.0)) - 1)
bilan['T3_ecart_relatif_a_z3'] = t3

# ------------------------------------------------------------------ P1 : loi de niveau
p1 = {}
for nom, chi2, zmax in (('DESI', lambda E: chi2_bao(E)[0], 2.33), ('chronometres', lambda E: chi2_cc(E)[0], 1.965)):
    mmax = 1 / (1 + zmax) ** 3
    ms = np.linspace(0, 0.9 * mmax, 46)
    cs = np.array([chi2(E_niveau(m)) for m in ms])
    p1[nom] = dict(m_max_admissible=mmax, meilleur_m=float(ms[cs.argmin()]), chi2_m0=float(cs[0]), chi2_m_un_dixieme_du_max=float(cs[5]),
                   chi2_m_moitie_du_max=float(cs[25]), croissant_partout=bool(np.all(np.diff(cs) > 0)))
bilan['P1_loi_de_niveau'] = p1

# ------------------------------------------------------------------ P2, P3, P4 : famille de freins
ns = np.round(np.arange(0.5, 4.0001, 0.02), 4)
pb = profil_n(lambda E: chi2_bao(E)[0], ns)
pc = profil_n(lambda E: chi2_cc(E)[0], ns)
pt = profil_n(lambda E: chi2_bao(E)[0] + chi2_cc(E)[0], ns)


def resume(p, ddl):
    i = p[:, 2].argmin()
    dx = p[:, 2] - p[i, 2]
    val = lambda n: float(dx[np.argmin(np.abs(p[:, 0] - n))])
    return dict(meilleur_n=float(p[i, 0]), w=float(p[i, 1]), chi2=float(p[i, 2]), degres_de_liberte=ddl,
                un_ecart_type=intervalle(p, 1.0), deux_ecarts_types=intervalle(p, 4.0),
                delta_chi2={'n=1': val(1), 'n=1.5': val(1.5), 'n=2': val(2), 'n=2.5': val(2.5), 'n=3': val(3)},
                w_a_n2=float(p[np.argmin(np.abs(p[:, 0] - 2)), 1]), bord_w_atteint=bool(p[i, 1] > 0.999))


bilan['P2_DESI_seul'] = resume(pb, 13 - 3)
bilan['P3_chronometres_seuls'] = resume(pc, 31 - 3)
bilan['P4_DESI_et_chronometres'] = resume(pt, 44 - 4)
wt = bilan['P4_DESI_et_chronometres']['w_a_n2']
bilan['P4_DESI_et_chronometres']['a_n2'] = dict(H0=chi2_cc(E_frein(wt, 2))[1], alpha=chi2_bao(E_frein(wt, 2))[1])
bilan['P4_DESI_et_chronometres']['a_n2']['r_d_Mpc'] = C / (bilan['P4_DESI_et_chronometres']['a_n2']['alpha'] * bilan['P4_DESI_et_chronometres']['a_n2']['H0'])
bilan['profil_DESI'] = {f'{n:.2f}': [float(w), float(c)] for n, w, c in pb[::5]}

# ------------------------------------------------------------------ T4 : exposant de croissance de la loi locale, ere de matiere
t4 = {}
for B in (0.0, 0.2, 1 / 3, 0.45):
    d0 = 1e-6
    c0 = math.sqrt(2.0)
    t0 = 2 / c0
    pt_ = 2 - 4 * B

    def droite(t, y, B=B):
        l1, c1, l2, c2_ = y
        return [-c1, -B * c1 * c1 - (1 - 2 * B) * math.exp(l1), -c2_, -B * c2_ * c2_ - (1 - 2 * B) * math.exp(l2)]
    y0 = [0.0, c0, math.log1p(d0), c0 - pt_ * d0 / t0]
    ts = [t0 * 2 ** 1.5, t0 * 8]
    sol = solve_ivp(droite, (t0, ts[-1]), y0, t_eval=ts, rtol=1e-13, atol=1e-15, method='DOP853')
    dl = np.expm1(sol.y[2] - sol.y[0])
    aa = np.exp(-sol.y[0] / 3)
    t4[f'{B:.4f}'] = dict(mesure=float(math.log(dl[1] / dl[0]) / math.log(aa[1] / aa[0])), theoreme=3 - 6 * B)
bilan['T4_exposant_de_croissance'] = t4

# ------------------------------------------------------------------ T5 : sphere newtonienne de coquilles, avec constante
G_M, LAM = 1.0, 0.3


def coquille(t, y, gm):
    r, v = y
    return [v, -gm / r ** 2 + LAM * r / 3]


v0 = math.sqrt(2 * G_M + LAM / 3)                      # platitude : v^2 = 2GM/r + Lambda r^2 / 3 en r = 1
sol = solve_ivp(coquille, (0, 2.0), [1.0, v0], args=(G_M,), rtol=1e-12, atol=1e-14, method='DOP853', dense_output=True)
ecart = 0.0
for t in (0.5, 1.0, 1.5):
    h = 1e-4
    cad = lambda s: 3 * sol.sol(s)[1] / sol.sol(s)[0]
    dcdt = (-cad(t + 2 * h) + 8 * cad(t + h) - 8 * cad(t - h) + cad(t - 2 * h)) / (12 * h)
    r = sol.sol(t)[0]
    loi = (3 * LAM - cad(t) ** 2) / 3 - 3 * G_M / r ** 3                      # 4 pi G rho = 3 GM / r^3
    ecart = max(ecart, abs(dcdt / loi - 1))
d0 = 1e-5
H0_ = math.sqrt(2.0)                                   # ere de matiere pure : v = sqrt(2GM/r)


def matiere(t, y):
    r1, v1, r2, v2 = y
    return [v1, -1.0 / r1 ** 2, v2, -(1 + d0) / r2 ** 2]


def atteint(a):
    ev = lambda t, y: y[0] - a
    ev.terminal = True
    s = solve_ivp(matiere, (0, 100), [1.0, H0_, 1.0, H0_ * (1 - d0 / 3)], events=ev, rtol=1e-13, atol=1e-15, method='DOP853')
    r1, _, r2, _ = s.y[:, -1]
    return (1 + d0) * (r1 / r2) ** 3 - 1


bilan['T5_coquilles'] = dict(ecart_relatif_a_la_loi_B_un_tiers=ecart, exposant_de_croissance=math.log(atteint(4.0) / atteint(2.0)) / math.log(2.0))

# ------------------------------------------------------------------ P5 : croissance des structures, famille B (forme seule, amplitude libre)
OM = w2
zf, ff, sf = FS8.T
wf = 1 / sf ** 2


def croissance(B):
    """f(z) et D(z) (normalise a z = 0) pour la loi locale B, sur le fond n = 2."""
    Om_a = lambda x: OM * math.exp(-3 * x) / (1 - OM + OM * math.exp(-3 * x))

    def droite(x, y):
        u, fr = y
        return [fr, -fr * fr - (-1.5 * Om_a(x) + 6 * B) * fr + 4.5 * (1 - 2 * B) * Om_a(x)]
    xs = np.log(1 / (1 + zf))[::-1]
    sol = solve_ivp(droite, (math.log(1e-3), 0.0), [0.0, 3 - 6 * B], t_eval=list(xs) + [0.0], rtol=1e-10, atol=1e-12, method='DOP853')
    u, fr = sol.y
    return fr[:-1][::-1], np.exp(u[:-1] - u[-1])[::-1], float(fr[-1])


def chi2_croissance(B):
    fr, D, _ = croissance(B)
    m = fr * D
    A = float((wf * ff * m).sum() / (wf * m * m).sum())
    return float((wf * (ff - A * m) ** 2).sum()), A


Bs = np.round(np.arange(0.0, 0.4951, 0.005), 4)
cg = np.array([chi2_croissance(B)[0] for B in Bs])
ib = cg.argmin()
pg = np.column_stack([Bs, Bs, cg])
vb = lambda B: float(cg[np.argmin(np.abs(Bs - B))] - cg[ib])
bilan['P5_croissance'] = dict(meilleur_B=float(Bs[ib]), chi2=float(cg[ib]), degres_de_liberte=6 - 2,
                              un_ecart_type=intervalle(pg, 1.0), deux_ecarts_types=intervalle(pg, 4.0),
                              delta_chi2={'B=0': vb(0), 'B=0.20': vb(0.2), 'B=0.25': vb(0.25), 'B=0.30': vb(0.3), 'B=1/3': vb(0.335),
                                          'B=0.40': vb(0.4), 'B=0.45': vb(0.45), 'B=0.49': vb(0.49)},
                              chi2_B_un_tiers_exact=chi2_croissance(1 / 3)[0], amplitude_B_un_tiers=chi2_croissance(1 / 3)[1],
                              f_aujourdhui={f'{B:.3f}': croissance(B)[2] for B in (0.0, 0.25, 1 / 3, 0.4, 0.49)},
                              Omega_m_du_fond=OM)

# ------------------------------------------------------------------ P6 : lecture cinematique (deficit de volume), Terre
MPC = 3.0856775814913673e22
H0s = 67.4e3 / MPC
cinf = 3 * H0s * math.sqrt(1 - OM)
V, R, GMt = 1.08321e21, 6.371e6, 3.986004418e14
g = GMt / R ** 2
v = cinf * V / (4 * math.pi * R ** 2)
acc = 2 * v * v / R
taux = 1.5 * math.sqrt(2 * GMt / R ** 3)
rho_t = 5513.4
G = 6.6743e-11
an = 365.25 * 86400
bilan['P6_lecture_cinematique'] = dict(cadence_libre_par_seconde=cinf, doublement_libre_milliards_d_annees=math.log(2) / cinf / an / 1e9,
                                       cadence_aujourdhui_sur_cadence_libre=1 / math.sqrt(1 - OM),
                                       vitesse_d_afflux_surface_m_s=v, acceleration_m_s2=acc, rapport_a_la_pesanteur=acc / g,
                                       exposant_de_l_acceleration=-5, vitesse_de_liberation_m_s=math.sqrt(2 * GMt / R),
                                       taux_de_destruction_requis_par_seconde=taux, rapport_au_taux_libre=taux / cinf,
                                       frein_dans_la_Terre_sur_moteur=4 * math.pi * G * rho_t / (cinf ** 2 / 3),
                                       frein_moyen_aujourdhui_sur_moteur=OM / (2 * (1 - OM)),
                                       redshift_d_equilibre_frein_moteur=(2 * (1 - OM) / OM) ** (1 / 3) - 1)

(ICI / 'c148c.json').write_text(json.dumps(bilan, indent=1, ensure_ascii=False, default=float))
json.dump(bilan, sys.stdout, indent=1, ensure_ascii=False, default=float)
print()
