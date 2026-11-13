# C-92 (exploratoire, criteres figes avant calcul) : chiralite d'orientation par lignee, miroir = copie ou reflet, au fil de la croissance.
# chi_L = (part de boucles d'aretes interieures a phase >0) - (part a phase <0), aretes orientees aine->cadet, sens direct.
import numpy as np, random, itertools
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.diag([1,-1]).astype(complex)
Pi=lambda n:0.5*(np.eye(2)+n[0]*sx+n[1]*sy+n[2]*sz); unit=lambda v:v/np.linalg.norm(v)
X0={100:np.array([1,1,1.]),1:np.array([1,-1,-1.]),2:np.array([-1,1,-1.]),3:np.array([-1,-1,1.])}
def history(seed,ngen):
    rng=random.Random(seed); X=dict(X0); T0=(100,1,2,3); axis={T0:unit(X[100]-sum(X0.values())/4)}; tets=[T0]; nv=200
    for gen in range(ngen):
        j=rng.randrange(len(tets)); T=tets.pop(j); al=np.array([rng.random()+1e-3 for _ in range(4)]); al/=al.sum()
        x=nv; nv+=1; X[x]=sum(al[i]*X[T[i]] for i in range(4)); kids=[tuple(x if i==m else T[i] for i in range(4)) for m in range(4)]
        for m,K in enumerate(kids): axis[K]=(T[m],K)   # axe defini geometriquement plus bas (sommet omis)
        tets+=kids
    return X,tets,axis
def chi(X,tets,axis,M):  # M : transformation lineaire appliquee a la geometrie (I = copie, reflet = diag(-1,1,1))
    Y={v:M@p for v,p in X.items()}; age=lambda v:(-1 if v in X0 else v)
    def ax(K):
        a=axis.get(K)
        if a is None or K==(100,1,2,3): return unit(Y[100]-sum(Y[v] for v in (100,1,2,3))/4)
        om,KK=a; return unit(Y[om]-sum(Y[v] for v in KK)/4)
    edges={}
    for K in tets:
        for e in itertools.combinations(K,2): edges.setdefault(tuple(sorted(e,key=age)),[]).append(K)
    ph=[]
    for (u,w),ring in edges.items():
        if len(ring)<3 or not all(sum(len(set(K)&set(L))==3 for L in ring if L!=K)==2 for K in ring): continue
        t=unit(Y[w]-Y[u]); e1=unit(np.cross(t,[0.3,0.7,0.1])); e2=np.cross(t,e1)
        order=sorted(ring,key=lambda K:np.arctan2((sum(Y[v] for v in K)/4-Y[u])@e2,(sum(Y[v] for v in K)/4-Y[u])@e1))
        Mx=np.eye(2,dtype=complex)
        for K in order: Mx=Mx@Pi(ax(K))
        b=np.trace(Mx)
        if abs(b)>1e-12: ph.append(np.sign(np.angle(b)))
    return (np.mean(ph) if ph else np.nan), len(ph)
I3=np.eye(3); Ref=np.diag([-1.,1,1])
print('gén | χ+ (moyenne sur 16 graines) | χ− copie | χ− reflet | nb boucles moyen')
for ngen in (2,4,6,8,10):
    a=[];b=[];c=[];nb=[]
    for seed in range(16):
        X,t,ax=history(seed,ngen); x1,n1=chi(X,t,ax,I3); x2,_=chi(X,t,ax,I3); x3,_=chi(X,t,ax,Ref)
        if not np.isnan(x1): a.append(x1); b.append(x2); c.append(x3); nb.append(n1)
    print(f'{ngen:3d} | {np.mean(a):+.3f} ± {np.std(a)/np.sqrt(len(a)):.3f} | {np.mean(b):+.3f} | {np.mean(c):+.3f} | {np.mean(nb):.1f}')
