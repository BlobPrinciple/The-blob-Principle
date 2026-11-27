# X-27 bis — Veille du 26 novembre 2026 (Riemann, Euler, Navier–Stokes) et contre-exemple de X-27 au noyau de Lean

TOE 0/7. Aucun verrou fermé.

Paroles de l'auteur. 26 novembre, 20 h 56 : « À toi de jouer tu vas vérifier les résultats annoncées de Riemann et autres pour voir ce qui peut aider ». 27 novembre, 7 h 08 : « Dépose et pousse à l’extrême ensuite toutes les recherches. »

## 275. Les limites d'abord

1. **Aucun des résultats annoncés ne ferme ni ne déplace un des sept verrous.** Ce sont des théorèmes de théorie des nombres et de mécanique des fluides. Ils ne disent rien de l'espace-temps, de la gravitation, du quantique, de la matière, du spectre, de la jauge, ni d'une prédiction.
2. **Je n'ai pas rejoué la preuve de Riemann.** Il faut 12 cœurs et 24 Go pour la version courte ; j'en ai 2 et 7. Mon contrôle propre est une lecture du dépôt et des énoncés. Pour le reste, je m'appuie sur les rejeux indépendants publiés.
3. **Personne n'a encore compris l'argument en entier**, d'après Quanta (24 novembre). Rien n'est relu par des pairs ni publié. Le tableau de bord indépendant affiche : « announced, machine-checked, not yet refereed ».
4. **Le pilote Lean ci-dessous certifie un énoncé que j'ai écrit moi-même.** Sa fidélité au carnet X-27 n'est pas contre-auditée. Un des vérificateurs (lean4lean) n'a pas pu lire mes fichiers. L'empreinte de l'archive de Lean n'a pas été comparée à une liste officielle.
5. **Le dictionnaire d'Eisenstein et la lecture des trois places sont des explorations hors protocole** : ni prédiction scellée, ni contre-audit.
6. **Versé le 27 novembre sur la branche de campagne, à la demande de l'auteur ; rien sur `main`.** Les essais du 26 novembre ont été faits avant ce versement et hors du protocole de scellement.

## 276. Ce qui a été annoncé

| Résultat | Qui, quand | Forme | État au 26 novembre |
|---|---|---|---|
| Hypothèse de Riemann, et la même pour toutes les fonctions L de Dirichlet | Levent Alpöge (Anthropic), avec Claude ; note de quatre pages le 20 novembre | Preuve en Lean seulement : 175 187 fichiers, 17,4 millions de lignes | Vérifiée par machine, par plusieurs équipes. Pas de preuve lisible. Non relue. |
| La même, réécrite | Luke Sernau et collègues d'Anthropic, avec Claude ; 25 novembre | 477 124 lignes (édition lisible), 112 827 lignes (édition compacte) | Dépôt communautaire avec contrôle automatique |
| Explosion en temps fini pour Euler 3D sans forçage | Alpöge, Buckmaster, Coiculescu, forte aide de l'IA | Preuve lisible et Lean | Le mieux digéré des trois (Tao, 20 novembre) |
| Explosion en temps fini pour Navier–Stokes 3D sans forçage | Alpöge et Buckmaster, forte aide de l'IA | Article et Lean | Stratégie claire, rédaction à refaire (Tao) |
| Navier–Stokes avec forçage | OpenAI, septembre | Preuve d'une centaine de pages, d'après ce qu'on a dit à Buckmaster | Non vue par lui ; dispute de priorité |
| Hypothèse de Riemann généralisée, sans IA | Alessandro Masullo, 940 pages, mises en ligne par Ravi Vakil | Manuscrit | Jugement réservé ; une preuve antérieure du même auteur n'avait pas tenu (Quanta) |
| Au moins 67,2 % des zéros de zêta sur la droite critique (41,6 % avant) | Claude, version de recherche ; 10 août | Article et Lean | Examiné à bref délai par Conrey et Goldston ; ce n'est pas une preuve de Riemann |

Portée de l'annonce de Riemann : les fonctions L de Dirichlet seulement, pas les fonctions de Dedekind ou automorphes en général. D'après Tao, la preuve semble mobiliser le programme de Langlands et la géométrie arithmétique ; son analyse est préliminaire. À ce qu'on en sait, elle ne passe pas par un opérateur physique : elle ne donne pas d'appui à une lecture « spectrale » de zêta.

## 277. Ce qui a été vérifié, et par qui

- **Andrew Sutherland (MIT)** : construction complète des 175 187 modules ; seuls axiomes : `propext`, `Classical.choice`, `Quot.sound` ; rejeu par `leanchecker` ; acceptation par les noyaux indépendants nanoda, con-leche, con-ron, lean4lean ; le « Comparator » confirme que les cinq énoncés sont ceux du défi écrit dans Mathlib ; reconstruction en bac à sable identique à l'octet près.
- **Autres rejeux** : Simon DeDeo, et d'autres recensés par le tableau de bord de Bartosz Naskręcki (quatre rapports indépendants concordants).
- **21 novembre** : un collectif de spécialistes de la formalisation se dit pleinement confiant dans la correction (Quanta).
- **Ce que cela prouve** : que les cinq énoncés formels découlent des trois axiomes usuels, selon ces noyaux et avec les définitions de Mathlib. `RiemannHypothesis` est la définition de Mathlib, pas une définition maison.
- **Ce qui manque** : une preuve lisible et la relecture. Maksym Radziwiłł juge la note de quatre pages incompréhensible par endroits. Un projet Polymath (Sahay, Sawin, Silberman) est ouvert depuis le 24 novembre pour en tirer une preuve humaine.

## 278. Mon contrôle propre

Dépôt `lsernau/grh-lean`, commit 72fead1, cloné et lu sans rien exécuter.

- Les cinq théorèmes sont dans `Main.lean`, avec les types annoncés.
- Dans les deux éditions : aucun `sorry`, aucune déclaration `axiom`, aucun `native_decide`, `unsafe`, `opaque`, `implemented_by`, `extern`, aucune macro ni commande exécutée à la compilation, aucune option qui saute le noyau.
- Compte des lignes : 477 151 et 112 854, soit les chiffres annoncés à 27 lignes près (deux petits fichiers annexes).

Ce contrôle ne remplace pas un rejeu.

## 279. Ce qui peut aider le Blob

### 279.1 La méthode de certification — essayée ici

La chaîne qui a servi pour Riemann (énoncé séparé de la preuve, liste des axiomes, noyaux indépendants) s'applique telle quelle aux énoncés [T] du laboratoire. Je l'ai fait pour le contre-exemple de X-27.

**Résultat : K20 est fausse, contrôlé par le noyau de Lean. [CERT pour l'énoncé formel]**

- `Enonce.lean` (128 lignes, écrit à la main, Lean seul sans Mathlib) : le produit, le germe, les retournements, l'empilement, la place admissible, le tissu, les 17 naissances, la place (18, 18, 16, −6, −3)/7.
- `Preuve.lean` (347 lignes, écrit par `genere.py`) : les témoins seulement. Parent et trois voisins de chaque naissance, mot de retournements de chaque constituant.
- Le théorème : (1) les 17 naissances forment un tissu ; (2) ce sont toutes des naissances dans la cellule ; (3) les 22 constituants sont dans l'empilement ; (4) la place est admissible ; (5) elle n'est pas dans l'empilement.

| Contrôle | Résultat |
|---|---|
| Lean 4.35.0 | accepte ; axiomes : `propext`, `Classical.choice`, `Quot.sound` |
| `leanchecker`, `leanchecker-paranoid`, `leanchecker --fresh` | acceptent |
| nanoda 0.4.19 (noyau en Rust), tout autre axiome interdit | 2 177 déclarations, aucune erreur |
| con-ron, con-leche | 1 924 déclarations acceptées chacun |
| lean4lean | n'a pas tourné (« incompatible header ») |
| Quatre versions faussées (place, naissance, témoin, place prise dans l'empilement) | refusées toutes les quatre |

Le tout se rejoue en une commande (`controle.sh`), en une minute et demie sur deux cœurs ; le second passage redonne la même sortie.

Empreintes SHA-256 : `Enonce.lean` 2a4a84c4f94f9b540baf94fb8676deb77a2012b6310134efe108d6633319cbf2 ; `genere.py` 5bca8203e7791299cf7cf9b9b234cd470119d0d4cf6e16b7a688b539e068db3e ; `Preuve.lean` aa239497e26e28311dbdf08fd375c768720783850e33005d5227a8d8a2189685.

Lean 4.35.0 vient de la page officielle des versions (GitHub, `leanprover/lean4`) ; SHA-256 de l'archive : 7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d.

Trois réserves sur l'énoncé. Les naissances y sont des vecteurs entiers (c'est le cas des 17). L'indépendance y est écrite sur les entiers, ce qui revient au même pour des vecteurs entiers. L'empilement y est défini comme l'orbite du germe sous les cinq retournements : il est entier par construction.

Un fait vu en passant, par la version faussée n° 3 : la place (2, 2, 2, −1, 0), que le tissu laisse vide, touche les quatre mêmes constituants que la place hors de l'empilement. Ce sont les deux boules qui ont ces quatre contacts : l'une est dans l'empilement, l'autre non.

### 279.2 Le gabarit d'Euler et de Navier–Stokes

La preuve de Navier–Stokes suit un schéma en trois temps : une solution approchée trouvée par le calcul, une théorie de perturbation rigoureuse qui en tire une solution exacte, une preuve formelle. C'est le chemin pour changer un fait « mesuré » en théorème. Dans la lecture de contact, l'arithmétique est déjà exacte : le passage se fait directement par témoins, comme en 5.1. Le gabarit servira là où le laboratoire n'a que des nombres approchés (limite continue).

### 279.3 Un pont arithmétique — piste, pas résultat

**Dictionnaire mesuré. [M, exploration]** Au rang 3, les voisins d'un constituant de l'empilement sont les sphères de Ford des entiers d'Eisenstein. Le constituant devient un plan ; chaque voisin y pose un point de contact α/β, fraction réduite d'entiers d'Eisenstein, et sa courbure vaut la norme de β. Épreuve exacte : sur les 48 381 vecteurs entiers ronds liés au premier constituant du germe (somme des coordonnées ≤ 301, courbure jusqu'à 225), 29 563 sont dans l'empilement et ce sont exactement les 29 563 sphères de Ford. Aucun désaccord. La construction est connue (Northshield, 2015) ; rien à revendiquer.

**Ce que dit la littérature.** Au rang 2, les voisins sont les cercles de Ford, donc les fractions de Farey, et l'hypothèse de Riemann équivaut à leur répartition la plus régulière possible (Franel et Landau, 1924 ; Zagier, 1981, pour les horocycles). Au rang 3, Romero et Verjovsky (2017) étudient les horosphères fermées de l'orbifold de Bianchi des entiers d'Eisenstein et notent, d'après Zagier et Sarnak, que la meilleure vitesse de répartition équivaut à l'hypothèse de Riemann pour la fonction zêta de ce corps. C'est une remarque dans leur article, pas un théorème qu'ils démontrent.

**Ce que l'annonce couvre.** Cette fonction zêta est le produit de zêta de Riemann et de la fonction L du caractère modulo 3. Les deux sont dans le théorème annoncé.

**Ce que cela donnerait.** Si la preuve tient et si la remarque est exacte : vus d'un constituant de l'empilement complet, ses voisins couvrent sa surface avec la meilleure régularité possible, à toute échelle. Cet énoncé ne porte ni sur un tissu en cours de croissance, ni sur l'empilement entier. Aucune preuve du laboratoire ne s'en sert. À garder pour le dossier de la limite continue (verrou V1).

### 279.4 Les trois places hors de l'empilement, relues — exploration

Algèbre exacte : si x = v/d est une boule ronde liée à un constituant c, alors q = v + (d − 1)·c est un vecteur entier rond, lié à c au même point, et x le contient.

**Constat. [M, 9 cas]** Pour les trois places hors de l'empilement connues (dénominateurs 3, 7 et 91), ce q est chaque fois un constituant de l'empilement, de courbure 3, 7 et 97 vu du premier constituant du germe. Pour les deux premières, c'est vrai depuis chacun de leurs quatre contacts. Dit autrement : chaque place hors de l'empilement connue est un vrai constituant, qui n'est pas né, gonflé autour de son point de contact. Sur 48 381 vecteurs entiers ronds liés au germe, 61 % seulement sont dans l'empilement : le constat n'est pas automatique. Neuf cas ne font pas une loi.

### 279.5 Calibrage

Annoncé ne veut pas dire relu. La preuve de Riemann est contrôlée par machine et incomprise ; les explosions de fluides attendent leur rédaction ; une dispute de priorité oppose déjà deux laboratoires. La barre de ce qui compte comme établi vient de monter : un énoncé formel public, des noyaux indépendants, un tableau de bord. Le laboratoire peut s'y mesurer dès maintenant pour ses énoncés mathématiques.

## 280. Ce qui ne peut pas aider

- Chercher un lien entre la droite critique et le Blob serait de la numérologie. Je n'en propose aucun.
- L'explosion des équations de fluides montre qu'une description continue peut casser en temps fini. C'est au mieux un appui d'idée pour un substrat discret, pas un argument.

## 281. Prochaine étape proposée

**X-28, avec deux outils nouveaux.** Démontrer, ou faire tomber, que la règle à la lettre garde le tissu dans l'empilement à tout palier, en prenant les coordonnées d'Eisenstein pour repère et Lean pour juge. Le constat 279.4 donne un premier énoncé à éprouver : toute place admissible hors de l'empilement contient un constituant de l'empilement qui n'est pas né.

## 282. Fichiers

`calculs/lean_x27/` : `Enonce.lean`, `Preuve.lean`, `genere.py`, `controle.sh`, `controle.out`. `calculs/x27bis_ford_eisenstein.py` et sa sortie ; `calculs/x27bis_gonflee.py` et sa sortie.

## Sources

- Tableau de bord indépendant : https://github.com/nasqret/riemann-rev
- Vérification de Sutherland : https://math.mit.edu/~drew/grh/
- Preuve condensée : https://github.com/lsernau/grh-lean
- Dépôt communautaire : https://github.com/leanprover-community/riemann-hypothesis
- Note d'origine (citée par le tableau de bord, non lue par moi) : https://alpo.ge/remark.pdf
- Quanta, dépêche du 24 novembre : https://www.quantamagazine.org/update/168664/
- Tao, 20 novembre : https://terrytao.wordpress.com/2026/11/20/unforced-euler-singularity-unforced-navier-stokes-singularity-and-the-generalized-riemann-hypothesis/
- Tao, 23 novembre (Euler) : https://terrytao.wordpress.com/2026/11/23/finite-time-singularity-formation-for-the-three-dimensional-euler-equations/
- G.R.H. Polymath, 24 novembre : https://terrytao.wordpress.com/2026/11/24/g-r-h-polymath/
- Déclaration de Buckmaster sur la priorité : https://cims.nyu.edu/~tristanb/statement.pdf
- Anthropic, 10 août (67,2 % des zéros) : https://www.anthropic.com/research/riemann-zeta
- Northshield, « Ford Circles and Spheres » : https://arxiv.org/abs/1503.00813
- Romero et Verjovsky, horosphères des orbifolds de Bianchi : https://arxiv.org/abs/1710.07890

TOE 0/7. Aucun verrou fermé.
