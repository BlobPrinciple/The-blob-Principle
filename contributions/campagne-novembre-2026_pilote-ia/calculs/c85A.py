# C-85A (protocole ChatGPT) : correspondance viabilite geometrique e^{-S} vs norme protegee a^T G_K a.
# Choix declares : complexes C-84 (grow, graines 0-5, generations 0-5), g=1.5 ; S calculee sur le complexe intact (deux lignees) ;
# la "persistance observee" n'est pas definie numeriquement dans le master -> non utilisee ; a parcourt 200 directions aleatoires + sommets.
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
from collections import Counter
dstar=2*np.pi/np.arccos(1/3)
def action(T):
    ne=Counter(e for t in T for e in itertools.combinations(t,2))
    return 3*len(T)+sum(-0.4*np.log(1+n)+0.05*(n-dstar)**2 for n in ne.values())
g=1.5; rng=np.random.default_rng(0)
for k in (2,3):
  Ks=[]
  for seed in range(6):
    for ngen in range(6):
      tp,tm,s,mir=grow(k,ngen,seed); F=[100+i for i in range(k)]
      cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
      key=tuple(sorted(tp))
      if key not in [x[0] for x in Ks]: Ks.append((key,V.T@V,action(tp+tm)))
  A=list(rng.normal(size=(200,k)))+list(np.eye(k))
  prop=0; flips=0; pairs=0; conc=0; tot=0
  for i in range(len(Ks)):
    for j in range(i+1,len(Ks)):
      Gi,Gj=Ks[i][1],Ks[j][1]; pairs+=1
      c=np.trace(Gi)/np.trace(Gj)
      if np.max(np.abs(Gi-c*Gj))<1e-10: prop+=1
      r=[a@Gi@a-a@Gj@a for a in A]
      if min(r)<0<max(r): flips+=1
      sS=np.sign(Ks[j][2]-Ks[i][2])   # e^{-S} favorise i si S_i<S_j
      conc+=sum(np.sign(x)==sS for x in r); tot+=len(r)
  print(f"k={k}: {len(Ks)} complexes distincts, {pairs} paires ; Gram proportionnelles : {prop} ; paires dont le classement par a†Ga dépend de a : {flips} ({100*flips/pairs:.1f} %) ; accord de classement e^-S vs a†Ga : {100*conc/tot:.1f} %")
print('--- contrôle de taille : paires à même nombre de tétraèdres ---')
for k in (2,3):
  Ks=[]
  for seed in range(12):
    for ngen in range(6):
      tp,tm,s,mir=grow(k,ngen,seed); F=[100+i for i in range(k)]
      cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
      key=tuple(sorted(tp))
      if key not in [x[0] for x in Ks]: Ks.append((key,V.T@V,action(tp+tm),len(tp)))
  A=list(rng.normal(size=(200,k)))
  conc=tot=pairs=0
  for i in range(len(Ks)):
    for j in range(i+1,len(Ks)):
      if Ks[i][3]!=Ks[j][3] or abs(Ks[i][2]-Ks[j][2])<1e-9: continue
      pairs+=1; sS=np.sign(Ks[j][2]-Ks[i][2])
      r=[a@Ks[i][1]@a-a@Ks[j][1]@a for a in A]; conc+=sum(np.sign(x)==sS for x in r); tot+=len(r)
  print(f"k={k}: {pairs} paires à taille égale ; accord e^-S vs a†Ga : {100*conc/tot:.1f} %")
