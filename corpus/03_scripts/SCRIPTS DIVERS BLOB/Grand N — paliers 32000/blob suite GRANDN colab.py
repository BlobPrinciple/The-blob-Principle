#!/usr/bin/env python3
# =====================================================================
#  BLOB — SUITE DE MESURES COMPLÈTE (COLAB)  —  2 juillet 2026
#  Pousse toutes les quantités [M] décisives à grande échelle (N, GPU).
#  Instrument de mesure : NE prouve rien en [T]. Ce qui reste [T]
#  (L2, géométrogenèse, réfutation RP) reste une preuve, pas une mesure.
# =====================================================================
#
#  ENTIÈREMENT AUTONOME : coller ce fichier dans UNE cellule Colab et lancer.
#  Aucun upload. Moteur embarqué. JSONs dans ./blob_out/ après CHAQUE palier.
#    - Runtime > GPU recommandé (transport optimal mésoscopique plus rapide).
#
#  CONFIG : régler PALIERS, SEEDS, SENSORS ci-dessous.
# =====================================================================

import os, sys, json, time, math, platform, warnings
import numpy as np
from collections import deque, defaultdict
from itertools import combinations
warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------
#  CONFIG  — calage des paliers et des capteurs
# ---------------------------------------------------------------------
KAPPA        = 6.6
PALIERS      = [32000]                     # SEUL point manquant (8000/16000 deja en main)
SEEDS        = [1, 2, 3, 4, 5, 6, 7, 8]    # 8 graines : fiabilise d_w (variance) + Var/N (L1)
OUTDIR       = "./blob_out"

# plafonds de N par capteur coûteux (au-delà : capteur sauté)
CAP_K4       = 16000     # find_all_K4 : fatness, Regge, structure
CAP_OT_MICRO = 8000      # Ollivier microscopique (OT 1-hop)
CAP_OT_MESO  = 0         # COUPE (O(N^2) memoire -> plantait a 32000)
CAP_RP       = 4000      # matrice de réflexion (positivité)
CAP_ALLPAIRS = 0         # COUPE (toutes-paires O(N^2) memoire)

# MCMC : facteurs de burn/production (équilibration)
BURN_F, PROD_F = 24, 4   # grand N : legerement reduit, reste equilibre

# Capteur RP : nombre d'échantillons Gibbs (COÛTEUX — chaque échantillon = 1 MCMC complet).
# Le corpus a déjà trouvé ce test non concluant ; le garder modeste. Mettre 0 pour désactiver.
REFLECTION_SAMPLES = 24

SENSORS = dict(   # activer/désactiver
    df=True, dw=True, ds=True, moments=True, ahlfors=True, chemdist=True,
    concentration=True, meanfield=True,
    # GRAND N : capteurs O(N^2)/memoire COUPES
    fatness=False, regge=False, ollivier_micro=False, ollivier_meso=False,
    reflection=False, structural=True,
)

# ---------------------------------------------------------------------
#  SETUP  — GPU, POT, environnement (précaution #3 : documentation)
# ---------------------------------------------------------------------
os.makedirs(OUTDIR, exist_ok=True)
try:
    import ot                      # POT : transport optimal
    HAVE_OT = True
except Exception:
    HAVE_OT = False
    os.system("pip -q install pot >/dev/null 2>&1")
    try:
        import ot; HAVE_OT = True
    except Exception:
        HAVE_OT = False
from scipy.optimize import brentq, linprog

def gpu_info():
    try:
        import torch
        return torch.cuda.is_available(), (torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu")
    except Exception:
        return False, "no-torch"
HAS_GPU, GPU_NAME = gpu_info()

ENV = dict(
    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
    python=sys.version.split()[0], numpy=np.__version__,
    platform=platform.platform(), have_ot=HAVE_OT, gpu=HAS_GPU, gpu_name=GPU_NAME,
    kappa=KAPPA, paliers=PALIERS, seeds=SEEDS, burn_f=BURN_F, prod_f=PROD_F,
)

# ---------------------------------------------------------------------
#  MOTEUR EMBARQUÉ (Blob V137 — autonome, aucun upload requis)
# ---------------------------------------------------------------------
from scipy.spatial import KDTree
import numpy as np
import math, time, json
from collections import deque
from scipy.spatial import KDTree

# ------------------------------------------------------------------ PARAMÈTRES
BETA  = 0.30      # coefficient de désordre (A4)
TAU   = 0.50      # température combinatoire (A5), effective = TAU/N
THETA = 0.50      # seuil de stabilité temporelle (A6) = (kappa0-2)/kappa0
# kappa = E/N attendu ; kappa=4 => E0=2N => degré moyen <d>=4
# (rappel convention : <d> = 2*E/N)

# --------------------------------------------------------- CONSTRUCTION GRAPHE
def rips_radius(N, kappa, mult=1.0):
    """Rayon de portée pour obtenir E0 = N*kappa/2 arêtes en moyenne (A3)."""
    return mult * (kappa / ((N - 1) * (4/3) * math.pi)) ** (1/3)

def E0_target(N, kappa):
    return max(N - 1, int(N * kappa / 2))

def lcc_size(adj, N):
    """Taille de la plus grande composante connexe."""
    seen = [False]*N; best = 0
    for s in range(N):
        if not seen[s]:
            sz = 0; q = deque([s]); seen[s] = True
            while q:
                v = q.popleft(); sz += 1
                for w in adj[v]:
                    if not seen[w]: seen[w] = True; q.append(w)
            best = max(best, sz)
    return best

def build_initial(N, seed, kappa, pool_mult=1.6):
    """Construit le RGG 3D initial avec E0 arêtes et un pool d'arêtes candidates."""
    r = rips_radius(N, kappa); r_p = pool_mult * r
    E0 = E0_target(N, kappa)
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0.0, 1.0, (N, 3))
    tree = KDTree(pts)
    adj = [set() for _ in range(N)]
    for i, j in tree.query_pairs(r):
        adj[i].add(j); adj[j].add(i)
    pool = list(tree.query_pairs(r_p))
    rng2 = np.random.default_rng(seed + 50_000)
    K = sum(len(adj[i]) for i in range(N)) // 2
    att = 0; max_att = 10 * abs(E0 - K) + 5000
    while K != E0 and att < max_att:
        att += 1
        if K < E0:
            if not pool: break
            u, v = pool[rng2.integers(len(pool))]
            if v not in adj[u]: adj[u].add(v); adj[v].add(u); K += 1
        else:
            edges = [(i, j) for i in range(N) for j in adj[i] if j > i]
            if not edges: break
            u, v = edges[rng2.integers(len(edges))]
            adj[u].discard(v); adj[v].discard(u)
            if lcc_size(adj, N) == N: K -= 1
            else: adj[u].add(v); adj[v].add(u)
    return pts, adj, pool, E0

# ----------------------------------------------------------- VIABILITÉ (A4)
def count_triangles(adj, N):
    n = 0
    for i in range(N):
        for j in adj[i]:
            if j > i:
                n += len(adj[i] & adj[j] & set(k for k in adj[j] if k > j))
    return n

def compute_S(adj, n_tri, N, gamma=0.0):
    """Fonctionnelle de viabilité S = log(1+n_tri) - beta*D - gamma*E/N (A4)."""
    degs = np.array([len(adj[i]) for i in range(N)], float)
    D = degs.std() / (degs.mean() + 1e-8)
    E = degs.sum() / 2.0
    return math.log(1 + n_tri) - BETA * D - gamma * E / N

def still_connected(adj, u, v, N):
    """Vérifie que retirer l'arête (u,v) ne déconnecte pas le graphe."""
    seen = {u}; q = deque([u])
    while q:
        node = q.popleft()
        for w in adj[node]:
            if w in seen: continue
            if (node == u and w == v) or (node == v and w == u): continue
            seen.add(w); q.append(w)
            if w == v: return True
    return False

def run_mcmc_canonical(pts, adj_init, pool, N, E0, seed, burn_f=50, prod_f=80):
    """Dynamique de viabilité à E fixé (échange d'arêtes). A5."""
    tau_eff = TAU / N
    rng = np.random.default_rng(seed + 200_000)
    adj = [set(a) for a in adj_init]
    edge_list = [(i, j) for i in range(N) for j in adj[i] if j > i]
    if not edge_list or not pool: return adj
    n_tri = count_triangles(adj, N)
    S_curr = compute_S(adj, n_tri, N)
    pool_arr = np.array(pool, dtype=np.int32); n_pool = len(pool_arr)
    for step in range((burn_f + prod_f) * N):
        if not edge_list: break
        io = int(rng.integers(len(edge_list))); u, v = edge_list[io]
        e_in = None
        for _ in range(30):
            ii = int(rng.integers(n_pool)); a, b = int(pool_arr[ii,0]), int(pool_arr[ii,1])
            if b not in adj[a]: e_in = (a, b); break
        if e_in is None: continue
        a, b = e_in
        if len(adj[u]) <= 2 or len(adj[v]) <= 2:
            if not still_connected(adj, u, v, N): continue
        tl = len(adj[u] & adj[v])
        adj[u].discard(v); adj[v].discard(u)
        adj[a].add(b); adj[b].add(a)
        tg = len(adj[a] & adj[b])
        nt = n_tri - tl + tg
        S_new = compute_S(adj, nt, N)
        if S_new - S_curr >= 0 or rng.random() < math.exp((S_new - S_curr) / tau_eff):
            n_tri = nt; S_curr = S_new; edge_list[io] = (a, b)
        else:
            adj[u].add(v); adj[v].add(u); adj[a].discard(b); adj[b].discard(a)
    return adj

def run_mcmc_grand_canonical(pts, adj_init, pool, N, seed, gamma, burn_f=40, prod_f=60):
    """Dynamique de viabilité à E LIBRE (ajout/suppression). Densité émergente. A5+III."""
    tau_eff = TAU / N
    rng = np.random.default_rng(seed + 300_000)
    adj = [set(a) for a in adj_init]
    pool_arr = np.array(pool, dtype=np.int32) if pool else np.empty((0,2),dtype=np.int32)
    n_pool = len(pool_arr); n_tri = count_triangles(adj, N)
    S_curr = compute_S(adj, n_tri, N, gamma)
    for step in range((burn_f + prod_f) * N):
        move = rng.integers(3)
        if move == 1 and n_pool > 0:           # AJOUT
            ii = int(rng.integers(n_pool)); a, b = int(pool_arr[ii,0]), int(pool_arr[ii,1])
            if b in adj[a]: continue
            tg = len(adj[a] & adj[b]); adj[a].add(b); adj[b].add(a)
            S_new = compute_S(adj, n_tri + tg, N, gamma)
            if S_new - S_curr >= 0 or rng.random() < math.exp((S_new - S_curr)/tau_eff):
                n_tri += tg; S_curr = S_new
            else: adj[a].discard(b); adj[b].discard(a)
        elif move == 2:                          # SUPPRESSION
            edges = [(i,j) for i in range(N) for j in adj[i] if j > i]
            if not edges: continue
            u, v = edges[int(rng.integers(len(edges)))]
            if len(adj[u]) <= 1 or len(adj[v]) <= 1: continue
            tl = len(adj[u] & adj[v]); adj[u].discard(v); adj[v].discard(u)
            S_new = compute_S(adj, n_tri - tl, N, gamma)
            if S_new - S_curr >= 0 or rng.random() < math.exp((S_new - S_curr)/tau_eff):
                n_tri -= tl; S_curr = S_new
            else: adj[u].add(v); adj[v].add(u)
    return adj

# ------------------------------------------------------- TOPOLOGIE DU LINK
def link_topology(adj, v):
    """Renvoie (n_K3, n_K4, chi) pour le sommet v. Théorème T1."""
    nb = list(adj[v]); d = len(nb)
    if d == 0: return 0, 0, 0
    link_adj = {w: set() for w in nb}
    nK3 = 0
    for i, a in enumerate(nb):
        for b in nb[i+1:]:
            if b in adj[a]:
                nK3 += 1; link_adj[a].add(b); link_adj[b].add(a)
    nK4 = 0
    for a in nb:
        la = list(link_adj[a])
        for i, x in enumerate(la):
            for y in la[i+1:]:
                if y in link_adj[x]: nK4 += 1
    nK4 //= 3
    return nK3, nK4, d - nK3 + nK4

def find_all_K4(adj, N):
    out = []
    for i in range(N):
        Ni = adj[i]
        for j in Ni:
            if j <= i: continue
            cij = Ni & adj[j]
            for k in cij:
                if k <= j: continue
                for l in (cij & adj[k]):
                    if l > k: out.append((i, j, k, l))
    return out

def neighbor_stability(adj0, adj1, N):
    """Stabilité f(v) = Jaccard des voisinages entre deux états (A6)."""
    f = np.zeros(N)
    for v in range(N):
        n0, n1 = adj0[v], adj1[v]
        u = n0 | n1
        f[v] = 1.0 if len(u) == 0 else len(n0 & n1) / len(u)
    return f

# --------------------------------------------------- CLASSIFICATION (Déf IV.1)
def classify_phases(adj_eq, adj_evolved, N, theta=THETA):
    """
    Définition EXACTE des trois phases (Partie IV.1) :
      - Λ        : n_K3 = 0  (aucun triangle)  + résidus de cœurs sous le seuil chi
      - DM       : dans un triangle, hors cœur baryonique stable
      - baryon   : dans un K4 stable (f>theta) ET chi(link) >= <chi> intrinsèque
    Renvoie (f_L, f_DM, f_b).
    """
    f_stable = neighbor_stability(adj_eq, adj_evolved, N)
    V_stable = {v for v in range(N) if f_stable[v] > theta}
    # sommets dans un triangle
    V_in_tri = set()
    for i in range(N):
        ni = adj_eq[i]
        for j in ni:
            if j <= i: continue
            common = ni & adj_eq[j]
            if common:
                V_in_tri.add(i); V_in_tri.add(j)
                V_in_tri.update(k for k in common if k > j)
    V_isolated = set(range(N)) - V_in_tri
    # sommets dans un K4
    V_in_K4 = set()
    for K in find_all_K4(adj_eq, N):
        for v in K: V_in_K4.add(v)
    V_K4_stable = V_in_K4 & V_stable
    if not V_K4_stable:
        return len(V_isolated)/N, (len(V_in_tri))/N, 0.0
    # seuil intrinsèque chi >= <chi>
    chi_pv = {v: link_topology(adj_eq, v)[2] for v in V_K4_stable}
    chi_mean = np.mean(list(chi_pv.values()))
    V_b = {v for v, c in chi_pv.items() if c >= chi_mean}
    V_K4_residual = V_K4_stable - V_b           # cœurs sous le seuil -> Λ
    V_DM = V_in_tri - V_K4_stable
    V_L = V_isolated | V_K4_residual
    return len(V_L)/N, len(V_DM)/N, len(V_b)/N

# ------------------------------------------------------ DIMENSION DE HAUSDORFF
def hausdorff_dim(adj, N, n_src=10):
    """Dimension de Hausdorff par croissance de boules géodésiques."""
    rng = np.random.default_rng(7)
    nodes = [v for v in range(N) if adj[v]]
    if len(nodes) < 15: return None
    slopes = []
    for _ in range(n_src):
        src = nodes[rng.integers(len(nodes))]
        dist = {src: 0}; q = deque([src])
        while q:
            v = q.popleft()
            for w in adj[v]:
                if w not in dist: dist[w] = dist[v]+1; q.append(w)
        rmax = max(dist.values())
        if rmax < 3: continue
        rs = np.arange(1, int(rmax*0.7)+1)
        cnt = np.array([sum(1 for dd in dist.values() if dd <= r) for r in rs], float)
        m = cnt >= 3
        if m.sum() < 3: continue
        s = np.polyfit(np.log(rs[m]), np.log(cnt[m]), 1)[0]
        slopes.append(s)
    return (float(np.mean(slopes)), float(np.std(slopes))) if slopes else None

# --- shim de compatibilité : B.foo -> fonctions embarquées ci-dessus ---
class _B: pass
B = _B()
for _name in ['rips_radius','E0_target','lcc_size','build_initial','count_triangles',
              'compute_S','still_connected','run_mcmc_canonical','run_mcmc_grand_canonical',
              'link_topology','find_all_K4','neighbor_stability','classify_phases','hausdorff_dim']:
    setattr(B, _name, globals()[_name])
B.TAU = TAU; B.BETA = BETA; B.THETA = THETA
# ======================================================================

TAU, BETA = B.TAU, B.BETA

def build_blob(N, seed, kappa=KAPPA):
    """Retourne (pts, adjB, adj0, pool) : Blob equilibre + RGG de reference (memes points)."""
    pts, adj0, pool, E0 = B.build_initial(N, seed, kappa)
    adjB = B.run_mcmc_canonical(pts, adj0, pool, N, E0, seed, burn_f=BURN_F, prod_f=PROD_F)
    return pts, adjB, adj0, pool

# =====================================================================
#  HELPERS  (BFS, distances, transport optimal, geometrie)
# =====================================================================
def bfs(adj, src, N, cap=10**9):
    dist = np.full(N, -1, dtype=np.int32); dist[src] = 0; q = deque([src])
    while q:
        x = q.popleft()
        if dist[x] >= cap: continue
        for w in adj[x]:
            if dist[w] < 0: dist[w] = dist[x] + 1; q.append(w)
    return dist

def all_pairs(adj, N):
    D = np.full((N, N), 10**6, dtype=np.int32)
    for s in range(N):
        d = bfs(adj, s, N); D[s] = np.where(d < 0, 10**6, d)
    return D

def W1(a, b, C):
    """Wasserstein-1 exact (POT) sinon LP scipy."""
    if HAVE_OT:
        return float(ot.emd2(a, b, C))
    n, m = C.shape; c = C.flatten(); Aeq = []; beq = []
    for i in range(n):
        r = np.zeros(n*m); r[i*m:(i+1)*m] = 1; Aeq.append(r); beq.append(a[i])
    for j in range(m):
        r = np.zeros(n*m); r[j::m] = 1; Aeq.append(r); beq.append(b[j])
    return float(linprog(c, A_eq=np.array(Aeq), b_eq=np.array(beq),
                         bounds=[(0, None)]*(n*m), method='highs').fun)

def W1_sinkhorn(a, b, C, reg=0.3):
    if HAVE_OT:
        return float(ot.sinkhorn2(a, b, C, reg))
    K = np.exp(-C/reg) + 1e-300; u = np.ones(len(a))
    for _ in range(400):
        v = b/(K.T@u + 1e-300); u = a/(K@v + 1e-300)
    return float(np.sum((u[:, None]*K*v[None, :])*C))

def dihedral(P):
    """P = 4x3 : les 6 angles diedres du tetraedre, par arete."""
    ang = {}
    for (i, j) in combinations(range(4), 2):
        k, l = [x for x in range(4) if x != i and x != j]
        e = P[j]-P[i]; e = e/(np.linalg.norm(e)+1e-15)
        cp = (P[k]-P[i]) - np.dot(P[k]-P[i], e)*e
        dp = (P[l]-P[i]) - np.dot(P[l]-P[i], e)*e
        cp /= (np.linalg.norm(cp)+1e-15); dp /= (np.linalg.norm(dp)+1e-15)
        ang[(i, j)] = float(np.arccos(np.clip(np.dot(cp, dp), -1, 1)))
    return ang

sig  = lambda x: 1/(1+np.exp(-x))
sigp = lambda x: sig(x)*(1-sig(x))
def torus_d(a, b):
    d = np.abs(a-b); return np.linalg.norm(np.minimum(d, 1-d))

# =====================================================================
#  CAPTEURS SUP-1
# =====================================================================
def sensor_df(adj, N, pts, n_src=16, seed=0):
    """d_f : croissance de boules geodesiques  |B(x,r)| ~ r^df."""
    rng = np.random.default_rng(seed); nodes = [v for v in range(N) if adj[v]]; sl = []
    for _ in range(n_src):
        s = nodes[rng.integers(len(nodes))]; d = bfs(adj, s, N); rmax = d[d >= 0].max()
        if rmax < 4: continue
        rs = np.arange(1, int(rmax*0.7)+1)
        cnt = np.array([np.sum((d >= 0) & (d <= r)) for r in rs], float)
        m = cnt >= 3
        if m.sum() < 3: continue
        sl.append(float(np.polyfit(np.log(rs[m]), np.log(cnt[m]), 1)[0]))
    return dict(df=float(np.mean(sl)) if sl else None, df_std=float(np.std(sl)) if sl else None)

def sensor_dw(adj, N, n_src=10, n_walks=1200, seed=0):
    """d_w : MSD, fenetre PRE-SATURATION auto-calee sur le diametre mesure.
    CORRECTIF (2 juillet nuit) : la fenetre fixe 8-60 depassait la saturation
    et gonflait d_w (~3 au lieu de ~2.3). On mesure le diametre chimique et on
    borne la fenetre a < diametre/2. Retourne aussi la version 'tardive' pour diagnostic."""
    rng = np.random.default_rng(seed); nodes = [v for v in range(N) if adj[v]]
    adjL = {v: list(adj[v]) for v in nodes}
    diam_samples = []
    tmax = 160
    msd = np.zeros(tmax+1); cnt = np.zeros(tmax+1)
    for _ in range(n_src):
        s = nodes[rng.integers(len(nodes))]; d = bfs(adj, s, N)
        dm = int(d[d >= 0].max()); diam_samples.append(dm)
        if dm < 10: continue
        for _ in range(n_walks):
            x = s
            for t in range(1, tmax+1):
                nb = adjL[x]; x = nb[rng.integers(len(nb))]
                if d[x] >= 0: msd[t] += d[x]**2; cnt[t] += 1
    diam = float(np.mean(diam_samples)) if diam_samples else 0.0
    msd = msd[1:]/np.maximum(cnt[1:], 1); ts = np.arange(1, tmax+1)
    # fenetre PRE-SATURATION : de 3 a diam*0.5 (jamais au-dela de la saturation)
    hi_ps = max(6, int(diam*0.5)); lo_ps = 3
    def fit(lo, hi):
        m = (ts >= lo) & (ts <= hi) & (msd > 0)
        if m.sum() < 3: return None
        return float(2.0/np.polyfit(np.log(ts[m]), np.log(msd[m]), 1)[0])
    dw_ps = fit(lo_ps, hi_ps)          # <-- la BONNE valeur (pre-saturation)
    dw_late = fit(8, 60)              # <-- diagnostic (contaminee) pour comparaison
    return dict(dw=dw_ps, dw_presaturation=dw_ps, dw_late_contaminated=dw_late,
                chem_diameter=diam, dw_window=[lo_ps, hi_ps])

def sensor_moments(adj, N, pts, radius=2.0):
    """Moments de volume (Bella-Schaffner) : E[rho^4], E[rho^-4] finis <=> condition OK."""
    # densite locale via boule geodesique de rayon 2
    nodes = [v for v in range(N) if adj[v]]; vol = []
    rng = np.random.default_rng(0)
    for s in rng.choice(nodes, min(400, len(nodes)), replace=False):
        d = bfs(adj, s, N, cap=int(radius))
        vol.append(int(np.sum((d >= 0) & (d <= radius))))
    vol = np.array(vol, float); rho = vol/np.mean(vol)
    return dict(E_rho4=float(np.mean(rho**4)), E_rho_m4=float(np.mean(rho**(-4.0))),
                vol_med=float(np.median(vol)))

def sensor_ahlfors(adj, N, pts):
    """Ahlfors : ratio p10/mediane des densites locales par echelle (regularite de volume)."""
    nodes = [v for v in range(N) if adj[v]]; out = {}
    rng = np.random.default_rng(0); S = rng.choice(nodes, min(300, len(nodes)), replace=False)
    for r in [1, 2, 3, 4]:
        vs = []
        for s in S:
            d = bfs(adj, s, N, cap=r); vs.append(int(np.sum((d >= 0) & (d <= r))))
        vs = np.array(vs, float)
        out[f"ahlfors_r{r}"] = float(np.percentile(vs, 10)/(np.median(vs)+1e-9))
    return out

def sensor_chemdist(adjB, adj0, N, pts, n_src=10):
    """L2 : distance chimique du recable vs RGG (memes points, paires lointaines)."""
    r = B.rips_radius(N, KAPPA, 1.0); rng = np.random.default_rng(0)
    nodes = [v for v in range(N) if adjB[v] and adj0[v]]
    srcs = rng.choice(nodes, min(n_src, len(nodes)), replace=False)
    ratios, strB, strR = [], [], []
    for s in srcs:
        dB = bfs(adjB, s, N); dR = bfs(adj0, s, N)
        for t in nodes:
            de = torus_d(pts[s], pts[t])
            if de > 0.35 and dB[t] > 0 and dR[t] > 0:
                ratios.append(dB[t]/dR[t]); strB.append(dB[t]*r/de); strR.append(dR[t]*r/de)
    ratios = np.array(ratios)
    return dict(chem_ratio_mean=float(ratios.mean()), chem_ratio_med=float(np.median(ratios)),
                chem_ratio_max=float(ratios.max()), stretch_blob=float(np.mean(strB)),
                stretch_rgg=float(np.mean(strR)))

def sensor_meanfield(adjB, N, pool):
    """Point 3 : constantes de champ moyen + |Phi'(p*)| (contraction)."""
    nE = sum(len(adjB[v]) for v in range(N))//2
    ntri = B.count_triangles(adjB, N); npool = len(pool)
    p = nE/npool; rho = ntri/N; z = 2*npool/N; delta = 3*ntri/max(nE, 1)
    L_tri = delta/(TAU*rho)
    try:
        beta_eff = brentq(lambda b: sig(L_tri-b)-p, -30, 30); Lstar = L_tri-beta_eff
        phiprime = float(sigp(Lstar)*L_tri/p)
    except Exception:
        beta_eff = Lstar = phiprime = None
    return dict(p_star=float(p), rho_star=float(rho), z_pool=float(z), delta=float(delta),
                L_tri=float(L_tri), beta_eff=beta_eff, phi_prime=phiprime,
                n_tri=int(ntri), n_edges=int(nE))

# =====================================================================
#  CAPTEURS GRAVITÉ (Phase 1.2)
# =====================================================================
def sensor_fatness(adj, N, pts, k4=None):
    """Fatness Theta=V/L^3 des K4, fraction de slivers, volume porte."""
    if k4 is None: k4 = B.find_all_K4(adj, N)
    Th, Vol = [], []
    for q in k4:
        P = pts[list(q)]
        e = [np.linalg.norm(P[i]-P[j]) for i in range(4) for j in range(i+1, 4)]
        L = max(e); V = abs(np.linalg.det(np.array([P[1]-P[0], P[2]-P[0], P[3]-P[0]])))/6
        Th.append(V/(L**3+1e-15)); Vol.append(V)
    Th, Vol = np.array(Th), np.array(Vol); thr = 0.05*0.117
    sl = Th < thr
    return dict(n_K4=len(k4), theta_med=float(np.median(Th)),
                sliver_frac=float(sl.mean()), sliver_vol_frac=float(Vol[sl].sum()/(Vol.sum()+1e-15)),
                theta_p1=float(np.percentile(Th, 1)), theta_p5=float(np.percentile(Th, 5)))

def sensor_regge(adj, N, pts, k4=None):
    """Test de variete : #tetra par 2-face (variete=2) + somme diedres/arete (2pi)."""
    if k4 is None: k4 = B.find_all_K4(adj, N)
    face_ct = defaultdict(int); edge_dih = defaultdict(float)
    for q in k4:
        v = list(q); P = pts[v]
        for f in combinations(v, 3): face_ct[frozenset(f)] += 1
        ang = dihedral(P)
        for a, (i, j) in enumerate(combinations(range(4), 2)):
            edge_dih[frozenset((v[i], v[j]))] += ang[(i, j)]
    fc = np.array(list(face_ct.values())); S = np.array(list(edge_dih.values()))
    return dict(faces_per_2face_mean=float(fc.mean()), faces_eq2_frac=float((fc == 2).mean()),
                faces_gt2_frac=float((fc > 2).mean()), faces_max=int(fc.max()),
                dihsum_mean=float(S.mean()), dihsum_near_2pi_frac=float((np.abs(S-2*np.pi) < 0.5).mean()))

def _ollivier(adj, D, N, edges, delta):
    ks = []
    for (u, v) in edges:
        Bu = np.where(D[u] <= delta)[0]; Bv = np.where(D[v] <= delta)[0]
        if len(Bu) < 2 or len(Bv) < 2: continue
        C = D[np.ix_(Bu, Bv)].astype(float)
        a = np.ones(len(Bu))/len(Bu); b = np.ones(len(Bv))/len(Bv)
        w = W1_sinkhorn(a, b, C) if (len(Bu)*len(Bv) > 2500) else W1(a, b, C)
        d = float(D[u, v]); ks.append(1.0 - w/d)
    return float(np.mean(ks)) if ks else None

def sensor_ollivier_micro(adjB, adj0, N, n_edges=200, seed=0):
    """Ollivier microscopique (delta=1, OT exact) Blob vs RGG."""
    rng = np.random.default_rng(seed)
    def sample(adj):
        E = [(i, j) for i in range(N) for j in adj[i] if j > i]
        if not E: return None
        S = [E[k] for k in rng.choice(len(E), min(n_edges, len(E)), replace=False)]
        ks = []
        for (u, v) in S:
            Nu, Nv = list(adj[u]), list(adj[v])
            if not Nu or not Nv: continue
            tt = set(Nv)
            Dd = {}
            for s in Nu:
                dist = {s: 0}; q = deque([s])
                while q:
                    x = q.popleft()
                    if dist[x] >= 4: continue
                    for w in adj[x]:
                        if w not in dist: dist[w] = dist[x]+1; q.append(w)
                Dd[s] = [dist.get(t, 5) for t in Nv]
            C = np.array([Dd[s] for s in Nu], float)
            ks.append(1.0 - W1(np.ones(len(Nu))/len(Nu), np.ones(len(Nv))/len(Nv), C))
        return float(np.mean(ks)) if ks else None
    return dict(ollivier_micro_blob=sample(adjB), ollivier_micro_rgg=sample(adj0))

def sensor_ollivier_meso(adjB, adj0, N, DB, DR, n_edges=60, seed=0):
    """Ollivier mesoscopique (delta=1,2,3,4) Blob vs RGG — LE test decisif gravite."""
    rng = np.random.default_rng(seed); out = {}
    def edges(adj):
        E = [(i, j) for i in range(N) for j in adj[i] if j > i]
        return [E[k] for k in rng.choice(len(E), min(n_edges, len(E)), replace=False)]
    eB, eR = edges(adjB), edges(adj0)
    for delta in [1, 2, 3, 4]:
        kB = _ollivier(adjB, DB, N, eB, delta); kR = _ollivier(adj0, DR, N, eR, delta)
        out[f"ollivier_meso_blob_d{delta}"] = kB
        out[f"ollivier_meso_rgg_d{delta}"]  = kR
        out[f"ollivier_meso_gap_d{delta}"]  = (kB-kR) if (kB is not None and kR is not None) else None
    return out

# =====================================================================
#  CAPTEUR PHASE 2 — positivité de réflexion (matrice de réflexion)
# =====================================================================
def sensor_reflection(pts, pool, N, seed, n_samples=40, n_func=8):
    """Test RP : matrice M_ij=<theta(F_i)F_j>, plan x=0.5. Valeur propre min <0 => RP refute."""
    # fonctions locales F = 1[arete (a,b) presente], a,b dans le demi x>0.5, et leur reflexion x->1-x
    half = [i for i in range(N) if pts[i, 0] > 0.5]
    # apparier chaque point du demi a son reflechi le plus proche
    rng = np.random.default_rng(seed)
    poolset = set(map(frozenset, pool))
    # choisir n_func paires d'aretes candidates dans le demi
    cand = [e for e in pool if pts[e[0], 0] > 0.5 and pts[e[1], 0] > 0.5]
    if len(cand) < n_func: return dict(rp_min_eig=None)
    F = [cand[k] for k in rng.choice(len(cand), n_func, replace=False)]
    # reflexion : trouver l'arete miroir (points reflechis les plus proches)
    def mirror(e):
        best = []
        for v in e:
            p = pts[v].copy(); p[0] = 1-p[0]
            j = min(half+[i for i in range(N) if pts[i, 0] <= 0.5],
                    key=lambda k: np.linalg.norm(pts[k]-p))
            best.append(j)
        return tuple(best)
    Fm = [mirror(e) for e in F]
    # echantillons Gibbs
    samples = []
    for s in range(n_samples):
        _, adjB, _, _ = build_blob(N, 10000+seed*100+s)
        samples.append(adjB)
    def val(adj, e): return 1.0 if (e[1] in adj[e[0]]) else 0.0
    M = np.zeros((n_func, n_func))
    for adj in samples:
        fi = np.array([val(adj, F[i]) for i in range(n_func)])
        fmi = np.array([val(adj, Fm[i]) for i in range(n_func)])
        M += np.outer(fmi, fi)
    M /= len(samples); M = 0.5*(M+M.T)
    eig = float(np.linalg.eigvalsh(M).min())
    return dict(rp_min_eig=eig, rp_note="min_eig<0 => RP refute (sinon non concluant)")

# =====================================================================
#  CAPTEURS STRUCTURELS
# =====================================================================
def sensor_structural(adjB, adj0, N, pts):
    degB = np.array([len(adjB[v]) for v in range(N)])
    degR = np.array([len(adj0[v]) for v in range(N)])
    ntriB = B.count_triangles(adjB, N)
    return dict(
        deg_mean=float(degB.mean()), deg_max=int(degB.max()),
        deg_max_over_logN=float(degB.max()/math.log(N)),   # Penrose : borne ~ A log N
        cv_deg=float(degB.std()/(degB.mean()+1e-9)),
        lcc_blob=float(B.lcc_size(adjB, N)/N), lcc_rgg=float(B.lcc_size(adj0, N)/N),
        n_tri=int(ntriB), rho_tri=float(ntriB/N),
        clustering_gain=float(ntriB/max(B.count_triangles(adj0, N), 1)),
    )

# =====================================================================
#  BOUCLE PRINCIPALE  — scan paliers × graines, JSON par palier
# =====================================================================
def run_palier(N):
    print(f"\n{'='*60}\n PALIER N={N}\n{'='*60}", flush=True)
    per_seed = []
    for seed in SEEDS:
        t0 = time.time(); rec = dict(N=N, seed=seed); pts = None
        try:
            pts, adjB, adj0, pool = build_blob(N, seed)
            k4 = None
            if (SENSORS['fatness'] or SENSORS['regge']) and N <= CAP_K4:
                k4 = B.find_all_K4(adjB, N)
            need_D = (SENSORS['ollivier_meso']) and N <= CAP_OT_MESO and N <= CAP_ALLPAIRS
            DB = DR = None
            if need_D:
                DB = all_pairs(adjB, N); DR = all_pairs(adj0, N)

            if SENSORS['df']:            rec.update(sensor_df(adjB, N, pts, seed=seed))
            if SENSORS['dw']:            rec.update(sensor_dw(adjB, N, seed=seed))
            if SENSORS['ds'] and rec.get('df') and rec.get('dw'):
                rec['ds'] = 2*rec['df']/rec['dw']
            if SENSORS['moments']:       rec.update(sensor_moments(adjB, N, pts))
            if SENSORS['ahlfors']:       rec.update(sensor_ahlfors(adjB, N, pts))
            if SENSORS['chemdist']:      rec.update(sensor_chemdist(adjB, adj0, N, pts))
            if SENSORS['meanfield']:     rec.update(sensor_meanfield(adjB, N, pool))
            if SENSORS['structural']:    rec.update(sensor_structural(adjB, adj0, N, pts))
            if SENSORS['fatness'] and k4 is not None: rec.update(sensor_fatness(adjB, N, pts, k4))
            if SENSORS['regge']   and k4 is not None: rec.update(sensor_regge(adjB, N, pts, k4))
            if SENSORS['ollivier_micro'] and N <= CAP_OT_MICRO:
                rec.update(sensor_ollivier_micro(adjB, adj0, N, seed=seed))
            if SENSORS['ollivier_meso'] and DB is not None:
                rec.update(sensor_ollivier_meso(adjB, adj0, N, DB, DR, seed=seed))
            if SENSORS['reflection'] and N <= CAP_RP and REFLECTION_SAMPLES > 0:
                rec.update(sensor_reflection(pts, pool, N, seed, n_samples=REFLECTION_SAMPLES))
            rec['ok'] = True
        except Exception as e:
            rec['ok'] = False; rec['error'] = f"{type(e).__name__}: {e}"
        rec['seconds'] = round(time.time()-t0, 1)
        print(f"  seed {seed}: {rec['seconds']}s  "
              f"dw={rec.get('dw')}  ds={rec.get('ds')}  chem_ratio={rec.get('chem_ratio_mean')}  "
              f"phi'={rec.get('phi_prime')}  sliver={rec.get('sliver_frac')}", flush=True)
        per_seed.append(rec)
        # SAUVEGARDE INCREMENTALE apres chaque graine (anti-perte sur deconnexion)
        try:
            import json as _json
            _json.dump({'N': N, 'per_seed_partial': per_seed},
                       open(f"{OUTDIR}/palier_{N}_partial.json", "w"))
        except Exception:
            pass
    # agregation par palier (moyenne + ecart-type sur graines) — inclut L1 (std/moy, Var/N)
    agg = {'N': N, 'n_seeds': len(per_seed)}
    keys = set().union(*[set(r.keys()) for r in per_seed]) - {'N', 'seed', 'ok', 'error', 'seconds', 'rp_note'}
    for k in keys:
        vals = [r[k] for r in per_seed if isinstance(r.get(k), (int, float))]
        if vals:
            agg[f"{k}_mean"] = float(np.mean(vals)); agg[f"{k}_std"] = float(np.std(vals))
    # L1 : concentration & susceptibilite de n_tri sur graines
    ntri = [r['n_tri'] for r in per_seed if 'n_tri' in r]
    if len(ntri) >= 2:
        ntri = np.array(ntri, float)
        agg['L1_std_over_mean'] = float(ntri.std()/ntri.mean())
        agg['L1_susceptibility_Var_over_N'] = float(ntri.var(ddof=1)/N)
    return dict(palier=agg, per_seed=per_seed)

def main():
    print(json.dumps(ENV, indent=2), flush=True)
    master = dict(env=ENV, paliers={})
    with open(f"{OUTDIR}/env.json", "w") as f: json.dump(ENV, f, indent=2)   # precaution #3
    for N in PALIERS:
        res = run_palier(N)
        master['paliers'][str(N)] = res
        # SAUVEGARDE INTERMEDIAIRE apres chaque palier (precaution #2)
        with open(f"{OUTDIR}/palier_{N}.json", "w") as f: json.dump(res, f, indent=2)
        with open(f"{OUTDIR}/master.json", "w") as f: json.dump(master, f, indent=2)
        print(f"  -> sauve {OUTDIR}/palier_{N}.json", flush=True)
    # ---- EXTRAPOLATION asymptotique (fits vs N) ----
    extrap = {}
    Ns = [int(k) for k in master['paliers']]
    def series(key):
        xs, ys = [], []
        for N in Ns:
            a = master['paliers'][str(N)]['palier']
            if f"{key}_mean" in a: xs.append(N); ys.append(a[f"{key}_mean"])
        return np.array(xs, float), np.array(ys, float)
    for key, target in [('dw', 2.0), ('ds', 3.0), ('df', 3.0)]:
        xs, ys = series(key)
        if len(xs) >= 3:
            # fit y = y_inf + c * N^{-b}  (extrapolation grossiere par log-log du residu)
            slope = float(np.polyfit(np.log(xs), ys, 1)[1])   # tendance simple
            extrap[key] = dict(values=list(zip(xs.tolist(), ys.tolist())),
                               last=float(ys[-1]), target=target,
                               trend_per_decade=float(np.polyfit(np.log10(xs), ys, 1)[0]))
    # gap Ollivier mesoscopique : tendance du |gap| avec delta et N (test gravite)
    xs, _ = series('ollivier_meso_gap_d2')
    if len(xs):
        extrap['ollivier_meso_gap_d2'] = [(int(N), master['paliers'][str(N)]['palier'].get('ollivier_meso_gap_d2_mean'))
                                          for N in Ns]
    master['extrapolation'] = extrap
    with open(f"{OUTDIR}/master.json", "w") as f: json.dump(master, f, indent=2)
    print("\n===== EXTRAPOLATION =====")
    print(json.dumps(extrap, indent=2))
    print(f"\nTerminé. JSONs dans {OUTDIR}/ (master.json + palier_*.json + env.json)")
    return master

if __name__ == "__main__":
    main()
