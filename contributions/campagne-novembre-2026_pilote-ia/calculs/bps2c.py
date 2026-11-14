#!/usr/bin/env python3
"""BP-S2c -- Recoupement independant des probabilites d'equilibre de BP-S2 (Claude, 14 novembre 2026).

Protocole de ChatGPT : BP_S2_PREENREGISTRE.md (empreinte aefdb108...4f28). Predictions : bps2c_prediction.txt (ecrit avant).
M1 : quadrature de Monte-Carlo directe pour A3 et A4.  M2 : echange de repliques pour F4, F5 (et A3 comme temoin).
Usage : python3 bps2c.py   (ecrit bps2c.json)
"""
import itertools
import json
import math
import sys

import numpy as np

RC = 1.15
EPS = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
TRI = np.array([[1 / math.sqrt(3), 0, 0], [-1 / (2 * math.sqrt(3)), 0.5, 0], [-1 / (2 * math.sqrt(3)), -0.5, 0]])
TET = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / math.sqrt(8)
out = {}


# ------------------------------------------------------------------ M1 : quadrature directe (un porteur mobile)
def quadrature(fixes, R, n_lots=40, lot=2_000_000, seed=14920):
    rng = np.random.default_rng(seed)
    centre = fixes.mean(0)
    nf = len(fixes)
    acc = np.zeros((n_lots, 3, 3))          # [lot, epsilon(0,2,4), (Z, K4 valide, K4 mauvais cote)]
    kmoy = np.zeros((n_lots, 3))
    for b in range(n_lots):
        x = rng.uniform(-R, R, (int(lot * 1.95), 3))
        x = x[(x ** 2).sum(1) <= R * R] + centre
        d = np.linalg.norm(x[:, None, :] - fixes[None], axis=2)
        ok = (d >= 1).all(1)
        x, d = x[ok], d[ok]
        c = d <= RC
        k = c.sum(1)
        if nf == 3:
            k4 = k == 3; mauvais = np.zeros(len(x), bool)
        else:
            k4 = np.zeros(len(x), bool); mauvais = np.zeros(len(x), bool)
            for i in range(4):                      # face opposee au sommet i
                face = [j for j in range(4) if j != i]
                touche = c[:, face].all(1)
                nrm = np.cross(fixes[face[1]] - fixes[face[0]], fixes[face[2]] - fixes[face[0]])
                cote_apex = np.sign(np.dot(fixes[i] - fixes[face[0]], nrm))
                cote = np.sign((x - fixes[face[0]]) @ nrm)
                k4 |= touche & (cote == -cote_apex); mauvais |= touche & (cote == cote_apex)
        for a, e in enumerate((0.0, 2.0, 4.0)):
            w = np.exp(e * k)
            acc[b, a] = [w.sum(), (w * k4).sum(), (w * mauvais).sum()]
            kmoy[b, a] = (w * k).sum()
    res = {}
    for a, e in enumerate((0, 2, 4)):
        p = acc[:, a, 1] / acc[:, a, 0]
        res[f'eps={e}'] = dict(K4=float(acc[:, a, 1].sum() / acc[:, a, 0].sum()), erreur=float(p.std(ddof=1) / math.sqrt(n_lots)),
                               mauvais_cote=float(acc[:, a, 2].sum() / acc[:, a, 0].sum()), contacts_moyens=float(kmoy[:, a].sum() / acc[:, a, 0].sum()))
    return res


# ------------------------------------------------------------------ M2 : echange de repliques
def moteur(N, R, fixes=None, depart='aleatoire', C=1000, pas=20000, rodage=4000, seed=0):
    rng = np.random.default_rng(seed)
    T = len(EPS)
    nf = 0 if fixes is None else len(fixes)
    centre = np.zeros(3) if fixes is None else fixes.mean(0)
    X = np.zeros((C, T, N, 3))
    if nf:
        X[:, :, :nf] = fixes
    if depart == 'compact':
        base = TET * 1.02 if N == 4 else np.vstack([TET, -TET[0] * (5 / 3)]) * 1.02       # apex miroir du sommet 0 par rapport a la face opposee
        base = base - base.mean(0) + centre
        if nf:
            raise ValueError
        X[:] = base
    else:
        for j in range(nf, N):
            todo = np.ones((C, T), bool)
            while todo.any():
                m = int(todo.sum())
                p = rng.uniform(-R, R, (m, 3))
                good = (p ** 2).sum(1) <= R * R
                p = p + centre
                if j:
                    d = np.linalg.norm(X[todo][:, :j] - p[:, None], axis=2)
                    good &= (d >= 1).all(1)
                idx = np.argwhere(todo)
                X[idx[good, 0], idx[good, 1], j] = p[good]
                todo[idx[good, 0], idx[good, 1]] = False
    ci, ti = np.meshgrid(np.arange(C), np.arange(T), indexing='ij')
    pairs = list(itertools.combinations(range(N), 2))
    quads = list(itertools.combinations(range(N), 4))

    def contacts(Y):
        D = np.linalg.norm(Y[:, :, :, None] - Y[:, :, None], axis=4)
        return D

    D = contacts(X)
    iu = np.triu_indices(N, 1)
    assert (D[:, :, iu[0], iu[1]] >= 1 - 1e-12).all() or nf      # (les fixes sont a distance 1 exactement)
    k = (D[:, :, iu[0], iu[1]] <= RC).sum(2)
    sig = np.array([0.05, 0.18, 0.5])
    n_mes = 0
    s_k4 = np.zeros((C, T)); s_2k4 = np.zeros((C, T)); s_9 = np.zeros((C, T)); s_k = np.zeros((C, T)); acc = 0; ech = 0; nech = 0
    eps = EPS[None, :]
    for step in range(pas):
        j = rng.integers(nf, N, (C, T))
        prop = X[ci, ti, j] + sig[rng.integers(0, 3, (C, T))][..., None] * rng.standard_normal((C, T, 3))
        dn = np.linalg.norm(X - prop[:, :, None], axis=3)                       # distances du point propose a tous
        dn[ci, ti, j] = 9.0
        ok = (dn >= 1).all(2) & (((prop - centre) ** 2).sum(2) <= R * R)
        do = np.linalg.norm(X - X[ci, ti, j][:, :, None], axis=3); do[ci, ti, j] = 9.0
        dk = (dn <= RC).sum(2) - (do <= RC).sum(2)
        ok &= rng.random((C, T)) < np.exp(np.minimum(0.0, eps * dk))
        X[ci[ok], ti[ok], j[ok]] = prop[ok]; k = k + dk * ok; acc += ok.mean()
        if step % 10 == 9:                                                       # echanges entre epsilons voisins
            for t0 in range((step // 10) % 2, T - 1, 2):
                a = np.exp(np.minimum(0.0, (EPS[t0] - EPS[t0 + 1]) * (k[:, t0 + 1] - k[:, t0])))
                sw = rng.random(C) < a
                X[sw, t0], X[sw, t0 + 1] = X[sw, t0 + 1].copy(), X[sw, t0].copy()
                k[sw, t0], k[sw, t0 + 1] = k[sw, t0 + 1].copy(), k[sw, t0].copy()
                ech += sw.mean(); nech += 1
        if step >= rodage and step % 20 == 19:
            D = contacts(X); Cc = D <= RC
            nk4 = np.zeros((C, T))
            for q in quads:
                nk4 += np.all([Cc[:, :, a, b] for a, b in itertools.combinations(q, 2)], axis=0)
            kk = Cc[:, :, iu[0], iu[1]].sum(2)
            assert (kk == k).all()
            s_k4 += nk4 >= 1; s_2k4 += nk4 >= 2; s_9 += kk == 9; s_k += kk; n_mes += 1
    Dfin = contacts(X)[:, :, iu[0], iu[1]]
    res = dict(N=N, R=R, depart=depart, chaines=C, pas=pas, mesures=n_mes, acceptation=float(acc / pas), echanges=float(ech / max(1, nech)),
               violations=int((Dfin < 1 - 1e-9).sum()) if not nf else None)
    for t, e in enumerate(EPS):
        f = s_k4[:, t] / n_mes
        res[f'eps={int(e)}'] = dict(K4=float(f.mean()), erreur=float(f.std(ddof=1) / math.sqrt(C)), deux_K4=float((s_2k4[:, t] / n_mes).mean()), erreur_deux_K4=float((s_2k4[:, t] / n_mes).std(ddof=1) / math.sqrt(C)),
                                    neuf_contacts=float((s_9[:, t] / n_mes).mean()), contacts_moyens=float((s_k[:, t] / n_mes).mean()),
                                    chaines_avec_K4=float((s_k4[:, t] > 0).mean()))
    return res


if __name__ == '__main__':
    for R in (1.8, 2.3):
        out[f'M1_A3_R={R}'] = quadrature(TRI, R); print('M1 A3', R, json.dumps(out[f'M1_A3_R={R}']), flush=True)
        out[f'M1_A4_R={R}'] = quadrature(TET, R); print('M1 A4', R, json.dumps(out[f'M1_A4_R={R}']), flush=True)
    for R in (1.8, 2.3):
        out[f'M2_A3_R={R}'] = moteur(4, R, fixes=TRI, seed=1); print('M2 A3', R, json.dumps(out[f'M2_A3_R={R}']), flush=True)
        for N in (4, 5):
            for dep in ('aleatoire', 'compact'):
                key = f'M2_F{N}_R={R}_{dep}'
                out[key] = moteur(N, R, depart=dep, seed=10 * N + (dep == 'compact')); print(key, json.dumps(out[key]), flush=True)
    json.dump(out, open('bps2c.json', 'w'), indent=1)
