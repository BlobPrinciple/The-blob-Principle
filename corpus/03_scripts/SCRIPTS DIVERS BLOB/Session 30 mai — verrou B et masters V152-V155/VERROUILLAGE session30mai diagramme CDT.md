# VERROUILLAGE — Session 30 mai 2026 : diagramme de phase, lien CDT, reformulation du verrou (B)

## Document autonome. Statuts au plus juste. Aucune inscription master (aucun [T] certain produit).

-----

## 0. Objet

Cette session prolonge le verrou (B) « d_w = 2 ». Elle n’a PAS produit de nouveau théorème.
Elle a produit : (i) une **reformulation conceptuelle** du verrou, (ii) un **lien précis et
ancré** avec les Causal Dynamical Triangulations (CDT), (iii) un **diagramme de phase mesuré**
du Blob, (iv) la **connexion** de tout cela à la lecture « cristallisation » déjà consignée.
Le verrou (B) reste **[T-star]** (conditionné à l’ergodicité/unicité de phase (H)).

-----

## 1. Reformulation conceptuelle du verrou (B) [I]

- **Auto-similarité plutôt que stationnarité.** (H) posée comme ergodicité statique est la
  mauvaise cible : le Blob est en **expansion** (loi de Hubble émergente déjà testée 28 mai —
  balises, v=H·d, taux local borné). La bonne propriété est l’**auto-similarité d’échelle**
  (mêmes lois partout, âges différents — « grand-père vs bébé »), pas la stationnarité.
- **Conséquence mesure (proposée, non exécutée).** d_w doit se lire en **comobile** : séparer
  la marche de l’inflation via une **fourmi à cadence fixe** (cadence 0 = balise = mesure pure
  de H ; cadence finie = marche+inflation ; différence = d_w comobile + H émergent).
- **Causalité = borne a priori uniforme [argument de preuve, R. Mirante].** Une borne indépendante
  de N tient à l’infini par construction. La causalité (taux local de mitose ≤ c, immuable)
  interdit l’emballement local → exclut la condensation → (H). Proposition : **c = vitesse
  maximale de la mitose** (c dérivé, non postulé ; cône de lumière = bord du cône de mitose).

-----

## 2. Lien CDT — résultat conceptuel majeur de la session [I, ancré sur arXiv vérifiés]

L’intuition « la causalité empêche la condensation » EST le mécanisme central de CDT
(Ambjørn–Loll–Jurkiewicz), résultat majeur et publié de la gravité quantique non-perturbative.

**Faits établis (CDT), vérifiés :**

- Sans causalité, les triangulations dégénèrent en phase **chiffonnée** (crumpled : simplexes
  agglutinés sur peu de sommets d’ordre énorme) ou **polymère ramifié** (filaments) ; pas de
  géométrie étendue. La causalité (structure de cône de lumière locale) sélectionne une **phase
  géométrique étendue de Sitter**. Réfs : arXiv:2401.09399 ; arXiv:1111.6938 ;
  Scholarpedia « Causal Dynamical Triangulation ».
- **Mécanisme précis = retrait des « baby universes ».** En DT euclidien, la fonction de
  partition est dominée par des bourgeons spatiaux (baby universes), entropiquement dominants
  mais dégénérés — source de l’aphysicalité. La causalité (pas de changement de topologie
  spatiale) les retire. Relation exacte (Ambjørn–Correia–Kristjansen–Loll) : intégrer les baby
  universes hors de DT donne CDT, et inversement. Réf : Found. Phys. 2015 (doi 10.1007/s10701-015-9972-8).
- En **2D, CDT est résolu analytiquement** par matrice de transfert ; limite continue universelle.
  Réfs : arXiv:1302.2440 ; arXiv:0911.4208. En 2+1 / 3+1D : Monte Carlo + action effective,
  **pas de [T] analytique fermé** (problème ouvert là aussi).
- La causalité locale suffit (sans feuilletage préféré) à faire émerger de Sitter. Réf :
  Jordan–Loll, arXiv:1305.4582.

**Transposition au Blob [I, hypothèse forte] :**

- clique/condensation du Blob ↔ baby universes/crumpled (entropiquement dominants, dégénérés).
  La condensation en clique localisée dans un RGG est un fait établi : **Chatterjee–Harel 2020,
  Ann. Probab. 48(2):574-621, arXiv:1401.7577**.
- Ce qui retire ces configurations dans le Blob : **−βD** (statique : une clique = degrés
  hétérogènes = D grand = pénalisé) **+ borne de mitose** (dynamique). Hypothèse : −βD est la
  **contrepartie énergétique** de la contrainte causale kinématique de CDT.
- **Neuf vs CDT :** causalité **dérivée** (du débit fini de mitose) au lieu de postulée, et
  **implémentée dynamiquement** (−βD + borne) au lieu d’imposée par décret → répond au problème
  que Loll cherche à résoudre (se débarrasser du feuilletage imposé).
- **Voie de preuve identifiée (non exécutée) :** matrice de transfert causale du Blob (outil
  déjà au corpus) → trou spectral → unicité de phase → (H) ; réaliste en basse dim/champ moyen.
  Pour 3D : viser le **diagramme de phase** au niveau de preuve CDT-standard (numérique +
  action effective), pas un [T] analytique fermé.

-----

## 3. Diagramme de phase mesuré (cette session) [M, exploratoire, N ≤ 3000]

**Moteur exact** (aucun proxy) : `build_initial` (RGG κ=6,6) + surcharge globale (β,τ) +
`mcmc_ON` (version O(N) **validée identique** au moteur de référence). Mesures : d_f
(`hausdorff_dim` consigné), d_s (loi de Weyl + heat-kernel).

**Grille (β,τ) à N=800** — transition NETTE, portée surtout par **τ** :

- τ froid (0,10) : **phase chiffonnée** — d_s ≈ 1,5 ; n_tri/N ≈ 9 ; D > 1. (sur-figé)
- τ modéré→chaud (0,5–2,0) : d_s ≈ 2,4–2,6 ; n_tri/N décroît ; D décroît.
- β = **régulateur** : réduit systématiquement D et n_tri/N (rôle anti-hétérogénéité confirmé),
  mais à τ froid ne suffit pas seul à éviter l’effondrement (diagramme 2D, comme CDT).

**Scaling en N (N=800→3000), deux méthodes (Weyl, heat-kernel) :**

- **Phase chiffonnée durablement décrochée** : d_s ≈ 1,1–1,7 à tout N, très loin du reste. ROBUSTE.
- **Blob nominal (0,30/0,50) nettement et durablement séparé** de la phase chiffonnée.

**Lecture (cohérente avec la cristallisation consignée, XV.13 [I]) :** l’axe τ est l’axe
gelé↔liquide↔bouillant ; la phase chiffonnée (τ→0) = sur-figé (glace dégénérée) ; le nominal
(τ=0,5) = fenêtre « liquide viable ». Lien formel : Kibble–Zurek (taux de trempe), consigné 25 mai.

**Fichiers :** `phase_diag_grille.py` (+`phase_diag_N800.json`), `phase_scaling.py`
(+`phase_scaling.json`), `phase_heatkernel_scaling.py` (+`phase_heatkernel_scaling.json`),
`phase_diag_calib.py`.

-----

## 4. Statut de d_s — rappel du consigné (NE PAS re-mesurer)

**Déjà établi le 25 mai (AC-30) :** la mesure brute du plateau intermédiaire [2,4] donne
d_s ≈ 2,5 à κ₀=6,6 (2,60 à N=800 ; 2,46 à N=2500), **croît avec κ₀** (→2,75 à κ₀=8). Le
« d_s = 3,045 [M] » d’origine a été **révisé par AC-30** : la mesure brute sous-estime ; le 3
ne se lit qu’après **calibration sur étalons** (réseaux à dimension connue). Les mesures brutes
de la présente session (~2,5) **retombent exactement** sur cette valeur consignée — rien de neuf,
rien à inscrire.

-----

## 5. Bilan honnête — acquis / non acquis

**Acquis (consignables [M]/[I]) :** existence d’une transition de phase dans le Blob ; phase
chiffonnée identifiée et durablement décrochée ; Blob nominal du bon côté ; lien CDT précis
(baby universes / causalité) avec réfs vérifiées ; transposition −βD = rempart anti-condensation ;
cohérence avec cristallisation (XV.13) et Kibble–Zurek (25 mai) ; reformulation auto-similarité.
**Non acquis :** convergence absolue de d_s vers 3 (mesure brute ~2,5, calibration étalons requise
— déjà su, AC-30) ; preuve analytique de (H)/unicité (ouvert, comme CDT en 3+1D).
**Verrou (B) : [T-star] inchangé. Aucune inscription master.**

-----

## 6. Leçon méthodologique de la session

Une partie des mesures de la session (plateau [2,4], scaling d_s) **re-dérivait des résultats
déjà consignés le 25 mai** (AC-30). Rappel de la règle d’or : **piocher dans le corpus AVANT de
calculer**. Le résultat NEUF et conservé est le lien CDT (§2) et la carte de phase (§3) ;
le reste était déjà acquis.

-----

## 7. Suites possibles (non engagées)

- (a) d_w en comobile + mesure de H émergent (nécessite la vraie mitose, non codée).
- (b) matrice de transfert causale du Blob (morceau analytique d’unicité de phase).
- (c) diagramme de phase au niveau CDT-standard (phase géométrique bordée crumpled/désordre),
  avec d_s lu via la calibration étalons consignée (pas la mesure brute).

-----

## ACTUALISATION 2 (30 mai, fin de session) — 3 phases, auto-corrections, [I] cycle, cible math

### A. Diagramme de phase consolidé [M, exploratoire, vrai moteur N=1000–1500]

- **τ froid (0,1)** : phase FILAMENTAIRE basse-dim (branched-polymer-like), d_s≈1,5, grand diamètre (37), faible volume/couche.
- **nominal (β=0,3 ; τ=0,5 ; κ=6,6)** : phase GÉOMÉTRIQUE COMPACTE 3D, d_s≈2,5–3, diamètre 16–17, V_max≈221.
- **κ croissant** : COMPACTION DENSE **sans crumpled pur**. Balayage κ=6,6→30 : diamètre 12,3→5,4 (effondre), n_tri/N 5,7→35,9 (explose) ; MAIS d_f plafonne ~2,8 (pas de divergence), maxdeg ~68 (pas O(N)), D 0,96→0,38 (degrés s’HOMOGÉNÉISENT).
- Paramètre d’ordre = **dimension (d_s/d_f) + structure (diamètre/densité)**, PAS cos².

### B. Auto-correction [AC] : marqueur cos² de Sitter NON discriminant

V(r)≈A cos²((r−r0)/B) ajuste bien PARTOUT (R²_dS : chiffonné 0,89 ; nominal 0,98 ; chaud 0,99) car tout graphe fini a une cloche V(r). Le « R²=0,99 de Sitter » (brique_de_Sitter.json, 18 mai) est **largement un artefact de finitude**, pas un marqueur de phase. À reclasser (esprit AC-30).

### C. −βD = rempart anti-crumpled [I→partiellement M]

−βD pénalise l’hétérogénéité des degrés → interdit la condensation en clique/vertex géant (Chatterjee-Harel, arXiv:1401.7577). Contrepartie énergétique de la contrainte causale CDT. Mesuré : à κ grand, D décroît (pas de condensation). Le Blob résiste au crumpled par construction.

### D. [I] Baby universe ↔ cycle local dissipatif — COHÉRENT, non prouvé

Réinterprétation : baby universe de CDT (bourgeon local) ↔ cycle local Ω⁰→Ω¹→Ω²→Ω³→effondrement→Ω⁰ (cosmogonie cyclique-locale V132). Différence féconde vs CDT : CDT supprime les baby universes (cherche un équilibre de Sitter) ; le Blob hors-équilibre/dissipatif en fait le MOTEUR. −βD trie : tue les bourgeons-condensation (cliques = crumpled), laisse vivre les cycles homogènes-dissipatifs. Cohérent avec thermo (t₂ s’allume à Ω³), 3 temporalités, substrat Ω⁰, R-4 (dissipation locale ∝ densité, XV.2 [M]).
À formaliser : baby universe CDT = SPATIAL (temps fixé) vs cycle Blob = TEMPOREL ; équivalence à construire.
Test possible [I]→[M] : renouvellement local des K4 le long du MCMC.
**STATUT : [I] cohérent** (ni [T] ni [M]). La cohérence interne achète [I], pas la preuve : être consistant avec d’autres postulats ≠ être démontré.

### E. Cible mathématique pour la suite

Verrou (B) d_w=2 reste **[T-star]**. Voie analytique la plus prometteuse identifiée : **matrice de transfert causale du Blob → trou spectral → unicité de phase (H) → d_w=2**. Analogue CDT 2D (soluble par matrice de transfert, arXiv:1302.2440 / 0911.4208).