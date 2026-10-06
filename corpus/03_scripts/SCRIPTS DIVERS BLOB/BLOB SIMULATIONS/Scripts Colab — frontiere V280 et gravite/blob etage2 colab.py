#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — ÉTAGE 2 : VÉRIFICATION LOURDE DU CANDIDAT FENÊTRE (β* = 2 et β = 4)
# Protocole pré-enregistré. Version 1.0 — 15 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# CONTEXTE : le scan de phase (N=6000, 30 points) a CONFIRMÉ la fenêtre
# variété+gravité : β*=2 (f_nv=0,014, r_eq=+0,592) et β=4 (f_nv=0,0007,
# r_eq=+0,547) — et l'énumération exacte micro donne β_RP ≈ 4 au même endroit.
# RÉSERVE MAJEURE (raison d'être de ce run) : toutes les preuves de géométrie
# 3D (d_s=3,002, d_w=2, gaussianité) ont été établies à β=0,30. À β*, la
# matière est deux fois plus rare. CE RUN TRANCHE : la dimension tient-elle ?
# CE QUE CE SCRIPT MESURE, par (β, graine), à N = 3×10⁵ :
#   E1. d_s (instrument GELÉ, contrôles exacts embarqués inchangés) + d_H (indicatif)
#   E2. d_w + gaussianité du Blob ÉQUILIBRÉ (marche déroulée) — verrouille
#       SUP-1 côté graphe de Gibbs (fenêtre ENFIN suffisante : (L/2)² ≈ 33)
#   E3. f_nv, part_m, med_m, certificat links (cycle/chemin) au grand N
#   E4. fait A (r_eq vs dilué) au grand N
# Blocs d_s/d_H/équilibrage : repris à l'IDENTIQUE du script limite continue
# (instrument validé sur étalons, d_s(β=0,3)=3,002±0,034 hier).
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback, warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import scipy.sparse as sp
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from collections import deque

# ───────────────────────── PARAMÈTRES ─────────────────────────
N          = 300_000
BETAS      = [2.0, 4.0]
SEEDS      = [31, 32, 33]     # 3 graines/β (réduire à [31, 32] si le temps manque)
DENSITY    = 200.0
KAPPA      = 10.0
RCUT       = 1.6
TAU        = 0.5
E_PER_N    = 5
SWEEPS_EQ  = 15
NSRC       = 24
TMAX       = 2000
K_WALK     = 8000             # marcheurs d_w/gaussianité
T_WALK     = 1500
NV_THRESH  = 10
EDGE_SAMPLE= 2500
OUT_JSON   = "etage2_results.json"

TMIN_DS = 20; THRESH_DS = 50.0; MINPTS_DS = 8
BMAX_FRAC = 4; MINPTS_DH = 4
BETA = 2.0                    # réassigné par point

GRID = """
════════════════ GRILLES PRÉ-ENREGISTRÉES (gravées AVANT lecture) ════════════════
CONTRÔLES EMBARQUÉS (inchangés — doivent passer, sinon ABORT) :
  cube 3D exact : d_s ∈ [2,95 ; 3,10] · carré 2D exact : d_s ∈ [1,95 ; 2,08]
E1 (LA QUESTION — la dimension tient-elle dans la fenêtre ?) :
  d_s(Blob, β) ∈ [2,85 ; 3,15] par β.
  → ✓ aux deux β : « le Blob possède un point de fonctionnement où géométrie
    3D + quasi-variété + gravité + (RP micro) coexistent » — mesure propre, pas [T].
  → ✓ à 2, ✗ à 4 : la fenêtre se referme côté dimension entre 2 et 4 — tel quel.
  → ✗ partout avec dilué ✓ : la dimension 3 dépendait de la dynamique condensée
    — verdict majeur inverse, tel quel.
  d_H rapporté à titre INDICATIF (biais transitoire +0,1/+0,2 démontré hier).
E2 (SUP-1 sur Gibbs — le verrou) : d_w(équilibré) ∈ [1,90 ; 2,11] ET
  gaussianité V2 (⟨kurt⟩ ∈ 3±3SE/3 ; max|k−3| < 4SE ; ⟨Q⟩ ∈ [0,80 ; 1,20]).
  ✓ → les deux conditions du PIT mesurées sur le graphe de GIBBS à grand N.
E3 (variété au grand N) : β=2 : f_nv ≤ 0,02 et links(cycle+chemin) ≥ 40 % ;
  β=4 : f_nv ≤ 0,002. Hors bande → dépendance de taille, tel quel.
E4 (gravité au grand N) : r_eq ≥ 0,50 et |r_rand| ≤ 0,2 aux deux β.
Tout écart se lit tel quel. Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

TGRID = np.unique(np.round(np.logspace(0, math.log10(TMAX), 70)).astype(int))

# ─────────────── INSTRUMENT GELÉ : d_s / d_H (identique 14/07) ───────────────
def fit_ds(pminus, Ngraph):
    ok = (TGRID >= TMIN_DS) & (pminus > THRESH_DS / Ngraph)
    npts = int(ok.sum())
    if npts < MINPTS_DS:
        return float("nan"), npts, (float("nan"), float("nan"))
    x = np.log(TGRID[ok]); y = np.log(pminus[ok])
    ls = -2 * np.diff(y) / np.diff(x)
    return float(-2 * np.polyfit(x, y, 1)[0]), npts, (float(ls.min()), float(ls.max()))

def ds_walk(A, nsrc=NSRC, seed=0):
    Ng = A.shape[0]
    deg = np.asarray(A.sum(1)).ravel()
    Pi = deg / deg.sum()
    rng = np.random.default_rng(seed)
    src = rng.choice(Ng, size=nsrc, replace=False)
    X = np.zeros((Ng, nsrc)); X[src, np.arange(nsrc)] = 1.0
    invd = 1.0 / deg
    rec = np.zeros(len(TGRID)); tj = 0
    for t in range(1, TGRID[-1] + 1):
        X = 0.5 * (X + invd[:, None] * (A @ X))
        if tj < len(TGRID) and t == TGRID[tj]:
            rec[tj] = float(np.mean(X[src, np.arange(nsrc)] - Pi[src])); tj += 1
    return rec, Ng

def bfs_dH(A, nsrc=NSRC, seed=0):
    Ng = A.shape[0]; ip, ix = A.indptr, A.indices
    rng = np.random.default_rng(seed)
    src = rng.choice(Ng, size=nsrc, replace=False)
    rmax = 120; counts = np.zeros(rmax + 1)
    for s in src:
        dist = np.full(Ng, -1, dtype=np.int32); dist[s] = 0; dq = deque([s])
        while dq:
            u = dq.popleft()
            for v in ix[ip[u]:ip[u + 1]]:
                if dist[v] < 0:
                    dist[v] = dist[u] + 1; dq.append(v)
        h = np.bincount(dist[dist >= 0]); cum = np.cumsum(h)
        m = min(len(cum), rmax + 1)
        counts[:m] += cum[:m]; counts[m:] += cum[-1]
    B = counts / nsrc
    rstar = 2
    while rstar + 1 <= rmax and B[rstar + 1] <= Ng / BMAX_FRAC:
        rstar += 1
    rs = np.arange(2, rstar + 1)
    if len(rs) < MINPTS_DH:
        return float("nan"), rstar, float("nan")
    best = (1e18, float("nan"), float("nan"))
    for aoff in np.arange(0.0, 2.01, 0.05):
        x = np.log(rs + aoff); y = np.log(B[2:rstar + 1])
        p = np.polyfit(x, y, 1)
        res = float(((np.polyval(p, x) - y) ** 2).sum())
        if res < best[0]:
            best = (res, float(p[0]), float(aoff))
    return best[1], rstar, best[2]

def torus_exact(L, dim):
    c = np.cos(2 * np.pi * np.arange(L) / L)
    lam = (c[:, None, None] + c[None, :, None] + c[None, None, :]).ravel() / 3.0 \
        if dim == 3 else (c[:, None] + c[None, :]).ravel() / 2.0
    lz = (1.0 + lam) / 2.0
    lz = lz[lz < 1.0 - 1e-12]
    Ng = L ** dim
    pm = (np.power(lz[:, None], TGRID[None, :].astype(float))).sum(0) / Ng
    return Ng, pm

def embedded_controls():
    N3, pm3 = torus_exact(50, 3); ds3, n3, _ = fit_ds(pm3, N3)
    N2, pm2 = torus_exact(160, 2); ds2, n2, _ = fit_ds(pm2, N2)
    print(f"CONTRÔLE cube 3D exact  : d_s = {ds3:.3f} ({n3} pts)  [requis 2,95–3,10]")
    print(f"CONTRÔLE carré 2D exact : d_s = {ds2:.3f} ({n2} pts)  [requis 1,95–2,08]")
    if not ((2.95 <= ds3 <= 3.10) and (1.95 <= ds2 <= 2.08)):
        print("✗✗ CONTRÔLE ÉCHOUÉ — ABORT."); sys.exit(1)
    print("✓ Contrôles embarqués passés.\n")

# ─────────────── GÉOMÉTRIE + ÉQUILIBRAGE (identiques, β paramétré) ───────────────
def build_pool(seed):
    rng = np.random.default_rng(seed)
    L = (N / DENSITY) ** (1 / 3)
    pts = rng.uniform(0, L, size=(N, 3))
    rc = RCUT * (3 * KAPPA / (4 * math.pi * DENSITY)) ** (1 / 3)
    tree = cKDTree(pts, boxsize=L)
    cand = tree.query_pairs(rc, output_type="ndarray")
    return pts, cand, L

def adj_from_active(cand, active_idx):
    adj = [set() for _ in range(N)]
    for k in active_idx:
        a, b = int(cand[k, 0]), int(cand[k, 1])
        adj[a].add(b); adj[b].add(a)
    return adj

def count_T(adj):
    t = 0
    for u in range(N):
        au = adj[u]
        for v in au:
            if v > u:
                t += len(au & adj[v])
    return t // 3

def equilibrate(adj, cand, seed, sweeps):
    rng = np.random.default_rng(seed + 7)
    te = TAU / N
    edge_list = [(i, j) for i in range(N) for j in adj[i] if j > i]
    E = len(edge_list)
    nt = count_T(adj)
    deg = np.array([len(a) for a in adj], dtype=np.int64)
    S2 = int((deg.astype(np.int64) ** 2).sum())
    mu = 2.0 * E / N
    def cv(s2):
        v = s2 / N - mu * mu
        return math.sqrt(v if v > 0 else 0.0) / mu
    npool = len(cand); acc = 0
    for sw in range(sweeps):
        for _ in range(3 * N):
            io = rng.integers(E); u, v = edge_list[io]
            ii = rng.integers(npool); a, b = int(cand[ii, 0]), int(cand[ii, 1])
            if b in adj[a] or v not in adj[u]: continue
            if len({u, v, a, b}) < 4: continue
            if deg[u] <= 2 or deg[v] <= 2: continue
            t_rm = len(adj[u] & adj[v])
            adj[u].discard(v); adj[v].discard(u)
            t_add = len(adj[a] & adj[b])
            dT = t_add - t_rm
            d2n = S2 + (-2 * deg[u] + 1) + (-2 * deg[v] + 1) + (2 * deg[a] + 1) + (2 * deg[b] + 1)
            dS = (math.log(1 + nt + dT) - math.log(1 + nt)) - BETA * (cv(d2n) - cv(S2))
            if dS >= 0 or rng.random() < math.exp(dS / te):
                adj[a].add(b); adj[b].add(a)
                deg[u] -= 1; deg[v] -= 1; deg[a] += 1; deg[b] += 1
                S2 = d2n; nt += dT; edge_list[io] = (a, b); acc += 1
            else:
                adj[u].add(v); adj[v].add(u)
        e_now = sum(len(s) for s in adj) // 2
        assert e_now == E, f"|E| VIOLÉ au sweep {sw}"
        print(f"    sweep {sw+1}/{sweeps} : T={nt}  CV={cv(S2):.4f}  acc={acc}", flush=True)
    return adj, nt, cv(S2)

def to_giant_csr(adj):
    rows = []; cols = []
    for i in range(N):
        for j in adj[i]:
            if j > i:
                rows.append(i); cols.append(j)
    A = sp.csr_matrix((np.ones(len(rows)), (np.array(rows), np.array(cols))), shape=(N, N))
    A = ((A + A.T) > 0).astype(float).tocsr()
    _, lab = connected_components(A, directed=False)
    keep = np.where(lab == np.bincount(lab).argmax())[0]
    return A[keep][:, keep].tocsr(), keep

# ─────────────── E2 : d_w + GAUSSIANITÉ (Gibbs, déroulé) ───────────────
def walk_msd_gauss(A, pts_g, L, seed):
    ip, ix = A.indptr, A.indices
    Ng = A.shape[0]
    r2 = np.random.default_rng(seed)
    u = r2.choice(Ng, size=K_WALK)
    X = np.zeros((K_WALK, 3))
    deg = (ip[1:] - ip[:-1])
    tg = np.unique(np.round(np.logspace(0, math.log10(T_WALK), 40)).astype(int))
    msd = np.zeros(len(tg)); tj = 0; snaps = {}
    for t in range(1, T_WALK + 1):
        r = (r2.random(K_WALK) * deg[u]).astype(np.int64)
        v = ix[ip[u] + r]
        dl = pts_g[v] - pts_g[u]; dl -= L * np.round(dl / L)
        X += dl; u = v
        if tj < len(tg) and t == tg[tj]:
            msd[tj] = float((X ** 2).sum(1).mean()); tj += 1
        if t in (300, 800, 1500): snaps[t] = X.copy()
    cap = (L / 2) ** 2
    ok = (tg >= 20) & (msd < cap)
    if ok.sum() >= 8:
        sl = float(np.polyfit(np.log(tg[ok]), np.log(msd[ok]), 1)[0]); dw = 2.0 / sl
    else:
        dw = float("nan")
    SEk = math.sqrt(24.0 / K_WALK)
    ks = []; Qs = []
    tstar = int(tg[ok][-1]) if ok.sum() else 0
    for t, Xs in snaps.items():
        if t > max(tstar, 300): continue
        for c in range(3):
            x = Xs[:, c]; s = x.std()
            ks.append(float(((x - x.mean()) ** 4).mean() / s ** 4))
            Qs.append(float((np.abs(x - x.mean()) > 3 * s).mean() / 0.0027))
    ks = np.array(ks); Qs = np.array(Qs)
    gpass = (len(ks) >= 3 and abs(ks.mean() - 3) < 3 * SEk / math.sqrt(len(ks))
             and np.abs(ks - 3).max() < 4 * SEk and 0.80 <= Qs.mean() <= 1.20)
    return dw, int(ok.sum()), tstar, float(ks.mean()) if len(ks) else float("nan"), \
           float(Qs.mean()) if len(Qs) else float("nan"), bool(gpass)

# ─────────────── E3 + E4 : STRUCTURE (f_nv, links) + GRAVITÉ (r_eq) ───────────────
def dihedral(pts, L, tet, edge):
    e0, e1 = edge; oth = [x for x in tet if x not in edge]
    ax = pts[e1] - pts[e0]; ax -= L * np.round(ax / L)
    n = np.linalg.norm(ax); ax = ax / max(n, 1e-12)
    vs = []
    for o in oth:
        po = pts[o] - pts[e0]; po -= L * np.round(po / L)
        pp = po - np.dot(po, ax) * ax
        vs.append(pp / max(np.linalg.norm(pp), 1e-12))
    return math.acos(np.clip(np.dot(vs[0], vs[1]), -1, 1))

def structure_and_gravity(adj, deg, pts, L, rng):
    """m_tet par arête (exact), f_nv, part_m, med_m, certificat links,
    et r_eq (échantillon EDGE_SAMPLE d'arêtes m_tet ≥ 2)."""
    A = sp.csr_matrix((np.ones(sum(len(a) for a in adj)),
                       ([i for i in range(N) for _ in adj[i]],
                        [j for i in range(N) for j in adj[i]])), shape=(N, N))
    A = ((A + A.T) > 0).astype(np.int8).tocsr()
    C = (A @ A).multiply(A)            # m_tri par arête (voisins communs)
    Cu = sp.triu(C, k=1).tocoo()
    cand_e = [(int(a), int(b)) for a, b, m in zip(Cu.row, Cu.col, Cu.data) if m >= 2]
    E_tot = E_PER_N * N
    m_tet = {}; links = {}
    for (a, b) in cand_e:
        W = adj[a] & adj[b]
        le = []
        for w in W:
            for x in adj[w] & W:
                if x > w: le.append((w, x))
        if len(le) >= 1:
            m_tet[(a, b)] = len(le)
            links[(a, b)] = le
    ms = np.array([m for m in m_tet.values() if m >= 2])
    f_nv = float((ms > NV_THRESH).sum()) / E_tot if len(ms) else 0.0
    part_m = float(ms[ms > NV_THRESH].sum()) / max(float(ms.sum()), 1.0) if len(ms) else 0.0
    med_m = float(np.median(ms)) if len(ms) else float("nan")
    # certificat links (cycle/chemin) sur arêtes m_tet ≥ 2
    ncyc = npath = noth = 0
    keys2 = [e for e, m in m_tet.items() if m >= 2]
    for e in keys2:
        le = links[e]
        dl = {}
        for (w, x) in le:
            dl[w] = dl.get(w, 0) + 1; dl[x] = dl.get(x, 0) + 1
        vs = set(dl)
        adjl = {}
        for (w, x) in le:
            adjl.setdefault(w, set()).add(x); adjl.setdefault(x, set()).add(w)
        start = next(iter(vs)); seen = {start}; st = [start]
        while st:
            u2 = st.pop()
            for v2 in adjl.get(u2, ()):
                if v2 not in seen: seen.add(v2); st.append(v2)
        conn = seen == vs
        dgs = sorted(dl.values())
        if conn and all(d == 2 for d in dgs) and len(le) == len(vs): ncyc += 1
        elif conn and dgs.count(1) == 2 and all(d <= 2 for d in dgs): npath += 1
        else: noth += 1
    link_frac = (ncyc + npath) / max(len(keys2), 1)
    # E4 : r_eq sur échantillon (dièdres)
    samp = keys2 if len(keys2) <= EDGE_SAMPLE else \
        [keys2[i] for i in rng.choice(len(keys2), size=EDGE_SAMPLE, replace=False)]
    xs = []; ys = []
    for (a, b) in samp:
        W = adj[a] & adj[b]
        tot = 0.0
        for (w, x) in links[(a, b)]:
            tot += dihedral(pts, L, (a, b, w, x), (a, b))
        d = 2 * math.pi - tot
        xs.append(float(deg[a] + deg[b])); ys.append(abs(d))
    r_eq = float(np.corrcoef(xs, ys)[0, 1]) if len(xs) > 30 and np.std(xs) > 0 else float("nan")
    return f_nv, part_m, med_m, link_frac, r_eq, len(keys2)

# ─────────────── PIPELINE PAR (β, graine) ───────────────
def run_point(beta, seed):
    global BETA
    BETA = beta
    res = {"beta": beta, "seed": seed, "N": N}
    t1 = time.time()
    pts, cand, L = build_pool(seed)
    E0 = E_PER_N * N
    assert len(cand) > E0
    rng = np.random.default_rng(seed)
    init = rng.choice(len(cand), size=E0, replace=False)
    adj = adj_from_active(cand, init)
    print(f"  équilibrage β={beta} ({SWEEPS_EQ} sweeps)…", flush=True)
    adj, T_eq, CV_eq = equilibrate(adj, cand, seed, SWEEPS_EQ)
    res["T_eq"] = int(T_eq); res["CV_eq"] = float(CV_eq)
    deg = np.array([len(a) for a in adj], dtype=np.int64)
    A_eq, keep = to_giant_csr(adj)
    res["giant"] = int(len(keep))
    # E1 : d_s / d_H
    pm, Ng = ds_walk(A_eq, seed=seed)
    ds, npts, loc = fit_ds(pm, Ng)
    dh, rstar, _ = bfs_dH(A_eq, seed=seed)
    res.update({"ds": ds, "ds_pts": npts, "ds_loc": list(loc), "dh": dh,
                "dh_rstar": int(rstar), "pm": pm.tolist()})
    # E2 : d_w + gaussianité (Gibbs)
    dw, nw, tstar, kmean, qmean, gpass = walk_msd_gauss(A_eq, pts[keep], L, seed + 5)
    res.update({"dw": dw, "dw_pts": nw, "t_star": tstar,
                "kurt_mean": kmean, "Q_mean": qmean, "gauss_pass": gpass})
    # E3 + E4 : structure + gravité
    f_nv, part_m, med_m, lfrac, r_eq, n2 = structure_and_gravity(adj, deg, pts, L, rng)
    res.update({"f_nv": f_nv, "part_m": part_m, "med_m": med_m,
                "link_frac": lfrac, "r_eq": r_eq, "n_edges_tet": n2})
    # témoin dilué (r_rand + d_s dilué, une fois)
    adj_d = adj_from_active(cand, np.random.default_rng(seed + 77).choice(len(cand), size=E0, replace=False))
    deg_d = np.array([len(a) for a in adj_d], dtype=np.int64)
    _, _, _, _, r_rand, _ = structure_and_gravity(adj_d, deg_d, pts, L, np.random.default_rng(seed + 3))
    res["r_rand"] = r_rand
    res["minutes"] = (time.time() - t1) / 60.0
    return res

# ───────────────────────── MAIN ─────────────────────────
if __name__ == "__main__":
    print(GRID)
    print(f"Environnement : python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"N={N}, β ∈ {BETAS} × graines {SEEDS}, τ={TAU}, |E|={E_PER_N}N, sweeps={SWEEPS_EQ}\n")
    embedded_controls()
    all_res = []
    t0 = time.time()
    for beta in BETAS:
        for sd in SEEDS:
            print(f"[β={beta} seed={sd}]", flush=True)
            try:
                r = run_point(beta, sd)
                all_res.append(r)
                print(f"  → d_s={r['ds']:.3f} ({r['ds_pts']} pts)  d_w={r['dw']:.2f} ({r['dw_pts']} pts, t*={r['t_star']})  "
                      f"gauss={'✓' if r['gauss_pass'] else '✗'} (⟨k⟩={r['kurt_mean']:.3f})", flush=True)
                print(f"    f_nv={r['f_nv']:.5f}  med_m={r['med_m']:.0f}  links={100*r['link_frac']:.0f}%  "
                      f"r_eq={r['r_eq']:+.3f} vs r_rand={r['r_rand']:+.2f}  [{r['minutes']:.0f} min]", flush=True)
            except Exception as ex:
                print(f"  ✗ échec : {ex}", flush=True)
                traceback.print_exc()
                all_res.append({"beta": beta, "seed": sd, "error": str(ex)})
            with open(OUT_JSON, "w") as f:
                json.dump(all_res, f)
    # ─── LECTURE AUTOMATIQUE ───
    ok = [r for r in all_res if "ds" in r]
    print(f"\n════════ LECTURE ({(time.time()-t0)/60:.0f} min) ════════")
    for beta in BETAS:
        s = [r for r in ok if r["beta"] == beta]
        if not s: continue
        g = lambda k: np.array([r[k] for r in s], float)
        E1 = 2.85 <= np.nanmean(g("ds")) <= 3.15
        E2 = (1.90 <= np.nanmean(g("dw")) <= 2.11) and all(r["gauss_pass"] for r in s)
        E3 = (np.nanmean(g("f_nv")) <= (0.02 if beta == 2.0 else 0.002)) and \
             (np.nanmean(g("link_frac")) >= 0.40 if beta == 2.0 else True)
        E4 = (np.nanmean(g("r_eq")) >= 0.50) and abs(np.nanmean(g("r_rand"))) <= 0.2
        print(f"β={beta}: d_s={np.nanmean(g('ds')):.3f}±{np.nanstd(g('ds')):.3f} "
              f"d_w={np.nanmean(g('dw')):.2f} f_nv={np.nanmean(g('f_nv')):.5f} "
              f"links={100*np.nanmean(g('link_frac')):.0f}% r_eq={np.nanmean(g('r_eq')):+.3f}")
        print(f"   E1 dimension {'✓' if E1 else '✗'} | E2 SUP-1 Gibbs {'✓' if E2 else '✗'} | "
              f"E3 variété {'✓' if E3 else '✗'} | E4 gravité {'✓' if E4 else '✗'}")
        if E1 and E2 and E3 and E4:
            print(f"   ★★★ β={beta} : POINT DE FONCTIONNEMENT COMPLET — géométrie 3D + "
                  f"quasi-variété + gravité + (RP micro) COEXISTENT. Mesure propre, pas [T].")
    print(f"\nRésultats complets : {OUT_JSON}")
