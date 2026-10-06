"""
================================================================================
 BLOB — UNIVERSALITE de l'exposant de flot  alpha   (AUTONOME, Colab)
================================================================================
 CANDIDAT INVARIANT n.2 :  (d_w - 2) ~ N^(-alpha),  alpha ~ 0.148  (mesure de
 reference : balayage 25k->1M, fac=130, echelle 0.15*diam).
 alpha est la VITESSE a laquelle la non-variete UV s'efface vers la variete 3D
 a l'IR. C'est un nombre sans dimension qui emerge de la dynamique.

 TEST DU GARDIEN deja passe (in-situ) : le RGG brut (zero viabilite) ne decroit
 PAS (d_w ~ 2.3 stable) -> alpha porte la signature de la viabilite.

 CE SCRIPT teste l'UNIVERSALITE : alpha est-il le MEME quand on change les
 parametres microscopiques ?
   C0  reference   beta=0.30  tau=0.50  kappa=6.6
   C1  viabilite x2  beta=0.60  tau=0.50  kappa=6.6
   C2  densite      beta=0.30  tau=0.50  kappa=9.0
   C3  temperature  beta=0.30  tau=0.25  kappa=6.6
   C4  null RGG brut (aucun MCMC ; controle, quasi gratuit)

 Verdict :
   alpha(C0) = alpha(C1) = alpha(C2) = alpha(C3)  (aux erreurs pres)
        -> alpha UNIVERSEL : candidat serieux de 2e invariant sans dimension.
   alpha varie avec les parametres
        -> alpha est un parametre deguise : on l'enterre (regle C.3).

 USAGE COLAB :
   !pip -q install numba
   %run blob_universalite_alpha.py
 Duree estimee : ~1h30-2h (4 conditions x 4 tailles + null).
 Un JSON par (condition, N) sauve immediatement + synthese finale.
================================================================================
"""
import time, math, json, os
import numpy as np
from numba import njit
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix

# =============================== CONFIG =======================================
# v2 — MULTI-GRAINES sur la question vivante : alpha(kappa=6.6) vs alpha(kappa=9).
# Le passage v1 (single-seed) a donne : C0 0.085, C1(beta x2) 0.097 (0.3 sigma, PASSE),
# C2(kappa 9) 0.153 (2.0 sigma : ZONE GRISE), C3(tau/2) non-monotone (sous-
# thermalise, invalide), C4 null RGG -0.002 (parfait). Ce v2 resout le 2 sigma.
N_LIST    = [25_000, 50_000, 100_000, 200_000]
N_SEEDS   = 4            # graines par condition -> alpha mesure avec son erreur
CONDITIONS = [
    dict(name="C0_ref",    beta=0.30, tau=0.50, kappa=6.6, mcmc=True,  tf=130),
    dict(name="C2_kappa9", beta=0.30, tau=0.50, kappa=9.0, mcmc=True,  tf=130),
    # C3 refait avec thermalisation triplee (le gel a tau/2 ralentit la relaxation) :
    dict(name="C3_tau025_tf390", beta=0.30, tau=0.25, kappa=6.6, mcmc=True, tf=390),
]
REL_SCALE = 0.15
POOL_FAC  = 1.6
CAP       = 64
N_START   = 40
T_CAP     = 2200
N_CHUNKS  = 10
SEED      = 0
OUTDIR    = "."



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


def measure_dw_ds(nbr, deg, N, seed):
    mask, gc = giant_component_mask(nbr, deg, N)
    gcn = np.where(mask)[0]
    rng = np.random.default_rng(seed * 7 + 99)
    diam = 0
    for s in rng.choice(gcn, min(5, gc), replace=False):
        diam = max(diam, int(bfs_dist(nbr, deg, s, N)[mask].max()))
    T = int(min(T_CAP, max(200, 3.0 * diam * diam)))
    starts = rng.choice(gcn, min(N_START, gc), replace=False)
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
    idx = np.asarray(starts); ar = np.arange(ns)
    P = np.zeros(T); MSD = np.zeros(T)
    for t in range(T):
        Dist = Wt @ Dist
        P[t] = Dist[idx, ar].mean()
        MSD[t] = (D2 * Dist).sum(0).mean()
    tt = np.arange(1, T + 1)
    dw = 2.0 / running_slope(tt, MSD)
    ds = -2.0 * running_slope(tt, P)
    rt = np.sqrt(np.maximum(MSD, 1e-12))
    i = int(np.nanargmin(np.abs(rt - REL_SCALE * diam)))
    ds_uv = float(ds[2]) if len(ds) > 2 and np.isfinite(ds[2]) else float('nan')
    return float(dw[i]), ds_uv, diam, int(gc)


def run_condition(cond):
    name = cond["name"]; beta = cond["beta"]; tau = cond["tau"]
    kappa = cond["kappa"]; use_mcmc = cond["mcmc"]; tf = cond.get("tf", 130)
    print(f"\n========== {name}  (beta={beta} tau={tau} kappa={kappa} "
          f"therm={tf}*N, {N_SEEDS} graines) ==========", flush=True)
    alphas = []; allpts = []
    Nsl = np.log(np.array(N_LIST, float))
    for sd in range(N_SEEDS):
        dws = []
        for N in N_LIST:
            t0 = time.time()
            edges, pool, r = build_geometric(N, kappa, POOL_FAC, sd)
            nbr, deg = build_nbr_arrays(edges, N, CAP)
            if use_mcmc:
                eu = edges[:, 0].copy(); ev = edges[:, 1].copy()
                pa = np.ascontiguousarray(pool[:, 0])
                pb = np.ascontiguousarray(pool[:, 1])
                mean = 2.0 * len(edges) / N
                nt = n_triangles(nbr, deg, N)
                tau_eff = tau / N
                total = tf * N
                chunk = max(1, total // N_CHUNKS)
                for c in range(N_CHUNKS):
                    nt = mcmc_chunk(nbr, deg, eu, ev, pa, pb,
                                    beta, tau_eff, mean, nt, chunk, CAP,
                                    sd * 1000 + 7 + c)
            dwx, dsuv, diam, gc = measure_dw_ds(nbr, deg, N, sd)
            dws.append(dwx)
            allpts.append(dict(seed=sd, N=N, d_w=dwx, d_s_uv=dsuv, diam=diam,
                               runtime_s=round(time.time() - t0, 1)))
            print(f"  graine {sd}  N={N:>8,} : d_w={dwx:.3f}  "
                  f"({time.time()-t0:.0f}s)", flush=True)
        v = np.array(dws)
        if np.all(v - 2.0 > 0.02):
            a = -float(np.polyfit(Nsl, np.log(v - 2.0), 1)[0])
            alphas.append(a)
            print(f"  >> graine {sd} : alpha = {a:.3f}", flush=True)
        json.dump(dict(name=name, alphas=alphas, points=allpts),
                  open(os.path.join(OUTDIR, f"alpha_v2_{name}.json"), "w"),
                  indent=2)
    arr = np.array(alphas)
    mu = float(arr.mean()); sg = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sg / np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    print(f"\n  >>> {name} : alpha = {mu:.3f} +/- {sg:.3f} (ecart-type)  "
          f"[+/- {sem:.3f} sur la moyenne, n={len(arr)}]", flush=True)
    return dict(name=name, beta=beta, tau=tau, kappa=kappa, tf=tf,
                alpha_mean=mu, alpha_std=sg, alpha_sem=sem, alphas=alphas)


def main():
    print(f"==== UNIVERSALITE alpha v2 (MULTI-GRAINES) ====  N_LIST={N_LIST}  "
          f"graines={N_SEEDS}", flush=True)
    results = []
    for cond in CONDITIONS:
        try:
            results.append(run_condition(cond))
        except Exception as ex:
            import traceback
            print(f"!!! {cond['name']} a echoue : {ex}\n"
                  f"{traceback.format_exc()}", flush=True)
        json.dump(results, open(os.path.join(OUTDIR,
                  "alpha_v2_synthese.json"), "w"), indent=2)

    print("\n================ SYNTHESE v2 ================")
    for r in results:
        print(f"  {r['name']:<18} alpha = {r['alpha_mean']:.3f} "
              f"+/- {r['alpha_sem']:.3f} (sem, n={len(r['alphas'])})")
    if len(results) >= 2:
        a, b = results[0], results[1]
        d = b["alpha_mean"] - a["alpha_mean"]
        s = math.sqrt(a["alpha_sem"] ** 2 + b["alpha_sem"] ** 2)
        sig = abs(d) / s if s > 0 else float("inf")
        print(f"\n  {b['name']} vs {a['name']} : Delta = {d:+.3f}  "
              f"({sig:.1f} sigma)")
        if sig < 2:
            print("  => COMPATIBLE avec l'independance en kappa, a la resolution")
            print("     du test : candidat RENFORCE (deja insensible a beta).")
            print("     (Independance non PROUVEE : seulement non refutee a "
                  f"{sig:.1f} sigma.)")
        elif sig > 3:
            print("  => alpha DEPEND de kappa : parametre deguise, pas un "
                  "invariant (regle C.3 : enterre).")
        else:
            print("  => encore en zone grise (2-3 sigma) : augmenter N_SEEDS.")
    print("\nFichiers : alpha_v2_<condition>.json + alpha_v2_synthese.json")


if __name__ == "__main__":
    main()
