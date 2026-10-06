#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# BLOB — TEST EMPIRIQUE DE POSITIVITÉ PAR RÉFLEXION (Osterwalder-Schrader)
# Le juge de la porte quantique. Version 1.0 — 13 juillet 2026.
# ═══════════════════════════════════════════════════════════════════════════
# ENJEU : la positivité par réflexion (PR) est la condition d'OS qui, si vérifiée,
# donne une théorie QUANTIQUE reconstruite (quantique DÉRIVÉ, pas postulé).
# Le diagnostic analytique (13/07) trouve deux obstructions de champ moyen (CV
# global, log-du-total). CE TEST tranche EMPIRIQUEMENT si, malgré l'écriture non
# locale de l'action, la MESURE satisfait quand même PR (échappatoire E1/E2) ou
# la viole franchement (⟹ [T-V275-5] définitif, extension WZ obligatoire).
#
# PRINCIPE (Glimm-Jaffe, Osterwalder-Schrader 1973) :
#   Soit Θ une réflexion échangeant Λ₊ (demi-espace "futur") et Λ₋ = Θ(Λ₊).
#   PR ⟺ pour toute fonctionnelle f supportée sur Λ₊ :  E[ (Θf)* · f ] ≥ 0.
#   La matrice M[i,j] = E[ (Θf_i)* · f_j ] doit être SEMI-DÉFINIE POSITIVE
#   (toutes valeurs propres ≥ 0) pour une base {f_i} de fonctionnelles.
#
# CONTRÔLE INTÉGRÉ (anti-artefact) : la MÊME matrice M est calculée sur des
# configurations ALÉATOIRES (non équilibrées). PR est une propriété de la mesure
# d'ÉQUILIBRE ; sur l'aléatoire, aucune structure PR n'est attendue. Le SIGNAL =
# écart(équilibré vs aléatoire). Si l'équilibré est SDP et l'aléatoire non, PR
# est réelle. Si les deux se ressemblent, l'estimateur ne capte rien de spécifique.
#
# CONVENTION : action complète S = log(1+T) − β·CV, mesure exp((N/τ)S),
# Metropolis maximisant S, |E| conservé et asserté. (Signe à confirmer au corpus.)
# ═══════════════════════════════════════════════════════════════════════════

import numpy as np, math, json, time, sys
from collections import defaultdict

# ───────────────────────── PARAMÈTRES ─────────────────────────
N            = 3000        # 3000 conseillé ; 8000+ pour très grand N si machine le permet
SUBSTRATES   = 24          # substrats indépendants (≥24 pour barres d'erreur nettes)
SEED_BANK    = list(range(2000, 2000 + SUBSTRATES))
DENSITY      = 200.0
KAPPA        = 10.0
RCUT         = 1.6
BETA         = 0.30
TAU          = 0.5
E_PER_N      = 5           # |E| = 5N (fixé, conservé)
SWEEPS_EQ    = 30
N_SAMPLES    = 40          # échantillons de configuration par substrat (pour les espérances)
DECORR_SWEEPS= 2           # sweeps de décorrélation entre échantillons
OUT_JSON     = "reflection_positivity_results.json"

GRID = """
════════════════ GRILLE PRÉ-ENREGISTRÉE (positivité par réflexion) ════════════════
On mesure M[i,j] = E[(Θf_i)·f_j] sur une base de K fonctionnelles supportées sur Λ₊.
PR ⟺ M semi-définie positive (SDP), i.e. λ_min(M_sym) ≥ 0.

VERDICT (gravé avant lecture) :
 • PR VÉRIFIÉE (quantique dérivable) si : λ_min(équilibré) ≥ −ε sur ≥ 90% des substrats
   ET nettement > λ_min(aléatoire). ε = tolérance numérique = 10⁻³·(échelle de M).
 • PR VIOLÉE (⟹ [T-V275-5] tient, extension WZ) si : λ_min(équilibré) < 0 franchement
   (< −10× tolérance) sur la majorité des substrats.
 • INDÉTERMINÉ si équilibré ≈ aléatoire (l'estimateur ne distingue pas la mesure d'équilibre).

Θ = réflexion géométrique (plan médian x → L−x) = composante spatiale du miroir CPT.
Λ₊ = sommets avec x < L/2 ; Λ₋ = Θ(Λ₊) = sommets x > L/2.
Fonctionnelles f_i = observables locales supportées sur Λ₊ (comptages de motifs par région).
Aucune réinterprétation post hoc. Le signe de λ_min tombe tel quel.
════════════════════════════════════════════════════════════════════════════════════
"""

# ───────────────────────── GÉOMÉTRIE + ÉTAT (action complète) ─────────────────────────
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
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    for j in grid[tuple((ci+[dx,dy,dz]) % ncell)]:
                        if j > i:
                            d = pts[i]-pts[j]; d -= L*np.round(d/L)
                            if (d*d).sum() < rc*rc: cand.append((i,j))
    return pts, sorted(set(cand)), L, rc

class BlobState:
    def __init__(self, cand, active_idx):
        self.cand = cand
        self.adj = defaultdict(set)
        self.active = set(active_idx)
        for k in active_idx:
            a,b = cand[k]; self.adj[a].add(b); self.adj[b].add(a)
        self.E = len(active_idx)
        self.deg = np.zeros(N, dtype=np.int64)
        for k in active_idx:
            a,b = cand[k]; self.deg[a]+=1; self.deg[b]+=1
        self.sum_d2 = int((self.deg.astype(np.int64)**2).sum())
        self.T = self._count_T()
    def _count_T(self):
        t=0
        for u in self.adj:
            for v in self.adj[u]:
                if v>u: t += len(self.adj[u]&self.adj[v])
        return t//3
    def cv(self):
        mu = 2.0*self.E/N
        var = self.sum_d2/N - mu*mu
        return math.sqrt(max(var,0.0))/mu
    def dS_swap(self,u,v,a,b):
        t_rm = len(self.adj[u]&self.adj[v])
        self.adj[u].discard(v); self.adj[v].discard(u)
        t_add = len(self.adj[a]&self.adj[b])
        self.adj[u].add(v); self.adj[v].add(u)
        dT = t_add - t_rm
        d_logT = math.log(1+self.T+dT) - math.log(1+self.T)
        d2_new = self.sum_d2 + (-2*self.deg[u]+1)+(-2*self.deg[v]+1)+(2*self.deg[a]+1)+(2*self.deg[b]+1)
        mu = 2.0*self.E/N
        cv_new = math.sqrt(max(d2_new/N - mu*mu,0.0))/mu
        return (d_logT - BETA*(cv_new-self.cv())), dT, d2_new
    def do_swap(self,u,v,a,b,dT,d2n):
        self.adj[u].discard(v); self.adj[v].discard(u)
        self.adj[a].add(b); self.adj[b].add(a)
        self.deg[u]-=1; self.deg[v]-=1; self.deg[a]+=1; self.deg[b]+=1
        self.sum_d2 = d2n; self.T += dT
    def assert_E(self,tag):
        e = sum(len(s) for s in self.adj.values())//2
        assert e==self.E==E_PER_N*N, f"|E| VIOLÉ [{tag}]: {e}/{self.E}/{E_PER_N*N}"

def equilibrate(state, cand, rng, sweeps):
    te = TAU/N; pool = np.array(cand)
    el = [(i,j) for i in range(N) for j in state.adj[i] if j>i]
    for sw in range(sweeps):
        for _ in range(3*N):
            io = rng.integers(len(el)); u,v = el[io]
            ii = rng.integers(len(pool)); a,b = int(pool[ii,0]), int(pool[ii,1])
            if b in state.adj[a] or v not in state.adj[u]: continue
            if len({u,v,a,b})<4: continue
            if state.deg[u]<=2 or state.deg[v]<=2: continue
            dS,dT,d2n = state.dS_swap(u,v,a,b)
            if dS>=0 or rng.random()<math.exp(dS/te):
                state.do_swap(u,v,a,b,dT,d2n); el[io]=(a,b)
        state.assert_E(f"eq_{sw}")
    return state, el

# ─────────────── FONCTIONNELLES LOCALES SUPPORTÉES SUR Λ₊ ───────────────
def build_regions(pts, L, K=8):
    """Λ₊ = {x < L/2}. On y découpe K sous-régions (tranches en y,z) et chaque
    fonctionnelle f_i = (# triangles dans la sous-région i) − moyenne. Locales, ⊂ Λ₊."""
    xpos = pts[:,0]
    plus_mask = xpos < L/2                      # Λ₊
    # sous-regions dans Λ₊ : quadrillage (y,z)
    ny = int(math.sqrt(K)); nz = (K+ny-1)//ny
    yb = (pts[:,1]//(L/ny)).astype(int); zb = (pts[:,2]//(L/nz)).astype(int)
    region_id = np.where(plus_mask, yb*nz+zb, -1)   # -1 = hors Λ₊
    return plus_mask, region_id, ny*nz

def reflect_vertex_map(pts, L):
    """Θ : x → L−x. Renvoie, pour chaque sommet i de Λ₊, le sommet miroir le plus
    proche dans Λ₋ (appariement géométrique). Involution approximée par plus-proche."""
    xr = pts.copy(); xr[:,0] = L - xr[:,0]        # position réfléchie
    # pour chaque sommet, trouver le plus proche de sa position réfléchie
    from scipy.spatial import cKDTree
    tree = cKDTree(pts)
    _, mirror = tree.query(xr, k=1)
    return mirror                                  # mirror[i] = image de i sous Θ

def functional_vector(state, region_id, n_reg):
    """f_i = # triangles dont les 3 sommets sont dans la sous-région i de Λ₊."""
    f = np.zeros(n_reg)
    for u in state.adj:
        ru = region_id[u]
        if ru < 0: continue
        for v in state.adj[u]:
            if v>u and region_id[v]==ru:
                for w in state.adj[u]&state.adj[v]:
                    if w>v and region_id[w]==ru:
                        f[ru]+=1
    return f

def reflected_functional(state, region_id, n_reg, mirror, pts, L):
    """Θf_i : la même fonctionnelle mais évaluée sur les images miroir (dans Λ₋)."""
    # region miroir : on ré-étiquette via mirror puis on compte dans Λ₋
    # Θf_i compte les triangles dans la région réfléchie i (côté Λ₋)
    # On construit region_id_reflected : pour un sommet j de Λ₋, quelle région i de Λ₊ ?
    reg_ref = -np.ones(N, dtype=int)
    for i in range(N):
        if region_id[i] >= 0:                      # i ∈ Λ₊, région region_id[i]
            reg_ref[mirror[i]] = region_id[i]       # son miroir porte la même étiquette
    f = np.zeros(n_reg)
    for u in state.adj:
        ru = reg_ref[u]
        if ru < 0: continue
        for v in state.adj[u]:
            if v>u and reg_ref[v]==ru:
                for w in state.adj[u]&state.adj[v]:
                    if w>v and reg_ref[w]==ru:
                        f[ru]+=1
    return f

# ─────────────── MATRICE DE POSITIVITÉ PAR RÉFLEXION ───────────────
def reflection_matrix(states, region_id, n_reg, mirror, pts, L):
    """M[i,j] = E[(Θf_i)·f_j] − E[Θf_i]E[f_j] (covariance réfléchie sous la mesure).
    PR ⟺ M_sym semi-définie positive."""
    F = np.array([functional_vector(s, region_id, n_reg) for s in states])       # (S, n_reg)
    TF = np.array([reflected_functional(s, region_id, n_reg, mirror, pts, L) for s in states])
    # centrer
    Fc = F - F.mean(0); TFc = TF - TF.mean(0)
    M = (TFc.T @ Fc) / len(states)                 # E[(Θf_i)(f_j)] centré
    Msym = 0.5*(M + M.T)                            # partie symétrique (PR concerne M_sym)
    eig = np.linalg.eigvalsh(Msym)
    return Msym, eig

# ───────────────────────── PIPELINE PAR GRAINE ─────────────────────────
def run_seed(seed):
    rng = np.random.default_rng(seed)
    pts, cand, L, rc = build_geometry(seed)
    E0 = E_PER_N*N
    plus_mask, region_id, n_reg = build_regions(pts, L, K=8)
    mirror = reflect_vertex_map(pts, L)
    res = {"seed": seed, "N": N, "n_reg": int(n_reg), "M_cand": len(cand)}

    # ── ÉQUILIBRÉ : collecter N_SAMPLES configurations décorrélées ──
    init = rng.choice(len(cand), size=E0, replace=False)
    st = BlobState(cand, init); st.assert_E("init")
    st, el = equilibrate(st, cand, rng, SWEEPS_EQ)
    eq_states = []
    for s in range(N_SAMPLES):
        st, el = equilibrate(st, cand, rng, DECORR_SWEEPS)
        # snapshot (copie légère de l'adjacence)
        snap = BlobState(cand, [k for k,(a,b) in enumerate(cand) if b in st.adj[a]])
        eq_states.append(snap)
    Msym_eq, eig_eq = reflection_matrix(eq_states, region_id, n_reg, mirror, pts, L)
    res["lambda_min_eq"] = float(eig_eq.min())
    res["lambda_max_eq"] = float(eig_eq.max())
    res["scale_eq"] = float(np.abs(Msym_eq).max())

    # ── ALÉATOIRE (contrôle) : N_SAMPLES configs non équilibrées ──
    rand_states = []
    for s in range(N_SAMPLES):
        idx = np.random.default_rng(seed+1000+s).choice(len(cand), size=E0, replace=False)
        rand_states.append(BlobState(cand, idx))
    Msym_rd, eig_rd = reflection_matrix(rand_states, region_id, n_reg, mirror, pts, L)
    res["lambda_min_rand"] = float(eig_rd.min())
    res["scale_rand"] = float(np.abs(Msym_rd).max())
    return res

# ───────────────────────── MAIN ─────────────────────────
if __name__ == "__main__":
    print(GRID)
    print(f"Environnement: python {sys.version.split()[0]}, numpy {np.__version__}")
    print(f"N={N}, substrats={SUBSTRATES}, β={BETA}, τ={TAU}, échantillons/substrat={N_SAMPLES}")
    print(f"Banque de graines: {SEED_BANK}\n")
    allr=[]; t0=time.time()
    for i,seed in enumerate(SEED_BANK):
        t1=time.time(); r=run_seed(seed); allr.append(r)
        with open(OUT_JSON,"w") as f: json.dump(allr,f)
        tol = 1e-3*r["scale_eq"]
        verdict = "SDP≈" if r["lambda_min_eq"]>=-tol else "NÉG"
        print(f"[{i+1}/{SUBSTRATES}] seed={seed}  λmin_eq={r['lambda_min_eq']:+.3e} "
              f"({verdict})  λmin_rand={r['lambda_min_rand']:+.3e}  "
              f"scale={r['scale_eq']:.1e}  ({time.time()-t1:.0f}s)")
    # ─── LECTURE SELON LA GRILLE ───
    lm_eq = np.array([r["lambda_min_eq"] for r in allr])
    lm_rd = np.array([r["lambda_min_rand"] for r in allr])
    sc = np.array([r["scale_eq"] for r in allr])
    tol = 1e-3*sc
    frac_sdp = np.mean(lm_eq >= -tol)
    print(f"\n═══ VERDICT (grille pré-enregistrée) ═══")
    print(f"λmin_eq   : moy={lm_eq.mean():+.3e}, min={lm_eq.min():+.3e}")
    print(f"λmin_rand : moy={lm_rd.mean():+.3e}")
    print(f"tolérance ε (moy) : {tol.mean():.3e}")
    print(f"Fraction de substrats avec λmin_eq ≥ −ε (SDP) : {frac_sdp:.0%}")
    sep = (lm_eq.mean() - lm_rd.mean())/ (math.sqrt(lm_eq.var()/len(lm_eq)+lm_rd.var()/len(lm_rd))+1e-30)
    print(f"Séparation équilibré vs aléatoire : {sep:+.1f}σ")
    if frac_sdp>=0.90 and lm_eq.mean() > lm_rd.mean() + 2*lm_eq.std():
        print("→ ✓ PR VÉRIFIÉE empiriquement : quantique DÉRIVABLE (E1/E2 sauve la situation).")
    elif (lm_eq < -10*tol).mean() > 0.5:
        print("→ ✗ PR VIOLÉE : [T-V275-5] tient, extension WZ obligatoire.")
    else:
        print("→ INDÉTERMINÉ : équilibré ≈ aléatoire, estimateur non discriminant. Raffiner.")
    print(f"\nTerminé en {(time.time()-t0)/60:.1f} min. Résultats: {OUT_JSON}")
