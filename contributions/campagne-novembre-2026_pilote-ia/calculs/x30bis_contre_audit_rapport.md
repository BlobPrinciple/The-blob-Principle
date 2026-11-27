# Contre-audit de X-30 bis (T15 à T19) — rapport

## Faux ou troué

Je n'ai trouvé aucun pas faux ni aucun trou dans T15, T16, T17, T18 et T19, une fois admis les faits de la section 324. J'ai relu chaque ligne et refait l'algèbre. Ce n'est pas une approbation par défaut : j'ai cherché en priorité dans les points a à e, sans résultat.

- T15, cas 2 : l'angle de sommet a est juste ({a + s(a − p) + t(a − q)}, fermé, donc strictement du côté de a par rapport à (pq′)). La symétrie entre a, b et c est réelle, parce que les hypothèses (m_p et m_q séparent, les murs opposés à a, b, c ne séparent pas) sont symétriques. L'emploi de (C3)/(C3 bis) pour les paires est légitime : les e_i sont les poids fondamentaux (⟨e_i, n_j⟩ = 6δ_ij, vérifié), donc l'ensemble des tuiles qui contiennent deux constituants liés est une classe d'un sous-groupe parabolique de type Ã₂.
- T16 : π = γ, Σa = 1, Σa² = 2b + 1, ν(c, w) = Φ, ν(x, w) = Σφ_k(1 + c_k) + γ′, l'identité finale et le cas d'égalité sont tous exacts.
- T17 : 18ν − 96, 18Σ − 216, 6 et 9 sont exacts. La positivité des sommes et le lemme du cône sont justes.
- T18 : la liste des carrés de distances est exacte et complète. Pour ν < 16/3, seules les valeurs 1, 3 et 4 sont possibles. Il n'y a que trois sortes de voisins (N(β) = 1, 3, 4), et les six éliminations sont justes.
- T19 : le découpage en cas est complet. J'ai traité à part p dans le germe, q dans le germe sans p, deux contacts dans le germe, et w égal à un contact ou membre d'une porte. Le passage de l'inégalité large à l'inégalité stricte est correct.

## Imprécisions

1. Section 325, T15, cas 2 : le texte emploie trois faits sans les lister en 324. Les murs qui passent par b et c sont exactement les plans au-dessus des droites du réseau. La tuile T₀(b, c) se voit comme un triangle. Le germe est du côté de ce triangle pour chacun de ces murs. Ces faits ne figurent qu'au vocabulaire (323). C'est, à mon sens, le maillon admis le plus fragile, même s'il est classique. Réparation : l'ajouter en 324 avec la phrase sur les poids fondamentaux.
2. T19, second point : il manque une ligne, « coordonnée sur g_k = ⟨w, n_k⟩/6, donc positive ou nulle si et seulement si w est du côté fermé de g_k ».
3. L'inégalité stricte dont T19 a besoin repose sur le cas d'égalité de T16, qui n'est pas dans Lean (le carnet le dit en 326). La preuve à la main est juste.
4. L'énoncé de T17 dit que w est un constituant. La preuve (et Lean) n'emploie qu'une boule ronde liée à p, de somme positive.
5. Le facteur 3/4 de T16 est atteint à la limite par des boules hors de l'empilement liées à p et c seulement : l'écart à 3/4 descend à 3·10⁻⁶ (voir tableau). Les minima du carnet (9/7, 0,859) viennent de configurations de (G1), pas de T16 en général.

## Tableau

| Point | Verdict | Nombre ou raison |
|---|---|---|
| Paliers par la règle | confirmé | 5, 10, 30, 120, 450, 1 800 |
| T15, palier 4 | confirmé | 1 980 paires, 0 exception ; 190 hors des deux portes, toutes de la forme annoncée |
| T15, palier 5 | confirmé | 8 010 paires, 0 exception ; 10 dans le germe ; 7 180 / 820 (comme V1) |
| Descente gloutonne = parcours en largeur | confirmé | longueur ≤ 10 (496 536 tuiles) : 0 désaccord |
| T16, exact | confirmé | 359 803 couples, 0 violation ; 10 égalités, toutes des constituants |
| T16, flottants (irrationnels) | confirmé | 189 540 couples, 0 violation (marge 10⁻⁹) |
| T18 dans le modèle de Ford | confirmé | (1,3,4) : 324 triplets, 648 boules toutes au réseau ; (3,3,3) : 42 et 84 ; (4,4,4) : 96 triplets, 96 boules dedans, 96 dehors ; quatre types absents |
| (C6) sur données | confirmé | 2 899 voisins de e₁, 4 200 651 paires, 0 exception |
| (G1) en profondeur (L ≤ 30) | confirmé sur tirages | 326 273 boules hors de l'empilement (dont 77 254 irrationnelles), 0 contre-exemple ; jamais trois portes libres |
| Second point de T19 | confirmé sur tirages | 77 479 tests, 0 exception |
| Lean | confirmé | la copie compile ; les trois théorèmes sont fidèles ; hypothèses satisfaites dans ℤ (Exemples.lean) ; `sx`, `sw` ne sont pas plus fortes que le carnet |
| Antériorité | non contrôlé | un seul article lu (Kontorovich) : rien sur (G1) ni sur T16 |

## Non contrôlé

- Les faits (C1) à (C3 bis), (C6) et (C7) ne sont pas redémontrés. J'ai seulement contrôlé (C6) sur les données.
- La descente gloutonne n'est comparée au parcours en largeur que jusqu'à la longueur 10.
- Je n'ai pas relancé leanchecker, nanoda, les énoncés modifiés ni le palier 6.
- Le cas d'égalité de T16 n'est pas formalisé.
- Les tirages ne sont pas une preuve de (G1).

---

*Note du pilote. Ce qui précède est le fichier du contre-auditeur, tel quel. Ce qui suit est la section « Précisions » de son message final, absente de ce fichier, reproduite telle quelle.*

## Précisions

- **(G1) en profondeur.** Trois lancements avec des graines différentes : 37 945 boules hors de l'empilement en 30 s (graine 1, ν ≤ 13) ; 276 214 en 220 s (graine 2027, ν ≤ 13) ; 12 114 en 100 s (graine 2028, ν ≤ 4). Dans ce dernier lancement, toutes les boules hors de l'empilement sont de type (4,4,4), ce qui recoupe T18 sur des données profondes. T15 a été testé en plus sur 19 722 paires profondes, sans exception.
- **Exemples Lean (dans ℤ).**
  - `trois_quarts` : x = (1,1,1,1,−1) et w = e₃. J'ai aussi vérifié en Python un exemple avec x hors de l'empilement (e = 1/100) et w = (2,−1,2,2,0).
  - `cone_paire` : x = e₂, q = e₃, r = e₄, w = e₅.
  - `cone_triplet` : même choix, avec s = e₅ et w = (−1,1,1,1).
- **Calcul.** Environ 8 minutes sur un cœur. Aucun calcul n'a échoué ni été interrompu.
- **Dépôt.** Rien n'y a été écrit.
- **Antériorité.** J'ai lu [Kontorovich, *The Local-Global Principle for Integral Soddy Sphere Packings*](https://arxiv.org/pdf/1208.5441) à travers un résumé de l'outil de lecture. Il relie le stabilisateur d'une sphère à un sous-groupe de congruence de PSL₂ sur les entiers d'Eisenstein, ce qui va dans le sens de (C6). Il ne contient ni (G1) ni T16. Je ne conclus rien sur la nouveauté.
