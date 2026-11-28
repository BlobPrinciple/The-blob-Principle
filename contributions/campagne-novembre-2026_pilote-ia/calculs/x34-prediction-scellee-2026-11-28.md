# X-34 — prédictions scellées avant calcul (28 novembre 2026)

Deux contrôles, écrits à partir des seuls textes de l'auteur (master V277 et son tome de campagne), sans son code. Programme : `x34_replication_blob_canonique.py`, déposé dans le même commit que ce texte, avant toute exécution autre qu'un essai de syntaxe à N = 200.

## R1 — Réplication du Blob canonique

**Source de la prédiction.** « Dossier de réplication indépendante — le Blob canonique », version 1.0, 4 juillet 2026 (master V277, p. 1127 à 1131). Le vecteur de référence et ses tolérances sont ceux du dossier ; je ne les choisis pas.

**Protocole gelé.** N = 2 000 ; graines 3401 et 3402 ; 40 balayages puis mesure, 8 balayages de plus puis mesure ; la mesure à 48 balayages fait foi.

**Critère du dossier.** Réussite si les huit grandeurs sont dans les tolérances et si la stratification de la multiplicité par bande de densité est dans l'ordre croissant.

| Grandeur | Référence (2 graines) | Tolérance |
|---|---|---|
| triangles par point | 4,96 à 5,09 | ±10 % |
| transitivité | 0,433 à 0,435 | ±10 % |
| dispersion des degrés | 0,85 à 0,88 | ±12 % |
| tétraèdres par point | 10,9 à 11,8 | ±15 % |
| multiplicité triangle → tétraèdre | 8,8 à 9,3 | ±15 % |
| fraction « dans un tétraèdre » | 0,25 à 0,26 | ±0,04 |
| fraction « triangle sans tétraèdre » | 0,42 à 0,44 | ±0,05 |
| fraction « arête seule » | 0,31 à 0,33 | ±0,05 |
| stratification | 0,1 à 0,2 ; 1,0 ; 5 ; 11 à 14 | ordre croissant |

**Prédiction du pilote.** Six grandeurs sur huit au moins dans les tolérances sur chaque graine, et l'ordre de la stratification reproduit. Grandeurs que je juge les plus exposées : les tétraèdres par point et la multiplicité (queue lourde des cliques), et la dispersion des degrés. Points de la spécification que j'ai dû interpréter, déclarés ici : écart-type de population pour la dispersion ; « reste connexe » compris comme « les deux extrémités restent reliées » ; multiplicité moyenne calculée comme 4 × tétraèdres / triangles.

**Ce qui me donnerait tort.** Moins de six grandeurs sur huit, ou la stratification dans le désordre. Un échec sera publié tel quel, avec les deux vecteurs.

## R2 — Témoin de définition pour le couplage courbure-matière

**Source.** Tome de campagne V277, Partie R (17 juillet 2026) : corrélation entre le déficit angulaire |δ_e| des arêtes portant au moins deux tétraèdres et la densité locale de tétraèdres, 0,675 ± 0,032 à N = 6 000, contre −0,29 sur graphe non équilibré.

**Hypothèse du pilote.** |δ_e| vaut, par définition, |2π − somme des angles dièdres des tétraèdres contenant e|. Dans un graphe où les cliques se recouvrent, cette somme croît avec leur nombre m_e. La corrélation mesurée serait donc portée, pour l'essentiel, par m_e lui-même.

**Protocole gelé.** Cadre de la Partie M : tore, densité 200, κ = 10, portée 1,6 × rayon, 5 N arêtes, S = log(1 + T) − β·CV, poids exp((N/τ)·S), τ = 0,5, β = 2, 30 balayages, départ d'un tirage uniforme de 5 N arêtes de la réserve (qui sert aussi de témoin non équilibré). N = 6 000 ; graines 3411 et 3412. Densité « aux sommets » : moyenne du nombre de tétraèdres aux deux extrémités ; densité « externe » : la même, privée des tétraèdres qui contiennent l'arête.

**Prédictions.**
1. À l'équilibre, corrélation entre |δ_e| et m_e supérieure ou égale à 0,85.
2. À l'équilibre, corrélation entre |δ_e| et la densité aux sommets entre 0,55 et 0,80 (le 0,675 du tome, à ±0,12).
3. À l'équilibre, corrélation partielle entre |δ_e| et la densité aux sommets, m_e étant fixé : inférieure à 0,25 en valeur absolue.
4. Sur le tirage non équilibré, corrélation entre |δ_e| et la densité aux sommets négative.

**Ce qui me donnerait tort.** Une corrélation partielle supérieure à 0,5 (prédiction 3) : le couplage ne serait alors pas un effet de définition, et je le graverai ainsi. Si la prédiction 2 échoue, mon modèle ne reproduit pas la mesure du tome et le témoin n'est pas concluant.

**Limite déclarée.** La définition exacte de la « densité locale de tétraèdres » du tome n'est pas donnée dans le texte lu ; j'en teste deux. Je ne suis pas un tiers indépendant : ceci est un contre-audit interne, pas la validation externe que le corpus attend.
