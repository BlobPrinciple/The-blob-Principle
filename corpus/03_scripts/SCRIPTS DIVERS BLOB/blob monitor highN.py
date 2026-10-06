#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
BLOB — MONITORING HAUTE-N DES SIGNATURES  (13 juin 2026)
================================================================================
Balaie N (jusqu'a 10^6) et trace l'EVOLUTION de chaque invariant/signature en
fonction de N, au POINT DE FONCTIONNEMENT DU CORPUS. Pour "situer toutes les
evolutions" : on voit si chaque signature croit, se stabilise, ou s'evanouit
quand N -> grand, et a quel sigma elle se tient face aux temoins (RGG, ER).

>>> POINT DE FONCTIONNEMENT <<<
  Le point corpus est n_tri/N ~ 5.4  (tri/arete=4.88 ; calcif/sommet=16.1 = 3*n_tri/N).
  CE N'EST PAS 16 (le 16.1 compte chaque triangle 3 fois).

  GINI -- piege d'etiquette RESOLU : le "Gini=0.8542" du corpus est le Gini de la
  MASSE (= triangles/sommet ; cf. invariants_grandN.py : gini(tpv)), PAS le Gini
  des degres. Ce script reporte donc DEUX colonnes :
     Gini_d = Gini des degres   (~0.38)
     Gini_m = Gini de la masse  (doit tomber sur ~0.854 au point corpus)
  Si Gini_m ~ 0.85, le generateur EST au point de travail -- aucun autre
  generateur n'est requis (l'ancienne note "remplace build_blob" etait un faux
  probleme ne d'une comparaison Gini-degres vs Gini-masse).

Couts : connectivite = O(N) (jusqu'a 10^6 OK). b1 (rang GF2) et Ollivier (transport)
sont chers -> plafonnes a N<=N_HEAVY_MAX (defaut 100k) ; au-dela, connectivite seule.
================================================================================
"""
import numpy as np
from numba import njit
from scipy.spatial import cKDTree
from scipy.optimize import linprog
import math

MAXD = 96
N_HEAVY_MAX = 100_000   # au-dela : b1/Ollivier sautes (trop chers)

# ----------------------------------------------------------------------------
# moteur (numba)
# ----------------------------------------------------------------------------
@njit(cache=True)
def _build_nbr(eu, ev, N, cap):
    deg = np.zeros(N, np.int64); nbr = -np.ones((N, cap), np.int64)
    for k in range(eu.shape[0]):
        u = eu[k]; v = ev[k]
        if deg[u] < cap: nbr[u, deg[u]] = v; deg[u] += 1
        if deg[v] < cap: nbr[v, deg[v]] = u; deg[v] += 1
    return nbr, deg

@njit(cache=True)
def _n_tri(nbr, deg, N):
    tot = 0
    for u in range(N):
        for i in range(deg[u]):
            a = nbr[u, i]
            if a <= u: continue
            for j in range(i + 1, deg[u]):
                b = nbr[u, j]
                if b <= u: continue
                for m in range(deg[a]):
                    if nbr[a, m] == b:
                        tot += 1; break
    return tot

@njit(cache=True)
def _tpv(nbr, deg, N):
    # triangles incidents a chaque sommet = "masse"/calcification (corpus :
    # invariants_grandN.py). C'est de SA distribution que vient Gini=0.8542.
    tpv = np.zeros(N, np.int64)
    for u in range(N):
        du = deg[u]; c = 0
        for ki in range(du):
            a = nbr[u, ki]
            for kj in range(ki + 1, du):
                b = nbr[u, kj]
                for m in range(deg[a]):
                    if nbr[a, m] == b:
                        c += 1; break
        tpv[u] = c
    return tpv

@njit(cache=True)
def _has(nbr, deg, a, b):
    for k in range(deg[a]):
        if nbr[a, k] == b: return True
    return False

@njit(cache=True)
def _common(nbr, deg, u, v):
    c = 0
    for k in range(deg[u]):
        x = nbr[u, k]
        for m in range(deg[v]):
            if nbr[v, m] == x: c += 1; break
    return c

@njit(cache=True)
def _rm(nbr, deg, u, v):
    du = deg[u]
    for k in range(du):
        if nbr[u, k] == v:
            nbr[u, k] = nbr[u, du - 1]; nbr[u, du - 1] = -1; deg[u] = du - 1; return

@njit(cache=True)
def _add(nbr, deg, a, b, cap):
    if deg[a] < cap: nbr[a, deg[a]] = b; deg[a] += 1
    if deg[b] < cap: nbr[b, deg[b]] = a; deg[b] += 1

@njit(cache=True)
def _mcmc(nbr, deg, eu, ev, pa, pb, beta, tau_eff, mean, nt0, nsteps, cap, seed):
    np.random.seed(seed)
    N = deg.shape[0]; E = eu.shape[0]; P = pa.shape[0]; nt = nt0
    sumsq = 0.0
    for i in range(N): sumsq += deg[i] * deg[i]
    cv = math.sqrt(max(sumsq / N - mean * mean, 0.0)) / mean
    S = math.log(1.0 + nt) - beta * cv
    for _ in range(nsteps):
        io = np.random.randint(0, E); u = eu[io]; v = ev[io]
        if deg[u] <= 2 or deg[v] <= 2: continue
        a = -1; b = -1; ok = False
        for _t in range(40):
            pi = np.random.randint(0, P); ca = pa[pi]; cb = pb[pi]
            if ca == u or ca == v or cb == u or cb == v: continue
            if deg[ca] >= cap or deg[cb] >= cap: continue
            if not _has(nbr, deg, ca, cb): a = ca; b = cb; ok = True; break
        if not ok: continue
        tl = _common(nbr, deg, u, v); tg = _common(nbr, deg, a, b)
        nt2 = nt - tl + tg
        du = deg[u]; dv = deg[v]; da = deg[a]; db = deg[b]
        nss = sumsq + (-2*du+1) + (-2*dv+1) + (2*da+1) + (2*db+1)
        cv2 = math.sqrt(max(nss / N - mean * mean, 0.0)) / mean
        S2 = math.log(1.0 + nt2) - beta * cv2
        if (S2 - S) >= 0.0 or np.random.random() < math.exp((S2 - S) / tau_eff):
            _rm(nbr, deg, u, v); _rm(nbr, deg, v, u); _add(nbr, deg, a, b, cap)
            nt = nt2; sumsq = nss; S = S2; eu[io] = a; ev[io] = b
    return nt

# ----------------------------------------------------------------------------
# generateurs
# ----------------------------------------------------------------------------
def _rips(N, seed, kappa, pf):
    rng = np.random.default_rng(seed); pts = rng.random((N, 3))
    r = (kappa / ((N - 1) * (4/3) * np.pi)) ** (1/3)
    tree = cKDTree(pts)
    pool = tree.query_pairs(pf * r, output_type='ndarray').astype(np.int64)
    dd = np.linalg.norm(pts[pool[:,0]] - pts[pool[:,1]], axis=1)
    pool = pool[np.argsort(dd)]
    E0 = min(int(round(N * kappa / 2)), len(pool))
    return pts, pool[:E0], pool

def build_blob(N, seed, kappa=6.6, pf=1.6, fac=120, tau_num=0.5):
    """
    >>> POUR DU DEFINITIF : remplace ce corps par TON generateur calibre. <<<
    Defaut : vise le point corpus en TRIANGLES (n_tri/N ~ 5.4, tau_num=0.5),
    mais Gini ~ 0.39 (corpus 0.854) -> proxy qualitatif seulement.
    """
    pts, edges, pool = _rips(N, seed, kappa, pf)
    nbr, deg = _build_nbr(edges[:,0].copy(), edges[:,1].copy(), N, MAXD)
    nt = _n_tri(nbr, deg, N)
    eu = edges[:,0].copy(); ev = edges[:,1].copy()
    pa = np.ascontiguousarray(pool[:,0]); pb = np.ascontiguousarray(pool[:,1])
    mean = 2.0 * len(edges) / N; steps = fac * N; chunk = steps // 8
    for c in range(8):
        nt = _mcmc(nbr, deg, eu, ev, pa, pb, 0.30, tau_num/N, mean, nt, chunk, MAXD, seed*100+1+c)
    return pts, nbr, deg

def build_rgg(N, seed, kappa=6.6, pf=1.6):
    pts, edges, _ = _rips(N, 90_000 + seed, kappa, pf)
    nbr, deg = _build_nbr(edges[:,0].copy(), edges[:,1].copy(), N, MAXD)
    return pts, nbr, deg

def build_er(N, seed, kappa=6.6):
    rng = np.random.default_rng(70_000 + seed); E = int(round(N * kappa / 2))
    eu = rng.integers(0, N, size=2*E); ev = rng.integers(0, N, size=2*E)
    m = eu != ev; eu = eu[m][:E]; ev = ev[m][:E]
    nbr, deg = _build_nbr(eu.astype(np.int64), ev.astype(np.int64), N, MAXD)
    return None, nbr, deg

# ----------------------------------------------------------------------------
# mesures
# ----------------------------------------------------------------------------
def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if x.sum() == 0: return 0.0
    c = np.arange(1, n + 1); return (2*np.sum(c*x)/(n*x.sum())) - (n+1)/n

def connectivity(nbr, deg, N):
    nt = _n_tri(nbr, deg, N); degf = deg.astype(float)
    tpv = _tpv(nbr, deg, N).astype(float)        # triangles/sommet = masse (calcification)
    p2 = np.sum(degf*(degf-1)/2)
    return dict(n_tri_par_N=nt/N, CV=degf.std()/degf.mean(),
                Gini_deg=gini(degf),             # Gini des DEGRES (~0.38)
                Gini_masse=gini(tpv),            # Gini de la MASSE = quantite du corpus (~0.854)
                calcif_sommet=float(tpv.mean()), # = 3*n_tri/N (~16.1)
                clustering=3*nt/p2 if p2 > 0 else 0.0)

def _edges(nbr, deg, N):
    I=[];J=[]
    for u in range(N):
        for k in range(deg[u]):
            v=int(nbr[u,k])
            if v>u: I.append(u);J.append(v)
    return np.array(I,np.int64), np.array(J,np.int64)

def b1_clique(nbr, deg, N):
    eid={}; idx=0
    for u in range(N):
        for k in range(deg[u]):
            v=int(nbr[u,k])
            if v>u: eid[(u,v)]=idx; idx+=1
    def E(x,y): return eid[(x,y)] if x<y else eid[(y,x)]
    piv={}; rank=0
    for u in range(N):
        nu=[int(nbr[u,k]) for k in range(deg[u]) if nbr[u,k]>u]; ns=set(nu)
        for i in range(len(nu)):
            a=nu[i]
            for j in range(i+1,len(nu)):
                b=nu[j]
                if b in ns and any(int(nbr[a,m])==b for m in range(deg[a])):
                    row=(1<<E(u,a))|(1<<E(u,b))|(1<<E(a,b))
                    while row:
                        lb=row&(-row)
                        if lb in piv: row^=piv[lb]
                        else: piv[lb]=row; rank+=1; break
    return idx - N + 1 - rank  # E - V + 1(connexe) - rang(d2)

def ollivier_conc(pts, nbr, deg, N, nsamp=300, seed=0, alpha=0.5):
    rng=np.random.default_rng(seed); I,J=_edges(nbr,deg,N)
    if len(I)==0: return np.nan
    idx=rng.choice(len(I),size=min(nsamp,len(I)),replace=False); kap=[];tri=[]
    for e in idx:
        u,v=int(I[e]),int(J[e])
        nu=[int(nbr[u,k]) for k in range(deg[u])]; nvv=[int(nbr[v,k]) for k in range(deg[v])]
        if not nu or not nvv: continue
        su=[u]+nu; pu=np.array([alpha]+[(1-alpha)/len(nu)]*len(nu))
        sv=[v]+nvv; pv=np.array([alpha]+[(1-alpha)/len(nvv)]*len(nvv))
        C=np.zeros((len(su),len(sv)))
        for ai,a in enumerate(su):
            adj=set(int(nbr[a,k]) for k in range(deg[a]))|{a}
            for bi,b in enumerate(sv): C[ai,bi]=0.0 if a==b else (1.0 if b in adj else 2.0)
        nA,nB=len(su),len(sv); Aeq=np.zeros((nA+nB,nA*nB))
        for ai in range(nA): Aeq[ai,ai*nB:(ai+1)*nB]=1
        for bi in range(nB): Aeq[nA+bi,bi::nB]=1
        res=linprog(C.ravel(),A_eq=Aeq,b_eq=np.concatenate([pu,pv]),bounds=[(0,None)]*(nA*nB),method='highs')
        if not res.success: continue
        nvset=set(nvv); cnt=sum(1 for x in nu if x in nvset)
        kap.append(1-res.fun); tri.append(cnt)
    kap=np.array(kap);tri=np.array(tri)
    if len(kap)<10: return np.nan
    med=np.median(tri)
    return kap[tri>med].mean()-kap[tri<=med].mean()

# ----------------------------------------------------------------------------
# monitoring : balayage en N
# ----------------------------------------------------------------------------
def monitor(N_list=(10_000, 30_000, 100_000, 300_000, 1_000_000), seeds=(0,1,2)):
    print("="*100)
    print("MONITORING HAUTE-N : evolution des signatures vs N (point corpus n_tri/N~5.4)")
    print("  Gini_m (masse = triangles/sommet) doit tomber sur ~0.854 = point corpus ; Gini_d = degres (~0.38)")
    print("="*100)
    hdr = f"{'N':>9} | {'n_tri/N':>8} {'CV':>7} {'Gini_d':>7} {'Gini_m':>7} {'clust':>7} | {'CVσ':>7} {'triσ':>7} {'clustσ':>8} | {'b1 Blob':>9} {'b1 ER':>9} {'x':>6} | {'Olliv Δ':>9}"
    print(hdr); print("-"*len(hdr))
    for N in N_list:
        heavy = N <= N_HEAVY_MAX
        cb=[]; cr=[]; tb=[]; tr=[]; clb=[]; clr=[]; gb=[]; gmb=[]
        b1b=[]; b1e=[]; ob=[]
        for s in seeds:
            pts,nbr,deg = build_blob(N, s)
            m = connectivity(nbr, deg, N)
            cb.append(m['CV']); tb.append(m['n_tri_par_N']); clb.append(m['clustering'])
            gb.append(m['Gini_deg']); gmb.append(m['Gini_masse'])
            ntpv_ctrl = m['n_tri_par_N']
            _,nbrR,degR = build_rgg(N, s); mr = connectivity(nbrR, degR, N)
            cr.append(mr['CV']); tr.append(mr['n_tri_par_N']); clr.append(mr['clustering'])
            if heavy:
                b1b.append(b1_clique(nbr, deg, N))
                _,nbrE,degE = build_er(N, s); b1e.append(b1_clique(nbrE, degE, N))
                ob.append(ollivier_conc(pts, nbr, deg, N, seed=s))
        def sig(a,b):
            a=np.array(a);b=np.array(b);sd=math.sqrt(a.std()**2+b.std()**2)
            return abs(a.mean()-b.mean())/sd if sd>1e-12 else 0
        cvs=sig(cb,cr); tris=sig(tb,tr); cls=sig(clb,clr)
        if heavy and np.mean(b1b)>0:
            b1s=f"{np.mean(b1b):>9.0f} {np.mean(b1e):>9.0f} {np.mean(b1e)/np.mean(b1b):>6.1f}"
            os=f"{np.nanmean(ob):>9.4f}"
        else:
            b1s=f"{'(saute)':>9} {'':>9} {'':>6}"; os=f"{'(saute)':>9}"
        print(f"{N:>9} | {np.mean(tb):>8.2f} {np.mean(cb):>7.3f} {np.mean(gb):>7.3f} {np.mean(gmb):>7.3f} {np.mean(clb):>7.3f} | "
              f"{cvs:>7.0f} {tris:>7.0f} {cls:>8.0f} | {b1s} | {os}")
    print("-"*len(hdr))
    print("LECTURE : on suit chaque signature quand N grandit. Robustes attendues : CV/tri/b1")
    print("(sigma qui CROIT avec N). Gini_m ~ 0.854 = preuve qu'on est au point de travail du corpus.")
    print("Si une signature s'evanouit a grand N, elle etait un artefact de taille finie ;")
    print("si elle se renforce, elle est structurelle.")


if __name__ == "__main__":
    # demarrage prudent ; pousse jusqu'a 10^6 une fois le moteur compile.
    monitor(N_list=(10_000, 30_000, 100_000), seeds=(0, 1, 2))
    # puis, pour le run extremement haut :
    # monitor(N_list=(300_000, 1_000_000), seeds=(0, 1, 2))
