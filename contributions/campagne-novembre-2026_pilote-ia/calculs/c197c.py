#!/usr/bin/env python3
"""C-197c -- contre-calcul independant du C-197 de ChatGPT (Claude, 17 novembre 2026), d'apres son seul PROTOCOLE SCELLE : croissance d'un graphe par naissances (p), contacts avec les voisins du
parent (q), fermeture de chemins de longueur deux (eta), rupture selon l'age. Generateur = hypothese d'AUDITEUR de ChatGPT. L'ordre fin des tirages n'est pas fixe par le protocole : accord statistique vise.
Predictions : c197c_prediction.txt. Usage : python3 c197c.py -> c197c.json"""
import itertools, json
from collections import Counter
import numpy as np

BRAS = dict(A=(0.28, 0, 0, False, 99), B=(0.28, 0.28, 0.16, False, 99), C=(0.28, 0.28, 0.16, True, 99), D=(0.28, 0, 0, True, 99), E=(0.28, 0.28, 0.16, True, 14))

def composantes(A, S=None):
    S = set(A) if S is None else S; vu = set(); out = []
    for s in sorted(S):
        if s in vu: continue
        pile = [s]; vu.add(s); c = [s]
        while pile:
            x = pile.pop()
            for y in A[x]:
                if y in S and y not in vu: vu.add(y); pile.append(y); c.append(y)
        out.append(c)
    return out

def poches(A):
    deg = {v: len(A[v]) for v in A}; S = set(A); pile = [v for v in S if deg[v] < 2]
    while pile:
        v = pile.pop()
        if v not in S: continue
        S.discard(v)
        for w in A[v]:
            if w in S:
                deg[w] -= 1
                if deg[w] < 2: pile.append(w)
    out = []
    for c in composantes(A, S):
        if len(c) >= 4:
            cs = set(c)
            if any((A[u] & A[w] & cs) for u in c for w in A[u] if w > u and w in cs): out.append(len(c))
    return sorted(out, reverse=True)

def mesure(A, N):
    E = sum(len(a) for a in A.values()) // 2; C = composantes(A); tri = sum(len(A[u] & A[w]) for u in A for w in A[u] if w > u) // 3
    deg = sorted(((len(A[v]), -v) for v in A), reverse=True); rang0 = 1 + sum(1 for v in A if len(A[v]) > len(A[0]))
    return dict(N=N, E=E, composantes=len(C), geante=max(len(c) for c in C), isoles=sum(1 for c in C if len(c) == 1), triangles=tri, b1=E - N + len(C), degre_racine=len(A[0]), degre_max=deg[0][0], rang_racine=rang0, poches=poches(A))

def k4(A):
    T = [(i, j, k, l) for i in A for j in A[i] if j > i for k in A[i] & A[j] if k > j for l in A[i] & A[j] & A[k] if l > k]; F = Counter(f for t in T for f in itertools.combinations(t, 3))
    return len(T), sum(1 for v in F.values() if v >= 3)

def simule(seed, bras):
    p, q, eta, rupt, tfin = BRAS[bras]; rn = np.random.default_rng(seed); rc = np.random.default_rng(seed + 2000000); rr = np.random.default_rng(seed + 3000000)
    A = {0: set()}; ne = {}; N = 1; out = dict(etats={}, pas=[]); decroit = False; cprec = 1
    def ajoute(u, w, t):
        cree = len(A[u] & A[w]); A[u].add(w); A[w].add(u); ne[(min(u, w), max(u, w))] = t; return cree
    for t in range(1, 29):
        cre = det = aj = sup = 0
        if rupt:
            for (u, w) in sorted(ne):
                a = t - ne[(u, w)]
                if a >= 1 and rr.random() < (0.055 if a < 6 else 0.14): det += len(A[u] & A[w]); A[u].discard(w); A[w].discard(u); del ne[(u, w)]; sup += 1
        nes = []
        if t <= tfin:
            tir = rn.random(N)
            for v in range(N):
                if tir[v] < p: nes.append((N, v)); N += 1
        for c, v in nes: A[c] = set()
        for c, v in nes: cre += ajoute(c, v, t); aj += 1
        if q:
            for c, v in nes:
                vo = sorted(A[v] - {c})
                if vo:
                    ch = rc.choice(len(vo), size=min(4, len(vo)), replace=False)
                    for i in ch:
                        if rc.random() < q and vo[i] not in A[c]: cre += ajoute(c, vo[i], t); aj += 1
        if eta:
            for u in range(N):
                if rc.random() < eta and A[u]:
                    vo = sorted(A[u]); v = vo[int(rc.integers(len(vo)))]; vw = sorted(A[v]); w = vw[int(rc.integers(len(vw)))]
                    if w != u and w not in A[u]: cre += ajoute(u, w, t); aj += 1
        nc = len(composantes(A)); decroit |= nc < cprec; cprec = nc
        out['pas'].append(dict(t=t, N=N, triangles_crees=cre, triangles_detruits=det, aretes_ajoutees=aj, aretes_rompues=sup, composantes=nc))
        if t in (8, 12, 14, 16, 20, 24, 28): out['etats'][t] = mesure(A, N)
    out['K4'], out['faces_surchargees'] = k4(A); out['composantes_ont_diminue'] = bool(decroit); return out

if __name__ == '__main__':
    res = {b: {} for b in BRAS}
    for s in range(197000, 197012):
        for b in BRAS: res[b][s] = simule(s, b)
        f = {b: res[b][s]['etats'][28] for b in BRAS}
        print(s, '| N', [f[b]['N'] for b in 'ABCDE'], '| A arbre', all(e['E'] == e['N'] - 1 and e['triangles'] == 0 for e in res['A'][s]['etats'].values()), '| B comp', f['B']['composantes'], 'tri', f['B']['triangles'], 'K4', res['B'][s]['K4'], 'surch', res['B'][s]['faces_surchargees'], 'rang racine', f['B']['rang_racine'],
              '| C E', f['C']['E'], 'comp', f['C']['composantes'], 'geante', f['C']['geante'], 'isoles', f['C']['isoles'], 'tri', f['C']['triangles'], 'K4', res['C'][s]['K4'], 'surch', res['C'][s]['faces_surchargees'], 'poches', f['C']['poches'][:6], len(f['C']['poches']), 'rang racine', f['C']['rang_racine'], 'deg', f['C']['degre_racine'], '/', f['C']['degre_max'],
              '| pas tardifs crees+detruits', sum(1 for x in res['C'][s]['pas'] if x['t'] >= 15 and x['triangles_crees'] and x['triangles_detruits']), '| D poches', len(f['D']['poches']), 'comp', f['D']['composantes'], '| E N14', res['E'][s]['etats'][14]['N'], 'aretes + / - apres 14 :', sum(x['aretes_ajoutees'] for x in res['E'][s]['pas'] if x['t'] > 14), sum(x['aretes_rompues'] for x in res['E'][s]['pas'] if x['t'] > 14), 'poches', len(f['E']['poches']), flush=True)
    G = range(197000, 197012); C = res['C']; B = res['B']
    print('N(28) moyenne %.1f, mediane %d, min %d, max %d' % (np.mean([C[s]['etats'][28]['N'] for s in G]), np.median([C[s]['etats'][28]['N'] for s in G]), min(C[s]['etats'][28]['N'] for s in G), max(C[s]['etats'][28]['N'] for s in G)))
    print('C : triangles', sum(1 for s in G if C[s]['etats'][28]['triangles']), '/12 ; K4', sum(1 for s in G if C[s]['K4']), '/12 ; >= 2 poches', sum(1 for s in G if len(C[s]['etats'][28]['poches']) >= 2), '/12 ; mediane composantes', np.median([C[s]['etats'][28]['composantes'] for s in G]), '; part de N (mediane) %.3f' % np.median([C[s]['etats'][28]['composantes'] / C[s]['etats'][28]['N'] for s in G]),
          '; part geante (mediane) %.3f' % np.median([C[s]['etats'][28]['geante'] / C[s]['etats'][28]['N'] for s in G]), '; composantes ont diminue :', sum(res[b][s]['composantes_ont_diminue'] for b in BRAS for s in G), '; mediane pas tardifs', np.median([sum(1 for x in C[s]['pas'] if x['t'] >= 15 and x['triangles_crees'] and x['triangles_detruits']) for s in G]),
          '; racine de plus grand degre :', sum(1 for s in G if C[s]['etats'][28]['rang_racine'] == 1), '/12 ; surcharges', sum(1 for s in G if C[s]['faces_surchargees']), '/12')
    print('B : une composante', sum(1 for s in G if B[s]['etats'][28]['composantes'] == 1), '/12 ; racine parmi les 3 plus grands degres', sum(1 for s in G if B[s]['etats'][28]['rang_racine'] <= 3), '/12 ; de plus grand degre', sum(1 for s in G if B[s]['etats'][28]['rang_racine'] == 1), '/12 ; surcharges', sum(1 for s in G if B[s]['faces_surchargees']), '/12')
    print('A et D sans poche :', all(not res[b][s]['etats'][28]['poches'] for b in 'AD' for s in G), '| E : N constant apres 14 :', all(res['E'][s]['etats'][28]['N'] == res['E'][s]['etats'][14]['N'] for s in G))
    json.dump(res, open('c197c.json', 'w'))
