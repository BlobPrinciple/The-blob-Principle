🇫🇷 Français · 🇬🇧 [English version](DEFI-M11_REPORT_EN.md)

# DEFI-M11 — Naître juste ou relaxer vite : ce que la loi d'attachement change, et la lenteur qu'elle ne change pas

*Contribution du pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026. Déposée comme toute contribution, en issue `ia-assistee`. Vérifiée par le pilote (énumération exacte et Monte-Carlo, chacun recoupé par une seconde implémentation indépendante) et relue par un second agent IA en relecteur hostile (trois corrections de fond retenues, voir § 5) ; **aucune relecture humaine à ce stade**.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Ce rapport ne change aucun statut épistémique. Il répond partiellement à DEFI-M11 (RO-25, RO-24), sur graphes abstraits.

## 1. La question

DEFI-M11 (#36), ouvert par [DEFI-M8_RAPPORT.md](DEFI-M8_RAPPORT.md) : l'attachement de Gibbs G\*, dérivé de S_sim, minimise exactement l'écart à π à la naissance, mais, sur huit cas exacts, il ralentit la relaxation qui suit ; l'attachement anti-Gibbs relaxe le plus vite dans cinq cas sur six. **Ce constat est-il général, et survit-il quand N grandit ?**

Cadre, notations et sources : ceux de DEFI-M8_RAPPORT.md (armature V347.1, § II.0 p. 10, RO-25 p. 11, A3–A4 p. 18 ; hypothèse H-abs : graphes abstraits étiquetés, β = 0,30, τ = 0,50). Famille de noyaux : G_θ(A | C) ∝ π_{N+1,M+k}(C + v_A)^θ, θ = −1, −0,5, 0 (uniforme U), 0,5, 1 (G\*). Un **balayage** vaut M + k échanges de Metropolis.

## 2. Résultat A — la carte exacte à au plus 7 sommets [CERT]

Tous les secteurs de départ (N, M) avec N = 4, 5, 6, M ≥ 1, et tous les k avec 2 ≤ k ≤ N − 1 dont le secteur d'arrivée a au moins deux états : **102 cas**, jusqu'à 352 716 états. Pour chaque cas et chaque θ, propagation exacte de la loi jusqu'à TV ≤ 0,01 (`defi_m11_carte_exacte.py`, ≈ 36 min).

| Ensemble | cas | G\* plus lent que U | G\* plus rapide | θ = −1 plus rapide que U | rapport t(G\*)/t(U), médiane (min–max) | rapport t(θ = −1)/t(U), médiane (min–max) |
|---|---|---|---|---|---|---|
| G\* gagne à la naissance | 57 | **50** | 7 | **44** | 1,28 (0,36–2,28) | 0,84 (0,19–1,73) |
| dont degré moyen d'arrivée ≥ 2 | 45 | 38 | 7 | 32 | — | — |
| dont degré moyen d'arrivée < 2 | 12 | 12 | 0 | 12 | — | — |
| G\* ne gagne pas à la naissance | 45 | 11 | 9 | 10 | — | — |

Par taille, parmi les cas où G\* gagne à la naissance : N = 4 : 6 sur 6 plus lents ; N = 5 : 14 sur 17 ; N = 6 : 30 sur 34. Les sept exceptions sont (N, M, k) = (5, 5, 2), (5, 6, 2), (5, 7, 3), (6, 6, 2), (6, 7, 2), (6, 10, 3), (6, 11, 4) ; dans cinq d'entre elles, t décroît avec θ (Gibbs le plus rapide). Dix des 57 gains à la naissance sont inférieurs à 10⁻³, et cinq des sept exceptions sont parmi eux : **pour un gain d'au moins 10⁻³, G\* est plus lent dans 45 cas sur 47**. Le groupe « G\* ne gagne pas » est fait, à 43 cas sur 45, d'égalités exactes de TV à la naissance (corollaire D1 de DEFI-M8).

**Lecture [CERT].** Sur ces petits graphes, « bien naître ralentit le pont » n'est pas un accident des huit cas de DEFI-M8 : il vaut dans 50 cas sur 57 où G\* fait mieux que l'uniforme à la naissance (88 %). Ce n'est pas une loi : sept exceptions, dont des secteurs denses.

**Recoupement.** Seconde implémentation sans code commun (`defi_m11_carte_second_moteur.py`, networkx et matrices denses) sur les 42 cas à au plus 6 sommets : mêmes nombres d'échanges dans les 210 comparaisons, TV à la naissance identiques à 3,3·10⁻¹⁶.

## 3. Résultat B — au-delà de l'énumération [M]

L'écart en variation totale sur toute la configuration n'est plus calculable au-delà de 7 sommets. On suit donc trois **observables** après la naissance : T_v (triangles contenant le nouveau-né), T (triangles du graphe) et D (dispersion des degrés), comparées à leur loi d'équilibre sous π_{N+1,M+k}. Secteur à densité fixe : M = 2N − 2, k = 4, donc M + k = 2(N + 1) et degré moyen 4 avant et après la naissance ; le nouveau-né naît avec le degré moyen. N = 8, 12, 16, 24, 32, 48 (campagne principale : 2 000 naissances par θ, parents tirés de π_{N,M} par une chaîne de Metropolis, un parent tous les 20 balayages), puis N = 48 et 64 pour θ = 0 et 1 (campagne longue : 600 naissances, jusqu'à 2 000 balayages ; même graine de départ que la principale à N = 48, donc partiellement dépendante). Moteur `numba` (`defi_m11_monte_carlo.py`).

**B1. Les observables globales oublient vite la loi d'attachement, mais pas complètement le mode lent.** À la naissance, G\* est plus proche de l'équilibre (écart réduit de T : de +0,09 à −0,29 selon N, contre −0,24 à −1,20 pour les autres θ). Dans la campagne principale (N = 8 à 48), après 4 balayages, les écarts réduits de T et D sont compris entre −0,18 et +0,02 pour tous les θ ; après 16 balayages, entre −0,07 et +0,06. Pour ces observables, aucun ordre « anti-Gibbs < uniforme < Gibbs » n'apparaît : quand une différence se voit, c'est G\* qui est le plus proche. Dans la campagne longue, T garde un écart de −0,11 à −0,15 après 16 balayages à N = 64 : les observables globales héritent elles aussi, à faible amplitude, du mode lent décrit en B2.

**B2. Les triangles du nouveau-né rejoignent l'équilibre de plus en plus lentement.** Le critère prévu dans le script (écart ≤ 0,1 écart-type, champ `critere` du JSON) n'est pas atteint en 300 balayages à N = 48 ; on lui a substitué **après coup** un demi-temps t½ : premier temps où l'écart de la moyenne de T_v à l'équilibre tombe sous la moitié de l'écart à la naissance (`defi_m11_demi_temps.py`). t½ ne mesure que la décroissance d'une moyenne : c'est un minorant de l'ordre du temps de mélange, pas le temps de mélange.

| N | 8 | 12 | 16 | 24 | 32 | 48 | 64 |
|---|---|---|---|---|---|---|---|
| t½ (balayages), θ = 0 | 0,5 | 2,7 | 7,5 | 22,9 | 46,8 | 138,6 (147,3) | 442,0 |
| t½, étendue sur les cinq θ | 0,3–0,6 | 1,3–3,2 | 4,7–7,5 | 22,8–23,8 | 39,2–58,2 | 138,6–158,7 | 442,0–448,4 (θ = 0 et 1) |

Entre parenthèses : campagne longue (600 naissances). De N = 12 à 64, t½ est multiplié par environ 160 quand N l'est par 5,3. Un ajustement en loi de puissance (N ≥ 12, tous θ) donne un exposant 3,0 (2,75 à 3,47 selon θ) ; les pentes locales à θ = 0 valent 3,6, 2,8, 2,5, 2,7 et 4,0, et sur N ≥ 24 une croissance exponentielle en N ajuste mieux qu'une loi de puissance. **La croissance est au moins de l'ordre de N³ balayages sur 8 ≤ N ≤ 64 ; une croissance plus rapide, éventuellement exponentielle, n'est pas exclue.** L'exposant varie peu avec le seuil (2,8 à 3,3 pour 3/4, 1/2 ou 1/4 de l'écart initial, selon le relecteur).

Dans la famille G_θ, θ ∈ [−1, 1], à k = 4, la loi d'attachement change peu ce temps dès N = 24 : l'étendue entre θ, rapportée au plus petit t½, vaut 4 % à N = 24 et 15 % à N = 48, dans le bruit d'échantillonnage (± 13 à ± 20 % selon le relecteur), mais 48 % à N = 32, où θ = 1 est le plus lent, au-delà du bruit. Ce n'est pas une surprise : un nouveau-né à quatre arêtes a au plus six triangles, alors qu'à l'équilibre **87 % (N = 16) à 97 % (N = 64) de la moyenne de T_v est portée par les sommets qui en ont plus de six** (19 à 39 % des sommets ; `defi_m11_queue_aristocratique.py`). Aucune loi de cette famille ne place le nouveau-né dans cette aristocratie : t½ mesure l'accession à l'aristocratie, propriété de la chaîne d'échange plus que du noyau de naissance. Avec un seuil absolu (écart ≤ 0,25 écart-type), G\* reste nettement plus rapide à petit N (N = 16 : 2,0 balayages contre 17,8 pour θ = −1, selon le relecteur).

**Contrôles.**
- Validation par le calcul exact (`defi_m11_validation.py`) : sur le secteur énumérable N = 6, M = 10, k = 4 (même densité), le Monte-Carlo reproduit les espérances exactes de T_v, T et D à dix instants et pour les cinq θ (6 000 naissances ; plus grand écart 2,5 erreurs-types sur 150 comparaisons) ; moyennes d'équilibre à 0,007 écart-type près.
- Équilibre (`defi_m11_diagnostic_equilibre.py`) : quatre chaînes indépendantes par taille, comparées sur deux moitiés de trajectoire ; leurs moyennes de T et D (donc de la moyenne de T_v sur les sommets, 3T/(N + 1)) diffèrent d'au plus 0,22 écart-type de l'observable ; taux d'acceptation 0,31 à 0,41. Ce contrôle porte sur des moyennes globales, pas sur le mélange au niveau d'un sommet.
- Seconde implémentation indépendante (`defi_m11_second_monte_carlo.py`, Python pur, générateur de la bibliothèque standard, θ = 0 ; code indépendant, même plan d'expérience) : t½ = 2,3, 5,1 et 21,6 balayages à N = 12, 16, 24 (contre 2,7, 7,5 et 22,9), soit un exposant 3,2 entre N = 12 et 24.
- Campagne indépendante du relecteur (son propre code, θ = 0, 2 000 naissances, espacements des parents de 20 à 300 balayages) : t½ = 7,0 à 8,0 (N = 16), 22,0 à 26,1 (N = 24), 45,6 à 48,2 (N = 32), 148,1 à 164,7 (N = 48) ; autocorrélation entre naissances successives entre −0,05 et +0,04 ; pas de biais lié à l'espacement des parents.

## 4. Lecture

- **[CERT]** Pour l'écart en variation totale sur toute la configuration, et à au plus 7 sommets, la naissance la plus fidèle ralentit presque toujours le pont (50 cas sur 57 ; 45 sur 47 quand son gain dépasse 10⁻³) et la naissance anti-Gibbs l'accélère le plus souvent (44 sur 57).
- **[M]** Pour les observables suivies, de N = 8 à 64, la loi d'attachement de la famille G_θ ne compte que pendant les premiers balayages. Les deux résultats ne se contredisent pas : ils mesurent des choses différentes (toute la configuration étiquetée contre trois projections), à des tailles différentes.
- **[M], le point le plus important pour RO-25** : sur graphes abstraits, le temps que met un nouveau-né à acquérir la masse triangulaire d'équilibre croît au moins comme N³ balayages entre N = 8 et 64, et la famille de lois d'attachement essayée n'y change que peu (au-delà du bruit seulement à N = 32), parce que cette masse est portée par une aristocratie de sommets que le nouveau-né doit rejoindre par les échanges. Si cette croissance se confirmait, la séparation des échelles de temps que demande le pont croissance → Gibbs (relaxer entre deux naissances) coûterait au moins de l'ordre de N⁴ échanges par naissance pour cette observable.
- À rapprocher, sous réserve, de la queue lente observée sur le moteur canonique dans DEFI-M9 ; mais le moteur canonique ne montre pas, à ce jour, de croissance en N de ce temps (le rôle de N y est [OPEN], DEFI-M10), et son décile massif est en partie fixé par la géométrie du nuage, mécanisme différent d'une aristocratie entre sommets échangeables.
- **[H]** Mécanisme non testé : la mesure π ∝ exp(N·S_sim/τ) se refroidit quand N grandit, ce qui suggérerait plutôt une croissance de type Arrhenius (exponentielle) qu'une loi de puissance.
- Rien de ceci ne réfute RO-25 : le temps reste fini à N fini, la mesure est faite sur graphes abstraits et non sur le moteur canonique, et d'autres observables, d'autres noyaux de relaxation ou d'autres lois de naissance (hors de la famille G_θ, ou avec un k variable) pourraient se comporter autrement.

## 5. Ce qui est établi, ce qui reste à vérifier, le point le plus fragile

- **Établi :** la carte exacte (102 cas, recoupée sur 42) ; les mesures Monte-Carlo de B1 et B2, validées par le calcul exact à N = 6 et recoupées par une seconde implémentation (N = 12, 16, 24) et par la campagne indépendante du relecteur (N = 16 à 48).
- **À vérifier :** tout, par une personne ; la forme de la croissance (puissance ou exponentielle) au-delà de N = 64 ; d'autres densités et d'autres k ; le moteur canonique (Rips), où les échanges sont restreints aux voisins géométriques ; le mélange au niveau d'un sommet dans la chaîne d'équilibre (les contrôles d'équilibre ne portent que sur des moyennes globales, et la validation à N = 6 ne contient pas d'aristocratie).
- **Relecture hostile (second agent IA) :** trois corrections de fond retenues — la mention de DEFI-M10 comme mesure était fausse (DEFI-M10 est ouvert), la loi « N³ » est devenue « au moins de l'ordre de N³, peut-être exponentielle », et l'indifférence à la loi d'attachement est restreinte à la famille G_θ à k = 4, avec sa raison (l'aristocratie). Corrections mineures : critère t½ déclaré a posteriori, dépendance partielle des deux campagnes, portée de B1, composition du groupe « G\* ne gagne pas ».
- **Point le plus fragile :** la forme et l'exposant de la croissance reposent sur sept tailles, un seul secteur de densité, une seule observable (la moyenne de T_v) et un critère choisi après coup ; l'écart entre les deux implémentations atteint 32 % à N = 16 (5,1 contre 7,5).

## 6. Prochain pas sur le chemin de preuve (P1)

**DEFI-M12 — La lenteur aristocratique.** Le temps d'accession d'un nouveau-né à la masse triangulaire d'équilibre croît-il comme une puissance de N ou exponentiellement ? Démontrez une borne (trou spectral du processus d'un sommet, goulot d'étranglement) ou mesurez-le jusqu'à N ≥ 128 sur graphes abstraits, à plusieurs densités, et sur le moteur canonique. Une croissance confirmée rend le pont RO-25 coûteux pour les sommets massifs ; une saturation le rend praticable.

## Reproduire

```bash
cd contributions/RO-25_pilote-ia
python3 defi_m11_carte_exacte.py            # ≈ 36 min, écrit defi_m11_carte.json
python3 defi_m11_carte_second_moteur.py     # ≈ 20 min, recoupement N ≤ 5
python3 defi_m11_carte_analyse.py           # écrit defi_m11_carte_analyse.json
pip install numba                           # 0.68.0
python3 defi_m11_validation.py              # ≈ 30 s
python3 defi_m11_monte_carlo.py             # ≈ 3 min, écrit defi_m11_monte_carlo.json
python3 defi_m11_monte_carlo.py --tailles 48,64 --thetas 0,1 --R 600 --balayages-max 2000 --sortie defi_m11_monte_carlo_long.json
python3 defi_m11_diagnostic_equilibre.py    # ≈ 5 s
python3 defi_m11_second_monte_carlo.py      # ≈ 10 min, Python pur
python3 defi_m11_demi_temps.py
python3 defi_m11_queue_aristocratique.py    # ≈ 1 min
```

Python 3.13, numpy 2.5.3, scipy 1.18.1, networkx 3.7, numba 0.68.0. Les graines sont fixées dans les scripts ; un même script rejoué sur une autre machine peut différer au niveau du bruit statistique (numba). Sorties écran : `defi_m11_*_sortie.txt`.
