# THE BLOB PRINCIPLE — C-146 / CAS-1
## Préenregistrement — bain fluctuant et orientation des rencontres entre tétraèdres
Date de gel : 2026-11-13. Statut à la rédaction : FIGÉ, NON CALCULÉ.

**Question**. Dans un modèle *postérieur* à la naissance des premières structures et à l'apparition postulée d'un bain, des fluctuations communes peuvent-elles créer une préférence d'interaction selon l'orientation de deux tétraèdres non interpénétrants, sans attraction gravitationnelle primitive ? L'interaction de Casimir réelle n'est pas assimilée d'office à ce modèle jouet gaussien classique.

**Modèle posé, non dérivé**. Champ scalaire gaussien, centré, en espace euclidien R^3 déjà donné, équilibre thermique à T>0, corrélation C(x,y)=exp(-|x-y|/ell), variance unitaire et longueur ell>0. Chaque tétraèdre est représenté par des points où la valeur du champ est contrainte à zéro (Dirichlet ponctuel idéal), sans épaisseur des parois et sans propriétés physiques des liants. Deux niveaux de discrétisation : (i) les 4 sommets ; (ii) les 4 sommets, 6 milieux d'arêtes et 4 barycentres de faces, soit 14 points. Une condition sur 4 ou 14 points n'est pas une condition aux limites sur toute une face ; ceci n'est pas une prédiction EM ou quantique de force Casimir réelle.

**Grandeur**. Pour deux listes de points distincts A et B, avec matrices de covariance C_A,C_B,C_AB :
  delta F/(kBT) = 1/2 [logdet(C_AB_ensemble)-logdet(C_A)-logdet(C_B)]
= 1/2 logdet(I - C_B^{-1/2} C_BA C_A^{-1} C_AB C_B^{-1/2}).
La normalisation retire les contributions d'autocontrainte des objets séparés ; les matrices sont supposées définies positives. Le zéro de l'énergie est la séparation infinie. Le signe n'est pas choisi après calcul. Formule issue du quotient des densités gaussiennes aux contraintes nulles.

**Géométries fixes sans interpénétration**. Tétraèdre régulier de côté 1. Triangle face XY aux sommets (0,1/sqrt(3),0),(-1/2,-1/(2sqrt(3)),0),(1/2,-1/(2sqrt(3)),0). Quatrième sommet (0,0,+h), h=sqrt(2/3). La face de l'objet A est dans z=0 et A occupe z<=0 pour F-F ; celle de B est dans z=g et B occupe z>=g. Scénarios : FF0 (faces alignées, rotation 0 autour z), FF60 (face B tournée de pi/3 autour z), TF (A pointe vers z=0 depuis z négatif, B face dans z=g avec apex positif), TT (A pointe vers z=0 depuis z négatif et B pointe vers z=g depuis z positif). Les coordonnées des pointes et faces sont placées de telle manière que les enveloppes sont dans les demi-espaces disjoints z<=0 et z>=g. Il s'agit de comparateurs géométriques, pas des quatre voies historiques d'assemblage C-1.

**Grille fermée**. ell={0.25,0.50,1.0} ; g={0.15,0.30,0.60,1.20} ; scénarios={FF0,FF60,TF,TT} ; prélèvements={4,14}, soit 96 couples. Calculer dF et l'écart signé de logdet pour chaque cas. Mesurer une dérivée de force numérique -dF/dg à g=0.30, pour ell=0.5, sur tous les scénarios et les deux densités, avec h_d=1e-4 et h_d/2 ; publier l'écart relatif. Toutes les distances sont exprimées en unités de côté, toutes les énergies en unités kBT.

**Prédictions/falsifications pré-déclarées**.
P1 [T, attendu] dF<=0 pour les 96 cas pour ce couplage de mêmes contraintes gaussiennes, à tolérance 1e-10 ; un résultat positif dénote erreur ou violation du modèle.
P2 [H] Pour chaque ell,g et densité, FF0 a une attraction (dF plus négative) au moins aussi forte que TT à séparation verticale g égale. Tout contre-exemple doit être listé.
P3 [H] Pour ell=0.25, g=0.15, FF0 a un dF strictement inférieur à FF60 aux deux densités ; sinon FAIL.
P4 [T, attendu] Après annulation du bloc C_AB, dF=0 à 1e-12 ; échange A/B et translation rigide dans l'espace conservent dF à 1e-10.
P5 [T, attendu] Une interaction irréductible à trois corps apparaît pour trois contraintes ponctuelles alignées à 0,d,2d (ell=0.5,d=0.30). Calcul : F123-F12-F13-F23+F1+F2+F3, exprimée en kBT. Les termes F_i désignent 1/2 logdet de chaque covariance restreinte ; le signe et la valeur seront publiés, sans sélection a posteriori.

**Comparateur indépendant**. Calculer dF par (a) trois logdet de matrices de covariance et (b) produit des valeurs singulières de la matrice de corrélations croisées blanchie. Exiger accord absolu <=1e-9, et SPD de C_ensemble (valeurs propres strictement positives). Contrôler aussi les limites g grand => dF tend vers 0 ; ell court => dF tend vers 0. Si des écarts apparaissent, classer NUM_INDETERMINE et ne pas corriger les valeurs après le gel.

**Statuts et bornes**. [T] identités mathématiques exactes, [CERT] double calcul validé, [M] faits internes au modèle, [H] hypothèses non dérivées, [FAIL] prédictions démenties, [OPEN] transition vers physique. Pas de gravitation primitive. La bathification par annihilation, l'origine des modes du champ, la métrique 3D, l'échelle ell, T et les contraintes des frontières ne sont PAS dérivées. Aucune naissance du premier simplexe, aucune liaison microscopique ou capture irréversible démontrée. TOE 0/7.

**Interdiction d'ajustement**. Aucun paramètre/critère ne change après empreinte. Une extension (sources réelles, champs vectoriels, maillages plus fins, modèles dissipatifs, premières annihilations) doit devenir CAS-2 et avoir son propre gel.
