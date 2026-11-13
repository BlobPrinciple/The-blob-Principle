#!/usr/bin/env python3
"""C-146 / CAS-1 -- contre-audit independant (Claude, 13 novembre 2026).

Protocole audite : C146_CAS1_PREENREGISTRE.md
SHA-256 cdd0ccd42b35152535d715ea31328d2022e5f17f8941b48b036d51a134c56f25

Programme ecrit sans reprendre celui de ChatGPT : la geometrie est reconstruite
d'apres le texte du protocole, l'interaction est calculee par conditionnement
(complement de Schur, factorisation de Cholesky) et non par trois logdet.
Predictions ecrites avant execution : c146_contre_audit_prediction.txt.

Usage : python3 c146_contre_audit.py  (ecrit c146_contre_audit.json et affiche le bilan)
"""
import json
import math
import pathlib
import sys

import numpy as np
from scipy.linalg import cho_factor, cho_solve

ICI = pathlib.Path(__file__).resolve().parent
R3 = math.sqrt(3.0)
H = math.sqrt(2.0 / 3.0)
FACE = np.array([[0.0, 1 / R3, 0.0], [-0.5, -1 / (2 * R3), 0.0], [0.5, -1 / (2 * R3), 0.0]])


def tourne(P, angle):
    c, s = math.cos(angle), math.sin(angle)
    M = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    return P @ M.T


def tetra(z_face, z_pointe, angle=0.0):
    """Tetraedre regulier de cote 1 : face horizontale a la cote z_face, pointe sur l'axe."""
    f = tourne(FACE, angle) + np.array([0.0, 0.0, z_face])
    return np.vstack([f, [0.0, 0.0, z_pointe]])


def scene(nom, g, angle_base_A=0.0):
    """Les quatre comparateurs du protocole. A dans z <= 0, B dans z >= g."""
    if nom == 'FF0':
        return tetra(0.0, -H), tetra(g, g + H)
    if nom == 'FF60':
        return tetra(0.0, -H), tetra(g, g + H, math.pi / 3)
    if nom == 'TF':
        return tetra(-H, 0.0, angle_base_A), tetra(g, g + H)
    if nom == 'TT':
        return tetra(-H, 0.0, angle_base_A), tetra(g + H, g)
    raise ValueError(nom)


def sites(V, m):
    """Points contraints. m = 4 : sommets. m = 14 : sommets, milieux d'aretes, barycentres de faces.
    m = ('reseau', k) : reseau triangulaire de k points par cote sur chacune des quatre faces."""
    if m == 4:
        return V.copy()
    if m == 14:
        P = [V[i] for i in range(4)]
        P += [(V[i] + V[j]) / 2 for i in range(4) for j in range(i + 1, 4)]
        P += [(V[a] + V[b] + V[c]) / 3 for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))]
        return np.array(P)
    k = m[1]
    vus = {}
    for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        for i in range(k):
            for j in range(k - i):
                l = k - 1 - i - j
                p = (i * V[a] + j * V[b] + l * V[c]) / (k - 1)
                vus[tuple(np.round(p, 10))] = p
    return np.array(list(vus.values()))


def noyau(X, Y, ell):
    d = np.linalg.norm(X[:, None, :] - Y[None, :, :], axis=2)
    return np.exp(-d / ell)


def interaction(A, B, ell):
    """dF/kBT = 1/2 ln det(I - C_A^-1 C_AB C_B^-1 C_BA), par Cholesky."""
    CA, CB, CAB = noyau(A, A, ell), noyau(B, B, ell), noyau(A, B, ell)
    fa, fb = cho_factor(CA), cho_factor(CB)
    M = np.eye(len(A)) - cho_solve(fa, CAB) @ cho_solve(fb, CAB.T)
    s, ld = np.linalg.slogdet(M)
    assert s > 0
    return 0.5 * ld


def information_mutuelle(A, B, ell):
    """I(A;B) = h(A) + h(B) - h(A,B), entropies differentielles gaussiennes, en nats."""
    def h(C):
        L = np.linalg.cholesky(C)
        return 0.5 * len(C) * math.log(2 * math.pi * math.e) + np.log(np.diag(L)).sum()
    CA, CB, CAB = noyau(A, A, ell), noyau(B, B, ell), noyau(A, B, ell)
    return h(CA) + h(CB) - h(np.block([[CA, CAB], [CAB.T, CB]]))


def dF(nom, g, ell, m, **kw):
    VA, VB = scene(nom, g, **kw)
    return interaction(sites(VA, m), sites(VB, m), ell)


bilan = {}

# ---------------------------------------------------------------- 1. recompte des 96 cas
ref = {}
for ligne in (ICI / 'chatgpt_cas1_96.csv').read_text().split():
    nom, g, ell, m, v = ligne.split(',')
    ref[(nom, float(g), float(ell), int(m))] = float(v)
ecarts = {k: abs(dF(k[0], k[1], k[2], k[3]) - v) for k, v in ref.items()}
moi = {k: dF(*k) for k in ref}
bilan['recompte_96'] = dict(n=len(ref), ecart_max=max(ecarts.values()),
                            n_sous_1e_9=sum(e < 1e-9 for e in ecarts.values()),
                            P1_tous_negatifs=all(v <= 1e-10 for v in moi.values()))
# P2, P3
p2 = [(m, ell, g) for m in (4, 14) for ell in (0.25, 0.5, 1.0) for g in (0.15, 0.30, 0.60, 1.20)
      if moi[('FF0', g, ell, m)] > moi[('TT', g, ell, m)] + 1e-12]
bilan['P2_contre_exemples'] = p2
bilan['P3'] = {m: (moi[('FF0', 0.15, 0.25, m)], moi[('FF60', 0.15, 0.25, m)]) for m in (4, 14)}
# P4 reellement calcule : bloc croise annule
A, B = (sites(V, 14) for V in scene('FF0', 0.30))
CA, CB = noyau(A, A, 0.5), noyau(B, B, 0.5)
Z = np.zeros((14, 14))
bilan['P4_bloc_croise_nul'] = 0.5 * (np.linalg.slogdet(np.block([[CA, Z], [Z, CB]]))[1]
                                     - np.linalg.slogdet(CA)[1] - np.linalg.slogdet(CB)[1])
# forces
forces_ref = {(4, 'FF0'): -2.5458975697356667, (4, 'FF60'): -0.3996037762538096,
              (4, 'TF'): -0.24226125162479795, (4, 'TT'): -0.8627228549340504,
              (14, 'FF0'): -4.76995496359045, (14, 'FF60'): -2.698348650413962,
              (14, 'TF'): -1.1449515816064348, (14, 'TT'): -0.8723368009189159}
forces = {}
for (m, nom), fr in forces_ref.items():
    def f(h):
        return -(dF(nom, 0.30 + h, 0.5, m) - dF(nom, 0.30 - h, 0.5, m)) / (2 * h)
    rich = (4 * f(5e-5) - f(1e-4)) / 3          # extrapolation de Richardson
    forces[f'{m}_{nom}'] = dict(moi=rich, chatgpt=fr, ecart_relatif=abs(rich - fr) / abs(fr))
bilan['forces'] = forces
# combien de cas depassent 1 kBT
bilan['n_plus_profond_que_1_kBT'] = sum(v < -1.0 for v in moi.values())

# ---------------------------------------------------------------- 2. identite d'information (A5)
bilan['A5_ecart_dF_plus_I'] = max(abs(dF(n, 0.30, 0.5, 14) + information_mutuelle(
    *(sites(V, 14) for V in scene(n, 0.30)), 0.5)) for n in ('FF0', 'FF60', 'TF', 'TT'))

# ---------------------------------------------------------------- 3. raffinement du maillage (A2)
raff = {}
for (g, ell) in ((0.30, 0.50), (0.15, 0.25)):
    lignes = []
    for k in (2, 3, 4, 5, 6, 8, 10, 12, 16):
        v = {n: dF(n, g, ell, ('reseau', k)) for n in ('FF0', 'FF60', 'TF', 'TT')}
        npts = len(sites(scene('FF0', g)[0], ('reseau', k)))
        lignes.append(dict(k=k, points_par_tetraedre=npts, **v,
                           FF60_sur_FF0=v['FF60'] / v['FF0'], TT_sur_FF0=v['TT'] / v['FF0'],
                           TF_sur_FF0=v['TF'] / v['FF0']))
    raff[f'g={g},ell={ell}'] = lignes
bilan['A2_raffinement'] = raff

# ---------------------------------------------------------------- 4. divergence au contact (A3)
c = {g: dF('FF0', g, 0.5, 14) for g in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5)}
bilan['A3_contact'] = dict(valeurs={str(g): v for g, v in c.items()},
                           pente_entre_1e_3_et_1e_4=(c[1e-3] - c[1e-4]) / math.log(1e-3 / 1e-4),
                           pente_entre_1e_4_et_1e_5=(c[1e-4] - c[1e-5]) / math.log(1e-4 / 1e-5))

# ---------------------------------------------------------------- 5. trois corps (A4)
def F(P, idx, ell=0.5):
    C = noyau(P[idx], P[idx], ell)
    return 0.5 * np.linalg.slogdet(C)[1]


def irreductible(P):
    return (F(P, [0, 1, 2]) - F(P, [0, 1]) - F(P, [0, 2]) - F(P, [1, 2]))  # F_i = 0 (variance 1)


d = 0.30
aligne = np.array([[0, 0, 0], [d, 0, 0], [2 * d, 0, 0]], float)
equi = np.array([[0, 0, 0], [d, 0, 0], [d / 2, d * R3 / 2, 0]], float)
rho = math.exp(-d / 0.5)
bilan['A4_trois_corps'] = dict(
    aligne=irreductible(aligne), aligne_analytique=-0.5 * math.log(1 - rho ** 4),
    moins_U13=-F(aligne, [0, 2]),
    equilateral=irreductible(equi),
    equilateral_analytique=-0.5 * math.log(1 - rho) + 0.5 * math.log(1 + 2 * rho) - 1.5 * math.log(1 + rho))

# ---------------------------------------------------------------- 6. orientation non precisee par le texte
# Le protocole ne fixe pas l'orientation de la base du tetraedre qui presente sa pointe (TF, TT).
sens = {}
for n in ('TF', 'TT'):
    for m in (4, 14):
        a, b = dF(n, 0.30, 0.5, m), dF(n, 0.30, 0.5, m, angle_base_A=math.pi / 3)
        sens[f'{n}_{m}'] = dict(base_0=a, base_60=b, ecart_relatif=abs(a - b) / abs(a))
bilan['orientation_base_non_precisee'] = sens

(ICI / 'c146_contre_audit.json').write_text(json.dumps(bilan, indent=1, ensure_ascii=False, default=float))
json.dump(bilan, sys.stdout, indent=1, ensure_ascii=False, default=float)
print()
