# C-90(2) exploratoire (Claude) : boucles d'aretes orientees. Arete orientee de l'aine vers le cadet (ordre de naissance) ;
# boucle parcourue dans le sens direct autour de l'arete (regle de la main droite, metrique enchassee).
exec(open('c90.py').read().split('allph=[]')[0])
age=lambda v:(-1 if v in X0 else v)
res=[]
for seed in range(8):
    rng=random.Random(seed); X=dict(X0); T0=(100,1,2,3); axis={T0:unit(X[100]-sum(X0.values())/4)}; tets=[T0]; nv=200
    for gen in range(6):
        j=rng.randrange(len(tets)); T=tets.pop(j)
        al=np.array([rng.random()+1e-3 for _ in range(4)]); al/=al.sum(); x=nv; nv+=1; X[x]=sum(al[i]*X[T[i]] for i in range(4))
        kids=[tuple(x if i==m else T[i] for i in range(4)) for m in range(4)]
        for m,K in enumerate(kids): axis[K]=unit(X[T[m]]-sum(X[v] for v in K)/4)
        tets+=kids
    edges={}
    for K in tets:
        for e in itertools.combinations(K,2): edges.setdefault(tuple(sorted(e,key=age)),[]).append(K)
    for (u,w),ring in edges.items():
        if len(ring)<3: continue
        # arete interieure si le cycle des faces se ferme
        ok=all(sum(len(set(K)&set(L))==3 for L in ring if L!=K)==2 for K in ring)
        if not ok: continue
        t=unit(X[w]-X[u]); e1=unit(np.cross(t,[0.3,0.7,0.1])); e2=np.cross(t,e1)
        def ang(K):
            c=sum(X[v] for v in K)/4-X[u]; return np.arctan2(c@e2,c@e1)
        order=sorted(ring,key=ang); M=np.eye(2,dtype=complex)
        for K in order: M=M@Pi(axis[K])
        b=np.trace(M)
        if abs(b)>1e-12: res.append(np.angle(b))
res=np.array(res)
print(f'{len(res)} boucles orientées (aîné→cadet, sens direct) : phase >0 : {np.mean(res>0):.3f} ; <0 : {np.mean(res<0):.3f} ; |φ| moyen {np.mean(np.abs(res))/np.pi:.3f}π')
