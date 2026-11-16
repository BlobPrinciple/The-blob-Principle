#!/usr/bin/env python3
"""C-190c -- contre-calcul independant du C-190 de ChatGPT (Claude, 16 novembre 2026) : phase sigma de Frank-Kasper (30 sites par maille quadratique, groupe P4_2/mnm n 136),
positions de la page softqc.wordpress.com/sigma (controlee), aucun potentiel. Positions equivalentes ecrites a la main d'apres les positions de Wyckoff 8i, 8j, 4f, 2b (pas de bibliotheque).
Meme detecteur que c189dc.py. AJOUT de Claude : balayage du seuil q de 1,10 a 1,70 pour chercher un plateau. Predictions : c190c_prediction.txt. Usage : python3 c190c.py -> c190c.json"""
import itertools, json, math
import numpy as np
from scipy.spatial import cKDTree

DS = 2 * math.pi / math.acos(1 / 3); CA = 131 / 253
h = 0.5
W8i = lambda x, y: [(x, y, 0), (-x, -y, 0), (-y + h, x + h, h), (y + h, -x + h, h), (-x + h, y + h, h), (x + h, -y + h, h), (y, x, 0), (-y, -x, 0)]
W8j = lambda x, z: [(x, x, z), (-x, -x, z), (-x + h, x + h, z + h), (x + h, -x + h, z + h), (-x + h, x + h, -z + h), (x + h, -x + h, -z + h), (x, x, -z), (-x, -x, -z)]
W4f = lambda x: [(x, x, 0), (-x, -x, 0), (-x + h, x + h, h), (x + h, -x + h, h)]
SITES = [('Z12', W8i(0.571, 0.243)), ('Z12', [(0, 0, h), (h, h, 0)]), ('Z14', W8i(0.371, 0.031)), ('Z14', W8j(0.319, 0.75)), ('Z15', W4f(0.104))]


def base():
    B = []; T = []
    for nom, L in SITES:
        u = sorted(set(tuple(round(c % 1, 9) % 1 for c in p) for p in L)); B += u; T += [nom] * len(u)
    return np.array(B), T, [len(set(tuple(round(c % 1, 9) % 1 for c in p) for p in L)) for _, L in SITES]


def mesure(q, R=2, detail=False):
    B, T, _ = base(); S = np.array([1, 1, CA]); cells = list(itertools.product(range(-R, R + 1), repeat=3))
    F = np.array([b + np.array(c) for c in cells for b in B]); typ = [t for c in cells for t in T]; P = F * S; tr = cKDTree(P)
    dmin = tr.query(P, k=2)[0][:, 1].min(); seuil = q * dmin + 1e-11; A = [set() for _ in P]
    for i, j in tr.query_pairs(seuil): A[i].add(j); A[j].add(i)
    dans = lambda f: bool(np.all(f >= -1e-9) and np.all(f < 1 - 1e-9))
    liens = {}; ent = {}; six = {}
    for i in range(len(P)):
        for j in A[i]:
            if j < i or not dans((F[i] + F[j]) / 2): continue
            com = A[i] & A[j]; adj = {c: com & A[c] for c in com}; k = sum(len(v) for v in adj.values()) // 2; liens[(i, j)] = k
            if k >= 3 and all(len(adj[c]) == 2 for c in com):
                c0 = next(iter(com)); vu = {c0}; pile = [c0]
                while pile:
                    x = pile.pop()
                    for y in adj[x]:
                        if y not in vu: vu.add(y); pile.append(y)
                if len(vu) == len(com):
                    ent[(i, j)] = k
                    if k == 6: cle = '-'.join(sorted((typ[i], typ[j]))); six[cle] = six.get(cle, 0) + 1
    nt = 0; vol = 0.0; surch = 0
    for i in range(len(P)):
        if not np.all(np.abs(F[i] - 0.5) < 1.6): continue
        for j in A[i]:
            if j < i: continue
            for k in A[i] & A[j]:
                if k < j: continue
                quat = A[i] & A[j] & A[k]
                if dans((F[i] + F[j] + F[k]) / 3) and len(quat) > 2: surch += 1
                for l in quat:
                    if l > k and dans((F[i] + F[j] + F[k] + F[l]) / 4):
                        v = abs(np.dot(P[j] - P[i], np.cross(P[k] - P[i], P[l] - P[i]))) / 6
                        if v > 1e-12: nt += 1; vol += v
    v = sorted(ent.values()); coord = {}
    for i in range(len(P)):
        if dans(F[i]): coord.setdefault(typ[i], []).append(len(A[i]))
    r = dict(q=round(q, 3), d_min=float(dmin), liens=len(liens), tetraedres=nt, volume_sur_maille=vol / CA, liens_entoures=len(v), distribution={int(k): v.count(k) for k in sorted(set(v))}, moyenne=(float(np.mean(v)) if v else None),
             n_e_de_tous_les_liens={int(k): list(liens.values()).count(k) for k in sorted(set(liens.values()))}, faces_surchargees=surch, coordination={k: sorted(set(x)) for k, x in coord.items()}, six_par_types=six, rayon=R)
    if detail:
        d = sorted(set(np.round(tr.query(P[:30 * 1 + 0], k=40)[0].ravel() / dmin, 3).tolist())); r['distances_sur_d_min'] = [x for x in d if 0 < x < 1.8]
    return r


if __name__ == '__main__':
    B, T, n = base(); out = dict(sites=n, total=len(B), d_etoile=DS, primaire=[mesure(1.30, detail=True), mesure(1.25), mesure(1.35), mesure(1.30, R=1)], balayage=[])
    print('sites', n, len(B)); print('distances/dmin', out['primaire'][0]['distances_sur_d_min'])
    for m in out['primaire']: print('q', m['q'], 'R', m['rayon'], 'liens', m['liens'], 'tetra', m['tetraedres'], 'vol %.6f' % m['volume_sur_maille'], 'entoures', m['liens_entoures'], m['distribution'], 'moy', m['moyenne'], 'tous', m['n_e_de_tous_les_liens'], 'surch', m['faces_surchargees'], m['coordination'], m['six_par_types'], flush=True)
    for q in np.arange(1.10, 1.701, 0.02):
        m = mesure(float(q), R=1); out['balayage'].append(m); print('balayage q %.2f' % q, m['liens'], m['tetraedres'], '%.4f' % m['volume_sur_maille'], m['liens_entoures'], m['distribution'], m['faces_surchargees'], flush=True)
    json.dump(out, open('c190c.json', 'w'), indent=1)
