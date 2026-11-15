#!/usr/bin/env python3
"""C-172 / PR-AB -- execution par Claude du protocole fige de ChatGPT (empreinte fa5711d7...c016), programme a moi, sans son code (15 novembre 2026).
Valeurs connues d'avance des deux auditeurs (X-4, C-169) : controle de reproduction, pas prediction aveugle."""
import json, math
from fractions import Fraction
import numpy as np, scipy.optimize as so
out = dict(A={}, temoins={}, B={})


def reseau(n):
    return np.array([(0, 1)] + [(p, 2 + i) for p in (0, 1) for i in range(n)] + [(2 + i, 2 + (i + 1) % n) for i in range(n)])


def coords(n, h, r):
    return np.array([[0, 0, h / 2], [0, 0, -h / 2]] + [[r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n), 0] for i in range(n)])


def energie(z, ed, L0):
    X = z.reshape(-1, 3); D = X[ed[:, 0]] - X[ed[:, 1]]; L = np.linalg.norm(D, axis=1); G = np.zeros_like(X); w = ((L - L0) / L)[:, None] * D
    np.add.at(G, ed[:, 0], w); np.add.at(G, ed[:, 1], -w); return 0.5 * ((L - L0) ** 2).sum(), G.ravel()


def hessien(X, ed, L0):
    N = len(X); H = np.zeros((3 * N, 3 * N))
    for (a, b), l0 in zip(ed, L0):
        d = X[a] - X[b]; L = np.linalg.norm(d); u = d / L; K = (1 - l0 / L) * np.eye(3) + (l0 / L) * np.outer(u, u); i, j = 3 * a, 3 * b
        H[i:i+3, i:i+3] += K; H[j:j+3, j:j+3] += K; H[i:i+3, j:j+3] -= K; H[j:j+3, i:i+3] -= K
    return H


def E2(v, n):
    h, r = v; p = math.sqrt(r * r + h * h / 4); q = 2 * r * math.sin(math.pi / n); return 0.5 * (h - 1) ** 2 + n * (p - 1) ** 2 + n / 2 * (q - 1) ** 2


for n in range(3, 13):
    ed = reseau(n); L0 = np.ones(len(ed))
    # A1 : deux variables, grille 9 x 9 de departs + depart de reference
    sols = []
    for h0 in np.linspace(0.3, 1.8, 9):
        for r0 in np.linspace(0.3, 1.8, 9):
            s = so.minimize(E2, [h0, r0], args=(n,), method='BFGS', options=dict(gtol=1e-13))
            if 0.3 <= s.x[0] <= 1.8 and 0.3 <= s.x[1] <= 1.8 and not any(abs(s.x[0] - a[0]) < 1e-6 and abs(s.x[1] - a[1]) < 1e-6 for a in sols): sols.append((float(s.x[0]), float(s.x[1]), float(s.fun)))
    ref = so.minimize(E2, [1.0, math.sqrt(3) / 2], args=(n,), method='BFGS', options=dict(gtol=1e-13))
    # ERRATUM (declare, apres la premiere execution gardee en *_v1) : le residu du gradient depassait le seuil 1e-8 du protocole (jusqu'a 3,4e-8) ; polissage par
    # resolution de dE/dh = dE/dr = 0 (gradient analytique), sans changer le seuil.
    def g2(v):
        h_, r_ = v; p = math.sqrt(r_ * r_ + h_ * h_ / 4); q = 2 * r_ * math.sin(math.pi / n)
        return [(h_ - 1) + 2 * n * (p - 1) * (h_ / 4) / p, 2 * n * (p - 1) * r_ / p + n * (q - 1) * 2 * math.sin(math.pi / n)]
    pol = so.root(g2, ref.x, tol=1e-15); h, r = pol.x; ref.fun = E2(pol.x, n)
    # A2 : toutes les coordonnees
    X = coords(n, h, r); Ef, G = energie(X.ravel(), ed, L0); H = hessien(X, ed, L0); w = np.linalg.eigvalsh(H)
    rig = int((np.abs(w) < 1e-6).sum()); neg = int((w < -1e-7).sum())
    def fd(pas):
        Hn = np.zeros_like(H); z = X.ravel()
        for j in range(len(z)):
            d = np.zeros(len(z)); d[j] = pas; Hn[:, j] = (energie(z + d, ed, L0)[1] - energie(z - d, ed, L0)[1]) / (2 * pas)
        return float(np.abs(Hn - H).max() / np.abs(H).max())
    gfd = max(abs((energie(X.ravel() + 1e-5 * e, ed, L0)[0] - energie(X.ravel() - 1e-5 * e, ed, L0)[0]) / 2e-5 - G[k]) for k, e in enumerate(np.eye(X.size)))
    pert = []
    for g in range(6):
        rng = np.random.Generator(np.random.PCG64(g)); s = so.minimize(energie, (X + 0.02 * rng.standard_normal(X.shape)).ravel(), args=(ed, L0), jac=True, method='L-BFGS-B', options=dict(gtol=1e-12, ftol=1e-18, maxiter=20000))
        Xp = s.x.reshape(-1, 3); a, b, c, d = Xp[0], Xp[1], Xp[2:], np.roll(Xp[2:], -1, axis=0); vols = np.einsum('ij,ij->i', np.cross(b - a, c - a), d - a) / 6
        pert.append(dict(graine=g, E=float(s.fun), vp_min=float(np.linalg.eigvalsh(hessien(Xp, ed, L0))[0]), cellule_inversee=bool((np.sign(vols) != np.sign(vols[0])).any())))
    out['A'][n] = dict(h=float(h), r=float(r), E_A1=float(ref.fun), E_A2=float(Ef), ecart_A1_A2=abs(float(ref.fun) - Ef), gradient_max=float(np.abs(G).max()), modes_rigides=rig, modes_negatifs=neg, vp_min=float(w[0]),
                       ecart_hessien_1e5=fd(1e-5), ecart_hessien_3e6=fd(3e-6), ecart_gradient_fd=float(gfd), minima_2_variables=sols, perturbations=pert)
    print('A', n, 'h %.9f r %.9f' % (h, r), 'E %.12f' % Ef, 'ecart A1-A2 %.1e' % out['A'][n]['ecart_A1_A2'], 'grad %.1e' % np.abs(G).max(), 'rigides', rig, 'negatifs', neg, 'hess fd %.1e %.1e' % (out['A'][n]['ecart_hessien_1e5'], out['A'][n]['ecart_hessien_3e6']),
          '| minima 2 var', len(sols), '| perturbes : E min %.9f' % min(p['E'] for p in pert), 'inversees', sum(p['cellule_inversee'] for p in pert), flush=True)
# temoins negatifs (n = 5)
n = 5; ed = reseau(n); h, r = out['A'][5]['h'], out['A'][5]['r']; X = coords(n, h, r); L3 = 1.03 * np.ones(len(ed))
s = so.minimize(energie, X.ravel(), args=(ed, L3), jac=True, method='L-BFGS-B', options=dict(gtol=1e-13, ftol=1e-18, maxiter=20000)); Xs = s.x.reshape(-1, 3)
i, j = np.triu_indices(len(X), 1); rap = np.linalg.norm(Xs[i] - Xs[j], axis=1) / np.linalg.norm(X[i] - X[j], axis=1)
out['temoins']['L0=1.03'] = dict(E_anciennes_coordonnees=float(energie(X.ravel(), ed, L3)[0]), E_relaxe=float(s.fun), rapport_E=float(s.fun / out['A'][5]['E_A2']), attendu=1.03 ** 2, rapport_distances_min=float(rap.min()), rapport_distances_max=float(rap.max()),
                                 ecart_hessien=float(np.abs(np.linalg.eigvalsh(hessien(Xs, ed, L3)) - np.linalg.eigvalsh(hessien(X, ed, np.ones(len(ed))))).max()))
L9 = np.ones(len(ed)); L9[-1] = 0.9; s = so.minimize(energie, X.ravel(), args=(ed, L9), jac=True, method='L-BFGS-B', options=dict(gtol=1e-13, ftol=1e-18, maxiter=20000)); Xs = s.x.reshape(-1, 3)
cote = np.linalg.norm(Xs[2:] - np.roll(Xs[2:], -1, axis=0), axis=1)
out['temoins']['un_lien_0.9'] = dict(E=float(s.fun), cotes_ceinture=[float(x) for x in cote], symetrie_brisee=bool(cote.max() - cote.min() > 1e-6), gradient_force_symetrique=float(np.abs(energie(X.ravel(), ed, L9)[1]).max()))
print('TEMOINS', json.dumps(out['temoins']), flush=True)
# B1 exact
c = Fraction(1, 3); T = {1: c, 2: 2 * c * c - 1}
for k in range(3, 7): T[k] = 2 * c * T[k - 1] - T[k - 2]
d2 = {k: Fraction(3, 2) * (1 - T[k]) for k in range(1, 7)}
out['B']['exact'] = dict(cos_5_theta=str(T[5]), d5_carre=str(d2[5]), d_carres={k: str(v) for k, v in d2.items()}, d2=str(d2[2]) + ' = 8/3', d3_carre_egale_25_9=bool(d2[3] == Fraction(25, 9)), d4_carre_egale_96_81=bool(d2[4] == Fraction(96, 81)),
                         d5_egale_1_9=bool(d2[5] == Fraction(1, 81)), ordre=bool(d2[2] > 1 and d2[3] > 1 and d2[4] > 1 and d2[5] < Fraction(1, 16) and d2[6] > Fraction(1, 16)))
# B2 numerique
th = math.acos(1 / 3); num = {}
for k in range(1, 7):
    X = np.array([[0, 0, .5], [0, 0, -.5]] + [[math.sqrt(3) / 2 * math.cos(i * th), math.sqrt(3) / 2 * math.sin(i * th), 0] for i in range(k + 1)])
    ar = [(0, 1)] + [(p, 2 + i) for p in (0, 1) for i in range(k + 1)] + [(2 + i, 3 + i) for i in range(k)]; L = [float(np.linalg.norm(X[a] - X[b])) for a, b in ar]
    vols = [abs(float(np.dot(np.cross(X[1] - X[0], X[2 + i] - X[0]), X[3 + i] - X[0]))) / 6 for i in range(k)]; d = float(np.linalg.norm(X[2] - X[2 + k]))
    num[k] = dict(sommets=len(X), cellules=k, aretes=len(ar), d=d, ecart_formule=abs(d - math.sqrt(3) * abs(math.sin(k * th / 2))), ecart_exact=abs(d - math.sqrt(float(d2[k]))), ecart_max_longueur=max(abs(l - 1) for l in L), volume_min=min(vols), volume_regulier=1 / (6 * math.sqrt(2)))
out['B']['numerique'] = num; out['B']['temoin_theta_pi_sur_2'] = dict(d5=math.sqrt(3) * abs(math.sin(5 * math.pi / 4)), different_de_1_9=bool(abs(math.sqrt(3) * abs(math.sin(5 * math.pi / 4)) - 1 / 9) > 0.1))
out['B']['temoin_k4_seuil_025'] = dict(d4=num[4]['d'], fusion=bool(num[4]['d'] < 0.25))
print('B exact', json.dumps(out['B']['exact'])); print('B num', {k: (round(v['d'], 12), '%.1e' % v['ecart_formule'], '%.1e' % v['ecart_max_longueur']) for k, v in num.items()}); print('B temoins', out['B']['temoin_theta_pi_sur_2'], out['B']['temoin_k4_seuil_025'])
json.dump(out, open('c172ab_c.json', 'w'), indent=1)
