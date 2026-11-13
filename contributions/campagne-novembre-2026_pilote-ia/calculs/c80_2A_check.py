exec(open('c80_2A.py').read().split('g=1.5; out=[]')[0])
import random
for g in (0.5,1.5,4.0):
 for k in (2,3):
  ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
  s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
  mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
  tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]
  sites=[100+i for i in range(k)]; nv=200; rng=random.Random(7)
  for gen in range(3):
    cells=R0(tp+tm,s); P,idx=kern(cells,s,g); Vs=np.array([P[:,idx[(c,)]] for c in sites]).T
    G=Vs.T@Vs
    gr=[];cs=[];ratios=[]; n3=sum(len(c)==4 for c in cells); n2=sum(len(c)==3 for c in cells)
    for j in range(len(tp)):
      t=tp[j]; tmir=tuple(sorted(mir[x] for x in t)); a,b=nv,nv+1
      s2=dict(s); sg=pol(t,s) or 1; s2[a]=sg; s2[b]=-sg
      tp2=tp[:j]+tp[j+1:]+[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
      tm2=[x for x in tm if x!=tmir]+[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
      cells2=R0(tp2+tm2,s2); P2,idx2=kern(cells2,s2,g)
      Vs2=np.array([P2[:,idx2[(c,)]] for c in sites]).T
      # matrice de transport en coordonnees de site
      Phi=np.zeros((len(cells2),k))
      for c,i in idx.items():
        if c in idx2: Phi[idx2[c]]+=Vs[i]
      Phi=P2@Phi; M=np.linalg.lstsq(Vs2,Phi,rcond=None)[0]
      ratios.append(np.max(np.abs(M-M[0,0]*np.eye(k)))); G2=Vs2.T@Vs2; gr.append(np.max(np.abs(G2/G2[0,0]-G/G[0,0]))); cs.append(M[0,0])
    print(f"g={g} k={k} gen={gen} n_parents={len(tp)} max|M-cI|={max(ratios):.1e} cellules après R0 : {n2} faces, {n3} tétras ; écart Gram normalisé={max(gr):.1e} ; c_T∈[{min(cs):.4f},{max(cs):.4f}]")
    j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir)
    a,b=nv,nv+1; nv+=2; sg=pol(t,s) or 1; s[a]=sg; s[b]=-sg; mir[a]=b; mir[b]=a
    tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
    tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
