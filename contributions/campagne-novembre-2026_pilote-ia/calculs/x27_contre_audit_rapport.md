# Contre-audit X-27 (code indépendant, arithmétique exacte)

## Écarts et erreurs trouvés

Aucune erreur de calcul. J'ai relevé trois imprécisions de formulation :

1. **E3** : (2,2,2,0,-1) est un côté libre de cellule dès la 1ʳᵉ naissance. En revanche, (2,2,2,-1,0) ne devient place admissible qu'après la 10ᵉ naissance, puis côté de cellule après la 11ᵉ. La formule « pendant ses 17 naissances » est donc fausse pour la seconde place.
2. **E2** : « l'ordre des naissances compte » est inexact. Les places admissibles ne dépendent que de l'ensemble des constituants. Ce qui compte, c'est quelles naissances ont eu lieu et lesquelles ont été omises, pas leur ordre.
3. **C (K20a)** : l'argument suppose que toute paire tangente de P est l'image de (e0, e1) par le groupe, c'est-à-dire qu'elle est contenue dans une grappe. Ce point n'est pas démontré dans le texte. Je l'ai seulement constaté sur 14 292 paires tangentes, sans exception. Le reste de l'argument est juste : deux centres du réseau à distance 2 de x sont distants de 2, 2√3 ou 4, et dans les trois cas x est un nœud du réseau.

## Tableau des contrôles

| Point | Verdict | Nombre ou raison |
|---|---|---|
| A1 | confirmé | 17/17 : norme 1 ; appartenance à P prouvée par mouvements de grappes ; aucun chevauchement ; exactement 4 contacts, tous tangents entre eux ; chaque naissance est retrouvée par mon solveur |
| A2 | confirmé | ⟨x',x'⟩ = 1 ; produit maximal sur les 22 constituants = −1 ; contacts : e0, e1, (5,3,5,−1,−1), (6,6,3,−2,0) ; rang 4 ; parent e0 (seul parent possible) ; 52 places au total, dont 1 seule hors de P (x'), aucune irrationnelle |
| A3 | confirmé | les s_j sont des matrices entières, donc P ⊂ Z⁵ ; les e_i forment une base, donc l'écriture de x' est unique ; dénominateur 7 |
| A4 | confirmé | réalisation : deux demi-espaces z<0 et z>2, puis isométrie. Les 20 boules sont bornées (b > 0), toutes dans la bande et disjointes deux à deux. x' : rayon 1, centre (−15/7, −3√3/7, 1), tangente aux deux plans, à (5,3,5,−1,−1) (r = 1/3) et à (6,6,3,−2,0). Plus petit écart non nul : 0,268. Aucun cas de « complément ». Ce contrôle n'est pas indépendant de la forme (c'est une isométrie), mais il tranche la question de l'orientation. |
| A5 | confirmé | ⟨x',y⟩ = 5/7 et −1/7, soit > −1 dans les deux cas : chevauchement. Les deux places sont dans P et admissibles. |
| A6 | confirmé | les 26 naissances sont valides, toutes dans une cellule. x = (8,8,7,−2,−2)/3 : norme 1, produit maximal −1, contacts e0, e1, (5,3,5,−1,−1), (14,12,8,−4,−1). Produits entre voisins : −5, −5, −17, donc non tangents. 77 places, 1 seule hors de P. |
| A7 | confirmé | aucune échappatoire. Le texte scellé dit « touche des voisins », pas « tous » ; la condition (4) est explicitée. Les naissances du contre-exemple satisfont même la condition plus forte « dans la cellule ». |
| B | confirmé (jusqu'au niveau 7 à symétrie près, niveau 4 sans réduction) | Sans réduction, niveaux 0 à 4 : 1/5/30/200/1 385 tissus et 5/40/330/2 760/22 955 places, toutes dans P. Le niveau 5 a été arrêté. À symétrie près : 1, 1, 2, 6, 23, 117, 704, 4 783 classes. Aucune place irrationnelle ni rationnelle non entière. Au niveau 7, 78 places entières ont échappé à ma table de P (borne trop basse) ; toutes les 78 sont prouvées dans P par descente dans le groupe. Je n'ai trouvé aucun contre-exemple à 7 naissances ou moins ; entre 8 et 16, rien n'a été cherché. |
| C (K18) | confirmé | la matrice de Gram 6×6 vaut 2I − J, de valeurs propres 2 et −4 : elle est inversible, donc de rang 6, impossible dans R⁵ |
| C (K20a) | confirmé, avec réserve | voir l'écart 3 |
| D | non tranché | Je n'ai trouvé aucune source qui énonce ce fait. Dans le modèle de la bande, c'est élémentaire : une sphère unité, hors réseau, dans une couche lacunaire. Il ne faut rien revendiquer de nouveau. Références consultées : [Kontorovich–Nakamura](https://arxiv.org/abs/1712.00147), [Soddy local-global](https://arxiv.org/abs/1208.5441). |
| E1 | établi | Il faut écrire « un tissu », pas « le tissu ». |
| E2 | trop fort | première moitié établie ; « l'ordre compte » est imprécis : c'est l'ensemble des naissances qui compte |
| E3 | trop fort | voir l'écart 1 |
| E4 | non contrôlé | règle de X-25 non réimplémentée |
| E5 | établi | confirmé jusqu'à 7 naissances. « Inconnu entre les deux » signifie de 8 à 17. |

## Non contrôlé

- E4.
- Le niveau 5 sans réduction (9 876 tissus) : arrêté sur demande.
- Une recherche de contre-exemple entre 8 et 16 naissances.
- Une démonstration de la transitivité sur les paires tangentes (point C).

Code : `core.py`, `check_A.py`, `check_A4_A6.py`, `check_E3_C.py`, `enum_B.py`, `descent.py`. Sorties : `full.out`, `sym.out`.
