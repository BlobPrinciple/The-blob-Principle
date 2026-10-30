🇫🇷 Français · 🇬🇧 [English version](DEFI-M13_REPORT_EN.md)

# DEFI-M13 — La barrière de l'aristocratie, mesurée : le profil d'énergie libre de T_v à degré moyen 4 et 6, et une question ouverte sur l'asymptotique

*Contribution du pilote IA du laboratoire (Claude, Anthropic), 30 octobre 2026. Déposée comme toute contribution, en issue `ia-assistee`. Vérifiée par le pilote (seconde implémentation indépendante par le code du moteur et par l'algorithme de biais, mesure dynamique séparée) et relue par un second agent IA en relecteur hostile (voir § 6) ; **aucune relecture humaine à ce stade**.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Ce rapport ne change aucun statut épistémique. Il répond partiellement à DEFI-M13 (RO-25, RO-20), sur graphes abstraits seulement ; aucune borne n'est démontrée et le moteur canonique n'est pas traité.

## 1. La question

DEFI-M13 (#42), ouvert par [DEFI-M12_RAPPORT.md](DEFI-M12_RAPPORT.md), § 7 : sur graphes abstraits à degré moyen 4, sous π ∝ exp(n·S_sim/τ), le demi-temps t½ d'autocorrélation de T_v (triangles contenant le sommet v) croît comme exp(0,96·√n) de n = 17 à 193, et l'aristocratie est une clique dominante de taille de l'ordre de √n ; à degré moyen 6, la croissance est plus rapide (exp(a·n^0,6) environ). **Pourquoi √n, et pourquoi pas à degré moyen 6 ?** Livrable : preuve ou réfutation d'une barrière en exp(Θ(√n)) (goulot d'étranglement, conductance, argument d'énergie libre), ou explication mesurée.

Sources qui font foi : armature V347.1, § II.0 (p. 10 : strates A_gen et A_Gibbs, S_sim(C) = log(1 + n_tri(C)) − β·D(C) ; les deux ponts absents, RO-25 et RO-08) ; encadré RO-25 (p. 11 : une dynamique jointe dont la loi conditionnelle à N fixé reproduise ou dérive π_N) ; axiomes A3–A4 [A][ARCH] (p. 18 : β = 0,30 ; π_N ∝ exp(N·S_sim/τ), τ = 0,50) ; A0′ (p. 18 : « sous ergodicité, ces poids gouvernent les fréquences empiriques de résidence à long terme » ; « persister » n'est pas défini par π_N > 0, RO-20). Cadre de calcul inchangé depuis DEFI-M8 (hypothèse H-abs, [DEFI-M8_RAPPORT.md](DEFI-M8_RAPPORT.md), § 2) : graphes simples étiquetés abstraits, D = écart-type de population des degrés / degré moyen, échanges de Metropolis à nombre d'arêtes M fixé, λ = n/τ = 2n ; un balayage vaut M échanges.

## 2. Méthode

**Idée.** DEFI-M12 a mesuré une lenteur ; la question « pourquoi » demande la loi d'équilibre dans les régions que la dynamique visite rarement. Les sommets étant échangeables, la loi P(T) de T_v est la même pour tout v ; F(T) = −log P(T) est le profil d'énergie libre le long de l'observable même dont DEFI-M12 a mesuré l'autocorrélation. Si la lenteur est la traversée activée d'un col de F, log t½ doit suivre la hauteur de ce col.

**Profil (`defi_m13_profil.py`).** Noyau de `defi_m12_lenteur.balayer` (même proposition, même S_sim), auquel s'ajoute un biais exp(w(T_0)) sur le nombre de triangles du sommet marqué 0 ; T_0 est tenu à jour à chaque échange. Support : [0, T_cap], T_cap = 1,15 × le T_v maximal observé dans une chaîne non biaisée issue d'un noyau planté, + 2. Wang–Landau (f de 1 à 10⁻⁵, platitude min H > 0,7 × moyenne sur tout le support), puis production à biais fixé (8 blocs de 5 000 balayages) et repondération, P ∝ H·exp(−w). Trois répétitions par point (deux à n = 257), graines distinctes. Contrôles exacts en fin de chaîne : n_tri = tr(A³)/6 et T_0 recalculés.

**Quatre estimateurs de la barrière de sortie B** (minimum roturier en T ≈ 0, minimum aristocratique dans la moitié haute du support, col = maximum de F entre les deux) : **brut** sur les valeurs entières de T ; **k** après regroupement de T en classes [C(k,2), C(k+1,2)) (F est très dentelé : les valeurs T = C(k,2), celles d'un voisinage complet, sont favorisées) ; **lissé** (moyenne glissante de 5 cases) ; **mfpt**, log du temps moyen de premier passage d'une diffusion unité le long de T, du minimum aristocratique au minimum roturier. Aucun n'est un temps : seule leur variation se compare à celle de log t½. Le choix de l'estimateur pèse (§ 3.3) ; c'est une limite de la méthode, pas un détail.

**Seconde implémentation (`defi_m13_second_moteur.py`), indépendante par le code du moteur et par l'algorithme de biais** (elle reprend le support et le masque du premier moteur, et l'analyse commune ; une seule course par taille). Voisinages en mots de 64 bits et popcount, T_0 recalculé en entier après chaque proposition (sans mise à jour incrémentale), générateur PCG64 en lots, départ « clique de taille 0,6·√(2M) contenant le sommet 0 », algorithme 1/t de Belardinelli et Pereyra (2007) au lieu de Wang–Landau ; même support que le premier moteur (lu dans son JSON, cases jamais atteintes exclues du critère). Une première version (récurrence multicanonique de Berg) ne convergeait pas à n ≥ 129 (cases intérieures vides) : abandonnée, non retenue.

**Mesure dynamique séparée (`defi_m13_sorties.py`).** Chaînes non biaisées (moteur de DEFI-M12), deux par taille, de 16 t½ (n = 193) à 400 t½ (n = 25) ; un sommet est « aristocrate » au-dessus de la moitié du T du minimum aristocratique, « roturier » sous T = 2, avec hystérésis entre les deux ; temps de séjour = temps total passé aristocrate / nombre de sorties. C'est une grandeur dynamique, qui dépend du noyau d'échange ; elle est distincte des fréquences de résidence stationnaires dont parle A0′.

**Écarts de méthode, déclarés.** Une première passe du profil (f final 2·10⁻⁴, platitude 0,5, production 8 × 2 000 balayages) donnait à n ≥ 129 des barrières non reproductibles d'une répétition à l'autre (jusqu'à 2 d'écart) ; elle a été remplacée par la passe décrite ci-dessus et n'est pas conservée. Deux défauts de Wang–Landau ont été corrigés en cours de mise au point (case nouvellement atteinte : biais hérité de la case courante ; platitude exigée sur tout le support et non sur les seules cases visitées). À n = 17, le critère de platitude n'est jamais atteint (cases inaccessibles, par exemple T_v = 27 avec 34 arêtes) : les 17 étapes vont au plafond, sans effet visible sur le profil (contrôle direct, § 3.1). Le support tronqué peut être dépassé par une chaîne libre (T observé 46 contre T_cap = 45 à n = 33, selon le relecteur) : masse négligeable, mais le support ne couvre pas tout. Le point n = 385 a échoué (une répétition sur deux bloquée en production dans la région aristocratique) : il est exclu de l'analyse et conservé dans `defi_m13_profil_c2_grand.json`.

## 3. Résultats

### 3.1 La loi d'équilibre de T_v est bimodale, avec un col qui monte [M]

À degré moyen 4, pour n ≥ 25, P(T_v) a deux modes : les roturiers en T = 0 et l'aristocratie autour de T ≈ C(k_ari, 2), séparés par un plateau dentelé. La classe k_ari du minimum aristocratique (5, 6, 7, 8, 9, 11, 12, 14,7 pour n = 17 à 193) suit la plus grande clique mesurée par DEFI-M12 (5,5 à 14,8) : le mode aristocratique correspond, approximativement, à l'appartenance à la clique dominante (un membre d'une clique de taille q a T ≈ C(q − 1, 2), donc k ≈ q − 1, alors que k_ari ≈ q : l'accord n'est qu'approché).

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 | 257 |
|---|---|---|---|---|---|---|---|---|---|
| ln t½ (DEFI-M12) | 2,22 | 3,07 | 3,77 | 4,99 | 5,96 | 7,74 | 9,19 | 11,63 | — |
| B brut | 0,55 | 0,70 | 0,86 | 1,73 | 2,65 | 5,07 | 7,37 | 11,01 | 16,37 |
| B k | 0,66 | 0,81 | 1,04 | 1,72 | 2,40 | 4,14 | 5,19 | 7,21 | 10,26 |
| B lissé | 0,24 | 0,43 | 0,62 | 1,38 | 2,17 | 4,24 | 6,13 | 9,18 | 13,72 |
| mfpt | 4,94 | 5,62 | 6,14 | 7,23 | 8,17 | 10,21 | 12,03 | 15,41 | 19,91 |
| B brut, second moteur | 0,57 | 0,59 | 0,79 | 1,89 | 2,69 | 5,14 | 7,50 | 11,68 | 16,14 |

Écart-type entre répétitions : ≤ 0,11 jusqu'à n = 65, 0,07 à 0,48 au-delà (`defi_m13_analyse_sortie.txt`, tableau A).

**Recoupement.** Profils F des deux implémentations, après recentrage, sur les cases à moins de 16 du minimum : écart quadratique moyen 0,06 à 0,16 jusqu'à n = 65, 0,15 à 0,44 de n = 97 à 193 (écart maximal 1,36) ; à n = 257, 1,16 à 1,43 (écart maximal 7,6) alors que les quatre barrières concordent à 0,4 près (premier moteur 16,37 ; 10,26 ; 13,72 ; 19,91 — second 16,14 ; 9,97 ; 13,72 ; 19,50). Aux petites tailles (n ≤ 65), l'histogramme direct d'une chaîne non biaisée reproduit le profil (écart quadratique 0,08 à 0,19 sur les cases à moins de 8 du minimum ; `defi_m13_analyse_sortie.txt`, B bis). **Troisième recoupement, par le relecteur**, avec son propre code (départ aléatoire, PCG64, longue chaîne non biaisée, histogramme direct sur tous les sommets, 1,5 à 4·10⁶ balayages) : B brut 0,83 ; 1,73 ; 2,66 ; 5,04 à n = 33, 49, 65, 97, contre 0,86 ; 1,73 ; 2,65 ; 5,07 ici.

### 3.2 Le t½ de DEFI-M12 suit le temps de séjour dans l'aristocratie [M]

| n | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|
| sorties comptées (deux chaînes) | 3 890 | 4 685 | 4 380 | 4 660 | 2 445 | 1 031 | 324 |
| séjour moyen (balayages) | 40 | 72 | 216 | 582 | 3 698 | 16 301 | 181 848 |
| séjour / t½ | 1,86 | 1,65 | 1,48 | 1,50 | 1,61 | 1,67 | 1,63 |

Le rapport reste entre 1,5 et 1,9 quand le séjour croît d'un facteur 4 500 (pour une sortie de loi exponentielle, on attendrait de l'ordre de 1/ln 2 ≈ 1,44 si t½ suivait la survie de l'appartenance). La lenteur mesurée par DEFI-M12 suit donc, à un facteur à peu près constant près, la persistance de l'appartenance à l'aristocratie. Pas de barres d'erreur ; à n = 193, chaque chaîne ne couvre qu'une dizaine de durées de vie de la clique et les 324 sorties sont corrélées.

### 3.3 Le col et la lenteur : même ordre de grandeur, relation non linéaire [M] ; forme de B [H]

- **Forme de B [H] : elle dépend de la plage.** Sur n = 33 à 257, les quatre estimateurs s'ajustent mieux par une droite en n que par une droite en √n (sommes des carrés des résidus : brut 0,60 contre 5,14 ; mfpt 0,26 contre 3,01 ; exposant libre 0,90 à 1,10). Mais ce verdict repose sur le point n = 257 (le plus fragile, § 5) et sur l'apparition du col aux petits n : **sur n = 65 à 193, B est compatible avec √n** (brut 0,01 contre 0,21 ; k 0,04 contre 0,21 ; lissé 0,00 contre 0,16 ; mfpt 0,04 contre 0,05 ; exposant libre 0,56 ; 0,30 ; 0,54 ; 0,73), et la pente ΔB/Δ√n y est à peu près constante (brut 1,36 ; 1,52 ; 1,44), avant de sauter à 2,51 au seul intervalle 193–257.
- **B contre ln t½.** Ajustement ln t½ = a·B + b sur n = 33 à 193 : a = 0,745 (brut), 1,237 (k), 0,885 (lissé), 0,840 (mfpt), plus grands résidus 0,26 à 0,52 ; la relation est concave (pentes locales du brut 1,39 → 0,67 ; du mfpt 1,13 → 0,72). Une traversée activée d'un col unique le long de T_v, à préfacteur constant, donnerait a = 1 ; rien ne garantit que le préfacteur soit constant, et le mfpt contient un terme entropique qui croît avec le support (4,94 à n = 17 pour B brut 0,55) : c'est un ordre de grandeur. **T_v n'est qu'une coordonnée de réaction approchée** : le profil donne l'ordre de grandeur et la tendance, pas une loi d'Arrhenius quantitative.
- **À n fixé (n = 65), quand λ croît.** λ = 66, 98, 130, 162, 194 : B brut −0,07 ; 1,29 ; 2,65 ; 4,31 ; 6,19. À λ = 66, il n'y a plus de col (B ≈ 0) : c'est le régime où DEFI-M12 a vu l'aristocratie se dissoudre (réglage c2T). Pentes sur λ ≥ 98 : dB/dλ = 0,051 (brut), 0,033 (k), 0,041 (lissé), 0,040 (mfpt), contre d ln t½/dλ = 0,031. Même constat : seul le regroupement en k suit la pente dynamique.

### 3.4 L'asymptotique reste ouverte : la prédiction à n = 257 dépend du modèle de calibration [H]

Les barrières sont mesurables là où la dynamique ne l'est plus. À n = 257, appliquées aux barrières mesurées (premier moteur), les relations ln t½ ↔ B calibrées sur n = 33 à 193 donnent :

| calibration | brut | k | lissé | mfpt |
|---|---|---|---|---|
| linéaire | 15,84 | 15,43 | 15,85 | 15,65 |
| pente du dernier intervalle | 15,21 | 15,32 | 15,26 | 14,87 |
| quadratique | 13,58 | 14,94 | 13,72 | 13,88 |

La loi de DEFI-M12 extrapolée donne 13,68 (t½ ≈ 8,7·10⁵ balayages) ; la calibration linéaire, 15,1 à 15,9 (3,5 à 7,7·10⁶). La relation étant concave, l'extrapolation linéaire surestime par construction ; la calibration quadratique est compatible avec la loi en √n pour trois estimateurs sur quatre. Ces prédictions ne sont pas indépendantes (mêmes données, mêmes ajustements). **Conclusion : les profils ne permettent pas de trancher si exp(0,96·√n) se prolonge au-delà de n = 193.** Seule une mesure dynamique à n = 257 (≈ 10⁷ balayages de 514 échanges, hors de portée de cette session) le dira.

### 3.5 Degré moyen 6 : le col apparaît plus tard [M], d'où un exposant effectif plus grand [H]

| n | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|
| ln t½ (DEFI-M12, c3) | 1,52 | 2,11 | 3,06 | 3,96 | 5,51 | 6,88 | 9,25 |
| B brut | −0,08 | −0,07 | 0,03 | 0,33 | 1,73 | 3,21 | 6,32 |
| B k | 0,01 | −0,15 | 0,20 | 0,63 | 2,06 | 3,20 | 5,40 |

À degré moyen 6, il n'y a pas de col jusqu'à n = 49 (les valeurs légèrement négatives signalent l'absence de minimum aristocratique distinct), alors que ln t½ y croît déjà de 1,5 : la lenteur aux petites tailles n'y est pas activée. Le col apparaît vers n = 65 puis croît vite (ΔB brut = 3,1 de 129 à 193, contre Δ ln t½ = 2,4). **[H]** L'exposant effectif γ ≈ 0,6 de DEFI-M12 (§ 3.2 de ce rapport-là) reflèterait ce croisement tardif entre un régime non activé et un régime activé, plutôt qu'une loi propre à cette densité.

## 4. Lecture pour le pont RO-25 et pour RO-20

- **[M]** La lenteur aristocratique de DEFI-M12 est une persistance d'appartenance (§ 3.2) adossée à une barrière d'équilibre réelle dans la loi de T_v (§ 3.1), absente quand λ est trop faible.
- **[H]** Sur n = 65 à 193, la barrière est compatible avec une croissance en √n ; le point n = 257 suggère une accélération, sans l'établir (§ 3.3–3.4). Si une croissance plus rapide que √n se confirmait, un pont croissance → Gibbs qui laisserait chaque nouveau-né rejoindre sa masse triangulaire d'équilibre avant la naissance suivante serait encore moins praticable que ne le disait DEFI-M12 (§ 4 de ce rapport-là) : l'intervalle entre naissances croîtrait plus vite que exp(0,96·√n). Même réserve qu'alors : RO-25 n'est pas réfuté ; le falsificateur de l'armature (p. 11) porte sur l'existence d'une extension markovienne, pas sur sa vitesse, et un autre noyau de relaxation peut mélanger plus vite.
- **[H] Vers RO-20.** A0′ (p. 18) relie les poids de π_N aux fréquences de résidence stationnaires, qui ne disent rien des durées ; le temps de séjour dans la clique dominante (§ 3.2) est, lui, une grandeur dynamique, propre au noyau. « Persister », au sens d'un séjour plus long que l'intervalle entre deux naissances, serait un critère distinct de π > 0 et chiffrable pour un noyau donné ; il reste à le formuler.
- **[OPEN]** Aucune borne démontrée ; T_v n'est pas la coordonnée de réaction exacte ; la question « pourquoi √n » de DEFI-M13 reste ouverte : sur 65–193, la barrière d'équilibre le long de T_v croît elle aussi comme √n, ce qui reporte la question de la dynamique sur la statique, sans l'expliquer.

## 5. Ce qui est établi, ce qui reste à vérifier, le point le plus fragile

- **Établi** (deux implémentations, répétitions, et un troisième moteur du relecteur jusqu'à n = 97) : la bimodalité de P(T_v) et la hauteur du col, n = 17 à 193 ; le rapport séjour/t½ constant (§ 3.2) ; l'absence de col à λ = 66 (n = 65) et à degré moyen 6 jusqu'à n = 49.
- **Dépend de l'estimateur ou de la plage** : la pente ln t½ contre B (0,75 à 1,24) et toute lecture quantitative de type Arrhenius ; la forme de B (√n sur 65–193, plus rapide si l'on inclut 257) ; la prédiction à n = 257.
- **À vérifier** : tout, par une personne ; la prédiction à n = 257 par une mesure dynamique ; une meilleure coordonnée de réaction (par exemple le nombre de voisins dans la clique dominante, ou un échantillonnage de chemins) ; le moteur canonique (DEFI-M10).
- **Point le plus fragile** : n = 257. La production à biais fixé n'y est pas plate (rapport min/moyenne 0,03 et 0,00 ; une répétition n'a pas visité T = 0 en production), les profils des deux moteurs y diffèrent localement de 7,6, et le point n = 385 a échoué. Les barrières concordent pourtant entre les deux moteurs (écarts ≤ 0,4) ; c'est pourquoi le § 3.4 reste une question ouverte. De n = 97 à 193, la production est aussi imparfaitement plate (rapport min/moyenne 0,04 à 0,57) ; les répétitions et le second moteur y concordent à ± 0,7 sur B.

## 6. Relecture hostile

Un second agent IA, qui n'a pas produit ce travail, a rejoué l'analyse (sortie identique octet pour octet), vérifié chaque nombre contre les JSON, contrôlé les deux moteurs (signe du biais, mise à jour de T_0, repondération, formule de Σd² : aucun bogue trouvé), vérifié les citations de l'armature (p. 10, 11, 18 : exactes) et refait les barrières à n = 33, 49, 65, 97 avec son propre code (§ 3.1). **Bloquants retenus et corrigés** : (1) la conclusion « la loi en exp(√n) ne devrait pas durer » et le titre ne tenaient pas ; la relation ln t½ ↔ B est concave, l'extrapolation linéaire surestime, une calibration quadratique est compatible avec √n : § 3.4 réécrit en question ouverte [H], tableau de sensibilité ajouté, titre changé ; (2) « le col monte plus vite que √n » reposait sur n = 257 : ajustements sur 65–193 ajoutés (compatibles avec √n), phrase passée en [H] ; (3) n = 257 retiré de « Établi » ; (4) lecture fautive d'A0′ (fréquences stationnaires contre temps de séjour dynamique) : phrases retirées ou reformulées. **Mineurs retenus** : écarts-types, fourchette 3,5·10⁶, platitude jamais atteinte à n = 17, support tronqué, contrôle direct ajouté à l'analyse, portée de l'indépendance du second moteur (une course par taille), réserves sur le mfpt, rapport attendu 1/ln 2 et corrélation des sorties, accord approché k_ari ≈ q, lien anglais.

## 7. Prochain pas sur le chemin de preuve (P1)

**DEFI-M14 — La loi en √n survit-elle à n = 257 ?** Mesurer le temps de séjour dans l'aristocratie (ou t½) à n = 257, et si possible au-delà, sur graphes abstraits à degré moyen 4 sous la mesure de l'armature, et trancher entre la loi exp(0,96·√n) de DEFI-M12 (ln t½ ≈ 13,7) et une croissance plus rapide (ln t½ ≈ 15 à 16 selon la calibration linéaire de ce rapport) ; ou démontrer une borne de la barrière d'appartenance à la clique dominante ; ou trouver une coordonnée de réaction meilleure que T_v.

## Reproduire

```bash
cd contributions/RO-25_pilote-ia
pip install numba                                    # 0.68.0
python3 defi_m13_profil.py --points c2:17,c2:25,c2:33,c2:49,c2:65,c2:97,c2:129,c2:193 --sortie defi_m13_profil_c2.json   # ≈ 4 min sur 2 cœurs
python3 defi_m13_profil.py --points c2:257,c2:385 --repetitions 2 --sortie defi_m13_profil_c2_grand.json                # ≈ 30 min
python3 defi_m13_profil.py --points c2:65:66,c2:65:98,c2:65:162,c2:65:194 --processus 1 --sortie defi_m13_profil_lambda.json
python3 defi_m13_profil.py --points c3:25,c3:33,c3:49,c3:65,c3:97,c3:129,c3:193 --repetitions 2 --processus 1 --sortie defi_m13_profil_c3.json
python3 defi_m13_second_moteur.py --points c2:17,c2:25,c2:33,c2:49,c2:65,c2:97,c2:129,c2:193 --sortie defi_m13_second_moteur.json
python3 defi_m13_second_moteur.py --points c2:257 --source defi_m13_profil_c2_grand.json --sortie defi_m13_second_moteur_257.json
python3 defi_m13_sorties.py --processus 1            # ≈ 10 min
python3 defi_m13_analyse.py                          # écrit defi_m13_analyse.json
```

Python 3.13, numpy 2.5.3, scipy 1.18.1, numba 0.68.0. Graines fixées ; un même script rejoué sur une autre machine peut différer au niveau du bruit statistique. Sorties écran : `defi_m13_*_sortie.txt`.
