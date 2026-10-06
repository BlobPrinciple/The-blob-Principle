#!/usr/bin/env python3
# ============================================================================
# BLOB — TEST DE RÉFUTATION DE (D), CIBLÉ (le SEUL test décisif restant)
# Zéro dépendance sauf numpy. But unique : Δ(R) = ⟨n△⟩(bord+) − ⟨n△⟩(bord−)
# au centre, pour R croissant, avec R PETIT devant la boîte (condition jamais
# respectée avant). Verdict : Δ(R)→0 avec bruit = indice unicité (D) ;
# plateau > 0 = candidat contre-exemple.
#
# FOURCHETTE CIBLÉE : N=150000 (assez grand pour L≈9, donc R jusqu'à 12 reste
# < rayon de boîte ≈ 45 en unités géodésiques) ; R ∈ {4,6,8,10,12} ; 5 graines.
# Pourquoi PAS le branchement : b≈24 mesuré, seuil FP=1.66, verdict connu
# (voie fermée) — inutile de le re-mesurer. On teste ce qui tranche vraiment.
# ============================================================================
import numpy as np, math
from collections import deque, defaultdict

N        = 150_000
DENSITY  = 200.0; KAPPA = 10.0; RCUT = 1.6
BETA     = 0.30; TAU = 0.5; E_FACTOR = 5
SWEEPS_EQ   = 15          # équilibrage global initial
SWEEPS_BC   = 25          # relaxation intérieure sous condition de bord
MU_BORD     = 2.0         # intensité du champ de bord antagoniste
RADII       = [4,6,8,10,12]
SEEDS       = [11,12,13,14,15]

def build(N, seed):
    rng=np.random.default_rng(seed); L=(N/DENSITY)**(1/3)
    pts=rng.uniform(0,L,size=(N,3))
    r_base=(3*KAPPA/(4*math.pi*DENSITY))**(1/3); rc=RCUT*r_base
    cell=rc; ncell=max(1,int(L/cell)); grid=defaultdict(list)
    for i,p in enumerate(pts): grid[tuple((p//cell).astype(int)%ncell)].append(i)
    cand=[]
    for i,p in enumerate(pts):
        ci=(p//cell).astype(int)
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                for dz in(-1,0,1):
                    for j in grid[tuple(((ci+[dx,dy,dz])%ncell))]:
                        if j>i:
                            d=pts[i]-pts[j]; d-=L*np.round(d/L)
                            if (d*d).sum()<rc*rc: cand.append((i,j))
    cand=list(set(cand)); E0=min(E_FACTOR*N,len(cand))
    idx=rng.choice(len(cand),size=E0,replace=False)
    adj=[set() for _ in range(N)]
    for k in idx: a,b=cand[k]; adj[a].add(b); adj[b].add(a)
    return pts,adj,cand,L

def count_tri(adj,N):
    t=0
    for u in range(N):
        for v in adj[u]:
            if v>u: t+=len(adj[u]&adj[v])
    return t//3

def still_conn(adj,u,v):
    if v not in adj[u]: return True
    seen={u}; dq=deque([u])
    while dq:
        x=dq.popleft()
        for y in adj[x]:
            if y==v and x==u: continue
            if y not in seen: seen.add(y); dq.append(y)
    return v in seen

def equilibrate(adj,cand,N,sweeps,seed):
    rng=np.random.default_rng(seed+7); pa=np.array(cand,dtype=np.int64)
    npool=len(pa); te=TAU/N; el=[(i,j) for i in range(N) for j in adj[i] if j>i]
    nt=count_tri(adj,N); deg=np.array([len(a) for a in adj]); S2=int((deg*deg).sum())
    dbar=deg.sum()/N
    def cv(s):
        v=s/N-dbar*dbar; return math.sqrt(v if v>0 else 0.)/dbar
    for _ in range(sweeps*N):
        io=int(rng.integers(len(el))); u,v=el[io]
        ii=int(rng.integers(npool)); a,b=int(pa[ii,0]),int(pa[ii,1])
        if b in adj[a]: continue
        if len(adj[u])<=2 or len(adj[v])<=2:
            if not still_conn(adj,u,v): continue
        tl=len(adj[u]&adj[v]); adj[u].discard(v);adj[v].discard(u);adj[a].add(b);adj[b].add(a)
        dtri=len(adj[a]&adj[b])-tl
        dS2=(-2*deg[u]+1)+(-2*deg[v]+1)+(2*deg[a]+1)+(2*deg[b]+1)
        dS=(math.log(1+nt+dtri)-math.log(1+nt))-BETA*(cv(S2+dS2)-cv(S2))
        if dS>=0 or rng.random()<math.exp(dS/te):
            nt+=dtri;el[io]=(a,b);S2+=dS2;deg[u]-=1;deg[v]-=1;deg[a]+=1;deg[b]+=1
        else: adj[u].add(v);adj[v].add(u);adj[a].discard(b);adj[b].discard(a)
    return adj,nt

def relax_bc(adj,cand,pts,N,center,R,sign,seed,box_radius):
    # BFS distances depuis le centre
    dist={center:0}; dq=deque([center])
    while dq:
        u=dq.popleft()
        for v in adj[u]:
            if v not in dist: dist[v]=dist[u]+1; dq.append(v)
    boundary=set(v for v in range(N) if R<dist.get(v,10**9)<=R+2)
    h=MU_BORD*sign
    rng=np.random.default_rng(seed+7); pa=np.array(cand,dtype=np.int64)
    npool=len(pa); te=TAU/N; nt=count_tri(adj,N)
    deg=np.array([len(a) for a in adj]); S2=int((deg*deg).sum()); dbar=deg.sum()/N
    def cv(s):
        v=s/N-dbar*dbar; return math.sqrt(v if v>0 else 0.)/dbar
    for _ in range(SWEEPS_BC*N):
        io=int(rng.integers(npool)); a,b=int(pa[io,0]),int(pa[io,1])
        touch = (a in boundary or b in boundary)
        if b in adj[a]:
            if len(adj[a])<=2 or len(adj[b])<=2: continue
            tl=len(adj[a]&adj[b]); adj[a].discard(b);adj[b].discard(a)
            dtri=-tl; dS2=(-2*deg[a]+1)+(-2*deg[b]+1)
            dS=(math.log(1+nt+dtri)-math.log(1+nt))-BETA*(cv(S2+dS2)-cv(S2)) - (h*dtri if touch else 0.)
            if dS>=0 or rng.random()<math.exp(dS/te):
                nt+=dtri;S2+=dS2;deg[a]-=1;deg[b]-=1
            else: adj[a].add(b);adj[b].add(a)
        else:
            tl=len(adj[a]&adj[b]); adj[a].add(b);adj[b].add(a)
            dtri=tl; dS2=(2*deg[a]+1)+(2*deg[b]+1)
            dS=(math.log(1+nt+dtri)-math.log(1+nt))-BETA*(cv(S2+dS2)-cv(S2)) + (h*dtri if touch else 0.)
            if dS>=0 or rng.random()<math.exp(dS/te):
                nt+=dtri;S2+=dS2;deg[a]+=1;deg[b]+=1
            else: adj[a].discard(b);adj[b].discard(a)
    core=[v for v in range(N) if dist.get(v,10**9)<=2]; loc=0
    for v in core:
        for u in adj[v]:
            if u>v: loc+=len(adj[v]&adj[u])
    # rayon de boite en unites geodesiques (pour verifier R << box)
    maxd=max(dist.values()) if dist else 0
    return loc/max(len(core),1), maxd

if __name__=="__main__":
    print(f"=== RÉFUTATION CIBLÉE de (D) — N={N}, R∈{RADII}, {len(SEEDS)} graines ===")
    print("    (le branchement n'est PAS re-testé : b≈24 >> seuil FP rigoureux 1.66 ⟹ voie polymères")
    print("     déjà fermée. Ce test-ci est le SEUL décisif restant.)\n")
    results={}
    for R in RADII:
        diffs=[]; boxes=[]
        for sd in SEEDS:
            pts,adj0,cand,L=build(N,sd)
            adj0,nt=equilibrate(adj0,cand,N,SWEEPS_EQ,sd)
            c=int(np.argmin(((pts-pts.mean(0))**2).sum(1)))
            ap,mdp=relax_bc([set(a) for a in adj0],cand,pts,N,c,R,+1,sd,L)
            am,mdm=relax_bc([set(a) for a in adj0],cand,pts,N,c,R,-1,sd,L)
            diffs.append(ap-am); boxes.append(mdp)
        d=np.array(diffs); box=np.mean(boxes)
        results[R]=(d.mean(),d.std())
        flag="⚠ R proche du bord de boîte" if R>0.6*box else "✓ R << boîte"
        print(f"  R={R:2d} : Δ={d.mean():+.3f} ± {d.std():.3f}  (rayon boîte géod.≈{box:.0f}, {flag})  détail={np.round(d,2)}")
    print("\n=== VERDICT (grille pré-enregistrée) ===")
    Rs=sorted(results); vals=[results[R][0] for R in Rs]
    trend="décroissant vers 0" if abs(vals[-1])<abs(vals[0]) and abs(vals[-1])<0.5 else ("plateau non nul" if min(abs(v) for v in vals[-2:])>0.5 else "non monotone")
    print(f"  tendance de |Δ(R)| : {trend}")
    if trend=="décroissant vers 0":
        print("  ⟹ INDICE d'unicité (D plausible) : le bord antagoniste ne se propage pas au centre.")
        print("     (INDICE numérique, PAS une preuve — garde IA-1. Renforce la voie S1.)")
    elif trend=="plateau non nul":
        print("  ⟹ CANDIDAT CONTRE-EXEMPLE à (D) : deux phases selon le bord. Session de confirmation requise.")
        print("     Si confirmé : étage 4–5 de la Cascade recule de [T*] vers [M-effectif].")
    else:
        print("  ⟹ NON CONCLUANT : augmenter graines ou vérifier R << boîte. Aucune conclusion.")
    print("\n  Rappel gravé : un Δ EXACTEMENT nul (barres nulles) = artefact de taille (R sature la boîte),")
    print("  PAS un signal d'unicité. Ne lire un indice d'unicité QUE si Δ→0 AVEC bruit résiduel.")
