#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — CYCLE 2 DE L'ACTION LOCALE : PARETO, HYSTÉRÉSIS-α, L2, TÉMOIN, TOPOLOGIE
# Protocole pré-enregistré. Version 1.0 — 17 juillet 2026.
# Suite du run V277bis (confirmé : d_s≈3 multi-tout ; RP exacte site+lien ; r_tet=0,612
# accessible à α=0,80). Ce run exécute les ordres du Tribunal des 8.
# ═══════════════════════════════════════════════════════════════════════════
# W1 PARETO FIN : grille α×β_ℓ au régime gravité (deg 10) → localiser le POINT JOINT
#     d_s∈[2,90;3,20] ET r_tet>0,50. Coordonnées de macroétat (F/V, CV) enregistrées
#     (consigne du tribunal : l'écart local/global doit se refermer à macroétat égal).
# W2 HYSTÉRÉSIS EN α : l'axe de la transition locale est α (falaise 0,62→0,72), pas β_ℓ.
#     Aller-retour α, protocole rapide → aire > 0 = mémoire du premier ordre sous localité.
# W3 CANDIDATE L2 : tilt linéaire S_L2 = a·T − b·X, coefficients DÉRIVÉS (a=1/(τ·t̄),
#     b=β/(2τ·CV·μ²), zéro paramètre ajusté) → d_s≈3 ET RP au plancher = équivalence en acte.
# W4 TÉMOIN GLOBAL INTÉGRÉ : action globale, mêmes features/bandes → DOIT violer fortement.
#     Boucle en interne la clause du contrôle (la non-cécité de l'instrument).
# W5 TOPOLOGIE SOUS LOCALE : b₁, χ, ratios au point C2 → le socle de e^{iω} vérifié.
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from collections import defaultdict
from itertools import combinations
import scipy.sparse as sp

DENSITY, KAPPA, RCUT, TAU = 200.0, 10.0, 1.6, 0.5
ALPHA_C2, BETAL_C2, DBAR_DIMS = 0.62, 0.15, 6.6
OUT = "cycle2_results.json"

GRID = """
════════════ GRILLE PRÉ-ENREGISTRÉE CYCLE 2 (gravée AVANT lecture) ════════════
W1 : POINT JOINT trouvé si ∃(α,β_ℓ) avec d_s∈[2,90;3,20] ET r_tet>0,50 (2 graines
     concordantes). Sinon : cartographier le front de Pareto tel quel (max r_tet à
     d_s∈bande). Lire AUSSI en macroétat (F/V, CV) : si r_tet(local)≈r_tet(global) à
     macroétat égal → le pont d'équivalence est soutenu.
W2 : aire d'hystérésis en α > 0,01 (aller-retour, 6 sw/pas) → PREMIER ORDRE et MÉMOIRE
     sous l'action locale [M]. |aire|<0,01 → non détectée, tel quel.
W3 : L2 (coefficients dérivés, zéro ajusté) : d_s∈[2,80;3,25] ET RP site ≤ 2·tol →
     ÉQUIVALENCE EN ACTE (le tilt du Théorème S reproduit la géométrie avec RP exacte).
     Dégénérescence (d_s effondré / T explose) → gravé tel quel (l'avertissement ERGM).
W4 : témoin global |min-eig| ≥ 10× le max local du run V277bis (≥0,4) → instrument
     non-aveugle certifié EN INTERNE. Sinon → toute la série RP à réauditer.
W5 : b₁/V > 1 (topologie riche, socle e^{iω}) ; ratios stables. Tel quel.
Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

# ─────────── géométrie + graphes ───────────
def build(N, seed):
    rng = np.random.default_rng(seed); L = (N/DENSITY)**(1/3)
    pts = rng.uniform(0, L, size=(N,3)); rc = RCUT*(3*KAPPA/(4*math.pi*DENSITY))**(1/3)
    nc = max(1,int(L/rc)); grid = defaultdict(list)
    for i,p in enumerate(pts): grid[tuple((p//rc).astype(int)%nc)].append(i)
    cand=[]
    for i,p in enumerate(pts):
        ci=(p//rc).astype(int)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    for j in grid[tuple((ci+[dx,dy,dz])%nc)]:
                        if j>i:
                            d=pts[i]-pts[j]; d-=L*np.round(d/L)
                            if (d*d).sum()<rc*rc: cand.append((i,j))
    return pts, sorted(set(cand)), L, rc, rng

def init_adj(cand, E, seed):
    rng=np.random.default_rng(seed); adj=defaultdict(set)
    for k in rng.choice(len(cand), size=E, replace=False):
        a,b=cand[k]; adj[a].add(b); adj[b].add(a)
    return adj

def degs(adj, N):
    d=np.zeros(N,dtype=np.int64)
    for u in adj: d[u]=len(adj[u])
    return d

def spA(adj, N):
    r=[];c=[]
    for u in adj:
        for v in adj[u]: r.append(u); c.append(v)
    return sp.csr_matrix((np.ones(len(r)),(r,c)), shape=(N,N))

# ─────────── instrument d_s (gelé + étalon) ───────────
def ds_measure(A, seed=0, cal=1.0):
    Ng=A.shape[0]; TG=np.unique(np.round(np.logspace(0, math.log10(200 if Ng<=8000 else 400), 45)).astype(int))
    deg=np.asarray(A.sum(1)).ravel(); Pi=deg/deg.sum()
    rng=np.random.default_rng(seed); src=rng.choice(Ng, size=8, replace=False)
    X=np.zeros((Ng,8)); X[src,np.arange(8)]=1.0; invd=1.0/np.maximum(deg,1)
    rec=np.zeros(len(TG)); tj=0
    for t in range(1, TG[-1]+1):
        X=0.5*(X+invd[:,None]*(A@X))
        if tj<len(TG) and t==TG[tj]: rec[tj]=float(np.mean(X[src,np.arange(8)]-Pi[src])); tj+=1
    ok=(TG>=4)&(TG<=60)&(rec>0)
    if ok.sum()<6: return float('nan')
    return cal*float(-2*np.polyfit(np.log(TG[ok]), np.log(rec[ok]), 1)[0])

def exact_cube(n):
    A=defaultdict(set)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i=x*n*n+y*n+z
                for dx,dy,dz in ((1,0,0),(0,1,0),(0,0,1)):
                    j=((x+dx)%n)*n*n+((y+dy)%n)*n+((z+dz)%n); A[i].add(j); A[j].add(i)
    return spA(A, n**3)

# ─────────── dynamique LOCALE L1 ───────────
def relax_L1(adj, d, cand, alpha, beta_l, dbar, N, seed, sw):
    rng=np.random.default_rng(seed); el=[(i,j) for i in range(N) for j in adj[i] if j>i]; acc=0; tot=0
    for _ in range(sw):
        for _ in range(3*N):
            io=rng.integers(len(el)); u,v=el[io]; ii=rng.integers(len(cand)); a,b=cand[ii]
            if b in adj[a] or v not in adj[u] or len({u,v,a,b})<4 or d[u]<=2 or d[v]<=2: continue
            tot+=1
            C=adj[u]&adj[v]; t_uv=len(C); dT=-alpha*math.log(1+t_uv)
            for w in C:
                tuw=len(adj[u]&adj[w]); tvw=len(adj[v]&adj[w])
                dT+=alpha*(math.log(tuw/(1+tuw))+math.log(tvw/(1+tvw)))
            adj[u].discard(v); adj[v].discard(u)
            C2=adj[a]&adj[b]; dT+=alpha*math.log(1+len(C2))
            for w in C2:
                taw=len(adj[a]&adj[w]); tbw=len(adj[b]&adj[w])
                dT+=alpha*(math.log((2+taw)/(1+taw))+math.log((2+tbw)/(1+tbw)))
            dQ=((d[u]-1-dbar)**2-(d[u]-dbar)**2)+((d[v]-1-dbar)**2-(d[v]-dbar)**2)\
              +((d[a]+1-dbar)**2-(d[a]-dbar)**2)+((d[b]+1-dbar)**2-(d[b]-dbar)**2)
            dS=dT-beta_l*dQ
            if dS>=0 or rng.random()<math.exp(dS/TAU):
                adj[a].add(b); adj[b].add(a); d[u]-=1; d[v]-=1; d[a]+=1; d[b]+=1; el[io]=(a,b); acc+=1
            else:
                adj[u].add(v); adj[v].add(u)
    return adj, d, acc/max(tot,1)

# ─────────── dynamique L2 (tilt linéaire, coefficients dérivés) ───────────
def relax_L2(adj, d, cand, a_c, b_c, N, seed, sw):
    """S_L2 = a_c·T − b_c·X ; ΔT par voisins communs, ΔX = dQ0 (X = Σd²)."""
    rng=np.random.default_rng(seed); el=[(i,j) for i in range(N) for j in adj[i] if j>i]; acc=0; tot=0
    for _ in range(sw):
        for _ in range(3*N):
            io=rng.integers(len(el)); u,v=el[io]; ii=rng.integers(len(cand)); a,b=cand[ii]
            if b in adj[a] or v not in adj[u] or len({u,v,a,b})<4 or d[u]<=2 or d[v]<=2: continue
            tot+=1
            dT=-len(adj[u]&adj[v])
            adj[u].discard(v); adj[v].discard(u)
            dT+=len(adj[a]&adj[b])
            dX=(-2*d[u]+1)+(-2*d[v]+1)+(2*d[a]+1)+(2*d[b]+1)
            dS=a_c*dT - b_c*dX
            if dS>=0 or rng.random()<math.exp(dS/TAU):
                adj[a].add(b); adj[b].add(a); d[u]-=1; d[v]-=1; d[a]+=1; d[b]+=1; el[io]=(a,b); acc+=1
            else:
                adj[u].add(v); adj[v].add(u)
    return adj, d, acc/max(tot,1)

# ─────────── dynamique GLOBALE (témoin) ───────────
def relax_global(adj, d, cand, beta, N, seed, sw):
    """S_g = log(1+T) − β·CV ; mesure exp((N/τ)S) → te=τ/N."""
    rng=np.random.default_rng(seed); te=TAU/N
    T=0
    for u in adj:
        for v in adj[u]:
            if v>u: T+=len(adj[u]&adj[v])
    T//=3
    X=int((d.astype(np.int64)**2).sum()); E=sum(len(adj[u]) for u in adj)//2; mu=2.0*E/N
    el=[(i,j) for i in range(N) for j in adj[i] if j>i]
    for _ in range(sw):
        for _ in range(3*N):
            io=rng.integers(len(el)); u,v=el[io]; ii=rng.integers(len(cand)); a,b=cand[ii]
            if b in adj[a] or v not in adj[u] or len({u,v,a,b})<4 or d[u]<=2 or d[v]<=2: continue
            t_rm=len(adj[u]&adj[v]); adj[u].discard(v); adj[v].discard(u)
            t_ad=len(adj[a]&adj[b]); adj[u].add(v); adj[v].add(u)
            dT=t_ad-t_rm
            dX=(-2*d[u]+1)+(-2*d[v]+1)+(2*d[a]+1)+(2*d[b]+1)
            cv0=math.sqrt(max(X/N-mu*mu,0))/mu; cv1=math.sqrt(max((X+dX)/N-mu*mu,0))/mu
            dS=math.log(1+T+dT)-math.log(1+T)-beta*(cv1-cv0)
            if dS>=0 or rng.random()<math.exp(dS/te):
                adj[u].discard(v); adj[v].discard(u); adj[a].add(b); adj[b].add(a)
                d[u]-=1; d[v]-=1; d[a]+=1; d[b]+=1; T+=dT; X+=dX; el[io]=(a,b)
    return adj, d

# ─────────── observables ───────────
def macro(adj, N):
    E=sum(len(adj[u]) for u in adj)//2
    tris=set()
    for u in adj:
        for v in adj[u]:
            if v>u:
                for w in adj[u]&adj[v]:
                    if w>v: tris.add((u,v,w))
    d=degs(adj,N); mu=2.0*E/N
    cv=float(np.sqrt(max((d.astype(float)**2).mean()-mu*mu,0))/mu)
    return len(tris)/N, cv, E

def rtet(adj, pts, L, N, seed):
    tris=set()
    for u in adj:
        for v in adj[u]:
            if v>u:
                for w in adj[u]&adj[v]:
                    if w>v: tris.add((u,v,w))
    e2t=defaultdict(list); tv=np.zeros(N)
    for (u,v,w) in tris:
        for x in adj[u]&adj[v]&adj[w]:
            if x>w:
                for e in combinations((u,v,w,x),2): e2t[tuple(sorted(e))].append((u,v,w,x))
                for z in (u,v,w,x): tv[z]+=1
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
        dl.append(abs(2*math.pi-sum(dih(t,e) for t in e2t[e]))); rho.append(0.5*(tv[e[0]]+tv[e[1]]))
    return float(np.corrcoef(rho,dl)[0,1]), len(ep)

def rp_bands(pts, L, rc, N, K=2):
    x=pts[:,0]; inP=(x>L/2+rc)&(x<L-rc); inM=(x>rc)&(x<L/2-rc)
    cy=np.minimum((pts[:,1]/L*K).astype(int),K-1); cz=np.minimum((pts[:,2]/L*K).astype(int),K-1)
    return inP, inM, cy*K+cz, K

def rp_feats(adj, N, inP, inM, cell, K):
    fP=np.zeros((K*K,2)); fM=np.zeros((K*K,2)); nP=np.zeros(K*K); nM=np.zeros(K*K)
    for i in range(N):
        if inP[i]: nP[cell[i]]+=1
        elif inM[i]: nM[cell[i]]+=1
    for u in adj:
        for v in adj[u]:
            if v>u:
                if inP[u] and inP[v]:
                    cc=len([w for w in adj[u]&adj[v] if inP[w]]); fP[cell[u],0]+=.5; fP[cell[v],0]+=.5; fP[cell[u],1]+=cc*.5; fP[cell[v],1]+=cc*.5
                elif inM[u] and inM[v]:
                    cc=len([w for w in adj[u]&adj[v] if inM[w]]); fM[cell[u],0]+=.5; fM[cell[v],0]+=.5; fM[cell[u],1]+=cc*.5; fM[cell[v],1]+=cc*.5
    fP/=np.maximum(nP[:,None],1); fM/=np.maximum(nM[:,None],1)
    return np.concatenate([[1.],fP.ravel()]), np.concatenate([[1.],fM.ravel()])

def safe_mineig(P, Q):
    keep=(P.std(0)>1e-9)&(Q.std(0)>1e-9); keep[0]=True
    P=P[:,keep]; Q=Q[:,keep]; G=(P.T@Q)/len(P); Gs=0.5*(G+G.T); n=Gs.shape[0]
    for reg in (1e-8,1e-6,1e-4,1e-2):
        try:
            return float(np.linalg.eigvalsh(Gs+reg*np.eye(n))[0]-reg)
        except np.linalg.LinAlgError:
            continue
    return float(np.min(np.diag(Gs)-(np.abs(Gs).sum(1)-np.abs(np.diag(Gs)))))

def rp_run(get_snap, pts, L, rc, N, M=60, block=10):
    inP, inM, cell, K = rp_bands(pts, L, rc, N)
    Ps=[]; Qs=[]
    for m in range(M):
        adj=get_snap(m); a_,b_=rp_feats(adj,N,inP,inM,cell,K); Ps.append(a_); Qs.append(b_)
    P=np.array(Ps); Q=np.array(Qs)
    me=safe_mineig(P,Q)
    nb=max(5,len(P)//block); rb=np.random.default_rng(11); boots=[]
    for _ in range(120):
        bi=rb.integers(0,nb,nb); idx=np.concatenate([np.arange(b*block,min((b+1)*block,len(P))) for b in bi])
        boots.append(safe_mineig(P[idx],Q[idx]))
    return me, 3*float(np.std(boots))

# ═══════════════════ MAIN ═══════════════════
if __name__=="__main__":
    print(GRID); t0=time.time()
    R={"meta":{"tau":TAU}}
    def save():
        with open(OUT,"w") as f: json.dump(R,f)

    d3=ds_measure(exact_cube(17),1); CAL=3.0/d3 if d3==d3 else 1.0
    R["instrument"]={"cube3D":d3,"cal":CAL}; print(f"instrument: cube3D={d3:.3f} cal={CAL:.4f}\n",flush=True); save()

    # ---------- W1 : PARETO FIN (régime gravité deg-10) ----------
    print("─── W1 : PARETO FIN α×β_ℓ (deg-10, 2 graines/pt) — le POINT JOINT ───")
    R["W1"]=[]
    N=6000; E=5*N
    for alpha in (0.64,0.68,0.72,0.76,0.80):
        for beta_l in (0.15,0.20,0.25):
            for seed in (9000,9001):
                try:
                    pts,cand,L,rc,_=build(N,seed)
                    adj=init_adj(cand,E,seed); d=degs(adj,N)
                    adj,d,acc=relax_L1(adj,d,cand,alpha,beta_l,10.0,N,seed+1,45)
                    ds=ds_measure(spA(adj,N),seed,CAL)
                    rt,nep=rtet(adj,pts,L,N,seed+2)
                    tbar,cv,_=macro(adj,N)
                    rec={"alpha":alpha,"beta_l":beta_l,"seed":seed,"d_s":ds,"r_tet":rt,"F/V":tbar,"CV":cv,"acc":acc}
                    R["W1"].append(rec); save()
                    joint='★JOINT' if (2.90<=ds<=3.20 and rt==rt and rt>0.50) else ''
                    print(f"  α={alpha:.2f} β={beta_l:.2f} s={seed}: d_s={ds:.3f} r_tet={rt:+.3f} F/V={tbar:.3f} CV={cv:.3f} {joint}  ({(time.time()-t0)/60:.0f}m)",flush=True)
                except Exception as ex:
                    print(f"  α={alpha} β={beta_l} s={seed} ÉCHEC: {ex}",flush=True)

    # ---------- W2 : HYSTÉRÉSIS EN α ----------
    print("\n─── W2 : HYSTÉRÉSIS EN α (l'axe de la transition locale) ───")
    N=6000; E=int(3.3*N)
    alphas=[0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85]
    try:
        pts,cand,L,rc,_=build(N,9100)
        adj=init_adj(cand,E,9100); d=degs(adj,N)
        up=[]
        for a in alphas:
            adj,d,_=relax_L1(adj,d,cand,a,BETAL_C2,DBAR_DIMS,N,9101,6)
            tb,cv,_=macro(adj,N); up.append(tb)
        dn=[]
        for a in alphas[::-1]:
            adj,d,_=relax_L1(adj,d,cand,a,BETAL_C2,DBAR_DIMS,N,9102,6)
            tb,cv,_=macro(adj,N); dn.append(tb)
        dn=dn[::-1]
        aire=float(np.sum((np.array(up)-np.array(dn))[:-1]*np.diff(alphas)))
        R["W2"]={"alphas":alphas,"FV_up":up,"FV_dn":dn,"aire":aire}; save()
        print(f"  F/V aller  : {[f'{x:.3f}' for x in up]}")
        print(f"  F/V retour : {[f'{x:.3f}' for x in dn]}")
        print(f"  aire = {aire:+.4f}  [seuil 0,01]  {'✓ PREMIER ORDRE + MÉMOIRE sous localité' if abs(aire)>0.01 else 'non détectée'}  ({(time.time()-t0)/60:.0f}m)",flush=True)
    except Exception as ex:
        print(f"  W2 ÉCHEC: {ex}",flush=True)

    # ---------- W3 : CANDIDATE L2 (coefficients dérivés) ----------
    print("\n─── W3 : L2 tilt linéaire (a=1/(τ·t̄), b=β/(2τ·CV·μ²) — zéro ajusté) ───")
    R["W3"]=[]
    N=5000; E=int(3.3*N)
    # coefficients dérivés du canonique dims : t̄≈0,346 (T=1728@N=5000), CV≈0,87, μ=6,6, β=0,3
    a_c=1.0/(TAU*0.346); b_c=0.30/(2*TAU*0.87*6.6**2)
    print(f"  coefficients dérivés : a={a_c:.3f}, b={b_c:.5f}")
    for seed in (9200,9201,9202):
        try:
            pts,cand,L,rc,_=build(N,seed)
            adj=init_adj(cand,E,seed); d=degs(adj,N)
            adj,d,acc=relax_L2(adj,d,cand,a_c,b_c,N,seed+1,70)
            ds=ds_measure(spA(adj,N),seed,CAL)
            tb,cv,_=macro(adj,N)
            rec={"seed":seed,"d_s":ds,"F/V":tb,"CV":cv,"acc":acc}
            R["W3"].append(rec); save()
            print(f"  s={seed}: d_s={ds:.3f}  F/V={tb:.3f} CV={cv:.3f}  acc={acc:.2f}  ({(time.time()-t0)/60:.0f}m)",flush=True)
        except Exception as ex:
            print(f"  s={seed} ÉCHEC: {ex}",flush=True)
    # RP de L2 (2 graines, M=60)
    for seed in (9200,9201):
        try:
            pts,cand,L,rc,_=build(N,seed)
            adj=init_adj(cand,E,seed); d=degs(adj,N)
            adj,d,_=relax_L2(adj,d,cand,a_c,b_c,N,seed+1,70)
            st={"adj":adj,"d":d}
            def snap(m, s=st, cc=cand, nn=N, sd=seed):
                s["adj"],s["d"],_=relax_L2(s["adj"],s["d"],cc,a_c,b_c,nn,sd+300+m,1)
                return s["adj"]
            me,tol=rp_run(snap,pts,L,rc,N,M=60)
            R["W3"].append({"seed":seed,"rp_mineig":me,"rp_tol":tol}); save()
            print(f"  RP L2 s={seed}: min-eig={me:+.4f} (tol {tol:.4f})  {'✓ plancher' if abs(me)<=2*tol else '✗'}  ({(time.time()-t0)/60:.0f}m)",flush=True)
        except Exception as ex:
            print(f"  RP L2 s={seed} ÉCHEC: {ex}",flush=True)

    # ---------- W4 : TÉMOIN GLOBAL INTÉGRÉ ----------
    print("\n─── W4 : TÉMOIN GLOBAL (doit violer fortement — boucle la clause) ───")
    N=5000; E=int(3.3*N)
    try:
        pts,cand,L,rc,_=build(N,5000)
        adj=init_adj(cand,E,5000); d=degs(adj,N)
        adj,d=relax_global(adj,d,cand,0.30,N,5001,40)
        st={"adj":adj,"d":d}
        def snapg(m, s=st, cc=cand, nn=N):
            s["adj"],s["d"]=relax_global(s["adj"],s["d"],cc,0.30,nn,6000+m,1)
            return s["adj"]
        me,tol=rp_run(snapg,pts,L,rc,N,M=40)
        R["W4"]={"global_mineig":me,"tol":tol}; save()
        print(f"  GLOBAL β=0,3 : min-eig={me:+.3f}  [grille : |me|≥0,4]  {'✓✓ instrument non-aveugle certifié' if abs(me)>=0.4 else '⚠ à réauditer'}  ({(time.time()-t0)/60:.0f}m)",flush=True)
    except Exception as ex:
        print(f"  W4 ÉCHEC: {ex}",flush=True)

    # ---------- W5 : TOPOLOGIE SOUS LOCALE ----------
    print("\n─── W5 : b₁, χ, ratios au point C2 ───")
    N=6000; E=int(3.3*N)
    try:
        pts,cand,L,rc,_=build(N,9300)
        adj=init_adj(cand,E,9300); d=degs(adj,N)
        adj,d,_=relax_L1(adj,d,cand,ALPHA_C2,BETAL_C2,DBAR_DIMS,N,9301,60)
        Ecnt=sum(len(adj[u]) for u in adj)//2
        seen=np.zeros(N,dtype=bool); comp=0
        for s0 in range(N):
            if not seen[s0] and adj.get(s0):
                comp+=1; stack=[s0]; seen[s0]=True
                while stack:
                    u=stack.pop()
                    for v in adj[u]:
                        if not seen[v]: seen[v]=True; stack.append(v)
        tris=set()
        for u in adj:
            for v in adj[u]:
                if v>u:
                    for w in adj[u]&adj[v]:
                        if w>v: tris.add((u,v,w))
        F=len(tris); T=0
        for (u,v,w) in tris:
            for x in adj[u]&adj[v]&adj[w]:
                if x>w: T+=1
        b1=Ecnt-N+comp; chi=N-Ecnt+F-T
        R["W5"]={"b1_over_V":b1/N,"chi_over_V":chi/N,"F/V":F/N,"T/V":T/N,"comp":comp}; save()
        print(f"  b₁/V={b1/N:.3f}  χ/V={chi/N:+.3f}  F/V={F/N:.3f}  T/V={T/N:.3f}  "
              f"{'✓ socle e^(iω) présent' if b1/N>1 else 'topologie pauvre'}  ({(time.time()-t0)/60:.0f}m)",flush=True)
    except Exception as ex:
        print(f"  W5 ÉCHEC: {ex}",flush=True)

    # ═══ synthèse ═══
    print(f"\n════════ SYNTHÈSE CYCLE 2 ({(time.time()-t0)/60:.0f} min) ════════")
    w1=[r for r in R.get("W1",[]) if r.get("r_tet")==r.get("r_tet")]
    joints=[r for r in w1 if 2.90<=r["d_s"]<=3.20 and r["r_tet"]>0.50]
    if joints:
        print(f"  ★★★ POINT JOINT TROUVÉ ({len(joints)} occurrence(s)) :")
        for r in joints[:4]:
            print(f"     α={r['alpha']} β_ℓ={r['beta_l']} s={r['seed']}: d_s={r['d_s']:.3f}, r_tet={r['r_tet']:+.3f}")
    elif w1:
        band=[r for r in w1 if 2.90<=r["d_s"]<=3.20]
        if band:
            best=max(band,key=lambda r:r["r_tet"])
            print(f"  point joint non atteint ; meilleur en bande : α={best['alpha']} β={best['beta_l']} r_tet={best['r_tet']:+.3f}")
    print(f"  Résultats complets : {OUT}")
    save()
