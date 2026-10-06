# =============================================================================
#  BLOB PRINCIPLE — SONDE GRAVITATIONNELLE HAUTE PRECISION
#  Campagne Colab : N = 2000 a 8000 en 4D, tout en creux, MINRES.
#  Objectif : ka < 1 pour amener le rapport d'Einstein-Hilbert de 10% a 1%.
#
#  Conforme a la Blob Core Specification v1.0 (sonde P1).
#  Les douze regles s'appliquent : graines declarees, Ward avant mesure,
#  plateau et non seuil choisi, rejets traces, erreurs separees.
# =============================================================================
#  COLAB : Execution > Modifier le type d'execution > RAM elevee recommandee.
#  Duree estimee : N=2000 ~ 15 min | N=4000 ~ 50 min | N=8000 ~ 3 h
# =============================================================================

!pip install -q numba

import numpy as np, math, itertools, time, json, os
import scipy.sparse as sp
from scipy.sparse.linalg import minres, LinearOperator, spsolve, factorized
from scipy.spatial import Delaunay

# ----------------------------------------------------------------- constantes
P10 = [(i,j) for i in range(5) for j in range(i+1,5)]          # 10 aretes
TRIS= [(i,j,k) for i in range(5) for j in range(i+1,5) for k in range(j+1,5)]  # 10 triangles
IDX = {e:i for i,e in enumerate(P10)}

# --------------------------------------------------- geometrie du pentachore
def emb5(Ls):
    """plonge un 5-simplexe dans R^4 depuis ses 10 longueurs. None si degenere."""
    L2 = np.zeros((5,5))
    for m,(i,j) in enumerate(P10):
        L2[i,j]=L2[j,i]=Ls[m]**2
    P = np.zeros((5,4))
    P[1,0] = Ls[IDX[(0,1)]]
    if P[1,0] < 1e-12: return None
    x = (L2[0,2]+P[1,0]**2-L2[1,2])/(2*P[1,0])
    y2 = L2[0,2]-x*x
    if y2 <= 1e-14: return None
    P[2,0], P[2,1] = x, math.sqrt(y2)
    for k in (3,4):
        x = (L2[0,k]+P[1,0]**2-L2[1,k])/(2*P[1,0])
        y = (L2[0,k]+P[2,0]**2+P[2,1]**2-L2[2,k]-2*x*P[2,0])/(2*P[2,1])
        r2 = L2[0,k]-x*x-y*y
        if r2 <= 1e-14: return None
        if k==3:
            P[3,0],P[3,1],P[3,2] = x,y,math.sqrt(r2)
        else:
            z = (L2[0,3]+ (x-P[3,0])**2 + (y-P[3,1])**2 - L2[3,4]
                 + P[3,2]**2 - x*x - y*y + 2*x*P[3,0] + 2*y*P[3,1]
                 - P[3,0]**2 - P[3,1]**2)/(2*P[3,2])
            w2 = L2[0,4]-x*x-y*y-z*z
            if w2 <= 1e-14: return None
            P[4,0],P[4,1],P[4,2],P[4,3] = x,y,z,math.sqrt(w2)
    return P

def tri_area(a,b,c):
    s = 2*a*a*b*b + 2*b*b*c*c + 2*c*c*a*a - a**4 - b**4 - c**4
    return 0.25*math.sqrt(max(s,0.0))

def dA_tri(a,b,c):
    A = tri_area(a,b,c)
    return np.array([a*(b*b+c*c-a*a), b*(a*a+c*c-b*b), c*(a*a+b*b-c*c)])/(8.0*max(A,1e-15))

def thetas(Ls):
    """10 angles diedres, par projection orthogonale exacte (domaine [0,pi])"""
    P = emb5(Ls)
    if P is None: return None
    out = np.zeros(10)
    for m,(i,j,k) in enumerate(TRIS):
        rest=[q for q in range(5) if q not in (i,j,k)]
        B=np.stack([P[j]-P[i],P[k]-P[i]]); Q,_=np.linalg.qr(B.T)
        pl=P[rest[0]]-P[i]; pm=P[rest[1]]-P[i]
        pl=pl-Q@(Q.T@pl); pm=pm-Q@(Q.T@pm)
        nl,nm=np.linalg.norm(pl),np.linalg.norm(pm)
        if nl<1e-12 or nm<1e-12: return None
        out[m]=math.acos(max(-1.0,min(1.0,float(pl@pm)/(nl*nm))))
    return out

def jac_theta(Ls,h=1e-5):
    """J[t,e] = d theta_t / d l_e — 20 plongements, difference centree"""
    J=np.zeros((10,10))
    for e in range(10):
        lp=Ls.copy(); lp[e]+=h; tp=thetas(lp)
        lm=Ls.copy(); lm[e]-=h; tm=thetas(lm)
        if tp is None or tm is None: return None
        J[:,e]=(tp-tm)/(2*h)
    return J

# ------------------------------------------------------ construction du 4-tore
def build_torus(N, seed, w=0.45, verbose=True):
    rng=np.random.default_rng(seed); P0=rng.uniform(0,1,size=(N,4))
    big=[P0]; ids=[np.arange(N)]; sh=[np.zeros((N,4))]
    for s in itertools.product((-1,0,1),repeat=4):
        if all(x==0 for x in s): continue
        m=np.ones(N,bool)
        for k in range(4):
            if s[k]==1:   m &= (P0[:,k]<w)
            elif s[k]==-1: m &= (P0[:,k]>1-w)
        if m.any():
            big.append(P0[m]+np.array(s,float)); ids.append(np.arange(N)[m])
            sh.append(np.tile(np.array(s,float),(m.sum(),1)))
    big=np.vstack(big); ids=np.concatenate(ids); sh=np.vstack(sh)
    if verbose: print(f"  Delaunay 4D sur {len(big)} points...", flush=True)
    tri=Delaunay(big)
    PENTS=[]
    for s5 in tri.simplices:
        c=big[s5].mean(0)
        if not (np.all(c>=0) and np.all(c<1)): continue
        b=[int(ids[x]) for x in s5]
        if len(set(b))!=5: continue
        PENTS.append((b,[sh[x].astype(int) for x in s5],big[s5].copy()))
    if verbose: print(f"  {len(PENTS)} pentachores retenus", flush=True)
    return P0, PENTS

def ekey(b1,s1,b2,s2):
    """cle d'arete = (paire, enroulement) — corrige la conflation"""
    if b1<b2: return (b1,b2,tuple(s2-s1))
    return (b2,b1,tuple(s1-s2))

# ------------------------------------------- assemblage SPARSE (formule Hamber)
def assemble(N, seed, w=0.45, verbose=True):
    """H = sum_t sym(grad delta_t (x) grad A_t)   — tout en creux"""
    t0=time.time()
    P0,PENTS = build_torus(N,seed,w,verbose)
    eid={}; edges=[]; tkey={}; hedges=[]
    for b,shs,pts in PENTS:
        for (x,y) in P10:
            k=ekey(b[x],shs[x],b[y],shs[y])
            if k not in eid: eid[k]=len(edges); edges.append(k)
        for (x,y,z) in TRIS:
            ii=tuple(sorted([eid[ekey(b[x],shs[x],b[y],shs[y])],
                             eid[ekey(b[x],shs[x],b[z],shs[z])],
                             eid[ekey(b[y],shs[y],b[z],shs[z])]]))
            if ii not in tkey: tkey[ii]=len(hedges); hedges.append(ii)
    E=len(edges); T=len(hedges)
    if verbose: print(f"  {E} aretes (avec enroulement), {T} charnieres", flush=True)

    Lg=np.zeros(E); mids=np.zeros((E,4)); dirs=np.zeros((E,4))
    for i,(b1,b2,wd) in enumerate(edges):
        p1=P0[b1]; p2=P0[b2]+np.array(wd,float)
        mids[i]=((p1+p2)/2)%1.0
        d=p2-p1; Lg[i]=np.linalg.norm(d); dirs[i]=d/Lg[i]

    gdel={}; rejets=0
    n_p=len(PENTS)
    for pi,(b,shs,pts) in enumerate(PENTS):
        if verbose and pi%2000==0 and pi>0:
            print(f"    ... {pi}/{n_p} pentachores  ({time.time()-t0:.0f}s)", flush=True)
        Ls=np.array([np.linalg.norm(pts[x]-pts[y]) for (x,y) in P10])
        loc=[eid[ekey(b[x],shs[x],b[y],shs[y])] for (x,y) in P10]
        J=jac_theta(Ls)
        if J is None: rejets+=1; continue
        for m,(x,y,z) in enumerate(TRIS):
            ii=tuple(sorted([eid[ekey(b[x],shs[x],b[y],shs[y])],
                             eid[ekey(b[x],shs[x],b[z],shs[z])],
                             eid[ekey(b[y],shs[y],b[z],shs[z])]]))
            ti=tkey[ii]
            d=gdel.setdefault(ti,{})
            for e in range(10):
                if abs(J[m,e])>1e-14:
                    d[loc[e]] = d.get(loc[e],0.0) - J[m,e]      # delta = 2pi - sum theta

    R=[];C=[];V=[]
    for ti,d in gdel.items():
        e3=hedges[ti]
        gA=dA_tri(Lg[e3[0]],Lg[e3[1]],Lg[e3[2]])
        for ea,va in d.items():
            for bi,eb in enumerate(e3):
                v=0.5*va*gA[bi]
                R.append(ea);C.append(eb);V.append(v)
                R.append(eb);C.append(ea);V.append(v)
    H=sp.coo_matrix((V,(R,C)),shape=(E,E)).tocsr()
    H=(H+H.T)*0.5

    gr=[];gc=[];gv=[]
    for i,(b1,b2,wd) in enumerate(edges):
        d=dirs[i]
        for k in range(4):
            gr.append(i); gc.append(4*b1+k); gv.append(-d[k])
            gr.append(i); gc.append(4*b2+k); gv.append(d[k])
    G=sp.coo_matrix((gv,(gr,gc)),shape=(E,4*N)).tocsr()

    if verbose:
        print(f"  assemblage termine : {rejets} rejets ({100*rejets/n_p:.2f}%), "
              f"{time.time()-t0:.0f}s", flush=True)
    return dict(H=H,G=G,mids=mids,Lg=Lg,dirs=dirs,E=E,N=N,rejets=rejets,
                npent=n_p, a=float(Lg.mean()))

# ------------------------------------------- projection de jauge EN OPERATEUR
class GaugeProj:
    """P = I - G (G^T G)^+ G^T, applique sans jamais densifier"""
    def __init__(self, G, reg=1e-10):
        self.G=G.tocsc()
        A=(G.T@G).tocsc()
        A=A+reg*sp.identity(A.shape[0],format='csc')
        self.solve=factorized(A)
    def __call__(self, x):
        return x - self.G@self.solve(self.G.T@x)

# --------------------------------------------------------------- test de Ward
def ward(d, proj, ntest=12, seed=0):
    """||H Q|| / ||H|| estime par vecteurs aleatoires DANS l'espace de jauge"""
    rng=np.random.default_rng(seed); H=d['H']; G=d['G']; E=d['E']
    num=0.0; den=0.0
    for _ in range(ntest):
        z=rng.normal(size=G.shape[1])
        g=G@z
        ng=np.linalg.norm(g)
        if ng<1e-12: continue
        g/=ng
        num+=np.linalg.norm(H@g)**2
        r=rng.normal(size=E); r/=np.linalg.norm(r)
        den+=np.linalg.norm(H@r)**2
    return math.sqrt(num/max(den,1e-300))

# ------------------------------------------------- reponse par MINRES + plateau
def response(d, proj, src, shift, maxiter=6000, tol=1e-9):
    """resout (-H + shift I) u = P src dans le secteur physique, rend src.u"""
    H=d['H']; E=d['E']
    def mv(x):
        px=proj(x)
        return proj(-(H@px)) + shift*px
    A=LinearOperator((E,E),matvec=mv,dtype=float)
    b=proj(src)
    u,info=minres(A,b,rtol=tol,maxiter=maxiter)
    u=proj(u)
    return float(b@u)

def ttbasis(kv):
    k=kv/np.linalg.norm(kv)
    M=np.eye(4)-np.outer(k,k)
    U,_,_=np.linalg.svd(M); B=U[:,:3]
    e1,e2,e3=B[:,0],B[:,1],B[:,2]
    return [np.outer(e1,e2)+np.outer(e2,e1),
            np.outer(e1,e3)+np.outer(e3,e1),
            np.outer(e2,e3)+np.outer(e3,e2),
            np.outer(e1,e1)-np.outer(e2,e2),
            (np.outer(e1,e1)+np.outer(e2,e2)-2*np.outer(e3,e3))/math.sqrt(3)]

def measure(d, shells=(1,2,3,4), shifts=(1e-3,1e-4,1e-5,1e-6,1e-7), verbose=True):
    """balaye les couches et les shifts (plateau) ; rend TT, trace et le rapport"""
    proj=GaugeProj(d['G'])
    wd=ward(d,proj)
    if verbose: print(f"  WARD = {wd:.3e}", flush=True)
    if wd>1e-2:
        print("  >>> REJETE par le test d'acceptation (regle 5). Pas de mesure.")
        return None
    a=d['a']; mids=d['mids']; Lg=d['Lg']; dirs=d['dirs']
    out=[]
    for n2 in shells:
        ns=[n for n in itertools.product(range(-2,3),repeat=4) if sum(x*x for x in n)==n2]
        for n in ns[:3]:
            kv=2*math.pi*np.array(n,float); k2=float(kv@kv); ph=np.cos(mids@kv)
            for shift in shifts:
                TTv=[]
                for eps in ttbasis(kv):
                    q=np.einsum('ei,ij,ej->e',dirs,eps,dirs)
                    s=Lg*q*ph; s-=s.mean(); nn=float(s@s)
                    if nn<1e-20: continue
                    TTv.append(response(d,proj,s,shift)/nn*k2*a*a)
                q=np.einsum('ei,ij,ej->e',dirs,np.eye(4),dirs)
                s=Lg*q*ph; s-=s.mean(); nn=float(s@s)
                tr=response(d,proj,s,shift)/nn*k2*a*a
                if TTv:
                    out.append(dict(n2=n2,ka=2*math.pi*math.sqrt(n2)*a,shift=shift,
                                    TT=float(np.mean(TTv)),TTsd=float(np.std(TTv)),
                                    trace=tr,ratio=tr/np.mean(TTv)))
            if verbose:
                last=out[-1]
                print(f"    |k|^2={n2} ka={last['ka']:.3f}  TT={last['TT']:+.4f} "
                      f"trace={last['trace']:+.4f}  r={last['ratio']:+.4f}", flush=True)
    return dict(ward=wd, rows=out, a=a, N=d['N'], rejets=d['rejets'], E=d['E'])

# ------------------------------------------------------------------ CAMPAGNE
#  GRAINES DECLAREES AVANT EXECUTION (regle 3)
CAMPAGNE = [(2000, 9001), (2000, 9002), (4000, 9003), (4000, 9004), (8000, 9005)]

if __name__ == "__main__":
    resultats=[]
    for N,seed in CAMPAGNE:
        print(f"\n{'='*66}\n  N = {N}   graine = {seed}\n{'='*66}", flush=True)
        t=time.time()
        d=assemble(N,seed)
        r=measure(d)
        if r is not None:
            r['seed']=seed; r['temps']=time.time()-t
            resultats.append(r)
            with open('blob_gravite_resultats.json','w') as f:
                json.dump(resultats,f,indent=1)
            print(f"  --> sauvegarde ({time.time()-t:.0f}s)", flush=True)
        del d

    # ---- extrapolation finale : r0 = ratio a ka -> 0
    print(f"\n{'='*66}\n  EXTRAPOLATION\n{'='*66}")
    ka=[];rt=[]
    for r in resultats:
        for row in r['rows']:
            if row['shift']<=1e-5:            # dans le plateau
                ka.append(row['ka']); rt.append(row['ratio'])
    ka=np.array(ka); rt=np.array(rt)
    m=ka<2.5
    if m.sum()>=4:
        A=np.vstack([np.ones(m.sum()),ka[m]**2]).T
        r0=np.linalg.lstsq(A,rt[m],rcond=None)[0][0]
        print(f"  points a ka<2.5 : {m.sum()}")
        print(f"  r0 = {r0:+.5f}     [Einstein-Hilbert D=4 : -1/3 = -0.33333]")
        print(f"  ecart : {100*abs(r0+1/3)*3:.2f} %")
    print("\n  Fichier de sortie : blob_gravite_resultats.json")
