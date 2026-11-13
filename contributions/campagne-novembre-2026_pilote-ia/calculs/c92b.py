# Correction : chiralite mesuree par rapport a l'orientation AMBIANTE fixe (ordre des boucles fixe par la geometrie de la lignee +,
# commun aux deux lignees via le miroir combinatoire ; axes calcules dans la geometrie propre de chaque lignee).
exec(open('c92.py').read().split('I3=np.eye(3)')[0])
def chi2(X,tets,axis,M):
    Y={v:M@p for v,p in X.items()}; age=lambda v:(-1 if v in X0 else v)
    def ax(K,Z):
        a=axis.get(K)
        if a is None or K==(100,1,2,3): return unit(Z[100]-sum(Z[v] for v in (100,1,2,3))/4)
        om,KK=a; return unit(Z[om]-sum(Z[v] for v in KK)/4)
    edges={}
    for K in tets:
        for e in itertools.combinations(K,2): edges.setdefault(tuple(sorted(e,key=age)),[]).append(K)
    ph=[]
    for (u,w),ring in edges.items():
        if len(ring)<3 or not all(sum(len(set(K)&set(L))==3 for L in ring if L!=K)==2 for K in ring): continue
        t=unit(X[w]-X[u]); e1=unit(np.cross(t,[0.3,0.7,0.1])); e2=np.cross(t,e1)   # ordre fixe (lignee +)
        order=sorted(ring,key=lambda K:np.arctan2((sum(X[v] for v in K)/4-X[u])@e2,(sum(X[v] for v in K)/4-X[u])@e1))
        Mx=np.eye(2,dtype=complex)
        for K in order: Mx=Mx@Pi(ax(K,Y))
        b=np.trace(Mx)
        if abs(b)>1e-12: ph.append(np.sign(np.angle(b)))
    return np.mean(ph)
I3=np.eye(3); Ref=np.diag([-1.,1,1])
print('gén | χ+ | χ− copie | χ− reflet | χ global copie | χ global reflet')
for ngen in (2,4,6,8,10):
    a=[];b=[]
    for seed in range(16):
        X,t,ax=history(seed,ngen); a.append(chi2(X,t,ax,I3)); b.append(chi2(X,t,ax,Ref))
    print(f'{ngen:3d} | {np.mean(a):+.3f} | {np.mean(a):+.3f} | {np.mean(b):+.3f} | {np.mean(a)+np.mean(a):+.3f} | {np.mean(a)+np.mean(b):+.3f}')
