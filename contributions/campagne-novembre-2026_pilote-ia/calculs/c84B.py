# C-84B (diagnostic) : flux de norme hors noyau pondere par les taux C-56, q = gamma * prod_{e in A}(1+n_e(K')), gamma=1.
# Choix declares avant calcul : n_e compte sur le complexe intact (les deux lignees) ; A = aretes dont l'ensemble des tetras incidents change ;
# psi = mode de sites uniforme normalise. Compare a la loi uniforme (q=1).
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
from collections import defaultdict
def inc(T):
    d=defaultdict(set)
    for t in T:
        for e in itertools.combinations(t,2): d[e].add(t)
    return d
for g in (0.5,1.5):
  for k in (2,3):
    for ngen in (1,2,3):
      tp,tm,s,mir=grow(k,ngen,0); F=[100+i for i in range(k)]
      cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
      a=np.ones(k); psi=V@a; psi/=np.linalg.norm(psi)
      I0=inc(tp+tm); rows=[]
      for t in tp:
        tmir=tuple(sorted(mir[x] for x in t)); A_,B_=1000,1001; s2=dict(s); sg=pol(t,s) or 1; s2[A_]=sg; s2[B_]=-sg
        bb=lambda T,x:[tuple(sorted(tuple(y for i,y in enumerate(T) if i!=j)+(x,))) for j in range(4)]
        tp2=[x for x in tp if x!=t]+bb(t,A_); tm2=[x for x in tm if x!=tmir]+bb(tmir,B_)
        I1=inc(tp2+tm2); Aset=[e for e in set(I0)|set(I1) if I0.get(e,set())!=I1.get(e,set())]
        q=np.prod([1+len(I1.get(e,())) for e in Aset],dtype=float)
        c2=R0(tp2+tm2,s2); P2,idx2=kern(c2,s2,g); Sp=np.zeros(len(c2))
        for c,i in idx.items():
          if c in idx2: Sp[idx2[c]]+=psi[i]
        leak=np.linalg.norm(Sp-P2@Sp)**2; rows.append((q,leak))
      q=np.array([r[0] for r in rows]); L=np.array([r[1] for r in rows])
      print(f"g={g} k={k} gen={ngen}: {len(rows)} naissances ; q ∈ [{q.min():.3g},{q.max():.3g}] ; fuite par naissance ∈ [{L.min():.4f},{L.max():.4f}] ; moyenne pondérée C-56 = {np.sum(q*L)/np.sum(q):.4f} vs uniforme = {L.mean():.4f} ; corrélation(q,fuite) = {np.corrcoef(q,L)[0,1] if len(rows)>2 and L.std()>1e-12 and q.std()>0 else float('nan'):.3f}")
