# =====================================================================================
# BLOB PRINCIPLE — SCALING DE L'UNIFICATION INFO<->GEOMETRIE + SIGNATURE MATIERE
# Script AUTONOME pour Google Colab. Paliers JSON : 1000, 2500, 5000, 10000, 15000, 25000.
# Fidele au moteur de reference (build_initial, run_mcmc_canonical) ET au moteur vivant
# de la session du 1 juin 2026 (Parties XLII, XLIV-XLVII). Aucune valeur modifiee.
#   BETA=0.30, TAU=0.50, kappa=6.6, mitose continue growth=0.12, effondrement 0.236*exp(-age/8)
#   t1=mitoses traversees, t2=dissipations subies, courbure Ollivier exacte (W1 BFS borne maxd=3)
# =====================================================================================
import numpy as np, math, time, json
from collections import deque
from scipy.spatial import KDTree

# ----------------------------- CONSTANTES (IDENTIQUES au corpus) -----------------------------
BETA  = 0.30      # coefficient de desordre (A4)
TAU   = 0.50      # temperature combinatoire (A5), effective = TAU/N
KAPPA = 6.6       # densite canonique (d_s=3)

# ----------------------------- MOTEUR DE REFERENCE (exact) -----------------------------
def rips_radius(N, kappa, mult=1.0):
    return mult * (kappa / ((N - 1) * (4/3) * math.pi)) ** (1/3)

def E0_target(N, kappa):
    return max(N - 1, int(N * kappa / 2))

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
    """Construit le RGG 3D initial avec E0 aretes et un pool d'aretes candidates."""
    r = rips_radius(N, kappa); r_p = pool_mult * r
    E0 = E0_target(N, kappa)
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0.0, 1.0, (N, 3))
    tree = KDTree(pts)
    adj = [set() for _ in range(N)]
    for i, j in tree.query_pairs(r):
        adj[i].add(j); adj[j].add(i)
    pool = list(tree.query_pairs(r_p))
    rng2 = np.random.default_rng(seed + 50_000)
    K = sum(len(adj[i]) for i in range(N)) // 2
    att = 0; max_att = 10 * abs(E0 - K) + 5000
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
            if j > i:
                n += len(adj[i] & adj[j] & set(k for k in adj[j] if k > j))
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
    """Verifie que retirer l'arete (u,v) ne deconnecte pas le graphe."""
    seen = {u}; q = deque([u])
    while q:
        node = q.popleft()
        for w in adj[node]:
            if w in seen: continue
            if (node == u and w == v) or (node == v and w == u): continue
            seen.add(w); q.append(w)
            if w == v: return True
    return False

# ----------------------------- COURBURE D'OLLIVIER-RICCI (exacte, du corpus) -----------------------------
def ollivier_edge(adj, x, y):
    """Ricci d'Ollivier kappa(x,y) = 1 - W1(m_x,m_y)/d(x,y), d=1 sur une arete.
       W1 approche par transport glouton (BFS borne maxd=3)."""
    Nx = list(adj[x]); Ny = set(adj[y])
    if not Nx or not Ny: return 0.0
    def d_short(a, bset, maxd=3):
        dist = {a: 0}; q = deque([a]); found = {}
        while q:
            u = q.popleft()
            if u in bset: found[u] = dist[u]
            if dist[u] >= maxd: continue
            for w in adj[u]:
                if w not in dist: dist[w] = dist[u] + 1; q.append(w)
        return found
    total = 0; cnt = 0
    for a in Nx:
        fd = d_short(a, Ny); total += (min(fd.values()) if fd else 3); cnt += 1
    return 1.0 - (total / cnt if cnt else 0)

# ----------------------------- MOTEUR VIVANT (Partie XLII, fidele) -----------------------------
def key(q): return tuple(sorted(q))

class BlobVivant:
    """Moteur vivant : croissance par mitose continue sans frontiere + cycle (effondrement->reservoir).
       Horloges t1 (mitoses traversees) / t2 (dissipations subies) par K4. Tout fidele a la session."""
    def __init__(self, N0=100, seed=1):
        self.beta = BETA; self.tau = TAU; self.kappa = KAPPA
        pts, a0, pool, E0 = build_initial(N0, seed, KAPPA)
        self.pts = [np.array(p) for p in pts]
        self.adj = [set(x) for x in a0]
        self.N = N0
        self.rng = np.random.default_rng(seed * 13)
        self.sweep = 0
        self.t1 = {}; self.t2 = {}; self.born = {}
        self.last_ratios = []

    def Sglob(self):
        d = np.array([len(self.adj[i]) for i in range(self.N)], float)
        D = d.std()/d.mean() if d.mean() > 0 else 0
        return math.log(1 + count_triangles(self.adj, self.N)) - self.beta * D

    def vg_local(self, parent, newp, r=0.32):
        # voisinage LOCAL (parent + ses voisins) pour scaler a grand N
        cand = [parent] + list(self.adj[parent])
        return [i for i in cand if np.linalg.norm(self.pts[i] - newp) < r]

    def step(self, growth=0.12):
        self.sweep += 1
        S = self.Sglob(); tau_eff = self.tau / max(self.N, 1)
        # --- rewiring (terreau) ---
        for _ in range(self.N):
            v = int(self.rng.integers(self.N))
            if not self.adj[v]: continue
            if self.rng.random() < 0.5:
                bb = int(self.rng.integers(self.N))
                if bb == v or bb in self.adj[v] or np.linalg.norm(self.pts[v]-self.pts[bb]) > 0.45: continue
                self.adj[v].add(bb); self.adj[bb].add(v); S2 = self.Sglob(); d = S2 - S
                if d >= 0 or self.rng.random() < math.exp(min(d/tau_eff, 30)): S = S2
                else: self.adj[v].discard(bb); self.adj[bb].discard(v)
            else:
                w = int(list(self.adj[v])[int(self.rng.integers(len(self.adj[v])))])
                if len(self.adj[v]) <= 2 or len(self.adj[w]) <= 2:
                    if not still_connected(self.adj, v, w, self.N): continue
                self.adj[v].discard(w); self.adj[w].discard(v); S2 = self.Sglob(); d = S2 - S
                if d >= 0 or self.rng.random() < math.exp(min(d/tau_eff, 30)): S = S2
                else: self.adj[v].add(w); self.adj[w].add(v)
        # --- MITOSE CONTINUE sans frontiere ---
        n_mit = max(2, int(self.N * growth)); mset = set()
        for _ in range(n_mit):
            parent = int(self.rng.integers(self.N))
            newp = self.pts[parent] + self.rng.normal(0, 0.10, 3)
            vois = self.vg_local(parent, newp)
            self.pts.append(newp); self.adj.append(set()); nid = self.N; self.N += 1
            if len(vois) < 2:
                self.adj[nid].add(parent); self.adj[parent].add(nid); mset.add(parent)
            else:
                knn = sorted(vois, key=lambda i: np.linalg.norm(self.pts[i]-newp))[:int(self.kappa)]
                for w in knn: self.adj[nid].add(w); self.adj[w].add(nid)
                mset |= set(knn)
        # --- horloges t1 (mitoses traversees) ---
        K4 = find_all_K4(self.adj, self.N); cur = set(key(q) for q in K4)
        for q in K4:
            k = key(q)
            if k not in self.born: self.born[k] = self.sweep; self.t1[k] = 0; self.t2[k] = 0
            if mset & set(q): self.t1[k] += 1
        # --- EFFONDREMENT age-dependant (cycle, pas mort) : t2 = dissipations subies ---
        ratios = []
        for q in K4:
            k = key(q); p_eff = 0.236 * math.exp(-max(self.t1.get(k, 0), 0)/8)
            if self.rng.random() < p_eff:
                self.t2[k] = self.t2.get(k, 0) + 1
                i, j = self.rng.choice(4, 2, replace=False); u, w = q[int(i)], q[int(j)]
                if w in self.adj[u] and len(self.adj[u]) > 2 and len(self.adj[w]) > 2 and still_connected(self.adj, u, w, self.N):
                    self.adj[u].discard(w); self.adj[w].discard(u)
        for k in list(self.born):
            if k not in cur:
                t1 = self.t1.get(k, 0); t2 = max(self.t2.get(k, 0), 1); ratios.append(t1/t2)
                del self.born[k]; self.t1.pop(k, None); self.t2.pop(k, None)
        self.last_ratios = ratios

# ----------------------------- MESURE AUX PALIERS (JSON) -----------------------------
def K_metrique(adj, pts, N, rng, k=80):
    """Courbure metrique (deficit angulaire, positions 3D) — INDEPENDANTE du comptage de triangles."""
    vs = rng.choice(N, min(N, k), replace=False); defs = []
    for v in vs:
        nb = list(adj[v])
        if len(nb) < 2: continue
        angs = []; pv = pts[v]
        for i in range(len(nb)):
            for j in range(i+1, len(nb)):
                a = pts[nb[i]] - pv; c = pts[nb[j]] - pv
                na = np.linalg.norm(a); nc = np.linalg.norm(c)
                if na > 1e-9 and nc > 1e-9:
                    cos = np.clip(np.dot(a, c)/(na*nc), -1, 1); angs.append(math.acos(cos))
        if angs: defs.append(2*math.pi - sum(angs)/max(1, len(angs))*len(nb))
    return float(np.mean(defs)) if defs else 0.0

def snapshot(bl, seed):
    N = bl.N; adj = bl.adj; pts = bl.pts; rng = np.random.default_rng(99)
    DI = math.log(1 + count_triangles(adj, N))
    # courbure d'Ollivier moyenne (echantillon)
    edges = [(v, w) for v in rng.choice(N, min(N, 200), replace=False) for w in adj[v] if v < w]
    if len(edges) > 60: edges = [edges[i] for i in rng.choice(len(edges), 60, replace=False)]
    Ko = float(np.mean([ollivier_edge(adj, u, w) for u, w in edges])) if edges else 0.0
    Km = K_metrique(adj, pts, N, rng)
    # SIGNATURE MATIERE : Ric(K4) vs Ric(fond)
    K4 = find_all_K4(adj, N); k4v = set(v for q in K4 for v in q)
    k4e = set()
    for q in K4:
        for i in range(4):
            for j in range(i+1, 4): k4e.add((min(q[i], q[j]), max(q[i], q[j])))
    k4e = list(k4e)
    if len(k4e) > 80: k4e = [k4e[i] for i in rng.choice(len(k4e), 80, replace=False)]
    be = [(v, w) for v in range(N) if v not in k4v for w in adj[v] if v < w]
    if len(be) > 80: be = [be[i] for i in rng.choice(len(be), 80, replace=False)]
    rk = np.array([ollivier_edge(adj, u, w) for u, w in k4e if w in adj[u]])
    rb = np.array([ollivier_edge(adj, u, w) for u, w in be])
    ric_k4 = float(rk.mean()) if len(rk) > 5 else 0.0
    ric_bulk = float(rb.mean()) if len(rb) > 5 else 0.0
    # t de Student matiere vs fond
    if len(rk) > 5 and len(rb) > 5:
        se = math.sqrt(rk.var()/len(rk) + rb.var()/len(rb)); tstat = float((rk.mean()-rb.mean())/se) if se > 0 else 0.0
    else: tstat = 0.0
    R = float(np.mean(bl.last_ratios)) if bl.last_ratios else 0.0
    d = np.array([len(adj[i]) for i in range(N)], float)
    return {
        "N": int(N), "seed": int(seed), "n_K4": len(K4),
        "deg_moy": float(d.mean()),
        "DI_info": float(DI), "K_ollivier_moy": Ko, "K_metrique_moy": Km,
        "Ric_K4": ric_k4, "Ric_fond": ric_bulk, "Ric_K4_moins_fond": ric_k4 - ric_bulk,
        "t_stat_matiere_vs_fond": tstat,
        "ratio_t1_t2_moy": R,
        "sweep": int(bl.sweep), "elapsed_s": round(time.time()-T0, 1)
    }

# ===================================== RUN =====================================
PALIERS = [1000, 2500, 5000, 10000, 15000, 25000]
SEED = 1            # change ici pour multi-seed (1, 2, 3...)
T0 = time.time()
results = []
bl = BlobVivant(N0=100, seed=SEED)
pi = 0
print(f"Demarrage scaling, seed={SEED}, paliers={PALIERS}")
print(f"{'N':>7} {'nK4':>6} {'deg':>5} {'Ric(K4)-fond':>13} {'t-stat':>7} {'DI<->Km(corr cumul)':>5}  {'t(s)':>7}")
# pour la correlation cumulee DI<->K_metrique le long du scaling
serie_DI = []; serie_Km = []
while bl.N < PALIERS[-1]:
    bl.step(growth=0.12)
    # echantillon de serie pour correlation (tous les ~5 sweeps)
    if bl.sweep % 5 == 0:
        rng = np.random.default_rng(bl.sweep)
        serie_DI.append(math.log(1 + count_triangles(bl.adj, bl.N)))
        serie_Km.append(K_metrique(bl.adj, bl.pts, bl.N, rng, k=60))
    if pi < len(PALIERS) and bl.N >= PALIERS[pi]:
        snap = snapshot(bl, SEED)
        # correlation cumulee DI <-> K_metrique (test de non-tautologie au scaling)
        if len(serie_DI) > 4 and np.std(serie_DI) > 0 and np.std(serie_Km) > 0:
            snap["corr_DI_Kmetrique_cumul"] = float(np.corrcoef(serie_DI, serie_Km)[0, 1])
        else:
            snap["corr_DI_Kmetrique_cumul"] = None
        results.append(snap)
        cc = snap.get("corr_DI_Kmetrique_cumul")
        print(f"{snap['N']:>7} {snap['n_K4']:>6} {snap['deg_moy']:>5.2f} "
              f"{snap['Ric_K4_moins_fond']:>+13.3f} {snap['t_stat_matiere_vs_fond']:>7.2f} "
              f"{(cc if cc is not None else 0):>+5.2f}  {snap['elapsed_s']:>7.1f}")
        # ecrire le JSON a CHAQUE palier (au cas ou la session Colab coupe)
        with open(f"blob_scaling_seed{SEED}.json", "w") as f:
            json.dump(results, f, indent=2)
        pi += 1
        while pi < len(PALIERS) and PALIERS[pi] <= bl.N: pi += 1

print(f"\nTermine. JSON ecrit : blob_scaling_seed{SEED}.json")
print(f"Paliers atteints : {[r['N'] for r in results]}")
print("\n=== VERDICT ATTENDU ===")
print("Ric(K4)-fond doit rester POSITIF a tous les paliers (signature matiere robuste).")
print("corr_DI_Kmetrique_cumul doit rester proche de -0.8 (unification info<->geometrie non tautologique).")
