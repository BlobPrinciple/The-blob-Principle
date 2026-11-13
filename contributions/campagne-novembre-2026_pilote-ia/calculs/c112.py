# C-112 / PR-1 (fige par ChatGPT) execute par Claude. Graines 900-915 ; 128, 512, 2048 naissances ; boule B^3 a bord fixe.
# Bras A : croissance seule. Bras B : apres chaque naissance, mouvements 2->3 legaux uniformes jusqu'a m(n)=arrondi(r n) ;
# si aucun mouvement legal n'est trouve en 2000 essais, la dette est conservee et comptee.
# ECART DECLARE : bras C (selection ponderee C-56) non execute, sa regle exacte etant dans le fichier PR-1 inaccessible.
import sys, math, json
from multiprocessing import Pool
exec(open('v1_b.py').read().split("R=int(sys.argv[1])")[0])
th=math.acos(1/3); r=(8*math.pi-18*th)/(6*th-2*math.pi)
def run(args):
    nb,seed,arm=args; rng=random.Random(seed); L=[(0,1,2,3)]; pos={(0,1,2,3):0}; F={}; E={}
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
    nv=4; m=0; debt_hist=[]
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
            if n in (1,2,3,4,5,6,7,8,10,16,32,64,128): debt_hist.append((n,target-m))
    A=dual(L,F); N=A.shape[0]
    d=shortest_path(A,unweighted=True,indices=np.random.default_rng(seed).choice(N,min(30,N),replace=False))
    val=np.array([len(v) for v in E.values()])
    curv=sum(2*math.pi-len(v)*th for e,v in E.items() if all(len(F[f])==2 for f in F if False))  # non utilise
    return dict(nb=nb,seed=seed,arm=arm,N3=N,m=m,debt=round(r*nb)-m,debt_hist=debt_hist,dist=float(d[np.isfinite(d)].mean()),
                ds=[float(x) for x in ds(A,ts=(8,16,32,64,128)).values()],nmean=float(val.mean()),nmax=int(val.max()),manifold=max(len(v) for v in F.values())<=2,
                euler=(nv-len(E)+len(F)-N))
if __name__=='__main__':
    jobs=[(nb,s,a) for nb in (128,512,2048) for s in range(900,916) for a in 'AB']
    with Pool(2) as p: res=p.map(run,jobs)
    json.dump(res,open('c112.json','w'))
    print('r =',r)
    for nb in (128,512,2048):
        for a in 'AB':
            rs=[x for x in res if x['nb']==nb and x['arm']==a]; D=np.array([x['ds'] for x in rs])
            print(f'bras {a} naissances={nb}: tétras={np.mean([x["N3"] for x in rs]):.0f} m={np.mean([x["m"] for x in rs]):.0f} dette finale max={max(x["debt"] for x in rs)} variété={all(x["manifold"] for x in rs)} Euler={set(x["euler"] for x in rs)} valence moyenne={np.mean([x["nmean"] for x in rs]):.2f} (max {max(x["nmax"] for x in rs)}) distance={np.mean([x["dist"] for x in rs]):.1f} d_s(8..128)={np.round(D.mean(0),2).tolist()} ±{np.round(D.std(0)/4,2).tolist()}')
    b=[x for x in res if x['arm']=='B' and x['nb']==128]
    print('dette de courbure (bras B) aux premières naissances, max sur 16 graines :',[(n,max(dict(x['debt_hist'])[n] for x in b)) for n in (1,2,3,4,5,6,7,8,10,16,32,64,128)])
