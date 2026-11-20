🇫🇷 Français · 🇬🇧 [English version](NOTE_EN.md)

# DEFI-R7 — La condensation viable en boîte périodique : elle survit, sans effet de taille, et grossit encore lentement

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Note du pilote IA du laboratoire (Claude, Anthropic), session planifiée du 20 novembre 2026, par délégation de Rudolphe Mirante. Non relue par une personne.

## Objet

DEFI-R7 ([#47](https://github.com/BlobPrinciple/The-blob-Principle/issues/47) ; `docs/defis.json`) part de la partie C de DEFI-R6 (`contributions/R6_pilote-ia/NOTE.md`, « C. La viabilité seule, sans germes ») : sous le moteur de mobilité archivé (`relax_positions`, `local_S`, `rgg_radius` de `corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob gravite colab.py`, V346 XXV.1 p. 642), la viabilité seule, depuis un départ uniforme, creuse des vides et fait naître un pic de P(k) à k = 3–5, environ 2,9·r_N. Deux questions : cette condensation s'arrête-t-elle à une échelle fixée par r_N, β et τ, ou mûrit-elle sans fin ? Survit-elle à une boîte périodique ? Livrable : campagne en boîte périodique, départ uniforme, au moins 3 tailles et 8 graines par point, jusqu'à au moins 1 280 balayages, L(t, N) avec barres d'erreur, comparée à r_N.

Ce que DEFI-R6 a établi et que cette note ne refait pas : la condensation existe en boîte rognée (8/8 graines, N = 2 500 et 5 000, jusqu'à 320 balayages) ; la mobilité sans viabilité ne la produit pas ; le relecteur de DEFI-R6 l'avait retrouvée dans la sous-boîte intérieure.

## Résultat en bref

1. **[M] La condensation survit à la boîte périodique.** Même règle, pas pris modulo 1 et distance d'image minimale au lieu du rognage : à N = 2 500, vides 0,811 ± 0,001 (80 balayages) et 0,867 ± 0,001 (320), contre 0,806 et 0,858 en boîte rognée ; pic de S(k) aux coquilles 3–4 dans les deux cas. Le bras mobile sans viabilité reste au niveau uniforme jusqu'à 1 280 balayages (vides 0,731 à 0,733 ; S_max de 1,04 à 1,9, maximum du bruit sur 31 coquilles).
2. **[T] Toute longueur propre à la règle est un multiple de r_N, par construction ; [M] aucun effet de taille de boîte n'est visible.** Le premier point est une analyse dimensionnelle, pas une mesure : κ fixe la densité en unités de r_N³, le pas vaut σ = 0,3·r_N, N//4 tentatives par balayage donnent la même cadence par sommet à tout N, β et τ sont sans dimension ; en unités de r_N, la seule autre longueur est la boîte. Ce que la mesure apporte : L/r_N = c(t) ne dépend pas de N à la précision obtenue, alors que la boîte contient 4 à 6,3 longueurs selon N. Avec l'estimateur coupé au même k·r_N à toutes les tailles, L₁c/r_N = 2,75 ; 2,73 ; 2,73 à 80 balayages et 2,95 ; 2,94 ; 2,93 à 1 280 (N = 2 500 ; 5 000 ; 10 000). La hauteur du pic ne dépend pas non plus de N (S_max ≈ 52 à 54 aux trois tailles à 1 280 balayages).
3. **[M] La longueur grossit encore, lentement, sans arrêt visible sur la fenêtre.** De 80 à 1 280 balayages, L₁c/r_N croît d'environ 7 % (pente d ln L₁c/d ln t = 0,026 ± 0,002 ; 0,027 ± 0,001 ; 0,026 ± 0,001 selon N) ; le sommet du pic glisse plus vite (L_pic/r_N 2,88 → 3,52 à N = 2 500), mais cet estimateur interpolé sur des coquilles entières 3–4 est fragile. Les accroissements par doublement du temps ne diminuent pas (L₁/r_N à N = 2 500 : 2,70 ; 2,70 ; 2,76 ; 2,82 ; 2,91 à 80, 160, 320, 640, 1 280). L'amplitude croît bien plus vite (S_max 12 → 52, vides 0,81 → 0,89 à N = 2 500). **[OPEN]** Arrêt à une longueur finie, ou mûrissement lent sans fin (logarithmique ou à petit exposant) : la fenêtre ne tranche pas.

**Verdict.** La condensation viable n'est pas un effet de bord : elle survit à la boîte périodique, et sa longueur, en unités de r_N, est la même à toutes les tailles mesurées. Que cette longueur soit « une échelle du modèle » est vrai par construction tant qu'elle n'atteint pas la boîte ; la vraie question de DEFI-R7 est donc celle du point 3 : c(t) a-t-il une limite ? Elle reste ouverte : à 1 280 balayages, la longueur grossit encore de quelques pour cent par doublement du temps. Si ce grossissement ne s'arrête pas, elle finira par atteindre la taille de la boîte, et la lecture « échelle microscopique, non cosmique » de DEFI-R6 (partie C) ne vaudrait que pour des durées finies. β et τ n'ont pas été variés. Aucun changement de statut ; armature V347.1 non touchée.

## Méthode

**Règle (reprise du moteur archivé, constantes inchangées).** κ = 6,6 ; β = 0,30 ; τ = 0,50 ; r_N = (κ/((N − 1)·4π/3))^{1/3} ; σ = 0,3·r_N ; N//4 tentatives par balayage ; un sommet isolé ne bouge pas ; acceptation de Metropolis sur la seule S locale du sommet déplacé, S(v) = ln(1 + triangles en v) − β·(écart-type de population / moyenne des degrés des voisins) ; bras mobile : acceptation 1/2. Le graphe est le graphe géométrique (0 < d < r_N) des positions : le moteur archivé le reconstruit lui aussi à chaque pas (`rebuild`) et, depuis un départ uniforme, son graphe initial est géométrique ; il est donc ici recalculé à la volée (seul écart, sans portée pratique : l'archive construit le graphe initial avec d ≤ r).

**Seule modification voulue.** Boîte périodique : pas pris modulo 1, distance d'image minimale. L'option `--rogne` rend le rognage `np.clip` du moteur archivé.

**Implémentation A** (`r7_periodique.py`, numba, listes de cellules de côté ≥ r_N ; aucun débordement de cellule, le code compte les refus forcés : 0 partout). Contrôle en boîte rognée, même départ uniforme, 8 graines, contre les fichiers de DEFI-R6 (`r6_campagne_N2500_b80_initpoisson.json`, `…_b320_…`, produits par le script de DEFI-R6 qui importe `relax_positions` tel quel ; contrôle donc indirect du moteur archivé) : vides 0,8064 ± 0,0008 contre 0,8054 ± 0,0008 (+0,9 σ) à 80 balayages, 0,8583 ± 0,0009 contre 0,8596 ± 0,0015 (−0,8 σ) à 320 ; coquille du pic 3–4 contre 3–4 ; bras mobile 0,7305 contre 0,7316.

**Mesures.** Vides : fraction des 20³ cellules vides (convention de DEFI-R6). S(k) = P(k)/N, P par FFT des comptes sur grille 64³ (affectation au plus proche, périodique), moyenne par coquille round(|k|) = 1 à 31 ; S = 1 pour l'uniforme. Trois longueurs, en unités de la boîte (L = 1/k, convention de DEFI-R6), divisées par r_N :
- **L₁c** = 1/k₁c, k₁c premier moment de l'excès (S − 1)₊ sur k ≤ ⌊0,8/r_N⌋ (9, 11, 14 selon N : même coupure en unités de r_N) — estimateur de tête ;
- L₁ = 1/k₁, même moment sur k ≤ 20 (coupure k·r_N = 1,71 ; 1,36 ; 1,08 selon N : estimateurs différents d'une taille à l'autre, donné pour comparaison avec la première version) ;
- L_pic, sommet du pic interpolé par une parabole sur trois coquilles.
La fenêtre de l'affectation au plus proche atténue S de moins de 3 % à k ≤ 6 et jusqu'à environ 28 % à k = 20 (selon un axe) ; elle tire L₁ un peu vers le haut aux grands N, d'où le choix de L₁c. Barres : erreur-type sur les graines. Les départs se recouvrent entre tailles (`default_rng(1000 + g)` : les 2 500 premiers points de N = 5 000 sont ceux de N = 2 500) : corrélation faible entre tailles, déclarée.

**Implémentation B** (`r7_second_moteur.py`, sans code commun) : Python et numpy, distances d'image minimale par force brute, générateur PCG64 sur d'autres graines, et facteur de structure **exact** |Σ_j exp(2iπ n·x_j)|²/N sur tous les vecteurs entiers n de la coquille (aucune grille). N = 2 500, 3 graines, 80 balayages (B est environ 40 fois plus lent que A).

## Mesures

Boîte périodique, départ uniforme ; erreur-type sur les graines.

| N (graines) | balayages | vides viab | vides mobile | L₁c/r_N | L₁/r_N | L_pic/r_N | S_max |
|---|---|---|---|---|---|---|---|
| 2500 (8) | 20 | 0,759 ± 0,001 | 0,731 | 2,57 ± 0,03 | 2,45 ± 0,03 | 2,73 ± 0,09 | 3,5 ± 0,1 |
| 2500 (8) | 80 | 0,811 ± 0,001 | 0,731 | 2,75 ± 0,02 | 2,70 ± 0,02 | 2,88 ± 0,05 | 12,1 ± 0,3 |
| 2500 (8) | 320 | 0,867 ± 0,001 | 0,732 | 2,79 ± 0,02 | 2,76 ± 0,01 | 3,25 ± 0,09 | 31,1 ± 1,2 |
| 2500 (8) | 1280 | 0,894 ± 0,001 | 0,732 | 2,95 ± 0,01 | 2,91 ± 0,01 | 3,52 ± 0,06 | 52,0 ± 2,6 |
| 2500 | pente d ln L/d ln t, t = 80–1280 | | | 0,026 ± 0,002 | 0,028 ± 0,002 | | |
| 5000 (8) | 20 | 0,602 ± 0,001 | 0,534 | 2,60 ± 0,02 | 2,57 ± 0,02 | 2,68 ± 0,07 | 3,6 ± 0,1 |
| 5000 (8) | 80 | 0,703 ± 0,001 | 0,535 | 2,73 ± 0,01 | 2,71 ± 0,01 | 2,83 ± 0,05 | 12,3 ± 0,2 |
| 5000 (8) | 320 | 0,799 ± 0,001 | 0,535 | 2,77 ± 0,01 | 2,73 ± 0,01 | 3,20 ± 0,05 | 31,1 ± 0,8 |
| 5000 (8) | 1280 | 0,839 ± 0,002 | 0,535 | 2,94 ± 0,01 | 2,91 ± 0,01 | 3,56 ± 0,11 | 51,6 ± 1,6 |
| 5000 | pente d ln L/d ln t, t = 80–1280 | | | 0,027 ± 0,001 | 0,025 ± 0,001 | | |
| 10000 (8) | 20 | 0,398 ± 0,001 | 0,290 | 2,61 ± 0,02 | 2,61 ± 0,02 | 2,79 ± 0,05 | 3,5 ± 0,1 |
| 10000 (8) | 80 | 0,550 ± 0,001 | 0,283 | 2,73 ± 0,01 | 2,72 ± 0,01 | 2,97 ± 0,02 | 12,8 ± 0,4 |
| 10000 (8) | 320 | 0,693 ± 0,001 | 0,285 | 2,76 ± 0,01 | 2,73 ± 0,01 | 3,16 ± 0,04 | 33,2 ± 0,7 |
| 10000 (8) | 1280 | 0,756 ± 0,001 | 0,288 | 2,93 ± 0,01 | 2,90 ± 0,01 | 3,56 ± 0,04 | 53,5 ± 1,0 |
| 10000 | pente d ln L/d ln t, t = 80–1280 | | | 0,026 ± < 0,001 | 0,023 ± 0,000 | | |

Seconde implémentation (N = 2 500, 80 balayages, 3 graines B contre 8 graines A) : vides 0,8096 ± 0,0021 contre 0,8111 ± 0,0008 (−0,7 σ) ; coquille du pic 4, 4, 4 contre 4 (sept graines) et 5 ; S(k) pour k = 1 à 6 : B 2,45 ; 6,15 ; 10,73 ; 12,25 ; 9,93 ; 5,54 contre A 1,78 ; 5,55 ; 9,53 ; 12,09 ; 9,74 ; 5,44, écarts de 0,2 à 2,1 erreurs combinées. B est plus haut que A aux six coquilles (+38 % à k = 1, +12 % à k = 3) ; la fenêtre de A (< 3 %) ne l'explique pas ; avec 3 graines et des coquilles corrélées au sein d'une même graine, l'écart reste compatible avec le bruit. Résultat : compatible ; cette seconde implémentation contrôle le codage de la règle et de la mesure, pas le modèle.

## Ce qui ne tient pas, ou pas encore

- **β et τ non variés.** Seul N varie ; l'indépendance en N n'est pas une découverte sur r_N (point 2). Le défi demandait aussi le rôle de β et τ. [OPEN]
- **Asymptotique.** Une croissance d'environ 7 % sur un facteur 16 en temps ne distingue ni un arrêt lointain, ni une loi logarithmique, ni une petite puissance ; les estimateurs ne donnent pas la même pente (≈ 0,026 pour L₁ et L₁c, ≈ 0,07 pour L_pic). [OPEN]
- **Taille de boîte.** À N = 2 500 la boîte ne contient que 4 longueurs ; le pic tombe sur les coquilles 3 à 4. La coïncidence aux trois tailles indique que la boîte ne fixe pas encore la longueur ; elle la fixerait si le grossissement continuait assez longtemps.
- **Une seule observable de forme** (S(k)) ; pas de mesure des amas dans l'espace réel ; positions finales non archivées.

## Écarts au livrable

- Le livrable est rempli pour la boîte périodique (3 tailles, 8 graines par point, départ uniforme, 1 280 balayages, L(t, N) avec erreurs-types, comparée à r_N). Il ne l'est pas pour β et τ, qui n'ont pas été variés (budget d'une exécution ; voir DEFI-R8).
- La seconde implémentation ne couvre que N = 2 500, 3 graines, 80 balayages (elle est environ 40 fois plus lente) ; les instants tardifs (320 à 1 280 balayages) et les tailles 5 000 et 10 000 reposent sur l'implémentation A seule.
- Les graines de N = 10 000 sont réparties dans quatre fichiers (`r7_N10000.json`, `_b`, `_c`, `_d`), calculés en parallèle ; elles sont disjointes.

## Ce que ceci change

- Pour la toile simulée (DEFI-R6) : la condensation propre à la viabilité n'est pas un artefact des faces rognées ; à 1 280 balayages au plus, sa longueur est de l'ordre de 3·r_N à toutes les tailles. Le mot « microscopique » de DEFI-R6 (partie C) doit être lu « à durée finie » tant que l'arrêt n'est pas établi.
- Rien au statut du programme ni à l'armature V347.1. Les portes physiques restent à 0/7.
- Défi dérivé : **DEFI-R8** — la condensation viable s'arrête-t-elle, et dépend-elle de β et τ ?

## Point le plus fragile

La question posée (arrêt ou mûrissement) n'est pas tranchée ; la seule affirmation forte de mesure est l'absence d'effet de taille, sur trois tailles, à un seul jeu (β, τ, σ/r_N), mesurée sur des coquilles entières aux petits k (3 à 7).

## Reproduire

```
pip install numba numpy scipy
cd contributions/R7_pilote-ia
python3 r7_periodique.py --N 2500 --graines 0:8 --sortie r7_N2500.json        # 1 à 2 min par graine
python3 r7_periodique.py --N 5000 --graines 0:8 --sortie r7_N5000.json        # ≈ 3 à 4 min par graine
python3 r7_periodique.py --N 10000 --graines 0:2 --sortie r7_N10000.json      # ≈ 5 à 6 min par graine
python3 r7_periodique.py --N 10000 --graines 2:4 --sortie r7_N10000_b.json
python3 r7_periodique.py --N 10000 --graines 4:6 --sortie r7_N10000_c.json
python3 r7_periodique.py --N 10000 --graines 6:8 --sortie r7_N10000_d.json
python3 r7_periodique.py --N 2500 --graines 0:8 --instants 0,80,320 --rogne --sortie r7_N2500_rogne.json
python3 r7_second_moteur.py --N 2500 --graines 0:3 --instants 0,80 --sortie r7_second_N2500.json   # ≈ 2 min par graine
python3 r7_analyse.py > r7_analyse_sortie.txt
python3 r7_tableau.py        # tableau de cette note ; --en pour la version anglaise
```
Durées mesurées sur 2 cœurs partagés entre trois calculs. numba 0.62.1.

## Relecture hostile

Un sous-agent IA, briefé avec la seule note, les scripts, les sorties et les références citées, a relu la première version. Trois bloquants retenus : (1) « l'échelle est fixée par r_N » était vrai par construction (analyse dimensionnelle) et contredisait « elle grossit » : titre, point 2 et verdict réécrits, la question centrale devient l'arrêt de c(t) ; (2) L₁ coupé à k ≤ 20 n'est pas le même estimateur d'une taille à l'autre : L₁c (coupure fixe en k·r_N) devient l'estimateur de tête ; (3) le texte annonçait des graines encore en calcul : chiffres resynchronisés sur la sortie finale. Mineurs retenus : fidélité de la règle confirmée par le relecteur (seul écart d ≤ r initial, sans portée), validation rognée déclarée indirecte, moteur B « compatible » et non « vérifie » (B au-dessus de A aux six coquilles), recouvrement des départs entre tailles, effet de la fenêtre chiffré, S_max du bras mobile donné, fragilité de L_pic.
