# Carnet du 22 novembre 2026 — X-23 : la règle de l'étage, démontrée sur les coques, mesurée dans les moteurs de l'auteur

Auteur unique : Rudolphe Mirante. Pilote IA et contre-auditeur : Claude (modèle claude-fable-5-2, choisi par l'auteur pour cette session). Contre-audit et recoupement indépendants : deux agents Claude sans accès à mes programmes (indépendance de programme, non de lignée : même famille de modèles que le pilote). Audit croisé avec ChatGPT : aucun ce jour, aucun message envoyé. Les numéros de section poursuivent ceux du carnet du 20 novembre.

**État en tête : TOE 0/7. Aucun verrou fermé.**

## 207. Ce qui est faux, dit en premier

**Prédictions scellées fausses.**

1. **A5** : « la naissance dans le volume garde la coque juste à l'étage k+1 pour tout k ». Faux au rang 1 : la cellule d'un polygone est son lien, la naissance « dans la cellule » y est la mitose de l'arête, et le polygone ne tient pas. Vrai aux rangs 2, 3 et 4. Trouvé par mon programme et, séparément, par le contre-audit.
2. **A6** : « sphères de rang 3 tirées au hasard : auto-contraintes > 0 ». Trop fort : le contre-audit produit une enveloppe à 6 sommets qui est empilée, donc sans auto-contrainte. Énoncé correct : ≥ 0, nul pour les seules empilées.
3. **B2** : j'annonçais le terreau non gelé à l'étage 3 à κ = 6,6 et un seuil entre 7 et 9,5. Faux : le seuil est à 6,45.
4. **B3** : j'annonçais le Blob non gelé à l'étage 2 au point de travail (confiance 60 %). Faux : 91 à 94 % de ses constituants sont dans un seul amas rigide. J'annonçais aussi « aucun gel de l'étage 3 du Blob jusqu'à κ = 8 ». Faux : seuil à 7,1–7,2.
5. **B6** : « le poids suit la masse du corpus, corrélation de rangs > 0,8 ». Faux pour le Blob : 0,38 ; 0,39 ; 0,47. *(Note du 23 novembre : ces trois décimales ne sont pas reproductibles au chiffre près — au rejeu, 0,40 et 0,42 pour les deux premières ; le verdict tient. Voir le carnet du 23 novembre, faute 30.)*
6. **H-FIGE** (« κ₀ = 6,6 est le point où l'étage 3 se fige ») : je la prédisais fausse partout. Elle est fausse pour le Blob et **soutenue pour le terreau**, selon le critère que j'avais scellé.
7. **X-23 bis** : S2 (le seuil monte avec la taille), S3 (témoin sans bord entre 7,3 et 8,1) et S4 (la coïncidence est un effet de taille finie) sont fausses toutes les trois. S5 : gel de l'étage 4 annoncé entre 9 et 11, mesuré à 8,2–8,4 ; écart entre étages annoncé de 2 à 3, mesuré de 1,7 à 1,8. S6 : le Blob gèle à l'étage 3 dès κ = 8.
8. **C2** : je penchais pour « la boule de tétraèdres ne tient pas l'étage 5 ». Faux : 77 % et 92 % dans le plus grand amas.
9. **X-23 D** : U4 (« forme à liens égaux rare pour les coques de rang 3 non justes ») fausse aux petites tailles : à 8 et 10 sommets, une forme est trouvée pour toutes les coques non justes sauf une au plus.
10. **X-23 E** : E2 (« le moteur complet reste sous le gel de l'étage 3, moins de 30 % ») fausse à chacun des 8 relevés (60 à 71 %). E3 (0,4 à 0,9 mécanisme par constituant) fausse dans 7 relevés sur 8 (0,27 à 0,40).
11. **X-23 F** : F2 (« le témoin à degrés conservés tient moins bien que le moteur ») fausse 6 fois sur 6. F3 (« terreau des mêmes points sous 30 % ») fausse 3 fois sur 6. F4 (« sans la force de bord, le gel tombe sous 50 % ») fausse : il monte.

**Fautes de méthode.**

12. **Lecture en virgule flottante non fiable.** Mon premier programme lisait le rang sur les valeurs propres de RᵀR avec un seuil relatif de 10⁻⁹. Or la plus petite valeur propre non nulle n'était qu'à un facteur 8 de la plus grande « nulle ». Premier essai sur le Blob : 367 mécanismes sur positions tirées, 365 sur positions réelles, amas incohérents. Tout a été refait en arithmétique entière exacte modulo 2³¹ − 1 (rang, vecteurs nuls, paires rigides), sans aucun seuil : 364 dans les deux cas. Les amas de la partie C, d'abord lus en flottant, ont été recalculés.
13. Le premier chargement du moteur a écrit un cache de compilation dans le dossier du corpus. Retiré ; les programmes écrivent désormais ce cache ailleurs.
14. Les compléments bis, ter, D, E et F ne figuraient pas au scellé d'origine. Chacun a reçu sa prédiction scellée avant calcul ; ils restent des décisions prises en voyant les résultats précédents, déclarées non aveugles.
15. X-23 D a été relancé après un premier départ : il s'arrêtait à la première forme trouvée, souvent un pliage où deux sommets non liés coïncident.
16. Le scellé d'origine est une empreinte dans le fil de la session, non un dépôt poussé avant calcul : je n'ai qu'un accès en lecture au dépôt.

## 208. Paroles de l'auteur prises comme point de départ

- 20 novembre, 07:03:37 UTC, à ChatGPT : « Tu dois définir chaque règle de ces évolutions et étages pour en comprendre la mécanique et la logique. Je crois que c'est la mécanique du réel. »
- 20 novembre, 06:49:31 UTC : « La 3D est plus facile que les autres mais plus difficile que la 1 ou 2D. » ; 06:33:16 UTC : « la 3D reste la moins énergivore ».
- 12 novembre, 19 h 29 UTC : « la 3D est le premier niveau qui permet toutes les structures avec un minimum d'énergie » (statut [H], « à tester »).
- 13 novembre, 08 h 29 UTC : « La solution la plus viable et la moins énergivore est toujours privilégiée ».
- Corpus, V346 p. 643 (XV.13, statut [I]) : « chaque palier doit se figer (se stabiliser) avant que le suivant ne croisse sur lui » ; p. 642 : « running d_s(κ₀) franchissant 3 vers κ₀≈6,6 […] l'analogue d'une cristallisation » ; p. 148 et 993 : le tétraèdre « naît creux et prend du poids en vieillissant ».
- 22 novembre, à Claude : « à toi de jouer, je débride toute la puissance disponible. Donne 100 % pour valider la TOE du Blob ».

Ces paroles sont enregistrées, non complétées. Les lectures ci-dessous sont les miennes.

## 209. Ma lecture, déclarée (hypothèses d'auditeur, non paroles de l'auteur)

- **L1. « Tenir l'étage d »** = être génériquement rigide en dimension d. C'est une propriété du réseau seul (Gluck 1975 ; Asimow et Roth 1978) : on ne pose aucune position, on balaie d.
- **L2. « Juste »** = tenir sans lien superflu : aucun mécanisme (ça tient), aucune auto-contrainte (aucun lien dont on pourrait se passer). C'est ainsi que je lis « viable et moins énergivore ». Réserve mesurée (section 216) : ce n'est pas l'énergie des ressorts de la règle U.
- **L3. « Coque fermée de rang k »** = sphère de cellules de dimension k, chaque face de dimension k−1 appartenant à exactement deux cellules. Rang 1 : polygone. Rang 2 : surface fermée de triangles, la plus petite étant la surface du tétraèdre. Rang 3 : sphère de tétraèdres. Son étage naturel est k+1.
- **L4. « Mitose de l'arête »** = celle de C-116 : le porteur naît sur un lien, chaque cellule qui porte ce lien se divise en deux.
- **L5. « Poids »** d'un corps rigide = nombre de ses auto-contraintes. Le corpus écrit déjà (V346 p. 1097) : « auto-contrainte ↔ signature mécanique de la matière ».

Vocabulaire : à l'étage d, un *mécanisme* est un mouvement qui respecte toutes les longueurs sans être un déplacement d'ensemble ; une *auto-contrainte* est un lien redondant. Pour V constituants et E liens : mécanismes − auto-contraintes = dV − d(d+1)/2 − E (Maxwell 1864, Calladine 1978 ; le corpus l'emploie p. 1096 avec d = 3 posé).

## 210. Partie A — ce qui se démontre

Prédiction scellée avant tout calcul de rigidité : `calculs/x23_regle_de_l_etage_prediction.txt`, SHA-256 `7c80008d46d64a9776a1a4c092cfb80c0e6bd1b83f9480f02ae7d266f00bb5a1` (22 novembre, 20:18:34 UTC). Programmes `x23_outils.py`, `x23_coques.py`. Ce sont des mathématiques classiques assemblées ; je n'en revendique aucune.

**A1 — Emboîtement [T].** Un réseau d'au moins d+1 constituants qui tient l'étage d tient l'étage d−1. *Preuve.* Soit p générique dans R^d et q sa projection dans R^(d−1). Un mouvement u de (G, q) se relève en (u, 0), mouvement de (G, p). Si G tient l'étage d, (u, 0) est un déplacement d'ensemble de R^d dont la dernière composante s'annule sur d+1 points en position générale : c'est un déplacement d'ensemble de R^(d−1). Les étages s'empilent donc dans l'ordre : c'est la forme exacte de « chaque palier doit se figer avant que le suivant ne croisse sur lui ».

**A2 — La mitose de l'arête garde la coque de triangles juste à l'étage 3 [T].** Sur une surface fermée de triangles, un lien (a, b) est porté par exactement deux triangles (a, b, x) et (a, b, y). La mitose retire (a, b) et relie le nouveau porteur à a, b, x, y : trois liens de plus, exactement le coût de l'étage 3. Ce geste est la *scission d'arête de Henneberg* de dimension 3, qui conserve « juste » (Tay et Whiteley 1985). Le tétraèdre creux est juste à l'étage 3 ; par récurrence toute coque née de lui par mitose de l'arête l'est aussi, **quel que soit le lien qui se divise**. À l'étage 2 la même coque a V−3 liens superflus ; à l'étage 4 elle a V−4 mécanismes.

**A3 — Rang 1 [T].** Un polygone gagne un lien par naissance. À l'étage 2 il a V−3 mécanismes : un de plus à chaque naissance. Seul le triangle tient.

**A4 — Rangs 3 et plus [T].** Une naissance sur un lien entouré de n_e sommets apporte 1 + n_e liens, avec n_e ≥ k. La coque tient l'étage k+1 (Kalai 1987) avec exactement E − (k+1)V + (k+1)(k+2)/2 auto-contraintes, soit la somme des (n_e − k) sur les naissances. Elle ne reste juste que si l'on choisit toujours un lien à l'entourage minimal ; sous choix uniforme le surplus croît sans borne.

**A5 — Naissance dans le volume [T, rangs ≥ 2].** Elle garde la coque juste à l'étage k+1 pour tout k ≥ 2 : elle ne désigne aucun étage. C'est le « aucun étage ne domine » de C-231. La sélection vient de la mitose de l'arête, non de l'empilement.

**A7 — Le budget [T en moyenne, M en simulation].** Sous mitose uniforme de l'arête, le nombre de liens par constituant tend vers k(k+1)/2 : 1 ; 3 ; 6 ; 10 ; 15. *Preuve (champ moyen ; l'argument général est du contre-audit, je l'ai revérifié).* Une naissance sur un lien d'entourage L change le nombre de faces de dimension j de ℓ_(j−1)(L) + ℓ_(j−2)(L) ; en sommant sur les liens, la croissance moyenne des faces de dimension j vaut [C(j+2,2) f_(j+1) + C(j+1,2) f_j] / f_1. En croissance linéaire, la relation au sommet (pas de face de dimension k+1) impose f_1/V = k(k+1)/2. Au rang 3, le nombre moyen de cellules autour d'un lien tend vers 5.

**Conséquence [T].** L'offre de liens de la mitose de l'arête, k(k+1)/2 par constituant, égale le coût de l'étage, k+1 par constituant, pour **k = 2 seulement** : c'est l'équation k(k+1)/2 = k+1. Et parmi tous les couples (rang, étage), (2, 3) est le seul où *toute* coque fermée sphérique est juste, quelle que soit sa taille : un polygone a E = V liens, jamais le compte d'un étage ; une surface fermée de triangles en a 3V − 6 (Euler), qui est le compte de l'étage 3 et de lui seul ; au-delà, seules les coques empilées sont justes.

**Contrôles numériques.** 873 états de coques (rangs 1 à 4, mitose uniforme, à entourage minimal, à entourage maximal), étages 1 à k+2, rang lu en flottant sur R et, tous les cinq pas, en arithmétique exacte : **0 violation**.

| Rang | Naissances | Étage k | Étage k+1 | Étage k+2 |
|---|---|---|---|---|
| 1 (polygone) | 40 | (0 ; 1) | (40 ; 0) | (80 ; 0) |
| 2 (triangles) | 60 | (0 ; 61) | **(0 ; 0) à chaque pas** | (60 ; 0) |
| 3, mitose uniforme | 45 | (0 ; 117 à 125) | (0 ; 71 à 79) | (0 à 4 ; 26 à 38) |
| 3, entourage minimal | 30 | (0 ; 31) | (0 ; 0) | (30 ; 0) |
| 4, mitose uniforme | 26 | (0 ; 86 à 106) | (0 ; 59 à 79) | (0 à 2 ; 33 à 53) |

(mécanismes ; auto-contraintes) à la fin. Enveloppes convexes aléatoires de rang 2, 12 à 200 sommets, et coque retournée 300 fois : (0 ; 0) à l'étage 3. Budget mesuré : 1,000 ; 3,000 ; 5,97 à 5,99 (20 000 constituants) ; 9,89 à 9,92 (12 000) ; 14,4 à 14,8 (3 000, encore croissant ; le contre-audit trouve 14,9 à 24 000).

## 211. Contre-audit indépendant de la partie A

Un agent Claude, sans mes programmes ni mon raisonnement, a reçu les énoncés avec la consigne de les réfuter, et a écrit son propre code. Verdicts : A1, A2, A3, A4 démontrés ; A5 fausse au rang 1 (corrigée ci-dessus) ; A6 trop forte (corrigée) ; A7 démontrée en moyenne pour tout k, par un argument plus général que le mien ; l'unicité vraie. Rangs exacts et flottants en accord dans tous ses cas.

**Faiblesses qu'il relève, toutes justes :**

1. La condition « la mitose conserve le juste » découle de « toute coque est juste » : elle n'ajoute rien à l'unicité.
2. La sélection de 3 est la formule d'Euler de la sphère face au nombre 6 des déplacements d'ensemble de l'espace à trois dimensions. Un tore aurait 6 liens superflus : le résultat tient à la sphère, pas à « surface fermée ».
3. Aux rangs ≥ 3, l'échec ne vient que du quantificateur « toute coque » : les coques empilées sont justes à tout rang.
4. Le rang k est lié à l'étage k+1 par choix. Tenir vaut à tout rang ≥ 2 ; seul « sans lien superflu » est propre au rang 2.
5. Tout est générique : la sphère flexible de Connelly (1977) existe, pour des positions particulières.

**Antériorité.** Que E = 3V − 6 égale le compte de Maxwell en dimension 3 est dans les manuels (Schulze et Whiteley, *Handbook of Discrete and Computational Geometry*, ch. 61 ; Maxwell l'avait vu en 1864). Ni lui ni moi n'avons trouvé de source qui en fasse un argument pour les trois dimensions. C'est une recherche négative, pas une preuve de nouveauté.

## 212. Ce que la partie A dit des paroles de l'auteur, et ce qu'elle ne dit pas

| Parole | Traduction sous L1–L4 | Statut |
|---|---|---|
| « La 3D est plus facile que les autres mais plus difficile que la 1 ou 2D » | Chaque étage coûte un lien de plus par constituant ; sous mitose de l'arête, le rang 1 ne tient pas, le rang 2 tient juste, les rangs suivants tiennent avec un surplus croissant | [T] sous mes lectures |
| « le premier niveau qui permet toutes les structures avec un minimum d'énergie » | Seul étage où toute coque fermée sphérique tient sans lien superflu, à toute taille | [T] sous mes lectures ; « énergie » lue comme nombre de liens, non comme énergie de ressort |
| « chaque palier doit se figer avant que le suivant ne croisse sur lui » | Emboîtement A1 ; seuils de gel ordonnés (section 214) | [T] et [M] |
| « naît creux et prend du poids » | La coque creuse est juste (poids nul) ; chaque lien au-delà ajoute une auto-contrainte | [T] pour le compte ; l'identification au « poids » reste ma lecture, et la « masse » du corpus ne la suit pas dans le Blob (B6 fausse) |

**Ce que cela ne dit pas.** Que l'espace a trois dimensions. Le théorème dit : *si* un lien tient une distance, *si* la fermeture est une sphère de cellules, et *si* l'on demande de tenir sans lien superflu sous la mitose de l'arête, alors le seul couple possible est (triangles, étage 3). Les trois « si » sont posés. C'est un second théorème conditionnel pour le nœud N1, à côté de C-135c, sous des conditions différentes : ni doublement synchrone, ni « la première fermeture bloque la mitose ».

**Limite mesurée (partie C, arithmétique exacte).** Le résultat vaut pour les coques *creuses*, pas pour un tissu de volumes. Une sphère de tétraèdres née par mitose uniforme (300 constituants, 5,7 à 5,8 liens par constituant) tient les étages 3, 4 et 5, pas le 6 ; ses liens superflus *diminuent* quand l'étage monte (853 ; 557 ; 262 pour une graine). Pour un tissu de volumes, l'étage 3 est donc le plus chargé en liens superflus, non le plus économe. Une boule de tétraèdres tient de même les étages 3 et 4, et le 5 à 77–92 %.

## 213. Partie B — l'ascenseur de rigidité dans `blob engine.py`

Moteur importé sans modification. Contrôle zéro-bis avant le scellé : point de travail redonné (5,2 et 6,2 triangles par constituant ; dispersion des degrés 0,83 et 0,95). N = 800, graines 0 et 1, κ = 4 à 10, étages 1 à 5 ; Blob (`build_blob`), terreau (`build_rgg`), témoin aléatoire (`build_er`, doublons retirés). 40 états, arithmétique exacte. « Gel » = plus grand amas rigide ≥ 50 % des constituants (ma convention).

**Contrôles.** Identité de Maxwell–Calladine : 0 écart sur 160 cas. Conséquences de A1 (plus grand amas et part figée décroissants avec l'étage) : 0 violation. Part figée jamais inférieure à la part par cliques de X-22 : 0 violation. Positions réelles du moteur et positions tirées au hasard : mêmes mécanismes, mêmes auto-contraintes, mêmes amas dans les 32 cas (B4 tenue). Cas connus (tétraèdre, octaèdre, K5, double banane, charnière) : exacts.

**Le témoin aléatoire retrouve la théorie.** Gel de l'étage 3 absent à κ = 5, présent à 6 ; étage 4 absent à 7, présent à 8 ; étage 5 absent à 9, présent à 10. Seuils connus : 3,588 ; 5,755 ; 7,843 (Peled 2026, arXiv:2605.25711), 9,896 par le même calcul. B1 tenue. L'étage d'un réseau sans structure suit son budget : environ κ/2.

**Plus grand amas rigide, en % des constituants (graines 0 et 1) :**

| κ | Terreau ét. 2 | Terreau ét. 3 | Terreau ét. 4 | Blob ét. 2 | Blob ét. 3 | Blob ét. 4 |
|---|---|---|---|---|---|---|
| 4 | 15 ; 10 | 3 ; 4 | 2 ; 2 | 5 ; 9 | 4 ; 4 | 4 ; 4 |
| 5 | 69 ; 59 | 7 ; 5 | 3 ; 3 | 35 ; 24 | 4 ; 9 | 4 ; 8 |
| 6 | 85 ; 92 | 10 ; 20 | 3 ; 6 | 86 ; 87 | 9 ; 10 | 4 ; 8 |
| **6,6** | 92 ; 95 | **66 ; 25** | 4 ; 9 | **91 ; 94** | **6 ; 11** | 5 ; 9 |
| 7 | 94 ; 96 | 75 ; 70 | 5 ; 9 | 97 ; 97 | 48 ; 30 | 6 ; 10 |
| 8 | 97 ; 99 | 84 ; 94 | 16 ; 23 | 97 ; 98 | 78 ; 68 | 6 ; 12 |
| 9 | 98 ; 99 | 94 ; 96 | 75 ; 71 | 100 ; 100 | 88 ; 89 | 59 ; 20 |
| 10 | 100 ; 99 | 97 ; 98 | 86 ; 89 | 100 ; 100 | 92 ; 93 | 80 ; 74 |

**Le Blob à son point de travail (κ₀ = 6,6).** Connexe ; **gelé à l'étage 2** (91 et 94 % dans un seul amas ; 94 % à N = 1600) ; **non gelé à l'étage 3** : 364 et 408 mécanismes, 610 et 654 auto-contraintes (B4 tenue), plus grand amas 5,5 et 11,4 % (8,4 % à N = 1600 ; 17 % en moyenne sur 8 graines), 20,6 et 24,5 % des constituants dans un corps rigide d'au moins quatre (B5 tenue ; par cliques : 17,2 et 21,6 %). Étage 4 : 5 et 9 %. Dans les mots du corpus : le palier 2 est figé, le palier 3 y pousse en grains.

**Le poids (L5).** 80 à 87 % des constituants du Blob ne portent aucune auto-contrainte à l'étage 3 ; les 10 % les plus chargés en portent 86 à 97 % (B7 tenue). Mais ce « poids » ne suit pas la « masse » du corpus (triangles incidents) : corrélation 0,38 à 0,47 (B6 fausse). Dans le terreau elle vaut 0,84 à 0,91. Mon dictionnaire « poids = auto-contrainte » n'est donc pas celui que le corpus mesure sous le nom de masse.

## 214. X-23 bis et ter — le terreau a une vraie transition de gel de l'étage 3 à κ = 6,45

Prédictions scellées : `x23bis_seuil_de_gel_prediction.txt` (SHA-256 `d72b06e7…a9ae`, 20:30:33 UTC) et `x23ter_seuil_fin_prediction.txt` (`e2708148…ebbc`, 20:34:41 UTC). J'avais écrit d'avance la raison de douter : le cube à bords libres est plus dense à l'intérieur (7,7 voisins au lieu de 6,6 à N = 800, calculé à la main), donc le seuil devait monter avec la taille. **Il ne monte pas.**

**Seuil à 50 % de l'étage 3, pas de 0,1 en κ, incertitude par rééchantillonnage des graines :**

| Taille | Terreau du moteur (bords libres) | Témoin sans bord |
|---|---|---|
| 800 (16 graines) | 6,45 ± 0,03 | 6,40 ± 0,03 |
| 1 600 (16 graines) | 6,43 ± 0,04 | 6,45 ± 0,02 |
| 3 200 (8 graines) | 6,48 ± 0,04 | 6,47 ± 0,02 |
| 4 800 (4 graines, pas de 0,2) | — | 6,45 |

Grille grossière de X-23 bis (pas de 0,4) : 6,48 ; 6,50 ; 6,48 ; 6,49 de N = 400 à 3 200 pour le terreau, 6,46 ; 6,45 ; 6,47 sans bord. La transition se raidit avec la taille (pente au seuil du témoin sans bord : 1,4 ; 1,5 ; 2,4). En dessous de 6,4 le plus grand amas fond quand N grandit (à 6,3 : 36 ; 30 ; 21 %) ; à partir de 6,5 il ne dépend plus de la taille (58 % environ). T1, T2, T4, T5, T6 tenues ; T3 tenue au sens où les courbes se rejoignent entre 6,4 et 6,5, sans croisement net.

**Recoupement indépendant.** Un second agent, sans mes fichiers, a reconstruit les graphes d'après leur seule définition et calculé à sa façon (élimination exacte, second nombre premier en contrôle) : **32 états sur 32 identiques** aux miens, mécanismes, auto-contraintes et plus grand amas, un par un (N = 800, graines 0 à 7, κ = 6,2 ; 6,6 ; 7,0 ; N = 1 600, graines 0 à 3, κ = 6,2 ; 6,6).

**L'échelle des étages du terreau** (N = 1 600 ; sans bord entre parenthèses) : étage 2 : 4,69 (4,65) ; étage 3 : 6,45 ; étage 4 : 8,21 (8,33) ; étage 5 : vers 10 (N = 800). Un étage tous les 1,7 à 1,8 voisins.

**Pour le Blob :** étage 2 : 5,28 et 5,27 ; étage 3 : 7,13 ± 0,06 et 7,20 ± 0,05 (N = 800 et 1 600). La viabilité déplace chaque seuil de 0,4 à 0,8 vers le haut : elle rassemble les liens dans les cœurs et dégèle le reste.

**Ce que cela établit [M, recoupé].** Le terreau du moteur a une transition de gel de l'étage 3 à κ = 6,45 ± 0,05, indépendante de la taille et des bords. La valeur canonique du corpus, κ₀ = 6,6 (« ≈ 6,6–7 », V346 p. 630), est 2 % au-dessus. Le corpus avait cherché un seuil à cet endroit et conclu qu'il n'y en avait pas (R-2, p. 631 : quatre hypothèses, « point quelconque d'un continuum lisse ») ; il avait relevé l'écart au seuil de champ moyen (« isostatique 6 ≠ 6,6 », p. 1250). Le seuil réel du terreau n'est pas 6 : il est 6,45.

**Ce que cela n'établit pas.** (a) Pourquoi l'auteur est arrivé à 6,6 : il y est arrivé par la dimension spectrale (p. 630–631), et je n'ai aucun lien démontré entre cette mesure et le gel. (b) Que 3 soit choisi : l'échelle a un barreau tous les 1,8 voisins, et κ₀ est posé sur le troisième. Ce résultat dit *quel* étage correspond à κ₀, par une mesure indépendante de la dimension spectrale ; il ne dit pas pourquoi celui-là. (c) Que le Blob lui-même soit gelé à l'étage 3 à κ₀ : il ne l'est pas. (d) Rien sur la nature. Je n'ai pas trouvé ce seuil dans la littérature consultée (recherche rapide).

## 215. X-23 E et F — le moteur complet de l'auteur, laissé libre de grandir, se tient à l'étage 3

Moteur `blob ablation labo colab.py` du corpus, chargé comme dans C-204c (lignes 1 à 228, empreinte vérifiée) : points dans l'espace, viabilité, liens ajoutés et retirés, mitose près du parent, désintégration des groupes de quatre. Son nombre de liens n'est pas posé. Prédictions scellées : `x23e_moteur_complet_prediction.txt` (`59fe97bd…1f68`), `x23f_temoins_et_ablations_prediction.txt` (`c1302244…1fdb`). **Non recoupé.**

| Graine | Constituants | Voisins | Étage 2 | Étage 3 | Étage 4 | Liens superflus à l'étage 4 |
|---|---|---|---|---|---|---|
| 1 | 300 (départ) | 6,60 | 93 % | 59 % | 12 % | 54 |
| 1 | 660 | 5,85 | 87 % | **61 %** | 0,9 % | **0** |
| 1 | 1 037 | 5,88 | 87 % | **66 %** | 0,9 % | 0 |
| 1 | 1 630 | 5,65 | 86 % | **62 %** | 0,4 % | 0 |
| 2 | 300 (départ) | 6,60 | 96 % | 88 % | 6 % | 14 |
| 2 | 660 | 5,84 | 94 % | **71 %** | 1,4 % | 0 |
| 2 | 1 037 | 5,69 | 88 % | **67 %** | 0,6 % | 0 |
| 2 | 1 630 | 5,62 | 88 % | **63 %** | 1,5 % | 2 |
| 3 ; 4 | 660 | 5,80 ; 5,78 | 85 ; 87 % | **60 ; 64 %** | 0,9 ; 1,1 % | 0 ; 0 |

Parti de 6,6 voisins, ce moteur **se défait de ses liens jusqu'à 5,6–5,9 voisins et reste gelé à l'étage 3** à chacun des huit relevés (60 à 71 %), avec 0,27 à 0,40 mécanisme et 0,18 à 0,30 lien superflu par constituant, et **rien à l'étage 4**. Ma prédiction E2 disait le contraire. Les liens superflus de l'étage 3 passent de 0,47–0,61 par constituant au départ à 0,20–0,27 à 660 constituants.

**Témoins (X-23 F), étage 3, plus grand amas :**

| État | Moteur | Réseau tiré au hasard, même budget | Mêmes degrés, liens rebattus | Terreau des mêmes points |
|---|---|---|---|---|
| graine 1, 660 (5,85) | 61 % | 89 ; 87 % | 81 ; 82 % | 27 % |
| graine 1, 1 037 (5,88) | 66 % | 91 ; 91 % | 80 ; 80 % | 31 % |
| graine 1, 1 630 (5,65) | 62 % | **0,2 ; 0,2 %** | 75 ; 76 % | 36 % |
| graine 2, 660 (5,84) | 71 % | 87 ; 89 % | 83 ; 83 % | 19 % |
| graine 2, 1 037 (5,69) | 67 % | **0,3 ; 0,3 %** | 79 ; 80 % | 30 % |
| graine 2, 1 630 (5,62) | 63 % | **0,2 ; 0,2 %** | 79 ; 76 % | 31 % |

Lecture, sans embellir. (1) Dans trois états sur six, le moteur tient l'étage 3 avec un budget (5,62 à 5,69 voisins) où un réseau tiré au hasard ne tient rien : il est sous le seuil 5,755. (2) Mais le même réseau, liens rebattus à degrés conservés, tient **mieux** que le moteur (75 à 83 %) : ce qui permet de tenir avec si peu est donc déjà dans le nombre de liens de chaque constituant, tel que le moteur le fabrique, et non dans son organisation dans l'espace, qui lui coûte au contraire 12 à 21 points. (3) Le terreau des mêmes points ne tient pas (19 à 36 %).

**Ablations (660 constituants, graines 1 et 2), étage 3, plus grand amas :** complet 61 ; 71 % — sans « bord » 79 ; 81 % (6,0 et 6,2 voisins) — sans « grav » 70 ; 76 % — sans « weak » 62 ; 64 % — sans « em » 61 ; 73 % — aucune force 78 ; 84 % (6,3 et 6,5 voisins). Étage 4 : 2 % au plus et 0 ou 1 lien superflu dans les douze exécutions. Le gel de l'étage 3 ne tient à aucune des quatre forces : il vient du socle (viabilité, mitose près du parent, désintégration des groupes de quatre). Les forces, celle de bord surtout, retirent des liens sans défaire le gel.

**Réserves.** Dans ce moteur, les points sont dans un espace à trois dimensions posé, le nouveau-né reçoit au plus six liens (partie entière de κ = 6,6, posé), et les taux de désintégration sont posés. Ce que je mesure : sous ces règles, le budget de liens s'ajuste de lui-même et le réseau reste à l'étage 3 sans rien porter à l'étage 4. Ce que je ne peux pas dire : que « 3 » en sorte sans avoir été mis.

## 216. X-23 D — sous la règle U, exploratoire

Prédiction scellée : `x23d_regle_U_prediction.txt` (`00a89aca…6160`). « Juste » parle de longueurs quelconques ; la règle U (12 novembre) donne à tous les liens la même longueur naturelle. Recherche numérique d'une forme où tous les liens valent 1 (chevauchements permis, réseau de barres) :

- coques de triangles, 5 à 20 sommets, 12 par taille : forme trouvée à l'étage 3 pour **108 coques sur 108** ; à l'étage 4 : 108 sur 108 ; à l'étage 2 : 6 sur 108 (des pliages). Sans sommets confondus, la recherche à 40 départs aboutit de moins en moins quand la taille grandit (12 sur 12 jusqu'à 7 sommets, 1 sur 12 à 20) : difficulté de recherche ou inexistence, non tranché.
- coques de rang 3 dans l'espace à quatre dimensions : empilées 32 sur 32 ; nées par mitose 8 ; 8 ; 7 ; 3 sur 8 à 6 ; 8 ; 10 ; 12 sommets, alors que 8 ; 5 ; 1 ; 0 d'entre elles seulement sont justes.

Conséquence : « lien superflu » n'est pas « énergie de ressort ». Avec des longueurs toutes égales, une coque qui a des liens superflus peut encore trouver une forme sans tension. Ma lecture L2 de « moins énergivore » compte des liens ; elle ne dit rien de l'énergie élastique de la règle U.

## 217. Ce que la journée donne, ce qu'elle ne donne pas

**Donne.**

1. Une règle de l'étage définie sans dimension posée, avec ses théorèmes (emboîtement, coût, mitose de l'arête, budget, unicité du couple triangles–étage 3), contre-auditée. Statut [T] sous cinq lectures qui sont les miennes.
2. Un fait mesuré et recoupé état par état : le terreau du moteur canonique gèle à l'étage 3 à κ = 6,45 ± 0,05, quelle que soit la taille, avec ou sans bord ; κ₀ = 6,6 est 2 % au-dessus. C'est la première fois que κ₀ est rattaché à un seuil.
3. La place des trois objets de l'auteur sur cette échelle, à κ₀ : le terreau au bord du gel de l'étage 3 ; le Blob de `blob engine.py` gelé à l'étage 2, l'étage 3 en grains ; le moteur complet avec mitose gelé à l'étage 3 et vide à l'étage 4, son budget étant passé de lui-même de 6,6 à 5,6–5,9 voisins (non recoupé).

**Ne donne pas.** Aucune loi physique. Ni l'espace, ni le temps, ni la gravitation, ni le quantique, ni les masses, ni la jauge, ni une prédiction confrontée à une mesure extérieure. « Pourquoi 3 » reçoit un second théorème conditionnel et une échelle mesurée, pas une dérivation : dans les moteurs, l'espace à trois dimensions des points et la valeur de κ restent posés.

**Verrous.** V1 (espace-temps) reste partiel, inchangé de statut ; s'y ajoutent ce théorème conditionnel et l'échelle de gel. V2 à V7 : rien. **TOE 0/7.**

## 218. À l'auteur, et suite proposée

Deux points lui reviennent, sans réponse soufflée :

1. Reconnaît-il « tenir » dans la rigidité (L1) et « moins énergivore » dans « sans lien superflu » (L2) ? Sans cela, la partie A reste un théorème de géométrie sans attache à sa cosmogonie.
2. Le tétraèdre « né creux » est-il la surface fermée de triangles, sans cellule intérieure (L3) ?

**Suite proposée, une seule :** faire recouper X-23 E par ChatGPT ou par un second moteur, puis chercher dans le moteur complet ce qui fixe son budget de 5,6 à 5,9 voisins — en particulier si ce budget survit quand on change la dimension de l'espace des points (2, 4, 5) : s'il suit la dimension, l'étage est hérité du plongement ; s'il reste celui de l'étage 3, quelque chose le choisit. Prédiction à sceller avant.

Non fait ce jour : C-224 à C-227 de ChatGPT toujours non contre-audités ; note « mécanique des étages » de ChatGPT non récupérée ; aucun message envoyé à ChatGPT ; rien de poussé au dépôt (accès en lecture seulement, en attente de la parole de l'auteur).

## 219. Fichiers

`calculs/` : `x23_regle_de_l_etage_prediction.txt`, `x23bis_seuil_de_gel_prediction.txt`, `x23ter_seuil_fin_prediction.txt`, `x23d_regle_U_prediction.txt`, `x23e_moteur_complet_prediction.txt`, `x23f_temoins_et_ablations_prediction.txt` ; `x23_outils.py`, `x23_coques.py`, `x23_moteur_etages.py`, `x23bis_seuil_de_gel.py` (modes bis et ter), `x23d_regle_U.py`, `x23e_moteur_complet.py`, `x23f_temoins_et_ablations.py` ; sorties `.out` et `.json` de même nom. Dépendances : numba et networkx, déjà au dossier. Écart déclaré : `x23bis_seuil_de_gel.py` a reçu son mode « ter » pendant que le mode bis tournait ; le plan bis n'a pas changé.

Sources extérieures : Y. Peled, « On the d-rigidity phase transition in random graphs », arXiv:2605.25711 ; B. Schulze et W. Whiteley, « Rigidity and scene analysis », *Handbook of Discrete and Computational Geometry*, ch. 61 ; H. Gluck (1975) ; L. Asimow et B. Roth (1978) ; T.-S. Tay et W. Whiteley (1985) ; G. Kalai (1987).

## 220. Versement (ajout de 21 h 15 UTC)

Parole de l'auteur, 21 h 10 UTC, en réponse à ma demande d'accord (20 h 52, redite à 21 h 04 : « Dis "pousse" et c'est fait, sur cette branche seulement ») : « Pousse au delà de tout, allons bien loin que tout ce que nous avons atteint à ce jour ! Ton fil conducteur la cosmogonie et le résultat est la validation de la toe. » Je la lis comme l'accord demandé pour ce versement, et comme la demande d'une nouvelle recherche, qui aura ses propres sections.

Versé sur la branche `versement/campagne-novembre-2026`, et sur elle seule. Ce que cela change aux phrases écrites plus haut : l'accès en écriture au dépôt a été obtenu à 20 h 53 UTC, après tous les calculs. Le point 16 de la section 207 reste donc vrai (le scellé d'origine n'a pas été poussé avant calcul), et le « rien de poussé au dépôt » de la section 218 décrit l'état d'avant ce versement. Entre 20 h 53 et 21 h 10, le contrôle automatique de fin de session demandait la poussée ; je l'ai préparée et retenue jusqu'à la parole de l'auteur.

Écart déclaré : avec ce versement part une correction du registre des empreintes de la branche, qui inscrivait trois fichiers d'un cache local absents du dépôt (commit séparé).

**TOE 0/7. Aucun verrou fermé.**
