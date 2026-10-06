#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — GRAVITÉ GRAND-N : caractérisation de la loi de saturation
# Protocole pré-enregistré. Version 1.0 — 13 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# CE QUE CE SCRIPT CORRIGE PAR RAPPORT AUX RUNS DE SESSION (conteneur) :
#  (1) ACTION COMPLÈTE : S = log(1+T) − β·CV(deg). Les équilibrages de session
#      omettaient le terme β·CV (simplification signalée). Ici il est inclus,
#      avec mise à jour O(1) de CV par swap.
#  (2) CONSERVATION |E| GARANTIE PAR ASSERTION après chaque phase (le bug
#      d'emballement « trou noir » identifié par R. est structurellement
#      impossible ici : l'injection se fait PAR TRANSFERT, |E| constant).
#  (3) GRILLE PRÉ-ENREGISTRÉE imprimée AVANT tout résultat. Aucun curseur ne
#      bouge après lecture.
#  (4) Banque de graines fixe, JSON par graine, log stdout, environnement doc.
# CONVENTION DYNAMIQUE : Metropolis maximisant S à température τ/N (convention
# observée de toutes les sessions ; à confirmer au corpus canonique — si la
# convention canonique est exp(−S/τe), inverser le signe de dS dans accept()).
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys
from collections import defaultdict
from itertools import combinations

# ───────────────────────── PARAMÈTRES ─────────────────────────
N            = 2000        # taille (2000 conseillé CPU ; 5000 si temps)
SUBSTRATES   = 20          # substrats indépendants (≥20 pour la grille C/D)
SEED_BANK    = list(range(1000, 1000 + SUBSTRATES))
DENSITY      = 200.0
KAPPA        = 10.0
RCUT         = 1.6
BETA         = 0.30
TAU          = 0.5
E_PER_N      = 5           # |E| = 5N (fixé, conservé)
SWEEPS_EQ    = 30          # équilibrage
M_INJECT     = 60          # arêtes TRANSFÉRÉES (injection à |E| constant)
FRAC_COMPACT = 0.03        # région compacte : fraction de sommets (≥40) — rayon auto-calculé
FRAC_DIFFUSE = 0.40        # région diffuse  : fraction de sommets (≥200) — rayon auto-calculé
ASSIM_SWEEPS = 6           # sweeps d'assimilation post-injection (|E| const)
EDGE_SAMPLE  = 5000        # max d'arêtes échantillonnées pour les déficits
OUT_JSON     = "gravite_grandN_results.json"

GRID = """
════════════════ GRILLE PRÉ-ENREGISTRÉE (gravée AVANT lecture) ════════════════
A. COUPLAGE courbure-densité : corrélation r entre |déficit de Regge| par arête
   et densité indépendante (deg(a)+deg(b)), équilibré vs aléatoire.
   → SIGNAL CONFIRMÉ si |r_eq − r_rand| ≥ 4σ sur ≥ 20 substrats.
B. FORME de la loi δ(m) (m = multiplicité tétraédrique de l'arête) :
   ajuster LINÉAIRE δ=a+b·m  vs  SATURATION δ=a−b·exp(−c·m).
   → « Einstein-linéaire » si R²_lin>0.7 ET pente stable (σ/|moy|<25%) ET
     ΔAIC(sat−lin) < 10.
   → « Saturation (Regge/ADJ, conforme T-V275-6) » si ΔAIC(lin−sat) > 10.
   → sinon « indéterminé ». La saturation N'EST PAS une loi nouvelle (Regge 1961).
C. EFFET DE STRUCTURE (étoile à neutrons vs planète gazeuse) : réponse en
   courbure à M_INJECT arêtes transférées, COMPACT (≈3% des sommets) vs DIFFUS
   (≈40%) — rayons auto-calculés et enregistrés. Mesure IMMÉDIATE.
   → significatif si écart > 2σ sur ≥ 20 essais.
D. ASSIMILATION (hypothèse R.) : l'effet C survit-il à ASSIM_SWEEPS de
   ré-équilibrage à |E| STRICTEMENT constant ? → survie si > 2σ APRÈS.
E. PRÉDICTION CV (champ moyen 13/07) : Var(deg)/Var(neutre) ∈ [0.96, 0.995]
   (décalage −0.5% à −4% ; valeur centrale prédite ≈ −1.5%).
Tout écart à la grille se lit tel quel. Aucune réinterprétation post hoc.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────────────── GÉOMÉTRIE ─────────────────────────
def build_geometry(seed):
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

# ─────────────────── ACTION COMPLÈTE, O(1) par swap ───────────────────
class BlobState:
    """État : adjacence + T (triangles) + Σdeg² pour CV en O(1). |E| invariant."""
    def __init__(self, cand, active_idx):
        self.cand = cand
        self.adj = defaultdict(set)
        self.active = set(active_idx)
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
        """ΔS pour retirer (u,v), ajouter (a,b). Ne modifie rien."""
        t_rm = len(self.adj[u] & self.adj[v])
        # simuler retrait pour compter les triangles créés par (a,b) SANS (u,v)
        self.adj[u].discard(v); self.adj[v].discard(u)
        t_add = len(self.adj[a] & self.adj[b])
        self.adj[u].add(v); self.adj[v].add(u)
        dT = t_add - t_rm
        d_logT = math.log(1 + self.T + dT) - math.log(1 + self.T)
        # ΔCV via Σd² (μ constant car |E| constant)
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
        assert e_now == self.E == E_PER_N * N, \
            f"|E| VIOLÉ [{tag}]: {e_now} vs {self.E} vs {E_PER_N*N}"

def equilibrate(state, cand, rng, sweeps):
    te = TAU / N
    pool = np.array(cand)
    edge_list = [(i, j) for i in range(N) for j in state.adj[i] if j > i]
    for sw in range(sweeps):
        for _ in range(3 * N):
            io = rng.integers(len(edge_list)); u, v = edge_list[io]
            ii = rng.integers(len(pool)); a, b = int(pool[ii, 0]), int(pool[ii, 1])
            if b in state.adj[a] or v not in state.adj[u]: continue
            if len({u, v, a, b}) < 4: continue   # garde: MAJ O(1) de Σd² exacte
            if state.deg[u] <= 2 or state.deg[v] <= 2: continue
            dS, dT, d2n = state.dS_swap(u, v, a, b)
            if dS >= 0 or rng.random() < math.exp(dS / te):
                state.do_swap(u, v, a, b, dT, d2n)
                edge_list[io] = (a, b)
        state.assert_E(f"eq_sweep_{sw}")
    return state

# ─────────────────── COURBURE DE REGGE (déficits) ───────────────────
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

def regge_deficits(state, pts, L, rng, region_mask=None):
    """Retourne listes (|δ|, m, k) par arête ; option région (centre)."""
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
    edges = [e for e, ts in e2t.items() if len(ts) >= 2]
    if region_mask is not None:
        edges = [e for e in edges if region_mask(e)]
    if len(edges) > EDGE_SAMPLE:
        idx = rng.choice(len(edges), size=EDGE_SAMPLE, replace=False)
        edges = [edges[i] for i in idx]
    out = []
    for e in edges:
        ts = e2t[e]
        d = 2 * math.pi - sum(dihedral(pts, L, t, e) for t in ts)
        out.append((abs(d), len(ts), int(state.deg[e[0]] + state.deg[e[1]])))
    return out

# ─────────────── INJECTION PAR TRANSFERT (|E| CONSTANT) ───────────────
def inject_transfer(state, cand, pts, L, center, radius, M, rng):
    """Active M arêtes candidates DANS la région, désactive M actives HORS
    région. |E| strictement conservé, asserté."""
    def in_region(i):
        d = pts[i] - center; d -= L * np.round(d / L)
        return np.linalg.norm(d) < radius
    reg = np.array([in_region(i) for i in range(N)])
    cand_in = [k for k, (a, b) in enumerate(cand)
               if reg[a] and reg[b] and (b not in state.adj[a])]
    act_out = [(i, j) for i in range(N) for j in state.adj[i]
               if j > i and not reg[i] and not reg[j]]
    M_eff = min(M, len(cand_in), len(act_out))
    assert M_eff >= 0.8 * M, f"Région trop petite: {M_eff}/{M} transferts possibles"
    rng.shuffle(cand_in); rng.shuffle(act_out)
    E_before = state.E
    for k in range(M_eff):
        a, b = cand[cand_in[k]]
        u, v = act_out[k]
        # activer (a,b), désactiver (u,v) — mise à jour complète de l'état
        t_rm = len(state.adj[u] & state.adj[v])
        state.adj[u].discard(v); state.adj[v].discard(u)
        t_add = len(state.adj[a] & state.adj[b])
        state.adj[a].add(b); state.adj[b].add(a)
        state.T += (t_add - t_rm)
        state.sum_d2 += (-2*state.deg[u]+1)+(-2*state.deg[v]+1)+(2*state.deg[a]+1)+(2*state.deg[b]+1)
        state.deg[u] -= 1; state.deg[v] -= 1; state.deg[a] += 1; state.deg[b] += 1
    state.assert_E("post_transfer")
    assert state.E == E_before
    return M_eff, reg

# ───────────────────────── PIPELINE PAR GRAINE ─────────────────────────
def run_seed(seed):
    rng = np.random.default_rng(seed)
    pts, cand, L, rc = build_geometry(seed)
    E0 = E_PER_N * N
    assert len(cand) > E0, "Pas assez d'arêtes candidates"
    res = {"seed": seed, "N": N, "M_cand": len(cand)}

    # ÉQUILIBRÉ (action complète)
    init = rng.choice(len(cand), size=E0, replace=False)
    st = BlobState(cand, init); st.assert_E("init")
    st = equilibrate(st, cand, rng, SWEEPS_EQ)
    res["T_eq"] = st.T; res["CV_eq"] = st.cv()
    res["Var_deg_eq"] = float(st.deg.var())

    # ALÉATOIRE (contrôle : même géométrie, pas d'équilibrage)
    init_r = np.random.default_rng(seed + 77).choice(len(cand), size=E0, replace=False)
    st_r = BlobState(cand, init_r); st_r.assert_E("rand")
    res["Var_deg_neutre"] = float(st_r.deg.var())

    # A/B : déficits (|δ|, m, k) équilibré et aléatoire
    D_eq = regge_deficits(st, pts, L, rng)
    D_rd = regge_deficits(st_r, pts, L, rng)
    def corr(D, idx):
        x = np.array([d[idx] for d in D], float); y = np.array([d[0] for d in D])
        if len(x) < 30 or x.std() == 0: return float("nan")
        return float(np.corrcoef(x, y)[0, 1])
    res["r_eq_k"]  = corr(D_eq, 2)   # couplage densité indépendante
    res["r_rand_k"] = corr(D_rd, 2)
    res["delta_m_eq"] = [[d[0], d[1]] for d in D_eq]   # pour fit lin vs sat (agrégé)

    # C/D : compact vs diffus, immédiat puis assimilation à |E| constant
    center = pts.mean(0)
    out_cd = {}
    n_comp = max(40, int(FRAC_COMPACT * N)); n_diff = max(200, int(FRAC_DIFFUSE * N))
    for label, n_target in (("compact", n_comp), ("diffus", n_diff)):
        R_abs = L * (3 * n_target / (4 * math.pi * N)) ** (1/3)  # rayon contenant ~n_target sommets
        # copie profonde de l'état équilibré
        st2 = BlobState(cand, [k for k, (a, b) in enumerate(cand) if b in st.adj[a]])
        st2.assert_E(f"copy_{label}")
        def region_mask(e):
            for i in e:
                d = pts[i] - center; d -= L * np.round(d / L)
                if np.linalg.norm(d) >= R_abs: return False
            return True
        d0 = sum(x[0] for x in regge_deficits(st2, pts, L, rng, region_mask))
        M_eff, reg = inject_transfer(st2, cand, pts, L, center, R_abs, M_INJECT, rng)
        d1 = sum(x[0] for x in regge_deficits(st2, pts, L, rng, region_mask))
        # assimilation à |E| constant (la dynamique restructure)
        st2 = equilibrate(st2, cand, np.random.default_rng(seed + 5), ASSIM_SWEEPS)
        d2 = sum(x[0] for x in regge_deficits(st2, pts, L, rng, region_mask))
        out_cd[label] = {"M_eff": int(M_eff),
                         "n_target": int(n_target),
                         "R_over_L": float(R_abs / L),
                         "resp_immediate": (d1 - d0) / max(M_eff, 1),
                         "resp_assimile":  (d2 - d0) / max(M_eff, 1)}
    res["injection"] = out_cd
    return res

# ───────────────────────── MAIN ─────────────────────────
if __name__ == "__main__":
    print(GRID)
    print(f"Environnement: python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"N={N}, substrats={SUBSTRATES}, β={BETA}, τ={TAU}, |E|={E_PER_N}N (asserté)")
    print(f"Banque de graines: {SEED_BANK}\n")
    all_res = []
    t0 = time.time()
    for i, seed in enumerate(SEED_BANK):
        t1 = time.time()
        r = run_seed(seed)
        all_res.append(r)
        with open(OUT_JSON, "w") as f:
            json.dump(all_res, f)          # sauvegarde graine par graine
        print(f"[{i+1}/{SUBSTRATES}] seed={seed}  T={r['T_eq']}  "
              f"r_eq={r['r_eq_k']:.3f} r_rand={r['r_rand_k']:.3f}  "
              f"C:imm {r['injection']['compact']['resp_immediate']:+.2f} vs "
              f"{r['injection']['diffus']['resp_immediate']:+.2f}  "
              f"({time.time()-t1:.0f}s)")
    # ─── LECTURE SELON LA GRILLE (automatique, sans curseur) ───
    req = np.array([r["r_eq_k"] for r in all_res])
    rrd = np.array([r["r_rand_k"] for r in all_res])
    gap = req.mean() - rrd.mean()
    sd = math.sqrt(req.var()/len(req) + rrd.var()/len(rrd))
    print(f"\nA. couplage: r_eq={req.mean():.3f}±{req.std():.3f} vs "
          f"r_rand={rrd.mean():.3f}±{rrd.std():.3f} → écart {abs(gap)/max(sd,1e-9):.1f}σ "
          f"[confirmé si ≥4σ]")
    ci = np.array([r["injection"]["compact"]["resp_immediate"] for r in all_res])
    di = np.array([r["injection"]["diffus"]["resp_immediate"]  for r in all_res])
    dd = ci - di; tC = dd.mean()/ (dd.std()/math.sqrt(len(dd)) + 1e-12)
    print(f"C. structure (immédiat): compact−diffus = {dd.mean():+.3f} ({tC:.1f}σ) "
          f"[significatif si >2σ]")
    ca = np.array([r["injection"]["compact"]["resp_assimile"] for r in all_res])
    da = np.array([r["injection"]["diffus"]["resp_assimile"]  for r in all_res])
    dda = ca - da; tD = dda.mean()/(dda.std()/math.sqrt(len(dda)) + 1e-12)
    print(f"D. assimilation: compact−diffus APRÈS = {dda.mean():+.3f} ({tD:.1f}σ) "
          f"[hypothèse R. soutenue si >2σ]")
    veq = np.array([r["Var_deg_eq"] for r in all_res])
    vne = np.array([r["Var_deg_neutre"] for r in all_res])
    print(f"E. CV: Var_eq/Var_neutre = {(veq/vne).mean():.4f} "
          f"[prédit ∈ [0.96, 0.995]]")
    print(f"B. forme δ(m): données brutes dans {OUT_JSON} (champ delta_m_eq) — "
          f"fit lin vs saturation à faire sur l'agrégat (ΔAIC, grille B).")
    print(f"\nTerminé en {(time.time()-t0)/60:.1f} min. Résultats: {OUT_JSON}")
