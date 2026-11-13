# C-114 — TOURNOI DES LOIS DE LOCALITE (Claude, 11 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Question : quelle regle, exprimee avec les seules grandeurs du Blob (valence, age, courbure, ressources), maintient les distances ?
# Commun : une lignee (boule), naissance = subdivision 1->4, reorganisations = Pachner 2<->3 legaux ; 128, 512, 2048 naissances ;
#   graines 1200-1207 ; R = 100 tentatives de reorganisation par naissance (sauf L0, L4a, L4b).
# Bras :
#  L0  temoin : naissances uniformes, aucune reorganisation.
#  L1a rigidite de courbure : Metropolis sur S = kappa * somme_aretes (n_e - d*)^2, kappa = 0,05 (valeur du master).
#  L1b idem kappa = 1.            L1c idem, descente stricte (accepte ssi dS <= 0).
#  L2  naissance selective : parent = celui des 8 candidats uniformes qui minimise dS ; reorganisation comme L1b.
#  L3  plafond de ressources : aucun sommet ne depasse le degre 20 (naissances et mouvements refuses sinon) ; reorganisation libre.
#  L4a paliers : naissance toujours dans le tetraedre le plus ancien, aucune reorganisation.
#  L4b paliers + courbure compensee (regle C-112 : 2->3 legaux uniformes jusqu'a arrondi(r n)).
# Mesures : d_s (graphe dual ET graphe des sommets, t = 8..128), distance moyenne duale, d_H = ln(N2/N1)/ln(D2/D1) entre 512 et 2048.
# Temoin d'instrument : cube triangule de Freudenthal (vraie 3D a bord), memes mesures.
# SUCCES : a 2048 naissances, d_s dual ET sommets dans 3 +/- 0,3 pour t = 8..64, stables entre 512 et 2048 aux echelles communes,
#   ET d_H dans 3 +/- 0,5. Sinon FAIL. PREDICTION ENREGISTREE : FAIL pour tous les bras ; L1c gele ; L3 et L4 restent ramifies.
# AMENDEMENT (apres le temoin d'instrument, AVANT tout resultat de bras) : le cube de Freudenthal, vraie 3D a bord, ne donne lui-meme
#   que d_s dual 2,3-2,9 et d_s sommets 3,1->2,2 a ces tailles (effets de bord). Le critere absolu 3 +/- 0,3 est donc inatteignable
#   meme par une vraie 3D. CRITERE AMENDE : profil d_s (dual ET sommets, t = 8..64) a moins de 0,3 du temoin de taille comparable,
#   ET distance duale moyenne a moins de 30 % de celle du temoin, ET tenue de 2048 a 8192 naissances (taille ajoutee : 8192).
import sys, math, json, random, itertools, heapq
import numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path
from multiprocessing import Pool
exec(open('v1_audit.py').read().split("if __name__")[0].split("import sys, random, itertools, numpy as np, scipy.sparse as sp")[1].split("def cubic")[0])
th=math.acos(1/3); dstar=2*math.pi/th; r=(8*math.pi-18*th)/(6*th-2*math.pi); TS=(8,16,32,64,128)
def vgraph(nv,edges):
    e=np.array(edges); A=sp.csr_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(nv,nv)); return ((A+A.T)>0).astype(float).tocsr()
def measure(L,F,E,nv,seed):
    A=dual(L,F); N=A.shape[0]; V=vgraph(nv,list(E.keys()))
    d=shortest_path(A,unweighted=True,indices=np.random.default_rng(seed).choice(N,min(30,N),replace=False))
    dv=shortest_path(V,unweighted=True,indices=np.random.default_rng(seed).choice(nv,min(30,nv),replace=False))
    val=np.array([len(v) for v in E.values()]); deg=np.array(V.sum(1)).ravel()
    return dict(N3=N,nv=nv,dist=float(d[np.isfinite(d)].mean()),distv=float(dv.mean()),dsd=[float(x) for x in ds(A,ts=TS).values()],
                dsv=[float(x) for x in ds(V,ts=TS).values()],nmean=float(val.mean()),degmax=int(deg.max()),
                manifold=max(len(v) for v in F.values())<=2,euler=nv-len(E)+len(F)-N)
def run(args):
    nb,seed,arm=args; rng=random.Random(seed); L=[]; pos={}; F={}; E={}; deg={}; stamp={}; heap=[]; cnt=[0]
    kappa={'L1a':0.05,'L1b':1.0,'L1c':1.0,'L2':1.0}.get(arm,0.0); f=lambda n:kappa*(n-dstar)**2
    def add(t):
        t=tuple(sorted(t)); pos[t]=len(L); L.append(t); cnt[0]+=1; stamp[t]=cnt[0]; heapq.heappush(heap,(cnt[0],t))
        for x in itertools.combinations(t,3): F.setdefault(x,set()).add(t)
        for x in itertools.combinations(t,2):
            if x not in E: E[x]=set(); deg[x[0]]=deg.get(x[0],0)+1; deg[x[1]]=deg.get(x[1],0)+1
            E[x].add(t)
    def rem(t):
        i=pos.pop(t); last=L.pop(); del stamp[t]
        if last!=t: L[i]=last; pos[last]=i
        for x in itertools.combinations(t,3):
            F[x].discard(t)
            if not F[x]: del F[x]
        for x in itertools.combinations(t,2):
            E[x].discard(t)
            if not E[x]: del E[x]; deg[x[0]]-=1; deg[x[1]]-=1
    add((0,1,2,3)); nv=4; m=0; acc=[0,0]; refus=0
    def birth(t):
        nonlocal nv
        rem(t)
        for k in range(4): add(tuple(nv if i==k else t[i] for i in range(4)))
        nv+=1
    def try23(t,metro):
        k=rng.randrange(4); fc=tuple(v for i,v in enumerate(t) if i!=k); ts=F[fc]
        if len(ts)!=2: return False
        t1,t2=tuple(ts); x=(set(t1)-set(fc)).pop(); y=(set(t2)-set(fc)).pop(); e=tuple(sorted((x,y)))
        if e in E: return False
        if arm=='L3' and (deg[x]>=20 or deg[y]>=20): return False
        if metro:
            dS=f(3)
            for pr in itertools.combinations(fc,2): n=len(E[pr]); dS+=f(n-1)-f(n)
            for u in (x,y):
                for a in fc: n=len(E[tuple(sorted((u,a)))]); dS+=f(n+1)-f(n)
            if arm=='L1c':
                if dS>0: return False
            elif rng.random()>=math.exp(-max(dS,0.0)): return False
        rem(t1); rem(t2)
        for pr in itertools.combinations(fc,2): add(pr+(x,y))
        return True
    def try32(t,metro):
        e=tuple(sorted(rng.sample(t,2))); ts=E[e]
        if len(ts)!=3: return False
        link=sorted(set().union(*map(set,ts))-set(e))
        if len(link)!=3 or tuple(link) in F: return False
        if metro:
            dS=-f(3)
            for pr in itertools.combinations(link,2): n=len(E[pr]); dS+=f(n+1)-f(n)
            for u in e:
                for a in link: n=len(E[tuple(sorted((u,a)))]); dS+=f(n-1)-f(n)
            if arm=='L1c':
                if dS>0: return False
            elif rng.random()>=math.exp(-max(dS,0.0)): return False
        for tt in list(ts): rem(tt)
        add(tuple(link)+(e[0],)); add(tuple(link)+(e[1],)); return True
    def dSbirth(t): return 4*f(3)+sum(f(len(E[x])+1)-f(len(E[x])) for x in itertools.combinations(t,2))
    for n in range(1,nb+1):
        if arm in ('L4a','L4b'):
            while True:
                s,t=heapq.heappop(heap)
                if stamp.get(t)==s: break
        elif arm=='L2':
            t=min((L[rng.randrange(len(L))] for _ in range(8)),key=dSbirth)
        elif arm=='L3':
            for _ in range(5000):
                t=L[rng.randrange(len(L))]
                if max(deg[v] for v in t)<20: break
            else: refus+=1; break
        else: t=L[rng.randrange(len(L))]
        birth(t)
        if arm in ('L1a','L1b','L1c','L2','L3'):
            for _ in range(100):
                t=L[rng.randrange(len(L))]
                if rng.random()<0.5: acc[0]+=try23(t,arm!='L3')
                else: acc[1]+=try32(t,arm!='L3')
        if arm=='L4b':
            target=round(r*n); tries=0
            while m<target and tries<2000:
                tries+=1
                if try23(L[rng.randrange(len(L))],False): m+=1; tries=0
    out=measure(L,F,E,nv,seed); out.update(nb=nb,seed=seed,arm=arm,acc=acc,arret=refus,naissances=nv-4); return out
def freudenthal(Lc):
    idx=lambda p:(p[0]*(Lc+1)+p[1])*(Lc+1)+p[2]; L=[];F={};E={}
    for c in itertools.product(range(Lc),repeat=3):
        for perm in itertools.permutations(range(3)):
            p=list(c); t=[idx(p)]
            for a in perm: p[a]+=1; t.append(idx(p))
            t=tuple(sorted(t)); L.append(t)
            for x in itertools.combinations(t,3): F.setdefault(x,set()).add(t)
            for x in itertools.combinations(t,2): E.setdefault(x,set()).add(t)
    return measure(L,F,E,(Lc+1)**3,0)
ARMS=('L0','L1a','L1b','L1c','L2','L3','L4a','L4b')
if __name__=='__main__':
    if sys.argv[1]=='temoin':
        prev=None
        for Lc in (8,12,16,20):
            o=freudenthal(Lc); dh='' if prev is None else f' d_H={np.log(o["N3"]/prev["N3"])/np.log(o["dist"]/prev["dist"]):.2f}'
            print(f'Freudenthal L={Lc}: tétras={o["N3"]} sommets={o["nv"]} d_s dual={np.round(o["dsd"],2).tolist()} d_s sommets={np.round(o["dsv"],2).tolist()} distance duale={o["dist"]:.1f}{dh}',flush=True); prev=o
    else:
        jobs=[(nb,s,a) for nb in (128,512,2048,8192) for s in range(1200,1208) for a in ARMS]
        with Pool(2) as p: res=p.map(run,jobs,chunksize=1)
        json.dump(res,open('c114.json','w'))
        for a in ARMS:
            D={}
            for nb in (128,512,2048,8192):
                rs=[x for x in res if x['nb']==nb and x['arm']==a]; D[nb]=(np.mean([x['N3'] for x in rs]),np.mean([x['dist'] for x in rs]))
                print(f'{a} n={nb}: nés={np.mean([x["naissances"] for x in rs]):.0f} tétras={D[nb][0]:.0f} acc={np.mean([x["acc"] for x in rs],axis=0).round(0).tolist()} valence={np.mean([x["nmean"] for x in rs]):.2f} degré max={np.mean([x["degmax"] for x in rs]):.0f} variété={all(x["manifold"] for x in rs)} Euler={set(x["euler"] for x in rs)} dist duale={D[nb][1]:.1f} sommets={np.mean([x["distv"] for x in rs]):.1f} d_s dual={np.round(np.mean([x["dsd"] for x in rs],axis=0),2).tolist()} d_s sommets={np.round(np.mean([x["dsv"] for x in rs],axis=0),2).tolist()}')
            print(f'   d_H(512→2048) = {np.log(D[2048][0]/D[512][0])/np.log(D[2048][1]/D[512][1]):.2f} ; d_H(2048→8192) = {np.log(D[8192][0]/D[2048][0])/np.log(D[8192][1]/D[2048][1]):.2f}',flush=True)
