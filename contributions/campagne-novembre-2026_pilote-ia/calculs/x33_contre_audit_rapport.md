# Contre-audit de X-33

## 1. Verdict
Tous les nombres refaits de 360 et 361 sont retrouvés. Aucun pas faux dans 359.
Trois phrases fausses de la prédiction ne sont pas déclarées. Deux trous mineurs ; l'unicité de T32.4 dépend d'un appariement non justifié.

## 2. Erreurs
Erreurs de déclaration :
- La prédiction de T31 dit « deux constituants liés sont mère et fille (ou parent et enfant), ou bien cousins nés à la même génération ». C'est faux pour les liens du germe. Corrigé sans déclaration.
- La prédiction de T30 dit « tout constituant né a exactement deux filles propres ». Le germe en a quatre. Ce défaut est déclaré pour D5, pas pour T30.
- La prédiction dit des impaires « (ce sont des reflets) ». Seules les transpositions en sont.

## 3. Trous
- **T32.4.** « Une seule façon » n'est vraie que si les deux filles à risque sont appariées entre elles. Sinon, deux façons identiques sont permises (`synthese.out`). Justification à écrire : la transposition de T(q) échangeant a et s, donc les sœurs, induit cet appariement.
- **Conséquence.** La « Raison » ne déduit pas « quatre âges différents ». Il manque une ligne : hors du germe, deux liés n'ont jamais le même âge. L'étiquette « [T] » omet « sous les faits admis ».
- **Sans trou** : l'emploi symétrique de T15, qui découle de son énoncé ; l'anneau, où six tuiles distinctes donnent u ≠ y (non écrit) ; les deux sens de T30 ; T31.4, q du palier 1 compris.

## 4. Imprécisions
- 356.13 et la table 360 disent « une phrase fausse » pour D4. Or « aucun entre constituants de la même génération » est faux aussi.
- 362, « à une symétrie du germe et un reflet près » : les reflets sont des symétries du germe, il y a une seule classe.
- 356.4, « s'excluent », dépend d'une lecture, que seule la section 362 avoue. « Anneau fermé » n'est pas défini.

## 5. Mes calculs

| Point | Obtenu | Accord | Fichier |
|---|---|---|---|
| Descente | 0 désaccord avec un parcours en largeur, rayon 7 | — | v0_criterion.out |
| D1 | 8 010 = 10 + 7 180 + 820 ; 0 hors de la forme ; murs 5/1 220/570 | oui | d1_5.out |
| D2 | 24, 690, 3 120, 3 270, 660, 12 ; classes [24], [12, 12] ; stabilisateurs : 5, pairs | oui | d2d3.out |
| D3, sur les 24 | 3 125, 12 500, 20 000, 16 000, 6 400, 1 024 | oui | d2d3.out |
| D4 | 20 470 ; 0 de même génération, 0 chevauchement ; 5 symétries, 0 impaire ; A vers B : 5 symétries, 0 paire | oui | d4_regle_10.out |
| D5 (a) | 51 100 constituants avec deux filles propres nées | oui | d5_hasard_1_20_10.out |
| D5 (b) | 44 départs, 2 598 156 déroulements : les 7 776 de T30, pour chaque départ ; génération 3, 8 tissus : 59 049 chacun | oui | d5_brute2.out, d5_brute3_8.out |
| D6 | 704 en 8 classes | oui | d6.out |
| T31.2 | 0 lien hors de la forme annoncée | oui | d5_hasard_1_20_10.out |
| T32.3 | 75 000 ; 0 lien entre non-sœurs ; 5 façons pour chacune des 7 650 paires | oui | synthese.out, d4_hasard_1_6_10.out |
| Conséquence | 5 105 cellules ; 4 800 sur 4 800 à quatre âges | oui | d4_regle_10.out |

## 6. Hors de l'énoncé
**Symétries cachées.** Dans D4, les cinq constituants de degré maximal (314) sont le germe. Toute isométrie conservant le tissu, ou envoyant A sur B, permute donc le germe, qui est une base : c'est une des 120. La restriction de 356.9 tombe ici.

## 7. Non contrôlé
- Les graines de X-32 : mes tirages diffèrent, et j'obtiens 12 224 liens de même génération.
- La réciproque de T30 au-delà de la génération 3. Pas à pas, elle n'est testée que sur des tirages, à h ≤ 6 (paramètre de `d5.py`).
- La formule à g ≥ 4, non énumérée.
- La variante D6 au-delà de la génération 2.
- Les faits admis, relus sans être recalculés.
- Le programme du pilote, lu en partie.
