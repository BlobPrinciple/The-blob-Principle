"""
================================================================================
 BLOB — RE-TEST des invariants N-plats poses, jusqu'a N=500 000  (Colab, numba)
================================================================================
 Le corpus a etabli ces invariants sur N<=2000 (souvent <1 decade). Cette
 session les a deja confirmes plats jusqu'a N=20 000 (pur-Python). Ce script
 pousse a N=500 000 avec numba pour le verdict definitif.

 Invariants mesures (tous sans dimension) :
   tri/arete      ~ 1,6     (triangles par arete ; count_triangles standard)
   Gini(masse)    ~ 0,854   (grumelosite ; masse = triangles incidents/sommet)
   tri/sommet     ~ 16      (calcification par sommet)
   CV(degre)      ~ 0,88    (dispersion du degre)
   clustering     ~ ?       (coef. de clustering global = 3*tri / chemins-2)
 Controle (NON-invariant attendu, le corpus dit qu'il DERIVE) :
   K4/sommet      (densite de 4-cliques ; ~10% de derive attendue)

 USAGE COLAB :
   !pip -q install numba
   %run blob_invariants_500k.py
 Duree : ~30-60 min (le K4-count domine ; il est saute au-dela de N=50k).
 Un JSON ecrit a chaque palier (invariants_500k.json).
================================================================================
"""
import time, math, json, gc
import numpy as np
from numba import njit
from scipy.spatial import cKDTree

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

# ----------------------------- mesures supplementaires -----------------------
@njit(cache=True)
def triangles_per_vertex(nbr, deg, N):
    tpv = np.zeros(N, dtype=np.int64)
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
def count_2paths(nbr, deg, N):
    # nombre de chemins de longueur 2 (pour le clustering global)
    tot = 0
    for u in range(N):
        d = deg[u]
        tot += d * (d - 1) // 2
    return tot


@njit(cache=True)
def k4_count(nbr, deg, N):
    cnt = 0
    for u in range(N):
        du = deg[u]
        for ki in range(du):
            v = nbr[u, ki]
            if v <= u:
                continue
            for kj in range(du):
                w = nbr[u, kj]
                if w <= v:
                    continue
                isvw = False
                for m in range(deg[v]):
                    if nbr[v, m] == w:
                        isvw = True; break
                if not isvw:
                    continue
                for kl in range(du):
                    x = nbr[u, kl]
                    if x <= w:
                        continue
                    okv = False
                    for m in range(deg[v]):
                        if nbr[v, m] == x:
                            okv = True; break
                    if not okv:
                        continue
                    okw = False
                    for m in range(deg[w]):
                        if nbr[w, m] == x:
                            okw = True; break
                    if okw:
                        cnt += 1
    return cnt


def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if n == 0 or x.sum() == 0:
        return float('nan')
    cum = np.cumsum(x)
    return float((n + 1 - 2 * np.sum(cum) / cum[-1]) / n)


CAP = 64; POOL_FAC = 1.6; THERM_FAC = 120; N_CHUNKS = 10; KAPPA = 6.6
DO_K4_UPTO = 50000  # au-dela, le comptage K4 (O(N deg^3)) est saute


def measure(N, seed):
    edges, pool, r = build_geometric(N, KAPPA, POOL_FAC, seed)
    nbr, deg = build_nbr_arrays(edges, N, CAP)
    eu = edges[:, 0].copy(); ev = edges[:, 1].copy()
    pa = np.ascontiguousarray(pool[:, 0]); pb = np.ascontiguousarray(pool[:, 1])
    del pool, edges; gc.collect()
    mean = 2.0 * eu.shape[0] / N
    nt = n_triangles(nbr, deg, N)
    total = THERM_FAC * N; chunk = max(1, total // N_CHUNKS)
    for c in range(N_CHUNKS):
        nt = mcmc_chunk(nbr, deg, eu, ev, pa, pb, 0.30, 0.5 / N, mean, nt,
                        chunk, CAP, seed * 100 + 1 + c)
    ntri = n_triangles(nbr, deg, N); E = int(deg.sum() // 2)
    tpv = triangles_per_vertex(nbr, deg, N)
    p2 = count_2paths(nbr, deg, N)
    clustering = 3.0 * ntri / p2 if p2 > 0 else float('nan')
    rec = dict(N=N, seed=seed, tri_per_edge=ntri / E, gini=gini(tpv),
               tri_per_vertex=float(tpv.mean()),
               cv_deg=float(deg.std() / deg.mean()),
               clustering=clustering, mean_deg=2.0 * E / N)
    if N <= DO_K4_UPTO:
        nK4 = k4_count(nbr, deg, N)
        rec['K4_per_vertex'] = nK4 / N
    else:
        rec['K4_per_vertex'] = None
    return rec


def main():
    NS = [2000, 10000, 50000, 100000, 250000, 500000]
    SEEDS = [0, 1, 2]
    print("RE-TEST GRAND N (kappa=6.6, therm=120N) jusqu'a N=500 000")
    print("Cibles : tri/arete~1,6 | Gini~0,854 | tri/sommet~16 | CVdeg~0,88\n")
    out = []
    for N in NS:
        nseed = SEEDS if N <= 100000 else SEEDS[:2]  # moins de graines aux tres grands N
        rows = []; t0 = time.time()
        for sd in nseed:
            r = measure(N, sd); rows.append(r)
            k4s = f"K4/N={r['K4_per_vertex']:.2f}" if r['K4_per_vertex'] else "K4/N=skip"
            print(f"  N={N:>7,} s{sd}: tri/E={r['tri_per_edge']:.3f}  "
                  f"Gini={r['gini']:.4f}  tri/V={r['tri_per_vertex']:.2f}  "
                  f"CVdeg={r['cv_deg']:.3f}  clust={r['clustering']:.4f}  {k4s}  "
                  f"({time.time()-t0:.0f}s)", flush=True)
        def m(k): return float(np.mean([x[k] for x in rows]))
        def s(k): return float(np.std([x[k] for x in rows]))
        agg = dict(N=N, triE_m=m('tri_per_edge'), triE_s=s('tri_per_edge'),
                   gini_m=m('gini'), gini_s=s('gini'),
                   triV_m=m('tri_per_vertex'), cvdeg_m=m('cv_deg'),
                   clust_m=m('clustering'))
        out.append(agg)
        json.dump(out, open('invariants_500k.json', 'w'), indent=2)
    print("\n=== SYNTHESE ===")
    print(f"{'N':>8} | {'tri/arete':>14} | {'Gini':>14} | {'tri/sommet':>11} | "
          f"{'CVdeg':>7} | {'clust':>7}")
    for a in out:
        print(f"{a['N']:>8} | {a['triE_m']:.3f}+/-{a['triE_s']:.3f} | "
              f"{a['gini_m']:.4f}+/-{a['gini_s']:.4f} | {a['triV_m']:>11.3f} | "
              f"{a['cvdeg_m']:>7.3f} | {a['clust_m']:>7.4f}")
    v0, v1 = out[0], out[-1]
    print(f"\nDERIVE {v0['N']}->{v1['N']} :")
    for key, name in [('triE_m','tri/arete'), ('gini_m','Gini'),
                      ('triV_m','tri/sommet'), ('cvdeg_m','CVdeg'),
                      ('clust_m','clustering')]:
        d = 100*(v1[key]-v0[key])/v0[key]
        verdict = "PLAT" if abs(d) < 3 else ("derive legere" if abs(d) < 8 else "DERIVE")
        print(f"  {name:<12}: {v0[key]:.4f} -> {v1[key]:.4f}  ({d:+.1f}%)  => {verdict}")


if __name__ == "__main__":
    main()
