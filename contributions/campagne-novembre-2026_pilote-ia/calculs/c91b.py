# Variante : naissance ISOLEE (dans la seule lignee +), symetrie miroir brisee. La fuite porte-t-elle alors une polarite ?
exec(open('c91_fuite.py').read().split('g=1.5; rows=[]')[0])
g=1.5
for k in (1,2):
  out=[]
  for seed in range(4):
    for ngen in range(4):
      tp,tm,s,mir=grow(k,ngen,seed); F=[100+i for i in range(k)]
      cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
      psi=V@np.ones(k); psi/=np.linalg.norm(psi)
      for t in tp:
        A=1000; s2=dict(s); s2[A]=int(np.sign(sum(s[v] for v in t))) or 1
        bb=[tuple(sorted(tuple(y for i,y in enumerate(t) if i!=j)+(A,))) for j in range(4)]
        c2=R0([x for x in tp if x!=t]+bb+tm,s2); P2,idx2=kern(c2,s2,g)
        Sp=np.zeros(len(c2))
        for c,i in idx.items():
          if c in idx2: Sp[idx2[c]]+=psi[i]
        R=Sp-P2@Sp; L=R@R; PL=np.array([np.sign(sum(s2[v] for v in c)) for c in c2])
        out.append((L,np.sum(R[PL>0]**2)/L,np.sum(R[PL<0]**2)/L,np.sum(PL*R**2)/L,round(np.trace(P2))))
  o=np.array(out)
  print(f"k={k} naissance isolée : fuite moyenne {o[:,0].mean():.3f} ; part + {o[:,1].mean():.3f}, part − {o[:,2].mean():.3f} ; ⟨Σ⟩ de la fuite moyen {o[:,3].mean():+.3f} (min {o[:,3].min():+.3f}, max {o[:,3].max():+.3f}) ; modes protégés restants : {sorted(set(o[:,4].astype(int)))}")
