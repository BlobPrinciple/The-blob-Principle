# T4 : comparateur connu (Maubach 3,2,1, tétraèdre ordonné) — mêmes mesures : degré maximal, distances entre fondateurs, ratio d_med / V^(1/3)
import sys, itertools
from statistics import median
from collections import deque
sys.argv=['x','none']
import c137c
ID=(0,1,2,3); cells=[tuple(c137c.E)]
for g in range(1,16):
    cells=c137c.step(cells,(3,2,1)[(g-1)%3],ID,ID)
    if g%3==0:
        N={}
        for x in cells:
            for a,b in itertools.combinations(x,2): N.setdefault(a,set()).add(b); N.setdefault(b,set()).add(a)
        dist=[]
        for i in range(4):
            d={c137c.E[i]:0}; q=deque([c137c.E[i]])
            while q:
                u=q.popleft()
                for v in N[u]:
                    if v not in d: d[v]=d[u]+1; q.append(v)
            dist+= [d[c137c.E[j]] for j in range(i+1,4)]
        deg=sorted(len(s) for s in N.values()); V=len(N)
        print(f"g={g} cellules={len(cells)} V={V} deg max/med/q95={deg[-1]}/{median(deg)}/{deg[int(0.95*(V-1))]} distances={dist} ratio={median(dist)/V**(1/3):.3f}",flush=True)
