#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — SCAN DE PHASE EN β (ÉTAGE 1) : EXISTE-T-IL UNE FENÊTRE VARIÉTÉ+GRAVITÉ ?
# Protocole pré-enregistré. Version 1.0 — 14 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# CONTEXTE : le multi-N a rendu G3 = « densité finie de défauts » à β=0,30
# (f_nv ≈ 0,21 stable, 98,8 % de la courbure dans les défauts). Le dégrossissage
# container a trouvé une PHASE FONDUE : à β=2, f_nv ÷15 avec T/N = 3,3 vivant ;
# à β=8, f_nv = 0, graphe quasi régulier. Le Blob a un diagramme de phase.
# QUESTION DE CE SCAN (la question qui décide du pilier) :
#   existe-t-il β* où [f_nv ≤ 0,05] ET [fait A vivant : r_eq ≥ 0,5, r_rand ~ 0] ?
#   → si OUI : fenêtre variété+gravité candidate → ÉTAGE 2 (vérification lourde
#     à N = 3×10⁵ avec l'instrument d_s gelé sur ce β*).
#   → si NON (r_eq s'effondre partout où f_nv ≤ 0,05) : variété et gravité
#     s'excluent à τ = 0,5 → le scan passe à τ.
# PÉRIMÈTRE DÉCLARÉ : τ = 0,5 fixe ; le scan 2D (β, τ) est l'étape suivante si
# nécessaire. f_nv est un PROXY de variété (les conditions de link viendront).
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback
from collections import defaultdict
from itertools import combinations
import scipy.sparse as sp

# ───────────────────────── PARAMÈTRES ─────────────────────────
BETAS        = [0.3, 0.7, 1.2, 2.0, 4.0]
SEEDS_PER_B  = 6
SEED_BASE    = 5000            # banque fraîche : 5000 + 100*i_beta + k
N            = 6000
DENSITY      = 200.0
KAPPA        = 10.0
RCUT         = 1.6
TAU          = 0.5
E_PER_N      = 5
SWEEPS_EQ    = 30
EDGE_SAMPLE  = 2500
NV_THRESH    = 10
K_WALK       = 3000
T_WALK       = 300             # d_w_UV seulement (t ∈ [3,10]) + t*
OUT_JSON     = "phase_scan_results.json"

BETA = 0.3                      # réassigné par point de scan

GRID = """
════════════════ GRILLES PRÉ-ENREGISTRÉES (gravées AVANT lecture) ════════════════
P1 (transition) : courbe f_nv(β) — localiser β_c où f_nv passe sous 0,05.
P2 (LA question) : r_eq(β) et r_rand(β).
    → FENÊTRE VARIÉTÉ+GRAVITÉ si ∃ β avec f_nv ≤ 0,05 ET r_eq ≥ 0,50
      ET |r_rand| ≤ 0,2  → CANDIDAT ÉTAGE 2 = plus petit β qui satisfait tout.
    → EXCLUSION à τ=0,5 si r_eq < 0,30 partout où f_nv ≤ 0,05 → scan τ ensuite.
    → Entre 0,30 et 0,50 : zone grise, raffiner autour.
P3 (suivi ×4,7) : Var_eq/Var_neutre (β) — le ×4,7 est-il propre à la phase
    condensée ? Rapporté tel quel (aucun pari).
P4 (piégeage) : d_w_UV(β) — prédiction : décroît vers ~2,05–2,10 quand les
    condensats fondent. Écart lu tel quel.
Tout écart aux grilles se lit tel quel. Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────── GÉOMÉTRIE / ÉTAT (pipeline validé, paramétré) ─────────────────
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
        dCV = cv_new - self.cv()
        return (d_logT - BETA * dCV), dT, d2_new
    def do_swap(self, u, v, a, b, dT, d2_new):
        self.adj[u].discard(v); self.adj[v].discard(u)
        self.adj[a].add(b); self.adj[b].add(a)
        self.deg[u] -= 1; self.deg[v] -= 1; self.deg[a] += 1; self.deg[b] += 1
        self.sum_d2 = d2_new; self.T += dT
    def assert_E(self, tag):
        e_now = sum(len(s) for s in self.adj.values()) // 2
        assert e_now == self.E == E_PER_N * N, f"|E| VIOLÉ [{tag}]"

def equilibrate(state, cand, rng, sweeps):
    te = TAU / N
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
    return e2t, len(tets)

def measure_A(state, e2t, pts, L, rng):
    edges = [e for e, ts in e2t.items() if len(ts) >= 2]
    if len(edges) < 30: return float("nan"), len(edges)
    if len(edges) > EDGE_SAMPLE:
        idx = rng.choice(len(edges), size=EDGE_SAMPLE, replace=False)
        edges = [edges[i] for i in idx]
    xs = []; ys = []
    for e in edges:
        ts = e2t[e]
        d = 2 * math.pi - sum(dihedral(pts, L, t, e) for t in ts)
        xs.append(float(state.deg[e[0]] + state.deg[e[1]])); ys.append(abs(d))
    if np.std(xs) == 0: return float("nan"), len(xs)
    return float(np.corrcoef(xs, ys)[0, 1]), len(xs)

def measure_fnv(e2t):
    ms = np.array([len(ts) for ts in e2t.values() if len(ts) >= 2])
    E = E_PER_N * N
    if len(ms) == 0: return 0.0, 0.0, float("nan")
    f_nv = float((ms > NV_THRESH).sum()) / E
    part_m = float(ms[ms > NV_THRESH].sum()) / max(float(ms.sum()), 1.0)
    return f_nv, part_m, float(np.median(ms))

def adj_to_csr(state):
    rows = []; cols = []
    for u in state.adj:
        for v in state.adj[u]:
            rows.append(u); cols.append(v)
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
    return ((A + A.T) > 0).astype(float).tocsr()

def walk_uv(state, pts, L, seed):
    A = adj_to_csr(state)
    ip, ix = A.indptr, A.indices
    r2 = np.random.default_rng(seed)
    u = r2.choice(N, size=K_WALK)
    X = np.zeros((K_WALK, 3))
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
    ok_uv = (tg >= 3) & (tg <= 10)
    sl_uv = float(np.polyfit(np.log(tg[ok_uv]), np.log(msd[ok_uv]), 1)[0])
    cap = (L / 2) ** 2
    okw = (tg >= 20) & (msd < cap)
    tstar = int(tg[okw][-1]) if okw.sum() else 0
    return 2.0 / sl_uv, tstar

# ───────────────────────── PIPELINE ─────────────────────────
def run_point(beta, seed):
    global BETA
    BETA = beta
    rng = np.random.default_rng(seed)
    pts, cand, L, rc = build_geometry(N, seed)
    E0 = E_PER_N * N
    assert len(cand) > E0
    st = BlobState(cand, rng.choice(len(cand), size=E0, replace=False))
    st.assert_E("init")
    st = equilibrate(st, cand, rng, SWEEPS_EQ)
    res = {"beta": beta, "seed": seed, "N": N, "T_eq": st.T, "CV_eq": st.cv(),
           "Var_deg_eq": float(st.deg.var())}
    st_r = BlobState(cand, np.random.default_rng(seed + 77).choice(len(cand), size=E0, replace=False))
    res["Var_deg_neutre"] = float(st_r.deg.var())
    pack, ntets = tets_pack(st)
    pack_r, _ = tets_pack(st_r)
    res["ntets"] = ntets
    res["r_eq"], res["nA"] = measure_A(st, pack, pts, L, rng)
    res["r_rand"], _ = measure_A(st_r, pack_r, pts, L, rng)
    res["f_nv"], res["part_m"], res["med_m"] = measure_fnv(pack)
    res["dw_uv"], res["t_star"] = walk_uv(st, pts, L, seed + 5)
    return res

if __name__ == "__main__":
    print(GRID)
    print(f"Environnement: python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"β ∈ {BETAS} × {SEEDS_PER_B} graines, N={N}, τ={TAU}, |E|={E_PER_N}N, "
          f"sweeps={SWEEPS_EQ}, seuil non-variété m>{NV_THRESH}\n")
    all_res = []
    t0 = time.time()
    for ib, beta in enumerate(BETAS):
        for k in range(SEEDS_PER_B):
            seed = SEED_BASE + 100 * ib + k
            t1 = time.time()
            try:
                r = run_point(beta, seed)
                all_res.append(r)
                print(f"β={beta} seed={seed}: T/N={r['T_eq']/N:.2f} CV={r['CV_eq']:.3f} "
                      f"f_nv={r['f_nv']:.4f} med_m={r['med_m']:.0f} r_eq={r['r_eq']:+.3f} "
                      f"r_rand={r['r_rand']:+.2f} d_w_UV={r['dw_uv']:.2f} ({time.time()-t1:.0f}s)",
                      flush=True)
            except Exception as ex:
                print(f"β={beta} seed={seed} ÉCHOUÉE: {ex}", flush=True)
                traceback.print_exc()
                all_res.append({"beta": beta, "seed": seed, "error": str(ex)})
            with open(OUT_JSON, "w") as f:
                json.dump(all_res, f)
    # ─── LECTURE AUTOMATIQUE ───
    ok = [r for r in all_res if "r_eq" in r]
    print(f"\n════════ LECTURE ({(time.time()-t0)/60:.1f} min) ════════")
    print(f"{'β':>5} | {'T/N':>5} | {'CV':>5} | {'f_nv':>7} | {'med_m':>5} | {'r_eq':>6} | {'r_rand':>6} | {'ratio':>5} | {'d_w_UV':>6}")
    stats = {}
    for beta in BETAS:
        s = [r for r in ok if r["beta"] == beta]
        if not s: continue
        g = lambda k: np.array([r[k] for r in s], float)
        stats[beta] = {
            "TN": g("T_eq").mean() / N, "CV": g("CV_eq").mean(),
            "fnv": np.nanmean(g("f_nv")), "med": np.nanmean(g("med_m")),
            "req": np.nanmean(g("r_eq")), "rrd": np.nanmean(g("r_rand")),
            "ratio": np.nanmean(g("Var_deg_eq") / g("Var_deg_neutre")),
            "dwu": np.nanmean(g("dw_uv")),
            "req_sd": np.nanstd(g("r_eq")),
        }
        st_ = stats[beta]
        print(f"{beta:>5} | {st_['TN']:>5.2f} | {st_['CV']:>5.3f} | {st_['fnv']:>7.4f} | "
              f"{st_['med']:>5.0f} | {st_['req']:>+6.3f} | {st_['rrd']:>+6.2f} | "
              f"{st_['ratio']:>5.2f} | {st_['dwu']:>6.2f}")
    cands = [b for b in BETAS if b in stats and stats[b]["fnv"] <= 0.05
             and stats[b]["req"] >= 0.50 and abs(stats[b]["rrd"]) <= 0.2]
    grey = [b for b in BETAS if b in stats and stats[b]["fnv"] <= 0.05
            and 0.30 <= stats[b]["req"] < 0.50]
    print()
    if cands:
        bstar = min(cands)
        print(f"P2 → ★ FENÊTRE VARIÉTÉ+GRAVITÉ : CANDIDAT ÉTAGE 2 = β* = {bstar}")
        print(f"     (f_nv={stats[bstar]['fnv']:.4f}, r_eq={stats[bstar]['req']:+.3f}±{stats[bstar]['req_sd']:.3f})")
        print(f"     → Étage 2 : vérification lourde à N=3×10⁵, instrument d_s gelé, sur β={bstar}.")
    elif grey:
        print(f"P2 → ZONE GRISE : r_eq ∈ [0,30 ; 0,50[ à f_nv ≤ 0,05 pour β ∈ {grey} — raffiner autour.")
    else:
        low = [b for b in BETAS if b in stats and stats[b]["fnv"] <= 0.05]
        if low:
            print(f"P2 → EXCLUSION à τ=0,5 : partout où f_nv ≤ 0,05 (β ∈ {low}), r_eq < 0,30")
            print(f"     → variété et gravité s'excluent à cette température → scan en τ.")
        else:
            print(f"P2 → aucun β du scan n'atteint f_nv ≤ 0,05 — étendre la gamme de β.")
    print(f"\nP1 : transition f_nv — lisible dans le tableau (β_c entre les colonnes où f_nv croise 0,05).")
    print(f"P3 : ratio(β) rapporté tel quel.  P4 : d_w_UV(β) vs prédiction ~2,05–2,10 en phase fondue.")
    print(f"\nRésultats complets : {OUT_JSON}")
