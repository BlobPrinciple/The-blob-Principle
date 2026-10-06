#!/usr/bin/env python3
# ============================================================================
#  blob_germe_colab.py  —  SUITE AUTONOME « GERME CRITIQUE DE STRAUSS »
#  Programme Blob Principle — R. Mirante — méthode corde de rappel
#
#  OBJET (pré-enregistré). La mesure grand-canonique du Blob présente une
#  transition de phase du 1er ordre (condensation de Strauss) : deux phases,
#  sparse (= Blob viable, triangulé, d=3) et dense (= condensé, non structuré).
#  À un tel bord, il existe un GERME CRITIQUE k* : un noyau dense de k < k*
#  sommets FOND (retour au sparse), un noyau de k > k* CROÎT (bascule dense).
#
#  QUESTION DÉCISIVE. À γ fixé (distance fixe au bord), k*(N) est-il
#    (a) INTRINSÈQUE  : k* ~ const en N   -> échelle combinatoire engendrée par
#        la dynamique elle-même (structure exacte requise par l'« Action 2 » /
#        Verrou #1 pour faire émerger une longueur — candidat mécanisme l_P) ;
#    (b) EXTENSIF     : k* ~ N            -> pas d'échelle intrinsèque, voie
#        fermée (on le grave aussi : un [FAIL] honnête vaut un [T]).
#
#  Le script ne prédit PAS la valeur de k*. Il rend le RATIO k*(N_grand)/k*(N_petit)
#  et le compare à 1 (intrinsèque) vs (N_grand/N_petit) (extensif). Rasoir forward.
#
#  Autonome : ne dépend d'aucun module Blob. Colab/CPU. numpy seul requis.
# ============================================================================

import json, math, time, random
import numpy as np
from scipy.spatial import cKDTree

# ----------------------------------------------------------------------------
#  CONFIG  (éditer ici sur Colab)
# ----------------------------------------------------------------------------
PRESET = "full"          # "quick" (~qq min) ou "full" (campagne, plus long)
KAPPA  = 6.6             # degré moyen cible du pool via r ; point de travail C3
BETA   = 0.30            # coeff dispersion de l'action S = log(1+n_tri) - BETA*CV - (gamma)E/N
TAU    = 0.50            # tau_eff = TAU/N
POOL_MULT = 1.6          # rayon pool = POOL_MULT * r (degré pool ~ 22.6)

if PRESET == "quick":
    N_LIST      = [600, 1200]
    GAMMA_LIST  = [0.46, 0.44]        # près de la ligne localisée (0.40 ; 0.48)
    SEEDS       = [1, 2]
    BURN_SPARSE = 20
    PROD_SWEEPS = 60
    K_GRID      = [15, 30, 60, 120, 240]
else:  # full
    N_LIST      = [600, 1200, 2400]
    # fenêtre de coexistence MESURÉE (3 juil.) : spinodale sparse ~0.40, sparse stable ~0.45.
    # k* fini et mesurable à l'intérieur ; ajuster si la ligne bouge au point de travail.
    GAMMA_LIST  = [0.44, 0.42, 0.41]
    SEEDS       = [1, 2, 3]
    BURN_SPARSE = 40
    PROD_SWEEPS = 140
    K_GRID      = [10, 20, 40, 80, 160, 320, 480]

# seuil de pente (normalisée /N /sweep) séparant croissance / fonte / quasi-critique
SLOPE_EPS = 0.010

# ----------------------------------------------------------------------------
#  MOTEUR AUTONOME  (RGG sur cube [0,1]^3 à bord, non périodique)
# ----------------------------------------------------------------------------
def build_pool(N, seed, kappa=KAPPA, pool_mult=POOL_MULT):
    rng = np.random.default_rng(seed)
    pts = rng.random((N, 3))
    r = (3.0 * kappa / (4.0 * math.pi * N)) ** (1.0 / 3.0)
    tree = cKDTree(pts)
    pairs = tree.query_pairs(r=pool_mult * r, output_type='ndarray')
    pool = [(int(a), int(b)) for a, b in pairs]  # liste d'arêtes candidates
    # graphe initial : sous-ensemble donnant ~degré kappa (mêmes règles que le moteur)
    # on prend les paires du rayon r (et non pool_mult*r) comme germe sparse
    init_pairs = tree.query_pairs(r=r, output_type='ndarray')
    adj = [set() for _ in range(N)]
    for a, b in init_pairs:
        adj[int(a)].add(int(b)); adj[int(b)].add(int(a))
    return pts, adj, pool

def count_triangles(adj, N):
    t = 0
    for i in range(N):
        Ni = adj[i]
        for j in Ni:
            if j > i:
                t += len(Ni & adj[j])
    return t // 1  # chaque triangle compté une fois par ce schéma (i<j, communs)

def n_tri_full(adj, N):
    # comptage exact : nombre de triangles = (1/3) sum_i C(voisins fermés)
    t = 0
    for i in range(N):
        Ni = adj[i]
        for j in Ni:
            if j > i:
                t += len(Ni & adj[j])
    return t // 3

# ----------------------------------------------------------------------------
#  MCMC grand-canonique + ensemencement de germe + critère de croissance
# ----------------------------------------------------------------------------
def growth_rate(N, seed, gamma, k_seed,
                burn_sparse=BURN_SPARSE, prod=PROD_SWEEPS, kappa=KAPPA):
    """Équilibre la phase sparse, ensemence un germe dense de k_seed sommets,
       puis mesure la PENTE de E(sweep) sur les 2/3 finaux de la production,
       normalisée /N. Retourne (slope_norm, E_sparse, E_seeded, E_end, traj)."""
    pts, adj, pool = build_pool(N, seed, kappa)
    rng = random.Random(seed * 7919 + 101 * k_seed + int(1000 * gamma))
    pool_set = set((min(a, b), max(a, b)) for a, b in pool)
    pool_list = list(pool_set)
    present = set((min(i, b), max(i, b)) for i in range(N) for b in adj[i] if b > i)
    present_list = list(present); pos = {e: q for q, e in enumerate(present_list)}
    absent_list = [e for e in pool_list if e not in present]
    apos = {e: q for q, e in enumerate(absent_list)}
    n_tri = n_tri_full(adj, N)
    tau_eff = TAU / N
    degs = np.array([len(adj[i]) for i in range(N)], dtype=float)
    S_of = lambda nt, cv, E: math.log(1.0 + nt) - BETA * cv - gamma * E / N
    E = len(present_list)
    S_curr = S_of(n_tri, float(degs.std() / (degs.mean() + 1e-8)), E)

    def sp(l, p, e):
        i = p[e]; x = l[-1]; l[i] = x; p[x] = i; l.pop(); del p[e]
    def ph(l, p, e):
        p[e] = len(l); l.append(e)

    def sweep():
        nonlocal n_tri, S_curr, E
        for _ in range(N):
            if rng.random() < 0.5 and absent_list:               # AJOUT
                e = absent_list[rng.randrange(len(absent_list))]; a, b = e
                tg = len(adj[a] & adj[b])
                degs[a] += 1; degs[b] += 1
                Sn = S_of(n_tri + tg, float(degs.std() / (degs.mean() + 1e-8)), E + 1)
                if Sn - S_curr >= 0 or rng.random() < math.exp(min(0.0, (Sn - S_curr) / tau_eff)):
                    adj[a].add(b); adj[b].add(a); n_tri += tg; S_curr = Sn; E += 1
                    sp(absent_list, apos, e); ph(present_list, pos, e)
                else:
                    degs[a] -= 1; degs[b] -= 1
            elif present_list:                                   # SUPPRESSION
                e = present_list[rng.randrange(len(present_list))]; a, b = e
                if len(adj[a]) <= 1 or len(adj[b]) <= 1:
                    continue
                tl = len(adj[a] & adj[b])
                degs[a] -= 1; degs[b] -= 1
                Sn = S_of(n_tri - tl, float(degs.std() / (degs.mean() + 1e-8)), E - 1)
                if Sn - S_curr >= 0 or rng.random() < math.exp(min(0.0, (Sn - S_curr) / tau_eff)):
                    adj[a].discard(b); adj[b].discard(a); n_tri -= tl; S_curr = Sn; E -= 1
                    sp(present_list, pos, e); ph(absent_list, apos, e)
                else:
                    degs[a] += 1; degs[b] += 1

    # 1) équilibrer la phase sparse
    for _ in range(burn_sparse):
        sweep()
    E_sparse = E

    # 2) ensemencer un germe dense : k_seed sommets spatialement contigus,
    #    on ajoute TOUTES les arêtes du pool internes non présentes
    if k_seed > 0:
        c = rng.randrange(N)
        d2 = np.sum((pts - pts[c]) ** 2, axis=1)
        idx = [int(x) for x in np.argsort(d2)[:k_seed]]
        idxs = set(idx)
        for a in idx:
            for b in idx:
                if b > a and (a, b) in pool_set and b not in adj[a]:
                    adj[a].add(b); adj[b].add(a)
                    degs[a] += 1; degs[b] += 1
                    e = (a, b); sp(absent_list, apos, e); ph(present_list, pos, e)
                    E += 1
        n_tri = n_tri_full(adj, N)
        S_curr = S_of(n_tri, float(degs.std() / (degs.mean() + 1e-8)), E)
    E_seeded = E

    # 3) production : trajectoire de E
    traj = np.empty(prod)
    for s in range(prod):
        sweep()
        traj[s] = E

    # pente sur les 2/3 finaux (rejet du transitoire d'installation du germe)
    start = prod // 3
    xs = np.arange(prod - start)
    ys = traj[start:]
    slope = float(np.polyfit(xs, ys, 1)[0]) if len(xs) > 2 else 0.0
    slope_norm = slope / N
    return slope_norm, E_sparse, E_seeded, float(traj[-1]), traj

def classify(slope_norm, eps=SLOPE_EPS):
    if slope_norm > eps:  return +1   # CROÎT -> nucléation vers dense
    if slope_norm < -eps: return -1   # FOND  -> retour sparse
    return 0                          # quasi-critique (près de k*)

# ----------------------------------------------------------------------------
#  Recherche de k* par balayage (le plus petit k qui CROÎT de façon robuste)
# ----------------------------------------------------------------------------
def find_kstar(N, gamma, seeds=SEEDS, kgrid=K_GRID, **kw):
    """Pour chaque k du grille, moyenne la pente sur les graines ; k* = plus
       petit k dont la pente moyenne franchit +eps (croissance robuste)."""
    rows = []
    kstar = None
    for k in kgrid:
        if k > N // 2:            # un germe reste une perturbation LOCALE (< moitié du système)
            continue
        slopes = []
        for sd in seeds:
            sn, Es, Esd, Ee, _ = growth_rate(N, sd, gamma, k, **kw)
            slopes.append(sn)
        mean_s = float(np.mean(slopes)); std_s = float(np.std(slopes))
        cls = classify(mean_s)
        rows.append(dict(k=k, slope_mean=mean_s, slope_std=std_s, cls=cls))
        if kstar is None and cls > 0:
            kstar = k
    return kstar, rows

# ----------------------------------------------------------------------------
#  CAMPAGNE + VERDICT
# ----------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("=" * 74)
    print("  GERME CRITIQUE DE STRAUSS — suite autonome (Blob Principle)")
    print(f"  preset={PRESET}  kappa={KAPPA}  beta={BETA}  tau={TAU}  slope_eps={SLOPE_EPS}")
    print("  Pré-enregistré : k*(N) intrinsèque (~const) => échelle engendrée")
    print("                   k*(N) extensif  (~N)      => pas d'échelle, voie fermée")
    print("=" * 74)
    results = {"config": dict(preset=PRESET, kappa=KAPPA, beta=BETA, tau=TAU,
                              N_list=N_LIST, gamma_list=GAMMA_LIST, seeds=SEEDS,
                              burn=BURN_SPARSE, prod=PROD_SWEEPS, kgrid=K_GRID,
                              slope_eps=SLOPE_EPS), "runs": []}
    for gamma in GAMMA_LIST:
        print(f"\n--- gamma = {gamma} ------------------------------------------------")
        kstar_by_N = {}
        for N in N_LIST:
            kstar, rows = find_kstar(N, gamma)
            kstar_by_N[N] = kstar
            desc = "  ".join(f"k={r['k']}:{'+' if r['cls']>0 else ('-' if r['cls']<0 else '0')}"
                             f"({r['slope_mean']:+.3f})" for r in rows)
            print(f"  N={N:5d}  k*={str(kstar):>5s}  | {desc}")
            results["runs"].append(dict(gamma=gamma, N=N, kstar=kstar, rows=rows))
        # verdict de ratio pour ce gamma
        Ns = [N for N in N_LIST if kstar_by_N.get(N)]
        if len(Ns) >= 2:
            Nlo, Nhi = Ns[0], Ns[-1]
            klo, khi = kstar_by_N[Nlo], kstar_by_N[Nhi]
            ratio_k = khi / klo
            ratio_N = Nhi / Nlo
            tag = ("INTRINSÈQUE (échelle engendrée)" if ratio_k < 0.5 * (1 + ratio_N) * 0.5 + 0.5
                   else "EXTENSIF")
            # critère net : proche de 1 => intrinsèque ; proche de ratio_N => extensif
            verdict = "INTRINSÈQUE" if abs(ratio_k - 1) < abs(ratio_k - ratio_N) else "EXTENSIF"
            print(f"    -> k*({Nhi})/k*({Nlo}) = {ratio_k:.2f}  (intrinsèque≈1 | extensif≈{ratio_N:.1f})"
                  f"  ==> {verdict}")
            results.setdefault("verdicts", []).append(
                dict(gamma=gamma, N_lo=Nlo, N_hi=Nhi, kstar_lo=klo, kstar_hi=khi,
                     ratio_k=ratio_k, ratio_N=ratio_N, verdict=verdict))

    dt = time.time() - t0
    results["runtime_s"] = dt
    with open("blob_germe_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n" + "=" * 74)
    print(f"  terminé en {dt:.0f}s  ->  blob_germe_results.json")
    if results.get("verdicts"):
        vs = [v["verdict"] for v in results["verdicts"]]
        n_int = vs.count("INTRINSÈQUE"); n_ext = vs.count("EXTENSIF")
        print(f"  BILAN : {n_int} gamma INTRINSÈQUE, {n_ext} EXTENSIF (sur {len(vs)})")
        if n_int > n_ext:
            print("  -> signal en faveur d'une ÉCHELLE COMBINATOIRE ENGENDRÉE")
            print("     (mécanisme candidat l_P ; à blinder : plus de graines, N=4800, runs longs)")
        elif n_ext > n_int:
            print("  -> germe EXTENSIF : pas d'échelle intrinsèque par cette voie (à graver)")
        else:
            print("  -> indécis : étendre graines / tailles / longueur de run")
    print("  Rappel discipline : [M] exploratoire ; aucun [T] ; k* ≠ l_P sans")
    print("  identification supplémentaire (une longueur engendrée est le PREMIER pas).")
    print("=" * 74)

if __name__ == "__main__":
    main()
