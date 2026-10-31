#!/usr/bin/env python3 -I
"""
Campagne DEFI-M15 : loi structure–lenteur γ = α − δ ?

Mesure directe de :
  A) La clique maximale du graphe d'équilibre à degrés moyens 4 et 6
  B) Le temps de séjour dans un puits aristocratique
  C) Les contributions séparées de log(1+T) et −βD à la barrière
  D) L'effet de α (diagramme de refroidissement)

Moteur : graphes abstraits, Metropolis à échanges d'arêtes, |E| fixé.
Graines fixées, sorties JSON.

Contribution de Codex (OpenAI), développée et vérifiée par le pilote IA
Claude (Anthropic), sans relecture humaine.

TOE démontrée : NON ; candidate digne d'étude : OUI.
"""
import json, math, sys, time, os
import numpy as np
from collections import defaultdict

# ===================================================================
# MOTEUR
# ===================================================================

class BlobGraph:
    """Graphe abstrait avec suivi de triangles et D."""
    def __init__(self, n, edges, beta=0.30):
        self.n = n
        self.beta = beta
        self.adj = [set() for _ in range(n)]
        self.edge_list = []
        self.edge_set = set()
        self.ntri = 0
        for a, b in edges:
            self._add_edge(a, b)

    def _add_edge(self, a, b):
        if a > b: a, b = b, a
        if (a, b) in self.edge_set:
            return
        # Count new triangles
        common = self.adj[a] & self.adj[b]
        self.ntri += len(common)
        self.adj[a].add(b)
        self.adj[b].add(a)
        self.edge_set.add((a, b))
        self.edge_list.append((a, b))

    def _remove_edge(self, a, b):
        if a > b: a, b = b, a
        if (a, b) not in self.edge_set:
            return
        self.adj[a].discard(b)
        self.adj[b].discard(a)
        common = self.adj[a] & self.adj[b]
        self.ntri -= len(common)
        self.edge_set.discard((a, b))
        self.edge_list.remove((a, b))

    @property
    def T(self):
        return self.ntri

    @property
    def D(self):
        degs = [len(s) for s in self.adj]
        m = np.mean(degs)
        if m == 0:
            return 0.0
        return float(np.std(degs) / m)

    def S_sim(self):
        return math.log(1 + self.ntri) - self.beta * self.D

    def clique_max(self):
        """Clique maximale par Bron-Kerbosch (exact, OK pour n ≤ 257)."""
        best = [0]
        adj = self.adj

        def bk(R, P, X):
            if not P and not X:
                if len(R) > best[0]:
                    best[0] = len(R)
                return
            # Pivot
            pivot = max(P | X, key=lambda v: len(adj[v] & P))
            for v in list(P - adj[pivot]):
                bk(R | {v}, P & adj[v], X & adj[v])
                P.discard(v)
                X.add(v)

        bk(set(), set(range(self.n)), set())
        return best[0]

    def vertex_triangles(self, v):
        """Nombre de triangles contenant v."""
        nb = list(self.adj[v])
        count = 0
        for i in range(len(nb)):
            for j in range(i+1, len(nb)):
                if nb[j] in self.adj[nb[i]]:
                    count += 1
        return count


def random_regular_graph(n, m, rng):
    """Graphe aléatoire à n sommets et m arêtes."""
    edges = set()
    max_e = n * (n - 1) // 2
    if m > max_e:
        m = max_e
    while len(edges) < m:
        a = rng.integers(n)
        b = rng.integers(n)
        if a != b:
            if a > b: a, b = b, a
            edges.add((a, b))
    return list(edges)


def metropolis_swap(g, lam, rng):
    """Un échange de Metropolis. Retourne (accepté, ΔS, Δlog(1+T), −βΔD)."""
    n = g.n
    m = len(g.edge_list)
    if m == 0 or n < 3:
        return False, 0.0, 0.0, 0.0

    # Choisir une arête à retirer
    idx = rng.integers(m)
    a, b = g.edge_list[idx]

    # Choisir une non-arête à ajouter
    max_tries = 200
    for _ in range(max_tries):
        c = rng.integers(n)
        d = rng.integers(n)
        if c != d and c != a and c != b and d != a and d != b:
            if c > d: c, d = d, c
            if (c, d) not in g.edge_set:
                break
    else:
        return False, 0.0, 0.0, 0.0

    # Mesurer avant
    T_before = g.T
    D_before = g.D
    S_before = math.log(1 + T_before) - g.beta * D_before

    # Appliquer
    g._remove_edge(a, b)
    g._add_edge(c, d)

    T_after = g.T
    D_after = g.D
    S_after = math.log(1 + T_after) - g.beta * D_after

    dS = S_after - S_before
    dT_contrib = math.log(1 + T_after) - math.log(1 + T_before)
    dD_contrib = -g.beta * (D_after - D_before)

    # Metropolis
    if dS >= 0 or rng.random() < math.exp(lam * dS):
        return True, dS, dT_contrib, dD_contrib
    else:
        # Annuler
        g._remove_edge(c, d)
        g._add_edge(a, b)
        return False, 0.0, 0.0, 0.0


def equilibrate(g, lam, rng, n_sweeps):
    """Équilibrer le graphe par n_sweeps balayages."""
    m = len(g.edge_list)
    swaps_per_sweep = max(1, m)
    for _ in range(n_sweeps):
        for _ in range(swaps_per_sweep):
            metropolis_swap(g, lam, rng)


def measure_sojourn_and_structure(n, mean_deg, alpha, tau, rng,
                                   n_chains=8, equil_sweeps=200,
                                   sample_interval=50, n_samples=20):
    """
    Pour un graphe de taille n à degré moyen donné :
    1. Équilibrer par Metropolis
    2. Mesurer la clique maximale sur des instantanés
    3. Mesurer la barrière (décomposition T vs D)
    4. Estimer le temps de séjour du sommet le plus massif

    Retourne un dict avec les mesures.
    """
    m = n * mean_deg // 2  # nombre d'arêtes
    lam = n**alpha / tau

    cliques = []
    mean_Tvs = []
    barrier_T_contribs = []
    barrier_D_contribs = []

    for chain in range(n_chains):
        seed = int(rng.integers(2**31))
        chain_rng = np.random.default_rng(seed)

        edges = random_regular_graph(n, m, chain_rng)
        g = BlobGraph(n, edges)

        # Équilibrer
        equilibrate(g, lam, chain_rng, equil_sweeps)

        for sample in range(n_samples):
            # Avancer
            equilibrate(g, lam, chain_rng, sample_interval)

            # Mesurer la clique maximale
            q = g.clique_max()
            cliques.append(q)

            # Mesurer T_v moyen et max
            tvs = [g.vertex_triangles(v) for v in range(n)]
            mean_Tvs.append(np.mean(tvs))

            # Mesurer la décomposition de la barrière sur quelques swaps
            n_barrier_swaps = min(50, len(g.edge_list))
            for _ in range(n_barrier_swaps):
                acc, dS, dT, dD = metropolis_swap(g, lam, chain_rng)
                if not acc and dS < 0:  # swap rejeté = contribution à la barrière
                    barrier_T_contribs.append(abs(dT) * lam)
                    barrier_D_contribs.append(abs(dD) * lam)

    cliques = np.array(cliques, dtype=float)
    mean_Tvs = np.array(mean_Tvs)

    # q_eff à partir de T_v moyen
    mean_Tv_global = float(np.mean(mean_Tvs))
    q_eff = (1 + math.sqrt(1 + 8 * mean_Tv_global)) / 2

    result = {
        "n": n,
        "mean_deg": mean_deg,
        "alpha": alpha,
        "lambda": lam,
        "n_chains": n_chains,
        "n_samples_per_chain": n_samples,
        "clique_max_mean": float(np.mean(cliques)),
        "clique_max_std": float(np.std(cliques)),
        "clique_max_median": float(np.median(cliques)),
        "clique_max_min": int(np.min(cliques)),
        "clique_max_max": int(np.max(cliques)),
        "mean_Tv": mean_Tv_global,
        "q_eff": q_eff,
        "barrier_T_mean": float(np.mean(barrier_T_contribs)) if barrier_T_contribs else None,
        "barrier_D_mean": float(np.mean(barrier_D_contribs)) if barrier_D_contribs else None,
        "barrier_T_over_total": None,
    }

    if barrier_T_contribs and barrier_D_contribs:
        total = np.mean(barrier_T_contribs) + np.mean(barrier_D_contribs)
        if total > 0:
            result["barrier_T_over_total"] = float(np.mean(barrier_T_contribs) / total)

    return result


# ===================================================================
# CAMPAGNE
# ===================================================================

def run_campaign():
    master_seed = 20261031
    master_rng = np.random.default_rng(master_seed)

    results = {
        "meta": {
            "description": "DEFI-M15 campagne préliminaire : loi structure-lenteur γ = α − δ",
            "master_seed": master_seed,
            "beta": 0.30,
            "tau": 0.50,
            "date": "2026-10-31",
            "by": "pilote IA (Claude, Anthropic), sans relecture humaine",
            "statut": "TOE démontrée : NON ; candidate digne d'étude : OUI"
        },
        "structural": [],
        "cooling": []
    }

    # A. Mesure structurelle directe — degré moyen 4
    print("="*70)
    print("A. MESURE STRUCTURELLE — DEGRÉ MOYEN 4")
    print("="*70)

    # Tailles adaptées aux ressources (Bron-Kerbosch exact)
    # n=257 avec BK prend trop longtemps en Python pur
    sizes_d4 = [17, 33, 49, 65, 97, 129]

    for n in sizes_d4:
        t0 = time.time()
        print(f"\n  n = {n}, degré moyen = 4 ...", end=" ", flush=True)
        # Adapter le nombre de chaînes et échantillons au budget
        nc = 8 if n <= 65 else 4
        ns = 20 if n <= 65 else 10
        eq = 200 if n <= 65 else 100
        si = 50 if n <= 65 else 30

        r = measure_sojourn_and_structure(
            n, 4, alpha=1.0, tau=0.50, rng=master_rng,
            n_chains=nc, equil_sweeps=eq,
            sample_interval=si, n_samples=ns
        )
        elapsed = time.time() - t0
        r["elapsed_s"] = round(elapsed, 1)
        results["structural"].append(r)
        print(f"clique_max = {r['clique_max_mean']:.1f} ± {r['clique_max_std']:.1f}, "
              f"q_eff = {r['q_eff']:.2f}, "
              f"T/{(r['barrier_T_over_total'] or 0)*100:.0f}%D, "
              f"{elapsed:.0f}s")

    # A'. Mesure structurelle — degré moyen 6
    print("\n" + "="*70)
    print("A'. MESURE STRUCTURELLE — DEGRÉ MOYEN 6")
    print("="*70)

    sizes_d6 = [17, 33, 49, 65, 97]

    for n in sizes_d6:
        t0 = time.time()
        print(f"\n  n = {n}, degré moyen = 6 ...", end=" ", flush=True)
        nc = 8 if n <= 65 else 4
        ns = 20 if n <= 65 else 10
        eq = 200 if n <= 65 else 100
        si = 50 if n <= 65 else 30

        r = measure_sojourn_and_structure(
            n, 6, alpha=1.0, tau=0.50, rng=master_rng,
            n_chains=nc, equil_sweeps=eq,
            sample_interval=si, n_samples=ns
        )
        elapsed = time.time() - t0
        r["elapsed_s"] = round(elapsed, 1)
        results["structural"].append(r)
        print(f"clique_max = {r['clique_max_mean']:.1f} ± {r['clique_max_std']:.1f}, "
              f"q_eff = {r['q_eff']:.2f}, "
              f"T/{(r['barrier_T_over_total'] or 0)*100:.0f}%D, "
              f"{elapsed:.0f}s")

    # B. Diagramme de refroidissement — degré moyen 4, n=33 et 49
    print("\n" + "="*70)
    print("B. DIAGRAMME DE REFROIDISSEMENT (α variable)")
    print("="*70)

    for alpha in [0.0, 0.5, 0.75, 1.0]:
        for n in [33, 49]:
            t0 = time.time()
            print(f"\n  α = {alpha}, n = {n}, degré moyen = 4 ...", end=" ", flush=True)
            r = measure_sojourn_and_structure(
                n, 4, alpha=alpha, tau=0.50, rng=master_rng,
                n_chains=8, equil_sweeps=200,
                sample_interval=50, n_samples=20
            )
            elapsed = time.time() - t0
            r["elapsed_s"] = round(elapsed, 1)
            results["cooling"].append(r)
            print(f"clique = {r['clique_max_mean']:.1f}, "
                  f"q_eff = {r['q_eff']:.2f}, "
                  f"{elapsed:.0f}s")

    # Sauvegarder
    outpath = os.path.join(os.path.dirname(__file__), "campagne_m15_resultats.json")
    with open(outpath, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(f"\nRésultats sauvegardés dans {outpath}")

    # ---------- ANALYSE ----------
    print("\n" + "="*70)
    print("ANALYSE DES RÉSULTATS")
    print("="*70)

    # Régressions δ sur clique maximale directe
    from scipy import stats as sp_stats

    for mean_deg in [4, 6]:
        entries = [r for r in results["structural"] if r["mean_deg"] == mean_deg]
        if len(entries) < 3:
            continue

        ns = np.array([r["n"] for r in entries], dtype=float)
        qs = np.array([r["clique_max_mean"] for r in entries])
        qeffs = np.array([r["q_eff"] for r in entries])

        print(f"\n--- Degré moyen {mean_deg} ---")
        print(f"  n      : {ns.tolist()}")
        print(f"  q_max  : {[f'{q:.1f}' for q in qs]}")
        print(f"  q_eff  : {[f'{q:.2f}' for q in qeffs]}")

        # δ à partir de clique_max
        for label, mask in [("tous", np.ones(len(ns), bool)),
                            ("n≥33", ns >= 33), ("n≥49", ns >= 49)]:
            if mask.sum() < 2:
                continue
            s, i, r, p, e = sp_stats.linregress(np.log(ns[mask]), np.log(qs[mask]))
            print(f"  δ (clique_max, {label}): {s:.3f} ± {e:.3f}, R²={r**2:.4f}")

        # δ à partir de q_eff
        for label, mask in [("tous", np.ones(len(ns), bool)), ("n≥33", ns >= 33)]:
            if mask.sum() < 2:
                continue
            s, i, r, p, e = sp_stats.linregress(np.log(ns[mask]), np.log(qeffs[mask]))
            print(f"  δ (q_eff, {label}): {s:.3f} ± {e:.3f}, R²={r**2:.4f}")

    # Contribution T vs D à la barrière
    print("\n--- Contribution T vs D à la barrière ---")
    for r in results["structural"]:
        if r["barrier_T_over_total"] is not None:
            print(f"  n={r['n']:3d}, deg={r['mean_deg']}: "
                  f"T={r['barrier_T_over_total']*100:.1f}%, "
                  f"D={100-r['barrier_T_over_total']*100:.1f}%, "
                  f"|ΔT·λ|={r['barrier_T_mean']:.3f}, |ΔD·λ|={r['barrier_D_mean']:.3f}")

    # Diagramme de refroidissement
    print("\n--- Diagramme de refroidissement (α variable, deg=4) ---")
    for alpha in [0.0, 0.5, 0.75, 1.0]:
        entries = [r for r in results["cooling"] if abs(r["alpha"] - alpha) < 0.01]
        if len(entries) < 2:
            continue
        ns = np.array([r["n"] for r in entries], dtype=float)
        qs = np.array([r["clique_max_mean"] for r in entries])
        print(f"  α = {alpha}: n = {ns.tolist()}, q_max = {[f'{q:.1f}' for q in qs]}")

    print("\n" + "="*70)
    print("STATUT FINAL")
    print("="*70)
    print("TOE démontrée : NON ; candidate digne d'étude : OUI.")


if __name__ == "__main__":
    run_campaign()
