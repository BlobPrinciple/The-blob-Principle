#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — RP-LOURD : LE RECOUVREMENT DES FENÊTRES (coexistence × reflection positivity)
# Protocole pré-enregistré. Version 1.0 — 16 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# LA QUESTION TOE : la fenêtre de coexistence (β_co ≈ 1,5, établie [M robuste]) et la
# fenêtre RP (β=4 : violation ~1/N [M-tendance] ; β=0,3 : violation structurelle [M])
# se recouvrent-elles sur l'axe β ?
#   → si la violation RP PURE à β=1,6 (et 2,5) décroît en ~1/N : la fenêtre RP
#     asymptotique descend jusqu'à la coexistence → le sudoku (espace+gravité+quantique
#     dans UN système) est possible à la limite.
#   → si elle est structurelle (plate/croissante) : fenêtres disjointes → architecture
#     multi-échelle requise (cohérente avec la cosmogonie du corpus).
# LEÇONS INTÉGRÉES (payées en session, 2 instruments annulés) :
#   • STATIONNARITÉ STRICTE : snapshots toujours au même β que l'équilibration.
#   • Témoin-dérive en CONTRÔLE POSITIF : l'instrument doit détecter une dérive volontaire.
#   • RÉPÉTABILITÉ mesurée (3 jeux, même état) → σ_rep entre dans le seuil.
#   • Bootstrap PAR BLOCS (autocorrélation) ; seuil = max(3σ_blocs, 3σ_rep).
#   • Base enrichie : K=3 (9 cellules) × 3 features (liens, triangles, tétraèdres
#     strictement internes à la bande) + constante = 28 dimensions, M=100 snapshots.
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback, warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from collections import defaultdict
from itertools import combinations

# ───────────────────────── PARAMÈTRES ─────────────────────────
DENSITY, KAPPA, RCUT, TAU, E_PER_N = 200.0, 10.0, 1.6, 0.5, 5
M_SNAP     = 100          # snapshots par point
SNAP_GAP   = 1            # sweeps entre snapshots (stationnaire)
K_GRID     = 3            # cellules K×K par côté
EQ_SW      = 24           # équilibration phase pure
BIPH_EQ    = 48           # équilibration libre du biphasé (stationnarité G1)
BLOCK      = 10           # taille de bloc bootstrap
OUT_JSON   = "rp_lourd_results.json"

# Plan d'expérience (config, beta, N, seeds)
PURE_SEEDS   = [4101, 4102, 4103]
PURE32_SEEDS = [4101, 4102]
ETAL_SEEDS   = [4101, 4102]
BIPH_SEEDS   = [4101, 4102, 4103]
PLAN = []
for b in (1.6, 2.5):
    for N in (8000, 16000):
        for s in PURE_SEEDS: PLAN.append(("pur", b, N, s))
    for s in PURE32_SEEDS: PLAN.append(("pur", b, 32000, s))
for N in (8000, 16000):
    for s in ETAL_SEEDS: PLAN.append(("pur", 4.0, N, s))
for s in BIPH_SEEDS: PLAN.append(("biphase", 1.6, 16000, s))
PLAN.append(("repeat", 1.6, 8000, 4101))     # répétabilité : 3 jeux, même état
PLAN.append(("derive", 1.6, 8000, 4101))     # contrôle positif : dérive volontaire 4→1,6

BETA = 1.6
GRID = """
════════════════ GRILLE PRÉ-ENREGISTRÉE (gravée AVANT lecture) ════════════════
SEUIL de violation par point : |min-eig| > max(3σ_bootstrap-blocs, 3σ_répétabilité).
PENTES (fit log-log |min-eig| vs N, par β, moyenne des graines) :
  β=4,0 (étalon)  : attendu ≈ −1 (consolidation multi-graines de la tendance 1/N).
  β=1,6 et β=2,5  : LA QUESTION.
    pente ≤ −0,7  → violation de taille finie : fenêtre RP asymptotique atteint ce β.
    pente ≥ −0,3  → violation structurelle : ce β est HORS fenêtre RP.
    entre les deux → zone grise, rapporter tel quel.
VERDICT-RECOUVREMENT :
  β=1,6 décroît           → fenêtres coexistence ∩ RP SE RECOUVRENT → sudoku possible
                            à la limite [M-tendance multi-graines].
  β=1,6 structurel,
  β=2,5 décroît           → frontière RP β* ∈ (1,6 ; 2,5) : recouvrement RATÉ de peu →
                            architecture multi-échelle OU β_co à déplacer.
  les deux structurels    → mur dur ≥ 2,5 : multi-échelle requise. Tel quel.
BIPHASÉ (16k, stationnaire 48 sw) vs PUR 1,6 (16k, mêmes graines) :
  Δ_poche = |min-eig(biph)| − |min-eig(pur)| ; la poche n'ajoute une violation propre
  que si Δ_poche > 3σ_rep. Sinon : toute la violation vient de la PHASE, pas de la matière.
CONTRÔLES : σ_rep rapportée ; le point 'derive' DOIT violer nettement plus que le pur
  stationnaire (détecteur d'artefact fonctionnel), sinon l'instrument est aveugle → tout NUL.
Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────── PIPELINE (container, validé bit-à-bit) ─────────────────
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
        d2_new = self.sum_d2 + (-2*self.deg[u]+1) + (-2*self.deg[v]+1) + (2*self.deg[a]+1) + (2*self.deg[b]+1)
        mu = 2.0 * self.E / self.N
        cv_new = math.sqrt(max(d2_new / self.N - mu * mu, 0.0)) / mu
        return (d_logT - BETA * (cv_new - self.cv())), dT, d2_new
    def do_swap(self, u, v, a, b, dT, d2_new):
        self.adj[u].discard(v); self.adj[v].discard(u)
        self.adj[a].add(b); self.adj[b].add(a)
        self.deg[u] -= 1; self.deg[v] -= 1; self.deg[a] += 1; self.deg[b] += 1
        self.sum_d2 = d2_new; self.T += dT

def relax(st, cand, beta, seed, sw, allowed=None):
    global BETA
    BETA = beta
    N = st.N
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

# ───────────────── FEATURES RP (bande stricte, base enrichie) ─────────────────
def make_bands(pts, L, rc, restrict=None):
    x = pts[:, 0]
    inP = (x > L/2 + rc) & (x < L - rc)
    inM = (x > rc) & (x < L/2 - rc)
    if restrict is not None:
        inP = inP & restrict; inM = inM & restrict
    return inP, inM

def rp_features(st, pts, L, inP, inM, K):
    """[1] + par cellule (y,z) et par côté : liens internes, triangles internes,
    tétraèdres internes — strictement dans la bande du côté considéré."""
    N = st.N
    cy = np.minimum((pts[:, 1] / L * K).astype(int), K - 1)
    cz = np.minimum((pts[:, 2] / L * K).astype(int), K - 1)
    cell = cy * K + cz
    fP = np.zeros((K * K, 3)); fM = np.zeros((K * K, 3))
    nP = np.zeros(K * K); nM = np.zeros(K * K)
    for i in range(N):
        if inP[i]: nP[cell[i]] += 1
        elif inM[i]: nM[cell[i]] += 1
    for side, mask, F in (("P", inP, fP), ("M", inM, fM)):
        nodes = [i for i in range(N) if mask[i]]
        nodeset = set(nodes)
        for u in nodes:
            su = st.adj[u]
            for v in su:
                if v > u and v in nodeset:
                    F[cell[u], 0] += 0.5; F[cell[v], 0] += 0.5
                    common = [w for w in (su & st.adj[v]) if w in nodeset]
                    c = len(common)
                    F[cell[u], 1] += c * 0.5; F[cell[v], 1] += c * 0.5
                    # tétraèdres internes portés par (u,v)
                    for wi in range(c):
                        w = common[wi]
                        if w > v:
                            sw = st.adj[w]
                            for xi in range(wi + 1, c):
                                xx = common[xi]
                                if xx > w and xx in sw:
                                    F[cell[u], 2] += 1.0/6; F[cell[v], 2] += 1.0/6
    fP /= np.maximum(nP[:, None], 1); fM /= np.maximum(nM[:, None], 1)
    return np.concatenate([[1.0], fP.ravel()]), np.concatenate([[1.0], fM.ravel()])

def gram_mineig(P, Q, rng, nboot=200, block=BLOCK):
    G = (P.T @ Q) / len(P); Gs = 0.5 * (G + G.T)
    me = float(np.linalg.eigvalsh(Gs)[0])
    block = min(block, max(2, len(P) // 5))   # garantit >=5 blocs
    nb = len(P) // block
    boots = []
    for _ in range(nboot):
        bi = rng.integers(0, nb, nb)
        idx = np.concatenate([np.arange(b * block, (b + 1) * block) for b in bi])
        Gb = (P[idx].T @ Q[idx]) / len(idx); Gb = 0.5 * (Gb + Gb.T)
        boots.append(np.linalg.eigvalsh(Gb)[0])
    return me, 3 * float(np.std(boots))

# ───────────────── POINT D'EXPÉRIENCE ─────────────────
def run_point(mode, beta, N, seed):
    pts, cand, L, rc = build_geometry(N, seed)
    rng = np.random.default_rng(seed)
    st = BlobState(N, cand, rng.choice(len(cand), size=E_PER_N * N, replace=False))
    restrict = None
    if mode == "pur":
        st = relax(st, cand, beta, seed + 1, EQ_SW)
        sample_beta = beta
    elif mode == "biphase":
        dv = pts - pts.mean(0); dv -= L * np.round(dv / L)
        matter = np.linalg.norm(dv, axis=1) < L * (3 * 0.25 / (4 * math.pi)) ** (1/3)
        sea = ~matter
        st = relax(st, cand, 0.3, seed + 1, 18, allowed=matter)
        st = relax(st, cand, 4.0, seed + 2, 18, allowed=sea)
        st = relax(st, cand, beta, seed + 3, BIPH_EQ)      # stationnarisation longue
        restrict = sea; sample_beta = beta
    elif mode == "derive":
        st = relax(st, cand, 4.0, seed + 1, EQ_SW)          # équilibré à 4…
        sample_beta = 1.6                                    # …échantillonné en DÉRIVE (contrôle positif)
    elif mode == "repeat":
        st = relax(st, cand, beta, seed + 1, EQ_SW)
        sample_beta = beta
    inP, inM = make_bands(pts, L, rc, restrict)
    rngb = np.random.default_rng(seed + 77)
    def one_set(snap_seed):
        nonlocal st
        Ps, Qs = [], []
        for m in range(M_SNAP):
            st = relax(st, cand, sample_beta, snap_seed + m, SNAP_GAP)
            a, b = rp_features(st, pts, L, inP, inM, K_GRID)
            Ps.append(a); Qs.append(b)
        return gram_mineig(np.array(Ps), np.array(Qs), rngb)
    if mode == "repeat":
        out = [one_set(seed + 1000 + 500 * k) for k in range(3)]
        return {"sets": [{"mineig": m, "tol": t} for m, t in out]}
    me, tol = one_set(seed + 1000)
    return {"mineig": me, "tol": tol}

# ───────────────── MAIN ─────────────────
if __name__ == "__main__":
    print(GRID)
    print(f"Environnement : python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"M={M_SNAP} snapshots (gap {SNAP_GAP} sw), base K={K_GRID} (D={1+3*K_GRID*K_GRID}), "
          f"{len(PLAN)} points. Estimation ~2,5-3,5 h.\n")
    all_res = []
    t0 = time.time()
    for (mode, beta, N, seed) in PLAN:
        t1 = time.time()
        try:
            r = run_point(mode, beta, N, seed)
            rec = {"mode": mode, "beta": beta, "N": N, "seed": seed, **r}
            all_res.append(rec)
            if mode == "repeat":
                vals = [s["mineig"] for s in r["sets"]]
                print(f"[{mode} β={beta} N={N} s={seed}] jeux={['%+.2f'%v for v in vals]} σ_rep={np.std(vals):.2f} ({(time.time()-t1)/60:.1f} min)", flush=True)
            else:
                print(f"[{mode} β={beta} N={N} s={seed}] min-eig={r['mineig']:+.3f} tol={r['tol']:.3f} ({(time.time()-t1)/60:.1f} min)", flush=True)
        except Exception as ex:
            print(f"[{mode} β={beta} N={N} s={seed}] ÉCHEC: {ex}", flush=True); traceback.print_exc()
            all_res.append({"mode": mode, "beta": beta, "N": N, "seed": seed, "error": str(ex)})
        with open(OUT_JSON, "w") as f:
            json.dump(all_res, f)
    # ─── SYNTHÈSE AUTOMATIQUE ───
    ok = [r for r in all_res if "mineig" in r or "sets" in r]
    print(f"\n════════ SYNTHÈSE ({(time.time()-t0)/60:.0f} min) ════════")
    rep = next((r for r in ok if r["mode"] == "repeat"), None)
    sigrep = np.std([s["mineig"] for s in rep["sets"]]) if rep else 1.12
    print(f"σ_répétabilité = {sigrep:.2f} → seuil violation = max(3σ_blocs, {3*sigrep:.1f})")
    der = next((r for r in ok if r["mode"] == "derive"), None)
    purs16_8k = [r for r in ok if r["mode"] == "pur" and r["beta"] == 1.6 and r["N"] == 8000]
    if der and purs16_8k:
        ref = np.mean([abs(r["mineig"]) for r in purs16_8k])
        print(f"Contrôle positif dérive : |{abs(der['mineig']):.1f}| vs pur stationnaire {ref:.1f} → "
              f"{'détecteur fonctionnel ✓' if abs(der['mineig'])>2*ref else 'DÉTECTEUR AVEUGLE ✗ — tout NUL'}")
    for b in (1.6, 2.5, 4.0):
        pts_b = [r for r in ok if r["mode"] == "pur" and r["beta"] == b]
        if not pts_b: continue
        Ns = sorted(set(r["N"] for r in pts_b))
        means = [np.mean([abs(r["mineig"]) for r in pts_b if r["N"] == n]) for n in Ns]
        if len(Ns) >= 2:
            slope = np.polyfit(np.log(Ns), np.log(np.maximum(means, 1e-6)), 1)[0]
            verdict = ("TAILLE FINIE (fenêtre RP atteint ce β)" if slope <= -0.7 else
                       ("STRUCTUREL (hors fenêtre RP)" if slope >= -0.3 else "zone grise"))
            print(f"β={b} : |min-eig| par N {dict(zip(Ns, [round(m,3) for m in means]))} → pente {slope:.2f} → {verdict}")
    # recouvrement
    def slope_of(b):
        pts_b = [r for r in ok if r["mode"] == "pur" and r["beta"] == b]
        Ns = sorted(set(r["N"] for r in pts_b))
        if len(Ns) < 2: return None
        means = [np.mean([abs(r["mineig"]) for r in pts_b if r["N"] == n]) for n in Ns]
        return np.polyfit(np.log(Ns), np.log(np.maximum(means, 1e-6)), 1)[0]
    s16, s25 = slope_of(1.6), slope_of(2.5)
    print()
    if s16 is not None and s16 <= -0.7:
        print("→ ★★★ RECOUVREMENT : la fenêtre RP asymptotique atteint β_co. Le sudoku (espace +")
        print("   gravité + quantique dans UN système) est possible à la limite [M-tendance multi-graines].")
    elif s16 is not None and s25 is not None and s25 <= -0.7:
        print("→ frontière RP β* ∈ (1,6 ; 2,5) : recouvrement raté de peu — multi-échelle ou β_co à déplacer.")
    elif s16 is not None and s25 is not None:
        print("→ mur dur ≥ 2,5 : fenêtres disjointes, architecture multi-échelle requise. Tel quel.")
    biph = [r for r in ok if r["mode"] == "biphase"]
    pur16k = [r for r in ok if r["mode"] == "pur" and r["beta"] == 1.6 and r["N"] == 16000]
    if biph and pur16k:
        d = np.mean([abs(r["mineig"]) for r in biph]) - np.mean([abs(r["mineig"]) for r in pur16k])
        print(f"Δ_poche (biphasé − pur, 16k) = {d:+.2f} → "
              f"{'la POCHE ajoute une violation propre' if d>3*sigrep else 'toute la violation vient de la PHASE (matière innocente)'}")
    print(f"\nRésultats complets : {OUT_JSON}")
