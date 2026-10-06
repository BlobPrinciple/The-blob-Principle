#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
BLOB — MOTEUR CANONIQUE + MESURES + TEMOINS + TESTS   (un seul fichier)
================================================================================
Objectif : un moteur propre, net, SANS AMBIGUITE, qui tourne a l'identique
  - sur Colab (numba present)  -> rapide, jusqu'a N ~ 10^6
  - en local  (numba absent)   -> pur-Python, N <= ~2000 pour les tests
Le MEME code dans les deux cas (numba optionnel ci-dessous).

DEFINITION DU MODELE (geometrique + viabilite) :
  N points uniformes dans le cube unite ; graphe de Rips au rayon r fixant le
  degre moyen a kappa ; MCMC de Metropolis maximisant
        S = log(1 + n_tri) - beta * CV(degres)
  par recablage d'aretes dans un voisinage geometrique (pool de Rips elargi).

PARAMETRES CANONIQUES (geles, = corpus) :
  kappa = 6.6 ; beta = 0.30 ; tau = 0.50 ; pool_fac = 1.6 ; therm_fac = 120
  ACCEPTATION : tau_eff = tau / N   (sensibilite O(1) par coup, independante de N).
  /!\\ C'est ce facteur 1/N qui fait grimper le systeme vers le point de travail ;
      un tau brut (sans /N) est ~N fois trop chaud et fait s'effondrer n_tri.

POINT DE TRAVAIL ATTENDU (= corpus, multi-graines) :
  n_tri/N       ~ 5.4     (densite de liaison tri/arete = 4.88)
  CV(degres)    ~ 0.87
  calcif/sommet ~ 16.1    (= 3 * n_tri/N ; nombre de triangles incidents/sommet)
  Gini(MASSE)   ~ 0.854   (Gini de la distribution triangles/sommet)
  Gini(degres)  ~ 0.38    (AUTRE quantite ; ne pas confondre avec Gini-masse)

SIGNATURES vs TEMOINS (RGG = Poisson+Rips sans viabilite ; ER = Erdos-Renyi),
au point de travail :
  CV, n_tri, Gini_masse : tres au-dessus du RGG
  b1 (1er nombre de Betti simplicial) : SUPPRIME (~x2.6 vs ER)
  courbure d'Ollivier : concentration matiere > RGG (de type gravitationnel)
  clustering : LEGEREMENT SOUS le RGG
================================================================================
"""
import math
import time
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import linprog

# ---- numba optionnel : meme code avec ou sans ----
try:
    from numba import njit
    HAVE_NUMBA = True
except Exception:                       # pas de numba -> decorateur neutre
    HAVE_NUMBA = False
    def njit(*args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return args[0]
        def deco(f):
            return f
        return deco

# ============================ PARAMETRES CANONIQUES ===========================
KAPPA      = 6.6
BETA       = 0.30
TAU        = 0.50
POOL_FAC   = 1.6
THERM_FAC  = 120     # nb total de pas MCMC = THERM_FAC * N
N_CHUNKS   = 8       # decoupage de la thermalisation
CAP        = 96      # capacite max de voisins (degre plafonne)
# ==============================================================================


# ------------------------------- GRAPHE (numba) -------------------------------
@njit(cache=True)
def _build_nbr(eu, ev, N, cap):
    deg = np.zeros(N, np.int64)
    nbr = -np.ones((N, cap), np.int64)
    for k in range(eu.shape[0]):
        u = eu[k]; v = ev[k]
        if deg[u] < cap:
            nbr[u, deg[u]] = v; deg[u] += 1
        if deg[v] < cap:
            nbr[v, deg[v]] = u; deg[v] += 1
    return nbr, deg


@njit(cache=True)
def _has(nbr, deg, a, b):
    for k in range(deg[a]):
        if nbr[a, k] == b:
            return True
    return False


@njit(cache=True)
def _common(nbr, deg, u, v):
    c = 0
    for k in range(deg[u]):
        x = nbr[u, k]
        for m in range(deg[v]):
            if nbr[v, m] == x:
                c += 1; break
    return c


@njit(cache=True)
def _rm(nbr, deg, u, v):
    du = deg[u]
    for k in range(du):
        if nbr[u, k] == v:
            nbr[u, k] = nbr[u, du - 1]; nbr[u, du - 1] = -1; deg[u] = du - 1
            return


@njit(cache=True)
def _add(nbr, deg, a, b, cap):
    if deg[a] < cap:
        nbr[a, deg[a]] = b; deg[a] += 1
    if deg[b] < cap:
        nbr[b, deg[b]] = a; deg[b] += 1


@njit(cache=True)
def _n_tri(nbr, deg, N):
    tot = 0
    for u in range(N):
        for i in range(deg[u]):
            a = nbr[u, i]
            if a <= u:
                continue
            for j in range(i + 1, deg[u]):
                b = nbr[u, j]
                if b <= u:
                    continue
                for m in range(deg[a]):
                    if nbr[a, m] == b:
                        tot += 1; break
    return tot


@njit(cache=True)
def _tpv(nbr, deg, N):
    """Triangles incidents par sommet = 'masse' / calcification (corpus)."""
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
def _mcmc(nbr, deg, eu, ev, pa, pb, beta, tau_eff, mean, nt0, nsteps, cap, seed):
    """Un bloc de nsteps de Metropolis sur S = log(1+n_tri) - beta*CV. En place."""
    np.random.seed(seed)
    N = deg.shape[0]; E = eu.shape[0]; P = pa.shape[0]; nt = nt0
    sumsq = 0.0
    for i in range(N):
        sumsq += deg[i] * deg[i]
    cv = math.sqrt(max(sumsq / N - mean * mean, 0.0)) / mean
    S = math.log(1.0 + nt) - beta * cv
    for _ in range(nsteps):
        io = np.random.randint(0, E); u = eu[io]; v = ev[io]
        if deg[u] <= 2 or deg[v] <= 2:           # garde-fou de connectivite
            continue
        a = -1; b = -1; ok = False
        for _t in range(40):                     # une non-arete candidate du pool
            pi = np.random.randint(0, P); ca = pa[pi]; cb = pb[pi]
            if ca == u or ca == v or cb == u or cb == v:
                continue
            if deg[ca] >= cap or deg[cb] >= cap:
                continue
            if not _has(nbr, deg, ca, cb):
                a = ca; b = cb; ok = True; break
        if not ok:
            continue
        tl = _common(nbr, deg, u, v)             # triangles perdus / gagnes
        tg = _common(nbr, deg, a, b)
        nt2 = nt - tl + tg
        du = deg[u]; dv = deg[v]; da = deg[a]; db = deg[b]
        nss = sumsq + (-2*du + 1) + (-2*dv + 1) + (2*da + 1) + (2*db + 1)
        cv2 = math.sqrt(max(nss / N - mean * mean, 0.0)) / mean
        S2 = math.log(1.0 + nt2) - beta * cv2
        if (S2 - S) >= 0.0 or np.random.random() < math.exp((S2 - S) / tau_eff):
            _rm(nbr, deg, u, v); _rm(nbr, deg, v, u); _add(nbr, deg, a, b, cap)
            nt = nt2; sumsq = nss; S = S2; eu[io] = a; ev[io] = b
    return nt


# ------------------------------- GENERATEURS ----------------------------------
def _rips(N, seed, kappa, pf):
    """Points de Poisson + graphe de Rips ; renvoie pts, aretes initiales, pool."""
    rng = np.random.default_rng(seed)
    pts = rng.random((N, 3))
    r = (kappa / ((N - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    tree = cKDTree(pts)
    pool = tree.query_pairs(pf * r, output_type='ndarray').astype(np.int64)
    dd = np.linalg.norm(pts[pool[:, 0]] - pts[pool[:, 1]], axis=1)
    pool = pool[np.argsort(dd)]                  # plus courtes d'abord
    E0 = min(int(round(N * kappa / 2)), len(pool))
    return pts, pool[:E0].copy(), pool


def build_blob(N, seed=0, kappa=KAPPA, pf=POOL_FAC, therm_fac=THERM_FAC):
    """Le Blob : Rips + MCMC de viabilite (tau_eff = TAU/N)."""
    pts, edges, pool = _rips(N, seed, kappa, pf)
    nbr, deg = _build_nbr(edges[:, 0].copy(), edges[:, 1].copy(), N, CAP)
    eu = edges[:, 0].copy(); ev = edges[:, 1].copy()
    pa = pool[:, 0].copy();  pb = pool[:, 1].copy()
    mean = 2.0 * len(edges) / N
    steps = therm_fac * N; chunk = max(steps // N_CHUNKS, 1)
    nt = _n_tri(nbr, deg, N)
    for c in range(N_CHUNKS):
        nt = _mcmc(nbr, deg, eu, ev, pa, pb, BETA, TAU / N, mean,
                   nt, chunk, CAP, seed * 100 + 1 + c)
    return pts, nbr, deg


def build_rgg(N, seed=0, kappa=KAPPA, pf=POOL_FAC):
    """Temoin RGG : Poisson + Rips SANS viabilite (meme nb d'aretes)."""
    pts, edges, _ = _rips(N, seed, kappa, pf)
    nbr, deg = _build_nbr(edges[:, 0].copy(), edges[:, 1].copy(), N, CAP)
    return pts, nbr, deg


def build_er(N, seed=0, kappa=KAPPA):
    """Temoin Erdos-Renyi : aretes aleatoires, meme nombre d'aretes."""
    rng = np.random.default_rng(70_000 + seed)
    E = int(round(N * kappa / 2))
    eu = rng.integers(0, N, size=3 * E); ev = rng.integers(0, N, size=3 * E)
    m = eu != ev; eu = eu[m][:E]; ev = ev[m][:E]
    nbr, deg = _build_nbr(eu.astype(np.int64), ev.astype(np.int64), N, CAP)
    return None, nbr, deg


# --------------------------------- MESURES ------------------------------------
def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if n == 0 or x.sum() == 0:
        return 0.0
    c = np.arange(1, n + 1)
    return (2 * np.sum(c * x) / (n * x.sum())) - (n + 1) / n


def measure(nbr, deg, N):
    """Invariants locaux : point de travail + clustering + les DEUX Gini."""
    nt = _n_tri(nbr, deg, N)
    degf = deg.astype(float)
    tpv = _tpv(nbr, deg, N).astype(float)        # masse = triangles/sommet
    p2 = np.sum(degf * (degf - 1) / 2)
    return dict(
        n_tri_par_N   = nt / N,
        CV            = degf.std() / degf.mean(),
        Gini_deg      = gini(degf),              # ~0.38
        Gini_masse    = gini(tpv),               # ~0.854 (quantite du corpus)
        calcif_sommet = float(tpv.mean()),       # = 3*n_tri/N ~16
        clustering    = 3 * nt / p2 if p2 > 0 else 0.0,
    )


def _edges(nbr, deg, N):
    I = []; J = []
    for u in range(N):
        for k in range(deg[u]):
            v = int(nbr[u, k])
            if v > u:
                I.append(u); J.append(v)
    return np.array(I, np.int64), np.array(J, np.int64)


def betti1(nbr, deg, N):
    """b1 simplicial = E - V + (composantes) - rang(d2) sur GF(2), exact."""
    eid = {}; idx = 0
    for u in range(N):
        for k in range(deg[u]):
            v = int(nbr[u, k])
            if v > u:
                eid[(u, v)] = idx; idx += 1
    def E(x, y):
        return eid[(x, y)] if x < y else eid[(y, x)]
    piv = {}; rank = 0
    for u in range(N):
        nu = [int(nbr[u, k]) for k in range(deg[u]) if nbr[u, k] > u]
        ns = set(nu)
        for i in range(len(nu)):
            a = nu[i]
            for j in range(i + 1, len(nu)):
                b = nu[j]
                if b in ns and any(int(nbr[a, m]) == b for m in range(deg[a])):
                    row = (1 << E(u, a)) | (1 << E(u, b)) | (1 << E(a, b))
                    while row:
                        lb = row & (-row)
                        if lb in piv:
                            row ^= piv[lb]
                        else:
                            piv[lb] = row; rank += 1; break
    # composantes connexes
    comp = 0; seen = np.zeros(N, bool)
    for s in range(N):
        if seen[s]:
            continue
        comp += 1; stack = [s]; seen[s] = True
        while stack:
            x = stack.pop()
            for k in range(deg[x]):
                y = int(nbr[x, k])
                if not seen[y]:
                    seen[y] = True; stack.append(y)
    return idx - N + comp - rank


def ollivier_conc(pts, nbr, deg, N, nsamp=120, seed=0, alpha=0.5):
    """Concentration de courbure d'Ollivier : kappa(aretes riches) - kappa(pauvres)."""
    rng = np.random.default_rng(seed)
    I, J = _edges(nbr, deg, N)
    if len(I) == 0:
        return np.nan
    idx = rng.choice(len(I), size=min(nsamp, len(I)), replace=False)
    kap = []; tri = []
    for e in idx:
        u, v = int(I[e]), int(J[e])
        nu = [int(nbr[u, k]) for k in range(deg[u])]
        nv = [int(nbr[v, k]) for k in range(deg[v])]
        if not nu or not nv:
            continue
        su = [u] + nu; pu = np.array([alpha] + [(1 - alpha) / len(nu)] * len(nu))
        sv = [v] + nv; pv = np.array([alpha] + [(1 - alpha) / len(nv)] * len(nv))
        C = np.zeros((len(su), len(sv)))
        for ai, a in enumerate(su):
            adj = set(int(nbr[a, k]) for k in range(deg[a])) | {a}
            for bi, b in enumerate(sv):
                C[ai, bi] = 0.0 if a == b else (1.0 if b in adj else 2.0)
        nA, nB = len(su), len(sv); Aeq = np.zeros((nA + nB, nA * nB))
        for ai in range(nA):
            Aeq[ai, ai * nB:(ai + 1) * nB] = 1
        for bi in range(nB):
            Aeq[nA + bi, bi::nB] = 1
        res = linprog(C.ravel(), A_eq=Aeq, b_eq=np.concatenate([pu, pv]),
                      bounds=[(0, None)] * (nA * nB), method='highs')
        if not res.success:
            continue
        nvset = set(nv); cnt = sum(1 for x in nu if x in nvset)
        kap.append(1 - res.fun); tri.append(cnt)
    kap = np.array(kap); tri = np.array(tri)
    if len(kap) < 10:
        return np.nan
    med = np.median(tri)
    return kap[tri > med].mean() - kap[tri <= med].mean()


# ---------------------------------- TESTS -------------------------------------
def _sig(a, b):
    a = np.array(a, float); b = np.array(b, float)
    sd = math.sqrt(a.std() ** 2 + b.std() ** 2)
    return abs(a.mean() - b.mean()) / sd if sd > 1e-12 else float('inf')


def run_tests(N=1200, seeds=(0, 1, 2), heavy=True, verbose=True):
    """Mesure Blob/RGG/ER multi-graines, puis verifie point de travail + signatures.
    Renvoie (n_pass, n_total). Affiche un tableau et une liste [PASS]/[FAIL]."""
    t0 = time.time()
    B = {k: [] for k in ('n_tri_par_N', 'CV', 'Gini_deg', 'Gini_masse',
                          'calcif_sommet', 'clustering')}
    R = {k: [] for k in B}
    blob_pts = {}; blob_g = {}
    for s in seeds:
        pts, nbr, deg = build_blob(N, s)
        m = measure(nbr, deg, N)
        for k in B:
            B[k].append(m[k])
        blob_pts[s] = pts; blob_g[s] = (nbr, deg)
        _, nbrR, degR = build_rgg(N, s)
        mr = measure(nbrR, degR, N)
        for k in R:
            R[k].append(mr[k])

    b1_blob = b1_er = None; oll_blob = oll_rgg = None
    if heavy:
        s = seeds[0]
        nbr, deg = blob_g[s]
        b1_blob = betti1(nbr, deg, N)
        _, nbrE, degE = build_er(N, s)
        b1_er = betti1(nbrE, degE, N)
        oll_blob = ollivier_conc(blob_pts[s], nbr, deg, N, seed=s)
        ptsR, nbrR, degR = build_rgg(N, s)
        oll_rgg = ollivier_conc(ptsR, nbrR, degR, N, seed=s)

    def mean(d, k):
        return float(np.mean(d[k]))

    if verbose:
        print("=" * 78)
        print(f"BLOB — TESTS CANONIQUES   (N={N}, graines={seeds}, "
              f"numba={'oui' if HAVE_NUMBA else 'non'})")
        print("=" * 78)
        print(f"{'quantite':<16}{'Blob':>10}{'RGG':>10}{'ER':>10}")
        for k, lab in [('n_tri_par_N', 'n_tri/N'), ('CV', 'CV(deg)'),
                       ('Gini_deg', 'Gini_deg'), ('Gini_masse', 'Gini_masse'),
                       ('calcif_sommet', 'calcif/somm'), ('clustering', 'clustering')]:
            print(f"{lab:<16}{mean(B, k):>10.3f}{mean(R, k):>10.3f}{'-':>10}")
        if heavy:
            print(f"{'b1 (Betti1)':<16}{b1_blob:>10.0f}{'-':>10}{b1_er:>10.0f}")
            print(f"{'Ollivier conc':<16}{oll_blob:>10.3f}{oll_rgg:>10.3f}{'-':>10}")
        print("-" * 78)

    checks = []
    # --- point de travail (= corpus) ---
    checks.append(("n_tri/N ~ 5.4",      4.5 <= mean(B, 'n_tri_par_N') <= 6.3,
                   f"{mean(B,'n_tri_par_N'):.2f}"))
    checks.append(("CV(deg) ~ 0.87",     0.78 <= mean(B, 'CV') <= 1.05,
                   f"{mean(B,'CV'):.3f}"))
    checks.append(("calcif/somm ~ 16.1", 13.5 <= mean(B, 'calcif_sommet') <= 18.5,
                   f"{mean(B,'calcif_sommet'):.2f}"))
    checks.append(("Gini_masse ~ 0.854", 0.83 <= mean(B, 'Gini_masse') <= 0.90,
                   f"{mean(B,'Gini_masse'):.3f}"))
    checks.append(("Gini_deg ~ 0.38",    0.30 <= mean(B, 'Gini_deg') <= 0.45,
                   f"{mean(B,'Gini_deg'):.3f}"))
    # --- signatures vs temoins ---
    checks.append(("CV >> RGG",          mean(B, 'CV') > 1.4 * mean(R, 'CV'),
                   f"{mean(B,'CV'):.3f} vs {mean(R,'CV'):.3f}  ({_sig(B['CV'],R['CV']):.0f}σ)"))
    checks.append(("n_tri > RGG",        mean(B, 'n_tri_par_N') > mean(R, 'n_tri_par_N'),
                   f"{mean(B,'n_tri_par_N'):.2f} vs {mean(R,'n_tri_par_N'):.2f}"))
    checks.append(("Gini_masse >> RGG",  mean(B, 'Gini_masse') > 1.3 * mean(R, 'Gini_masse'),
                   f"{mean(B,'Gini_masse'):.3f} vs {mean(R,'Gini_masse'):.3f}"))
    checks.append(("clustering < RGG",   mean(B, 'clustering') < mean(R, 'clustering'),
                   f"{mean(B,'clustering'):.3f} vs {mean(R,'clustering'):.3f}"))
    if heavy:
        ratio = (b1_er / b1_blob) if b1_blob else 0.0
        checks.append(("b1 supprime vs ER (x>1.5)", ratio > 1.5,
                       f"ER/Blob = {ratio:.1f}  (b1: {b1_blob:.0f} vs {b1_er:.0f})"))
        checks.append(("Ollivier > RGG (gravite)", (oll_blob is not None and
                       oll_rgg is not None and oll_blob > oll_rgg),
                       f"{oll_blob:.3f} vs {oll_rgg:.3f}"))

    n_pass = 0
    if verbose:
        print("RESULTATS :")
    for name, ok, val in checks:
        n_pass += int(bool(ok))
        if verbose:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name:<28} {val}")
    if verbose:
        print("-" * 78)
        print(f"  {n_pass}/{len(checks)} tests passes   [duree {time.time()-t0:.0f}s]")
        print("=" * 78)
    return n_pass, len(checks)


if __name__ == "__main__":
    # local (sans numba) : N modeste. Sur Colab (numba) : monter N et les graines.
    run_tests(N=1200, seeds=(0, 1, 2), heavy=True)
