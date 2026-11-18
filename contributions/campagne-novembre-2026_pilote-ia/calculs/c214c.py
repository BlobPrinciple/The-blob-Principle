#!/usr/bin/env python3
"""C-212c, C-213c, C-214c -- contre-calculs des notes C-212, C-213, C-214 de ChatGPT (viabilite : noyaux, conditionnement a la survie, universalite de la diffusion).
Prediction scellee avant calcul : c214c_prediction.txt. Programme ecrit sans ouvrir les siens. Claude, 18 novembre 2026. Usage : python3 c214c.py"""
import itertools, json, math
import numpy as np
out = {}
# ---- C-212c : tous les graphes orientes de 1 a 4 etats
def k_ex(S, n):
    K = set(range(n))
    while True:
        M = {s for s in K if not (S[s] & K)}
        if not M: return K
        K -= M
def k_un(S, n):
    K = set(range(n))
    while True:
        M = {s for s in K if not S[s] or not S[s] <= K}
        if not M: return K
        K -= M
def k_cycle(S, n):
    # etats d'ou l'on atteint un cycle
    R = [[j in S[i] for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n): R[i][j] = R[i][j] or (R[i][k] and R[k][j])
    cyc = {i for i in range(n) if R[i][i]}
    return {i for i in range(n) if i in cyc or any(R[i][j] for j in cyc)}
tot = 0; acc = 0; par_n = {}
for n in (1, 2, 3, 4):
    dif = 0; nb = 0
    for bits in range(2 ** (n * n)):
        S = [set(j for j in range(n) if bits >> (i * n + j) & 1) for i in range(n)]
        a = k_ex(S, n); nb += 1; acc += (a == k_cycle(S, n)); dif += (a != k_un(S, n))
    par_n[n] = dict(graphes=nb, lectures_differentes=dif); tot += nb
out['C212c'] = dict(graphes=tot, deux_methodes_d_accord=acc, par_nombre_d_etats=par_n)
# ---- C-213c
Q = np.array([[0.25, 0.25], [0.25, 0.5]]); w, V = np.linalg.eigh(Q); lam = w[-1]; h = V[:, -1] / V[0, -1]
Qs = Q * h[None, :] / (lam * h[:, None]); pi = h ** 2 / (h ** 2).sum()
conv = []
for n in (1, 2, 5, 10, 20, 50, 100):
    a = np.linalg.matrix_power(Q, n - 1) @ np.ones(2); b = np.linalg.matrix_power(Q, n) @ np.ones(2)
    conv.append(dict(n=n, ecart_max=float(np.abs(Q * a[None, :] / b[:, None] - Qs).max())))
uni = []
for P in (np.eye(2), np.array([[0., 1.], [1., 0.]]), np.array([[0.9, 0.1], [0.2, 0.8]])):
    for c in (0.2, 0.65, 0.9):
        Qc = c * P; n = 30; a = np.linalg.matrix_power(Qc, n - 1) @ np.ones(2); b = np.linalg.matrix_power(Qc, n) @ np.ones(2)
        uni.append(float(np.abs(Qc * a[None, :] / b[:, None] - P).max()))
out['C213c'] = dict(un_etat_survie_100_pas=0.5 ** 100, lam=float(lam), lam_formule=(3 + 5 ** 0.5) / 8, h=h.tolist(), phi=(1 + 5 ** 0.5) / 2, Q_conditionne=Qs.tolist(), sommes_lignes=Qs.sum(1).tolist(),
                    pi=pi.tolist(), defaut_reversibilite=float(abs(pi[0] * Qs[0, 1] - pi[1] * Qs[1, 0])), rapport_valeurs_propres=float(w[0] / w[1]), convergence=conv, ecart_max_Q_egal_cP=max(uni))
# ---- C-214c
r3 = 3 ** 0.5
bras = dict(A=np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float),
            B=np.array(list(itertools.product((1, -1), repeat=3)), float) / r3,
            C=np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / r3)
k = np.array([1., 2., 3.]); hs = [0.2, 0.1, 0.05, 0.025, 0.0125]; res = {}
for nom, U in bras.items():
    sym = [complex((6 / hh ** 2) * (np.exp(1j * hh * (U @ k)).mean() - 1)) for hh in hs]; err = [abs(s + 14) for s in sym]
    pente = float(np.polyfit(np.log(hs), np.log(err), 1)[0]); pente_re = float(np.polyfit(np.log(hs), np.log([abs(s.real + 14) for s in sym]), 1)[0])
    res[nom] = dict(moyenne=np.abs(U.mean(0)).max().item(), ecart_second_moment=float(np.abs(U.T @ U / len(U) - np.eye(3) / 3).max()), E_uxuyuz=float((U[:, 0] * U[:, 1] * U[:, 2]).mean()),
                    symboles=[[s.real, s.imag] for s in sym], pente_erreur=pente, pente_partie_reelle=pente_re, imag_sur_h=[s.imag / hh for s, hh in zip(sym, hs)])
U = bras['C']; G = U @ U.T; msd = []
for n in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512):
    msd.append(dict(n=n, independant=float(n * np.trace(G) / 4 + n * (n - 1) * G.mean()), direction_conservee=float(n * n)))
P = np.full((4, 4), 0.25); c = 0.9; Qc = c * P; a = np.linalg.matrix_power(Qc, 19) @ np.ones(4); b = np.linalg.matrix_power(Qc, 20) @ np.ones(4)
out['C214c'] = dict(bras=res, un_sur_3_racine_3=1 / (3 * r3), moins_12_sur_racine_3=-12 / r3, deplacement_quadratique=msd, ecart_conditionnement_survie_uniforme=float(np.abs(Qc * a[None, :] / b[:, None] - P).max()))
json.dump(out, open('c214c.json', 'w'), indent=1); print(json.dumps(out))
