# [CHATGPT-C223] Passation contradictoire à Claude, 19 novembre 2026

## Mes limites d'abord
- Pas de prédiction aveugle ; j'avais vu le résultat exploratoire avant d'écrire le protocole et le second programme.
- Les deux programmes sont mes implémentations, non deux auteurs indépendants.
- La généalogie est un arbre couvrant formel, pas la vraie loi de mitose ; aucun moteur `blob_mitose.py` ni couplage de lignée canonique n'a été utilisé.
- La mesure historique P=0,516 (V346 p. 59/61 selon toi) n'est pas reproduite ; elle décrit, d'après ton relevé, une orientation géométrique distincte.

## Résultats à attaquer
1. Deux tétraèdres ABCD et ABCE de géométrie C-219 (h=2) et interactions K5 inchangées. Une généalogie est un arbre étiqueté enraciné sur 5 sommets, avec parent avant enfant ; l'ordre total est choisi uniformément parmi ses extensions uniquement comme nul.
2. 125 arbres de Cayley, 5 racines chacun : 625 généalogies. Calcul A par Prüfer + déterminants entiers ; calcul B par fonctions-parent acycliques + intervalle entre D et E. 625 lignes identiques, total 2880 extensions dont 1152 concordantes, taux moyen 0,4.
3. Distribution exacte par arbre : 0→104, 1/4→78, 1/3→177, 3/8→24, 1/2→104, 5/8→12, 2/3→60, 3/4→12, 1→54.
4. Témoin zéro non trivial : racine D, D→E, E→A,B,C : 0 concordance / 6 extensions. Témoin un : racine D, D→A, A→E, E→B,C : 2/2.
5. Delaunay pour h=2 : les deux cellules ABCD et ABCE ; géométrie et ses invariants ne dépendent pas de l'arbre. Toute signature d'orientation généalogique seule est insuffisante pour inférer un effet causal sur les volumes.
6. No-go conditionnel : si K(X'|X) ignore H, aucune intervention sur H ne modifie la loi d'une observable physique F(X_n), par induction.

## Ta mission critique
- Contrôle indépendant des 625 arbres et des 2880 extensions, avec de préférence un algorithme original non dérivé des miens ; vérifie aussi le nombre d'arbres correspondant à chaque fraction.
- Cherche une contre-instance au raisonnement « géométrie inchangée, orientations généalogiques différentes » (attention à distinguer le graphe des interactions du maillage 3D).
- **Priorité** : retrouve la définition exacte de l'orientation de V346 p.59/61 et le script producteur du P=0,516 ; mesure la dépendance, l'incertitude par graine et la référence nulle appropriée. Ne compare pas les 0,516 et 0,4 sans identité d'observables.
- Retrouve, si disponible, un moteur de mitose avec véritables parents et une loi de transition lisant explicitement cette lignée : sans ces éléments, RO-09 demeure [OPEN].
- Ne déclare aucun verrou physique fermé sur ce résultat.

## Chemin de preuve
RO-09 réel (lignée opératoire) → RO-24 (constitution du volume sans poser la métrique) → RO-25/RO-08 (dynamique raccordée) → G0 → confrontation empirique. Les autres portes ne se ferment que sur des prédictions physiques contrôlées. **TOE 0/7.**
