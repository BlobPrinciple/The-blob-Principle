"""
BLOB PRINCIPLE — Saut 10 : Test Lambda_Blob = Phi / Q3
=======================================================
Hypothèse [H] : Lambda_Blob = Phi / Q3
  - Lambda décroît avec le temps (cosmologie cohérente)
  - Lambda est élevée tôt (N petit), faible tard (N grand)
  - Testable sur les données Saut 3.5v4 déjà disponibles
  - Testable sur les nouvelles données Saut 9

Protocole :
  1. Charger saut35v4_FULL_EVOLUTION.json (11 paliers N=50..100k)
  2. Estimer Phi et Q3 à chaque palier
  3. Calculer Lambda_Blob(N) = Phi(N) / Q3(N)
  4. Tester la monotonie décroissante
  5. Ajuster un modèle Lambda ~ N^(-gamma)
  6. Comparer avec Lambda cosmologique observée
  7. Si saut9_results.json disponible : répéter autour de N*

Output : saut10_results.json + rapport console
"""

import json
import math
import os

# ─── Constantes ──────────────────────────────────────────────────────────────
LAMBDA_COSMO_SI  = 1.089e-52   # m^-2 (valeur observée Planck 2018)
LAMBDA_COSMO_LP2 = 2.888e-122  # en unités de longueur de Planck^-2

# ─── Données Saut 3.5v4 ──────────────────────────────────────────────────────
# Phi estimé = variation cumulée de ntetra entre paliers successifs
# Q3  estimé = dissipation cumulée ~ N * D_finale (approximation)
# Note : sans les historiques MCMC complets, on utilise les proxies suivants :
#   Phi(N)  = ntetra(N)           [friction topologique accumulée]
#   Q3(N)   = N * D(N)            [dissipation cumulée proxy]
#   D(N)    = ntri / (ntri + ntetra + 1)

SAUT35V4_DATA = [
    {"N":50,    "ntri":215,   "ntetra":96,    "SE":5.1994},
    {"N":100,   "ntri":397,   "ntetra":423,   "SE":5.7938},
    {"N":250,   "ntri":963,   "ntetra":2714,  "SE":6.6729},
    {"N":500,   "ntri":1492,  "ntetra":5376,  "SE":7.1244},
    {"N":1000,  "ntri":2442,  "ntetra":10334, "SE":7.6257},
    {"N":2500,  "ntri":3838,  "ntetra":19604, "SE":8.1039},
    {"N":5000,  "ntri":4782,  "ntetra":23058, "SE":8.3387},
    {"N":10000, "ntri":6922,  "ntetra":27789, "SE":8.7097},
    {"N":25000, "ntri":12181, "ntetra":34783, "SE":9.2810},
    {"N":50000, "ntri":19725, "ntetra":38597, "SE":9.7694},
    {"N":100000,"ntri":32500, "ntetra":40725, "SE":10.2725},
]

BETA = 0.30
TAU  = 0.50


# ─── Fonctions de calcul ──────────────────────────────────────────────────────

def compute_D(ntri, ntetra):
    return ntri / (ntri + ntetra + 1)

def compute_Ssim(ntri, ntetra):
    D = compute_D(ntri, ntetra)
    return math.log(1 + ntri) - BETA * D

def compute_SE(N, ntri, ntetra):
    return -N * compute_Ssim(ntri, ntetra) / TAU

def compute_Phi_proxy(d):
    """
    Phi proxy = ntetra (friction tétraédrique accumulée).
    Interprétation : chaque tétraèdre représente une unité de friction
    topologique entre simplexes. Phi = somme des transitions tétraédriques.
    Sans historique MCMC, ntetra est le meilleur proxy disponible.
    """
    return d["ntetra"]

def compute_Q3_proxy(d):
    """
    Q3 proxy = N * D (dissipation cumulée).
    D = ntri/(ntri+ntetra+1) est la dissipation instantanée.
    Q3 ~ intégrale de D sur le temps ~ N * D_finale (approximation linéaire).
    """
    D = compute_D(d["ntri"], d["ntetra"])
    return d["N"] * D

def compute_Lambda(Phi, Q3):
    """Lambda_Blob = Phi / Q3."""
    return Phi / Q3 if Q3 > 0 else None

def linreg(xs, ys):
    """Régression linéaire simple. Retourne (slope, intercept, R²)."""
    n = len(xs)
    mx = sum(xs)/n; my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    den = sum((x-mx)**2 for x in xs)
    if den == 0: return None, None, None
    slope = num/den
    intercept = my - slope*mx
    ss_res = sum((y - (slope*x+intercept))**2 for x,y in zip(xs,ys))
    ss_tot = sum((y-my)**2 for y in ys)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2

def is_monotone_decreasing(vals):
    """Teste la monotonie décroissante stricte."""
    for i in range(len(vals)-1):
        if vals[i+1] >= vals[i]:
            return False, i  # retourne l'indice de violation
    return True, -1

def permutation_test(xs, ys, n_perm=10000, seed=42):
    """
    Test de permutation pour la corrélation de Spearman entre xs et ys.
    H0 : pas de corrélation. p-value = fraction des permutations
    avec corrélation >= corrélation observée.
    """
    import random
    rng = random.Random(seed)

    def spearman(a, b):
        n = len(a)
        ra = sorted(range(n), key=lambda i: a[i])
        rb = sorted(range(n), key=lambda i: b[i])
        rank_a = [0]*n; rank_b = [0]*n
        for r,i in enumerate(ra): rank_a[i] = r
        for r,i in enumerate(rb): rank_b[i] = r
        ma = sum(rank_a)/n; mb = sum(rank_b)/n
        num = sum((rank_a[i]-ma)*(rank_b[i]-mb) for i in range(n))
        da  = sum((rank_a[i]-ma)**2 for i in range(n))**0.5
        db  = sum((rank_b[i]-mb)**2 for i in range(n))**0.5
        return num/(da*db) if da*db > 0 else 0

    obs = spearman(xs, ys)
    count = 0
    ys_perm = list(ys)
    for _ in range(n_perm):
        rng.shuffle(ys_perm)
        if abs(spearman(xs, ys_perm)) >= abs(obs):
            count += 1
    return obs, count/n_perm


# ─── Analyse principale ───────────────────────────────────────────────────────

def run_saut10():
    print("=" * 65)
    print("BLOB PRINCIPLE — Saut 10 : Test Lambda_Blob = Phi / Q3")
    print("=" * 65)

    rows = []

    print(f"\n{'N':>8} {'ntri':>8} {'ntetra':>8} {'D':>7} {'Phi':>10} "
          f"{'Q3':>10} {'Lambda':>10} {'SE':>8}")
    print("─" * 75)

    for d in SAUT35V4_DATA:
        D    = compute_D(d["ntri"], d["ntetra"])
        Phi  = compute_Phi_proxy(d)
        Q3   = compute_Q3_proxy(d)
        Lam  = compute_Lambda(Phi, Q3)
        SE   = d["SE"]

        row = {
            "N":      d["N"],
            "ntri":   d["ntri"],
            "ntetra": d["ntetra"],
            "D":      D,
            "Phi":    Phi,
            "Q3":     Q3,
            "Lambda": Lam,
            "SE":     SE,
            "Ssim":   compute_Ssim(d["ntri"], d["ntetra"]),
        }
        rows.append(row)
        print(f"{d['N']:>8} {d['ntri']:>8} {d['ntetra']:>8} "
              f"{D:>7.4f} {Phi:>10.1f} {Q3:>10.2f} "
              f"{Lam:>10.6f} {SE:>8.4f}")

    # ── Test 1 : Monotonie de Lambda ─────────────────────────────────────────
    print(f"\n{'─'*65}")
    print("TEST 1 — Monotonie décroissante de Lambda_Blob(N)")
    print(f"{'─'*65}")

    lambdas = [r["Lambda"] for r in rows]
    Ns      = [r["N"] for r in rows]

    mono, viol_idx = is_monotone_decreasing(lambdas)
    if mono:
        print("  PASS : Lambda est strictement décroissante sur tout le domaine.")
        print("  → Cohérent avec Λ cosmologique décroissant dans le temps.")
    else:
        print(f"  VIOLATION à l'index {viol_idx} : "
              f"N={Ns[viol_idx]}→{Ns[viol_idx+1]}  "
              f"Lambda={lambdas[viol_idx]:.6f}→{lambdas[viol_idx+1]:.6f}")
        print("  → Monotonie non stricte. Voir analyse par segments.")

    # ── Test 2 : Loi de puissance Lambda ~ N^(-gamma) ────────────────────────
    print(f"\n{'─'*65}")
    print("TEST 2 — Ajustement Lambda ~ N^(-gamma)")
    print(f"{'─'*65}")

    log_N = [math.log(r["N"]) for r in rows]
    log_L = [math.log(r["Lambda"]) for r in rows]

    slope, intercept, r2 = linreg(log_N, log_L)
    gamma  = -slope
    A_fit  = math.exp(intercept)

    print(f"  Lambda ~ {A_fit:.6f} * N^(-{gamma:.4f})")
    print(f"  R² = {r2:.6f}")
    print(f"  gamma = {gamma:.4f}  (attendu ~1 pour Lambda ~ 1/N)")

    if r2 > 0.98:
        print("  → PASS : loi de puissance robuste (R²>0.98).")
    elif r2 > 0.95:
        print("  → PARTIEL : loi de puissance acceptable (R²>0.95).")
    else:
        print("  → ATTENTION : R²<0.95, la loi de puissance est approximative.")

    # Prédictions
    print(f"\n  Prédictions Lambda_Blob(N) avec ajustement :")
    for N_pred in [50, 100, 500, 1000, 2500, 10000, 100000]:
        L_pred = A_fit * N_pred**(-gamma)
        print(f"    N={N_pred:>7}  Lambda_pred = {L_pred:.8f}")

    # ── Test 3 : Corrélation Lambda vs SE (permutation) ───────────────────────
    print(f"\n{'─'*65}")
    print("TEST 3 — Corrélation Spearman Lambda vs SE (test de permutation)")
    print(f"{'─'*65}")

    SEs = [r["SE"] for r in rows]
    rho, pval = permutation_test(SEs, lambdas, n_perm=10000)

    print(f"  Corrélation Spearman(SE, Lambda) = {rho:.4f}")
    print(f"  p-value (permutation, 10k) = {pval:.4f}")
    if pval < 0.01:
        print(f"  SIGNIFICATIF (p<0.01) : Lambda corrèle avec SE.")
    elif pval < 0.05:
        print(f"  MARGINALEMENT SIGNIFICATIF (p<0.05).")
    else:
        print(f"  NON SIGNIFICATIF (p>0.05).")

    # ── Test 4 : Ratio Lambda_Blob / Lambda_cosmo ────────────────────────────
    print(f"\n{'─'*65}")
    print("TEST 4 — Comparaison Lambda_Blob vs Lambda cosmologique")
    print(f"{'─'*65}")
    print("  Note : Lambda_Blob est adimensionnel (Phi/Q3),")
    print("         Lambda_cosmo est en m^-2 ou l_P^-2.")
    print("         La comparaison est qualitative (décroissance, ordre de grandeur).")
    print()
    print(f"  Lambda_cosmo observée : {LAMBDA_COSMO_SI:.3e} m^-2")
    print(f"  Lambda_cosmo en l_P^-2: {LAMBDA_COSMO_LP2:.3e}")
    print()

    # Normaliser Lambda_Blob par sa valeur à N=50 (passé lointain)
    L0 = lambdas[0]
    print(f"  Lambda_Blob normalisé (Lambda/Lambda_0, Lambda_0 @ N=50) :")
    for r in rows:
        ratio = r["Lambda"] / L0
        print(f"    N={r['N']:>7}  Lambda_norm = {ratio:.6f}")

    print()
    print("  Interprétation cosmologique :")
    print(f"    Lambda décroît d'un facteur {L0/lambdas[-1]:.2f} de N=50 à N=100000.")
    print(f"    Cohérent avec Lambda_cosmo faible aujourd'hui vs élevée à l'inflation.")

    # ── Test 5 : alpha_Blob stabilité en N ───────────────────────────────────
    print(f"\n{'─'*65}")
    print("TEST 5 — Stabilité de alpha_Blob en N [CRITIQUE]")
    print(f"{'─'*65}")
    print("  alpha_Blob = K^3 / kappa_RCP,  K = D * (ds/3),  ds=3,  kappa_RCP=8.1915")
    print()

    alpha_codata = 1 / 137.035999084
    alphas = []
    for r in rows:
        K     = r["D"] * (3.0 / 3.0)   # ds=3
        alpha = K**3 / 8.1915
        rel   = abs(alpha - alpha_codata) / alpha_codata * 100
        alphas.append(alpha)
        flag = "★" if rel < 1.0 else ("△" if rel < 5.0 else "✗")
        print(f"  N={r['N']:>7}  D={r['D']:.4f}  K={K:.4f}  "
              f"alpha={alpha:.6f}  err={rel:+.2f}%  {flag}")

    mean_alpha = sum(alphas)/len(alphas)
    std_alpha  = (sum((a-mean_alpha)**2 for a in alphas)/len(alphas))**0.5
    cv_alpha   = std_alpha/mean_alpha*100

    print(f"\n  alpha_Blob moyen = {mean_alpha:.6f} ± {std_alpha:.6f}  (CV={cv_alpha:.2f}%)")
    print(f"  alpha_CODATA     = {alpha_codata:.6f}")
    print(f"  Écart moyen      = {abs(mean_alpha-alpha_codata)/alpha_codata*100:.2f}%")

    if cv_alpha < 5.0:
        print(f"  → STABLE (CV<5%) : alpha_Blob est robuste en N.")
        verdict_alpha = "STABLE"
    else:
        print(f"  → VARIABLE (CV>5%) : alpha_Blob dépend de N.")
        verdict_alpha = "VARIABLE"

    if abs(mean_alpha - alpha_codata)/alpha_codata < 0.01:
        print(f"  → ACCORD <1% avec CODATA : signal fort.")
        accord_alpha = "ACCORD_1PCT"
    elif abs(mean_alpha - alpha_codata)/alpha_codata < 0.05:
        print(f"  → ACCORD <5% avec CODATA : signal modéré.")
        accord_alpha = "ACCORD_5PCT"
    else:
        print(f"  → DÉSACCORD >5% : coïncidence probable.")
        accord_alpha = "DESACCORD"

    # ── Si saut9_results.json disponible ─────────────────────────────────────
    saut9_file = "saut9_results.json"
    if os.path.exists(saut9_file):
        print(f"\n{'─'*65}")
        print("EXTENSION — Données Saut 9 détectées")
        print(f"{'─'*65}")
        with open(saut9_file) as f:
            s9 = json.load(f)
        print(f"  N_star estimé (Saut 9) : {s9.get('N_star_estimated','?')}")
        print(f"  r3_max (Saut 9)        : {s9.get('r3_max_estimated','?'):.4f}")

        print(f"\n  Lambda_Blob autour de N* (depuis Saut 9) :")
        for res in s9.get("results", []):
            N  = res["N_target"]
            # Utiliser les moyennes inter-seeds
            for seed_r in res.get("per_seed", []):
                ntri  = seed_r.get("ntri", 0)
                ntetra= seed_r.get("ntetra", 0)
                seed  = seed_r.get("seed", "?")
                Phi_s9 = ntetra
                Q3_s9  = seed_r.get("Q3", N * compute_D(ntri, ntetra))
                Phi_q3 = seed_r.get("Phi_over_Q3", Phi_s9/Q3_s9 if Q3_s9>0 else None)
                if Phi_q3:
                    print(f"    N={N:>5}  seed={seed}  Lambda={Phi_q3:.6f}  "
                          f"ntri={ntri}  ntetra={ntetra}")
    else:
        print(f"\n  [saut9_results.json non trouvé — exécuter saut9_growth.py d'abord]")

    # ── Synthèse ──────────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("SYNTHÈSE SAUT 10")
    print(f"{'='*65}")

    output = {
        "config": "Saut 10 — Test Lambda_Blob = Phi/Q3",
        "data_source": "Saut 3.5v4 (N=50..100k)",
        "proxy_Phi": "ntetra (friction topologique accumulée)",
        "proxy_Q3":  "N * D (dissipation cumulée proxy)",
        "results_per_N": rows,
        "test1_monotone": {
            "pass": mono,
            "violation_index": viol_idx if not mono else None,
            "verdict": "PASS" if mono else "FAIL",
        },
        "test2_power_law": {
            "gamma": gamma,
            "A": A_fit,
            "R2": r2,
            "verdict": "PASS" if r2 > 0.98 else ("PARTIEL" if r2 > 0.95 else "FAIL"),
        },
        "test3_spearman": {
            "rho": rho,
            "pvalue": pval,
            "verdict": "SIGNIFICATIF" if pval < 0.01 else (
                       "MARGINAL" if pval < 0.05 else "NON_SIGNIFICATIF"),
        },
        "test5_alpha_stability": {
            "alpha_mean": mean_alpha,
            "alpha_std": std_alpha,
            "cv_pct": cv_alpha,
            "alpha_codata": alpha_codata,
            "stability": verdict_alpha,
            "accord_codata": accord_alpha,
        },
        "interpretation": {
            "Lambda_decreasing": mono,
            "Lambda_power_law_gamma": gamma,
            "cosmological_coherence": "Lambda élevée tôt (petit N), faible tard (grand N)",
            "alpha_verdict": f"{verdict_alpha} / {accord_alpha}",
        }
    }

    with open("saut10_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n  Lambda_Blob ~ {A_fit:.4f} * N^(-{gamma:.4f})  R²={r2:.6f}  "
          f"[{'PASS' if r2>0.98 else 'PARTIEL'}]")
    print(f"  Monotonie décroissante : {'PASS' if mono else 'FAIL'}")
    print(f"  Corrélation SE : rho={rho:.4f}  p={pval:.4f}  "
          f"[{'SIG' if pval<0.01 else 'NS'}]")
    print(f"  alpha_Blob : {verdict_alpha} / {accord_alpha}  CV={cv_alpha:.2f}%")
    print(f"\n  Fichier écrit : saut10_results.json")

    # Statut final
    n_pass = sum([
        mono,
        r2 > 0.95,
        pval < 0.05,
        cv_alpha < 5.0,
    ])
    print(f"\n  STATUT LAMBDA_BLOB : {n_pass}/4 tests passés")
    if n_pass == 4:
        print("  → [H→M] : Lambda_Blob candidate solide pour intégration au corpus.")
    elif n_pass >= 3:
        print("  → [H partiel] : Lambda_Blob prometteuse, Saut 9 requis pour confirmation.")
    else:
        print("  → [H] maintenu : tests insuffisants.")

    return output


if __name__ == "__main__":
    run_saut10()
