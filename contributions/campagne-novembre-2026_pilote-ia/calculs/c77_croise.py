# C-77 : branche « contacts croisés » (p0-n1, p1-n0) contre branche « jumeaux » (p0-n0, p1-n1), sans ajustement.
import random, itertools
exec(open('c76_naissances_signees.py').read().split('res={}')[0])
def run(cross,seeds=6,gens=3):
    hist=set()
    for seed in range(seeds):
        rng=random.Random(seed)
        # tetra + : 0,1,2,3 ; tetra - : 4,5,6,7 ; jumeaux i <-> i+4
        pairs=[(0,5),(1,4)] if cross else [(0,4),(1,5)]
        ren={}; s={}
        for j,(a,b) in enumerate(pairs): ren[a]=100+j; ren[b]=100+j
        for v in range(8): ren.setdefault(v,v)
        for v in range(8):
            if ren[v]==v: s[v]=1 if v<4 else -1
        for j in range(2): s[100+j]=0
        mir={v:(v+4)%8 for v in range(8)}
        mir2={}
        for v in range(8): mir2[ren[v]]=ren[mir[v]]
        tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]
        nv=200; out=[tuple(modes(R0(tp+tm,s),s,g) for g in (0.5,1.5,4.0))]
        for gen in range(gens):
            j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir2[x] for x in t)); tm.remove(tmir)
            a,b=nv,nv+1; nv+=2; sg=pol(t,s) or 1; s[a]=sg; s[b]=-sg; mir2[a]=b; mir2[b]=a
            tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
            tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
            out.append(tuple(modes(R0(tp+tm,s),s,g) for g in (0.5,1.5,4.0)))
        hist.add(tuple(o[1] for o in out))
    return hist
print("jumeaux (p_i-n_i) : modes a g=1.5 par generation :",run(False))
print("croises (p0-n1,p1-n0) : modes a g=1.5 par generation :",run(True))
