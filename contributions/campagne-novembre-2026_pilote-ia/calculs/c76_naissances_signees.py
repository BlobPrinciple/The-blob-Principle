# C-76 (preregistre) : apres fusion, naissances jumelees SIGNEES (le nouveau porteur prend le signe de la lignee du tetraedre :
# signe de la somme des polarites du tetra parent ; le miroir recoit le signe oppose), y compris dans les tetras qui touchent
# les points de rencontre. Puis R0 (rupture des cellules de polarite nulle). Succes : modes = k (nombre de fusions) toujours.
import random
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
def pol(c,s): return np.sign(sum(s[v] for v in c))
def modes(cells,s,g):
    cells=sorted(cells,key=lambda c:(len(c),c)); idx={c:i for i,c in enumerate(cells)}; n=len(cells); d=np.zeros((n,n))
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f and f in idx: d[idx[c],idx[f]]+=(-1)**j
    D=d+d.T; G=np.diag([(-1)**(len(c)-1) for c in cells]); S=np.diag([pol(c,s) for c in cells])
    return int(np.sum(abs(np.linalg.eigvalsh(D+g*S@G))<1e-9))
def R0(maxs,s):
    cells=complex_from_max(maxs); bad=[c for c in cells if len(c)==2 and pol(c,s)==0]
    return [c for c in cells if not any(set(e)<=set(c) for e in bad)]
res={}
for k in (1,2,3):
    for seed in range(8):
        rng=random.Random(seed)
        ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
        s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
        mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
        tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]
        nv=200; out=[]
        for gen in range(4):
            j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir)
            a,b=nv,nv+1; nv+=2; sg=pol(t,s) or 1; s[a]=sg; s[b]=-sg; mir[a]=b; mir[b]=a
            tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
            tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
            cells=R0(tp+tm,s); out.append(tuple(modes(cells,s,g) for g in (0.5,1.5,4.0)))
        res.setdefault(k,set()).add(tuple(out))
for k,v in res.items(): print(f"k={k}: {len(v)} historique(s) distinct(s) ; modes par generation :",sorted(v)[:3])
