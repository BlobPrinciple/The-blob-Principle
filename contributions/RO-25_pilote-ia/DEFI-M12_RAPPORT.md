🇫🇷 Français · 🇬🇧 [English version](DEFI-M12_REPORT_EN.md)

# DEFI-M12 — La lenteur aristocratique : ni loi de puissance ni exponentielle en n ; à degré moyen 4, t½ ≈ exp(0,96·√n) de n = 17 à 193

*Contribution du pilote IA du laboratoire (Claude, Anthropic), 27 octobre 2026. Déposée comme toute contribution, en issue `ia-assistee`. Vérifiée par le pilote (deux méthodes de mesure, seconde implémentation indépendante par le code) et relue par un second agent IA en relecteur hostile, avec son propre moteur (voir § 6) ; **aucune relecture humaine à ce stade**.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Ce rapport ne change aucun statut épistémique. Il répond partiellement à DEFI-M12 (RO-25, RO-20), sur graphes abstraits seulement ; le moteur canonique n'est pas traité.

## 1. La question

DEFI-M12 (#38), ouvert par [DEFI-M11_RAPPORT.md](DEFI-M11_RAPPORT.md), § 3 B2 : sur graphes abstraits à degré moyen 4, le demi-temps t½ que met un nouveau-né à acquérir sa masse triangulaire d'équilibre passe de 0,5 balayage (N = 8) à 442 (N = 64), « au moins de l'ordre de N³, peut-être exponentiel ». **Puissance de N ou exponentielle ?** Livrable ([DEFIS.md](../../DEFIS.md), ligne DEFI-M12) : une borne démontrée, ou une mesure jusqu'à N ≥ 128 à au moins deux densités, avec barres d'erreur, et sur le moteur canonique à N ≥ 250.

Sources qui font foi : armature V347.1, § II.0 (strates A_gen et A_Gibbs, p. 10 ; les deux ponts absents, RO-25 et RO-08) ; encadré RO-25 (p. 11 : une dynamique jointe à N variable, qui combine mitose/fermeture et relaxation, et dont la loi conditionnelle à N fixé reproduise ou dérive π_N) ; axiomes A3–A4, étiquetés [A][ARCH] (p. 18) : S_sim(C) = log(1 + n_tri(C)) − β·D(C), β = 0,30 ; π_N ∝ exp(N·S_sim/τ), τ = 0,50 ; A0′ (p. 18 : « persister » n'est pas défini par π_N > 0, RO-20). Cadre de calcul : hypothèse H-abs de [DEFI-M8_RAPPORT.md](DEFI-M8_RAPPORT.md), § 2 (graphes simples étiquetés abstraits, sans contrainte Rips ; D = écart-type de population des degrés / degré moyen ; échanges de Metropolis à nombre d'arêtes fixé). n désigne le nombre de sommets (n = N + 1 après une naissance), M le nombre d'arêtes, λ le facteur de la mesure π ∝ exp(λ·S_sim) (λ = n/τ = 2n pour l'axiome A4) ; un **balayage** vaut M échanges. La naissance étudiée (attachement à k = 4 sommets) n'est pas le générateur μ de A_gen (p. 10 : une feuille, une seule arête, aucune fermeture) : c'est le cadre de DEFI-M11.

## 2. Méthode

**Méthode stationnaire (nouvelle, `defi_m12_lenteur.py`).** Dans une chaîne à l'équilibre, on enregistre T_v (triangles contenant v) pour tous les sommets tous les Δ balayages, et l'on calcule l'autocorrélation poolée C(t), avec une moyenne commune à tous les sommets (égale à 3T/n). t½ est le premier temps où C(t) = 1/2 (interpolation linéaire). C(t) suit essentiellement la persistance de l'appartenance à l'aristocratie : à n = 65, le relecteur obtient t½ = 412 pour T_v, 389 pour l'indicatrice T_v > 6 et 289 pour l'appartenance aux neuf sommets les plus triangulés. t½ est un demi-temps d'autocorrélation d'une observable, pas un temps de mélange. Trois réglages :

- **c2** : M = 2n (degré moyen 4, la densité de DEFI-M11), λ = n/τ (axiome A4) ;
- **c3** : M = 3n (degré moyen 6), λ = n/τ ;
- **c2T** : M = 2n, λ = 33/τ = 66 fixe (température effective tenue constante).

n = 17, 25, 33, 49, 65, 97, 129, 193 ; L = 3 000 enregistrements par chaîne (6 000 en c2T) ; quatre chaînes par point, deux de départ aléatoire et deux de départ « noyau planté » (clique de taille maximale compatible avec M) ; barre : écart-type entre chaînes / 2 (erreur-type sur quatre chaînes, probablement optimiste : voir § 5). Δ vise t½/Δ ≥ 5, sauf c3 à n ≤ 25 (Δ = 1 balayage, t½/Δ = 2,2 et 4,6) et c2T à n = 129 et 193 (Δ = 1, t½/Δ = 6,5 et 2,7) ; le relecteur estime le biais d'interpolation inférieur à 1 % même à t½/Δ = 2,2.

**Passes écartées.** Deux passes avaient un Δ trop grand : la première pour c3 et c2T (Δ de c2), la seconde pour c2T (Δ = 5). Elles sont conservées (`defi_m12_lenteur_premiere_passe_sortie.txt`, `defi_m12_lenteur_c3_c2T_sortie.txt`) et exclues de l'analyse, qui ne retient que les chaînes au Δ du code final (`defi_m12_analyse.py`). Ce n'est pas un tri sur les résultats : c3 écarté et c3 retenu diffèrent de 1 à 4 % ; c2T écarté est biaisé vers le haut parce que t½ y est de l'ordre de Δ ou moins (par exemple 157 au lieu de 6,5 à n = 129 avec Δ = 314).

**Méthode naissance (celle de DEFI-M11, `defi_m12_naissance.py`).** Le moteur `defi_m11_monte_carlo.experience` est réutilisé sans modification (attachement uniforme, k = 4, M = 2N − 2) à N = 96 (400 naissances) et N = 128 (200 naissances), avec un rodage des parents de 12 000 et 40 000 balayages et un espacement de 1 000 et 3 000 balayages (0,3 t½ à N = 128 : les naissances ne sont pas indépendantes, et l'intervalle à 90 % par bootstrap est donc optimiste) ; t½ par la fonction de [defi_m11_demi_temps.py](defi_m11_demi_temps.py).

**Test direct du refroidissement (`defi_m12_arrhenius.py`, suggéré par le relecteur).** À n = 65 fixé, λ = 98, 162, 194 (s'ajoutent λ = 66 de c2T et λ = 130 de c2) ; à λ fixé, n = 49 contre 65 (λ = 98) et n = 65 contre 97 (λ = 194). Quatre chaînes par point, t½/Δ entre 13 et 17.

## 3. Résultats

### 3.1 Degré moyen 4, mesure de l'armature (c2) : t½ ≈ exp(0,96·√n) de n = 17 à 193 [M]

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|---|
| t½ stationnaire (balayages) | 9,2 ± 0,1 | 21,5 ± 0,4 | 43,3 ± 0,7 | 146 ± 2 | 389 ± 4 | 2 297 ± 64 | 9 760 ± 173 | 111 873 ± 1 230 |
| t½ naissance (DEFI-M11 jusqu'à 65 ; ici à 97 et 129, IC 90 %) | 7,5 | 22,9 | 46,8 | 139 ; 147 | 442 | 2 383 (1 860–3 141) | 11 317 (7 719–26 437) | — |
| Δ log t½ / Δ log n | — | 2,19 | 2,53 | 3,08 | 3,46 | 4,43 | 5,07 | 6,05 |
| Δ log t½ / Δ √n | — | 0,97 | 0,94 | 0,97 | 0,92 | 0,99 | 0,96 | 0,96 |

- La pente log-log croît sans cesse (2,2 → 6,1) : **pas de loi de puissance** sur cette plage. La pente par unité de n décroît (0,106 → 0,038) : **pas d'exponentielle en n** non plus. La pente par unité de √n est constante à ± 4 %.
- Ajustements sur n ≥ 25 (somme des carrés des résidus de log t½) : puissance (exposant 4,13) 1,26 ; exponentielle en n 1,06 ; exponentielle de √n 0,0020 (log t½ = 0,964·√n − 1,77 ; plus grand résidu 4 %). À exposant libre, log t½ = a·n^γ + b donne **γ = 0,507 ± 0,010** (n ≥ 25) et 0,497 ± 0,027 (n ≥ 49).
- **Prédiction hors échantillon** (ajustement sur n ≤ 97, prédiction à n = 129 et 193) : exponentielle de √n, 9 611 et 110 086 balayages, rapports mesure/prédiction **1,02 et 1,02** ; loi de puissance, rapports 2,0 et 5,8 ; exponentielle en n, 0,47 et 0,09.
- Les deux méthodes concordent : à n = 97 et 129, les intervalles à 90 % des t½ de naissance (1 860–3 141 ; 7 719–26 437) contiennent les t½ stationnaires (2 297 ; 9 760) ; de n = 17 à 65, les écarts vont de −19 % à +14 %.
- En échanges de Metropolis (2n·t½), le demi-temps passe de 3·10² échanges à n = 17 à 4,3·10⁷ à n = 193.

### 3.2 Degré moyen 6 (c3) : sur-polynomial aussi, mais pas en exp(a√n) [M]

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|---|
| t½ (balayages) | 2,20 ± 0,02 | 4,57 ± 0,03 | 8,25 ± 0,14 | 21,4 ± 0,2 | 52,7 ± 0,4 | 247 ± 2 | 974 ± 14 | 10 447 ± 214 |
| Δ log t½ / Δ √n | — | 0,83 | 0,79 | 0,76 | 0,85 | 0,86 | 0,91 | 0,94 |

À n égal, la relaxation est plus rapide qu'à degré moyen 4, mais elle aussi sur-polynomiale (pentes log-log 1,9 → 5,9). Des trois formes à deux paramètres, l'exponentielle de √n est la moins mauvaise (somme des carrés 0,062 contre 0,49 et 1,53), mais sa pente dérive (0,76 → 0,94) et la prédiction hors échantillon sous-estime n = 193 d'un facteur 1,6. À exposant libre : **γ = 0,63 ± 0,01** (n ≥ 25), 0,61 ± 0,01 (n ≥ 49). La forme exp(a√n) n'est donc pas universelle : à cette densité, la croissance est plus rapide, sans être exponentielle en n sur la plage mesurée.

### 3.3 La lenteur suit λ, pas la taille [M]

**À λ fixé (c2T, λ = 66), quand n croît :**

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|---|
| t½ (balayages) | 117 ± 4 | 56,3 ± 0,9 | 43,8 ± 1,2 | 37,1 ± 0,9 | 34,0 ± 1,0 | 17,7 ± 0,8 | 6,5 ± 0,3 | 2,7 ± 0,1 |
| part de la moyenne de T_v portée par les sommets à T_v > 6 | 0,98 | 0,96 | 0,94 | 0,87 | 0,79 | 0,54 | 0,27 | 0,07 |

t½ décroît avec n et l'aristocratie se dissout. Ce test, à lui seul, ne sépare pas deux choses : à λ fixé, augmenter n change l'état d'équilibre lui-même (l'aristocratie disparaît). Il montre que la croissance de λ avec n est nécessaire à la lenteur. (Contrôle de reproductibilité : à n = 33, c2T et c2 ont le même λ et des t½ voisins, 43,8 et 43,3.)

**À n fixé (n = 65), quand λ croît :**

| λ | 66 | 98 | 130 | 162 | 194 |
|---|---|---|---|---|---|
| t½ (balayages) | 34,0 ± 1,0 | 141 ± 2 | 389 ± 4 | 1 032 ± 17 | 2 873 ± 58 |

log t½ est affine en λ pour λ ≥ 98 (pente 0,031) : signature d'une barrière activée, de type Arrhenius, à n fixé. **À λ égal et n différent** : t½(n = 49, λ = 98) = 141 contre t½(n = 65, λ = 98) = 141 ; t½(n = 97, λ = 194) = 2 276 contre t½(n = 65, λ = 194) = 2 873. Sur ces points, t½ dépend surtout de λ, et seulement faiblement de n à λ fixé (il décroît avec n).

**Lecture.** La lenteur de 3.1 est portée par l'échelle λ = n/τ de l'axiome A4, qui refroidit la mesure quand n grandit, et non par la taille du noyau d'échange. Le mécanisme [H] de DEFI-M11 (§ 4, « refroidissement ») est **compatible** avec ces mesures (condition nécessaire vérifiée, croissance activée en λ à n fixé) ; la forme exp(a·n) qu'il suggérait n'est pas observée le long de λ = 2n.

### 3.4 Anatomie de l'aristocratie à degré moyen 4 : une clique dominante de taille de l'ordre de √n [M], et une lecture [H]

Quarante instantanés d'équilibre par taille, une chaîne par taille, réglage c2 (`defi_m12_structure.py` ; instantanés corrélés, espacés de 0,19 t½ à n = 193 ; pas de barres d'erreur) :

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|---|
| plus grande clique (moyenne) | 5,5 | 5,8 | 6,5 | 7,7 | 8,8 | 10,8 | 12,1 | 14,8 |
| part de Σ T_v portée par ses sommets | 0,74 | 0,69 | 0,72 | 0,75 | 0,78 | 0,83 | 0,85 | 0,90 |
| T_v maximal | 17,5 | 23,0 | 28,7 | 40,4 | 50,3 | 67,9 | 82,1 | 112,4 |

La plus grande clique (exacte) croît comme n^0,47 (n ≥ 33) et ses sommets portent de 69 à 90 % des triangles : à cette densité, l'« aristocratie » de DEFI-M11 est pour l'essentiel **une clique dominante de taille de l'ordre de √n**. log t½ est affine en la taille q de cette clique sur n ≥ 33 (pente 0,94, plus grand résidu 0,13), moins bien qu'en √n (résidu 0,04) ; q variant comme n^0,47, ce n'est pas une confirmation indépendante.

**Lecture [H], non démontrée.** Pour qu'un sommet extérieur entre dans la clique dominante, ou qu'un membre en sorte, il faut défaire puis refaire de l'ordre de q arêtes portant chacune de l'ordre de q triangles. Si chaque étape coûte un facteur de Boltzmann d'au plus e^(−c), avec c > 0 indépendant de n, le temps d'échange de membres est au moins de l'ordre de exp(c·q) = exp(c′·√n). Variante plus précise (du relecteur) : retirer une arête de la clique coûte environ λ·q/T avec T ≈ q³/6, soit 6λ/q² ; ce coût est constant le long de λ = 2n (car q² ∝ n), d'où une barrière d'environ 6λ/q ∝ √n ; à n fixé, il est proportionnel à λ (cohérent avec 3.3) ; à λ fixé, il décroît quand q grandit (cohérent avec c2T). **Tension non résolue** : ce schéma prédit aussi exp(a√n) à degré moyen 6, où l'on mesure γ ≈ 0,6 (3.2) ; la structure n'y a pas été mesurée.

### 3.5 Recoupements

- **Seconde implémentation, indépendante par le code** (`defi_m12_second_moteur.py` : voisinages en mots de 64 bits et popcount, générateur PCG64 de numpy, T_v par diag(A³), autocorrélation par somme directe ; aucun code commun ; mêmes Δ, même rodage de 200 Δ, même estimateur, deux chaînes par point, départs aléatoires seulement). c2, n = 17, 33, 65, 129 : t½ = 8,9, 44,0, 387, 10 074 contre 9,2, 43,3, 389, 9 760 (−3 % à +3 %). c3 (Δ de la première passe, t½/Δ ≈ 1,7 à 3 pour n = 33 à 129) : 2,16, 8,44, 54,7, 978 contre 2,20, 8,25, 52,7, 974 (−2 % à +4 %). Elle a d'abord révélé une erreur de *son propre* code (somme des carrés des degrés fausse quand un sommet de l'arête ajoutée coïncide avec un sommet de l'arête retirée), corrigée avant toute comparaison ; elle contrôle désormais à chaque enregistrement les triangles, les degrés et Σ d².
- **Moteur du relecteur** (son propre code Metropolis, c2) : t½ = 44,4, 144, 2 194, 9 467 à n = 33, 49, 97, 129, contre 43,3, 146, 2 297, 9 760 ; même nombre moyen de triangles.
- **Moteur de référence** : le noyau paramétré de `defi_m12_lenteur.py` reproduit bit à bit `defi_m11_monte_carlo.balayer` pour λ = n/τ (même graine, 20 000 échanges ; vérifié aussi par le relecteur à n = 49).
- **Équilibre** : départs aléatoires et « noyau planté » donnent le même nombre moyen de triangles (écart ≤ 1,3, pour un écart-type de T de 5 à 45) et des t½ compatibles (écart-type relatif entre les quatre chaînes ≤ 6 % en c2 et c3, ≤ 9 % en c2T).

## 4. Lecture pour le pont RO-25

- **[M]** Sur graphes abstraits, à degré moyen 4 et sous la mesure de l'armature, le demi-temps d'autocorrélation poolée de T_v, qui suit pour l'essentiel la persistance de l'appartenance à l'aristocratie, croît comme exp(0,96·√n) de n = 17 à 193, prédiction hors échantillon comprise ; à degré moyen 6, plus vite (exp(a·n^0,6) environ) sur la plage mesurée. Cette croissance est portée par λ = n/τ (3.3).
- **Conséquence [H], extrapolation au-delà de n = 193.** Un pont croissance → Gibbs qui laisserait chaque nouveau-né rejoindre sa masse triangulaire d'équilibre avant la naissance suivante, avec ce noyau d'échange, demanderait un intervalle entre naissances de l'ordre de t½(n) ≈ 0,17·exp(0,96·√n) balayages : 1,4·10⁵ à n = 200, et de l'ordre de 10⁴¹ à n = 10⁴ si la loi se prolongeait. **Ce pont-là ne serait pas praticable à grand n pour les sommets massifs, si la loi se prolongeait et si l'on exige la loi conditionnelle des graphes étiquetés.**
- **Ce que cela ne réfute pas.** RO-25 n'est pas réfuté : le falsificateur de l'armature (p. 11) porte sur l'*existence* d'une extension markovienne locale, pas sur sa lenteur. La lenteur mesurée est celle de l'échange d'arêtes à nombre fixé ; un autre noyau de relaxation (mouvements de sommets, échanges d'étiquettes) peut mélanger plus vite. Mais un échange d'étiquettes rend l'identité du nouveau-né, donc la généalogie, indifférente : la lenteur porte précisément sur la mémoire de qui est né quand. Enfin, la naissance étudiée n'est pas le μ de A_gen (§ 1).
- **Lien avec RO-20 [H].** La clique dominante persiste d'autant plus longtemps que n grandit : sa persistance est un candidat de critère « persister » distinct de π > 0 (A0′, p. 18), à examiner.
- **Moteur canonique [OPEN].** Rien de ceci n'est mesuré sur le moteur canonique (Rips), où DEFI-M9 ne voit pas, à ce jour, de croissance en N du corps de la loi des masses ; DEFI-M10 reste le défi qui doit trancher.

## 5. Ce qui est établi, ce qui reste à vérifier, le point le plus fragile

- **Établi** : les séries c2, c3 et c2T et le test à n fixé (quatre chaînes par point), recoupés par une seconde implémentation (huit points), par le moteur du relecteur (quatre points) et, pour c2, par la méthode naissance (sept tailles).
- **À vérifier** : tout, par une personne ; la forme au-delà de n = 193 ; la forme à degré moyen 6 et à d'autres densités ; la lecture « barrière ∝ taille de la clique » ; le moteur canonique.
- **Barres d'erreur** : ce sont des erreurs-types sur quatre chaînes, probablement optimistes. Le relecteur, reproduisant à n = 65 le protocole de n = 193 (huit chaînes de 28 t½, rodage 1,9 t½), trouve un écart-type par chaîne de 5,7 %, contre 2,2 % entre les quatre chaînes de n = 193 ; pondéré par les barres du rapport, l'ajustement en √n donne χ² = 12,8 pour 5 degrés de liberté. La conclusion repose sur la forme (pentes, exposant libre, prédiction), pas sur ces barres.
- **Règles de lisibilité de l'armature** (p. 18, règle 10.4, stabilité à l'allongement) : non appliquées à n = 193 (pas de chaîne plus longue) ; le relecteur ne trouve pas de biais d'allongement à n = 65 (389,4 contre 389,2).
- **Point le plus fragile** : à n = 193 (c2), le rodage ne vaut que 1,9 t½ et la chaîne 28 t½ ; l'accord des départs aléatoires et plantés, et la prédiction faite sur n ≤ 97, rassurent sans démontrer. L'exponentielle de √n est un ajustement sur huit tailles, pas une loi démontrée, et elle ne vaut pas à degré moyen 6.

## 6. Relecture hostile

Un second agent IA, qui n'a pas produit ce travail, a rejoué l'analyse (sorties identiques octet pour octet), contrôlé chaque nombre contre les JSON et les références à l'armature (p. 10, 11, 18 : conformes), et refait la courbe c2 avec son propre moteur (§ 3.5). Bloquants retenus et corrigés : « confirmée » remplacé par « compatible » au § 3.3, avec ajout du test direct à n fixé qu'il a proposé, puis rejoué par le pilote (`defi_m12_arrhenius.py`) ; conséquence pour RO-25 étiquetée [H], préfacteur 0,17 rétabli, conclusion rendue conditionnelle ; titre et § 3.1 restreints au degré moyen 4, exposant libre de c3 (≈ 0,6) ajouté ; lecture [H] corrigée (sens de l'inégalité, notation, tension avec c3) ; phrase fausse « encadrent » corrigée ; chiffres corrigés (pente 0,106 → 0,038 ; 974 ; exceptions à t½/Δ ≥ 5). Mineurs retenus : barres optimistes (§ 5), interprétation de C(t) (§ 2), structure sans barres (§ 3.4), bootstrap de naissance optimiste, μ de A_gen, règle 10.4, passes écartées détaillées, portée de la seconde implémentation, références précisées. Non appliqué : espaces insécables (convention typographique actuelle du dépôt).

## 7. Prochain pas sur le chemin de preuve (P1)

**DEFI-M13 — La barrière de la clique dominante.** À degré moyen 4 sous π ∝ exp(n·S_sim/τ) : démontrer, ou réfuter, que la plus grande clique a une taille de l'ordre de √n et que le temps d'échange de ses membres par échanges d'arêtes croît comme exp(Θ(√n)) (goulot d'étranglement, borne de conductance) ; expliquer pourquoi la croissance est plus rapide à degré moyen 6 (γ ≈ 0,6) ; chercher la même signature sur le moteur canonique à N ≥ 250 (DEFI-M10).

## Reproduire

```bash
cd contributions/RO-25_pilote-ia
pip install numba                                    # 0.68.0
python3 defi_m12_lenteur.py --tailles 17,25,33,49,65,97,129,193 --reglages c2 --L 3000 --sortie defi_m12_lenteur.json   # ≈ 20 min sur 2 cœurs
python3 defi_m12_lenteur.py --tailles 17,25,33,49,65,97,129,193 --reglages c3 --L 3000 --sortie defi_m12_lenteur_c3_c2T.json  # ≈ 15 min
python3 defi_m12_lenteur.py --tailles 17,25,33,49,65,97,129,193 --reglages c2T --L 6000 --sortie defi_m12_lenteur_c2T.json    # ≈ 1 min
python3 defi_m12_second_moteur.py --tailles 17,33,65,129 --reglage c2 --L 3000
python3 defi_m12_second_moteur.py --tailles 17,33,65,129 --reglage c3 --L 3000 --sortie defi_m12_second_moteur_c3.json
python3 defi_m12_naissance.py --tailles 96 --R 400 --sortie defi_m12_naissance_96.json     # ≈ 10 min
python3 defi_m12_naissance.py --tailles 128 --R 200 --sortie defi_m12_naissance_128.json   # ≈ 20 min
python3 defi_m12_structure.py                        # ≈ 5 min
python3 defi_m12_analyse.py                          # écrit defi_m12_analyse.json
python3 defi_m12_arrhenius.py                        # ≈ 3 min, lit defi_m12_analyse.json
```

Python 3.13, numpy 2.5.3, scipy 1.18.1, networkx 3.7, numba 0.68.0. Graines fixées ; un même script rejoué sur une autre machine peut différer au niveau du bruit statistique. Le fichier déposé `defi_m12_lenteur_c3_c2T.json` contient aussi les chaînes c2T de la deuxième passe écartée (Δ = 5, ancienne version de `delta_pour`), que l'analyse ignore ; la deuxième commande ci-dessus ne les régénère pas. Sorties écran : `defi_m12_*_sortie.txt`.
