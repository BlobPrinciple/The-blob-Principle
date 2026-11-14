# C-84A : certificat independant de G_K - G_K' = R^T R >= 0 sous naissances jumelees (toutes les naissances, plusieurs histoires).
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
from fractions import Fraction
out=[]
for g in (0.5,1.5,4.0):
  for k in (1,2,3):
    for seed in range(4):
      for ngen in (0,1,2,3):
        tp,tm,s,mir=grow(k,ngen,seed); F=[100+i for i in range(k)]
        cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T; G=V.T@V
        nv=1000
        for t in tp:
          tmir=tuple(sorted(mir[x] for x in t)); a,b=nv,nv+1; s2=dict(s); sg=pol(t,s) or 1; s2[a]=sg; s2[b]=-sg
          bb=lambda T,x:[tuple(sorted(tuple(y for i,y in enumerate(T) if i!=j)+(x,))) for j in range(4)]
          tp2=[x for x in tp if x!=t]+bb(t,a); tm2=[x for x in tm if x!=tmir]+bb(tmir,b)
          c2=R0(tp2+tm2,s2); P2,idx2=kern(c2,s2,g)
          if round(np.trace(P2))!=k: continue
          SV=np.zeros((len(c2),k)); lost=0
          for c,i in idx.items():
            if c in idx2: SV[idx2[c]]+=V[i]
            else: lost=max(lost,np.abs(V[i]).max())
          iso=np.max(np.abs(SV.T@SV-G))
          R=SV-P2@SV; V2=np.array([P2[:,idx2[(c,)]] for c in F]).T; G2=V2.T@V2
          D=G-G2; ev=np.linalg.eigvalsh(D)
          out.append((g,k,iso,lost,np.max(np.abs(R.T@R-D)),ev.min(),int(np.sum(ev>1e-10)),ev.max()))
o=np.array([x[2:] for x in out])
print('naissances testées',len(out))
print('max |S†S - G| (isométrie) =',o[:,0].max(),' ; max coefficient perdu (cellules disparues) =',o[:,1].max())
print('max |R†R - (G-G\')| =',o[:,2].max(),' ; min valeur propre de G-G\' =',o[:,3].min())
for g in (0.5,1.5,4.0):
  for k in (1,2,3):
    sel=[x for x in out if x[0]==g and x[1]==k]
    print(f'g={g} k={k}: rangs {sorted(set(x[6] for x in sel))}, fraction max de norme quittant le noyau {max(x[7] for x in sel):.4f}')
# cas exact
tp,tm,s,mir=grow(1,0,0); g=1.5
