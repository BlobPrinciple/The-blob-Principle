# C-116 — LA MITOSE DE L'ARETE (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Constat [T] : sous naissances 1->4 et mouvements 2->3, aucune arete n'est jamais subdivisee ; la distance entre porteurs existants
#   ne croit jamais (sauf +1 au plus par mouvement 3->2). Aucune expansion n'est possible. Or la cosmogonie dit : "l'univers s'etoffe
#   partout en meme temps et s'etire via l'arete", "plus il y a de monde sur le fil, plus le fil s'allonge", "N_g = 2^g".
# Traduction testee : mitose = un nouveau porteur nait SUR une arete (bissection) ; chaque cellule autour de l'arete se divise en DEUX.
# Germe : un tetraedre (0,1,2,3) dont les aretes ont un ordre de naissance 03,02,13,01,12,23 (choix declare ; controle : ordre tire au hasard).
# Bras (cible : 4 096 puis 32 768 tetraedres ; 6 graines 1500-1505 pour les bras aleatoires) :
#  S1 paliers : a chaque generation, chaque cellule se divise une fois, sur sa plus ancienne arete, avec propagation
#     (une arete ne se divise que si elle est la plus ancienne de toutes les cellules qui la portent ; sinon la cellule voisine se divise d'abord).
#  S1r idem, ordre de naissance des aretes du germe tire au hasard.
#  S2 paliers 1->8 (toutes les aretes divisees), diagonale de l'octaedre (= canal de K4) tiree au hasard dans chaque cellule.
#  A1 arete tiree uniformement, sans regle d'age.        A2 horloge du porteur : sommet uniforme, puis une de ses aretes au hasard.
#  A3 horloge de la cellule : cellule uniforme, division sur sa plus ancienne arete, SANS propagation.
#  A4 horloge de la cellule : cellule uniforme, division sur sa plus ancienne arete, AVEC propagation (S1 asynchrone).
#  A5 = A1 + 100 tentatives de reorganisation 2<->3 par naissance sous rigidite kappa = 1 (regle L1b de C-114).
#  M1 melange : une fois sur deux A4, une fois sur deux naissance 1->4 dans une cellule uniforme.
#  L0 naissances 1->4 seules (ancien modele), pour le controle des distances.
# Mesures : instrument de C-114 (d_s dual et sommets, t = 8..128 ; distance duale moyenne) ; degre maximal ; distance entre les 4 porteurs du germe.
# TEMOIN : S1 lui-meme est, par construction, la triangulation d'un tetraedre euclidien (3D conservee, non emergente) ; temoin cubique de C-114 rappele.
# CRITERE (forme amendee de C-114) : profil d_s (dual ET sommets, t = 8..64) a moins de 0,3 de S1 a taille egale, distance duale a moins de 30 %,
#   aux deux tailles. Le critere absolu 3 +/- 0,3 est conserve dans l'archive et reste inatteignable a ces tailles (C-114).
# PREDICTIONS ENREGISTREES : S1r = S1 ; S2 PASS ; A1, A2, A3 FAIL (moyeux) ; A4 PASS ; A5 FAIL ; M1 FAIL ; L0 FAIL et distance du germe = 1.
# AMENDEMENT DECLARE APRES PILOTE (512 cellules, avant toute campagne) : la regle "plus ancienne arete" ne redonne PAS le raffinement
#   regulier (contre-exemple exact : cellule [z'',z',z,w], l'arete la plus ancienne z'z est plus courte que z''z). Ma croyance a priori etait fausse.
#   La regle metrique "l'arete la plus LONGUE (la plus etiree) se divise", avec naissance au milieu du fil, est ajoutee comme bras distincts ;
#   les bras d'age sont conserves tels que preenregistres et renommes S1a, S1ar, A3a, A4a. Bras ajoutes (longueur, ex aequo -> la plus ancienne) :
#   S1 (germe de Kuhn (0,0,0),(1,0,0),(1,1,0),(1,1,1)), S1g (germe regulier), A3, A4 (germe de Kuhn), A4g (germe regulier) ; M1 utilise A4.
#   TEMOIN = S1 (longueur, germe de Kuhn). Predictions ajoutees : S1 = reseau de Kuhn exact ; S1g PASS ; A3 FAIL ; A4, A4g PASS ; S1a, A3a, A4a FAIL.
# BRAS AJOUTE APRES C-116 bis (declare) : A6 = A4 mais la cellule est tiree avec une probabilite proportionnelle a son VOLUME
#   ("l'univers s'etoffe partout en meme temps" = naissances uniformes dans l'espace, et non une horloge par cellule).
#   PREDICTION ENREGISTREE AVANT CALCUL : degre maximal <= 34, distances a moins de 15 % de S1 aux trois tailles (4 096, 32 768, 262 144) : PASS.
import sys, math, json, random, itertools
import numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path
from multiprocessing import Pool
import c114
dstar=c114.dstar
def finish(L,F,E,nv,seed,extra):
    out=c114.measure(L,F,E,nv,seed); V=c114.vgraph(nv,list(E.keys()))
    d=shortest_path(V,unweighted=True,indices=[0,1,2,3])[:,[0,1,2,3]]; out['germe']=float(d[np.triu_indices(4,1)].mean())
    deg=np.array(V.sum(1)).ravel(); out['degmoy']=float(deg.mean()); out['deg99']=float(np.percentile(deg,99)); out.update(extra); return out
def run(args):
    arm,target,seed=args; rng=random.Random(seed); L=[]; pos={}; F={}; E={}; stamp={}; cnt=[0]; EL=[]; epos={}; nbr={}; elen={}
    byage=arm in ('S1a','S1ar','A3a','A4a')
    P=[(1.,1.,1.),(1.,-1.,-1.),(-1.,1.,-1.),(-1.,-1.,1.)] if arm in ('S1g','A4g') else [(0.,0.,0.),(1.,0.,0.),(1.,1.,0.),(1.,1.,1.)]
    def key(x):
        if byage: return (0.0,stamp[x])
        l=elen.get(x)
        if l is None:
            p,q=P[x[0]],P[x[1]]; l=elen[x]=-((p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2)
        return (l,stamp[x])
    f=lambda n:(n-dstar)**2
    def add(t):
        t=tuple(sorted(t)); pos[t]=len(L); L.append(t)
        for x in itertools.combinations(t,3): F.setdefault(x,set()).add(t)
        for x in itertools.combinations(t,2):
            if x not in E:
                E[x]=set(); epos[x]=len(EL); EL.append(x); nbr.setdefault(x[0],set()).add(x[1]); nbr.setdefault(x[1],set()).add(x[0])
                if x not in stamp: cnt[0]+=1; stamp[x]=cnt[0]
            E[x].add(t)
    def rem(t):
        i=pos.pop(t); last=L.pop()
        if last!=t: L[i]=last; pos[last]=i
        for x in itertools.combinations(t,3):
            F[x].discard(t)
            if not F[x]: del F[x]
        for x in itertools.combinations(t,2):
            E[x].discard(t)
            if not E[x]:
                del E[x]; i=epos.pop(x); last=EL.pop()
                if last!=x: EL[i]=last; epos[last]=i
                nbr[x[0]].discard(x[1]); nbr[x[1]].discard(x[0])
    order=[(0,3),(0,2),(1,3),(0,1),(1,2),(2,3)]
    if arm=='S1ar': rng.shuffle(order)
    for e in order: cnt[0]+=1; stamp[e]=cnt[0]
    add((0,1,2,3)); nv=4; acc=[0,0]; nb=0
    def bisect(e):
        nonlocal nv,nb
        a,b=e; m=nv; nv+=1; nb+=1; ts=list(E[e]); p,q=P[a],P[b]; P.append(((p[0]+q[0])/2,(p[1]+q[1])/2,(p[2]+q[2])/2)); elen.pop(e,None)
        cnt[0]+=1; stamp[(a,m)]=cnt[0]; cnt[0]+=1; stamp[(b,m)]=cnt[0]
        for t in ts: rem(t)
        stamp.pop(e,None)
        for t in ts:
            o=tuple(v for v in t if v!=a and v!=b); add((a,m)+o); add((b,m)+o)
    def oldest(t): return min(itertools.combinations(t,2),key=key)
    def divide(t):
        while t in pos:
            cur=t
            while True:
                e=oldest(cur); best=key(e); nxt=None
                for t2 in E[e]:
                    s2=key(oldest(t2))
                    if s2<best: best=s2; nxt=t2
                if nxt is None: bisect(e); break
                cur=nxt
    vb=[1.0]
    def vol(t):
        a,b,c,d=(P[v] for v in t); u=[b[i]-a[i] for i in range(3)]; v=[c[i]-a[i] for i in range(3)]; w=[d[i]-a[i] for i in range(3)]
        return abs(u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]))
    def pick_vol():
        rej=0
        while True:
            t=L[rng.randrange(len(L))]; x=vol(t)
            if x>vb[0]: vb[0]=x
            if rng.random()<x/vb[0]: return t
            rej+=1
            if rej>60: vb[0]=max(vol(q) for q in L); rej=0
    def birth14():
        nonlocal nv,nb
        t=L[rng.randrange(len(L))]; rem(t); P.append(tuple(sum(P[v][i] for v in t)/4 for i in range(3)))
        for k in range(4): add(tuple(nv if i==k else t[i] for i in range(4)))
        nv+=1; nb+=1
    def relax():
        for _ in range(100):
            t=L[rng.randrange(len(L))]
            if rng.random()<0.5:
                k=rng.randrange(4); fc=tuple(v for i,v in enumerate(t) if i!=k); ts=F[fc]
                if len(ts)!=2: continue
                t1,t2=tuple(ts); x=(set(t1)-set(fc)).pop(); y=(set(t2)-set(fc)).pop(); e=tuple(sorted((x,y)))
                if e in E: continue
                dS=f(3)
                for pr in itertools.combinations(fc,2): n=len(E[pr]); dS+=f(n-1)-f(n)
                for u in (x,y):
                    for a in fc: n=len(E[tuple(sorted((u,a)))]); dS+=f(n+1)-f(n)
                if rng.random()>=math.exp(-max(dS,0.0)): continue
                rem(t1); rem(t2)
                for pr in itertools.combinations(fc,2): add(pr+(x,y))
                acc[0]+=1
            else:
                e=tuple(sorted(rng.sample(t,2))); ts=E[e]
                if len(ts)!=3: continue
                link=sorted(set().union(*map(set,ts))-set(e))
                if len(link)!=3 or tuple(link) in F: continue
                dS=-f(3)
                for pr in itertools.combinations(link,2): n=len(E[pr]); dS+=f(n+1)-f(n)
                for u in e:
                    for a in link: n=len(E[tuple(sorted((u,a)))]); dS+=f(n-1)-f(n)
                if rng.random()>=math.exp(-max(dS,0.0)): continue
                for tt in list(ts): rem(tt)
                stamp.pop(e,None); elen.pop(e,None)
                add(tuple(link)+(e[0],)); add(tuple(link)+(e[1],)); acc[1]+=1
    if arm in ('S1','S1g','S1a','S1ar'):
        gen=0
        while len(L)<target:
            for t in list(L):
                if t in pos: divide(t)
            gen+=1
        extra=dict(generations=gen)
    else:
        while len(L)<target:
            if arm=='A1' or arm=='A5':
                bisect(EL[rng.randrange(len(EL))])
                if arm=='A5': relax()
            elif arm=='A2':
                v=rng.randrange(nv); w=rng.choice(sorted(nbr[v])); bisect((min(v,w),max(v,w)))
            elif arm in ('A3','A3a'): bisect(oldest(L[rng.randrange(len(L))]))
            elif arm in ('A4','A4a','A4g'): divide(L[rng.randrange(len(L))])
            elif arm=='A6': divide(pick_vol())
            elif arm=='M1':
                if rng.random()<0.5: divide(L[rng.randrange(len(L))])
                else: birth14()
            elif arm=='L0': birth14()
        extra={}
    extra.update(arm=arm,target=target,seed=seed,naissances=nb,acc=acc)
    return finish(L,F,E,nv,seed,extra)
def run_S2(args):
    arm,target,seed=args; rng=random.Random(seed); T=[(0,1,2,3)]; nv=4; g=0
    while len(T)<target:
        mid={}; new=[]
        def m(a,b):
            nonlocal nv
            k=(a,b) if a<b else (b,a)
            if k not in mid: mid[k]=nv; nv+=1
            return mid[k]
        for (a,b,c,d) in T:
            ab,ac,ad,bc,bd,cd=m(a,b),m(a,c),m(a,d),m(b,c),m(b,d),m(c,d)
            new+=[(a,ab,ac,ad),(b,ab,bc,bd),(c,ac,bc,cd),(d,ad,bd,cd)]
            p,q,ring=[(ab,cd,(ac,ad,bd,bc)),(ac,bd,(ab,ad,cd,bc)),(ad,bc,(ab,ac,cd,bd))][rng.randrange(3)]
            new+=[(p,q,ring[i],ring[(i+1)%4]) for i in range(4)]
        T=new; g+=1
    L=[tuple(sorted(t)) for t in T]; F={}; E={}
    for t in L:
        for x in itertools.combinations(t,3): F.setdefault(x,set()).add(t)
        for x in itertools.combinations(t,2): E.setdefault(x,set()).add(t)
    return finish(L,F,E,nv,seed,dict(arm=arm,target=target,seed=seed,naissances=nv-4,acc=[0,0],generations=g))
def job(a): return run_S2(a) if a[0]=='S2' else run(a)
ARMS=('S1','S1g','S1a','S1ar','S2','A1','A2','A3a','A4a','A3','A4','A4g','A6','A5','M1','L0')
if len(sys.argv)>3: ARMS=tuple(sys.argv[3].split(','))
def show(res,targets):
    for a in ARMS:
        for tg in targets:
            rs=[x for x in res if x['arm']==a and x['target']==tg]
            if not rs: continue
            mean=lambda k:np.mean([x[k] for x in rs])
            print(f'{a} cible={tg} (n={len(rs)}): tétras={mean("N3"):.0f} sommets={mean("nv"):.0f} valence={mean("nmean"):.2f} degré moy={mean("degmoy"):.1f} p99={mean("deg99"):.0f} max={mean("degmax"):.0f} variété={all(x["manifold"] for x in rs)} Euler={set(x["euler"] for x in rs)} germe={mean("germe"):.1f} dist duale={mean("dist"):.1f} sommets={mean("distv"):.1f} d_s dual={np.round(np.mean([x["dsd"] for x in rs],axis=0),2).tolist()} d_s sommets={np.round(np.mean([x["dsv"] for x in rs],axis=0),2).tolist()}',flush=True)
if __name__=='__main__':
    targets=[int(x) for x in sys.argv[1].split(',')]; seeds=range(1500,1500+int(sys.argv[2]))
    jobs=[(a,tg,s) for tg in targets for a in ARMS for s in (seeds if a not in ('S1','S1g','S1a') else [1500])]
    with Pool(2) as p: res=p.map(job,jobs,chunksize=1)
    json.dump(res,open(f'c116_{sys.argv[1].replace(",","_")}.json','w')); show(res,targets)
