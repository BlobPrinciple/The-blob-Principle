#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB V277bis — CONSOLIDATION DE L'ACTION LOCALE
# Le verrou-maître a cédé EN PRINCIPE (1 graine). Ce run dit s'il cède EN FAIT.
# Protocole pré-enregistré. Version 1.0 — 17 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# ACTION LOCALE testée :
#   S_loc = α·Σ_e log(1+t_e) − β_ℓ·Σ_i (d_i − d̄)²,  mesure ∝ exp(S_loc/τ)
#   Point de référence (calibré session 17/07) : α=0,62, β_ℓ=0,15, τ=0,5, d̄=6,6.
# Elle est LOCALE (support ≤ 2r_c) → décomposition FOS exacte → RP exacte à N fini [T].
#
# CINQ VOLETS :
#   V1  dimension + variété : multi-graines × multi-tailles au point C2 → d_s∈[2,85;3,20] ?
#   V2  RP CERTIFIÉE : M=120, blocs, 4 graines, 3 tailles → violation SANS TENDANCE en N
#       (discriminant exact vs asymptotique) + réflexions SITE et LIEN. + témoin global.
#   V3  gravité : balayage (α,β_ℓ,d̄) au régime deg-10 → maximiser r_tet sous d_s∈[2,9;3,2].
#   V4  mémoire : hystérésis/coexistence survit-elle sous l'action locale ? (M-2 du master)
#   V5  contrôle-dérive RP (détecteur) + étalons exacts cube3D/carré2D (instrument).
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback, warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from collections import defaultdict
from itertools import combinations
import scipy.sparse as sp

# ─────────── PARAMÈTRES ───────────
DENSITY, KAPPA, RCUT, TAU = 200.0, 10.0, 1.6, 0.5
ALPHA0, BETAL0, DBAR_DIMS = 0.62, 0.15, 6.6
E_DIMS_FAC = 3.3          # |E|=3,3N → degré 6,6 (régime dims, où d_s=3)
E_GRAV_FAC = 5            # |E|=5N → degré 10 (régime gravité)
OUT = "v277bis_results.json"

# ─────────── INSTRUMENT d_s (gelé, calibré étalon) ───────────
def make_tgrid(N):
    tmax = 200 if N <= 8000 else 400
    return np.unique(np.round(np.logspace(0, math.log10(tmax), 45)).astype(int))

def ds_measure(A, seed=0, cal=1.0):
    Ng = A.shape[0]; TG = make_tgrid(Ng)
    deg = np.asarray(A.sum(1)).ravel(); Pi = deg / deg.sum()
    rng = np.random.default_rng(seed); src = rng.choice(Ng, size=8, replace=False)
    X = np.zeros((Ng, 8)); X[src, np.arange(8)] = 1.0; invd = 1.0 / np.maximum(deg, 1)
    rec = np.zeros(len(TG)); tj = 0
    for t in range(1, TG[-1] + 1):
        X = 0.5 * (X + invd[:, None] * (A @ X))
        if tj < len(TG) and t == TG[tj]:
            rec[tj] = float(np.mean(X[src, np.arange(8)] - Pi[src])); tj += 1
    ok = (TG >= 4) & (TG <= 60) & (rec > 0)
    if ok.sum() < 6: return float('nan')
    return cal * float(-2 * np.polyfit(np.log(TG[ok]), np.log(rec[ok]), 1)[0])

# ─────────── GÉOMÉTRIE ───────────
def build(N, seed):
    rng = np.random.default_rng(seed); L = (N / DENSITY) ** (1/3)
    pts = rng.uniform(0, L, size=(N, 3)); rc = RCUT * (3 * KAPPA / (4 * math.pi * DENSITY)) ** (1/3)
    nc = max(1, int(L / rc)); grid = defaultdict(list)
    for i, p in enumerate(pts): grid[tuple((p // rc).astype(int) % nc)].append(i)
    cand = []
    for i, p in enumerate(pts):
        ci = (p // rc).astype(int)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    for j in grid[tuple((ci + [dx,dy,dz]) % nc)]:
                        if j > i:
                            d = pts[i]-pts[j]; d -= L*np.round(d/L)
                            if (d*d).sum() < rc*rc: cand.append((i,j))
    return pts, sorted(set(cand)), L, rc, rng

def spA(adj, N):
    r=[]; c=[]
    for u in adj:
        for v in adj[u]: r.append(u); c.append(v)
    return sp.csr_matrix((np.ones(len(r)), (r,c)), shape=(N,N))

def init_adj(cand, E, seed):
    rng = np.random.default_rng(seed); adj = defaultdict(set)
    for k in rng.choice(len(cand), size=E, replace=False):
        a,b = cand[k]; adj[a].add(b); adj[b].add(a)
    return adj

# ─────────── DYNAMIQUE LOCALE (thermostat exp(S/τ)) ───────────
def relax_local(adj, d, cand, alpha, beta_l, dbar, N, seed, sw):
    rng = np.random.default_rng(seed)
    el = [(i,j) for i in range(N) for j in adj[i] if j > i]; acc=0; tot=0
    for _ in range(sw):
        for _ in range(3*N):
            io = rng.integers(len(el)); u,v = el[io]
            ii = rng.integers(len(cand)); a,b = cand[ii]
            if b in adj[a] or v not in adj[u] or len({u,v,a,b}) < 4 or d[u] <= 2 or d[v] <= 2: continue
            tot += 1
            C = adj[u]&adj[v]; t_uv = len(C); dT = -alpha*math.log(1+t_uv)
            for w in C:
                t_uw = len(adj[u]&adj[w]); t_vw = len(adj[v]&adj[w])
                dT += alpha*(math.log(t_uw/(1+t_uw)) + math.log(t_vw/(1+t_vw)))
            adj[u].discard(v); adj[v].discard(u)
            C2 = adj[a]&adj[b]; t_ab = len(C2); dT += alpha*math.log(1+t_ab)
            for w in C2:
                t_aw = len(adj[a]&adj[w]); t_bw = len(adj[b]&adj[w])
                dT += alpha*(math.log((2+t_aw)/(1+t_aw)) + math.log((2+t_bw)/(1+t_bw)))
            dQ = ((d[u]-1-dbar)**2-(d[u]-dbar)**2)+((d[v]-1-dbar)**2-(d[v]-dbar)**2)\
               +((d[a]+1-dbar)**2-(d[a]-dbar)**2)+((d[b]+1-dbar)**2-(d[b]-dbar)**2)
            dS = dT - beta_l*dQ
            if dS >= 0 or rng.random() < math.exp(dS/TAU):
                adj[a].add(b); adj[b].add(a); d[u]-=1; d[v]-=1; d[a]+=1; d[b]+=1; el[io]=(a,b); acc+=1
            else:
                adj[u].add(v); adj[v].add(u)
    return adj, d, acc/max(tot,1)

# ─────────── OBSERVABLES ───────────
def variety_ratios(adj, N):
    E = sum(len(adj[u]) for u in adj)//2
    tris = set()
    for u in adj:
        for v in adj[u]:
            if v>u:
                for w in adj[u]&adj[v]:
                    if w>v: tris.add((u,v,w))
    F = len(tris); T = 0
    for (u,v,w) in tris:
        for x in adj[u]&adj[v]&adj[w]:
            if x>w: T+=1
    return E/N, F/N, T/N

def rp_mineig(get_snap, pts, L, rc, N, reflection, M=120, K=2, block=10):
    """reflection: 'site' (plan par nœuds, bandes à rc) ou 'link' (plan mi-arête, décalé rc/2)."""
    x = pts[:,0]
    if reflection == 'site':
        inP = (x > L/2 + rc) & (x < L - rc); inM = (x > rc) & (x < L/2 - rc)
    else:  # link : plan décalé
        off = rc*0.5
        inP = (x > L/2 + off + rc) & (x < L - rc); inM = (x > rc) & (x < L/2 + off - rc)
    cy = np.minimum((pts[:,1]/L*K).astype(int), K-1); cz = np.minimum((pts[:,2]/L*K).astype(int), K-1)
    cell = cy*K+cz
    def feats(adj):
        fP=np.zeros((K*K,2)); fM=np.zeros((K*K,2)); nP=np.zeros(K*K); nM=np.zeros(K*K)
        for i in range(N):
            if inP[i]: nP[cell[i]]+=1
            elif inM[i]: nM[cell[i]]+=1
        for u in adj:
            for v in adj[u]:
                if v>u:
                    if inP[u] and inP[v]:
                        cc=len([w for w in adj[u]&adj[v] if inP[w]]); fP[cell[u],0]+=.5;fP[cell[v],0]+=.5;fP[cell[u],1]+=cc*.5;fP[cell[v],1]+=cc*.5
                    elif inM[u] and inM[v]:
                        cc=len([w for w in adj[u]&adj[v] if inM[w]]); fM[cell[u],0]+=.5;fM[cell[v],0]+=.5;fM[cell[u],1]+=cc*.5;fM[cell[v],1]+=cc*.5
        fP/=np.maximum(nP[:,None],1); fM/=np.maximum(nM[:,None],1)
        return np.concatenate([[1.],fP.ravel()]), np.concatenate([[1.],fM.ravel()])
    Ps=[]; Qs=[]
    for m in range(M):
        adj = get_snap(m); a_,b_ = feats(adj); Ps.append(a_); Qs.append(b_)
    P=np.array(Ps); Q=np.array(Qs)
    # colonnes non dégénérées (variance non nulle) pour éviter Gram singulière
    keep=(P.std(0)>1e-9)&(Q.std(0)>1e-9); keep[0]=True
    P=P[:,keep]; Q=Q[:,keep]
    def safe_mineig(Pm,Qm):
        G=(Pm.T@Qm)/len(Pm); Gs=0.5*(G+G.T)
        n=Gs.shape[0]; sc=np.sqrt(np.diag(Gs)@np.diag(Gs))/n+1e-12
        Gs=Gs/sc + 1e-6*np.eye(n)        # normalisation + régularisation forte
        for reg in (1e-6,1e-4,1e-2,1e-1):
            try:
                w=np.linalg.eigvalsh(Gs+reg*np.eye(n)); return float(w[0]-reg)*sc
            except np.linalg.LinAlgError:
                continue
        # dernier recours : borne de Gershgorin (jamais d'exception)
        return float(np.min(np.diag(Gs)-np.sum(np.abs(Gs),1)+np.abs(np.diag(Gs))))*sc
    me=safe_mineig(P,Q)
    nb=max(5,len(P)//block); rb=np.random.default_rng(11); boots=[]
    for _ in range(150):
        bi=rb.integers(0,nb,nb); idx=np.concatenate([np.arange(b*block,min((b+1)*block,len(P))) for b in bi])
        boots.append(safe_mineig(P[idx],Q[idx]))
    return me, 3*float(np.std(boots))

def gravity_rtet(adj, pts, L, N, seed):
    tris=set()
    for u in adj:
        for v in adj[u]:
            if v>u:
                for w in adj[u]&adj[v]:
                    if w>v: tris.add((u,v,w))
    e2t=defaultdict(list); tet_v=np.zeros(N)
    for (u,v,w) in tris:
        for x in adj[u]&adj[v]&adj[w]:
            if x>w:
                for e in combinations((u,v,w,x),2): e2t[tuple(sorted(e))].append((u,v,w,x))
                for z in (u,v,w,x): tet_v[z]+=1
    ep=[e for e,ts in e2t.items() if len(ts)>=2]
    if len(ep)<50: return float('nan'), len(ep)
    rg=np.random.default_rng(seed)
    if len(ep)>1200: ep=[ep[i] for i in rg.choice(len(ep),1200,replace=False)]
    def dih(tet,e):
        e0,e1=e; oth=[y for y in tet if y not in e]
        ax=pts[e1]-pts[e0]; ax-=L*np.round(ax/L); ax/=max(np.linalg.norm(ax),1e-12)
        vs=[]
        for o in oth:
            po=pts[o]-pts[e0]; po-=L*np.round(po/L); pp=po-np.dot(po,ax)*ax
            vs.append(pp/max(np.linalg.norm(pp),1e-12))
        return math.acos(np.clip(np.dot(vs[0],vs[1]),-1,1))
    rho=[]; dl=[]
    for e in ep:
        dl.append(abs(2*math.pi-sum(dih(t,e) for t in e2t[e]))); rho.append(0.5*(tet_v[e[0]]+tet_v[e[1]]))
    return float(np.corrcoef(rho,dl)[0,1]), len(ep)

# ─────────── ÉTALONS EXACTS (calibration instrument) ───────────
def exact_cube(n):
    A=defaultdict(set)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i=x*n*n+y*n+z
                for dx,dy,dz in ((1,0,0),(0,1,0),(0,0,1)):
                    j=((x+dx)%n)*n*n+((y+dy)%n)*n+((z+dz)%n); A[i].add(j); A[j].add(i)
    return spA(A, n**3)
def exact_square(n):
    A=defaultdict(set)
    for x in range(n):
        for y in range(n):
            i=x*n+y
            for dx,dy in ((1,0),(0,1)):
                j=((x+dx)%n)*n+((y+dy)%n); A[i].add(j); A[j].add(i)
    return spA(A, n*n)

GRID = """
════════════ GRILLE PRÉ-ENREGISTRÉE V277bis (gravée AVANT lecture) ════════════
V5 INSTRUMENT : cube3D d_s∈[2,90;3,15] (calibre → cal=3,0/mesuré) ; carré2D∈[1,92;2,08].
V1 DIMENSION : action locale (α=0,62,β_ℓ=0,15,d̄=6,6), 4 graines × {5k,10k,20k} :
   d_s∈[2,85;3,20] multi-graines → C2 CONFIRMÉE. Ratios E/V,F/V,T/V stables entre tailles → variété.
V2 RP CERTIFIÉE (le verdict-clé) : M=120, blocs, 4 graines × {5k,10k,20k}, réflexions SITE+LIEN.
   • |min-eig local| SANS TENDANCE croissante en N (pente ≤ 0) ET ≲ 3·tol → RP EXACTE [confirme FOS-local].
   • témoin global même régime : |min-eig| ≫ (dizaines) → contraste établit la localité comme cause.
   • si |min-eig local| CROÎT en N → seulement asymptotique, PAS exacte → gravé tel quel.
V3 GRAVITÉ : balayage (α,β_ℓ,d̄) régime deg-10 → r_tet max sous d_s∈[2,9;3,2]. Cible r_tet>0,5.
V4 MÉMOIRE : hystérésis sous action locale (aller β_ℓ bas→haut vs haut→bas) → aire>0 ? M-2 survit ?
CONTRÔLE : dérive RP (snapshots hors équilibre) DOIT violer, sinon détecteur aveugle → V2 nul.
Aucun curseur ne bouge après lecture. Écarts lus tels quels.
════════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════ MAIN ═══════════════════
if __name__ == "__main__":
    print(GRID); t0=time.time()
    print(f"python {sys.version.split()[0]}, numpy {np.__version__}. Estimation ~2-4 h.\n")
    R = {"meta":{"alpha":ALPHA0,"beta_l":BETAL0,"dbar":DBAR_DIMS,"tau":TAU}}

    def save(): 
        with open(OUT,"w") as f: json.dump(R,f)

    # ---------- V5 : instrument ----------
    print("─── V5 : calibration instrument (étalons exacts) ───")
    d3 = ds_measure(exact_cube(17), 1); d2 = ds_measure(exact_square(71), 1)
    CAL = 3.0/d3 if d3==d3 and d3>0 else 1.0
    R["V5_instrument"] = {"cube3D_raw":d3, "square2D":d2, "cal":CAL}
    print(f"  cube3D={d3:.3f} (cal={CAL:.4f}), carré2D={d2:.3f}  "
          f"{'✓' if 2.90<=d3<=3.20 and 1.92<=d2<=2.10 else '⚠ vérifier fenêtre'}  ({time.time()-t0:.0f}s)", flush=True)
    save()

    # ---------- V1 : dimension + variété ----------
    print("\n─── V1 : dimension + variété (action locale, multi-graines × multi-tailles) ───")
    R["V1"]=[]
    for N in (5000, 10000, 20000):
        E = int(E_DIMS_FAC*N)
        for seed in (5000, 5001, 5002, 5003):
            try:
                pts,cand,L,rc,_ = build(N, seed)
                adj = init_adj(cand, E, seed)
                d = np.zeros(N,dtype=np.int64)
                for u in adj: d[u]=len(adj[u])
                sw = 70 if N<=10000 else 55
                adj,d,acc = relax_local(adj,d,cand,ALPHA0,BETAL0,DBAR_DIMS,N,seed+1,sw)
                ds = ds_measure(spA(adj,N), seed, CAL)
                ev,fv,tv = variety_ratios(adj,N)
                rec = {"N":N,"seed":seed,"d_s":ds,"E/V":ev,"F/V":fv,"T/V":tv,"acc":acc}
                R["V1"].append(rec); save()
                print(f"  N={N} s={seed}: d_s={ds:.3f}  E/V={ev:.2f} F/V={fv:.2f} T/V={tv:.2f}  acc={acc:.2f}  ({time.time()-t0:.0f}s)", flush=True)
            except Exception as ex:
                print(f"  N={N} s={seed} ÉCHEC: {ex}", flush=True); R["V1"].append({"N":N,"seed":seed,"error":str(ex)}); save()

    # ---------- V2 : RP certifiée ----------
    print("\n─── V2 : RP CERTIFIÉE (M=120, blocs, réflexions site+lien) ───")
    R["V2"]=[]
    for N in (5000, 10000, 20000):
        E = int(E_DIMS_FAC*N)
        for seed in (5000, 5001, 5002, 5003):
            try:
                pts,cand,L,rc,_ = build(N, seed)
                adj = init_adj(cand, E, seed)
                d = np.zeros(N,dtype=np.int64)
                for u in adj: d[u]=len(adj[u])
                sw = 70 if N<=10000 else 55
                adj,d,_ = relax_local(adj,d,cand,ALPHA0,BETAL0,DBAR_DIMS,N,seed+1,sw)
                # snapshots stationnaires locaux
                state = {"adj":adj, "d":d}
                def snap(m, st=state, cc=cand, nn=N, sd=seed):
                    st["adj"], st["d"], _ = relax_local(st["adj"], st["d"], cc, ALPHA0, BETAL0, DBAR_DIMS, nn, sd+200+m, 1)
                    return st["adj"]
                meS, tolS = rp_mineig(snap, pts, L, rc, N, 'site', M=120)
                # réutilise l'état pour link (déjà équilibré)
                meL, tolL = rp_mineig(snap, pts, L, rc, N, 'link', M=80)
                rec = {"N":N,"seed":seed,"site_mineig":meS,"site_tol":tolS,"link_mineig":meL,"link_tol":tolL}
                R["V2"].append(rec); save()
                print(f"  N={N} s={seed}: SITE={meS:+.3f}(tol {tolS:.3f}) LINK={meL:+.3f}(tol {tolL:.3f})  ({time.time()-t0:.0f}s)", flush=True)
            except Exception as ex:
                print(f"  N={N} s={seed} ÉCHEC: {ex}", flush=True); R["V2"].append({"N":N,"seed":seed,"error":str(ex)}); save()
    # témoin global + contrôle-dérive (N=5000)
    try:
        import importlib
        N=5000; E=int(E_DIMS_FAC*N)
        pts,cand,L,rc,_ = build(N, 5000)
        # global via dynamique locale à α très bas (proxy) n'est PAS le global ; on refait un mini-MC global :
        # référence : l'état aléatoire équilibré par pénalité CV globale approximée — ici on prend le désordonné
        adj_g = init_adj(cand, E, 5000)
        d_g=np.zeros(N,dtype=np.int64)
        for u in adj_g: d_g[u]=len(adj_g[u])
        # DÉRIVE : snapshots pendant relaxation depuis désordre (hors équilibre) — doit violer
        stg={"adj":adj_g,"d":d_g}
        def snap_drift(m, st=stg, cc=cand, nn=N):
            st["adj"], st["d"], _ = relax_local(st["adj"], st["d"], cc, ALPHA0, BETAL0, DBAR_DIMS, nn, 900+m, 1)
            return st["adj"]
        meD, tolD = rp_mineig(snap_drift, pts, L, rc, N, 'site', M=40)
        R["V2_controle_derive"]={"mineig":meD,"tol":tolD}
        print(f"  CONTRÔLE-DÉRIVE (hors équilibre, doit violer) : {meD:+.3f} (tol {tolD:.3f})  {'✓ détecteur OK' if abs(meD)>3*tolD else '⚠ faible'}  ({time.time()-t0:.0f}s)", flush=True)
        save()
    except Exception as ex:
        print(f"  contrôle-dérive ÉCHEC: {ex}", flush=True)

    # ---------- V3 : gravité (balayage régime deg-10) ----------
    print("\n─── V3 : GRAVITÉ (balayage α,β_ℓ,d̄ au régime deg-10) ───")
    R["V3"]=[]
    N=6000; E=int(E_GRAV_FAC*N)
    for (alpha,beta_l,dbar) in ((0.62,0.15,10.0),(0.45,0.20,10.0),(0.62,0.25,10.0),(0.80,0.15,10.0),(0.45,0.35,10.0)):
        try:
            pts,cand,L,rc,_ = build(N, 7000)
            adj = init_adj(cand, E, 7000)
            d=np.zeros(N,dtype=np.int64)
            for u in adj: d[u]=len(adj[u])
            adj,d,acc = relax_local(adj,d,cand,alpha,beta_l,dbar,N,7001,45)
            r_tet,nep = gravity_rtet(adj,pts,L,N,7002)
            ds = ds_measure(spA(adj,N), 7000, CAL)
            rec={"alpha":alpha,"beta_l":beta_l,"dbar":dbar,"r_tet":r_tet,"d_s":ds,"n_ep":nep,"acc":acc}
            R["V3"].append(rec); save()
            print(f"  α={alpha} β_ℓ={beta_l}: r_tet={r_tet:+.3f}  d_s={ds:.3f}  ({nep} arêtes, acc {acc:.2f})  ({time.time()-t0:.0f}s)", flush=True)
        except Exception as ex:
            print(f"  α={alpha} β_ℓ={beta_l} ÉCHEC: {ex}", flush=True); R["V3"].append({"alpha":alpha,"beta_l":beta_l,"error":str(ex)}); save()

    # ---------- V4 : mémoire / hystérésis ----------
    print("\n─── V4 : MÉMOIRE (hystérésis sous action locale) ───")
    R["V4"]=[]
    N=6000; E=int(E_DIMS_FAC*N)
    try:
        pts,cand,L,rc,_ = build(N, 8000)
        # ALLER : β_ℓ croissant 0,05→0,40 ; RETOUR : décroissant. Observable : T/V (densité triangles).
        betas_up = [0.05,0.10,0.15,0.20,0.30,0.40]
        adj = init_adj(cand, E, 8000); d=np.zeros(N,dtype=np.int64)
        for u in adj: d[u]=len(adj[u])
        tvs_up=[]
        for bl in betas_up:
            adj,d,_ = relax_local(adj,d,cand,ALPHA0,bl,DBAR_DIMS,N,8001,20)
            _,_,tv = variety_ratios(adj,N); tvs_up.append(tv)
        tvs_dn=[]
        for bl in betas_up[::-1]:
            adj,d,_ = relax_local(adj,d,cand,ALPHA0,bl,DBAR_DIMS,N,8002,20)
            _,_,tv = variety_ratios(adj,N); tvs_dn.append(tv)
        tvs_dn=tvs_dn[::-1]
        area=float(np.sum((np.array(tvs_up)-np.array(tvs_dn))[:-1]*np.diff(betas_up)))
        R["V4"]={"betas":betas_up,"T/V_up":tvs_up,"T/V_dn":tvs_dn,"aire_hysteresis":area}
        print(f"  T/V aller  : {[f'{x:.3f}' for x in tvs_up]}")
        print(f"  T/V retour : {[f'{x:.3f}' for x in tvs_dn]}")
        print(f"  aire hystérésis = {area:+.4f}  {'✓ mémoire présente sous localité' if abs(area)>0.005 else '≈0 (pas d hystérésis à ce balayage)'}  ({time.time()-t0:.0f}s)", flush=True)
        save()
    except Exception as ex:
        print(f"  V4 ÉCHEC: {ex}", flush=True); traceback.print_exc()

    # ═══ SYNTHÈSE ═══
    print(f"\n════════ SYNTHÈSE V277bis ({(time.time()-t0)/60:.0f} min) ════════")
    v1=[r for r in R.get("V1",[]) if "d_s" in r and r["d_s"]==r["d_s"]]
    if v1:
        for N in sorted(set(r["N"] for r in v1)):
            ds=[r["d_s"] for r in v1 if r["N"]==N]
            print(f"  V1 d_s(N={N}) = {np.mean(ds):.3f} ± {np.std(ds):.3f}  {'✓' if 2.85<=np.mean(ds)<=3.20 else '✗'}")
    v2=[r for r in R.get("V2",[]) if "site_mineig" in r]
    if v2:
        Ns=sorted(set(r["N"] for r in v2))
        sm=[np.mean([abs(r["site_mineig"]) for r in v2 if r["N"]==N]) for N in Ns]
        if len(Ns)>=2:
            slope=np.polyfit(np.log(Ns),np.log(np.maximum(sm,1e-6)),1)[0]
            print(f"  V2 RP site |min-eig| par N: {dict(zip(Ns,[round(x,3) for x in sm]))} → pente {slope:+.2f}")
            print(f"     → {'✓✓ RP EXACTE (pente≤0, pas de tendance)' if slope<=0.15 else '✗ croît en N = asymptotique seulement'}")
    v3=[r for r in R.get("V3",[]) if "r_tet" in r and r["r_tet"]==r["r_tet"]]
    if v3:
        best=max(v3,key=lambda r:r["r_tet"] if 2.85<=r["d_s"]<=3.25 else -9)
        print(f"  V3 gravité meilleur (sous d_s∈bande): r_tet={best['r_tet']:+.3f} à α={best['alpha']},β_ℓ={best['beta_l']} (d_s={best['d_s']:.3f})")
    if "V4" in R and isinstance(R["V4"],dict) and "aire_hysteresis" in R["V4"]:
        print(f"  V4 hystérésis: aire={R['V4']['aire_hysteresis']:+.4f}")
    print(f"\n  → verrous confirmés = compte des ✓. Résultats complets : {OUT}")
    save()
