# C-91 / PR-1 (preenregistre par ChatGPT) execute par Claude. k=1, graines 100-163, 10 generations, g in {0.5,1.5,4}, Dirichlet(1,1,1,1).
import numpy as np, random, itertools, json, sys
exec(open('c80_2A.py').read().split('g=1.5; out=[]')[0])
unit=lambda v:v/np.linalg.norm(v)
X0={100:np.array([1,1,1.]),1:np.array([1,-1,-1.]),2:np.array([-1,1,-1.]),3:np.array([-1,-1,1.])}
n0=unit(X0[100]-sum(X0.values())/4)
def plane_normal(vlab): return unit(np.cross(n0,X0[vlab]-X0[100]))   # plan contenant c, l'axe initial et la direction du sommet vlab
U={'ref':plane_normal(1),'ctl2':plane_normal(2),'ctl3':plane_normal(3)}
def mirror_lab(v): return v if v==100 else v+1000
def G_of(tets,g):
    s={}; 
    for T in tets:
        for v in T: s[v]=0 if v==100 else 1
    mt=[tuple(sorted(mirror_lab(v) for v in T)) for T in tets]
    for T in mt:
        for v in T: s[v]=0 if v==100 else -1
    cells=R0([tuple(sorted(T)) for T in tets]+mt,s); P,idx=kern(cells,s,g)
    return P[idx[(100,)],idx[(100,)]], round(np.trace(P))
def axis(X,ax,K):
    if K not in ax: return n0
    om,KK=ax[K]; return unit(X[om]-sum(X[v] for v in KK)/4)
g=float(sys.argv[1]); res=[]
for seed in range(100,164):
    rng=np.random.default_rng(seed); X=dict(X0); tets=[(100,1,2,3)]; ax={}; nv=200; hist=[]
    for gen in range(10):
        G,kd=G_of(tets,g); cands=[K for K in tets if 100 in K]
        rows=[]
        for K in cands:
            kids=[tuple(9999 if i==m else K[i] for i in range(4)) for m in range(4)]
            G2,kd2=G_of([T for T in tets if T!=K]+kids,g)
            if kd2!=1: continue
            n=axis(X,ax,K); d={nm:float((n@u)**2) for nm,u in U.items()}
            rows.append(dict(L=1-G2/G,**d))
        hist.append(rows)
        # naissance reellement tiree (uniforme sur tous les tetras), Dirichlet(1,1,1,1)
        j=int(rng.integers(len(tets))); T=tets.pop(j); al=rng.dirichlet([1,1,1,1]); x=nv; nv+=1
        X[x]=sum(al[i]*X[T[i]] for i in range(4)); kids=[tuple(x if i==m else T[i] for i in range(4)) for m in range(4)]
        for m,K in enumerate(kids): ax[K]=(T[m],K)
        tets+=kids
    res.append(hist)
json.dump(res,open(f'c91_g{g}.json','w')); print('done',g)
