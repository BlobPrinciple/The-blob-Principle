#!/usr/bin/env python3
"""C-204c -- le moteur de l'auteur (corpus : << blob ablation labo colab.py >>, lignes 1 a 228 executees telles quelles) mesure au critere << spectre de tissu mur >>.
Seuls la taille d'arret, les graines et les mesures finales sont du pilote. (Claude, 17 novembre 2026.) Predictions : c204c_prediction.txt. Usage : python3 c204c.py -> c204c.json"""
import itertools, json, sys, time, hashlib, os
from collections import Counter, defaultdict
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(ICI, '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB', 'Session 30 mai — verrou B et masters V152-V155', 'blob ablation labo colab.py')
brut = open(SRC, 'rb').read(); assert hashlib.sha256(brut).hexdigest() == '9d36fc7a847f7ed92500b7e06a910f49ed12e2b769312e7fad28f2ce13416003'
L = brut.decode('utf-8').split('\n'); fin = next(i for i, l in enumerate(L) if l.startswith('def mesure(')); M = {}; exec('\n'.join(L[:fin]), M); Blob = M['Blob']

def mesure(bl):
    N = bl.N; A = bl.adj; X = np.array(bl.pts); T = M['find_all_K4'](A, N); F = Counter(f for t in T for f in itertools.combinations(sorted(t), 3)); E = sum(len(a) for a in A) // 2
    k5 = sum(1 for t in T for m in (A[t[0]] & A[t[1]] & A[t[2]] & A[t[3]]) if m > max(t)); par = defaultdict(list)
    for t in T:
        t = tuple(sorted(t))
        for e in itertools.combinations(t, 2): par[e].append(tuple(x for x in t if x not in e))
    an = Counter()
    for e, P in par.items():
        dg = Counter(x for p in P for x in p)
        if all(v == 2 for v in dg.values()) and len(dg) == len(P):
            adj = defaultdict(list)
            for a, b in P: adj[a].append(b); adj[b].append(a)
            vu = {P[0][0]}; pile = [P[0][0]]
            while pile:
                x = pile.pop()
                for y in adj[x]:
                    if y not in vu: vu.add(y); pile.append(y)
            if len(vu) == len(dg): an[len(P)] += 1
    vol = [abs(np.linalg.det(X[list(t[1:])] - X[t[0]])) / 6 for t in T]; nf = len(F) or 1; npo = len(par) or 1
    return dict(N=N, E=E, voisins_moyens=2 * E / N, cellules=len(T), groupes_de_5=k5, faces_portantes=len(F), faces_exposees=sum(1 for v in F.values() if v == 1), faces_a_deux=sum(1 for v in F.values() if v == 2), faces_surchargees=sum(1 for v in F.values() if v > 2),
                part_surchargee=sum(1 for v in F.values() if v > 2) / nf, part_exposee=sum(1 for v in F.values() if v == 1) / nf, max_par_face=max(F.values()) if F else 0, liens_portants=len(par), anneaux_fermes={int(k): v for k, v in sorted(an.items())},
                part_5_6=(an[5] + an[6]) / npo, volume_median=float(np.median(vol)) if vol else None, distance_min=float(min(np.linalg.norm(X[i] - X[j]) for i in range(N) for j in A[i] if j > i)))

if __name__ == '__main__':
    cible = int(sys.argv[1]) if len(sys.argv) > 1 else 600; out = []
    for seed in (1, 2, 3, 4):
        t0 = time.time(); bl = Blob(N0=300, seed=seed, forces=("grav", "em", "weak", "bord")); tours = 0
        while bl.N < cible: bl.step(0.12); tours += 1
        m = mesure(bl); m.update(graine=seed, tours=tours, secondes=round(time.time() - t0)); out.append(m)
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()}, flush=True); json.dump(out, open(os.path.join(ICI, 'c204c.json'), 'w'), indent=1)
