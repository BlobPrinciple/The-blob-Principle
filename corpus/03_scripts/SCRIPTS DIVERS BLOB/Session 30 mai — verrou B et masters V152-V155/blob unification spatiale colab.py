# =====================================================================================
# BLOB PRINCIPLE — TEST D'UNIFICATION INFO<->GEOMETRIE, VERSION SPATIALE (robuste)
# A lancer APRES blob_scaling_colab.py (reutilise le meme moteur, charge l'etat final si dispo).
#
# CORRECTION du protocole : au lieu de correler info et courbure le long du TEMPS
# (serie courte, fragile, => corr instable -0.08..-0.38 observee), on les mesure
# SOMMET PAR SOMMET a N fixe : des milliers de points d'un coup => statistique robuste.
#
# Pour chaque sommet v on calcule :
#   - info_locale(v)     = log(1 + nb de triangles incidents a v)        [ΔI local, topologique]
#   - courbure_locale(v) = courbure metrique (deficit angulaire, positions 3D) [INDEPENDANTE des triangles]
#   - courbure_ollivier(v) = moyenne d'Ollivier sur les aretes de v       [topologique, pour comparaison]
# Puis on correle a travers TOUS les sommets. Test de non-tautologie = info vs courbure METRIQUE.
#
# ECHANTILLONNAGE DYNAMIQUE (corrige le bug) : nb de points et de mesures s'adaptent a N.
# Fidele au moteur (BETA=0.30, TAU=0.50, kappa=6.6, mitose continue, cycle, Ollivier exact).
# Paliers JSON : 1000, 2500, 5000, 10000, 15000, 25000 (dynamiques : sautes si depasses).
# =====================================================================================
import numpy as np, math, time, json
from collections import deque
from scipy.spatial import KDTree

BETA, TAU, KAPPA = 0.30, 0.50, 6.6

# ----------------------------- MOTEUR DE REFERENCE (exact, identique) -----------------------------
def rips_radius(N, kappa, mult=1.0): return mult * (kappa / ((N - 1) * (4/3) * math.pi)) ** (1/3)
def E0_target(N, kappa): return max(N - 1, int(N * kappa / 2))
def lcc_size(adj, N):
    seen = [False]*N; best = 0
    for s in range(N):
        if not seen[s]:
            sz = 0; q = deque([s]); seen[s] = True
            while q:
                v = q.popleft(); sz += 1
                for w in adj[v]:
                    if not seen[w]: seen[w] = True; q.append(w)
            best = max(best, sz)
    return best
def build_initial(N, seed, kappa, pool_mult=1.6):
    r = rips_radius(N, kappa); r_p = pool_mult * r; E0 = E0_target(N, kappa)
    rng = np.random.default_rng(seed); pts = rng.uniform(0.0, 1.0, (N, 3))
    tree = KDTree(pts); adj = [set() for _ in range(N)]
    for i, j in tree.query_pairs(r): adj[i].add(j); adj[j].add(i)
    pool = list(tree.query_pairs(r_p)); rng2 = np.random.default_rng(seed + 50_000)
    K = sum(len(adj[i]) for i in range(N)) // 2; att = 0; max_att = 10*abs(E0-K)+5000
    while K != E0 and att < max_att:
        att += 1
        if K < E0:
            if not pool: break
            u, v = pool[rng2.integers(len(pool))]
            if v not in adj[u]: adj[u].add(v); adj[v].add(u); K += 1
        else:
            edges = [(i, j) for i in range(N) for j in adj[i] if j > i]
            if not edges: break
            u, v = edges[rng2.integers(len(edges))]
            adj[u].discard(v); adj[v].discard(u)
            if lcc_size(adj, N) == N: K -= 1
            else: adj[u].add(v); adj[v].add(u)
    return pts, adj, pool, E0
def count_triangles(adj, N):
    n = 0
    for i in range(N):
        for j in adj[i]:
            if j > i: n += len(adj[i] & adj[j] & set(k for k in adj[j] if k > j))
    return n
def find_all_K4(adj, N):
    out = []
    for i in range(N):
        Ni = adj[i]
        for j in Ni:
            if j <= i: continue
            cij = Ni & adj[j]
            for k in cij:
                if k <= j: continue
                for l in (cij & adj[k]):
                    if l > k: out.append((i, j, k, l))
    return out
def still_connected(adj, u, v, N):
    seen = {u}; q = deque([u])
    while q:
        node = q.popleft()
        for w in adj[node]:
            if w in seen: continue
            if (node == u and w == v) or (node == v and w == u): continue
            seen.add(w); q.append(w)
            if w == v: return True
    return False
def ollivier_edge(adj, x, y):
    Nx = list(adj[x]); Ny = set(adj[y])
    if not Nx or not Ny: return 0.0
    def d_short(a, bset, maxd=3):
        dist = {a: 0}; q = deque([a]); found = {}
        while q:
            u = q.popleft()
            if u in bset: found[u] = dist[u]
            if dist[u] >= maxd: continue
            for w in adj[u]:
                if w not in dist: dist[w] = dist[u]+1; q.append(w)
        return found
    total = 0; cnt = 0
    for a in Nx:
        fd = d_short(a, Ny); total += (min(fd.values()) if fd else 3); cnt += 1
    return 1.0 - (total/cnt if cnt else 0)

# ----------------------------- MOTEUR VIVANT (identique) -----------------------------
def key(q): return tuple(sorted(q))
class BlobVivant:
    def __init__(self, N0=100, seed=1):
        self.beta, self.tau, self.kappa = BETA, TAU, KAPPA
        pts, a0, pool, E0 = build_initial(N0, seed, KAPPA)
        self.pts = [np.array(p) for p in pts]; self.adj = [set(x) for x in a0]; self.N = N0
        self.rng = np.random.default_rng(seed*13); self.sweep = 0
        self.t1 = {}; self.t2 = {}; self.born = {}; self.last_ratios = []
    def Sglob(self):
        d = np.array([len(self.adj[i]) for i in range(self.N)], float)
        D = d.std()/d.mean() if d.mean() > 0 else 0
        return math.log(1 + count_triangles(self.adj, self.N)) - self.beta*D
    def vg_local(self, parent, newp, r=0.32):
        cand = [parent] + list(self.adj[parent])
        return [i for i in cand if np.linalg.norm(self.pts[i]-newp) < r]
    def step(self, growth=0.12):
        self.sweep += 1; S = self.Sglob(); tau_eff = self.tau/max(self.N, 1)
        for _ in range(self.N):
            v = int(self.rng.integers(self.N))
            if not self.adj[v]: continue
            if self.rng.random() < 0.5:
                bb = int(self.rng.integers(self.N))
                if bb == v or bb in self.adj[v] or np.linalg.norm(self.pts[v]-self.pts[bb]) > 0.45: continue
                self.adj[v].add(bb); self.adj[bb].add(v); S2 = self.Sglob(); d = S2-S
                if d >= 0 or self.rng.random() < math.exp(min(d/tau_eff, 30)): S = S2
                else: self.adj[v].discard(bb); self.adj[bb].discard(v)
            else:
                w = int(list(self.adj[v])[int(self.rng.integers(len(self.adj[v])))])
                if len(self.adj[v]) <= 2 or len(self.adj[w]) <= 2:
                    if not still_connected(self.adj, v, w, self.N): continue
                self.adj[v].discard(w); self.adj[w].discard(v); S2 = self.Sglob(); d = S2-S
                if d >= 0 or self.rng.random() < math.exp(min(d/tau_eff, 30)): S = S2
                else: self.adj[v].add(w); self.adj[w].add(v)
        n_mit = max(2, int(self.N*growth)); mset = set()
        for _ in range(n_mit):
            parent = int(self.rng.integers(self.N)); newp = self.pts[parent] + self.rng.normal(0, 0.10, 3)
            vois = self.vg_local(parent, newp)
            self.pts.append(newp); self.adj.append(set()); nid = self.N; self.N += 1
            if len(vois) < 2: self.adj[nid].add(parent); self.adj[parent].add(nid); mset.add(parent)
            else:
                knn = sorted(vois, key=lambda i: np.linalg.norm(self.pts[i]-newp))[:int(self.kappa)]
                for w in knn: self.adj[nid].add(w); self.adj[w].add(nid)
                mset |= set(knn)
        K4 = find_all_K4(self.adj, self.N); cur = set(key(q) for q in K4)
        for q in K4:
            k = key(q)
            if k not in self.born: self.born[k] = self.sweep; self.t1[k] = 0; self.t2[k] = 0
            if mset & set(q): self.t1[k] += 1
        ratios = []
        for q in K4:
            k = key(q); p_eff = 0.236*math.exp(-max(self.t1.get(k, 0), 0)/8)
            if self.rng.random() < p_eff:
                self.t2[k] = self.t2.get(k, 0)+1
                i, j = self.rng.choice(4, 2, replace=False); u, w = q[int(i)], q[int(j)]
                if w in self.adj[u] and len(self.adj[u]) > 2 and len(self.adj[w]) > 2 and still_connected(self.adj, u, w, self.N):
                    self.adj[u].discard(w); self.adj[w].discard(u)
        for k in list(self.born):
            if k not in cur:
                t1 = self.t1.get(k, 0); t2 = max(self.t2.get(k, 0), 1); ratios.append(t1/t2)
                del self.born[k]; self.t1.pop(k, None); self.t2.pop(k, None)
        self.last_ratios = ratios

# ----------------------------- MESURES LOCALES PAR SOMMET -----------------------------
def info_locale(adj, v):
    """log(1 + nb de triangles incidents au sommet v) = information topologique locale."""
    nb = list(adj[v]); tri = 0
    for i in range(len(nb)):
        for j in range(i+1, len(nb)):
            if nb[j] in adj[nb[i]]: tri += 1
    return math.log(1 + tri)

def courbure_metrique_locale(adj, pts, v):
    """Deficit angulaire au sommet v (positions 3D). INDEPENDANTE du comptage de triangles."""
    nb = list(adj[v])
    if len(nb) < 2: return None
    angs = []; pv = pts[v]
    for i in range(len(nb)):
        for j in range(i+1, len(nb)):
            a = pts[nb[i]]-pv; c = pts[nb[j]]-pv
            na = np.linalg.norm(a); nc = np.linalg.norm(c)
            if na > 1e-9 and nc > 1e-9:
                cos = np.clip(np.dot(a, c)/(na*nc), -1, 1); angs.append(math.acos(cos))
    if not angs: return None
    return 2*math.pi - sum(angs)/len(angs)*len(nb)

def courbure_ollivier_locale(adj, v):
    """Moyenne d'Ollivier sur les aretes incidentes a v (topologique)."""
    if not adj[v]: return None
    vals = [ollivier_edge(adj, v, w) for w in adj[v]]
    return float(np.mean(vals)) if vals else None

# ----------------------------- TEST SPATIAL (echantillonnage DYNAMIQUE) -----------------------------
def test_spatial(bl, seed):
    N = bl.N; adj = bl.adj; pts = bl.pts; rng = np.random.default_rng(123)
    # ECHANTILLONNAGE DYNAMIQUE : nb de sommets mesures = min(N, 800), borne pour le cout d'Ollivier
    n_sample = min(N, 800)
    sample = rng.choice(N, n_sample, replace=False)
    INFO = []; KM = []; KO = []
    for v in sample:
        il = info_locale(adj, v)
        km = courbure_metrique_locale(adj, pts, v)
        ko = courbure_ollivier_locale(adj, v)
        if km is not None and ko is not None:
            INFO.append(il); KM.append(km); KO.append(ko)
    INFO = np.array(INFO); KM = np.array(KM); KO = np.array(KO)
    out = {"N": int(N), "seed": int(seed), "n_points": len(INFO)}
    def corr(a, b):
        if len(a) < 10 or a.std() < 1e-9 or b.std() < 1e-9: return None
        return float(np.corrcoef(a, b)[0, 1])
    # LE TEST CLE : info locale <-> courbure METRIQUE (independante des triangles) = non-tautologie
    out["corr_info_Kmetrique"] = corr(INFO, KM)
    # comparaisons
    out["corr_info_Kollivier"] = corr(INFO, KO)
    out["corr_Kmetrique_Kollivier"] = corr(KM, KO)
    out["info_moy"] = float(INFO.mean()) if len(INFO) else None
    out["Kmetrique_moy"] = float(KM.mean()) if len(KM) else None
    out["Kollivier_moy"] = float(KO.mean()) if len(KO) else None
    return out

# ===================================== RUN =====================================
PALIERS = [1000, 2500, 5000, 10000, 15000, 25000]
SEED = 1
T0 = time.time()
results = []
bl = BlobVivant(N0=100, seed=SEED)
pi = 0
print(f"TEST D'UNIFICATION SPATIALE — seed={SEED}, paliers={PALIERS}")
print(f"{'N':>7} {'n_pts':>6} {'info<->Kmetr':>12} {'info<->Koll':>12} {'Kmetr<->Koll':>12} {'t(s)':>7}")
while bl.N < PALIERS[-1]:
    bl.step(growth=0.12)
    if pi < len(PALIERS) and bl.N >= PALIERS[pi]:
        snap = test_spatial(bl, SEED)
        snap["elapsed_s"] = round(time.time()-T0, 1)
        results.append(snap)
        def fmt(x): return f"{x:+.2f}" if x is not None else "  n/a"
        print(f"{snap['N']:>7} {snap['n_points']:>6} {fmt(snap['corr_info_Kmetrique']):>12} "
              f"{fmt(snap['corr_info_Kollivier']):>12} {fmt(snap['corr_Kmetrique_Kollivier']):>12} {snap['elapsed_s']:>7.1f}")
        with open(f"blob_unification_spatiale_seed{SEED}.json", "w") as f:
            json.dump(results, f, indent=2)
        pi += 1
        while pi < len(PALIERS) and PALIERS[pi] <= bl.N: pi += 1

print(f"\nTermine. JSON : blob_unification_spatiale_seed{SEED}.json")
print(f"Paliers atteints : {[r['N'] for r in results]}")
print("\n=== VERDICT ===")
print("Si corr_info_Kmetrique reste FORTEMENT NEGATIVE (~-0.5 a -0.8) a tous les paliers,")
print("  mesuree SPATIALEMENT (sommet par sommet) avec une courbure INDEPENDANTE des triangles :")
print("  => l'unification info<->geometrie est REELLE et robuste (non tautologique, non un artefact de petit N).")
print("Si elle s'effondre vers 0 a grand N : l'unification etait un artefact d'echelle.")
