#!/usr/bin/env python3
"""C-199c -- contre-calcul independant du C-199 de ChatGPT (Claude, 17 novembre 2026), d'apres son seul PROTOCOLE : sorties du minimum local LJ13 a six (graine 192009 de C-192-U).
Methode propre : voisins par perturbation + minimisation, chaine d'images relachee, col par annulation du gradient, hessien, descentes. Physique connue des amas de Lennard-Jones.
Predictions : c199c_prediction.txt. Usage : python3 c199c.py -> c199c.json"""
import json
import numpy as np, scipy.optimize as so
from c187c import lj
from c189c import mesure
from x15_six_dans_un_minimum_local import X as X0

def mini(x): r = so.minimize(lj, x.ravel(), jac=True, method='L-BFGS-B', options=dict(maxiter=20000, gtol=1e-11, ftol=1e-15)); r = so.minimize(lj, r.x, jac=True, method='BFGS', options=dict(gtol=1e-10, maxiter=5000)); return r.x.reshape(-1, 3), float(r.fun)
def kabsch(P, Q):
    """aligne P sur Q (memes indices) : rotation + translation."""
    Pc, Qc = P - P.mean(0), Q - Q.mean(0); U, S, Vt = np.linalg.svd(Pc.T @ Qc); d = np.sign(np.linalg.det(U @ Vt)); R = U @ np.diag([1, 1, d]) @ Vt; return Pc @ R + Q.mean(0)
def hess(z, h=1e-5): H = np.array([(lj(z + h * v)[1] - lj(z - h * v)[1]) / (2 * h) for v in np.eye(len(z))]); return (H + H.T) / 2
def sp(X): m = mesure(X, 1.30 + 1e-12); return dict(tetraedres=m['tetraedres'], distribution={int(k): v for k, v in m['distribution'].items()}, surcharges=m['faces_surchargees'])
def chaine(A, B, n=21, iters=4000, pas=2e-4):
    P = np.array([A + (B - A) * t for t in np.linspace(0, 1, n)]); e0 = max(lj(p.ravel())[0] for p in P)
    for _ in range(iters):
        for i in range(1, n - 1):
            g = lj(P[i].ravel())[1].reshape(-1, 3); tau = P[i + 1] - P[i - 1]; tau /= np.linalg.norm(tau); g = g - (g * tau).sum() * tau; P[i] = P[i] - pas * g
        s = np.concatenate([[0], np.cumsum([np.linalg.norm(P[i + 1] - P[i]) for i in range(n - 1)])]); s /= s[-1]; Q = P.copy()
        for i in range(1, n - 1):
            t = i / (n - 1); j = min(np.searchsorted(s, t) - 1, n - 2); j = max(j, 0); w = (t - s[j]) / (s[j + 1] - s[j]); Q[i] = P[j] + w * (P[j + 1] - P[j])
        P = Q
    E = [float(lj(p.ravel())[0]) for p in P]; return P, E, float(e0)

if __name__ == '__main__':
    A, EA = mini(X0); out = dict(depart=dict(E=EA, ecart_au_fourni=float(abs(A - X0).max()), **sp(A)))
    w = np.linalg.eigvalsh(hess(A.ravel())); out['depart'].update(modes_nuls=int((abs(w) < 1e-3).sum()), negatives=int((w < -1e-3).sum()), plus_petite_positive=float(w[w > 1e-3].min()))
    phi = (1 + 5 ** .5) / 2; ico = np.array([p for a in (1, -1) for b in (phi, -phi) for p in ((0, a, b), (a, b, 0), (b, 0, a))], float); I, EI = mini(np.vstack([[0, 0, 0], ico / np.linalg.norm(ico[0])])); out['icosaedre'] = dict(E=EI, ecart=EA - EI)
    print('depart', out['depart'], '| icosaedre', out['icosaedre'], flush=True)
    vois = {}
    for s in range(199000, 199060):
        rng = np.random.default_rng(s); B, EB = mini(A + rng.normal(0, 0.10 + 0.02 * (s % 6), A.shape))
        if EB < EA - 1e-6 and round(EB, 5) not in vois: vois[round(EB, 5)] = (kabsch(B, A), EB, s)
    print('minimums voisins plus bas :', sorted(vois), flush=True); out['voisins'] = []; cols = []
    for k in sorted(vois, reverse=True)[:8] if len(vois) > 8 else sorted(vois):
        B, EB, s = vois[k]; P, E, e0 = chaine(A, B); i = int(np.argmax(E)); r = so.least_squares(lambda z: lj(z)[1], P[i].ravel(), xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=400); z = r.x; g = float(np.linalg.norm(lj(z)[1])); ES = float(lj(z)[0])
        w, V = np.linalg.eigh(hess(z)); neg = int((w < -1e-3).sum()); nul = int((abs(w) < 1e-3).sum()); d = dict(graine=s, E_voisin=EB, spectre_voisin=sp(B), E_max_droite=e0 - EA, E_max_chaine=max(E) - EA, col_E=ES, barriere=ES - EA, gradient=g, negatives=neg, modes_nuls=nul, vp_negative=float(w[0]))
        if g < 1e-6 and neg == 1:
            fins = []
            for sg in (1, -1): Y, EY = mini(z.reshape(-1, 3) + sg * 0.02 * V[:, 0].reshape(-1, 3)); fins.append(dict(E=EY, spectre=sp(Y)))
            d['descentes'] = fins; d['relie_le_depart'] = bool(any(abs(f['E'] - EA) < 1e-6 for f in fins)); d['autre_plus_bas'] = bool(any(f['E'] < EA - 1e-6 for f in fins)); cols.append(d)
        out['voisins'].append(d); print({k2: (round(v, 6) if isinstance(v, float) else v) for k2, v in d.items()}, flush=True)
    ok = [c for c in cols if c['relie_le_depart'] and c['autre_plus_bas']]; out['cols_certifies'] = len(ok)
    if ok:
        b = min(ok, key=lambda c: c['barriere']); out['plus_basse'] = b; print('PLUS BASSE BARRIERE CERTIFIEE %.6f' % b['barriere'], '| col E %.6f' % b['col_E'], '| arrivee', [f for f in b['descentes'] if f['E'] < EA - 1e-6])
    json.dump(out, open('c199c.json', 'w'), indent=1)
