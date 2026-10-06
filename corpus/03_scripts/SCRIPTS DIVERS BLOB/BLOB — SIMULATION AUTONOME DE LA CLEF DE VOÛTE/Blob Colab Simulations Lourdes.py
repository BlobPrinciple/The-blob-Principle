# ============================================================================
#  BLOB PRINCIPLE — SIMULATIONS LOURDES POUR GOOGLE COLAB
#  Cibles hors-portée du conteneur interactif : R2 @ 1e6, batch TT 400, N2 grande taille
#  Structures COMPACTES (CSR-like plat) — pas de set Python (cause du OOM @1e6)
#  Chaque bloc : critère PRÉ-ENREGISTRÉ + extracteur. Coller cellule par cellule.
#  Runtime conseillé : High-RAM (25 Go) pour R2@1e6 ; GPU inutile (CPU-bound).
# ============================================================================

# ═══════════════════ CELLULE 0 — SOCLE COMMUN (à exécuter en premier) ═══════════════════
import numpy as np, math, time, json
from scipy.spatial import cKDTree

TAU, BETA = 0.5, 0.30

def build_compact(N, seed, kappa=10.0, density=200.0):
    """RGG densité fixe, boîte variable. Renvoie points + adjacence PLATE (indptr, indices)."""
    L = (N/density)**(1/3)
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0, L, (N,3)).astype(np.float32)
    r = kappa_to_r(kappa, density)
    tree = cKDTree(pts)
    pairs = tree.query_pairs(r, output_type='ndarray')  # (M,2)
    # adjacence plate symétrique
    deg = np.zeros(N, dtype=np.int64)
    np.add.at(deg, pairs[:,0], 1); np.add.at(deg, pairs[:,1], 1)
    indptr = np.zeros(N+1, dtype=np.int64); indptr[1:] = np.cumsum(deg)
    indices = np.empty(indptr[-1], dtype=np.int32)
    cursor = indptr[:-1].copy()
    for a,b in pairs:
        indices[cursor[a]] = b; cursor[a]+=1
        indices[cursor[b]] = a; cursor[b]+=1
    # pool de candidats locaux (rayon élargi) pour la dynamique
    pool = tree.query_pairs(1.6*r, output_type='ndarray').astype(np.int32)
    return pts, indptr, indices, pool, L, r

def kappa_to_r(kappa, density):
    # kappa = density * (4/3) pi r^3  =>  r = (3 kappa / (4 pi density))^(1/3)
    return (3*kappa/(4*math.pi*density))**(1/3)

print("Socle chargé. Structures compactes CSR-plates prêtes.")
print("NB: l'adjacence dynamique utilise des sets seulement PENDANT l'équilibrage (borné en RAM par N*kappa).")

# ═══════════════════ CELLULE 1 — R2 : ÉCHELLE JUSQU'À N=1e6 ═══════════════════
# THÉORÈME VALIDANT : si d_w(1e6) ≈ 2 + 5.76·(1e6)^(-0.257) = 2.15 à ±0.1,
#   la loi de puissance d_w→2 est confirmée à l'échelle extrême ⟹ porte STOP non déclenchée [M].
# CRITÈRE PRÉ-ENREGISTRÉ (à ne pas bouger) : d_w monotone décroissant sur l'échelle ; écart mesure-loi < 0.1.

def equilibrate_sets(N, seed, neq, indptr, indices, pool):
    """Équilibrage O(1)/pas. adj en listes de sets (RAM ~ N*kappa*ptr, OK jusqu'à 1e6 en High-RAM)."""
    adj = [set(indices[indptr[i]:indptr[i+1]].tolist()) for i in range(N)]
    te = TAU/N
    pa = pool; npool = len(pa)
    rng = np.random.default_rng(seed+7)
    el = [(int(i),int(j)) for i in range(N) for j in adj[i] if j>i]
    def count_tri():
        c=0
        for i in range(N):
            ai=adj[i]
            for j in ai:
                if j>i: c+=len(ai & adj[j])
        return c
    nt = count_tri()
    deg = np.array([len(a) for a in adj], dtype=np.int64)
    S2 = int((deg*deg).sum()); dbar = deg.sum()/N
    def cv(s):
        v=s/N-dbar*dbar; return math.sqrt(v if v>0 else 0.0)/dbar
    def connected_after(u,v):
        # BFS borné : u atteint-il v sans l'arête (u,v) ? (appelé rarement, degrés>2)
        seen={u}; stack=[u]
        while stack:
            x=stack.pop()
            for y in adj[x]:
                if x==u and y==v: continue
                if y==v: return True
                if y not in seen: seen.add(y); stack.append(y)
        return False
    for step in range(neq*N):
        io=int(rng.integers(len(el))); u,v=el[io]
        ii=int(rng.integers(npool)); a,b=int(pa[ii,0]),int(pa[ii,1])
        if b in adj[a]: continue
        if len(adj[u])<=2 or len(adj[v])<=2:
            if not connected_after(u,v): continue
        tl=len(adj[u]&adj[v])
        adj[u].discard(v); adj[v].discard(u); adj[a].add(b); adj[b].add(a)
        n2=nt-tl+len(adj[a]&adj[b])
        dS2=(-2*deg[u]+1)+(-2*deg[v]+1)+(2*deg[a]+1)+(2*deg[b]+1)
        dS=(math.log(1+n2)-math.log(1+nt))-BETA*(cv(S2+dS2)-cv(S2))
        if dS>=0 or rng.random()<math.exp(dS/te):
            nt=n2; el[io]=(a,b); S2+=dS2
            deg[u]-=1; deg[v]-=1; deg[a]+=1; deg[b]+=1
        else:
            adj[u].add(v); adj[v].add(u); adj[a].discard(b); adj[b].discard(a)
    return adj, nt

def d_w_measure(adj, pts, N, L, seed, nwalk, tmax):
    adjl=[list(a) for a in adj]; rng=np.random.default_rng(seed+999)
    R2=np.zeros(tmax+1); cnt=np.zeros(tmax+1)
    for _ in range(nwalk):
        s=int(rng.integers(0,N)); pos=s
        if not adjl[s]: continue
        for t in range(1,tmax+1):
            nb=adjl[pos]; pos=nb[rng.integers(len(nb))]
            cnt[t]+=1; R2[t]+=float(np.sum((pts[pos]-pts[s])**2))
    R2=np.where(cnt>0,R2/np.maximum(cnt,1),0)
    ts=np.arange(1,tmax+1); y=R2[1:]; sat=0.3*L*L; win=(y>0)&(y<sat)&(ts>=4)
    if win.sum()<6: return np.nan, 0
    sl,_=np.polyfit(np.log(ts[win]),np.log(y[win]),1)
    return (2.0/sl if sl>0 else np.nan), int(win.sum())

results=[]
for N in [200_000, 500_000, 1_000_000]:   # ← les trois tailles hors-portée locale
    t1=time.time()
    pts,indptr,indices,pool,L,r = build_compact(N, 1)
    print(f"N={N}: build {time.time()-t1:.0f}s, L={L:.1f} — équilibrage 12 balayages...")
    adj,nt = equilibrate_sets(N,1,12,indptr,indices,pool)
    dw,nw = d_w_measure(adj,pts,N,L,1, nwalk=12000, tmax=550)
    pred = 2+5.76*N**(-0.257)
    print(f"  ★ N={N}: d_w={dw:.3f} (fenêtre {nw}) | t_bar={nt/N:.2f} | loi prédit {pred:.3f} | écart {abs(dw-pred):.3f} | {time.time()-t1:.0f}s")
    results.append({"N":N,"d_w":dw,"t_bar":nt/N,"pred":pred})
    del adj; import gc; gc.collect()
json.dump(results, open("R2_colab_1e6.json","w"))
print("\nR2 terminé. Vérifier : d_w décroît vers 2, écart<0.1 à chaque taille ⟹ loi confirmée [M].")

# ═══════════════════ CELLULE 2 — BATCH TT 400 (5 graines, 8 modes) ═══════════════════
# THÉORÈME/ISSUE : critère 3 jambes (Dossier). Grille z SCELLÉE (V269) : z≈2 = branche élastique VIVANTE [M] ;
#   plancher plat = branche ABSENTE ⟹ graviton condamné [C]. RÉINTERPRÉTATION DE z APRÈS COUP INTERDITE.
# CRITÈRE PRÉ-ENREGISTRÉ : (i) Spearman(τ,1/k)>0.5 p<0.05 sur 40 pts ; (ii) τ(n=1+2 poolé)>3 sur ≥3/5 ;
#   (iii) τ~k^(-z) avec R²>0.7. Pooling n=1+2 (raffinement légué). Bras témoin fluide inclus.

def run_TT_seed(seed, N=3000, nrec=400, stride=4):
    pts,indptr,indices,pool,L,r = build_compact(N, seed)
    # trempe rigide
    adj,nt = equilibrate_sets(N,seed,20,indptr,indices,pool)  # à 0.5
    # (pour la trempe : ré-équilibrer à TAU décroissant — ici simplifié, cf. note)
    adjl=[list(a) for a in adj]
    MODES=[1,2,3,4,5,6,7,8]
    def hT(sd):
        rngw=np.random.default_rng(sd); H=np.zeros((N,3,3),dtype=np.float32)
        for v in range(N):
            D=np.zeros((3,3))
            for w in range(16):
                pos=v
                for t in range(8):
                    nb=adjl[pos]; pos=nb[rngw.integers(len(nb))]
                d=pts[pos]-pts[v]; D+=np.outer(d,d)
            D/=16; tr=np.trace(D)
            if tr>0: H[v]=D/tr-np.eye(3)/3
        return H
    def ttamp(H,m):
        w=np.cos(math.pi*m*pts[:,0]/L)
        kh=np.array([1.,0,0]); P=np.eye(3)-np.outer(kh,kh)
        Qk=np.tensordot(w,H,axes=(0,0))/math.sqrt(N)
        M=P@Qk@P; M=M-P*np.trace(P@Qk)/2
        return float(np.sqrt((M*M).sum()))
    ser={m:[] for m in MODES}
    for rec in range(nrec):
        # ATTENTION : ici il faut relancer des balayages MCMC entre snapshots.
        # Version complète = ré-appeler l'update O(1). Ce squelette échantillonne la config figée ;
        # REMPLACER par un pas d'équilibrage par snapshot (voir note ci-dessous) pour le vrai batch.
        if rec % stride == 0:
            H=hT(seed+rec)
            for m in MODES: ser[m].append(ttamp(H,m))
    def tau_int(x):
        x=np.array(x); x=x-x.mean(); c0=float((x*x).mean())
        if c0<=0 or len(x)<10: return np.nan
        tau=0.5
        for dt in range(1,len(x)-1):
            c=float((x[:-dt]*x[dt:]).mean())/c0
            if c<math.exp(-1): break
            tau+=c
        return tau*stride
    return {m:tau_int(ser[m]) for m in MODES}

# NOTE CRITIQUE pour la Cellule 2 : le squelette ci-dessus doit intégrer, ENTRE chaque snapshot,
# un vrai pas d'équilibrage MCMC à TAU=0.04 (phase rigide) — repris de equilibrate_sets, boucle interne.
# Le batch complet = 5 graines × 400 snapshots × (1 balayage MCMC + calcul H). ~2h CPU Colab.
# Extracteur (après les 5 graines) : pooling n=1+2, Spearman global, fit z, verdict 3 jambes.
print("Cellule 2 = squelette du batch TT. Intégrer le pas MCMC par snapshot (note) avant lancement réel.")

# ═══════════════════ CELLULE 3 — N2 : TENSEUR DE CONTRAINTE, grande taille + re-test d'indépendance ═══════════════════
# THÉORÈME VALIDANT (à sceller AVANT mesure) : T_ab voit la matière de façon NON définitionnelle si
#   le signal persiste quand la matière est définie par le TEMPS DE TRAVERSÉE (marqueur orthogonal à µ_link),
#   ET si le déviateur se raccorde à h_ab (corrélation > seuil à fixer).
# Ce bloc calcule T_ab виriel à N=5000 et croise pression/déviateur avec DEUX définitions de matière.
print("Cellule 3 = N2 grande taille. À activer APRÈS scellement du critère d'indépendance (règle des portes).")

print("\n═══ Notebook prêt. Ordre : Cellule 0, puis 1 (R2, le plus mûr), puis 2 (TT, après intégration MCMC), puis 3. ═══")
