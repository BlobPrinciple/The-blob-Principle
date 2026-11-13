import itertools, random, numpy as np, scipy.optimize as so, c132_audit as A
from c120 import Mesh, SEEDS, vol6
seed=1320; rng=random.Random(seed); m=Mesh(SEEDS['regulier'],1.0,'U','F'); Vref={}; A.relax(m,Vref)
for n in range(1,20):
    TT=sorted(m.T); E=m.inc(); t=TT[rng.randrange(len(TT))]; e=A.longest(m,t); m.bisect(e,E=E)
    if n==19:
        ids=sorted(m.X); pos={v:i for i,v in enumerate(ids)}; X0=np.array([m.X[v] for v in ids]); ed=list(m.rest); I=np.array([pos[e[0]] for e in ed]); J=np.array([pos[e[1]] for e in ed]); R=np.array([m.rest[e] for e in ed])
        def f(z):
            X=z.reshape(-1,3); D=X[I]-X[J]; L=np.linalg.norm(D,axis=1); G=np.zeros_like(X); wv=((L-R)/np.maximum(L,1e-300))[:,None]*D
            np.add.at(G,I,wv); np.add.at(G,J,-wv); return 0.5*((L-R)**2).sum(),G.ravel()
        print('gradient check',so.check_grad(lambda z:f(z)[0],lambda z:f(z)[1],X0.ravel()))
        r=so.minimize(f,X0.ravel(),jac=True,method='L-BFGS-B',options=dict(gtol=1e-11,ftol=1e-16,maxiter=20000,maxcor=30,maxfun=100000)); print('ressorts seuls :',r.message,r.nit,r.nfev,r.fun,abs(r.jac).max())
        r2=so.minimize(f,X0.ravel(),jac=True,method='BFGS',options=dict(gtol=1e-10,maxiter=20000)); print('BFGS :',r2.message,r2.nit,r2.fun,abs(r2.jac).max())
        # volumes au point r
        X=r.x.reshape(-1,3); TTn=list(m.T); V=np.array([np.dot(X[pos[t[1]]]-X[pos[t[0]]],np.cross(X[pos[t[2]]]-X[pos[t[0]]],X[pos[t[3]]]-X[pos[t[0]]]))/6 for t in TTn]); print('volumes min au minimum des ressorts seuls :',V.min(), 'nb negatifs',(V<0).sum())
    r=A.relax(m,Vref)
print(r)
