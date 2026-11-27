# X-30, première partie — La fenêtre et la descente : deux lemmes vers l'énoncé (G), l'un contrôlé par Lean

**Rédigé par Claude, pilote IA et contre-auditeur.** Auteur du Blob Principle : Rudolphe Mirante. La cosmogonie lui appartient.

TOE 0/7. Aucun verrou fermé.

**Parole de l'auteur** (27 novembre, 10 h 17, heure de Paris) : « Tu dois pouvoir aller beaucoup plus loin ! Il est temps de valider la toe du blob. Le monde vit un paradigme informatique et mathématiques avec l’ia et cela valide chaque jour un peu plus le blob. Donc fais le nécessaire ! »

Prédiction scellée avant tout calcul : `calculs/x30_fenetre_prediction.txt`, SHA-256 `ae760b44d3c476596eae0262b4dae846e92e15e42618fca3095cfb6e2d2f4325`, poussée sur la branche à 9 h 26 UTC (commit b0ab500).

## 312. Ce qui est faux, manque ou reste ouvert, d'abord

1. **La TOE n'est pas validée, et ce carnet ne la valide pas.** Aucun verrou ne bouge. Les sept verrous demandent chacun une dérivation et, pour le septième, une prédiction indépendante confirmée ; rien de cela n'est dans ce carnet.
2. **Les résultats de mathématiques obtenus ailleurs avec l'IA ne valident pas le Blob.** Ils montrent qu'une preuve contrôlée par machine est à portée d'un laboratoire. C'est une méthode, pas un contenu. Je l'applique ici ; dire davantage serait présenter une analogie comme une identité.
3. **(G) n'est toujours pas démontré.** Ce carnet apporte deux lemmes et un énoncé plus fort, (G1), vérifié et non démontré.
4. **Un chiffre de X-29 bis était mal dit.** J'y écrivais qu'au palier 3, 234 100 boules « chevauchent un ancêtre ». Le test compte comme chevauchement le cas où la boule est elle-même cet ancêtre : 43 900 de ces boules sont des constituants de l'empilement. Les boules hors de l'empilement sont 190 200 au palier 3 et 699 024 au palier 4 : 889 224 en tout, et non 973 778. Les clauses R2 et R3 restent vraies telles qu'elles étaient scellées ; le carnet X-29 est corrigé.
5. **Lean ne contrôle que T13, et pour une boule à coordonnées rationnelles.** T12 et T14 ne sont pas formalisés.
6. **Le contrôle de T12 laisse de côté les boules irrationnelles** : 92 880 sur 237 300 au palier 3. La preuve les couvre, pas le calcul.
7. **Non fait** : une preuve de (G) ou de (G1) ; le plus petit contre-exemple à K20 ; le palier 7 ; tout travail sur un verrou.
8. **Clauses chiffrées** : les quatre sont vraies (section 316). Aucune exception à T12 ni à T13 dans les données.

## 313. Vocabulaire

- **Descente** d'une boule de coordonnées y : tant qu'une coordonnée est strictement négative, retournement dans le mur correspondant du germe (y_j devient −y_j, les autres augmentent de y_j). Elle **s'achève** si toutes les coordonnées deviennent positives ou nulles. Après k retournements, les coordonnées sont celles de la boule dans la base d'une tuile de l'empilement.
- **Parent** de u : un des quatre constituants de son plancher. **Mur du plancher** de u : de normale n = u − u′, où u′ est l'autre côté du plancher ; ⟨n, n⟩ = 12, ⟨u, n⟩ = 6.

## 314. Ce qui est démontré

**T13 (fenêtre). [T, contrôlé par Lean pour une boule rationnelle]** Soit {f₁, f₂, f₃, f₄, u} une tuile et x une boule ronde liée à u qui ne chevauche aucun des f. Alors x est tout entière au-delà du mur opposé à u, du côté de u : ⟨x, n⟩ ≥ 6. L'égalité n'a lieu que si x est l'un des quatre constituants obtenus en retournant un f.

Preuve. Écrivons x = Σ a_j f_j + b u et A = Σ a_j. Dans la base d'une tuile, ⟨x, u⟩ = b − A, ⟨x, f_j⟩ = 2a_j − A − b, ⟨x, x⟩ = 2 Σ a_j² + b² − 2Ab − A², et ⟨x, n⟩ = 6b. Le contact donne b = A − 1. Le non-chevauchement donne a_j ≤ A − 1. La rondeur donne Σ a_j² = A². Posons c_j = A − 1 − a_j ≥ 0. Alors Σ c_j = 3A − 4 et Σ c_j² = 3A² − 6A + 4, donc 2 Σ_{i<j} c_i c_j = (3A − 4)² − (3A² − 6A + 4) = 6 (A − 1)(A − 2). Le membre de gauche est positif ou nul, et A ≥ 4/3 > 1 : donc A ≥ 2, b ≥ 1, ⟨x, n⟩ ≥ 6. Comme 6 > √12, la boule ne coupe pas le mur. Égalité : tous les produits c_i c_j sont nuls, un seul c_j est non nul et vaut 2 ; x = u + Σ_{k≠j} f_k − f_j, le retourné de f_j.

**T12 (descente). [T]** Soit x une boule ronde dont la descente s'achève, dans une tuile T. Si x n'est pas dans l'empilement, elle chevauche un constituant de T, et tout constituant lié à x est dans T. Par conséquent une boule liée à quatre constituants indépendants dont la descente s'achève est dans l'empilement : **la descente d'une place hors de l'empilement ne s'achève jamais.**

Preuve. Dans la base de T, x = Σ y_k u_k avec y_k ≥ 0 ; posons s = Σ y_k. La rondeur donne 2 Σ y_k² − s² = 1 ; comme Σ y_k² ≤ s², s ≥ 1. Si s = 1, Σ y_k² = s² : une seule coordonnée est non nulle, x est un constituant de T. Si s > 1 : pour un constituant v hors de T, ⟨u_k, v⟩ ≤ −1 pour tout k, donc ⟨x, v⟩ ≤ −s < −1 : v n'est pas lié à x. Et x chevauche un constituant de T : sinon 2y_k − s ≤ −1 pour tout k, donc y_k ≤ (s − 1)/2 et 1 + s² = 2 Σ y_k² ≤ (s − 1) s, soit 1 ≤ −s. Enfin, quatre constituants de T sont tous liés : c'est une cellule, et une boule liée aux quatre en est un côté (X-28, T1), donc un constituant.

À chaque retournement la somme des coordonnées diminue de deux fois la coordonnée retournée ; une descente qui s'achève finit avec une somme au moins égale à 1. Une somme négative ou nulle certifie donc qu'elle ne s'achèvera pas.

**T14 (conséquences). [T, sous les faits de X-28 et X-29]**
- Les ancêtres de u sont tous du côté du germe du mur de son plancher, ou sur ce mur. Preuve : le plancher est sur le mur. Un constituant du mur a sa tuile-porte du côté du germe (C3 bis), donc son plancher aussi. Un constituant strictement du côté du germe n'a que des tuiles de ce côté (C2). On conclut de génération en génération.
- Dans un tissu clos par plancher, toute place admissible est au-delà du mur du plancher de chacun de ses contacts hors du germe (T13, le plancher étant né), et tous ses contacts sont sur ce mur ou au-delà (deux boules liées ne sont pas strictement de part et d'autre d'un mur, X-28, C4).

## 315. Le lemme de la fenêtre devant Lean

`calculs/lean_x30/Fenetre.lean` (Lean 4 seul, sans Mathlib, écrit à la main ; premier essai accepté). La boule a pour coordonnées (a₁, a₂, a₃, a₄ ; b)/D dans la base de la tuile, D > 0 entier. Conclusion formelle : a₁ + a₂ + a₃ + a₄ ≥ 2D, c'est-à-dire ⟨x, n⟩ ≥ 6. Le cas d'égalité et le cas d'une boule irrationnelle ne sont pas dans le fichier.

| Contrôle | Résultat |
|---|---|
| Lean 4.35.0 | accepte ; axiomes : `propext`, `Classical.choice`, `Quot.sound` |
| `leanchecker`, `leanchecker-paranoid` | acceptent |
| nanoda 0.4.19, tout autre axiome interdit | accepte (2 648 déclarations) |
| con-ron, con-leche | 2 364 déclarations acceptées chacun |
| Quatre énoncés modifiés (conclusion renforcée d'une unité ; chevauchement de f₄ permis ; dénominateur nul permis ; rondeur remplacée par une inégalité) | le script de preuve ne passe plus, quatre fois sur quatre |

Ce dernier contrôle montre que la preuve se sert de ces hypothèses. Il ne montre pas que les énoncés modifiés sont faux.

## 316. Les quatre clauses chiffrées

| Clause | Prédit | Obtenu | Verdict |
|---|---|---|---|
| U1, T13 sur données, palier 3 | zéro exception | 10 640 couples (boule, contact dont aucun parent n'est chevauché) ; plus petite valeur de ⟨x, n⟩ : 6 ; 6 560 égalités, toutes des retournés | vraie |
| U2, T12 sur données, palier 3 | la descente s'achève si et seulement si la boule est dans l'empilement | 144 420 boules rationnelles : 47 100 s'achèvent et sont dans l'empilement, 97 320 quittent le cône et sont hors de l'empilement ; 0 exception ; 92 880 boules irrationnelles laissées de côté | vraie |
| U3, (G1), paliers 3 et 4 | toute boule hors de l'empilement chevauche un parent d'un de ses contacts (confiance 55 %) | palier 3 : 190 200 boules hors de l'empilement, toutes ; palier 4, 10 parents à symétrie près : 699 024 boules hors de l'empilement, toutes ; aucune exception | vraie |
| U4, Lean | T13 accepté | accepté (section 315) | vraie |

## 317. L'énoncé qui reste à démontrer, plus fort et plus simple

**(G1) [H]** Toute boule ronde hors de l'empilement, liée à un constituant et à trois de ses voisins, chevauche un **parent** de l'un des quatre.

(G1) entraîne (G) : un parent est un ancêtre. Il donnerait un critère local : dans n'importe quel tissu, une place admissible dont les quatre contacts ont leurs parents nés est dans l'empilement. Plus besoin de toute l'ascendance.

Avec T13, (G1) se redit ainsi : une boule liée aux quatre, et située au-delà du mur du plancher de chacun d'eux sans en chevaucher aucun membre, est un constituant. T12 dit de quel côté chercher la preuve : une telle boule, si elle n'était pas un constituant, aurait une descente sans fin.

## 318. Contre-audit indépendant

**En cours au moment de ce versement.** Le sous-agent indépendant des passages précédents relit les preuves de T12, T13 et T14, l'énoncé Lean, refait U1, U2 et U3 au palier 3 avec son propre code, et cherche à casser (G1) dans des tuiles profondes. Tant que son rapport n'est pas versé, aucun résultat de ce carnet n'a été contrôlé par un autre que moi, sauf T13 par Lean.

## 319. Ce que cela donne, et ce que cela ne donne pas

Cela donne deux lemmes démontrés, dont un accepté par Lean et trois vérificateurs extérieurs, et un énoncé local, (G1), vérifié sans exception. Cela rapproche d'une preuve de la question laissée par X-27.

Cela ne valide pas la TOE. Cela ne donne ni l'espace-temps, ni la gravitation, ni rien de quantique, et ne dit pas quelle règle de naissance est celle du Blob.

## 320. Suite proposée

**X-30, seconde partie : démontrer (G1).** En parallèle, et c'est ce qui compte pour la validation : reprendre le premier des verrous par ordre de rendement, la loi de cadence de V1, avec la même discipline — prédiction scellée, calcul, contre-audit, Lean là où un lemme s'y prête.

## 321. Fichiers

- `calculs/x30_fenetre_prediction.txt` : prédiction scellée.
- `calculs/x30_fenetre_descente.py` ; sorties `x30_tout_3.out`, `x30_tout_4_sym.out`.
- `calculs/lean_x30/` : `Fenetre.lean`, `controle.sh`, `controle.out`.
- `calculs/x30_contre_audit_rapport.md` : rapport du contre-audit, à verser tel quel dès réception.

TOE 0/7. Aucun verrou fermé.
