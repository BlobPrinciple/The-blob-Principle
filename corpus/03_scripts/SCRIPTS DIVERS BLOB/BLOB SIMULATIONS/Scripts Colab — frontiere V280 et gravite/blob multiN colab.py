#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — MULTI-N : CONVERGENCE EN TAILLE DU VOLET COURBURE + CASE B + SUP-1
# Protocole pré-enregistré. Version 1.0 — 14 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# QUATRE FRONTS SERVIS PAR CE RUN :
#  (R8)   Le tribunal a nommé le trou : toute la gravité vit à N=2000, une seule
#         taille. Ici : N ∈ {1000, 2000, 4000}, 10 graines par taille.
#  (B)    Case B du sudoku : le Blob équilibré n'est pas localement une
#         triangulation de variété (m médian 46 vs ~5). L'observable décisive
#         f_nv(N) — la fraction non-variété — se dilue-t-elle avec N ?
#  (SUP-1) d_w et gaussianité du noyau sur le graphe de GIBBS (équilibré) —
#         INDICATIF à ces tailles (fenêtre courte) ; le verrouillage grand N
#         = patch MSD (3 lignes) du script limite continue, run séparé.
#  (v2)   Le ×4,7 (Var_eq/Var_neutre) : invariant thermodynamique ou artefact
#         de taille ?
# PÉRIMÈTRE DÉCLARÉ : pas d'injection ici (la localisation multi-N = phase 2).
# Blocs géométrie/état/équilibrage : repris du pipeline validé (T/CV reproduits
# bit-à-bit au container le 14/07), paramétrés en N.
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback
from collections import defaultdict
from itertools import combinations
import scipy.sparse as sp

# ───────────────────────── PARAMÈTRES ─────────────────────────
SIZES        = [1000, 2000, 4000]
SEEDS_PER_N  = 10
SEED_BASE    = {1000: 4100, 2000: 4200, 4000: 4300}   # banques distinctes, fraîches
DENSITY      = 200.0
KAPPA        = 10.0
RCUT         = 1.6
BETA         = 0.30
TAU          = 0.5
E_PER_N      = 5
SWEEPS_EQ    = 30
EDGE_SAMPLE  = 3000        # pour la mesure A
NV_THRESH    = 10          # seuil non-variété : m > 10 (une variété 3D a m ≈ 5)
K_WALK       = 4000        # marcheurs pour d_w / gaussianité
T_WALK       = 1500
OUT_JSON     = "multiN_results.json"

GRID = """
════════════════ GRILLES PRÉ-ENREGISTRÉES (gravées AVANT lecture) ════════════════
G1 (R8 — fait A en taille) : r_eq(N) et r_rand(N) par taille.
    ROBUSTE si |r_eq(4000) − r_eq(1000)| ≤ 0,05 ET r_rand ∈ [−0,2 ; 0,2] partout.
    Dérive > 0,10 → à lire tel quel (dépendance de taille réelle).
G2 (×4,7) : ratio(N) = Var_eq/Var_neutre par taille.
    INVARIANT THERMODYNAMIQUE si max/min ≤ 1,30 sur les trois tailles.
    Sinon : dépendance de taille, la cible du modèle v2 change de nature.
G3 (CASE B — LA grille décisive) : f_nv(N) = #{arêtes actives : m > 10}/E  et
    part_m(N) = Σm(m>10)/Σm(m≥2) [proxy exact de la part de courbure, identité
    de Regge], contrôle part_δ sur échantillon.
    → f_nv(4000)/f_nv(1000) < 0,80  : les défauts SE DILUENT — limite = variété
      à défauts localisés (le pilier passe ; Dodziuk-Patodi s'active).
    → ratio ∈ [0,80 ; 1,25]         : densité FINIE de défauts — objet mixte.
    → ratio > 1,25                  : les condensats DOMINENT la limite.
    Chaque issue se lit telle quelle. Aucune n'est « mauvaise » a priori.
G4 (SUP-1 sur Gibbs — INDICATIF) : d_w équilibré sur fenêtre t ∈ [20, t*],
    t* = max t tel que MSD < (L/2)² ; ≥ 8 points sinon « insuffisant à ce N ».
    Gaussianité (grille multiplicité V2) si t* ≥ 300, sinon non jugée.
    d_w_UV (t ∈ [3,10]) rapporté : le piégeage des condensats doit s'y voir.
Tout écart aux grilles se lit tel quel. Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────── GÉOMÉTRIE (pipeline validé, paramétrée) ─────────────────
def build_geometry(N, seed):
    rng = np.random.default_rng(seed)
    L = (N / DENSITY) ** (1/3)
    pts = rng.uniform(0, L, size=(N, 3))
    r_base = (3 * KAPPA / (4 * math.pi * DENSITY)) ** (1/3)
    rc = RCUT * r_base
    cell = rc; ncell = max(1, int(L / cell))
    grid = defaultdict(list)
    for i, p in enumerate(pts):
        grid[tuple((p // cell).astype(int) % ncell)].append(i)
    cand = []
    for i, p in enumerate(pts):
        ci = (p // cell).astype(int)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in grid[tuple((ci + [dx, dy, dz]) % ncell)]:
                        if j > i:
                            d = pts[i] - pts[j]; d -= L * np.round(d / L)
                            if (d * d).sum() < rc * rc:
                                cand.append((i, j))
    return pts, sorted(set(cand)), L, rc

class BlobState:
    def __init__(self, N, cand, active_idx):
        self.N = N; self.cand = cand
        self.adj = defaultdict(set)
        for k in active_idx:
            a, b = cand[k]; self.adj[a].add(b); self.adj[b].add(a)
        self.E = len(active_idx)
        self.deg = np.zeros(N, dtype=np.int64)
        for k in active_idx:
            a, b = cand[k]; self.deg[a] += 1; self.deg[b] += 1
        self.sum_d2 = int((self.deg.astype(np.int64) ** 2).sum())
        self.T = self._count_T()
    def _count_T(self):
        t = 0
        for u in self.adj:
            for v in self.adj[u]:
                if v > u: t += len(self.adj[u] & self.adj[v])
        return t // 3
    def cv(self):
        mu = 2.0 * self.E / self.N
        var = self.sum_d2 / self.N - mu * mu
        return math.sqrt(max(var, 0.0)) / mu
    def dS_swap(self, u, v, a, b):
        t_rm = len(self.adj[u] & self.adj[v])
        self.adj[u].discard(v); self.adj[v].discard(u)
        t_add = len(self.adj[a] & self.adj[b])
        self.adj[u].add(v); self.adj[v].add(u)
        dT = t_add - t_rm
        d_logT = math.log(1 + self.T + dT) - math.log(1 + self.T)
        d2_new = self.sum_d2 \
            + (-2 * self.deg[u] + 1) + (-2 * self.deg[v] + 1) \
            + ( 2 * self.deg[a] + 1) + ( 2 * self.deg[b] + 1)
        mu = 2.0 * self.E / self.N
        cv_new = math.sqrt(max(d2_new / self.N - mu * mu, 0.0)) / mu
        dCV = cv_new - self.cv()
        return (d_logT - BETA * dCV), dT, d2_new
    def do_swap(self, u, v, a, b, dT, d2_new):
        self.adj[u].discard(v); self.adj[v].discard(u)
        self.adj[a].add(b); self.adj[b].add(a)
        self.deg[u] -= 1; self.deg[v] -= 1; self.deg[a] += 1; self.deg[b] += 1
        self.sum_d2 = d2_new; self.T += dT
    def assert_E(self, tag):
        e_now = sum(len(s) for s in self.adj.values()) // 2
        assert e_now == self.E == E_PER_N * self.N, f"|E| VIOLÉ [{tag}]"

def equilibrate(state, cand, rng, sweeps):
    te = TAU / state.N
    edge_list = [(i, j) for i in range(state.N) for j in state.adj[i] if j > i]
    for sw in range(sweeps):
        for _ in range(3 * state.N):
            io = rng.integers(len(edge_list)); u, v = edge_list[io]
            ii = rng.integers(len(cand)); a, b = cand[ii]
            if b in state.adj[a] or v not in state.adj[u]: continue
            if len({u, v, a, b}) < 4: continue
            if state.deg[u] <= 2 or state.deg[v] <= 2: continue
            dS, dT, d2n = state.dS_swap(u, v, a, b)
            if dS >= 0 or rng.random() < math.exp(dS / te):
                state.do_swap(u, v, a, b, dT, d2n)
                edge_list[io] = (a, b)
        state.assert_E(f"eq_{sw}")
    return state

# ─────────────── COURBURE DE REGGE ───────────────
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

def tets_pack(state):
    tris = set()
    for u in state.adj:
        for v in state.adj[u]:
            if v > u:
                for w in state.adj[u] & state.adj[v]:
                    if w > v: tris.add((u, v, w))
    tets = []
    for (u, v, w) in tris:
        for x in state.adj[u] & state.adj[v] & state.adj[w]:
            if x > w: tets.append((u, v, w, x))
    e2t = defaultdict(list)
    for t in tets:
        for e in combinations(t, 2):
            e2t[tuple(sorted(e))].append(t)
    return e2t

def measure_A(state, e2t, pts, L, rng):
    edges = [e for e, ts in e2t.items() if len(ts) >= 2]
    if len(edges) > EDGE_SAMPLE:
        idx = rng.choice(len(edges), size=EDGE_SAMPLE, replace=False)
        edges = [edges[i] for i in idx]
    xs = []; ys = []
    for e in edges:
        ts = e2t[e]
        d = 2 * math.pi - sum(dihedral(pts, L, t, e) for t in ts)
        xs.append(float(state.deg[e[0]] + state.deg[e[1]])); ys.append(abs(d))
    if len(xs) < 30 or np.std(xs) == 0: return float("nan"), len(xs)
    return float(np.corrcoef(xs, ys)[0, 1]), len(xs)

def measure_fnv(state, e2t, pts, L, rng):
    """Case B : fraction non-variété et part de masse (m et δ-échantillon)."""
    ms = np.array([len(ts) for ts in e2t.values()])
    ms = ms[ms >= 2]
    E = E_PER_N * state.N
    f_nv = float((ms > NV_THRESH).sum()) / E
    part_m = float(ms[ms > NV_THRESH].sum()) / max(float(ms.sum()), 1.0)
    # contrôle part_δ sur échantillon
    edges = [e for e, ts in e2t.items() if len(ts) >= 2]
    if len(edges) > 4000:
        idx = rng.choice(len(edges), size=4000, replace=False)
        edges = [edges[i] for i in idx]
    s_hi = 0.0; s_all = 0.0
    for e in edges:
        ts = e2t[e]
        d = abs(2 * math.pi - sum(dihedral(pts, L, t, e) for t in ts))
        s_all += d
        if len(ts) > NV_THRESH: s_hi += d
    part_d = s_hi / max(s_all, 1e-12)
    return f_nv, part_m, part_d, float(np.median(ms)) if len(ms) else float("nan")

def adj_to_csr(state):
    rows = []; cols = []
    for u in state.adj:
        for v in state.adj[u]:
            rows.append(u); cols.append(v)
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(state.N, state.N))
    return ((A + A.T) > 0).astype(float).tocsr()

def walk_gibbs(state, pts, L, seed):
    """d_w + gaussianité sur le graphe ÉQUILIBRÉ (fenêtre bornée par le tore)."""
    A = adj_to_csr(state)
    ip, ix = A.indptr, A.indices
    r2 = np.random.default_rng(seed)
    u = r2.choice(state.N, size=K_WALK)
    X = np.zeros((K_WALK, 3))
    deg = (ip[1:] - ip[:-1])
    tg = np.unique(np.round(np.logspace(0, math.log10(T_WALK), 40)).astype(int))
    msd = np.zeros(len(tg)); tj = 0
    snaps = {}
    for t in range(1, T_WALK + 1):
        r = (r2.random(K_WALK) * deg[u]).astype(np.int64)
        v = ix[ip[u] + r]
        dl = pts[v] - pts[u]; dl -= L * np.round(dl / L)
        X += dl; u = v
        if tj < len(tg) and t == tg[tj]:
            msd[tj] = float((X ** 2).sum(1).mean()); tj += 1
        if t in (300, 800, 1500): snaps[t] = X.copy()
    # fenêtre : t* = dernier t avec MSD < (L/2)²
    cap = (L / 2) ** 2
    ok = (tg >= 20) & (msd < cap)
    npts = int(ok.sum())
    if npts >= 8:
        sl = float(np.polyfit(np.log(tg[ok]), np.log(msd[ok]), 1)[0])
        dw = 2.0 / sl
    else:
        dw = float("nan")
    ok_uv = (tg >= 3) & (tg <= 10)
    sl_uv = float(np.polyfit(np.log(tg[ok_uv]), np.log(msd[ok_uv]), 1)[0])
    dw_uv = 2.0 / sl_uv
    tstar = int(tg[ok][-1]) if npts else 0
    # gaussianité (grille V2 multiplicité) seulement si t* ≥ 300
    gauss = None
    if tstar >= 300:
        SEk = math.sqrt(24.0 / K_WALK)
        ks = []; Qs = []
        for t, Xs in snaps.items():
            if t > tstar: continue
            for c in range(3):
                x = Xs[:, c]; s = x.std()
                ks.append(float(((x - x.mean()) ** 4).mean() / s ** 4))
                Qs.append(float((np.abs(x - x.mean()) > 3 * s).mean() / 0.0027))
        ks = np.array(ks); Qs = np.array(Qs)
        gauss = {
            "mean_kurt": float(ks.mean()), "max_dev": float(np.abs(ks - 3).max()),
            "mean_Q": float(Qs.mean()),
            "pass": bool(abs(ks.mean() - 3) < 3 * SEk / math.sqrt(len(ks))
                         and np.abs(ks - 3).max() < 4 * SEk
                         and 0.80 <= Qs.mean() <= 1.20),
        }
    return dw, npts, tstar, dw_uv, gauss

# ───────────────────────── PIPELINE ─────────────────────────
def run_one(N, seed):
    rng = np.random.default_rng(seed)
    pts, cand, L, rc = build_geometry(N, seed)
    E0 = E_PER_N * N
    assert len(cand) > E0
    st = BlobState(N, cand, rng.choice(len(cand), size=E0, replace=False))
    st.assert_E("init")
    st = equilibrate(st, cand, rng, SWEEPS_EQ)
    res = {"N": N, "seed": seed, "T_eq": st.T, "CV_eq": st.cv(),
           "Var_deg_eq": float(st.deg.var())}
    st_r = BlobState(N, cand, np.random.default_rng(seed + 77).choice(len(cand), size=E0, replace=False))
    res["Var_deg_neutre"] = float(st_r.deg.var())
    pack = tets_pack(st); pack_r = tets_pack(st_r)
    res["r_eq"], res["nA"] = measure_A(st, pack, pts, L, rng)
    res["r_rand"], _ = measure_A(st_r, pack_r, pts, L, rng)
    f_nv, part_m, part_d, med_m = measure_fnv(st, pack, pts, L, rng)
    res.update({"f_nv": f_nv, "part_m": part_m, "part_d": part_d, "med_m": med_m})
    dw, npts, tstar, dw_uv, gauss = walk_gibbs(st, pts, L, seed + 5)
    res.update({"dw_eq": dw, "dw_pts": npts, "t_star": tstar,
                "dw_uv": dw_uv, "gauss": gauss})
    return res

if __name__ == "__main__":
    print(GRID)
    print(f"Environnement: python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"Tailles {SIZES} × {SEEDS_PER_N} graines, β={BETA}, τ={TAU}, "
          f"|E|={E_PER_N}N, sweeps={SWEEPS_EQ}, seuil non-variété m>{NV_THRESH}\n")
    all_res = []
    t0 = time.time()
    for N in SIZES:
        for k in range(SEEDS_PER_N):
            seed = SEED_BASE[N] + k
            t1 = time.time()
            try:
                r = run_one(N, seed)
                all_res.append(r)
                g = r["gauss"]
                print(f"N={N} seed={seed}: T/N={r['T_eq']/N:.2f} r_eq={r['r_eq']:+.3f} "
                      f"ratio={r['Var_deg_eq']/r['Var_deg_neutre']:.2f} f_nv={r['f_nv']:.4f} "
                      f"part_m={r['part_m']:.3f} d_w={r['dw_eq']:.2f}({r['dw_pts']}p,t*={r['t_star']}) "
                      f"uv={r['dw_uv']:.2f} ({time.time()-t1:.0f}s)", flush=True)
            except Exception as ex:
                print(f"N={N} seed={seed} ÉCHOUÉE: {ex}", flush=True)
                traceback.print_exc()
                all_res.append({"N": N, "seed": seed, "error": str(ex)})
            with open(OUT_JSON, "w") as f:
                json.dump(all_res, f)
    # ─── LECTURE AUTOMATIQUE PAR LES GRILLES ───
    ok = [r for r in all_res if "r_eq" in r]
    print(f"\n════════ LECTURE ({(time.time()-t0)/60:.1f} min) ════════")
    for N in SIZES:
        sub = [r for r in ok if r["N"] == N]
        if not sub: continue
        re_ = np.array([r["r_eq"] for r in sub]); rr = np.array([r["r_rand"] for r in sub])
        ra = np.array([r["Var_deg_eq"] / r["Var_deg_neutre"] for r in sub])
        fv = np.array([r["f_nv"] for r in sub]); pm = np.array([r["part_m"] for r in sub])
        dw = np.array([r["dw_eq"] for r in sub]); du = np.array([r["dw_uv"] for r in sub])
        mm = np.array([r["med_m"] for r in sub])
        print(f"N={N}: r_eq={re_.mean():+.3f}±{re_.std():.3f}  r_rand={np.nanmean(rr):+.3f}  "
              f"ratio={ra.mean():.2f}±{ra.std():.2f}  f_nv={fv.mean():.4f}±{fv.std():.4f}  "
              f"part_m={pm.mean():.3f}  med_m={mm.mean():.0f}  "
              f"d_w={(np.nanmean(dw) if not np.all(np.isnan(dw)) else float('nan')):.2f}  d_w_UV={np.nanmean(du):.2f}")
    def bym(key):
        return {N: np.mean([r[key] for r in ok if r["N"] == N]) for N in SIZES}
    NLO, NHI = SIZES[0], SIZES[-1]
    re_m = bym("r_eq"); ra_m = {N: np.mean([r["Var_deg_eq"]/r["Var_deg_neutre"] for r in ok if r["N"]==N]) for N in SIZES}
    fv_m = bym("f_nv"); pm_m = bym("part_m")
    dA = re_m[NHI] - re_m[NLO]
    print(f"\nG1 (fait A) : Δr_eq({NHI}−{NLO}) = {dA:+.3f}  "
          f"[|Δ|≤0,05 robuste] → {'✓ ROBUSTE EN TAILLE' if abs(dA)<=0.05 else ('dérive ' + ('modérée (≤0,10)' if abs(dA)<=0.10 else 'RÉELLE (>0,10)'))}")
    rmax = max(ra_m.values()); rmin = min(ra_m.values())
    print(f"G2 (×4,7)   : ratios " + "/".join(f"{ra_m[N]:.2f}" for N in SIZES) + f"  max/min={rmax/rmin:.2f} "
          f"[≤1,30 invariant] → {'✓ INVARIANT THERMODYNAMIQUE' if rmax/rmin<=1.30 else 'DÉPENDANCE DE TAILLE'}")
    rf = fv_m[NHI]/max(fv_m[NLO],1e-12); rp = pm_m[NHI]/max(pm_m[NLO],1e-12)
    verdictB = ("DÉFAUTS QUI SE DILUENT — variété à défauts localisés" if rf < 0.80
                else ("DENSITÉ FINIE DE DÉFAUTS — objet mixte" if rf <= 1.25
                else "LES CONDENSATS DOMINENT LA LIMITE"))
    print(f"G3 (CASE B) : f_nv " + "→".join(f"{fv_m[N]:.4f}" for N in SIZES) + f" (ratio {rf:.2f}) ; "
          f"part_m ratio {rp:.2f}\n              → {verdictB}")
    print(f"G4 (SUP-1)  : d_w équilibré et d_w_UV par taille ci-dessus — INDICATIF ; "
          f"verrouillage = MSD grand N (patch limite continue).")
    print(f"\nRésultats complets : {OUT_JSON}")
