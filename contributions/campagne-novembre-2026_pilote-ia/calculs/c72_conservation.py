# C-72 (preenregistre) : le nombre de modes neutres proteges est-il conserve sur plusieurs generations
# de naissances JUMELEES (1->4 sur un tetra + 1->4 sur son miroir) ? et detruit par les naissances isolees ?
import random
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
def run(k,gens,twin,seed,g=1.5):
    rng=random.Random(seed)
    tp=[(0,1,2,3)]; tm=[(4,5,6,7)]; s={**{i:1 for i in range(4)},**{i:-1 for i in range(4,8)}}; mir={i:(i+4)%8 for i in range(8)}
    edges=[(i,i+4) for i in range(k)]; nv=8; out=[]
    for gen in range(gens+1):
        maxs=tp+tm+edges; cells=complex_from_max(maxs); D,G,idx=ops(cells); S=polar(cells,s)
        H=D+g*S@G; ev=np.linalg.eigvalsh(H); z=int(np.sum(abs(ev)<1e-8))
        out.append(z)
        if gen==gens: break
        j=rng.randrange(len(tp)); t=tp.pop(j); a=nv; nv+=1; s[a]=1
        tp+= [tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
        if twin:
            tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir); b=nv; nv+=1; s[b]=-1; mir[a]=b; mir[b]=a
            tm+= [tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
    return out
for k in (1,2,3):
    for twin in (True,False):
        res=[run(k,4,twin,sd) for sd in range(6)]
        print(f"k={k} {'jumelees' if twin else 'isolees '} : modes par generation", res[0], "| toutes graines identiques :",all(r==res[0] for r in res))
