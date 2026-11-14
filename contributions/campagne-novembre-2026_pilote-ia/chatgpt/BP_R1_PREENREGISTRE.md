# THE BLOB PRINCIPLE — BP-R1 / GEL AVANT CALCUL
## Fermeture relationnelle nue, dimension et compatibilité avec un tissu de tétraèdres

Date de gel : 13 novembre 2026. Volet THÉORIQUE nouveau, indépendant de C-145/PR-3. PR-3 reste FIGÉ et NON EXÉCUTÉ. Le présent document précède l'exécution du script BP_R1_exhaustif.py.

### Question
Peut-on déduire la sélection du tétraèdre rempli, sa dimension physique 3 et une croissance tissulaire à partir de relations binaires locales, de leur fermeture et d'une exclusion de valence, sans postuler au départ une géométrie 3D ?

### Variables et définitions fixées
- G=(V,E) : graphe simple fini non orienté à sommets étiquetés, sans coordonnées, masses, forces, horloge physique ou énergie. Une « itération » est une profondeur d'actualisation combinatoire, PAS du temps physique.
- Règle A (fermeture nue simultanée) : à l'itération t, ajouter TOUTES les arêtes manquantes entre sommets qui partagent au moins un voisin dans G_t. Ne jamais supprimer une arête. Aucune priorité, aucune randomisation.
- Règle B (restriction structurelle, pas dynamique) : interdire les graphes dont le degré maximal dépasse b=3. Nous n'inventons pas un algorithme séquentiel de résolution de contacts en présence de conflits ; nous examinons la compatibilité des graphes finaux avec cette règle.
- Interprétation topologique : pour le même 1-squelette K4, comparer trois complexes : (X1) seules arêtes ; (X2) quatre faces triangulaires remplies mais pas de cellule 3D ; (X3) tétraèdre rempli (faces et 3-cellule). Les faces et les cellules sont des données supplémentaires, non contenues dans une arête.
- Tissu : deux tétraèdres abstraits [0,1,2,3] et [0,1,2,4] collés par la face commune [0,1,2], soit 5 sommets. Aucun angle ou volume euclidien n'est supposé pour ce comptage.

### Prédictions formelles antérieures à l'exécution
P1 [T] Règle A : G_t = G_0^(2^t), puissance par distance dans la composante d'origine. Toute composante connexe initiale de diamètre d devient clique au plus tard à t=ceil(log2 d); pas de limite spéciale à K4. Les composantes disjointes ne se relient jamais.
P2 [T] Trois complexes X1, X2, X3 ont exactement le même 1-squelette K4 mais des dimensions maximales respectives 1, 2 et 3 ; donc l'adjacence seule ne détermine pas un volume ni la dimension topologique du remplissage.
P3 [T] Dans un graphe connexe de n>4 avec degré maximal <=3, il ne peut exister de K4 en sous-graphe, puisqu'un sommet de K4 a déjà trois voisins internes et aucun des quatre ne peut avoir une arête externe. En particulier, un réseau connecté avec cap b=3 ne peut intégrer un tétraèdre K4.
P4 [T] Deux K4 collés par une face ont degrés (4,4,4,3,3), 9 arêtes, 7 faces triangulaires uniques, 2 cellules tétraédriques, caractéristique d'Euler V-E+F-T=1. Une restriction b=3 est incompatible avec ce tissu.
P5 [T] Une mise à jour déterministe équivariante par permutation préserve les automorphismes de l'état initial, donc ne peut choisir de manière unique un porteur privilégié dans un état initial exactement symétrique sans hypothèse supplémentaire ou hasard.

### Calculs et contrôles préenregistrés
- Énumérer tous les graphes SIMPLES ÉTIQUETÉS sur n=2,3,4,5,6 (respectivement 2^1, 2^3, 2^6, 2^10, 2^15). Les états ne sont PAS quotientés par isomorphisme. Isoler les graphes connexes.
- Pour chacun, itérer la règle A jusqu'au point fixe, consigner étapes requises, taille du clique final, première itération à laquelle K4 est présent, première apparition K5 (si n>=5). Vérifier formule P1 contre diamètre du graphe initial.
- Comparer EXACTEMENT deux implémentations indépendantes de la transition : A par intersections binaires de voisinages, B par recherche des chemins de longueur deux via listes de voisins. En cas de désaccord, FAIL du contrôle et résultat non classable.
- Vérifier pour n=2..6 les comptes de graphes connexes étiquetés standards (1,4,38,728,26704), en tant que témoins indépendants du résultat physique.
- Vérifier le nombre de graphes connexes satisfaisant max degré <=3 ET contenant K4 pour n=5 et 6 : prédit exactement zéro (contrôle P3).
- Vérifier le témoin négatif d'un graphe déconnecté (deux arêtes disjointes sur 4 sommets) qui ne devient pas K4 ; le témoin positif d'un chemin de 5 sommets (devient K5) ; K4 fixe ; graphe vide fixe.
- Le script doit publier ses comptages et les états détaillés, pas les résumer en « simulations physiques ». Toute comparaison sur graphes étiquetés n'est PAS une probabilité sur les univers possibles.

### Verdicts pré-déclarés
- PASS analytique si P1-P5 sont démontrés logiquement et vérifiés par les contrôles exacts.
- FAIL d'une sélection de la dimension 3 par les seuls postulats ci-dessus si les états peuvent produire K5 et/ou les trois remplissages X1/X2/X3 restent indiscernables par l'adjacence.
- OPEN : naissance de 3D, loi de liaison durable, masse, temps, transfert d'énergie, quantique, relativité, gravitation, correspondances observationnelles. Aucun passage TOE n'est revendiqué, TOE 0/7.

### Non-transfert et discipline
C-145 PR-3 n'est ni modifié ni exécuté ici. Aucun résultat combinatoire n'établit un processus physique réel. Les théorèmes sont des faits de théorie des graphes ou de topologie conditionnels aux définitions. Les contre-exemples interdisent ces mécanismes EXACTS comme explication suffisante, sans réfuter d'autres mécanismes Blob plus riches.
