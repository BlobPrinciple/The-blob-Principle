#!/usr/bin/env python3
"""C-211c, COMPLEMENT APRES LECTURE de la note et de la passation de ChatGPT (declare) : (1) son temoin a parent p(n) = valuation 2-adique de n ;
(2) noyau existentiel contre noyau universel sur un exemple de mon choix. Ecrit sans ouvrir verification_c211.py. Claude, 18 novembre 2026."""
import itertools, json
def v2(n):
    k = 0
    while n % 2 == 0: n //= 2; k += 1
    return k
def k4(E, N):
    A = {i: set() for i in range(N)}
    for u, v in E: A[u].add(v); A[v].add(u)
    return sum(1 for q in itertools.combinations(range(N), 4) if all(b in A[a] for a, b in itertools.combinations(q, 2))) if N <= 64 else \
           sum(1 for u, v in E for w in A[u] & A[v] if w > max(u, v) for x in A[u] & A[v] & A[w] if x > w)
out = dict(temoin=[])
for N in (4, 8, 128, 256):
    EA = {(min(n, v2(n)), max(n, v2(n))) for n in range(1, N)}; EB = EA | {(0, 2), (1, 3), (2, 3)}
    par = {i: sum(1 for n in range(1, N) if v2(n) == i) for i in range(4)}
    out['temoin'].append(dict(N=N, parent_toujours_plus_ancien=all(v2(n) < n for n in range(1, N)), aretes_A=len(EA), arbre_A=(len(EA) == N - 1), K4_A=k4(EA, N), aretes_B=len(EB), K4_B=k4(EB, N), naissances_des_parents_0_a_3=par))
succ = {'origine': ['boucle', 'impasse'], 'boucle': ['boucle'], 'impasse': []}
def noyau(succ, tous):
    K = set(succ)
    while True:
        M = {s for s in K if not succ[s] or (not set(succ[s]) <= K if tous else not set(succ[s]) & K)}
        if not M: return sorted(K)
        K -= M
out['existentiel'] = noyau(succ, False); out['universel'] = noyau(succ, True)
json.dump(out, open('c211c_complement.json', 'w'), indent=1); print(json.dumps(out))
