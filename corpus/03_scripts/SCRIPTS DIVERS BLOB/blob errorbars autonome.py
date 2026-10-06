"""
================================================================================
 BLOB — BARRES D'ERREUR sur d_w a grand N  (multi-graines, AUTONOME)
================================================================================
 Entierement autonome : tout le moteur (numba) est embarque, AUCUN import d'un
 autre fichier. Une seule cellule Colab suffit.

 Pourquoi : le balayage single-seed a atteint son plancher de bruit — la baisse
 de d_w par decade (~0.05-0.10) est devenue comparable a la dispersion
 graine-a-graine, donc on ne peut plus distinguer "recouvrement lent vers 2" de
 "plateau a ~2.5". Ce script mesure d_w avec un ECART-TYPE en relancant plusieurs
 GRAINES par taille, a une echelle relative fixe (0.15*diam), pour trancher.

 Lecture :
   - d_w(N) baisse de plus de ~2*sigma d'une taille a l'autre -> trend REEL
     (recouvrement si ca continue vers 2 ; anomalie si ca se fige a ~2.5) ;
   - d_w(N) se recouvrent dans les barres d'erreur -> bruit (plateau probable).

 USAGE COLAB :
   !pip -q install numba
   # coller ce fichier dans une cellule, ou %run blob_errorbars.py
 Regler N_LIST / N_SEEDS ci-dessous. Commencer par [250000], 8 graines.
================================================================================
"""
import time, math, json
import numpy as np
from numba import njit
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix

# =============================== CONFIG =======================================
N_LIST    = [250_000]   # tailles a tester (commencer par 250k, le moins cher)
N_SEEDS   = 8           # graines par taille (>=6 pour un ecart-type fiable)
REL_SCALE = 0.15        # echelle relative ou lire d_w (le creux diffusif)

KAPPA     = 6.6
BETA      = 0.30
TAU       = 0.50
THERM_FAC = 130         # pas de thermalisation = THERM_FAC * N
POOL_FAC  = 1.6
CAP       = 64
N_SRC_DF  = 200
N_START   = 48
T_CAP     = 3000
N_CHUNKS  = 13
# Astuce cout : 500k -> mettre N_SEEDS=4-5 ; 1M trop cher en multi-seed.
# ==============================================================================


# ----------------------------- NUMBA : graphe --------------------------------
@njit(cache=True)
def build_nbr_arrays(edges, N, cap):
    nbr = np.full((N, cap), -1, dtype=np.int32)
    deg = np.zeros(N, dtype=np.int32)
    for e in range(edges.shape[0]):
        a = edges[e, 0]; b = edges[e, 1]
        if deg[a] < cap:
            nbr[a, deg[a]] = b; deg[a] += 1
        if deg[b] < cap:
            nbr[b, deg[b]] = a; deg[b] += 1
    return nbr, deg


@njit(cache=True, inline='always')
def _has_edge(nbr, deg, a, b):
    for k in range(deg[a]):
        if nbr[a, k] == b:
            return True
    return False


@njit(cache=True, inline='always')
def _common(nbr, deg, u, v):
    c = 0
    for k in range(deg[u]):
        x = nbr[u, k]
        for m in range(deg[v]):
            if nbr[v, m] == x:
                c += 1
                break
    return c


@njit(cache=True, inline='always')
def _remove(nbr, deg, u, v):
    du = deg[u]
    for k in range(du):
        if nbr[u, k] == v:
            nbr[u, k] = nbr[u, du - 1]
            nbr[u, du - 1] = -1
            deg[u] = du - 1
            return


@njit(cache=True, inline='always')
def _add(nbr, deg, a, b, cap):
    if deg[a] < cap:
        nbr[a, deg[a]] = b; deg[a] += 1
    if deg[b] < cap:
        nbr[b, deg[b]] = a; deg[b] += 1


@njit(cache=True)
def n_triangles(nbr, deg, N):
    tot = 0
    for u in range(N):
        for k in range(deg[u]):
            v = nbr[u, k]
            if v > u:
                tot += _common(nbr, deg, u, v)
    return tot // 3


@njit(cache=True)
def mcmc_chunk(nbr, deg, edge_u, edge_v, pool_a, pool_b,
               beta, tau_eff, mean, nt0, nsteps, cap, seed):
    np.random.seed(seed)
    N = deg.shape[0]
    E = edge_u.shape[0]
    P = pool_a.shape[0]
    nt = nt0
    sumsq = 0.0
    for i in range(N):
        sumsq += deg[i] * deg[i]
    cv = math.sqrt(max(sumsq / N - mean * mean, 0.0)) / mean
    S = math.log(1.0 + nt) - beta * cv
    for _ in range(nsteps):
        io = np.random.randint(0, E)
        u = edge_u[io]; v = edge_v[io]
        if deg[u] <= 2 or deg[v] <= 2:
            continue
        a = -1; b = -1; ok = False
        for _try in range(40):
            pi = np.random.randint(0, P)
            ca = pool_a[pi]; cb = pool_b[pi]
            if ca == u or ca == v or cb == u or cb == v:
                continue
            if deg[ca] >= cap or deg[cb] >= cap:
                continue
            if not _has_edge(nbr, deg, ca, cb):
                a = ca; b = cb; ok = True; break
        if not ok:
            continue
        tl = _common(nbr, deg, u, v)
        tg = _common(nbr, deg, a, b)
        nt2 = nt - tl + tg
        du = deg[u]; dv = deg[v]; da = deg[a]; db = deg[b]
        nss = sumsq + (-2 * du + 1) + (-2 * dv + 1) + (2 * da + 1) + (2 * db + 1)
        cv2 = math.sqrt(max(nss / N - mean * mean, 0.0)) / mean
        S2 = math.log(1.0 + nt2) - beta * cv2
        if (S2 - S) >= 0.0 or np.random.random() < math.exp((S2 - S) / tau_eff):
            _remove(nbr, deg, u, v)
            _remove(nbr, deg, v, u)
            _add(nbr, deg, a, b, cap)
            nt = nt2; sumsq = nss; S = S2
            edge_u[io] = a; edge_v[io] = b
    return nt


# ----------------------------- NUMBA : parcours ------------------------------
@njit(cache=True)
def bfs_dist(nbr, deg, src, N):
    dist = np.full(N, -1, dtype=np.int32)
    queue = np.empty(N, dtype=np.int32)
    head = 0; tail = 0
    queue[tail] = src; tail += 1; dist[src] = 0
    while head < tail:
        x = queue[head]; head += 1
        dx = dist[x]
        for k in range(deg[x]):
            y = nbr[x, k]
            if dist[y] == -1:
                dist[y] = dx + 1
                queue[tail] = y; tail += 1
    return dist


@njit(cache=True)
def giant_component_mask(nbr, deg, N):
    comp = np.full(N, -1, dtype=np.int32)
    queue = np.empty(N, dtype=np.int32)
    best_id = -1; best_size = 0; cid = 0
    for s in range(N):
        if comp[s] != -1 or deg[s] == 0:
            continue
        head = 0; tail = 0
        queue[tail] = s; tail += 1; comp[s] = cid
        size = 0
        while head < tail:
            x = queue[head]; head += 1; size += 1
            for k in range(deg[x]):
                y = nbr[x, k]
                if comp[y] == -1:
                    comp[y] = cid
                    queue[tail] = y; tail += 1
        if size > best_size:
            best_size = size; best_id = cid
        cid += 1
    mask = (comp == best_id)
    return mask, best_size


@njit(cache=True)
def build_W_arrays(nbr, deg, N):
    nnz = N
    for i in range(N):
        nnz += deg[i]
    indptr = np.zeros(N + 1, dtype=np.int64)
    indices = np.empty(nnz, dtype=np.int32)
    data = np.empty(nnz, dtype=np.float64)
    pos = 0
    for i in range(N):
        indptr[i] = pos
        indices[pos] = i
        data[pos] = 0.5 if deg[i] > 0 else 1.0
        pos += 1
        if deg[i] > 0:
            w = 0.5 / deg[i]
            for k in range(deg[i]):
                indices[pos] = nbr[i, k]
                data[pos] = w
                pos += 1
    indptr[N] = pos
    return indptr, indices, data


# ----------------------------- Python : outils -------------------------------
def build_geometric(N, kappa, pool_fac, seed):
    rng = np.random.default_rng(seed)
    pts = rng.random((N, 3))
    r = (kappa / ((N - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    tree = cKDTree(pts)
    pool = tree.query_pairs(pool_fac * r, output_type='ndarray').astype(np.int32)
    dd = np.linalg.norm(pts[pool[:, 0]] - pts[pool[:, 1]], axis=1)
    pool = pool[np.argsort(dd)]
    E0 = min(int(round(N * kappa / 2)), len(pool))
    edges = pool[:E0].copy()
    return edges, pool, r


def running_slope(x, y, win=1.8):
    x = np.asarray(x, float); y = np.asarray(y, float)
    lx = np.log(x); ly = np.log(y)
    out = np.full(len(x), np.nan)
    for i in range(len(x)):
        m = (x >= x[i] / win) & (x <= x[i] * win) & np.isfinite(ly)
        if m.sum() >= 4:
            out[i] = np.polyfit(lx[m], ly[m], 1)[0]
    return out


def measure_df(nbr, deg, N, sources, maxr):
    V = np.zeros(maxr + 1)
    for s in sources:
        d = bfs_dist(nbr, deg, s, N)
        dd = d[d >= 0]
        dd = dd[dd <= maxr]
        hist = np.bincount(dd, minlength=maxr + 1)[:maxr + 1]
        V += np.cumsum(hist)
    return V / len(sources)


def measure_walk(nbr, deg, N, starts, T):
    indptr, indices, data = build_W_arrays(nbr, deg, N)
    W = csr_matrix((data, indices, indptr), shape=(N, N))
    Wt = W.T.tocsr()
    ns = len(starts)
    D2 = np.zeros((N, ns))
    for c, s in enumerate(starts):
        dd = bfs_dist(nbr, deg, s, N).astype(np.float64)
        dd[dd < 0] = 0.0
        D2[:, c] = dd * dd
    Dist = np.zeros((N, ns))
    for c, s in enumerate(starts):
        Dist[s, c] = 1.0
    idx = np.asarray(starts)
    ar = np.arange(ns)
    P = np.zeros(T); MSD = np.zeros(T)
    for t in range(T):
        Dist = Wt @ Dist
        P[t] = Dist[idx, ar].mean()
        MSD[t] = (D2 * Dist).sum(0).mean()
    return np.arange(1, T + 1), P, MSD


# --------------------------- une graine -> d_w -------------------------------
def one_seed(N, seed, verbose=True):
    t0 = time.time()
    tau_eff = TAU / N
    edges, pool, r = build_geometric(N, KAPPA, POOL_FAC, seed)
    nbr, deg = build_nbr_arrays(edges, N, CAP)
    eu = edges[:, 0].copy(); ev = edges[:, 1].copy()
    pa = np.ascontiguousarray(pool[:, 0]); pb = np.ascontiguousarray(pool[:, 1])
    mean = 2.0 * len(edges) / N
    nt = n_triangles(nbr, deg, N)
    total = THERM_FAC * N
    chunk = max(1, total // N_CHUNKS)
    for c in range(N_CHUNKS):
        nt = mcmc_chunk(nbr, deg, eu, ev, pa, pb,
                        BETA, tau_eff, mean, nt, chunk, CAP, seed * 1000 + 1 + c)
    mask, gc = giant_component_mask(nbr, deg, N)
    gcn = np.where(mask)[0]
    rng = np.random.default_rng(seed * 7 + 99)
    diam = 0
    for s in rng.choice(gcn, min(5, gc), replace=False):
        diam = max(diam, int(bfs_dist(nbr, deg, s, N)[mask].max()))
    T = int(min(T_CAP, max(200, 3.0 * diam * diam)))
    maxr = min(diam, 60)
    starts = rng.choice(gcn, min(N_START, gc), replace=False)
    tt, P, MSD = measure_walk(nbr, deg, N, starts, T)
    dw = 2.0 / running_slope(tt, MSD)
    ds = -2.0 * running_slope(tt, P)
    rt = np.sqrt(np.maximum(MSD, 1e-12))
    rstar = REL_SCALE * diam
    i = int(np.nanargmin(np.abs(rt - rstar)))
    dwx, dsx = float(dw[i]), float(ds[i])
    src = rng.choice(gcn, min(N_SRC_DF, gc), replace=False)
    Vr = measure_df(nbr, deg, N, src, maxr)
    dfr = np.concatenate([[np.nan], running_slope(np.arange(1, maxr + 1), Vr[1:])])
    ri = int(round(rstar))
    dfx = float(dfr[ri]) if ri < len(dfr) and np.isfinite(dfr[ri]) else float('nan')
    if verbose:
        print(f"    (graine {seed}: diam={diam}, gc={100*gc/N:.1f}%, {time.time()-t0:.0f}s)",
              flush=True)
    return dwx, dfx, dsx, diam


def main():
    print(f"==== BARRES D'ERREUR d_w (AUTONOME) ====  N_LIST={N_LIST}  "
          f"graines={N_SEEDS}  echelle={REL_SCALE}*diam", flush=True)
    print("(1er appel : compilation numba ~20s)\n", flush=True)
    allres = {}
    for N in N_LIST:
        dws, dfs, dss = [], [], []
        t0 = time.time()
        for s in range(N_SEEDS):
            dw, df, ds, diam = one_seed(N, s)
            dws.append(dw); dfs.append(df); dss.append(ds)
            print(f"  N={N:,} graine {s+1}/{N_SEEDS} : d_w={dw:.3f}  d_f={df:.2f}  "
                  f"d_s={ds:.2f}", flush=True)
        v = np.array(dws)
        mu = float(v.mean())
        sg = float(v.std(ddof=1)) if len(v) > 1 else 0.0
        sem = sg / np.sqrt(len(v)) if len(v) > 1 else 0.0
        print(f"\n  >>> N={N:,} : d_w = {mu:.3f} +/- {sg:.3f} (ecart-type)  "
              f"[+/- {sem:.3f} sur la moyenne, n={len(v)}]")
        print(f"      d_f = {np.nanmean(dfs):.2f}   d_s = {np.nanmean(dss):.2f}   "
              f"[{time.time()-t0:.0f}s]\n", flush=True)
        allres[str(N)] = dict(d_w_seeds=dws, d_f_seeds=dfs, d_s_seeds=dss,
                              d_w_mean=mu, d_w_std=sg, d_w_sem=sem,
                              d_f_mean=float(np.nanmean(dfs)),
                              d_s_mean=float(np.nanmean(dss)))
        json.dump(allres, open("blob_errorbars.json", "w"), indent=2)
        print("   -> sauve blob_errorbars.json", flush=True)

    if len(allres) >= 2:
        print("\n================ COMPARAISON ================")
        Ns = sorted(int(k) for k in allres)
        for k in range(len(Ns) - 1):
            a = allres[str(Ns[k])]; b = allres[str(Ns[k + 1])]
            d = a["d_w_mean"] - b["d_w_mean"]
            s = math.sqrt(a["d_w_sem"] ** 2 + b["d_w_sem"] ** 2)
            sig = d / s if s > 0 else float('inf')
            verdict = ("BAISSE significative" if sig > 2 else
                       "PLATEAU dans les barres d'erreur")
            print(f"  {Ns[k]:,} -> {Ns[k+1]:,} : d_w {a['d_w_mean']:.3f} -> "
                  f"{b['d_w_mean']:.3f}  (Delta={d:+.3f}, {sig:.1f}sigma) : {verdict}")
        print("\n  baisse significative qui continue -> RECOUVREMENT (d_w->2).")
        print("  plateau dans les barres d'erreur   -> ANOMALIE douce reelle (d_w->~2.5).")
    else:
        print("Pour comparer, mettre >=2 tailles dans N_LIST (ex: [250000, 500000]).")


if __name__ == "__main__":
    main()
