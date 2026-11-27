# X-30, seconde partie — (G1) démontré sous des faits classiques admis : les trois quarts et le cône

**Rédigé par Claude, pilote IA et contre-auditeur.** Auteur du Blob Principle : Rudolphe Mirante. La cosmogonie lui appartient.

TOE 0/7. Aucun verrou fermé.

**Parole de l'auteur** (27 novembre, rapportée dans le relais de session de 11 h 03, heure de Paris) : « Je veux démontrer la cosmogonie les détails viendront ! Vas y »

Prédiction scellée avant tout calcul : `calculs/x30bis_demonstration_de_G1_prediction.txt`, SHA-256 `281121420e1ff210aff489a809686bc8455169322fd0be515020f587da2858b6`, poussée sur la branche à 10 h 54 UTC (commit e3fb3fc).

## 322. Ce qui est faux, manque ou reste ouvert, d'abord

1. **La cosmogonie n'est pas démontrée, et ce carnet ne la démontre pas.** Aucun verrou ne bouge. Ce qui est démontré ici est un énoncé de géométrie des empilements de sphères, dans la lecture de contact de rang 3, qui reste une lecture du pilote. Du premier maillon (une seule réalisation de la mitose), il ferme une question et en laisse deux : le lien avec la division de l'arête n'est pas entamé, et la règle de naissance du Blob reste la parole de l'auteur.
2. **(G1) est démontré sous des faits classiques que je n'ai pas redémontrés** (section 324) : la structure de groupe de Coxeter de l'empilement et ses conséquences sur les murs, la description des voisins d'un constituant par les sphères de Ford des entiers d'Eisenstein, le rangement en réseau triangulaire des constituants liés à deux constituants liés. Ils sont contrôlés sur données (clauses V1 et V5), pas démontrés ici. **Aucun humain n'a lu cette preuve.** Elle a été écrite par une IA et relue par une IA de la même famille.
3. **Lean ne contrôle pas toute la preuve.** Le relais demandait Lean pour chaque lemme ; ce n'est pas atteint. Sont devant Lean : T16 en entier, T17 en entier, et la partie arithmétique de T18. Ne le sont pas : T15 (de la combinatoire des murs), la partie géométrique de T18 (où sont posées les boules tangentes), l'assemblage T19, et le dictionnaire entre boules et coordonnées. La prédiction scellée ne promettait que les deux inégalités ; le cas d'égalité de T16, les signes de T17 et l'arithmétique de T18 sont un ajout non scellé (section 326).
4. **Le point dur annoncé dans le relais n'a pas été résolu : il a été contourné.** Je devais comprendre ce que devient le plancher d'un constituant replié dans un mur. La preuve ne replie rien. Elle regarde la place depuis son parent, et ne se sert des planchers que par un lemme sur les paires liées (T15).
5. **Un calcul mal dimensionné.** Un ajout non scellé (toutes les boules d'une fenêtre, toutes les bases à distance 6 : 7 548 boules, 677 bases) était trop gros. Je l'ai arrêté après 17 minutes environ, avant qu'il ait fini, et relancé plus petit (section 328).
6. **La moitié « exactement les côtés libres » de la conjecture (C) reste ouverte.** (G1) dit qu'une place admissible d'un tissu clos par plancher est dans l'empilement. Il ne dit pas qu'elle est le côté d'une cellule née ; c'est toujours seulement constaté (350 tissus, X-29).
7. **Ce que le contre-audit a trouvé** (section 330). Aucun pas faux, aucun trou, une fois admis les faits de la section 324. Cinq imprécisions, toutes reprises : trois faits employés dans T15 sans être listés parmi les faits admis ; une ligne manquante dans T19 ; l'inégalité stricte de T19 reposait sur un cas d'égalité absent de Lean (il y est maintenant) ; l'énoncé de T17 demandait trop ; et le facteur 3/4 de T16 est approché d'aussi près qu'on veut par des boules hors de l'empilement, ce que mes minima sur données ne montraient pas. Un de ses trois tirages en profondeur n'a pas été enregistré, et une de ses sorties était tronquée : je l'ai relancée.
8. **Antériorité : presque pas cherchée.** Un seul article lu, à travers un outil de lecture et non ligne à ligne (section 330). Je ne dis d'aucun énoncé de ce carnet qu'il est nouveau.
9. **Non fait** : T15, la partie géométrique de T18 et T19 devant Lean ; le palier 7 ; le plus petit contre-exemple à K20 ; le lien avec la division de l'arête ; le temps ; tout travail sur un verrou.
10. **Clauses chiffrées** : les sept sont vraies (section 327). Aucune exception à T15, T16, T17 ni T18 dans les données.

## 323. Vocabulaire

Celui de X-27 à X-30, plus ceci.

- **ν(a, b) = (1 − ⟨a, b⟩)/2.** Deux boules sont liées si ν = 1, se chevauchent si ν < 1. Pour deux constituants distincts, ν est un entier au moins égal à 1 (X-28).
- **T(u)** : la tuile-porte de u ; pour un constituant du germe, la tuile du germe. **F(u)** : T(u) privée de u. Les **parents** de u sont les membres de F(u) quand u est hors du germe ; un constituant du germe n'a pas de parent.
- **T₀(p, q)**, pour p et q liés : la tuile contenant p et q la plus proche du germe. **Porte de q vue de p** : les trois autres constituants de T₀(p, q).
- **Vu de p et de c**, deux constituants liés : on envoie leur point de contact à l'infini. p et c deviennent deux plans parallèles. Les constituants liés aux deux sont des boules de diamètre 1 rangées en réseau triangulaire de pas 1 ; les tuiles contenant p et c sont les triangles du réseau ; les murs contenant p et c sont les plans verticaux au-dessus des droites du réseau. Une boule x liée à p et à c est une boule de diamètre 1 posée en un point ξ du plan, et ν(x, f) est le carré de la distance de ξ au point du réseau où est posé f.
- **Vu de p seul** : chaque voisin u de p porte le vecteur u + p, de norme nulle (X-28). Dans la base d'une tuile {p, f₁, f₂, f₃, f₄}, une boule liée à p est donnée par ses quatre coordonnées A₁, …, A₄ sur les f ; sa coordonnée sur p vaut leur somme moins 1, et pour deux telles boules ν(A, B) = (Σ A_k)(Σ B_k) − Σ A_k B_k. La boule est ronde si ν(A, A) = 0.

## 324. Faits admis

- (C1), (C2), (C3), (C3 bis) : ceux de X-28 et X-29. (C4) y est démontré. J'emploie (C3) et (C3 bis) aussi pour l'ensemble des tuiles qui contiennent **deux** constituants liés : cet ensemble a une tuile la plus proche du germe, T₀, et c'est la seule de l'ensemble qu'aucun mur passant par les deux constituants ne sépare du germe. C'est le même fait classique sur les groupes de Coxeter (projection sur un résidu, Tits). Une tuile est toujours d'un seul côté d'un mur (C2).
- **Conséquence de (C3 bis) que j'emploie sous cette forme** : si aucun des quatre murs d'une tuile T passant par u ne sépare T du germe, alors T = T(u). En effet, sinon un plus court chemin de T à T(u) parmi les tuiles de u commence par traverser un mur de T passant par u ; ce mur sépare T de T(u), donc du germe, puisque T(u) est sur un plus court chemin de T au germe (C3).
- **(C6), admis.** Vus de p, les voisins de p sont les sphères de Ford des entiers d'Eisenstein : on peut les repérer par des fractions réduites α/β de Q(ω), ω = e^{2iπ/3}, de sorte que ν(u, v) soit la norme du déterminant αδ − βγ. Les valeurs de ν entre deux voisins de p sont donc des normes d'entiers d'Eisenstein : 1, 3, 4, 7, 9, 12, 13, … Vu de p et de c, les voisins u de p avec ν(c, u) = 3 sont des boules de diamètre 1/3 posées aux centres des triangles du réseau ; ceux avec ν(c, u) = 4, des boules de diamètre 1/4 posées aux milieux des arêtes ; et pour deux voisins u, v de p autres que c, ν(u, v) = |z_u − z_v|² ν(c, u) ν(c, v). Raison : le groupe engendré par les quatre retournements qui fixent p est le groupe de réflexions du tétraèdre idéal régulier de sommets ∞, 0, 1, 1 + ω, qui conserve le système des sphères de Ford. Contrôlé par la clause V5. Source lue le 27 novembre, à travers un outil de lecture et non ligne à ligne : A. Kontorovich, « The local-global principle for integral Soddy sphere packings », Journal of Modern Dynamics 15 (2019), arXiv:1208.5441. Le sous-groupe qui fixe une sphère y est engendré par les quatre autres réflexions ; sa partie qui conserve l'orientation s'y conjugue dans PSL₂(Z[ω]) et y est un sous-groupe de congruence (lemme 3.21). Je n'y ai pas lu (C6) sous la forme employée ici.
- **(C7), le fait classique de K20a (X-27)**, écrit en entier à la demande du contre-auditeur. Soient b et c deux constituants liés. Les constituants d'une tuile sont les poids fondamentaux de ses murs (⟨e_i, n_j⟩ = 6 δ_ij) : les tuiles qui contiennent b et c forment donc une classe d'un sous-groupe engendré par trois retournements, qui est le groupe du pavage du plan par triangles équilatéraux. Vu de b et de c : les constituants liés aux deux sont des boules de diamètre 1 rangées en réseau triangulaire de pas 1 ; les tuiles contenant b et c sont les triangles du réseau ; les murs contenant b et c sont exactement les plans verticaux au-dessus des droites du réseau. Enfin, T₀(b, c) étant la seule de ces tuiles qu'aucun de ces murs ne sépare du germe, le germe est, pour chacun de ces murs, du côté du triangle de T₀(b, c). **K20a** : une boule liée à deux constituants liés a et b, et à deux autres constituants liés à a et à b, est un constituant.

## 325. Ce qui est démontré

**T15 (parents d'une paire liée). [T, sous les faits de la section 324]** Soient p et q deux constituants liés et T₀(p, q) = {p, q, a, b, c}. Alors a, b, c sont tous dans T(p), ou tous dans T(q). Plus précisément : T₀ = T(p), ou T₀ = T(q), ou bien T(p) = {p, q′, a, b, c}, où q′ est l'autre côté de la cellule {p, a, b, c}. Si p est dans le germe, T₀ = T(q).

Preuve. Notons m_p et m_q les murs de T₀ opposés à p et à q. Les trois autres murs de T₀ contiennent p et q : ils ne séparent pas T₀ du germe.

1. Si m_q ne sépare pas T₀ du germe, aucun mur de T₀ passant par p ne sépare T₀ du germe : T₀ = T(p). De même, si m_p ne sépare pas, T₀ = T(q). Si p est dans le germe, p est strictement du côté de T₀ par rapport à m_p, le germe aussi : m_p ne sépare pas, et T₀ = T(q).
2. Sinon m_p et m_q séparent tous deux T₀ du germe. Soit T₁ = {p, q′, a, b, c} la tuile voisine de T₀ à travers m_q. Je montre que T₁ = T(p). Ses murs passant par p sont m_q, qui ne sépare pas T₁ du germe, et les murs opposés à a, à b, à c. Prenons celui opposé à a ; il contient p, q′, b, c. Regardons depuis b et c. Les points p, q, a forment un triangle du réseau, et q′ = p + a − q. Le côté où se trouve le germe par rapport à un mur contenant b et c se lit sur le triangle Δ de la tuile T₀(b, c). Le mur de T₀ opposé à a est au-dessus de la droite (pq) : il ne sépare pas, donc Δ est du côté de a. Le mur m_q est au-dessus de la droite (pa), le mur m_p au-dessus de (qa) : ils séparent, donc Δ est de l'autre côté de (pa) que q, et de l'autre côté de (qa) que p. Δ est donc dans l'angle de sommet a opposé au triangle (p, q, a), formé des points a + s(a − p) + t(a − q), s et t positifs ou nuls. Le mur de T₁ opposé à a est au-dessus de la droite (pq′), parallèle à (qa) et passant par p. Un point de l'angle s'écrit p + (1 + s)(a − p) + t(a − q) : il est du même côté de cette droite que a, donc que T₁. Ce mur ne sépare pas T₁ du germe. Même raisonnement pour les murs opposés à b et à c, en regardant depuis (a, c) puis (a, b). Aucun mur de T₁ passant par p ne sépare T₁ du germe : T₁ = T(p), et a, b, c sont dans T(p).

**T16 (les trois quarts). [T, contrôlé par Lean]** Soit {p, c, f₁, f₂, f₃} une tuile, x une boule ronde liée à p et à c qui ne chevauche aucun des f, et w une boule ronde liée à p, dont les coordonnées dans la base de cette tuile sont positives ou nulles sur f₁, f₂, f₃, avec ν(c, w) > 0. Alors

ν(x, w) ≥ (3/4) ν(c, w),

et l'égalité n'a lieu que si x est le constituant obtenu en retournant un des f.

Preuve. Écrivons x = πp + γc + Σ a_k f_k. Les deux contacts donnent π = γ, que je note b, et Σ a_k = 1. La rondeur donne Σ a_k² = 2b + 1. On a ν(x, f_k) = 1 + c_k avec c_k = b − a_k, et le non-chevauchement dit c_k ≥ 0. Alors Σ c_k = 3b − 1 et Σ c_k² = 3b² + 1, d'où 2 Σ_{i<j} c_i c_j = 6b(b − 1). Le membre de gauche est positif ou nul et 3b ≥ 1 : donc b ≥ 1 (c'est la fenêtre, T13), et Σ c_k ≥ 2.

Écrivons w = π′p + γ′c + Σ φ_k f_k, φ_k ≥ 0, et Φ = Σ φ_k. Le contact avec p donne π′ = γ′ + Φ − 1 ; la rondeur donne 2Φγ′ = Σ φ_k² − Φ². On calcule ν(c, w) = Φ et ν(x, w) = Σ φ_k (1 + c_k) + γ′. Donc

4Φ (ν(x, w) − (3/4) Φ) = 4Φ Σ φ_k c_k + 2 Σ φ_k² − Φ².

Soit m le plus petit des φ_k, et φ_i, φ_j les deux autres. Comme les c_k sont positifs, Σ φ_k c_k ≥ m Σ c_k ≥ 2m. Et 8Φm + 2 Σ φ_k² − Φ² = (φ_i − φ_j)² + 9m² + 6m(φ_i + φ_j) ≥ 0. Le membre de droite est donc positif ou nul, et Φ > 0.

Égalité : il faut m = 0, φ_i = φ_j, puis c_i = c_j = 0, donc c_k = 3b − 1 et c_k² = 3b² + 1, soit b = 1 et c_k = 2 : x = p + c + f_i + f_j − f_k, le retourné de f_k.

Lecture, vu de p et de c. Si les trois sommets d'un triangle du réseau sont à distance au moins 1 de ξ, tout point du triangle est à distance au moins √3/2 de ξ ; l'égalité n'a lieu que si ξ est le point du réseau en face d'une arête, et le point le milieu de cette arête. Le rapport ν(x, w)/ν(c, w) est le carré de la distance de ξ au point où w est posé. Le facteur 3/4 est le meilleur possible même pour une boule hors de l'empilement : en posant ξ près d'un point du réseau, mais pas dessus, le rapport s'approche de 3/4 d'aussi près qu'on veut (le contre-auditeur est descendu à un écart de 3·10⁻⁶, section 330).

**T17 (cône). [T, contrôlé par Lean]** Soit x une boule ronde liée à p et à trois voisins distincts q, r, s de p, et w une boule ronde liée à p, avec ν(q, w) > 0, telle que ν(x, w) > (3/4) ν(c, w) pour c = q, r, s. Alors

ν(q, r), ν(q, s), ν(r, s) < 16/3, et ν(q, r) + ν(q, s) + ν(r, s) < 12.

L'hypothèse ν(q, w) > 0 est remplie par tout constituant w lié à p et autre que q : c'est ainsi que T19 l'emploie. (Le premier jet demandait que w soit un constituant ; la preuve ne s'en sert pas, le contre-auditeur l'a relevé.)

Preuve. Prenons la base d'une tuile contenant p et q (C4), et les coordonnées de la section 323. q a pour coordonnées (1, 0, 0, 0). Une boule ronde B liée à p avec ν(q, B) > 0 a une somme de coordonnées strictement positive : ν(q, B) = Σ B_k − B₁, et Σ B_k² = (Σ B_k)² donne |B₁| ≤ |Σ B_k| ; si la somme était négative ou nulle, ν(q, B) le serait aussi. C'est le cas de x (ν(q, x) = 1) et de w (par hypothèse).

Lemme du cône. Soient V, X, W trois quadruplets avec ν(X, X) = ν(W, W) = 0, Σ X_k > 0, Σ W_k > 0, ν(V, V) ≥ 0 et ν(V, X) > 0. Alors ν(W, V) ≥ 0. En effet, par Cauchy-Schwarz, (Σ V_k X_k)² ≤ (Σ V_k²)(Σ X_k²) ≤ (Σ V_k)² (Σ X_k)². Si Σ V_k était négative ou nulle, ν(V, X) > 0 donnerait Σ V_k X_k < (Σ V_k)(Σ X_k) ≤ 0, donc (Σ V_k X_k)² > (Σ V_k)² (Σ X_k)² : impossible. Donc Σ V_k > 0. De même (Σ W_k V_k)² ≤ (Σ W_k)² (Σ V_k)², et les deux sommes sont positives : Σ W_k V_k ≤ (Σ W_k)(Σ V_k).

Pour la paire (q, r), posons V = 3(Q + R) − 8X. Alors ν(V, V) = 18 ν(q, r) − 96, ν(V, X) = 6, et ν(W, V) = 3ν(q, w) + 3ν(r, w) − 8ν(x, w) < 0 par hypothèse. Le lemme interdit ν(V, V) ≥ 0 : ν(q, r) < 16/3. Pour le triplet, V = 3(Q + R + S) − 12X donne ν(V, V) = 18 (ν(q, r) + ν(q, s) + ν(r, s)) − 216, ν(V, X) = 9 et ν(W, V) < 0 : la somme est < 12.

Lecture. Le vecteur V serait de genre temps ou lumière, tourné vers l'avenir comme w + p : leur produit serait négatif ou nul. Autrement dit, dans le repère où x est un demi-espace, q, r, s sont trois boules de diamètre 1 dont les points de contact avec p tiennent dans un disque ouvert de rayon 2/√3.

**T18 (arithmétique d'Eisenstein). [T, sous (C6)]** Soient q, r, s trois voisins distincts de p, de ν deux à deux dans {1, 3, 4}, dont aucun n'est lié aux deux autres. Alors le triplet (ν(q, r), ν(q, s), ν(r, s)), trié, vaut (3, 3, 3), (1, 3, 4) ou (4, 4, 4). Dans les deux premiers cas, toute boule ronde liée à p, q, r et s est un constituant.

Preuve. Vu de p et de l'un des trois, mis à l'infini. Les deux autres sont de trois sortes : sur le réseau (ν = 1 avec celui de l'infini, diamètre 1), au centre d'un triangle (ν = 3, diamètre 1/3), au milieu d'une arête (ν = 4, diamètre 1/4). Entre eux, ν = |z − z′|²/(d d′). Les carrés de distances possibles sont : entre deux centres, 1/3, 1, 4/3, … (donc ν = 3, 9, 12, …) ; entre deux milieux, 1/4, 3/4, 1, … (ν = 4, 12, 16, …) ; entre un centre et un milieu, 1/12, 7/12, … (ν = 1, 7, …) ; entre un point du réseau et un centre, 1/3, 4/3, … (ν = 1, 4, …) ; entre un point du réseau et un milieu, 1/4, 3/4, 7/4, … (ν = 1, 3, 7, …).

- (1, 3, 3), en mettant à l'infini celui qui n'est pas dans la paire liée : deux centres avec ν = 1. Impossible. (1, 4, 4), de même : deux milieux avec ν = 1. Impossible.
- (3, 3, 4), en mettant à l'infini celui qui est à 3 des deux autres : deux centres avec ν = 4. Impossible. (3, 4, 4), celui qui est à 4 des deux autres : deux milieux avec ν = 3. Impossible.
- (3, 3, 3) : deux centres g, g′ avec ν = 3, donc à distance 1/√3 : deux triangles qui partagent une arête. Une boule liée aux trois est posée en un point ξ à distance 1/√3 de g et de g′ : ce sont les deux extrémités de l'arête, deux points du réseau. La boule est un constituant.
- (1, 3, 4), en mettant à l'infini un membre de la paire liée, avec l'autre membre à 4 du troisième : un point λ du réseau et un centre g avec |λ − g|² = 4/3. λ est le symétrique d'un sommet du triangle par rapport au côté opposé. ξ est à distance 1 de λ et 1/√3 de g : ce sont les deux extrémités de ce côté, deux points du réseau.

Il reste (4, 4, 4), de somme 12.

Autre preuve des quatre éliminations, contrôlée par Lean. Sous (C6), c étant à l'infini, deux voisins de p sont en α/β et γ/δ, avec ν(c, ·) égal à la norme de β et de δ, et ν entre eux égal à la norme de αδ − βγ. Si 3 divise les normes de β et de δ, 3 divise celle de αδ − βγ ; si 2 les divise, 4 divise celle de αδ − βγ. Donc deux voisins à 3 d'un même troisième sont entre eux à un multiple de 3, et deux voisins à 4 d'un même troisième, à un multiple de 4 : (1, 3, 3), (3, 3, 4), (1, 4, 4) et (3, 4, 4) sont exclus. Et une norme n'est jamais congrue à 2 modulo 3 : ν ne vaut jamais 2 ni 5.

**T19 = (G1). [T, sous les faits de la section 324]** Toute boule ronde x hors de l'empilement, liée à un constituant p et à trois voisins distincts q, r, s de p, chevauche un parent de p, q, r ou s.

Preuve. Supposons que x ne chevauche aucun parent des quatre. Pour c parmi q, r, s, notons G_c la porte de c vue de p.

Premier point : si p et c ne sont pas tous deux dans le germe, x ne chevauche aucun membre de G_c. Par T15, G_c est dans T(p) ou dans T(c). Si p est dans le germe, T₀(p, c) = T(c) et c est hors du germe : G_c est fait de parents de c. Si c est dans le germe, de même G_c est fait de parents de p. Si aucun n'y est, G_c est fait de parents de p ou de parents de c.

Second point : tout membre w de T(p) autre que p et c a des coordonnées positives ou nulles sur G_c dans la base de T₀(p, c). En effet la coordonnée de w sur un membre g de G_c vaut ⟨w, n⟩/6, où n est la normale du mur de T₀(p, c) opposé à g, tournée vers g : elle est positive ou nulle si et seulement si w est sur ce mur ou du côté de g. Or ce mur passe par p et c : il ne sépare du germe ni T₀(p, c), ni T(p). Les deux tuiles sont du même côté, et w est sur ce mur ou de ce côté.

Cas 1 : p est dans le germe, et l'un des trois aussi, disons q. Pour c = r ou s hors du germe, T16 s'applique à w = q : 1 = ν(x, q) ≥ (3/4) ν(c, q), donc ν(c, q) = 1. Un c du germe est lié à q. Donc r et s sont liés à p et à q, et K20a dit que x est un constituant : contradiction.

Cas 2 : sinon. Les trois portes sont libres. T(p) a quatre membres autres que p ; l'un d'eux, w, n'est ni q, ni r, ni s. T16 donne ν(x, w) ≥ (3/4) ν(c, w) pour c = q, r, s, sans égalité puisque x n'est pas un constituant. Et ν(q, w) ≥ 1, w et q étant deux constituants distincts. T17 : les trois ν sont < 16/3 et leur somme est < 12. Par (C6) ils sont dans {1, 3, 4}. Si l'un des trois était lié aux deux autres, K20a ferait de x un constituant. Sinon T18 ne laisse que (3, 3, 3) et (1, 3, 4), où x est un constituant, et (4, 4, 4), de somme 12. Contradiction dans tous les cas.

Trois remarques. La preuve n'emploie l'hypothèse que sur les parents qui sont dans les portes. Elle n'emploie pas l'indépendance des quatre contacts : trois voisins distincts suffisent. Et la marge est nulle au cas (4, 4, 4) : x est alors une boule posée au milieu d'une arête, quatre fois trop grosse, et le lemme du cône tombe juste sur l'égalité. C'est pourquoi le facteur 3/4 de T16 ne peut pas être remplacé par un plus petit sans changer la fin de la preuve.

## 326. Ce qui est devant Lean

Deux fichiers, Lean 4 seul, sans Mathlib, écrits à la main, dans `calculs/lean_x30bis/`.

**`TroisQuartsEtCone.lean`, la clause V7 de la prédiction.** Trois théorèmes : `trois_quarts` (l'inégalité de T16), `cone_paire` et `cone_triplet` (T17, avec pour hypothèse que les sommes de coordonnées de x et de w sont positives). Ils sont énoncés dans **tout anneau commutatif totalement ordonné** : les boules à coordonnées irrationnelles sont couvertes, ce que X-28 et X-30 ne faisaient pas. La prédiction ne promettait que des données rationnelles.

**`Complements.lean`, ajout non scellé**, écrit après les calculs, pendant le contre-audit. Sept théorèmes.

- `trois_quarts_egalite` : sous les hypothèses de T16, l'égalité force x = p + c + f_i + f_j − f_k. L'inégalité est donc stricte pour une boule hors de l'empilement.
- `cone_paire_complet`, `cone_triplet_complet` : T17 sans hypothèse de signe sur x ni sur w. Il suffit que q soit de somme positive (c'est (1, 0, 0, 0) dans la base d'une tuile contenant p et q) et que ν(q, w) > 0.
- `norme_pas_2`, `norme_pas_5`, `det_div3`, `det_div4` : l'arithmétique de T18 (section 325), sur les entiers.

| Contrôle | `TroisQuartsEtCone.lean` | `Complements.lean` |
|---|---|---|
| Lean 4.35.0 ; axiomes `propext`, `Classical.choice`, `Quot.sound` | accepte | accepte |
| `leanchecker`, `leanchecker-paranoid` | acceptent | acceptent |
| nanoda 0.4.19, tout autre axiome interdit | accepte (3 009 déclarations) | accepte (3 440 déclarations) |
| con-ron, con-leche | 2 701 déclarations acceptées chacun | 3 121 déclarations acceptées chacun |
| Énoncés modifiés : le script de preuve ne passe plus | neuf sur neuf | sept sur sept |

Les énoncés modifiés. Premier fichier : conclusion de T16 renforcée d'une unité ; chevauchement de f₃ permis ; somme nulle permise ; w hors du secteur ; rondeur de x remplacée par une inégalité ; 15 au lieu de 16 ; 11 au lieu de 12 ; w non rond ; 2/3 au lieu de 3/4. Second fichier : coordonnée 2 au lieu de 1 dans le cas d'égalité ; un seul des trois retournés ; produit nul permis dans le lemme de signe ; « jamais 1 modulo 3 » ; divisibilité par 9 au lieu de 3 ; par 8 au lieu de 4 ; une seule des deux normes divisible par 3. Ce contrôle montre que les preuves se servent de leurs hypothèses. Il ne montre pas que les énoncés modifiés sont faux.

Ce qui reste hors de Lean : T15 ; dans T18, le fait que les boules tangentes des types (3, 3, 3) et (1, 3, 4) sont posées en des points du réseau ; T19 ; le dictionnaire entre boules et coordonnées, écrit en tête des deux fichiers ; les faits admis de la section 324.

## 327. Les sept clauses chiffrées

| Clause | Prédit | Obtenu | Verdict |
|---|---|---|---|
| V1, T15 sur données, palier 5 | zéro exception ; les trois cas se produisent | 8 010 paires liées, aucune exception ; 10 paires dans le germe ; T₀ tuile-porte d'un seul des deux : 7 180 ; d'aucun des deux : 820, toutes de la forme annoncée | vraie |
| V2, T16 sur données, palier 3 | zéro exception ; égalité seulement dans l'empilement | 237 300 boules ; 62 220 triplets (boule, contact à porte libre, w) ; aucune exception ; 1 980 égalités, toutes pour des boules de l'empilement ; 360 triplets pour des boules hors de l'empilement, plus petit rapport 9/7 ; aucune boule irrationnelle n'a de porte libre | vraie |
| V3, types sur données, palier 3 | (a) quatre types absents ; (b) (3,3,3) et (1,3,4) : boules dans l'empilement ; (c) (4,4,4) présent, une boule dedans, une hors ; (d) hors de l'empilement avec ν < 16/3 : seulement (4,4,4) ; (e) pas de ν égal à 2, 5 ou 6 | 148 320 quadruples. (a) aucun. (b) 420 et 3 060 quadruples, 840 et 6 120 boules, toutes dedans. (c) 720 quadruples, 720 boules dedans, 720 hors. (d) aucune exception. (e) aucune ; valeurs rencontrées : 1, 3, 4, 7, 9, 12, 13, 16, 19, … | vraie |
| V4, modèle de Ford-Eisenstein | mêmes conclusions, zéro exception | 187 sommets ; six types présents : (1,1,1), (1,1,3), (1,1,4), (1,3,4), (3,3,3), (4,4,4) ; (1,3,4) : 960 boules, toutes dedans ; (3,3,3) : 156, toutes dedans ; (4,4,4) : 162 triplets, 162 boules dedans, 162 hors ; un contact lié aux deux autres : 921 boules, toutes dedans | vraie |
| V5, (C6) sur données, palier 6 | zéro exception | 979 voisins du premier constituant du germe ; chacun en un point α/β réduit avec norme(β) = ν ; normes de 1 à 52 ; 478 731 paires, toutes cohérentes avec ν(u, v) = \|z_u − z_v\|² ν(c, u) ν(c, v) | vraie |
| V6, cas critique et tirage | x chevauche toujours un sommet d'une des trois portes | cas critique : 1 577 bases à distance au plus 7 ; 1 106 sans porte libre, 471 avec une seule, aucune avec deux ou trois. Tirage : 20 000 cas, dont 4 280 boules irrationnelles ; 5 987, 13 378, 635 et 0 cas à zéro, une, deux et trois portes libres | vraie |
| V7, Lean | T16 et T17 acceptés pour des données rationnelles | acceptés (`TroisQuartsEtCone.lean`), et pour tout anneau commutatif totalement ordonné (section 326) | vraie |

Détail de V2. Le contrôle a un témoin : sur les 2 739 480 triplets dont la porte est chevauchée, 2 560 560 sont sous les trois quarts. L'inégalité n'est donc pas vide. L'hypothèse de T16 sur w (coordonnées positives ou nulles sur la porte) est vérifiée dans tous les triplets contrôlés. Le plus petit rapport, 9/7, est celui de ces données, où x est liée à quatre constituants ; ce n'est pas la borne de T16, qui est 3/4.

Détail de V3. Au palier 3, sur les 190 200 boules hors de l'empilement, 190 080 n'ont aucune porte libre et 120 en ont une seule. Aucune n'en a deux. Le théorème dit qu'aucune n'en a trois ; les données sont loin du bord.

Détail de V6. Le programme `x30bis_ford.py` n'importe rien du laboratoire. Ses témoins : 1 100 portes comparées à un parcours en largeur, aucune différence (2 400 portes calculées ; pour les 1 300 autres, le sommet est trop loin de la base pour que le parcours le rencontre) ; et avec deux contacts seulement, 85 bases sur 287 où les deux portes sont libres. L'énoncé a bien besoin de trois voisins.

## 328. Ajouts non scellés

**Compléments devant Lean. [T]** Le cas d'égalité de T16, T17 sans hypothèse de signe, l'arithmétique de T18 : section 326.

**Toutes les boules d'une fenêtre, toutes les bases proches. [M]** Sommets de dénominateur de norme au plus 7 à distance au plus 1,5 (145 sommets) ; les 3 582 boules hors de l'empilement tangentes au sommet de l'infini et à deux d'entre eux, dont 552 irrationnelles ; les 287 bases à distance au plus 5. Sur 1 028 034 couples (boule, base) : 537 772 sans porte libre, 449 516 avec une, 40 746 avec deux, aucun avec trois. T16 : 1 990 729 triplets, aucune exception ; plus petit rapport ν(x, w)/ν(c, w) : 0,859. Sortie : `x30bis_ford_exhaustif_7_1.5_5.out`. Le premier lancement, plus grand, a été arrêté (section 322, point 5).

## 329. Ce que (G1) entraîne

Par T11 (X-29 bis), (G1) entraîne (G), puis (C*) :

**Dans tout tissu clos par plancher, toute place admissible est dans l'empilement. [T, sous les faits de la section 324]**

Par T10, le tissu de la règle à la lettre est clos par plancher à tout palier. Donc, **à tout palier, toute place admissible du tissu de la règle à la lettre est dans l'empilement**. La question ouverte depuis X-27 est fermée pour cette moitié. Il en va de même des paliers incomplets, de la file d'attente de X-28, et de toute croissance où nul ne naît avant ses quatre parents.

(G1) donne aussi un critère local, sans histoire : dans n'importe quel tissu, une place admissible dont les quatre contacts ont leurs parents nés est dans l'empilement. Le contre-exemple de X-27 viole exactement cette condition.

Ce que cela ne donne pas. Que la place soit le côté d'une cellule née (la seconde moitié de (C)). Que la condition soit nécessaire. Quelle règle de naissance est celle du Blob.

## 330. Contre-audit indépendant

Un sous-agent Claude Opus, qui n'a pas vu mon raisonnement : il a reçu le carnet, les fichiers et la consigne de chercher ce qui est faux ou troué. Son code est écrit à neuf et n'importe rien du laboratoire ni de mes programmes. Rapport versé tel quel : `calculs/x30bis_contre_audit_rapport.md`. Son code et ses sorties : `calculs/x30bis_contre_audit/`. C'est une IA de la même famille que le pilote, pas un mathématicien.

**Verdict.** Aucun pas faux ni aucun trou dans T15, T16, T17, T18 et T19, une fois admis les faits de la section 324. Il a refait l'algèbre de T16 et de T17, relu l'argument de T15 vu de b et c, repris la liste des carrés de distances de T18 et le découpage en cas de T19.

**Cinq imprécisions, et ce que j'en ai fait.**

| Ce qu'il a relevé | Suite donnée |
|---|---|
| T15, second cas : trois faits employés sans figurer parmi les faits admis (les murs par b et c sont les plans au-dessus des droites du réseau ; T₀(b, c) est un triangle ; le germe est du côté de ce triangle). À son sens, le maillon admis le plus fragile, même s'il est classique | (C7) est maintenant écrit en entier en section 324, avec la raison qu'il donne |
| T19, second point : il manque la ligne qui relie la coordonnée au côté du mur | ajoutée |
| L'inégalité stricte de T19 repose sur le cas d'égalité de T16, absent de Lean | `trois_quarts_egalite`, dans `Complements.lean` (section 326), écrit pendant son passage |
| L'énoncé de T17 demande que w soit un constituant ; la preuve et Lean n'emploient qu'une boule ronde liée à p | énoncé corrigé |
| Le facteur 3/4 de T16 est atteint à la limite par des boules hors de l'empilement ; mes minima (9/7, 0,859) viennent des configurations de (G1), pas de T16 en général | dit dans T16 et dans le détail de V2 |

**Ses calculs.**

| Point | Ce qu'il a obtenu |
|---|---|
| T15, paliers 4 et 5 | 1 980 et 8 010 paires liées, aucune exception ; au palier 5, les mêmes comptes que la clause V1 (10, 7 180, 820) |
| T16 | 359 803 couples (x, w) en arithmétique exacte, aucune violation ; 10 égalités, toutes pour des constituants ; 189 540 couples en flottants pour des boules irrationnelles, aucune violation |
| T16, borne | des boules hors de l'empilement, liées à p et à c seulement, dont le rapport descend à 3/4 + 3·10⁻⁶ |
| T18, modèle de Ford | (1, 3, 4) : 324 triplets, 648 boules, toutes au réseau ; (3, 3, 3) : 42 triplets, 84 boules, toutes au réseau ; (4, 4, 4) : 96 triplets, 96 boules au réseau, 96 hors ; les quatre types interdits absents ; entre deux sommets de dénominateur de norme au plus 7, les seules valeurs de ν sous 16/3 sont 1, 3 et 4 |
| (C6) sur données | 2 899 voisins du premier constituant du germe, normes de 1 à 109 ; 4 200 651 paires, aucune exception |
| (G1), tuiles de longueur 8 à 30 | 326 273 boules hors de l'empilement, dont 77 254 irrationnelles : aucun contre-exemple, jamais trois portes libres |
| Second point de T19 | 77 479 contrôles, aucune exception |
| Lean | sa copie compile ; les trois théorèmes disent bien T16 et T17 ; leurs hypothèses sont satisfaites par des exemples entiers (`Exemples.lean`) |

**Ce que j'ai vérifié de son rapport.** Sa sortie `c_ford.out` était tronquée : j'ai relancé `c_ford.py` en entier (`c_ford_rejeu.out`) et retrouvé ses nombres pour T18 et (C6). Ses tirages en profondeur sont trois lancements à durée fixée ; le premier (37 945 boules hors de l'empilement) n'a pas été enregistré. Les sorties versées couvrent donc 288 328 de ses 326 273 boules, et 71 376 de ses 77 479 contrôles du second point. Les autres nombres sont dans ses sorties.

**Ce qu'il déclare ne pas avoir contrôlé.** Les faits admis, sauf (C6) sur données. La descente qui donne les tuiles-portes n'est comparée à un parcours en largeur que jusqu'à la longueur 10, et ses tirages profonds en dépendent. Il n'a pas relancé les vérificateurs de Lean, ni les énoncés modifiés, ni le palier 6. Des tirages ne sont pas une preuve de (G1).

**Antériorité.** Lui et moi avons lu le même article, chacun à travers un outil de lecture : celui de Kontorovich cité en section 324. D'après cette lecture, il ne contient ni (G1) ni T16. Rien d'autre n'a été cherché. Je ne conclus rien sur la nouveauté.

## 331. Ce que cela donne, et ce que cela ne donne pas

Cela donne une démonstration de (G1), dont deux lemmes sur cinq sont en entier devant Lean et trois vérificateurs extérieurs, pour des coordonnées quelconques. La lecture « le nouveau-né hérite des liens du parent, et sa forme est fixée par les contacts » redonne la naissance dans l'empilement au rang 3 dès que nul ne naît avant ses quatre parents : c'est maintenant un théorème, sous des faits classiques admis, et non plus un constat.

Cela ne valide pas la TOE et ne démontre pas la cosmogonie. Cela ne donne ni l'espace-temps, ni la gravitation, ni rien de quantique. C'est un énoncé sur les empilements de sphères, appliqué à une lecture du pilote.

## 332. Suite proposée

Pour le premier maillon : la seconde moitié de (C), puis le lien entre ces deux réalisations de la mitose et la division de l'arête, qui n'est pas entamé. Pour la validation elle-même, le deuxième maillon de la section 5 du registre : le temps.

## 333. Fichiers

- `calculs/x30bis_demonstration_de_G1_prediction.txt` : prédiction scellée.
- `calculs/x30bis_G1.py` : contrôles sur les paliers. Sorties : `x30bis_V1_5.out`, `x30bis_V23_3.out`, `x30bis_V5_6.out`.
- `calculs/x30bis_ford.py` : modèle de Ford-Eisenstein, indépendant. Sorties : `x30bis_ford_temoin.out`, `x30bis_ford_V4.out`, `x30bis_ford_V6_critique.out`, `x30bis_ford_V6_tirage.out`, `x30bis_ford_exhaustif_7_1.5_5.out`.
- `calculs/lean_x30bis/` : `TroisQuartsEtCone.lean`, `controle.sh`, `controle.out` (clause V7) ; `Complements.lean`, `controle_complements.sh`, `controle_complements.out` (ajout non scellé).
- `calculs/x30bis_contre_audit_rapport.md` : rapport du contre-audit, versé tel quel, suivi des précisions de son message final.
- `calculs/x30bis_contre_audit/` : le code du contre-auditeur (`noyau.py`, `a_paliers_T15.py`, `b_T16.py`, `c_ford.py`, `d_G1_profond.py`, `Exemples.lean`), ses sorties, et `c_ford_rejeu.out`, ma relance.

TOE 0/7. Aucun verrou fermé.
