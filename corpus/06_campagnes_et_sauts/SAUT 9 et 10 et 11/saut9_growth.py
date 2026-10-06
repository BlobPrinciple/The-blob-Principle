"""
BLOB PRINCIPLE — Saut 9 : Cartographie fine de la transition N* = 2500
=======================================================================
Protocole : croissance par mitose (Blob 2.0), identique à Saut 3.5v4.
Paliers fins autour de N* : {2000, 2200, 2500, 2800, 3000}
3 seeds par palier | 5M pas MCMC par palier
Mesures : ntri, ntetra, r3, Phi, Q3, SE, distribution P(ntetra)
Output  : saut9_results.json + saut9_distributions.json
"""

import random
import math
import json
import time
import collections

# ─── Paramètres Blob ────────────────────────────────────────────────────────
KAPPA_0   = 8        # degré moyen cible
BETA      = 0.30     # poids dissipation dans Ssim
TAU       = 0.50     # température MCMC
RCP_COORD = 8.1915   # coordinence Bernal (pour alpha_Blob)

# ─── Paramètres Saut 9 ──────────────────────────────────────────────────────
N_TARGETS  = [2000, 2200, 2500, 2800, 3000]   # paliers fins autour de N*
N_SEEDS    = 3
STEPS_PER_NODE = 1000          # pas MCMC par nœud ajouté (calibré sur Saut 3.5v4)
SNAPSHOT_EVERY = 100           # snapshot tous les 100 nœuds pour distribution P(ntetra)

# ─── Structures de données ───────────────────────────────────────────────────

class BlobGraph:
    """Graphe simplexial Blob avec comptage ntri/ntetra et calcul Phi/Q3."""

    def __init__(self, seed):
        random.seed(seed)
        self.seed = seed
        # Initialisation : graphe complet K_4 (4 nœuds, 6 arêtes, 4 triangles, 1 tétraèdre)
        self.N = 4
        self.adj = {i: set() for i in range(4)}
        for i in range(4):
            for j in range(i+1, 4):
                self.adj[i].add(j)
                self.adj[j].add(i)

        # Compteurs de simplexes
        self.triangles  = set()   # frozensets de 3
        self.tetrahedra = set()   # frozensets de 4
        self._rebuild_simplices()

        # Historique pour Q3 (dissipation cumulée)
        self.Q3_history = []      # liste de D à chaque step
        self.Phi_history = []     # liste de Phi (transitions tétra)
        self.step_count  = 0

    def _rebuild_simplices(self):
        """Recompte triangles et tétraèdres depuis l'adjacence."""
        self.triangles  = set()
        self.tetrahedra = set()
        nodes = list(self.adj.keys())
        for i in range(len(nodes)):
            ni = nodes[i]
            for j in range(i+1, len(nodes)):
                nj = nodes[j]
                if nj not in self.adj[ni]: continue
                for k in range(j+1, len(nodes)):
                    nk = nodes[k]
                    if nk not in self.adj[ni] or nk not in self.adj[nj]: continue
                    self.triangles.add(frozenset([ni,nj,nk]))
                    for l in range(k+1, len(nodes)):
                        nl = nodes[l]
                        if (nl in self.adj[ni] and nl in self.adj[nj]
                                and nl in self.adj[nk]):
                            self.tetrahedra.add(frozenset([ni,nj,nk,nl]))

    def _count_simplices_fast(self, u, v):
        """Compte les triangles et tétraèdres contenant l'arête (u,v)."""
        common2 = self.adj[u] & self.adj[v]
        tri_uv  = len(common2)
        tetra_uv = 0
        common2_list = list(common2)
        for i in range(len(common2_list)):
            w = common2_list[i]
            common3 = (self.adj[u] & self.adj[v] & self.adj[w]) - {u, v, w}
            tetra_uv += len(common3)
        tetra_uv //= 1  # chaque tétraèdre compté une fois par arête
        return tri_uv, tetra_uv

    def D(self):
        """Dissipation D = ntri / (ntri + ntetra + 1)."""
        nt  = len(self.triangles)
        nte = len(self.tetrahedra)
        return nt / (nt + nte + 1)

    def Ssim(self):
        """Score de viabilité Ssim = log(1+ntri) - beta*D."""
        return math.log(1 + len(self.triangles)) - BETA * self.D()

    def SE(self):
        """Entropie simplexiale SE = -N*Ssim/tau."""
        return -self.N * self.Ssim() / TAU

    def edges(self):
        return sum(len(v) for v in self.adj.values()) // 2

    def r3(self):
        nt  = len(self.triangles)
        nte = len(self.tetrahedra)
        return nte / nt if nt > 0 else 0.0

    def mcmc_step(self):
        """
        Un pas MCMC Metropolis-Hastings : swap d'arête.
        Choisit une arête (u,v), un nœud w non adjacent à u,
        propose de déplacer v→w (swap : retire (u,v), ajoute (u,w)).
        Accepte selon exp(N*ΔSsim/tau).
        """
        nodes = list(self.adj.keys())
        # Choisir une arête au hasard
        u = random.choice(nodes)
        if not self.adj[u]:
            return
        v = random.choice(list(self.adj[u]))

        # Cible : nœud non adjacent à u (autre que u lui-même)
        non_adj = [w for w in nodes if w != u and w not in self.adj[u]]
        if not non_adj:
            return
        w = random.choice(non_adj)

        # Calculer ΔSsim
        S_before = self.Ssim()
        # Appliquer le swap temporairement
        self.adj[u].remove(v)
        self.adj[v].remove(u)
        self.adj[u].add(w)
        self.adj[w].add(u)
        # Recompter simplexes affectés (rapide : seulement autour de u)
        # Pour la rigueur, on recompte tout (plus lent mais correct)
        self._rebuild_simplices()
        S_after = self.Ssim()

        # Acceptation MH
        delta = self.N * (S_after - S_before) / TAU
        if delta < 0 and random.random() > math.exp(delta):
            # Rejeter : annuler le swap
            self.adj[u].remove(w)
            self.adj[w].remove(u)
            self.adj[u].add(v)
            self.adj[v].add(u)
            self._rebuild_simplices()

        # Enregistrer D pour Q3
        d_now = self.D()
        self.Q3_history.append(d_now)
        self.step_count += 1

    def grow_to(self, N_target, steps_per_node=STEPS_PER_NODE,
                snapshot_every=SNAPSHOT_EVERY, verbose=True):
        """
        Croissance par mitose jusqu'à N_target.
        À chaque ajout de nœud : connecter à KAPPA_0 voisins aléatoires,
        puis faire steps_per_node pas MCMC.
        Retourne snapshots de (N, ntri, ntetra, r3, D, SE) tous les snapshot_every nœuds.
        """
        snapshots = []
        prev_tetra = len(self.tetrahedra)

        while self.N < N_target:
            # ── Mitose : ajouter un nœud ────────────────────────────────
            new_node = max(self.adj.keys()) + 1
            self.adj[new_node] = set()
            self.N += 1

            # Connecter à min(KAPPA_0, N-1) voisins existants
            existing = [n for n in self.adj.keys() if n != new_node]
            k = min(KAPPA_0, len(existing))
            targets = random.sample(existing, k)
            for t in targets:
                self.adj[new_node].add(t)
                self.adj[t].add(new_node)

            self._rebuild_simplices()

            # ── MCMC ────────────────────────────────────────────────────
            for _ in range(steps_per_node):
                self.mcmc_step()

            # ── Phi (friction tétraédrique) ─────────────────────────────
            curr_tetra = len(self.tetrahedra)
            delta_tetra = abs(curr_tetra - prev_tetra)
            self.Phi_history.append(delta_tetra)
            prev_tetra = curr_tetra

            # ── Snapshot ────────────────────────────────────────────────
            if self.N % snapshot_every == 0 or self.N == N_target:
                snap = {
                    "N":      self.N,
                    "ntri":   len(self.triangles),
                    "ntetra": len(self.tetrahedra),
                    "r3":     self.r3(),
                    "D":      self.D(),
                    "SE":     self.SE(),
                    "edges":  self.edges(),
                }
                snapshots.append(snap)
                if verbose and self.N % 200 == 0:
                    print(f"  N={self.N:5d}  ntri={snap['ntri']:6d}  "
                          f"ntetra={snap['ntetra']:6d}  r3={snap['r3']:.4f}  "
                          f"D={snap['D']:.4f}")

        return snapshots

    def final_metrics(self):
        """Métriques finales du palier."""
        Q3 = sum(self.Q3_history)
        Phi = sum(self.Phi_history)
        nte = len(self.tetrahedra)
        nt  = len(self.triangles)
        return {
            "N":        self.N,
            "edges":    self.edges(),
            "ntri":     nt,
            "ntetra":   nte,
            "r3":       self.r3(),
            "D":        self.D(),
            "SE":       self.SE(),
            "Ssim":     self.Ssim(),
            "Q3":       Q3,
            "Phi":      Phi,
            "Phi_over_Q3": Phi / Q3 if Q3 > 0 else None,   # ← Saut 10 preview
            "steps":    self.step_count,
        }


# ─── Calcul alpha_Blob ───────────────────────────────────────────────────────

def compute_alpha_blob(D_val, ds=3.0):
    """
    alpha_Blob = K^3 / kappa_RCP
    K = D * (ds / 3)
    """
    K = D_val * (ds / 3.0)
    alpha = (K ** 3) / RCP_COORD
    alpha_codata = 1 / 137.035999084
    rel_err = abs(alpha - alpha_codata) / alpha_codata
    return {
        "K":          K,
        "alpha_Blob": alpha,
        "alpha_CODATA": alpha_codata,
        "relative_error": rel_err,
        "stable":     rel_err < 0.01,   # critère : <1% d'écart
    }


# ─── Null model ──────────────────────────────────────────────────────────────

def null_model_metrics(N, n_samples=1000, seed=42):
    """
    Modèle Null : graphe aléatoire E=4N-4, pas de biais MCMC.
    Comptage moyen de ntri et ntetra sur n_samples réalisations.
    """
    rng = random.Random(seed)
    ntri_list, ntetra_list = [], []
    E = 4 * N - 4

    for _ in range(n_samples):
        nodes = list(range(N))
        adj = {i: set() for i in range(N)}
        edges_added = 0
        while edges_added < E:
            u, v = rng.sample(nodes, 2)
            if v not in adj[u]:
                adj[u].add(v); adj[v].add(u)
                edges_added += 1

        # Comptage rapide
        nt = 0; nte = 0
        for i in nodes:
            for j in list(adj[i]):
                if j <= i: continue
                common = adj[i] & adj[j]
                nt += len(common)
                for k in common:
                    if k <= j: continue
                    nte += len(adj[i] & adj[j] & adj[k])
        ntri_list.append(nt // 1)
        ntetra_list.append(nte // 1)

    return {
        "N": N,
        "null_ntri_mean":   sum(ntri_list)/len(ntri_list),
        "null_ntetra_mean": sum(ntetra_list)/len(ntetra_list),
        "null_ntri_std":    (sum((x-sum(ntri_list)/len(ntri_list))**2
                             for x in ntri_list)/len(ntri_list))**0.5,
    }


# ─── Main ────────────────────────────────────────────────────────────────────

def run_saut9():
    print("=" * 60)
    print("BLOB PRINCIPLE — Saut 9 : Transition N* = 2500")
    print("=" * 60)

    results      = []    # résultats par palier + seed
    distributions = {}   # P(ntetra) : snapshots fins

    t0_global = time.time()

    for N_target in N_TARGETS:
        print(f"\n{'─'*50}")
        print(f"PALIER N = {N_target}")
        print(f"{'─'*50}")

        palier_results = []
        snapshots_all  = []

        for seed in range(N_SEEDS):
            print(f"\n  Seed {seed+1}/{N_SEEDS}")
            t0 = time.time()

            blob = BlobGraph(seed=seed * 1000 + N_target)
            snaps = blob.grow_to(
                N_target,
                steps_per_node=STEPS_PER_NODE,
                snapshot_every=SNAPSHOT_EVERY,
                verbose=True,
            )
            metrics = blob.final_metrics()
            alpha   = compute_alpha_blob(metrics["D"])

            elapsed = time.time() - t0
            metrics["seed"]          = seed
            metrics["N_target"]      = N_target
            metrics["time_sec"]      = elapsed
            metrics["alpha_Blob"]    = alpha
            palier_results.append(metrics)
            snapshots_all.extend(snaps)

            print(f"  → ntri={metrics['ntri']}  ntetra={metrics['ntetra']}  "
                  f"r3={metrics['r3']:.4f}  Q3={metrics['Q3']:.1f}  "
                  f"Phi={metrics['Phi']:.1f}  α={alpha['alpha_Blob']:.6f}  "
                  f"({elapsed:.1f}s)")

        # Statistiques inter-seeds
        r3s    = [r["r3"]    for r in palier_results]
        nts    = [r["ntri"]  for r in palier_results]
        ntes   = [r["ntetra"] for r in palier_results]
        Q3s    = [r["Q3"]    for r in palier_results]
        Phis   = [r["Phi"]   for r in palier_results]
        alphas = [r["alpha_Blob"]["alpha_Blob"] for r in palier_results]

        def mean(x): return sum(x)/len(x)
        def std(x):
            m = mean(x)
            return (sum((xi-m)**2 for xi in x)/len(x))**0.5
        def cv(x): return std(x)/mean(x)*100 if mean(x)!=0 else None

        summary = {
            "N_target":     N_target,
            "seeds":        N_SEEDS,
            "r3_mean":      mean(r3s),   "r3_std":   std(r3s),   "r3_cv":   cv(r3s),
            "ntri_mean":    mean(nts),   "ntri_std": std(nts),
            "ntetra_mean":  mean(ntes),  "ntetra_std": std(ntes), "ntetra_cv": cv(ntes),
            "Q3_mean":      mean(Q3s),   "Q3_std":   std(Q3s),
            "Phi_mean":     mean(Phis),  "Phi_std":  std(Phis),
            "alpha_mean":   mean(alphas),"alpha_std": std(alphas),
            "alpha_codata": 1/137.035999084,
            "alpha_stable": std(alphas)/mean(alphas)*100 < 1.0 if mean(alphas)!=0 else False,
            "per_seed":     palier_results,
        }
        results.append(summary)
        distributions[str(N_target)] = snapshots_all

        print(f"\n  RÉSUMÉ N={N_target}:")
        print(f"    r3   = {mean(r3s):.4f} ± {std(r3s):.4f}  (CV={cv(r3s):.1f}%)")
        print(f"    ntetra = {mean(ntes):.1f} ± {std(ntes):.1f}  (CV={cv(ntes):.1f}%)")
        print(f"    Q3   = {mean(Q3s):.1f} ± {std(Q3s):.1f}")
        print(f"    Phi  = {mean(Phis):.1f} ± {std(Phis):.1f}")
        print(f"    α    = {mean(alphas):.6f} ± {std(alphas):.6f}  "
              f"({'STABLE' if summary['alpha_stable'] else 'VARIABLE'})")

    # Analyse transition : trouver N* = argmax(r3_mean)
    print(f"\n{'='*60}")
    print("ANALYSE TRANSITION N*")
    print(f"{'='*60}")
    r3_means = [(r["N_target"], r["r3_mean"]) for r in results]
    N_star_est = max(r3_means, key=lambda x: x[1])
    print(f"  r3 par palier : {[(n,f'{r:.4f}') for n,r in r3_means]}")
    print(f"  N* estimé = {N_star_est[0]}  (r3_max = {N_star_est[1]:.4f})")

    total_time = (time.time() - t0_global) / 60
    print(f"\nTemps total : {total_time:.1f} min")

    # Sauvegarde
    output = {
        "config":    "Saut 9 — Cartographie fine N*",
        "N_targets": N_TARGETS,
        "N_seeds":   N_SEEDS,
        "steps_per_node": STEPS_PER_NODE,
        "N_star_estimated": N_star_est[0],
        "r3_max_estimated": N_star_est[1],
        "total_time_min": total_time,
        "results":   results,
    }
    with open("saut9_results.json", "w") as f:
        json.dump(output, f, indent=2)
    with open("saut9_distributions.json", "w") as f:
        json.dump(distributions, f, indent=2)

    print("\nFichiers écrits : saut9_results.json | saut9_distributions.json")
    return output


if __name__ == "__main__":
    run_saut9()
