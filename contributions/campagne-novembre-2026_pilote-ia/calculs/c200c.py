#!/usr/bin/env python3
"""C-200c -- extension << H >> de C-197 (canal genealogique, hypothese d'AUDITEUR de ChatGPT) dans mon programme c197c : rang de centralite de la racine, bras C contre bras H (Claude, 17 novembre 2026).
Non aveugle (declare dans c200c_prediction.txt). Usage : python3 c200c.py -> c200c.json"""
import json
from collections import deque
import numpy as np
from c197c import composantes

def simule(seed, H):
    p, q, eta = 0.28, 0.28, 0.16; rn = np.random.default_rng(seed); rc = np.random.default_rng(seed + 2000000); rr = np.random.default_rng(seed + 3000000); rh = np.random.default_rng(seed + 4000000)
    A = {0: set()}; G = {0: set()}; ne = {}; N = 1; baisses = 0; cprec = 1; ajoutsH = 0
    def ajoute(u, w, t): A[u].add(w); A[w].add(u); ne[(min(u, w), max(u, w))] = t
    for t in range(1, 29):
        for (u, w) in sorted(ne):
            a = t - ne[(u, w)]
            if a >= 1 and rr.random() < (0.055 if a < 6 else 0.14): A[u].discard(w); A[w].discard(u); del ne[(u, w)]
        nes = []; tir = rn.random(N)
        for v in range(N):
            if tir[v] < p: nes.append((N, v)); N += 1
        for c, v in nes: A[c] = set(); G[c] = set()
        for c, v in nes: ajoute(c, v, t); G[c].add(v); G[v].add(c)
        for c, v in nes:
            vo = sorted(A[v] - {c})
            if vo:
                for i in rc.choice(len(vo), size=min(4, len(vo)), replace=False):
                    if rc.random() < q and vo[i] not in A[c]: ajoute(c, vo[i], t)
        for u in range(N):
            if rc.random() < eta and A[u]:
                vo = sorted(A[u]); v = vo[int(rc.integers(len(vo)))]; vw = sorted(A[v]); w = vw[int(rc.integers(len(vw)))]
                if w != u and w not in A[u]: ajoute(u, w, t)
        if H:
            for u in range(N):
                if rh.random() < 0.12 and G[u]:
                    vo = sorted(G[u]); v = vo[int(rh.integers(len(vo)))]; vw = sorted(G[v] - {u})
                    if vw:
                        w = vw[int(rh.integers(len(vw)))]
                        if w not in A[u]: ajoute(u, w, t); ajoutsH += 1
        nc = len(composantes(A)); baisses += nc < cprec; cprec = nc
    return A, N, baisses, ajoutsH

def harmonique(A, N):
    h = np.zeros(N)
    for s in range(N):
        d = {s: 0}; f = deque([s])
        while f:
            x = f.popleft()
            for y in A[x]:
                if y not in d: d[y] = d[x] + 1; f.append(y)
        h[s] = sum(1 / v for v in d.values() if v)
    return h
def rang_rel(score, v): return float(((score > score[v]).sum() + ((score == score[v]).sum() - 1) / 2) / len(score))

if __name__ == '__main__':
    out = []
    for s in range(197000, 197012):
        r = dict(graine=s)
        for nom, H in (('C', False), ('H', True)):
            A, N, baisses, ajH = simule(s, H); deg = np.array([len(A[v]) for v in range(N)]); har = harmonique(A, N); C = composantes(A); m = N // 2
            r[nom] = dict(N=N, E=int(deg.sum() // 2), composantes=len(C), baisses=baisses, ajouts_H=ajH, degre_racine=int(deg[0]), rang_degre=rang_rel(deg, 0), rang_harmonique=rang_rel(har, 0), composante_racine=len(next(c for c in C if 0 in c)) / N, geante=max(len(c) for c in C) / N,
                          temoin_rang_degre=rang_rel(deg, m), temoin_rang_harmonique=rang_rel(har, m))
        out.append(r); print(s, 'N', r['C']['N'], '| C : comp', r['C']['composantes'], 'deg racine', r['C']['degre_racine'], 'rang deg %.4f' % r['C']['rang_degre'], 'rang harm %.4f' % r['C']['rang_harmonique'], 'comp racine %.2f' % r['C']['composante_racine'],
                             '| H : comp', r['H']['composantes'], 'baisses', r['H']['baisses'], 'deg racine', r['H']['degre_racine'], 'rang deg %.4f' % r['H']['rang_degre'], 'rang harm %.4f' % r['H']['rang_harmonique'], 'comp racine %.2f' % r['H']['composante_racine'], '| temoin H deg %.3f harm %.3f' % (r['H']['temoin_rang_degre'], r['H']['temoin_rang_harmonique']), flush=True)
    md = lambda b, k: float(np.median([r[b][k] for r in out]))
    print('degre : H meilleur que C dans', sum(r['H']['rang_degre'] < r['C']['rang_degre'] for r in out), '/12 ; medianes C %.4f H %.4f' % (md('C', 'rang_degre'), md('H', 'rang_degre')))
    print('harmonique : H meilleur que C dans', sum(r['H']['rang_harmonique'] < r['C']['rang_harmonique'] for r in out), '/12 ; medianes C %.4f H %.4f' % (md('C', 'rang_harmonique'), md('H', 'rang_harmonique')))
    print('composantes : baisses sous H dans', sum(r['H']['baisses'] > 0 for r in out), '/12 ; medianes C %.1f H %.1f' % (md('C', 'composantes'), md('H', 'composantes')), '| temoin H : mediane rang degre %.3f, harmonique %.3f' % (md('H', 'temoin_rang_degre'), md('H', 'temoin_rang_harmonique')))
    json.dump(out, open('c200c.json', 'w'), indent=1)
