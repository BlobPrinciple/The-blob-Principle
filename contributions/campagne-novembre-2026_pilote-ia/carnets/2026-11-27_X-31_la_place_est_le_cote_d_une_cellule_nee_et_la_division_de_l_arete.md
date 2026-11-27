# X-31 — La place du nouveau-né est le côté d'une cellule née ; la division de l'arête, vue d'un fil

**Rédigé par Claude, pilote IA et contre-auditeur.** Auteur du Blob Principle : Rudolphe Mirante. La cosmogonie lui appartient.

TOE 0/7. Aucun verrou fermé.

**Parole de l'auteur** (27 novembre, 17 h 04, heure de Paris) : « Continue et reste sur la ligne précise de la cosmogonie et rien d'autre ! »

La ligne suivie est le point 1 de la section 5 du registre, « une seule réalisation de la mitose ». Il y restait, dans l'ordre : démontrer que la place du nouveau-né est le côté d'une cellule née ; puis le lien avec la division de l'arête, pas entamé.

Prédiction scellée avant tout calcul : `calculs/x31_cellule_et_arete_prediction.txt`, SHA-256 `d0bf1d158d4da3eff8195fd83a6ffad85fd31c15c9379684213e5768bf912efc`, poussée sur la branche à 16 h 22 UTC (commit 7f8c283).

## 334. Ce qui est faux, manque ou reste ouvert, d'abord

1. **La cosmogonie n'est pas démontrée.** Aucun verrou ne bouge. Le point 1 du registre n'est pas clos : une seule réalisation de la mitose n'est toujours pas tenue de bout en bout.
2. **Une clause scellée est fausse, et l'énoncé T25 que j'avais annoncé est faux dans sa formule.** J'avais prédit, pour les voisins communs de deux constituants du germe, 3, 6, 12, 21, 33, 48, 66 aux paliers 0 à 6. Le calcul donne 3, 6, 12, 21, 30, 42, 57. J'avais vérifié à la main les quatre premiers termes et prolongé la suite sans preuve. La conclusion tient (croissance quadratique, pas de doublement) ; la formule scellée, non. L'énoncé corrigé et sa preuve sont en section 337.
3. **Une seconde clause est fausse d'une unité.** J'avais écrit qu'un constituant du germe a 979 voisins au palier 6, en citant X-30 bis. Il en a 980 : le nombre de X-30 bis ne comptait pas le voisin envoyé à l'infini. Erreur de lecture de ma part.
4. **La clause B3 est vraie telle qu'écrite, mais sa borne venait de la formule fausse.** Le plus grand nombre de voisins communs au palier 6 est 57, non 66.
5. **Le lien avec la division de l'arête est entamé, pas clos.** Ce carnet dit où elle ressemble à la naissance dans la cellule et ce qui les sépare. Il ne les unifie pas. Sous la règle à la lettre, le rang 3 ne porte pas N = 2^g ; une autre règle est éprouvée en X-32.
6. **La condition « nul ne naît avant ses quatre parents » n'est pas automatique.** Dans 200 tissus tirés au hasard qui la respectent, 2 908 places admissibles sur 16 008 ont un parent qui n'est pas né. Les occuper romprait la condition. Une règle de naissance doit donc les interdire ; la règle à la lettre n'en offre jamais (T9, X-29).
7. **Tout repose sur des faits classiques admis**, ceux de X-30 bis, plus un pour T25 et un pour T24 (section 336). Le lemme T15 de X-30 bis porte la partie A ; il n'est pas devant Lean. **Rien de ce carnet n'est devant Lean. Aucun humain ne l'a lu.**
8. **Le contre-audit a trouvé quatre points faux ou troués dans mon premier jet** (section 341), tous dans la partie B. T23 disait « quatre cellules nouvelles » : c'est au moins quatre, sept ou dix quand la place touche plus de quatre constituants nés. T24 oubliait « à partir du palier 1 » dans une de ses phrases. Sa preuve employait au rang 2 un énoncé démontré seulement au rang 3. Et la section 340 disait plus que ce qui est démontré. Tout est corrigé ici. Il n'a rien trouvé de faux dans la partie A.
9. **Rien de nouveau n'est revendiqué.** T24 est la structure de Farey des cercles tangents à un cercle donné, classique. Antériorité non cherchée pour le reste.
10. **Non fait** : Lean ; le compte de la trame régulière ; le temps (point 2 du registre) ; tout travail sur un verrou.
11. **Clauses chiffrées** : neuf vraies sur onze (section 338). Fausses : B2, et B5 pour un de ses quatre nombres. L'énoncé T23, annoncé sans clause, était faux en général tel que scellé (point 8).

## 335. Vocabulaire

Celui de X-27 à X-30 bis, plus ceci.

- **Fil** : deux constituants liés. **Fils d'une cellule** : ses six paires. Deux fils d'une cellule sont **opposés** s'ils n'ont aucun constituant commun.
- **Parent, cousin.** Les parents de u sont les quatre autres constituants de sa tuile-porte. Deux constituants liés p et q sont **cousins** si aucun n'est parent de l'autre : c'est le troisième cas de T15 (X-30 bis). Ils ont alors trois parents communs a, b, c, et ferment ensemble l'anneau de six constituants liés à a, b et c.
- **Vue d'un fil (p, q)** : les constituants liés à p et à q, rangés en réseau triangulaire (X-30 bis, section 323).
- **Étendue** d'un triplet d'entiers : le plus grand moins le plus petit.

## 336. Faits admis

Ceux de X-30 bis, section 324 : (C1) à (C3 bis), leur emploi pour les tuiles contenant deux constituants liés, (C7). S'y ajoutent des résultats déjà au dossier : T15 et (C*) (X-30 bis, démontrés sous ces faits), T7 et T10 (X-29).

Deux faits classiques de plus, chacun pour un seul énoncé.

- **(C8), pour T25.** Si la tuile du germe contient p et q, et si l est lié à p et à q, la tuile-porte de l contient p et q. C'est la projection sur un résidu dans un groupe de Coxeter (Tits) : la tuile de l la plus proche d'une tuile de (p, q) est encore une tuile de (p, q).
- **(C9), pour T24.** Au rang 2, les tuiles (quatre disques tous liés) forment un arbre : de chaque tuile on passe à quatre voisines en retournant un disque, et aucun chemin ne se referme. Deux disques liés sont dans une même tuile, trois disques tous liés dans deux tuiles voisines exactement, et les tuiles qui contiennent un disque donné forment un sous-arbre. C'est la structure classique du groupe d'Apollonius.

## 337. Ce qui est démontré

### Partie A. La place est le côté d'une cellule née

**T20 (parent ou cousin). [T, sous les faits admis]** Dans un tissu clos par plancher, soit p un constituant né et x un constituant de l'empilement, non né, lié à p. Alors p est un parent de x, ou bien p et x sont cousins. Dans ce second cas, x est le côté non né de la cellule née {p, a, b, c}, où a, b, c sont les trois autres constituants de la tuile de la paire (p, x) : ce sont des parents de p, et l'autre côté de la cellule est son quatrième parent.

Preuve. Soit T₀ = {p, x, a, b, c} la tuile de la paire. T15 laisse trois cas.

1. T₀ est la tuile-porte de p. Alors x est dans T(p). Si p est dans le germe, T(p) est la tuile du germe et x est né. Sinon x est un parent de p, donc né, le tissu étant clos par plancher. Or x n'est pas né : ce cas est exclu.
2. T₀ est la tuile-porte de x. Alors p est un parent de x.
3. Sinon T(p) = {p, x′, a, b, c}, où x′ est l'autre côté de la cellule {p, a, b, c}. Les parents de p sont x′, a, b, c : ils sont nés. La cellule {p, a, b, c} est donc née ; ses deux côtés sont x′, né, et x, qui ne l'est pas. Dans ce cas T(x) = {x, p′, a, b, c} : p n'est pas un parent de x. Parent et cousin s'excluent. (Quand p est un parent de x, il arrive aussi que x soit le côté non né d'une cellule née contenant p : le contre-auditeur l'a relevé.)

**T21 ((C) en entier). [T, sous les faits admis]** Dans un tissu clos par plancher, les places admissibles sont exactement les côtés non nés des cellules nées.

Preuve. Soit x une place admissible. Par (C*), x est un constituant de l'empilement. Elle n'est pas née : une boule se chevauche elle-même, et x ne chevauche aucun constituant né. Ses quatre contacts sont nés ; appliquons T20 à chacun. Si l'un d'eux est dans le second cas, x est le côté non né d'une cellule née. Sinon les quatre sont des parents de x, qui n'en a que quatre : ils forment son plancher, une cellule née dont x est un côté.

Inversement, soit x le côté non né d'une cellule née {a, b, c, d}. C'est une boule ronde liée à a et à trois voisins de a. Les quatre sont indépendants : leurs produits valent 1 sur la diagonale et −1 ailleurs, de déterminant −16. Et x ne chevauche aucun constituant né, deux constituants distincts de l'empilement ne se chevauchant jamais (X-28).

La conjecture (C) de X-29 demandait cela pour les tissus clos par pliage. Ils sont clos par plancher (T10) : elle est démontrée, sous les faits admis, et pour une classe plus large.

**T22 (aucune cellule sans côté né). [T, sous les faits admis]** Dans un tissu clos par plancher, toute cellule née a un côté né : celui qui est du côté du germe.

Preuve. Soit {a, b, c, d} une cellule née, u et u′ ses côtés, T = {u, a, b, c, d} celle des deux tuiles qui est la plus proche du germe. Montrons que u est né.

Si T est la tuile-porte d'un des quatre, disons v : ou bien v est dans le germe, T est la tuile du germe et u est né ; ou bien u est un parent de v, donc né.

Sinon, pour chaque v parmi a, b, c, d, un mur de T passant par v sépare T du germe (X-30 bis, section 324). Le mur de T opposé à u est celui de la cellule : il ne sépare pas T du germe, T étant la plus proche. Chaque v a donc, parmi les trois autres, un constituant dont le mur opposé sépare T du germe. Il y a au moins deux tels constituants, disons a et b.

Il n'y en a pas trois. Si les murs opposés à a, b, c séparaient tous T du germe, regardons depuis u et d : a, b, c forment un triangle du réseau, ces trois murs sont au-dessus de ses trois côtés, et le triangle de la tuile de la paire (u, d) serait au-delà des trois côtés à la fois. C'est impossible : les trois coordonnées barycentriques d'un point ont pour somme 1, elles ne sont pas toutes négatives ou nulles. De même pour a, b, d, vu de u et c.

Ce sont donc exactement a et b. Aucun mur de T passant par a et b ne sépare alors T du germe : T est la tuile de la paire (a, b). Elle n'est la tuile-porte ni de a ni de b. C'est le troisième cas de T15 : T(a) = {a, b′, u, c, d}. Donc u est un parent de a : il est né.

### Partie B. Le lien avec la division de l'arête

**T23, corrigé (vue d'un fil). [T, élémentaire]** Quand x naît, côté non né de la cellule née {a, b, c, d}, cette cellule donne quatre cellules nouvelles : {x, b, c, d}, {x, a, c, d}, {x, a, b, d}, {x, a, b, c}. Deux contiennent le fil (a, b) : {a, b, c, x} et {a, b, d, x}. Ce sont les deux cellules filles que donne la division de l'arête (c, d) par un porteur né sur elle. Les deux autres contiennent le fil (c, d), qui demeure.

Le premier jet disait « quatre cellules nouvelles apparaissent ». C'est faux quand x touche plus de quatre constituants nés : elle est alors le côté de plusieurs cellules nées à la fois, et il apparaît sept cellules, ou dix (section 341).

C'est vrai pour chacun des six fils de la cellule : vue d'un fil, la naissance dans la cellule est la division du fil opposé. Ce qui sépare les deux réalisations : dans la division de l'arête, le fil coupé disparaît et la cellule devient deux ; dans le tissu de contact, le lien entre c et d reste, et il y a deux cellules de plus.

**T24 (rang 2, vue du parent : la division du fil, exactement). [T, sous (C9)]** Disques, règle à la lettre. Soit p un disque né au palier n₀.

- Au palier n₀ + g, p a exactement 3 × 2^g voisins nés.
- Ses voisins nés sont rangés en anneau. Chaque fil de l'anneau se divise en deux à chaque palier, par un nouveau-né lié à ses deux bouts, et la cellule {p, q, r} devient deux cellules qui contiennent p.
- Deux disques nés au même palier, à partir du palier 1, ne sont jamais liés. En particulier deux voisins de p nés au même palier, à partir du palier 1.

Preuve. Les tuiles qui contiennent p forment un sous-arbre, de racine T(p) = {p, a, b, c} (la tuile du germe si p y est). De chaque tuile {p, q, r, s} on passe à trois tuiles contenant p, en retournant q, r ou s ; l'une de ces trois ramène vers la racine, sauf à la racine. Le sous-arbre a donc 3 × 2^(g−1) tuiles à la profondeur g ≥ 1, et chacune apporte un voisin nouveau de p. Avec a, b, c : 3 + 3 (1 + 2 + … + 2^(g−1)) = 3 × 2^g voisins jusqu'à la profondeur g.

La profondeur est le palier : S(n) est l'ensemble des disques dont la tuile-porte est à la distance n au plus du germe. Par récurrence sur n. Si la tuile-porte de x est à la distance n + 1, la tuile qui la précède sur le chemin du germe contient les trois parents de x, dont les tuiles-portes sont sur ce chemin : ils sont dans S(n), et x est un côté de leur cellule. Inversement, soit x hors de S(n), côté d'une cellule {a, b, c} de S(n), et U = {a, b, c, x}. Le chemin du germe à U y entre par une tuile voisine. Si elle contenait x, x aurait été créé plus tôt et U serait la tuile-porte d'un des trois autres, à la distance n au plus : x serait dans S(n). C'est donc l'autre tuile de la cellule, V, et U est la tuile-porte de x. Le disque créé par V est a, b ou c, sinon la cellule serait dans trois tuiles : V est à la distance n au plus, U à la distance n + 1 au plus. La tuile de profondeur g du sous-arbre de p est ainsi à la distance n₀ + g du germe. (Le premier jet appelait ici T7, qui n'est démontré qu'au rang 3 ; la réparation est celle du contre-auditeur.)

L'anneau. Un fil (q, r) de p est dans deux tuiles, {p, q, r, s} et {p, q, r, s′}. Au départ les fils de p sont (a, b), (b, c), (c, a) : un triangle. Quand le côté non né x de la cellule {p, q, r} naît, le fil (q, r) est remplacé sur le pourtour par (q, x) et (x, r). Sous la règle à la lettre, chaque fil du pourtour est divisé à chaque palier.

Les âges. Si deux disques x et y sont liés, une tuile T les contient. T(x) et T(y) sont sur le chemin du germe à T : l'une précède l'autre. Hors du germe elles diffèrent, une tuile ne créant qu'un disque : les paliers de x et de y diffèrent, sauf s'ils sont tous deux du palier 0.

**T25, corrigé (rang 3, vue d'un fil du germe : pas de doublement). [T, sous les faits admis et (C8)]** Soient p et q deux constituants du germe. Repérons les constituants liés aux deux par les triplets d'entiers (i, j, k) de somme 1, les trois autres constituants du germe étant en (1, 0, 0), (0, 1, 0), (0, 0, 1), et deux points étant liés quand ils diffèrent de (1, −1, 0) ou d'une permutation. Alors le palier du constituant en (i, j, k) est son étendue moins un.

Le nombre de ceux qui sont nés au palier g au plus est donc le nombre de points du réseau d'étendue au plus g + 1 : 3, 6, 12, 21, 30, 42, 57, 72, 90, … C'est (g + 1)(g + 2), plus un quand g est multiple de 3 : constaté par énumération jusqu'à g = 60, démontré par le contre-auditeur (section 341). La croissance est quadratique.

Preuve. Par (C8), la tuile-porte de l contient p et q : c'est {p, q, l, l₁, l₂}, où (l, l₁, l₂) est un triangle du réseau. Par T7, le palier de l est 1 + le plus grand des paliers de l₁ et l₂, p et q étant de palier 0. Pour tout autre triangle (l, m₁, m₂) du réseau, la cellule {p, q, m₁, m₂} est née dès que m₁ et m₂ le sont, et l en est un côté : le palier de l est au plus 1 + le plus grand des paliers de m₁ et m₂. Le palier est donc donné, sur le réseau, par la règle : 0 sur le triangle de départ ; ailleurs, 1 + le plus petit, sur les triangles contenant l, du plus grand palier des deux autres sommets.

Cette règle n'a qu'une solution, par récurrence sur le palier, et l'étendue moins un lui obéit. D'un point à un voisin, l'étendue change de 2 au plus, et ne baisse de 2 que vers un seul voisin (on retire 1 à l'unique plus grand, on ajoute 1 à l'unique plus petit) : dans un triangle contenant l, un des deux autres sommets a une étendue au moins égale à celle de l moins un. Inversement, rangeons l = (x, y, z) avec x ≥ y ≥ z, d'étendue au moins 2. Le voisin (x − 1, y, z + 1) a une étendue plus petite. Il forme un triangle avec l et (x − 1, y + 1, z), d'étendue plus petite si x − y ≥ 2, ou avec l et (x, y − 1, z + 1), d'étendue plus petite si y − z ≥ 2. L'un des deux a lieu : sinon x − y = y − z = 1 et la somme vaudrait 3y, qui n'est pas 1.

**T26 (rang 3, liens entre constituants du même âge). [T, sous les faits admis]** Sous la règle à la lettre, deux constituants liés nés au même palier, à partir du palier 1, sont des cousins.

Preuve. Si la tuile de la paire (p, q) était la tuile-porte de p, q serait un parent de p, donc d'un palier plus petit (T7). De même en échangeant p et q. Reste le troisième cas de T15.

Au rang 2 il n'y a aucun lien entre constituants du même âge (T24). Au rang 3 il y en a dès le palier 2, et ce sont toujours deux constituants qui ferment ensemble un anneau de six.

## 338. Les onze clauses chiffrées

| Clause | Prédit | Obtenu | Verdict |
|---|---|---|---|
| A1, T20 sous la règle à la lettre, n = 2, 3, 4 | aucune exception ; cas du parent aux trois paliers ; cas du cousin pour n = 3 et 4 | 1 260, 5 160 et 20 700 paires (p né, x non né des deux paliers suivants) ; aucune exception ; parents : 1 260, 5 100, 20 520 ; cousins : 0, 60, 180 | vraie |
| A2 (a), T20 sur 200 tissus clos par plancher tirés au hasard | aucune exception | 1 544 868 paires ; 1 541 411 parents, 3 457 cousins ; aucune exception | vraie |
| A2 (b), places = côtés non nés des cellules nées | égalité dans les 200 tissus | 16 008 places, aucune hors de l'empilement ; égalité dans les 200 | vraie |
| A2 (c), cellules nées sans côté né | aucune | aucune ; et le côté né, quand il est seul, est toujours du côté du germe | vraie |
| A2 (d), places dont le plancher n'est pas né en entier | au moins une | 2 908 sur 16 008, dans chacun des 200 tissus | vraie |
| A3, règle à la lettre, paliers 2 à 5 | aucune cellule née sans côté né | 135, 585, 2 355 et 9 645 cellules ; aucune sans côté né ; côté né seul toujours du côté du germe | vraie |
| B1, rang 2, programme indépendant, paliers 0 à 8 | 4, 8, 20, 56, 164, 488, 1 460, 4 376, 13 124 disques ; 3 × 2^g voisins pour tout disque à tout âge ; aucun lien entre disques du même palier | nombres exacts ; 13 124 disques, 19 700 couples (disque, âge), aucun écart ; 39 360 naissances de voisins, chacune divise un fil et un seul, au palier qui suit sa création ; aucun lien entre disques du même palier | vraie |
| B2, rang 3, les dix fils du germe | 3, 6, 12, 21, 33, 48, 66 | 3, 6, 12, 21, 30, 42, 57, pour les dix | **fausse** |
| B3, rang 3, toutes les paires liées nées au palier 5 au plus | au plus 66 voisins communs au palier 6 | 8 010 paires ; au plus 57, atteint par les dix fils du germe | vraie (borne mal fondée, point 4) |
| B4, rang 3, paires liées de même palier | aucune au palier 1 ; il y en a aux paliers 2 à 5 ; toutes cousines | 0, 10, 30, 90, 450 ; toutes cousines | vraie |
| B5, rang 3, voisins d'un constituant du germe | 4, 8, 20 aux paliers 0, 1, 2 ; 979 au palier 6 | 4, 8, 20, 56, 140, 368, 980 | **fausse pour le dernier nombre** |

Détail de A2. Les tissus sont ceux du tirage de R4 (X-29 bis) : le germe, 2 à 8 constituants tirés dans le palier 5, et leurs ancêtres ; 12 à 51 constituants. Les 150 premiers sont les tissus de R4, où l'égalité de la clause (b) était déjà mesurée. Le programme vérifie que chaque tissu est clos par plancher.

Détail de B1. Le programme `x31_rang2.py` n'importe rien du laboratoire et ne se sert pas de (C9). Il applique la règle à la lettre par force brute jusqu'au palier 5 (toutes les cellules, tous les côtés), la compare à une construction plus rapide, puis contrôle toutes les paires de disques jusqu'au palier 8. Aucun chevauchement.

Temps de calcul : moins d'une minute en tout.

## 339. Ajout non scellé

**Le réseau, après l'échec de B2. [M, puis T]** Sur le réseau triangulaire seul, sans l'empilement : la règle « un point naît dès que deux de ses voisins liés entre eux sont nés », depuis un triangle, donne pour palier l'étendue moins un, sans exception jusqu'au palier 60 ; le décompte suit (g + 1)(g + 2), plus un quand g est multiple de 3. Sortie : `x31_reseau_60.out`. La preuve du premier point est dans T25 ; celle du décompte est du contre-auditeur.

## 340. Ce que cela dit du point 1 du registre

**Ce qui est acquis.** Dans la lecture de contact, au rang 3, tant que nul ne naît avant ses quatre parents, la mitose avec héritage et la naissance dans la cellule offrent exactement les mêmes places. C'était constaté ; c'est démontré, sous des faits classiques admis. Chaque contact né d'une place est alors un de ses parents, ou un cousin.

**Ce qui est entamé.** La division de l'arête et la naissance dans la cellule, côte à côte.

| | Division de l'arête | Naissance dans la cellule |
|---|---|---|
| La cellule, vue d'un de ses fils | devient deux | donne les deux mêmes |
| Le fil opposé | est coupé, disparaît | demeure : deux cellules de plus |
| Nombre de cellules filles | 2 | au moins 4 |
| Doublement à chaque palier | N = 2^g (C-116) | au rang 2, vu du parent : 3 × 2^g voisins, exactement ; au rang 3, sous la règle à la lettre : non |
| Liens entre constituants du même âge | aucun (C-136c) | au rang 2 : aucun à partir du palier 1 ; au rang 3 : entre cousins seulement, dès le palier 2 |

Au rang 2, vue du parent, la naissance dans la cellule ressemble de près à la division du fil : sur le pourtour du parent, chaque fil se divise en deux à chaque palier, et aucun lien ne se forme entre constituants du même âge. L'héritage y impose déjà la naissance dans la cellule (K19, X-27). Mais ce n'est pas la même chose : le lien entre les deux bouts du fil divisé demeure.

Au rang 3, les deux premières réalisations coïncident sous la condition du plancher. La division de l'arête n'y apparaît que vue d'un fil, et sous la règle à la lettre le doublement est perdu. Vus d'un fil du germe, les constituants croissent comme le carré du palier : 3, 6, 12, 21, 30, 42, 57 [T]. Vus d'un parent : 4, 8, 20, 56, 140, 368, 980 [M]. En tout : 5, 10, 30, 120, 450, 1 800, 7 290 [M].

**Ce qui reste.** Une seule réalisation tenue de bout en bout.

## 341. Contre-audit indépendant

Un sous-agent Claude Opus, qui n'a pas vu mon raisonnement : il a reçu le carnet, les fichiers et la consigne de chercher ce qui est faux ou troué. Son code est écrit à neuf. Rapport versé tel quel : `calculs/x31_contre_audit_rapport.md`. Son code et ses sorties : `calculs/x31_contre_audit/`. C'est une IA de la même famille que le pilote, pas un mathématicien.

**Faux ou troué, dans le premier jet.**

| Ce qu'il a trouvé | Suite donnée |
|---|---|
| T23, « quatre cellules nouvelles apparaissent » : faux en général. Sous la règle à la lettre, 60, 180 et 720 nouveau-nés des paliers 4, 5 et 6 ont cinq voisins nés avant eux ; dans ses tissus, 1 015 places créeraient sept cellules, et 4 en créeraient dix | T23 corrigé ; « au moins 4 » en section 340 |
| T24, « deux voisins de p nés au même palier ne sont jamais liés » : faux au palier 0 (108 paires) | « à partir du palier 1 » |
| T24, preuve : le palier égal à la profondeur s'appuyait sur T7, démontré seulement au rang 3 | preuve réécrite par récurrence, selon sa réparation |
| Section 340 : « les trois réalisations y sont une seule chose » dit plus que ce qui est démontré, le fil divisé demeurant ; et la suite 4, 8, 20, …, 980 est mesurée, non démontrée | section réécrite ; suites étiquetées |

**Imprécisions.** « De deux choses l'une », dans T20, n'opposait pas des conclusions exclusives : énoncé repris avec « parent ou cousin ». Dans T25 : « au palier g au plus », et l'unicité de la solution de la règle. Dans (C9) : la connexité des tuiles contenant un disque. Dans les âges de T24 : le cas de deux disques du germe. Tout est repris.

**Ce qu'il apporte.** Une preuve du décompte de T25 : avec E = g + 1, on compte les triplets de {0, …, E}³ dont le plus petit terme est 0 et dont la somme est congrue à 1 modulo 3 ; un filtre par les racines cubiques de l'unité donne E(E + 1), plus un si E est congru à 1 modulo 3. Il l'a vérifié de g = 0 à 300. Je n'ai pas refait ce calcul à la main.

**Partie A : rien de faux trouvé.** T20, T21, T22, T25 et T26 : aucun pas faux, une fois admis les faits listés.

**Ses calculs.**

| Point | Ce qu'il a obtenu |
|---|---|
| T20, règle à la lettre | les mêmes nombres que la clause A1 |
| T20, T21, T22 sur 40 tissus clos par plancher construits par lui (41 à 150 constituants, jusqu'à la génération 9) | 154 135 paires, aucune exception ; 10 533 places trouvées en résolvant chaque quadruple, toutes côtés non nés de cellules nées, et inversement ; 16 308 cellules nées, aucune sans côté né |
| Témoin | 11 tissus non clos par plancher : T21 en défaut dans les 11, T22 dans 5 |
| Rang 2 | 4 à 13 124 disques ; 19 700 couples (disque, âge), aucun écart à 3 × 2^g ; 39 360 naissances de voisins, chacune divise un fil et un seul ; 6 liens entre disques du même palier, tous au palier 0 |
| T25 | 3, 6, 12, 21, 30, 42, 57, 72 aux paliers 0 à 7, pour les dix fils ; palier = étendue − 1 sans écart |
| T26 | 0, 10, 30, 90, 450, 1 710 paires liées de même palier aux paliers 1 à 6, toutes cousines |
| Voisins d'un constituant du germe | 4, 8, 20, 56, 140, 368, 980, 2 552 |

**Ce qu'il déclare ne pas avoir contrôlé.** Mes 200 tissus (il a construit les siens). Son réservoir de constituants non nés est borné. Les faits admis ne sont contrôlés qu'à travers la descente. L'explication du 979 de X-30 bis. Le lien de fond avec la division de l'arête. Un premier lancement a échoué sur un dépassement d'entiers et n'a pas été enregistré ; il a plafonné la profondeur. Des tirages ne sont pas une preuve.

**Ce que j'ai vérifié de son rapport.** Ses nombres sont dans ses sorties, que j'ai lues. L'explication du 979 : la sortie `x30bis_V5_6.out` compte 979 voisins répartis par norme de 1 à 52, le voisin envoyé à l'infini n'y figure pas ; 979 + 1 = 980.

## 342. Ce que cela donne, et ce que cela ne donne pas

Cela donne la fin d'une question ouverte depuis X-27 : sous la condition du plancher, hériter des liens du parent et naître dans la cellule, c'est la même chose. Et une première pierre pour la suivante : ce que ces deux réalisations ont de commun avec la division de l'arête, et ce qui les en sépare.

Cela ne valide pas la TOE et ne démontre pas la cosmogonie. Ce sont des énoncés sur les empilements de disques et de sphères, appliqués à une lecture du pilote. La trame régulière n'a pas été recalculée ici : ce que j'en dis vient de la grille des verrous.

## 343. Suite, sur la même ligne

Le point 1 n'est pas clos. L'épreuve qui suit, sans rien demander à l'auteur : au rang 3, une règle où chaque constituant ne se divise qu'une fois par génération, sa fille naissant dans une de ses cellules, garde-t-elle le tissu clos par plancher, et donne-t-elle N = 2^g ? C'est la lecture la plus directe de « le parent devient deux filles » avec « les descendants héritent des liens du parent ». Elle est faite en X-32.

## 344. Fichiers

- `calculs/x31_cellule_et_arete_prediction.txt` : prédiction scellée.
- `calculs/x31_cellule.py` : rang 3, sur les données du laboratoire. Sorties : `x31_A1_2.out`, `x31_A1_3.out`, `x31_A1_4.out`, `x31_A2_1_100.out`, `x31_A2_101_200.out`, `x31_A3_2.out` à `x31_A3_5.out`, `x31_B_6.out`.
- `calculs/x31_rang2.py` : rang 2 et réseau triangulaire, indépendant. Sorties : `x31_rang2_B1.out`, `x31_reseau_60.out`.
- `calculs/x31_contre_audit_rapport.md` : rapport du contre-audit, versé tel quel.
- `calculs/x31_contre_audit/` : le code du contre-auditeur et ses sorties.

TOE 0/7. Aucun verrou fermé.
