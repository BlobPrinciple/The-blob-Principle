"""
================================================================================
BLOB — SCALING DU GAP CURL DE MAXWELL (photon transverse), MULTI-SEEDS, vs kappa
================================================================================
Objet : trancher si le gap du Laplacien de Hodge L1 = d1^T d1 (secteur curl-curl,
        transverse = le photon) sur le sous-complexe FIDELE∩VIABLE du Blob converge
        en N^(-2/3) (loi de Weyl 3D, gap·N^(2/3) CONSTANT) — et si la PHASE COMPACTE
        (kappa grand) le redresse vers ce comportement.

Rappels consignes (corpus, 29 mai) :
  - Rips brut          : gap_curl ~ N^(-0,28)  (erratique, NE converge pas)
  - Etalon cubique 3D  : gap_curl ~ N^(-2/3)   (gap·N^(2/3) ~ 19,3 CONSTANT)
Verdict precedent (mon conteneur, 1 seul seed) : BRUITE, non concluant. D'ou ce
script MULTI-SEEDS a grand N, a executer sur Colab (CPU suffit ; aucune dependance
hors numpy/scipy/matplotlib, tous presents sur Colab).

AUTONOME : le moteur du Blob (RGG 3D + viabilite canonique O(N), VALIDE identique au
moteur de reference) est integre ci-dessous. Aucun fichier externe requis.

Methode du gap_curl : STRICTEMENT identique a test_maxwell_souscomplexe.py du corpus
(Delaunay∩Blob -> d1 bord oriente arete->triangle -> L1t=d1^T d1 -> plus petite vp non nulle).

USAGE COLAB : coller ce fichier dans une cellule et executer. Ajuster le bloc CONFIG.
Sauvegarde progressive en JSON (gap_curl_results.json) pour ne rien perdre si timeout.
================================================================================
"""
import numpy as np, math, time, json
from collections import deque
from scipy.spatial import KDTree, Delaunay
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

# ============================== CONFIG (a ajuster) ==============================
# NB : moteur de REFERENCE exact (run_mcmc_canonical) = O(N^2) par run -> N modere.
#      gap_curl a TRES grande variance (std/mean ~0,2-0,3) -> beaucoup de seeds requis.
KAPPAS  = [6.6, 12.0, 18.0]          # 6.6 = phase nominale ; 12,18 = phase compacte (test du redressement)
N_LIST  = [400, 600, 800, 1000, 1200]   # rester modere : canonical est O(N^2)
SEEDS   = list(range(16))            # >=12-20 indispensable vu la variance du gap_curl
BURN_F, PROD_F = 50, 80              # defauts du moteur de reference (NE PAS changer)
RUN_ETALON = True                    # controle de methode : gap·N^(2/3) doit etre ~constant (exposant -2/3)
ETALON_M   = [6, 8, 10, 12]          # cotes du cube (N = m^3)
TIME_BUDGET = 1e9                    # secondes (ex 18000 = 5h pour une session Colab)
OUTFILE = "gap_curl_results.json"
# ===============================================================================

BETA, TAU = 0.30, 0.50

# ----------------------------- MOTEUR BLOB (integre) ---------------------------
def rips_radius(N, kappa): return (kappa / ((N - 1) * (4/3) * math.pi)) ** (1/3)
def E0_target(N, kappa):   return max(N - 1, int(N * kappa / 2))

def lcc_size(adj, N):
    seen=[False]*N; best=0
    for s in range(N):
        if not seen[s]:
            sz=0; q=deque([s]); seen[s]=True
            while q:
                v=q.popleft(); sz+=1
                for w in adj[v]:
                    if not seen[w]: seen[w]=True; q.append(w)
            best=max(best,sz)
    return best

def build_initial(N, seed, kappa, pool_mult=1.6):
    r=rips_radius(N,kappa); r_p=pool_mult*r; E0=E0_target(N,kappa)
    rng=np.random.default_rng(seed); pts=rng.uniform(0.0,1.0,(N,3))
    tree=KDTree(pts); adj=[set() for _ in range(N)]
    for i,j in tree.query_pairs(r): adj[i].add(j); adj[j].add(i)
    pool=list(tree.query_pairs(r_p)); rng2=np.random.default_rng(seed+50_000)
    K=sum(len(adj[i]) for i in range(N))//2; att=0; max_att=10*abs(E0-K)+5000
    while K!=E0 and att<max_att:
        att+=1
        if K<E0:
            if not pool: break
            u,v=pool[rng2.integers(len(pool))]
            if v not in adj[u]: adj[u].add(v); adj[v].add(u); K+=1
        else:
            edges=[(i,j) for i in range(N) for j in adj[i] if j>i]
            if not edges: break
            u,v=edges[rng2.integers(len(edges))]
            adj[u].discard(v); adj[v].discard(u)
            if lcc_size(adj,N)==N: K-=1
            else: adj[u].add(v); adj[v].add(u)
    return pts, adj, pool, E0

def count_triangles(adj, N):
    n=0
    for i in range(N):
        for j in adj[i]:
            if j>i:
                n+=len(adj[i] & adj[j] & set(k for k in adj[j] if k>j))
    return n

def still_connected(adj, u, v, N):
    seen={u}; q=deque([u])
    while q:
        node=q.popleft()
        for w in adj[node]:
            if w in seen: continue
            if (node==u and w==v) or (node==v and w==u): continue
            seen.add(w); q.append(w)
            if w==v: return True
    return False

def compute_S(adj, n_tri, N):
    degs=np.array([len(adj[i]) for i in range(N)],float)
    D=degs.std()/(degs.mean()+1e-8)
    return math.log(1+n_tri)-BETA*D

def run_mcmc_canonical(pts, adj_init, pool, N, E0, seed, burn_f=BURN_F, prod_f=PROD_F):
    """MOTEUR DE REFERENCE EXACT (viabilite canonique, E fixe). Identique au corpus.
       compute_S recalcule D a chaque pas -> O(N) par pas (lent a grand N, mais EXACT/sans biais)."""
    tau_eff=TAU/N; rng=np.random.default_rng(seed+200_000)
    adj=[set(a) for a in adj_init]
    edge_list=[(i,j) for i in range(N) for j in adj[i] if j>i]
    if not edge_list or not pool: return adj
    n_tri=count_triangles(adj,N); S_curr=compute_S(adj,n_tri,N)
    pool_arr=np.array(pool,dtype=np.int32); n_pool=len(pool_arr)
    for step in range((burn_f+prod_f)*N):
        if not edge_list: break
        io=int(rng.integers(len(edge_list))); u,v=edge_list[io]
        e_in=None
        for _ in range(30):
            ii=int(rng.integers(n_pool)); a,bb=int(pool_arr[ii,0]),int(pool_arr[ii,1])
            if bb not in adj[a]: e_in=(a,bb); break
        if e_in is None: continue
        a,bb=e_in
        if len(adj[u])<=2 or len(adj[v])<=2:
            if not still_connected(adj,u,v,N): continue
        tl=len(adj[u]&adj[v])
        adj[u].discard(v); adj[v].discard(u); adj[a].add(bb); adj[bb].add(a)
        tg=len(adj[a]&adj[bb]); nt=n_tri-tl+tg
        S_new=compute_S(adj,nt,N)
        if S_new-S_curr>=0 or rng.random()<math.exp((S_new-S_curr)/tau_eff):
            n_tri=nt; S_curr=S_new; edge_list[io]=(a,bb)
        else:
            adj[u].add(v); adj[v].add(u); adj[a].discard(bb); adj[bb].discard(a)
    return adj

# --------------------- GAP CURL DE HODGE (identique au corpus) -----------------
def extract_faithful(adjB, P):
    """Tetraedres de Delaunay dont les 6 aretes existent dans le Blob."""
    dela=Delaunay(P); tets=[]
    for t in dela.simplices:
        t=sorted(int(x) for x in t)
        if all((t[j] in adjB[t[i]]) for i in range(4) for j in range(i+1,4)):
            tets.append(tuple(t))
    return tets

def smallest_nonzero_eig(L1t, tol=1e-7):
    """Plus petite valeur propre NON nulle de L1t (gere le noyau H1).
       1) shift-invert sigma~0 (rapide/robuste, OK grand N) ; 2) repli SM (comme le corpus)."""
    n=L1t.shape[0]
    if n<12: return None
    kk=min(120,n-2)
    # 1) shift-invert : trouve les vp les plus proches de 0 (noyau + 1eres non nulles)
    try:
        ev=eigsh(L1t,k=kk,sigma=1e-6,which='LM',return_eigenvectors=False,maxiter=20000)
        ev=np.sort(ev[ev>tol])
        if len(ev): return float(ev[0])
    except Exception:
        pass
    # 2) repli : SM direct (methode du corpus, k=60)
    try:
        ev=eigsh(L1t,k=min(60,n-2),which='SM',return_eigenvectors=False,maxiter=20000)
        ev=np.sort(ev[ev>tol])
        return float(ev[0]) if len(ev) else None
    except Exception:
        return None

def curl_gap(tets):
    """L1t = d1^T d1 (curl-curl, secteur transverse de Maxwell). Plus petite vp non nulle."""
    Eset=set(); Fset=set()
    for t in tets:
        for i in range(4):
            for j in range(i+1,4): Eset.add((t[i],t[j]))
        for i in range(4):
            for j in range(i+1,4):
                for k in range(j+1,4): Fset.add((t[i],t[j],t[k]))
    E=sorted(Eset); F=sorted(Fset)
    if len(E)<10 or len(F)<5: return None
    eidx={e:i for i,e in enumerate(E)}
    rows=[]; cols=[]; vals=[]
    for fi,(a,c,d) in enumerate(F):
        for (x,y),s in [((a,c),1),((a,d),-1),((c,d),1)]:
            rows.append(fi); cols.append(eidx[(x,y)]); vals.append(s)
    d1=coo_matrix((vals,(rows,cols)),shape=(len(F),len(E))).tocsr()
    L1t=(d1.T@d1)
    return smallest_nonzero_eig(L1t)

# ------------------------------- ETALON CUBIQUE --------------------------------
def etalon_gap(m, seed=0):
    """Reseau cubique m^3 (leger jitter pour eviter la degenerescence de Delaunay)."""
    rng=np.random.default_rng(seed)
    g=np.linspace(0.05,0.95,m)
    P=np.array([(x,y,z) for x in g for y in g for z in g],float)
    P=P+rng.uniform(-0.012,0.012,P.shape)
    tets=[sorted(int(x) for x in t) for t in Delaunay(P).simplices]
    return curl_gap([tuple(t) for t in tets]), len(P)

# ----------------------------------- RUN ---------------------------------------
def fit_exponent(Ns, gaps):
    Ns=np.array(Ns,float); gaps=np.array(gaps,float)
    slope=np.polyfit(np.log(Ns),np.log(gaps),1)[0]
    cst=gaps*Ns**(2/3)
    return slope, cst.mean(), cst.std()

def main():
    t0=time.time(); results={"config":{"KAPPAS":KAPPAS,"N_LIST":N_LIST,"SEEDS":SEEDS,
                   "BURN_F":BURN_F,"PROD_F":PROD_F}, "blob":{}, "etalon":{}}
    print("="*78)
    print("GAP CURL DE MAXWELL — multi-seeds — cible Weyl 3D : gap·N^(2/3) CONSTANT, exposant -0,667")
    print("="*78)

    if RUN_ETALON:
        print("\n[ETALON CUBIQUE 3D — controle de methode : doit donner gap·N^(2/3) ~ constant]")
        print(f"  {'N':>6} {'gap_curl':>11} {'gap·N^(2/3)':>12}")
        Es=[]; Eg=[]
        for m in ETALON_M:
            g,Nc=etalon_gap(m)
            if g:
                Es.append(Nc); Eg.append(g)
                results["etalon"][str(Nc)]=g
                print(f"  {Nc:>6} {g:>11.5f} {g*Nc**(2/3):>12.3f}   [{time.time()-t0:.0f}s]")
        if len(Es)>=2:
            sl,cm,cs=fit_exponent(Es,Eg)
            print(f"  -> exposant N^({sl:.3f}) | gap·N^(2/3) = {cm:.2f} ± {cs:.2f}  (constant attendu)")
        json.dump(results,open(OUTFILE,"w"),indent=2)

    for kappa in KAPPAS:
        tag=" (CONTROLE reprod. Rips brut)" if abs(kappa-6.6)<1e-9 else ""
        print(f"\n[BLOB kappa={kappa}{tag}]")
        print(f"  {'N':>6} {'<gap_curl>':>11} {'± std':>9} {'<gap>·N^(2/3)':>14} {'n_seeds':>8}")
        kres={}; Ns_ok=[]; G_mean=[]
        for N in N_LIST:
            if time.time()-t0>TIME_BUDGET: print("  [budget atteint]"); break
            gaps=[]
            for s in SEEDS:
                pts,a0,pool,E0=build_initial(N,s,kappa)
                if lcc_size(a0,N)/N<0.85: continue
                adjB=run_mcmc_canonical(pts,a0,pool,N,E0,s)
                g=curl_gap(extract_faithful(adjB,np.array(pts)))
                if g is not None: gaps.append(g)
            if len(gaps)>=2:
                gm=float(np.mean(gaps)); gs=float(np.std(gaps))
                kres[str(N)]={"mean":gm,"std":gs,"n":len(gaps),"gaps":gaps}
                Ns_ok.append(N); G_mean.append(gm)
                print(f"  {N:>6} {gm:>11.5f} {gs:>9.5f} {gm*N**(2/3):>14.3f} {len(gaps):>8}   [{time.time()-t0:.0f}s]")
                results["blob"][str(kappa)]=kres; json.dump(results,open(OUTFILE,"w"),indent=2)
        if len(Ns_ok)>=2:
            sl,cm,cs=fit_exponent(Ns_ok,G_mean)
            verdict="CONVERGE vers Weyl 3D" if cs/cm<0.18 else "NE converge pas (encore)"
            print(f"  -> exposant N^({sl:.3f}) [cible -0,667] | gap·N^(2/3)={cm:.2f}±{cs:.2f} -> {verdict}")

    json.dump(results,open(OUTFILE,"w"),indent=2)
    print(f"\nResultats sauvegardes dans {OUTFILE}. [total {time.time()-t0:.0f}s]")

    # plot optionnel
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(7,5))
        for kappa in KAPPAS:
            kd=results["blob"].get(str(kappa),{})
            Ns=sorted(int(n) for n in kd); 
            if not Ns: continue
            y=[kd[str(n)]["mean"]*n**(2/3) for n in Ns]
            e=[kd[str(n)]["std"]*n**(2/3) for n in Ns]
            plt.errorbar(Ns,y,yerr=e,marker='o',capsize=3,label=f"Blob κ={kappa}")
        if results["etalon"]:
            En=sorted(int(n) for n in results["etalon"]); yE=[results["etalon"][str(n)]*n**(2/3) for n in En]
            plt.plot(En,yE,'k--s',label="étalon cubique 3D")
        plt.xlabel("N"); plt.ylabel("gap_curl · N^(2/3)")
        plt.title("Weyl 3D <=> courbe horizontale (constante)")
        plt.legend(); plt.grid(alpha=0.3); plt.savefig("gap_curl_scaling.png",dpi=130)
        print("Figure : gap_curl_scaling.png")
    except Exception as e:
        print("(plot ignore:",e,")")

if __name__=="__main__":
    main()
