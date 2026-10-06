#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# BLOB — PASSE COMPLÈTE DE VALIDATION (préalable à la gravure V277bis)
# Version 1.0 — 18 juillet 2026. Autonome (aucune dépendance au module bgrav).
# ═══════════════════════════════════════════════════════════════════════════════
# SIX VOLETS. Toutes les grilles sont PRÉ-ENREGISTRÉES ci-dessous, gravées AVANT lecture.
#
#  W1  SIGNATURE TORE COMPLÈTE — 30 modes : comptage 6/12/8 aux ratios 1/2/3.
#      (Points entiers sur les sphères k²=1,2,3 du tore T³ : (±1,0,0)→6 ; (±1,±1,0)→12 ;
#       (±1,±1,±1)→8.) Si le comptage sort, la preuve-tore est TOTALE et entière.
#  W2  CONSTANTES — test de la boussole (plateau + réversibilité) multi-graines,
#      + amplification dynamique C_blob/C_aléa, + N-dépendance de chaque constante.
#  W3  DÉSORDRE — exposant de décroissance de l'éclatement intra-couche en N.
#  W4  POINT FIXE DIMENSIONNEL — attracteur : 2 inits opposées × graines × tailles.
#  W5  MUR UNIFIÉ — balayage fin β : ξ, χ et RP mesurés ENSEMBLE. Les 3 pics coïncident-ils ?
#  W6  ACTION LOCALE À GRAND N — d_s, RP site+lien, gravité (confirmations V277bis).
# ═══════════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, warnings
warnings.filterwarnings("ignore")
from collections import defaultdict, deque
from itertools import combinations
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

# ─────────────────────────── RÉGLAGES ───────────────────────────
PRESET = "complet"     # "rapide" (~1 h) | "complet" (~3-4 h) | "maximal" (~8-10 h)
OUT    = "passe_complete_results.json"

CFG = {
 "rapide":  {"N_SPEC":  8000, "N_CST": [4000, 8000],          "N_FIX":  6000, "N_MUR":  8000, "N_LOC":  8000, "SW": 30, "MRP":  60},
 "complet": {"N_SPEC": 20000, "N_CST": [5000, 10000, 20000],  "N_FIX": 10000, "N_MUR": 12000, "N_LOC": 20000, "SW": 35, "MRP": 100},
 "maximal": {"N_SPEC": 50000, "N_CST": [10000, 25000, 50000], "N_FIX": 20000, "N_MUR": 20000, "N_LOC": 40000, "SW": 40, "MRP": 140},
}[PRESET]

DENSITY, KAPPA, RCUT, TAU = 200.0, 10.0, 1.6, 0.5
E_GRAV, E_DIMS = 5, 3.3          # |E| = 5N (gravité) ; 3,3N (dims)
ALPHA_L, BETAL_L, DBAR_L = 0.62, 0.15, 6.6   # point C2 de l'action locale

GRILLE = """
════════ GRILLE PRÉ-ENREGISTRÉE — PASSE COMPLÈTE (gravée AVANT lecture) ════════
W1 TORE : couche 1 = 6 modes dans [1,00;1,30] ; couche 2 = 12 modes autour de 2
   ([1,6;2,4]) ; couche 3 = 8 modes autour de 3 ([2,6;3,4]) — comptage r₃(m) des points
   entiers sur les sphères m=1,2,3. TROIS états comparés (le test n'est discriminant
   qu'ainsi) : VIABLE (β=3) / ALÉATOIRE dilué (topologie héritée du plongement périodique)
   / CONDENSÉ type L2 (α élevé, β_ℓ=0). Lecture :
     • viable ET aléa = 6/12/8, condensé ≠ → la dynamique viable PRÉSERVE la variété là où
       la phase dégénérée la DÉTRUIT. C'est la revendication honnête (non « le Blob crée un
       tore » : la topologie vient du substrat périodique).
     • viable ≠ 6/12/8 → gravé tel quel.
W2 CONSTANTES : ⟨C⟩ est une constante si (a) plateau <5 % de part et d'autre de β_c,
   (b) réversibilité <3 % (aller-retour), (c) dérive en N <3 % sur toutes les tailles.
   Amplification A = C_blob/C_aléa : constante si dérive en N <5 %.
W3 DÉSORDRE : éclatement δ₂ = λ₂/λ₁−1 et δ₃ = λ₃/λ₁−1 décroissent en N avec exposant
   ajusté p ; si p < −0,3 net → grandeurs de taille finie (NON constantes), tendance vers
   la dégénérescence du tore. Si p ≈ 0 → ce sont de vraies constantes de désordre.
W4 POINT FIXE : les deux inits opposées (dense / arbre) convergent à <5 % l'une de l'autre,
   pour chaque graine et chaque taille → d_s=3 ATTRACTEUR [confirmation multi-tout].
W5 MUR : ξ, χ et |min-eig RP| mesurés sur β ∈ [1,30 ; 2,60]. Si les trois maxima tombent
   dans une fenêtre de ±0,15 en β → UNIFICATION mur/criticité/quantique [T-numérique].
   Sinon → gravé tel quel (trois phénomènes distincts ou β_c hors fenêtre).
W6 ACTION LOCALE : d_s ∈ [2,85;3,20] ; |min-eig| ≤ 3·tol aux DEUX réflexions ; r_tet > 0
   à grand N → confirmations V277bis étendues.
Aucun curseur ne bouge après lecture. Tous les écarts sont lus tels quels.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────────────── GÉOMÉTRIE / GRAPHES ─────────────────────────
def build(N, seed):
    rng = np.random.default_rng(seed); L = (N / DENSITY) ** (1/3)
    pts = rng.uniform(0, L, size=(N, 3))
    rc  = RCUT * (3 * KAPPA / (4 * math.pi * DENSITY)) ** (1/3)
    nc = max(1, int(L / rc)); grid = defaultdict(list)
    for i, p in enumerate(pts): grid[tuple((p // rc).astype(int) % nc)].append(i)
    cand = []
    for i, p in enumerate(pts):
        ci = (p // rc).astype(int)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in grid[tuple((ci + [dx, dy, dz]) % nc)]:
                        if j > i:
                            d = pts[i] - pts[j]; d -= L * np.round(d / L)
                            if (d * d).sum() < rc * rc: cand.append((i, j))
    return pts, sorted(set(cand)), L, rc, rng

def init_adj(cand, E, seed):
    rng = np.random.default_rng(seed); adj = defaultdict(set)
    for k in rng.choice(len(cand), size=int(E), replace=False):
        a, b = cand[k]; adj[a].add(b); adj[b].add(a)
    return adj

def init_sparse(cand, E, N, seed):
    """Init 'arbre + extras' : minimise les triangles au départ (pour W4)."""
    rng = np.random.default_rng(seed); adj = defaultdict(set); parent = list(range(N))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    perm = rng.permutation(len(cand)); used = 0; taken = set()
    for k in perm:
        a, b = cand[k]; ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb; adj[a].add(b); adj[b].add(a); taken.add(k); used += 1
        if used >= min(N - 1, E): break
    for k in perm:
        if used >= E: break
        if k in taken: continue
        a, b = cand[k]
        if b in adj[a]: continue
        adj[a].add(b); adj[b].add(a); used += 1
    return adj

def degs(adj, N):
    d = np.zeros(N, dtype=np.int64)
    for u in adj: d[u] = len(adj[u])
    return d

def spA(adj, N):
    r = []; c = []
    for u in adj:
        for v in adj[u]: r.append(u); c.append(v)
    return sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(N, N))

# ───────────────────────── DYNAMIQUES ─────────────────────────
def relax_global(adj, d, cand, beta, N, seed, sw):
    """Action GLOBALE canonique : S = log(1+T) − β·CV ; mesure exp((N/τ)S) → te = τ/N."""
    rng = np.random.default_rng(seed); te = TAU / N
    T = 0
    for u in adj:
        for v in adj[u]:
            if v > u: T += len(adj[u] & adj[v])
    T //= 3
    X = int((d.astype(np.int64) ** 2).sum()); E = int(sum(len(adj[u]) for u in adj) // 2)
    mu = 2.0 * E / N
    el = [(i, j) for i in range(N) for j in adj[i] if j > i]
    for _ in range(sw):
        for _ in range(3 * N):
            io = rng.integers(len(el)); u, v = el[io]
            ii = rng.integers(len(cand)); a, b = cand[ii]
            if b in adj[a] or v not in adj[u] or len({u, v, a, b}) < 4 or d[u] <= 2 or d[v] <= 2: continue
            t_rm = len(adj[u] & adj[v]); adj[u].discard(v); adj[v].discard(u)
            t_ad = len(adj[a] & adj[b]); adj[u].add(v); adj[v].add(u)
            dT = t_ad - t_rm
            dX = (-2*d[u] + 1) + (-2*d[v] + 1) + (2*d[a] + 1) + (2*d[b] + 1)
            cv0 = math.sqrt(max(X / N - mu*mu, 0)) / mu
            cv1 = math.sqrt(max((X + dX) / N - mu*mu, 0)) / mu
            dS = math.log(1 + T + dT) - math.log(1 + T) - beta * (cv1 - cv0)
            if dS >= 0 or rng.random() < math.exp(dS / te):
                adj[u].discard(v); adj[v].discard(u); adj[a].add(b); adj[b].add(a)
                d[u] -= 1; d[v] -= 1; d[a] += 1; d[b] += 1; T += dT; X += dX; el[io] = (a, b)
    return adj, d

def relax_local(adj, d, cand, alpha, beta_l, dbar, N, seed, sw):
    """Action LOCALE : S = α·Σ_e log(1+t_e) − β_ℓ·Σ_i (d_i−d̄)² ; mesure exp(S/τ)."""
    rng = np.random.default_rng(seed)
    el = [(i, j) for i in range(N) for j in adj[i] if j > i]; acc = 0; tot = 0
    for _ in range(sw):
        for _ in range(3 * N):
            io = rng.integers(len(el)); u, v = el[io]
            ii = rng.integers(len(cand)); a, b = cand[ii]
            if b in adj[a] or v not in adj[u] or len({u, v, a, b}) < 4 or d[u] <= 2 or d[v] <= 2: continue
            tot += 1
            C = adj[u] & adj[v]; dT = -alpha * math.log(1 + len(C))
            for w in C:
                tuw = len(adj[u] & adj[w]); tvw = len(adj[v] & adj[w])
                dT += alpha * (math.log(tuw / (1 + tuw)) + math.log(tvw / (1 + tvw)))
            adj[u].discard(v); adj[v].discard(u)
            C2 = adj[a] & adj[b]; dT += alpha * math.log(1 + len(C2))
            for w in C2:
                taw = len(adj[a] & adj[w]); tbw = len(adj[b] & adj[w])
                dT += alpha * (math.log((2 + taw) / (1 + taw)) + math.log((2 + tbw) / (1 + tbw)))
            dQ = ((d[u]-1-dbar)**2 - (d[u]-dbar)**2) + ((d[v]-1-dbar)**2 - (d[v]-dbar)**2) \
               + ((d[a]+1-dbar)**2 - (d[a]-dbar)**2) + ((d[b]+1-dbar)**2 - (d[b]-dbar)**2)
            dS = dT - beta_l * dQ
            if dS >= 0 or rng.random() < math.exp(dS / TAU):
                adj[a].add(b); adj[b].add(a); d[u] -= 1; d[v] -= 1; d[a] += 1; d[b] += 1
                el[io] = (a, b); acc += 1
            else:
                adj[u].add(v); adj[v].add(u)
    return adj, d, acc / max(tot, 1)

# ───────────────────────── OBSERVABLES ─────────────────────────
def spectrum(adj, N, k=30):
    A = spA(adj, N); d = np.asarray(A.sum(1)).ravel()
    Lp = (sp.diags(d) - A).tocsr()
    for attempt in ("shift", "sm"):
        try:
            if attempt == "shift":
                vals = eigsh(Lp, k=k, sigma=1e-6, which='LM', return_eigenvectors=False, maxiter=5000)
            else:
                vals = eigsh(Lp, k=k, which='SM', return_eigenvectors=False, maxiter=20000, tol=1e-6)
            return np.sort(vals)
        except Exception:
            continue
    return None

def clustering(adj, N, nsamp=1200, seed=0):
    rng = np.random.default_rng(seed)
    nodes = [u for u in adj if len(adj[u]) >= 2]
    if not nodes: return float('nan')
    samp = rng.choice(nodes, size=min(nsamp, len(nodes)), replace=False)
    cs = []
    for u in samp:
        nb = list(adj[u]); k = len(nb)
        if k < 2: continue
        links = sum(1 for i in range(k) for j in range(i+1, k) if nb[j] in adj[nb[i]])
        cs.append(2 * links / (k * (k - 1)))
    return float(np.mean(cs))

def ds_measure(adj, N, seed=0, cal=1.0):
    A = spA(adj, N)
    tmax = 200 if N <= 8000 else 400
    TG = np.unique(np.round(np.logspace(0, math.log10(tmax), 45)).astype(int))
    deg = np.asarray(A.sum(1)).ravel(); Pi = deg / deg.sum()
    rng = np.random.default_rng(seed); src = rng.choice(N, size=8, replace=False)
    X = np.zeros((N, 8)); X[src, np.arange(8)] = 1.0; invd = 1.0 / np.maximum(deg, 1)
    rec = np.zeros(len(TG)); tj = 0
    for t in range(1, TG[-1] + 1):
        X = 0.5 * (X + invd[:, None] * (A @ X))
        if tj < len(TG) and t == TG[tj]:
            rec[tj] = float(np.mean(X[src, np.arange(8)] - Pi[src])); tj += 1
    ok = (TG >= 4) & (TG <= 60) & (rec > 0)
    if ok.sum() < 6: return float('nan')
    return cal * float(-2 * np.polyfit(np.log(TG[ok]), np.log(rec[ok]), 1)[0])

def exact_cube(n):
    A = defaultdict(set)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i = x*n*n + y*n + z
                for dx, dy, dz in ((1,0,0),(0,1,0),(0,0,1)):
                    j = ((x+dx)%n)*n*n + ((y+dy)%n)*n + ((z+dz)%n)
                    A[i].add(j); A[j].add(i)
    return A, n**3

def corr_length(adj, d, N, seed, nsrc=40, rmax=12):
    dd = d.astype(float) - d.astype(float).mean()
    rng = np.random.default_rng(seed)
    nodes = [u for u in adj if adj[u]]
    srcs = rng.choice(nodes, size=min(nsrc, len(nodes)), replace=False)
    prod = defaultdict(list)
    for s0 in srcs:
        dist = {s0: 0}; q = deque([s0])
        while q:
            u = q.popleft()
            if dist[u] >= rmax: continue
            for v in adj[u]:
                if v not in dist: dist[v] = dist[u] + 1; q.append(v)
        for v, r in dist.items():
            if r > 0: prod[r].append(dd[s0] * dd[v])
    rs = []; cs = []
    for r in range(1, rmax + 1):
        if len(prod.get(r, [])) > 30: rs.append(r); cs.append(np.mean(prod[r]))
    rs = np.array(rs); cs = np.array(cs)
    pos = cs > 0
    if pos.sum() < 4: return float('nan')
    sl = np.polyfit(rs[pos], np.log(cs[pos]), 1)[0]
    return -1.0 / sl if sl < 0 else float('inf')

def rtet(adj, pts, L, N, seed):
    tris = set()
    for u in adj:
        for v in adj[u]:
            if v > u:
                for w in adj[u] & adj[v]:
                    if w > v: tris.add((u, v, w))
    e2t = defaultdict(list); tv = np.zeros(N)
    for (u, v, w) in tris:
        for x in adj[u] & adj[v] & adj[w]:
            if x > w:
                for e in combinations((u, v, w, x), 2): e2t[tuple(sorted(e))].append((u, v, w, x))
                for z in (u, v, w, x): tv[z] += 1
    ep = [e for e, ts in e2t.items() if len(ts) >= 2]
    if len(ep) < 50: return float('nan'), len(ep)
    rg = np.random.default_rng(seed)
    if len(ep) > 1200: ep = [ep[i] for i in rg.choice(len(ep), 1200, replace=False)]
    def dih(tet, e):
        e0, e1 = e; oth = [y for y in tet if y not in e]
        ax = pts[e1] - pts[e0]; ax -= L * np.round(ax / L); ax /= max(np.linalg.norm(ax), 1e-12)
        vs = []
        for o in oth:
            po = pts[o] - pts[e0]; po -= L * np.round(po / L); pp = po - np.dot(po, ax) * ax
            vs.append(pp / max(np.linalg.norm(pp), 1e-12))
        return math.acos(np.clip(np.dot(vs[0], vs[1]), -1, 1))
    rho = []; dl = []
    for e in ep:
        dl.append(abs(2*math.pi - sum(dih(t, e) for t in e2t[e])))
        rho.append(0.5 * (tv[e[0]] + tv[e[1]]))
    return float(np.corrcoef(rho, dl)[0, 1]), len(ep)

# ───────────────────────── RP (réflexions site / lien) ─────────────────────────
def rp_bands(pts, L, rc, N, reflection, K=2):
    x = pts[:, 0]
    if reflection == 'site':
        inP = (x > L/2 + rc) & (x < L - rc); inM = (x > rc) & (x < L/2 - rc)
    else:
        off = 0.5 * rc
        inP = (x > L/2 + off + rc) & (x < L - rc); inM = (x > rc) & (x < L/2 + off - rc)
    cy = np.minimum((pts[:, 1] / L * K).astype(int), K - 1)
    cz = np.minimum((pts[:, 2] / L * K).astype(int), K - 1)
    return inP, inM, cy * K + cz, K

def rp_feats(adj, N, inP, inM, cell, K):
    fP = np.zeros((K*K, 2)); fM = np.zeros((K*K, 2)); nP = np.zeros(K*K); nM = np.zeros(K*K)
    for i in range(N):
        if inP[i]: nP[cell[i]] += 1
        elif inM[i]: nM[cell[i]] += 1
    for u in adj:
        for v in adj[u]:
            if v > u:
                if inP[u] and inP[v]:
                    cc = len([w for w in adj[u] & adj[v] if inP[w]])
                    fP[cell[u],0] += .5; fP[cell[v],0] += .5; fP[cell[u],1] += cc*.5; fP[cell[v],1] += cc*.5
                elif inM[u] and inM[v]:
                    cc = len([w for w in adj[u] & adj[v] if inM[w]])
                    fM[cell[u],0] += .5; fM[cell[v],0] += .5; fM[cell[u],1] += cc*.5; fM[cell[v],1] += cc*.5
    fP /= np.maximum(nP[:, None], 1); fM /= np.maximum(nM[:, None], 1)
    return np.concatenate([[1.], fP.ravel()]), np.concatenate([[1.], fM.ravel()])

def safe_mineig(P, Q):
    keep = (P.std(0) > 1e-9) & (Q.std(0) > 1e-9); keep[0] = True
    P = P[:, keep]; Q = Q[:, keep]
    G = (P.T @ Q) / len(P); Gs = 0.5 * (G + G.T); n = Gs.shape[0]
    for reg in (1e-8, 1e-6, 1e-4, 1e-2):
        try: return float(np.linalg.eigvalsh(Gs + reg * np.eye(n))[0] - reg)
        except np.linalg.LinAlgError: continue
    return float(np.min(np.diag(Gs) - (np.abs(Gs).sum(1) - np.abs(np.diag(Gs)))))

def rp_run(get_snap, pts, L, rc, N, reflection='site', M=100, block=10):
    inP, inM, cell, K = rp_bands(pts, L, rc, N, reflection)
    Ps = []; Qs = []
    for m in range(M):
        adj = get_snap(m); a_, b_ = rp_feats(adj, N, inP, inM, cell, K); Ps.append(a_); Qs.append(b_)
    P = np.array(Ps); Q = np.array(Qs)
    me = safe_mineig(P, Q)
    nb = max(5, len(P) // block); rb = np.random.default_rng(11); boots = []
    for _ in range(120):
        bi = rb.integers(0, nb, nb)
        idx = np.concatenate([np.arange(b*block, min((b+1)*block, len(P))) for b in bi])
        boots.append(safe_mineig(P[idx], Q[idx]))
    return me, 3 * float(np.std(boots))

# ═══════════════════════════════ MAIN ═══════════════════════════════
if __name__ == "__main__":
    print(GRILLE)
    print(f"PRESET = {PRESET}  |  {CFG}\n"); t0 = time.time()
    R = {"meta": {"preset": PRESET, "cfg": CFG, "tau": TAU,
                  "action_locale": {"alpha": ALPHA_L, "beta_l": BETAL_L, "dbar": DBAR_L}}}
    def save():
        with open(OUT, "w") as f: json.dump(R, f)
    def el(): return f"({(time.time()-t0)/60:.0f} min)"

    # ── instrument : étalon cube exact ──
    Ac, Nc = exact_cube(17)
    ds_cube = ds_measure(Ac, Nc, 1)
    CAL = 3.0 / ds_cube if ds_cube == ds_cube and ds_cube > 0 else 1.0
    R["instrument"] = {"cube3D_raw": ds_cube, "cal": CAL}; save()
    print(f"instrument : cube3D={ds_cube:.3f} → cal={CAL:.4f}  {el()}\n", flush=True)

    # ─────────── W1 : SIGNATURE TORE COMPLÈTE (6/12/8) ───────────
    print("─── W1 : SIGNATURE TORE — comptage 6/12/8 aux ratios 1/2/3 ───")
    R["W1"] = []
    Ns = CFG["N_SPEC"]
    for seed in (11000, 11001):
        try:
            pts, cand, L, rc, rng = build(Ns, seed)
            adj = init_adj(cand, E_GRAV * Ns, seed); d = degs(adj, Ns)
            adj, d = relax_global(adj, d, cand, 3.0, Ns, seed + 1, CFG["SW"])
            vals = spectrum(adj, Ns, k=30)
            if vals is None:
                print(f"  graine {seed} : spectre non convergé {el()}", flush=True); continue
            lam1 = vals[1]; rat = (vals[1:] / lam1).tolist()
            n1 = int(sum(1 for r in rat if 1.00 <= r <= 1.30))
            n2 = int(sum(1 for r in rat if 1.60 <= r <= 2.40))
            n3 = int(sum(1 for r in rat if 2.60 <= r <= 3.40))
            R["W1"].append({"N": Ns, "seed": seed, "type": "viable", "ratios": rat,
                            "n1": n1, "n2": n2, "n3": n3}); save()
            print(f"  VIABLE  s={seed} : comptage {n1}/{n2}/{n3}  [attendu 6/12/8]  {el()}", flush=True)
            print(f"     ratios : {[f'{r:.3f}' for r in rat[:26]]}", flush=True)
            # ── TÉMOIN 1 : substrat dilué au hasard (topologie héritée du plongement) ──
            adj_r = init_adj(cand, E_GRAV * Ns, seed + 777)
            vr = spectrum(adj_r, Ns, k=30)
            if vr is not None:
                rr = (vr[1:] / vr[1]).tolist()
                m1 = int(sum(1 for r in rr if 1.00 <= r <= 1.30))
                m2 = int(sum(1 for r in rr if 1.60 <= r <= 2.40))
                m3 = int(sum(1 for r in rr if 2.60 <= r <= 3.40))
                R["W1"].append({"N": Ns, "seed": seed, "type": "aleatoire", "ratios": rr,
                                "n1": m1, "n2": m2, "n3": m3}); save()
                print(f"  ALÉA    s={seed} : comptage {m1}/{m2}/{m3}  (héritage du plongement) {el()}", flush=True)
            # ── TÉMOIN 2 : état condensé type L2 (doit DÉTRUIRE la structure de variété) ──
            adj_c = init_adj(cand, E_GRAV * Ns, seed + 999); dc = degs(adj_c, Ns)
            adj_c, dc, _ = relax_local(adj_c, dc, cand, 3.0, 0.0, 10.0, Ns, seed + 998, max(8, CFG["SW"] // 4))
            vc = spectrum(adj_c, Ns, k=30)
            if vc is not None:
                rcz = (vc[1:] / max(vc[1], 1e-12)).tolist()
                q1 = int(sum(1 for r in rcz if 1.00 <= r <= 1.30))
                q2 = int(sum(1 for r in rcz if 1.60 <= r <= 2.40))
                q3 = int(sum(1 for r in rcz if 2.60 <= r <= 3.40))
                R["W1"].append({"N": Ns, "seed": seed, "type": "condense", "ratios": rcz,
                                "n1": q1, "n2": q2, "n3": q3}); save()
                print(f"  CONDENSÉ s={seed}: comptage {q1}/{q2}/{q3}  (doit détruire 6/12/8) {el()}", flush=True)
        except Exception as ex:
            print(f"  graine {seed} ÉCHEC W1 : {ex}", flush=True)

    # ─────────── W2 : CONSTANTES (boussole + N) ───────────
    print("\n─── W2 : CONSTANTES — boussole (plateau + réversibilité) et N-dépendance ───")
    R["W2"] = []
    for Nc2 in CFG["N_CST"]:
        for seed in (12000, 12001):
            try:
                pts, cand, L, rc, rng = build(Nc2, seed)
                # départ phase pure β=3
                adj = init_adj(cand, E_GRAV * Nc2, seed); d = degs(adj, Nc2)
                adj, d = relax_global(adj, d, cand, 3.0, Nc2, seed + 1, CFG["SW"])
                C_start = clustering(adj, Nc2, seed=seed + 2)
                v = spectrum(adj, Nc2, k=6)
                l21 = float(v[2]/v[1]) if v is not None else float('nan')
                l31 = float(v[3]/v[1]) if v is not None else float('nan')
                # traversée β=1,4
                for b in (2.0, 1.4):
                    adj, d = relax_global(adj, d, cand, b, Nc2, seed + 3, max(20, CFG["SW"] - 10))
                C_beyond = clustering(adj, Nc2, seed=seed + 4)
                # retour β=3
                for b in (2.0, 3.0):
                    adj, d = relax_global(adj, d, cand, b, Nc2, seed + 5, max(20, CFG["SW"] - 10))
                C_back = clustering(adj, Nc2, seed=seed + 6)
                # contrôle dilué aléatoire (même |E|)
                adj_r = init_adj(cand, E_GRAV * Nc2, seed + 777)
                C_alea = clustering(adj_r, Nc2, seed=seed + 8)
                rec = {"N": Nc2, "seed": seed, "C_pure": C_start, "C_beyond": C_beyond,
                       "C_back": C_back, "C_alea": C_alea, "ampl": C_start / max(C_alea, 1e-9),
                       "l21": l21, "l31": l31}
                R["W2"].append(rec); save()
                print(f"  N={Nc2} s={seed}: ⟨C⟩={C_start:.4f} (plateau {abs(C_start-C_beyond)/C_start*100:.1f}%, "
                      f"rév {abs(C_back-C_start)/C_start*100:.1f}%)  A={rec['ampl']:.2f}  "
                      f"λ₂/λ₁={l21:.4f} λ₃/λ₁={l31:.4f}  {el()}", flush=True)
            except Exception as ex:
                print(f"  N={Nc2} s={seed} ÉCHEC W2 : {ex}", flush=True)

    # ─────────── W3 : exposant de désordre ───────────
    print("\n─── W3 : DÉSORDRE — exposant de décroissance de l'éclatement intra-couche ───")
    try:
        pts_n = []; d2 = []; d3 = []
        for r in R["W2"]:
            if r["l21"] == r["l21"] and r["l31"] == r["l31"]:
                pts_n.append(r["N"]); d2.append(r["l21"] - 1); d3.append(r["l31"] - 1)
        if len(set(pts_n)) >= 2:
            lx = np.log(np.array(pts_n, dtype=float))
            p2 = float(np.polyfit(lx, np.log(np.maximum(d2, 1e-9)), 1)[0])
            p3 = float(np.polyfit(lx, np.log(np.maximum(d3, 1e-9)), 1)[0])
            R["W3"] = {"exposant_delta2": p2, "exposant_delta3": p3}; save()
            print(f"  δ₂ ~ N^({p2:+.2f})   δ₃ ~ N^({p3:+.2f})   "
                  f"→ {'taille finie (tend vers la dégénérescence du tore)' if min(p2,p3) < -0.3 else 'constantes de désordre'}  {el()}", flush=True)
    except Exception as ex:
        print(f"  W3 ÉCHEC : {ex}", flush=True)

    # ─────────── W4 : POINT FIXE (attracteur) ───────────
    print("\n─── W4 : POINT FIXE DIMENSIONNEL — 2 inits opposées × graines ───")
    R["W4"] = []
    Nf = CFG["N_FIX"]
    for seed in (13000, 13001):
        try:
            pts, cand, L, rc, rng = build(Nf, seed)
            out = {}
            for label, mk in (("dense", lambda: init_adj(cand, int(E_DIMS * Nf), seed)),
                              ("sparse", lambda: init_sparse(cand, int(E_DIMS * Nf), Nf, seed))):
                adj = mk(); d = degs(adj, Nf)
                ds0 = ds_measure(adj, Nf, seed, CAL)
                adj, d, _ = relax_local(adj, d, cand, ALPHA_L, BETAL_L, DBAR_L, Nf, seed + 1, CFG["SW"] + 10)
                ds1 = ds_measure(adj, Nf, seed, CAL)
                out[label] = (ds0, ds1)
            ecart = abs(out["dense"][1] - out["sparse"][1]) / max(out["dense"][1], 1e-9) * 100
            R["W4"].append({"N": Nf, "seed": seed, "dense": out["dense"], "sparse": out["sparse"],
                            "ecart_pct": ecart}); save()
            print(f"  N={Nf} s={seed}: dense {out['dense'][0]:.2f}→{out['dense'][1]:.3f} | "
                  f"sparse {out['sparse'][0]:.2f}→{out['sparse'][1]:.3f} | écart {ecart:.1f}%  "
                  f"{'✓ attracteur' if ecart < 5 else ''}  {el()}", flush=True)
        except Exception as ex:
            print(f"  s={seed} ÉCHEC W4 : {ex}", flush=True)

    # ─────────── W5 : MUR UNIFIÉ (ξ, χ, RP ensemble) ───────────
    print("\n─── W5 : MUR UNIFIÉ — ξ, χ et RP sur balayage fin de β ───")
    R["W5"] = []
    Nm = CFG["N_MUR"]
    try:
        pts, cand, L, rc, rng = build(Nm, 14000)
        for beta in (2.60, 2.20, 1.90, 1.70, 1.55, 1.40, 1.30):
            adj = init_adj(cand, E_GRAV * Nm, 14000); d = degs(adj, Nm)
            adj, d = relax_global(adj, d, cand, beta, Nm, 14001, CFG["SW"])
            xi = corr_length(adj, d, Nm, 14002)
            chi = float(np.var(d.astype(float)))
            state = {"adj": adj, "d": d}
            def snapg(m, st=state, cc=cand, nn=Nm, bb=beta):
                st["adj"], st["d"] = relax_global(st["adj"], st["d"], cc, bb, nn, 14100 + m, 1)
                return st["adj"]
            me, tol = rp_run(snapg, pts, L, rc, Nm, 'site', M=max(30, CFG["MRP"] // 3))
            R["W5"].append({"beta": beta, "xi": xi, "chi": chi, "rp_mineig": me, "rp_tol": tol}); save()
            print(f"  β={beta:.2f}: ξ={xi:.2f}  χ={chi:.2f}  |RP|={abs(me):.2f}  {el()}", flush=True)
    except Exception as ex:
        print(f"  W5 ÉCHEC : {ex}", flush=True)

    # ─────────── W6 : ACTION LOCALE À GRAND N ───────────
    print("\n─── W6 : ACTION LOCALE — d_s, RP site+lien, gravité à grand N ───")
    R["W6"] = []
    Nl = CFG["N_LOC"]
    for seed in (15000, 15001):
        try:
            pts, cand, L, rc, rng = build(Nl, seed)
            adj = init_adj(cand, int(E_DIMS * Nl), seed); d = degs(adj, Nl)
            adj, d, acc = relax_local(adj, d, cand, ALPHA_L, BETAL_L, DBAR_L, Nl, seed + 1, CFG["SW"] + 15)
            ds = ds_measure(adj, Nl, seed, CAL)
            state = {"adj": adj, "d": d}
            def snapl(m, st=state, cc=cand, nn=Nl, sd=seed):
                st["adj"], st["d"], _ = relax_local(st["adj"], st["d"], cc, ALPHA_L, BETAL_L, DBAR_L, nn, sd + 200 + m, 1)
                return st["adj"]
            meS, tolS = rp_run(snapl, pts, L, rc, Nl, 'site', M=CFG["MRP"])
            meL, tolL = rp_run(snapl, pts, L, rc, Nl, 'link', M=max(40, CFG["MRP"] * 2 // 3))
            # gravité au régime deg-10
            adjg = init_adj(cand, E_GRAV * Nl, seed + 5); dg = degs(adjg, Nl)
            adjg, dg, _ = relax_local(adjg, dg, cand, 0.72, 0.20, 10.0, Nl, seed + 6, CFG["SW"])
            rt, nep = rtet(adjg, pts, L, Nl, seed + 7)
            R["W6"].append({"N": Nl, "seed": seed, "d_s": ds, "site": meS, "site_tol": tolS,
                            "link": meL, "link_tol": tolL, "r_tet": rt, "acc": acc}); save()
            print(f"  N={Nl} s={seed}: d_s={ds:.3f} | RP site={meS:+.4f}(tol {tolS:.4f}) "
                  f"link={meL:+.4f}(tol {tolL:.4f}) | r_tet={rt:+.3f}  {el()}", flush=True)
        except Exception as ex:
            print(f"  N={Nl} s={seed} ÉCHEC W6 : {ex}", flush=True)

    # ─────────────────── SYNTHÈSE ───────────────────
    print(f"\n════════════ SYNTHÈSE PASSE COMPLÈTE ({(time.time()-t0)/60:.0f} min) ════════════")
    if R.get("W1"):
        cnt = [(r["n1"], r["n2"], r["n3"]) for r in R["W1"]]
        print(f"  W1 tore : comptages {cnt}  [attendu (6,12,8)]")
    if R.get("W2"):
        Cs = [r["C_pure"] for r in R["W2"]]; A = [r["ampl"] for r in R["W2"]]
        print(f"  W2 ⟨C⟩ = {np.mean(Cs):.4f} ± {np.std(Cs):.4f} (toutes tailles) | amplification A = {np.mean(A):.2f} ± {np.std(A):.2f}")
        for Nc2 in sorted(set(r["N"] for r in R["W2"])):
            v = [r["C_pure"] for r in R["W2"] if r["N"] == Nc2]
            print(f"     N={Nc2}: ⟨C⟩={np.mean(v):.4f}")
    if R.get("W4"):
        ec = [r["ecart_pct"] for r in R["W4"]]
        print(f"  W4 attracteur : écart dense/sparse = {np.mean(ec):.1f}% (max {max(ec):.1f}%)")
    if R.get("W5"):
        bx = max(R["W5"], key=lambda r: (r["xi"] if r["xi"] == r["xi"] else -1))["beta"]
        bc = max(R["W5"], key=lambda r: r["chi"])["beta"]
        br = max(R["W5"], key=lambda r: abs(r["rp_mineig"]))["beta"]
        print(f"  W5 pics : ξ@β={bx} | χ@β={bc} | RP@β={br} → "
              f"{'✓✓ COÏNCIDENCE (unification mur/criticité/quantique)' if max(bx,bc,br)-min(bx,bc,br) <= 0.15 else 'pics distincts — tel quel'}")
    if R.get("W6"):
        print(f"  W6 action locale : " + " | ".join(
            f"N={r['N']} d_s={r['d_s']:.3f} site={abs(r['site'])/max(r['site_tol'],1e-9):.2f}·tol "
            f"link={abs(r['link'])/max(r['link_tol'],1e-9):.2f}·tol r_tet={r['r_tet']:+.2f}" for r in R["W6"]))
    print(f"\n  Résultats complets : {OUT}")
    save()
