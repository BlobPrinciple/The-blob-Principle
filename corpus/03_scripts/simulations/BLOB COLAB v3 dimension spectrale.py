# =============================================================================
#  BLOB PRINCIPLE — DIMENSION SPECTRALE PAR NOYAU DE LA CHALEUR
#  Campagne Colab : N jusqu'a 8000 en 3D, 600 en 4D. Aucune valeur propre.
#
#  POURQUOI CE SCRIPT EXISTE
#  Trois chantiers du corpus butent sur le MEME mur : ~5 mailles par dimension.
#  Pour d_s, la diagonalisation complete est impossible au-dela de N~400
#  (dim ~ 27N). La sortie est la TRACE STOCHASTIQUE : Hutchinson + quadrature
#  de Lanczos, qui donne Tr(exp(-t*Delta)) sans jamais calculer un spectre.
#
#  CHAQUE PIECE A ETE VALIDEE LOCALEMENT AVANT EXPEDITION
#   [1] etoile de Hodge : somme|v*| = 1 a 3.8e-15 sur 3 tailles (pavage Voronoi)
#   [2] rembourrage ADAPTATIF sur l'invariant de pavage primal — un w fixe
#       donnait un pentachore duplique et 4e-3 d'erreur
#   [3] orientation CANONIQUE des bords — l'ordre local donnait Betti [1,0,0,0]
#       au lieu de [1,3,3,1]
#   [4] chaines construites DEPUIS LE HAUT — les coordonnees d'un sous-simplexe
#       stocke depuis un autre translate rendaient le dual faux (somme = 2.4)
#   [5] Lanczos m=250 : a m=40 l'erreur etait de 100 %. Le spectre couvre six
#       ordres de grandeur (32 a 2.05e6) a cause des simplexes fins.
#   Validation finale : max d_s stochastique contre exact, ecart 0.06 a 0.08.
#
#  COLAB : RAM elevee. Duree : N=1000 ~2min | 3000 ~8min | 8000 ~35min
# =============================================================================

import numpy as np, math, itertools, time, json
import scipy.sparse as sp
from scipy.spatial import Delaunay

# ------------------------------------------------------------------ geometrie
def circumcenter(pts):
    p0=pts[0]; V=pts[1:]-p0
    if len(V)==0: return p0.copy()
    G=V@V.T; b=0.5*np.einsum('ij,ij->i',V,V)
    try: lam=np.linalg.solve(G,b)
    except np.linalg.LinAlgError: return None
    return p0+lam@V

def svol(pts):
    V=pts[1:]-pts[0]
    if len(V)==0: return 0.0
    G=V@V.T; d=np.linalg.det(G)
    return math.sqrt(d)/math.factorial(len(V)) if d>0 else 0.0

def canon(vs,pos):
    """[3] ordre CANONIQUE, independant du simplexe parent"""
    o=int(np.argmin(vs)); r=pos[o]
    tags=[(vs[i],tuple(np.round(pos[i]-r,7))) for i in range(len(vs))]
    perm=sorted(range(len(vs)),key=lambda i:tags[i])
    return tuple(tags[i] for i in perm), perm
KF=lambda vs,pos: canon(vs,pos)[0]

def build(N,seed,n,w):
    rng=np.random.default_rng(seed); P0=rng.uniform(0,1,size=(N,n))
    big=[P0]; ids=[np.arange(N)]
    for s in itertools.product((-1,0,1),repeat=n):
        if all(x==0 for x in s): continue
        m=np.ones(N,bool)
        for k in range(n):
            if   s[k]== 1: m&=(P0[:,k]<w)
            elif s[k]==-1: m&=(P0[:,k]>1-w)
        if m.any(): big.append(P0[m]+np.array(s,float)); ids.append(np.arange(N)[m])
    big=np.vstack(big); ids=np.concatenate(ids)
    tri=Delaunay(big); T=[]
    for s in tri.simplices:
        c=big[s].mean(0)
        if np.all(c>=0) and np.all(c<1):
            b=[int(ids[x]) for x in s]
            if len(set(b))==n+1: T.append((b,big[s].copy()))
    return T

def pvol(T,n):
    fa=math.factorial(n)
    return sum(abs(np.linalg.det(np.array([p[i]-p[0] for i in range(1,n+1)])))/fa for b,p in T)

def build_adaptive(N,seed,n,verbose=True):
    """[2] on augmente w jusqu'a ce que le pavage PRIMAL soit exact"""
    for w in (0.45,0.55,0.65,0.75,0.85,0.95):
        T=build(N,seed,n,w); v=pvol(T,n)
        if verbose: print(f"    w={w:.2f} : {len(T)} top-simplexes, volume primal {v:.10f}",flush=True)
        if abs(v-1)<1e-10: return T,w
    return None,None

# -------------------------------------------------------- [4] dual DEPUIS LE HAUT
def dual_from_top(TOPS,n):
    dual=[dict() for _ in range(n+1)]
    prim=[dict() for _ in range(n+1)]
    for base,pts in TOPS:
        pts=np.asarray(pts,dtype=float)
        cc={}
        for k in range(n+1):
            for c in itertools.combinations(range(n+1),k+1):
                cc[c]=circumcenter(pts[list(c)])
                kk=KF([base[i] for i in c],[pts[i] for i in c])
                if kk not in prim[k]: prim[k][kk]=svol(pts[list(c)])
                if kk not in dual[k]: dual[k][kk]=0.0
        for k in range(n+1):
            for c in itertools.combinations(range(n+1),k+1):
                if cc[c] is None: continue
                kk0=KF([base[i] for i in c],[pts[i] for i in c])
                stack=[(c,[cc[c]],1.0)]
                while stack:
                    cur,chain,sg=stack.pop()
                    if len(cur)==n+1:
                        dual[k][kk0]+=sg*svol(np.array(chain)); continue
                    for j in range(n+1):
                        if j in cur: continue
                        nxt=tuple(sorted(cur+(j,)))
                        cn=cc[nxt]; ck=cc[cur]
                        if cn is None or ck is None: continue
                        wv=pts[j]-ck
                        if len(cur)>1:
                            B=pts[list(cur)][1:]-pts[list(cur)][0]
                            Q,_=np.linalg.qr(B.T); wv=wv-Q@(Q.T@wv)
                        s=1.0 if float((cn-ck)@wv)>=0 else -1.0
                        stack.append((nxt,chain+[cn],sg*s))
    return dual,prim

# ------------------------------------------- Laplacien de Hodge METRIQUE
def hodge_laplacian(TOPS,n,verbose=True):
    dual,prim=dual_from_top(TOPS,n)
    tv=sum(dual[0].values())
    if verbose: print(f"    VALIDATION dual : somme|v*| = {tv:.10f} (ecart {abs(tv-1):.1e})",flush=True)
    if abs(tv-1)>1e-8: return None,None,None
    idx=[{kk:i for i,kk in enumerate(prim[k])} for k in range(n+1)]
    f=[len(prim[k]) for k in range(n+1)]
    dm=[]
    for k in range(n):
        R=[];C=[];V=[];seen=set()
        for base,pts in TOPS:
            for c in itertools.combinations(range(n+1),k+2):
                vs=[base[i] for i in c]; pp=[pts[i] for i in c]
                kk1,perm=canon(vs,pp)
                if kk1 in seen: continue
                seen.add(kk1); i1=idx[k+1][kk1]
                vsc=[vs[i] for i in perm]; ppc=[pp[i] for i in perm]
                for m in range(len(vsc)):
                    kk0,_=canon([vsc[i] for i in range(len(vsc)) if i!=m],
                                [ppc[i] for i in range(len(ppc)) if i!=m])
                    if kk0 in idx[k]: R.append(i1);C.append(idx[k][kk0]);V.append((-1)**m)
        dm.append(sp.coo_matrix((V,(R,C)),shape=(f[k+1],f[k])).tocsr())
    for k in range(n-1):
        z=(dm[k+1]@dm[k])
        mx=abs(z).max() if z.nnz else 0.0
        if mx>1e-12:
            print(f"    >>> d o d = {mx:.2e} != 0, orientation fautive"); return None,None,None
    if verbose: print("    d o d = 0 verifie a tous les niveaux",flush=True)
    star=[]
    for k in range(n+1):
        pv=np.array([prim[k][kk] if k>0 else 1.0 for kk in prim[k]])
        dv=np.array([dual[k][kk] if k<n else 1.0 for kk in prim[k]])
        star.append(np.maximum(np.where(pv>1e-14,dv/np.maximum(pv,1e-300),1.0),1e-12))
    Dw=[(sp.diags(np.sqrt(star[k+1]))@dm[k]@sp.diags(1.0/np.sqrt(star[k]))).tocsr() for k in range(n)]
    B=[]
    for k in range(n+1):
        A=sp.csr_matrix((f[k],f[k]))
        if k<n: A=A+(Dw[k].T@Dw[k])
        if k>0: A=A+(Dw[k-1]@Dw[k-1].T)
        B.append(A)
    return sp.block_diag(B,format='csr'),f,star

# ------------------------------ [5] TRACE STOCHASTIQUE (Hutchinson + Lanczos)
def lanczos_quad(A,z,ts,m):
    Nd=len(z); nz=np.linalg.norm(z); q=z/nz
    Q=[q]; al=[]; be=[]; qm=np.zeros(Nd); b=0.0
    for j in range(m):
        v=A@Q[-1]-b*qm
        a=float(Q[-1]@v); v=v-a*Q[-1]
        for u in Q: v=v-float(u@v)*u
        bb=np.linalg.norm(v)
        al.append(a); qm=Q[-1]
        if bb<1e-12: break
        be.append(bb); Q.append(v/bb); b=bb
    k=len(al)
    T=np.diag(al)+np.diag(be[:k-1],1)+np.diag(be[:k-1],-1)
    th,S=np.linalg.eigh(T); wq=S[0,:]**2
    return np.array([nz*nz*float(np.sum(wq*np.exp(-t*th))) for t in ts])

def heat_trace(A,ts,nprobe=16,m=250,seed=0,verbose=True):
    rng=np.random.default_rng(seed); acc=np.zeros(len(ts)); t0=time.time()
    for p in range(nprobe):
        acc+=lanczos_quad(A,rng.choice([-1.0,1.0],size=A.shape[0]),ts,m)
        if verbose and (p+1)%4==0:
            print(f"      sonde {p+1}/{nprobe}  ({time.time()-t0:.0f}s)",flush=True)
    return acc/nprobe

def ds_curve(P,ts): return -2*np.gradient(np.log(P),np.log(ts))

# ============================================================== AUTO-TEST
def autotest():
    print("="*68); print("  AUTO-TEST"); print("="*68)
    TOPS,w=build_adaptive(90,802,3,verbose=False)
    if TOPS is None: print("  [a] ECHEC : aucun rembourrage ne pave. ARRET."); return False
    print(f"  [a] pavage primal exact a w={w:.2f} ({len(TOPS)} tetraedres)")
    A,f,star=hodge_laplacian(TOPS,3,verbose=True)
    if A is None: print("  ECHEC assemblage. ARRET."); return False
    ev=[np.sort(np.linalg.eigvalsh(A[sum(f[:k]):sum(f[:k+1]),sum(f[:k]):sum(f[:k+1])].toarray()))
        for k in range(4)]
    z=[int((e<1e-7*max(e[-1],1)).sum()) for e in ev]
    print(f"  [b] Betti = {z}   [T^3 attendu : 1,3,3,1]")
    if z!=[1,3,3,1]: print("  ECHEC : Betti faux. ARRET."); return False
    ts=np.logspace(-3.4,-0.4,26)
    lam=np.sort(np.concatenate(ev))
    dex=ds_curve(np.array([np.exp(-t*lam).sum() for t in ts]),ts)
    dst=ds_curve(heat_trace(A,ts,nprobe=16,m=250,seed=3,verbose=False),ts)
    e=abs(dex.max()-dst.max())
    print(f"  [c] max d_s : exact {dex.max():.4f} | stochastique {dst.max():.4f} | ecart {e:.4f}")
    if e>0.15: print("  ECHEC : estimateur stochastique hors tolerance. ARRET."); return False
    print("  ==> AUTO-TEST PASSE.\n"); return True

# ================================================================= CAMPAGNE
#  GRAINES DECLAREES AVANT EXECUTION
CAMPAGNE=[(3,1000,9201),(3,3000,9202),(3,8000,9203),(4,200,9211),(4,600,9212)]

if __name__=="__main__":
    if not autotest(): raise SystemExit("auto-test echoue")
    out=[]
    ts=np.logspace(-4.0,-0.2,34)
    for n,N,seed in CAMPAGNE:
        print("="*68); print(f"  dim={n}  N={N}  graine={seed}   ({N**(1.0/n):.2f} mailles/dim)")
        print("="*68,flush=True)
        t0=time.time()
        TOPS,w=build_adaptive(N,seed,n)
        if TOPS is None: print("  pavage impossible, on passe"); continue
        A,f,star=hodge_laplacian(TOPS,n)
        if A is None: continue
        print(f"    f={f}  dim={A.shape[0]}  ({time.time()-t0:.0f}s)",flush=True)
        P=heat_trace(A,ts,nprobe=16,m=250,seed=seed)
        ds=ds_curve(P,ts); i=int(np.argmax(ds))
        r=dict(dim=n,N=N,seed=seed,w=w,f=f,ndim=int(A.shape[0]),
               ts=ts.tolist(),P=P.tolist(),ds=ds.tolist(),
               ds_max=float(ds[i]),t_max=float(ts[i]),temps=time.time()-t0)
        out.append(r)
        with open('blob_ds_v3.json','w') as fp: json.dump(out,fp)
        print(f"    >>> max d_s = {ds[i]:.4f} a t = {ts[i]:.5f}   [attendu {n}]   ({time.time()-t0:.0f}s)",flush=True)
    print("="*68); print("  SYNTHESE"); print("="*68)
    for n in (3,4):
        v=[(r['N'],r['ds_max']) for r in out if r['dim']==n]
        if v:
            print(f"  dim={n} : " + " | ".join(f"N={N} -> {d:.3f}" for N,d in v) + f"   [attendu {n}]")
    print("\n  Sortie : blob_ds_v3.json")
