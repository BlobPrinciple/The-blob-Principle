<!-- Note du pilote : rapport du contre-auditeur indépendant (sous-agent Claude Opus), troisième passage (X-30), reçu le 27 novembre 2026. Reproduit sans modification sous cette ligne. Les suites données sont à la section 318 du carnet X-30. -->

# Contre-audit X-30 (troisième passage)

## Faux ou troué

Rien de faux. Trois imprécisions :

1. **T14, second point.** L'argument « deux boules liées ne sont pas strictement de part et d'autre d'un mur » est renvoyé à (C4). Or (C4) ne traite que des constituants entiers. Pour une place x quelconque, il faut ajouter que T13 donne ⟨x, n⟩ ≥ 6 > √12 : la boule fermée de x est alors strictement au-delà du mur, et la conclusion suit.
2. **T13.** « Au-delà » n'a le sens « loin du germe » que si la tuile est la tuile-porte de u. L'énoncé vaut pour toute tuile.
3. **T12.** « La somme diminue de deux fois la coordonnée retournée » : il faut lire « de deux fois sa valeur absolue ». La descente n'est pas déterministe, mais la preuve vaut quel que soit l'ordre des retournements.

Points dont tu doutais, tous justes :
- **T12, coordonnées après k retournements.** Ce sont celles de x dans la base de la tuile g⁻¹(germe), avec g le produit des retournements faits ; la règle de retournement est la même dans la base de n'importe quelle tuile.
- **T12, emploi de T1.** Quatre membres d'une tuile forment une cellule, c'est-à-dire un parent et trois voisins indépendants : T1 s'applique, et les deux boules qu'il autorise sont les deux côtés de la cellule, deux constituants.
- **T14, de génération en génération.** La récurrence est juste. Un ancêtre sur le mur a sa tuile-porte du côté du germe (C3 bis) ; un ancêtre strictement du côté du germe n'a de tuiles que de ce côté.

J'ai refait l'algèbre de T13 : b = A − 1, Σa² = A², 2Σc_ic_j = 6(A−1)(A−2), A ≥ 4/3. Le cas d'égalité est juste.

## Tableau

| Point | Verdict | Nombre ou raison |
|---|---|---|
| T13, T12, T14 | confirmés | imprécisions 1 à 3 |
| Lean `fenetre` | confirmé | fidèle pour x rationnel (contact éliminé par b = A − D ; non-chevauchement ; rondeur Σa² = A²) ; recompilé, 0 `sorry`, axiomes standards ; satisfaisable : a = (1,1,1,−1), D = 1 (retourné de f₄, cas d'égalité) |
| Palier 3, partage | confirmé | 237 300 boules : 47 100 dans l'empilement, 190 200 hors |
| U1 | confirmé | 10 640 couples ; minimum 6 ; 6 560 égalités, toutes des retournés |
| U2 | confirmé | 144 420 rationnelles (92 880 irrationnelles) : 47 100 descentes achevées, toutes dans l'empilement ; 97 320 qui quittent le cône, toutes hors |
| U3, (G1) au palier 3 | confirmé | 190 200 hors de l'empilement, toutes chevauchent un parent |
| E, palier 3 | confirmé | 190 200 hors ; 43 900 égales à un ancêtre ; 3 200 constituants qui ne le sont pas |
| E, second passage | inchangé | mon test ne cherchait le chevauchement que pour les boules déjà reconnues hors de l'empilement : les 2 163 082 sont toutes hors |
| (G1) en profondeur | non infirmé | 2 419 980 quadruples, tuiles jusqu'à la longueur 20, tuiles-portes jusqu'à 37 ; 1 302 727 boules hors de l'empilement, toutes chevauchent un parent ; 0 contre-exemple |

## Non contrôlé

- Le palier 4 (sortie `x30_tout_4_sym.out`).
- Les contrôles Lean annexes (leanchecker, nanoda, con-ron, énoncés modifiés).
- T12 en calcul pour les boules irrationnelles.
- (G1) n'est éprouvé que par tirage ; ce n'est pas une preuve.
