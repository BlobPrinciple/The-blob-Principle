# Contre-audit independant de C-98 (ChatGPT) par Claude : dimension spectrale du graphe dual, croissance 1->4 + mouvements 2<->3 LEGAUX.
# Choix declares AVANT calcul : une lignee (boule) ; parent de naissance uniforme ; R tentatives de reorganisation par naissance ;
# chaque tentative : tetra uniforme, puis a pile ou face : (2->3) face uniforme du tetra, legale si face interieure et arete (x,y) absente ;
# (3->2) arete uniforme du tetra, legale si exactement 3 tetras autour, lien de 3 sommets, face-lien absente.
# Diffusion : marche paresseuse W=(I+D^-1 A)/2 sur le graphe dual ; P(t) moyenne sur 400 departs ; d_s(t)=-2 dlnP/dlnt (difference centree en log).
import sys, random, itertools, numpy as np, scipy.sparse as sp
def grow(nb,R,seed):
    rng=random.Random(seed); tets={(0,1,2,3)}; L=[(0,1,2,3)]; pos={(0,1,2,3):0}
    F={}; E={}
    def add(t):
        t=tuple(sorted(t)); tets.add(t); pos[t]=len(L); L.append(t)
        for f in itertools.combinations(t,3): F.setdefault(f,set()).add(t)
        for e in itertools.combinations(t,2): E.setdefault(e,set()).add(t)
    def rem(t):
        tets.discard(t); i=pos.pop(t); last=L.pop()
        if last!=t: L[i]=last; pos[last]=i
        for f in itertools.combinations(t,3):
            F[f].discard(t)
            if not F[f]: del F[f]
        for e in itertools.combinations(t,2):
            E[e].discard(t)
            if not E[e]: del E[e]
    for f in itertools.combinations((0,1,2,3),3): F.setdefault(f,set()).add((0,1,2,3))
    for e in itertools.combinations((0,1,2,3),2): E.setdefault(e,set()).add((0,1,2,3))
    nv=4; acc=[0,0]
    for b in range(nb):
        t=L[rng.randrange(len(L))]; rem(t)
        for m in range(4): add(tuple(nv if i==m else t[i] for i in range(4)))
        nv+=1
        for _ in range(R):
            t=L[rng.randrange(len(L))]
            if rng.random()<0.5:
                f=tuple(v for i,v in enumerate(t) if i!=rng.randrange(4)) if False else None
                k=rng.randrange(4); f=tuple(v for i,v in enumerate(t) if i!=k); ts=F[f]
                if len(ts)!=2: continue
                t1,t2=tuple(ts); x=(set(t1)-set(f)).pop(); y=(set(t2)-set(f)).pop(); e=tuple(sorted((x,y)))
                if e in E: continue
                rem(t1); rem(t2)
                for pr in itertools.combinations(f,2): add(pr+(x,y))
                acc[0]+=1
            else:
                e=tuple(sorted(rng.sample(t,2))); ts=E[e]
                if len(ts)!=3: continue
                link=sorted(set().union(*map(set,ts))-set(e))
                if len(link)!=3 or tuple(link) in F: continue
                for tt in list(ts): rem(tt)
                add(tuple(link)+(e[0],)); add(tuple(link)+(e[1],)); acc[1]+=1
    # verification de variete : aucune face dans plus de 2 tetras
    assert max(len(v) for v in F.values())<=2
    return L,F,acc
def dual(L,F):
    idx={t:i for i,t in enumerate(L)}; r=[];c=[]
    for f,ts in F.items():
        if len(ts)==2:
            a,b=[idx[t] for t in ts]; r+=[a,b]; c+=[b,a]
    return sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(len(L),len(L)))
def ds(A,ts=(4,8,16,32,64),nstart=400,seed=0):
    n=A.shape[0]; d=np.array(A.sum(1)).ravel(); d[d==0]=1
    W=0.5*(sp.eye(n)+sp.diags(1/d)@A).tocsr(); WT=W.T.tocsr()
    rng=np.random.default_rng(seed); st=rng.choice(n,min(nstart,n),replace=False)
    X=np.zeros((n,len(st))); X[st,np.arange(len(st))]=1; P={}; tmax=int(max(ts)*1.5)+1
    for t in range(1,tmax+1):
        X=WT@X; P[t]=X[st,np.arange(len(st))].mean()
    out={}
    for t in ts:
        a,b=int(round(t/1.5)),int(round(t*1.5)); out[t]=-2*np.log(P[b]/P[a])/np.log(b/a)
    return out
def cubic(Lc):
    n=Lc**3; I=np.arange(n).reshape(Lc,Lc,Lc); r=[];c=[]
    for ax in range(3):
        J=np.roll(I,1,axis=ax); r+=list(I.ravel())+list(J.ravel()); c+=list(J.ravel())+list(I.ravel())
    return sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(n,n))
if __name__=='__main__':
    print('témoin cubique 3D périodique L=20 :',{t:round(v,2) for t,v in ds(cubic(20)).items()})
    nb=int(sys.argv[1])
    for R in (0,4,16,64,128):
        res=[];nt=[];ac=np.zeros(2)
        for seed in range(5):
            L,F,acc=grow(nb,R,seed); res.append(list(ds(dual(L,F)).values())); nt.append(len(L)); ac+=acc
        res=np.array(res)
        print(f'R={R:3d} naissances={nb} tétras≈{int(np.mean(nt))} (2→3 acceptés {int(ac[0]/5)}, 3→2 {int(ac[1]/5)}) d_s à t=4,8,16,32,64 :',np.round(res.mean(0),2).tolist(),'± (t=16)',round(res[:,2].std(),2))
