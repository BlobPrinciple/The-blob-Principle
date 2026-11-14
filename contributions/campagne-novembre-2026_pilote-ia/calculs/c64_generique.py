import random, itertools, networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
random.seed(11)
def stacked(N):
    tets=[(0,1,2,3)]
    for v in range(4,N):
        t=tets.pop(random.randrange(len(tets)))
        for i in range(4): tets.append(tuple(sorted(tuple(x for j,x in enumerate(t) if j!=i)+(v,))))
    return tets
def a_un_miroir(N,tets,s):
    G=nx.Graph(); [G.add_edge(a,b) for t in tets for a,b in itertools.combinations(t,2)]
    F=set(tets)
    for m in GraphMatcher(G,G).isomorphisms_iter():
        if all(s[m[v]]==-s[v] for v in G) and all(tuple(sorted(m[x] for x in t)) in F for t in tets):
            return True
    return False
print(" N   poches avec un miroir exact (polarites equilibrees au hasard)")
for N in (4,5,6,8,10,12,14):
    ok=0; essais=200
    for _ in range(essais):
        tets=stacked(N); signs=[1]*(N//2)+[-1]*(N//2)+[0]*(N%2); random.shuffle(signs)
        ok+=a_un_miroir(N,tets,dict(enumerate(signs)))
    print(f"{N:2d}   {ok}/{essais} = {100*ok/essais:.1f} %")
