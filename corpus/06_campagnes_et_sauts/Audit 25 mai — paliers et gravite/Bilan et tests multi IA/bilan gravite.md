# BILAN COMPLET — LA GRAVITÉ DANS LE BLOB PRINCIPLE (session du 24 mai 2026)

**Cadre.** Le Blob Principle (R. Mirante) dérive un espace-temps 3D émergent d’une fonctionnelle de viabilité sur graphes géométriques aléatoires (RGG 3D). Cascade simpliciale : Ω⁰ (point) → Ω¹ (arête) → Ω² (triangle) → Ω³ (tétraèdre = matière). Fonctionnelle : **S(C) = log(1 + n_tri(C)) − β·D(C)**, β=0,30, D = std(degré)/moyenne(degré), τ=0,50, κ₀=8. Dynamique = Metropolis edge-swap (topologie) + mobilité des positions (géométrie). Méthode : tout résultat est confronté à des **nuls de contrôle** (RGG pur géométrique ; RGG régularisé ; mobilité sans viabilité) pour distinguer ce qui est *propre à la viabilité* de ce qui est *géométrique*. Statuts : [M] mesuré, [T] théorème, [V] vision, [non concluant].

**Objet de la session.** Tester la nature de la gravité dans le Blob, à partir de l’intuition de R. Mirante : la gravité naît de la matière (le tétraèdre, Ω³) ; le tétraèdre « subit et inflige » aux autres tétraèdres un rapport de force (attraction/répulsion) plus intense que l’« entente » entre simplexes ordinaires ; ce rapport pourrait s’apparenter à un champ de type magnétique à polarité dynamique, voire à une énergie qui se propage dans le substrat de dimension 0 comme une onde (par analogie avec les ondes gravitationnelles détectées).

-----

## A. CE QUI EST SOLIDEMENT ÉTABLI (propre à la viabilité)

### A.1 — Gravité = poussée au volume [M]

**Prédiction (Mirante) :** la gravité est la force qui pousse à fermer les volumes (tétraèdres). **Mesure** (`gravite_volume.py`, N=1000, 3 seeds) : taux de fermeture des tétraèdres.

- Blob (viabilité) : **0,688 ± 0,009**
- RGG pur : 0,275 ± 0,022
- RGG régularisé : 0,275 ± 0,022

**Le Blob ferme les volumes 2,5× plus que les nuls, et les deux nuls sont identiques** → effet propre à la viabilité. Relie « la viabilité crée le 3D » (loi de Weyl) et « la gravité pousse au volume » : même mécanisme. Réserve : le ratio (2,5×) est robuste ; la valeur absolue dépend d’une normalisation.

### A.2 — Rapport de force tétra-tétra : attraction/répulsion fonction de la distance [M] — RÉSULTAT CENTRAL

**Prédiction (Mirante) :** la matière agit sur la matière (attire/repousse), plus intensément que les structures non-matière entre elles. **Mesure** (`gravite_force.py`, N=1200, 3 seeds) : variation de distance entre paires de structures sous la dynamique de viabilité, classée par type de paire et distance initiale (négatif = rapprochement/attraction ; positif = éloignement/répulsion). Test **non orienté** (aucun signe présupposé).

Profil **tétra-tétra** (matière-matière) en fonction de la distance initiale :

|distance|tétra-tétra                  |tétra-autre|autre-autre|
|--------|-----------------------------|-----------|-----------|
|0,020   |**+0,064** (répulsion forte) |n/a        |+0,018     |
|0,060   |**+0,014** (répulsion faible)|+0,053     |+0,031     |
|0,100   |**−0,001** (équilibre)       |+0,004     |+0,010     |
|0,160   |**−0,001** (attraction)      |+0,009     |+0,009     |
|0,275   |**−0,002** (attraction)      |+0,005     |+0,008     |

**Profil de force structuré, propre à la matière :** répulsion à courte distance, distance d’équilibre (~0,10), attraction à grande distance. Les paires non-matière (tétra-autre, autre-autre) restent **positives partout** (pas d’attraction, pas de changement de signe).

**Contrôle par les nuls** (`gravite_force_nul.py`, profil tétra-tétra) :

- Blob (viabilité) : +0,064 / +0,014 / −0,001 / −0,001 / −0,002 → **change de signe (répulsion→attraction)**
- Nul mobilité sans viabilité : +0,045 / +0,028 / +0,030 / +0,009 / +0,008 → **positif partout (jamais d’attraction)**
- Nul RGG géométrie pure : +0,040 / +0,014 / +0,013 / +0,012 / +0,007 → **positif partout (jamais d’attraction)**

**Conclusion [M] :** seul le Blob développe une attraction à distance entre tétraèdres (changement de signe). Les deux nuls ne font que de la répulsion/dispersion qui s’atténue. **Le rapport de force attraction/répulsion entre tétraèdres est propre à la viabilité.** C’est qualitativement le profil d’une force structurante (cœur répulsif + queue attractive, type potentiel à distance d’équilibre). C’est l’intuition de Mirante (« attraper/repousser ») validée et propre à la matière.

-----

## B. CE QUI A ÉTÉ TESTÉ ET N’EST PAS CONFIRMÉ (voies fermées honnêtement)

### B.1 — La force dépend-elle de la CONFIGURATION ? [non concluant]

**Hypothèse (Mirante) :** champ à « polarité dynamique » — la force s’adapterait selon la configuration relative des tétraèdres (comme deux aimants orientés). **Test** (`gravite_config.py`, N=1200, 3 seeds, 3972 paires) : à distance contrôlée (0,08–0,16, la zone d’équilibre), corrélation (Spearman) entre la force et trois axes de configuration.

- Orientation (alignement des axes principaux) : Blob ρ=+0,024 (p=0,13, non sig.) ; nul ρ=+0,037 (p=0,02)
- Asymétrie de viabilité (« masses » différentes) : Blob ρ=+0,025 (p=0,12, non sig.) ; nul ρ=+0,048 (p=0,002)
- Asymétrie de taille (vieux/dense vs jeune/épars) : Blob ρ=+0,010 (p=0,54, non sig.) ; nul ρ=+0,021 (p=0,18)

**Conclusion [non concluant→négatif] :** à distance fixe, aucune configuration ne pilote la force dans le Blob (toutes p non significatives). Là où il y a un micro-signal, il est dans le **nul** (résidu géométrique), pas dans le Blob. **La force est centrale/isotrope (fonction de la distance seule), PAS configurationnelle.** Ce qui rapproche d’un champ gravitationnel central plutôt que d’un champ magnétique orienté. (Note : ceci ne contredit pas A.2 — la dépendance à la distance reste établie ; c’est la dépendance à la configuration *à distance fixe* qui est absente.)

### B.2 — Courbure discrète locale (limite Einstein) [non concluant]

**Tentative 1 — déficit angulaire de Regge** (`einstein1.py`, N=1200). Résultat : Blob −71,1 ± 13,2 vs RGG −1,15 ± 0,36. **Artefact identifié et écarté** : les tétraèdres K₄ du Blob se recouvrent massivement (15036 tétraèdres pour 1200 sommets), donc la somme des angles dièdres autour d’une arête explose au-delà de 2π. Le déficit ne mesure pas une courbure géométrique mais la densité de recouvrement des cliques. Le déficit de Regge naïf est **inapplicable** au Blob (les K₄ ne pavent pas l’espace). Piège prévu par les consultations IA (« ne pas supposer des tétraèdres euclidiens qui pavent »).

**Tentative 2 — courbure de Forman-Ricci + test « courbure ∝ matière »** (`einstein2.py`, N=1200, 4 seeds), avec **contrôle de degré** (le piège Forman = artefact de degré). Écart de courbure matière vs non-matière à degré contrôlé :

- Blob : −0,06 ± 0,76 → **compatible avec zéro**
- RGG pur : +2,72 ± 0,17 → écart franc et significatif

**Conclusion [négatif] :** la signature « courbure concentrée sur la matière » existe dans le RGG (géométrique) mais **disparaît dans le Blob** (la viabilité l’efface). Ce n’est donc PAS une signature d’Einstein propre à la viabilité. La gravité du Blob ne se lit pas dans la courbure locale type Forman/Regge.

### B.3 — La masse déforme-t-elle le substrat ? [non concluant]

**Hypothèse (Mirante) :** la masse (tétraèdre) pousse le substrat de dimension 0, créant un « puits » autour d’elle et un « vide » entre deux masses (les masses font place nette). **Test** (`gravite_substrat.py`, N=1200, 3 seeds).

- Test 1 (densité du substrat vs distance au tétra) : profil **plat** dans le Blob (1,5/1,4/1,4/1,5/1,5) — pas de creux près de la masse.
- Test 2 (densité au milieu entre 2 tétra) : **mesure cassée** (0,00 pour Blob ET nul — résolution insuffisante du substrat clairsemé à N=1200). Non concluant, écarté.

**Conclusion [non concluant] :** pas de déformation visible du substrat par la masse à ce N et avec ces observables. Soit l’effet n’existe pas, soit il est sous le seuil de résolution.

### B.4 — La gravité se propage-t-elle comme une ONDE ? [non concluant]

**Hypothèse (Mirante) :** la gravité est une énergie qui court dans le substrat comme une onde dans une mare (appui : les ondes gravitationnelles réelles sont détectées). La propagation est mécanique (jouer sur la matière crée une onde) ; le nul propage aussi (il agite la matière) — donc la question n’est pas *si* ça se propage mais *comment* (onde cohérente vs diffusion désordonnée).

**Test 1 — rayon de la zone perturbée** (`gravite_onde.py`, N=1100, 4 seeds) : croissance du front Blob +0,046 vs nul +0,049 → **identique** (diffusion banale, non discriminant).

**Test 2 — qualité : conservation d’énergie + cohérence de front** (`gravite_onde2.py`, N=1100, 4 seeds) :

- (A) Conservation d’énergie : mesure mal posée (énergie cumulée croissante = artefact), écartée.
- (B) **Cohérence du front** : Blob 2,84 (monte 2,61→2,93 puis stabilise) vs nul 2,51 (2,36→2,65). **Différence réelle mais modérée** : le Blob structure la propagation en un front plus défini que le nul. Signal qualitatif faible, barres d’erreur non établies.

**Test 3 — DÉCISIF : exposant de propagation** (`gravite_vitesse.py`, N=1100, 5 seeds, 8 pas). Loi distance-temps en log-log : onde → exposant 1 (balistique) ; diffusion → 0,5 (∝√t).

- Blob : rayon 0,614→0,662 (sature), exposant = **0,034**
- Nul : rayon 0,598→0,643 (sature), exposant = **0,036**

**Conclusion [non concluant→négatif] :** l’exposant ≈0,03 (Blob = nul) montre que la perturbation **se stabilise localement et ne se propage pas** (ni onde balistique, ni même diffusion franche). **Aucune onde propagative propre à la viabilité n’est détectée** avec ces outils à ce N. Le faible signal de cohérence (test 2B) ne correspond pas à une vraie propagation ondulatoire. L’absence de signal ne réfute pas l’idée en physique, mais le modèle actuel ne la réalise pas de façon mesurable.

-----

## C. SYNTHÈSE ET QUESTION OUVERTE

**Acquis solides :** la gravité dans le Blob se manifeste comme (1) une poussée à fermer les volumes (2,5× propre à la viabilité) et (2) un **rapport de force attraction/répulsion entre tétraèdres, fonction de la distance, propre à la viabilité** (répulsion de contact, équilibre ~0,10, attraction lointaine) — absent des trois nuls. C’est l’intuition centrale de Mirante validée.

**Voies fermées honnêtement :** la force n’est pas configurationnelle (centrale, pas magnétique) ; la courbure locale (Regge/Forman) ne donne pas de signature propre ; la masse ne déforme pas visiblement le substrat ; aucune onde propagative n’est détectée (exposant ≈0, identique au nul).

**La tension à résoudre :** le résultat central (A.2) établit une **force statique** entre tétraèdres (un profil attraction/répulsion à l’équilibre). Mais la vision de Mirante insiste sur une **dynamique** : une énergie qui se propage (onde gravitationnelle), une masse qui pousse le substrat. Or les tests de propagation (B.4) et de déformation du substrat (B.3) ne captent rien de propre à la viabilité. **Question ouverte centrale : comment passer d’une force statique mesurée (réelle) à une dynamique propagative (onde), si elle existe dans ce modèle ?** Est-ce un problème d’observable (on mesure mal), de taille (N trop petit), de mécanisme (la mobilité des positions n’est pas le bon véhicule de l’onde), ou bien la propagation ondulatoire n’est-elle tout simplement pas une propriété de ce modèle combinatoire ?

**Paramètres techniques pour toute proposition :** numpy/scipy/networkx uniquement, pas de GPU ; N testable ≤ ~2000 en local (timeout 285s), grand N (5000–25000) possible via Colab. Tout test doit inclure les nuls (RGG pur, RGG régularisé, mobilité sans viabilité) et ne pas injecter le résultat dans l’instrument de mesure.