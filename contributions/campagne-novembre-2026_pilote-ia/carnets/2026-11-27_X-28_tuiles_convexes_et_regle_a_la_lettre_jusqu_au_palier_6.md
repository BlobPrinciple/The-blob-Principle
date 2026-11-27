# X-28 — Quel tissu reste dans l'empilement : les tuiles convexes, et la règle à la lettre jusqu'au palier 6

**Rédigé par Claude, pilote IA et contre-auditeur.** Auteur du Blob Principle : Rudolphe Mirante. La cosmogonie lui appartient.

TOE 0/7. Aucun verrou fermé.

**Parole de l'auteur** (27 novembre, 7 h 08, heure de Paris) : « Dépose et pousse à l’extrême ensuite toutes les recherches. »

Prédiction scellée avant tout calcul : `calculs/x28_tissu_convexe_prediction.txt`, SHA-256 `c1576d634f56ee07ae24914e32a4f38f76db7cde54e29cb5165b2be08fb48bf5`, poussée sur la branche à 6 h 42 UTC (commit 58934bb).

## 283. Ce qui est faux, manque ou reste ouvert, d'abord

1. **Aucun verrou ne bouge.** Tout ce carnet est de la géométrie de la lecture de contact, rang 3.
2. **La voie que je proposais pour démontrer la règle à la lettre est tombée. [FAIL]** Le « tissu comblé » (le tissu, plus ses places à cinq contacts) est à tuiles convexes aux paliers 3, 4 et 5, mais pas au palier 6 : 360 murs sur 38 070 y ont un constituant au-delà. Mon calcul et celui du contre-auditeur, indépendants, donnent le même résultat. La réduction que j'avais écrite ne mène donc nulle part (sections 289 et 291).
3. **La règle à la lettre n'est pas démontrée à tout palier.** Le théorème T3 demande des tuiles convexes ; la règle à la lettre n'en a plus dès le palier 3. Qu'elle garde le tissu dans l'empilement est vrai par le calcul jusqu'au palier 6, pas par preuve.
4. **Le contre-audit a trouvé des trous dans trois preuves** (section 292). T1 : une hypothèse affirmée sans preuve, et inutile. T3 : l'étape 3 était mal justifiée, et l'un des « faits classiques » (deux constituants liés partagent une tuile) n'est pas un fait sur les groupes de Coxeter mais un fait sur l'empilement. T6 : deux trous. Les preuves sont réécrites ici (sections 285, 286, 289). Au moment de ce versement, les passages réécrits sont en cours de relecture par le même auditeur.
5. **Un calcul a été tué par le système.** La seconde file d'attente de la clause N7 s'est arrêtée à 400 naissances sur 445 (code 137 ; le contre-audit calculait en même temps). Je l'ai relancée à l'identique ; la sortie interrompue est gardée (`x28_file_2_445_interrompu.out`).
6. **Un seul des cinq énoncés annoncés est contrôlé par Lean** : T2, et seulement pour une boule x à coordonnées rationnelles. Mon premier script de preuve a été refusé ; le second passe. T1, T3, T4 et T5 ne sont pas formalisés.
7. **Quatre résultats de ce carnet n'étaient pas prédits** et ne sont donc pas scellés : le lemme du pliage (T6), le lemme du toit (T2 bis), la forme des places, le tissu comblé (section 289).
8. **Non fait** : le plus petit contre-exemple (toujours entre 9 et 17 naissances) ; le palier 7. Antériorité : non tranchée (section 293).
9. **Clauses chiffrées** : les neuf sont vraies (section 288). Aucune exception à T1–T5 dans les données.

## 284. Vocabulaire

Produit, germe, empilement, lien, place admissible, cellule, côté d'une cellule : ceux de X-27.

- **Tuile** : cinq constituants tous liés. **Tuile née** d'un tissu : ses cinq constituants sont nés.
- **Mur d'une cellule** : la sphère orthogonale à ses quatre constituants. Les deux côtés t et t′ de la cellule sont images l'un de l'autre dans ce mur ; le vecteur t − t′ lui est orthogonal. Un constituant u est **au-delà du mur**, du côté de t′, si ⟨u, t − t′⟩ < 0.
- **Tissu à tuiles convexes** : tout constituant est dans une tuile née ; les tuiles nées se tiennent de proche en proche par des cellules ; pour toute cellule née dont un seul côté t est né, aucun constituant né n'est au-delà du mur.
- **ν(q, r) = (1 − ⟨q, r⟩)/2.** Pour deux constituants de l'empilement c'est un entier, égal à 1 s'ils sont liés : la somme des coordonnées d'un constituant est impaire, donc le produit de deux constituants aussi.
- **Vu d'un constituant p**, à tout voisin u de p on attache le vecteur u + p. Il est orthogonal à p et de norme nulle. Pour deux voisins u, v de p : ⟨u + p, v + p⟩ = ⟨u, v⟩ − 1. Deux voisins sont liés si ce produit vaut −2, séparés s'il est plus petit.
- **Milieu de q et r vu de p** : le vecteur q + r + 2p. Il est **dans la tuile née T** (T contient p) si ses coordonnées dans la base T sont positives ou nulles sur les quatre constituants de T autres que p.

## 285. Ce qui est démontré

**T1 (miroir). [T]** Soient p un constituant et q, r, s trois de ses voisins, les quatre indépendants. Les boules rondes liées aux quatre sont deux au plus, et images l'une de l'autre dans la sphère orthogonale aux quatre.

Preuve. Les vecteurs q + p, r + p, s + p sont orthogonaux à p, de norme nulle, indépendants, de produits deux à deux strictement négatifs : le déterminant de leurs produits est strictement négatif, ils engendrent un espace de signature (2, 1). Avec p, les quatre constituants engendrent donc un espace de signature (3, 1), et le vecteur d qui leur est orthogonal est de norme strictement positive : c'est une vraie sphère. Tout vecteur s'écrit x₀ + λd avec x₀ combinaison des quatre. Les quatre contacts fixent x₀. La rondeur donne λ² ⟨d, d⟩ = 1 − ⟨x₀, x₀⟩ : deux valeurs opposées de λ au plus, échangées par le miroir d. (La première rédaction s'appuyait sur « quatre constituants ne passent pas par un même point », affirmé sans preuve ; le contre-audit l'a relevé. L'énoncé est restreint au cas qui sert, un parent et trois voisins.)

**T2 (pont). [T, contrôlé par Lean]** Soit T = {p, a, b, c, d} une tuile, x une boule liée à p qui ne chevauche ni a, ni b, ni c, ni d, et q, r deux constituants de l'empilement liés à p et à x. Si le milieu de q et r vu de p est dans T, alors q et r sont liés.

Preuve. Posons ξ = x + p et, pour k dans {a, b, c, d}, g_k = −⟨ξ, k + p⟩/2. Ne pas chevaucher k donne g_k ≥ 1. Écrivons q + r + 2p = Σ α_k (k + p), avec α_k ≥ 0, et A = Σ α_k.
- Produit avec ξ. À gauche : ⟨ξ, q + p⟩ + ⟨ξ, r + p⟩ = −4, car x est liée à q et à r. À droite : −2 Σ α_k g_k ≤ −2A. Donc A ≤ 2.
- Norme. À gauche : 2 ⟨q + p, r + p⟩ = −4ν(q, r). À droite : −2 (A² − Σ α_k²). Donc 2ν = A² − Σ α_k².
- Comme Σ α_k² ≥ A²/4 pour quatre nombres, 2ν ≤ (3/4) A² ≤ 3, donc ν ≤ 3/2. Or ν est un entier, et ν ≥ 1 : q et r sont deux constituants distincts de l'empilement, ils ne se chevauchent pas. Donc ν = 1.

La rondeur de x ne sert pas.

**T3 (tissu à tuiles convexes). [T, sous les faits classiques de la section 286]** Dans un tissu à tuiles convexes, toute place admissible est le côté d'une cellule née. Elle est donc dans l'empilement.

**T4 (hexagone). [T]** Autour de trois constituants tous liés p, a, b, six constituants forment un anneau ; chacun est lié à ses deux voisins de l'anneau. Si q et r y sont séparés par un seul constituant m, toute boule ronde liée à p, q et r qui ne chevauche ni a ni b est m.

Preuve. Dans l'anneau, q + r = p + a + b + m (c'est la formule de l'autre côté d'une cellule). Vu de p : (q + p) + (r + p) = (a + p) + (b + p) + (m + p). Le produit avec ξ = x + p donne −4 = ⟨ξ, a + p⟩ + ⟨ξ, b + p⟩ + ⟨ξ, m + p⟩ ≤ −4 + ⟨ξ, m + p⟩, donc ⟨ξ, m + p⟩ ≥ 0. Or ξ et m + p sont deux vecteurs de norme nulle, tous deux de produit négatif avec a + p : ils sont du même côté du cône, leur produit est négatif ou nul, et nul seulement s'ils sont proportionnels. Donc ξ = μ (m + p). L'égalité partout donne ⟨ξ, a + p⟩ = −2, d'où μ = 1 et x = m.

**T5 (gonflée). [T]** Si une boule x est liée à un constituant p au point où un constituant F touche p, et liée à un autre voisin q de p, alors x = (F − (ν − 1) p)/ν avec ν = ν(F, q).

Preuve. Les boules liées à p en ce point sont les μF − (1 − μ)p, μ > 0. Le contact avec q donne μ ⟨F, q⟩ + (1 − μ) = −1, soit μ = 2/(1 − ⟨F, q⟩) = 1/ν.

Conséquence. Tous les voisins de p que touche x ont le même produit avec F. Le constat à 9 cas de X-27 bis est de l'algèbre : chaque place hors de l'empilement dont le point de contact avec p est celui d'un constituant F est ce F gonflé, de dénominateur ν.

## 286. Preuve de T3

Faits classiques admis.

- (C1) Le groupe engendré par les cinq retournements est un groupe de Coxeter : chaque retournement est d'ordre 2, le produit de deux retournements distincts est d'ordre 3, sans autre relation. Les tuiles de l'empilement correspondent une à une à ses éléments. Deux tuiles sont voisines quand elles partagent une cellule. (Vinberg, déjà invoqué en K11 ; Graham, Lagarias, Mallows, Wilks et Yan, 2006, théorème 5.1 d'après le contre-auditeur.)
- (C2) Chaque mur partage les tuiles en deux moitiés et ne coupe aucune tuile. Un chemin de tuiles voisines est un plus court chemin si et seulement s'il ne traverse aucun mur deux fois. Un ensemble de tuiles qui contient tous les plus courts chemins entre deux de ses tuiles est une intersection de moitiés (Tits).
- (C3) Soit R l'ensemble des tuiles qui contiennent un constituant p. R contient tous les plus courts chemins entre deux de ses tuiles. Pour toute tuile c, R a une tuile la plus proche de c, par laquelle passe un plus court chemin de c à chaque tuile de R.

Fait sur l'empilement, démontré ici.

- **(C4) [T]** Des constituants de l'empilement tous liés entre eux sont dans une même tuile de l'empilement. Preuve. Pour un mur, de normale n = t − t′ (entière, primitive, de norme 12), et un constituant u, le retournement dans le mur envoie u sur u − ⟨u, n⟩ n/6, qui est un vecteur entier : ⟨u, n⟩ est un multiple de 6. Donc u est orthogonal au mur, ou bien |⟨u, n⟩| ≥ 6 > √12 : sa boule fermée est strictement d'un côté. Deux constituants strictement de part et d'autre d'un mur n'ont aucun point commun : ils ne sont pas liés. Récurrence sur la somme des coordonnées des constituants de l'ensemble σ, des entiers strictement positifs. Si σ est dans le germe, la tuile du germe convient. Sinon soit q dans σ hors du germe, et T une tuile contenant q la plus proche du germe. T n'est pas la tuile du germe ; un de ses murs la sépare donc du germe, et c'est le mur opposé à q, sinon la tuile voisine contiendrait q et serait plus proche. q est strictement au-delà de ce mur ; les autres membres de σ, liés à q, sont sur le mur ou au-delà. Le retournement dans ce mur diminue la somme des coordonnées de q, ne grandit celle d'aucun autre, et envoie σ sur un ensemble de constituants tous liés : par récurrence celui-ci est dans une tuile, dont l'image contient σ.

Preuve de T3. Soit K l'ensemble des tuiles nées, x une place admissible, p son parent, q, r, s les trois voisins de p qu'elle touche.

1. K contient tous les plus courts chemins entre deux de ses tuiles. Sinon un plus court chemin sortirait de K par une cellule née dont l'autre côté n'est pas né ; il ne retraverse pas ce mur (C2) et finit dans K, au-delà du mur : contraire à l'hypothèse.
2. Deux constituants nés et liés p, q sont dans une même tuile née. Prenons une tuile née c contenant q et une tuile née c′ contenant p. Soit d la tuile de p la plus proche de c. Elle est sur un plus court chemin de c à c′ (C3), donc dans K (étape 1). Elle contient q : par (C4) une tuile e contient p et q ; un plus court chemin de c à e passe par d (C3), et il reste parmi les tuiles de q (C3 appliqué à q).
3. Vu de p, c'est-à-dire dans l'hyperplan orthogonal à p, les tuiles de p découpent un espace hyperbolique de dimension 3 en tétraèdres à sommets à l'infini : le tétraèdre de la tuile T est l'ensemble des Σ α_k (k + p), α_k ≥ 0, k dans T autre que p, et ses sommets sont les points à l'infini des vecteurs k + p. Les tuiles nées de p contiennent tous les plus courts chemins entre deux d'entre elles (étape 1 et C3) : par (C2), appliqué au groupe des retournements qui fixent p, la réunion U de leurs tétraèdres est une intersection de demi-espaces fermés. Un demi-espace fermé qui contient un tétraèdre de sommet z a z dans son adhérence à l'infini ; s'il a ainsi deux points à l'infini, il contient la géodésique qui les joint.
4. Par l'étape 2, les points à l'infini de q + p et de r + p sont des sommets de tétraèdres de U. Par l'étape 3, la géodésique qui les joint est dans U. Le vecteur q + r + 2p, somme de q + p et de r + p, est sur cette géodésique : le milieu de q et r vu de p est dans une tuile née.
5. T2 : q et r sont liés. De même q et s, r et s. Avec p, lié aux trois, ce sont quatre constituants tous liés : une cellule née, dont x est un côté.

La première rédaction des étapes 2 et 3 était fautive (section 292) : elle rangeait (C4) parmi les faits classiques et justifiait l'étape 3 par une phrase non démontrée.

## 287. Le lemme du pont devant Lean

`calculs/lean_x28/Pont.lean` (190 lignes, Lean 4 seul, sans Mathlib, écrit à la main). L'énoncé est celui de T2, avec x donnée par un numérateur entier et un dénominateur D > 0, et le milieu pris à un facteur entier N > 0 près. Conclusion formelle : ⟨q, r⟩ ≥ −2. Le passage à « q et r sont liés » (produit impair, constituants distincts) n'est pas dans le fichier. Le fichier ne couvre qu'une boule x à coordonnées rationnelles ; la preuve sur papier vaut pour toute boule, y compris à coordonnées quadratiques.

| Contrôle | Résultat |
|---|---|
| Lean 4.35.0 | accepte ; axiomes : `propext`, `Classical.choice`, `Quot.sound` |
| `leanchecker`, `leanchecker-paranoid` | acceptent |
| nanoda 0.4.19, tout autre axiome interdit | accepte |
| con-ron, con-leche | 2 415 déclarations acceptées chacun |
| Quatre énoncés affaiblis ou renforcés (conclusion −1 ; contact avec r remplacé par une inégalité ; un coefficient autorisé à −1 ; chevauchement de a autorisé) | le script de preuve ne passe plus, quatre fois sur quatre |

Ce dernier contrôle montre que la preuve se sert de ces hypothèses. Il ne montre pas que les énoncés modifiés sont faux.

## 288. Les neuf clauses chiffrées

| Clause | Prédit | Obtenu | Verdict |
|---|---|---|---|
| N1, palier 4 | places = côtés libres ; entre 1 200 et 1 380 | 450 constituants ; 1 350 places, toutes côtés libres ; 0 hors empilement ; 0 sans cellule | vraie |
| N2, palier 5 | idem | 1 800 constituants ; 5 490 places, toutes côtés libres ; 0 ; 0 | vraie |
| N3, palier 6 | idem, si le budget le permet | 7 290 constituants ; 21 870 places, toutes côtés libres ; 0 ; 0 (216 s) | vraie |
| N4, convexité | convexe aux paliers 0, 1, 2 ; pas aux paliers 3, 4, 5 | convexe à 0, 1, 2 ; murs avec un constituant au-delà : 120 sur 390, 360 sur 1 530, 1 440 sur 6 210 (et 6 480 sur 25 110 au palier 6) | vraie |
| N5, tissu de X-27 | pas convexe ; deux paires non liées, milieu dans aucune tuile née | 7 murs sur 56 ; produits −5 et −13, 0 tuile née sur 18 pour chacune | vraie |
| N6, T2 sur données | zéro exception | 333 522 paires contrôlées ; 322 074 ont leur milieu dans une tuile née, toutes liées ; les 11 448 autres ne sont pas liées | vraie |
| N7, paliers incomplets | zéro hors empilement, zéro sans cellule | (a) file d'attente, 445 naissances : tirage 1, 1 795 places rencontrées, 0 et 0 ; tirage 2 (relancé après l'arrêt par le système) : 1 795 places rencontrées, 0 et 0, 2 419 155 quadruples ; les deux tirages finissent sur le tissu du palier 4 ; (b) six tissus de 788 à 1 462 constituants, 2 221 à 4 368 places, 0 et 0 | vraie |
| N8, jumelle de la troisième place | dans l'empilement | (2, 2, 2, −1, 0), dans l'empilement, pas née | vraie |
| N9, outil | mêmes places que l'outil de X-27 | paliers 0 à 3 : 5, 20, 90, 330, identiques ; palier 4 : les 1 350 places de la file d'attente menée à son terme, identiques | vraie |

Témoin de N4 au palier 3 : autour de (0, 0, 0, 1, 0), (0, 0, 0, 0, 1) et (−1, 0, 2, 2, 2), nés aux paliers 0, 0 et 2, cinq membres de l'anneau sont nés et quatre tuiles sur six. C'est le genre de témoin annoncé.

La règle à la lettre, palier par palier :

| Palier | Constituants | Tuiles nées | Places = côtés libres | Triplets examinés | Convexe |
|---:|---:|---:|---:|---:|---|
| 0 | 5 | 1 | 5 | 4 | oui |
| 1 | 10 | 6 | 20 | 60 | oui |
| 2 | 30 | 36 | 90 | 1 206 | oui |
| 3 | 120 | 156 | 330 | 29 039 | non |
| 4 | 450 | 636 | 1 350 | 478 159 | non |
| 5 | 1 800 | 2 616 | 5 490 | 8 755 307 | non |
| 6 | 7 290 | 10 536 | 21 870 | 165 819 084 | non |

Les trois places hors de l'empilement connues ont **la même jumelle** : (2, 2, 2, −1, 0), une place de l'empilement que ces tissus ont laissée vide. Je tenais l'énoncé général (toute jumelle est dans l'empilement) pour faux ; je ne l'ai pas éprouvé au-delà de ces trois cas.

## 289. Ajouts non prédits

**T6 (pliage). [T, non scellé]** Sous la règle à la lettre, soit un mur qui laisse le germe d'un côté, et u un constituant né strictement de l'autre côté. Alors l'image de u dans le mur est née au même palier que u, ou avant.

Preuve, par récurrence sur le palier k de u. Par (C2) un mur ne coupe aucune tuile ; par (C4) un constituant est sur le mur ou strictement d'un côté. u est le côté d'une cellule C née avant k, dont l'autre côté v est né avant k. La tuile C ∪ {u} est au-delà du mur. Si v est strictement du côté du germe, les tuiles C ∪ {u} et C ∪ {v} sont de part et d'autre du mur : C est sur le mur, et l'image de u est v. Sinon chaque membre de C ∪ {v} est sur le mur ou au-delà, et son image est née au même palier que lui ou avant : ceux du mur ne bougent pas, les autres par récurrence. L'image de C est donc une cellule née avant k dont un côté, l'image de v, est né ; l'image de u est son autre côté : elle naît au palier k au plus tard. (La première rédaction avait deux trous, relevés par le contre-audit : elle affirmait sans preuve que deux constituants de part et d'autre d'un mur ne sont pas liés, et ne disait pas pourquoi la cellule image a un côté né.)

Conséquences. Si le côté t d'une cellule est né et pas l'autre côté t′, le germe est du côté de t. Tout constituant né au-delà d'un tel mur a son image née. **Contrôle [M]** : aux paliers 3 à 6, 180, 720, 2 880 et 16 200 constituants au-delà d'un mur de surface, tous d'image née, tous de palier au moins égal à celui de l'image. Le carnet X-29 étend l'énoncé et le contrôle à tous les murs.

**T2 bis (toit). [T, non scellé, non contrôlé par Lean]** Soit {p, q, λ₁, λ₂, λ₃} une tuile, x une boule liée à p et à q qui ne chevauche aucun λ_i, et r un constituant lié à p et à x. Si les coordonnées de r dans cette tuile sont positives ou nulles sur λ₁, λ₂, λ₃, alors q et r sont liés.

Preuve. Écrivons r = πp + aq + Σ b_i λ_i, B = Σ b_i ≥ 0. Produit avec p : π = a + B − 1. Produit avec x : a + B ≤ 1. Produit avec q : 2B = 1 − ⟨q, r⟩, soit B = ν(q, r). Norme : 1 = 2(π² + a² + Σ b_i²) − (π + a + B)² ; avec Σ b_i² ≥ B²/3 on en tire B (3a + B) ≥ 0. Si B > 0 : a ≥ −B/3, donc (2/3) B ≤ a + B ≤ 1 et ν ≤ 3/2, ν = 1 (ν est un entier au moins égal à 1, comme en T2). Si B = 0, ⟨q, r⟩ = 1 : r serait q.

Lecture : dans la bande entre deux constituants liés p et q, si les trois constituants du réseau au-dessus de r sont nés, aucune place liée à p, q et r n'existe sauf si r est lui-même du réseau.

**La forme des places sous la règle à la lettre. [M]** Aux paliers 0 à 6, chaque place a quatre ou cinq contacts. Quatre : une cellule née. Cinq : deux cellules nées qui partagent trois constituants ; les deux autres contacts ne sont pas liés, leur produit vaut −5. La place est alors le dernier membre manquant d'un anneau (T4). Places à symétrie près, à quatre contacts et à cinq contacts : 91 et 25 au palier 3, 270 et 66 au palier 4, 784 et 180 au palier 5, 2 091 et 580 au palier 6 ; aucune à cinq contacts aux paliers 0, 1 et 2.

**Le tissu comblé : à tuiles convexes aux paliers 3, 4 et 5, pas au palier 6. [M ; FAIL pour la voie proposée]** Ajoutons au tissu d'un palier ses places à cinq contacts. Aux paliers 3, 4 et 5 (60, 180 et 720 ajouts), le tissu obtenu est à tuiles convexes : aucun constituant au-delà d'aucun mur de surface ; chaque ajout n'entre que dans deux tuiles. Au palier 6 (3 240 ajouts, 17 016 tuiles), 360 murs de surface sur 38 070 ont un constituant né au-delà. Témoin : la cellule {(−6, 0, 10, 15, 18), (−1, 0, 2, 2, 2), (0, 0, 0, 0, 1), (−10, 1, 16, 22, 28)}, de côté né (−5, 1, 7, 11, 13) et de côté libre (−12, 0, 21, 28, 36) ; le constituant né (−8, −2, 17, 22, 28) est au-delà de son mur.

**Corollaire de T3. [T]** Là où le tissu comblé est à tuiles convexes (paliers 3, 4, 5), toute place du tissu qui ne chevauche aucun des ajouts est le côté d'une cellule née.

## 290. Ce que cela dit du contre-exemple de X-27

Le tissu de X-27 n'a pas de tuiles convexes : 7 murs de surface sur 56 ont un constituant né au-delà. Pour sa place hors de l'empilement, parent (1, 0, 0, 0, 0), deux paires de contacts ne sont pas liées, et le milieu de chacune, vu du parent, n'est dans aucune des 18 tuiles nées. C'est ce que T2 exige de tout contre-exemple : **entre deux contacts non liés d'une place, vu du parent, le tissu a un creux.**

Le même énoncé, tourné vers les tissus : un tissu sans creux — à tuiles convexes — n'offre que des côtés de cellule. L'héritage des liens et la forme fixée par les contacts y entraînent la naissance dans la cellule, comme au rang 2 (K19), où c'est vrai de tout tissu.

## 291. Ce qui reste ouvert

**La règle à la lettre à tout palier. [OUVERT]** Mesurée vraie jusqu'au palier 6 et dans huit tissus à palier incomplet. J'avais écrit ici une réduction : démontrer, pour tout palier, (a) que le tissu comblé est à tuiles convexes et (b) qu'aucune place ne chevauche un des ajouts sans lui être égale. **(a) est fausse au palier 6** (section 289). Cette réduction est abandonnée.

Ce qui reste comme prise : le pliage (T6). Le tissu de la règle à la lettre est stable quand on replie vers le germe ; le tissu du contre-exemple de X-27 a des creux. Le carnet X-29, dont la prédiction a été scellée et poussée avant calcul (commit d3c1008), éprouve cette prise.

**Le plus petit contre-exemple** : toujours entre 9 et 17 naissances.

## 292. Contre-audit indépendant

Un sous-agent indépendant (Claude Opus), qui n'avait pas vu mon raisonnement, a relu les preuves et refait les calculs avec son propre code. Son rapport est versé tel quel : `calculs/x28_contre_audit_rapport.md`.

Ce qu'il a trouvé, et ce que j'en ai fait.

1. La réduction (a) est fausse au palier 6. Accepté : déclaré en tête ; sections 289, 291 et 294 réécrites.
2. T3, étape 3 : justification fautive. Accepté : étape réécrite avec son argument (intersection de deux ensembles convexes, demi-espaces fermés, points à l'infini).
3. (C3), dernière clause : ce n'est pas un fait sur les groupes de Coxeter. Accepté : la clause est retirée de (C3) ; (C4) est énoncé et démontré.
4. T6 : deux trous. Accepté : preuve réécrite.
5. T1 : hypothèse affirmée sans preuve. Accepté : énoncé restreint au cas qui sert, preuve refaite sans cette hypothèse.
6. T2 : ν ≥ 1 omis ; Lean ne couvre qu'une boule rationnelle. Accepté : ajouté aux sections 283, 285 et 287.
7. Section 293 : une phrase invérifiable. Accepté : remplacée.

Ce qu'il a confirmé par son propre calcul : les tailles et les places des paliers 0 à 4 ; la convexité aux paliers 0 à 5 ; T2 sur 24 420 paires ; les chiffres du tissu de X-27 ; le pliage aux murs de surface aux paliers 3 à 5 ; l'absence de contre-exemple à T2 sur 2 859 tuiles tirées au hasard (recherche en nombres flottants) ; le fichier Lean (il compile, ses hypothèses sont satisfaisables).

Ce qu'il n'a pas contrôlé : les clauses N7 et N9 ; les places au palier 5 et au-delà ; T2 bis sur données ; la correspondance entre tuiles et éléments du groupe ; les vérificateurs extérieurs de Lean et les énoncés modifiés.

Second passage (relecture des preuves réécrites) : en cours au moment de ce versement. Son rapport sera versé avec celui de X-29.

## 293. Ce que cela donne, et ce que cela ne donne pas

Cela donne une condition géométrique simple sous laquelle la lecture « le nouveau-né hérite des liens du parent, et sa forme est fixée par les contacts » suffit à imposer la naissance dans la cellule au rang 3 ; une preuve contrôlée par machine de son lemme central ; et la règle à la lettre vérifiée jusqu'au palier 6 au lieu du palier 3 : 7 290 constituants au lieu de 120.

Cela ne donne ni l'espace-temps, ni la gravitation, ni rien de quantique. Cela ne dit pas quelle règle de naissance est celle du Blob : c'est la parole de l'auteur. Cela ne démontre pas la règle à la lettre.

Antériorité : non tranchée. Le contre-auditeur n'a rien trouvé, en quatre recherches, qui énonce T2 ou T3 ; il n'a vu que le titre de trois des quatre références. Je ne dis donc pas que T2 et T3 sont nouveaux. (C4) et les lemmes sur les murs sont du folklore des groupes de réflexions.

## 294. Suite proposée

**X-29 : le pliage.** Le tissu de la règle à la lettre est-il clos par pliage pour tous les murs, et un tissu clos par pliage peut-il offrir une place hors de l'empilement ? Prédiction scellée : `calculs/x29_pliage_prediction.txt`.

## 295. Fichiers

- `calculs/x28_tissu_convexe_prediction.txt` : prédiction scellée.
- `calculs/x28_tissu_convexe.py` : énumérateur nouveau, paliers, file d'attente, paliers incomplets, tissus de X-27. Sorties : `x28_paliers_5.out`, `x28_paliers_6.out`, `x28_paliers_5.json`, `x28_paliers_6.json`, `x28_places_palier_4.json`, `x28_file_1_445.out`, `x28_file_2_445.out`, `x28_file_2_445_interrompu.out`, `x28_file_1_places_finales.json`, `x28_file_2_places_finales.json`, `x28_partiel.out`, `x28_x27.out`, `x28_x27.json`, `x28_temoin_palier_3.json`.
- `calculs/x28_ajouts.py` : ajouts non prédits. Sorties : `x28_ajouts_contacts.out`, `x28_ajouts_pliage.out`, `x28_ajouts_comble.out`.
- `calculs/lean_x28/` : `Pont.lean`, `controle.sh`, `controle.out`.
- `calculs/x28_contre_audit_rapport.md` : rapport du contre-audit, versé tel quel.

Sources citées : Graham, Lagarias, Mallows, Wilks, Yan, « Apollonian circle packings: geometry and group theory III. Higher dimensions », Discrete & Computational Geometry 35 (2006) ; Vinberg sur les groupes de réflexions hyperboliques ; Tits pour les complexes de Coxeter. Vinberg et Tits sont cités de mémoire ; le contre-auditeur a lu un résumé de la première référence (arXiv math/0010324).

TOE 0/7. Aucun verrou fermé.
