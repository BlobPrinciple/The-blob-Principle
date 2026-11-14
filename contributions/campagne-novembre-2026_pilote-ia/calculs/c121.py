# C-121 — MITOSE IMPOSEE PAR L'INSTINCT, LIEU CHOISI PAR LA TENSION (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Motif : C-120/PR-1 montre que des ressorts seuls ne DECLENCHENT jamais une naissance depuis l'equilibre. Dans la cosmogonie, la mitose n'attend pas
#   un gain d'energie : c'est l'instinct du simplexe ("etre, maintenant et eternellement"). La tension ne ferait que choisir le LIEU.
# Regle confirmee par Rudolphe (12 nov., 12 h 25) : U, les fils nes d'une division gardent la longueur naturelle commune l0 = 1.
# Modele, sans parametre libre :
#   - un ressort par arete distincte, E = 1/2 Somme (l - 1)^2 ; la trame est maintenue a son equilibre homothetique (echelle s = Somme L / Somme L^2) ;
#   - naissances uniformes dans l'espace : la cellule est tiree avec une probabilite proportionnelle a son volume ;
#   - parmi ses six fils, celui dont la division coute le moins d'energie elastique a l'insertion (patch complet) recoit le porteur, en son milieu ;
#   - bras T : avec propagation (si une cellule voisine autour de ce fil a un fil moins couteux, elle se divise d'abord) ; bras T0 : sans propagation.
# Germe de Kuhn. Cibles 4 096 et 32 768 cellules ; graines 1600-1605. Temoins : S1 et A6 de C-116 (memes instruments).
# Mesures : degre maximal ; qualite minimale des cellules (volume / diametre^3 ; S1 : 0,0295) ; part des naissances sur le fil le plus long de la cellule tiree ;
#   distance du germe (en fils) ; distance duale ; d_s ; facteur d'echelle physique s ; energie residuelle par arete.
# CRITERE : celui de C-116 (profil d_s a 0,3 de S1, distance duale a 30 %, aux deux tailles) ET qualite minimale >= 0,003 ET degre maximal <= 40.
# PREDICTION ENREGISTREE : T et T0 FAIL (cellules degenerees, moyeux) ; part du fil le plus long entre 40 % et 80 %.
import sys, math, json, random, itertools
import numpy as np
from multiprocessing import Pool
import c114, c116
def run(args):
    arm,target,seed=args; rng=random.Random(seed); L=[]; pos={}; F={}; E={}; EL={}; S=[0.0,0.0]
    P=[(0.,0.,0.),(1.,0.,0.),(1.,1.,0.),(1.,1.,1.)]
    def dist(a,b): p,q=P[a],P[b]; return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2)
    def add(t):
        t=tuple(sorted(t)); pos[t]=len(L); L.append(t)
        for x in itertools.combinations(t,3): F.setdefault(x,set()).add(t)
        for x in itertools.combinations(t,2):
            if x not in E: E[x]=set(); l=dist(*x); EL[x]=l; S[0]+=l; S[1]+=l*l
            E[x].add(t)
    def rem(t):
        i=pos.pop(t); last=L.pop()
        if last!=t: L[i]=last; pos[last]=i
        for x in itertools.combinations(t,3):
            F[x].discard(t)
            if not F[x]: del F[x]
        for x in itertools.combinations(t,2):
            E[x].discard(t)
            if not E[x]: del E[x]; l=EL.pop(x); S[0]-=l; S[1]-=l*l
    add((0,1,2,3)); nv=4; nb=0; stat=[0,0,0]
    def bisect(e):
        nonlocal nv,nb
        a,b=e; m=nv; nv+=1; nb+=1; ts=list(E[e]); p,q=P[a],P[b]; P.append(((p[0]+q[0])/2,(p[1]+q[1])/2,(p[2]+q[2])/2))
        for t in ts: rem(t)
        for t in ts:
            o=tuple(v for v in t if v!=a and v!=b); add((a,m)+o); add((b,m)+o)
    def dEi(e):
        s=S[0]/S[1]; a,b=e; p,q=P[a],P[b]; m=((p[0]+q[0])/2,(p[1]+q[1])/2,(p[2]+q[2])/2); l=EL[e]; tot=2*(s*l/2-1)**2-(s*l-1)**2
        for x in set(v for t in E[e] for v in t if v!=a and v!=b):
            r=P[x]; tot+=(s*math.sqrt((r[0]-m[0])**2+(r[1]-m[1])**2+(r[2]-m[2])**2)-1)**2
        return 0.5*tot
    def best(t): return min(((round(dEi(e),12),-EL[e],e) for e in itertools.combinations(t,2)))
    def vol(t):
        a,b,c,d=(P[v] for v in t); u=[b[i]-a[i] for i in range(3)]; v=[c[i]-a[i] for i in range(3)]; w=[d[i]-a[i] for i in range(3)]
        return abs(u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]))
    vb=[1.0]
    def pick():
        rej=0
        while True:
            t=L[rng.randrange(len(L))]; x=vol(t)
            if x>vb[0]: vb[0]=x
            if rng.random()<x/vb[0]: return t
            rej+=1
            if rej>60: vb[0]=max(vol(q) for q in L); rej=0
    while len(L)<target:
        t=pick(); lmax=max(EL[e] for e in itertools.combinations(t,2))
        if arm=='T0':
            v,_,e=best(t); stat[0]+=1; stat[1]+=EL[e]>=lmax-1e-12; bisect(e)
        else:
            # ECART DECLARE APRES PILOTE : la boucle "jusqu'a ce que la cellule tiree soit divisee" ne termine pas (le fil le moins couteux change apres
            # chaque naissance). Regle retenue : UNE naissance par tirage, au bout de la chaine de propagation (au plus 200 pas).
            cur=t; steps=0
            while True:
                v,_,e=best(cur); nxt=None
                for t2 in E[e]:
                    v2,_,e2=best(t2)
                    if v2<v-1e-12: v=v2; nxt=t2
                if nxt is None or steps>=200: break
                cur=nxt; steps+=1
            stat[0]+=1; stat[1]+=(cur==t and EL[e]>=lmax-1e-12); stat[2]+=steps; bisect(e)
    s=S[0]/S[1]; lmin=min(EL.values()); q=np.array([vol(t)/6/max(EL[e] for e in itertools.combinations(t,2))**3 for t in L])
    extra=dict(arm=arm,target=target,seed=seed,naissances=nb,acc=[0,0],echelle=s,alpha=1/(s*lmin),qmin=float(q.min()),q5=float(np.percentile(q,5)),qmed=float(np.median(q)),
               part_plus_long=stat[1]/max(1,stat[0]),residuel=0.5*(1-S[0]**2/(len(EL)*S[1])),rapport_longueurs=max(EL.values())/lmin)
    return c116.finish(L,F,E,nv,seed,extra)
if __name__=='__main__':
    targets=[int(x) for x in sys.argv[1].split(',')]; ns=int(sys.argv[2])
    jobs=[(a,tg,s) for tg in targets for a in ('T','T0') for s in range(1600,1600+ns)]
    with Pool(2) as p: res=p.map(run,jobs,chunksize=1)
    json.dump(res,open(f'c121_{sys.argv[1].replace(",","_")}.json','w'))
    for a in ('T','T0'):
        for tg in targets:
            rs=[x for x in res if x['arm']==a and x['target']==tg]; m=lambda k:np.mean([x[k] for x in rs])
            print(f'{a} cible={tg} (n={len(rs)}): tétras={m("N3"):.0f} sommets={m("nv"):.0f} degré max={m("degmax"):.0f} p99={m("deg99"):.0f} qmin={m("qmin"):.5f} q5%={m("q5"):.4f} qméd={m("qmed"):.4f} part fil le plus long={100*m("part_plus_long"):.1f} % alpha={m("alpha"):.3f} Lmax/Lmin={m("rapport_longueurs"):.1f} résiduel/arête={m("residuel"):.4f} échelle s={m("echelle"):.2f} germe={m("germe"):.1f} dist duale={m("dist"):.1f} sommets={m("distv"):.1f} d_s dual={np.round(np.mean([x["dsd"] for x in rs],axis=0),2).tolist()} d_s sommets={np.round(np.mean([x["dsv"] for x in rs],axis=0),2).tolist()}',flush=True)
