# Les contributions de retour niveau par niveau : M_E = V''^+ P'' S' Pi_E S V  (coordonnees de sites). Proportionnelles a l'identite ?
exec(open('c94.py').read().split("if __name__")[0])
def chain(k,seed,ngen,g=1.5):
    rng=random.Random(seed)
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
    tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]; F=[100+i for i in range(k)]; nv=200; snaps=[]
    for gen in range(ngen+1):
        cells=R0(tp+tm,s); Hm,idx=H(cells,s,g); P,_=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T; snaps.append((cells,idx,Hm,P,V))
        j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir)
        a,b=nv,nv+1; nv+=2; sg=pol(t,s) or 1; s[a]=sg; s[b]=-sg; mir[a]=b; mir[b]=a
        tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
        tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
    return snaps
def Smat(a,b):
    S=np.zeros((len(b[0]),len(a[0])))
    for c,i in a[1].items():
        if c in b[1]: S[b[1][c],i]=1
    return S
worst=0; tot=0; retmax=0
for k in (2,3):
  for seed in range(6):
    sn=chain(k,seed,5)
    for n in range(len(sn)-2):
        A,B,C=sn[n],sn[n+1],sn[n+2]; S1=Smat(A,B); S2=Smat(B,C)
        e,U=np.linalg.eigh(B[2]); lab=np.cumsum(np.r_[0,np.diff(e)>1e-8])
        for L in np.unique(lab):
            UE=U[:,lab==L]
            if abs(e[lab==L][0])<1e-9: continue
            M=np.linalg.pinv(C[4])@C[3]@S2@UE@UE.T@S1@A[4]
            sc=np.trace(M)/k; worst=max(worst,np.abs(M-sc*np.eye(k)).max()); retmax=max(retmax,abs(sc)); tot+=1
print(tot,'niveaux excités testés ; max |M_E − c_E·I| =',worst,' ; max |c_E| =',retmax)
