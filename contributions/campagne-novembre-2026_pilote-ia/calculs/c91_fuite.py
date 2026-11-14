# Hypothese de Rudolphe (17 h 32) : une fuite d'un univers a l'autre cree la chiralite. Test rapide (exploratoire) :
# a chaque naissance jumelee, ou va la norme qui quitte le noyau (lignee +, lignee -, contact) et porte-t-elle une polarite <Sigma> ?
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
g=1.5; rows=[]
for k in (1,2):
  for seed in range(4):
    for ngen in range(4):
      tp,tm,s,mir=grow(k,ngen,seed); F=[100+i for i in range(k)]
      cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
      for a0 in (np.ones(k),)+((np.array([1.,0.]),) if k==2 else ()):
        psi=V@a0; psi/=np.linalg.norm(psi)
        for t in tp:
          tmir=tuple(sorted(mir[x] for x in t)); A,B=1000,1001; s2=dict(s); sg=int(np.sign(sum(s[v] for v in t))) or 1; s2[A]=sg; s2[B]=-sg
          bb=lambda T,x:[tuple(sorted(tuple(y for i,y in enumerate(T) if i!=j)+(x,))) for j in range(4)]
          c2=R0([x for x in tp if x!=t]+bb(t,A)+[x for x in tm if x!=tmir]+bb(tmir,B),s2); P2,idx2=kern(c2,s2,g)
          Sp=np.zeros(len(c2))
          for c,i in idx.items():
            if c in idx2: Sp[idx2[c]]+=psi[i]
          R=Sp-P2@Sp; L=R@R
          PL=np.array([np.sign(sum(s2[v] for v in c)) for c in c2])
          wp=np.sum(R[PL>0]**2)/L; wm=np.sum(R[PL<0]**2)/L; w0=np.sum(R[PL==0]**2)/L
          sig=np.sum(PL*R**2)/L
          rows.append((k,L,wp,wm,w0,sig))
r=np.array(rows)
for k in (1,2):
  q=r[r[:,0]==k]
  print(f"k={k}: {len(q)} naissances ; fuite moyenne {q[:,1].mean():.3f} ; part lignée + {q[:,2].mean():.3f}, lignée − {q[:,3].mean():.3f}, contact {q[:,4].mean():.3f} ; ⟨Σ⟩ de la fuite : moyenne {q[:,5].mean():+.2e}, max |⟨Σ⟩| {np.abs(q[:,5]).max():.2e}")
