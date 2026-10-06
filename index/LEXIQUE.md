# LEXIQUE — corpus Blob Principle

*Établi le 24 septembre 2026 par relevé du corpus. 3 446 fichiers, 16,46 Go, du 5 avril au 9 septembre 2026.*

**Deux niveaux de certitude dans ce document.** Ce qui est **attesté** vient du texte du corpus lui-même. Ce qui est **déduit** vient des motifs de noms de fichiers et n'a pas été confirmé dans le texte — corrigez-le si je me suis trompé.

---

## 1. Les étiquettes épistémiques

*Attesté — convention du corpus.*

| Étiquette | Sens |
|---|---|
| `[T]` | Théorème — démontré |
| `[T*]`, `[T-star]` | Quasi-démontré, une lacune identifiée |
| `[T_I]` | Employée en partie CLXXVI pour SUP-1. **Hors convention** — à normaliser ou à définir |
| `[M]` | Mesuré |
| `[O]` | Observation |
| `[I]` | Identification |
| `[P]` | Prédiction |
| `[H]` | Hypothèse |
| `[F]` | Résultat formel |
| `[FAIL]` | Échec honnête — présenté en premier, jamais reformulé |
| `[Q]` | Question ouverte |

---

## 2. Le vocabulaire de travail

### Documents

| Terme | Sens | Où |
|---|---|---|
| **master** | Le document principal, versionné en continu. V346 = 1 918 pages | `00 COURANT`, `01 MASTERS` |
| **manifeste** | Version courte et publiable du master | `10 DOCUMENTS EN VRAC/Manifestes` |
| **FULL / COMPLET** | Version intégrale d'un document | partout |
| **LIGHT** | Version allégée du même document | partout |
| **HORS SÉRIE** | Édition spéciale — seulement en v89 | `10 …/Masters et manuscrits` |
| **annexe / supplément** | Module détachable du master | `10 …/Annexes et supplements` |
| **paper A / B0 / B1 / B2** | Articles courts destinés à publication séparée | `10 …/Papers et preprints` |
| **armature canonique** | Squelette de structure, pas un master. V347.1 = 29 pages | `00 COURANT` |
| **tome** | Découpe du master en volumes | `01 MASTERS` |

### Protocole de validation

| Terme | Sens | Certitude |
|---|---|---|
| **verrou** `verrou_N_M_nom` | Test numéroté de fermeture d'une question. Chaque verrou a un `.py` et un `.json` — le script et son résultat. Ex. `verrou_1_2_RGG_negatif` | déduit |
| **verrouillage** | La campagne qui ferme une série de verrous | attesté (`AC31_verrouillage.md`) |
| **brique** | Unité de construction d'une preuve, désignée par lettre (X, Z) ou par numéro (`brique_2_5`, `brique_5defs`). Variante `LOCK` = version figée | déduit |
| **LOCK / locks closed** | État figé d'un résultat, non rejouable | déduit |
| **AC-NN** | Auto-correction numérotée. AC-31 verrouillage, AC-32 fermeture du squeeze, AC-33 traçabilité | attesté |
| **corde de rappel** | Protocole en trois gestes : recouper (2-3 IA) · confronter (source externe) · arbitrer (humain du métier) | attesté |
| **rasoir d'Ockham opérationnel** | L'explication la plus simple qui survit à trois épreuves indépendantes : cohérence interne, confrontation externe, recoupement | attesté |
| **tribunal des 8** | Huit relecteurs hostiles fictifs, du probabiliste à l'expérimentateur | attesté |

### Campagnes numériques

| Terme | Sens | Certitude |
|---|---|---|
| **saut N** | Avancée de recherche numérotée, chacune avec son rapport PDF. Sauts 1 à 36 au moins | déduit |
| **palier** `blob_paliers_N####` | Mesure à N fixé, N croissant de 1 000 à 16 700 | déduit |
| **checkpoint** `checkpoint_######` | État MCMC sauvegardé, indexé par le nombre de pas. De 1 000 à 2 000 000 | déduit |
| **creuser_** | Script exploratoire, sans garantie de résultat | déduit |
| **balayage / sweep** | Exploration systématique d'un paramètre | déduit |
| **banc** | Jeu de référence pour comparaison | déduit |

### Objets mathématiques

| Symbole | Sens | Certitude |
|---|---|---|
| **κ** (kappa) | Degré du graphe de candidats. κ₀ = 6,6 chez AC-32, κ = 8 ailleurs — **valeurs divergentes, à trancher** | attesté |
| **χ** (chi) | Caractéristique d'Euler. `chi_mean`, `chi_max3`, `chi_rare` | déduit |
| **β** (beta) | Coefficient de pénalité de la fonctionnelle de viabilité | attesté |
| **τ** (tau) | Température de la mesure de Gibbs | attesté |
| **d_s** | Dimension spectrale. Plateau mesuré 3,03–3,07 en régime infrarouge | attesté |
| **d_H** | Dimension de Hausdorff. Mesurée ≥ 3, croissante 3,11 → 3,34 | attesté |
| **d_w** | Exposant de marche. 2,84 mesuré — lu comme artefact de taille finie par CXL.7, comme confusion avec d_f par AF.1. **Deux diagnostics incompatibles** | attesté |
| **d_f** | Dimension fractale | attesté |
| **K4** | Le tétraèdre — graphe minimal viable pour l'émergence 3D | attesté |
| **n_tri** | Nombre de triangles du graphe | attesté |
| **S** | La fonctionnelle de viabilité. Forme courte S = log(1+n_tri) − βD ; forme étendue S = ΔI − αK − βD. **Les deux circulent, à trancher** | attesté |

### Verrous nommés

| Nom | Objet | État au corpus |
|---|---|---|
| **INF-1** | Borne inférieure d_s ≥ 3 | `[T]` — deux routes : Delmotte 1999 (AC-32.1) et voie isopérimétrique (V236) |
| **SUP-1** | Borne supérieure d_s ≤ 3 | `[T_I]` fermé le 18 juillet 2026, partie CLXXVI, par Carne–Varopoulos |
| **L1.C.r** | Isopérimétrie | `[T]` — Marton sous Dobrushin-Shlosman, c̄ ≈ 0,19 |
| **M2-W_Theoreme_…** | Série de neuf théorèmes : GEN-WELLPOSED, H-LOCAL, Q-TIME, RG-1CELL, RG-RAY, RP, TOP-KIN, VOL-COVER, VOL-RATIO | `04 PORTES ET AUDITS` |
| **G0 à G6** | Les sept portes de qualification TOE | **0/7 fermées** |

### Théorèmes établis

OBSTRUCTION-HOLLOW · seuil géométrique · ROOT-MIXTURE · F3-MONOTONICITY · ET-ENERGY avec son corollaire ET-GLOBAL · Value Wall.

### Échecs honnêtes confirmés

4ᵉ lepton (7,5 GeV, exclu par LEP) · K1 (dérivation de Hubble) · K2 (Ω_DM/Ω_b) · K2_topo (ρ2−ρ3=3, falsifié à 14–44σ).

---

## 3. Où se trouve quoi

| Dossier | Fichiers | Volume | Période | Contenu |
|---|---:|---:|---|---|
| `00 COURANT` | 3 | 0,01 Go | 08–09/09 | Master V346, armature V347.1, section V345 |
| `01 MASTERS (filiation PDF)` | 110 | 0,56 Go | 26/05 → 08/09 | V248 → V346, un dossier par version |
| `02 VERSIONS (V92 a V197)` | 2 169 | 0,18 Go | 06/04 → 07/06 | 56 versions, scripts et données de chaque campagne |
| `03 LIVRES` | 93 | 0,02 Go | 11/05 → 06/07 | *Le Blob Surnaturel*, *Du simplexe au complexe*, dossier Odile Jacob |
| `04 PORTES ET AUDITS` | 36 | 0,07 Go | 26/07 → 03/08 | Relevé des 7 portes, théorèmes M2-W, scripts de vérification |
| `05 SCRIPTS` | 130 | 0,03 Go | 22/05 → 27/07 | Scripts Colab et simulations |
| `06 DONNEES` | 11 | 0,00 Go | 12/06 → 02/07 | Invariants 500k, universalité alpha, paliers |
| `07 PARADIGMES TECHNOLOGIQUES` | 220 | 0,04 Go | 13/05 → 17/08 | HYDROSCOPE-IT, SILENTIA-PS, VIATRON-S, campagne D87 |
| `08 CAMPAGNES ET SAUTS` | 186 | 0,01 Go | 12/04 → 12/06 | Sauts 1 à 36, scaling V30, cascade, test O2v4, ALPHA, BANC |
| `09 SAUVEGARDES` | 312 | 0,16 Go | 14/04 → 20/05 | Archives Blob, back-ups de mai, manuscrits V109–V135 |
| `10 DOCUMENTS EN VRAC` | 74 | 0,03 Go | 05/04 → 24/05 | Classés par nature en onze rubriques |
| `90 ARCHIVES ZIP` | 101 | **15,35 Go** | 21/04 → 30/07 | Archives totales — candidates à l'élimination |

---

## 4. Conventions de nommage constatées

- **Version** : `V` suivi de deux ou trois chiffres. Parfois `v` minuscule sur les versions anciennes (v66, v89). Parfois avec un suffixe : `V277 bis`, `V347_1`.
- **Taille d'échantillon** : `N####` — `N500`, `N1500`, `N2000`, `N20000`.
- **Couple script/résultat** : même racine, extensions `.py` et `.json`. Ex. `verrou_1_2_RGG_negatif.py` et `.json`.
- **Générations** : suffixes `.gen1`, `.gen2`, `.gen3` sur les banques `.pkl`, avec leur empreinte `.sha256` à côté.
- **Livrable** : `Livrable N` ou `D##` — deux systèmes coexistent.

---

## 5. Cinq points à trancher, relevés en rangeant

1. **La fonctionnelle S a deux formes** en circulation — courte et étendue. Elles ne sont pas équivalentes.
2. **κ vaut 6,6 ou 8** selon les documents.
3. **d_w ≈ 2,84** reçoit deux explications incompatibles : artefact de fenêtre, ou confusion avec d_f.
4. **`[T_I]`** n'appartient pas à la convention d'étiquetage.
5. **Cinquante versions manquent** entre V92 et V197 — dont V105, où est attestée la forme étendue de S. Elles sont peut-être dans les archives ZIP ; c'est une raison de plus de vérifier ces archives avant d'en supprimer une seule.
