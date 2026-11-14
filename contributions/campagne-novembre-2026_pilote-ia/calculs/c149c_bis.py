#!/usr/bin/env python3
"""C-149c bis -- COMPLEMENT APRES COUP (declare) : l'instabilite de la trame de palier reguliere sous la regle U.
La prediction A6 de c149c_prediction.txt (stabilite) est FAUSSE. Ici : (1) spectre de Bloch sur toute la zone ; (2) etat flambe de
plus basse energie trouve, maille libre (echelle et forme), plusieurs graines ; (3) son tenseur des contraintes.
Aucune prediction ecrite avant ce complement : resultats exploratoires."""
import itertools, json, math, sys
import numpy as np, scipy.optimize as so
from c149c import classes_de_palier, reseau, etat, viriel, viriels_de_site, hessien
cl = classes_de_palier(); out = {}
lam0 = None
# ---------- (1) Bloch : base de 8 sites, maille conventionnelle 2
def dyn(k, a):
    base = list(itertools.product(range(2), repeat=3)); ix = {p: i for i, p in enumerate(base)}
    M = np.zeros((24, 24), complex)
    for p in base:
        for d in cl[p]:
            q = tuple((p[i] + d[i]) % 2 for i in range(3)); dv = np.array(d, float); L = a * np.linalg.norm(dv); n = dv / np.linalg.norm(dv); f = L - 1
            kk = np.outer(n, n) + (f / L) * (np.eye(3) - np.outer(n, n)); i, j = ix[p], ix[q]
            M[3*i:3*i+3, 3*i:3*i+3] += kk; M[3*i:3*i+3, 3*j:3*j+3] -= kk * np.exp(1j * np.dot(k, dv))
    return M
a = (3 + 3 * math.sqrt(2) + math.sqrt(3)) / 12
m = 24; pire = (1e9, None); gam = np.linalg.eigvalsh(dyn(np.zeros(3), a))
for t in itertools.product(range(m + 1), repeat=3):
    k = np.pi * np.array(t) / m        # zone de la maille conventionnelle : composantes dans [0, pi]
    ev = np.linalg.eigvalsh(dyn(k, a))
    if ev[0] < pire[0] - 1e-12: pire = (float(ev[0]), [x / m for x in t])
out['bloch'] = dict(a=a, minimum=pire[0], k_sur_pi=pire[1], gamma_plus_petites=[round(float(x), 6) for x in gam[:8]])
# seuil : a partir de quelle echelle la trame reguliere est stable (dilatation imposee)
def stable(s):
    return min(np.linalg.eigvalsh(dyn(np.pi * np.array(t) / 8, s))[0] for t in itertools.product(range(9), repeat=3)) > -1e-9
lo, hi = a, 1.2
assert not stable(lo) and stable(hi)
for _ in range(40):
    mid = (lo + hi) / 2
    lo, hi = (lo, mid) if stable(mid) else (mid, hi)
out['seuil_de_stabilite'] = dict(a_seuil=hi, rapport_a_seuil_sur_a_etoile=hi / a, force_fil_d_axe_au_seuil=hi - 1)
# mode instable a Gamma : qui bouge ?
w, v = np.linalg.eigh(dyn(np.zeros(3), a)); vec = v[:, 0].real.reshape(8, 3)
out['mode_gamma'] = {str(p): np.round(vec[i] / np.abs(vec).max(), 3).tolist() for i, p in enumerate(itertools.product(range(2), repeat=3))}
# ---------- (2) etat flambe, maille libre
def flambe(n, seed, amp=0.05):
    N, I, J, D = reseau(n, classes=cl); rng = np.random.default_rng(seed)
    def fun(z):
        U = z[:3 * N].reshape(-1, 3); h = z[3 * N:]
        F = np.array([[h[0], h[3], h[4]], [h[3], h[1], h[5]], [h[4], h[5], h[2]]])          # F symetrique (pas de rotation)
        B = D @ F.T + U[J] - U[I]; L = np.linalg.norm(B, axis=1); f = L - 1; w_ = (f / L)[:, None] * B
        G = np.zeros_like(U); np.add.at(G, J, w_); np.add.at(G, I, -w_)
        GF = np.einsum('ea,eb->ab', w_, D)
        gh = np.array([GF[0, 0], GF[1, 1], GF[2, 2], GF[0, 1] + GF[1, 0], GF[0, 2] + GF[2, 0], GF[1, 2] + GF[2, 1]])
        return 0.5 * (f ** 2).sum(), np.concatenate([G.ravel(), gh])
    z0 = np.concatenate([amp * rng.standard_normal(3 * N), [a, a, a, 0, 0, 0]])
    r = so.minimize(fun, z0, jac=True, method='L-BFGS-B', options=dict(gtol=1e-12, ftol=1e-17, maxiter=200000, maxfun=400000, maxcor=40))
    U = r.x[:3 * N].reshape(-1, 3); h = r.x[3 * N:]; F = np.array([[h[0], h[3], h[4]], [h[3], h[1], h[5]], [h[4], h[5], h[2]]])
    B = D @ F.T + U[J] - U[I]; L = np.linalg.norm(B, axis=1); f = L - 1; V = N * np.linalg.det(F)
    sig = np.einsum('e,ea,eb->ab', f / L, B, B) / V
    H = hessien(N, I, J, B, L, f); ev = np.linalg.eigvalsh(H) if N <= 216 else None
    W = viriels_de_site(N, I, J, B, L, f); tr = np.trace(W, axis1=1, axis2=2); deg = np.bincount(np.concatenate([I, J]), minlength=N)
    lam = np.linalg.norm(D, axis=1)
    # volumes orientes des cellules : cliques a 4 du graphe des fils (cellules du complexe), signe compare a l'etat regulier
    return dict(n=n, graine=seed, E_par_porteur=float(r.fun / N), E_par_fil=float(r.fun / len(L)), gradient_max=float(np.abs(r.jac).max()),
                F=np.round(F, 6).tolist(), volume_par_porteur=float(V / N), sigma_max=float(np.abs(sig).max()),
                hessien_min=None if ev is None else float(ev[0]), hessien_nulles=None if ev is None else int((np.abs(ev) < 1e-7).sum()),
                deplacement_rms=float(np.sqrt(((U - U.mean(0)) ** 2).sum(1).mean())),
                L_axes=[float(L[abs(lam - 1) < 1e-9].min()), float(L[abs(lam - 1) < 1e-9].mean()), float(L[abs(lam - 1) < 1e-9].max())],
                L_faces=[float(L[abs(lam - math.sqrt(2)) < 1e-9].min()), float(L[abs(lam - math.sqrt(2)) < 1e-9].mean()), float(L[abs(lam - math.sqrt(2)) < 1e-9].max())],
                L_espace=[float(L[lam > 1.7].min()), float(L[lam > 1.7].mean()), float(L[lam > 1.7].max())],
                fils_comprimes=float((f < 0).mean()), trace_site_26=float(tr[deg == 26].mean()), trace_site_10=float(tr[deg == 10].mean()),
                pression_site_26=float(-tr[deg == 26].mean() / (3 * V / N)), pression_site_10=float(-tr[deg == 10].mean() / (3 * V / N)))
res = []
for n, seeds in ((2, range(8)), (4, range(8)), (6, range(4))):
    for s in seeds:
        r = flambe(n, 1490 + s); res.append(r); print(json.dumps(r), flush=True)
out['flambes'] = res
best = min(res, key=lambda r: r['E_par_porteur']); out['meilleur'] = best
out['E_regulier_par_porteur'] = 0.5 * (7 - (3 + 3 * math.sqrt(2) + math.sqrt(3)) ** 2 / 12)
json.dump(out, open('c149c_bis.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'flambes'}, indent=1))
