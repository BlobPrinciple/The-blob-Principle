🇫🇷 Français · 🇬🇧 [English version](DEFI-M14_REPORT_EN.md)

# DEFI-M14 — Temps de séjour dans l'aristocratie à n = 225 et 257 : la loi en √n tient à 225, est dépassée de 30 % à 257 (verdict selon le critère écrit d'avance : non tranché) ; un point exploratoire à n = 289 indique une accélération

*Contribution du pilote IA du laboratoire (Claude, Anthropic), 6 novembre 2026. Déposée comme toute contribution, en issue `ia-assistee`. Prédictions et critère de décision écrits avant toute mesure (`defi_m14_prediction.py`) ; mesure par deux moteurs sans code commun pour le noyau ; relue par un second agent IA en relecteur hostile (voir § 6) ; **aucune relecture humaine à ce stade**.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Ce rapport ne change aucun statut épistémique. Il fournit la mesure demandée par DEFI-M14 (RO-25, RO-20) à n = 257, sur graphes abstraits seulement, sans trancher la question au sens du critère fixé d'avance ; aucune borne n'est démontrée, l'asymptotique reste ouverte et le moteur canonique n'est pas traité.

## 1. La question

DEFI-M14 (#44), ouvert par [DEFI-M13_RAPPORT.md](DEFI-M13_RAPPORT.md), § 7 : sur graphes abstraits à degré moyen 4, sous π ∝ exp(n·S_sim/τ), le demi-temps t½ d'autocorrélation de T_v (triangles contenant le sommet v) suit ln t½ = 0,964·√n − 1,77 de n = 17 à 193 ([DEFI-M12_RAPPORT.md](DEFI-M12_RAPPORT.md)), et le temps de séjour dans l'aristocratie vaut 1,5 à 1,9 fois t½ ([DEFI-M13_RAPPORT.md](DEFI-M13_RAPPORT.md), § 3.2). À n = 257, la dynamique avait été jugée hors de portée ; la barrière d'équilibre y prédisait ln t½ entre 13,6 et 15,9 selon la calibration, contre 13,68 pour la loi en √n (même rapport, § 3.4). **La loi en √n est-elle asymptotique, ou un effet de croisement ?** Livrable : t½ ou temps de séjour mesuré à n = 257, et si possible au-delà, avec barres d'erreur.

Sources qui font foi : armature V347.1, § II.0 (p. 10 : strates A_gen et A_Gibbs, S_sim(C) = log(1 + n_tri(C)) − β·D(C) ; « Deux ponts sont absents : A_gen→A_Gibbs (RO-25) et A_Gibbs→B (RO-08) ») ; encadré RO-25 (p. 11 : une dynamique jointe dont « la loi conditionnelle à N fixé reproduise, ou dérive, la mesure π_N » ; falsificateur : « aucune extension markovienne locale » ne possède à la fois la généalogie voulue et cette loi) ; axiomes A3–A4 [A][ARCH] (p. 18 : β = 0,30 ; π_N(C) = Z_N⁻¹ exp(N·S_sim(C)/τ), τ = 0,50) ; A0′ (p. 18 : « Sous ergodicité, ces poids gouvernent les fréquences empiriques de résidence à long terme » ; « persister » n'est pas défini, RO-20). Numéros de page du PDF `corpus/00_master_courant/BLOB_PRINCIPLE_MASTER_V347_1_ARMATURE_CANONIQUE.pdf`, vérifiés par extraction de texte. Cadre de calcul inchangé depuis DEFI-M8 (hypothèse H-abs, [DEFI-M8_RAPPORT.md](DEFI-M8_RAPPORT.md), § 2) : graphes simples étiquetés abstraits, D = écart-type de population des degrés / degré moyen, échanges de Metropolis à nombre d'arêtes M = 2n fixé, λ = n/τ = 2n ; un balayage vaut M échanges.

## 2. Méthode

**Prédictions écrites avant la mesure (`defi_m14_prediction.py`, exécuté le 6 novembre 2026 à 08 h 49 UTC ; première chaîne lancée vers 08 h 50).** L'antériorité ne repose que sur l'horodatage des fichiers dans l'environnement du pilote : rien n'a été déposé publiquement avant la mesure, ce n'est donc pas un préenregistrement vérifiable par un tiers. À partir des seuls séjours de DEFI-M13 (n = 25 à 193), il fixe les prédictions de séjour à n = 225 et 257 : ajustement de ln séjour en √n sur n ≥ 65 (5,6·10⁵ et 1,55·10⁶ balayages) ou n ≥ 97 (5,3·10⁵ et 1,43·10⁶) ; loi t½ de DEFI-M12 × 1,63 (5,3·10⁵ et 1,43·10⁶) ; ajustement linéaire en n (8,8·10⁵ et 3,6·10⁶ depuis n ≥ 65 ; 2,5·10⁶ à n = 257 depuis n ≥ 97) ; calibration linéaire de DEFI-M13 × 1,63 (5,9 à 13·10⁶ à n = 257). **Critère** : la loi en √n « survit » à n = 257 si le séjour mesuré tombe dans [0,6 ; 1,7]·10⁶ ; elle est « contredite par une croissance plus rapide » au-dessus de 3·10⁶ ; entre les deux, non tranché. Le point n = 289 a été ajouté après la mesure à 257 ; il n'est couvert par aucune prédiction écrite d'avance : il est **exploratoire**.

**Grandeur (`defi_m14_sejour.py`)** : celle de `defi_m13_sorties.py`, inchangée. Tous les Δ balayages, T_v de tous les sommets ; un sommet devient « aristocrate » quand T_v ≥ T_haut, « roturier » quand T_v ≤ 2, et garde son état entre les deux ; T_haut = moitié du T du minimum aristocratique du profil de DEFI-M13 (n = 193 : 112 → 56 ; n = 257 : 136 → 68 ; n = 225 : 124 → 62, interpolé ; n = 289 : 148 → 74, extrapolé, aucun profil n'y ayant été mesuré). Séjour = temps total passé aristocrate (sommets × balayages) / nombre de sorties. Δ = t½ prévu par la loi de DEFI-M12 / 40, comme dans DEFI-M13 (21 921 balayages à n = 257). En plus : autocorrélation poolée de T_v (tous les sommets, moyenne commune) et son t½.

**Deux moteurs sans code commun pour le noyau.** **A** : noyau de `defi_m12_lenteur.balayer` (matrice booléenne, générateur numba), départ « noyau planté » de `defi_m12_lenteur.depart`, autocorrélation par FFT. **B** : noyau de `defi_m12_second_moteur.avancer_compte` (mots de 64 bits, popcount, PCG64 en lots), départ planté reconstruit dans `defi_m14_sejour.py`, T_v par la diagonale de A³, autocorrélation par somme directe. Contrôles exacts : n_tri = tr(A³)/6 en fin de chaîne (A), à chaque enregistrement (B). Barre d'erreur du moteur B : huit blocs consécutifs par chaîne, séjour par bloc, erreur-type sur les seize blocs.

**Campagne.** n = 257 : deux chaînes A et deux chaînes B de 2·10⁷ balayages après 10⁶ de rodage (≈ 15 t½, ≈ 10 séjours par chaîne). n = 225 : deux chaînes B de 1,3·10⁷. n = 289 : deux chaînes B de 3·10⁷ (≈ 5 t½, ≈ 3,4 séjours par chaîne), et une chaîne A de 1,5·10⁷ ajoutée pendant la relecture. Contrôle à n = 193 : deux chaînes B de 4·10⁶, à comparer aux chaînes A de DEFI-M13. Contrôle du départ à n = 257 : deux chaînes B partant d'un graphe aléatoire (sans clique plantée), 3·10⁶ de rodage, 1,2·10⁷ de production.

**Écart de méthode, déclaré.** `defi_m14_sejour.py` a été modifié deux fois en cours de campagne, sans toucher aux noyaux ni à la grandeur mesurée : après les chaînes A à n = 257 (ajout de la sortie par blocs, absente de ces JSON) et après les chaînes B à 193, 225 et 257 (seuil à n = 289 ; option de départ aléatoire, d'où la clé `depart` absente des premiers JSON). Le script déposé est la dernière version ; il reproduit les premières chaînes à l'identique pour une même graine (les ajouts n'appellent aucun nombre aléatoire).

## 3. Résultats

### 3.1 Les deux moteurs concordent [M]

| | chaînes (séjour, balayages) | séjour poolé | sorties | t½ par chaîne |
|---|---|---|---|---|
| n = 193, A (DEFI-M13) | 184 637 ; 179 059 | 181 814 | 324 | — |
| n = 193, B | 192 149 ; 172 039 | 181 500 ± 5 300 | 728 | 117 873 ; 107 827 |
| n = 257, A | 2 070 971 ; 1 971 460 | 2,020·10⁶ | 359 | 1 272 835 ; 1 239 095 |
| n = 257, B | 2 047 446 ; 1 981 036 | 2,014·10⁶ ± 0,072·10⁶ | 360 | 1 345 007 ; 1 310 941 |

À n = 257, les deux moteurs concordent à 0,3 % sur le séjour ; leurs t½ sont compatibles (ceux de B sont 6 % au-dessus de ceux de A, pour un écart interne d'environ 3 % par moteur, soit environ 2 écarts-types) ; le nombre moyen d'aristocrates est 18,13 à 18,14 dans les quatre chaînes, identique sur les deux moitiés de chaque chaîne (aucune dérive) ; le T_v maximal moyen, 138,4, retrouve le minimum aristocratique du profil d'équilibre de DEFI-M13 (136). À n = 193, le moteur B retrouve le séjour de DEFI-M13 à 0,2 % près. **Contrôle du départ** : deux chaînes B partant d'un graphe aléatoire, sans clique plantée, forment d'elles-mêmes l'aristocratie (18,15 aristocrates en moyenne) et donnent un séjour de 1,85·10⁶ (1 814 328 ; 1 891 687 ; 235 sorties), 0,92 fois celui des chaînes plantées, avec des chaînes 1,7 fois plus courtes : le résultat ne vient pas du départ planté, commun aux deux moteurs.

### 3.2 Le séjour à n = 225, 257 et 289 [M ; n = 289 exploratoire]

| n | 193 | 225 | 257 | 289 |
|---|---|---|---|---|
| séjour poolé (balayages) | 1,818·10⁵ | 5,58·10⁵ ± 0,12·10⁵ | 2,02·10⁶ ± 0,07·10⁶ | 8,92·10⁶ ± 0,76·10⁶ |
| ln séjour | 12,11 | 13,23 | 14,52 | 16,00 |
| prévu, √n depuis n ≥ 65 | — | 5,61·10⁵ | 1,55·10⁶ | — |
| mesuré / prévu | — | 0,99 | 1,30 | — |
| ln t½ par chaîne | 11,68 ; 11,59 | 12,77 ; 12,74 | 14,06 ; 14,03 ; 14,11 ; 14,09 | 15,53 ; 15,54 |
| ln t½, loi de DEFI-M12 | 11,62 | 12,69 | 13,68 | 14,62 |
| aristocrates (moyenne) | 16,5 | 17,4 | 18,1 | 19,0 |
| séjour / t½ | 1,61 | 1,61 | 1,52 à 1,61 | 1,60 |

(Séjour à 193 : moteur A, DEFI-M13 ; ln t½ et séjour/t½ à 193 : moteur B ; 225 et 289 : moteur B ; 257 : moyenne géométrique des moteurs A et B. Barres : erreur-type par blocs du moteur B ; les sorties par bloc sont sous-dispersées, ces barres ne sont donc pas plus larges que celles de Poisson et ne comptent aucune erreur systématique ; à 289, chaque bloc est plus court qu'un séjour.)

- **n = 225** : la prédiction en √n écrite d'avance est vérifiée (rapport 0,99 ; 1,06 contre la loi de DEFI-M12).
- **n = 257** : séjour 2,02·10⁶, ln t½ = 14,03 à 14,11. Selon le critère fixé d'avance, le verdict est **non tranché** (entre 1,7 et 3·10⁶). La calibration linéaire de DEFI-M13 (ln t½ = 15,1 à 15,9 ; séjour 5,9 à 13·10⁶) est exclue : mesuré 3 à 6,5 fois plus court. La loi en √n prolongée (séjour 1,43 à 1,55·10⁶) est dépassée : mesuré 1,30 à 1,41 fois plus long ; en comptant l'incertitude de l'extrapolation elle-même (Poisson sur les points de DEFI-M13), l'écart vaut environ 4 écarts-types, moins si l'on compte les résidus de l'ajustement. Ce test fait après coup ne remplace pas le critère fixé d'avance, qui dit « non tranché ».
- **n = 289** (exploratoire : ajouté après coup, seuil extrapolé, ≈ 3,4 séjours par chaîne) : séjour 8,9·10⁶, ln t½ = 15,53, soit 2,5 fois la loi de DEFI-M12. Les deux chaînes B donnent exactement le même séjour (64 sorties et même temps aristocrate chacune) : coïncidence vérifiée, leurs blocs, leurs états intermédiaires et leurs t½ diffèrent. Contrôles courts, ajoutés pendant la relecture : une chaîne du moteur A de 1,5·10⁷ balayages donne 1,02·10⁷ (28 sorties ; ln t½ = 15,54 ; 19,02 aristocrates), et la chaîne indépendante du relecteur 1,4·10⁷ ± 0,4·10⁷ (16 sorties) ; tous sont très au-dessus de l'extrapolation en √n (3,6 à 4,0·10⁶), mais leurs incertitudes sont larges.
- Le rapport séjour/t½ reste entre 1,52 et 1,61 : le t½ de DEFI-M12 continue de suivre l'appartenance à l'aristocratie.

### 3.3 La pente locale monte à partir de n ≈ 225 [M jusqu'à 257, H au-delà]

Pente locale Δ ln séjour / Δ√n : 0,93 (49 → 65) ; 1,04 (65 → 97) ; 0,98 (97 → 129) ; 0,95 (129 → 193) ; 1,01 (193 → 225) ; **1,25 (225 → 257) ; 1,53 (257 → 289)**. Jusqu'à n = 225, la pente est constante à ± 0,05 près, c'est la loi en √n ; sur 225 → 257 (deux moteurs à 257, un seul à 225), elle vaut 1,25. Erreurs-types des deux dernières pentes, propagées depuis les blocs : 0,04 et 0,10 ; l'écart à 1 vaut donc environ six et cinq erreurs-types (corrélation entre sorties non prise en compte au-delà des blocs). **[H]** Le point exploratoire 289 prolonge cette montée (1,53) : la croissance serait plus rapide que exp(c·√n) au-delà de n ≈ 225. Cette lecture repose sur un point non prévu d'avance ; elle demande un second moteur à pleine longueur, un profil d'équilibre à n = 289 et des tailles plus grandes.

### 3.4 Forme asymptotique : non déterminée [H]

Ajustement ln séjour = a + b·n^γ, pondéré par l'erreur de Poisson 1/√(sorties) (scipy `curve_fit` ; la version non pondérée, recoupée par balayage de γ avec moindres carrés écrits à la main, figure dans `defi_m14_analyse_sortie.txt`, mais avec trois paramètres sur quatre à sept points elle n'a pas de précision utile) : γ = 0,37 ± 0,04 sur n = 65 à 193 (χ² = 0,1 pour 1 ddl) ; 0,41 ± 0,03 jusqu'à 225 (1,7 pour 2) ; 0,50 ± 0,02 jusqu'à 257 (33,6 pour 3) ; 0,54 ± 0,02 jusqu'à 289 (77 pour 4) ; 1,28 ± 0,09 sur 129 à 289 seuls (6,0 pour 2). L'exposant effectif monte quand on ajoute les grandes tailles, et les χ² deviennent énormes : avec les barres de Poisson, aucune loi exp(b·n^γ) à γ fixé ne décrit l'ensemble, mais ces barres ne comptent ni la corrélation des sorties ni d'éventuelles erreurs systématiques, et une structure non lisse n'est pas exclue. **[H]** La loi exp(0,96·√n) de DEFI-M12 serait une loi de plage (n = 17 à 225) plutôt qu'une asymptotique. Ce que devient la croissance au-delà de n = 289 (exp(c·n), plus vite encore, ou un nouveau palier) reste **[OPEN]**.

## 4. Lecture pour le pont RO-25 et pour RO-20

- **[M]** La lenteur aristocratique ne se tasse pas à n = 257 : le séjour y dépasse de 30 à 41 % l'extrapolation en √n. **[H]** Avec le point exploratoire 289 : de n = 225 à 289 (√n passe de 15 à 17), le séjour serait multiplié par 16, contre 6,9 à 7,1 pour la loi en √n (selon la loi de DEFI-M12 ou l'ajustement fixé d'avance).
- **[H]** Le coût d'un pont croissance → Gibbs qui laisserait chaque nouveau-né rejoindre sa masse triangulaire d'équilibre avant la naissance suivante, déjà sur-polynomial dans DEFI-M12 (§ 4 de ce rapport-là), croît encore plus vite que ne le disait la loi en √n. Même réserve qu'alors : RO-25 n'est pas réfuté ; le falsificateur de l'armature (p. 11) porte sur l'existence d'une extension markovienne, pas sur sa vitesse ; un autre noyau de relaxation (échanges non locaux, mouvements collectifs) peut mélanger plus vite, et rien ici ne concerne le moteur canonique.
- **[H] Vers RO-20.** Le séjour dans la clique dominante, de 10⁵ à 10⁷ balayages sur cette plage, est une durée propre au noyau et croissante avec n ; c'est un candidat chiffrable pour « persister » (séjour plus long que l'intervalle entre deux naissances), distinct de π > 0 (A0′, p. 18), qu'il reste à formuler.
- **[OPEN]** Pourquoi la pente monte-t-elle vers n ≈ 225 ? Le nombre d'aristocrates (16,5 → 19,0) et leur T_v maximal moyen (112 → 153) croissent régulièrement sur 193–289 ; la mesure ne dit pas quel événement (perte d'arêtes une à une, ou réorganisation collective de la clique) contrôle la sortie.

## 5. Ce qui est établi, ce qui reste à vérifier, le point le plus fragile

- **Établi** (deux moteurs à n = 193 et 257, départ planté et départ aléatoire à 257, répétitions, prédictions écrites d'avance, mesure indépendante du relecteur à 193 et 257) : séjour et t½ à n = 257 ; la mesure y dépasse la loi en √n de 30 à 41 % (verdict selon le critère fixé d'avance : non tranché) ; la calibration linéaire de DEFI-M13 (ln t½ = 15 à 16 à n = 257) est exclue.
- **Mesuré, un seul moteur** : n = 225, où la loi en √n est vérifiée (moteur B, qui retrouve le moteur A à 0,2 % près à n = 193 et à 0,3 % près à n = 257).
- **Exploratoire** : n = 289 (moteur B à pleine longueur, contrôles courts par le moteur A et par le relecteur) et la montée de la pente au-delà de 257.
- **À vérifier** : tout, par une personne ; n = 289 par le moteur A à pleine longueur et par un profil d'équilibre (le seuil y est extrapolé) ; n ≥ 321 ; la forme asymptotique ; une coordonnée de réaction qui explique la montée de la pente ; le moteur canonique (DEFI-M10).
- **Point le plus fragile** : n = 289. Chaque chaîne n'y couvre qu'environ 3,4 séjours (128 sorties en tout, corrélées : ce sont les mêmes 19 places qui se renouvellent), le rodage (10⁶ balayages) n'y vaut que 0,11 séjour, le seuil T_haut = 74 y est extrapolé (le rapport T_haut / T_v maximal reste entre 0,48 et 0,50 à toutes les tailles), et aucune prédiction n'avait été écrite avant la mesure. Le verdict sur n = 257 seul est « non tranché » au sens du critère fixé d'avance ; la conclusion « la pente monte » repose sur 257 et 289 ensemble.

## 6. Relecture hostile

Un second agent IA, qui n'a pas produit ce travail, a recalculé chaque nombre contre les JSON, contrôlé le code (seuils, hystérésis, comptage, équivalence en loi des deux noyaux, même S_sim, même Δ), vérifié les citations de l'armature (p. 10, 11, 18 : conformes) et refait la mesure avec son propre noyau écrit de zéro (listes de voisins, générateur xoshiro256**) : séjour 15 400 ± 350 à n = 129 (DEFI-M13 : 16 301), 193 060 ± 12 000 à n = 193 (181 800), 2,02·10⁶ ± 0,27·10⁶ à n = 257 (2,02·10⁶), 1,4·10⁷ ± 0,4·10⁷ à n = 289 (8,9·10⁶). Il a testé à n = 129 les effets qui pourraient fabriquer la montée de pente : seuil (± 12 %, rapport T_haut / T_v maximal constant entre tailles), pas Δ (un Δ plus grand allonge le séjour ; Δ/t½ diminuant avec n, ce biais va contre la conclusion), chaînes courtes à départ planté et départ aléatoire (pas de biais significatif). Il conclut que la mesure tient et que l'interprétation était sur-affirmée.

**Bloquants retenus et corrigés** : (1) le titre et les § 3.3, 3.4 et 7 affirmaient « la loi en √n ne se prolonge pas au-delà de n ≈ 225 » alors que le critère fixé d'avance dit « non tranché » à 257 et que la conclusion reposait sur le point 289, ajouté après coup : titre réécrit, 289 déclaré exploratoire, conclusions passées en [H] ; (2) « 6,5 à 8 erreurs-types » ignorait l'incertitude de l'extrapolation : environ 4 écarts-types, test après coup qui ne remplace pas le critère ; (3) les exposants du § 3.4 avaient des précisions sans objet (fits non pondérés, 1 ddl) : refaits pondérés, avec χ² ; (4) « 7,7 » faux : 6,9 à 7,1 ; (5) étiquettes [M] des conclusions sur 289 passées en [H] ; (6) « préenregistré » non vérifiable par un tiers (rien de déposé avant la mesure) et script modifié après les premières chaînes : déclarés au § 2. **Mineurs retenus** : séjour poolé 181 814 (non 181 848) ; légende de la colonne 193 ; « ≈ 15 t½ » (non 10) à 257 ; « 1,7 fois » (non deux fois) ; sens de « sous-estime » ; n = 225 retiré d'« Établi » ; T_v 112 (non 111) ; t½ A/B « compatibles » ; nature des barres par blocs (sous-dispersion, blocs plus courts que le séjour à 289) ; rodage court à 289 ; coïncidence des deux chaînes B à 289 signalée ; contrôle par le moteur A à 289 ajouté ; lien anglais.

## 7. Prochain pas sur le chemin de preuve (P1)

**DEFI-M16 — Après √n : la loi de la lenteur aristocratique.** Sur graphes abstraits à degré moyen 4 sous la mesure de l'armature, le séjour dans l'aristocratie suit exp(0,96·√n) jusqu'à n ≈ 225, la dépasse de 30 % à n = 257, et un point exploratoire à n = 289 indique une accélération (pente locale en √n de 1,0 à 1,5 entre n = 193 et 289 ; ce rapport). Livrable : le séjour à n ≥ 321 (deux moteurs, profil d'équilibre à la même taille) et la forme de la croissance ; ou le mécanisme de sortie (chemin le plus probable, échantillonnage de chemins de transition) qui explique le changement de pente vers n ≈ 225 ; ou une borne démontrée. Dans tous les cas, le critère de décision est déposé publiquement (issue ou commit) avant la mesure.

## Reproduire

```bash
cd contributions/RO-25_pilote-ia
pip install numba                                    # 0.68.0
python3 defi_m14_prediction.py                       # prédictions (lit defi_m13_sorties.json)
python3 defi_m14_sejour.py --moteur A --points 257:1,257:2 --balayages 2e7 --rodage 1e6 --sortie defi_m14_sejour_A.json        # ≈ 1 h sur 2 cœurs
python3 defi_m14_sejour.py --moteur B --points 257:11,257:12 --balayages 2e7 --rodage 1e6 --sortie defi_m14_sejour_B_257.json   # ≈ 20 min
python3 defi_m14_sejour.py --moteur B --points 225:11,225:12 --balayages 1.3e7 --rodage 1e6 --sortie defi_m14_sejour_B_225.json # ≈ 13 min
python3 defi_m14_sejour.py --moteur B --points 193:11,193:12 --balayages 4e6 --rodage 5e5 --sortie defi_m14_sejour_B_193.json    # ≈ 3 min
python3 defi_m14_sejour.py --moteur B --points 289:11,289:12 --balayages 3e7 --rodage 1e6 --sortie defi_m14_sejour_B_289.json   # ≈ 33 min
python3 defi_m14_sejour.py --moteur A --points 289:1 --balayages 1.5e7 --rodage 1e6 --processus 1 --sortie defi_m14_sejour_A_289.json        # ≈ 50 min
python3 defi_m14_sejour.py --moteur B --points 257:21,257:22 --balayages 1.2e7 --rodage 3e6 --depart aleatoire --sortie defi_m14_sejour_B_257_aleatoire.json
python3 defi_m14_analyse.py                          # écrit defi_m14_analyse.json
```

Python 3.13, numpy 2.5.3, scipy 1.18.1, numba 0.68.0. Graines fixées ; un même script rejoué sur une autre machine peut différer au niveau du bruit statistique. Sorties écran : `defi_m14_*_sortie.txt`. Les fichiers `*.partiel_*.json` sont les derniers états intermédiaires des chaînes (témoins de progression).
