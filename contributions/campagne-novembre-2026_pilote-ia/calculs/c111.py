# C-111 / PR-1 (fige par ChatGPT) — campagne d'exploration, executee par Claude.
# ECARTS DECLARES (budget de calcul) : graines 600-605 pour 84 et 324 sommets (400 balayages, mesures sur la 2e moitie) ;
# graines 600-601 et 150 balayages pour 1 284 sommets ; pas d'hysteresis ni d'autocorrelation formelle ; campagne de confirmation non lancee.
import sys, math, json
from multiprocessing import Pool
exec(open('v1_b.py').read().split("R=int(sys.argv[1])")[0])
dstar=2*math.pi/math.acos(1/3)
def run(args):
    nb,lam,seed,nsw=args; f=lambda n:-lam*math.log(1+n)+0.05*(n-dstar)**2
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
    N0=len(L); lo=[]; n3=[]
    for sw in range(nsw):
        for _ in range(N0):
            N=len(L); t=L[rng.randrange(N)]
            if rng.random()<0.5:
                k=rng.randrange(4); fc=tuple(v for i,v in enumerate(t) if i!=k); ts=F[fc]
                if len(ts)!=2: continue
                t1,t2=tuple(ts); x=(set(t1)-set(fc)).pop(); y=(set(t2)-set(fc)).pop(); e=tuple(sorted((x,y)))
                if e in E: continue
                dS=3+f(3)
                for pr in itertools.combinations(fc,2): n=len(E[pr]); dS+=f(n-1)-f(n)
                for u in (x,y):
                    for a in fc: n=len(E[tuple(sorted((u,a)))]); dS+=f(n+1)-f(n)
                if dS<0 or rng.random()<math.exp(-dS)*N/(N+1):
                    rem(t1); rem(t2)
                    for pr in itertools.combinations(fc,2): add(pr+(x,y))
            else:
                e=tuple(sorted(rng.sample(t,2))); ts=E[e]
                if len(ts)!=3: continue
                link=sorted(set().union(*map(set,ts))-set(e))
                if len(link)!=3 or tuple(link) in F: continue
                dS=-3-f(3)
                for pr in itertools.combinations(link,2): n=len(E[pr]); dS+=f(n+1)-f(n)
                for u in e:
                    for a in link: n=len(E[tuple(sorted((u,a)))]); dS+=f(n-1)-f(n)
                if dS<0 or rng.random()<math.exp(-dS)*N/(N-1):
                    for tt in list(ts): rem(tt)
                    add(tuple(link)+(e[0],)); add(tuple(link)+(e[1],))
        if sw>=nsw//2: lo.append(sum(math.log(1+len(v)) for v in E.values())); n3.append(len(L))
    A=dual(L,F); n=A.shape[0]
    d=shortest_path(A,unweighted=True,indices=np.random.default_rng(seed).choice(n,min(30,n),replace=False))
    return dict(nb=nb,lam=lam,seed=seed,N0=N0,lnO=lo,n3=n3,dist=float(d[np.isfinite(d)].mean()),ds=[float(x) for x in ds(A,ts=(8,16,32,64,128)).values()],manifold=max(len(v) for v in F.values())<=2)
if __name__=='__main__':
    LAM=[0,0.2,0.4,0.6,0.8,1,1.5,2,3,4,6,8,12,16]
    nb=int(sys.argv[1]); seeds=[int(x) for x in sys.argv[2].split(',')]; nsw=int(sys.argv[3])
    jobs=[(nb,l,s,nsw) for l in LAM for s in seeds]
    with Pool(int(sys.argv[4])) as p: res=p.map(run,jobs)
    json.dump(res,open(f'c111_{nb}.json','w')); print('fini',nb)
