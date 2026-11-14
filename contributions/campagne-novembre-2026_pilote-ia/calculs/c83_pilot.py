exec(open('c83.py').read().split("#MAIN")[0])
import time
for k in (2,3):
    tp,tm,s,mir=init(k); nv=200; rng=random.Random(0)
    for _ in range(3):
        m=('B',tp[rng.randrange(len(tp))]); tp,tm,s,mir,nv=apply(m,tp,tm,s,mir,nv)
    print('k',k,'moves',len([m for m in moves(tp,s,[100+i for i in range(k)]) if m[0]!='B']))
    t=time.time(); r=run(1.5,k,[1]*k,0,1000,(tp,tm,s,mir,nv)); print(r,len(KC),round(time.time()-t,1),'s')
