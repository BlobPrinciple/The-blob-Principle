#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#  BLOB — LA SIMULATION TOTALE V286 (Colab). Autonome. 18 juillet 2026.
#  Huit volets = huit questions restées ouvertes ce jour. Grilles PRÉ-ENREGISTRÉES.
#
#  A. n_e → TRANSITION ℤ₂  ★ TEST PHARE (prédiction du tome V285)
#     Papier-crayon : n_e = 3F/E = t̄ (point de travail de l'action) ≈ 1,9 au degré 10,
#     contre 4 sur réseau cubique. La minceur en 2-cellules empêche la percolation des
#     vortex, donc le confinement. PRÉDICTION : en montant le degré (donc n_e), la
#     transition ℤ₂ doit RÉAPPARAÎTRE au-dessus de n_e ≈ 4.
#     GRILLE : pour chaque degré, χ_max(N) mesuré à 2 tailles avec barres jackknife.
#       TRANSITION si χ_max CROÎT (>2σ) ET si le pic est INTÉRIEUR à la fenêtre κ.
#       Si la transition apparaît pour n_e>4 et pas en dessous → LOI STRUCTURELLE.
#       Si elle n'apparaît à aucun n_e → l'absence n'est pas due à la minceur (réfute AY).
#     (Le code de jauge est validé en interne contre ⟨P⟩=tanh(κ) — self-test obligatoire.)
#
#  B. TROUS ARITHMÉTIQUES MULTIPLES  ★ le test le plus falsifiable du corpus
#     r₃(m)=0 ⟺ m=4^a(8b+7) : m = 7, 15, 23, 28, 31...  Le trou à 7 est confirmé (V281).
#     GRILLE : sur 300+ modes, les fenêtres [m−0,4 ; m+0,4] pour m ∈ {7,15,23} doivent
#     avoir une densité ≤ 50% des fenêtres voisines. 3/3 = signature arithmétique
#     profonde ; 1/3 ou 2/3 = rapporté tel quel (l'élargissement croît avec m).
#
#  C. FLOT DE RENORMALISATION ÉTENDU (point 50)
#     R = blocage spatial + restauration du degré (seule version non contaminante).
#     GRILLE : 4 niveaux, 2 tailles. d_s → point fixe ? ⟨C⟩ → valeur universelle ?
#     Le tome V284 a mesuré ⟨C⟩ : 0,198 → 0,335 → 0,333 (viable) et 0,118 → 0,327 (aléa).
#     QUESTION : la valeur limite 0,33 est-elle un VRAI point fixe (stable sur 4 niveaux) ?
#
#  D. EXPOSANTS CRITIQUES — BON OBSERVABLE (répare le volet F4 mal conçu)
#     F4 utilisait Var(degré), quantité INTENSIVE : aucun scaling possible. Le bon
#     observable est χ_T = Var(T)/N (mesuré 1,88 à β=3 → 297 à β=1,55 : il diverge).
#     GRILLE : χ_T,max ~ N^{γ/(νd)} avec R² ≥ 0,9 sur 3+ tailles → premier exposant du Blob.
#
#  E. MITOSE v3 — CROISSANCE À DENSITÉ CONSTANTE (v1 et v2 invalidées)
#     v2 a échoué car croître à volume fixe = densifier (92→200). v3 : la boîte grandit
#     avec N (densité fixe), candidats recalculés par vague, germe équilibré.
#     GRILLE : d_s ∈ [2,7;3,3] à CHAQUE étape ET CV(⟨C⟩) < 8% → la cosmogonie de
#     croissance éternelle est compatible avec la physique mesurée.
#
#  F. CHEEGER — SCALING h·N^{1/3} (la grille initiale était mal posée)
#     Un tore 3D a h ~ surface/volume ~ N^{-1/3}. GRILLE : h·N^{1/3} constant (±20%)
#     sur 3 tailles → pas de goulot, hypothèse d'expansion soutenue pour INF-1.
#
#  G. PERCOLATION DELAUNAY À HAUT DEGRÉ (F1 continué)
#     V281 : fraction retenue ×65 (0,28%→18,4% de deg-10 à deg-30) mais géante <1%.
#     GRILLE : deg 30→42. PERCOLE si géante ≥50% ET span ≥80%. Rapporter aussi la
#     fraction du graphe candidat occupée (tension de saturation : au-delà de 85%,
#     la sélection viable devient triviale et un succès ne prouverait rien).
#
#  H. INSTRUMENT d_s À GRANDE TAILLE (F5 continué)
#     Biais direct +0,37 à +0,42 décroissant. GRILLE : à N=40k, l'écart |d_s − 2d_f/d_w|
#     doit passer sous 0,25 ; extrapolation de la loi d'échelle du biais.
# ═══════════════════════════════════════════════════════════════════════════════
import numpy as np, math, json, time, warnings
warnings.filterwarnings("ignore")
from collections import defaultdict, deque, Counter
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
try:
    from scipy.spatial import Delaunay
    HAS_DEL = True
except Exception:
    HAS_DEL = False

PRESET = "complet"      # "rapide" (~1h30) | "complet" (~5h) | "maximal" (~12h+)
OUT = "blob_total_V286_results.json"
CFG = {
 "rapide":  {"A_N":[2500,6000],      "A_degs":[10,16,22],       "B_N":15000,"B_k":220,
             "C_N":8000,  "C_lev":3, "D_N":[4000,8000,16000],   "E_N0":1200,"E_max":2400,
             "F_N":[2000,4000,8000], "G_N":8000, "G_degs":[30,36,42], "H_N":[8000,20000]},
 "complet": {"A_N":[2500,6000,12000],"A_degs":[10,16,22,28],    "B_N":30000,"B_k":340,
             "C_N":20000, "C_lev":4, "D_N":[6000,12000,24000],  "E_N0":2000,"E_max":6000,
             "F_N":[3000,6000,12000],"G_N":15000,"G_degs":[30,36,42],"H_N":[8000,20000,40000]},
 "maximal": {"A_N":[2500,6000,12000,24000],"A_degs":[10,16,22,28,34],"B_N":50000,"B_k":460,
             "C_N":30000, "C_lev":5, "D_N":[6000,12000,24000,48000],"E_N0":3000,"E_max":12000,
             "F_N":[3000,6000,12000,24000],"G_N":20000,"G_degs":[30,36,42,48],"H_N":[8000,20000,40000,80000]},
}[PRESET]
DENS, KAP, RC, TAU = 200.0, 10.0, 1.6, 0.5
ALPHA, BETAL, DBAR = 0.62, 0.15, 6.6

# ─────────────────────────── briques communes ───────────────────────────
def build(N, seed, dens=DENS):
    rng = np.random.default_rng(seed); L = (N/dens)**(1/3)
    pts = rng.uniform(0, L, size=(N,3)); rc = RC*(3*KAP/(4*math.pi*dens))**(1/3)
    nc = max(1, int(L/rc)); g = defaultdict(list)
    for i,p in enumerate(pts): g[tuple((p//rc).astype(int)%nc)].append(i)
    cand = []
    for i,p in enumerate(pts):
        ci = (p//rc).astype(int)
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                for dz in(-1,0,1):
                    for j in g[tuple((ci+[dx,dy,dz])%nc)]:
                        if j>i:
                            dd = pts[i]-pts[j]; dd -= L*np.round(dd/L)
                            if (dd*dd).sum() < rc*rc: cand.append((i,j))
    return pts, sorted(set(cand)), L, rc, rng

def relax_global(adj, d, cand, beta, N, seed, sw):
    """Action GLOBALE S = log(1+T) − β·CV, mesure exp((N/τ)S). Moteur canonique."""
    rng = np.random.default_rng(seed); te = TAU/N
    T = 0
    for u in adj:
        for v in adj[u]:
            if v>u: T += len(adj[u]&adj[v])
    T //= 3
    X = int((d.astype(np.int64)**2).sum()); E = int(sum(len(adj[u]) for u in adj)//2); mu = 2.0*E/N
    el = [(i,j) for i in adj for j in adj[i] if j>i]
    for _ in range(sw):
        for _ in range(3*N):
            io = rng.integers(len(el)); u,v = el[io]; ii = rng.integers(len(cand)); a,b = cand[ii]
            if b in adj[a] or v not in adj[u] or len({u,v,a,b})<4 or d[u]<=2 or d[v]<=2: continue
            t_rm = len(adj[u]&adj[v]); adj[u].discard(v); adj[v].discard(u)
            t_ad = len(adj[a]&adj[b]); adj[u].add(v); adj[v].add(u)
            dT = t_ad - t_rm
            dX = (-2*d[u]+1)+(-2*d[v]+1)+(2*d[a]+1)+(2*d[b]+1)
            cv0 = math.sqrt(max(X/N-mu*mu,0))/mu; cv1 = math.sqrt(max((X+dX)/N-mu*mu,0))/mu
            dS = math.log(1+T+dT)-math.log(1+T)-beta*(cv1-cv0)
            if dS>=0 or rng.random()<math.exp(dS/te):
                adj[u].discard(v); adj[v].discard(u); adj[a].add(b); adj[b].add(a)
                d[u]-=1; d[v]-=1; d[a]+=1; d[b]+=1; T+=dT; X+=dX; el[io]=(a,b)
    return adj, d, T

def viable(N, seed, beta=3.0, deg=10, sw=28, dens=DENS):
    pts, cand, L, rc, rng = build(N, seed, dens)
    E = min(int(deg*N/2), len(cand))
    adj = defaultdict(set)
    for k in rng.choice(len(cand), size=E, replace=False):
        a,b = cand[k]; adj[a].add(b); adj[b].add(a)
    d = np.zeros(N, dtype=np.int64)
    for u in adj: d[u] = len(adj[u])
    adj, d, T = relax_global(adj, d, cand, beta, N, seed+1, sw)
    return pts, cand, L, rc, adj, d, T

def complexe(adj):
    """→ E, F, tri_e (F,3 ids d'arêtes), Tl (par arête : ids de triangles), eid, edges"""
    eid={}; edges=[]
    for u in adj:
        for v in adj[u]:
            if v>u: eid[(u,v)]=len(edges); edges.append((u,v))
    E=len(edges); tris=[]
    for u in adj:
        for v in adj[u]:
            if v>u:
                for w in adj[u]&adj[v]:
                    if w>v: tris.append((u,v,w))
    F=len(tris)
    tri_e=np.zeros((F,3),dtype=np.int64); T_e=[[] for _ in range(E)]
    for ti,(u,v,w) in enumerate(tris):
        for k,(a,b) in enumerate(((u,v),(v,w),(u,w))):
            e=eid[(a,b)]; tri_e[ti,k]=e; T_e[e].append(ti)
    return E, F, tri_e, [np.array(x,dtype=np.int64) for x in T_e], eid, edges, tris

def spectrum(adj, n, k):
    keys=sorted(adj); idx={u:i for i,u in enumerate(keys)}; m=len(keys); r=[]; c=[]
    for u in adj:
        for v in adj[u]:
            if v in idx: r.append(idx[u]); c.append(idx[v])
    A=sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(m,m))
    dd=np.asarray(A.sum(1)).ravel(); Lp=(sp.diags(dd)-A).tocsr()
    try: return np.sort(eigsh(Lp,k=k,sigma=1e-6,which='LM',return_eigenvectors=False,maxiter=20000))
    except Exception: return None

def ds_heat(adj, n, seed, lo=4, hi=60, tmax=200, cal=0.948):
    keys=sorted(adj); idx={u:i for i,u in enumerate(keys)}; m=len(keys); r=[]; c=[]
    for u in adj:
        for v in adj[u]:
            if v in idx: r.append(idx[u]); c.append(idx[v])
    if len(r)<10: return float('nan')
    A=sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(m,m))
    deg=np.asarray(A.sum(1)).ravel(); Pi=deg/max(deg.sum(),1)
    TG=np.unique(np.round(np.logspace(0,math.log10(tmax),40)).astype(int))
    rg=np.random.default_rng(seed); okn=np.flatnonzero(deg>0)
    src=rg.choice(okn,size=min(8,len(okn)),replace=False)
    X=np.zeros((m,len(src))); X[src,np.arange(len(src))]=1.0
    invd=1.0/np.maximum(deg,1); rec=np.zeros(len(TG)); tj=0
    for t in range(1,TG[-1]+1):
        X=0.5*(X+invd[:,None]*(A@X))
        if tj<len(TG) and t==TG[tj]: rec[tj]=float(np.mean(X[src,np.arange(len(src))]-Pi[src])); tj+=1
    ok=(TG>=lo)&(TG<=hi)&(rec>0)
    return cal*float(-2*np.polyfit(np.log(TG[ok]),np.log(rec[ok]),1)[0]) if ok.sum()>=5 else float('nan')

def clustering(adj, seed, ns=600):
    rg=np.random.default_rng(seed); nodes=[u for u in adj if len(adj[u])>=2]
    if len(nodes)<20: return float('nan')
    samp=rg.choice(nodes,size=min(ns,len(nodes)),replace=False); cs=[]
    for u in samp:
        nb=list(adj[u]); k=len(nb)
        if k<2: continue
        links=sum(1 for i in range(k) for j in range(i+1,k) if nb[j] in adj[nb[i]])
        cs.append(2*links/(k*(k-1)))
    return float(np.mean(cs))

# ── jauge ℤ₂ : mise à jour DIRECTE (aucune indirection d'indice — bug du 18/07 corrigé)
def z2_chi(E, F, tri_e, Tl, kappa, seed, therm=70, meas=260, nb=20):
    rg=np.random.default_rng(seed)
    s=rg.choice([-1,1],size=E).astype(np.int8)
    P=s[tri_e].prod(axis=1).astype(np.int8); Ps=[]
    for sw in range(therm+meas):
        order=rg.permutation(E); u01=rg.random(E)
        for i in range(E):
            e=order[i]; tl=Tl[e]
            if tl.size==0: continue
            dS=-2.0*kappa*int(P[tl].sum())
            if dS>=0 or u01[i]<math.exp(dS):
                s[e]=-s[e]; P[tl]=-P[tl]
        if sw>=therm: Ps.append(float(P.mean()))
    Ps=np.array(Ps); n=len(Ps)//nb; vals=[]
    for b in range(nb):
        keep=np.concatenate([Ps[:b*n],Ps[(b+1)*n:]]); vals.append(F*keep.var())
    vals=np.array(vals)
    err=math.sqrt((nb-1)/nb*((vals-vals.mean())**2).sum())
    return float(Ps.mean()), F*float(Ps.var()), err

def z2_selftest(E,F,tri_e,Tl):
    """OBLIGATOIRE : ⟨P⟩(κ=0,2) doit valoir tanh(0,2)=0,1974 à 0,03 près."""
    m,_,_ = z2_chi(E,F,tri_e,Tl,0.2,999,therm=40,meas=80)
    return m, abs(m-math.tanh(0.2))<=0.03

# ─────────────────────────────── main ───────────────────────────────
if __name__=="__main__":
    print(f"BLOB — SIMULATION TOTALE V286 | PRESET={PRESET}"); print(CFG); print()
    t0=time.time(); R={"meta":{"preset":PRESET,"cfg":CFG}}
    def save():
        with open(OUT,"w") as f: json.dump(R,f)
    def el(): return f"({(time.time()-t0)/60:.0f}min)"

    # ══ A ══ n_e → transition ℤ₂  (TEST PHARE)
    print("─── A : n_e → TRANSITION ℤ₂ (prédiction V285 : réapparition au-dessus de n_e≈4) ───")
    R["A"]=[]; kappas=[0.20,0.35,0.50,0.70,0.95,1.25,1.60]
    for deg in CFG["A_degs"]:
        rowdeg={"deg":deg,"sizes":[]}
        for N in CFG["A_N"]:
            try:
                pts,cand,L,rc,adj,d,T = viable(N,31000,2.5,deg,24)
                E,F,tri_e,Tl,eid,edges,tris = complexe(adj)
                ne = 3*F/E if E else 0
                if N==CFG["A_N"][0]:
                    mt,ok = z2_selftest(E,F,tri_e,Tl)
                    rowdeg["selftest_tanh"]={"mean":mt,"pass":bool(ok)}
                    print(f"  deg={deg}: n_e={ne:.2f} | self-test tanh : {mt:.4f} {'✓' if ok else '✗ MOTEUR INVALIDE'}",flush=True)
                chis=[]
                for kap in kappas:
                    m,chi,err = z2_chi(E,F,tri_e,Tl,kap,4242,therm=60,meas=200)
                    chis.append({"kappa":kap,"P":m,"chi":chi,"err":err})
                imax=int(np.argmax([c["chi"] for c in chis]))
                rowdeg["sizes"].append({"N":N,"F":F,"E":E,"n_e":ne,"chi":chis,
                                        "chi_max":chis[imax]["chi"],"chi_max_err":chis[imax]["err"],
                                        "kappa_max":chis[imax]["kappa"],
                                        "interior":bool(0<imax<len(kappas)-1)})
                print(f"    N={N}: n_e={ne:.2f} χ_max={chis[imax]['chi']:.3f}±{chis[imax]['err']:.3f} à κ={chis[imax]['kappa']} "
                      f"{'(intérieur)' if 0<imax<len(kappas)-1 else '(BORD)'} {el()}",flush=True)
            except Exception as ex:
                print(f"    N={N} deg={deg} ÉCHEC : {ex}")
        # verdict par degré : croissance de χ_max avec N
        ss=rowdeg["sizes"]
        if len(ss)>=2:
            a,ea=ss[0]["chi_max"],ss[0]["chi_max_err"]; b,eb=ss[-1]["chi_max"],ss[-1]["chi_max_err"]
            sig=(b-a)/max(math.sqrt(ea*ea+eb*eb),1e-9)
            rowdeg["growth_sigma"]=sig
            rowdeg["verdict"]=("TRANSITION" if (sig>2 and ss[-1]["interior"]) else
                               ("indice" if sig>1 else "crossover"))
            print(f"  → deg={deg} (n_e={ss[-1]['n_e']:.2f}) : χ_max {a:.3f}→{b:.3f} ({sig:+.1f}σ) ⟹ {rowdeg['verdict']}",flush=True)
        R["A"].append(rowdeg); save()
    tr=[(x["sizes"][-1]["n_e"],x.get("verdict")) for x in R["A"] if x["sizes"]]
    print(f"  ★ SYNTHÈSE A : "+" | ".join(f"n_e={a:.1f}→{b}" for a,b in tr))

    # ══ B ══ trous arithmétiques multiples
    print("\n─── B : TROUS ARITHMÉTIQUES r₃(m)=0 pour m = 7, 15, 23 ───")
    try:
        Nb=CFG["B_N"]
        pts,cand,L,rc,adj,d,T = viable(Nb,21000,3.0,10,26)
        vals=spectrum(adj,Nb,CFG["B_k"])
        if vals is not None:
            rat=vals[1:]/vals[1]
            R["B"]={"N":Nb,"nmodes":len(rat),"ratios":rat.tolist()[:600],"holes":{}}
            def dens(lo,hi): return float(((rat>=lo)&(rat<=hi)).sum()/(hi-lo))
            for m in (7,15,23):
                dh=dens(m-0.40,m+0.40)
                dn=(dens(m-1.40,m-0.60)+dens(m+0.60,m+1.40))/2
                r_=dh/max(dn,1e-9)
                R["B"]["holes"][str(m)]={"dens_hole":dh,"dens_nb":dn,"ratio":r_,"pass":bool(r_<=0.5)}
                print(f"  m={m:>2} (r₃=0) : densité trou={dh:.1f} voisines={dn:.1f} → rapport {r_:.2f} "
                      f"{'★ TROU' if r_<=0.5 else ('◐' if r_<=0.75 else '✗')}  {el()}",flush=True)
            npass=sum(1 for v in R["B"]["holes"].values() if v["pass"])
            print(f"  ★ {npass}/3 trous confirmés")
            save()
    except Exception as ex: print(f"  B ÉCHEC : {ex}")

    # ══ C ══ flot de renormalisation étendu
    print("\n─── C : FLOT DE RENORMALISATION (blocage spatial + degré restauré) ───")
    def spatial_R(adj, coords, L, target=10.0):
        n0=len(coords); k=max(2,int(round((n0/4.0)**(1/3))))
        cell=np.minimum((coords/L*k).astype(int),k-1)
        bid=(cell[:,0]*k+cell[:,1])*k+cell[:,2]
        w=defaultdict(int)
        for u in adj:
            for v in adj[u]:
                if v>u and bid[u]!=bid[v]:
                    a,b=bid[u],bid[v]; w[(min(a,b),max(a,b))]+=1
        used=sorted(set(bid.tolist())); ren={c:i for i,c in enumerate(used)}; n=len(used)
        pairs=sorted(w.items(),key=lambda kv:-kv[1])[:max(1,int(target*n/2))]
        new=defaultdict(set)
        for (a,b),_ in pairs: new[ren[a]].add(ren[b]); new[ren[b]].add(ren[a])
        ctr=np.zeros((n,3))
        for c in used:
            mem=np.flatnonzero(bid==c); ctr[ren[c]]=coords[mem].mean(0)
        return new, ctr, n
    R["C"]={}
    try:
        Nc=CFG["C_N"]
        pts,cand,L,rc,adj,d,T = viable(Nc,95000,3.0,10,28)
        adjr=defaultdict(set)
        rgr=np.random.default_rng(999)
        for k in rgr.choice(len(cand),size=min(5*Nc,len(cand)),replace=False):
            a,b=cand[k]; adjr[a].add(b); adjr[b].add(a)
        for tag,a0 in (("viable",adj),("alea",adjr)):
            cur=defaultdict(set,{u:set(v) for u,v in a0.items()}); co=pts.copy(); flow=[]
            for lev in range(CFG["C_lev"]):
                n=len(co)
                ds=ds_heat(cur,n,10+lev,lo=(4 if n>3000 else 3),hi=(60 if n>3000 else 25),tmax=(200 if n>3000 else 80))
                C=clustering(cur,20+lev)
                flow.append({"lev":lev,"n":n,"d_s":ds,"C":C})
                print(f"  {tag} R^{lev}: n={n:>6} d_s={ds:>5.2f} ⟨C⟩={C:>6.3f}  {el()}",flush=True)
                if lev<CFG["C_lev"]-1 and n>200: cur,co,_=spatial_R(cur,co,L)
                else: break
            R["C"][tag]=flow; save()
        cv=[x["C"] for x in R["C"]["viable"]][1:]; ca=[x["C"] for x in R["C"]["alea"]][1:]
        if cv and ca:
            print(f"  → ⟨C⟩ après R : viable {cv} | aléa {ca} — point fixe commun ? "
                  f"{'OUI' if abs(np.mean(cv)-np.mean(ca))<0.05 else 'NON'}")
    except Exception as ex: print(f"  C ÉCHEC : {ex}")

    # ══ D ══ exposants critiques, BON observable
    print("\n─── D : EXPOSANTS CRITIQUES via χ_T = Var(T)/N (répare F4) ───")
    R["D"]=[]
    for beta in (1.70,1.55,1.45,1.35):
        row={"beta":beta,"pts":[]}
        for N in CFG["D_N"]:
            try:
                pts,cand,L,rc,adj,d,T = viable(N,61000,beta,10,26)
                Ts=[]
                dd=d.copy()
                for m in range(18):
                    adj,dd,Tm = relax_global(adj,dd,cand,beta,N,61500+m,1); Ts.append(Tm)
                Ts=np.array(Ts,dtype=float)
                row["pts"].append({"N":N,"chi_T":float(Ts.var()/N),"T":float(Ts.mean())})
                print(f"  β={beta} N={N:>6}: χ_T=Var(T)/N={Ts.var()/N:>8.2f}  {el()}",flush=True)
            except Exception as ex: print(f"    β={beta} N={N} échec : {ex}")
        if len(row["pts"])>=3:
            xs=np.log([p["N"] for p in row["pts"]]); ys=np.log([max(p["chi_T"],1e-9) for p in row["pts"]])
            p=np.polyfit(xs,ys,1); r2=float(np.corrcoef(xs,ys)[0,1]**2)
            row["expo"]=float(p[0]); row["r2"]=r2
            print(f"  → β={beta} : χ_T ~ N^{p[0]:.3f} (R²={r2:.2f}) {'★ EXPOSANT' if r2>=0.9 else ''}",flush=True)
        R["D"].append(row); save()

    # ══ E ══ mitose v3 (densité constante)
    print("\n─── E : MITOSE v3 — croissance à DENSITÉ CONSTANTE ───")
    R["E"]=[]
    try:
        n=CFG["E_N0"]; step=0
        pts,cand,L,rc,adj,d,T = viable(n,55000,3.0,10,34)
        while True:
            ds=ds_heat(adj,n,55100+step); C=clustering(adj,55200+step)
            R["E"].append({"N":n,"d_s":ds,"C":C,"L":L}); save()
            print(f"  N={n:>6} L={L:.2f} densité={n/L**3:.0f}: d_s={ds:.3f} ⟨C⟩={C:.4f}  {el()}",flush=True)
            if n>=CFG["E_max"]: break
            n2=min(int(n*1.5),CFG["E_max"])
            pts2,cand2,L2,rc2,rng2 = build(n2,55000+step+1)   # boîte plus grande, densité identique
            adj2=defaultdict(set)
            keep=min(int(10*n2/2),len(cand2))
            for k in rng2.choice(len(cand2),size=keep,replace=False):
                a,b=cand2[k]; adj2[a].add(b); adj2[b].add(a)
            d2=np.zeros(n2,dtype=np.int64)
            for u in adj2: d2[u]=len(adj2[u])
            adj2,d2,_=relax_global(adj2,d2,cand2,3.0,n2,55300+step,10)  # relaxation COURTE (croissance)
            adj,d,n,L,cand = adj2,d2,n2,L2,cand2; step+=1
        dss=[x["d_s"] for x in R["E"]]; Cs=[x["C"] for x in R["E"]]
        okd=all(2.7<=x<=3.3 for x in dss if not math.isnan(x)); cv=float(np.std(Cs)/np.mean(Cs))
        print(f"  → d_s {['%.2f'%x for x in dss]} {'✓' if okd else '✗'} | CV(⟨C⟩)={cv*100:.1f}% {'✓' if cv<0.08 else '✗'}")
        print(f"  ★ {'MITOSE-STABLE : la croissance préserve les invariants' if (okd and cv<0.08) else 'non stable — gravé tel quel'}")
    except Exception as ex: print(f"  E ÉCHEC : {ex}")

    # ══ F ══ Cheeger scaling
    print("\n─── F : CHEEGER — scaling h·N^{1/3} ───")
    R["F"]=[]
    for N in CFG["F_N"]:
        try:
            pts,cand,L,rc,adj,d,T = viable(N,61000,3.0,10,26)
            keys=sorted(adj); idx={u:i for i,u in enumerate(keys)}; m=len(keys); r=[]; c=[]
            for u in adj:
                for v in adj[u]: r.append(idx[u]); c.append(idx[v])
            A=sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(m,m))
            dv=np.asarray(A.sum(1)).ravel(); Lp=(sp.diags(dv)-A).tocsr()
            w,vecs=eigsh(Lp,k=3,sigma=1e-6,which='LM',maxiter=15000)
            f=vecs[:,np.argsort(w)[1]]; order=np.argsort(f); vol=dv.sum()
            inS=np.zeros(m,bool); volS=0; cut=0; best=1e9
            nbrs=[set() for _ in range(m)]
            for u in adj:
                for v in adj[u]: nbrs[idx[u]].add(idx[v])
            for i in order[:m-1]:
                inS[i]=True; volS+=dv[i]
                for w2 in nbrs[i]: cut += -1 if inS[w2] else +1
                if 0.02*vol<volS<0.98*vol:
                    phi=cut/max(min(volS,vol-volS),1)
                    if phi<best: best=phi
            R["F"].append({"N":N,"h":best,"hN13":best*N**(1/3)}); save()
            print(f"  N={N:>6}: h={best:.4f}  h·N^(1/3)={best*N**(1/3):.3f}  {el()}",flush=True)
        except Exception as ex: print(f"  N={N} échec F : {ex}")
    if len(R["F"])>=3:
        v=[x["hN13"] for x in R["F"]]
        print(f"  → h·N^(1/3) = {['%.2f'%x for x in v]} — dispersion {np.std(v)/np.mean(v)*100:.0f}% "
              f"{'✓ CONSTANT : pas de goulot' if np.std(v)/np.mean(v)<0.20 else '✗ dérive'}")

    # ══ G ══ percolation Delaunay haut degré
    if HAS_DEL:
        print("\n─── G : PERCOLATION DELAUNAY À HAUT DEGRÉ ───")
        R["G"]=[]
        try:
            Ng=CFG["G_N"]
            ptsg,candg,Lg,rcg,rngg = build(Ng,81000)
            tri=Delaunay(ptsg); simp=tri.simplices
            marg=0.05*Lg; inner=np.all((ptsg>marg)&(ptsg<Lg-marg),axis=1)
            simp_in=simp[np.array([all(inner[v] for v in s) for s in simp])]
            print(f"  Delaunay intérieurs : {len(simp_in)}  {el()}",flush=True)
            for deg in CFG["G_degs"]:
                E=min(deg*Ng//2,len(candg))
                occup=E/len(candg)
                adjg=defaultdict(set)
                for k in rngg.choice(len(candg),size=E,replace=False):
                    a,b=candg[k]; adjg[a].add(b); adjg[b].add(a)
                dg=np.zeros(Ng,dtype=np.int64)
                for u in adjg: dg[u]=len(adjg[u])
                adjg,dg,_=relax_global(adjg,dg,candg,3.0,Ng,81002+deg,20)
                ret=[]
                for s in simp_in:
                    a,b,c,e4=sorted(s.tolist())
                    if (b in adjg[a]) and (c in adjg[a]) and (e4 in adjg[a]) and (c in adjg[b]) and (e4 in adjg[b]) and (e4 in adjg[c]):
                        ret.append((a,b,c,e4))
                nr=len(ret); rec={"deg":deg,"occup_cand":occup,"retained":nr,"frac":nr/len(simp_in)}
                if nr>0:
                    f2t=defaultdict(list)
                    for ti,(a,b,c,e4) in enumerate(ret):
                        for f in ((a,b,c),(a,b,e4),(a,c,e4),(b,c,e4)): f2t[f].append(ti)
                    par=list(range(nr))
                    def find(x):
                        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
                        return x
                    for f,ts in f2t.items():
                        for i in range(1,len(ts)):
                            a,b=find(ts[0]),find(ts[i])
                            if a!=b: par[a]=b
                    comp=Counter(find(i) for i in range(nr)); gi=max(comp,key=comp.get)
                    giant=comp[gi]
                    gx=[ptsg[v,0] for i in range(nr) if find(i)==gi for v in ret[i]]
                    span=(max(gx)-min(gx))/(Lg-2*marg)
                    rec.update({"giant_frac":giant/nr,"span":span,"percole":bool(giant/nr>=0.5 and span>=0.8)})
                R["G"].append(rec); save()
                print(f"  deg={deg}: occup candidats={occup*100:.0f}% | retenus {nr} ({rec['frac']*100:.1f}%) | "
                      f"géante {rec.get('giant_frac',0)*100:.1f}% | span {rec.get('span',0)*100:.0f}% "
                      f"{'★ PERCOLE' if rec.get('percole') else ''}  {el()}",flush=True)
        except Exception as ex: print(f"  G ÉCHEC : {ex}")

    # ══ H ══ instrument d_s
    print("\n─── H : INSTRUMENT d_s vs EINSTEIN à grande taille ───")
    R["H"]=[]
    for N in CFG["H_N"]:
        try:
            pts,cand,L,rc,adj,d,T = viable(N,91000,3.0,10,30)
            rgs=np.random.default_rng(1); nodes=[u for u in adj if adj[u]]
            srcs=rgs.choice(nodes,size=12,replace=False); grow=defaultdict(list)
            for s0 in srcs:
                dist={s0:0}; q=deque([s0])
                while q:
                    u=q.popleft()
                    if dist[u]>=10: continue
                    for v in adj[u]:
                        if v not in dist: dist[v]=dist[u]+1; q.append(v)
                cnt=Counter(dist.values()); cum=0
                for rr in range(0,11): cum+=cnt.get(rr,0); grow[rr].append(cum)
            rs=np.arange(2,8); Bs=np.array([np.mean(grow[rr]) for rr in rs])
            d_f=float(np.polyfit(np.log(rs),np.log(Bs),1)[0])
            rgw=np.random.default_rng(2); starts=rgw.choice(nodes,size=200,replace=False); dists={}
            for s0 in starts:
                ddm={s0:0}; q=deque([s0])
                while q:
                    u=q.popleft()
                    if ddm[u]>=14: continue
                    for v in adj[u]:
                        if v not in ddm: ddm[v]=ddm[u]+1; q.append(v)
                dists[s0]=ddm
            cur=np.array(starts); TT=[3,5,8,12,18,27,40,60]; msd={t:[] for t in TT}
            for t in range(1,61):
                for i in range(len(cur)):
                    if rgw.random()<0.5:
                        nb=list(adj[cur[i]]); cur[i]=nb[rgw.integers(len(nb))]
                if t in TT:
                    for i in range(len(cur)):
                        msd[t].append(dists[starts[i]].get(cur[i],15)**2)
            tt=np.array(TT,dtype=float); mm=np.array([np.mean(msd[t]) for t in TT]); ok=(tt>=3)&(tt<=40)
            d_w=2.0/float(np.polyfit(np.log(tt[ok]),np.log(mm[ok]),1)[0])
            ein=2*d_f/d_w; dsd=ds_heat(adj,N,3,lo=8,hi=120,tmax=400)
            R["H"].append({"N":N,"d_f":d_f,"d_w":d_w,"einstein":ein,"ds_direct":dsd,"ecart":abs(dsd-ein)})
            save()
            print(f"  N={N:>6}: d_f={d_f:.3f} d_w={d_w:.3f} 2d_f/d_w={ein:.3f} | d_s direct={dsd:.3f} écart={abs(dsd-ein):.3f} {el()}",flush=True)
        except Exception as ex: print(f"  N={N} échec H : {ex}")
    if len(R["H"])>=2:
        e=[x["ecart"] for x in R["H"]]
        print(f"  → écart : {['%.3f'%x for x in e]} — {'✓ décroît (biais d instrument)' if e[-1]<e[0] else '✗ stable'}")

    print(f"\n════ FIN — {OUT}  ({(time.time()-t0)/60:.0f} min) ════"); save()
