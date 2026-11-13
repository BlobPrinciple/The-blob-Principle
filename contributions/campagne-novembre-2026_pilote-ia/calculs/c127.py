# C-127 — SI L'ETIREMENT EST DONNE, LA TENSION SUFFIT-ELLE A FAIRE LA MITOSE REGULIERE ? (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Constat (C-120, C-121) : des ressorts seuls ne declenchent ni ne placent correctement les naissances a l'equilibre.
# Constat (C-119, audit C-120) : en trame etiree, la division du fil le plus long ABAISSE l'energie et c'est le premier fil a devenir favorable.
# Cosmogonie : l'arete est l'energie sombre, l'etirement est premier ("l'univers s'etire via l'arete").
# Modele, sans parametre libre : regle U (l0 = 1), un ressort par arete, E = 1/2 Somme (s L - 1)^2 ; le facteur d'echelle s est IMPOSE et croit
#   lentement (limite quasi statique : sa loi en temps n'intervient pas) ; les coordonnees plongees sont comobiles.
#   Une naissance a lieu des qu'une division devient spontanee (variation d'energie a l'insertion < 0, patch complet) ; s'il y en a plusieurs,
#   la plus favorable d'abord. Aucune naissance n'est imposee, aucun fil n'est designe.
# Germe de Kuhn ; depart a l'equilibre du germe (s = 0,756). Arret a 4 096, 32 768 cellules. Processus deterministe (aucune graine).
# Controle : germe regulier (meme regle).
# Mesures : part des naissances sur un fil qui est le plus long de toutes ses cellules ; qualite minimale ; degre maximal ; instrument de C-116 ;
#   loi N(s) (attendu N proportionnel a s^3 si la trame reste reguliere) ; energie par arete.
# CRITERE : celui de C-116 (profil d_s a 0,3 de S1, distance duale a 30 %, aux deux tailles) ET qualite minimale >= 0,003 ET degre maximal <= 40
#   ET part du fil le plus long >= 90 %.
# PREDICTION ENREGISTREE : PASS pour le germe de Kuhn (reproduction de S1 a l'interieur, ecarts au bord) ; germe regulier : inconnu.
import sys, math, json, heapq, itertools
import numpy as np
import c114, c116
def run(seedname,target,rand=None):
    import random as _r; rg=_r.Random(rand) if rand is not None else None; W=[0.0]
    L=[]; pos={}; F={}; E={}; EL={}; ver={}; heap=[]; cnt=[0]; SS=[0.0,0.0]; ratios=[]; dEs=[]
    P={'Kuhn':[(0.,0.,0.),(1.,0.,0.),(1.,1.,0.),(1.,1.,1.)],'regulier':[(1.,1.,1.),(1.,-1.,-1.),(-1.,1.,-1.),(-1.,-1.,1.)],
       'deforme':[(0.,0.,0.),(1.,0.,0.),(1.,1.,0.),(1.,1.,1.2)],'quasi-regulier':[(1.,1.,1.),(1.,-1.,-1.),(-1.,1.,-1.),(-1.,-1.,1.1)],
       'quelconque':[(0.,0.,0.),(1.,0.,0.),(0.3,0.9,0.),(0.4,0.35,0.8)]}[seedname]
    def dist(a,b): p,q=P[a],P[b]; return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2)
    def add(t):
        t=tuple(sorted(t)); pos[t]=len(L); L.append(t)
        for x in itertools.combinations(t,3): F.setdefault(x,set()).add(t)
        for x in itertools.combinations(t,2):
            if x not in E: E[x]=set(); EL[x]=dist(*x); SS[0]+=EL[x]; SS[1]+=EL[x]**2
            E[x].add(t)
    def rem(t):
        i=pos.pop(t); last=L.pop()
        if last!=t: L[i]=last; pos[last]=i
        for x in itertools.combinations(t,3):
            F[x].discard(t)
            if not F[x]: del F[x]
        for x in itertools.combinations(t,2):
            E[x].discard(t)
            if not E[x]: del E[x]; SS[0]-=EL[x]; SS[1]-=EL[x]**2; del EL[x]; ver.pop(x,None)
    def coef(e):
        a,b=e; p,q=P[a],P[b]; m=((p[0]+q[0])/2,(p[1]+q[1])/2,(p[2]+q[2])/2); l=EL[e]; sd=0.0; sd2=0.0; n=0
        for x in set(v for t in E[e] for v in t if v!=a and v!=b):
            r=P[x]; d=math.sqrt((r[0]-m[0])**2+(r[1]-m[1])**2+(r[2]-m[2])**2); sd+=d; sd2+=d*d; n+=1
        return sd2-l*l/2, sd, n+1
    def window(e):
        A,B,C=coef(e)
        if A>1e-15:
            disc=B*B-A*C
            if disc<=0: return None
            r=math.sqrt(disc); return (B-r)/A,(B+r)/A
        if A<-1e-15: return (B-math.sqrt(B*B-A*C))/A, float('inf')
        return C/(2*B), float('inf')
    def dE(e,s): A,B,C=coef(e); return 0.5*(A*s*s-2*B*s+C)
    def push(e):
        cnt[0]+=1; ver[e]=cnt[0]; w=window(e)
        if w is not None: heapq.heappush(heap,(w[0],cnt[0],e,w[1]))
    add((0,1,2,3))
    for e in list(E): push(e)
    nv=4; s=sum(EL.values())/sum(l*l for l in EL.values()); s0=s; active={}; hist=[]; nb=0; nlong=0; nlongcell=0
    while len(L)<target:
        while heap and heap[0][0]<=s+1e-12:
            s1,v,e,s2=heapq.heappop(heap)
            if ver.get(e)==v: active[e]=(v,s2)
        cand=[(dE(e,s),e) for e,(v,s2) in active.items() if ver.get(e)==v and s<s2]
        active={e:active[e] for _,e in cand}
        cand=[c for c in cand if c[0]<-1e-12]
        if not cand:
            while heap and ver.get(heap[0][2])!=heap[0][1]: heapq.heappop(heap)
            if not heap: break
            s_new=max(s,heap[0][0])*(1+1e-9); W[0]+=0.5*((s_new**2-s**2)*SS[1]-2*(s_new-s)*SS[0]); s=s_new; continue
        d,e=(min(cand) if rg is None else rg.choice(sorted(cand))); a,b=e; l=EL[e]; ratios.append(s*SS[1]/SS[0]); dEs.append(d)
        longall=all(l>=max(EL[x] for x in itertools.combinations(t,2))-1e-12 for t in E[e]); nlong+=longall; nb+=1
        ts=list(E[e]); m=nv; nv+=1; p,q=P[a],P[b]; P.append(((p[0]+q[0])/2,(p[1]+q[1])/2,(p[2]+q[2])/2)); active.pop(e,None)
        for t in ts: rem(t)
        new=[]
        for t in ts:
            o=tuple(v for v in t if v!=a and v!=b); add((a,m)+o); add((b,m)+o); new+=[tuple(sorted((a,m)+o)),tuple(sorted((b,m)+o))]
        for x in set(x for t in new for x in itertools.combinations(t,2)): active.pop(x,None); push(x)
        if nb%max(1,target//40)==0 or len(L)>=target: hist.append((len(L),s))
    def vol(t):
        a,b,c,d=(np.array(P[v]) for v in t); return abs(float(np.dot(b-a,np.cross(c-a,d-a))))/6
    q=np.array([vol(t)/max(EL[e] for e in itertools.combinations(t,2))**3 for t in L]); lmin=min(EL.values()); n1=len(EL); SL=sum(EL.values()); SL2=sum(l*l for l in EL.values())
    extra=dict(arm='C127-'+seedname,target=target,seed=0,naissances=nb,acc=[0,0],s0=s0,s=s,alpha=1/(s*lmin),qmin=float(q.min()),q5=float(np.percentile(q,5)),part_plus_long=nlong/max(1,nb),
               rapport_longueurs=max(EL.values())/lmin,surtension_min=float(min(ratios[len(ratios)//4:])),surtension_max=float(max(ratios[len(ratios)//4:])),surtension_moy=float(np.mean(ratios[len(ratios)//4:])),dE_moy=float(np.mean(dEs)),dE_min=float(min(dEs)),travail=W[0],E_final=0.5*(s*s*SL2-2*s*SL+n1),E_par_arete=0.5*(s*s*SL2-2*s*SL+n1)/n1,hist=hist,s_equilibre=SL/SL2)
    return c116.finish(L,F,E,nv,0,extra)
if __name__=='__main__':
    for seedname in sys.argv[2].split(','):
        for target in [int(x) for x in sys.argv[1].split(',')]:
            o=run(seedname,target); h=o['hist']
            expo=np.polyfit(np.log([x[1] for x in h[len(h)//3:]]),np.log([x[0] for x in h[len(h)//3:]]),1)[0] if len(h)>6 else float('nan')
            print(f"{o['arm']} cible={target}: surtension s/s_eq (3 derniers quarts) min={o['surtension_min']:.3f} moy={o['surtension_moy']:.3f} max={o['surtension_max']:.3f} ; ΔE à la naissance moy={o['dE_moy']:.2e} min={o['dE_min']:.2e} ; tétras={o['N3']} sommets={o['nv']} naissances={o['naissances']} part fil le plus long={100*o['part_plus_long']:.1f} % degré max={o['degmax']} qmin={o['qmin']:.5f} q5%={o['q5']:.4f} Lmax/Lmin={o['rapport_longueurs']:.2f} s: {o['s0']:.3f} -> {o['s']:.3f} (équilibre libre {o['s_equilibre']:.3f}) alpha={o['alpha']:.3f} exposant N~s^x: {expo:.2f} E/arête={o['E_par_arete']:.4f} germe={o['germe']:.1f} dist duale={o['dist']:.1f} sommets={o['distv']:.1f} d_s dual={np.round(o['dsd'],2).tolist()} d_s sommets={np.round(o['dsv'],2).tolist()}",flush=True)
            json.dump({k:v for k,v in o.items()},open(f"c127_{seedname}_{target}.json",'w'))
