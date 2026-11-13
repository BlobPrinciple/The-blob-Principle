# C-85A : test de permutation demande par ChatGPT (S permutee a l'interieur des groupes de meme taille ; unite = complexe).
exec(open('c85A.py').read().split("g=1.5; rng")[0])
from scipy.optimize import brentq
print('n_min =', brentq(lambda n:-0.4/(1+n)+0.1*(n-dstar),1,10))
g=1.5; rng=np.random.default_rng(1)
for k in (2,3):
  Ks=[]
  for seed in range(12):
    for ngen in range(6):
      tp,tm,s,mir=grow(k,ngen,seed); F=[100+i for i in range(k)]
      cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
      key=tuple(sorted(tp))
      if key not in [x[0] for x in Ks]: Ks.append((key,V.T@V,action(tp+tm),len(tp)))
  A=rng.normal(size=(200,k))
  def agree(Svals):
    conc=tot=0
    for i in range(len(Ks)):
      for j in range(i+1,len(Ks)):
        if Ks[i][3]!=Ks[j][3] or abs(Svals[i]-Svals[j])<1e-9: continue
        sS=np.sign(Svals[j]-Svals[i]); r=np.einsum('ni,ij,nj->n',A,Ks[i][1]-Ks[j][1],A)
        conc+=np.sum(np.sign(r)==sS); tot+=len(r)
    return conc/tot
    
  S0=np.array([x[2] for x in Ks]); obs=agree(S0)
  groups={}
  for i,x in enumerate(Ks): groups.setdefault(x[3],[]).append(i)
  null=[]
  for b in range(500):
    Sp=S0.copy()
    for gidx in groups.values(): Sp[gidx]=rng.permutation(S0[gidx])
    null.append(agree(Sp))
  null=np.array(null); print(f"k={k}: {len(Ks)} complexes, groupes de taille {sorted((t,len(v)) for t,v in groups.items())} ; accord observé {obs:.3f} ; nul moyen {null.mean():.3f} ± {null.std():.3f} ; p = {(np.sum(null>=obs)+1)/(len(null)+1):.4f}")
