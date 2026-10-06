#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — CONSOLIDATION DU BLOC MÉMOIRE (6 graines, N=6000)
# Protocole pré-enregistré. Version 1.0 — 15 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# Ce run transforme en résultat de corpus les 8 [M] du bloc mémoire, obtenus
# en exploration container (2 graines, N≤4000). Quatre modules, tous à grille
# gravée, tous avec témoins/z-scores intégrés :
#   M1 — HYSTÉRÉSIS 1er ORDRE à 3 vitesses : aire A(v) + barres d'erreur.
#        (établit : thermodynamique si A plafonne ; ratio A_lent/A_rapide.)
#   M2 — PATH-DEPENDENCE : 3 chemins → même (β=1,5). Séparation scalaire vs intra ;
#        Jaccard des hubs (géographie).
#   M3 — GARDE DE VIABILITÉ appariée : perturbation + témoin de dérive, 2 phases.
#        (Δ = S_perturbé − S_témoin ; symétrique auto-cicatrisant vs condensé cicatrice.)
#   M4 — CARTE DES ÉTAGES : z-hystérésis par dim (0→3) → mémoriel/amnésique/invariant.
# Résultats attendus (déposés) : hystérésis thermo (ratio > 0,6) ; états distincts
# (sep > 3× intra) ; garde asymétrique (Δ_sym ≈ 0 > Δ_cond) ; mémoire = combinatoire
# (CV/T/N/n_tet mémoriels), métrique amnésique (⟨A△⟩, ⟨V_K4⟩ z<3), ⟨ℓ⟩ quasi-gelé.
# Pipeline (build_geometry/BlobState/equilibrate) : identique au container validé.
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback
from collections import defaultdict
from itertools import combinations

# ───────────────────────── PARAMÈTRES ─────────────────────────
N          = 6000
SEEDS      = [7001, 7002, 7003, 7004, 7005, 7006]   # 6 graines fraîches
DENSITY    = 200.0
KAPPA      = 10.0
RCUT       = 1.6
TAU        = 0.5
E_PER_N    = 5
OUT_JSON   = "memoire_consol_results.json"

UP   = [0.3, 1.0, 1.5, 2.0, 2.5, 3.0]
DOWN = [2.5, 2.0, 1.5, 1.0, 0.3]
MIDS = [1.0, 1.5, 2.0, 2.5]
SPEEDS = [(5, "rapide"), (12, "moyen"), (25, "lent")]
INIT_SW = 25
PERTURB_NSWAP = int(0.04 * E_PER_N * N)   # ≈ 4 % des arêtes
BETA = 0.3

GRID = """
════════════════ GRILLES PRÉ-ENREGISTRÉES (gravées AVANT lecture) ════════════════
M1 HYSTÉRÉSIS : A(v) = Σ_mids |f_nv↑−f_nv↓|. Thermodynamique si A_lent/A_rapide > 0,6
   (plateau) ; cinétique si < 0,3. Barres = écart-type sur 6 graines.
M2 PATH-DEP : 3 chemins (direct/montée/descente) → β=1,5. États distincts si
   |f_nv(montée)−f_nv(descente)| > 3×(écart intra-graine). Jaccard hubs : géographie.
M3 GARDE : Δ = S(perturbé+relax) − S(témoin relax), par phase. Garde parfaite |Δ|<0,01 ;
   cicatrice Δ<−0,01. Prédiction : Δ_sym > Δ_cond (symétrique garde mieux).
M4 ÉTAGES : z(obs) = ⟨|↑−↓|⟩_mids / σ_intra. Mémoriel z>3 & amp≥6% ; amnésique z<3 &
   amp≥6% ; invariant amp<6%. Attendu : combinatoire mémorielle, métrique amnésique.
Tout écart se lit tel quel. Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────── PIPELINE (identique container) ─────────────────
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

def equilibrate(st, cand, beta, seed, sw):
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
            dS, dT, d2n = st.dS_swap(u, v, a, b)
            if dS >= 0 or rng.random() < math.exp(dS / te):
                st.do_swap(u, v, a, b, dT, d2n); el[io] = (a, b)
    return st

def perturb(st, cand, n, seed):
    rng = np.random.default_rng(seed)
    el = [(i, j) for i in range(N) for j in st.adj[i] if j > i]
    done = 0; tries = 0
    while done < n and tries < 20 * n:
        tries += 1
        io = rng.integers(len(el)); u, v = el[io]
        ii = rng.integers(len(cand)); a, b = cand[ii]
        if b in st.adj[a] or v not in st.adj[u]: continue
        if len({u, v, a, b}) < 4: continue
        if st.deg[u] <= 2 or st.deg[v] <= 2: continue
        dS, dT, d2n = st.dS_swap(u, v, a, b)
        st.do_swap(u, v, a, b, dT, d2n); el[io] = (a, b); done += 1
    return st

def clone(st, cand):
    return BlobState(cand, [k for k, (a, b) in enumerate(cand) if b in st.adj[a]])

# ───────────────── MESURES ─────────────────
def tets_tris(st):
    tris = set()
    for u in st.adj:
        for v in st.adj[u]:
            if v > u:
                for w in st.adj[u] & st.adj[v]:
                    if w > v: tris.add((u, v, w))
    tets = []; e2m = defaultdict(int)
    for (u, v, w) in tris:
        for x in st.adj[u] & st.adj[v] & st.adj[w]:
            if x > w:
                tets.append((u, v, w, x))
                for e in combinations((u, v, w, x), 2): e2m[tuple(sorted(e))] += 1
    return tris, tets, e2m

def f_nv_of(st):
    _, _, e2m = tets_tris(st)
    ms = [m for m in e2m.values() if m >= 2]
    return float(sum(1 for m in ms if m > 10)) / st.E if ms else 0.0

def hubs(st, frac=0.05):
    return set(np.argsort(-st.deg)[:int(frac * N)].tolist())

def jac(a, b): return len(a & b) / max(len(a | b), 1)
def S_of(st, beta): return math.log(1 + st.T) - beta * st.cv()

def full_obs(st, pts, L, seed):
    tris, tets, _ = tets_tris(st)
    el = np.array([(i, j) for i in range(N) for j in st.adj[i] if j > i])
    d = pts[el[:, 0]] - pts[el[:, 1]]; d -= L * np.round(d / L)
    o = {"CV": st.cv(), "TN": st.T / N, "ntet": len(tets) / N,
         "ell": float(np.linalg.norm(d, axis=1).mean())}
    rng = np.random.default_rng(seed)
    tl = list(tris)
    if tl:
        s = [tl[i] for i in rng.choice(len(tl), size=min(400, len(tl)), replace=False)]
        ar = []
        for (a, b, c) in s:
            ab = pts[b] - pts[a]; ab -= L * np.round(ab / L)
            ac = pts[c] - pts[a]; ac -= L * np.round(ac / L)
            ar.append(0.5 * np.linalg.norm(np.cross(ab, ac)))
        o["A3"] = float(np.mean(ar))
    else: o["A3"] = float("nan")
    if tets:
        s = [tets[i] for i in rng.choice(len(tets), size=min(400, len(tets)), replace=False)]
        vs = []
        for (a, b, c, dd) in s:
            ab = pts[b] - pts[a]; ab -= L * np.round(ab / L)
            ac = pts[c] - pts[a]; ac -= L * np.round(ac / L)
            ad = pts[dd] - pts[a]; ad -= L * np.round(ad / L)
            vs.append(abs(np.dot(ab, np.cross(ac, ad))) / 6.0)
        o["VK4"] = float(np.mean(vs))
    else: o["VK4"] = float("nan")
    return o

OBSK = ("CV", "TN", "ntet", "ell", "A3", "VK4")

# ───────────────── MODULES PAR GRAINE ─────────────────
def module_hysteresis(cand, pts, L, seed):
    """M1 : aire à 3 vitesses."""
    out = {}
    for sw, label in SPEEDS:
        st = BlobState(cand, np.random.default_rng(seed).choice(len(cand), size=E_PER_N*N, replace=False))
        st = equilibrate(st, cand, 0.3, seed + 1, max(INIT_SW, sw))
        upd = {}
        for i, b in enumerate(UP):
            st = equilibrate(st, cand, b, seed + 100 + i, sw); upd[b] = f_nv_of(st)
        dnd = {}
        for i, b in enumerate(DOWN):
            st = equilibrate(st, cand, b, seed + 200 + i, sw); dnd[b] = f_nv_of(st)
        A = sum(abs(dnd[b] - upd[b]) for b in MIDS if b in upd and b in dnd)  # mids présents
        out[label] = {"A": A, "up": upd, "down": dnd}
    return out

def module_path(cand, pts, L, seed):
    """M2 : 3 chemins → β=1,5, scalaires + hubs."""
    def path_A(r):
        st = BlobState(cand, np.random.default_rng(r).choice(len(cand), size=E_PER_N*N, replace=False))
        return equilibrate(st, cand, 1.5, r + 1, 25)
    def path_B(r):
        st = BlobState(cand, np.random.default_rng(r).choice(len(cand), size=E_PER_N*N, replace=False))
        st = equilibrate(st, cand, 0.3, r + 1, 25); st = equilibrate(st, cand, 1.0, r + 2, 8)
        return equilibrate(st, cand, 1.5, r + 3, 8)
    def path_C(r):
        st = BlobState(cand, np.random.default_rng(r).choice(len(cand), size=E_PER_N*N, replace=False))
        st = equilibrate(st, cand, 3.0, r + 1, 25); st = equilibrate(st, cand, 2.5, r + 2, 8)
        st = equilibrate(st, cand, 2.0, r + 3, 8); return equilibrate(st, cand, 1.5, r + 4, 8)
    o = {}
    for name, fn in (("A", path_A), ("B", path_B), ("C", path_C)):
        st = fn(seed)
        o[name] = {"f_nv": f_nv_of(st), "CV": st.cv(), "TN": st.T / N, "hubs": sorted(hubs(st))}
    return o

def module_guard(cand, pts, L, seed):
    """M3 : garde appariée avec témoin de dérive, 2 phases."""
    o = {}
    for beta, label in ((0.3, "condense"), (3.0, "symetrique")):
        st = BlobState(cand, np.random.default_rng(seed).choice(len(cand), size=E_PER_N*N, replace=False))
        st = equilibrate(st, cand, beta, seed + 1, 25)
        st_T = clone(st, cand); st_P = clone(st, cand)
        st_P = perturb(st_P, cand, PERTURB_NSWAP, seed + 2)
        st_P = equilibrate(st_P, cand, beta, seed + 3, 10)
        st_T = equilibrate(st_T, cand, beta, seed + 3, 10)
        o[label] = {"delta": S_of(st_P, beta) - S_of(st_T, beta),
                    "S_eq": S_of(st, beta)}
    return o

def module_floors(cand, pts, L, seed):
    """M4 : z-hystérésis par étage, 3 snapshots/palier."""
    st = BlobState(cand, np.random.default_rng(seed).choice(len(cand), size=E_PER_N*N, replace=False))
    st = equilibrate(st, cand, 0.3, seed + 1, INIT_SW)
    up = {}; down = {}; sig = defaultdict(list); allv = defaultdict(list)
    def palier(st, b, sd):
        st = equilibrate(st, cand, b, sd, 8)
        snaps = [full_obs(st, pts, L, sd + 1)]
        st = equilibrate(st, cand, b, sd + 2, 2); snaps.append(full_obs(st, pts, L, sd + 3))
        st = equilibrate(st, cand, b, sd + 4, 2); snaps.append(full_obs(st, pts, L, sd + 5))
        m = {}
        for k in OBSK:
            vals = [o[k] for o in snaps]
            m[k] = float(np.mean(vals)); sig[k].append(float(np.std(vals))); allv[k].append(m[k])
        return st, m
    for i, b in enumerate(UP):
        st, m = palier(st, b, seed + 100 + 7 * i); up[b] = m
    for i, b in enumerate(DOWN):
        st, m = palier(st, b, seed + 400 + 7 * i); down[b] = m
    o = {}
    mids = [b for b in MIDS if b in up and b in down]
    for k in OBSK:
        sep = float(np.mean([abs(up[b][k] - down[b][k]) for b in mids]))
        s = math.sqrt(np.mean(np.array(sig[k]) ** 2))
        amp = (max(allv[k]) - min(allv[k])) / max(abs(np.mean(allv[k])), 1e-12)
        o[k] = {"z": sep / max(s, 1e-12), "amp": amp}
    return o

# ───────────────── MAIN ─────────────────
if __name__ == "__main__":
    print(GRID)
    print(f"Environnement : python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"N={N}, graines {SEEDS}, τ={TAU}, |E|={E_PER_N}N. 4 modules × {len(SEEDS)} graines.\n")
    all_res = []
    t0 = time.time()
    for seed in SEEDS:
        print(f"[seed {seed}]", flush=True)
        try:
            pts, cand, L, rc = build_geometry(seed)
            r = {"seed": seed}
            t1 = time.time()
            r["M1"] = module_hysteresis(cand, pts, L, seed)
            print(f"  M1 hystérésis : A_rapide={r['M1']['rapide']['A']:.3f} A_lent={r['M1']['lent']['A']:.3f} ({time.time()-t1:.0f}s)", flush=True)
            r["M2"] = module_path(cand, pts, L, seed)
            sep = abs(r["M2"]["B"]["f_nv"] - r["M2"]["C"]["f_nv"])
            print(f"  M2 path : f_nv B={r['M2']['B']['f_nv']:.3f} C={r['M2']['C']['f_nv']:.3f} sep={sep:.3f} ({time.time()-t1:.0f}s)", flush=True)
            r["M3"] = module_guard(cand, pts, L, seed)
            print(f"  M3 garde : Δ_cond={r['M3']['condense']['delta']:+.4f} Δ_sym={r['M3']['symetrique']['delta']:+.4f} ({time.time()-t1:.0f}s)", flush=True)
            r["M4"] = module_floors(cand, pts, L, seed)
            print(f"  M4 étages : z(TN)={r['M4']['TN']['z']:.1f} z(A3)={r['M4']['A3']['z']:.1f} z(VK4)={r['M4']['VK4']['z']:.1f} ({time.time()-t1:.0f}s)", flush=True)
            all_res.append(r)
        except Exception as ex:
            print(f"  ✗ échec : {ex}", flush=True); traceback.print_exc()
            all_res.append({"seed": seed, "error": str(ex)})
        with open(OUT_JSON, "w") as f:
            json.dump(all_res, f)
    # ─── SYNTHÈSE ───
    ok = [r for r in all_res if "M1" in r]
    print(f"\n════════ SYNTHÈSE ({(time.time()-t0)/60:.0f} min, {len(ok)}/{len(SEEDS)} graines) ════════")
    if not ok:
        print("Aucune graine exploitable."); sys.exit(0)
    def arr(f): return np.array([f(r) for r in ok])
    Ar = arr(lambda r: r["M1"]["rapide"]["A"]); Al = arr(lambda r: r["M1"]["lent"]["A"])
    print(f"M1 : A_rapide={Ar.mean():.3f}±{Ar.std():.3f}  A_lent={Al.mean():.3f}±{Al.std():.3f}  ratio={Al.mean()/max(Ar.mean(),1e-9):.2f}  "
          f"→ {'THERMODYNAMIQUE (1er ordre)' if Al.mean()/max(Ar.mean(),1e-9)>0.6 else ('cinétique' if Al.mean()/max(Ar.mean(),1e-9)<0.3 else 'intermédiaire')}")
    sep = arr(lambda r: abs(r["M2"]["B"]["f_nv"] - r["M2"]["C"]["f_nv"]))
    intra = arr(lambda r: abs(r["M2"]["B"]["f_nv"] - r["M2"]["A"]["f_nv"])).std() + 1e-9
    jbc = arr(lambda r: jac(set(r["M2"]["B"]["hubs"]), set(r["M2"]["C"]["hubs"])))
    print(f"M2 : sep(B,C)={sep.mean():.3f}±{sep.std():.3f}  (intra≈{intra:.3f}) → {'ÉTATS DISTINCTS' if sep.mean()>3*intra else 'non distincts'} ; Jaccard hubs B↔C={jbc.mean():.3f}")
    dc = arr(lambda r: r["M3"]["condense"]["delta"]); dsy = arr(lambda r: r["M3"]["symetrique"]["delta"])
    print(f"M3 : Δ_condensé={dc.mean():+.4f}±{dc.std():.4f}  Δ_symétrique={dsy.mean():+.4f}±{dsy.std():.4f}  "
          f"→ {'symétrique GARDE MIEUX (auto-cicatrisant)' if dsy.mean()>dc.mean()+0.005 else 'garde comparable'}")
    print(f"M4 (carte des étages, z & amplitude moyens) :")
    names = {"CV": "dim0", "TN": "dim2", "ntet": "dim3", "ell": "dim1", "A3": "dim2", "VK4": "dim3"}
    for k in OBSK:
        z = arr(lambda r: r["M4"][k]["z"]); a = arr(lambda r: r["M4"][k]["amp"])
        cl = "INVARIANT" if a.mean() < 0.06 else ("MÉMORIEL" if z.min() > 3 else "AMNÉSIQUE")
        print(f"   {k:>5} ({names[k]}) : z={z.mean():.1f}±{z.std():.1f}  amp={100*a.mean():.0f}%  → {cl}")
    print(f"\nRésultats complets : {OUT_JSON}")
