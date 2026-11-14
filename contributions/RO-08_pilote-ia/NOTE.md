🇫🇷 Français · 🇬🇧 [English version](NOTE_EN.md)

# RO-08 — Le graphe du Blob ne peut être le 1-squelette d'aucune 3-variété fermée connexe

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Note du pilote IA du laboratoire (Claude, Anthropic), session planifiée du 13 novembre 2026, par délégation de Rudolphe Mirante. Non relue par une personne. Premier travail du laboratoire sur le pont RO-08.

## Objet

RO-08 (armature V347.1, II.0, p. 11) demande d'envoyer le régime Ω³ de la couche historique A_Gibbs sur une triangulation fermée de topologie contrôlée, ou de montrer que B est un secteur typique ou limite de A_Gibbs ; falsificateur : « les configurations Ω³ typiques ne forment pas de 3-variétés fermées, ou leur topologie n'est pas contrôlable ».

Ce que le corpus a déjà établi, et que cette note ne refait pas :
- le **complexe de cliques** du Blob n'est pas une 3-pseudovariété (V346, CXL.2.4, Proposition 2, p. 1195 imprimée, PDF 1243 : multiplicité moyenne des 2-faces ≈ 9–10, 3,6 à 5 % des faces à exactement 2) ;
- le sous-complexe **Delaunay ∩ Blob** est de type variété mais ne percole pas (V346, AD.1–AD.2, tome V279, et CXL.3 : 2,5–2,6 % des tétraèdres, couverture 13–15 % des sommets).

Question restée ouverte : en **gardant les sommets et les arêtes** du Blob et en choisissant **librement** les triangles et les tétraèdres (pas forcément les cliques), peut-on obtenir une triangulation fermée ? C'est la voie la plus économe vers B : elle ne change ni la population ni les liaisons.

## Résultat en bref

1. **[T] Non, pour toute configuration, au degré moyen canonique.** Le moteur A_Gibbs fixe |E| = round(κN/2) avec κ = 6,6 (armature, tableau des paramètres, κ₀ ; `blob engine.py`, `KAPPA = 6.6`). Or toute triangulation simpliciale d'une 3-variété fermée connexe vérifie f₁ ≥ 4f₀ − 10 (théorème de la borne inférieure de Walkup, 1970), soit un degré moyen ≥ 8 − 20/N. Le moteur prend |E| = round(3,3·N) et l'échange d'arêtes conserve |E| ; f₁ < 4f₀ − 10 dès N ≥ 16 (à N = 14 et 15, égalité par l'arrondi). Aucune configuration de A_Gibbs à N ≥ 16 n'est le 1-squelette d'une 3-variété fermée connexe, quelles que soient les faces choisies et l'état de la chaîne (pour k composantes, la borne devient f₁ ≥ 4f₀ − 10k ; les configurations mesurées ici sont connexes, mais le moteur ne le garantit pas). Pour T³ en particulier, la borne est plus forte : f₁ ≥ 4f₀ − 10 + 10·β₁ = 4f₀ + 20 (Novik–Swartz, Adv. Math. 222 (2009) 2059–2084, pour M orientable sur le corps choisi ; rappelée par Lutz–Sulanke–Swartz 2009), degré moyen ≥ 8 + 40/N.
2. **[M] Localement, le Blob est plus loin de B que le témoin sans viabilité.** Trois conditions locales nécessaires (ci-dessous), testées sur le moteur canonique (N = 500 à 4 000, 4 graines) : 96 à 97,5 % des sommets en violent au moins une selon N (92 % pour le graphe géométrique sans viabilité, 100 % pour Erdős–Rényi), 65 % des arêtes ont moins de 3 voisins communs (40 % sans viabilité). Dans le cœur du cube (loin des faces), 96 % des sommets du Blob violent une condition. Le déficit local (somme de max(0, 3d − 6 − t)) vaut 6,1 par sommet pour le Blob contre 3,6 sans viabilité. La condition de link (C2) seule n'est pas plus violée par le Blob (0,776) que sans viabilité (0,781) : l'écart vient de C1, de C3 et du déficit.
3. **[M] Le paradoxe de l'aristocratie.** Le Blob franchit le seuil global nécessaire n_tri/N ≥ κ − 2 = 4,6 (5,0 à 5,4 en moyenne par N ; 4,82 à 6,04 par configuration), que le témoin sans viabilité ne franchit pas (3,6 à 3,9). Mais il concentre les triangles : 31 % de ses sommets n'en portent aucun, 27 % ont un degré < 4 ; seul le décile le plus massif (137 triangles et degré 21 en moyenne) satisfait presque partout la condition de link (97,5 %), et 76 % de ses sommets restent en violation, pour au moins 74 % par la condition d'arête (C3), sur leurs liens vers les sommets pauvres. La viabilité crée assez de triangles en tout, mais les place à l'opposé de ce qu'exige une variété, où chaque sommet porte exactement 3d − 6 faces triangulaires.

**Verdict.** Le pont RO-08 ne peut pas être une simple « mise en faces » du graphe de A_Gibbs : il doit changer les arêtes (en ajouter au moins 0,7·N − 10 pour la borne de Walkup, au moins 0,7·N + 20 pour T³), ou les sommets (gros-grain), ou passer par une autre construction. Le falsificateur de RO-08 est atteint **pour cette voie seule** ; RO-08 reste ouvert pour les autres. Aucun changement de statut.

## Conditions nécessaires utilisées

Soit G = (V, E) le 1-squelette d'une triangulation simpliciale K (complexe simplicial, non un Δ-complexe) d'une 3-variété fermée, d_v le degré de v, t_v le nombre d'arêtes de G entre voisins de v (triangles de G en v), c_uv le nombre de voisins communs de u et v.

- **(C1) d_v ≥ 4 [T].** Le link de v est une 2-sphère triangulée, qui a au moins 4 sommets.
- **(C2) t_v ≥ 3d_v − 6 [T].** Les sommets du link de v sont exactement les voisins de v (toute arête vw de K donne le sommet w du link, et réciproquement). Une 2-sphère triangulée à d sommets a 3d − 6 arêtes (Euler) ; chaque arête ab du link est une arête de K entre voisins de v. Donc G[N(v)] a au moins 3d_v − 6 arêtes. Pour une triangulation de drapeau (faces = cliques), c'est une égalité, avec d_v ≥ 6.
- **(C3) c_uv ≥ 3 [T].** Le link de l'arête uv est un cercle triangulé (au moins 3 sommets), dont les sommets sont des voisins communs de u et v.
- **(Glob) n_tri/N ≥ κ − 2 [T].** Somme de (C2) sur v : 3·n_tri ≥ 6|E| − 6N.
- **(W) f₁ ≥ 4f₀ − 10 [T, cité].** D. W. Walkup, « The lower bound conjecture for 3- and 4-manifolds », *Acta Mathematica* 125 (1970), 75–107. Énoncée pour M connexe. Borne pour T³ : f₁ − 4f₀ + 10 ≥ 10·β₁ (I. Novik, E. Swartz, « Socles of Buchsbaum modules, complexes and posets », Adv. Math. 222 (2009) 2059–2084, M orientable sur le corps choisi), rappelée dans F. H. Lutz, T. Sulanke, E. Swartz, « f-vectors of 3-manifolds », *Electron. J. Combin.* 16(2) (2009), R13 ; β₁(T³) = 3. (W) seule suffit au point 1 ; la borne T³ n'est qu'un renforcement.

(C1) à (C3) et (W) sont indépendantes (un graphe peut vérifier (W) et avoir un sommet de degré 3) ; à κ = 6,6, (W) suffit, et (C1) à (C3) disent **où** le graphe échoue.

## Mesures

`ro08_squelette.py` (ensembles Python) et `ro08_second_moteur.py` (matrices creuses : t_v = (A³)_vv/2, c_uv = (A²)_uv) ; moteur `corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py` importé tel quel (κ 6,6 ; β 0,30 ; τ 0,50 ; pool_fac 1,6 ; therm_fac 120). Écart maximal entre les deux implémentations : 0 sur cinq quantités (sommets en violation, C2, arêtes C3, n_tri/N, déficit), 32 configurations ; la relecture hostile a recalculé de son côté (networkx) N = 1 000 graine 0 et N = 4 000 graine 1, à l'identique. |E| = 3,3·N exactement dans les 32 configurations.

**Contrôle positif** : germe de Freudenthal–Kuhn de T³ (L = 4 et 5, degré 14) : zéro violation, n_tri/N = 12 = κ − 2 exactement, égalité de drapeau partout.

| modèle | N | sommets en violation | C1 (d < 4) | C2 | arêtes C3 (c < 3) | n_tri/N (seuil 4,6) | déficit C2 / N |
|---|---|---|---|---|---|---|---|
| Blob | 500 | 0,963 ± 0,009 | 0,302 | 0,737 | 0,608 | 5,29 | 5,46 |
| Blob | 1 000 | 0,972 ± 0,006 | 0,277 | 0,772 | 0,640 | 5,38 | 6,01 |
| Blob | 2 000 | 0,975 ± 0,002 | 0,274 | 0,772 | 0,645 | 5,04 | 6,04 |
| Blob | 4 000 | 0,975 ± 0,003 | 0,273 | 0,776 | 0,649 | 5,23 | 6,11 |
| sans viabilité (RGG) | 4 000 | 0,920 ± 0,004 | 0,127 | 0,781 | 0,397 | 3,60 | 3,59 |
| Erdős–Rényi (|E| à 0,1 % près, doublons) | 4 000 | 1,000 | 0,105 | 0,959 | 1,000 | 0,01 | 13,79 |

(moyennes sur 4 graines, écart-type entre graines.) Cœur du cube (sommets à plus de 2r des faces, 1 401 sommets à N = 4 000) : 0,963 pour le Blob, 0,919 sans viabilité. Relaxation quatre fois plus longue (N = 1 000, 2 graines) : 0,966 et 0,968, inchangé.

Ventilation par décile de masse triangulaire, Blob, N = 4 000 (déciles par rang, 4 graines) :

| décile | masse moyenne | degré moyen | C1 | C2 | en violation |
|---|---|---|---|---|---|
| 0–2 | 0 | 3,3 | 0,61–0,65 | 0,68–0,69 | 1,000 |
| 5 | 1,6 | 5,1 | 0,144 | 0,968 | 1,000 |
| 8 | 9,7 | 8,8 | 0 | 0,938 | 0,988 |
| 9 | 137,6 | 21,4 | 0 | 0,025 | 0,764 |

## Limites

- Le point 1 porte sur le moteur canonique (κ = 6,6 imposé). Une variante de A_Gibbs à κ ≥ 8 échapperait à (W) ; elle échapperait peut-être aussi aux conditions locales, ce qui n'est pas testé ici. [OPEN]
- Le moteur vit dans un cube à bord (V346, CXL.8) ; une triangulation fermée n'en a pas. Le cœur du cube donne les mêmes chiffres, et (W) ne dépend pas du bord.
- Un pont par gros-grain (R-TRUE, blocs) ou par une construction qui ajoute des arêtes n'est pas exclu. La note dit seulement qu'il faut changer le graphe.
- La comparaison au témoin sans viabilité est à |E| égal mais pas à loi d'équilibre comparable (le RGG n'est pas relaxé).

## Question ouverte

Quel est le plus petit nombre de changements d'arêtes qui fait d'une configuration typique de A_Gibbs le 1-squelette d'une triangulation de T³, et ce coût par sommet tend-il vers une limite quand N croît ? Une mesure de Gibbs à κ ≥ 8 garde-t-elle l'aristocratie, qui est l'obstacle local mesuré ici ?

## Reproduire

```
pip install numba scipy
python3 contributions/RO-08_pilote-ia/ro08_squelette.py      # ≈ 1 min ; ro08_squelette.json
python3 contributions/RO-08_pilote-ia/ro08_second_moteur.py  # ≈ 1 min ; dernière ligne ACCORD
```
