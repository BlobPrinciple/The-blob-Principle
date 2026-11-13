# C-113 (protocole propose par ChatGPT, execute par Claude). Graphe des SOMMETS. Graines 1000-1015 ; 128, 512, 2048 naissances par lignee.
# Dynamiques : A croissance seule ; B courbure compensee (C-112). Temoin : lignee isolee. Jumeaux : deux copies (histoire miroir = meme
# combinatoire) identifiees en k = 1, 2, 3 sommets de contact.
# CHOIX DECLARES (non fixes par le protocole) : contacts = sommets 0..k-1 du tetraedre germe ; marche paresseuse 1/2 ; estimateur d_s
# identique a v1_audit (fenetre t/1,5 .. 1,5 t) ; departs "pres" = distance <= 1 d'un contact, "volume" = distance >= 3 ;
# traversee = masse dans l'autre lignee (hors contacts) pour un depart uniforme dans la lignee + hors contacts.
import sys, math, json, random, itertools
import numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path
from multiprocessing import Pool
th=math.acos(1/3); r=(8*math.pi-18*th)/(6*th-2*math.pi); TS=(8,16,32,64,128)
def lineage(nb,seed,arm):
    rng=random.Random(seed); L=[(0,1,2,3)]; pos={(0,1,2,3):0}; F={}; E={}
    def add(t):
        t=tuple(sorted(t)); pos[t]=len(L); L.append(t)
        for x in itertools.combinations(t,3): F.setdefault(x,set()).add(t)
        for x in itertools.combinations(t,2): E.setdefault(x,set()).add(t)
    def rem(t):
        i=pos.pop(t); last=L.pop()
        if last!=t: L[i]=last; pos[last]=i
        for x in itertools.combinations(t,3):
            F[x].discard(t)
            if not F[x]: del F[x]
        for x in itertools.combinations(t,2):
            E[x].discard(t)
            if not E[x]: del E[x]
    for x in itertools.combinations((0,1,2,3),3): F.setdefault(x,set()).add((0,1,2,3))
    for x in itertools.combinations((0,1,2,3),2): E.setdefault(x,set()).add((0,1,2,3))
    nv=4; m=0
    for n in range(1,nb+1):
        t=L[rng.randrange(len(L))]; rem(t)
        for k in range(4): add(tuple(nv if i==k else t[i] for i in range(4)))
        nv+=1
        if arm=='B':
            target=round(r*n); tries=0
            while m<target and tries<2000:
                tries+=1; t=L[rng.randrange(len(L))]; k=rng.randrange(4); fc=tuple(v for i,v in enumerate(t) if i!=k); ts=F[fc]
                if len(ts)!=2: continue
                t1,t2=tuple(ts); x=(set(t1)-set(fc)).pop(); y=(set(t2)-set(fc)).pop(); e=tuple(sorted((x,y)))
                if e in E: continue
                rem(t1); rem(t2)
                for pr in itertools.combinations(fc,2): add(pr+(x,y))
                m+=1; tries=0
    return nv,list(E.keys())
def graph(nv,edges,k):
    # k=0 : lignee isolee. k>=1 : deux copies, sommets 0..k-1 communs.
    if k==0:
        n=nv; e=np.array(edges)
    else:
        def mp(v): return v if v<k else v+nv-k
        n=2*nv-k; e=np.array(edges+[(mp(a),mp(b)) for a,b in edges])
        e=np.unique(np.sort(e,axis=1),axis=0)
    A=sp.csr_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(n,n)); A=((A+A.T)>0).astype(float).tocsr()
    return A
def walk(A,starts,tmax=193):
    n=A.shape[0]; d=np.array(A.sum(1)).ravel()
    WT=(0.5*(sp.eye(n)+sp.diags(1/d)@A)).T.tocsr()
    X=np.zeros((n,len(starts))); X[starts,np.arange(len(starts))]=1; P={}; snaps={}
    for t in range(1,tmax+1):
        X=WT@X; P[t]=X[starts,np.arange(len(starts))].mean()
        if t in TS: snaps[t]=X.copy()
    return P,snaps
def dsof(P): return [float(-2*np.log(P[int(round(t*1.5))]/P[int(round(t/1.5))])/np.log(int(round(t*1.5))/int(round(t/1.5)))) for t in TS]
def run(args):
    nb,seed,arm=args; nv,edges=lineage(nb,seed,arm); out=dict(nb=nb,seed=seed,arm=arm,nv=nv)
    rng=np.random.default_rng(seed)
    for k in (0,1,2,3):
        A=graph(nv,edges,k); n=A.shape[0]; kc=max(k,1); cont=list(range(kc))
        dist=shortest_path(A,unweighted=True,indices=cont).min(0)
        plus=np.arange(kc,nv)                     # lignee + hors contacts
        def pick(mask):
            idx=plus[mask[plus]]; return rng.choice(idx,min(300,len(idx)),replace=False) if len(idx) else None
        res={}
        for name,mask in (('tout',np.ones(n,bool)),('pres',dist<=1),('volume',dist>=3)):
            st=pick(mask)
            if st is None: res[name]=None; continue
            P,snaps=walk(A,st); res[name]=dsof(P)
            if name=='tout' and k>0:
                res['traversee']=[float(snaps[t][nv:,:].sum(0).mean()) for t in TS]
        deg=np.array(A.sum(1)).ravel(); res['pi_contacts']=float(deg[:kc].sum()/deg.sum()); res['frac_volume']=float((dist[plus]>=3).mean())
        out[f'k{k}']=res
    return out
if __name__=='__main__':
    jobs=[(nb,s,a) for nb in (128,512,2048) for s in range(1000,1016) for a in 'AB']
    with Pool(2) as p: res=p.map(run,jobs)
    json.dump(res,open('c113.json','w'))
    def av(rs,k,key):
        v=[x[f'k{k}'][key] for x in rs if x[f'k{k}'].get(key) is not None]
        return (np.round(np.mean(v,axis=0),2).tolist(),len(v)) if v else None
    for a in 'AB':
        for nb in (128,512,2048):
            rs=[x for x in res if x['nb']==nb and x['arm']==a]
            print(f'--- bras {a}, {nb} naissances, {rs[0]["nv"]} sommets par lignée')
            for k in (0,1,2,3):
                print(f'  k={k}: d_s tout={av(rs,k,"tout")} près={av(rs,k,"pres")} volume={av(rs,k,"volume")} traversée={av(rs,k,"traversee")} pi(F)={np.mean([x[f"k{k}"]["pi_contacts"] for x in rs]):.4f} part volume={np.mean([x[f"k{k}"]["frac_volume"] for x in rs]):.2f}')
