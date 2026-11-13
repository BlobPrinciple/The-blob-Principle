# C-137c / PR-1 : (i) prolongement DECLARE HORS PROTOCOLE des quatre classes conformes, etendues et a degre stable jusqu'a la generation 15 (32 768 cellules) ;
#                 (ii) phase 4 du protocole : construction ordonnee analogue en dimensions 2 et 4 (dimension 3 en temoin).
import json, itertools, sys
from fractions import Fraction as Fr
from c137c import E, step, sane
def graph(cells):
    N={}
    for x in cells:
        for a,b in itertools.combinations(x,2): N.setdefault(a,set()).add(b); N.setdefault(b,set()).add(a)
    return N
def bfs(N,s):
    d={s:0}; q=[s]
    for u in q:
        for v in N[u]:
            if v not in d: d[v]=d[u]+1; q.append(v)
    return d
res=json.load(open('c137c_phase2.json')); want={}
for r in res:
    p=r['pal']['12']; key=(tuple(p['comptes']),p['degmax'],tuple(p['fondateurs']))
    if p['degmax']==r['pal']['9']['degmax'] and min(p['fondateurs'])>=8: want.setdefault(key,r['rule'])
print('(i) prolongement à la génération 15 :')
for key,rule in want.items():
    w,p1,p2=tuple(rule[0]),tuple(rule[1]),tuple(rule[2]); cells=[tuple(E)]; ok=True
    for g in range(1,16):
        cells=step(cells,w[(g-1)%3],p1,p2)
        if cells is None: ok=False; print('   règle',rule,': choix incompatibles à la génération',g); break
        if g in (12,15):
            N=graph(cells); fd=sorted(bfs(N,E[i])[E[j]] for i,j in itertools.combinations(range(4),2)); print(f'   règle {rule} g={g} : {len(cells)} cellules, {len(N)} porteurs, degré max {max(len(v) for v in N.values())}, distances entre fondateurs {fd}',flush=True)
print('(ii) phase 4 : règle ordonnée en dimension n (battement n, n-1, ..., 1 ; fil x0-x_d ; filles (x0..x_{d-1}, z, ..) et (x1..x_d, z, ..))')
for n,gmax in ((2,12),(3,12),(4,12)):
    V=[tuple(Fr(int(i==j)) for j in range(n+1)) for i in range(n+1)]; cells=[tuple(V)]; born={v:0 for v in V}; ok=True
    for g in range(1,gmax+1):
        d=n-((g-1)%n); des=[frozenset((x[0],x[d])) for x in cells]; D=set(des)
        if any(f in D and f!=e for x,e in zip(cells,des) for f in map(frozenset,itertools.combinations(x,2))): ok=False; print(f'   n={n} : choix incompatibles à la génération {g}'); break
        new=[]
        for x in cells:
            z=tuple((x[0][i]+x[d][i])/2 for i in range(n+1)); born.setdefault(z,g); new.append(x[:d]+(z,)+x[d+1:]); new.append(x[1:d+1]+(z,)+x[d+1:])
        cells=new
        if g%n==0:
            F={}
            for x in cells:
                for f in itertools.combinations(sorted(x),n): F[f]=F.get(f,0)+1
            N=graph(cells); cls={v:(born[v]-(g-n) if born[v]>g-n else 0) for v in N}; same=sum(1 for a in N for b in N[a] if a<b and cls[a]==cls[b]); rainbow=all(sorted(cls[v] for v in x)==list(range(n+1)) for x in cells)
            fd=sorted(set(bfs(N,V[i])[V[j]] for i,j in itertools.combinations(range(n+1),2)))
            print(f'   n={n} g={g:2d} : {len(cells):5d} cellules, {len(N):4d} porteurs, conforme, facettes dans plus de deux cellules {sum(v>2 for v in F.values())}, degré max {max(len(v) for v in N.values())}, fils entre même classe d\'âge {same}, {n+1} classes par cellule {rainbow}, distances entre fondateurs {fd}',flush=True)
