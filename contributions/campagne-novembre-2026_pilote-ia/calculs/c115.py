# C-115 / PR-1 (protocole FIGE par ChatGPT le 11 nov., execute par Claude le 12 nov.). Rigidite x plafond de degre x budget de ressources.
# Action S_kappa = 3 N3 + kappa Somme_e (n_e - d*)^2 - 0,4 Somme_e ln(1+n_e). kappa = 0,05 ; 0,2 ; 0,5 ; 1 ; 2 ; 4.
# Naissances 1->4 (parent uniforme) : 512, 2048, 8192 ; graines 1400-1407 ; 100 tentatives de reorganisation 2<->3 par naissance ;
# acceptation de Metropolis-Hastings avec les probabilites de proposition dans les deux sens (facteur N/(N+1) et N/(N-1)).
# Controles : sans plafond / degre des sommets <= 20 (des la premiere naissance) ; budget N1 <= 7 (N0 - 1) a kappa = 0,05 ; 1 ; 2.
# Croissance bloquee (5000 tirages sans parent admissible) : declaree, non contournee.
# ECARTS DECLARES : le fichier PR-1 est inaccessible (bac a sable de ChatGPT) ; le protocole est repris du message. Choix de Claude :
#   naissance = parent uniforme (comme C-114), le terme 3 N3 n'entre que dans les reorganisations ; temoins = ceux de C-114 et C-116
#   (Freudenthal a bord libre ; raffinement euclidien a bord fixe = S1) ; le temoin periodique n'est pas refait.
#   Taille 8192 : graines 1400-1403 seulement (budget de calcul).
import sys, math, json, random, itertools
import numpy as np
from multiprocessing import Pool
import c114
dstar=c114.dstar
def run(args):
    nb,seed,kappa,cap,budget=args; rng=random.Random(seed); L=[]; pos={}; F={}; E={}; deg={}
    f=lambda n:kappa*(n-dstar)**2-0.4*math.log(1+n)
    def add(t):
        t=tuple(sorted(t)); pos[t]=len(L); L.append(t)
        for x in itertools.combinations(t,3): F.setdefault(x,set()).add(t)
        for x in itertools.combinations(t,2):
            if x not in E: E[x]=set(); deg[x[0]]=deg.get(x[0],0)+1; deg[x[1]]=deg.get(x[1],0)+1
            E[x].add(t)
    def rem(t):
        i=pos.pop(t); last=L.pop()
        if last!=t: L[i]=last; pos[last]=i
        for x in itertools.combinations(t,3):
            F[x].discard(t)
            if not F[x]: del F[x]
        for x in itertools.combinations(t,2):
            E[x].discard(t)
            if not E[x]: del E[x]; deg[x[0]]-=1; deg[x[1]]-=1
    add((0,1,2,3)); nv=4; acc=[0,0]; born=0; blocked=False
    for n in range(1,nb+1):
        for _ in range(5000):
            t=L[rng.randrange(len(L))]
            if cap and max(deg[v] for v in t)>=20: continue
            if budget and len(E)+4>7*nv: continue
            break
        else: blocked=True; break
        rem(t)
        for k in range(4): add(tuple(nv if i==k else t[i] for i in range(4)))
        nv+=1; born+=1
        for _ in range(100):
            N=len(L); t=L[rng.randrange(N)]
            if rng.random()<0.5:
                k=rng.randrange(4); fc=tuple(v for i,v in enumerate(t) if i!=k); ts=F[fc]
                if len(ts)!=2: continue
                t1,t2=tuple(ts); x=(set(t1)-set(fc)).pop(); y=(set(t2)-set(fc)).pop(); e=tuple(sorted((x,y)))
                if e in E: continue
                if cap and (deg[x]>=20 or deg[y]>=20): continue
                if budget and len(E)+1>7*(nv-1): continue
                dS=3+f(3)
                for pr in itertools.combinations(fc,2): m=len(E[pr]); dS+=f(m-1)-f(m)
                for u in (x,y):
                    for a in fc: m=len(E[tuple(sorted((u,a)))]); dS+=f(m+1)-f(m)
                if dS>700 or rng.random()>=min(1.0,math.exp(-dS)*N/(N+1)): continue
                rem(t1); rem(t2)
                for pr in itertools.combinations(fc,2): add(pr+(x,y))
                acc[0]+=1
            else:
                e=tuple(sorted(rng.sample(t,2))); ts=E[e]
                if len(ts)!=3: continue
                link=sorted(set().union(*map(set,ts))-set(e))
                if len(link)!=3 or tuple(link) in F: continue
                dS=-3-f(3)
                for pr in itertools.combinations(link,2): m=len(E[pr]); dS+=f(m+1)-f(m)
                for u in e:
                    for a in link: m=len(E[tuple(sorted((u,a)))]); dS+=f(m-1)-f(m)
                if dS>700 or rng.random()>=min(1.0,math.exp(-dS)*N/(N-1)): continue
                for tt in list(ts): rem(tt)
                add(tuple(link)+(e[0],)); add(tuple(link)+(e[1],)); acc[1]+=1
    out=c114.measure(L,F,E,nv,seed); out.update(nb=nb,seed=seed,kappa=kappa,cap=cap,budget=budget,acc=acc,born=born,blocked=blocked,N1=len(E)); return out
if __name__=='__main__':
    sizes=[int(x) for x in sys.argv[1].split(',')]; ns=int(sys.argv[2])
    arms=[(k,c,False) for k in (0.05,0.2,0.5,1,2,4) for c in (False,True)]+[(k,False,True) for k in (0.05,1,2)]
    jobs=[(nb,s,k,c,b) for nb in sizes for (k,c,b) in arms for s in range(1400,1400+ns)]
    with Pool(2) as p: res=p.map(run,jobs,chunksize=1)
    json.dump(res,open(f'c115_{sys.argv[1].replace(",","_")}.json','w'))
    for (k,c,b) in arms:
        for nb in sizes:
            rs=[x for x in res if x['nb']==nb and x['kappa']==k and x['cap']==c and x['budget']==b]; m=lambda key:np.mean([x[key] for x in rs])
            print(f'kappa={k} plafond={"20" if c else "non"} budget={"7" if b else "non"} n={nb}: nés={m("born"):.0f} bloqué={sum(x["blocked"] for x in rs)}/{len(rs)} tétras={m("N3"):.0f} N1/N0={m("N1")/m("nv"):.2f} valence={m("nmean"):.2f} degré max={m("degmax"):.0f} dist duale={m("dist"):.1f} sommets={m("distv"):.1f} d_s dual={np.round(np.mean([x["dsd"] for x in rs],axis=0),2).tolist()} d_s sommets={np.round(np.mean([x["dsv"] for x in rs],axis=0),2).tolist()}',flush=True)
