#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — LIMITE CONTINUE, VOLET DIMENSIONS (d_s, d_H) — GRAND N (Colab)
# Protocole pré-enregistré. Version 1.0 — 14 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# CONTEXTE : l'instrument a été VALIDÉ au container le 14/07 sur étalons exacts
# (calibration sur vérités connues, JAMAIS sur le Blob) :
#   d_s : cube 3D exact 3,036 ✓ · carré 2D exact 2,013 ✓ (anti-réglage) ·
#         pipeline sparse ≡ Fourier ±0,000 ✓ · RGG nu N=1e5 → 2,935 ✓
#   d_H : cube 3,065 ✓ · carré 2,017 ✓ · RGG nu → 3,053 ✓
# FENÊTRES GELÉES (aucun curseur ne bouge ici) :
#   d_s : fit log-log de p(t)−π sur {t ≥ 20  ET  p−π ≥ 50/N}, ≥ 8 points requis.
#   d_H : fit décalé log B vs log(r+a), a∈[0;2], fenêtre r∈[2, r*], B(r*) ≤ N/4,
#         ≥ 4 points requis.
# CE SCRIPT MESURE : d_s et d_H du BLOB ÉQUILIBRÉ (action complète
# S = log(1+T) − β·CV, |E| = 5N conservé) CONTRE le contrôle DILUÉ (même
# géométrie, mêmes E = 5N arêtes, non équilibré), à N grand.
# Il traite le volet DIMENSIONS de la limite continue ; le volet régularité
# métrique/courbure est distinct (run gravité grand-N séparé).
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback
import scipy.sparse as sp
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from collections import deque

# ───────────────────────── PARAMÈTRES ─────────────────────────
N          = 300_000          # taille (300k conseillé ; 150k minimum pour la fenêtre d_s)
SEEDS      = [21, 22, 23, 24] # graines indépendantes
DENSITY    = 200.0
KAPPA      = 10.0
RCUT       = 1.6
BETA       = 0.30
TAU        = 0.5
E_PER_N    = 5                # |E| = 5N, conservé par swap
SWEEPS_EQ  = 15               # équilibrage (3N tentatives / sweep)
NSRC       = 24               # sources pour la marche et le BFS
TMAX       = 2000             # horizon de la marche paresseuse
OUT_JSON   = "limite_continue_results.json"

# Fenêtres GELÉES de l'instrument (validées container 14/07) :
TMIN_DS    = 20
THRESH_DS  = 50.0
MINPTS_DS  = 8
BMAX_FRAC  = 4                # d_H : B(r*) ≤ N/4
MINPTS_DH  = 4

GRID = """
════════════════ GRILLE PRÉ-ENREGISTRÉE (gravée AVANT lecture) ════════════════
CONTRÔLES EMBARQUÉS (doivent passer, sinon ABORT — environnement suspect) :
  cube 3D exact (Fourier, L=50)  : d_s ∈ [2,95 ; 3,10]  (référence 3,036)
  carré 2D exact (Fourier, L=160): d_s ∈ [1,95 ; 2,08]  (référence 2,013)
PRÉDICTIONS (posées avant run) :
  P1. Blob équilibré : d_s ∈ [2,85 ; 3,15]   (corpus : 3,045 ± 0,026 à N=3000)
  P2. Blob équilibré : d_H ∈ [2,85 ; 3,15]   (corpus : d_H ≥ 3 [M])
  P3. Dilué (contrôle) : d_s et d_H ∈ [2,85 ; 3,15] (RGG 3D dilué reste 3D)
LECTURE (automatique) :
  Blob ET dilué dans les cibles → « dimensions conformes à une variété 3D »
     — le volet dimensionnel de la limite continue tient au niveau numérique
     (mesure propre, instrument validé ; PAS un [T]).
  Blob hors cible, dilué dedans → déviation SPÉCIFIQUE À LA DYNAMIQUE
     — front nouveau, à investiguer avant toute conclusion.
  Les deux hors cible → effet de taille/fenêtre → documenter, augmenter N.
  Fenêtre < points requis → verdict « insuffisant à ce N », PAS un résultat.
Tout écart à la grille se lit tel quel. Aucune réinterprétation post hoc.
════════════════════════════════════════════════════════════════════════════════
"""

TGRID = np.unique(np.round(np.logspace(0, math.log10(TMAX), 70)).astype(int))

# ─────────────── INSTRUMENT GELÉ : d_s ───────────────
def fit_ds(pminus, Ngraph):
    ok = (TGRID >= TMIN_DS) & (pminus > THRESH_DS / Ngraph)
    npts = int(ok.sum())
    if npts < MINPTS_DS:
        return float("nan"), npts, (float("nan"), float("nan"))
    x = np.log(TGRID[ok]); y = np.log(pminus[ok])
    ls = -2 * np.diff(y) / np.diff(x)
    return float(-2 * np.polyfit(x, y, 1)[0]), npts, (float(ls.min()), float(ls.max()))

def ds_walk(A, nsrc=NSRC, seed=0):
    """Marche paresseuse P' = (I + D⁻¹A)/2 ; retour aux sources − stationnaire."""
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

# ─────────────── INSTRUMENT GELÉ : d_H ───────────────
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

# ─────────────── CONTRÔLES EMBARQUÉS (exacts, Fourier) ───────────────
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
    ok = (2.95 <= ds3 <= 3.10) and (1.95 <= ds2 <= 2.08)
    if not ok:
        print("✗✗ CONTRÔLE ÉCHOUÉ — environnement suspect. ABORT (règle : le cube DOIT rendre 3).")
        sys.exit(1)
    print("✓ Contrôles embarqués passés — instrument opérationnel dans cet environnement.\n")
    return ds3, ds2

# ─────────────── GÉOMÉTRIE + ÉTAT (action complète, |E| conservé) ───────────────
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
    """Swaps Metropolis à |E| constant, action complète S = log(1+T) − β·CV,
    température effective τ/N (convention corpus : mesure ∝ exp((N/τ)·S))."""
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
    npool = len(cand)
    acc = 0
    for sw in range(sweeps):
        for _ in range(3 * N):
            io = rng.integers(E); u, v = edge_list[io]
            ii = rng.integers(npool); a, b = int(cand[ii, 0]), int(cand[ii, 1])
            if b in adj[a] or v not in adj[u]: continue
            if len({u, v, a, b}) < 4: continue          # garde : MAJ O(1) exacte de Σd²
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
        assert e_now == E, f"|E| VIOLÉ au sweep {sw}: {e_now} vs {E}"
        print(f"    sweep {sw+1}/{sweeps} : T={nt}  CV={cv(S2):.4f}  acc={acc}", flush=True)
    return adj, nt, cv(S2)

def to_giant_csr(adj):
    rows = []; cols = []
    for i in range(N):
        for j in adj[i]:
            if j > i:
                rows.append(i); cols.append(j)
    r = np.array(rows); c = np.array(cols)
    A = sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(N, N))
    A = ((A + A.T) > 0).astype(float).tocsr()
    _, lab = connected_components(A, directed=False)
    keep = np.where(lab == np.bincount(lab).argmax())[0]
    return A[keep][:, keep].tocsr(), len(keep)

# ─────────────── PIPELINE PAR GRAINE ───────────────
def run_seed(seed):
    res = {"seed": seed, "N": N}
    t1 = time.time()
    pts, cand, L = build_pool(seed)
    E0 = E_PER_N * N
    assert len(cand) > E0, "Pool insuffisant"
    res["pool"] = int(len(cand))
    rng = np.random.default_rng(seed)

    # BLOB ÉQUILIBRÉ
    init = rng.choice(len(cand), size=E0, replace=False)
    adj = adj_from_active(cand, init)
    print(f"  équilibrage (action complète, {SWEEPS_EQ} sweeps)…", flush=True)
    adj, T_eq, CV_eq = equilibrate(adj, cand, seed, SWEEPS_EQ)
    res["T_eq"] = int(T_eq); res["CV_eq"] = float(CV_eq)
    A_eq, ng_eq = to_giant_csr(adj)
    res["giant_eq"] = int(ng_eq)
    pm, Ng = ds_walk(A_eq, seed=seed)
    ds_eq, np_eq, loc_eq = fit_ds(pm, Ng)
    dh_eq, r_eq, a_eq = bfs_dH(A_eq, seed=seed)
    res["ds_eq"] = ds_eq; res["ds_eq_pts"] = np_eq; res["ds_eq_loc"] = list(loc_eq)
    res["dh_eq"] = dh_eq; res["dh_eq_rstar"] = int(r_eq); res["dh_eq_a"] = a_eq
    res["pm_eq"] = pm.tolist()

    # CONTRÔLE DILUÉ (même géométrie, mêmes E arêtes, PAS d'équilibrage)
    init_d = np.random.default_rng(seed + 77).choice(len(cand), size=E0, replace=False)
    adj_d = adj_from_active(cand, init_d)
    A_di, ng_di = to_giant_csr(adj_d)
    res["giant_dil"] = int(ng_di)
    pmd, Ngd = ds_walk(A_di, seed=seed + 1)
    ds_di, np_di, loc_di = fit_ds(pmd, Ngd)
    dh_di, r_di, a_di = bfs_dH(A_di, seed=seed + 1)
    res["ds_dil"] = ds_di; res["ds_dil_pts"] = np_di
    res["dh_dil"] = dh_di; res["dh_dil_rstar"] = int(r_di)
    res["pm_dil"] = pmd.tolist()

    res["minutes"] = (time.time() - t1) / 60.0
    return res

# ───────────────────────── MAIN ─────────────────────────
if __name__ == "__main__":
    print(GRID)
    print(f"Environnement : python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"N={N}, graines={SEEDS}, β={BETA}, τ={TAU}, |E|={E_PER_N}N (asserté), "
          f"sweeps={SWEEPS_EQ}\nInstrument gelé : t_min={TMIN_DS}, seuil={int(THRESH_DS)}/N, "
          f"≥{MINPTS_DS} pts ; d_H décalé, B≤N/{BMAX_FRAC}\n")
    embedded_controls()
    all_res = []
    t0 = time.time()
    for i, sd in enumerate(SEEDS):
        print(f"[{i+1}/{len(SEEDS)}] seed={sd}", flush=True)
        try:
            r = run_seed(sd)
            all_res.append(r)
            print(f"  → BLOB : d_s={r['ds_eq']:.3f} ({r['ds_eq_pts']} pts, loc[{r['ds_eq_loc'][0]:.2f},{r['ds_eq_loc'][1]:.2f}])  "
                  f"d_H={r['dh_eq']:.3f} (r≤{r['dh_eq_rstar']})", flush=True)
            print(f"  → DILUÉ: d_s={r['ds_dil']:.3f} ({r['ds_dil_pts']} pts)  "
                  f"d_H={r['dh_dil']:.3f} (r≤{r['dh_dil_rstar']})  [{r['minutes']:.0f} min]", flush=True)
        except Exception as ex:
            print(f"  ✗ graine {sd} échouée : {ex}", flush=True)
            traceback.print_exc()
            all_res.append({"seed": sd, "error": str(ex)})
        with open(OUT_JSON, "w") as f:
            json.dump(all_res, f)                      # sauvegarde graine par graine
    # ─── LECTURE SELON LA GRILLE (automatique) ───
    okres = [r for r in all_res if "ds_eq" in r and not math.isnan(r["ds_eq"])]
    print(f"\n════════ LECTURE (grille appliquée telle quelle, {(time.time()-t0)/60:.0f} min) ════════")
    if not okres:
        print("Aucune graine exploitable (fenêtres insuffisantes ou erreurs) → augmenter N.")
        sys.exit(0)
    dse = np.array([r["ds_eq"] for r in okres]); dhe = np.array([r["dh_eq"] for r in okres])
    dsd = np.array([r["ds_dil"] for r in okres if not math.isnan(r["ds_dil"])])
    dhd = np.array([r["dh_dil"] for r in okres if not math.isnan(r["dh_dil"])])
    print(f"BLOB  : d_s = {dse.mean():.3f} ± {dse.std():.3f}  |  d_H = {dhe.mean():.3f} ± {dhe.std():.3f}  ({len(okres)} graines)")
    if len(dsd): print(f"DILUÉ : d_s = {dsd.mean():.3f} ± {dsd.std():.3f}  |  d_H = {dhd.mean():.3f} ± {dhd.std():.3f}")
    P1 = 2.85 <= dse.mean() <= 3.15; P2 = 2.85 <= dhe.mean() <= 3.15
    P3 = (len(dsd) > 0 and 2.85 <= dsd.mean() <= 3.15) and (len(dhd) > 0 and 2.85 <= dhd.mean() <= 3.15)
    print(f"P1 (Blob d_s ∈ [2,85;3,15]) : {'✓' if P1 else '✗'}")
    print(f"P2 (Blob d_H ∈ [2,85;3,15]) : {'✓' if P2 else '✗'}")
    print(f"P3 (dilué conforme)          : {'✓' if P3 else '✗'}")
    if P1 and P2 and P3:
        print("\n⟹ DIMENSIONS CONFORMES À UNE VARIÉTÉ 3D (Blob équilibré ET contrôle).")
        print("  Le volet dimensionnel de la limite continue tient au niveau numérique,")
        print("  avec un instrument validé sur étalons. Ce n'est PAS un [T] ; c'est une")
        print("  mesure propre. Volet suivant : régularité métrique/courbure (run gravité).")
    elif P3 and not (P1 and P2):
        print("\n⟹ DÉVIATION SPÉCIFIQUE À LA DYNAMIQUE (dilué conforme, Blob non).")
        print("  Front nouveau — ne pas conclure, investiguer (échelles, τ, sweeps).")
    else:
        print("\n⟹ Effet de taille/fenêtre probable (contrôle dilué lui-même hors cible)")
        print("  → augmenter N avant toute lecture sur le Blob.")
