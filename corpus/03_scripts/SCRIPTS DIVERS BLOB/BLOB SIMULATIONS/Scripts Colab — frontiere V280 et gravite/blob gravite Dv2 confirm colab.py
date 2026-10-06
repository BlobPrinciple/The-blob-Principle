#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — GRAVITÉ D-v2 : SURVIE DE LA STRUCTURE SPATIALE À L'ASSIMILATION
# Protocole pré-enregistré. Version 1.0 — 14 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# CE QUE CE SCRIPT CORRIGE (leçons du run 13/07 + dépouillement 14/07) :
#  (1) TÉMOIN Δ_net : un clone de l'état équilibré subit les MÊMES sweeps
#      d'assimilation SANS injection → la dérive de fond (T croît encore) est
#      mesurée et SOUSTRAITE. (Défaut fatal du run 1 : diffus +343 → +13711
#      par simple dérive ; verdict D non interprétable.)
#  (2) QUANTITÉ GRAVÉE P-R2 (choix de R., 14/07, AVANT ce run) :
#      SURVIE = corrélation de Pearson entre le champ d'excès IMMÉDIAT et le
#      champ d'excès ASSIMILÉ NET, par SOMMET, sur la zone de mesure.
#      Seuil : corr > 0,30 ET IC bootstrap 95 % excluant 0, sur ≥ 15/20 graines.
#  (3) Normalisation régionale corrigée : par arête interne (jamais /M_eff
#      après assimilation).
#  (4) CHAMPS PAR SOMMET SAUVEGARDÉS dans le JSON (plus de données perdues).
#  (5) GRAINES FRAÎCHES 2000–2019 (le run 1 utilisait 1000–1019).
#  (6) try/except par graine : aucune graine ne tue le run.
# Blocs build_geometry / BlobState / equilibrate / dihedral / inject_transfer :
# repris à l'IDENTIQUE du script du 13/07 (pipeline dont T/CV ont été reproduits
# bit-à-bit au container le 14/07).
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys, traceback
from collections import defaultdict
from itertools import combinations

# ───────────────────────── PARAMÈTRES ─────────────────────────
N            = 2000
SUBSTRATES   = 20
SEED_BANK    = list(range(3000, 3000 + SUBSTRATES))   # graines FRAÎCHES — run de CONFIRMATION H-ancrage
DENSITY      = 200.0
KAPPA        = 10.0
RCUT         = 1.6
BETA         = 0.30
TAU          = 0.5
E_PER_N      = 5
SWEEPS_EQ    = 30
M_INJECT     = 60
FRAC_COMPACT = 0.03
FRAC_DIFFUSE = 0.40
ASSIM_SWEEPS = 6
EDGE_SAMPLE  = 3000        # pour la mesure A (continuité)
N_BOOT       = 1000        # bootstrap IC de la corrélation spatiale
OUT_JSON     = "gravite_Dv2_confirm_results.json"

GRID = """
════════════════ GRILLE PRÉ-ENREGISTRÉE (gravée AVANT lecture) ════════════════
P-R2 — PRINCIPALE (quantité choisie et gravée par R. le 14/07) :
  Injection COMPACTE. Champs par sommet sur la ZONE DE MESURE (définie
  géométriquement : distance euclidienne au centre < R_abs + rc, donc cible +
  une couche d'une portée d'arête ; indépendante du graphe, stable).
    D(i)      = Σ |δ_e| des arêtes internes à la zone, incidentes à i, m_e ≥ 2
    ΔD_imm    = D_immédiat − D_avant
    ΔD_net    = D_assimilé − D_témoin        (témoin = mêmes sweeps SANS injection)
    corr_s    = Pearson( ΔD_imm , ΔD_net )   sur les sommets de la zone
  → SURVIE DE LA STRUCTURE SPATIALE si corr_s > 0,30 ET IC95 (bootstrap 1000)
    excluant 0, sur ≥ 15/20 graines.
  → PAS DE SURVIE si ≤ 7/20. Entre 8 et 14 : INDÉTERMINÉ, lu tel quel.
SECONDAIRES (exploratoires déclarés — aucun pari) :
  S1. corr_s pour l'injection DIFFUSE (même définition).
  S2. C-v2 immédiat NORMALISÉ PAR ARÊTE INTERNE de la cible :
      (d1−d0)/n_arêtes_internes(avant), compact vs diffus, apparié (info).
  S3. Localisation : ΔD_net moyen cible vs couronne (l'excès reste-t-il dedans ?).
  S4. A (continuité run 1) : r_eq vs r_rand.  S5. Var_eq/Var_neutre (suivi ×4,6).
Tout écart à la grille se lit tel quel. Aucun curseur ne bouge après lecture.
════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────────── GÉOMÉTRIE (identique run 1) ─────────────────────
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

# ───────────── ACTION COMPLÈTE, O(1) par swap (identique run 1) ─────────────
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
            if len({u, v, a, b}) < 4: continue
            if state.deg[u] <= 2 or state.deg[v] <= 2: continue
            dS, dT, d2n = state.dS_swap(u, v, a, b)
            if dS >= 0 or rng.random() < math.exp(dS / te):
                state.do_swap(u, v, a, b, dT, d2n)
                edge_list[io] = (a, b)
        state.assert_E(f"eq_sweep_{sw}")
    return state

def clone_state(st, cand):
    st2 = BlobState(cand, [k for k, (a, b) in enumerate(cand) if b in st.adj[a]])
    st2.assert_E("clone")
    return st2

# ─────────────── COURBURE DE REGGE (identique run 1) ───────────────
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
    """Énumération unique triangles→tétraèdres→e2t pour un état donné."""
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

def regge_field(e2t, pts, L, zone_set, zone_idx):
    """Champ par sommet : D(i) = Σ|δ_e| des arêtes INTERNES à la zone (m≥2),
    chaque arête contribuant à ses deux extrémités. Retour aligné sur zone_idx."""
    D = np.zeros(len(zone_idx))
    loc = {v: i for i, v in enumerate(zone_idx)}
    for e, ts in e2t.items():
        if len(ts) < 2: continue
        a, b = e
        if a in zone_set and b in zone_set:
            d = abs(2 * math.pi - sum(dihedral(pts, L, t, e) for t in ts))
            D[loc[a]] += d; D[loc[b]] += d
    return D

def region_sum_and_edges(e2t, pts, L, cible_set):
    """Somme des |δ| et nombre d'arêtes internes à la CIBLE (pour C-v2)."""
    s = 0.0; n = 0
    for e, ts in e2t.items():
        if len(ts) < 2: continue
        a, b = e
        if a in cible_set and b in cible_set:
            s += abs(2 * math.pi - sum(dihedral(pts, L, t, e) for t in ts)); n += 1
    return s, n

def regge_sample(state, pts, L, rng):
    """(|δ|, k) échantillonné — pour la mesure A (continuité run 1)."""
    e2t = tets_pack(state)
    edges = [e for e, ts in e2t.items() if len(ts) >= 2]
    if len(edges) > EDGE_SAMPLE:
        idx = rng.choice(len(edges), size=EDGE_SAMPLE, replace=False)
        edges = [edges[i] for i in idx]
    out = []
    for e in edges:
        ts = e2t[e]
        d = 2 * math.pi - sum(dihedral(pts, L, t, e) for t in ts)
        out.append((abs(d), int(state.deg[e[0]] + state.deg[e[1]])))
    return out

# ─────────────── INJECTION PAR TRANSFERT (identique run 1) ───────────────
def inject_transfer(state, cand, pts, L, center, radius, M, rng):
    def in_region(i):
        d = pts[i] - center; d -= L * np.round(d / L)
        return np.linalg.norm(d) < radius
    reg = np.array([in_region(i) for i in range(N)])
    cand_in = [k for k, (a, b) in enumerate(cand)
               if reg[a] and reg[b] and (b not in state.adj[a])]
    act_out = [(i, j) for i in range(N) for j in state.adj[i]
               if j > i and not reg[i] and not reg[j]]
    M_eff = min(M, len(cand_in), len(act_out))
    assert M_eff >= 0.8 * M, f"Région trop petite: {M_eff}/{M}"
    rng.shuffle(cand_in); rng.shuffle(act_out)
    E_before = state.E
    for k in range(M_eff):
        a, b = cand[cand_in[k]]
        u, v = act_out[k]
        t_rm = len(state.adj[u] & state.adj[v])
        state.adj[u].discard(v); state.adj[v].discard(u)
        t_add = len(state.adj[a] & state.adj[b])
        state.adj[a].add(b); state.adj[b].add(a)
        state.T += (t_add - t_rm)
        state.sum_d2 += (-2*state.deg[u]+1)+(-2*state.deg[v]+1)+(2*state.deg[a]+1)+(2*state.deg[b]+1)
        state.deg[u] -= 1; state.deg[v] -= 1; state.deg[a] += 1; state.deg[b] += 1
    state.assert_E("post_transfer")
    assert state.E == E_before
    return M_eff

def pearson_boot(x, y, rng, nboot=N_BOOT):
    if x.std() == 0 or y.std() == 0: return float("nan"), float("nan"), float("nan")
    r = float(np.corrcoef(x, y)[0, 1])
    n = len(x); bs = []
    for _ in range(nboot):
        idx = rng.integers(0, n, size=n)
        xa, ya = x[idx], y[idx]
        if xa.std() > 0 and ya.std() > 0:
            bs.append(float(np.corrcoef(xa, ya)[0, 1]))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return r, float(lo), float(hi)

# ───────────────────────── PIPELINE PAR GRAINE ─────────────────────────
def run_seed(seed):
    rng = np.random.default_rng(seed)
    pts, cand, L, rc = build_geometry(seed)
    E0 = E_PER_N * N
    assert len(cand) > E0
    res = {"seed": seed, "N": N, "M_cand": len(cand)}

    # ÉQUILIBRÉ + contrôles de continuité
    init = rng.choice(len(cand), size=E0, replace=False)
    st = BlobState(cand, init); st.assert_E("init")
    st = equilibrate(st, cand, rng, SWEEPS_EQ)
    res["T_eq"] = st.T; res["CV_eq"] = st.cv(); res["Var_deg_eq"] = float(st.deg.var())
    st_r = BlobState(cand, np.random.default_rng(seed + 77).choice(len(cand), size=E0, replace=False))
    res["Var_deg_neutre"] = float(st_r.deg.var())
    A_eq = regge_sample(st, pts, L, rng); A_rd = regge_sample(st_r, pts, L, rng)
    def corr2(D):
        x = np.array([d[1] for d in D], float); y = np.array([d[0] for d in D])
        return float(np.corrcoef(x, y)[0, 1]) if len(x) > 30 and x.std() > 0 else float("nan")
    res["r_eq_k"] = corr2(A_eq); res["r_rand_k"] = corr2(A_rd)

    # TÉMOIN (unique par graine) : mêmes sweeps d'assimilation, SANS injection
    st_tem = clone_state(st, cand)
    st_tem = equilibrate(st_tem, cand, np.random.default_rng(seed + 555), ASSIM_SWEEPS)
    res["T_temoin"] = st_tem.T
    pack_avant = tets_pack(st)
    pack_tem   = tets_pack(st_tem)

    center = pts.mean(0)
    out = {}
    for label, frac in (("compact", FRAC_COMPACT), ("diffus", FRAC_DIFFUSE)):
        n_target = max(40, int(frac * N)) if label == "compact" else max(200, int(frac * N))
        R_abs = L * (3 * n_target / (4 * math.pi * N)) ** (1/3)
        # zone de mesure GÉOMÉTRIQUE (gravée) : < R_abs + rc
        dvec = pts - center; dvec -= L * np.round(dvec / L)
        dist = np.linalg.norm(dvec, axis=1)
        cible_idx = np.where(dist < R_abs)[0]
        zone_idx  = np.where(dist < R_abs + rc)[0]
        cible_set = set(cible_idx.tolist()); zone_set = set(zone_idx.tolist())

        D_avant = regge_field(pack_avant, pts, L, zone_set, zone_idx)
        d0, n0 = region_sum_and_edges(pack_avant, pts, L, cible_set)
        D_tem = regge_field(pack_tem, pts, L, zone_set, zone_idx)

        st_inj = clone_state(st, cand)
        M_eff = inject_transfer(st_inj, cand, pts, L, center, R_abs, M_INJECT,
                                np.random.default_rng(seed + 9))
        pack_imm = tets_pack(st_inj)
        D_imm = regge_field(pack_imm, pts, L, zone_set, zone_idx)
        d1, n1 = region_sum_and_edges(pack_imm, pts, L, cible_set)

        st_inj = equilibrate(st_inj, cand, np.random.default_rng(seed + 5), ASSIM_SWEEPS)
        pack_ass = tets_pack(st_inj)
        D_ass = regge_field(pack_ass, pts, L, zone_set, zone_idx)

        dDi = D_imm - D_avant
        dDn = D_ass - D_tem
        r, lo, hi = pearson_boot(dDi, dDn, np.random.default_rng(seed + 13))
        in_c = np.isin(zone_idx, cible_idx)
        out[label] = {
            "M_eff": int(M_eff), "n_target": int(n_target), "R_over_L": float(R_abs / L),
            "n_zone": int(len(zone_idx)),
            "corr_s": r, "corr_lo": lo, "corr_hi": hi,
            "Cv2_imm_par_arete": float((d1 - d0) / max(n0, 1)),
            "n_aretes_cible_avant": int(n0), "n_aretes_cible_apres": int(n1),
            "dDnet_moy_cible": float(dDn[in_c].mean()),
            "dDnet_moy_couronne": float(dDn[~in_c].mean()) if (~in_c).sum() else float("nan"),
            "champ_zone_idx": zone_idx.tolist() if label == "compact" else None,
            "champ_D_avant": D_avant.tolist() if label == "compact" else None,
            "champ_D_imm":   D_imm.tolist()   if label == "compact" else None,
            "champ_D_assim": D_ass.tolist()   if label == "compact" else None,
            "champ_D_temoin": D_tem.tolist()  if label == "compact" else None,
        }
    res["injection"] = out
    return res

# ───────────────────────── MAIN ─────────────────────────
if __name__ == "__main__":
    print(GRID)
    print(f"Environnement: python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"N={N}, substrats={SUBSTRATES}, graines={SEED_BANK[0]}–{SEED_BANK[-1]}, "
          f"β={BETA}, τ={TAU}, |E|={E_PER_N}N (asserté), assim={ASSIM_SWEEPS} sweeps + TÉMOIN\n")
    all_res = []
    t0 = time.time()
    for i, seed in enumerate(SEED_BANK):
        t1 = time.time()
        try:
            r = run_seed(seed)
            all_res.append(r)
            c = r["injection"]["compact"]
            print(f"[{i+1}/{SUBSTRATES}] seed={seed}  T={r['T_eq']}→tém.{r['T_temoin']}  "
                  f"corr_s={c['corr_s']:+.3f} [{c['corr_lo']:+.2f},{c['corr_hi']:+.2f}]  "
                  f"({time.time()-t1:.0f}s)", flush=True)
        except Exception as ex:
            print(f"[{i+1}/{SUBSTRATES}] seed={seed} ÉCHOUÉE: {ex}", flush=True)
            traceback.print_exc()
            all_res.append({"seed": seed, "error": str(ex)})
        with open(OUT_JSON, "w") as f:
            json.dump(all_res, f)
    ok = [r for r in all_res if "injection" in r]
    print(f"\n════════ LECTURE P-R2 (grille appliquée telle quelle, {(time.time()-t0)/60:.1f} min) ════════")
    if not ok:
        print("Aucune graine exploitable."); sys.exit(0)
    surv = sum(1 for r in ok
               if r["injection"]["compact"]["corr_s"] > 0.30
               and r["injection"]["compact"]["corr_lo"] > 0)
    rs = np.array([r["injection"]["compact"]["corr_s"] for r in ok])
    print(f"corr_s (compact) = {rs.mean():+.3f} ± {rs.std():.3f}  |  graines en survie : {surv}/{len(ok)}")
    if surv >= 15:  print("→ P-R2 : ✓ SURVIE DE LA STRUCTURE SPATIALE (prédiction de R. validée)")
    elif surv <= 7: print("→ P-R2 : ✗ PAS DE SURVIE (l'assimilation efface la structure)")
    else:           print("→ P-R2 : INDÉTERMINÉ (entre 8 et 14) — lu tel quel")
    rd = np.array([r["injection"]["diffus"]["corr_s"] for r in ok])
    print(f"S1 diffus : corr_s = {np.nanmean(rd):+.3f} ± {np.nanstd(rd):.3f} (exploratoire)")
    cc = np.array([r["injection"]["compact"]["Cv2_imm_par_arete"] for r in ok])
    dc = np.array([r["injection"]["diffus"]["Cv2_imm_par_arete"] for r in ok])
    print(f"S2 C-v2 immédiat/arête interne : compact {cc.mean():+.3f}±{cc.std():.3f} "
          f"vs diffus {dc.mean():+.3f}±{dc.std():.3f} (info)")
    tc = np.array([r["injection"]["compact"]["dDnet_moy_cible"] for r in ok])
    kc = np.array([r["injection"]["compact"]["dDnet_moy_couronne"] for r in ok])
    print(f"S3 localisation : ΔD_net cible {tc.mean():+.2f} vs couronne {kc.mean():+.2f}")
    req = np.array([r["r_eq_k"] for r in ok]); rrd = np.array([r["r_rand_k"] for r in ok])
    print(f"S4 couplage A : r_eq {req.mean():.3f}±{req.std():.3f} vs r_rand {rrd.mean():.3f}±{rrd.std():.3f}")
    veq = np.array([r["Var_deg_eq"] for r in ok]); vne = np.array([r["Var_deg_neutre"] for r in ok])
    print(f"S5 Var_eq/Var_neutre = {(veq/vne).mean():.2f} (suivi du ×4,6)")
    print(f"\nRésultats complets (champs par sommet inclus) : {OUT_JSON}")
