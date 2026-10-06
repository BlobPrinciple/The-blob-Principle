"""
================================================================================
 BLOB — RELANCE DES VOIES :  (A) TEST DE MORT de la queue de calcification
                             (B) RONDEUR K-L v2 blindee (temoin positif S3)
================================================================================
 MODULE A — La distribution de calcification (triangles/sommet = la masse, CVI)
 a une queue POWER-LAW (Dll=+280/+790 vs exp) d'exposant alpha_PL=1,66+/-0,05,
 N-stable, kappa en ZONE GRISE (2,0 sigma) — le pattern exact d'alpha_flow v1.
 PROTOCOLE DE MORT PRE-DECLARE (tribunal R1) :
   4 graines x {kappa=6,6 ; 9,0} x {N=2000, 5000, 20000, 50000}
   xmin scanne {q70, q75, q80} (robustesse au choix de coupure)
   SEUILS : <2 sigma compatible | >3 sigma enterre.
 INTERDIT (paragraphe C.3, R7) : identifier une fraction simple avant verdict.

 MODULE B — Le verrou C (de Sitter) a ete ROUVERT par la rondeur de
 Klitgaard-Loll a ~3 sigma (V222 paragraphe 123.1). Blindage requis :
   - temoin POSITIF : RGG sur la 3-sphere S3 (courbure positive vraie)
   - multi-N : 20000 et 50000 (controle taille finie)
   - n x 4 : 240 paires par delta, deltas 1..8.
 Lecture attendue si la rondeur du Blob est reelle : pente(S3) < pente(Blob)
 < pente(RGG plat ~ 0), avec l'ER en effondrement petit-monde.

 USAGE COLAB :  !pip -q install numba   puis   %run blob_mort_queue_et_rondeur_v2.py
 Duree : module A ~20-40 min ; module B ~40-80 min.
 JSON continus : queue_mort.json, rondeur_v2.json.
================================================================================
"""
import time, math, json, gc
import numpy as np
from numba import njit
from scipy.spatial import cKDTree

import math
import numpy as np
from numba import njit
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix

# =============================== CONFIG =======================================
# Balayage en taille : un JSON COMPLET est sauve par palier (immediatement).
N_SWEEP   = [5_000, 10_000, 25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000]
KAPPA     = 6.6       # degre moyen (point de travail du corpus)
BETA      = 0.30      # poids de la viabilite
TAU       = 0.50      # temperature
THERM_FAC = 130       # pas de thermalisation = THERM_FAC * N  (corpus = 130)
POOL_FAC  = 1.6       # rayon du pool de candidats = POOL_FAC * r_arete
SEED      = 0
CAP       = 64        # capacite max du tableau de voisins (degre plafonne)
OUTDIR    = "."       # dossier de sortie (JSON + figures)

# --- mesure ---
N_SRC_DF  = 200       # sources BFS pour d_f
N_START   = 48        # departs de marche pour d_s / d_w (baisser a 32 si N>=500k lent)
T_CAP     = 3000      # plafond du nb de pas de marche (cout ~ E*N_START*T)
N_CHUNKS  = 13        # nb de blocs de thermalisation (affichage du n_tri)
# ==============================================================================


# ----------------------------- NUMBA : graphe --------------------------------
@njit(cache=True)
def build_nbr_arrays(edges, N, cap):
    nbr = np.full((N, cap), -1, dtype=np.int32)
    deg = np.zeros(N, dtype=np.int32)
    for e in range(edges.shape[0]):
        a = edges[e, 0]; b = edges[e, 1]
        if deg[a] < cap:
            nbr[a, deg[a]] = b; deg[a] += 1
        if deg[b] < cap:
            nbr[b, deg[b]] = a; deg[b] += 1
    return nbr, deg


@njit(cache=True, inline='always')
def _has_edge(nbr, deg, a, b):
    for k in range(deg[a]):
        if nbr[a, k] == b:
            return True
    return False


@njit(cache=True, inline='always')
def _common(nbr, deg, u, v):
    # nombre de voisins communs de u et v (triangles passant par l'arete u-v)
    c = 0
    for k in range(deg[u]):
        x = nbr[u, k]
        for m in range(deg[v]):
            if nbr[v, m] == x:
                c += 1
                break
    return c


@njit(cache=True, inline='always')
def _remove(nbr, deg, u, v):
    du = deg[u]
    for k in range(du):
        if nbr[u, k] == v:
            nbr[u, k] = nbr[u, du - 1]
            nbr[u, du - 1] = -1
            deg[u] = du - 1
            return


@njit(cache=True, inline='always')
def _add(nbr, deg, a, b, cap):
    if deg[a] < cap:
        nbr[a, deg[a]] = b; deg[a] += 1
    if deg[b] < cap:
        nbr[b, deg[b]] = a; deg[b] += 1


@njit(cache=True)
def n_triangles(nbr, deg, N):
    # comptage total, une seule fois au depart. Chaque arete (u<v) compte ses
    # voisins communs = triangles passant par elle ; chaque triangle etant vu
    # par ses 3 aretes, on divise par 3.
    tot = 0
    for u in range(N):
        for k in range(deg[u]):
            v = nbr[u, k]
            if v > u:
                tot += _common(nbr, deg, u, v)
    return tot // 3


@njit(cache=True)
def mcmc_chunk(nbr, deg, edge_u, edge_v, pool_a, pool_b,
               beta, tau_eff, mean, nt0, nsteps, cap, seed):
    """Un bloc de nsteps de MCMC. Modifie nbr/deg/edge_* en place. Renvoie n_tri."""
    np.random.seed(seed)
    N = deg.shape[0]
    E = edge_u.shape[0]
    P = pool_a.shape[0]
    nt = nt0
    sumsq = 0.0
    for i in range(N):
        sumsq += deg[i] * deg[i]
    cv = math.sqrt(max(sumsq / N - mean * mean, 0.0)) / mean
    S = math.log(1.0 + nt) - beta * cv

    for _ in range(nsteps):
        io = np.random.randint(0, E)
        u = edge_u[io]; v = edge_v[io]
        # garde-fou de connectivite (leger) : ne pas appauvrir les noeuds rares
        if deg[u] <= 2 or deg[v] <= 2:
            continue
        # chercher une non-arete candidate (a,b) dans le pool, distincte de u,v
        a = -1; b = -1; ok = False
        for _try in range(40):
            pi = np.random.randint(0, P)
            ca = pool_a[pi]; cb = pool_b[pi]
            if ca == u or ca == v or cb == u or cb == v:
                continue
            if deg[ca] >= cap or deg[cb] >= cap:
                continue
            if not _has_edge(nbr, deg, ca, cb):
                a = ca; b = cb; ok = True; break
        if not ok:
            continue
        # triangles : perdus par retrait u-v, gagnes par ajout a-b
        # (les voisins communs ne dependent pas de l'existence de l'arete elle-meme)
        tl = _common(nbr, deg, u, v)
        tg = _common(nbr, deg, a, b)
        nt2 = nt - tl + tg
        du = deg[u]; dv = deg[v]; da = deg[a]; db = deg[b]
        nss = sumsq + (-2 * du + 1) + (-2 * dv + 1) + (2 * da + 1) + (2 * db + 1)
        cv2 = math.sqrt(max(nss / N - mean * mean, 0.0)) / mean
        S2 = math.log(1.0 + nt2) - beta * cv2
        if (S2 - S) >= 0.0 or np.random.random() < math.exp((S2 - S) / tau_eff):
            _remove(nbr, deg, u, v)
            _remove(nbr, deg, v, u)
            _add(nbr, deg, a, b, cap)
            nt = nt2; sumsq = nss; S = S2
            edge_u[io] = a; edge_v[io] = b
        # rejet -> rien a defaire (aucune modification n'a ete appliquee)
    return nt


# ----------------------------- NUMBA : parcours ------------------------------
@njit(cache=True)
def bfs_dist(nbr, deg, src, N):
    dist = np.full(N, -1, dtype=np.int32)
    queue = np.empty(N, dtype=np.int32)
    head = 0; tail = 0
    queue[tail] = src; tail += 1; dist[src] = 0
    while head < tail:
        x = queue[head]; head += 1
        dx = dist[x]
        for k in range(deg[x]):
            y = nbr[x, k]
            if dist[y] == -1:
                dist[y] = dx + 1
                queue[tail] = y; tail += 1
    return dist


@njit(cache=True)
def giant_component_mask(nbr, deg, N):
    comp = np.full(N, -1, dtype=np.int32)
    queue = np.empty(N, dtype=np.int32)
    best_id = -1; best_size = 0; cid = 0
    for s in range(N):
        if comp[s] != -1 or deg[s] == 0:
            continue
        head = 0; tail = 0
        queue[tail] = s; tail += 1; comp[s] = cid
        size = 0
        while head < tail:
            x = queue[head]; head += 1; size += 1
            for k in range(deg[x]):
                y = nbr[x, k]
                if comp[y] == -1:
                    comp[y] = cid
                    queue[tail] = y; tail += 1
        if size > best_size:
            best_size = size; best_id = cid
        cid += 1
    mask = (comp == best_id)
    return mask, best_size


@njit(cache=True)
def build_W_arrays(nbr, deg, N):
    """CSR de la marche paresseuse W (reste 1/2, sinon voisin uniforme)."""
    nnz = N
    for i in range(N):
        nnz += deg[i]
    indptr = np.zeros(N + 1, dtype=np.int64)
    indices = np.empty(nnz, dtype=np.int32)
    data = np.empty(nnz, dtype=np.float64)
    pos = 0
    for i in range(N):
        indptr[i] = pos
        indices[pos] = i
        data[pos] = 0.5 if deg[i] > 0 else 1.0
        pos += 1
        if deg[i] > 0:
            w = 0.5 / deg[i]
            for k in range(deg[i]):
                indices[pos] = nbr[i, k]
                data[pos] = w
                pos += 1
    indptr[N] = pos
    return indptr, indices, data


# ----------------------------- Python : outils -------------------------------
def build_geometric(N, kappa, pool_fac, seed):
    rng = np.random.default_rng(seed)
    pts = rng.random((N, 3))
    r = (kappa / ((N - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    tree = cKDTree(pts)
    pool = tree.query_pairs(pool_fac * r, output_type='ndarray').astype(np.int32)
    # trier le pool par distance ; les E0 plus courtes = aretes initiales
    # (fixe le degre moyen a EXACTEMENT kappa, comme le corpus E0 = N*kappa/2,
    #  sans le sous-comptage de bord du cube)
    dd = np.linalg.norm(pts[pool[:, 0]] - pts[pool[:, 1]], axis=1)
    pool = pool[np.argsort(dd)]
    E0 = min(int(round(N * kappa / 2)), len(pool))
    edges = pool[:E0].copy()
    return edges, pool, r


def running_slope(x, y, win=1.8):
    x = np.asarray(x, float); y = np.asarray(y, float)
    lx = np.log(x); ly = np.log(y)
    out = np.full(len(x), np.nan)
    for i in range(len(x)):
        m = (x >= x[i] / win) & (x <= x[i] * win) & np.isfinite(ly)
        if m.sum() >= 4:
            out[i] = np.polyfit(lx[m], ly[m], 1)[0]
    return out

CAP=64; POOL_FAC=1.6; THERM_FAC=120; N_CHUNKS=10

def therm_blob(N,kappa,seed):
    edges,pool,r=build_geometric(N,kappa,POOL_FAC,seed)
    nbr,deg=build_nbr_arrays(edges,N,CAP)
    eu=edges[:,0].copy();ev=edges[:,1].copy()
    pa=np.ascontiguousarray(pool[:,0]);pb=np.ascontiguousarray(pool[:,1])
    del pool,edges; gc.collect()
    mean=2.0*eu.shape[0]/N; nt=n_triangles(nbr,deg,N)
    total=THERM_FAC*N; chunk=max(1,total//N_CHUNKS)
    for c in range(N_CHUNKS):
        nt=mcmc_chunk(nbr,deg,eu,ev,pa,pb,0.30,0.5/N,mean,nt,chunk,CAP,seed*100+1+c)
    return nbr,deg

def raw_rgg(N,kappa,seed):
    edges,pool,r=build_geometric(N,kappa,POOL_FAC,seed)
    return build_nbr_arrays(edges,N,CAP)

def er_graph(N,kappa,seed):
    rng=np.random.default_rng(seed+777)
    E=int(round(N*kappa/2))
    a=rng.integers(0,N,size=int(E*1.3)); b=rng.integers(0,N,size=int(E*1.3))
    m=a!=b
    pairs=np.unique(np.sort(np.stack([a[m],b[m]],1),axis=1),axis=0)[:E]
    return build_nbr_arrays(pairs.astype(np.int32),N,CAP)

def s3_rgg(N,kappa,seed):
    """RGG sur la 3-sphere unite (temoin POSITIF : courbure +1 vraie)."""
    rng=np.random.default_rng(seed+31)
    x=rng.normal(size=(N,4)); x/= np.linalg.norm(x,axis=1)[:,None]
    # rayon angulaire pour degre moyen kappa : frac calotte = (th - sin th cos th)/pi
    lo,hi=1e-3,np.pi/2
    for _ in range(60):
        th=0.5*(lo+hi)
        frac=(th-np.sin(th)*np.cos(th))/np.pi
        if (N-1)*frac>kappa: hi=th
        else: lo=th
    th=0.5*(lo+hi); rch=2*np.sin(th/2)   # corde equivalente
    tree=cKDTree(x); pairs=np.array(list(tree.query_pairs(rch)),dtype=np.int32)
    return build_nbr_arrays(pairs,N,CAP)

# ----------------------------- MODULE A : mort de la queue --------------------
@njit(cache=True)
def triangles_per_vertex(nbr,deg,N):
    tpv=np.zeros(N,dtype=np.int64)
    for u in range(N):
        du=deg[u]; c=0
        for ki in range(du):
            a=nbr[u,ki]
            for kj in range(ki+1,du):
                b=nbr[u,kj]
                for m in range(deg[a]):
                    if nbr[a,m]==b:
                        c+=1; break
        tpv[u]=c
    return tpv

def tail_alpha(c,q):
    c=np.asarray(c,float); xmin=np.quantile(c,q)
    tail=c[c>=xmin]; n=len(tail)
    if n<30 or xmin<=0: return None
    apl=1+n/np.sum(np.log(tail/xmin))
    llpl=n*np.log(apl-1)-n*np.log(xmin)-apl*np.sum(np.log(tail/xmin))
    lam=1/(tail.mean()-xmin+1e-12)
    llex=n*np.log(lam)-lam*np.sum(tail-xmin)
    return apl,llpl-llex

def module_A():
    print("\n########## MODULE A : TEST DE MORT — queue de calcification ##########")
    NS=[2000,5000,20000,50000]; SEEDS=[0,1,2,3]; KAPPAS=[6.6,9.0]; QS=[0.70,0.75,0.80]
    res={}
    for kap in KAPPAS:
        for N in NS:
            key=f"k{kap}_N{N}"; res[key]={q:[] for q in QS}
            t0=time.time()
            for sd in SEEDS:
                nbr,deg=therm_blob(N,kap,sd)
                tpv=triangles_per_vertex(nbr,deg,N)
                for q in QS:
                    out=tail_alpha(tpv,q)
                    if out: res[key][q].append((out[0],out[1]))
                del nbr,deg; gc.collect()
            a75=[x[0] for x in res[key][0.75]]
            print(f"  kappa={kap} N={N:>6}: alpha(q75)={np.mean(a75):.3f}±{np.std(a75):.3f} "
                  f"Dll={np.mean([x[1] for x in res[key][0.75]]):+.0f}  ({time.time()-t0:.0f}s)",flush=True)
            json.dump({k:{str(q):v for q,v in d.items()} for k,d in res.items()},
                      open('queue_mort.json','w'),indent=1)
    # VERDICTS
    print("\n=== VERDICTS (seuils pre-declares : <2s compatible | >3s enterre) ===")
    for q in QS:
        a66=np.concatenate([[x[0] for x in res[f"k6.6_N{N}"][q]] for N in NS])
        a90=np.concatenate([[x[0] for x in res[f"k9.0_N{N}"][q]] for N in NS])
        d=np.mean(a90)-np.mean(a66)
        se=np.sqrt(np.var(a66,ddof=1)/len(a66)+np.var(a90,ddof=1)/len(a90))
        sig=abs(d)/se
        v="COMPATIBLE" if sig<2 else ("zone grise" if sig<3 else "ENTERRE (kappa-dependant)")
        print(f"  xmin=q{int(q*100)} : alpha(6,6)={np.mean(a66):.3f} vs alpha(9)={np.mean(a90):.3f} "
              f"-> Delta={d:+.3f} ({sig:.1f} sigma) => {v}")
    # stabilite N a kappa=6,6
    for q in [0.75]:
        means=[np.mean([x[0] for x in res[f"k6.6_N{N}"][q]]) for N in NS]
        drift=100*(means[-1]-means[0])/means[0]
        print(f"  Stabilite N (q75, kappa=6,6) : {means[0]:.3f} -> {means[-1]:.3f} ({drift:+.1f}%)")

# ----------------------------- MODULE B : rondeur v2 --------------------------
@njit(cache=True)
def sphere_at(nbr,deg,src,N,radius):
    dist=np.full(N,-1,np.int32); q=np.empty(N,np.int32)
    h=0;t=0;q[t]=src;t+=1;dist[src]=0
    out=np.empty(N,np.int32); no=0
    while h<t:
        x=q[h];h+=1
        if dist[x]==radius:
            out[no]=x;no+=1; continue
        if dist[x]>radius: break
        for k in range(deg[x]):
            y=nbr[x,k]
            if dist[y]==-1:
                dist[y]=dist[x]+1; q[t]=y;t+=1
    return out[:no],dist

def kq_profile(nbr,deg,N,seed,deltas=(1,2,3,4,5,6,7,8),npairs=240,nsamp=24):
    rng=np.random.default_rng(seed+5)
    prof={}
    for d0 in deltas:
        vals=[]; tries=0
        while len(vals)<npairs and tries<npairs*8:
            tries+=1
            p=int(rng.integers(0,N))
            Sp,_=sphere_at(nbr,deg,p,N,d0)
            if len(Sp)==0: continue
            pp=int(Sp[rng.integers(0,len(Sp))])
            Spp,_=sphere_at(nbr,deg,pp,N,d0)
            if len(Spp)==0: continue
            A=Sp[rng.integers(0,len(Sp),min(nsamp,len(Sp)))]
            Bs=Spp[rng.integers(0,len(Spp),min(nsamp,len(Spp)))]
            tot=0.0;cnt=0
            for a in A:
                _,dA=sphere_at(nbr,deg,int(a),N,4*d0)
                for b in Bs:
                    if dA[b]>=0: tot+=dA[b];cnt+=1
            if cnt>0: vals.append(tot/cnt/d0)
        prof[d0]=(float(np.mean(vals)),float(np.std(vals)),len(vals))
    return prof

def module_B():
    print("\n########## MODULE B : RONDEUR K-L v2 (temoin positif S3, multi-N, n x 4) ##########")
    out={}
    jobs=[("S3_sphere",s3_rgg,20000),("BLOB",therm_blob,20000),("BLOB",therm_blob,50000),
          ("RGG_plat",raw_rgg,20000),("ER",er_graph,20000)]
    for name,builder,N in jobs:
        t0=time.time()
        nbr,deg=builder(N,6.6,0)
        prof=kq_profile(nbr,deg,N,0)
        key=f"{name}_N{N}"
        out[key]={str(k):v for k,v in prof.items()}
        json.dump(out,open('rondeur_v2.json','w'),indent=1)
        # pente meso 3..8 ponderee
        ds=np.array([d for d in sorted(prof) if d>=3])
        if len(ds)<2: ds=np.array(sorted(prof))
        ms=np.array([prof[d][0] for d in ds])
        sems=np.array([prof[d][1]/np.sqrt(max(prof[d][2],1)) for d in ds])
        w=1/np.maximum(sems,1e-9)**2
        W=np.sum(w);X=np.sum(w*ds);Y=np.sum(w*ms);XX=np.sum(w*ds*ds);XY=np.sum(w*ds*ms)
        slope=(W*XY-X*Y)/(W*XX-X*X); err=np.sqrt(W/(W*XX-X*X))
        print(f"  [{key}] pente(3..8) = {slope:+.4f} ± {err:.4f}  ({time.time()-t0:.0f}s)",flush=True)
        del nbr,deg; gc.collect()
    print("\nLECTURE : ordre attendu si rondeur reelle : pente(S3) < pente(BLOB) < pente(RGG)~0,")
    print("ER hors classe. La pente S3 calibre la FORME d'une courbure positive vraie a ce N/kappa.")

if __name__=='__main__':
    module_A()
    module_B()
    print("\nTermine. JSON : queue_mort.json, rondeur_v2.json — a renvoyer pour verdicts.")
