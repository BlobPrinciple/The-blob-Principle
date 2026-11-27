# Contre-audit X-32 (T27, T28)

## Faux ou troué

Rien qui renverse T27 ou T28 ; quatre trous réparables.

1. **T28, « Deux constituants différents n'ont aucune fille propre commune (T27) » : faux tel qu'écrit.** Chaque constituant du palier 1 est fille propre de quatre constituants du germe ; T27 exclut le germe et le palier 1. Réparation : « différents et hors du germe ». Sans conséquence : seul cas employé dès la génération 2.
2. **T28, « aucune n'était née » : affirmé sans preuve.** Il manque : toute née à h ≥ 2 est fille propre d'une née à h − 1, et sa mère propre est unique (T27). Une fille propre d'un constituant hors du germe a une tuile-porte de longueur ≥ 2 : elle n'est ni du germe ni du palier 1. Une fille propre de c, née à g, ne naît donc qu'à g + 1.
3. **T27, mère propre, cas d'un seul mur : « ce serait T′(x) ».** Le cas T(g) = T(x) est oublié. Réparation : T(x) aurait ses cinq murs non séparants, ce serait la tuile du germe.
4. **T27, cas de deux murs : « sans être la tuile-porte d'aucun des deux ».** Il faut aussi exclure les deux autres parents et T(x). Réparation : le mur opposé à f passe par tous les autres constituants de T′(x), et celui opposé à f̃ passe par f. T(x) s'exclut comme au point 3.

Justes, sous les faits admis : l'ordre T′, T, T* ; les distances le long de l'anneau ; « donc cousins » ; le compte 0, 1 ou 2 ; les comptes 3 et 2 de T28 ; le plancher né ; T21. La preuve donne au moins 2 options à l'ancienne mère et au moins 3 à la nouvelle-née : aucun ordre de choix ne peut bloquer la règle.

## Imprécisions

- La « mère » de T28 (celle qui choisit) diffère de la mère propre dès la deuxième fille ; la section 346 ne la définit pas.
- Section 345, point 2 : « deux ou trois filles possibles » ne vaut que pour l'ancienne mère ; la nouvelle-née en a 3 ou 4.
- Section 345, point 3 : « à chaque génération, deux sur trois » est faux au début. La part occupée vaut 1,0 à la génération 0, puis 0,5 ; elle tombe vers 0,34 à partir de la génération 5.
- Sections 345 (point 4) et 350 : les liens de même génération dépendent de la stratégie de choix. À la génération 10, j'en compte 9 198 sur 30 tirages au hasard et 28 160 sur 44 lancements « priver_fille ». Au hasard, l'ordre de grandeur concorde.
- Sections 351 et 353 : « une seule chose » et « ce qui séparait […] était la règle » sont des lectures. Une règle tient ; rien ne montre que c'était le seul obstacle.

| Point | Verdict | Nombre ou raison | Fichier |
|---|---|---|---|
| T27, règle à la lettre, q jusqu'au palier 5 | confirmé | 1 795 q, 7 180 cellules : 4 820 filles propres, 2 360 cousins, 0 autre, 0 désaccord avec le mur | t27_palier6.out |
| Tailles de la règle à la lettre | confirmé | 5, 10, 30, 120, 450, 1 800, 7 290 | t27_palier6.out |
| Filles propres par palier | confirmé | 5 à 4 ; 20 à 3 ; 60 à 3 et 30 à 2 ; 240 et 90 ; 900 et 450 | t27_palier6.out |
| Mère propre unique ou aucune | confirmé | 1 220 avec une mère, 570 sans, tous avec deux parents cousins | t27_palier6.out |
| T28 : 30 tirages, puis 5 stratégies × 44 départs, 10 générations | confirmé | 250 lancements, 0 blocage, 5 120 partout, 0 erreur, 0 chevauchement | t28_bilan.out |
| Options minimales | confirmé | ancienne mère ≥ 2, nouvelle-née ≥ 3 ; au plus bas, 1 option restante (stratégie adverse) | t28_bilan.out |
| Tuile-porte par descente | confirmé | descente après 4 retournements au hasard, 0 écart | t28_bilan.out |
| Voisins d'une nouvelle-née | confirmé | 4 ou 5 | t28_bilan.out |
| Variante libre (hors T28) | glouton bloqué | le glouton bloque dans 14 lancements sur 15 ; un couplage parfait est toujours trouvé ; 5 120 constituants | libre_resume.out |
| Places laissées libres | imprécis | 1,0 ; 0,5 ; …, puis environ 0,34 | places_t28_1_3.out |
| SHA-256 de la prédiction | confirmé | 707c45ef…3535321 | sha_prediction.out |

## Non contrôlé

- Les faits admis ((C3) pour trois constituants, (C3 bis)) : relus en termes de groupe de Coxeter, non calculés.
- Rien devant Lean ; rien au-delà de 10 générations ; choix non énumérés.
- Ni les symétries des 44 départs, ni les voisins selon l'âge, ni le commit.

Des tirages ne sont pas une preuve.
