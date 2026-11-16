#!/usr/bin/env python3
"""C-184c -- contre-calcul independant du C-184 de ChatGPT (Claude, 16 novembre 2026) : tetraedres reguliers accoles face a face HORS GRILLE, 64 naissances, bras R (face admissible
au hasard) et bras A (face dont le nouvel apex a le plus de sommets anciens a moins de 0,15). Ecrit d'apres son seul PROTOCOLE FIGE ; resultats non lus avant le scelle de
c184c_prediction.txt. Hypothese d'auditeur de ChatGPT, pas une loi du Blob. Usage : python3 c184c.py <R|A> <graine>  -> c184c_<bras>_<graine>.json"""
import itertools, json, math, sys
import numpy as np
from scipy.spatial import ConvexHull
from c182c import chevauche, faces, VREF, H

RC = math.sqrt(6) / 4; EPS = 0.15


def etat(X, T):
    Xa = np.array(X); F = faces(T); B = sum(1 for v in F.values() if len(v) == 1); Ni = sum(1 for v in F.values() if len(v) == 2); E = {}
    for t in T:
        for e in itertools.combinations(sorted(t), 2): E[e] = E.get(e, 0) + 1
    bord = set(e for f, v in F.items() if len(v) == 1 for e in itertools.combinations(f, 2)); L = np.array([np.linalg.norm(Xa[a] - Xa[b]) for a, b in E])
    return dict(N=len(T), sommets=len(X), B=B, C_dual=Ni - len(T) + 1, aretes_interieures=sum(1 for e in E if e not in bord), faces_a_plus_de_2=sum(1 for v in F.values() if len(v) > 2), cellules_par_arete_max=max(E.values()),
                aretes_a_5_cellules=sum(1 for v in E.values() if v == 5), aretes_a_4_cellules=sum(1 for v in E.values() if v == 4), E_U=float((0.5 * (L - 1) ** 2).sum()), ecart_longueur_max=float(abs(L - 1).max()),
                densite=float(len(T) * VREF / ConvexHull(Xa).volume), V_enveloppe=float(ConvexHull(Xa).volume), B_sur_N=B / len(T))


def trajectoire(bras, seed, naissances=64, jalons=(16, 32, 48, 65)):
    rng = np.random.Generator(np.random.PCG64(seed))
    X = [np.array([0., 0, 0]), np.array([1., 0, 0]), np.array([.5, math.sqrt(3) / 2, 0]), np.array([.5, math.sqrt(3) / 6, H])]; T = [(0, 1, 2, 3)]
    out = dict(bras=bras, graine=seed, jalons=[], Q_choisis=[], rejets_collision=0, rejets_doublon=0, distances_proches=[], stop=None)
    for m in range(1, naissances + 1):
        F = faces(T); bord = sorted(f for f, v in F.items() if len(v) == 1); Xa = np.array(X); cen = np.array([Xa[list(t)].mean(axis=0) for t in T]); cand = []
        for f in bord:
            t = F[f][0]; d = (set(t) - set(f)).pop(); a, b, c = f; n = np.cross(X[b] - X[a], X[c] - X[a]); n /= np.linalg.norm(n)
            if np.dot(X[d] - X[a], n) > 0: n = -n
            q = (X[a] + X[b] + X[c]) / 3 + H * n; dist = np.linalg.norm(Xa - q, axis=1)
            if dist.min() < 1e-8: out['rejets_doublon'] += 1; continue
            Qt = np.array([X[a], X[b], X[c], q]); cq = Qt.mean(axis=0); proches = np.nonzero(np.linalg.norm(cen - cq, axis=1) <= 2 * RC + 1e-9)[0]
            if any(chevauche(Xa[list(T[i])], Qt) for i in proches): out['rejets_collision'] += 1; continue
            pr = [float(dist[i]) for i in range(len(X)) if i not in f and dist[i] <= EPS]; cand.append((f, q, len(pr), pr))
        if not cand: out['stop'] = m; break
        if bras == 'A': qm = max(c[2] for c in cand); cand = [c for c in cand if c[2] == qm]
        f, q, Q, pr = cand[int(rng.integers(len(cand)))]
        X.append(q); T.append(tuple(sorted(f + (len(X) - 1,)))); out['Q_choisis'].append(Q); out['distances_proches'] += pr
        if len(T) in jalons: out['jalons'].append(etat(X, T))
    chev = sum(1 for t1, t2 in itertools.combinations(T, 2) if np.linalg.norm(np.array(X)[list(t1)].mean(axis=0) - np.array(X)[list(t2)].mean(axis=0)) <= 2 * RC and chevauche(np.array(X)[list(t1)], np.array(X)[list(t2)]))
    out.update(naissances_reussies=len(T) - 1, naissances_Q_positif=sum(1 for x in out['Q_choisis'] if x > 0), Q_total=sum(out['Q_choisis']), chevauchements_finaux=chev, final=etat(X, T))
    return out


if __name__ == '__main__':
    bras, seed = sys.argv[1], int(sys.argv[2]); r = trajectoire(bras, seed); json.dump(r, open(f'c184c_{bras}_{seed}.json', 'w')); f = r['final']
    print(bras, seed, 'naiss', r['naissances_reussies'], 'Q>0', r['naissances_Q_positif'], 'Qtot', r['Q_total'], 'B', f['B'], 'C', f['C_dual'], 'int', f['aretes_interieures'], 'f>2', f['faces_a_plus_de_2'], 'chev', r['chevauchements_finaux'],
          'E_U %.1e' % f['E_U'], 'max/arete', f['cellules_par_arete_max'], 'a5', f['aretes_a_5_cellules'], 'densite %.4f' % f['densite'], 'rejets', r['rejets_collision'], r['rejets_doublon'], 'dmin %.5f' % (min(r['distances_proches']) if r['distances_proches'] else float('nan')), flush=True)
