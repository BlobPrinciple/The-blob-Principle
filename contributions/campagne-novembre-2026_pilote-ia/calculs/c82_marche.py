# C-82 (i)-(ii) : execution du preenregistrement ChatGPT (texte integral archive au §23).
# CHOIX D'IMPLEMENTATION FIGES AVANT EXECUTION (a signaler) :
#  - configuration initiale minimale = celle de C-76 (un tetra par lignee, k sommets fusionnes neutres) ;
#  - censure : trajectoire arretee et comptee a part si le complexe R0 depasse CAP=500 cellules ;
#  - arithmetique flottante float64 (tolerance 1e-9 pour le noyau) et non rationnelle : deviation declaree ;
#  - ressources : N=100 seulement et 64 graines (0..63) au lieu de 256 ; N=1000 non execute ;
#  - drift exact : enumere sur les 10 premiers etats visites des graines 0..3 seulement.
import sys, random, itertools, numpy as np, json
exec(open('c80_2A.py').read().split('g=1.5; out=[]')[0])
CAP=500
def init(k):
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
    tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]
    return tp,tm,s,mir
def M_(T,mir): return tuple(sorted(mir[x] for x in T))
def moves(tp,s,F):
    mv=[('B',t) for t in tp]
    faces={}
    for t in tp:
        for f in itertools.combinations(t,3): faces.setdefault(f,[]).append(t)
    edges={tuple(sorted(e)) for t in tp for e in itertools.combinations(t,2)}
    for f,ts in faces.items():
        if len(ts)==2:
            x=(set(ts[0])-set(f)).pop(); y=(set(ts[1])-set(f)).pop(); e=tuple(sorted((x,y)))
            if e not in edges and x not in F and y not in F: mv.append(('23',(f,x,y)))
    for e in edges:
        if any(v in F for v in e): continue
        around=[t for t in tp if set(e)<=set(t)]
        if len(around)==3:
            link=sorted(set().union(*map(set,around))-set(e))
            if len(link)==3 and not any(set(link)<=set(t) for t in tp): mv.append(('32',e))  # Pachner : face-lien absente (corrige C-83-R)
    return mv
def apply(m,tp,tm,s,mir,nv):
    s=dict(s); mir=dict(mir); typ,arg=m
    def b(T,a): return [tuple(sorted(tuple(x for i,x in enumerate(T) if i!=j)+(a,))) for j in range(4)]
    if typ=='B':
        t=arg; tmir=M_(t,mir); a,bb=nv,nv+1; sg=pol(t,s) or 1; s[a]=sg; s[bb]=-sg; mir[a]=bb; mir[bb]=a
        tp2=[x for x in tp if x!=t]+b(t,a); tm2=[x for x in tm if x!=tmir]+b(tmir,bb); return tp2,tm2,s,mir,nv+2
    if typ=='23':
        f,x,y=arg
        def d23(L,f,x,y):
            old=[tuple(sorted(f+(x,))),tuple(sorted(f+(y,)))]
            return [t for t in L if t not in old]+[tuple(sorted((x,y)+e)) for e in itertools.combinations(f,2)]
        fm=M_(f,mir); return d23(tp,f,x,y),d23(tm,fm,mir[x],mir[y]),s,mir,nv
    if typ=='32':
        def d32(L,e):
            around=[t for t in L if set(e)<=set(t)]; link=sorted(set().union(*map(set,around))-set(e))
            return [t for t in L if t not in around]+[tuple(sorted(link+[e[0]])),tuple(sorted(link+[e[1]]))]
        return d32(tp,arg),d32(tm,M_(arg,mir)),s,mir,nv
def basis(cells,s,g,F):
    P,idx=kern(cells,s,g); return P,idx,np.array([P[:,idx[(c,)]] for c in F]).T
def step_transport(cells,P,idx,Vs,cells2,s2,g,F,k):
    if any(len(c)>1 and pol(c,s2)==0 for c in cells2): return None
    P2,idx2,Vs2=basis(cells2,s2,g,F)
    if round(np.trace(P2))!=k: return None
    Phi=np.zeros((len(cells2),k))
    for c,i in idx.items():
        if c in idx2: Phi[idx2[c]]+=Vs[i]
    return np.linalg.lstsq(Vs2,P2@Phi,rcond=None)[0],(P2,idx2,Vs2)
def run(g,k,a0,seed,N,drift=False):
    rng=random.Random(seed); tp,tm,s,mir=init(k); F=[100+i for i in range(k)]; nv=200
    a=np.array(a0,float); cells=R0(tp+tm,s); P,idx,Vs=basis(cells,s,g,F)
    W=[];dr=[];ncyc=0;rej=0;hist=[]
    for n in range(N):
        mv=moves(tp,s,F)
        if drift and n<10:
            ws=[]
            for m in mv:
                st=apply(m,tp,tm,s,mir,nv); c2=R0(st[0]+st[1],st[2]); r=step_transport(cells,P,idx,Vs,c2,st[2],g,F,k)
                if r: b2=r[0]@a; ws.append(b2**2/np.sum(b2**2))
            if ws: dr.append(np.max(np.abs(np.mean(ws,axis=0)-a**2/np.sum(a**2))))
        rng.shuffle(mv); ok=False
        for m in mv:  # tirage uniforme parmi les orbites admissibles (rejet des inadmissibles)
            st=apply(m,tp,tm,s,mir,nv); c2=R0(st[0]+st[1],st[2])
            if len(c2)>CAP: return dict(cens=True,n=n,W=W,dr=dr,ncyc=ncyc,rej=rej)
            r=step_transport(cells,P,idx,Vs,c2,st[2],g,F,k)
            if r is None: rej+=1; continue
            ok=True; break
        if not ok: return dict(cens=True,n=n,W=W,dr=dr,ncyc=ncyc,rej=rej,blocked=True)
        M,(P,idx,Vs)=r; a=M@a; tp,tm,s,mir,nv=st; cells=c2
        hist.append(m[0]); ncyc+=(len(hist)>1 and hist[-2]=='23' and hist[-1]=='32')
        if np.linalg.norm(a)==0: return dict(fail=True)
        W.append((a**2/np.sum(a**2)).tolist())
    return dict(cens=False,n=N,W=W,dr=dr,ncyc=ncyc,rej=rej,types=''.join(x[0] for x in hist))
if __name__=='__main__':
    g=float(sys.argv[1]); k=int(sys.argv[2]); a0=json.loads(sys.argv[3]); seeds=int(sys.argv[4])
    res=[run(g,k,a0,sd,100,drift=(sd<4)) for sd in range(seeds)]
    json.dump(res,open(f'c82_res_g{g}_k{k}_{"".join(map(str,a0))}.json','w'))
    print(g,k,a0,'done')
