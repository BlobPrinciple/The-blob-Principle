# V1-ACTION (regle figee par ChatGPT : equilibre proportionnel a e^{-S}, coefficients du master inchanges), execute par Claude.
# ECARTS DECLARES : le fichier PR-1 (tailles, graines, fenetres) est inaccessible ; choix de Claude figes avant calcul :
#  nombre de sommets fixe V = 84, 324, 1284 (croissance stellaire de 80, 320, 1280 naissances, puis AUCUNE naissance) ;
#  Metropolis-Hastings sur mouvements 2<->3 legaux, proposition "tetra uniforme / pile ou face / face ou arete uniforme",
#  facteur de Hastings N/(N+1) (2->3) et N/(N-1) (3->2) ; 50, 200, 800 tentatives par tetra initial (controle de convergence) ;
#  graines 300-302 ; diffusion : memes fenetres t = 8..128 que le contre-audit ; prediction enregistree : regime ramifie (d_s ~ 1,4).
import sys, math
exec(open('v1_b.py').read().split("R=int(sys.argv[1])")[0])
dstar=2*math.pi/math.acos(1/3); f=lambda n:-0.4*math.log(1+n)+0.05*(n-dstar)**2
def run(nb,sweeps,seed):
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
    nv=4
    for b in range(nb):
        t=L[rng.randrange(len(L))]; rem(t)
        for m in range(4): add(tuple(nv if i==m else t[i] for i in range(4)))
        nv+=1
    N0=len(L); out={}; acc=[0,0]; marks=sorted(sweeps); step=0
    for target in marks:
        while step<target*N0:
            step+=1; N=len(L); t=L[rng.randrange(N)]
            if rng.random()<0.5:
                k=rng.randrange(4); fc=tuple(v for i,v in enumerate(t) if i!=k); ts=F[fc]
                if len(ts)!=2: continue
                t1,t2=tuple(ts); x=(set(t1)-set(fc)).pop(); y=(set(t2)-set(fc)).pop(); e=tuple(sorted((x,y)))
                if e in E: continue
                dS=3+f(3)
                for pr in itertools.combinations(fc,2): n=len(E[pr]); dS+=f(n-1)-f(n)
                for u in (x,y):
                    for a in fc: n=len(E[tuple(sorted((u,a)))]); dS+=f(n+1)-f(n)
                if rng.random()<min(1.0,math.exp(-dS)*N/(N+1)):
                    rem(t1); rem(t2)
                    for pr in itertools.combinations(fc,2): add(pr+(x,y))
                    acc[0]+=1
            else:
                e=tuple(sorted(rng.sample(t,2))); ts=E[e]
                if len(ts)!=3: continue
                link=sorted(set().union(*map(set,ts))-set(e))
                if len(link)!=3 or tuple(link) in F: continue
                dS=-3-f(3)
                for pr in itertools.combinations(link,2): n=len(E[pr]); dS+=f(n+1)-f(n)
                for u in e:
                    for a in link: n=len(E[tuple(sorted((u,a)))]); dS+=f(n-1)-f(n)
                if rng.random()<min(1.0,math.exp(-dS)*N/(N-1)):
                    for tt in list(ts): rem(tt)
                    add(tuple(link)+(e[0],)); add(tuple(link)+(e[1],)); acc[1]+=1
        A=dual(L,F); n=A.shape[0]
        d=shortest_path(A,unweighted=True,indices=np.random.default_rng(seed).choice(n,min(30,n),replace=False))
        out[target]=(n,acc[0],acc[1],d[np.isfinite(d)].mean(),list(ds(A,ts=(8,16,32,64,128)).values()))
    assert max(len(v) for v in F.values())<=2
    return N0,out
nb=int(sys.argv[1]); res={}
for seed in (300,301,302):
    N0,o=run(nb,(0,50,200,800),seed)
    for k,v in o.items(): res.setdefault(k,[]).append(v)
for k,v in res.items():
    print(f'naissances={nb} tétras initiaux={N0} balayages={k}: tétras={np.mean([x[0] for x in v]):.0f} acceptés 2→3={np.mean([x[1] for x in v]):.0f} 3→2={np.mean([x[2] for x in v]):.0f} distance={np.mean([x[3] for x in v]):.1f} d_s(8,16,32,64,128)={np.round(np.mean([x[4] for x in v],axis=0),2).tolist()}')
