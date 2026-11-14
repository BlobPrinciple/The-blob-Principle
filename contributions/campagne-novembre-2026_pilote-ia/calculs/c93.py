# Le « choc » au point de rencontre : recouvrement des projecteurs spinoriels des deux lignees sur les tetras qui touchent le contact.
# Reflet = symetrie par le plan passant par le contact c (le contact est fixe par le miroir). Copie = meme geometrie.
exec(open('c92.py').read().split('I3=np.eye(3)')[0])
c=X0[100]; nrm=unit(c)            # plan de reflexion contenant c : normale orthogonale a c
m=unit(np.cross(c,[1,0,0])); Ref=np.eye(3)-2*np.outer(m,m)
def ax(Z,axis,K):
    a=axis.get(K)
    if a is None or K==(100,1,2,3): return unit(Z[100]-sum(Z[v] for v in (100,1,2,3))/4)
    om,KK=a; return unit(Z[om]-sum(Z[v] for v in KK)/4)
for ngen in (0,4,10,25):
    ov_ref=[];ov_cop=[]
    for seed in range(16):
        X,tets,axis=history(seed,ngen); Y={v:Ref@p for v,p in X.items()}
        for K in tets:
            if 100 not in K: continue
            n1=ax(X,axis,K); n2=ax(Y,axis,K)
            ov_ref.append(np.trace(Pi(n1)@Pi(n2)).real); ov_cop.append(1.0)
    print(f'gén {ngen:2d} : tétras au contact {len(ov_ref)//16:.0f}/graine ; recouvrement des spins au contact, reflet : moyen {np.mean(ov_ref):.3f}, min {np.min(ov_ref):.3f} ; copie : 1,000')
