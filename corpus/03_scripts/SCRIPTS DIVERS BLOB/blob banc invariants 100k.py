"""
================================================================================
 BLOB — BANC UNIVERSEL D'INVARIANTS  (Colab, numba)  jusqu'a N=100 000
================================================================================
 Teste AUTOMATIQUEMENT toutes nos categories de tentative d'invariant et rend
 un verdict par candidat. Repond a l'angle mort identifie : on cherchait des
 invariants de FORME (ratios statiques) ; il faut aussi tester les invariants
 de FLOT (exposants) et croiser plusieurs parametres.

 TROIS FAMILLES testees :

 [A] RATIOS STATIQUES (doivent etre N-plats ET kappa-plats pour etre invariants)
     A1 tri/arete         A2 Gini(masse)       A3 tri/sommet
     A4 CV(degre)         A5 clustering global A6 K4/sommet (controle: derive)
     -> mesures a plusieurs N (N-platitude) ET plusieurs kappa (kappa-platitude).

 [B] EXPOSANTS DE LOI D'ECHELLE (invariants DYNAMIQUES ; l'angle mort historique)
     B1 exposant de b1 ~ N^p           (loi topologique)
     B2 exposant de n_K4 ~ N^q         (croissance de la matiere)
     B3 exposant de Fano(K4) vs N      (fluctuations - lead Sorkin)
     -> un exposant est un invariant candidat ssi il est STABLE multi-graines.

 [C] RATIOS SPECTRAUX (decorreles du geometrique ? candidats 'couplage')
     C1 lambda2/lambda1   C2 lambda3/lambda1  du laplacien de marche
     -> testes pour platitude N + kappa + barres d'erreur (le corpus les dit bruites).

 VERDICT AUTOMATIQUE par candidat :
   INVARIANT      : plat en N (<3%) ET (si applicable) plat en kappa (CV<5%)
   PARAMETRE      : derive nettement en N ou en kappa
   BRUITE         : CV multi-graines > seuil -> pas un invariant fiable
   CANDIDAT-FLOT  : exposant stable multi-graines (a confirmer plus loin)

 USAGE COLAB :
   !pip -q install numba
   %run blob_banc_invariants_100k.py
 Duree : ~40-90 min (famille A+B legere ; C spectral plus lourd ; K4 saute >50k).
 JSON ecrit en continu (banc_invariants.json).
================================================================================
"""
import time, math, json, gc
import numpy as np
from numba import njit
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

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

# =============================== mesures =====================================
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
    tot = 0
    for u in range(N):
        d = deg[u]; tot += d * (d - 1) // 2
    return tot


@njit(cache=True)
def k4_count(nbr, deg, N):
    cnt = 0
    for u in range(N):
        du = deg[u]
        for ki in range(du):
            v = nbr[u, ki]
            if v <= u: continue
            for kj in range(du):
                w = nbr[u, kj]
                if w <= v: continue
                ok = False
                for m in range(deg[v]):
                    if nbr[v, m] == w: ok = True; break
                if not ok: continue
                for kl in range(du):
                    x = nbr[u, kl]
                    if x <= w: continue
                    o1 = False
                    for m in range(deg[v]):
                        if nbr[v, m] == x: o1 = True; break
                    if not o1: continue
                    o2 = False
                    for m in range(deg[w]):
                        if nbr[w, m] == x: o2 = True; break
                    if o2: cnt += 1
    return cnt


def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if n == 0 or x.sum() == 0: return float('nan')
    cum = np.cumsum(x)
    return float((n + 1 - 2 * np.sum(cum) / cum[-1]) / n)


def betti1_gf2(nbr, deg, N):
    # b1 = nE - rang(d1 sur GF(2)) - (nV - b0) ... approx via rang du bord triangle->arete
    # Estimation rapide : b1 = E - V + b0 - (independent triangle relations).
    # Pour la loi d'echelle on prend la cyclomatique du 1-squelette moins les
    # triangles independants : b1 ~ (E - V + comp) - rank_d2. On approxime rank_d2
    # par le nombre de triangles (borne sup) -> proxy grossier mais N-coherent.
    # Mieux : on renvoie la cyclomatique (E-V+comp), invariant topologique du graphe.
    E = int(deg.sum() // 2)
    mask, gc_ = giant_component_mask(nbr, deg, N)
    # nombre de composantes : approx 1 (graphe geometrique dense) -> comp=1
    return E - N + 1


def lap_walk_ratios(nbr, deg, N, k=4):
    # 2 plus petits ratios spectraux non triviaux du laplacien de marche normalise
    indptr, indices, data = build_W_arrays(nbr, deg, N)
    W = csr_matrix((data, indices, indptr), shape=(N, N))
    # laplacien L = I - D^-1 A ; on utilise W (lazy) -> L_lazy = I - W
    # valeurs propres de L via eigsh sur (I - W) symetrise approx : on passe par
    # le laplacien normalise symetrique L_sym = I - D^-1/2 A D^-1/2
    deg_f = deg.astype(np.float64)
    dinv = 1.0 / np.sqrt(np.maximum(deg_f, 1.0))
    # A = adjacence
    rows = []; cols = []
    for i in range(N):
        for kk in range(deg[i]):
            rows.append(i); cols.append(nbr[i, kk])
    A = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
    Dh = csr_matrix((dinv, (np.arange(N), np.arange(N))), shape=(N, N))
    Lsym = csr_matrix((np.ones(N), (np.arange(N), np.arange(N)))) - Dh @ A @ Dh
    try:
        if N <= 3000:
            ev = np.linalg.eigvalsh(Lsym.toarray())
        else:
            ev = eigsh(Lsym, k=max(k, 6), which='SM')[0]
        ev = np.sort(np.abs(ev))
        ev = ev[ev > 1e-7]
        if len(ev) >= 3:
            return float(ev[1] / ev[0]), float(ev[2] / ev[0])
    except Exception:
        pass
    return float('nan'), float('nan')


CAP = 64; POOL_FAC = 1.6; THERM_FAC = 120; N_CHUNKS = 10
DO_K4_UPTO = 50000
DO_SPECTRAL_UPTO = 30000  # eigsh trop lourd au-dela


def therm_graph(N, kappa, seed):
    edges, pool, r = build_geometric(N, kappa, POOL_FAC, seed)
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
    return nbr, deg


def static_ratios(nbr, deg, N, want_k4=True, want_spec=True):
    ntri = n_triangles(nbr, deg, N); E = int(deg.sum() // 2)
    tpv = triangles_per_vertex(nbr, deg, N)
    p2 = count_2paths(nbr, deg, N)
    out = dict(tri_per_edge=ntri / E, gini=gini(tpv),
               tri_per_vertex=float(tpv.mean()),
               cv_deg=float(deg.std() / deg.mean()),
               clustering=3.0 * ntri / p2 if p2 > 0 else float('nan'),
               b1_cyclo=betti1_gf2(nbr, deg, N), nK4=None)
    if want_k4 and N <= DO_K4_UPTO:
        nK4 = k4_count(nbr, deg, N)
        out['nK4'] = nK4; out['K4_per_vertex'] = nK4 / N
    if want_spec and N <= DO_SPECTRAL_UPTO:
        r2, r3 = lap_walk_ratios(nbr, deg, N)
        out['lam2_lam1'] = r2; out['lam3_lam1'] = r3
    return out


# ----------------------------- FAMILLE A + C : N-platitude -------------------
def family_AC():
    print("\n########## FAMILLE A (ratios statiques) + C (spectraux) : N-platitude ##########")
    print("    (la N-platitude se juge a thermalisation COMPLETE = 120N ; sous-thermalise, tout derive)")
    NS = [2000, 10000, 50000, 100000]
    SEEDS = [0, 1, 2]
    agg = []
    for N in NS:
        nseed = SEEDS if N <= 50000 else SEEDS[:2]
        rows = []; t0 = time.time()
        for sd in nseed:
            nbr, deg = therm_graph(N, 6.6, sd)
            r = static_ratios(nbr, deg, N)
            rows.append(r)
            k4 = f"K4/N={r.get('K4_per_vertex', float('nan')):.2f}" if r.get('nK4') else "K4=skip"
            sp = (f"l2/l1={r.get('lam2_lam1', float('nan')):.3f}"
                  if 'lam2_lam1' in r else "spec=skip")
            print(f"  N={N:>7,} s{sd}: tri/E={r['tri_per_edge']:.3f} Gini={r['gini']:.4f} "
                  f"CVdeg={r['cv_deg']:.3f} clust={r['clustering']:.4f} {k4} {sp} "
                  f"({time.time()-t0:.0f}s)", flush=True)
            del nbr, deg; gc.collect()
        def m(k): return float(np.nanmean([x.get(k, np.nan) for x in rows]))
        def s(k): return float(np.nanstd([x.get(k, np.nan) for x in rows]))
        a = dict(N=N)
        for k in ['tri_per_edge', 'gini', 'tri_per_vertex', 'cv_deg', 'clustering',
                  'K4_per_vertex', 'lam2_lam1', 'lam3_lam1']:
            a[k + '_m'] = m(k); a[k + '_s'] = s(k)
        agg.append(a)
        json.dump(agg, open('banc_invariants.json', 'w'), indent=2)
    return agg


# ----------------------------- FAMILLE B : exposants -------------------------
def family_B():
    print("\n########## FAMILLE B (exposants de loi d'echelle) : invariants de FLOT ##########")
    NS = [2000, 5000, 10000, 25000, 50000]
    SEEDS = [0, 1]
    data = {k: {N: [] for N in NS} for k in ['b1', 'nK4']}
    for N in NS:
        for sd in SEEDS:
            nbr, deg = therm_graph(N, 6.6, sd)
            data['b1'][N].append(betti1_gf2(nbr, deg, N))
            if N <= DO_K4_UPTO:
                data['nK4'][N].append(k4_count(nbr, deg, N))
            del nbr, deg; gc.collect()
        print(f"  N={N:>6,}: b1={np.mean(data['b1'][N]):.0f}  "
              f"nK4={np.mean(data['nK4'][N]) if data['nK4'][N] else float('nan'):.0f}", flush=True)
    # fit des exposants, par graine, pour avoir une barre d'erreur
    res = {}
    for key in ['b1', 'nK4']:
        exps = []
        valid_N = [N for N in NS if data[key][N]]
        nrep = min(len(data[key][N]) for N in valid_N) if valid_N else 0
        for rep in range(nrep):
            xs = np.log(valid_N)
            ys = np.log([data[key][N][rep] for N in valid_N])
            exps.append(float(np.polyfit(xs, ys, 1)[0]))
        if exps:
            res[key] = dict(exp_mean=float(np.mean(exps)),
                            exp_std=float(np.std(exps)), exps=exps)
            print(f"  exposant {key}: {res[key]['exp_mean']:.3f} +/- "
                  f"{res[key]['exp_std']:.3f}")
    json.dump(res, open('banc_exposants.json', 'w'), indent=2)
    return res


# ----------------------------- FAMILLE A/C : kappa-platitude -----------------
def family_kappa():
    print("\n########## FAMILLE A+C : kappa-platitude (N fixe=20000) ##########")
    KS = [4.0, 5.5, 6.6, 8.0]
    N = 20000; SEEDS = [0, 1]
    perk = {}
    for kap in KS:
        rows = []
        for sd in SEEDS:
            nbr, deg = therm_graph(N, kap, sd)
            rows.append(static_ratios(nbr, deg, N, want_k4=False))
            del nbr, deg; gc.collect()
        def m(k): return float(np.nanmean([x.get(k, np.nan) for x in rows]))
        perk[kap] = {k: m(k) for k in ['tri_per_edge', 'gini', 'cv_deg',
                                       'clustering', 'lam2_lam1', 'lam3_lam1']}
        print(f"  kappa={kap}: tri/E={perk[kap]['tri_per_edge']:.3f} "
              f"Gini={perk[kap]['gini']:.4f} clust={perk[kap]['clustering']:.4f}", flush=True)
    json.dump({str(k): v for k, v in perk.items()},
              open('banc_kappa.json', 'w'), indent=2)
    return perk


def verdicts(agg_N, exps, perk):
    print("\n" + "=" * 70)
    print("VERDICTS PAR CANDIDAT")
    print("=" * 70)
    names = {'tri_per_edge': 'tri/arete', 'gini': 'Gini(masse)',
             'tri_per_vertex': 'tri/sommet', 'cv_deg': 'CV(degre)',
             'clustering': 'clustering', 'K4_per_vertex': 'K4/sommet (controle)',
             'lam2_lam1': 'lambda2/lambda1', 'lam3_lam1': 'lambda3/lambda1'}
    print("\n[A+C] RATIOS — N-platitude (2k->100k) ET kappa-platitude :")
    for key, nm in names.items():
        v0 = agg_N[0].get(key + '_m'); v1 = agg_N[-1].get(key + '_m')
        if v0 is None or v1 != v1 or v0 != v0:
            print(f"  {nm:<22}: (donnees insuffisantes)"); continue
        driftN = 100 * (v1 - v0) / v0 if v0 else float('nan')
        # kappa CV
        kvals = [perk[k][key] for k in perk if key in perk[k] and perk[k][key] == perk[k][key]]
        cvk = 100 * np.std(kvals) / np.mean(kvals) if kvals and np.mean(kvals) else float('nan')
        if 'controle' in nm:
            verdict = "PARAMETRE (attendu)" if abs(driftN) > 5 else "?? (devait deriver)"
        elif abs(driftN) < 3 and (cvk != cvk or cvk < 5):
            verdict = "INVARIANT (N-plat ET kappa-plat)"
        elif abs(driftN) < 3:
            verdict = f"N-plat mais kappa-DEPENDANT (CV_k={cvk:.0f}%) -> geometrique"
        else:
            verdict = "PARAMETRE (derive en N)"
        print(f"  {nm:<22}: N {v0:.4f}->{v1:.4f} ({driftN:+.1f}%) | "
              f"kappa CV={cvk:.1f}% => {verdict}")
    print("\n[B] EXPOSANTS — invariants de FLOT (stabilite multi-graines) :")
    for key, nm in [('b1', 'exposant b1~N^p'), ('nK4', 'exposant nK4~N^q')]:
        if key in exps:
            e = exps[key]
            verdict = ("CANDIDAT-FLOT stable" if e['exp_std'] < 0.03
                       else "BRUITE (exposant instable)")
            print(f"  {nm:<22}: {e['exp_mean']:.3f} +/- {e['exp_std']:.3f} => {verdict}")
    print("\nNote : un ratio 'INVARIANT' geometrique ne perce PAS le mur des valeurs")
    print("(theoreme V201) ; seuls des invariants de nature COUPLAGE le perceraient,")
    print("et le corpus n'en a trouve aucun. Les exposants de FLOT (famille B) sont")
    print("la piste neuve : un exposant stable multi-graines et kappa-universel serait")
    print("le 2e invariant. (cf. alpha_flow, teste separement.)")


def main():
    print("###### BANC UNIVERSEL D'INVARIANTS DU BLOB (jusqu'a N=100 000) ######")
    t0 = time.time()
    agg_N = family_AC()
    exps = family_B()
    perk = family_kappa()
    verdicts(agg_N, exps, perk)
    print(f"\nTermine en {(time.time()-t0)/60:.1f} min. "
          f"JSON : banc_invariants.json, banc_exposants.json, banc_kappa.json")


if __name__ == "__main__":
    main()
