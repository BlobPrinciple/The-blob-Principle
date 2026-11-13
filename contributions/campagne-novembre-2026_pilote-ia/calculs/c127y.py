# C-127 ter — controle DECLARE : meme processus que C-127 bis (bord entraine, interieur libre), avec une force numerique d'exclusion declaree :
#   penalite w * Somme_t max(0, eps*Vref_t - V_t)^2, eps = 0,2, ou Vref_t est le volume de la cellule a sa naissance (apres insertion), w = 1e4 / Vref^2.
#   Elle interdit qu'une cellule tombe sous 20 % de son volume de naissance (exclusion spatiale de C-12 et C-15). Ce bras ne valide pas C-127 bis.
# CRITERE : part du fil le plus long >= 90 %, qualite minimale >= 0,003, degre maximal <= 40, aucune inversion, jusqu'a 512 cellules.
# PREDICTION ENREGISTREE : PASS.
import sys, itertools, math, numpy as np, scipy.optimize as so
from c120 import Mesh, SEEDS, vol6
target=int(sys.argv[1]); eps=0.2; m=Mesh(SEEDS['Kuhn'],1.0,'U','X'); s=0.756; step=1.005; nb=0; nlong=0; Vref={}
def setrest(s):
    m.l0=1.0/s
    for e in m.rest: m.rest[e]=m.l0
def relax():
    for t in m.T:
        if t not in Vref: Vref[t]=vol6(m.X,t)/6
    for t in list(Vref):
        if t not in m.T: del Vref[t]
    ids=sorted(m.X); pos={v:i for i,v in enumerate(ids)}; X0=np.array([m.X[v] for v in ids]); ed=list(m.rest); I=np.array([pos[e[0]] for e in ed]); J=np.array([pos[e[1]] for e in ed]); R=np.array([m.rest[e] for e in ed])
    TT=list(m.T); T=np.array([[pos[v] for v in t] for t in TT]); VR=np.array([Vref[t] for t in TT]); w=1e4/VR**2
    fi=np.array([pos[v] for v in ids if v not in m.fixed],int)
    if len(fi)==0: return dict(valid=True,pen=0.0,nact=0)
    def fun(z):
        X=X0.copy(); X[fi]=z.reshape(-1,3); D=X[I]-X[J]; L=np.linalg.norm(D,axis=1); G=np.zeros_like(X); wv=((L-R)/np.maximum(L,1e-300))[:,None]*D
        np.add.at(G,I,wv); np.add.at(G,J,-wv); E=0.5*((L-R)**2).sum()
        a,b,c,d=(X[T[:,i]] for i in range(4)); V=np.einsum('ij,ij->i',b-a,np.cross(c-a,d-a))/6; df=np.maximum(0,eps*VR-V); pen=(w*df**2).sum()
        if pen>0:
            k=(-2*w*df/6)[:,None]; gb=np.cross(c-a,d-a)*k; gc=np.cross(d-a,b-a)*k; gd=np.cross(b-a,c-a)*k
            np.add.at(G,T[:,1],gb); np.add.at(G,T[:,2],gc); np.add.at(G,T[:,3],gd); np.add.at(G,T[:,0],-(gb+gc+gd))
        return E+pen,G[fi].ravel()
    r=so.minimize(fun,X0[fi].ravel(),jac=True,method='L-BFGS-B',options=dict(gtol=1e-10,ftol=1e-15,maxiter=50000,maxcor=40,maxfun=200000))
    Xn=X0.copy(); Xn[fi]=r.x.reshape(-1,3)
    for v in ids: m.X[v]=Xn[pos[v]]
    V=np.array([vol6(m.X,t)/6 for t in TT]); return dict(valid=bool(V.min()>0),pen=float(r.fun-m.energy()),nact=int((V<eps*VR).sum()))
setrest(s); nact_max=0
while len(m.T)<target:
    E=m.inc(); d,e=min((m.dE_insert(e,E),e) for e in E)
    if d<-1e-12*max(1.0,m.energy()):
        l=m.length(e); nlong+=all(l>=max(m.length(x) for x in itertools.combinations(sorted(t),2))-1e-9 for t in E[e]); nb+=1; m.bisect(e,E=E); r=relax()
    else:
        s*=step; setrest(s); r=relax()
    nact_max=max(nact_max,r['nact'])
    if not r['valid']: print('ARRÊT : cellule retournée à',len(m.T),'cellules, naissance',nb); break
    if nb and nb%40==0 and d<0:
        mt=m.metrics(); print(f'  naissances={nb} cellules={mt["N3"]} s={s:.3f} part du fil le plus long={100*nlong/nb:.1f} % degré max={mt["degmax"]} qmin={mt["qmin"]:.4f} Lmax/Lmin={mt["Lmax"]/mt["Lmin"]:.2f} cellules au contact de l\'exclusion={r["nact"]}',flush=True)
mt=m.metrics()
print(f'FINAL : cellules={mt["N3"]} sommets={mt["N0"]} naissances={nb} s={s:.3f} part du fil le plus long={100*nlong/max(1,nb):.1f} % degré max={mt["degmax"]} qmin={mt["qmin"]:.4f} Lmax/Lmin={mt["Lmax"]/mt["Lmin"]:.2f} inversions={mt["inversions"]} auto-intersections={mt["autointersections"]} max de cellules au contact de l\'exclusion={nact_max}')
