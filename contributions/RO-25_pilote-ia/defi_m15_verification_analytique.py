#!/usr/bin/env python3 -I
"""
Vérification analytique indépendante de l'hypothèse γ = α − δ.

Ce script :
1. Refait la dérivation pas à pas et vérifie les facteurs/signes.
2. Recharge les données de DEFI-M11 (demi-temps, queue aristocratique).
3. Refait les régressions log t½ / log N sur plusieurs fenêtres.
4. Estime δ à partir de la moyenne de T_v à l'équilibre (q_eff).
5. Teste la prédiction γ = 1 − δ.

TOE démontrée : NON ; candidate digne d'étude : OUI.
"""
import json, math
import numpy as np
from scipy import stats

# ---------- 1. Chargement des données DEFI-M11 ----------

with open("/home/claude/the-blob-principle/contributions/RO-25_pilote-ia/defi_m11_demi_temps.json") as f:
    dt_data = json.load(f)

with open("/home/claude/the-blob-principle/contributions/RO-25_pilote-ia/defi_m11_queue_aristocratique.json") as f:
    queue_data = json.load(f)

# ---------- 2. Vérification analytique de la dérivation ----------

print("="*70)
print("VÉRIFICATION ANALYTIQUE DE L'HYPOTHÈSE γ = α − δ")
print("="*70)

print("""
Dérivation :
  S_sim = log(1 + T) − βD
  π ∝ exp(λ S_sim),  λ = n^α / τ

  Dans une clique de taille q :
    T ~ C(q,3) = q(q−1)(q−2)/6 ~ q³/6

  [Vérification] T pour q = 5 : C(5,3) = 10, q³/6 = 20.83
    Le facteur q³/6 est une approximation valable pour q grand.
    Pour q petit, T = q(q−1)(q−2)/6 est exact.

  Retirer une arête (a,b) de la clique détruit exactement (q−2) triangles
  (tous les sommets c ≠ a,b forment un triangle a-b-c).
  [Vérification] q=5 : retirer une arête détruit 3 triangles. ✓

  Variation de log(1+T) quand on retire une arête :
    Δ log(1+T) = log(1 + T − (q−2)) − log(1 + T)

    Pour T >> q−2 (c'est-à-dire q >> 3) :
    |Δ log(1+T)| ≈ (q−2)/T ≈ (q−2)/(q³/6) ≈ 6/q²

  Coût en S_sim d'une arête retirée (hors D) :
    λ · |Δ log(1+T)| ≈ 6λ/q²

  Pour remplacer un membre de la clique par un étranger :
    - Retirer ses (q−1) arêtes vers la clique : coût total ≈ (q−1)·6λ/q² ≈ 6λ/q
    - Ajouter (q−1) arêtes vers le remplaçant : gain similaire

  La barrière est dominée par la phase de retrait (les arêtes sont retirées
  avant d'être reconstruites) :
    B_triangle ≈ 6λ/q ≈ 6 n^α / (τ q)

  Avec q ~ n^δ :
    B_triangle ~ n^(α−δ)

  Temps de séjour activé :
    t_séjour ~ exp(c · n^(α−δ))

  Donc log t ~ n^γ avec γ = α − δ.

  Avec α = 1 (axiome A4) : γ = 1 − δ.
""")

# Vérification numérique du facteur
for q in [5, 10, 20, 50]:
    T_exact = q*(q-1)*(q-2)//6
    T_approx = q**3 / 6
    delta_exact = q - 2  # triangles détruits par le retrait d'une arête
    delta_log_exact = abs(math.log(1 + T_exact - delta_exact) - math.log(1 + T_exact))
    delta_log_approx = 6 / q**2
    print(f"  q={q:3d}: T_exact={T_exact:6d}, T≈q³/6={T_approx:8.1f}, "
          f"|Δlog(1+T)|_exact={delta_log_exact:.4f}, ≈6/q²={delta_log_approx:.4f}, "
          f"ratio={delta_log_exact/delta_log_approx:.3f}")

print()
print("[CERT] Les facteurs sont corrects. L'approximation 6/q² est valable")
print("       pour q ≥ 10 (ratio exact/approx > 0.9).")
print("       Le facteur exact est (q−2)/T = 6(q−2)/(q(q−1)(q−2)) = 6/(q(q−1)).")
print()
print("ATTENTION : la dérivation suppose que la contribution −βD est négligeable")
print("           par rapport à la contribution triangulaire. C'est le point 4")
print("           du protocole : à vérifier expérimentalement.")

# ---------- 3. Régressions t½ vs N (exposant γ) ----------

print()
print("="*70)
print("RÉGRESSIONS : t½ vs N (exposant γ mesuré)")
print("="*70)

# Extraire les données θ = 0 de la campagne principale
theta0_data = [(r["N"], r["t_demi_balayages"])
               for r in dt_data["lignes"]
               if r["theta"] == 0.0 and r["campagne"] == "defi_m11_monte_carlo.json"]
# Ajouter N=64 de la campagne longue
theta0_data.extend([(r["N"], r["t_demi_balayages"])
                     for r in dt_data["lignes"]
                     if r["theta"] == 0.0 and r["N"] == 64])

theta0_data.sort()
print(f"\nDonnées θ=0 : {theta0_data}")

# t½ est en balayages. Un balayage = M+k échanges = 2(N+1) échanges.
# La question est : t½ en balayages croît-il comme N^γ ?
# Le rapport dit « au moins N³ balayages ».
# L'hypothèse prédit log(t_séjour) ~ n^γ, pas t ~ n^γ.
#
# DISTINCTION CRUCIALE :
# - Le rapport M11 mesure t½ en balayages (une observable de relaxation)
# - L'hypothèse prédit log(t_séjour) ~ n^γ pour le temps de séjour activé
# - Ce sont des quantités DIFFÉRENTES !
# - t½ est un temps de relaxation (premier passage d'une moyenne)
# - t_séjour est un temps de séjour dans un puits de potentiel
#
# Si la barrière est B ~ n^(α-δ), le temps de SÉJOUR suit
# t_séjour ~ exp(c·n^(α-δ)), donc log(t_séjour) ~ n^(α-δ).
#
# Le t½ de M11 mesure la relaxation vers l'équilibre,
# pas le temps de séjour dans un puits. Ce sont des phénomènes liés
# mais pas identiques.

Ns = np.array([d[0] for d in theta0_data])
t_half = np.array([d[1] for d in theta0_data])

print("\n--- Régression loi de puissance : t½ = a · N^γ ---")
for label, mask in [("N ≥ 8", Ns >= 8), ("N ≥ 12", Ns >= 12),
                     ("N ≥ 16", Ns >= 16), ("N ≥ 24", Ns >= 24)]:
    x = np.log(Ns[mask])
    y = np.log(t_half[mask])
    slope, intercept, r, p, se = stats.linregress(x, y)
    print(f"  {label}: γ = {slope:.3f} ± {se:.3f}, R² = {r**2:.4f}, n_pts = {mask.sum()}")

# Pentes locales
print("\n--- Pentes locales log(t½)/log(N) entre points adjacents ---")
for i in range(len(Ns)-1):
    pente = (math.log(t_half[i+1]) - math.log(t_half[i])) / (math.log(Ns[i+1]) - math.log(Ns[i]))
    print(f"  N={Ns[i]}→{Ns[i+1]}: pente = {pente:.2f}")

# Test exponentiel : log(t½) vs N
print("\n--- Régression exponentielle : log(t½) = a + b·N ---")
for label, mask in [("N ≥ 12", Ns >= 12), ("N ≥ 24", Ns >= 24)]:
    x = Ns[mask].astype(float)
    y = np.log(t_half[mask])
    slope, intercept, r, p, se = stats.linregress(x, y)
    print(f"  {label}: b = {slope:.4f} ± {se:.4f}, R² = {r**2:.4f}")

# Test sous-exponentiel : log(t½) vs N^γ pour différents γ
print("\n--- Test : log(t½) vs N^γ, différents γ candidats ---")
for gamma in [0.5, 0.6, 0.7, 0.8, 1.0]:
    mask = Ns >= 12
    x = Ns[mask].astype(float)**gamma
    y = np.log(t_half[mask])
    slope, intercept, r, p, se = stats.linregress(x, y)
    print(f"  γ = {gamma:.1f}: R² = {r**2:.4f}")

# ---------- 4. Estimation de δ (exposant de la clique) ----------

print()
print("="*70)
print("ESTIMATION DE δ : taille de la structure dominante")
print("="*70)

# À partir de la queue aristocratique, on a la moyenne de T_v à l'équilibre.
# Dans une clique de taille q, un sommet a T_v = C(q-1, 2) = (q-1)(q-2)/2.
# Si q sommets sont dans la clique et n+1-q hors de la clique :
#   <T_v> ≈ q · (q-1)(q-2)/2 / (n+1)
#
# Mais c'est trop simplifié. Utilisons q_eff = (1 + sqrt(1 + 8 T_v_mean))/2
# qui suppose que le sommet moyen est dans une clique de taille q_eff.
# C'est une approximation grossière.
#
# En fait, la donnée la plus directe serait la clique maximale du graphe,
# qu'on n'a pas ici. On a la moyenne de T_v sur tous les sommets.

print("\nMoyenne de T_v à l'équilibre et q_eff :")
for entry in queue_data:
    N1 = entry["N_plus_1"]
    N = N1 - 1
    mean_Tv = entry["moyenne_T_v"]
    # q_eff tel que C(q-1,2) = T_v_mean => q_eff = (1 + sqrt(1+8·T_v_mean))/2
    q_eff = (1 + math.sqrt(1 + 8*mean_Tv)) / 2
    print(f"  N+1={N1:3d}, N={N:3d}, <T_v>={mean_Tv:.3f}, q_eff={q_eff:.3f}")

# Régressions δ = log(q_eff)/log(N)
Ns_q = []
q_effs = []
for entry in queue_data:
    N = entry["N_plus_1"] - 1
    mean_Tv = entry["moyenne_T_v"]
    q_eff = (1 + math.sqrt(1 + 8*mean_Tv)) / 2
    Ns_q.append(N)
    q_effs.append(q_eff)

Ns_q = np.array(Ns_q, dtype=float)
q_effs = np.array(q_effs)

print("\n--- Régression log(q_eff) vs log(N), différentes fenêtres ---")
for label, mask in [("N ≥ 8", Ns_q >= 8), ("N ≥ 16", Ns_q >= 16),
                     ("N ≥ 24", Ns_q >= 24), ("N ≥ 32", Ns_q >= 32)]:
    if mask.sum() < 2:
        continue
    x = np.log(Ns_q[mask])
    y = np.log(q_effs[mask])
    slope, intercept, r, p, se = stats.linregress(x, y)
    print(f"  {label}: δ = {slope:.3f} ± {se:.3f}, R² = {r**2:.4f}, n_pts = {mask.sum()}")

# ---------- 5. Prédiction γ = 1 − δ ----------

print()
print("="*70)
print("TEST DE LA PRÉDICTION γ = 1 − δ")
print("="*70)

# La prédiction est que log(t_séjour) ~ n^γ avec γ = 1 - δ.
# Mais t½ est un temps de relaxation, pas un temps de séjour.
#
# Le rapport M11 ajuste t½ ~ N^exposant (loi de puissance).
# La prédiction de la dérivation est log(t_séjour) ~ N^γ (Arrhenius).
#
# Si t½ ~ N^p, alors log(t½) = p·log(N) + const
# Si t ~ exp(c·N^γ), alors log(t) = c·N^γ
#
# Ce ne sont PAS les mêmes quantités.
#
# Le rapport M11 signale lui-même [H] le mécanisme Arrhenius.
# Le protocole mélange les deux : il parle de γ mesuré ≈ 0.507
# pour le degré moyen 4, mais les données M11 mesurent un EXPOSANT
# de loi de puissance de t½, pas un exposant d'Arrhenius.

# Régressions pour γ_puissance (t½ ~ N^γ)
mask = Ns >= 12
x = np.log(Ns[mask])
y = np.log(t_half[mask])
gamma_puissance, intercept, r, p, se = stats.linregress(x, y)

# Estimation de δ à partir de q_eff (N ≥ 16)
mask_q = Ns_q >= 16
xq = np.log(Ns_q[mask_q])
yq = np.log(q_effs[mask_q])
delta, intercept_q, r_q, p_q, se_q = stats.linregress(xq, yq)

print(f"\nExposant de loi de puissance : t½ ~ N^{gamma_puissance:.3f} (N ≥ 12)")
print(f"Exposant structurel : q_eff ~ N^{delta:.3f} (N ≥ 16)")
print(f"Prédiction γ = 1 − δ = {1 - delta:.3f}")
print(f"Valeur mesurée (puissance) : {gamma_puissance:.3f}")
print(f"Écart : {abs(gamma_puissance - (1 - delta)):.3f}")

print("""
ATTENTION CRITIQUE :
1. La dérivation prédit un temps de séjour ACTIVÉ : log(t) ~ n^γ.
   Les données M11 mesurent un temps de RELAXATION : t½ ~ N^p.
   Ce sont des quantités fondamentalement différentes.

2. L'exposant p ≈ 3 de la loi de puissance t½ ~ N^p n'est pas
   le γ de la prédiction Arrhenius log(t) ~ N^γ.

3. Pour tester correctement l'hypothèse, il faudrait mesurer
   le temps de SÉJOUR dans un puits aristocratique, pas le temps
   de relaxation après naissance.

4. La concordance ou discordance entre p et 1−δ ne valide ni
   ne réfute l'hypothèse : elle compare des quantités différentes.

5. Le terme −βD n'est pas mesuré séparément (point 4 du protocole).

CONCLUSION INTERMÉDIAIRE :
- La dérivation est algébriquement correcte.
- La prédiction (Arrhenius) ne peut pas être testée directement
  sur les données M11, qui mesurent un temps de relaxation.
- Il faut une nouvelle campagne qui mesure le temps de SÉJOUR
  dans un puits aristocratique, pas le t½ après naissance.
""")

# ---------- 6. Sensibilité aux fenêtres ----------

print("="*70)
print("SENSIBILITÉ AUX FENÊTRES D'AJUSTEMENT")
print("="*70)

# Pour le γ puissance
print("\nExposant de loi de puissance γ_p (t½ ~ N^γ_p) :")
windows = [("N≥8", 8), ("N≥12", 12), ("N≥16", 16), ("N≥24", 24)]
gammas_p = []
for label, nmin in windows:
    mask = Ns >= nmin
    if mask.sum() < 2:
        continue
    x = np.log(Ns[mask])
    y = np.log(t_half[mask])
    s, i, r, p, e = stats.linregress(x, y)
    gammas_p.append(s)
    print(f"  {label}: γ_p = {s:.3f} ± {e:.3f} (R²={r**2:.4f})")

print(f"\n  Étendue : {min(gammas_p):.3f} – {max(gammas_p):.3f}")

# Pour le δ
print("\nExposant structurel δ (q_eff ~ N^δ) :")
deltas = []
for label, nmin in [("N≥8", 8), ("N≥16", 16), ("N≥24", 24)]:
    mask = Ns_q >= nmin
    if mask.sum() < 2:
        continue
    x = np.log(Ns_q[mask])
    y = np.log(q_effs[mask])
    s, i, r, p, e = stats.linregress(x, y)
    deltas.append(s)
    print(f"  {label}: δ = {s:.3f} ± {e:.3f} (R²={r**2:.4f})")

print(f"\n  Étendue : {min(deltas):.3f} – {max(deltas):.3f}")

print()
print("="*70)
print("RÉSUMÉ")
print("="*70)
print("""
STATUT : [H] hypothèse non testable sur les données existantes.

1. La dérivation algébrique γ = α − δ est correcte [CERT].
   Facteur exact : 6/(q(q−1)) ≈ 6/q².

2. L'hypothèse prédit un comportement ARRHENIUS (log t ~ n^γ)
   pour le temps de SÉJOUR dans un puits aristocratique.

3. Les données M11 mesurent un temps de RELAXATION (t½) après
   naissance, qui suit une LOI DE PUISSANCE t½ ~ N^3.

4. Ces deux quantités ne sont pas comparables directement.
   L'exposant 3 de t½ n'est ni γ ni 1−δ.

5. q_eff estimé à partir de <T_v> donne δ ≈ 0.11–0.14,
   ce qui prédirait γ ≈ 0.86–0.89. Mais q_eff est une
   approximation grossière de la clique maximale.

6. Pour tester l'hypothèse, il faut :
   a) Mesurer le temps de SÉJOUR dans un puits (pas t½)
   b) Mesurer la clique MAXIMALE (pas q_eff)
   c) Séparer les contributions T et D dans la barrière
   d) Faire varier α pour tester γ(α) = α − δ

TOE démontrée : NON ; candidate digne d'étude : OUI.
""")
