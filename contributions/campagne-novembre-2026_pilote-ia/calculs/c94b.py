# Controle : le flux de retour (complement spectral -> nouveau noyau) est-il nul ?  ||P' S (I-P)|| , et P' S P compare a V' V^+
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
mx=0;mx2=0;n=0
for g in (0.5,1.5,4.0):
  for k in (1,2,3):
    for seed in range(4):
      for ngen in range(4):
        tp,tm,s,mir=grow(k,ngen,seed); F=[100+i for i in range(k)]
        cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
        for t in tp:
          tmir=tuple(sorted(mir[x] for x in t)); A,B=1000,1001; s2=dict(s); sg=int(np.sign(sum(s[v] for v in t))) or 1; s2[A]=sg; s2[B]=-sg
          bb=lambda T,x:[tuple(sorted(tuple(y for i,y in enumerate(T) if i!=j)+(x,))) for j in range(4)]
          c2=R0([x for x in tp if x!=t]+bb(t,A)+[x for x in tm if x!=tmir]+bb(tmir,B),s2); P2,idx2=kern(c2,s2,g)
          if round(np.trace(P2))!=k: continue
          S=np.zeros((len(c2),len(cells)))
          for c,i in idx.items():
            if c in idx2: S[idx2[c],i]=1
          mx=max(mx,np.linalg.norm(P2@S@(np.eye(len(cells))-P),2)); n+=1
print(n,'naissances ; norme max du flux de retour ||P\' S (I-P)|| =',mx)
