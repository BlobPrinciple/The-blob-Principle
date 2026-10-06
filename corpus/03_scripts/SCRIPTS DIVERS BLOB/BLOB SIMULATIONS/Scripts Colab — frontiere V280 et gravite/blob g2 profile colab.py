#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — G2 : LE PROFIL-UNIVERS (la gravité survit-elle à la limite de champ faible ?)
# Protocole pré-enregistré. Version 1.0 — 16 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# QUESTION : dans la fenêtre variété (β=2), le couplage gravitationnel r_eq
# (corrélation courbure–densité, fait A) tend-il vers :
#   (a) un PLATEAU ε > 0 → gravité faible mais RÉELLE à la limite (profil de notre
#       univers : espace quasi-plat, G adimensionnel ~10^-38, mais non nul) ;
#   (b) ZÉRO → pas de gravité asymptotique : le fait A était une corrélation de
#       taille finie, la gravité du Blob s'évapore dans le continuum.
# ENJEU : (a) = la gravité est une propriété structurelle du Blob [candidate TOE
# gravitationnelle sérieuse] ; (b) = la gravité n'émerge pas dans la bonne phase.
# À l'étage 2, r_eq(β=2) décroissait avec N (0,59→0,41→0,14) — MAIS cette décroissance
# était mesurée à la MAUVAISE densité (degré). Ici : densité = TÉTRAÈDRES (dim-3 baryonique,
# correction établie en session) ET fenêtre de tailles étendue jusqu'à 10^6.
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback, warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from collections import defaultdict
from itertools import combinations

DENSITY, KAPPA, RCUT, TAU, E_PER_N = 200.0, 10.0, 1.6, 0.5, 5
BETA_TEST = 2.0
EQ_SW     = 30
EDGE_SAMPLE = 3000
NV_THRESH = 10
OUT_JSON  = "g2_profile_results.json"

# tailles croissantes ; seeds décroissants avec N (coût)
PLAN = []
for N, seeds in [(6000, [5201,5202,5203,5204]),
                 (12000,[5201,5202,5203,5204]),
                 (25000,[5201,5202,5203]),
                 (50000,[5201,5202,5203]),
                 (100000,[5201,5202]),
                 (250000,[5201,5202]),
                 (500000,[5201]),
                 (1000000,[5201])]:
    for s in seeds: PLAN.append((N, s))

BETA = BETA_TEST
GRID = """
════════════════ GRILLE PRÉ-ENREGISTRÉE (gravée AVANT lecture) ════════════════
r_eq(N) = corr(ρ_tet, |δ|) à β=2, ρ_tet = densité locale de tétraèdres (dim-3 matière).
FIT : r_eq(N) = ε + c·N^(−p), ajusté sur toutes les tailles (moyennes par N, barres = graines).
VERDICT (le plateau ε est le paramètre décisif) :
  ε > 0,05 et significatif (ε > 2×barre au plus grand N) → PLATEAU : gravité faible
    RÉELLE à la limite. Profil-univers confirmé [M robuste]. La gravité est structurelle.
  ε compatible avec 0 (|ε| < barre) → la gravité s'évapore : r_eq → 0. Fait A = corrélation
    de taille finie. Tel quel — résultat majeur, honnête.
  intermédiaire → rapporter ε et son intervalle ; trancher exige N encore plus grand.
CONTRÔLE : à chaque N, r_eq mesuré aussi en variable DEGRÉ (l'ancienne, mauvaise) pour
  vérifier que la correction dim-3 change le verdict (le degré donnait →0 ; les tétraèdres ?).
CONTRÔLE-SUBSTRAT : r_eq sur graphe ALÉATOIRE (non équilibré) à chaque N → doit être ≈ 0
  (la gravité vient de la dynamique, pas du substrat).
Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

def build_geometry(N, seed):
    rng = np.random.default_rng(seed)
    L = (N / DENSITY) ** (1/3)
    pts = rng.uniform(0, L, size=(N, 3))
    rc = RCUT * (3 * KAPPA / (4 * math.pi * DENSITY)) ** (1/3)
    cell = rc; ncell = max(1, int(L / cell))
    grid = defaultdict(list)
    for i, p in enumerate(pts):
        grid[tuple((p // cell).astype(int) % ncell)].append(i)
    cand = []
    for i, p in enumerate(pts):
        ci = (p // cell).astype(int)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in grid[tuple((ci + [dx, dy, dz]) % ncell)]:
                        if j > i:
                            d = pts[i] - pts[j]; d -= L * np.round(d / L)
                            if (d * d).sum() < rc * rc:
                                cand.append((i, j))
    return pts, sorted(set(cand)), L, rc

class BlobState:
    def __init__(self, N, cand, active_idx):
        self.N=N; self.cand=cand; self.adj=defaultdict(set)
        for k in active_idx:
            a,b=cand[k]; self.adj[a].add(b); self.adj[b].add(a)
        self.E=len(active_idx); self.deg=np.zeros(N,dtype=np.int64)
        for k in active_idx:
            a,b=cand[k]; self.deg[a]+=1; self.deg[b]+=1
        self.sum_d2=int((self.deg.astype(np.int64)**2).sum()); self.T=self._cT()
    def _cT(self):
        t=0
        for u in self.adj:
            for v in self.adj[u]:
                if v>u: t+=len(self.adj[u]&self.adj[v])
        return t//3
    def cv(self):
        mu=2.0*self.E/self.N; var=self.sum_d2/self.N-mu*mu
        return math.sqrt(max(var,0.0))/mu
    def dS_swap(self,u,v,a,b):
        t_rm=len(self.adj[u]&self.adj[v]); self.adj[u].discard(v); self.adj[v].discard(u)
        t_add=len(self.adj[a]&self.adj[b]); self.adj[u].add(v); self.adj[v].add(u)
        dT=t_add-t_rm; d_logT=math.log(1+self.T+dT)-math.log(1+self.T)
        d2=self.sum_d2+(-2*self.deg[u]+1)+(-2*self.deg[v]+1)+(2*self.deg[a]+1)+(2*self.deg[b]+1)
        mu=2.0*self.E/self.N; cvn=math.sqrt(max(d2/self.N-mu*mu,0.0))/mu
        return (d_logT-BETA*(cvn-self.cv())),dT,d2
    def do_swap(self,u,v,a,b,dT,d2):
        self.adj[u].discard(v); self.adj[v].discard(u); self.adj[a].add(b); self.adj[b].add(a)
        self.deg[u]-=1; self.deg[v]-=1; self.deg[a]+=1; self.deg[b]+=1
        self.sum_d2=d2; self.T+=dT

def equilibrate(st,cand,beta,seed,sw):
    global BETA; BETA=beta; N=st.N; rng=np.random.default_rng(seed); te=TAU/N
    el=[(i,j) for i in range(N) for j in st.adj[i] if j>i]
    for _ in range(sw):
        for _ in range(3*N):
            io=rng.integers(len(el)); u,v=el[io]
            ii=rng.integers(len(cand)); a,b=cand[ii]
            if b in st.adj[a] or v not in st.adj[u]: continue
            if len({u,v,a,b})<4: continue
            if st.deg[u]<=2 or st.deg[v]<=2: continue
            dS,dT,d2=st.dS_swap(u,v,a,b)
            if dS>=0 or rng.random()<math.exp(dS/te):
                st.do_swap(u,v,a,b,dT,d2); el[io]=(a,b)
    return st

def dih(pts,L,tet,e):
    e0,e1=e; oth=[x for x in tet if x not in e]
    ax=pts[e1]-pts[e0]; ax-=L*np.round(ax/L); ax/=max(np.linalg.norm(ax),1e-12)
    vs=[]
    for o in oth:
        po=pts[o]-pts[e0]; po-=L*np.round(po/L); pp=po-np.dot(po,ax)*ax
        vs.append(pp/max(np.linalg.norm(pp),1e-12))
    return math.acos(np.clip(np.dot(vs[0],vs[1]),-1,1))

def r_eq_both(st,pts,L,seed):
    """retourne (r_eq_tet, r_eq_deg) : corrélation |δ| vs densité tétraèdres ET vs degré."""
    N=st.N; tris=set()
    for u in range(N):
        for v in st.adj[u]:
            if v>u:
                for w in st.adj[u]&st.adj[v]:
                    if w>v: tris.add((u,v,w))
    e2t=defaultdict(list); tet_v=np.zeros(N)
    for (u,v,w) in tris:
        for x in st.adj[u]&st.adj[v]&st.adj[w]:
            if x>w:
                for e in combinations((u,v,w,x),2): e2t[tuple(sorted(e))].append((u,v,w,x))
                for z in (u,v,w,x): tet_v[z]+=1
    edges=[e for e,ts in e2t.items() if len(ts)>=2]
    if len(edges)<40: return float('nan'),float('nan')
    rng=np.random.default_rng(seed)
    if len(edges)>EDGE_SAMPLE: edges=[edges[i] for i in rng.choice(len(edges),EDGE_SAMPLE,replace=False)]
    dl=[]; rt=[]; rd=[]
    for e in edges:
        d=abs(2*math.pi-sum(dih(pts,L,t,e) for t in e2t[e]))
        dl.append(d); rt.append(0.5*(tet_v[e[0]]+tet_v[e[1]])); rd.append(0.5*(st.deg[e[0]]+st.deg[e[1]]))
    dl=np.array(dl); rt=np.array(rt); rd=np.array(rd)
    r_tet=float(np.corrcoef(rt,dl)[0,1]) if np.std(rt)>0 else float('nan')
    r_deg=float(np.corrcoef(rd,dl)[0,1]) if np.std(rd)>0 else float('nan')
    return r_tet,r_deg

if __name__ == "__main__":
    print(GRID)
    print(f"Environnement : python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"β={BETA_TEST}, {len(PLAN)} points, N jusqu'à 10^6. Estimation ~2-4 h.\n")
    all_res=[]; t0=time.time()
    for (N,seed) in PLAN:
        t1=time.time()
        try:
            pts,cand,L,rc=build_geometry(N,seed)
            rng=np.random.default_rng(seed)
            # contrôle-substrat : graphe aléatoire
            st_r=BlobState(N,cand,rng.choice(len(cand),size=E_PER_N*N,replace=False))
            rt_rand,_=r_eq_both(st_r,pts,L,seed+1)
            # Blob équilibré
            st=BlobState(N,cand,rng.choice(len(cand),size=E_PER_N*N,replace=False))
            st=equilibrate(st,cand,BETA_TEST,seed+2,EQ_SW)
            rt,rd=r_eq_both(st,pts,L,seed+3)
            rec={"N":N,"seed":seed,"r_tet":rt,"r_deg":rd,"r_rand":rt_rand}
            all_res.append(rec)
            print(f"[N={N} s={seed}] r_eq(tét)={rt:+.4f}  r_eq(deg)={rd:+.4f}  r_rand={rt_rand:+.4f}  ({(time.time()-t1)/60:.1f} min)",flush=True)
        except Exception as ex:
            print(f"[N={N} s={seed}] ÉCHEC: {ex}",flush=True); traceback.print_exc()
            all_res.append({"N":N,"seed":seed,"error":str(ex)})
        with open(OUT_JSON,"w") as f: json.dump(all_res,f)
    # ─── SYNTHÈSE ───
    ok=[r for r in all_res if "r_tet" in r and not math.isnan(r["r_tet"])]
    print(f"\n════════ SYNTHÈSE ({(time.time()-t0)/60:.0f} min) ════════")
    Ns=sorted(set(r["N"] for r in ok))
    def mean_at(N,key): 
        vs=[r[key] for r in ok if r["N"]==N and not math.isnan(r[key])]
        return (np.mean(vs),np.std(vs)/max(len(vs)**0.5,1)) if vs else (float('nan'),float('nan'))
    print(f"{'N':>8} | {'r_eq(tét)':>16} | {'r_eq(deg)':>12} | {'r_rand':>8}")
    for N in Ns:
        mt,et=mean_at(N,"r_tet"); md,ed=mean_at(N,"r_deg"); mr,_=mean_at(N,"r_rand")
        print(f"{N:>8} | {mt:+.4f} ± {et:.4f} | {md:+.4f} | {mr:+.4f}")
    # fit plateau sur r_tet
    xs=np.array([N for N in Ns]); ys=np.array([mean_at(N,"r_tet")[0] for N in Ns])
    lastbar=mean_at(Ns[-1],"r_tet")[1]
    try:
        from scipy.optimize import curve_fit
        popt,_=curve_fit(lambda N,eps,c,p: eps+c*N**(-p), xs, ys, p0=[0.1,1.0,0.3], maxfev=10000, bounds=([-0.5,-10,0.01],[1,10,2]))
        eps,c,p=popt
        print(f"\nFIT r_eq(tét) = ε + c·N^(−p) : ε={eps:+.4f}, c={c:.3f}, p={p:.2f}")
        print(f"barre au plus grand N ({Ns[-1]}) = {lastbar:.4f}")
        if eps>0.05 and eps>2*max(lastbar,1e-4):
            print(f"→ ★★★ PLATEAU ε={eps:.3f} > 0 SIGNIFICATIF : GRAVITÉ FAIBLE RÉELLE À LA LIMITE.")
            print(f"   Profil-univers confirmé [M robuste] : la gravité est structurelle dans la fenêtre")
            print(f"   variété. Le Blob a une gravité asymptotique — candidate TOE gravitationnelle sérieuse.")
        elif abs(eps)<max(lastbar,0.03):
            print(f"→ ε compatible avec 0 : la gravité s'ÉVAPORE (r_eq→0). Fait A = corrélation de taille")
            print(f"   finie dans la fenêtre variété. Résultat majeur — tel quel.")
        else:
            print(f"→ ε={eps:.3f} intermédiaire (intervalle non tranché) : N encore plus grand requis. Tel quel.")
    except Exception as e:
        print(f"\nfit non convergé ({e}) — lecture directe du tableau ci-dessus. Tel quel.")
    print(f"\nRésultats complets : {OUT_JSON}")
