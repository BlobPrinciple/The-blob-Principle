# Carnet du 23 novembre 2026, suite — X-27 : la mitose avec héritage, lue comme un contact. Un tissu peut sortir de l'empilement

**Rédigé par Claude, pilote IA et contre-auditeur.** Auteur du Blob Principle : Rudolphe Mirante. La cosmogonie lui appartient ; ce carnet ne grave rien.

**TOE 0/7. Aucun verrou fermé.**

Ce carnet suit celui de X-26 (sections 251 à 261), le même jour.

---

## 262. Ce qui est faux, manque ou a échoué, dit en premier

1. **Ma conjecture K20 est fausse.** Je l'avais scellée ainsi : « au rang 3, quel que soit l'ordre des naissances, toute place admissible appartient à l'empilement. Le tissu ne peut pas en sortir. » Contre-exemple exact (section 266) : après 17 naissances, toutes dans la cellule, un tissu offre une place admissible qui n'est pas dans l'empilement. Le verdict que j'attendais, « K20 vraie dans tous les essais, sans démonstration », était exact à la lettre et faux sur le fond.
2. **Aucun essai prédit n'a vu ce contre-exemple.** 1 807 400 places examinées dans tous les tissus de six naissances au plus, 8 264 dans quarante croissances longues, 5 286 dans vingt croissances ajoutées : toutes dans l'empilement. Je l'ai trouvé par le raisonnement, en cherchant à démontrer K20 et en n'y arrivant pas. Mes ordres « adverses » ne l'étaient pas : le bon adversaire ne cherche pas les places sans cellule, il laisse vides des places libres et fait naître ailleurs.
3. **Deux clauses chiffrées sont fausses.** M6 : je prédisais des places sans cellule dans au moins 3 croissances au hasard sur 20 ; il n'y en a dans aucune. M10 : je prédisais que le moteur complet fait naître dans une cellule dans 45 à 70 % des cas ; c'est 36,2 à 43,3 %.
4. **Une clause est vraie mais vide.** M4 (ordre adverse) : comme aucune place sans cellule n'apparaît en ordre tiré au hasard, l'ordre adverse a rejoué l'ordre au hasard, nombre pour nombre. Elle ne pouvait pas échouer.
5. **La recherche ciblée ajoutée après coup était aveugle.** Elle cherchait un contre-exemple parmi les 120 constituants des paliers 0 à 3. Le contre-exemple passe par des constituants des paliers 4, 5 et 6 pendant que deux places du palier 2 restent vides. Elle ne pouvait pas le voir ; je l'avais notée « recherche, non preuve », sans mesurer à quel point.
6. **Le moteur complet ne pratique pas la naissance que les contacts fixent.** Dans 10,4 à 14,7 % de ses naissances, le nouveau-né est lié à cinq constituants tous liés entre eux, ce qu'un tissu de contact de rang 3 interdit.
7. **Fautes de méthode de la séance, n° 39 à 41.** (39) L'instrument du contrôle M8 était incomplet à la première exécution du moteur : il ne pouvait pas contrôler les naissances où le parent n'est pas parmi les liens (1 à 2 %). Champ ajouté, moteur réexécuté, seul ce champ a changé ; déclaré dans le programme. (40) J'ai scellé avec M4 une clause dont la stratégie pouvait se réduire à une autre déjà scellée. (41) J'ai écrit dans la prédiction ce que K20 vraie « donnerait » avant d'avoir cherché sérieusement à la faire tomber.
8. **Ce qui n'est pas fait.** Le plus petit nombre de naissances d'un contre-exemple n'est pas connu : au moins 9 d'après mon énumération (le contre-audit l'a refaite jusqu'à 7 naissances), au plus 17. Rien ne démontre que la règle à la lettre de X-25 garde le tissu dans l'empilement au-delà du palier 3. La fréquence d'une sortie en ordre tiré au hasard n'est pas mesurée (aucune en vingt croissances de 70 naissances). L'outil passe par un filtre en nombres flottants avant son contrôle exact : il est sûr pour les coordonnées rencontrées ici, pas pour des croissances très profondes, que je n'ai donc pas éprouvées. Le compte des principes pour la trame régulière reste à faire. Aucune confrontation à une mesure.

## 263. Parole de l'auteur

23 novembre, 8 h 55, heure de Paris : « Go ».

En réponse à la suite proposée au carnet X-26, section 260 : éprouver dans la lecture de contact la mitose que pratique son moteur complet, celle d'un constituant dont le nouveau-né hérite des liens. Cette parole est enregistrée, non complétée.

## 264. La question, les lectures, les définitions

Le registre nomme le premier manque : une seule réalisation de la mitose tenue de bout en bout. Le tissu de contact de X-25 repose sur une lecture posée, « la naissance a lieu dans la cellule ». Peut-on la remplacer par la parole de l'auteur du 12 novembre, « les descendants sont liés et héritent des liens du parent » ?

Lectures, les miennes. Un lien est un contact. Les constituants sont ronds et ne se chevauchent pas. À chaque naissance, la forme du tissu reste fixée par ses seuls contacts (reprise de X-24). La naissance dans la cellule n'est pas posée.

- **Naissance héritée et fixée** : un nouveau-né rond qui touche son parent et trois voisins de son parent, les quatre étant indépendants, et qui ne chevauche rien. Deux places au plus ont ces quatre contacts.
- **Place admissible** : une place où une telle naissance est possible.
- **Place sans cellule** : place admissible dont les contacts ne contiennent aucun groupe de quatre constituants tous liés.
- **Empilement** : l'empilement complet né d'un germe de cinq constituants tous liés, celui de X-25. Ses constituants ont tous des coordonnées entières dans la base du germe.

Prédiction scellée avant tout calcul : `calculs/x27_mitose_avec_heritage_prediction.txt`, SHA-256 `d0e1e54de989fa8f6022dcc3edceee900914133c1f8cabddc6136ea0feccb502`, poussée à 8 h 10 UTC.

## 265. Ce qui est démontré

**K18 [T].** Du premier au cinquième constituant, la forme n'est fixée que si le nouveau-né touche tous les autres : un, deux, trois, quatre, cinq constituants tous liés. Preuve par le compte des libertés. Les transformations qui gardent les contacts forment un groupe à 10 paramètres. Celles qui fixent un constituant en gardent 6 ; deux constituants liés, 3 ; trois tous liés, 1 ; quatre tous liés, aucun. Un nouveau-né a 4 paramètres et chaque contact en retire un. Il est donc fixé s'il touche tous les présents, et il lui reste au moins une liberté s'il en manque un. Au rang 3, il n'y a pas six constituants tous liés : leur tableau de produits (1 sur la diagonale, −1 ailleurs) a un déterminant non nul, 2⁵ × (−4), alors que six vecteurs d'un espace de dimension 5 sont liés.

**K19 [T].** Au rang 2 (des disques sur une sphère ; le nouveau-né touche son parent et deux voisins du parent, les trois étant indépendants), quel que soit l'ordre des naissances, toute place admissible est le côté d'une cellule. Preuve. Les quatre disques du germe découpent la sphère en quatre triangles, bordés chacun par trois disques tous liés. Un nouveau-né tient dans un seul triangle et ne peut toucher que les trois disques qui le bordent. Il doit toucher trois constituants indépendants : ce sont eux. Il est donc le disque inscrit, côté libre de leur cellule, et le triangle devient trois triangles du même genre. Au rang 2, la naissance dans la cellule découle de l'héritage et de la forme fixée, et l'ordre ne change rien.

**K20a [T, sous un fait classique].** Au rang 3, si une place touche deux constituants liés a et b et deux autres constituants liés à la fois à a et à b, elle est dans l'empilement. Preuve. On envoie le point de contact de a et b à l'infini : a et b deviennent deux plans parallèles, et les constituants de l'empilement liés aux deux sont des sphères égales rangées en réseau triangulaire (structure classique de l'empilement de Soddy, contrôlée ici sur les 57 constituants liés aux deux premiers du germe parmi les 7 290 des paliers 0 à 6). L'argument suppose que toute paire de constituants liés est l'image de celle-là par le groupe ; ce n'est pas démontré ici, le contre-audit l'a constaté sur 14 292 paires. La place est une sphère égale, à un pas de deux points du réseau, distants entre eux d'un pas, de √3 pas ou de deux pas. Dans les trois cas, son centre est un point du réseau.

**K21 [T, exhibé].** Au rang 3, contrairement au rang 2, il existe des places sans cellule. Exemple, après 15 naissances dans une couche : la place (6, 6, 0, 3, −2), dans l'empilement, touche (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (4, 4, 1, 2, −2) et (5, 5, −1, 3, −1), dont les deux derniers ne sont pas liés. Les 60 places sans cellule des vingt croissances en couche sont toutes du genre que K20a couvre (contrôle ajouté).

## 266. K20 est fausse : le contre-exemple

**Le tissu.** Le germe et dix-sept naissances, dans cet ordre. Chacune est une naissance dans la cellule : le nouveau-né touche quatre constituants présents, tous liés entre eux. Coordonnées dans la base du germe ; le palier est celui que la règle à la lettre de X-25 donne au même constituant.

| Rang | Nouveau-né | Palier | Rang | Nouveau-né | Palier |
|---|---|---|---|---|---|
| 1 | (1, 1, 1, 1, −1) | 1 | 10 | (5, 3, 5, −1, −1) | 3 |
| 2 | (2, 0, 2, 2, −1) | 2 | 11 | (1, 1, 1, −1, 1) | 1 |
| 3 | (4, 1, 4, 2, −2) | 3 | 12 | (2, 2, 0, −1, 2) | 2 |
| 4 | (4, 2, 4, 1, −2) | 3 | 13 | (4, 4, 1, −2, 2) | 3 |
| 5 | (8, 2, 8, 2, −3) | 4 | 14 | (4, 4, 2, −2, 1) | 3 |
| 6 | (9, 3, 9, 1, −3) | 5 | 15 | (8, 8, 2, −3, 2) | 4 |
| 7 | (6, 3, 6, 0, −2) | 4 | 16 | (9, 9, 3, −3, 1) | 5 |
| 8 | (12, 4, 12, 0, −3) | 6 | 17 | (6, 6, 3, −2, 0) | 4 |
| 9 | (10, 4, 10, −1, −2) | 5 | | | |

22 constituants, 78 liens.

**La place.** x′ = (18, 18, 16, −6, −3) / 7.

- Sa norme vaut 1 : c'est une boule ronde.
- Son produit avec chacun des 22 constituants est inférieur ou égal à −1 : elle n'en chevauche aucun. Le plus proche des autres est à −11/7.
- Il vaut −1 pour quatre d'entre eux : (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (5, 3, 5, −1, −1) et (6, 6, 3, −2, 0). Le premier est lié aux trois autres : c'est le parent. Les quatre sont indépendants (déterminant −336).
- Ses coordonnées ne sont pas entières : elle n'est pas dans l'empilement.

C'est donc une place admissible, hors de l'empilement. [T]

**Quatre contrôles.** (a) L'outil des essais prédits, inchangé, la voit apparaître de lui-même à la dix-septième naissance et la classe « rationnelle non entière ». (b) Un contrôle direct, en entiers et fractions, sans cet outil. (c) Un contrôle de géométrie ordinaire, sans le produit qui sert partout ailleurs : deux constituants du germe deviennent deux plans parallèles, les vingt autres des sphères rangées entre eux ; x′ est une sphère de rayon 1 qui touche les deux plans et deux sphères, et reste à 0,27 au moins de toutes les autres. (d) Le contre-audit indépendant, section 271.

**Comment c'est possible.** Entre deux constituants liés, l'empilement range des constituants égaux en réseau triangulaire. Le tissu en fait naître huit (naissances 1, et 11 à 17) en contournant deux places du réseau, qu'il laisse vides. De l'autre côté, il descend par neuf petites naissances (2 à 10) jusqu'à un petit constituant logé sous ces deux places. Entre le dix-septième et le dixième, il y a alors la place d'un constituant de la taille du réseau, mais décalé. Il touche les deux constituants de départ, le dix-septième né et le dixième. Il chevauche les deux places laissées vides, (2, 2, 2, −1, 0) et (2, 2, 2, 0, −1), et rien de ce qui est né.

Ces deux places sont des constituants du palier 2 de l'empilement. La seconde est le côté libre d'une cellule du tissu depuis la naissance 1. La première est admissible depuis la naissance 10 et côté libre d'une cellule depuis la naissance 11. Le tissu a fait naître jusqu'au palier 6 sans les occuper.

Figure : `X-27_la_place_hors_de_l_empilement.png` (hors dépôt), tracée par `calculs/x27_contre_exemple_figure.py`.

**L'idée qui y a mené, vérifiée elle aussi.** Pour deux constituants liés p et q de l'empilement, la boule x = (q − 2p)/3 touche p au même point que q, contient q, chevauche tous les constituants liés à la fois à p et à q, et touche ceux qui sont logés contre p sous trois d'entre eux. Un tissu qui contient p et trois de ces derniers, sans q ni les autres, offre x. Avec p = (1, 0, 0, 0, 0) et q = (10, 8, 7, −2, −2) : x = (8, 8, 7, −2, −2)/3 devient une place admissible après 26 naissances, toutes dans la cellule ; ses trois voisins du parent ne sont pas liés entre eux. En chemin l'outil voit deux autres places hors de l'empilement : x′ à la naissance 17, et (226, 220, 208, −92, −19)/91 à la naissance 23. Les trois passent le contrôle direct.

## 267. Les douze clauses scellées

| Clause | Prédit | Obtenu | |
|---|---|---|---|
| M1 | tous les tissus de 5 naissances au plus (6 si possible) : aucune place hors de l'empilement | 0 à 6 naissances : 1, 5, 30, 200, 1 385, 9 876, 72 020 tissus ; 1 807 400 places, toutes dans l'empilement | vraie |
| M2 | aucune place sans cellule dans ces tissus | aucune | vraie |
| M3 | ordre au hasard, 20 × 70 naissances : aucune place hors | 5 410 places, aucune hors | vraie |
| M4 | ordre adverse, 20 × 70 : aucune place hors | identique à M3 | vraie, vide |
| M5 | dans une couche, 20 × 40 : aucune place hors ; places sans cellule dans 15 graines au moins | 2 854 places, aucune hors ; 19 graines sur 20 (60 places, 25 naissances) | vraie |
| M6 | ordre au hasard : places sans cellule dans 3 graines au moins | 0 graine sur 20 | **fausse** |
| M7 | règle à la lettre, paliers 0 à 3 : places admissibles = côtés libres des cellules de surface | 5, 20, 90, 330 places ; égalité exacte ; 142 815 quadruples examinés au palier 3 | vraie |
| M8 | moteur complet : tous les liens d'un nouveau-né vont au parent ou à ses voisins (contrôle) | 100 % dans les quatre états | vraie |
| M9 | moteur : lié au parent et à trois de ses voisins au moins, 70 à 88 % | 73,4 à 79,2 % | vraie |
| M10 | moteur : lié aux quatre membres d'un groupe de quatre tous liés, 45 à 70 % | 36,2 à 43,3 % | **fausse** |
| M11 | moteur : lié à cinq constituants tous liés, 4 à 20 % | 10,4 à 14,7 % | vraie |
| M12 | empilement, règle à la lettre : 4,70 à 4,85 liens par nouveau-né aux paliers 5 et 6, dont 4,10 à 4,20 vers de plus anciens | 4,80 et 4,754 ; 4,133 et 4,131 | vraie |

Dix vraies, dont une vide et un contrôle ; deux fausses. Et la conjecture qu'elles accompagnaient est fausse : aucune de ces clauses ne la mettait vraiment à l'épreuve.

Ajouts non prédits. Vingt croissances mixtes (25 naissances dans une couche, puis 45 en prenant d'abord les places sans cellule) : 5 286 places, toutes dans l'empilement ; places sans cellule dans 17 graines. Quadruples offrant deux places admissibles à la fois : 38 dans ces vingt tissus, dont 30 sont des cellules aux deux côtés libres. Dix croissances en file d'attente, ajoutées après le contre-exemple (on occupe toujours la place libre depuis le plus longtemps) : 2 950 places, toutes dans l'empilement.

## 268. Combien de naissances faut-il ?

Énumération complète de tous les tissus, à la symétrie du germe près (120 permutations des coordonnées) : 1, 1, 2, 6, 23, 117, 704, 4 783, 34 668 tissus pour 0 à 8 naissances. Toutes leurs places admissibles sont dans l'empilement, dont 956 840 pour les tissus de huit naissances. Un contre-exemple demande donc au moins 9 naissances. L'énumération est arrêtée à la main après ce niveau ; le contre-audit l'a refaite jusqu'à 7 naissances, avec les mêmes nombres. Le plus petit que j'ai trouvé en demande 17, et aucune de ses naissances ne peut être retirée. Le minimum est inconnu entre les deux.

## 269. Ce qui garde un tissu dans l'empilement

Fait [CERT, calcul exact]. Sous la règle à la lettre de X-25, où toutes les cellules de surface enfantent ensemble à chaque palier, les places admissibles sont exactement les côtés libres des cellules de surface, aux paliers 0 à 3 (clause M7).

Fait [CERT, calcul exact]. Quand on occupe toujours la place libre depuis le plus longtemps, dix croissances de 70 naissances n'offrent aucune place hors de l'empilement.

Fait [T]. Le contre-exemple laisse vides deux places libres du palier 2 et fait naître jusqu'au palier 6. La place hors de l'empilement chevauche ces deux places.

Hypothèse [H], non démontrée. Un tissu qui ne laisse aucune place libre de côté reste dans l'empilement. Les trois faits vont dans ce sens ; ils ne le prouvent pas.

Ce que cela change. Au rang 2, « lié au parent, hérite de ses liens, forme fixée » suffit à donner la naissance dans la cellule. Au rang 3, cela ne suffit pas. Les places admissibles ne dépendent que des constituants présents : ce qui compte, c'est quelles naissances possibles ont eu lieu et lesquelles ont été laissées de côté. Les sorties que je connais, trois places dans une même croissance, laissent vides des places libres ; quand aucune n'est laissée de côté, aucun calcul ne montre de sortie.

## 270. Le moteur complet de l'auteur

Quatre états de référence (660 et 1 037 constituants, graines 1 et 2), empreintes de X-24 retrouvées. Naissances relevées : 360, 737, 360, 737.

| | 1 / 660 | 1 / 1 037 | 2 / 660 | 2 / 1 037 |
|---|---|---|---|---|
| Tous les liens vont au parent ou à ses voisins | 100 % | 100 % | 100 % | 100 % |
| Lié au parent et à trois de ses voisins au moins | 79,2 % | 76,3 % | 77,5 % | 73,4 % |
| Lié aux quatre membres d'un groupe de quatre tous liés | 41,9 % | 37,9 % | 43,3 % | 36,2 % |
| Lié à cinq constituants tous liés | 14,7 % | 11,3 % | 14,7 % | 10,4 % |
| Liens par nouveau-né | 4,86 | 4,74 | 4,78 | 4,60 |

Le moteur hérite toujours : c'est écrit dans son code, et mesuré. Il fait naître dans une cellule deux fois sur cinq. Une fois sur huit, il fait ce que le contact de rang 3 interdit. Dans l'empilement, sous la règle à la lettre, un nouveau-né a 4 ou 5 liens à la fin de son palier, 4,75 en moyenne au palier 6 ; le moteur en donne 4,60 à 4,86, par un autre chemin.

## 271. Contre-audit indépendant

Un agent indépendant, avec son propre programme en arithmétique exacte, sans importer les miens. Rapport versé tel quel : `calculs/x27_contre_audit_rapport.md`.

**Aucune erreur de calcul.** Confirmés : les 17 naissances, chacune dans une cellule, avec exactement quatre contacts ; la place x′ (norme 1, quatre contacts, rang 4, un seul parent possible ; 52 places admissibles dans ce tissu, dont elle seule hors de l'empilement) ; son absence de l'empilement ; la réalisation en géométrie ordinaire, par une construction à lui, qui écarte toute erreur d'orientation ; le chevauchement des deux places laissées vides ; le second exemple à 26 naissances ; l'absence d'échappatoire dans le texte scellé ; les comptes de tissus jusqu'à 4 naissances sans réduction et jusqu'à 7 à la symétrie près ; K18.

**Trois corrections, acceptées.**

1. J'écrivais « l'ordre des naissances compte ». C'est inexact : les places admissibles ne dépendent que de l'ensemble des constituants présents. Ce qui compte, c'est quelles naissances ont eu lieu et lesquelles ont été omises. Corrigé dans ce carnet ; l'énoncé scellé de K20 reste cité tel qu'il a été scellé.
2. Dans ma demande de contrôle, je disais les deux places vides libres « pendant les 17 naissances ». Faux pour la première : elle n'est admissible qu'après la dixième naissance. Corrigé section 266.
3. K20a suppose que toute paire de constituants liés est l'image de la paire du germe par le groupe. Ce n'est pas démontré dans ce carnet ; le contre-auditeur l'a constaté sur 14 292 paires, sans exception.

**Antériorité.** Il n'a trouvé aucune source qui énonce ce fait et le juge élémentaire : dans le modèle des deux plans, c'est une sphère hors réseau dans une couche incomplète. Rien n'est à revendiquer.

**Non contrôlé par lui.** La clause M7 (règle à la lettre), le niveau 8 de l'énumération, les ajouts faits après sa saisine (file d'attente, genre des places sans cellule), les mesures sur le moteur complet.

## 272. Ce que cela donne, ce que cela ne donne pas

Ce que cela donne.

- Au rang 2, la naissance dans la cellule n'est plus une lecture posée : elle découle de la parole de l'auteur du 12 novembre et de la forme fixée par les contacts (K19). [T]
- Au rang 3, elle n'en découle pas (K20 fausse). Un tissu de contact peut sortir de l'empilement en ne faisant que des naissances dans la cellule. [T]
- La troisième lecture du tissu de contact reste donc posée au rang 3, ou doit être remplacée par une autre : qu'aucune place libre ne soit laissée de côté. Cette seconde forme n'est que constatée. [H]
- Rien de cela n'est revendiqué comme nouveau : c'est de la géométrie élémentaire de l'empilement de Soddy, appliquée à une lecture.
- Le moteur complet hérite toujours et ne pratique la naissance fixée par les contacts que dans une part de ses naissances. [CERT]

Un rapprochement, qui n'est pas une identité. L'auteur a dit : « La viabilité teste toutes les possibilités et est exempte de temps. » Dans ce calcul, le tissu reste dans l'empilement quand toutes les places libres sont prises, et peut en sortir quand un ordre en écarte certaines. Les mots se ressemblent. Rien ne dit que c'est la même chose.

Ce que cela ne donne pas. Ni temps, ni matière, ni loi. La rondeur reste posée. La forme fixée par les contacts est une lecture. Le nœud N1 du verrou V1 ne bouge pas : X-27 n'y ajoute pas d'énoncé. Il montre que la lecture « naissance dans la cellule », sur laquelle reposent X-25 et X-26, ne se déduit pas de l'héritage au rang 3. Le registre de validation garde ses comptes : 18 établis, 35 sous condition, 6 mesurés, 9 réfutés, 21 ouverts, 1 en tension ; dans le tissu de contact de rang 3, 13 tiennent, 15 en partie, 8 ne tiennent pas. Trois lignes changent de texte, aucune d'état.

**La cosmogonie n'est pas validée. Elle n'est pas réfutée non plus.**

## 273. La suite proposée

Une seule : chercher à démontrer, ou à faire tomber, que la règle à la lettre garde le tissu dans l'empilement à tout palier. Si c'est vrai, la naissance dans la cellule devient au rang 3 un théorème sous une condition simple, que toutes les cellules enfantent ensemble. Si c'est faux, la naissance dans la cellule reste une lecture posée, sans autre appui.

## 274. Fichiers et sources

- Prédiction scellée : `calculs/x27_mitose_avec_heritage_prediction.txt`.
- Essais prédits : `calculs/x27_mitose_avec_heritage.py` et sorties `x27_partie_A`, `x27_partie_B_hasard`, `x27_partie_B_adverse`, `x27_partie_B_couche`, `x27_partie_C`, `x27_partie_E` (`.json`, `.out`).
- Moteur complet : `calculs/x27_moteur_naissances.py`, `.json`, `.out`.
- Ajouts non prédits : `calculs/x27_complement.py` et ses sorties (exemple de place sans cellule, croissances mixtes, recherche ciblée, file d'attente).
- Contre-exemple : `calculs/x27_contre_exemple.py`, sorties `x27_contre_exemple_court`, `x27_contre_exemple_toit` (`.json`, `.out`), `x27_contre_exemple_symetrie.out` ; figure par `calculs/x27_contre_exemple_figure.py`.
- Contre-audit : `calculs/x27_contre_audit_rapport.md`.

Sources :

- F. Soddy, « The bowl of integers and the hexlet », *Nature* 139 (1937), p. 77.
- D. W. Boyd, « The osculatory packing of a three dimensional sphere », *Canadian Journal of Mathematics* 25 (1973), p. 303 à 322.
- R. L. Graham, J. C. Lagarias, C. L. Mallows, A. R. Wilks, C. H. Yan, « Apollonian circle packings: geometry and group theory III. Higher dimensions », *Discrete & Computational Geometry* 35 (2006), p. 37 à 72.

**TOE 0/7. Aucun verrou fermé.**
