# Carnet du 22 novembre 2026, soir — X-24 : du contact au groupe de Lorentz ; ce qui porte l'étage dans le moteur complet

Auteur unique : Rudolphe Mirante. Pilote IA et contre-auditeur : Claude (modèle claude-fable-5-2). Contre-audit et recoupement indépendants : deux agents Claude sans accès à mes programmes ni à mes résultats (indépendance de programme, non de lignée : même famille de modèles que le pilote). Audit croisé avec ChatGPT : aucun ce soir, aucun message envoyé. Les numéros de section poursuivent ceux du carnet X-23 du même jour.

**État en tête : TOE 0/7. Aucun verrou fermé.**

## 221. Ce qui est faux, dit en premier

**Mes trois hypothèses sur le moteur complet sont fausses.**

1. **H-PORTE** (énoncé central de la partie B) : « l'étage le plus haut qui gèle suit le nombre de liens donnés au nouveau-né, non la dimension de l'espace des points ». La moitié « dimension » tient en dimension 3, 4 et 5. La moitié « liens du nouveau-né » est fausse : avec huit liens par naissance (κ = 8,6), le moteur complet se défait de ses liens jusqu'à 6,2–6,7 voisins et reste à l'étage 3 ; l'étage 4 y est à 0,9–2,0 %.
2. **H-QUATRE** (X-24 bis) : « l'étage le plus haut qui gèle vaut la taille du groupe qui se défait, moins un ». Réfutée par son propre critère scellé : avec des groupes de cinq et κ = 8,6, sans force, l'étage 5 gèle à 1 037 constituants (66 % et 58 %) ; et avec les groupes de quatre de l'auteur, κ = 8,6, sans force, l'étage 4 gèle (65,5 à 75,5 %).
3. **H-BORD** (X-24 ter) : « à κ = 8,6, c'est la force de bord qui retient le moteur à l'étage 3 ». Réfutée : sans la force de bord, le moteur reste à 6,4–6,9 voisins et l'étage 4 sous 3 % dans trois relevés sur quatre (21 % dans le quatrième). C'est sans la force « grav » qu'il monte : 7,0–7,1 voisins, étage 4 gelé à 1 037 constituants (52 % et 51 %).

**Autres prédictions scellées fausses.**

4. **B1** : budget entre 5,3 et 6,2 voisins en dimension 2, 4 et 5. Faux pour 1 relevé sur 12 (6,45 en dimension 5).
5. **B2**, clause sur la dimension 2 (confiance 55 %) : étage 3 gelé. Faux : 10 à 17 %.
6. **B3** : étage 4 sous 5 % en dimension 5. Faux pour la graine 1 : 46 % et 37 %.
7. **B4** : à κ = 8,6, budget entre 7,0 et 8,3 voisins et étage 4 gelé. Faux deux fois : 6,2 à 6,7 voisins, étage 4 à 2 % au plus.
8. **B5** : à κ = 4,6, budget entre 3,6 et 4,5 voisins. Faux : 4,8 à 5,0, le moteur *ajoute* des liens. Étage 3 sous 10 % : faux pour 1 relevé sur 4 (11,2 %).
9. **Q1** : sans désintégration, « plus de 9 voisins » puis « plus de 12 voisins ». Faux : 7,9–8,2 et 10,0–10,7. Les étages annoncés gelés le sont.
10. **Q2** : « étage 5 non gelé avec des groupes de cinq ». Faux à κ = 8,6 (point 2).
11. **Q4** : groupes de quatre, κ = 8,6, sans force : « 6,3 à 7,2 voisins, étage 4 sous 5 % ». Faux deux fois : 7,4–7,7 voisins, étage 4 gelé.
12. **Q5** : fausse en partie (section 229).
13. **F1** fausse dans ses deux clauses ; **F2** fausse pour « grav », et pour « em » dans deux relevés sur quatre (12 et 13 % à l'étage 4).
14. **L2** (X-24 quater) : exposant de décroissance annoncé entre 1,5 et 4. Faux pour deux naissances sur trois (5,1).
15. **N1** : résidu de tangence annoncé sous 10⁻⁹. Manqué pour 1 calcul sur 120 (2,3 × 10⁻⁹). Cause identifiée : l'arithmétique flottante de la disposition de proche en proche ; le même calcul mené à 60 chiffres donne 6,7 × 10⁻⁵¹.

Soit vingt-deux clauses fausses, comptées une à une, sur les quatre scellés de la soirée.

**Fautes de méthode et écarts.**

16. X-24 bis, ter et quater sont des compléments décidés en voyant les résultats précédents. Chacun a sa prédiction scellée avant calcul ; aucun n'est aveugle.
17. Les quatre scellés sont des empreintes horodatées par le Projet de l'auteur et des commits locaux datés, non des dépôts publics poussés avant calcul.
18. La prédiction de X-24 ter contenait une phrase inexacte sur Q5. Je l'ai corrigée avant de la sceller : l'empreinte donnée est celle du texte corrigé.
19. Ajouts après exécution, déclarés : le programme de la partie A a reçu un mode de contrôle pour le point 15 ; le programme de X-24 bis a reçu le mode d'ablation de X-24 ter ; le programme de X-24 quater a reçu une mesure de son bruit. Les plans scellés n'ont pas changé. J'avais d'abord écrit, sans le mesurer, que le changement dû à une naissance passait sous le bruit au-delà de 13 liens : la mesure du bruit dit le contraire (section 227).
20. Les sorties de la partie B, écrites une par exécution, ont été regroupées en un fichier par expérience après contrôle ligne à ligne (76 relevés).
21. Le contrôle N3 (signature) est vrai par construction dès que l'empilement existe : il ne teste rien de plus que N1.
22. **« Groupe de symétrie de la forme » : formule inexacte.** Je l'ai employée dans le statut visé du scellé et dans un message à l'auteur (21 h 35 UTC). Le contre-audit l'a relevée : une forme donnée n'a qu'un nombre fini de symétries. Ce qui est vrai : la forme n'est définie qu'à une transformation de Lorentz près, et ce groupe vient avec la rondeur que je pose (section 226).
23. Deux énoncés corrigés par le contre-audit : K7 disait « unique à une rotation près » là où il faut « à une isométrie près » ; K1 ne précisait pas le groupe du cercle. Un passage manquait à K2 (le complémentaire global).

## 222. Paroles de l'auteur prises comme point de départ

- 13 novembre : « Le simplexe est la forme la plus infinitésimale possible, avant même la matière ; ce n'est pas une notion de distance mais de contact. »
- 12 novembre : « Un simplexe ne peut pas en chevaucher un autre à sa naissance » (« à tester ») ; « La première fermeture bloque la mitose ».
- 12 novembre : « L'énergie n'appartient pas au simplexe. »
- 13 novembre : « La vitesse de la lumière est liée à la causalité : la vitesse maximale est celle de la mitose. »
- 20 novembre : « Tu dois définir chaque règle de ces évolutions et étages pour en comprendre la mécanique et la logique. »
- 22 novembre, 21 h 10 UTC : « Pousse au delà de tout, allons bien loin que tout ce que nous avons atteint à ce jour ! Ton fil conducteur la cosmogonie et le résultat est la validation de la toe. »

Ces paroles sont enregistrées, non complétées. Les lectures ci-dessous sont les miennes.

**Le point faible de X-23 que cette soirée attaque.** Son théorème supposait qu'un lien tient une distance, demandait des positions génériques, et laissait posé l'espace à trois dimensions des moteurs.

## 223. Mes lectures, déclarées (hypothèses d'auditeur, non paroles de l'auteur)

- **C1.** Un lien est un contact, non une distance tenue : deux constituants liés se touchent, deux constituants non liés ne se touchent pas, aucun n'en chevauche un autre.
- **C2.** Le contact d'un constituant est rond : un constituant n'a aucune direction privilégiée. Dans un espace de contacts de dimension k (la sphère S^k), un constituant est une calotte ronde.
- **C3.** (= L3 de X-23) Coque fermée de rang k = sphère de cellules de dimension k. La plus petite est le bord du simplexe : k+2 constituants tous en contact.
- **C4.** (= L4 de X-23) Mitose de l'arête de C-116.

*Réalisation par contacts* d'une coque de rang k : des calottes rondes de S^k, d'intérieurs disjoints, tangentes exactement le long des liens. Deux réalisations sont *la même* si une transformation de Möbius de S^k envoie l'une sur l'autre : ce sont les transformations de la sphère qui envoient toute calotte ronde sur une calotte ronde (pour le cercle, le groupe projectif PGL(2,R)).

*Écriture commode.* Une calotte de S^k est un vecteur u de l'espace de Minkowski à (k+1)+1 dimensions, de carré ⟨u,u⟩ = 1. Deux calottes se touchent si ⟨u,v⟩ = −1 ; elles sont disjointes si ⟨u,v⟩ < −1. Ce produit, dit inversif, ne change pas sous les transformations de Möbius. Les produits fixent la configuration au signe global près : des deux configurations u et −u (toutes les calottes remplacées par leurs complémentaires), une seule est faite de calottes d'intérieurs disjoints.

## 224. Partie A — ce qui se démontre

Prédiction scellée avant tout calcul : `calculs/x24_contact_et_porteur_de_l_etage_prediction.txt`, SHA-256 `d287d0a3fa12fc54313064f13cc957147229992665bee313d92c74e753b8bf95` (22 novembre, 21:34:04 UTC). Ce sont des mathématiques classiques assemblées ; je n'en revendique aucune.

**K1 — Rang 1 [T].** Un polygone à V constituants se réalise par V arcs qui se touchent bout à bout et font le tour du cercle. Une réalisation est donc la donnée des V points de contact. Le groupe de Möbius du cercle a trois paramètres et place trois points où l'on veut : il reste V−3 paramètres libres. La réalisation n'est unique que pour le triangle. C'est le même nombre que les V−3 mécanismes de X-23 (A3) : le polygone ne tient pas.

**K2 — Rang 2 [T].** Toute coque de triangles a une réalisation par contacts, et une seule : c'est le théorème de Koebe, Andreev et Thurston sur les empilements de cercles. La mitose de l'arête garde une coque de triangles. Donc à chaque naissance, quel que soit le lien qui se divise, la coque a une forme et une seule, sans aucune hypothèse de position générique.

**K3 — Rangs 3 et plus [T].** Il existe des coques nées par mitose qui n'ont aucune réalisation, dès la deuxième naissance. *Preuve.* Partons du bord du simplexe, k+2 constituants numérotés de 1 à k+2. La mitose du lien (1,2) crée un constituant w lié à tous les autres et retire le lien (1,2). Le lien (3,4) est alors entouré de k+1 constituants (1, 2, w, 5, …, k+2). Sa mitose crée w′, lié à tous, et retire (3,4). Le réseau obtenu est le graphe complet à k+4 constituants privé des deux liens (1,2) et (3,4). Supposons-le réalisé. Envoyons à l'infini le point de contact de w et w′ : ces deux calottes deviennent deux demi-espaces à bords parallèles, et tous les autres constituants, qui touchent w et w′, sont des boules égales, de rayon 1, centrées dans l'hyperplan médian. Les k−2 constituants 5, …, k+2 se touchent deux à deux : leurs centres forment un simplexe régulier de côté 2. Les constituants 1, 2, 3 et 4 les touchent tous : leurs centres sont sur un cercle de rayon ρ, avec ρ² = 2(m+1)/m et m = k−2, donc ρ² > 2. Sur ce cercle, deux boules en contact sont séparées par un angle θ = 2 arcsin(1/ρ), strictement inférieur à un quart de tour. Or les contacts 1–3, 3–2, 2–4, 4–1 demandent une chaîne fermée de quatre boules : la somme de quatre pas, chacun de +θ ou de −θ, doit faire un nombre entier de tours. Quatre pas dans le même sens font 4θ < 2π ; trois contre un font 2θ < π ; deux contre deux ramènent une boule sur une autre. Contradiction. Pour k = 3 le cercle a le rayon 2 : c'est le sextuplet de Soddy, qui se ferme en six boules, jamais en quatre. L'échec dépend du lien choisi : le départ et la première naissance ont toujours une forme, et une seule ; la forme disparaît, par exemple, quand la seconde naissance se fait sur un lien sans constituant commun avec le premier.

**K4 — Conséquence [T].** « Toute coque née par mitose a une réalisation par contacts, et une seule » est vrai au rang 2 et à lui seul. Au rang 1 la forme n'est pas fixée ; aux rangs 3 et plus, certaines naissances n'ont aucune forme.

**K5 — Le groupe [T].** Au rang 2, la forme n'est définie qu'à une transformation de Möbius de la sphère S² près. Ce groupe est le groupe de Lorentz de l'espace-temps à 3+1 dimensions (O⁺(3,1) avec les réflexions, SO⁺(3,1) sans) : il agit sur les vecteurs u de l'écriture ci-dessus. En général, le groupe de Möbius de S^k est le groupe de Lorentz à (k+1)+1 dimensions : chaque rang a le sien. Ce que K4 choisit, c'est le rang, et par lui 3+1. **Ce groupe n'est pas le groupe de symétrie d'une coque**, dont la forme n'a qu'un nombre fini de symétries. C'est le groupe des changements de point de vue qui conservent ce dont parlent C1 et C2, des calottes rondes et leurs contacts : il vient avec la rondeur posée.

**K6 — Le nombre quatre [T].** Sur S^k, au plus k+2 calottes se touchent deux à deux. *Preuve.* La matrice des produits de n calottes toutes en contact vaut 1 sur la diagonale et −1 ailleurs ; elle a n−1 valeurs propres égales à 2, alors que l'espace n'a que k+1 directions de genre espace. Au rang 2 : quatre constituants au plus, jamais cinq.

**K7 — La forme canonique [T].** La réalisation du rang 2 donne un polyèdre convexe dont toutes les arêtes sont tangentes à la sphère (polyèdre de Koebe), unique à une transformation de Lorentz près, et unique à une isométrie de la sphère près (rotation ou symétrie) une fois centré (Springborn 2005). Convexe et à faces triangulaires, il est infiniment peu déformable (Dehn 1916) : la coque y tient l'étage 3, sans mécanisme ni lien superflu, sans hypothèse générique. Ses cellules sont les faces d'un polyèdre convexe : aucune n'en chevauche une autre, à aucune naissance.

**Le compte.** Une coque de triangles a 3V − 6 liens. Les contacts posent 3V − 6 conditions sur 3V inconnues, et le groupe de Lorentz a 6 paramètres. C'est le compte de Maxwell de X-23, où les six déplacements d'ensemble de l'espace (trois rotations, trois translations) sont remplacés par les six transformations de Lorentz (trois rotations, trois changements de vitesse).

**Deux remarques, démontrées elles aussi.**

- *Le doublement s'arrête à quatre.* Le corpus fait naître les porteurs par doublement avec héritage complet des liens : 1, 2, 4 (C-135c). Au rang 2, le pas suivant est impossible : huit constituants ne peuvent pas tous se toucher (K6).
- *La première naissance.* Sur le tétraèdre creux, la mitose d'un lien sépare les deux parents : leur produit inversif passe de −1 (contact) à −7 exactement. Avec deux naissances sur deux liens opposés, la coque est l'octaèdre et les trois paires opposées sont à −3. Au rang k, le contre-audit donne −(1 + 2(k+1)/(k−1)) après une naissance : −7, −5, −13/3 aux rangs 2, 3, 4.

## 225. Vérifications numériques de la partie A

Programme `x24_contacts.py`. Empilement calculé par la méthode de Newton sur les sommes d'angles, puis disposé de proche en proche ; contrôles en arithmétique flottante, et à 60 chiffres pour 34 coques jusqu'à 40 constituants.

**Rang 2 : 60 coques nées par mitose uniforme (6 graines ; 4 à 300 constituants).**

| Contrôle | Résultat |
|---|---|
| N1. Une forme est trouvée | 60 sur 60 ; résidu de tangence relatif au plus 2,7 × 10⁻¹⁰ au premier calcul ; 2,3 × 10⁻⁹ pour un des 120 calculs (seuil manqué, point 15) |
| Aucun chevauchement | 60 sur 60 ; le plus grand produit entre constituants non liés vaut −1,18 |
| N2. Unicité : deux calculs depuis deux faces extérieures différentes | Mêmes produits inversifs pour toutes les paires ; écart relatif au plus 5,8 × 10⁻⁹ |
| N3. Rang 4 et signature (3,1) de la matrice des produits | 60 sur 60 (vrai par construction) |
| N4. Rigidité : noyau du jacobien des contacts | Dimension 6 pour 60 coques sur 60 ; à 60 chiffres pour 34 coques : dimension 6, égale à l'action des six générateurs de Lorentz |
| N5. Polyèdre de Koebe centré | Convexe, mêmes faces que la coque : 60 sur 60 ; arêtes tangentes à 1,9 × 10⁻¹¹ près ; rang de rigidité 3V − 6 : 60 sur 60, confirmé à 60 chiffres pour 34 |

Les constituants d'une même coque ont des tailles très inégales : dans la forme centrée, leurs rayons angulaires vont de 0,02° à 76°. La mitose uniforme fait de gros constituants anciens et une poussière de jeunes.

**Rang 1 (N6).** Noyau de dimension V pour V = 4 à 12 (3 de symétrie, V−3 libertés) ; dimension 3 pour le triangle.

**Rangs 3, 4 et 5 (N7).** Recherche par moindres carrés, 200 départs, chevauchements comptés.

| Rang | Départ (k+2 constituants) | Une naissance | Deux naissances |
|---|---|---|---|
| 3 | forme trouvée, noyau 10 | forme trouvée, noyau 10 | aucune : plus petit résidu 0,90 |
| 4 | forme trouvée, noyau 15 | forme trouvée, noyau 15 | aucune : plus petit résidu 0,76 |
| 5 | forme trouvée, noyau 21 | forme trouvée, noyau 21 | aucune : plus petit résidu 0,66 |

Si l'on cesse de compter les chevauchements, la recherche trouve des « solutions » de résidu 10⁻¹⁶ où deux boules sont confondues : c'est le cas dégénéré que la preuve de K3 écarte.

**Recoupement indépendant.** Un agent, sans mes programmes, a calculé à sa façon les empilements de 12 coques (4 à 20 constituants, graines 0 et 1) : **630 produits inversifs sur 630 identiques aux miens**, écart relatif au plus 4 × 10⁻¹³.

## 226. Contre-audit indépendant de la partie A

Un agent Claude, sans mes programmes ni mon raisonnement, a reçu les sept énoncés avec la consigne de les réfuter. Il a écrit son propre code et vérifié les références en ligne.

**Verdicts.** K1, K3, K4 et K6 : démontrés par lui. K2, K5 et K7 : vrais par la littérature, qu'il a vérifiée. Aucun énoncé réfuté. Numérique : sur 12 coques, noyau de dimension 6, rang 3V − 6, polyèdre strictement convexe, aucun chevauchement. Pour K3, 300 départs : plus petit résidu 0,90 au rang 3 et 0,76 au rang 4, comme les miens.

**Ce qu'il corrige.**

1. K7 : le représentant centré de Springborn est unique à une isométrie près, symétries comprises, et non « à une rotation près ». Corrigé.
2. K1 : sur le cercle, toute transformation est conforme ; le groupe de Möbius du cercle doit être défini comme le groupe projectif PGL(2,R). Corrigé (section 223).
3. K2 : les produits ne distinguent pas une configuration de son complémentaire global. Une seule des deux est un empilement ; il faut le dire pour conclure à l'unicité. Ajouté (section 223).
4. K3 : sa preuve, par la matrice des produits, est plus forte que la mienne. Aucune forme n'existe même si l'on tolère que des constituants non liés se chevauchent : la seule issue algébrique est que deux constituants soient confondus. Il précise que l'échec dépend du lien choisi.

**Ce en quoi ma phrase de synthèse disait trop. Ses sept points sont justes.**

1. Chaque rang a « son » groupe de Lorentz. Le rang 2 n'est distingué que par l'existence et l'unicité de la forme, non par le fait d'avoir un tel groupe.
2. **Ce groupe n'est pas le groupe de symétrie d'une coque.** C'est l'équivalence que j'ai posée entre réalisations ; les symétries d'une forme donnée sont en nombre fini.
3. C'est un isomorphisme abstrait avec le groupe des isométries de l'espace hyperbolique à trois dimensions. La construction ne contient ni temps, ni causalité, ni métrique, ni dynamique.
4. Avec les réflexions, le groupe est O⁺(3,1), non SO⁺(3,1).
5. Le résultat dépend des définitions : contact si et seulement si lien, mitose de l'arête seule, équivalence de Möbius. Avec des chevauchements réglés, la réponse change.
6. Au rang 3, l'échec ne touche que certains choix de liens ; le départ et la première naissance ont une forme.
7. L'unicité au rang 2 est le théorème de Koebe, Andreev et Thurston, non un résultat nouveau.

*Ma réponse au point 2, pour ne rien retirer de trop.* L'équivalence de Möbius n'est pas un choix libre : c'est le groupe de toutes les transformations de la sphère qui envoient les calottes rondes sur des calottes rondes. Mais cela revient à dire qu'elle est apportée par la lecture C2 : poser des constituants ronds, c'est poser cette géométrie, et son groupe avec elle.

**Antériorité.** L'écriture des cercles comme vecteurs d'un espace de Minkowski est connue : Graham, Lagarias, Mallows, Wilks et Yan (arXiv:math/0010298) ; Kocik (arXiv:0706.0372) ; Stange, qui parle d'empiler des cercles dans l'espace-temps et nomme SO⁺(1,3) (arXiv:1208.4836). L'action du groupe de Lorentz sur la sphère céleste par transformations de Möbius est classique (Penrose et Rindler ; Oblak, arXiv:1508.00920). Thurston tire l'unicité de la rigidité de Mostow dans l'espace hyperbolique. D'après le contre-audit, Chen (2016, théorème 3.3) montre que trois boules mutuellement tangentes et un cycle de boules qui les touchent toutes ne s'empilent que si le cycle en compte six : c'est K3 au rang 3. Ni l'agent ni moi n'avons trouvé de source qui tire « 3+1 » de l'unicité des empilements. La recherche a été limitée : ce n'est pas une preuve de nouveauté. J'ai vérifié moi-même le titre et les auteurs de quatre de ces références.

## 227. Ce que la partie A dit des paroles de l'auteur, et ce qu'elle ne dit pas

| Parole | Traduction sous C1–C4 | Statut |
|---|---|---|
| « ce n'est pas une notion de distance mais de contact » | Les seuls contacts fixent la forme de la coque de triangles, à une transformation de Lorentz près ; à aucun autre rang | [T] sous mes lectures |
| « La première fermeture bloque la mitose » ; l'arrêt à quatre porteurs (nœud N1) | Quatre constituants ronds au plus se touchent tous ; le doublement 1, 2, 4 ne peut pas continuer | [T] sous C1–C3, au rang 2 |
| « Un simplexe ne peut pas en chevaucher un autre à sa naissance » | Au rang 2, les cellules sont les faces d'un polyèdre convexe à chaque naissance ; aux rangs ≥ 3 certaines naissances n'ont aucune forme sans chevauchement | [T] sous mes lectures |
| « L'énergie n'appartient pas au simplexe » | La forme est fixée sans ressort ni énergie | Compatible |
| « la vitesse maximale est celle de la mitose » | Pour deux constituants liés, le vecteur u + v est de genre lumière ; pour deux constituants non liés, il est de genre temps | [T] pour la géométrie, [H] pour tout sens physique |

**Ce que cela ajoute à X-23.** Trois réserves tombent : la distance tenue n'est plus posée (contact), la position générique n'est plus demandée (la forme canonique est convexe, donc rigide), et le nombre quatre sort de K6 au lieu d'être admis. Le groupe de Lorentz à 3+1 dimensions y apparaît, mais comme le groupe de la géométrie des contacts ronds, que la lecture C2 apporte avec elle : ce que le théorème choisit, c'est le rang. C-117 avait obtenu, de son côté, une vitesse unique au premier ordre pour des ondes.

**Ce que cela ne dit pas.**

1. Que l'espace-temps a 3+1 dimensions. Le théorème dit : *si* un lien est un contact, *si* un constituant est rond, *si* la fermeture est une sphère de cellules, alors le seul rang où toute naissance garde une forme unique est le rang 2, et cette forme n'est définie qu'à une transformation de Lorentz près. Les trois « si » sont posés.
2. Que ce groupe agit sur une physique. Ce n'est pas même le groupe de symétrie d'une forme : c'est celui des changements de point de vue d'une géométrie de contacts, et il vient avec la rondeur posée, à tout rang. Il n'y a ici ni temps, ni mouvement, ni limite continue, ni courbure.
3. Que les constituants vivent dans un espace à trois dimensions. Ils sont rangés sur une sphère à deux dimensions ; le 3 est la dimension du polyèdre, le 3+1 celle de l'espace où s'écrivent les vecteurs.
4. Que la rondeur est dérivée. C2 est posé. Avec des formes non rondes, des empilements existent encore, mais le groupe est perdu.
5. Que le résultat vaut au-delà de la sphère. Comme dans X-23, un tore se comporterait autrement.
6. Que le résultat survit à d'autres définitions. Si l'on admet des chevauchements réglés entre constituants, ou d'autres naissances que la mitose de l'arête, la conclusion change.
7. Qu'aux rangs 3 et plus rien ne tient. L'échec n'y vient que de certains choix de liens ; le départ et la première naissance ont une forme unique.

**Limite mesurée : la forme est un problème global (X-24 quater).** Prédiction scellée : `x24quater_localite_d_une_naissance_prediction.txt` (`9da00ca9…580a`). Sur la coque régulière née par mitose synchrone (octaèdre, puis g paliers où chaque cellule se divise une fois : 8 × 2^g cellules, l'analogue à deux dimensions de C-116), j'ajoute une naissance et je compare, lien par lien, un invariant local de la forme avant et après. Résultat à 1 026 constituants, trois naissances :

| Distance au lien divisé (en liens) | 1 | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|
| Changement relatif médian, naissance 1 | 1,0 × 10⁻² | 1,2 × 10⁻³ | 1,8 × 10⁻⁴ | 4,8 × 10⁻⁵ | 1,7 × 10⁻⁵ | 6,9 × 10⁻⁶ | 4,3 × 10⁻⁶ |
| Changement relatif médian, naissances 2 et 3 | 5,3 × 10⁻³ | 6,2 × 10⁻⁴ | 3,4 × 10⁻⁵ | 3,3 × 10⁻⁶ | 7,6 × 10⁻⁷ | 2,2 × 10⁻⁷ | 7,3 × 10⁻⁸ |

Une naissance change la forme partout (L1 tenue), faiblement au loin (L3 tenue). De 2 à 12 liens, la décroissance suit mieux une loi de puissance qu'une exponentielle, avec un exposant de 3,3 pour un type de lien et de 5,1 pour l'autre (L2 fausse sur l'exposant). Bruit du calcul, mesuré après coup en calculant la même coque depuis deux faces extérieures : médiane 10⁻¹², au plus 5 × 10⁻¹⁰. Le changement reste au-dessus de ce bruit jusqu'au bout de la coque : 10⁻⁷ à 24 liens pour la naissance 1, 2 × 10⁻⁹ à 27 liens pour les deux autres. **Conséquence : dans cette lecture, la forme se réajuste d'un seul coup sur toute la coque. Il n'en sort aucune vitesse de propagation. La causalité demandée par V1 n'est pas dérivée.** Les naissances 2 et 3 sont images l'une de l'autre par une symétrie de la coque : elles comptent pour une. Non recoupé.

## 228. Partie B — le moteur complet en dimension 2, 4 et 5, puis avec κ = 4,6 et 8,6

Moteur `blob ablation labo colab.py` du corpus, exécuté après remplacement de texte en six endroits, comptés un par un : la valeur de κ ; la dimension D des points au tirage de départ et au déplacement du nouveau-né ; le volume de la boule unité dans le rayon de départ ; les trois longueurs absolues du source (0,10 ; 0,32 ; 0,45), multipliées par le rapport des rayons de départ. **Contrôle zéro (B0) tenu** : à D = 3 et κ = 6,6, la variante redonne exactement les liens et les positions du moteur non modifié (graines 1 et 2, 660 et 1 037 constituants). Quatre forces, graines 1 et 2, relevés à 660 et 1 037 constituants, arithmétique exacte. Dans chaque case : graine 1 puis graine 2 à 660, puis de même à 1 037. Plus grand amas rigide en % des constituants.

| D | κ | Voisins | Étage 2 | Étage 3 | Étage 4 |
|---|---|---|---|---|---|
| 2 | 6,6 | 5,43 ; 5,47 ; 5,53 ; 5,45 | 75 ; 71 ; 89 ; 84 | **17 ; 12 ; 16 ; 10** | 0,9 ; 3,2 ; 1,2 ; 1,7 |
| 3 | 6,6 | 5,85 ; 5,84 ; 5,88 ; 5,69 | 87 ; 93 ; 87 ; 88 | **60 ; 71 ; 66 ; 67** | 0,9 ; 1,4 ; 0,9 ; 0,6 |
| 4 | 6,6 | 6,16 ; 6,11 ; 6,00 ; 5,89 | 91 ; 91 ; 90 ; 88 | **74 ; 77 ; 69 ; 72** | 0,9 ; 1,2 ; 0,6 ; 0,6 |
| 5 | 6,6 | 6,45 ; 6,05 ; 6,10 ; 5,59 | 86 ; 88 ; 84 ; 84 | **75 ; 70 ; 65 ; 59** | 46 ; 0,8 ; 37 ; 0,6 |
| 3 | 4,6 | 4,79 ; 4,85 ; 5,00 ; 4,91 | 82 ; 84 ; 85 ; 85 | 11 ; 2,6 ; 9,5 ; 2,2 | 0,8 ; 0,9 ; 0,5 ; 0,6 |
| 3 | 8,6 | 6,69 ; 6,50 ; 6,24 ; 6,22 | 95 ; 94 ; 92 ; 92 | **83 ; 76 ; 77 ; 78** | 2,0 ; 1,5 ; 0,9 ; 0,9 |

L'étage 5 est à 0,9 % au plus dans les 24 relevés.

**Lecture, sans embellir.**

1. **Ce n'est pas l'espace à trois dimensions des points qui fait l'étage 3.** Avec des points à quatre ou cinq dimensions, le moteur reste à l'étage 3 et ne monte pas au 4. Une exception partielle : en dimension 5, graine 1, un amas de l'étage 4 couvre 46 % puis 37 % des constituants, sous le seuil de gel.
2. **Le plan, lui, abaisse l'étage.** Avec des points à deux dimensions, le moteur garde 5,4 à 5,5 voisins mais ne gèle que l'étage 2.
3. **Le nombre de liens du nouveau-né ne le fait pas non plus.** De 4 à 8 liens par naissance, l'apport brut double ; le budget, lui, ne va que de 4,8 à 6,7 voisins. Le moteur règle son budget.

## 229. X-24 bis — le groupe qui se défait

Prédiction scellée : `x24bis_groupe_qui_se_defait_prediction.txt` (`d2e6d730…f598`, 21:41:02 UTC). Le seul puits de liens systématique du socle est la désintégration des groupes de quatre constituants tous liés : à chaque tour, un groupe d'âge a perd un lien avec la probabilité 0,236 exp(−a/8). C'est aussi la seule règle du socle qui nomme un nombre. Variantes : groupes de trois, de cinq, ou aucune désintégration. **Contrôle zéro (Q0) tenu.** D = 3, mêmes relevés, étages 2 à 6.

| Forces | Groupe qui se défait | κ | Voisins | Étage 3 | Étage 4 | Étage 5 | Étage 6 |
|---|---|---|---|---|---|---|---|
| aucune | trois | 6,6 | 4,31 ; 4,50 ; 4,19 ; 4,21 | 2,0 ; 1,5 ; 1,3 ; 1,5 | < 1 | < 1 | < 1 |
| aucune | quatre | 6,6 | 6,28 ; 6,47 ; 6,62 ; 6,50 | **78 ; 84 ; 77 ; 81** | 0,8 ; 0,8 ; 7,2 ; 1,6 | < 1 | < 1 |
| aucune | quatre | 8,6 | 7,72 ; 7,49 ; 7,73 ; 7,41 | 90 ; 86 ; 87 ; 82 | **75 ; 69 ; 72 ; 65** | < 1 | < 1 |
| aucune | cinq | 6,6 | 7,31 ; 7,55 ; 7,59 ; 7,62 | 80 ; 88 ; 82 ; 86 | **60 ; 66 ; 65 ; 68** | < 1 | < 1 |
| aucune | cinq | 8,6 | 8,69 ; 8,90 ; 8,88 ; 9,07 | 88 ; 92 ; 84 ; 90 | 84 ; 83 ; 76 ; 81 | 5,2 ; 27 ; **66 ; 58** | ≤ 1,1 |
| aucune | aucun | 6,6 | 7,89 ; 7,94 ; 8,04 ; 8,24 | 75 ; 85 ; 79 ; 83 | **51 ; 67 ; 63 ; 73** | 13 ; 5,5 ; 31 ; 4,9 | ≤ 3,2 |
| aucune | aucun | 8,6 | 10,02 ; 10,32 ; 10,33 ; 10,72 | 89 ; 89 ; 83 ; 87 | 81 ; 87 ; 77 ; 81 | **58 ; 77 ; 71 ; 76** | 15 ; 13 ; 49 ; 54 |
| quatre | aucun | 6,6 | 8,19 ; 8,14 ; 8,82 ; 8,70 | 59 ; 82 ; 79 ; 82 | 48 ; 32 ; 58 ; 75 | 20 ; 5,5 ; 24 ; 6,7 | ≤ 3,3 |
| quatre | cinq | 8,6 | 7,26 ; 7,66 ; 7,09 ; 7,40 | 82 ; 87 ; 74 ; 83 | 34 ; 60 ; 29 ; 57 | ≤ 1,7 | < 1 |

Avec des groupes de trois, l'étage 2 est gelé (74 ; 78 ; 61 ; 72 %).

**Lecture.**

1. **Le groupe qui se défait déplace le budget, donc l'étage** : 4,2–4,5 voisins et l'étage 2 avec des groupes de trois ; 6,3–6,6 et l'étage 3 avec les groupes de quatre de l'auteur ; 7,3–7,6 et l'étage 4 avec des groupes de cinq. Sans désintégration : 7,9–8,2, étage 4.
2. **Mais il ne le fixe pas seul** : à κ = 8,6 et sans force, les groupes de quatre laissent monter le budget à 7,4–7,7 et l'étage 4 gèle ; les groupes de cinq laissent geler l'étage 5 à 1 037 constituants. H-QUATRE est réfutée.
3. **Le moteur tient un étage plus haut que la dimension de l'espace de ses points** : avec des groupes de cinq, des points à trois dimensions portent l'étage 4, et l'étage 5 à κ = 8,6. L'étage est une affaire de budget de liens, non de plongement.
4. Dans les réseaux où des groupes se défont, l'étage gèle avec moins de liens que le seuil publié du réseau tiré au hasard : étage 3 gelé à 5,6 voisins (seuil : 5,755), étage 4 à 7,3 (7,843), étage 5 à 8,9 et 9,1 mais pas dans un relevé à 8,9 (9,896 ; Peled 2026). Le témoin direct n'a été fait que pour l'étage 3 (X-23 F). Sans désintégration, il faut davantage de liens (étage 4 non gelé à 8,1 et 8,2 voisins avec les quatre forces) : les liens s'y entassent dans des groupes serrés.

## 230. X-24 ter — à κ = 8,6, quelle force retient le moteur à l'étage 3 ?

Prédiction scellée : `x24ter_quelle_force_prediction.txt` (`af882f4a…b3a8`, 21:47:03 UTC). Source de l'auteur, seule la valeur de κ changée ; quatre ablations simples.

| Forces actives | Voisins | Étage 3 | Étage 4 |
|---|---|---|---|
| les quatre (rappel) | 6,69 ; 6,50 ; 6,24 ; 6,22 | 83 ; 76 ; 77 ; 78 | 2,0 ; 1,5 ; 0,9 ; 0,9 |
| sans « bord » | 6,62 ; 6,89 ; 6,45 ; 6,63 | 83 ; 85 ; 76 ; 79 | 1,4 ; 21 ; 2,2 ; 2,2 |
| sans « grav » | 6,96 ; 7,04 ; 7,14 ; 7,02 | 89 ; 82 ; 85 ; 79 | 0,9 ; 23 ; **52 ; 51** |
| sans « em » | 6,49 ; 6,61 ; 6,08 ; 6,48 | 81 ; 81 ; 70 ; 80 | 2,6 ; 13 ; 1,9 ; 12 |
| sans « weak » | 6,72 ; 6,56 ; 6,48 ; 6,34 | 81 ; 78 ; 82 ; 75 | 7,0 ; 0,8 ; 2,5 ; 7,4 |
| aucune (rappel) | 7,72 ; 7,49 ; 7,73 ; 7,41 | 90 ; 86 ; 87 ; 82 | 75 ; 69 ; 72 ; 65 |

La force de bord n'est pas celle qui retient (H-BORD réfutée). La seule ablation qui fasse franchir le gel de l'étage 4 est celle de « grav », le choix du parent là où la courbure d'Ollivier est la plus forte, et de justesse (52 et 51 %). Aucune ablation simple ne rend les 7,4–7,7 voisins du moteur sans force : la retenue est partagée et ne s'additionne pas. Je ne sais pas l'attribuer davantage avec deux graines.

## 231. Recoupement indépendant du moteur

Un second agent, sans mes programmes ni mes résultats, a exécuté le source de l'auteur et écrit ses propres variantes d'après leur seule description, puis calculé la rigidité à sa façon (élimination exacte modulo deux nombres premiers, amas par cliques maximales). Dix états : le moteur non modifié (graines 1 et 2, 660 et 1 037 constituants) ; dimension 4 ; κ = 8,6 avec les quatre forces ; κ = 8,6 sans force ; groupes de cinq à κ = 8,6. **116 comparaisons sur 116 identiques** : empreinte de la liste des liens, nombre de liens, rang, mécanismes, auto-contraintes et plus grand amas aux étages 3, 4 et, pour quatre états, 5. Un écart de convention : là où aucun amas n'atteint d+1 constituants, il note 0 et je note le plus grand groupe de constituants tous liés (5 sur 1 037).

Ce recoupement couvre aussi X-23 E, que le carnet précédent déclarait non recoupé : ses quatre états à 660 et 1 037 constituants sont retrouvés nombre pour nombre.

## 232. Ce que les parties B donnent : la mécanique de l'étage dans le moteur complet

L'auteur demandait de définir chaque règle des étages pour en comprendre la mécanique. Pour son moteur complet, voici ce qui est mesuré.

1. **L'étage suit le budget de liens.** Hors du plan, l'étage 3 n'est pas gelé à 5,0 voisins et l'est à 5,6. L'étage 4 n'est jamais gelé sous 7,0 voisins ; il l'est toujours à partir de 7,3 quand des groupes se défont ; entre les deux, il l'est ou non. L'étage 5 gèle vers 9.
2. **Le budget est réglé par le moteur.** Il résulte d'un apport (les liens donnés à la naissance, donc κ) et de puits : la désintégration des groupes, et les forces. Avec toutes les règles de l'auteur, le budget reste entre 4,8 et 6,7 voisins quand l'apport double.
3. **L'espace des points n'y est pour rien au-dessus de trois dimensions**, et abaisse l'étage dans le plan.
4. **Aucune règle ne porte le 3 à elle seule.** J'en ai proposé trois, toutes fausses. Aux réglages de l'auteur (κ = 6,6, groupes de quatre, quatre forces), le moteur est à l'étage 3 et y reste quand on change la dimension (4 ou 5) ou l'apport (κ = 8,6). Changer la taille du groupe qui se défait déplace l'étage dans le socle sans force (étage 2 avec des groupes de trois, étage 4 avec des groupes de cinq) ; avec les quatre forces et des groupes de cinq, l'étage 4 ne gèle que pour une graine sur deux.

Deux nombres restent donc posés dans le moteur : κ₀ = 6,6 et le quatre des groupes qui se défont. La partie A dit d'où le quatre peut venir si un lien est un contact (K6). Elle ne dit rien de 6,6 ; X-23 (A7) donnait 6 pour la mitose de l'arête sur la coque creuse.

## 233. Ce que la soirée donne, ce qu'elle ne donne pas

**Donne.**

1. Une règle de l'étage en contacts, démontrée, sans distance posée ni position générique : la coque de triangles est la seule dont chaque naissance garde une forme unique ; quatre constituants au plus se touchent tous ; les cellules ne se chevauchent jamais ; la forme n'est définie qu'à une transformation de Lorentz à 3+1 dimensions près. Statut [T] sous quatre lectures qui sont les miennes, contre-audité.
2. Un fait mesuré : le moteur complet de l'auteur reste à l'étage 3 quand ses points sont à quatre ou cinq dimensions (un état de la dimension 4 recoupé nombre pour nombre). Ce n'est pas l'espace posé qui fait son 3.
3. La mécanique de cet étage : un budget de liens réglé par le moteur, que déplacent la taille du groupe qui se défait et, sans les forces, κ.
4. Une limite mesurée de la lecture par contacts : une naissance change la forme partout, sans délai.

**Ne donne pas.** Aucune loi physique. Ni le temps, ni une dynamique, ni une limite continue, ni la courbure, ni la gravitation, ni le quantique, ni les masses, ni la jauge, ni une prédiction confrontée à une mesure extérieure. Le groupe de Lorentz obtenu est celui d'une géométrie de contacts posée ronde, pas celui d'un mouvement.

**Verrous.** V1 (espace-temps) reste partiel, statut inchangé. S'y ajoutent, pour le nœud « pourquoi 3 » et « l'arrêt à quatre porteurs », un troisième théorème conditionnel, et pour la « limite lorentzienne » rien de plus que ceci : le groupe apparaît comme celui des changements de point de vue d'une géométrie de contacts, sans aucune causalité. V2 à V7 : rien. **TOE 0/7.** La validation demandée par l'auteur n'est pas obtenue.

## 234. À l'auteur, et suite proposée

Trois points lui reviennent, sans réponse soufflée :

1. Reconnaît-il dans C1 sa phrase du 13 novembre : un lien est-il le contact de deux constituants ?
2. Un constituant est-il rond, c'est-à-dire sans direction privilégiée (C2) ?
3. Dans son moteur, la désintégration des groupes de quatre est-elle le cycle qu'il a décrit le 12 novembre (première fermeture, usure, reprise) ?

**Suite proposée, une seule.** La lecture par contacts donne une forme, pas un temps. Chercher si la suite des formes, de palier en palier de la mitose synchrone, a une loi : taille des constituants, forme limite, et ce qui tiendrait lieu de durée entre deux paliers. Prédiction à sceller avant. Si aucune loi n'en sort, la lecture par contacts reste un théorème de géométrie sur le nœud N1, sans prise sur le reste de V1.

Non fait ce soir : C-224 à C-227 de ChatGPT toujours non contre-audités ; note « mécanique des étages » de ChatGPT non récupérée ; aucun message envoyé à ChatGPT ; X-24 ter et quater non recoupés.

## 235. Fichiers

`calculs/` : prédictions `x24_contact_et_porteur_de_l_etage_prediction.txt`, `x24bis_groupe_qui_se_defait_prediction.txt`, `x24ter_quelle_force_prediction.txt`, `x24quater_localite_d_une_naissance_prediction.txt` ; programmes `x24_contacts.py`, `x24_moteur_dimension.py`, `x24bis_groupe_qui_se_defait.py` (X-24 bis et ter), `x24quater_localite_d_une_naissance.py` ; sorties `x24_contacts.json` et `.out`, `x24_contacts_controle_300.json` et `.out`, `x24_coques_definitions.json` (les 60 coques), `x24_moteur_dimension.json` et `.out`, `x24bis_groupe_qui_se_defait.json` et `.out`, `x24ter_quelle_force.json` et `.out`, `x24quater_localite_d_une_naissance.json` et `.out`, `x24quater_bruit.json` et `.out`. Dépendance ajoutée : mpmath.

Sources extérieures : P. Koebe (1936) ; E. M. Andreev (1970) ; W. P. Thurston, *The Geometry and Topology of Three-Manifolds*, ch. 13 ; B. Springborn, « A unique representation of polyhedral types. Centering via Möbius transformations », *Math. Z.* (2005), doi:10.1007/s00209-004-0713-5 ; M. Dehn, *Math. Ann.* 77 (1916) ; F. Soddy, *Nature* (1937) ; H. Chen, « Apollonian ball packings and stacked polytopes », *Discrete Comput. Geom.* (2016) ; R. L. Graham, J. C. Lagarias, C. L. Mallows, A. R. Wilks et C. H. Yan, arXiv:math/0010298 ; J. Kocik, arXiv:0706.0372 ; K. E. Stange, arXiv:1208.4836 ; B. Oblak, arXiv:1508.00920 ; Y. Peled, arXiv:2605.25711.

**TOE 0/7. Aucun verrou fermé.**
