import itertools, random, numpy as np, c132_audit as A
from c120 import Mesh, SEEDS, vol6
for seed in (1320,1321):
    rng=random.Random(seed); m=Mesh(SEEDS['regulier'],1.0,'U','F'); Vref={}; A.relax(m,Vref)
    for n in range(1,32):
        TT=sorted(m.T); E=m.inc(); t=TT[rng.randrange(len(TT))]; e=A.longest(m,t); m.bisect(e,E=E); r=A.relax(m,Vref)
        if r['gmax']>1e-6 or r['viol']>1e-7: print(seed,n,len(m.T),{k:(round(v,8) if isinstance(v,float) else v) for k,v in r.items()})
