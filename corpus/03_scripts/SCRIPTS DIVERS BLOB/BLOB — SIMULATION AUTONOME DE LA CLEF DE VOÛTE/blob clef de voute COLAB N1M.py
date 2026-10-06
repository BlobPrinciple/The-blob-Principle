#!/usr/bin/env python3
# ============================================================================
# BLOB — SIMULATION AUTONOME DE LA CLEF DE VOÛTE (contraction D)
# Zéro dépendance externe (numpy seul). Tourne tel quel : python3 ce_fichier.py
# Sur Colab : augmenter N à 100000+ pour que les tests soient concluants.
# Contient : (1) construction du substrat, (2) équilibrage au point de travail,
# (3) TEST DE RÉFUTATION (bord antagoniste par CHAMP, pas gel), (4) MESURE DU
# TAUX DE BRANCHEMENT des triangles présents (jalon S2-v3, seuil 4,5).
# ============================================================================
import numpy as np, math
from collections import deque, defaultdict

N        = 1_000_000   # réglé pour Colab (RAM ≥ 12 Go requise). Voir NOTES en bas.
DENSITY  = 200.0
KAPPA    = 10.0
RCUT     = 1.6
BETA     = 0.30
TAU      = 0.5
E_FACTOR = 5           # E0 = 5N
SEEDS    = [11]   # 1 graine pour le 1er run 1M ; ajouter 12,13 ensuite

def build(N, seed):
    rng = np.random.default_rng(seed)
    L = (N/DENSITY)**(1/3)
    pts = rng.uniform(0, L, size=(N,3))
    r_base = (3*KAPPA/(4*math.pi*DENSITY))**(1/3)
    rc = RCUT*r_base
    # voisins par grille
    cell = rc; ncell = max(1,int(L/cell))
    grid = defaultdict(list)
    def cidx(p): return tuple((p//cell).astype(int)%ncell)
    for i,p in enumerate(pts): grid[cidx(p)].append(i)
    cand=[]
    for i,p in enumerate(pts):
        ci=(p//cell).astype(int)
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                for dz in(-1,0,1):
                    c=tuple(((ci+[dx,dy,dz])%ncell))
                    for j in grid[c]:
                        if j>i:
                            d=pts[i]-pts[j]; d-=L*np.round(d/L)
                            if (d*d).sum()<rc*rc: cand.append((i,j))
    cand=list(set(cand))
    # substrat dilué : E0 = 5N arêtes tirées
    E0=min(E_FACTOR*N, len(cand))
    idx=rng.choice(len(cand), size=E0, replace=False)
    adj=[set() for _ in range(N)]
    for k in idx:
        a,b=cand[k]; adj[a].add(b); adj[b].add(a)
    return pts, adj, cand, L

def count_tri(adj,N):
    t=0
    for u in range(N):
        for v in adj[u]:
            if v>u: t+=len(adj[u]&adj[v])
    return t//3

def still_conn(adj,u,v,N):
    if v not in adj[u]: return True
    seen={u}; dq=deque([u])
    while dq:
        x=dq.popleft()
        for y in adj[x]:
            if y==v and x==u: continue
            if y not in seen: seen.add(y); dq.append(y)
    return v in seen

def equilibrate(adj, cand, N, sweeps, tau, seed):
    rng=np.random.default_rng(seed+7+int(tau*1000))
    pa=np.array(cand,dtype=np.int64); npool=len(pa); te=tau/N
    el=[(i,j) for i in range(N) for j in adj[i] if j>i]
    nt=count_tri(adj,N)
    deg=np.array([len(a) for a in adj],dtype=np.int64); S2=int((deg*deg).sum())
    dbar=deg.sum()/N
    def cv(s):
        v=s/N-dbar*dbar; return math.sqrt(v if v>0 else 0.0)/dbar
    for _ in range(sweeps*N):
        io=int(rng.integers(len(el))); u,v=el[io]
        ii=int(rng.integers(npool)); a,b=int(pa[ii,0]),int(pa[ii,1])
        if b in adj[a]: continue
        if len(adj[u])<=2 or len(adj[v])<=2:
            if not still_conn(adj,u,v,N): continue
        tl=len(adj[u]&adj[v])
        adj[u].discard(v); adj[v].discard(u); adj[a].add(b); adj[b].add(a)
        dtri=len(adj[a]&adj[b])-tl
        dS2=(-2*deg[u]+1)+(-2*deg[v]+1)+(2*deg[a]+1)+(2*deg[b]+1)
        dS=(math.log(1+nt+dtri)-math.log(1+nt))-BETA*(cv(S2+dS2)-cv(S2))
        if dS>=0 or rng.random()<math.exp(dS/te):
            nt+=dtri; el[io]=(a,b); S2+=dS2; deg[u]-=1;deg[v]-=1;deg[a]+=1;deg[b]+=1
        else:
            adj[u].add(v);adj[v].add(u);adj[a].discard(b);adj[b].discard(a)
    return adj, nt

def branching_rate(adj, N):
    # JALON S2-v3 : taux de branchement de l'arbre des TRIANGLES présents partageant une arête.
    # On construit le graphe des triangles (noeud=triangle présent ; lien=partage d'arête)
    # et on mesure le degré moyen = branchement effectif. Seuil FP : < 4.5 ⟹ convergence.
    tris=[]
    edge2tri=defaultdict(list)
    for u in range(N):
        for v in adj[u]:
            if v>u:
                common=adj[u]&adj[v]
                for w in common:
                    if w>v:
                        t=(u,v,w); tris.append(t)
    tset=set(tris)
    for (u,v,w) in tris:
        for e in [(u,v),(u,w),(v,w)]:
            edge2tri[e].append((u,v,w))
    if not tris: return float('nan'), 0
    degs=[]
    for t in tris:
        u,v,w=t; nb=set()
        for e in [(u,v),(u,w),(v,w)]:
            for t2 in edge2tri[e]:
                if t2!=t: nb.add(t2)
        degs.append(len(nb))
    return float(np.mean(degs)), len(tris)

def refutation_field(adj, cand, pts, N, center, R_geo, mu_bord, seed, sweeps=20):
    # bord antagoniste par CHAMP (mu_bord>0 favorise triangles au bord ; <0 les defavorise)
    # sans GELER : on ajoute mu_bord a l'acceptation pour les aretes touchant la couronne.
    dist={center:0}; dq=deque([center])
    while dq:
        u=dq.popleft()
        for v in adj[u]:
            if v not in dist: dist[v]=dist[u]+1; dq.append(v)
    boundary=set(v for v in range(N) if R_geo<dist.get(v,999)<=R_geo+2)
    rng=np.random.default_rng(seed+7); pa=np.array(cand,dtype=np.int64); npool=len(pa)
    te=TAU/N; nt=count_tri(adj,N)
    deg=np.array([len(a) for a in adj],dtype=np.int64); S2=int((deg*deg).sum()); dbar=deg.sum()/N
    def cv(s):
        v=s/N-dbar*dbar; return math.sqrt(v if v>0 else 0.0)/dbar
    for _ in range(sweeps*N):
        io=int(rng.integers(npool)); a,b=int(pa[io,0]),int(pa[io,1])
        h = mu_bord if (a in boundary or b in boundary) else 0.0
        if b in adj[a]:
            if len(adj[a])<=2 or len(adj[b])<=2: continue
            tl=len(adj[a]&adj[b]); adj[a].discard(b); adj[b].discard(a)
            dtri=-tl; dS2=(-2*deg[a]+1)+(-2*deg[b]+1)
            dS=(math.log(1+nt+dtri)-math.log(1+nt))-BETA*(cv(S2+dS2)-cv(S2)) - h*dtri
            if dS>=0 or rng.random()<math.exp(dS/te):
                nt+=dtri;S2+=dS2;deg[a]-=1;deg[b]-=1
            else: adj[a].add(b);adj[b].add(a)
        else:
            tl=len(adj[a]&adj[b]); adj[a].add(b); adj[b].add(a)
            dtri=tl; dS2=(2*deg[a]+1)+(2*deg[b]+1)
            dS=(math.log(1+nt+dtri)-math.log(1+nt))-BETA*(cv(S2+dS2)-cv(S2)) + h*dtri
            if dS>=0 or rng.random()<math.exp(dS/te):
                nt+=dtri;S2+=dS2;deg[a]+=1;deg[b]+=1
            else: adj[a].discard(b);adj[b].discard(a)
    core=[v for v in range(N) if dist.get(v,999)<=2]; loc=0
    for v in core:
        for u in adj[v]:
            if u>v: loc+=len(adj[v]&adj[u])
    return loc/max(len(core),1)

if __name__=="__main__":
    print(f"=== BLOB clef de voûte — N={N} (↑100000 sur Colab) ===\n")
    print("--- (1) JALON S2-v3 : taux de branchement des triangles présents (seuil FP=4.5) ---")
    rates=[]
    for sd in SEEDS:
        pts,adj,cand,L=build(N,sd)
        adj,nt=equilibrate(adj,cand,N,15,0.5,sd)
        adj,nt=equilibrate(adj,cand,N,18,0.10,sd)
        r,ntri=branching_rate(adj,N)
        rates.append(r)
        print(f"  graine {sd}: t̄={nt/N:.2f}, #triangles={ntri}, BRANCHEMENT MOYEN={r:.2f}  {'< 4.5 ✓ (FP convergerait)' if r<4.5 else '≥ 4.5 ✗ (FP diverge)'}")
    print(f"  → branchement moyen sur graines : {np.nanmean(rates):.2f}")
    print(f"  VERDICT S2-v3 : {'CONVERGENCE FP plausible → piste vers preuve de (D)' if np.nanmean(rates)<4.5 else 'FP diverge → Pirogov-Sinai requis'}\n")
    RUN_REFUTATION = False   # passer à True pour le test de bord (très lourd à 1M ; lancer séparément)
    if not RUN_REFUTATION:
        print("--- (2) TEST DE RÉFUTATION : désactivé par défaut à 1M (RUN_REFUTATION=True pour l'activer) ---")
        print("    (le jalon (1) est le résultat clé ; le test de bord se lance en run séparé.)")
        import sys as _s; _s.exit(0)
    print("--- (2) TEST DE RÉFUTATION par champ de bord (grand N requis pour conclure) ---")
    for R in [4,6,8]:
        diffs=[]
        for sd in SEEDS:
            pts,adj,cand,L=build(N,sd)
            adj,nt=equilibrate(adj,cand,N,12,0.5,sd)
            c=int(np.argmin(((pts-pts.mean(0))**2).sum(1)))
            import copy
            ap=refutation_field([set(a) for a in adj],cand,pts,N,c,R,+2.0,sd)
            am=refutation_field([set(a) for a in adj],cand,pts,N,c,R,-2.0,sd)
            diffs.append(ap-am)
        d=np.array(diffs)
        print(f"  R={R}: ⟨n△⟩(bord+)−⟨n△⟩(bord−) au centre = {d.mean():+.3f} ± {d.std():.3f}")
    print("\n  Lecture : écart→0 quand R↑ = indice d'unicité (D) ; plateau>0 = candidat contre-exemple.")
    print("  (Indice numérique, jamais une preuve. À N=2000 non concluant ; relancer N≥10^5 sur Colab.)")


# ============================================================================
# NOTES COLAB — LANCEMENT À N = 1 000 000
# ----------------------------------------------------------------------------
# 1) RAM : la construction du substrat garde toutes les listes d'adjacence en
#    mémoire. À 1M points avec E0=5M arêtes, prévoir ≥ 12 Go (runtime Colab
#    "High-RAM"). Si MemoryError : réduire E_FACTOR ou N par paliers (200k,
#    500k) pour cartographier la faisabilité avant 1M.
# 2) TEMPS : l'équilibrage fait sweeps*N propositions. À 1M avec 15+18 sweeps,
#    c'est ~33M d'itérations Python — comptez plusieurs heures. Pour accélérer :
#    (a) réduire les sweeps (ex. 8+8) pour un premier signal ; (b) porter la
#    boucle interne en numba/@njit (le cœur Metropolis est local et vectorisable
#    par arête) ; (c) découper en checkpoints (sauver adj toutes les N itérations).
# 3) RÉSULTAT CLÉ = le JALON S2-v3 (branchement des triangles présents). À N=2000
#    il valait ~24 (seuil FP=4.5). L'enjeu du run 1M : ce branchement CONVERGE-t-il
#    vers une valeur asymptotique < 4.5 (→ Fernández-Procacci sauve (D)) ou reste-t-il
#    ≥ 4.5 (→ Pirogov-Sinai requis) ? C'est LA question que 1M tranche.
# 4) TEST DE RÉFUTATION : mettre RUN_REFUTATION=True et lancer SÉPARÉMENT. À grand N,
#    R peut monter à 12-15 en restant petit devant la boîte : un écart ⟨n△⟩+ − ⟨n△⟩-
#    qui décroît vers 0 AVEC bruit résiduel = indice d'unicité ; un plateau > 0 =
#    candidat contre-exemple à (D). (Jamais une preuve — garde IA-1.)
# 5) Sauvegarde : ajouter np.savez('blob_1M_state.npz', ...) après équilibrage
#    pour ne pas reperdre 33M d'itérations en cas de déconnexion Colab.
# ============================================================================
