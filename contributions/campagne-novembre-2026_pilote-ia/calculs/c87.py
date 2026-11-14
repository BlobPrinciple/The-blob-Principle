# C-87 (exploratoire, protocole ChatGPT) : dimension de l'algebre de Lie des generateurs "sommets" (antisymetriques sur les sommets
# charges d'une lignee, repliques par le miroir, etendus aux cochaines par derivation exterieure) qui commutent avec D et Sigma.Gamma,
# le long de la croissance jumelee signee (graines 0-3, generations 0-4), k=1,2. Aucun ajustement : solution = noyau lineaire.
exec(open('c86D.py').read().split('for kind in')[0])
exec(open('c81_32.py').read().split('g=1.5; F=')[0].split("exec(open('c80_2A.py')")[0])
import random
def grow2(k,ngen,seed):
    rng=random.Random(seed)
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
    tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]; nv=200
    for gen in range(ngen):
      j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir)
      a,b=nv,nv+1; nv+=2; sg=int(np.sign(sum(s[v] for v in t))) or 1; s[a]=sg; s[b]=-sg; mir[a]=b; mir[b]=a
      tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
      tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
    return tp,tm,s,mir
for k in (1,2):
  for seed in range(4):
    row=[]
    for ngen in range(5):
      tp,tm,s,mir=grow2(k,ngen,seed); cells=R0(tp+tm,s); d,D,G,S,idx=ops_(cells,s,1.5); SG=S@G
      ch=sorted({v for t in tp for v in t if s[v]!=0})  # sommets charges de la lignee + (signes herites possibles des deux signes)
      basis=[]
      for i,j in itertools.combinations(range(len(ch)),2):
        u,w=ch[i],ch[j]
        Jv={u:{w:-1.0},w:{u:1.0},mir[u]:{mir[w]:-1.0},mir[w]:{mir[u]:1.0}}
        basis.append(Jop(cells,idx,Jv))
      if not basis: row.append(0); continue
      Mcon=np.array([np.concatenate([(B@D-D@B).ravel(),(B@SG-SG@B).ravel()]) for B in basis]).T
      sv=np.linalg.svd(Mcon,compute_uv=False); dim=int(np.sum(sv<1e-9))+max(0,len(basis)-len(sv))
      row.append(dim)
    print(f"k={k} graine {seed} : dimension de l'algèbre de symétries continues, générations 0→4 : {row}")
