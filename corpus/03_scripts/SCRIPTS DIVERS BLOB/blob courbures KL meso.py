"""
================================================================================
 BLOB — COURBURES : rondeur de Klitgaard-Loll (P2) + Ollivier MESOSCOPIQUE (P4)
================================================================================
 P2 — LE DISCRIMINANT DE SITTER QUI MANQUAIT. Klitgaard-Loll (PRD 97:046008 &
 106017, 2018 ; EPJ C 80:990, 2020 "How round is the quantum de Sitter
 universe?") definissent la courbure de Ricci QUANTIQUE :
     K_q(delta) = d_bar(S_p, S_p') / delta,
 ou d_bar est la distance moyenne entre les spheres de rayon delta centrees en
 deux points p,p' eux-memes a distance delta. Le PROFIL K_q(delta), compare a
 celui d'une sphere/de Sitter vs espace plat vs graphe generique, est un test
 de "rondeur" SANS calibration. Notre verrou C (de Sitter via cloche cos2)
 etait mort faute de discriminant : ce test EST le discriminant.

 P4 — OLLIVIER MESOSCOPIQUE -> ACTION D'EINSTEIN-HILBERT MESUREE.
 van der Hoorn-Cunningham-Lippner-Trugenberger-Krioukov (PRR 3:013211, 2021) :
 la courbure d'Ollivier sur RGG converge vers la Ricci de la variete SEULEMENT
 en regime mesoscopique (boules de rayon delta, distances re-echelonnees).
 On mesure kappa_meso(x,y) = 1 - W1(mu_x, mu_y)/d(x,y) avec mu = uniforme sur
 la boule B(., delta), W1 approche par appariement glouton d'echantillons.
 Sortie : champ de Ricci rigoureux (coeur matiere vs fluide) + Sigma kappa
 (premier morceau MESURE de l'action effective — la clef des [O], gel V178).

 Temoins systematiques : RGG brut (zero viabilite) et graphe d'Erdos-Renyi de
 meme densite. AUCUNE calibration sur valeur cible.

 USAGE COLAB :  !pip -q install numba   puis   %run blob_courbures_KL_meso.py
 Duree : ~30-60 min. JSON : courbures_KL.json, courbures_meso.json.
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

CAP=64; POOL_FAC=1.6; THERM_FAC=120; N_CHUNKS=10; KAPPA=6.6

def therm_blob(N,seed):
    edges,pool,r=build_geometric(N,KAPPA,POOL_FAC,seed)
    nbr,deg=build_nbr_arrays(edges,N,CAP)
    eu=edges[:,0].copy();ev=edges[:,1].copy()
    pa=np.ascontiguousarray(pool[:,0]);pb=np.ascontiguousarray(pool[:,1])
    del pool,edges; gc.collect()
    mean=2.0*eu.shape[0]/N; nt=n_triangles(nbr,deg,N)
    total=THERM_FAC*N; chunk=max(1,total//N_CHUNKS)
    for c in range(N_CHUNKS):
        nt=mcmc_chunk(nbr,deg,eu,ev,pa,pb,0.30,0.5/N,mean,nt,chunk,CAP,seed*100+1+c)
    return nbr,deg

def raw_rgg(N,seed):
    edges,pool,r=build_geometric(N,KAPPA,POOL_FAC,seed)
    nbr,deg=build_nbr_arrays(edges,N,CAP)
    return nbr,deg

def er_graph(N,seed):
    rng=np.random.default_rng(seed+777)
    E=int(round(N*KAPPA/2))
    a=rng.integers(0,N,size=int(E*1.3)); b=rng.integers(0,N,size=int(E*1.3))
    m=a!=b; pairs=np.unique(np.sort(np.stack([a[m],b[m]],1),axis=1),axis=0)[:E]
    nbr,deg=build_nbr_arrays(pairs.astype(np.int32),N,CAP)
    return nbr,deg

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

# -------------------- P2 : rondeur de Klitgaard-Loll --------------------
def kq_profile(nbr,deg,N,seed,deltas=(1,2,3,4,5,6),npairs=60,nsamp=24):
    rng=np.random.default_rng(seed+5)
    prof={}
    for d0 in deltas:
        vals=[]
        tries=0
        while len(vals)<npairs and tries<npairs*8:
            tries+=1
            p=int(rng.integers(0,N))
            Sp,distp=sphere_at(nbr,deg,p,N,d0)
            if len(Sp)==0: continue
            pp=int(Sp[rng.integers(0,len(Sp))])  # p' a distance exactement delta
            Spp,distpp=sphere_at(nbr,deg,pp,N,d0)
            if len(Spp)==0: continue
            # distance moyenne entre les deux spheres (echantillonnee)
            A=Sp[rng.integers(0,len(Sp),min(nsamp,len(Sp)))]
            Bs=Spp[rng.integers(0,len(Spp),min(nsamp,len(Spp)))]
            tot=0.0;cnt=0
            for a in A:
                _,dA=sphere_at(nbr,deg,int(a),N,4*d0)  # BFS limite
                for b in Bs:
                    if dA[b]>=0: tot+=dA[b];cnt+=1
            if cnt>0: vals.append(tot/cnt/d0)
        prof[d0]=(float(np.mean(vals)),float(np.std(vals)),len(vals))
    return prof

# -------------------- P4 : Ollivier mesoscopique --------------------
def ollivier_meso(nbr,deg,N,seed,delta=3,npairs=150,nsamp=20):
    """kappa(x,y)=1 - W1(mu_x,mu_y)/d(x,y), mu=uniforme sur B(.,delta), x,y a distance delta.
       W1 approche par appariement glouton (borne sup serree a ces tailles)."""
    rng=np.random.default_rng(seed+9)
    # richesse K4 locale (proxy coeur/fluide) : triangles incidents
    tri_v=np.zeros(N,np.int64)
    for u in range(N):
        s=set(nbr[u,:deg[u]].tolist())
        c=0
        for i in range(deg[u]):
            a=nbr[u,i]
            for j in range(deg[a]):
                if nbr[a,j] in s and nbr[a,j]>a: c+=1
        tri_v[u]=c
    thr=np.quantile(tri_v,0.8)
    res={'core':[],'fluid':[]}
    tries=0
    while (len(res['core'])<npairs//2 or len(res['fluid'])<npairs//2) and tries<npairs*10:
        tries+=1
        x=int(rng.integers(0,N))
        Sx,distx=sphere_at(nbr,deg,x,N,delta)
        if len(Sx)==0: continue
        y=int(Sx[rng.integers(0,len(Sx))])
        # boules
        Bx=np.where((distx>=0)&(distx<=delta))[0]
        Sy,disty=sphere_at(nbr,deg,y,N,delta)
        By=np.where((disty>=0)&(disty<=delta))[0]
        if len(Bx)<4 or len(By)<4: continue
        A=Bx[rng.integers(0,len(Bx),nsamp)]; Bs=By[rng.integers(0,len(By),nsamp)]
        # matrice de distances depuis chaque a (BFS limite a 4*delta)
        D=np.full((nsamp,nsamp),1e9)
        for i,a in enumerate(A):
            _,dA=sphere_at(nbr,deg,int(a),N,4*delta)
            for j,b in enumerate(Bs):
                if dA[b]>=0: D[i,j]=dA[b]
        # appariement glouton
        used=np.zeros(nsamp,bool); tot=0.0
        order=np.argsort(D.min(axis=1))
        for i in order:
            j=int(np.argmin(np.where(used,1e18,D[i])))
            used[j]=True; tot+=D[i,j]
        W1=tot/nsamp
        kap=1.0 - W1/delta
        key='core' if tri_v[x]>=thr else 'fluid'
        res[key].append(kap)
    return {k:(float(np.mean(v)),float(np.std(v)),len(v)) for k,v in res.items() if v}

def main():
    out_kl={}; out_ms={}
    for name,builder in [('BLOB',therm_blob),('RGG_brut',raw_rgg),('ER',er_graph)]:
        N=20000 if name=='BLOB' else 20000
        t0=time.time()
        nbr,deg=builder(N,0)
        prof=kq_profile(nbr,deg,N,0)
        out_kl[name]={str(k):v for k,v in prof.items()}
        ms=ollivier_meso(nbr,deg,N,0)
        out_ms[name]=ms
        print(f"[{name}] ({time.time()-t0:.0f}s)")
        print("  K_q(delta) [rondeur K-L] :", {k:f"{v[0]:.3f}" for k,v in prof.items()})
        print("  kappa_meso  [Ollivier]   :", {k:f"{v[0]:+.3f}±{v[1]:.3f}(n={v[2]})" for k,v in ms.items()})
        json.dump(out_kl,open('courbures_KL.json','w'),indent=2)
        json.dump(out_ms,open('courbures_meso.json','w'),indent=2)
        del nbr,deg; gc.collect()
    print("\nLECTURE : (P2) comparer le PROFIL K_q(delta) du Blob a ceux des temoins —")
    print("une signature de Sitter = profil de spherecite distinct des temoins plats/aleatoires.")
    print("(P4) kappa_meso(core) > kappa_meso(fluid) > 0 ~ Ricci>0 sur la matiere, ~0 fluide ;")
    print("Sigma kappa = premier morceau mesure de l'action d'Einstein-Hilbert discrete.")

if __name__=='__main__':
    main()
