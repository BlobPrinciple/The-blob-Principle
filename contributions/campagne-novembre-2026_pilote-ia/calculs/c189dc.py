#!/usr/bin/env python3
"""C-189Dc -- contre-calcul independant du C-189D de ChatGPT (Claude, 16 novembre 2026) : temoin positif cristallographique. Aucun potentiel, aucun terme du Blob : positions publiees,
puis la meme mesure que c189c.py (lien si distance <= q fois la plus petite distance, q = 1,30 ; 1,25 ; 1,35 ; tetraedre = clique de 4 ; lien entoure = sommets opposes en un seul cycle).
 A15 (Cr3Si, cP8, Pm-3n n 223) et temoin negatif cubique a faces centrees : protocole de ChatGPT (lu seul avant le scelle).
 C15 (Cu2Mg, phase de Laves cubique, cF24, Fd-3m n 227) : AJOUT de Claude, meme mesure.
Positions controlees sur www.atomic-scale-physics.de/lattice/struk/a15.html et c15.html. Predictions : c189dc_prediction.txt.  Usage : python3 c189dc.py -> c189dc.json"""
import itertools, json, math
import numpy as np
from scipy.spatial import cKDTree

DS = 2 * math.pi / math.acos(1 / 3)
A15 = [(0, 0, 0), (.5, .5, .5), (.25, .5, 0), (.75, .5, 0), (0, .25, .5), (0, .75, .5), (.5, 0, .25), (.5, 0, .75)]
FCC = [(0, 0, 0), (0, .5, .5), (.5, 0, .5), (.5, .5, 0)]
C15 = [tuple(np.add(b, t) % 1) for t in FCC for b in [(1 / 8,) * 3, (7 / 8,) * 3, (.5, .5, .5), (.5, .25, .25), (.25, .5, .25), (.25, .25, .5)]]


def mesure(base, q, R=2):
    base = np.array(base, float); P = np.array([b + np.array(c) for c in itertools.product(range(-R, R + 1), repeat=3) for b in base]); tr = cKDTree(P)
    dmin = min(d for d in tr.query(P[:len(base) * 3], k=2)[0][:, 1]); seuil = q * dmin + 1e-11
    A = [set() for _ in P]
    for i, j in tr.query_pairs(seuil): A[i].add(j); A[j].add(i)
    dans = lambda x: bool(np.all(x >= -1e-9) and np.all(x < 1 - 1e-9))
    liens = {}; ent = {}; long_par_ne = {}
    for i in range(len(P)):
        for j in A[i]:
            if j < i or not dans((P[i] + P[j]) / 2): continue
            com = A[i] & A[j]; adj = {c: com & A[c] for c in com}; k = sum(len(v) for v in adj.values()) // 2; liens[(i, j)] = k
            if k >= 3 and all(len(adj[c]) == 2 for c in com):
                c0 = next(iter(com)); vu = {c0}; pile = [c0]
                while pile:
                    x = pile.pop()
                    for y in adj[x]:
                        if y not in vu: vu.add(y); pile.append(y)
                if len(vu) == len(com): ent[(i, j)] = k; long_par_ne.setdefault(k, set()).add(round(float(np.linalg.norm(P[i] - P[j])), 6))
    tets = set(); surch = 0; vol = 0.0
    for i in range(len(P)):
        if not np.all(np.abs(P[i] - 0.5) < 1.6): continue
        for j in A[i]:
            if j < i: continue
            for k in A[i] & A[j]:
                if k < j: continue
                quat = [l for l in A[i] & A[j] & A[k]]
                if dans((P[i] + P[j] + P[k]) / 3) and len(quat) > 2: surch += 1
                for l in quat:
                    if l > k and dans((P[i] + P[j] + P[k] + P[l]) / 4):
                        v = abs(np.dot(P[j] - P[i], np.cross(P[k] - P[i], P[l] - P[i]))) / 6
                        if v > 1e-12: tets.add((i, j, k, l)); vol += v
    v = sorted(ent.values()); h = {int(k): v.count(k) for k in sorted(set(v))}; coord = np.mean([len(A[i]) for i in range(len(P)) if dans(P[i])])
    return dict(q=q, d_min=float(dmin), atomes_par_maille=len(base), coordination_moyenne=float(coord), liens_par_maille=len(liens), tetraedres_par_maille=len(tets), volume_des_tetraedres=vol, liens_entoures=len(v), distribution=h,
                moyenne=(float(np.mean(v)) if v else None), part_six=(v.count(6) / len(v) if v else None), ecart_a_d_etoile=(float(np.mean(v)) - DS if v else None), longueurs_par_n_e={int(k): sorted(x) for k, x in long_par_ne.items()},
                n_e_de_tous_les_liens={int(k): list(liens.values()).count(k) for k in sorted(set(liens.values()))}, faces_surchargees=surch, rayon_super_reseau=R)


if __name__ == '__main__':
    out = {}
    for nom, base in (('A15', A15), ('CFC', FCC), ('C15', C15)):
        out[nom] = [mesure(base, q) for q in (1.30, 1.25, 1.35)] + [mesure(base, 1.30, R=1)]
        for m in out[nom]: print(nom, 'q', m['q'], 'R', m['rayon_super_reseau'], 'Z %.4f' % m['coordination_moyenne'], 'liens', m['liens_par_maille'], 'tetra', m['tetraedres_par_maille'], 'vol %.9f' % m['volume_des_tetraedres'], 'entoures', m['liens_entoures'], m['distribution'],
                                   'moy', m['moyenne'], 'ecart d*', m['ecart_a_d_etoile'], 'long', m['longueurs_par_n_e'], 'tous', m['n_e_de_tous_les_liens'], 'surch', m['faces_surchargees'], flush=True)
    json.dump(out, open('c189dc.json', 'w'), indent=1)
