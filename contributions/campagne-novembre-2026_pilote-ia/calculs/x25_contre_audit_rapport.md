# Contre-audit X-25

## 1) Verdicts
- **E1 VRAI.** L'orthogonal de la cellule est une droite de genre espace : deux solutions. Vérifié exactement pour n = 2 à 8.
- **E2 VRAI.** Formule exacte (Tchebychev, n = 3 à 8) ; chaîne 1 − 2k² vérifiée.
- **E3 VRAI AVEC RÉSERVE.** Sur toutes les suites : n = 4, minimum de 4 naissances (79/81) ; n = 5 à 8, minimum de 3 (−1/4, 29/125, 13/27, 215/343). n = 2 jusqu'à la profondeur 7 et n = 3 jusqu'à la profondeur 6 : aucun croisement ni emboîtement. « À toute profondeur » est le théorème connu (Boyd ; GLMWY), et E4 ne le prouve pas.
- **E4 FAILLE.** L'argument prouve que les **bords** ne se croisent pas (|⟨a,b⟩| ≥ 1), pas que les intérieurs sont disjoints. Sur 7 275 miroirs de type u de W, on compte 0 croisement mais 6 457 080 paires emboîtées. Il faut un argument de plus (domaine fondamental de Γ_f) ou citer GLMWY III. Avec ⟨u_i,d_i⟩ < 0, il faut poser f_i = +d_i. Niven ne prouve aucun chevauchement.
- **E5 VRAI AVEC RÉSERVE.** Je retrouve tous les nombres par un code indépendant, et aussi avec trois ordres aléatoires. Jamais k ≥ 3 ; au palier 6, la surface est une 3-variété close (χ = 0) dont les arêtes sont exactement les contacts. Réserves :
  - parmi les fermetures des paliers 4 à 6, 60, 180 et 720 sont des naissances doubles : leur lien **est posé par une naissance**. Les contacts réellement non posés sont 0, 0, 10, 30, 90, 450, 1 710 (2 290 au total, et non 3 250) ;
  - l'argument « une infinité de configurations » ne suffit pas. Le bon argument : le lien d'une arête dans le tissu est un plan triangulé, qui ne contient aucune 2-sphère finie.
- **E6 VRAI AVEC RÉSERVE, connu.** Modulo ±, « genre temps » couvre à la fois disjointes et emboîtées. « Aucune paire de genre espace » veut donc dire « aucun croisement », pas « aucun chevauchement ». Le genre lumière inclut le contact intérieur. La lecture vaut à tout rang (dS_{n+1}). Le cosh τ est exact.
- **E7 VRAI** :
  - N1 : Gram de taille 6, de rang 6 > 5 ;
  - N2 : découle de E2 ;
  - N3 : N2 appliquée au triangle (a, b, x) ;
  - N4 : découle de E1 ;
  - N7 : après inversion au point de contact, deux cercles de centres x et y se coupent en au plus deux points.

  Conditions nécessaires, pas suffisantes.
- **E8.** Mots de trop :
  - « le seul » : non démontré pour n ≥ 4, et vide puisque ces rangs chevauchent ;
  - « est un espace-temps » : écrire « se lit comme de Sitter, cinématiquement, à tout rang » ;
  - « le lien est un rayon de lumière » : écrire « tout lien est de genre lumière », sans la réciproque ;
  - « exclus » doit être suivi de « sous cette lecture ».

## 2) Nombres recalculés
E1, E2, E6, les minima de E3, les murs, les paliers et fermetures de E5, et N7 sur l'état graine 1 à 1 037 constituants (empreinte c0e1a427…, 3 violations). **Aucun écart.**

Classements :
- confirmés faux : A7, B1 à B3, Q4, T1 (7/8), T2 (10/12), T4 première clause (0/4), T6 (3/4), N7 ;
- vrais : A8, B4, T3, T5, T7.

À corriger :
- Q4 : les fermetures sont justes aux paliers 4 et 5 ; seul le palier 6 est faux ;
- Q5 : la clause « 4,60 à 4,70 tétraèdres par lien » est vraie (4,65). Q5 est donc partiellement vraie.

## 3) Antériorité
- Soddy, « The bowl of integers and the hexlet », *Nature* 139 (1937).
- Boyd, « The osculatory packing of a three dimensional sphere », *Canad. J. Math.* 25 (1973).
- Graham, Lagarias, Mallows, Wilks, Yan, « Apollonian circle packings: geometry and group theory III. Higher dimensions », *Discrete Comput. Geom.* 35 (2006) : packing en dimension 3 seulement, groupes de Coxeter, hexlet.
- Maxwell, « Sphere packings and hyperbolic reflection groups », *J. Algebra* 79 (**1982**).
- Baragar, « Higher dimensional Apollonian packings, revisited », *Geom. Dedicata* (2018).
- H. Chen, « Apollonian ball packings and stacked polytopes », *Discrete Comput. Geom.* 55 (2016) : un polytope empilé est apollonien ssi aucun triangle n'est partagé par six 4-cliques. C'est la fermeture de E5.
- De Sitter : Hertrich-Jeromin (2003) ; Fennen–Giulini (arXiv:1909.08109), qui posent contact ⇔ genre lumière.

E1 à E4 et E6 sont connus. Me paraissent non publiés : les comptes de la règle « surface », l'énoncé explicite de N7, l'application aux moteurs.

## 4) Erreurs, par gravité
1. E4 donné comme une preuve, alors que l'emboîtement n'est pas exclu.
2. E8 : sur-affirmations (« le seul », « espace-temps », lumière ⇔ lien).
3. E5 : 3 250 à ramener à 2 290 ; l'argument « jamais 3→2 » est invalide en l'état.
4. Signe de f_i ; année de Maxwell ; Q4 et Q5 à nuancer.

## 5) Ce que cela ne donne pas
- Ni dynamique ni temps physique : le palier n'est pas un temps.
- Aucune métrique dérivée : celle de de Sitter est posée a priori.
- Aucune causalité dynamique.
- Aucune matière.
- Aucun lien démontré avec le moteur réel : il pratique une autre naissance, viole N7, et T8 a échoué.

V1 reste ouvert.
