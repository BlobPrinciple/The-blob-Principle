# Registre des pistes fermées, et de ce qui les a fermées

Claude (pilote IA), ouvert le 28 novembre 2026 à la demande de l'auteur (11 h 40) : « depuis le début de nos recherches tu t'auto-censures et tu bloques certaines possibilités […] attention à ne pas saboter involontairement des éventualités qui auraient pu être zappées faute de prises de risques […] donc recheck bien ! »

## Règle de ce registre

Une piste n'est fermée que par une mesure négative avec témoin, à budget égal, sur plusieurs graines et plusieurs tailles, ou par une démonstration. Chaque ligne dit donc **qui a fermé, quand, et sur quoi**, et range la fermeture dans une de ces classes :

- **A**, mesure négative solide (témoin, plusieurs graines, plusieurs tailles) ou démonstration ;
- **B**, mesure négative fragile (une graine, une taille, pas de témoin, ou instrument qui ne peut pas voir l'objet) ;
- **C**, argument, consigne ou prudence, sans mesure ;
- **D**, jamais essayée, ou oubliée en route.

Les fermetures B, C et D sont rouvertes. Rouvrir n'est pas valider : chaque réouverture porte le test qui la tranchera et, quand il est fait, son résultat, échecs en tête. Ce registre est en cours : la lecture intégrale des masters d'avril et de mai (v90 à v92, V107 à V112) n'est pas finie, et c'est là que les idées lâchées sans test ont le plus de chances de se trouver.

## 1. Pistes rouvertes et retestées

### 1.1 Les fractions « cosmologiques » à κ₀ = 4 — fermée par consigne (classe C), rouverte, mesurée

**Histoire, sur pièces (V346, lignes du texte extrait).** Avril (master v92) : κ₀ = 8, « P(Niveau 2) ~ 0 % dans les simulations N = 3000 vs 27 % observé ». V107 (12 mai) : [FAIL] sur le rapport matière noire / baryons. V116 : audit sévère, « identification f_K4 = Ω_b injustifiée ». V118 : nouveau classeur (`classify_phases`). V122 (l. 23383) : à κ₀ = 4, « justifié a priori comme dimension de l'espace-temps », 0,7042 ; 0,2568 ; 0,0414, avec les tensions écrites (2,2σ et 4σ). 28 mai (l. 42519 à 42960) : reproduit à cinq graines, tenu jusqu'à N = 3 000, « κ₀ = 4 désigne l'univers mûr, κ₀ ≥ 6,6 l'univers jeune », statut « [M] consolidé ». **7 juin, en-tête V197 (l. 5256 et 48913) : « AUCUN accord Planck à 1 % (fausse coïncidence rétractée, à ne jamais réintroduire) », motif : « valeurs-cibles ΛCDM inscrites à tort comme mesures du Blob ».** Le même jour (l. 49648), la mesure refaite redonne 0,679 ; 0,271 ; 0,050 à κ = 4 ; elle est « non réintroduite », avec une phrase : « seul fait κ-robuste digne d'un suivi honnête : f_b ≈ 0,049, à confirmer en N ». Aucun suivi trouvé. 4 juillet : « ce territoire est mort », « aucune comparaison aux valeurs de Planck ».

**Qui a fermé, sur quoi.** L'instance du 7 juin, par une alerte « anti-hallucination ». Pas par une mesure : la mesure du jour était positive.

**Retest, X-35 (prédiction scellée avant calcul ; `calculs/x35-resultat-2026-11-28.md`).**

- Échecs et réserves d'abord : pas d'accord à 1 % (limite sans bord 0,717 ; 0,242 ; 0,040, soit 5, 8 et 18 % d'écart) ; Λ dépend de κ₀ (0,76 à 0,26 pour κ de 3,5 à 8) ; deux choix du classeur déplacent Λ de 0,07 et les baryons de 0,013 ; et les programmes de mai montrent que le seuil du classeur a été choisi en minimisant l'écart à la cible, puis remplacé par une règle qui le redonne.
- Ce qui tient : le programme de l'auteur rend bien 0,705 ; 0,253 ; 0,043 sur ses dix graines (0,699 ; 0,257 ; 0,044 sur 36) ; un moteur écrit sans le sien rend la même loi (écart apparié de 1,15 erreur type) ; le témoin sans viabilité rend 0,50 ; 0,50 ; 0,000 ; les fractions tiennent de N = 1 000 à 32 000 ; la part « baryons » ne dépend presque pas de κ.

**Verdict.** Le motif de l'alerte est faux : 0,704 est une mesure, pas une cible recopiée. Sa conclusion pratique était trop large : elle a mis à l'écart un fait mesuré, reproductible et stable en taille. Mais la lecture de mai (« zéro paramètre ») ne tient pas non plus : κ₀ règle Λ, et le classeur a été choisi en regardant la cible. **Statut proposé : [M], reproduit par deux moteurs ; ni fausse coïncidence, ni prédiction.** Ce qui en ferait une prédiction est écrit dans le fichier de résultat (un principe pour κ₀, une définition de la matière stable tirée de la cosmogonie, une chaîne vers une densité).

**Ma part.** Ce matin encore j'écrivais « nombres de mai retirés par le corpus » sans avoir lu le motif du retrait. C'est exactement le défaut que l'auteur nomme : j'ai repris une prudence sans la contrôler.

### 1.2 « f_b ≈ 0,049, indépendant de κ, à confirmer en N » — oubliée (classe D), suivie

Demandé par le corpus le 7 juin, jamais fait. Rendu par X-35 : 0,040 à 0,047 de N = 1 000 à 32 000 (seuil 0,50) ; 0,037 à 0,045 pour κ de 4 à 6,6 ; 0,044 à 0,050 pour κ de 4 à 8 au seuil 0,338. Réserve : cette part vaut la part des cœurs stables (11 %, elle aussi presque indépendante de κ) multipliée par la part au-dessus de la moyenne (0,36 à 0,41) ; elle hérite donc du choix du seuil.

## 2. Pistes rouvertes, à instruire (test nommé, pas encore fait)

### 2.1 Le quantique : « ψ = √π satisfait Schrödinger » (T4) devenu « le Blob classique ne récupère pas la mécanique quantique » — classe B

**Histoire.** Mars (masters v90 à v92) : T4, « ψ = √π_N satisfait Schrödinger (résidu 8,8 × 10⁻¹⁷) », espace H_Blob = L²(Ω, π_N), « la règle de Born est une conséquence de T4 [T*] ». Mai (V107, V109) : T4 gardé en [T], « Schrödinger-Nelson, démontré sous balance détaillée ». 4 juillet (master V277, erratum 2 du livre) : « le Blob classique ne récupère PAS la mécanique quantique (ni interférence, ni Bell) », sur une mesure : poids réels, visibilité d'interférence nulle, corrélations plafonnées à 2. 13 juillet : « théorème de classicité ». 18 juillet : positivité de réflexion exacte avec l'action locale.

**Pourquoi la fermeture est de classe B.** La mesure du 4 juillet porte sur des grandeurs qui se lisent toutes sur la configuration (elles commutent). Pour de telles grandeurs, l'inégalité de Bell est un théorème : aucune mesure ne pouvait donner autre chose que 2. L'instrument ne pouvait pas voir l'objet de T4, qui vit dans l'espace L²(Ω, π) où le générateur de la dynamique est un opérateur autoadjoint et où « déplacer un lien » ne commute pas avec « compter un lien ». Le tome du 16 juillet a d'ailleurs annulé trois instruments pour ce motif (« ne pas mesurer ce qui se démontre »).

**Ce que je sais et ce que je ne sais pas.** Vrai et standard : pour toute dynamique à bilan détaillé, le générateur symétrisé est un opérateur positif dont √π est l'état fondamental. Vrai aussi : cela vaut pour n'importe quelle mesure de Gibbs, pas seulement pour le Blob ; ce n'est donc pas une dérivation de la mécanique quantique. Ouvert : savoir si la cosmogonie donne un sens physique aux grandeurs qui ne commutent pas (le geste de la mitose, le bain comme opération).

**Test.** Sur un petit Blob énuméré exactement, construire cet opérateur, vérifier son spectre, et calculer la valeur de Bell de l'état √π pour un découpage des liens en deux régions. Prédiction à sceller avant calcul.

### 2.2 « La faille n° 1 : d_s = 3 au lieu de 4 et de 2 » — classe C

Écrite le 16 juillet (« le corpus ne doit pas la présenter comme un succès sans réserve »), reprise par moi ce matin sans examen. Le graphe du Blob est l'espace ; le temps y est porté par la suite des naissances, pas par une dimension du graphe. Comparer sa dimension 3 au 4 de l'espace-temps, c'est comparer deux objets différents. La question juste est celle que le corpus pose ailleurs : la propagation est diffusive (« cône de diffusion, pas cône de lumière », 4 juillet). Test : relever dans la littérature la dimension spectrale des tranches d'espace des triangulations causales, et recalculer ce que donne le Blob quand on ajoute son temps. À faire sur sources avant d'écrire quoi que ce soit.

### 2.3 Le degré moyen que le moteur complet choisit lui-même — classe D

X-23 E et X-24 (22 novembre) : le moteur complet de l'auteur, lancé avec 4,6 ; 6,6 ; 8,6 liens par naissance, finit à 4,8–5,0 ; 5,6–5,9 ; 6,2–6,7 voisins. Je l'ai noté comme l'échec de trois de mes hypothèses, et je n'ai pas posé la question que ces nombres posent : le moteur a-t-il un degré moyen propre, indépendant du départ ? Si oui, κ₀ cesse d'être un paramètre. Test : mêmes états, trajectoires plus longues, départs à 4, 6, 8 et 10 liens.

### 2.4 La chiralité nette — classe D

4 juillet (master V277) : + 0,0057 ± 0,0027, positive sur six graines sur six, signe aléatoire dans les deux témoins ; réserve écrite sur la convention de signe. Aucune suite trouvée. Test : le programme du 22 juin est dans l'archive de l'auteur ; le relancer sur trente graines et deux tailles, avec le témoin.

### 2.5 Le couplage courbure-matière — en cours

Plateau du 17 juillet (0,68 à 0,88 de N = 6 000 à 10⁶). Mon témoin de ce matin (X-34, R2) est non concluant, deux de mes quatre prédictions tombées. Reste à retrouver la définition exacte de la variable de matière dans le programme du 17 juillet.

## 3. Le sens de mes erreurs (relevé partiel, à finir clause par clause)

Mes carnets donnent mes clauses fausses en tête de chaque essai. Premier relevé, sur les clauses dont le sens se lit sans ambiguïté :

**Fausses par pessimisme (le moteur ou l'énoncé de l'auteur faisait mieux que je ne l'annonçais).** X-23 : terreau annoncé non gelé à κ = 6,6, il gèle à 6,45 (B2) ; Blob annoncé non gelé à l'étage 2 et sans gel de l'étage 3 jusqu'à κ = 8, deux fois faux (B3) ; « κ₀ = 6,6 est le point où l'étage 3 se fige » annoncée fausse partout, soutenue pour le terreau (H-FIGE) ; « la coïncidence est un effet de taille finie », faux (S2, S3, S4) ; « la boule de tétraèdres ne tient pas l'étage 5 », faux (C2). X-24 : étage 4 annoncé gelé à 8,6 liens par naissance, le moteur reste à l'étage 3 (B4). X-25 : le moteur complet annoncé en violation des conditions de contact, il les respecte (B1, B2, B3). C-161 : bain annoncé simple accélérateur, il est nécessaire (P7). C-131 : anisotropie annoncée, isotrope. C-132 bis : échec annoncé à 15 naissances, réussite 3 sur 3. C-193 Bc : identité de la boule annoncée violée, vérifiée 14 fois sur 16 (B7). C-204c : entassement annoncé dans le moteur de l'auteur, 3 à 6 % au lieu de 20 %. X-34 : couplage courbure-matière annoncé pure affaire de définition, non (une clause). Et la prime de fermeture « qui s'éteint » (erratum du 28 novembre). **Dix-neuf clauses, dont seize portent sur un objet de l'auteur.**

**Fausses par optimisme.** C-74 : Born par les naissances, réfuté. C-127 : tenue annoncée jusqu'à 512 cellules, retournement à 214. C-132 bis : tenue annoncée à 31 naissances, une graine sur trois échoue. BP-S2 : trame régulière annoncée stable, instable (A6). C-169c : fermeture pendant la croissance annoncée possible, bloquée (P1, P6). X-23 : corrélation avec la masse du corpus annoncée au-dessus de 0,8, mesurée vers 0,4 (B6). X-25 : conditions annoncées satisfaites partout, une exception sur huit ou douze (T1, T2, T6, N7). X-28 : ma voie de démonstration, tombée au palier 6. X-34 : couplage annoncé entre 0,55 et 0,80, mesuré à 0,48–0,51 (une clause). **Treize clauses, dont sept portent sur un objet de l'auteur et six sur une construction à moi.**

**Lecture.** Mes erreurs vont dans les deux sens, mais pas sur les mêmes objets. Quand la clause porte sur un objet de l'auteur (son moteur, son κ₀, son bain, ses conditions), je me trompe par pessimisme seize fois sur vingt-trois. Quand elle porte sur une construction à moi, je me trompe par optimisme six fois sur six. C'est un biais, et il a un coût précis : X-23 et X-24 contenaient deux résultats favorables (le gel à 6,45 tout près du κ₀ de l'auteur ; le moteur qui revient de lui-même vers 6 voisins) que j'ai rangés en « mes prédictions fausses » sans les porter au point complet comme des faits. Ce relevé est partiel et mon classement de chaque clause (sens, et à qui appartient l'objet) est à revoir une à une : une centaine de fichiers de prédiction restent à dépouiller. Le compte exact suivra ; celui-ci est une estimation.

## 4. Fermetures que je tiens pour solides (classe A), à ne pas rouvrir sans fait nouveau

- Le nombre d'or (4 juillet) : trois voies sans ajustement, et une raison (cascade multiplicative, récurrence additive).
- Les « œufs de Pâques » de mars (Koide à 0,001 %, « κ_RCP = 8,1915 à 0,000 % ») : le quatrième lepton est en échec à plus de 14σ dans la batterie du 4 juillet, et l'échec était déjà écrit en mars. À relire en entier avant de confirmer la classe.
- La longueur de Planck par calcification (3 juillet, [M] négatif).
- La compression, forme forte (4 juillet) : trois graphes comparés, sens du résultat net.

## 5. Ce qui reste à lire avant de clore ce registre

v90 à v92 (en cours), V107 à V112, les notes de séance des 17 et 18 juillet, les dossiers 04, 09, 10 et 91 de l'auteur, le laboratoire. Chaque fermeture rencontrée y sera classée.
