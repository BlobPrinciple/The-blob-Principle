#!/usr/bin/env python3
"""X-4 [EXPLORATOIRE] -- Claude, 15 novembre 2026. Controle rapide, par un calcul a moi, de deux faits d'exploration de ChatGPT (C-167-E, C-168-E) :
(1) couronne fermee de n tetraedres autour d'un fil (deux poles, polygone de n sommets, 3n+1 liens de longueur naturelle 1) : energie minimale et stabilite ;
(2) eventail ouvert de cinq tetraedres reguliers : distance entre les deux sommets du bord ; energie apres pose d'un lien de longueur 1 entre eux ; energie si on les reunit.
Minimisation dans TOUTES les coordonnees (pas seulement la famille symetrique), depart symetrique legerement bruite."""
import itertools, json, math
import numpy as np, scipy.optimize as so
def energie(z, ed):
    X = z.reshape(-1, 3); D = X[ed[:, 0]] - X[ed[:, 1]]; L = np.linalg.norm(D, axis=1); G = np.zeros_like(X); w = ((L - 1) / L)[:, None] * D
    np.add.at(G, ed[:, 0], w); np.add.at(G, ed[:, 1], -w); return 0.5 * ((L - 1) ** 2).sum(), G.ravel()
def hess_min(X, ed):
    n = len(X); H = np.zeros((3 * n, 3 * n))
    for a, b in ed:
        d = X[a] - X[b]; L = np.linalg.norm(d); u = d / L; K = np.outer(u, u) + (1 - 1 / L) * (np.eye(3) - np.outer(u, u)); i, j = 3 * a, 3 * b
        H[i:i+3, i:i+3] += K; H[j:j+3, j:j+3] += K; H[i:i+3, j:j+3] -= K; H[j:j+3, i:i+3] -= K
    w = np.linalg.eigvalsh(H); return float(w[0]), int((w < -1e-7).sum())
def relaxe(X, ed, bruit=0.0, seed=0):
    rng = np.random.default_rng(seed); r = so.minimize(energie, (X + bruit * rng.standard_normal(X.shape)).ravel(), args=(ed,), jac=True, method='L-BFGS-B', options=dict(gtol=1e-13, ftol=1e-18, maxiter=20000))
    return r.x.reshape(-1, 3), float(r.fun)
out = {'couronnes': {}}
for n in range(3, 13):
    X = np.array([[0, 0, .5], [0, 0, -.5]] + [[math.sqrt(3) / 2 * math.cos(2 * math.pi * k / n), math.sqrt(3) / 2 * math.sin(2 * math.pi * k / n), 0] for k in range(n)])
    ed = np.array([(0, 1)] + [(p, 2 + k) for p in (0, 1) for k in range(n)] + [(2 + k, 2 + (k + 1) % n) for k in range(n)])
    Xs, Es = relaxe(X, ed); vm, neg = hess_min(Xs, ed); Xb, Eb = min((relaxe(X, ed, 0.05, s) for s in range(6)), key=lambda t: t[1])
    out['couronnes'][n] = dict(E_symetrique=Es, vp_min=vm, modes_negatifs=neg, E_apres_bruit=Eb, vp_min_apres_bruit=hess_min(Xb, ed)[0])
    print('couronne', n, 'E sym %.12f' % Es, 'modes negatifs', neg, '| meilleur de 6 departs bruites %.12f' % Eb, 'vp min %.4f' % hess_min(Xb, ed)[0])
# eventail ouvert de cinq
th = math.acos(1 / 3); X = np.array([[0, 0, .5], [0, 0, -.5]] + [[math.sqrt(3) / 2 * math.cos(k * th), math.sqrt(3) / 2 * math.sin(k * th), 0] for k in range(6)])
ed0 = [(0, 1)] + [(p, 2 + k) for p in (0, 1) for k in range(6)] + [(2 + k, 3 + k) for k in range(5)]
d = float(np.linalg.norm(X[2] - X[7])); print('eventail de cinq : distance des deux sommets du bord %.15f (1/9 = %.15f)' % (d, 1 / 9), 'E depart', energie(X.ravel(), np.array(ed0))[0])
ed1 = np.array(ed0 + [(2, 7)]); X1, E1 = relaxe(X, ed1); print('lien de longueur 1 pose entre eux : E avant %.10f (32/81 = %.10f), apres relaxation %.14f' % (energie(X.ravel(), ed1)[0], 32 / 81, E1), 'vp min', hess_min(X1, ed1))
# reunion des deux sommets : couronne de cinq
Xf = np.vstack([X[:7]]); Xf[2] = (X[2] + X[7]) / 2; edf = np.array([(0, 1)] + [(p, 2 + k) for p in (0, 1) for k in range(5)] + [(2 + k, 2 + (k + 1) % 5) for k in range(5)]); X2, E2 = relaxe(Xf, edf)
print('sommets reunis (couronne de cinq) : E apres relaxation %.14f' % E2, 'vp min', hess_min(X2, edf))
out['eventail'] = dict(distance=d, E_lien_pose=float(energie(X.ravel(), ed1)[0]), E_lien_relaxe=E1, E_reunion=E2)
json.dump(out, open('x4_couronnes.json', 'w'), indent=1)
