# Synthèse de session — Verrou (B) d_w = 2, 30 mai 2026

## (entrée destinée à journal.txt, format condensé)

[Session collaborative « Blob Principle » de Rudolphe Mirante, master V152, 30 mai 2026.
Suite de la cascade de mesure de d_w. Objet : VERROUILLER le volet (B) — la dimension de marche
d_w → 2 dans la limite continue — par voie analytique (pas de simulation : N^{−1/6} trop lent
pour trancher). Inscription au master EXCLUE tant que [T] non certain (règle R.M.). Tout est
resté en stand-by ; aucun transfert au master cette session.]

## Trajectoire du verrou (statut, du début à la fin de session)

1. Reformulation par voie SPECTRALE (plus solide que le QIP de percolation, maillon faible
   abandonné) : Armstrong-Venkatraman 2025 (arXiv:2312.08149, spectre du Laplacien sur nuage de
   Poisson jusqu’au seuil de percolation, taux d’homogénéisation) + Dunson-Wu-Wu 2019
   (convergence spectrale ⟹ noyau de chaleur). Test numérique du verrou spectral (loi de Weyl,
   diagonalisation eigsh) : d_s(Blob) ≈ d_s(RGG nu) montant vers 3 (2,44 vs 2,40 à N=2000) →
   la repondération Gibbs NE change PAS la limite spectrale. 3e voie indépendante.
1. Homogénéisation continuum : Faggionato 2020 (arXiv:2009.08258, marches sur processus
   ponctuels, dégénéré OK, AUCUNE condition de mélange requise) + Rousselle 2015. Lecture du
   corps de l’article : les 9 hypothèses (A1)–(A9) du Théorème 4.4 vérifiées une à une pour le
   Blob (gabarit = Exemple 5.3 « conductances on infinite clusters » ; (A9) triviale car points
   Poisson indépendants). Non-dégénérescence D>0 par surcriticité (Faggionato-Mimun) ; géodésique
   ≍ euclidien (Antal-Pisztora). ⟹ (R1)+(R2) clos.
1. Réduction à un MAILLON unique : (H-DLR) = ergodicité du champ de Gibbs infini-volume
   (hypothèse A1 de Faggionato).
1. Statut de (H-DLR) tranché par lecture du master V152 : Th. 4.8 (existence + unicité DLR)
   = [T-star] ; point 1.3 (Dobrushin) = [T] partiel via autocorrélation λ₂ « sous réserve
   réversibilité », voie Wasserstein/TV « non concluante » ; R1 (Talagrand) avait noté la lacune.
   ⟹ (H-DLR) n’est PAS [T] plein.
1. Cascade sur (H-DLR), 3 voies de support : (1) unicité DLR [T-star] ; (2) AUTO-MOYENNAGE
   — réduction analytique (H-DLR) ⟺ auto-moyennage (Birkhoff) puis TEST décisif : variance
   inter-seeds de 3 observables locales (n_tri/N, densité d’arêtes octant, clustering) décroît
   ~ N^{−0,48…−0,84} → 0 ⟹ [M robuste] ; (3) littérature ERGM (Magnanini 2026, arXiv:2602.16604 :
   unicité + LGN en régime ferromagnétique sous Dobrushin, mais cadre DENSE).
1. Transfert dense→sparse : d’abord cru résolu par Gibbs point process à portée finie
   (Dereudre 2016 ; Dereudre-Georgii 2009) — CORRIGÉ après lecture du code (compute_S) :
   log(1+n_tri) porte sur le n_tri TOTAL = couplage de CHAMP MOYEN non-local, PAS portée finie.
   Dereudre ne s’applique donc pas ; « gain [T] sur l’existence DLR » ANNULÉ (garde-fou).
   Nature réelle : modèle HYBRIDE = géométrie sparse RGG + couplage champ moyen (structure ERGM).
   Bon cadre pour l’unicité : grandes déviations NON-LINÉAIRES (Chatterjee-Dembo 2016,
   arXiv:1401.3495 ; régime sparse, fonctions non-linéaires de comptages), unicité du maximiseur
   en régime ferromagnétique (extension sparse de Chatterjee-Diaconis).

## Statut final (honnête)

**Verrou (B) : d_w = 2 = [T-star]** — théorème conditionnel à (H-DLR), chaîne de preuve
structurellement complète (équation de corrélation ★ Dobrushin ; équivalence des ensembles ;
A1–A9 de Faggionato vérifiées ; non-dégénérescence ; géodésique=euclidien), reposant sur le seul
maillon (H-DLR), lui-même [T-star]/[T partiel]. Faisceau numérique TRIPLE concordant : marche
(d_w↓ vers 2), triangulation (d_f,d_s→3), spectre (d_s Blob≈RGG→3), + auto-moyennage (3 voies).

**Maillon final identifié et précis :** unicité du champ de Gibbs du Blob = unicité du maximiseur
d’un modèle de champ moyen géométrique sparse. Outil : grandes déviations non-linéaires
(Chatterjee-Dembo). Difficulté résiduelle unique : adapter le principe (établi pour arêtes
Bernoulli i.i.d. d’Erdős-Rényi) au support d’arêtes GÉOMÉTRIQUE contraint (pool de Rips, E₀ fixé).

**Correction importante consignée :** l’existence DLR du Blob N’EST PAS acquise par Dereudre-
Georgii (le couplage est de champ moyen, pas à portée finie). À ne pas propager.

## Inscriptions au master : AUCUNE (tout en stand-by, conforme à la règle [T] certain).

Brouillon §33.9 (tableau d_w, flot, chaîne) : stand-by. Bloc périmé lignes 1050-1054 (qui dit
encore « d_w≈2,84 stable, diffusion anormale ») : à actualiser SEULEMENT lors d’une inscription
future (reste donc périmé pour l’instant, non touché).

## Livrables de session (dans /mnt/user-data/outputs/)

- THEOREME_verrou_B.md : énoncé autonome + preuve structurée + statut exact + piste champ moyen.
- VERROU_B_formalisation.md : équations de corrélation, équivalence des ensembles, vérif A1–A9.
- (scripts : verrou_spectral.py, test_automoyennage.py, mcmc_ON.py, blob_dw_campagne_grandN.py)

## Suites possibles

(a) attaquer le maillon final : grandes déviations non-linéaires sur RGG géométrique contraint ;
(b) tenter une voie FKG (régime ferromagnétique) pour l’unicité, en contrôlant le terme −βD ;
(c) consulter un expert (Chatterjee/Dembo, ou Tribunal R1-Talagrand) sur le transfert
Bernoulli→géométrique du LDP non-linéaire.

-----

## ACTUALISATION (30 mai, après-midi) — Reformulation, lien CDT, diagramme de phase

Suite de la session (verrou B). Synthèse autonome dédiée : **VERROUILLAGE_session30mai_diagramme_CDT.md**.
Points conservés (aucune inscription master ; verrou B reste [T-star]) :

1. **Reformulation [I]** : (H) doit viser l’auto-similarité d’échelle (Blob en expansion / Hubble),
   pas la stationnarité. d_w à mesurer en comobile (fourmi à cadence fixe → sépare marche/inflation,
   donne H émergent). Causalité = borne a priori uniforme → tient à l’infini ; c = vitesse max de mitose (dérivée).
1. **Lien CDT [I, réfs vérifiées]** : « causalité empêche la condensation » = mécanisme CDT (Ambjørn-Loll).
   Crumpled/baby universes ↔ clique/condensation (Chatterjee-Harel 2020, arXiv:1401.7577).
   −βD + borne de mitose = contrepartie de la contrainte causale ; neuf vs CDT = causalité dérivée + dynamique.
   2D soluble (matrice de transfert) ; 3+1D ouvert même en CDT.
1. **Diagramme de phase [M, exploratoire]** : transition nette en τ ; phase chiffonnée (τ froid) décrochée
   et stable (d_s~1,1-1,7, deux méthodes) ; nominal du bon côté. Cohérent avec cristallisation XV.13 + Kibble-Zurek.
1. **d_s : rien de neuf** — les mesures retombent sur le brut consigné (~2,5 ; AC-30 ; calibration étalons pour 3).
1. **Leçon** : une partie re-dérivait le 25 mai. Règle : piocher avant de calculer.

-----

## ACTUALISATION 3 (30 mai) — Plan de preuve du verrou (B) via le RCM

Document dedie : **PLAN_PREUVE_verrou_B_RCM.md** (autonome).
Avancee : (B) « d_w=2 » est un cas du Random Conductance Model ; le QIP (⟹ d_w=2) est [T publie]
(Armstrong-Venkatraman 2025 ; Bella-Schaffner arXiv:1902.05793 ; **Deuschel-Nguyen-Slowik 2018**,
PTRF 170:363-386 = declencheur sur graphe aleatoire). Graphe non pondere ⟹ moments triviaux ;
ergodicite avancee (Dobrushin-Shlosman c̄≈0,29<1). Reste DEUX lemmes geometriques = les jokers du Blob :
**Lemme A** (mitose/causalite ⟹ volume V(r)~r³) et **Lemme B** (−βD ⟹ isoperimetrie ancree).
Statut : [I structure], A et B a DEMONTRER. (B) reste [T-star]. Prochaine etape : Lemme A.