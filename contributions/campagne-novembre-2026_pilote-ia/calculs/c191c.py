#!/usr/bin/env python3
"""C-191c -- contre-calcul independant du C-191-U de ChatGPT (Claude, 16 novembre 2026) : diffusion dq_i/dt = somme sur les voisins (q_j - q_i) sur les graphes de liens des cristaux A15 et sigma
(tores de L x L x L mailles et tore 8 x 4 x 2). Ecrit d'apres son seul PROTOCOLE SCELLE. AJOUT de Claude, declare avant calcul : memes mesures sur deux reseaux SANS motif cinq/six
(cubique a faces centrees, cubique simple) et sur C15, pour voir si le resultat doit quelque chose aux tissus de tetraedres. Predictions : c191c_prediction.txt. Usage : python3 c191c.py -> c191c.json"""
import itertools, json, math
import numpy as np
from c189dc import A15, FCC, C15
from c190c import base as base_sigma, CA

def voisins(B, S, q=1.30):
    B = np.array(B, float); S = np.array(S, float); n = len(B); D = list(itertools.product((-1, 0, 1), repeat=3))
    P = [(i, d, (B[i] + np.array(d)) * S) for d in D for i in range(n)]; dmin = min(np.linalg.norm(p[2] - B[i] * S) for i in range(n) for p in P if not (p[0] == i and p[1] == (0, 0, 0)))
    V = [(i, j, d, (B[j] + np.array(d) - B[i]) * S) for i in range(n) for (j, d, x) in P if not (j == i and d == (0, 0, 0)) and np.linalg.norm(x - B[i] * S) <= q * dmin + 1e-11]
    return n, V, dmin

def spectre(n, V, L):
    vals = []
    for p in itertools.product(*[range(l) for l in L]):
        k = np.array([2 * math.pi * p[a] / L[a] for a in range(3)]); M = np.zeros((n, n), complex)
        for i, j, d, x in V: M[i, i] += 1; M[i, j] -= np.exp(1j * np.dot(k, d))
        vals += list(np.linalg.eigvalsh(M))
    vals = np.sort(np.array(vals)); return vals

def etude(nom, B, S):
    n, V, dmin = voisins(B, S); deg = [sum(1 for v in V if v[0] == i) for i in range(n)]; r = dict(structure=nom, sites=n, liens_par_maille=len(V) / 2, degres=sorted(set(deg)), d_min=float(dmin),
        somme_des_vecteurs_de_lien_max=float(max(np.linalg.norm(sum(v[3] for v in V if v[0] == i)) for i in range(n))), D_naif=[float(sum(v[3][a] ** 2 for v in V) / 2 / n) for a in range(3)], tores=[])
    for L in ((3, 3, 3), (4, 4, 4), (5, 5, 5), (6, 6, 6), (8, 4, 2)):
        w = spectre(n, V, L); zeros = int((abs(w) < 1e-9).sum()); l2 = float(w[w > 1e-9].min()); Lx = max(L[a] * S[a] for a in range(3))
        r['tores'].append(dict(L=list(L), N=n * L[0] * L[1] * L[2], zeros=zeros, vp_min=float(w.min()), lambda2=l2, lambda2_fois_longueur_max_au_carre=l2 * Lx * Lx, vp_max=float(w.max())))
    return r

if __name__ == '__main__':
    Bs, Ts, _ = base_sigma(); out = []
    for nom, B, S in (('A15', A15, (1, 1, 1)), ('sigma', Bs, (1, 1, CA)), ('C15', C15, (1, 1, 1)), ('cubique a faces centrees', FCC, (1, 1, 1)), ('cubique simple', [(0, 0, 0)], (1, 1, 1))):
        r = etude(nom, B, S); out.append(r)
        print(nom, 'liens', r['liens_par_maille'], 'degres', r['degres'], 'somme vecteurs %.1e' % r['somme_des_vecteurs_de_lien_max'], 'D naif', [round(x, 5) for x in r['D_naif']])
        for t in r['tores']: print('   L', t['L'], 'N', t['N'], 'zeros', t['zeros'], 'lambda2 %.9f' % t['lambda2'], 'x Lmax^2 = %.5f' % t['lambda2_fois_longueur_max_au_carre'], '(4 pi^2 D naif = %.5f)' % (4 * math.pi ** 2 * r['D_naif'][0]), flush=True)
    # controle direct : relaxation du mode lent sur A15 4x4x4 par integration exacte de la matrice assemblee
    n, V, _ = voisins(A15, (1, 1, 1)); L = 4; idx = {(i, a, b, c): i + n * (a + L * (b + L * c)) for i in range(n) for a in range(L) for b in range(L) for c in range(L)}; N = n * L ** 3; M = np.zeros((N, N))
    for (i, a, b, c), I in idx.items():
        for i2, j, d, x in V:
            if i2 == i: J = idx[(j, (a + d[0]) % L, (b + d[1]) % L, (c + d[2]) % L)]; M[I, I] += 1; M[I, J] -= 1
    w, U = np.linalg.eigh(M); q0 = U[:, 1]; qt = U @ (np.exp(-w / w[1]) * (U.T @ q0)); ctrl = dict(symetrique=bool(np.allclose(M, M.T)), sommes_de_lignes=float(abs(M.sum(1)).max()), lambda2_assemble=float(w[1]), nombre_de_zeros=int((abs(w) < 1e-9).sum()),
        erreur_relaxation=float(np.linalg.norm(qt - math.exp(-1) * q0)), conservation=float(abs(qt.sum() - q0.sum())))
    print('controle A15 4^3 :', ctrl); json.dump(dict(structures=out, controle=ctrl), open('c191c.json', 'w'), indent=1)
