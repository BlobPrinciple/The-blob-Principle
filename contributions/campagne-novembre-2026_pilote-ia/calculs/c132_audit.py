# C-132 / PR-1 (protocole FIGE par ChatGPT le 12 nov. 2026, empreinte 23f707d7...) — EXECUTION INDEPENDANTE par Claude (contre-audit).
# Mecanique du protocole : tetraedre regulier d'arete 1, un ressort par arete (K = 1), regle U (toute arete nouvelle a pour repos 1) ou B (repos = longueur
#   a la naissance) ; naissance = bissection d'une arete et de tout son patch, au milieu ; AUCUNE echelle imposee ; detente libre de tous les sommets ;
#   exclusion : aucune cellule sous 20 % de son volume a l'insertion.
# Bras du protocole : P = U-primitif (cellule tiree uniformement, sa plus longue arete au moment de la naissance) ; B = memes aretes que P, regle B ;
#   R = arete tiree uniformement parmi les six de la cellule. Graines 1320, 1321, 1322. Releves a 1, 3, 7, 15, 31 naissances.
# Critere fige "expansion collective conditionnelle" : >= 15 naissances, aucune inversion, qmin >= 0,01 (q = 6√2 V / d^3), au moins une distance entre
#   fondateurs augmentee de plus de 5 %, volume total > volume initial.
# ECARTS ET EXTENSIONS DECLARES (Claude) :
#  (1) exclusion par penalite (w = 1e4 / Vref^2 sur le deficit sous 0,2 Vref), comme dans C-127 ter ; le rapport V / Vref minimal est releve ;
#  (2) mon generateur aleatoire n'est pas celui de ChatGPT : les trajectoires different, la comparaison est statistique ;
#  (3) extension hors protocole : releves a 63, 127 et 255 naissances ;
#  (4) bras L, hors protocole (regle de la cosmogonie, C-116) : cellule tiree en proportion de son volume, le fil le plus long d'abord AVEC propagation
#      (si une cellule autour du fil a un fil plus long, elle passe d'abord), une naissance par tirage.
# DECLARATION : avant de lancer, j'ai vu dans la conversation un resultat provisoire de ChatGPT (graine 1320, 15 naissances : qmin = 0,0042, aucune inversion).
# PREDICTION ENREGISTREE : P : volume et distances augmentent (PASS local) mais qmin < 0,01 a 15 naissances (FAIL du critere collectif) ; B : aucun mouvement ;
#   R : pire que P ; L : qmin >= 0,01 a 15 et 31 naissances (PASS du critere collectif) et degre maximal <= 40 a 255 naissances ; volume par cellule borne.
import sys, itertools, math, json, random, numpy as np, scipy.optimize as so
from c120 import Mesh, SEEDS, vol6
HOOK=None
EPS=0.2; VS=1/(6*math.sqrt(2)); CHECK=(1,3,7,15,31,63,127,255)
def relax(m,Vref):
    # ECART DECLARE APRES PILOTE : la penalite raide de C-127 ter ne converge pas ici (gradient residuel de l'ordre de 1, positions figees). Remplacee par un
    # lagrangien augmente : contraintes g_t = (0,2 Vref_t - V_t) / V_regulier <= 0 (meme ensemble admissible, mise a l'echelle absolue pour le conditionnement), multiplicateurs lambda_t >= 0, minimisations internes L-BFGS ; on releve le residu
    # des conditions d'optimalite (gradient du lagrangien) et la violation maximale. Une trajectoire non convergee est declaree INCONCLUSIVE.
    for t in m.T:
        if t not in Vref: Vref[t]=vol6(m.X,t)/6
    for t in list(Vref):
        if t not in m.T: del Vref[t]
    ids=sorted(m.X); pos={v:i for i,v in enumerate(ids)}; X0=np.array([m.X[v] for v in ids]); ed=list(m.rest); I=np.array([pos[e[0]] for e in ed]); J=np.array([pos[e[1]] for e in ed]); R=np.array([m.rest[e] for e in ed])
    TT=list(m.T); T=np.array([[pos[v] for v in t] for t in TT]); VR=np.array([Vref[t] for t in TT]); lam=np.zeros(len(TT)); mu=10.0; x=X0.ravel().copy(); prev=None; pdl=None
    def parts(z):
        X=z.reshape(-1,3); D=X[I]-X[J]; L=np.linalg.norm(D,axis=1); G=np.zeros_like(X); wv=((L-R)/np.maximum(L,1e-300))[:,None]*D
        np.add.at(G,I,wv); np.add.at(G,J,-wv); E=0.5*((L-R)**2).sum()
        a,b,c,d=(X[T[:,i]] for i in range(4)); V=np.einsum('ij,ij->i',b-a,np.cross(c-a,d-a))/6
        return X,E,G,V,(a,b,c,d)
    def addc(G,coef,abcd):   # ajoute Somme_t coef_t * grad(V_t)
        a,b,c,d=abcd; k=(coef/6)[:,None]; gb=np.cross(c-a,d-a)*k; gc=np.cross(d-a,b-a)*k; gd=np.cross(b-a,c-a)*k
        np.add.at(G,T[:,1],gb); np.add.at(G,T[:,2],gc); np.add.at(G,T[:,3],gd); np.add.at(G,T[:,0],-(gb+gc+gd))
    def fun(z):
        X,E,G,V,abcd=parts(z); g=(EPS*VR-V)/VS; a=np.maximum(0,lam+mu*g); addc(G,-a/VS,abcd); return E+((a**2-lam**2).sum())/(2*mu),G.ravel()
    for outer in range(300):
        r=so.minimize(fun,x,jac=True,method='L-BFGS-B',options=dict(gtol=1e-11,ftol=1e-16,maxiter=20000,maxcor=30,maxfun=100000)); x=r.x
        X,E,G,V,abcd=parts(x); g=(EPS*VR-V)/VS; new=np.maximum(0,lam+mu*g); viol=float(np.maximum(0,g).max()); dl=float(abs(new-lam).max()); lam=new
        if viol<1e-9 and dl<1e-7: break
        if (prev is not None and viol>0.25*prev and viol>1e-9) or (pdl is not None and dl>0.3*pdl): mu=min(mu*3,3e3)
        prev=viol; pdl=dl
    X,E,G,V,abcd=parts(x); addc(G,-lam/VS,abcd); kkt=float(abs(G).max())
    for v in ids: m.X[v]=X[pos[v]]
    return dict(valid=bool(V.min()>0),nact=int((lam>1e-9).sum()),ratio=float((V/VR).min()),gmax=kkt,viol=float(np.maximum(0,EPS-V/VR).max()),lmax=float(lam.max()),outer=outer)
def longest(m,t): return max(itertools.combinations(sorted(t),2),key=lambda e:(round(m.length(e),9),e))
def run(arm,seed,nmax,replay=None):
    rng=random.Random(seed); m=Mesh(SEEDS['regulier'],1.0,'B' if arm=='B' else 'U','F'); Vref={}; relax(m,Vref); V0=sum(vol6(m.X,t) for t in m.T)/6
    f0=[m.length(e) for e in itertools.combinations(range(4),2)]; rows=[]; cum=0.0; seq=[]; gworst=0.0; rmin=1.0; nlong=0
    for n in range(1,nmax+1):
        TT=sorted(m.T); E=m.inc()
        if arm=='B': e=replay[n-1]
        elif arm=='L':
            vols=[vol6(m.X,t) for t in TT]; t=rng.choices(TT,weights=vols)[0]; steps=0
            while True:
                e=longest(m,t); l=m.length(e); nxt=None
                for t2 in E[e]:
                    e2=longest(m,t2)
                    if m.length(e2)>l+1e-9: l=m.length(e2); nxt=t2
                if nxt is None or steps>=200: break
                t=nxt; steps+=1
        else:
            t=TT[rng.randrange(len(TT))]; e=longest(m,t) if arm=='P' else sorted(itertools.combinations(sorted(t),2))[rng.randrange(6)]
        l=m.length(e); nlong+=all(l>=max(m.length(x) for x in itertools.combinations(sorted(t2),2))-1e-9 for t2 in E[e])
        Eb=m.energy(); dEi=m.dE_insert(e,E); cum+=max(0.0,dEi); m.bisect(e,E=E); seq.append(e); r=relax(m,Vref); gworst=max(gworst,r['gmax']); rmin=min(rmin,r['ratio'])
        if not r['valid']: rows.append(dict(n=n,statut='INVERSION',N3=len(m.T))); break
        if n in CHECK:
            L={x:m.length(x) for x in m.rest}; vols=[vol6(m.X,t)/6 for t in m.T]; q=[6*math.sqrt(2)*vol6(m.X,t)/6/max(L[x] for x in itertools.combinations(sorted(t),2))**3 for t in m.T]
            deg={}
            for a,b in m.rest: deg[a]=deg.get(a,0)+1; deg[b]=deg.get(b,0)+1
            P=np.array(list(m.X.values())); from scipy.spatial.distance import pdist
            f=[m.length(x) for x in itertools.combinations(range(4),2)]
            rows.append(dict(n=n,statut='ok',N0=len(m.X),N1=len(m.rest),N3=len(m.T),E=m.energy(),E_par_fil=m.energy()/len(m.rest),cum=cum,Vratio=sum(vols)/V0,Vcell=sum(vols)/len(m.T)/V0,diam=float(pdist(P).max()),
                fmoy=float(np.mean(f)/np.mean(f0)),fmax=float(max(fi/f0i for fi,f0i in zip(f,f0))),qmin=min(q),q10=float(np.percentile(q,10)),qmed=float(np.median(q)),degmax=max(deg.values()),inv=int(sum(v<=0 for v in vols)),
                Lmin=min(L.values()),Lmax=max(L.values()),nact=r['nact'],ratio=rmin,gmax=gworst,part_long=nlong/n))
            if HOOK: HOOK(rows[-1])
    return rows,seq
if __name__=='__main__':
    nmax=int(sys.argv[1]); arms=sys.argv[2].split(','); out={}
    for seed in (1320,1321,1322):
        seqP=None
        for arm in arms:
            if arm=='B' and seqP is None: continue
            rows,seq=run(arm,seed,nmax,replay=seqP)
            if arm=='P': seqP=seq
            out[f'{arm}-{seed}']=rows
            for r in rows:
                if r['statut']!='ok': print(f'{arm} graine {seed} n={r["n"]}: {r["statut"]} à {r["N3"]} cellules',flush=True); continue
                print(f'{arm} graine {seed} n={r["n"]:3d} cellules={r["N3"]:4d} V/V0={r["Vratio"]:8.3f} V/cellule={r["Vcell"]:.3f} diam={r["diam"]:.3f} fondateurs moy×{r["fmoy"]:.3f} max×{r["fmax"]:.3f} E={r["E"]:.4f} E/fil={r["E_par_fil"]:.4f} activation cumulée={r["cum"]:.3f} qmin={r["qmin"]:.4f} q10%={r["q10"]:.3f} qméd={r["qmed"]:.3f} degré max={r["degmax"]} L∈[{r["Lmin"]:.2f},{r["Lmax"]:.2f}] au contact={r["nact"]} V/Vref min={r["ratio"]:.3f} grad max={r["gmax"]:.1e} fil le plus long du patch={100*r["part_long"]:.0f} %',flush=True)
    json.dump(out,open(f'c132_audit_{sys.argv[2].replace(",","")}_{nmax}.json','w'))
