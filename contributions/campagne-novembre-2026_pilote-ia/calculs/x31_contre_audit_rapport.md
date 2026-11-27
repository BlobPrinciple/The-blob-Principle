# Contre-audit de X-31 (sections 334 à 344)

Code neuf, sans rien importer du laboratoire ; entiers exacts, sauf les boules non entières (flottants). Descente contrôlée contre un parcours en largeur : 19 380 contrôles, aucun désaccord.

## Faux ou troué

1. **T23, « quatre cellules nouvelles apparaissent ».** Faux dès que x a d'autres voisins nés que a, b, c, d : sous la règle, 60, 180, 720 nouveau-nés (paliers 4 à 6) en ont 5 ; dans mes tissus, des places créent 7 ou 10 cellules. Réparation : « au moins quatre », et corriger « cellules filles : 4 » en section 340.
2. **T24, « deux voisins de p nés au même palier ne sont jamais liés ».** Faux au palier 0 (108 paires, par exemple p dans le germe). Réparation : « à partir du palier 1 ».
3. **T24, « la profondeur est le palier ».** Trou : la preuve emploie T7 au rang 2, ni démontré ni admis. Réparation, par récurrence : S(n) = disques dont la tuile-porte est à distance au plus n ; un triplet lié est dans deux tuiles voisines, et le disque créé par la plus proche est dans le triplet.
4. **Section 340, « une seule chose vue de trois façons ».** Trop fort : T24 ne décrit que le pourtour vu de p ; dans le tissu, le fil divisé demeure (votre propre tableau). La suite 4, 8, 20, 56, 140, 368, 980 est mesurée, non démontrée.

T20, T21, T22, T25, T26 : aucun pas faux sous les faits admis (p dans le germe bien traité ; « pas trois » épuise les cas).

## Imprécisions

- **T20, « de deux choses l'une ».** Non exclusif : la conclusion du second cas vaut aussi pour 60, 240, 900 paires où p est parent (7 456 dans mes tissus).
- **T25.** Écrire « au palier g au plus » (nombres cumulés). L'unicité de la solution de la règle manque (une ligne de récurrence). Le décompte se démontre : avec E = g + 1, compter les u de {0..E}³ de minimum 0 et de somme ≡ 1 (mod 3) ; le filtre par les racines cubiques de l'unité donne E(E + 1) + [E ≡ 1], soit (g + 1)(g + 2) + [3 | g] (vérifié jusqu'à g = 300).
- **T24.** La connexité des tuiles de p n'est pas dans (C9) ; « elles diffèrent » est faux si les deux disques sont dans le germe.

| Point | Verdict | Nombre ou raison | Fichier |
|---|---|---|---|
| A1, T20, règle, n = 2, 3, 4 | confirmé | 1 260, 5 160, 20 700 paires ; parents 1 260, 5 100, 20 520 ; cousins 0, 60, 180 ; 0 exception | a_regle_rang3.out |
| T20, 40 tissus (41 à 150 constituants, génération jusqu'à 9) | confirmé | 154 135 paires ; 151 496 parents ; 2 639 cousins ; 0 exception | b_tissus_1_40.out, f_resume.out |
| T21, places par résolution directe | confirmé | 40 tissus sur 40 ; 10 533 places = côtés non nés ; 0 place non entière libre (flottants) | b_tissus_1_40.out |
| T22 | confirmé | règle : 135, 585, 2 355, 9 645 cellules ; mes tissus : 16 308 ; aucune sans côté né ; côté né seul toujours du côté du germe | a_regle_rang3.out, b_tissus_1_40.out |
| Témoin non clos | confirmé | 11 essais non clos : T21 en défaut 11 fois, T22 5 fois | c_temoin.out |
| T23 | faux | 60, 180, 720 nouveau-nés à 5 voisins ; 1 015 places à 7 cellules, 4 à 10 | a_regle_rang3.out, b_tissus_1_40.out |
| Rang 2 : tailles, 3 × 2^g, division d'un fil | confirmé | 4 à 13 124 disques ; 19 700 couples, 0 écart ; 39 360 naissances, chacune divise un seul fil du pourtour | d_rang2.out |
| Rang 2 : liens de même palier | faux au palier 0, confirmé à partir du palier 1 | 6 liens, tous au palier 0 ; 108 paires de voisins | d_rang2.out |
| T25, les dix fils | confirmé | 3, 6, 12, 21, 30, 42, 57, 72 (paliers 0 à 7) ; palier = étendue − 1 sans écart | a_regle_rang3.out, e_reseau.out |
| T26 | confirmé | paliers 1 à 6 : 0, 10, 30, 90, 450, 1 710 paires, toutes cousines | a_regle_rang3.out |
| (g), voisins d'un constituant du germe | confirmé | 4, 8, 20, 56, 140, 368, 980, 2 552 | a_regle_rang3.out, e_reseau.out |
| Explication du 979 (X-30 bis) | non contrôlé | programme de X-30 bis non relancé | — |

## Non contrôlé

Vos 200 tissus de A2 ; tout réservoir au-delà du résidu de rayon 3 (plus places et côtés) pour T20 ; les faits (C1) à (C9), sauf à travers la descente ; Lean ; le lien conceptuel avec la division de l'arête. Un premier lancement a échoué (dépassement d'entiers 64 bits), non enregistré : j'ai plafonné la génération. Des tirages ne sont pas une preuve.
