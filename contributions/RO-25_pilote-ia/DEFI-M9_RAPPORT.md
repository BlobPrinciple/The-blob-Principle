🇫🇷 Français · 🇬🇧 [English version](DEFI-M9_REPORT_EN.md)

# DEFI-M9 — L'aristocratie des sommets massifs : largement partagée entre chaînes, lente à rejoindre

*Contribution du pilote IA du laboratoire (Claude, Anthropic), 16 octobre 2026. Suite de l'avancée n° 3 ([DEFI-M7_RAPPORT.md](DEFI-M7_RAPPORT.md), issue #17). Relue par un second agent IA, relecteur hostile qui ne l'avait pas produite ; ses objections ont été intégrées (§3.3, §4). Non relue par une personne.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Aucun changement de statut.

## 1. Question

Le pont croissance → Gibbs (RO-25) exige qu'un sommet né par croissance devienne indiscernable d'un sommet tiré sous π_N (armature V347.1, p. 11, RO-25 : « la loi conditionnelle à N fixé reproduise, ou dérive, la mesure π_N de A_Gibbs »). DEFI-M7 a laissé un point ouvert : la masse triangulaire du nouveau-né restait en déficit moyen (−3,0 ± 2,0 à 512 balayages, [DEFI-M7_RAPPORT.md](DEFI-M7_RAPPORT.md) §3.3). DEFI-M9 demande si ce déficit se résorbe, ou si la viabilité fige une aristocratie de sommets massifs.

## 2. Protocole (fixé avant exécution)

- **Moteur** : `corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py`, importé tel quel ; paramètres canoniques gelés (κ = 6,6 ; β = 0,30 ; τ = 0,50 ; facteur de réservoir 1,6 ; τ_eff = τ/N ; thermalisation 120 N pas).
- **Naissance** : loi de DEFI-M7, reprise sans changement : point uniforme dans le cube, relié à ses k plus proches voisins (k = 3 ou 4, pour garder |E| = round(κ(N+1)/2)) ; ses paires à distance < 1,6 r entrent dans le réservoir ; r reste celui de N₀. **[H-loc]** (hypothèse de localité, [H] au sens de l'armature) : cette loi est posée, non dérivée (objet de DEFI-M8).
- **Observable** : la loi, et non plus la moyenne. Pour la masse x du nouveau-né (triangles incidents), on calcule son rang relatif u = (#{autres < x} + U·#{autres = x}) / (N − 1), U uniforme pour départager les ex aequo. **[H]** Si la chaîne atteint une loi stationnaire unique, le nouveau-né y est échangeable avec les autres sommets (position uniforme, même règle de réservoir au rayon r(N₀)), donc u suit la loi uniforme. Deux réserves : cette loi stationnaire n'est pas exactement ∝ exp(S/τ_eff) (le garde-fou deg ≤ 2, les 40 essais et la paire disjointe de {u, v} rompent la balance détaillée), et elle n'est pas le π_N canonique, qui prendrait r(N). Le même u est calculé pour un **sommet témoin** tiré au hasard parmi les sommets d'origine : il donne le plancher statistique à effectif égal.
- **Plan** : N₀ = 250, 500, 1 000, 2 000 ; 10 graines × 20 naissances successives = **200 naissances par taille** ; décalages t = 0, 16, 64, 256, 1 024, 2 048 balayages (1 balayage = |E| tentatives).
- **Statistiques** : moyenne de u (0,5 attendu) ; variation totale sur 10 classes de u contre l'uniforme (TV₁₀) ; test de Kolmogorov-Smirnov ; part de u > 0,9 (0,1 attendu).
- **Contrôles de figement** (ajoutés après lecture des résultats de naissance, et déclarés comme tels) : sur la chaîne stationnaire sans naissance, persistance du décile supérieur de masse sur 4 096 balayages ; puis trois chaînes sur le **même nuage de points** : A au départ canonique (paires les plus courtes), B au départ aléatoire (paires du réservoir tirées au hasard) avec une autre graine de Metropolis, et C, témoin ajouté à la demande du relecteur, au même départ que A avec une autre graine ; comparées après 4 096 balayages. On relève aussi la part du décile près des faces du cube et son recouvrement avec le décile de degré de réservoir.

## 3. Résultats

### 3.1 Le corps de la loi n'est plus distinguable de celui de la population après 16 à 256 balayages [M]

Rang relatif moyen u du nouveau-né (± erreur-type), p du test de Kolmogorov-Smirnov, et TV₁₀ ; entre parenthèses, le témoin.

| N₀ | t = 0 | t = 16 | t = 256 | t = 2 048 |
|---|---|---|---|---|
| 250 | 0,370 ± 0,013 ; p = 7·10⁻¹⁵ ; TV 0,28 (0,085) | 0,439 ± 0,020 ; p = 0,021 ; TV 0,12 | 0,463 ± 0,020 ; p = 0,16 ; TV 0,08 | 0,488 ± 0,020 ; p = 0,71 ; TV 0,065 (0,085) |
| 500 | 0,374 ± 0,015 ; p = 4·10⁻¹³ ; TV 0,27 (0,12) | 0,494 ± 0,019 ; p = 0,54 ; TV 0,12 | 0,492 ± 0,019 ; p = 0,59 ; TV 0,08 | 0,506 ± 0,020 ; p = 0,78 ; TV 0,10 (0,06) |
| 1 000 | 0,370 ± 0,015 ; p = 8·10⁻¹² ; TV 0,26 (0,10) | 0,507 ± 0,019 ; p = 0,33 ; TV 0,095 | 0,480 ± 0,019 ; p = 0,20 ; TV 0,09 | 0,518 ± 0,019 ; p = 0,62 ; TV 0,095 (0,07) |
| 2 000 | 0,362 ± 0,015 ; p = 1·10⁻¹² ; TV 0,25 (0,06) | 0,487 ± 0,020 ; p = 0,63 ; TV 0,105 | 0,485 ± 0,020 ; p = 0,79 ; TV 0,08 | 0,518 ± 0,019 ; p = 0,15 ; TV 0,10 (0,065) |

À la naissance, la loi du nouveau-né est nettement décalée vers le bas (TV₁₀ ≈ 0,26). Dès 16 balayages pour N₀ ≥ 500, et vers 256 balayages pour N₀ = 250, elle n'est plus distinguable de la loi uniforme **à 200 naissances** : TV₁₀ retombe au niveau du témoin (0,05 à 0,135 pour 200 tirages). Un non-rejet n'est pas une convergence : le témoin lui-même donne p = 0,011 une fois (N₀ = 2 000, t = 64). Ce temps ne croît pas de N₀ = 250 à N₀ = 2 000.

### 3.2 La queue massive est rejointe lentement [M]

Toutes tailles réunies (800 naissances) :

| t (balayages) | 0 | 16 | 64 | 256 | 1 024 | 2 048 |
|---|---|---|---|---|---|---|
| nouveau-nés dans le décile supérieur (u > 0,9) | 0,000 | 0,0625 | 0,070 | 0,0725 | 0,0725 | 0,085 |
| témoins dans le décile supérieur | 0,105 | 0,103 | 0,108 | 0,106 | 0,110 | 0,099 |
| p binomial (nouveau-nés contre 0,1) | 4·10⁻³⁷ | 2·10⁻⁴ | 0,004 | 0,008 | 0,008 | 0,175 |
| écart moyen de masse nouveau-né − population (pondéré) | −14,4 ± 0,05 | −5,8 ± 1,2 | −4,9 ± 1,2 | −4,3 ± 1,3 | −4,0 ± 1,3 | −3,2 ± 1,3 |

Le corps de la loi n'est plus distinguable ; la queue, si : jusqu'à 1 024 balayages, les nouveau-nés entrent dans le décile massif moins souvent que le hasard (6 à 7 % contre 10 %, p de 2·10⁻⁴ à 0,008), et ce sont ces sommets qui portent la moyenne (Gini de la masse ≈ 0,854, en-tête du moteur ; [DEFI-M7_RAPPORT.md](DEFI-M7_RAPPORT.md) §3.3). À 2 048 balayages, la part atteint 8,5 %, sans écart significatif à 10 % (p = 0,175), mais l'écart moyen reste de −3,2 ± 1,3. Les six décalages portent sur les mêmes naissances : ces p ne sont pas indépendants.

Le déficit moyen relevé par DEFI-M7 est donc réel, mais il n'est pas un déficit global : il se concentre dans la queue supérieure, qui se remplit lentement.

### 3.3 Le décile massif est largement partagé entre chaînes indépendantes [M, partiel]

- **Chaîne stationnaire** (N = 500 et 2 000, 3 graines chacune) : la corrélation de rang de Spearman entre la masse de chaque sommet à t₀ et à t₀ + t retombe à 0,34–0,54 dès 16 balayages et y reste jusqu'à 4 096 ; mais **72 % à 88 %** des sommets du décile supérieur à t₀ y sont encore après 4 096 balayages (10 % si le décile se renouvelait au hasard parmi tous les sommets ; de l'ordre de 15 % à 25 % s'il se renouvelait au hasard parmi les seuls sommets éloignés des bords, que le décile occupe surtout, voir plus bas). Sur un nuage à N = 250, le relecteur a observé une persistance de 0,96 à 1 024 balayages tombée à 0,36 à 4 096 : le décile n'est pas figé à toutes les tailles.
- **Trois chaînes, même nuage** (10 nuages, N = 250, 500, 2 000 ; `defi_m9_deux_chaines.json`), après 4 096 balayages :

| N | nuage | persistance de A | recouvrement A–B (autre départ) | recouvrement A–C (même départ) |
|---|---|---|---|---|
| 250 | 300 / 301 / 302 | 0,80 / 0,92 / 0,85 | 0,88 / 0,88 / 0,92 | 0,76 / 0,88 / 0,88 |
| 500 | 300 / 301 / 302 / 303 | 0,86 / 0,64 / 0,78 / 0,80 | **0,56** / 0,72 / 0,96 / 0,92 | **0,96** / 0,74 / 0,90 / 0,92 |
| 2 000 | 300 / 301 / 302 | 0,82 / 0,75 / 0,75 | 0,95 / 0,81 / 0,80 | 0,955 / 0,84 / 0,79 |

Sur 9 nuages sur 10, deux chaînes de départs différents désignent autant de sommets massifs communs que deux chaînes de même départ (A–B ≈ A–C, de 0,72 à 0,96) : le décile y est fixé par le nuage, non par l'état initial. Sur le nuage 300 à N = 500, A–B = 0,56 contre A–C = 0,96 : là, le décile garde la mémoire de l'état initial sur 4 096 balayages.

- **Ce que « fixé par le nuage » recouvre** : le cube n'est pas périodique, et le décile massif évite les bords (part des sommets à moins de r d'une face : 45 % à 78 % de tous les sommets, 0 % à 56 % du décile). Le décile de masse recouvre le décile de degré de réservoir à 28 % à 88 % (ce dernier, entier à nombreux ex aequo, contient 10,0 % à 12,8 % des sommets, ce qui gonfle légèrement ce recouvrement). Une part de cette hiérarchie est donc un effet de boîte finie.

Ce contrôle ne teste pas l'âge : dans ces chaînes, tous les sommets ont le même âge. Il établit que, sur la plupart des nuages, la hiérarchie massive est largement une propriété du nuage de points (positions, bords compris) et non de l'histoire de la chaîne. Que le nouveau-né rejoigne à terme la masse que lui assigne sa position est une **[H]**, non mesurée ici : un premier essai du relecteur (N₀ = 500, 100 naissances, chaîne indépendante sur le même nuage) donne une corrélation de rang de 0,235 entre masse en croissance et masse d'équilibre, et ne tranche pas.

### 3.4 Recoupement par une seconde implémentation du même noyau [M]

`defi_m9_second_moteur.py` réécrit le modèle à partir de sa spécification, sans importer le moteur du corpus (matrice d'adjacence dense, triangles par diag(A³)/2, générateur aléatoire distinct). C'est un recoupement de code, pas de modèle : même auteur, même spécification, mêmes particularités du noyau de proposition. Point de travail retrouvé : n_tri/N = 5,02 et Gini(masse) = 0,821 à N = 250 (10 graines), 5,38 et 0,853 à N = 500 (6 graines), pour 5,4 et 0,854 annoncés (en-tête du moteur, N = 1 200) ; le relecteur a mesuré le moteur canonique à N égal : 5,29 et 0,830 (N = 250), 5,16 et 0,846 (N = 500), compatibles vu l'étalement entre graines (4,6 à 6,4).

- Naissances (120 à N₀ = 250, 72 à N₀ = 500) : u moyen 0,384 et 0,348 à t = 0 ; 0,485 et 0,528 à 256 balayages ; 0,485 et 0,455 à 2 048 balayages (KS : p = 0,53 et 0,06). Part dans le décile supérieur à 2 048 balayages : 8,3 % et 9,7 %. Tableau voisin de §3.1, plus bruité (u = 0,455, p = 0,06 à N₀ = 500) ; l'effectif ne permet pas de tester la queue.
- Deux chaînes (N = 500, 4 nuages) : recouvrement 0,87 à 0,96, persistance 0,72 à 0,96. Même lecture que les 9 nuages concordants du §3.3 (le témoin C n'a pas été rejoué sur ce second code).

## 4. Ce qui est établi, ce qui ne l'est pas, le point le plus fragile

- **Mesuré [M]** (moteur canonique, N₀ = 250 à 2 000, loi de naissance [H-loc]) : à 200 naissances par taille, le corps de la loi des masses du nouveau-né n'est plus distinguable de celle de la population après 16 à 256 balayages, sans croissance avec N ; les nouveau-nés entrent dans le décile massif moins souvent que le hasard jusqu'à 1 024 balayages au moins.
- **Mesuré, partiel [M]** : sur 9 nuages sur 10, le décile massif est largement partagé par des chaînes de départs différents ; il évite les bords du cube.
- **Non établi [OPEN]** : le rôle de l'âge (ordre des naissances) dans la hiérarchie ; le temps qu'il faut pour que la part des nouveau-nés dans le décile massif atteigne 10 %, et sa dépendance en N ; toute borne démontrée.
- **[H]** Lecture pour la cosmogonie : sur le moteur canonique, une grande part de la hiérarchie des sommets massifs tient au nuage de points (positions et bords). Si le Livre I attend une hiérarchie héritée de la généalogie, ces mesures ne la montrent pas ; elles ne l'excluent pas non plus.
- **Points fragiles** : (1) la loi de naissance est posée [H-loc], et r reste celui de N₀, si bien que 20 naissances ajoutent jusqu'à 8 % de points à rayon fixe pour N₀ = 250 (1 % pour N₀ = 2 000) ; (2) le désordre figé des positions et les bords non périodiques sont des propriétés du moteur Rips [ARCH], pas nécessairement du Blob : ce résultat dit peut-être plus sur A_Gibbs que sur la cosmogonie ; (3) les contrôles de figement (§3.3) ont été ajoutés après lecture des premiers résultats, et le témoin C à la demande du relecteur ; (4) le calcul principal a été interrompu pendant N₀ = 2 000 et repris en deux moitiés (graines 0 à 4 et 5 à 9), avec les mêmes graines, puis fusionné (`defi_m9_fusion.py`) ; les données brutes par naissance ne sont archivées que pour N₀ = 2 000 ; (5) le témoin est classé dans une population qui contient jusqu'à 19 nouveau-nés récents, encore en déficit (biais faible vers le haut) ; (6) aucune relecture humaine.

## 5. Effet proposé et prochain pas

- DEFI-M9 reste **ouvert**, avec un résultat partiel inscrit : la hiérarchie massive est en grande partie une propriété du nuage ; le temps d'accès du nouveau-né à la queue et le rôle de l'âge restent ouverts.
- Le coût du pont estimé par DEFI-M7 (de l'ordre de 10 |E| tentatives par naissance) vaut pour le corps de la loi ; pour la queue massive, il est au moins de l'ordre de 100 fois plus élevé (déficit encore significatif à 1 024 balayages) et reste à mesurer.
- **Défi dérivé DEFI-M10 — la lente accession au décile massif** : combien de balayages faut-il pour que la part des nouveau-nés dans le décile supérieur atteigne 10 %, et ce temps croît-il avec N ? Le nouveau-né rejoint-il la masse d'équilibre de sa position ? Livrable : part mesurée à ± 1 point (au moins 1 000 naissances par taille, au moins deux tailles) jusqu'à au moins 16 384 balayages, comparée nouveau-né par nouveau-né à la masse d'équilibre de sa position (chaîne indépendante sur le même nuage), de préférence dans une boîte périodique pour écarter l'effet de bord ; ou borne démontrée.

## Reproduire

```bash
pip install numba                                                     # facultatif mais conseillé
python3 contributions/RO-25_pilote-ia/defi_m9_aristocratie.py         # plan complet, ≈ 1 h avec numba
python3 contributions/RO-25_pilote-ia/defi_m9_aristocratie.py --figement-seul --sortie defi_m9_figement.json
python3 contributions/RO-25_pilote-ia/defi_m9_deux_chaines.py         # ≈ 10 min
python3 contributions/RO-25_pilote-ia/defi_m9_second_moteur.py        # ≈ 4 min
python3 contributions/RO-25_pilote-ia/defi_m9_deux_chaines_second_moteur.py   # ≈ 30 s
python3 contributions/RO-25_pilote-ia/defi_m9_queue.py                # analyse de la queue
```

Le calcul déposé a été mené en morceaux (`--tailles 2000 --graines 0:5`, puis `5:10`, `--sans-figement`), puis fusionné par `defi_m9_fusion.py`. Python 3.13.16, numpy 2.5.3, scipy 1.18.1, numba 0.68.0. Sorties : `defi_m9_resultats.json`, `defi_m9_queue.json`, `defi_m9_figement.json`, `defi_m9_deux_chaines.json`, `defi_m9_second_moteur.json`, `defi_m9_deux_chaines_second_moteur.json`.
