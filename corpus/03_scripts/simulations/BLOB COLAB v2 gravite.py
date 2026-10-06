# =============================================================================
#  BLOB PRINCIPLE — SONDE GRAVITATIONNELLE, VERSION 2 (corrigee et validee)
#
#  CE QUI A CHANGE PAR RAPPORT A LA V1 (qui a echoue sur 5 configurations) :
#   [1] emb5 reecrit par MATRICE DE GRAM + CHOLESKY.
#       La v1 avait une formule algebriquement fausse pour la 4e coordonnee
#       -> 43 % de rejets, Ward = 0.75, tout rejete par le test d'acceptation.
#       Nouvelle version validee : identique a la reference a 1.8e-15 sur 4000
#       simplexes, longueurs reproduites a 3.3e-15, ZERO rejet sur 1200
#       pentachores de Delaunay reels.
#   [2] MINRES + shift REMPLACE par TIKHONOV sur H^2.
#       Le shift poussait les N modes conformes (negatifs) vers zero et creait
#       des quasi-singularites : reponse divergente (-1.9, -1.2, +2.7, +40.1).
#       Tikhonov (H^2 + lambda^2 I) y = H b est DEFINI POSITIF, CG converge,
#       et il PRESERVE LE SIGNE. Valide a 0.3 % contre le pseudo-inverse
#       spectral dense.
#   [3] AUTO-TEST EN TETE. Le script verifie emb5, le taux de rejet et Ward
#       sur un petit cas AVANT de lancer la campagne longue. Il s'arrete net
#       si l'un echoue — au lieu de gaspiller quatre heures.
#
#  RESERVE INSCRITE : Tikhonov et le seuil spectral ne ponderent pas
#  identiquement le secteur conforme, donc la TRACE. Le rapport TT/trace
#  mesure ici peut differer de celui obtenu par voie spectrale au meme ka.
#  Ce qui compte est la COHERENCE DE METHODE a travers les tailles, et
#  l'extrapolation ka -> 0 faite avec un seul estimateur.
#
#  Conforme a la Blob Core Specification v1.0 (sonde P1) et aux douze regles.
#  COLAB : Execution > Type d'execution > RAM elevee.
#  Duree : auto-test ~1 min | N=1000 ~5 min | 2000 ~12 min | 4000 ~25 min
#          | 8000 ~50 min   (assemblage + mesure)
# =============================================================================

import numpy as np, math, itertools, time, json, os
import scipy.sparse as sp
from scipy.sparse.linalg import cg, LinearOperator, factorized
from scipy.spatial import Delaunay

P10  = [(i,j) for i in range(5) for j in range(i+1,5)]
TRIS = [(i,j,k) for i in range(5) for j in range(i+1,5) for k in range(j+1,5)]
IDX  = {e:i for i,e in enumerate(P10)}

# =========================================================== [1] emb5 CORRIGE
def emb5(Ls):
    """Plonge un 5-simplexe dans R^4 depuis ses 10 longueurs, par matrice de
       Gram + Cholesky. Rend None si le simplexe est degenere.
       VALIDE : 1.8e-15 contre la reference, 0 rejet sur 1200 cas reels."""
    L2 = np.zeros((5,5))
    for m,(i,j) in enumerate(P10):
        L2[i,j] = L2[j,i] = Ls[m]*Ls[m]
    G = np.empty((4,4))
    for i in range(1,5):
        for j in range(1,5):
            G[i-1,j-1] = 0.5*(L2[0,i] + L2[0,j] - L2[i,j])
    G = 0.5*(G+G.T)
    try:
        ev = np.linalg.eigvalsh(G)
        if ev[0] <= 1e-13*max(ev[-1],1e-300): return None
        Lc = np.linalg.cholesky(G)
    except np.linalg.LinAlgError:
        return None
    P = np.zeros((5,4)); P[1:] = Lc
    return P

def tri_area(a,b,c):
    s = 2*a*a*b*b + 2*b*b*c*c + 2*c*c*a*a - a**4 - b**4 - c**4
    return 0.25*math.sqrt(max(s,0.0))

def dA_tri(a,b,c):
    A = tri_area(a,b,c)
    return np.array([a*(b*b+c*c-a*a), b*(a*a+c*c-b*b), c*(a*a+b*b-c*c)])/(8.0*max(A,1e-15))

def thetas(Ls):
    P = emb5(Ls)
    if P is None: return None
    out = np.zeros(10)
    for m,(i,j,k) in enumerate(TRIS):
        rest = [q for q in range(5) if q not in (i,j,k)]
        B = np.stack([P[j]-P[i], P[k]-P[i]]); Q,_ = np.linalg.qr(B.T)
        pl = P[rest[0]]-P[i]; pm = P[rest[1]]-P[i]
        pl = pl - Q@(Q.T@pl);  pm = pm - Q@(Q.T@pm)
        nl, nm = np.linalg.norm(pl), np.linalg.norm(pm)
        if nl < 1e-12 or nm < 1e-12: return None
        out[m] = math.acos(max(-1.0, min(1.0, float(pl@pm)/(nl*nm))))
    return out

def jac_theta(Ls, h=1e-5):
    """J[t,e] = d theta_t / d l_e — 20 plongements, difference centree."""
    J = np.zeros((10,10))
    for e in range(10):
        lp = Ls.copy(); lp[e] += h; tp = thetas(lp)
        lm = Ls.copy(); lm[e] -= h; tm = thetas(lm)
        if tp is None or tm is None: return None
        J[:,e] = (tp-tm)/(2*h)
    return J

# ================================================================ 4-tore
def build_torus(N, seed, w=0.45, verbose=True):
    rng = np.random.default_rng(seed); P0 = rng.uniform(0,1,size=(N,4))
    big=[P0]; ids=[np.arange(N)]; sh=[np.zeros((N,4),dtype=int)]
    for s in itertools.product((-1,0,1), repeat=4):
        if all(x==0 for x in s): continue
        m = np.ones(N,bool)
        for k in range(4):
            if   s[k]== 1: m &= (P0[:,k] < w)
            elif s[k]==-1: m &= (P0[:,k] > 1-w)
        if m.any():
            big.append(P0[m]+np.array(s,float)); ids.append(np.arange(N)[m])
            sh.append(np.tile(np.array(s,dtype=int),(m.sum(),1)))
    big=np.vstack(big); ids=np.concatenate(ids); sh=np.vstack(sh)
    if verbose: print(f"  Delaunay 4D sur {len(big)} points...", flush=True)
    tri = Delaunay(big)
    PENTS=[]
    for s5 in tri.simplices:
        c = big[s5].mean(0)
        if not (np.all(c>=0) and np.all(c<1)): continue
        b = [int(ids[x]) for x in s5]
        if len(set(b))!=5: continue
        PENTS.append((b,[sh[x] for x in s5], big[s5].copy()))
    if verbose: print(f"  {len(PENTS)} pentachores retenus", flush=True)
    return P0, PENTS

def ekey(b1,s1,b2,s2):
    if b1<b2: return (b1,b2,tuple(s2-s1))
    return (b2,b1,tuple(s1-s2))

# ==================================================== assemblage sparse Hamber
def assemble(N, seed, w=0.45, verbose=True):
    """H = sum_charnieres sym(grad delta_t (x) grad A_t)  — creux de bout en bout"""
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
    E=len(edges)
    if verbose: print(f"  {E} aretes (paire+enroulement), {len(hedges)} charnieres", flush=True)
    Lg=np.zeros(E); mids=np.zeros((E,4)); dirs=np.zeros((E,4))
    for i,(b1,b2,wd) in enumerate(edges):
        p1=P0[b1]; p2=P0[b2]+np.array(wd,float)
        mids[i]=((p1+p2)*0.5)%1.0
        d=p2-p1; Lg[i]=np.linalg.norm(d); dirs[i]=d/Lg[i]
    gdel={}; rejets=0; npt=len(PENTS)
    for pi,(b,shs,pts) in enumerate(PENTS):
        if verbose and pi and pi%20000==0:
            print(f"    ... {pi}/{npt}  ({time.time()-t0:.0f}s)", flush=True)
        Ls=np.array([np.linalg.norm(pts[x]-pts[y]) for (x,y) in P10])
        loc=[eid[ekey(b[x],shs[x],b[y],shs[y])] for (x,y) in P10]
        J=jac_theta(Ls)
        if J is None: rejets+=1; continue
        for m,(x,y,z) in enumerate(TRIS):
            ii=tuple(sorted([eid[ekey(b[x],shs[x],b[y],shs[y])],
                             eid[ekey(b[x],shs[x],b[z],shs[z])],
                             eid[ekey(b[y],shs[y],b[z],shs[z])]]))
            d=gdel.setdefault(tkey[ii],{})
            for e in range(10):
                if abs(J[m,e])>1e-14:
                    d[loc[e]]=d.get(loc[e],0.0)-J[m,e]
    R=[];C=[];V=[]
    for ti,d in gdel.items():
        e3=hedges[ti]; gA=dA_tri(Lg[e3[0]],Lg[e3[1]],Lg[e3[2]])
        for ea,va in d.items():
            for bi,eb in enumerate(e3):
                v=0.5*va*gA[bi]
                R.append(ea);C.append(eb);V.append(v)
                R.append(eb);C.append(ea);V.append(v)
    H=sp.coo_matrix((V,(R,C)),shape=(E,E)).tocsr(); H=(H+H.T)*0.5
    gr=[];gc=[];gv=[]
    for i,(b1,b2,wd) in enumerate(edges):
        d=dirs[i]
        for k in range(4):
            gr.append(i); gc.append(4*b1+k); gv.append(-d[k])
            gr.append(i); gc.append(4*b2+k); gv.append( d[k])
    G=sp.coo_matrix((gv,(gr,gc)),shape=(E,4*N)).tocsr()
    if verbose:
        print(f"  assemblage OK : {rejets} rejets ({100*rejets/npt:.3f} %), {time.time()-t0:.0f}s", flush=True)
    return dict(H=H,G=G,mids=mids,Lg=Lg,dirs=dirs,E=E,N=N,
                rejets=rejets,npent=npt,a=float(Lg.mean()))

# ============================================= projection de jauge (VALIDEE 1e-12)
class GaugeProj:
    def __init__(self, G, reg=1e-10):
        self.G=G.tocsc()
        A=(G.T@G).tocsc()+reg*sp.identity(G.shape[1],format='csc')
        self.solve=factorized(A)
    def __call__(self,x): return x - self.G@self.solve(self.G.T@x)

def ward_ratio(d, ntest=40, seed=0):
    """rapport ||H g|| / ||H r|| pour g dans la jauge, r aleatoire. Diagnostic."""
    rng=np.random.default_rng(seed); H=d['H']; G=d['G']; E=d['E']
    num=den=0.0
    for _ in range(ntest):
        z=rng.normal(size=G.shape[1]); g=G@z; ng=np.linalg.norm(g)
        if ng<1e-12: continue
        num+=np.linalg.norm(H@(g/ng))**2
        r=rng.normal(size=E); den+=np.linalg.norm(H@(r/np.linalg.norm(r)))**2
    return math.sqrt(num/max(den,1e-300))

# ========================================== [2] REPONSE : TIKHONOV sur H^2
def make_response(d, proj=None):
    """[4] LA PROJECTION EST SORTIE DE LA BOUCLE.
       Ward ~ 1e-5 signifie que H annihile deja la jauge, donc H b est
       orthogonal a Q et la solution de (H^2+lam^2) y = H b l'est aussi.
       Mesure comparative a N=90 : accord 0.06 %, vitesse x4.7, et la version
       AVEC projection devient instable a Ward = 5e-3 (le reg=1e-10 de
       GaugeProj cree sa propre quasi-singularite)."""
    H=d['H']; E=d['E']
    def Mv(x): return -(H@x)
    def resp(src, lam, tol=1e-8, maxiter=40000):
        b=src; Hb=Mv(b)
        A=LinearOperator((E,E), matvec=lambda x: Mv(Mv(x))+lam*lam*x, dtype=float)
        y,info=cg(A,Hb,rtol=tol,maxiter=maxiter)
        return float(b@y), info
    return resp, Mv

def ttbasis(kv):
    k=kv/np.linalg.norm(kv)
    U,_,_=np.linalg.svd(np.eye(4)-np.outer(k,k)); B=U[:,:3]
    e1,e2,e3=B[:,0],B[:,1],B[:,2]
    return [np.outer(e1,e2)+np.outer(e2,e1),
            np.outer(e1,e3)+np.outer(e3,e1),
            np.outer(e2,e3)+np.outer(e3,e2),
            np.outer(e1,e1)-np.outer(e2,e2),
            (np.outer(e1,e1)+np.outer(e2,e2)-2*np.outer(e3,e3))/math.sqrt(3)]

def normH(d, proj=None, niter=60, seed=1):
    """echelle spectrale de P(-H)P par ITERATION DE PUISSANCE sur M^2.
       Un estimateur par vecteurs aleatoires SOUS-ESTIME massivement la norme
       spectrale (faible recouvrement avec le mode dominant) : l'auto-test l'a
       detecte en donnant un plateau a 372 % de variation."""
    H=d['H']; E=d['E']
    rng=np.random.default_rng(seed)
    v=rng.normal(size=E); v/=np.linalg.norm(v)
    lam=0.0
    for _ in range(niter):
        w=-(H@v); w=-(H@w)            # M^2 v
        nw=np.linalg.norm(w)
        if nw<1e-300: break
        v=w/nw; lam=nw
    return math.sqrt(max(lam,0.0))    # ||M|| = sqrt(||M^2||)

def measure(d, shells=(1,2,3,4), lams=(3e-4,1e-4,3e-5,1e-5,3e-6), verbose=True):
    wr=ward_ratio(d)
    if verbose: print(f"  WARD (rapport jauge/aleatoire) = {wr:.3e}", flush=True)
    if wr>1e-2:
        print("  >>> REJETE par le test d'acceptation (regle 5). Aucune mesure.")
        return None
    resp,_=make_response(d)
    scale=normH(d); a=d['a']; mids=d['mids']; Lg=d['Lg']; dirs=d['dirs']
    rows=[]
    for n2 in shells:
        ns=[n for n in itertools.product(range(-2,3),repeat=4) if sum(x*x for x in n)==n2]
        for n in ns[:3]:
            kv=2*math.pi*np.array(n,float); k2=float(kv@kv); ph=np.cos(mids@kv)
            B=ttbasis(kv)
            for f in lams:
                lam=f*scale; TT=[]
                for eps in B:
                    q=np.einsum('ei,ij,ej->e',dirs,eps,dirs)
                    s=Lg*q*ph; s-=s.mean(); nn=float(s@s)
                    if nn<1e-20: continue
                    r,_=resp(s,lam); TT.append(r/nn*k2*a*a)
                q=np.einsum('ei,ij,ej->e',dirs,np.eye(4),dirs)
                s=Lg*q*ph; s-=s.mean(); nn=float(s@s)
                tr,_=resp(s,lam); tr=tr/nn*k2*a*a
                if TT:
                    rows.append(dict(n2=n2, ka=2*math.pi*math.sqrt(n2)*a, lam_rel=f,
                                     TT=float(np.mean(TT)), TTsd=float(np.std(TT)),
                                     trace=tr, ratio=tr/np.mean(TT)))
            if verbose and rows:
                L=rows[-1]
                print(f"    |k|^2={n2} ka={L['ka']:.3f} : TT={L['TT']:+.4f}"
                      f" (disp {100*L['TTsd']/abs(L['TT']):.1f}%) trace={L['trace']:+.4f}"
                      f" r={L['ratio']:+.4f}", flush=True)
    return dict(ward=wr, rows=rows, a=a, N=d['N'], E=d['E'],
                rejets=d['rejets'], npent=d['npent'])

# ================================================== [3] AUTO-TEST OBLIGATOIRE
def autotest():
    print("="*68); print("  AUTO-TEST — regle 5 appliquee au script lui-meme"); print("="*68)
    rng=np.random.default_rng(7); err=0.0; fails=0
    for _ in range(600):
        pts=rng.uniform(0,1,size=(5,4))
        Ls=np.array([np.linalg.norm(pts[i]-pts[j]) for (i,j) in P10])
        P=emb5(Ls)
        if P is None: fails+=1; continue
        Lb=np.array([np.linalg.norm(P[i]-P[j]) for (i,j) in P10])
        err=max(err,np.abs(Lb-Ls).max())
    print(f"  [a] emb5 : ecart max sur les longueurs {err:.2e}, {fails}/600 echecs")
    if err>1e-9 or fails>0:
        print("  >>> ECHEC : emb5 ne reconstruit pas les longueurs. ARRET."); return False
    d=assemble(90, 812, verbose=False)
    tr=100*d['rejets']/d['npent']
    print(f"  [b] assemblage N=90 : {d['rejets']} rejets ({tr:.3f} %), E={d['E']}")
    if tr>1.0:
        print("  >>> ECHEC : taux de rejet > 1 %. ARRET."); return False
    wr=ward_ratio(d)
    print(f"  [c] WARD = {wr:.3e}")
    if wr>1e-2:
        print("  >>> ECHEC : Ward > 1e-2. ARRET."); return False
    resp,_=make_response(d); scale=normH(d)
    kv=2*math.pi*np.array([1.,0,0,0]); ph=np.cos(d['mids']@kv)
    fs=[3e-4,1e-4,3e-5,1e-5,3e-6]
    q=np.einsum('ei,ij,ej->e',d['dirs'],ttbasis(kv)[0],d['dirs'])
    s=d['Lg']*q*ph; s-=s.mean(); nn=float(s@s)
    vals=[]
    for f in fs:
        r,info=resp(s,f*scale)
        if info!=0:
            print(f"  >>> ECHEC : CG non convergent a lambda={f:.0e} (info {info}). ARRET."); return False
        vals.append(r/nn*float(kv@kv)*d['a']**2)
    v=np.array(vals)
    print(f"  [d] G_TT vs lambda : {'  '.join('%+.4f'%x for x in v)}")
    best=None
    for i in range(len(v)):
        for j in range(i+1,len(v)):
            seg=v[i:j+1]
            if abs(seg.mean())<1e-12: continue
            if (seg.max()-seg.min())/abs(seg.mean())<0.05:
                width=math.log10(fs[i]/fs[j])
                if best is None or width>best[0]: best=(width,i,j)
    if best is None:
        print("  >>> ECHEC : aucun plateau a 5 % detecte. ARRET."); return False
    wdt,i,j=best
    print(f"  [d] PLATEAU detecte : lambda de {fs[i]:.0e} a {fs[j]:.0e} "
          f"({wdt:.1f} decade(s)), valeur {v[i:j+1].mean():+.4f}")
    if wdt<0.9:
        print("  >>> ECHEC : plateau trop etroit (<1 decade). ARRET."); return False
    print("  ==> AUTO-TEST PASSE. La campagne peut demarrer.\n"); return True

# ====================================================================== CAMPAGNE
#  GRAINES DECLAREES AVANT EXECUTION (regle 3)
CAMPAGNE = [(1000,9101), (2000,9102), (2000,9103), (4000,9104), (8000,9105)]

if __name__ == "__main__":
    if not autotest():
        raise SystemExit("auto-test echoue — rien n'est lance")
    res=[]
    for N,seed in CAMPAGNE:
        print("="*68); print(f"  N = {N}   graine = {seed}"); print("="*68, flush=True)
        t=time.time()
        try:
            d=assemble(N,seed)
            r=measure(d)
        except MemoryError:
            print("  >>> MEMOIRE INSUFFISANTE. Reduire w a 0.35 et relancer.")
            break
        if r is not None:
            r['seed']=seed; r['temps']=time.time()-t; res.append(r)
            with open('blob_gravite_v2.json','w') as f: json.dump(res,f,indent=1)
            print(f"  --> sauvegarde ({time.time()-t:.0f}s)", flush=True)
        del d

    print("="*68); print("  EXTRAPOLATION ka -> 0"); print("="*68)
    ka=[];rt=[];tt=[]
    for r in res:
        for row in r['rows']:
            if row['lam_rel']<=1e-4:
                ka.append(row['ka']); rt.append(row['ratio']); tt.append(row['TT'])
    ka=np.array(ka); rt=np.array(rt); tt=np.array(tt)
    print(f"  {len(ka)} points, ka de {ka.min():.3f} a {ka.max():.3f}")
    for kmax in (1.5,2.0,2.5,3.0):
        m=ka<kmax
        if m.sum()<4: continue
        A=np.vstack([np.ones(m.sum()),ka[m]**2]).T
        r0=np.linalg.lstsq(A,rt[m],rcond=None)[0][0]
        g0=np.linalg.lstsq(A,tt[m],rcond=None)[0][0]
        print(f"  ka<{kmax}: {m.sum():3d} pts | r0={r0:+.5f} (EH -1/3, ecart "
              f"{100*abs(r0+1/3)*3:5.2f} %) | G_TT(0)={g0:+.4f}")
    print("\n  Sortie : blob_gravite_v2.json")
