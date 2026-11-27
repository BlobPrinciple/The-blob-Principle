# X-29 et X-29 bis — Le pliage vers le germe, puis le plancher : ce qui tient un tissu dans l'empilement

**Rédigé par Claude, pilote IA et contre-auditeur.** Auteur du Blob Principle : Rudolphe Mirante. La cosmogonie lui appartient.

TOE 0/7. Aucun verrou fermé.

**Parole de l'auteur** (27 novembre, 7 h 08, heure de Paris) : « Dépose et pousse à l’extrême ensuite toutes les recherches. »

Deux prédictions scellées avant tout calcul. X-29 : `calculs/x29_pliage_prediction.txt`, SHA-256 `725060cde2ef5095118630475f8bedfb01028822dff5f66b80753b3ee050041a`, poussée sur la branche à 7 h 29 UTC (commit d3c1008). X-29 bis : `calculs/x29bis_plancher_prediction.txt`, SHA-256 `99ee80f122255db7327a7de8cb418567c9c096c1022785b0c933a10458ac6c38`, poussée à 7 h 46 UTC (commit 19ddb75).

## 296. Ce qui est faux, manque ou reste ouvert, d'abord

1. **Aucun verrou ne bouge.** Tout ce carnet est de la géométrie de la lecture de contact, rang 3.
2. **La règle à la lettre n'est toujours pas démontrée à tout palier.** Ce carnet la ramène à un énoncé sur l'empilement seul, (G), section 307 : vérifié sur 973 778 boules, non démontré. La voie proposée dans X-28 était tombée au palier 6 ; celle-ci tient jusqu'ici, ce qui ne prouve rien.
3. **Un énoncé annoncé était trop fort.** J'avais scellé T11 comme une équivalence entre (C*) et (G). Seul un sens est exact tel quel : (G) entraîne (C*). Dans l'autre sens il faut ajouter le germe aux ancêtres (section 305).
4. **Le pliage était la mauvaise frontière.** La conjecture (C) de X-29 a tenu, mais des tissus qui ne sont pas clos par pliage restent aussi dans l'empilement (clauses Q4, Q6). D'où X-29 bis et une condition plus faible, le plancher.
5. **Un programme a planté.** Le premier lancement de la clause R2 s'est arrêté sur une erreur d'indice (quadruple sans ancêtre), avant tout résultat. Corrigé, relancé.
6. **Mes confiances étaient mal réglées.** J'avais donné 50 % aux clauses Q3 (b) et (c) et 35 % à R4 (b), en craignant une place de l'empilement sans cellule née. Elle ne s'est pas montrée une seule fois, sur 212 551 places. Je n'ai pas de preuve qu'elle ne peut pas exister.
7. **L'épreuve scellée de Q3 portait sur de petits tissus** : la clause écartait les tirages de plus de 350 constituants, 83 sur 200. Je les ai calculés ensuite, hors scellé (section 301).
8. **(G) n'est contrôlé que sur des quadruples nés avant le palier 5.** Rien n'est contrôlé pour des constituants profonds, sinon à travers les tissus tirés.
9. **T8, T9 et T10 reposent sur des faits classiques que je n'ai pas redémontrés** (section 298). Aucun énoncé de ce carnet n'est contrôlé par Lean.
10. **Non fait** : une preuve de (G) ; le plus petit contre-exemple à K20 (toujours entre 9 et 17 naissances) ; le palier 7.
11. **Clauses chiffrées** : les six de X-29 et les cinq de X-29 bis sont vraies (sections 300 et 306). Aucune exception à T6, T7 ni T10 dans les données.

## 297. Vocabulaire

Celui de X-27 et X-28, plus ceci.

- **Mur de l'empilement** : la sphère orthogonale aux quatre constituants d'une cellule de l'empilement. Sa normale est n = t − t′, différence des deux côtés de la cellule ; ⟨n, n⟩ = 12. L'image d'un vecteur v dans le mur est v − ⟨v, n⟩ n/6.
- **Côté du germe** d'un mur : celui où se trouve la tuile du germe. Un constituant est **au-delà** du mur s'il est strictement de l'autre côté.
- **Pliage** : un constituant au-delà d'un mur est remplacé par son image dans ce mur ; les autres ne bougent pas.
- **Tissu clos par pliage** : tout constituant né est dans une tuile née, et pour tout mur et tout constituant né u au-delà de ce mur, l'image de u est née.
- **Tuile-porte** d'un constituant u de l'empilement : parmi les tuiles qui contiennent u, la plus proche du germe. **Plancher** de u : les quatre autres constituants de sa tuile-porte.
- **Règle à la lettre**, énoncé retenu : S(0) est le germe ; S(n+1) est S(n) plus tous les côtés non nés des cellules de S(n). Le **palier** de u est le premier n tel que u est dans S(n).

## 298. Faits admis, faits démontrés ailleurs

- (C1), (C2), (C3), admis, et (C4), démontré : ceux de X-28, section 286. En particulier un mur ne coupe aucune tuile ; un constituant est sur un mur ou strictement d'un côté ; des constituants tous liés sont dans une même tuile.
- (C2 bis), admis. Les murs qui séparent une tuile du germe sont ceux que traverse un plus court chemin de cette tuile au germe.
- (C3 bis), admis. La tuile-porte de u est la seule tuile contenant u qu'aucun mur passant par u ne sépare du germe.
- (C5), admis. L'ordre de Bruhat sur les éléments du groupe, donc sur les tuiles, est engendré par : T′ < T si T′ est l'image de T dans un mur qui sépare T du germe (Björner et Brenti, *Combinatorics of Coxeter groups*, chapitre 2, cité de mémoire).

## 299. Ce qui est démontré

**T6 (pliage, tous les murs). [T]** Sous la règle à la lettre, à tout palier, le tissu est clos par pliage. L'image d'un constituant né au-delà d'un mur est née au même palier, ou avant.

Preuve, par récurrence sur le palier k de u. Un constituant du germe n'est au-delà d'aucun mur. Si k ≥ 1, u est un côté non né d'une cellule C de S(k−1), et C ∪ {u} est une tuile (C4). Un mur ne coupe aucune tuile : si u est au-delà du mur, chaque membre de C est sur le mur ou au-delà. Son image est dans S(k−1) : lui-même s'il est sur le mur, sinon par récurrence. L'image de C est donc une cellule de S(k−1), et l'image de u est un de ses côtés : elle est dans S(k−1), ou bien c'est un côté non né d'une cellule de S(k−1), donc elle est dans S(k).

X-28 n'énonçait le pliage que pour les murs de surface.

**T7 (le palier se lit sur le plancher). [T]** Sous la règle à la lettre, pour u hors du germe : palier(u) = 1 + le plus grand palier des quatre constituants du plancher de u.

Preuve. Soit m le plus grand palier du plancher. Le plancher est une cellule de S(m) dont u est un côté : palier(u) ≤ m + 1. Dans l'autre sens, soit k le palier de u : u est un côté d'une cellule C de S(k−1). Allons de la tuile C ∪ {u} à la tuile-porte de u par un plus court chemin de tuiles contenant u (C3). Chaque mur traversé passe par u et sépare la tuile de départ de la tuile-porte ; aucun mur passant par u ne sépare la tuile-porte du germe (C3 bis) ; ce mur sépare donc du germe la tuile que l'on quitte. À chaque pas, les quatre constituants autres que u sont sur le mur ou au-delà, et T6 dit que leurs images sont nées au même palier ou avant. À l'arrivée, le plancher est dans S(k−1) : m ≤ k − 1.

Conséquence : le palier de naissance d'un constituant ne dépend que de sa place dans l'empilement. Il se calcule de proche en proche à partir du germe, sans dérouler l'histoire.

**T8 (ordre de Bruhat). [T, sous C5]** Un tissu est clos par pliage si et seulement si ses tuiles nées forment une partie commençante de l'ordre de Bruhat : avec une tuile, toutes celles qui sont au-dessous d'elle.

Preuve. Si le tissu est clos et si un mur sépare une tuile née T du germe, chaque constituant de T est sur le mur ou au-delà, son image est née, donc l'image de T est une tuile née. Réciproquement, un constituant né u au-delà d'un mur est dans une tuile née, que ce mur sépare du germe ; l'image de cette tuile est née, donc celle de u. (C5) traduit.

**T9 (critère de la cellule). [T]** Dans un tissu clos par pliage, un constituant x de l'empilement qui n'est pas né est le côté d'une cellule née si et seulement si son plancher est né.

Preuve. Si le plancher est né, c'est une cellule née dont x est un côté. Réciproquement, si x est le côté d'une cellule née C, on va de C ∪ {x} à la tuile-porte de x comme dans la preuve de T7 ; à chaque pas les quatre constituants autres que x restent nés.

## 300. Les six clauses chiffrées

| Clause | Prédit | Obtenu | Verdict |
|---|---|---|---|
| Q1 (a), pliage, tous les murs, paliers 0 à 6 | zéro exception | 203 925 triplets (tuile née, mur, constituant au-delà) au palier 6 ; aucune image non née, à aucun palier | vraie |
| Q1 (b), formule de T7 | vraie pour les 7 285 constituants hors germe du palier 6 | vraie pour les 7 285 ; chacun a une tuile-porte née et une seule | vraie |
| Q2, tissus de X-27 | pas clos par pliage | tissu de 22 : 78 images non nées sur 151 triplets (26 distinctes) ; tissu du toit, 31 constituants : 215 sur 348 (63 distinctes) | vraie |
| Q3, 200 tissus clos par pliage tirés au hasard | (a) zéro place hors de l'empilement ; (b) zéro place sans cellule ; (c) places = côtés libres | 117 tissus gardés, 83 écartés ; 35 534 places admissibles ; (a) 0 ; (b) 0 ; (c) égalité dans les 117 | vraies toutes trois |
| Q4, les mêmes plus la moitié de leurs côtés libres | zéro place hors de l'empilement | 88 994 places ; 0 hors de l'empilement ; aucun des 117 tissus n'est plus clos par pliage | vraie |
| Q5, clôture par pliage du tissu de 22 | la place hors de l'empilement n'y est plus admissible ; toutes les places dans l'empilement | 51 constituants (29 ajoutés en 2 tours), 68 tuiles nées ; la place n'est plus admissible ; sa jumelle (2, 2, 2, −1, 0) est née ; 155 places, toutes côtés libres, toutes dans l'empilement | vraie |
| Q6, six tissus incomplets de X-28 | aucun n'est clos par pliage | images non nées : 326, 521, 449, 296, 516, 421 | vraie |

Détail de Q1, la règle à la lettre palier par palier :

| Palier | Constituants | Tuiles nées | Triplets contrôlés | Images non nées | Constituants où T7 est contrôlée | Plus longue tuile née |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 5 | 1 | 0 | 0 | 0 | 0 |
| 1 | 10 | 6 | 5 | 0 | 5 | 1 |
| 2 | 30 | 36 | 105 | 0 | 25 | 3 |
| 3 | 120 | 156 | 915 | 0 | 115 | 4 |
| 4 | 450 | 636 | 6 165 | 0 | 445 | 6 |
| 5 | 1 800 | 2 616 | 37 425 | 0 | 1 795 | 7 |
| 6 | 7 290 | 10 536 | 203 925 | 0 | 7 285 | 9 |

La longueur d'une tuile est le nombre de murs qui la séparent du germe. Au palier 6 le tissu contient les tuiles de longueur 0 à 9, par longueur : 1, 5, 20, 70, 240, 810, 2 730, 4 320, 2 250, 90.

Détail de Q2. Le tissu de X-27 contient (2, 2, 0, −1, 2) mais pas son image (1, 1, −1, 1, 1) dans le mur de normale (1, 1, 1, −2, 1). Or (1, 1, −1, 1, 1) est un voisin immédiat du germe, l'un des cinq premiers nés de la règle à la lettre. Le tissu de X-27 est allé loin en laissant vide ce qui est près.

Détail de Q3. Chaque tissu est la réunion de un à trois intervalles de Bruhat [germe, w], w de longueur 3 à 12. Dans les 117 tissus, le contrôle du pliage sur toutes les tuiles nées ne trouve aucune image manquante ; dans 42 d'entre eux les tuiles nées sont plus nombreuses que celles des intervalles tirés. Aucune cellule née n'y est sans côté né.

## 301. Ajouts non scellés

**Le programme suit l'énoncé. [M]** T6 et T7 portent sur l'énoncé mathématique de la règle ; les tissus calculés viennent du programme de X-25. Aux paliers 0 à 5, les naissances du palier suivant sont exactement les côtés non nés des cellules des tuiles nées : 5, 20, 90, 330, 1 350, 5 490, mêmes ensembles (`x29_regle_6.out`).

**Les tirages écartés. [M]** Les 83 tissus que Q3 écartait ont de 359 à 1 962 constituants, 702 en médiane. Ils offrent 164 988 places admissibles : aucune hors de l'empilement, aucune sans cellule, et dans les 83 les places sont exactement les côtés libres. Avec les 117 de Q3 : 200 tissus clos par pliage, 200 522 places, aucune hors de l'empilement.

## 302. La conjecture

**(C) [H]** Dans un tissu clos par pliage, les places admissibles sont exactement les côtés non nés des cellules nées. En particulier aucune n'est hors de l'empilement.

Par T9, ces côtés sont les constituants non nés dont le plancher est né.

Ce que (C) donnerait. Avec T6, la règle à la lettre garderait le tissu dans l'empilement à tout palier : c'est la question ouverte depuis X-27. Plus largement, toute règle de naissance qui garde le tissu clos par pliage y resterait.

Ce qui l'appuie : les paliers 0 à 6 de la règle à la lettre (X-28), les 200 tissus tirés (Q3 et section 301), la clôture du contre-exemple de X-27 (Q5). Ce qui manque : une preuve.

Ce que (C) ne dit pas. Le pliage n'est pas nécessaire : les six tissus incomplets de X-28 et les 117 tissus de Q4 ne sont pas clos par pliage et n'offrent pourtant aucune place hors de l'empilement. C'est ce qui a conduit à X-29 bis.

## 303. Ce que cela dit du contre-exemple de X-27

X-28 disait : entre deux contacts non liés de sa place hors de l'empilement, vu du parent, le tissu a un creux. X-29 dit où est le creux, vu du germe : il manque au tissu de X-27 vingt-six images par pliage, dont un voisin immédiat du germe. Quand on les lui rend — vingt-neuf constituants en tout, clôture comprise —, la jumelle (2, 2, 2, −1, 0) naît, la place hors de l'empilement disparaît, et les 155 places qui restent sont des côtés de cellule.

La règle où toutes les cellules enfantent ensemble ne laisse jamais ce genre de creux (T6). C'est un énoncé de géométrie. Il ne dit pas quelle règle de naissance est celle du Blob : c'est la parole de l'auteur.

## 304. X-29 bis : nul ne naît avant son plancher

Le plancher d'un constituant u, ce sont les quatre sphères de l'interstice où u est inscrit dans la construction classique de l'empilement : ses quatre parents au sens d'Apollonius. Les **ancêtres** de u sont son plancher, le plancher de son plancher, et ainsi de suite jusqu'au germe. Un tissu est **clos par plancher** s'il contient le germe et si tout constituant né a son plancher né.

## 305. Ce qui est démontré (X-29 bis)

**T10. [T]** Un tissu clos par pliage est clos par plancher. Le tissu de la règle à la lettre l'est à tout palier ; il le reste si l'on n'y ajoute qu'une partie des naissances du palier suivant ; un tissu clos par pliage le reste si on lui ajoute une partie quelconque de ses côtés libres.

Preuve. Dans un tissu clos par pliage, un constituant né u est dans une tuile née ; on va de cette tuile à la tuile-porte de u comme dans la preuve de T7, et les quatre autres constituants restent nés : le plancher est né. Pour la règle à la lettre, T7 suffit : le plancher de u est né avant u. Un côté libre d'une cellule née d'un tissu clos par pliage a son plancher né (T9).

**T11. [T]** (G) entraîne (C*).

- **(C*)** Dans tout tissu clos par plancher, toute place admissible est dans l'empilement.
- **(G)** Toute boule ronde hors de l'empilement, liée à un constituant p et à trois voisins q, r, s de p, les quatre indépendants, chevauche un ancêtre de p, q, r ou s.

Preuve. Soit x une place admissible d'un tissu clos par plancher, de contacts p, q, r, s. Si x était hors de l'empilement, elle chevaucherait un ancêtre de l'un des quatre (G) ; cet ancêtre est né : x ne serait pas admissible.

Dans l'autre sens : si une boule x hors de l'empilement, liée à p, q, r, s, ne chevauche aucun de leurs ancêtres ni aucun constituant du germe, alors le germe, les quatre et leurs ancêtres forment un tissu clos par plancher dont x est une place admissible, et (C*) est fausse. (C*) équivaut donc à (G) affaibli de « ou un constituant du germe ». J'avais scellé « équivalents » sans cette réserve.

(G) ne parle que de l'empilement : plus aucun tissu, plus aucune histoire.

## 306. Les cinq clauses chiffrées de X-29 bis

| Clause | Prédit | Obtenu | Verdict |
|---|---|---|---|
| R1, tissus de X-27 | pas clos par plancher ; la place hors de l'empilement chevauche un ancêtre d'un de ses contacts, et (2, 2, 2, −1, 0) en est un | tissu de 22 : 5 constituants nés sans leur plancher complet ; tissu du toit : 8. La place chevauche 2 des 10 ancêtres de ses contacts : (2, 2, 2, −1, 0) et (2, 2, 2, 0, −1), aucun des deux né | vraie |
| R2, (G) au palier 3, tous les parents | zéro exception | 148 320 quadruples, dont 27 180 sans boule ; 237 300 boules : 234 100 chevauchent un ancêtre ; les 3 200 autres sont dans l'empilement | vraie |
| R3, (G) au palier 4, parents à symétrie près | zéro exception | 10 parents ; 478 159 quadruples, dont 106 551 sans boule ; 736 478 boules : 735 054 chevauchent un ancêtre ; les 1 424 autres sont dans l'empilement | vraie |
| R4, 150 tissus clos par plancher tirés au hasard | (a) zéro place hors de l'empilement ; (b) zéro place sans cellule | 12 à 51 constituants, 29 en médiane ; aucun n'est clos par pliage ; 12 029 places ; (a) 0 ; (b) 0 ; places = côtés libres dans les 150 | vraies toutes deux |
| R5, six tissus incomplets de X-28 | clos par plancher | les six le sont | vraie |

Détail de R1. Dans le tissu de X-27, (4, 4, 2, −2, 1) est né sans son parent (2, 2, 2, −1, 0), et (4, 2, 4, 1, −2) sans son parent (2, 2, 2, 0, −1). La place hors de l'empilement chevauche précisément ces deux parents absents.

Le chevauchement est décidé par le test exact de l'outil de X-27 ; un filtre en nombres flottants ne sert qu'à écarter les cas à plus de 10⁻⁶ du contact.

## 307. L'énoncé qui reste à démontrer

**(G) [H]** Toute boule ronde hors de l'empilement, liée à un constituant et à trois de ses voisins, chevauche un ancêtre de l'un des quatre.

Ce que (G) donnerait, par T11 puis T10 : toute croissance où nul ne naît avant ses quatre parents reste dans l'empilement ; en particulier la règle à la lettre, à tout palier ; en particulier aussi les paliers incomplets et la file d'attente de X-28, que le pliage n'expliquait pas.

Ce qui l'appuie : 973 778 boules aux paliers 3 et 4, sans exception ; 150 tissus clos par plancher tirés au hasard ; tout ce qui appuie (C), qui en est un cas particulier ; le contre-exemple de X-27, qui viole exactement cette condition.

Dans les données, plus fort : les places admissibles d'un tissu clos par plancher sont exactement les côtés non nés de ses cellules nées (350 tissus sur 350, sections 300, 301 et 306). Je ne l'érige pas en énoncé.

Ce que (G) ne dit pas. La condition est suffisante, si (G) est vraie ; rien ne dit qu'elle soit nécessaire. Elle ne dit pas quelle règle de naissance est celle du Blob : c'est la parole de l'auteur.

## 308. Contre-audit indépendant

**En cours au moment de ce versement.** Un sous-agent indépendant relit les preuves de T6 à T11, refait Q1, Q2, Q5, R1 et R2 avec son propre code, et cherche à casser (C) et (G) sur des cas plus profonds que les miens. Tant que son rapport n'est pas versé, aucun résultat de ce carnet n'a été contrôlé par un autre que moi.

## 309. Ce que cela donne, et ce que cela ne donne pas

Cela donne trois théorèmes sur la règle à la lettre : son tissu est clos par pliage vers le germe à tout palier ; le palier de chaque constituant se lit sur son plancher ; nul n'y naît avant ses quatre parents. Cela donne un dictionnaire avec un objet classique, les parties commençantes de l'ordre de Bruhat. Cela donne surtout la question de X-27 réduite à un énoncé sur l'empilement seul, (G), que l'on peut attaquer sans plus parler de naissance.

Cela ne donne ni l'espace-temps, ni la gravitation, ni rien de quantique. Cela ne démontre pas la règle à la lettre.

Antériorité : non tranchée ; une recherche limitée est demandée au contre-auditeur. Le lien entre pliage et ordre de Bruhat (T8) est très probablement classique. Je ne dis d'aucun énoncé de ce carnet qu'il est nouveau.

## 310. Suite proposée

**X-30 : démontrer (G), ou la réfuter.** Chercher une exception parmi les quadruples profonds ; sinon démontrer (G) vu du parent, où les voisins sont les sphères de Ford des entiers d'Eisenstein (X-27 bis).

## 311. Fichiers

- `calculs/x29_pliage_prediction.txt`, `calculs/x29bis_plancher_prediction.txt` : prédictions scellées.
- `calculs/x29_pliage.py` : pliage, tuiles-portes, intervalles de Bruhat, clôture. Sorties : `x29_paliers_6.out` (Q1), `x29_x27.out` (Q2, Q5), `x29_hasard_1_100.out` et `x29_hasard_101_200.out` (Q3, Q4), `x29_partiel.out` (Q6), `x29_regle_6.out`, `x29_ecartes_1_100.out` et `x29_ecartes_101_200.out` (ajouts non scellés).
- `calculs/x29bis_plancher.py` : planchers, ancêtres, énoncé (G). Sorties : `x29bis_x27.out` (R1), `x29bis_G_3.out` (R2), `x29bis_G_4_sym.out` (R3), `x29bis_hasard_1_75.out` et `x29bis_hasard_76_150.out` (R4), `x29bis_partiel.out` (R5).
- `calculs/x29_contre_audit_rapport.md` : rapport du contre-audit, à verser tel quel dès réception.

Sources citées : Björner et Brenti, *Combinatorics of Coxeter groups* (Springer, 2005), de mémoire ; les sources de X-28.

TOE 0/7. Aucun verrou fermé.
