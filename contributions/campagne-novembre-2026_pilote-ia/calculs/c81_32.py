# C-81 (preenregistre par ChatGPT, execute par Claude) : paire miroir de mouvements de Pachner 3->2
# supprimant une ancienne arete chargee (hors F). Admissibilite : F intact, dim ker = k, aucune cellule nouvelle de polarite nulle.
# Transport : restriction (coefficients gardes sur cellules persistantes), puis P0'. Mesure : matrice M en base de sites.
exec(open('c80_2A.py').read().split('g=1.5; out=[]')[0])
import random
from collections import defaultdict
def grow(k,ngen,seed):
    rng=random.Random(seed)
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
    tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]; nv=200
    for gen in range(ngen):
      j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir)
      a,b=nv,nv+1; nv+=2; sg=pol(t,s) or 1; s[a]=sg; s[b]=-sg; mir[a]=b; mir[b]=a
      tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
      tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
    return tp,tm,s,mir
def move32(tets,e):
    around=[t for t in tets if set(e)<=set(t)]
    if len(around)!=3: return None
    link=sorted(set().union(*map(set,around))-set(e))
    if len(link)!=3: return None
    new=[tuple(sorted(link+[e[0]])),tuple(sorted(link+[e[1]]))]
    if any(set(link)<=set(t) for t in tets): return None  # Pachner : face-lien absente (corrige C-83-R)
    # l'arete doit etre interieure : chaque face autour de e partagee par 2 des 3 tetras
    return [t for t in tets if t not in around]+new
g=1.5; F=lambda k:[100+i for i in range(k)]; rows=[]
for k in (1,2,3):
  for seed in range(6):
    for ngen in (2,3,4):
      tp,tm,s,mir=grow(k,ngen,seed); sites=F(k)
      cells=R0(tp+tm,s); P,idx=kern(cells,s,g)
      if np.trace(P).round()!=k: continue
      Vs=np.array([P[:,idx[(c,)]] for c in sites]).T
      edges={tuple(sorted(e)) for t in tp for e in itertools.combinations(t,2)}
      for e in sorted(edges):
        if any(v in sites for v in e): continue
        tp2=move32(tp,e)
        if tp2 is None: continue
        em=tuple(sorted(mir[v] for v in e)); tm2=move32(tm,em)
        if tm2 is None: continue
        cells2=R0(tp2+tm2,s)
        if any(len(c)>1 and pol(c,s)==0 for c in cells2 if c not in cells): continue
        P2,idx2=kern(cells2,s,g)
        if round(np.trace(P2))!=k: rows.append((k,seed,ngen,e,'dim ker change',round(np.trace(P2)))); continue
        Vs2=np.array([P2[:,idx2[(c,)]] for c in sites]).T
        Phi=np.zeros((len(cells2),k))
        for c,i in idx.items():
          if c in idx2: Phi[idx2[c]]+=Vs[i]
        Phi=P2@Phi; M=np.linalg.lstsq(Vs2,Phi,rcond=None)[0]
        G=Vs.T@Vs; G2=Vs2.T@Vs2
        pred=np.linalg.solve(G2.T,G.T).T  # G_old G_new^{-1}, sens croissance inverse : ici "ancien"=avant 3->2 (plus d'aretes)
        rows.append((k,seed,ngen,e,np.round(M,6).tolist(),np.max(np.abs(M-np.eye(k))),np.max(np.abs(M-np.linalg.inv(G2)@G)),np.max(np.abs(M-G@np.linalg.inv(G2))),np.max(np.abs(M.T-np.linalg.inv(G2)@G))))
done=set()
for r in rows:
  key=(r[0],str(r[4]))
  if key in done: continue
  done.add(key); print(r)
print('nb cas',len(rows),' max|M-I| global =',max((r[5] for r in rows if len(r)==9),default=None))
