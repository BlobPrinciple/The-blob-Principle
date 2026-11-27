# X-32 — Le parent devient deux filles : au rang 3, une règle qui tient N = 5 × 2^g avec l'héritage et la naissance dans la cellule

**Rédigé par Claude, pilote IA et contre-auditeur.** Auteur du Blob Principle : Rudolphe Mirante. La cosmogonie lui appartient.

TOE 0/7. Aucun verrou fermé.

**Parole de l'auteur** (27 novembre, 17 h 04, heure de Paris) : « Continue et reste sur la ligne précise de la cosmogonie et rien d'autre ! »

La ligne suivie est toujours le point 1 de la section 5 du registre, « une seule réalisation de la mitose ». X-31 laissait la question : au rang 3, une réalisation peut-elle tenir ensemble « le parent devient deux filles », N = 2^g, l'héritage des liens d'un parent unique et la naissance dans la cellule ?

Prédiction scellée avant tout calcul : `calculs/x32_deux_filles_prediction.txt`, SHA-256 `707c45ef49dad1f61e62cb97dc610b957930c28246c483d358b9841453535321`, poussée sur la branche à 16 h 36 UTC (commit 682fb1f).

## 345. Ce qui est faux, manque ou reste ouvert, d'abord

1. **La cosmogonie n'est pas démontrée.** Aucun verrou ne bouge. Ce carnet montre qu'une règle de naissance existe, dans le tissu de contact de rang 3, qui tient ensemble la naissance dans la cellule et trois principes que la règle à la lettre ne portait pas. Il ne montre pas que cette règle est celle du Blob.
2. **La règle laisse des choix, et rien ici ne dit lequel le Blob fait.** Au départ, 44 façons d'apparier les cinq constituants du germe à leurs filles. Ensuite, à chaque génération, deux ou trois filles possibles pour une mère qui a déjà enfanté, trois ou quatre pour une nouvelle-née. C'est une famille de réalisations, pas une réalisation.
3. **Elle n'occupe pas toutes les places.** Toutes sont occupées à la première génération, la moitié à la deuxième ; à partir de la cinquième, deux places admissibles sur trois environ restent libres (mesuré sur trois tirages). « Toutes les cellules enfantent ensemble » n'y tient plus ; « tout constituant se divise à chaque génération » y tient.
4. **Elle ne porte pas « aucun lien entre porteurs du même âge ».** Des constituants nés à la même génération se lient : 5 898 liens de ce genre à la dixième génération, sur 20 tirages au hasard et 51 200 naissances. Mesuré, non prédit ; et le nombre dépend de la façon de choisir (section 352).
5. **Elle ne dit rien du reste** : ni le temps, ni l'étirement par l'arête, ni le bain, ni la fermeture qui bloque la mitose. Ici rien ne bloque jamais.
6. **Tout repose sur les faits classiques admis de X-30 bis**, employés une fois de plus pour trois constituants liés (section 347). **Rien n'est devant Lean. Aucun humain n'a lu ce carnet.**
7. **Le contre-audit a trouvé quatre trous dans la rédaction des preuves** (section 352), dont une phrase fausse telle qu'écrite : « deux constituants différents n'ont aucune fille propre commune » ne vaut que hors du germe. Aucun ne renverse T27 ni T28 ; tous sont réparés ici. Il a aussi relevé que les sections 351 et 353 présentaient des lectures comme des résultats : elles sont reprises.
8. **Rien de nouveau n'est revendiqué.** Antériorité non cherchée.
9. **Clauses chiffrées** : les quatre sont vraies (section 349).

## 346. Vocabulaire

Celui de X-29 à X-31, plus ceci.

- **T′(q)**, pour q hors du germe : la tuile voisine de la tuile-porte T(q) à travers le plancher de q. Elle est plus proche du germe que T(q), d'un pas.
- **Fille propre** de q : un constituant x dont le plancher est une des quatre cellules de T(q) qui contiennent q. Alors q est un parent de x. **Mère propre** de x : le constituant dont x est une fille propre, quand il est seul. Les cinq constituants du palier 1 sont, chacun, fille propre de quatre constituants du germe.
- **Mère**, dans la règle de T28 : le constituant qui prend x pour fille. C'est un parent de x. À partir de sa deuxième fille, ce n'est plus sa mère propre.
- **Génération** : le rang de la naissance sous la règle de T28. À ne pas confondre avec le palier, qui est celui de la règle à la lettre.

## 347. Faits admis

Ceux de X-30 bis, section 324, et T15, T21 (X-30 bis, X-31). J'emploie (C3) pour les tuiles qui contiennent **trois** constituants tous liés : elles sont six, en anneau (T4, X-28) ; l'une est la plus proche du germe, et le long de l'anneau les distances au germe sont d, d + 1, d + 2, d + 3, d + 2, d + 1. C'est le même fait classique sur les groupes de Coxeter. Conséquence : la tuile voisine de la plus proche a un mur de l'anneau qui la sépare du germe, celui qu'elle partage avec elle, et un qui ne la sépare pas ; la tuile la plus éloignée a ses deux murs de l'anneau qui la séparent du germe.

## 348. Ce qui est démontré

**T27 (les filles propres). [T, sous les faits admis]** Soit q hors du germe, de plancher {f₁, f₂, f₃, f₄}, et x_i le côté au-delà de la cellule de T(q) qui ne contient pas f_i. Alors x_i est une fille propre de q si et seulement si le mur de T′(q) opposé à f_i ne sépare pas T′(q) du germe ; sinon q et x_i sont cousins. Le nombre de murs de T′(q) qui la séparent du germe vaut 0, 1 ou 2 : q a 4, 3 ou 2 filles propres. Un constituant hors du germe et du palier 1 a une seule mère propre, ou aucune ; dans ce dernier cas deux de ses parents sont cousins.

Preuve. Notons T = T(q), T′ = T′(q), C_i la cellule T privée de f_i, et T* = C_i ∪ {x_i}. Aucun mur de T passant par q ne sépare T du germe ; le mur de C_i passe par q, donc il sépare T* du germe.

Les murs de T* qui passent par x_i sont de deux sortes.

1. Le mur opposé à f_j, pour j ≠ i. Il contient q et les deux autres f. Autour de ces trois constituants, T est la tuile de l'anneau la plus proche du germe : ses deux murs de l'anneau passent par q. T* est sa voisine. Son autre mur de l'anneau, opposé à f_j, ne la sépare donc pas du germe.
2. Le mur opposé à q. Il contient x_i et les trois f autres que f_i. Autour de ces trois, l'anneau contient T′, T et T*, dans cet ordre. Les murs de l'anneau de T′ sont celui du plancher, qui ne la sépare pas du germe, et celui opposé à f_i. Si ce dernier ne sépare pas T′ du germe, T′ est la plus proche de l'anneau ; T* est à deux pas, et son mur opposé à q ne la sépare pas du germe. S'il la sépare, la plus proche est au-delà de T′ ; T* est la plus éloignée, et son mur opposé à q la sépare du germe.

Dans le premier cas, aucun mur de T* passant par x_i ne la sépare du germe : T* est la tuile-porte de x_i, dont le plancher est C_i. Dans le second, T* n'est la tuile-porte ni de x_i ni de q, et aucun mur passant par q et x_i ne la sépare du germe (ce sont ceux du point 1) : T* est la tuile de la paire (q, x_i), qui sont cousins.

Le compte. Le mur du plancher ne sépare pas T′ du germe. Parmi les quatre autres, trois ne peuvent pas la séparer à la fois (l'argument des coordonnées barycentriques de T22, X-31). Aucun ne la sépare si et seulement si T′ est la tuile du germe.

La mère propre. Soit x hors du germe et du palier 1 ; T′(x) n'est pas la tuile du germe, un ou deux de ses murs la séparent du germe, opposés à des parents de x. S'il n'y en a qu'un, opposé à f : T′(x) est la tuile-porte de f, et x est une fille propre de f. Aucun autre parent g ne convient : T(g) contiendrait le plancher de x, ce serait T(x) ou T′(x). Ce n'est pas T(x) : aucun de ses cinq murs ne la séparerait du germe, ce serait la tuile du germe. Ce n'est pas T′(x) : le mur opposé à f, qui passe par g, la sépare du germe. S'il y en a deux, opposés à f et f̃ : T′(x) est la tuile de la paire (f, f̃), qui sont cousins. Elle n'est la tuile-porte de personne : le mur opposé à f passe par tous ses autres constituants, et le mur opposé à f̃ passe par f. Et T(x) n'est la tuile-porte d'aucun parent, comme ci-dessus : x n'a pas de mère propre.

**T28 (le parent devient deux filles : une réalisation qui tient). [T, sous les faits admis]** Règle. Génération 0 : le germe. À chaque génération, tout constituant né p donne une fille et une seule. Génération 1 : la fille d'un constituant u du germe est le côté au-delà d'une cellule du germe qui contient u, les cinq filles étant distinctes. Ensuite : si p n'a pas encore de fille, sa fille est une de ses filles propres ; sinon c'est une fille propre de sa dernière fille, dont le plancher contient p. Deux constituants ne prennent jamais la même fille.

Alors :

1. la règle peut toujours être suivie, et de plusieurs façons ;
2. N = 5 × 2^g, exactement ;
3. le tissu est clos par plancher à toute génération, donc dans l'empilement et sans chevauchement ;
4. chaque naissance a lieu à une place admissible, côté non né d'une cellule née ; la nouvelle-née est liée à sa mère et à trois voisins de sa mère.

Preuve. Génération 1. Le côté au-delà de la cellule du germe qui ne contient pas v est lié à tout constituant du germe autre que v. Il suffit d'une permutation du germe sans point fixe ; il y en a 44.

Ensuite, par récurrence : tout constituant né hors du germe est du palier 1 ou a une mère propre. Il a donc 4 ou 3 filles propres (T27), jamais 2.

Soit c née à la génération g, de mère p ; p est un parent de c. Si c est du palier 1, son plancher est une cellule du germe, et ses quatre filles propres ont pour planchers c et trois constituants de cette cellule : trois de ces planchers contiennent p. Sinon c a une mère propre e et un plancher {e, a, b, d} ; ses filles propres ont pour planchers les cellules de T(c) qui contiennent c et e. Si p = e, les trois contiennent p ; sinon deux. Dans tous les cas p a au moins deux filles possibles, et c a au moins trois filles propres. Quel que soit l'ordre des choix, chacune trouve une fille : la règle ne se bloque jamais.

Une fille propre de c n'est demandée que par c et par la mère de c, une fois chacune, à la génération g + 1. Deux constituants différents, hors du germe, n'ont aucune fille propre commune (T27). Les filles sont donc toutes distinctes.

Aucune n'était née. Toute née à une génération h ≥ 2 est fille propre d'une née à la génération h − 1, et n'a qu'une mère propre. Une fille propre d'un constituant hors du germe a une tuile-porte à deux pas du germe au moins : elle n'est ni du germe, ni du palier 1. Une fille propre de c, née à la génération g, ne peut donc naître qu'à la génération g + 1. Le nombre double.

Le plancher d'une nouvelle-née x, fille propre de c, est fait de c et de trois parents de c : tous nés. Le tissu reste clos par plancher. Par T21, x est une place admissible. Elle est liée à sa mère, qui est dans son plancher, et aux trois autres constituants de ce plancher, qui sont des voisins de sa mère. Elle a une mère propre : la récurrence continue.

**Ce que la règle tient ensemble.** Dans le tissu de contact de rang 3 : le parent devient deux filles, lui-même et la nouvelle-née ; N = 5 × 2^g ; les descendants sont liés et la fille hérite de trois liens d'un parent unique ; la naissance a lieu dans une cellule, du côté libre ; rien ne se chevauche ; nul ne naît avant ses quatre parents.

## 349. Les quatre clauses chiffrées

| Clause | Prédit | Obtenu | Verdict |
|---|---|---|---|
| C1, T27 sur la règle à la lettre, jusqu'au palier 5 | « fille propre » si et seulement si le mur ne sépare pas ; sinon cousins ; aucune exception | 1 795 constituants, 7 180 cellules : 4 820 filles propres, 2 360 cousins, aucun autre cas ; aucun désaccord avec le mur | vraie |
| C2, nombre de filles propres | 4 pour les 5 du palier 1 ; 3 pour les 20 du palier 2 ; au palier 3, 3 pour 60 et 2 pour 30 ; jamais 0 ni 1 | exactement cela ; au palier 4 : 3 pour 240, 2 pour 90 ; au palier 5 : 3 pour 900, 2 pour 450 | vraie |
| C3, la règle de T28, 20 tirages, 10 générations | jamais d'échec ; 5, 10, 20, …, 5 120 ; constituants distincts ; clos par plancher ; aucun chevauchement | aucun échec ; mêmes nombres dans les 20 tirages ; aucun doublon ; clos par plancher à chaque génération ; aucun chevauchement à la génération 10 | vraie |
| C4, chaque naissance | côté non né d'une cellule née, liée à sa mère ; au moins deux filles possibles pour chaque mère | sans exception sur les 20 tirages ; la dernière fille avait 3 filles propres 51 000 fois, 4 les 100 fois où elle est du palier 1 | vraie |

Détail de C1. Les murs de T′(q) qui la séparent du germe : aucun pour 5 constituants, un pour 1 220, deux pour 570.

Détail de C3. La tuile-porte de chaque nouvelle-née est recalculée par descente, sans se servir de T27. Le contrôle du chevauchement porte sur toutes les paires des 5 120 constituants.

Temps de calcul : moins d'une minute en tout.

## 350. Mesures sans prédiction

**Liens entre constituants de la même génération. [M]** Sur les 20 tirages au hasard, aux générations 2 à 10 : 55, 48, 89, 189, 403, 712, 1 456, 2 923, 5 898. Aucun à la génération 1. Ce nombre dépend de la façon de choisir : le contre-auditeur en trouve environ deux fois plus par naissance avec d'autres choix (section 352).

**Palier et génération. [M]** À chaque génération g, le plus grand palier des nouvelles-nées est g.

**Voisins selon l'âge, à la génération 10. [M]** Une nouvelle-née a 4 ou 5 voisins. Puis, en moyenne : 6,2 à une génération d'âge, 10,2 à deux, 15,7 à trois, 22,9 à quatre, 32,4 à cinq ; les constituants du germe en ont 212 en moyenne (de 100 à 381).

**Places laissées libres. [M]** Trois tirages, jusqu'à la génération 8. Au départ 5 places, toutes occupées ; puis 20, dont 10 occupées ; à 1 280 constituants, 3 742, 3 724 et 3 747 places admissibles, dont un tiers environ est occupé à la génération suivante.

## 351. Ce que cela dit du point 1 du registre

Sous la règle à la lettre, toutes les cellules enfantent, le nombre est multiplié par 4 environ, et la nouvelle-née n'a pas de parent unique. Trois principes y échouaient ensemble : N = 2^g, le parent qui devient deux filles, l'héritage des liens d'un parent unique.

La règle de T28 les tient tous les trois, dans le même tissu, avec la naissance dans la cellule et la condition du plancher. Le doublement, que seule la division de l'arête portait, y est.

Ma lecture, qui n'est pas un résultat : au rang 3, ce qui empêchait ces principes de tenir ensemble était la règle « toutes les cellules enfantent », non le tissu. Il est montré qu'une règle tient ; il n'est pas montré que c'était le seul obstacle.

Ce qu'elle ne règle pas. Elle n'est pas unique. Elle ne dit pas pourquoi une place plutôt qu'une autre. Elle laisse libres deux places sur trois. Et l'arête coupée y demeure, comme en X-31 : ce n'est pas la division de l'arête de la trame régulière.

## 352. Contre-audit indépendant

Un sous-agent Claude Opus, qui n'a pas vu mon raisonnement : il a reçu le carnet, les fichiers et la consigne de chercher ce qui est faux ou troué. Son code est écrit à neuf. Rapport versé tel quel : `calculs/x32_contre_audit_rapport.md`. Son code et ses sorties : `calculs/x32_contre_audit/`. C'est une IA de la même famille que le pilote, pas un mathématicien.

**Verdict.** Aucune erreur qui renverse T27 ou T28. Quatre trous de rédaction dans le premier jet.

| Ce qu'il a trouvé | Suite donnée |
|---|---|
| T28, « deux constituants différents n'ont aucune fille propre commune » : faux tel qu'écrit, les constituants du palier 1 étant filles propres de quatre constituants du germe | « hors du germe », seul cas employé |
| T28, « aucune n'était née » : affirmé sans preuve | preuve ajoutée, la sienne |
| T27, mère propre, un seul mur : le cas T(g) = T(x) oublié | ajouté |
| T27, deux murs : il fallait aussi exclure les deux autres parents et T(x) | ajouté |

**Imprécisions, reprises.** Le mot « mère » n'était pas défini. « Deux ou trois filles possibles » ne valait que pour une mère qui a déjà enfanté. « Deux places sur trois à chaque génération » est faux aux premières générations. Les liens entre constituants de la même génération dépendent de la façon de choisir. Les sections 351 et 353 donnaient des lectures pour des résultats.

**Ce qu'il apporte.** La preuve donne plus que l'énoncé : la mère a au moins deux choix et la nouvelle-née au moins trois filles propres, donc la règle ne se bloque dans aucun ordre de choix.

**Ses calculs.**

| Point | Ce qu'il a obtenu |
|---|---|
| T27, jusqu'au palier 5 | les mêmes nombres que les clauses C1 et C2 ; 1 220 constituants à une mère propre, 570 sans mère propre, ceux-ci toujours avec deux parents cousins |
| T28 | 250 lancements de 10 générations : 30 au hasard, et cinq façons de choisir faites pour mettre la règle en défaut, chacune sur les 44 départs. Aucun blocage ; 5 120 constituants partout ; aucun doublon ; aucun chevauchement |
| Choix restants | au moins deux pour une mère qui a déjà enfanté, au moins trois pour une nouvelle-née ; au plus bas, un seul choix restant après celui de l'autre |
| Voisins d'une nouvelle-née | 4 ou 5 dans tous les lancements |
| Liens de même génération, génération 10 | 9 198 sur 30 tirages au hasard ; 28 160 sur 44 lancements avec une autre façon de choisir |
| Places laissées libres | part occupée : 1, puis 0,5, puis environ 0,34 à partir de la génération 5 |

**Hors de l'énoncé, à son initiative.** Une règle plus libre : chaque constituant prend pour fille n'importe quel constituant non né dont il est un parent et dont les quatre parents sont nés. Un choix de proche en proche se bloque dans 14 lancements sur 15 : un constituant reste sans fille. Mais un appariement complet existe à chaque fois. La règle de T28 est une façon de ne jamais se bloquer ; ce n'est pas la seule façon de doubler.

**Ce qu'il déclare ne pas avoir contrôlé.** Les faits admis, relus sans calcul. Rien au-delà de 10 générations ; tous les choix n'ont pas été énumérés. Les classes de symétrie des 44 départs. Les moyennes de voisins selon l'âge. Des tirages ne sont pas une preuve.

**Ce que j'ai vérifié de son rapport.** Ses nombres sont dans ses sorties, que j'ai lues : six fichiers de lancements (30 + 5 × 44 = 250), tous sans blocage.

## 353. Ce que cela donne, et ce que cela ne donne pas

Cela donne une réponse à la question laissée par X-31 : oui, au rang 3, une règle tient ensemble le doublement, le parent unique, l'héritage et la naissance dans la cellule. Le point 1 du registre avance d'un pas ; il n'est pas clos.

Cela ne valide pas la TOE et ne démontre pas la cosmogonie. C'est de la géométrie des empilements de sphères, appliquée à une lecture du pilote. La règle est posée par le pilote pour éprouver un principe de l'auteur ; elle n'est pas dérivée de la cosmogonie.

## 354. Suite, sur la même ligne

Deux épreuves restent au point 1. Ce qui fixe le choix de la fille : les 44 départs et les choix suivants donnent-ils des tissus différents, ou le même à symétrie près ? Et ce que la fermeture bloque : l'auteur dit que la première fermeture bloque la mitose ; ici rien ne bloque. Puis le point 2 : le temps.

## 355. Fichiers

- `calculs/x32_deux_filles_prediction.txt` : prédiction scellée.
- `calculs/x32_deux_filles.py`. Sorties : `x32_T27_6.out`, `x32_chaine_1_20.out`, `x32_libres_1_3.out`.
- `calculs/x32_contre_audit_rapport.md` : rapport du contre-audit, versé tel quel.
- `calculs/x32_contre_audit/` : le code du contre-auditeur et ses sorties.

TOE 0/7. Aucun verrou fermé.
