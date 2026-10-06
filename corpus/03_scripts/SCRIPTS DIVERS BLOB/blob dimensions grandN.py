"""
================================================================================
 BLOB PRINCIPLE — Secteur dimensionnel a grand N  (Google Colab)
================================================================================
 Moteur viabilite COMPILE (numba, ~50-100x plus rapide que Python pur) +
 mesure des trois dimensions COURANTES sur la meme marche :
     d_f(r)  : geometrique  (croissance de volume, BFS)
     d_s(t)  : spectrale     (proba de retour, marche paresseuse)
     d_w(t)  : de marche     (deplacement quadratique moyen, distance de graphe)
 La fermeture d'Einstein / Alexander-Orbach   d_s * d_w = 2 d_f   est utilisee
 comme FILTRE DE FIABILITE : on ne fait confiance a la mesure qu'aux echelles ou
 elle ferme (~1). C'est l'auto-validation du secteur dynamique.

 OBJECTIF : trancher, a N >> 50 000, si l'anomalie diffusive observee a N=30-50k
 (d_w ~ 2,6 ; deficit spectral d_s < d_f = 3, signature dynamique de la
 non-variete CXVIII) PERSISTE (sous-diffusion reelle) ou se RESORBE vers la
 variete (d_w -> 2, d_s -> 3) au plus profond IR.

 Modele : graphe geometrique aleatoire 3D (degre moyen kappa) + MCMC maximisant
     S = log(1 + n_tri) - beta * CV(degres)
 par echange d'aretes dans le pool geometrique. Parametres du corpus :
     beta = 0.30 , tau = 0.50 , tau_eff = tau/N , kappa = 6.6.

 USAGE COLAB :
     !pip -q install numba
     # puis copier-coller ce fichier dans une cellule, ou :
     # %run blob_dimensions_grandN.py
 Regler N ci-dessous. Premier run : numba compile (~20 s), runs suivants caches.
================================================================================
"""

import time
import math
import numpy as np
from numba import njit
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix

# =============================== CONFIG =======================================
# Balayage en taille : un JSON COMPLET est sauve par palier (immediatement).
N_SWEEP   = [5_000, 10_000, 25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000]
KAPPA     = 6.6       # degre moyen (point de travail du corpus)
BETA      = 0.30      # poids de la viabilite
TAU       = 0.50      # temperature
THERM_FAC = 130       # pas de thermalisation = THERM_FAC * N  (corpus = 130)
POOL_FAC  = 1.6       # rayon du pool de candidats = POOL_FAC * r_arete
SEED      = 0
CAP       = 64        # capacite max du tableau de voisins (degre plafonne)
OUTDIR    = "."       # dossier de sortie (JSON + figures)

# --- mesure ---
N_SRC_DF  = 200       # sources BFS pour d_f
N_START   = 48        # departs de marche pour d_s / d_w (baisser a 32 si N>=500k lent)
T_CAP     = 3000      # plafond du nb de pas de marche (cout ~ E*N_START*T)
N_CHUNKS  = 13        # nb de blocs de thermalisation (affichage du n_tri)
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
    # nombre de voisins communs de u et v (triangles passant par l'arete u-v)
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
    # comptage total, une seule fois au depart. Chaque arete (u<v) compte ses
    # voisins communs = triangles passant par elle ; chaque triangle etant vu
    # par ses 3 aretes, on divise par 3.
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
    """Un bloc de nsteps de MCMC. Modifie nbr/deg/edge_* en place. Renvoie n_tri."""
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
        # garde-fou de connectivite (leger) : ne pas appauvrir les noeuds rares
        if deg[u] <= 2 or deg[v] <= 2:
            continue
        # chercher une non-arete candidate (a,b) dans le pool, distincte de u,v
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
        # triangles : perdus par retrait u-v, gagnes par ajout a-b
        # (les voisins communs ne dependent pas de l'existence de l'arete elle-meme)
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
        # rejet -> rien a defaire (aucune modification n'a ete appliquee)
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
    """CSR de la marche paresseuse W (reste 1/2, sinon voisin uniforme)."""
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
    # trier le pool par distance ; les E0 plus courtes = aretes initiales
    # (fixe le degre moyen a EXACTEMENT kappa, comme le corpus E0 = N*kappa/2,
    #  sans le sous-comptage de bord du cube)
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


# ================================== MAIN =====================================
def _verdict_and_reliable(rows, diam):
    """Fenetre la plus fiable (fermeture ~1) DANS la bande diffusive
       (au-dela de l'UV, en-deca de la saturation de bord) + verdict."""
    lo = max(3.0, 0.08 * diam)
    hi = max(lo + 1.0, 0.30 * diam)
    best = None
    for (t_, rv, dsi, dwi, dfh, clos) in rows:
        if lo <= rv <= hi:
            score = abs(clos - 1.0)
            if best is None or score < best[0]:
                best = (score, t_, rv, dsi, dwi, dfh, clos)
    if best is None:  # bande vide (tres petit N) : repli sur r < 0.25*diam
        for (t_, rv, dsi, dwi, dfh, clos) in rows:
            if rv < 0.25 * diam:
                score = abs(clos - 1.0)
                if best is None or score < best[0]:
                    best = (score, t_, rv, dsi, dwi, dfh, clos)
    if best is None:
        return None, "non concluant (pas de fenetre fiable)"
    _, t_, rv, dsi, dwi, dfh, clos = best
    anomale = (dwi > 2.25) and (dsi < dfh - 0.25)
    variete = (abs(dwi - 2.0) < 0.25) and (abs(dsi - 3.0) < 0.30)
    if variete:
        verdict = "RECOUVREMENT DE VARIETE (d_w->2, d_s->3) : diffusion normale au profond IR"
    elif anomale:
        verdict = "ANOMALIE PERSISTANTE (d_w>2, d_s<d_f) : non-variete CXVIII dynamique"
    else:
        verdict = "INTERMEDIAIRE / non concluant a cette taille"
    reliable = dict(t=int(t_), r=float(rv), d_s=float(dsi), d_w=float(dwi),
                    d_f=float(dfh), closure=float(clos))
    return reliable, verdict


def run_one(N):
    t0 = time.time()
    tau_eff = TAU / N
    print(f"\n############### N = {N:,} ###############", flush=True)

    edges, pool, r = build_geometric(N, KAPPA, POOL_FAC, SEED)
    print(f"[{time.time()-t0:5.0f}s] geometrie : r={r:.5f}  |aretes|={len(edges):,}  "
          f"|pool|={len(pool):,}  (degre~{2*len(edges)/N:.2f})", flush=True)
    nbr, deg = build_nbr_arrays(edges, N, CAP)
    edge_u = edges[:, 0].copy(); edge_v = edges[:, 1].copy()
    pool_a = np.ascontiguousarray(pool[:, 0]); pool_b = np.ascontiguousarray(pool[:, 1])
    mean = 2.0 * len(edges) / N
    nt = n_triangles(nbr, deg, N)

    total = THERM_FAC * N
    chunk = max(1, total // N_CHUNKS)
    print(f"[{time.time()-t0:5.0f}s] thermalisation {total:,} pas "
          f"(compilation numba au 1er bloc)...", flush=True)
    for c in range(N_CHUNKS):
        nt = mcmc_chunk(nbr, deg, edge_u, edge_v, pool_a, pool_b,
                        BETA, tau_eff, mean, nt, chunk, CAP, SEED + 1 + c)
        if (c + 1) % max(1, N_CHUNKS // 4) == 0 or c == N_CHUNKS - 1:
            print(f"[{time.time()-t0:5.0f}s]   {100*(c+1)//N_CHUNKS:3d}%  n_tri={nt:,}  "
                  f"<k>={deg.mean():.2f}  CV={deg.std()/deg.mean():.3f}", flush=True)

    mask, gc = giant_component_mask(nbr, deg, N)
    gc_nodes = np.where(mask)[0]
    rng = np.random.default_rng(7)
    diam = 0
    for s in rng.choice(gc_nodes, min(5, gc), replace=False):
        diam = max(diam, int(bfs_dist(nbr, deg, s, N)[mask].max()))
    T = int(min(T_CAP, max(200, 3.0 * diam * diam)))
    maxr = min(diam, 60)
    print(f"[{time.time()-t0:5.0f}s] geante {gc:,}/{N:,} ({100*gc/N:.1f}%)  diam~{diam}  "
          f"T={T}  (marche ~{len(edges)*2*N_START*T/1e9:.1f} Gflops)", flush=True)

    src_df = rng.choice(gc_nodes, min(N_SRC_DF, gc), replace=False)
    Vr = measure_df(nbr, deg, N, src_df, maxr)
    rr = np.arange(maxr + 1)
    df_r = np.concatenate([[np.nan], running_slope(rr[1:], Vr[1:])])

    starts = rng.choice(gc_nodes, min(N_START, gc), replace=False)
    tt, Pret, MSD = measure_walk(nbr, deg, N, starts, T)
    print(f"[{time.time()-t0:5.0f}s] mesures finies", flush=True)

    floor = 8.0 / gc
    ds = -2.0 * running_slope(tt, Pret)
    dw = 2.0 / running_slope(tt, MSD)
    rt = np.sqrt(np.maximum(MSD, 1e-12))

    def df_at(rv):
        i = int(round(rv))
        return df_r[i] if 1 <= i < len(df_r) and np.isfinite(df_r[i]) else np.nan

    rows = []
    for i in range(len(tt)):
        if Pret[i] < floor * 1.5:
            continue
        rv = rt[i]; dfh = df_at(rv)
        if not (np.isfinite(ds[i]) and np.isfinite(dw[i]) and np.isfinite(dfh)):
            continue
        rows.append((int(tt[i]), float(rv), float(ds[i]), float(dw[i]),
                     float(dfh), float(ds[i] * dw[i] / (2 * dfh))))

    pic_df = float(np.nanmax(df_r[3:min(10, len(df_r))]))
    reliable, verdict = _verdict_and_reliable(rows, diam)

    print(f"   d_f(pic)={pic_df:.2f}", end="")
    if reliable:
        print(f" | fenetre fiable t={reliable['t']} r={reliable['r']:.1f} : "
              f"d_s={reliable['d_s']:.2f} d_w={reliable['d_w']:.2f} "
              f"d_f={reliable['d_f']:.2f} (ferm {reliable['closure']:.3f})")
    else:
        print()
    print(f"   VERDICT: {verdict}", flush=True)

    def J(a):
        return [None if not np.isfinite(x) else float(x) for x in a]

    res = dict(
        N=int(N), kappa=KAPPA, beta=BETA, tau=TAU, therm_fac=THERM_FAC,
        seed=SEED, runtime_s=round(time.time() - t0, 1),
        gc=int(gc), gc_frac=round(gc / N, 4), diam=int(diam), T=int(T),
        n_tri=int(nt), mean_deg=round(float(deg.mean()), 3),
        cv_deg=round(float(deg.std() / deg.mean()), 4),
        pic_df=pic_df, reliable=reliable, verdict=verdict,
        r_axis=rr.tolist(), df_r=J(df_r),
        t_axis=[int(x) for x in tt], d_s_t=J(ds), d_w_t=J(dw),
        P_return=J(Pret), MSD=J(MSD),
        closure_rows=[dict(t=a, r=b, ds=c, dw=d, df=e, closure=f)
                      for (a, b, c, d, e, f) in rows],
    )
    return res


def main():
    import json, os
    os.makedirs(OUTDIR, exist_ok=True)
    print(f"==== BALAYAGE BLOB ====  N = {N_SWEEP}", flush=True)
    print(f"kappa={KAPPA} beta={BETA} tau={TAU} therm={THERM_FAC}*N | "
          f"un JSON complet par palier, sauve immediatement.\n", flush=True)
    summary = []
    for N in N_SWEEP:
        try:
            res = run_one(N)
        except Exception as ex:
            import traceback
            print(f"!!! N={N} a echoue : {ex}\n{traceback.format_exc()}", flush=True)
            continue
        path = os.path.join(OUTDIR, f"blob_dims_N{N}.json")
        with open(path, "w") as f:
            json.dump(res, f)
        print(f"   -> sauve {path}  ({res['runtime_s']}s)", flush=True)
        rel = res["reliable"] or {}
        summary.append(dict(N=N, gc=res["gc"], diam=res["diam"], pic_df=res["pic_df"],
                            d_s=rel.get("d_s"), d_w=rel.get("d_w"), d_f=rel.get("d_f"),
                            closure=rel.get("closure"), verdict=res["verdict"],
                            runtime_s=res["runtime_s"]))
        with open(os.path.join(OUTDIR, "blob_sweep_summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

    print("\n================ SCALING (fenetre fiable) ================")
    print(f"{'N':>11} {'d_f pic':>8} {'d_s':>6} {'d_w':>6} {'ferm':>6}  verdict")
    for s in summary:
        ds_ = f"{s['d_s']:.2f}" if s['d_s'] is not None else "  -  "
        dw_ = f"{s['d_w']:.2f}" if s['d_w'] is not None else "  -  "
        cl_ = f"{s['closure']:.2f}" if s['closure'] is not None else "  -  "
        v = ("ANOMALIE" if "ANOMALIE" in s['verdict']
             else "VARIETE" if "VARIETE" in s['verdict'] else "inter.")
        print(f"{s['N']:>11,} {s['pic_df']:>8.2f} {ds_:>6} {dw_:>6} {cl_:>6}  {v}")

    print("\n--- LECTURE DU SCALING ---")
    print("Colonne d_w en descendant les N :")
    print("  d_w reste ~2.6              -> sous-diffusion REELLE, anomalie persistante (CXVIII)")
    print("  d_w descend vers 2 (d_s->3) -> RECOUVREMENT de variete au profond IR")
    print("d_f pic doit se stabiliser a 3 (volume 3D).")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        Ns = [s['N'] for s in summary]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(Ns, [s['pic_df'] for s in summary], 'ko-', label=r'$d_f$ (volume)')
        ax.plot(Ns, [s['d_s'] if s['d_s'] is not None else np.nan for s in summary],
                'o-', color='C0', label=r'$d_s$ (spectrale)')
        ax.plot(Ns, [s['d_w'] if s['d_w'] is not None else np.nan for s in summary],
                'o-', color='C3', label=r'$d_w$ (marche)')
        ax.axhline(3, ls=':', c='g', lw=1, label='3 (variete)')
        ax.axhline(2, ls=':', c='r', lw=1, label='2 (diff. normale)')
        ax.set_xscale('log'); ax.set_xlabel('N'); ax.set_ylabel('dimension')
        ax.set_ylim(1.5, 3.5); ax.legend(); ax.grid(alpha=.3)
        ax.set_title('Scaling des dimensions (fenetre fiable) vs N')
        p = os.path.join(OUTDIR, "blob_sweep_scaling.png")
        plt.tight_layout(); plt.savefig(p, dpi=120)
        print(f"\n[fig] {p}")
    except Exception as ex:
        print(f"[fig] indisponible ({ex})")

    print("\nTermine. -> blob_dims_N*.json (un par palier) + blob_sweep_summary.json "
          "+ blob_sweep_scaling.png")


if __name__ == "__main__":
    main()
