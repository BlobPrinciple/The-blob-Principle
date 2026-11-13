# Contre-audit C-97A (ChatGPT) : exposant 2/3 des incidences du contact, et pente de ||G_n|| avec l'enumerateur reel de C-80.
import numpy as np, random
# (1) combinatoire pure, enumerateur C-80 (parent uniforme parmi les tetras de la lignee +)
def X_of(seed,N):
    rng=random.Random(seed); tp=[(100,1,2,3)]; nv=200; out=[]
    for n in range(1,N+1):
        t=tp.pop(rng.randrange(len(tp))); a=nv; nv+=1
        tp+=[tuple(a if i==m else t[i] for i in range(4)) for m in range(4)]
        if n in (100,1000,10000): out.append(sum(100 in T for T in tp))
    return out
X=np.array([X_of(s,10000) for s in range(400)],float)
for (n1,n2),(i,j) in zip(((100,1000),(1000,10000)),((0,1),(1,2))):
    print(f'pente log E[X] entre n={n1} et {n2} : {np.log(X[:,j].mean()/X[:,i].mean())/np.log(n2/n1):.4f}  (2/3 = 0.6667)')
# (2) ||G_n|| sur le vrai complexe jumeau, k=1, g=1.5, n jusqu'a 40
exec(open('c94c.py').read().split("worst=0")[0])
for g in (1.5,):
    L=[]
    for seed in range(6):
        sn=chain(1,seed,40,g); L.append([ (s_[4].T@s_[4])[0,0] for s_ in sn])
    L=np.array(L).mean(0); n=np.arange(len(L))
    for a,b in ((10,20),(20,40)):
        print(f'g={g} pente log G_n entre n={a} et {b} : {np.log(L[b]/L[a])/np.log(b/a):.3f}  (prédiction asymptotique -2/3)')
