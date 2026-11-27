<!-- Note du pilote : rapport du contre-auditeur indépendant (sous-agent Claude Opus), premier passage, reçu le 27 novembre 2026. Reproduit sans modification sous cette ligne. Les suites données sont à la section 292 du carnet X-28. -->

# Contre-audit X-28

## Écarts et erreurs trouvés

1. **La réduction (a) de la section 291 est déjà réfutée, par les propres données du carnet.** `x28_ajouts_comble.out` donne au palier 6 un tissu comblé **non convexe** (360 murs sur 38 070). Mon calcul indépendant donne le même résultat : convexe aux paliers 3, 4 et 5, 360 murs mauvais au palier 6, avec le témoin cellule {(−4,1,16,4,16), (−3,0,12,4,12), e₅, e₃}. « Il suffirait de démontrer pour tout palier (a) » propose donc une voie fausse, et X-29 (section 294) la reprend. En 289, «CB6» doit valoir 5.
2. **T3, étape 3 : lacune.** La conclusion est juste : la réunion des cônes est convexe. Mais la justification donnée ne la prouve pas. La phrase « Ce sont les tuiles de p qui restent du bon côté de tous les murs de l'étape 1 passant par p » n'est pas démontrée, et elle n'est pas nécessaire. Le bon argument : K convexe et R_p convexe, donc K∩R_p est convexe dans le complexe de W_p. Il faut aussi la description de Tits, valable même aux rayons nuls q+p, r+p, qui sont des pointes du pavage idéal {3,3,6}. Pour ces pointes, un argument de projection sur le résidu du point est nécessaire, et le carnet n'en dit rien. (C2), tel qu'il est énoncé, ne vaut qu'à l'intérieur du cône de Tits.
3. **(C3), dernière clause : ce n'est pas un fait de Coxeter seul.** proj_{R_p}(c) ∈ R_q n'est vrai que si R_p∩R_q ≠ ∅, c'est-à-dire si p et q liés partagent une tuile de l'empilement. C'est un fait sur l'empilement (vrai par arithméticité et rationalité des points de contact, mais ni cité ni démontré). La section 283.3 le range à tort parmi les faits classiques.
4. **T6 : deux trous.** (i) Le carnet affirme sans preuve que « deux constituants strictement de part et d'autre d'un mur ne sont jamais liés ». C'est vrai, par l'argument suivant : leur point de contact serait sur le mur, donc v = image de u, donc u serait tangent au mur, donc ⟨u, t−t′⟩ = ±√12, ce qui est impossible pour un vecteur entier. Données : 0 paire liée à travers un mur, paliers 0 à 5. (ii) Pour que l'image de u naisse, il faut que la cellule image C* ait un côté né, et ce point n'est pas justifié. Si l'autre côté v de C est du côté du germe, tous les membres de C sont sur le mur, donc C est la cellule du mur et u* = v. C'est réparable, mais absent du carnet.
5. **T1 : hypothèse affirmée.** « Quatre constituants ne passent pas par un même point » est faux pour des vecteurs entiers de norme 1 quelconques. C'est vrai pour des membres de l'empilement (au plus deux sphères par point), mais non démontré. Le « miroir » n'est une sphère que si ⟨d,d⟩ > 0. C'est le cas pour p et trois voisins : la signature est (3,1).
6. **T2 :** « ν entier, donc ν = 1 » omet ν ≥ 1, qui demande q ≠ r et le non-chevauchement des membres distincts de l'empilement. Lean : seul le cas x rationnel (v/D) est couvert. Les places quadratiques invoquées en T3 ne le sont pas (la preuve papier les couvre).
7. **Section 293 :** « cinq fois plus loin en paliers, soixante fois en constituants ». Je n'ai pas pu le vérifier faute de référence X-27 chiffrée ; 7 290/120 ≈ 61.

Le reste a été vérifié et est juste. J'ai refait l'algèbre de T2 : A ≤ 2 et 2ν = A² − Σα². J'ai refait celle de T2 bis : π = a+B−1, a+B ≤ 1, B = ν, Σb² = B(2a+B), d'où B(3a+B) ≥ 0. T4 est juste : deux vecteurs nuls de produit négatif avec a+p sont dans la même nappe, ξ ≠ 0. T5 est juste. Les étapes 1, 2, 4 et 5 de T3 aussi.

## Tableau

| Point | Verdict | Nombre ou raison |
|---|---|---|
| T1 | confirmé avec lacune | hypothèse « pas de point commun » affirmée (n° 5) |
| T2 | confirmé | algèbre refaite ; lacune ν ≥ 1 mineure |
| T2 bis | confirmé | algèbre refaite |
| T3 | confirmé sous lacunes | étape 3 et C3 (n° 2, 3) ; étapes 1, 2, 4, 5 justes |
| C1 | confirmé | GLMWY III, th. 5.1 : (S_jS_k)³ = I, A₃ de Coxeter hyperbolique ; angles π/3 recalculés (⟨w_i,w_j⟩ = −6, norme 12) |
| C2 | confirmé avec réserve | vrai dans le cône de Tits ; pointes non traitées |
| C3 | confirmé avec réserve | exige R_p∩R_q ≠ ∅ |
| T4 | confirmé | — |
| T5 | confirmé | — |
| T6 | confirmé sous lacunes | n° 4 |
| B1 | confirmé | 5, 10, 30, 120, 450, 1 800, 7 290 ; libres 5, 20, 90, 330, 1 350, 5 490, 21 870 |
| B2 | confirmé | toutes les places = côtés libres : 5, 20, 90, 330, 1 350 ; 0 irrationnelle, 0 dégénérée ; 148 320 puis 2 442 840 triplets (tous les parents) |
| B3 | confirmé | convexe à 0, 1, 2 ; 120/390, 360/1 530, 1 440/6 210 |
| B4 | confirmé | paliers 0–4 : 24 420 paires, 23 700 milieux dans une tuile, toutes liées, 0 exception ; 720 hors tuile, toutes non liées |
| B5 | confirmé | 22 constituants, 18 tuiles, 7/56 murs ; produits −5 et −13, 0/18 ; jumelle (2,2,2,−1,0), non née |
| B6 | confirmé | images nées, palier ≤ : 180/180 (p3), 720/720 (p4), 2 880/2 880 (p5) |
| B7 | confirmé (empirique) | 2 859 tuiles aléatoires, 182 597 paires non liées à milieu dans T, programme linéaire en flottants : 0 cas réalisable |
| Lean `pont` | confirmé | compile (3,7 s) ; 0 `sorry` ; axiomes standards ; hypothèses satisfaisables (germe, q=a, r=b, x=p+a+b+c−d) ; x rationnel seulement |
| Tissu comblé convexe | infirmé au palier 6 | 360/38 070 |
| D. Antériorité T2/T3 | non tranché | rien trouvé |

## Non contrôlé

N7 (files d'attente, paliers incomplets) ; N9 (comparaison à l'outil X-27) ; B2 au palier 5 ; T2 bis sur données ; « 9 cas » de X-27 bis ; « tuiles ↔ éléments du groupe » (toute 5-clique de l'empilement dans l'orbite) ; outils Lean annexes (leanchecker, nanoda, mutants). En B7, le programme linéaire en flottants sert à chercher des cas, pas à décider. Sources : [GLMWY III, arXiv math/0010324](https://arxiv.org/abs/math/0010324) ; [Kontorovich–Nakamura, arXiv 1712.00147](https://arxiv.org/abs/1712.00147) ; [Local-global Soddy, arXiv 1208.5441](https://arxiv.org/pdf/1208.5441) ; aucun n'énonce T2 ou T3 (recherche limitée à 4 requêtes).
