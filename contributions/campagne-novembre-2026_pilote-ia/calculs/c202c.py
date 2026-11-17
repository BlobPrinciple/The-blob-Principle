#!/usr/bin/env python3
"""C-202c -- regle decrite au master V346 (XV.8, XV.9) : croissance sommet par sommet pres d'un parent, liaison par proximite dans un terreau, interdiction des cellules de dimension > 3 ;
soumise au critere << spectre de tissu mur >> (volume d'abord). Les valeurs numeriques sont des hypotheses d'AUDITEUR (voir c202c_prediction.txt). (Claude, 17 novembre 2026.)
Usage : python3 c202c.py -> c202c.json"""
import itertools, json
from collections import Counter, defaultdict
import numpy as np

R = 1.30
def croissance(seed, filtre, N=600):
    rng = np.random.default_rng(seed); X = np.zeros((N, 3)); A = [set() for _ in range(N)]; deg150 = None; refus = 0
    for c in range(1, N):
        p = int(rng.integers(0, c)); u = rng.normal(size=3); X[c] = X[p] + u / np.linalg.norm(u); d = np.linalg.norm(X[:c] - X[c], axis=1)
        for w in np.argsort(d):
            if d[w] > R: break
            w = int(w)
            if filtre:
                com = A[c] & A[w]   # un groupe de 5 apparait si 3 voisins communs sont tous lies entre eux
                if any(b in A[a] and e in A[a] and e in A[b] for a, b, e in itertools.combinations(sorted(com), 3)): refus += 1; continue
            A[c].add(w); A[w].add(c)
        if c + 1 == 150: deg150 = sum(len(a) for a in A[:150]) / 150
    return X, A, deg150, refus

def mesure(X, A):
    N = len(A); T = [(i, j, k, l) for i in range(N) for j in A[i] if j > i for k in A[i] & A[j] if k > j for l in A[i] & A[j] & A[k] if l > k]
    vol = [abs(np.linalg.det(X[list(t[1:])] - X[t[0]])) / 6 for t in T]; F = Counter(f for t in T for f in itertools.combinations(t, 3))
    k5 = sum(1 for t in T for m in (A[t[0]] & A[t[1]] & A[t[2]] & A[t[3]]) if m > t[3])
    par = defaultdict(list)
    for t in T:
        for e in itertools.combinations(t, 2): par[e].append(tuple(x for x in t if x not in e))
    anneaux = Counter(); portes = len(par)
    for e, L in par.items():
        dg = Counter(x for p in L for x in p)
        if all(v == 2 for v in dg.values()) and len(dg) == len(L):
            adj = defaultdict(list)
            for a, b in L: adj[a].append(b); adj[b].append(a)
            s = L[0][0]; vu = {s}; pile = [s]
            while pile:
                x = pile.pop()
                for y in adj[x]:
                    if y not in vu: vu.add(y); pile.append(y)
            if len(vu) == len(dg): anneaux[len(L)] += 1
    E = sum(len(a) for a in A) // 2
    return dict(N=N, E=E, voisins_moyens=2 * E / N, cellules=len(T), volume_min=float(min(vol)) if vol else None, cellules_plates=sum(1 for v in vol if v < 1e-9), faces=len(F), faces_surchargees=sum(1 for v in F.values() if v > 2),
                part_surchargee=(sum(1 for v in F.values() if v > 2) / len(F) if F else 0.0), groupes_de_5=k5, liens_portant_une_cellule=portes, anneaux_fermes={int(k): v for k, v in sorted(anneaux.items())},
                part_5_6=((anneaux[5] + anneaux[6]) / portes if portes else 0.0))

if __name__ == '__main__':
    out = {}
    for nom, filtre in (('P', False), ('PV', True)):
        out[nom] = []
        for s in range(202000, 202008):
            X, A, d150, refus = croissance(s, filtre); m = mesure(X, A); m.update(graine=s, voisins_moyens_a_150=d150, liens_refuses=refus); out[nom].append(m)
            print(nom, s, '| voisins', '%.1f' % m['voisins_moyens'], '(a 150 : %.1f)' % d150, '| cellules', m['cellules'], '| faces surchargees', m['faces_surchargees'], '/', m['faces'], '= %.3f' % m['part_surchargee'], '| groupes de 5', m['groupes_de_5'],
                  '| anneaux fermes', m['anneaux_fermes'], '| part 5+6 %.4f' % m['part_5_6'], '| refus', refus, '| volume min %.2e' % (m['volume_min'] or 0), flush=True)
    json.dump(out, open('c202c.json', 'w'), indent=1)
