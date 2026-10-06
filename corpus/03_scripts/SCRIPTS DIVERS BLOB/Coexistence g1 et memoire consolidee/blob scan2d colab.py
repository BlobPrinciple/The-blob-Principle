#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — SCAN 2D (β, τ) : PORTE (a) — UNE SECONDE TEMPÉRATURE BRISE-T-ELLE
#                         LE TRILEMME ?
# Protocole pré-enregistré. Version 1.0 — 15 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# LE TRILEMME (établi hier) : sur l'axe β à τ=0,5, les trois trésors —
# géométrie 3D, variété (f_nv→0), gravité (r_eq) — ne coexistent JAMAIS à la
# limite. Racine diagnostiquée : 98,8 % de la courbure vit dans les défauts,
# donc β couple INDISSOCIABLEMENT homogénéité (variété) et dissolution des
# hubs (mort de la gravité). Portes 0 et D fermées : la gravité est absente
# de la phase fondue, statiquement ET dynamiquement.
# HYPOTHÈSE DE LA PORTE (a) : τ (température de la mesure exp((N/τ)S)) contrôle
# l'AMPLITUDE des fluctuations INDÉPENDAMMENT de β. Existe-t-il (β*, τ*) où les
# défauts restent LOCALEMENT hétérogènes (gravité vivante) mais GLOBALEMENT
# dilués (variété) ? τ bas = mesure piquée (près du minimum d'action) ;
# τ haut = mesure diffuse (near-uniforme sur les configs).
# CE QUE CE SCRIPT MESURE, par (β, τ), N=6000, 5 graines :
#   f_nv (variété), r_eq vs r_rand (gravité), med_m, ratio Var, d_w_UV, T/N, CV.
# PÉRIMÈTRE : N=6000 (comme le scan β) ; le candidat gagnant, s'il existe, ira
# à l'étage 2 (N=3e5). Un point (β,τ) où f_nv≤0,05 ET r_eq≥0,50 = BRÈCHE.
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback
from collections import defaultdict
from itertools import combinations
import scipy.sparse as sp

# ───────────────────────── PARAMÈTRES ─────────────────────────
# grille 2D : 3 β × 3 τ = 9 points (β=2 est le bord de la fenêtre à τ=0,5)
BETAS      = [1.2, 2.0, 3.0]
TAUS       = [0.2, 0.5, 1.2]
SEEDS_PT   = 5
SEED_BASE  = 6000            # 6000 + 100*i_beta + 10*i_tau + k
N          = 6000
DENSITY    = 200.0
KAPPA      = 10.0
RCUT       = 1.6
E_PER_N    = 5
SWEEPS_EQ  = 30
EDGE_SAMPLE= 2500
NV_THRESH  = 10
K_WALK     = 3000
T_WALK     = 300
OUT_JSON   = "scan2d_results.json"

BETA = 2.0; TAU = 0.5        # réassignés par point

GRID = """
════════════════ GRILLE PRÉ-ENREGISTRÉE (gravée AVANT lecture) ════════════════
LA QUESTION (porte a) : ∃ (β,τ) avec f_nv ≤ 0,05 ET r_eq ≥ 0,50 ET |r_rand| ≤ 0,2 ?
  → BRÈCHE DANS LE TRILEMME : candidat étage 2. Le plan (β,τ) sépare ce que β
    seul ne pouvait pas → la limite continue variété+gravité redevient possible.
  → AUCUN point ne satisfait les deux : le trilemme RÉSISTE à τ →
    porte (a) close, on passe à (b) action modifiée. Gravé sans détour.
LECTURE DIRECTIONNELLE (pré-écrite) :
  • τ BAS (0,2) : mesure piquée. Prédiction — renforce l'ordre existant (hubs plus
    marqués à β bas, pavage plus net à β haut) ; peu susceptible d'ouvrir une brèche
    mais teste si « geler » près du minimum sépare les échelles.
  • τ HAUT (1,2) : mesure diffuse. Prédiction — near-uniform, f_nv remonte vers RGG
    (~0,21) partout, gravité s'affaiblit (désordre). Le test décisif est la DIAGONALE :
    un τ intermédiaire à β modéré pourrait tenir la niche.
  • L'espoir précis : (β≈1,2, τ bas) où med_m descend vers 5 SANS dissoudre les
    corrélations — le « pavage hétérogène ». Falsifiable ici.
Chaque issue se lit telle quelle. Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────── GÉOMÉTRIE / ÉTAT (pipeline validé) ─────────────────
def build_geometry(N, seed):
    rng = np.random.default_rng(seed)
    L = (N / DENSITY) ** (1/3)
    pts = rng.uniform(0, L, size=(N, 3))
    rc = RCUT * (3 * KAPPA / (4 * math.pi * DENSITY)) ** (1/3)
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
    def __init__(self, cand, active_idx):
        self.cand = cand
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
        mu = 2.0 * self.E / N
        var = self.sum_d2 / N - mu * mu
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
        mu = 2.0 * self.E / N
        cv_new = math.sqrt(max(d2_new / N - mu * mu, 0.0)) / mu
        return (d_logT - BETA * (cv_new - self.cv())), dT, d2_new
    def do_swap(self, u, v, a, b, dT, d2_new):
        self.adj[u].discard(v); self.adj[v].discard(u)
        self.adj[a].add(b); self.adj[b].add(a)
        self.deg[u] -= 1; self.deg[v] -= 1; self.deg[a] += 1; self.deg[b] += 1
        self.sum_d2 = d2_new; self.T += dT
    def assert_E(self, tag):
        e_now = sum(len(s) for s in self.adj.values()) // 2
        assert e_now == self.E == E_PER_N * N, f"|E| VIOLÉ [{tag}]"

def equilibrate(state, cand, rng, sweeps):
    te = TAU / N                       # ← τ intervient ICI (température de mesure)
    edge_list = [(i, j) for i in range(N) for j in state.adj[i] if j > i]
    for sw in range(sweeps):
        for _ in range(3 * N):
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

# ─────────────── MESURES ───────────────
def dihedral(pts, L, tet, edge):
    e0, e1 = edge; oth = [x for x in tet if x not in edge]
    ax = pts[e1] - pts[e0]; ax -= L * np.round(ax / L)
    ax = ax / max(np.linalg.norm(ax), 1e-12)
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
    e2t = defaultdict(list)
    for (u, v, w) in tris:
        for x in state.adj[u] & state.adj[v] & state.adj[w]:
            if x > w:
                for e in combinations((u, v, w, x), 2):
                    e2t[tuple(sorted(e))].append((u, v, w, x))
    return e2t

def measure_A(state, e2t, pts, L, rng):
    edges = [e for e, ts in e2t.items() if len(ts) >= 2]
    if len(edges) < 30: return float("nan")
    if len(edges) > EDGE_SAMPLE:
        edges = [edges[i] for i in rng.choice(len(edges), size=EDGE_SAMPLE, replace=False)]
    xs = []; ys = []
    for e in edges:
        ts = e2t[e]
        d = 2 * math.pi - sum(dihedral(pts, L, t, e) for t in ts)
        xs.append(float(state.deg[e[0]] + state.deg[e[1]])); ys.append(abs(d))
    return float(np.corrcoef(xs, ys)[0, 1]) if np.std(xs) > 0 else float("nan")

def measure_fnv(e2t):
    ms = np.array([len(ts) for ts in e2t.values() if len(ts) >= 2])
    E = E_PER_N * N
    if len(ms) == 0: return 0.0, 0.0, float("nan")
    return float((ms > NV_THRESH).sum()) / E, \
           float(ms[ms > NV_THRESH].sum()) / max(float(ms.sum()), 1.0), \
           float(np.median(ms))

def adj_csr(state):
    rows = []; cols = []
    for u in state.adj:
        for v in state.adj[u]:
            rows.append(u); cols.append(v)
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
    return ((A + A.T) > 0).astype(float).tocsr()

def walk_uv(state, pts, L, seed):
    A = adj_csr(state); ip, ix = A.indptr, A.indices
    r2 = np.random.default_rng(seed)
    u = r2.choice(N, size=K_WALK); X = np.zeros((K_WALK, 3))
    deg = (ip[1:] - ip[:-1])
    tg = np.unique(np.round(np.logspace(0, math.log10(T_WALK), 25)).astype(int))
    msd = np.zeros(len(tg)); tj = 0
    for t in range(1, T_WALK + 1):
        r = (r2.random(K_WALK) * deg[u]).astype(np.int64)
        v = ix[ip[u] + r]
        dl = pts[v] - pts[u]; dl -= L * np.round(dl / L)
        X += dl; u = v
        if tj < len(tg) and t == tg[tj]:
            msd[tj] = float((X ** 2).sum(1).mean()); tj += 1
    ok = (tg >= 3) & (tg <= 10)
    return 2.0 / float(np.polyfit(np.log(tg[ok]), np.log(msd[ok]), 1)[0])

def run_point(beta, tau, seed):
    global BETA, TAU
    BETA = beta; TAU = tau
    rng = np.random.default_rng(seed)
    pts, cand, L, rc = build_geometry(N, seed)
    E0 = E_PER_N * N
    assert len(cand) > E0
    st = BlobState(cand, rng.choice(len(cand), size=E0, replace=False))
    st = equilibrate(st, cand, rng, SWEEPS_EQ)
    res = {"beta": beta, "tau": tau, "seed": seed, "N": N,
           "T_eq": st.T, "CV_eq": st.cv(), "Var_deg_eq": float(st.deg.var())}
    st_r = BlobState(cand, np.random.default_rng(seed + 77).choice(len(cand), size=E0, replace=False))
    res["Var_deg_neutre"] = float(st_r.deg.var())
    pack = tets_pack(st); pack_r = tets_pack(st_r)
    res["r_eq"] = measure_A(st, pack, pts, L, rng)
    res["r_rand"] = measure_A(st_r, pack_r, pts, L, rng)
    res["f_nv"], res["part_m"], res["med_m"] = measure_fnv(pack)
    res["dw_uv"] = walk_uv(st, pts, L, seed + 5)
    return res

if __name__ == "__main__":
    print(GRID)
    print(f"Environnement : python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"β ∈ {BETAS} × τ ∈ {TAUS} × {SEEDS_PT} graines, N={N}, |E|={E_PER_N}N, sweeps={SWEEPS_EQ}\n")
    all_res = []
    t0 = time.time()
    for ib, beta in enumerate(BETAS):
        for it, tau in enumerate(TAUS):
            for k in range(SEEDS_PT):
                seed = SEED_BASE + 100 * ib + 10 * it + k
                t1 = time.time()
                try:
                    r = run_point(beta, tau, seed)
                    all_res.append(r)
                    print(f"β={beta} τ={tau} s={seed}: T/N={r['T_eq']/N:.2f} f_nv={r['f_nv']:.4f} "
                          f"med_m={r['med_m']:.0f} r_eq={r['r_eq']:+.3f} r_rand={r['r_rand']:+.2f} "
                          f"d_w_UV={r['dw_uv']:.2f} ({time.time()-t1:.0f}s)", flush=True)
                except Exception as ex:
                    print(f"β={beta} τ={tau} s={seed} ÉCHEC: {ex}", flush=True)
                    traceback.print_exc()
                    all_res.append({"beta": beta, "tau": tau, "seed": seed, "error": str(ex)})
                with open(OUT_JSON, "w") as f:
                    json.dump(all_res, f)
    # ─── LECTURE AUTOMATIQUE ───
    ok = [r for r in all_res if "r_eq" in r]
    print(f"\n════════ CARTE (β, τ) ({(time.time()-t0)/60:.1f} min) ════════")
    print(f"{'β':>5} {'τ':>5} | {'T/N':>5} | {'f_nv':>7} | {'med_m':>5} | {'r_eq':>7} | {'r_rand':>6} | {'ratio':>5} | {'d_w_UV':>6}")
    S = {}
    for beta in BETAS:
        for tau in TAUS:
            s = [r for r in ok if r["beta"] == beta and r["tau"] == tau]
            if not s: continue
            g = lambda k: np.array([r[k] for r in s], float)
            S[(beta, tau)] = {
                "TN": g("T_eq").mean() / N, "fnv": np.nanmean(g("f_nv")),
                "med": np.nanmean(g("med_m")), "req": np.nanmean(g("r_eq")),
                "req_sd": np.nanstd(g("r_eq")), "rrd": np.nanmean(g("r_rand")),
                "ratio": np.nanmean(g("Var_deg_eq") / g("Var_deg_neutre")),
                "dwu": np.nanmean(g("dw_uv")),
            }
            x = S[(beta, tau)]
            print(f"{beta:>5} {tau:>5} | {x['TN']:>5.2f} | {x['fnv']:>7.4f} | {x['med']:>5.0f} | "
                  f"{x['req']:>+7.3f} | {x['rrd']:>+6.2f} | {x['ratio']:>5.2f} | {x['dwu']:>6.2f}")
    breaches = [(b, t) for (b, t) in S if S[(b, t)]["fnv"] <= 0.05
                and S[(b, t)]["req"] >= 0.50 and abs(S[(b, t)]["rrd"]) <= 0.2]
    grey = [(b, t) for (b, t) in S if S[(b, t)]["fnv"] <= 0.05
            and 0.35 <= S[(b, t)]["req"] < 0.50]
    print()
    if breaches:
        bstar = min(breaches, key=lambda bt: (S[bt]["fnv"], -S[bt]["req"]))
        print(f"★★★ BRÈCHE DANS LE TRILEMME : (β,τ) = {breaches} → candidat étage 2 = {bstar}")
        print(f"    f_nv={S[bstar]['fnv']:.4f}, r_eq={S[bstar]['req']:+.3f}±{S[bstar]['req_sd']:.3f} — τ SÉPARE ce que β seul ne pouvait pas.")
        print(f"    → étage 2 sur ce point (N=3e5) pour vérifier que la brèche survit à la limite.")
    elif grey:
        print(f"ZONE GRISE : r_eq ∈ [0,35;0,50[ à f_nv≤0,05 pour {grey} — raffiner τ autour avant conclusion.")
    else:
        print(f"AUCUNE BRÈCHE : partout où f_nv≤0,05, r_eq<0,35 — LE TRILEMME RÉSISTE À τ.")
        print(f"→ porte (a) CLOSE. Passage à (b) : action modifiée (terme Regge-Einstein découplant")
        print(f"  courbure-densité du sur-empilement). Gravé sans détour.")
    print(f"\nRésultats complets : {OUT_JSON}")
