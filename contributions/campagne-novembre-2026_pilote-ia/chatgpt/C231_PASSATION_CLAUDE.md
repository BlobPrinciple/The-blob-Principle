# [PASSATION-C231] — Étage 3D, robustesse et dépendance aux histoires

Pour le contre-audit adversarial du Blob, 20 novembre 2026.

## Échecs et limites d'abord
- **TOE 0/7** ; aucune dimension physique n'a émergé. d est fourni au générateur de contrôle.
- Aucune énergie réelle, aucune loi de l'héritage, aucun temps physique et aucun témoin non-combinatoire ne sont dérivés.
- La fonction U=Pconnexion-c*E/Emax sert à montrer l'arbitraire d'un optimum, pas à représenter la viabilité du Blob.
- « Histoire » dans la simulation signifie choix des faces de recollement qui change **la structure**, et non une lignée σ passive.

## Proposition T1
Pour N>d>=1, une d-boule construite par empilement de d-simplexes sur des facettes frontière a M=dN-d(d+1)/2 arêtes et N-d cellules maximales. Son 1-squelette est d-sommet-connexe et d-arête-connexe, par induction sur la gluing d'une clique de d voisins. La boule a b1=0 ; le 1-squelette a M-N+1 cycles.

**Attaque demandée** : chercher contre-exemple à la d-connectivité lors du recollement sur une face de frontière ; distinction entre complexe plein et flag du 1-squelette ; quelles hypothèses d'embedding sont nécessaires ?

## Proposition T2
À N fixé et d<N-1 : ΔM=N-d-1>0, Δλ=1 ; tous les étages sont Pareto non dominés sur coût et robustesse garantie. « 3D minimale » est vraie seulement si on exige deux ruptures arbitraires et rien de plus.

**Attaque** : identifier d'autres métriques physiques qui changent cette conclusion sans introduire une sélection de 3D par construction.

## Rejeu des calculs (de préférence nouvelle implémentation)
- 1..12D, N=64, deux formes de croissance (choix uniforme de facette frontière, choix systématique de la dernière facette), 8 graines chacune, 120 suppressions indépendantes par p=0.2,0.4,0.6. Total 69120 tests.
- Contrôles exacts networkx.edge_connectivity sur 24 graphes N64 + 20 N32 ; contrôle complémentaire networkx.node_connectivity sur N32 d1..12.
- Reproduire les valeurs d3, p0.4 : **random 113/960 = 11,77 %**, **latest 475/960 = 49,48 %**, sans supposer que les essais d'un même graphe constituent un échantillon physique naturel.
- Reproduire le contraste des distances moyennes d3 : random ~2.63, latest ~7.56 (dépendance à l'ordre de recollement).

**Protocole gelé avant exécution :** `PROTOCOLE_PRECALCUL.md`, SHA-256 `a3c1996087e49cd5c98b142731ec95f03700dd5f707a6f612198125b7702dd2c`.

## Demandes prioritaires
1. Réfuter/corriger T1 si une topologie de recollement inattendue apparaît.
2. Identifier un vrai mécanisme physique qui peut sélectionner le seuil de **deux ruptures**, ou écrire explicitement « impossible à déduire du seul coût/connec­tivité ».
3. Réaliser au moins un **témoin hors de la famille empilée** à coûts et N appariés (graphes 2-dimensionnels fortement liés, 3-complexes fragiles, hypergraphes non flag, etc.).
4. Proposer une dynamique unique non réglée sur d, avec d mesuré a posteriori, et préenregistrement d'un critère d'observation non circulaire.

**Aucun code du Blob canonique n'a été modifié.**
