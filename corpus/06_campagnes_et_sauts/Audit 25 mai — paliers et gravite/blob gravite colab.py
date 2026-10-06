# ==============================================================================
# BLOB PRINCIPLE — GRAVITÉ : SCALING COMPLET (Colab, autonome)
# Rassemble tous les tests de gravité de la session du 24 mai 2026, à grand N.
# Tranche : (A) force tétra-tétra attraction/répulsion, (B) ponts matière-matière
# (4e dim), (C) propagation/onde de viabilité, le tout vs 3 nuls et en scaling N.
#
# UN JSON PAR PALIER (sauvegarde immédiate). Paliers : 1000, 2500, 5000, 10000,
# puis tous les 5000 jusqu'à 100000 tant que la machine suit.
# numpy/scipy/networkx uniquement. Lancer dans Colab.
# ==============================================================================
import numpy as np, json, math, time, gc
from scipy.spatial import cKDTree
from collections import deque

KAPPA=6.6; BETA=0.30; TAU=0.50
PALIERS=[1000,2500,5000,10000]+list(range(15000,100001,5000))
SEEDS_BY_N=lambda N: 6 if N<=2500 else (4 if N<=10000 else (3 if N<=30000 else 2))
BUDGET_HEURES=11.5   # arrêt propre avant cette limite

# ---------- construction ----------
def rgg_radius(N,kappa): return (kappa/((N-1)*4.0/3.0*math.pi))**(1.0/3.0)

def build_initial(N, seed, kappa=KAPPA):
    rng=np.random.default_rng(seed); pts=rng.uniform(0,1,(N,3))
    r=rgg_radius(N,kappa); tree=cKDTree(pts)
    pairs=tree.query_pairs(r,output_type='ndarray')
    adj=[set() for _ in range(N)]
    for i,j in pairs: adj[i].add(int(j)); adj[j].add(int(i))
    return pts, adj, r

def lcc_frac(adj,N):
    seen=np.zeros(N,bool); best=0
    for s in range(N):
        if seen[s]: continue
        cnt=0; dq=deque([s]); seen[s]=True
        while dq:
            u=dq.popleft(); cnt+=1
            for w in adj[u]:
                if not seen[w]: seen[w]=True; dq.append(w)
        best=max(best,cnt)
    return best/N

# ---------- viabilité ----------
def local_S(adj,v,beta=BETA):
    ni=list(adj[v])
    if len(ni)<2: return 0.0
    tri=0
    for a in range(len(ni)):
        na=adj[ni[a]]
        for c in range(a+1,len(ni)):
            if ni[c] in na: tri+=1
    degs=np.fromiter((len(adj[u]) for u in ni),float)
    return math.log(1+tri)-beta*(degs.std()/degs.mean() if degs.mean()>0 else 0)

# ---------- dynamique edge-swap canonique (topologie) ----------
def mcmc_topo(pts,adj,N,r,seed,viab=True,sweeps=3,beta=BETA,tau=TAU):
    rng=np.random.default_rng(seed); tree=cKDTree(pts)
    pool=tree.query_pairs(r*1.3,output_type='ndarray')  # candidats d'arêtes
    npool=len(pool); tau_eff=tau/N
    nsteps=sweeps*N
    for _ in range(nsteps):
        a,c=pool[rng.integers(npool)]
        if c in adj[a]: continue
        u=rng.integers(N)
        if not adj[u]: continue
        w=list(adj[u])[rng.integers(len(adj[u]))]
        if viab: Sb=local_S(adj,a)+local_S(adj,c)+local_S(adj,u)+local_S(adj,w)
        adj[u].discard(w);adj[w].discard(u);adj[a].add(int(c));adj[c].add(int(a))
        if viab:
            dS=local_S(adj,a)+local_S(adj,c)+local_S(adj,u)+local_S(adj,w)-Sb
            if not(dS>=0 or rng.random()<math.exp(dS/tau_eff)):
                adj[a].discard(c);adj[c].discard(a);adj[u].add(w);adj[w].add(u)
    return adj

# ---------- détection des tétraèdres (K4) — version efficace ----------
def find_tets(adj,N,cap=200000):
    tets=[]
    for i in range(N):
        ni=[x for x in adj[i] if x>i]
        for a in range(len(ni)):
            j=ni[a]; nij=adj[i]&adj[j]
            for k in nij:
                if k>j:
                    common=nij&adj[k]
                    for l in common:
                        if l>k: tets.append((i,j,k,l))
                        if len(tets)>=cap: return tets
    return tets

def matter_set(adj,N,tets=None):
    if tets is None: tets=find_tets(adj,N)
    s=set()
    for t in tets:
        for x in t: s.add(x)
    return s, tets

# ---------- mobilité des positions (pour la force tétra-tétra) ----------
def relax_positions(pts,adj,N,r,seed,viab=True,sweeps=5,beta=BETA,tau=TAU):
    rng=np.random.default_rng(seed+777); sigma=0.3*r
    def rebuild(v):
        for u in list(adj[v]): adj[u].discard(v)
        adj[v]=set(); d=np.linalg.norm(pts-pts[v],axis=1)
        for u in np.where((d<r)&(d>0))[0]: adj[v].add(int(u)); adj[int(u)].add(v)
    for _ in range(sweeps):
        for _ in range(N//4):
            v=rng.integers(N)
            if not adj[v]: continue
            So=local_S(adj,v); op=pts[v].copy(); oav=set(adj[v]); onb={u:set(adj[u]) for u in adj[v]}
            pts[v]=np.clip(pts[v]+rng.normal(0,sigma,3),0,1); rebuild(v)
            if viab:
                dS=local_S(adj,v)-So; acc=(dS>=0) or (rng.random()<math.exp(dS/tau))
            else: acc=rng.random()<0.5
            if not acc:
                pts[v]=op
                for u in list(adj[v]): adj[u].discard(v)
                adj[v]=oav
                for u,s in onb.items(): adj[u]=s
    return pts,adj

# ================== TESTS ==================
def test_force_tetra(pts0,pts1,adj0,N,tets):
    """(A) Profil attraction/répulsion tétra-tétra vs distance. Renvoie variation moyenne par bin."""
    mat,_=matter_set(adj0,N,tets)
    is_m=np.zeros(N,bool)
    for v in mat: is_m[v]=True
    rng=np.random.default_rng(0); npairs=min(20000,N*8)
    I=rng.integers(0,N,npairs); J=rng.integers(0,N,npairs)
    m=I!=J; I,J=I[m],J[m]
    d0=np.linalg.norm(pts0[I]-pts0[J],axis=1); d1=np.linalg.norm(pts1[I]-pts1[J],axis=1)
    dd=d1-d0; tt=is_m[I]&is_m[J]
    bins=np.array([0,0.04,0.08,0.12,0.20,0.35]); prof=[]
    idx=np.digitize(d0,bins)-1
    for k in range(len(bins)-1):
        mk=(idx==k)&tt
        prof.append(float(dd[mk].mean()) if mk.sum()>5 else None)
    return prof

def test_ponts(adj,N,tets):
    """(B) Ponts matière-matière : tétra lointains en 3D partageant des voisins (proximité 4D cachée)."""
    mat,_=matter_set(adj,N,tets)
    mat=np.array(sorted(mat))
    if len(mat)<20: return None
    return None  # calculé dans le pipeline avec positions

def test_ponts_pos(adj,N,pts,tets):
    mat,_=matter_set(adj,N,tets)
    mat=np.array(sorted(mat)); non=np.array([v for v in range(N) if v not in set(mat.tolist())])
    if len(mat)<20 or len(non)<20: return None
    rng=np.random.default_rng(1)
    def shared_far(group):
        vals=[]
        for _ in range(3000):
            i,j=int(group[rng.integers(len(group))]),int(group[rng.integers(len(group))])
            if i==j: continue
            if np.linalg.norm(pts[i]-pts[j])<0.3: continue
            vals.append(len(adj[i]&adj[j]))
        return float(np.mean(vals)) if vals else 0.0
    return shared_far(mat), shared_far(non)

def test_propagation(pts,adj,N,r,seed,viab,tets):
    """(C) Propagation d'une perturbation de viabilité en distance géodésique. Exposant."""
    if len(tets)<5: return None
    rng=np.random.default_rng(seed+50); src=list(tets[rng.integers(len(tets))])
    S0=np.array([local_S(adj,v) for v in range(N)])
    # géodésique depuis src
    dist=np.full(N,-1,int); dq=deque(src)
    for s in src: dist[s]=0
    while dq:
        u=dq.popleft()
        if dist[u]>=10: continue
        for w in adj[u]:
            if dist[w]<0: dist[w]=dist[u]+1; dq.append(w)
    adj_w=[set(a) for a in adj]
    for a in range(4):
        for c in range(a+1,4):
            if src[c] in adj_w[src[a]]: adj_w[src[a]].discard(src[c]); adj_w[src[c]].discard(src[a])
    fronts=[]
    for step in range(6):
        adj_w=mcmc_topo(pts,adj_w,N,r,seed+100+step,viab=viab,sweeps=1)
        St=np.array([local_S(adj_w,v) for v in range(N)])
        dS=np.abs(St-S0); mask=(dist>0)&(dist<9)
        thr=dS[mask].mean()*0.5 if mask.sum()>0 else 0
        sel=mask&(dS>thr)
        fronts.append(float(np.average(dist[sel],weights=dS[sel])) if sel.sum()>3 else None)
    f=[x for x in fronts if x]
    if len(f)<3: return None
    t=np.arange(1,len(f)+1)
    expo=float(np.polyfit(np.log(t),np.log(f),1)[0])
    return expo

# ================== PIPELINE PAR PALIER ==================
def run_palier(N, t0, budget):
    res={'N':N,'seeds':{}}
    nseed=SEEDS_BY_N(N)
    for seed in range(nseed):
        if time.time()-t0>budget: break
        entry={}
        try:
            # BLOB
            pts,adj,r=build_initial(N,seed)
            if lcc_frac(adj,N)<0.7:
                entry['skip']='lcc faible'; res['seeds'][seed]=entry; continue
            adj=mcmc_topo(pts,adj,N,r,seed,viab=True,sweeps=3)
            tets=find_tets(adj,N)
            entry['n_tets']=len(tets)
            # (B) ponts
            pp=test_ponts_pos(adj,N,pts,tets)
            if pp: entry['ponts_mat']=pp[0]; entry['ponts_sub']=pp[1]
            # (C) propagation
            entry['expo_prop']=test_propagation(pts,adj,N,r,seed,True,tets)
            # (A) force : relaxer positions et comparer
            pts0=pts.copy()
            pts2,adj2=relax_positions(pts.copy(),[set(a) for a in adj],N,r,seed,viab=True,sweeps=4)
            entry['force_profile']=test_force_tetra(pts0,pts2,adj,N,tets)
            # NUL (swaps aléatoires) pour propagation + ponts
            ptsn,adjn,rn=build_initial(N,seed)
            adjn=mcmc_topo(ptsn,adjn,N,rn,seed,viab=False,sweeps=3)
            tetsn=find_tets(adjn,N)
            entry['n_tets_nul']=len(tetsn)
            entry['expo_prop_nul']=test_propagation(ptsn,adjn,N,rn,seed,False,tetsn)
            ppn=test_ponts_pos(adjn,N,ptsn,tetsn)
            if ppn: entry['ponts_mat_nul']=ppn[0]; entry['ponts_sub_nul']=ppn[1]
        except Exception as e:
            entry['error']=str(e)
        res['seeds'][seed]=entry
        gc.collect()
    return res

def main():
    t0=time.time(); budget=BUDGET_HEURES*3600
    print(f"GRAVITÉ SCALING — paliers {PALIERS[0]}..{PALIERS[-1]}, budget {BUDGET_HEURES}h")
    for N in PALIERS:
        if time.time()-t0>budget:
            print(f"[STOP budget] arrêt avant N={N}"); break
        tN=time.time()
        print(f"\n=== N={N} ({SEEDS_BY_N(N)} seeds) ===")
        res=run_palier(N,t0,budget)
        fname=f"blob_gravite_N{N}.json"
        json.dump(res, open(fname,'w'))
        # résumé court
        seeds=res['seeds']
        nt=[seeds[s].get('n_tets') for s in seeds if 'n_tets' in seeds[s]]
        ep=[seeds[s].get('expo_prop') for s in seeds if seeds[s].get('expo_prop') is not None]
        epn=[seeds[s].get('expo_prop_nul') for s in seeds if seeds[s].get('expo_prop_nul') is not None]
        pm=[seeds[s].get('ponts_mat') for s in seeds if seeds[s].get('ponts_mat') is not None]
        pmn=[seeds[s].get('ponts_mat_nul') for s in seeds if seeds[s].get('ponts_mat_nul') is not None]
        print(f"  -> {fname} [{time.time()-tN:.0f}s ce palier, {(time.time()-t0)/60:.0f}min total]")
        if nt: print(f"     tétraèdres: {np.mean(nt):.0f}")
        if ep and epn: print(f"     exposant propagation: Blob={np.mean(ep):.3f} vs Nul={np.mean(epn):.3f}")
        if pm and pmn: print(f"     ponts matière: Blob={np.mean(pm):.4f} vs Nul={np.mean(pmn):.4f}")
    print(f"\nTERMINÉ. {(time.time()-t0)/60:.0f} min. Fichiers: blob_gravite_N*.json")

if __name__=="__main__":
    main()
