#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — CONSOLIDATION G1 : COEXISTENCE « POCHES DANS LA MER »
# Matière gravitante (condensé) DANS espace variété (fondu), même système.
# Protocole pré-enregistré. Version 1.0 — 16 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# CONTEXTE : le trilemme (gravité/variété/3D jamais au même POINT du diagramme,
# établi §M) trouve sa résolution dans le PREMIER ORDRE (hystérésis thermo, M-6.1) :
# une transition du 1er ordre autorise la COEXISTENCE SPATIALE de deux phases dans
# un même système (comme eau/glace). Test container préliminaire [M, 2 graines] :
# une poche condensée relâchée en dynamique LIBRE près de β_co garde sa gravité
# (r_eq 0,54→0,71) pendant que la mer garde sa variété (f_nv=0,011). CE RUN consolide.
# CE QUE CE SCRIPT MESURE, par (β_co, durée, graine), N=10000 :
#   poche : r_eq(interne), f_nv(interne)   |   mer : f_nv(interne), r_eq(interne)
#   + dérive d'interface : évolution de f_nv(mer) avec la durée (la mer condense-t-elle ?)
# GRILLE : critère PAR GRAINE cette fois (le préliminaire ne tranchait pas 2001).
# β_co scanné pour LOCALISER le vrai point de coexistence (le préliminaire supposait 1,6).
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback, warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from collections import defaultdict
from itertools import combinations

# ───────────────────────── PARAMÈTRES ─────────────────────────
N          = 10000
SEEDS      = [2100, 2101, 2102, 2103, 2104, 2105]
BETA_CO    = [1.4, 1.6, 1.8]          # scan pour localiser β_co réel
DURATIONS  = [8, 16, 32]              # sweeps de relaxation libre (test de durée)
POCKET_FRAC = 0.25                    # fraction volumique de la poche
BETA_LO    = 0.3                      # phase condensée (poche)
BETA_HI    = 3.0                      # phase variété (mer)
PREP_SW    = 20                       # sweeps de préparation par région
DENSITY    = 200.0
KAPPA      = 10.0
RCUT       = 1.6
TAU        = 0.5
E_PER_N    = 5
EDGE_SAMPLE = 900
NV_THRESH  = 10
OUT_JSON   = "coexistence_g1_results.json"

BETA = 1.6

GRID = """
════════════════ GRILLE PRÉ-ENREGISTRÉE (gravée AVANT lecture) ════════════════
QUESTION : le 1er ordre autorise-t-il une coexistence spatiale STABLE
  matière-gravitante / espace-variété dans un même système ?
CRITÈRE PAR GRAINE (corrige l'ambiguïté du préliminaire) :
  une graine SATISFAIT à (β_co, durée) si r_eq(poche) ≥ 0,45 ET f_nv(mer) ≤ 0,05.
VERDICTS :
  • ROBUSTE si, à au moins un β_co, ≥ 5/6 graines satisfont À TOUTES les durées
    (8,16,32) : la coexistence est STABLE dans la durée → architecture TOE
    « poches dans la mer » [M robuste]. β_co* = celui qui maximise le taux.
  • MÉTASTABLE-COURT si satisfait à durée 8 mais dégrade à 32 (mer condense ou
    poche fond) : coexistence transitoire seulement → [M] avec durée de vie finie.
  • ÉCHOUE si < 5/6 même à durée 8 : pas de coexistence robuste à N=10000. Tel quel.
DÉRIVE D'INTERFACE : f_nv(mer) vs durée — pente > 0 = la mer condense lentement
  (contamination par la poche) ; pente ≈ 0 = interface stable.
LOCALISATION β_co : le β_co réel est celui où poche et mer sont TOUTES DEUX le plus
  proche de leurs valeurs pures (équilibre des pressions de phase).
Tout écart se lit tel quel. Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────── PIPELINE (identique container validé) ─────────────────
def build_geometry(seed):
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
        d2_new = self.sum_d2 + (-2*self.deg[u]+1) + (-2*self.deg[v]+1) + (2*self.deg[a]+1) + (2*self.deg[b]+1)
        mu = 2.0 * self.E / N
        cv_new = math.sqrt(max(d2_new / N - mu * mu, 0.0)) / mu
        return (d_logT - BETA * (cv_new - self.cv())), dT, d2_new
    def do_swap(self, u, v, a, b, dT, d2_new):
        self.adj[u].discard(v); self.adj[v].discard(u)
        self.adj[a].add(b); self.adj[b].add(a)
        self.deg[u] -= 1; self.deg[v] -= 1; self.deg[a] += 1; self.deg[b] += 1
        self.sum_d2 = d2_new; self.T += dT

def relax(st, cand, beta, seed, sw, allowed=None):
    global BETA
    BETA = beta
    rng = np.random.default_rng(seed)
    te = TAU / N
    el = [(i, j) for i in range(N) for j in st.adj[i] if j > i]
    for _ in range(sw):
        for _ in range(3 * N):
            io = rng.integers(len(el)); u, v = el[io]
            ii = rng.integers(len(cand)); a, b = cand[ii]
            if b in st.adj[a] or v not in st.adj[u]: continue
            if len({u, v, a, b}) < 4: continue
            if st.deg[u] <= 2 or st.deg[v] <= 2: continue
            if allowed is not None and not (allowed[u] and allowed[v] and allowed[a] and allowed[b]): continue
            dS, dT, d2n = st.dS_swap(u, v, a, b)
            if dS >= 0 or rng.random() < math.exp(dS / te):
                st.do_swap(u, v, a, b, dT, d2n); el[io] = (a, b)
    return st

# ───────────────── MESURE PAR RÉGION ─────────────────
def dih(pts, L, tet, e):
    e0, e1 = e; oth = [x for x in tet if x not in e]
    ax = pts[e1] - pts[e0]; ax -= L * np.round(ax / L); ax /= max(np.linalg.norm(ax), 1e-12)
    vs = []
    for o in oth:
        po = pts[o] - pts[e0]; po -= L * np.round(po / L); pp = po - np.dot(po, ax) * ax
        vs.append(pp / max(np.linalg.norm(pp), 1e-12))
    return math.acos(np.clip(np.dot(vs[0], vs[1]), -1, 1))

def region_stats(st, pts, L, masks, seed):
    tris = set()
    for u in st.adj:
        for v in st.adj[u]:
            if v > u:
                for w in st.adj[u] & st.adj[v]:
                    if w > v: tris.add((u, v, w))
    e2t = defaultdict(list)
    for (u, v, w) in tris:
        for x in st.adj[u] & st.adj[v] & st.adj[w]:
            if x > w:
                for e in combinations((u, v, w, x), 2): e2t[tuple(sorted(e))].append((u, v, w, x))
    out = {}
    rng = np.random.default_rng(seed)
    for name, mask in masks.items():
        edges = [e for e, ts in e2t.items() if len(ts) >= 2 and mask[e[0]] and mask[e[1]]]
        Ein = sum(1 for i in range(N) if mask[i] for j in st.adj[i] if j > i and mask[j])
        ms = [len(e2t[e]) for e in edges]
        f_nv = float(sum(1 for m in ms if m > NV_THRESH)) / max(Ein, 1)
        samp = edges if len(edges) <= EDGE_SAMPLE else [edges[i] for i in rng.choice(len(edges), EDGE_SAMPLE, replace=False)]
        if len(samp) > 40:
            xs = [float(st.deg[e[0]] + st.deg[e[1]]) for e in samp]
            ys = [abs(2 * math.pi - sum(dih(pts, L, t, e) for t in e2t[e])) for e in samp]
            r_eq = float(np.corrcoef(xs, ys)[0, 1]) if np.std(xs) > 0 else float("nan")
        else:
            r_eq = float("nan")
        out[name] = {"f_nv": f_nv, "r_eq": r_eq, "n_edges": len(edges)}
    return out

# ───────────────── PIPELINE PAR (β_co, graine) ─────────────────
def run_seed_beta(seed, beta_co):
    pts, cand, L, rc = build_geometry(seed)
    dv = pts - pts.mean(0); dv -= L * np.round(dv / L)
    dist = np.linalg.norm(dv, axis=1)
    Rp = L * (3 * POCKET_FRAC / (4 * math.pi)) ** (1/3)
    pocket = dist < Rp; sea = ~pocket
    masks = {"poche": pocket, "mer": sea}
    rng = np.random.default_rng(seed)
    st = BlobState(cand, rng.choice(len(cand), size=E_PER_N*N, replace=False))
    # préparation biphasée (swaps internes seulement)
    st = relax(st, cand, BETA_LO, seed + 1, PREP_SW, allowed=pocket)
    st = relax(st, cand, BETA_HI, seed + 2, PREP_SW, allowed=sea)
    prep = region_stats(st, pts, L, masks, seed + 3)
    # relaxation LIBRE, mesurée à chaque durée (cumulative)
    traj = {"prep": prep}
    done = 0
    for target in DURATIONS:
        st = relax(st, cand, beta_co, seed + 100 + done, target - done, allowed=None)
        done = target
        traj[f"free_{target}"] = region_stats(st, pts, L, masks, seed + 200 + target)
    return traj

# ───────────────── MAIN ─────────────────
if __name__ == "__main__":
    print(GRID)
    print(f"Environnement : python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"N={N}, graines {SEEDS}, β_co ∈ {BETA_CO}, durées {DURATIONS}, poche={POCKET_FRAC:.0%}\n")
    all_res = []
    t0 = time.time()
    for beta_co in BETA_CO:
        for seed in SEEDS:
            t1 = time.time()
            try:
                traj = run_seed_beta(seed, beta_co)
                rec = {"seed": seed, "beta_co": beta_co, "traj": traj}
                all_res.append(rec)
                p8 = traj["free_8"]; p32 = traj[f"free_{DURATIONS[-1]}"]
                print(f"β_co={beta_co} s={seed}: [8sw] poche r_eq={p8['poche']['r_eq']:+.3f} f_nv={p8['poche']['f_nv']:.3f} | mer f_nv={p8['mer']['f_nv']:.4f}"
                      f"  →[32sw] poche r_eq={p32['poche']['r_eq']:+.3f} | mer f_nv={p32['mer']['f_nv']:.4f}  ({time.time()-t1:.0f}s)", flush=True)
            except Exception as ex:
                print(f"β_co={beta_co} s={seed} ÉCHEC: {ex}", flush=True); traceback.print_exc()
                all_res.append({"seed": seed, "beta_co": beta_co, "error": str(ex)})
            with open(OUT_JSON, "w") as f:
                json.dump(all_res, f)
    # ─── LECTURE AUTOMATIQUE ───
    ok = [r for r in all_res if "traj" in r]
    print(f"\n════════ VERDICT ({(time.time()-t0)/60:.0f} min, {len(ok)} points) ════════")
    def satisfies(stats):
        return (not math.isnan(stats["poche"]["r_eq"])) and stats["poche"]["r_eq"] >= 0.45 and stats["mer"]["f_nv"] <= 0.05
    best_beta = None; best_rate = -1
    for beta_co in BETA_CO:
        s = [r for r in ok if r["beta_co"] == beta_co]
        if not s: continue
        # taux à chaque durée
        rates = {}
        for target in DURATIONS:
            rates[target] = sum(1 for r in s if satisfies(r["traj"][f"free_{target}"])) / len(s)
        rate_all = sum(1 for r in s if all(satisfies(r["traj"][f"free_{t}"]) for t in DURATIONS)) / len(s)
        rp8 = np.mean([r["traj"]["free_8"]["poche"]["r_eq"] for r in s])
        fm8 = np.mean([r["traj"]["free_8"]["mer"]["f_nv"] for r in s])
        fm32 = np.mean([r["traj"][f"free_{DURATIONS[-1]}"]["mer"]["f_nv"] for r in s])
        drift = fm32 - fm8
        print(f"β_co={beta_co}: taux[8sw]={rates[DURATIONS[0]]:.0%} [16]={rates[DURATIONS[1]]:.0%} [32]={rates[DURATIONS[-1]]:.0%} | TOUTES durées={rate_all:.0%} | "
              f"⟨r_eq poche⟩={rp8:+.2f} ⟨f_nv mer⟩ {fm8:.4f}→{fm32:.4f} (dérive {drift:+.4f})")
        if rate_all > best_rate:
            best_rate = rate_all; best_beta = beta_co
    print()
    if best_rate >= 5/6:
        print(f"→ ★★★ COEXISTENCE ROBUSTE à β_co*={best_beta} ({best_rate:.0%} des graines, TOUTES durées).")
        print(f"   Architecture TOE « poches dans la mer » établie [M robuste] : matière gravitante")
        print(f"   et espace variété coexistent stablement dans un même système. Le 1er ordre résout le trilemme.")
    elif any(sum(1 for r in ok if r['beta_co']==b and satisfies(r['traj']['free_8']))/max(sum(1 for r in ok if r['beta_co']==b),1) >= 5/6 for b in BETA_CO):
        print(f"→ COEXISTENCE MÉTASTABLE-COURTE : robuste à 8 sw, dégrade à 32 sw (voir dérive).")
        print(f"   Durée de vie finie à N={N} — [M], à étendre (N plus grand, ou mécanisme de tension d'interface).")
    else:
        print(f"→ pas de coexistence robuste (< 5/6) même à 8 sw. Le préliminaire 2 graines était optimiste. Tel quel.")
    print(f"\nRésultats complets : {OUT_JSON}")
