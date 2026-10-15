🇫🇷 Français · 🇬🇧 [English version](DEFI-M7_REPORT_EN.md)

# DEFI-M7 — Le coût du pont croissance → Gibbs sur le moteur canonique

*Contribution du pilote IA du laboratoire (Claude, Anthropic), 15 octobre 2026. Suite directe de l'avancée n° 2 ([RAPPORT.md](RAPPORT.md), issue #16). Non relue par une personne.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Aucun changement de statut.

## 1. Question

Après la naissance d'un sommet (une arête de mitose et des arêtes de fermeture), combien d'échanges de Metropolis par arête faut-il pour que le nouveau-né devienne indiscernable d'un sommet typique ? Ce coût reste-t-il borné quand N grandit ? Sur graphes abstraits, l'avancée n° 2 donnait 2,5 à 4,7 échanges par arête pour N = 5 à 7.

## 2. Protocole (fixé avant exécution)

- **Moteur** : `corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py`, importé tel quel, paramètres canoniques gelés (κ = 6,6 ; β = 0,30 ; τ = 0,50 ; facteur de réservoir 1,6 ; τ_eff = τ/N ; thermalisation 120 N pas). Contrairement à l'avancée n° 2, la contrainte géométrique de Rips est ici **présente**.
- **Naissance** : nouveau point uniforme dans le cube, relié à ses k plus proches voisins, k (3 ou 4) choisi pour garder |E| = round(κ(N+1)/2) ; ses paires à distance < 1,6 r entrent dans le réservoir ; r reste celui de N₀. **[H-loc]** Cette loi d'attachement est posée, non dérivée (objet de DEFI-M8).
- **Mesure** : degré et triangles incidents du nouveau-né aux décalages t = 0 à 512 balayages (1 balayage = |E| tentatives d'échange), comparés à la moyenne de tous les sommets au même instant ; écart moyen et erreur-type sur toutes les naissances et graines.
- **Plan** : N₀ = 250, 500, 1 000, 2 000 (4 graines, 20 à 25 naissances successives par graine) et 4 000 (3 graines, 12 naissances).
- **Contrôle préalable** : le point de travail du moteur est-il stationnaire ? La chaîne de `build_blob` a été prolongée jusqu'à 2 520 N pas (21 fois la thermalisation canonique) pour N = 500, 1 000 et 2 000.

## 3. Résultats

### 3.1 Le point de travail est stationnaire à l'échelle des observables globales [M]

Sur 3 graines × 3 tailles, n_tri/N, CV(degrés) et Gini(masse) ne dérivent pas entre 120 N et 2 520 N pas : leurs variations restent dans les fluctuations de chaque graine (par exemple N = 2 000, graine 1 : n_tri/N = 5,146 → 5,137 ; CV = 0,876 → 0,881). Les écarts **entre** graines (N = 1 000 : n_tri/N de 5,05 à 6,04) persistent sur toute la durée : ils reflètent le désordre figé des positions (chaque graine tire son propre nuage de points, donc sa propre mesure π), pas un défaut de thermalisation. Fichier : `defi_m7_stationnarite.json`.

### 3.2 Le degré du nouveau-né se relaxe en 8 à 16 balayages, sans croissance avec N [M]

Écart moyen nouveau-né − population, en degré (population : 6,6) :

| N₀ | t = 0 | t = 4 | t = 8 | t = 16 | t = 512 | t_relax (écart < 2 erreurs-types) |
|---|---|---|---|---|---|---|
| 250 | −3,28 ± 0,05 | −1,31 ± 0,33 | −0,70 ± 0,44 | −0,52 ± 0,51 | −0,40 ± 0,51 | 8 |
| 500 | −3,32 ± 0,05 | −1,26 ± 0,31 | −0,49 ± 0,40 | −0,36 ± 0,48 | −0,21 ± 0,50 | 8 |
| 1 000 | −3,32 ± 0,05 | −1,17 ± 0,31 | −0,88 ± 0,41 | −0,48 ± 0,42 | −0,48 ± 0,49 | 16 |
| 2 000 | −3,30 ± 0,05 | −1,34 ± 0,38 | −0,68 ± 0,47 | −0,33 ± 0,58 | −0,36 ± 0,61 | 8 |
| 4 000 | −3,27 ± 0,08 | −0,99 ± 0,49 | −0,99 ± 0,58 | −0,63 ± 0,65 | −0,43 ± 0,79 | 8 |

Le temps de relaxation **par arête** ne croît pas de N = 250 à N = 4 000 (8 à 16 balayages). Conséquence directe : le coût d'une naissance, en tentatives d'échange, est de l'ordre de 10 |E|, donc **proportionnel à N** ; faire croître le Blob de N₀ à N en gardant la loi conditionnelle proche de π coûte de l'ordre de N² tentatives. Le pont est praticable, au prix d'un travail global quadratique.

### 3.3 Les triangles du nouveau-né : non résolu [M][OPEN]

Écart moyen en triangles incidents (population : 15,3 à 16,2) :

| N₀ | t = 0 | t = 8 | t = 16 | t = 64 | t = 512 |
|---|---|---|---|---|---|
| 250 | −14,9 ± 0,2 | −6,6 ± 2,8 | −3,2 ± 3,8 | −3,1 ± 3,6 | −2,5 ± 3,8 |
| 500 | −14,4 ± 0,1 | −7,2 ± 2,0 | −4,6 ± 3,0 | −4,9 ± 2,8 | −3,2 ± 3,3 |
| 1 000 | −15,2 ± 0,2 | −8,0 ± 2,8 | −6,3 ± 3,2 | −5,0 ± 3,6 | −3,6 ± 3,8 |
| 2 000 | −14,2 ± 0,1 | −6,4 ± 2,8 | −2,5 ± 4,4 | −1,9 ± 4,7 | −2,0 ± 4,8 |
| 4 000 | −14,6 ± 0,2 | −9,0 ± 3,9 | −6,5 ± 4,9 | −5,1 ± 6,3 | −3,6 ± 6,2 |

Le déficit passe sous 2 erreurs-types vers 16 balayages, mais les erreurs-types sont grandes, car la masse triangulaire est très concentrée (Gini ≈ 0,86 : quelques sommets portent beaucoup de triangles). Toutes tailles confondues, l'écart à 512 balayages vaut environ −3,0 ± 2,0 : **compatible avec zéro à 1,5 erreur-type, mais aussi avec un déficit durable** (un nouveau-né qui n'accède pas au statut des sommets massifs). Ces données ne permettent pas de trancher.

## 4. Ce qui est établi, ce qui reste à vérifier, le point le plus fragile

- **Établi [M]** : stationnarité des observables globales sur 21 fois la thermalisation canonique ; relaxation du degré en 8 à 16 balayages, sans croissance de N = 250 à 4 000 ; coût global d'une naissance proportionnel à N.
- **Non établi [OPEN]** : la relaxation de la masse triangulaire du nouveau-né ; une borne démontrée (trou spectral) ; la dépendance à la loi d'attachement.
- **Point le plus fragile** : l'observable. Comparer des moyennes est un critère nécessaire, pas suffisant ; il faudrait comparer les lois (variation totale sur l'histogramme des triangles incidents), avec beaucoup plus de naissances.

## 5. Effet proposé et prochain pas

- DEFI-M7 reste **ouvert**, avec un résultat partiel inscrit : coût par arête borné pour le degré dans la plage mesurée.
- **Défi dérivé DEFI-M9** : le nouveau-né atteint-il un jour la masse triangulaire typique, ou la viabilité fige-t-elle une aristocratie de sommets massifs ? Livrable : loi des triangles incidents du nouveau-né contre loi de la population, en variation totale, avec au moins 200 naissances par taille.

## Reproduire

```bash
pip install numba            # facultatif, accélère le moteur ; sans numba, réduire le plan
python3 contributions/RO-25_pilote-ia/defi_m7_stationnarite.py   # ≈ 15 s avec numba
python3 contributions/RO-25_pilote-ia/defi_m7_cout_du_pont.py    # ≈ 6 min avec numba
```

Python 3.13, numpy 2.5.3, scipy 1.18.1, numba 0.68.0. Sorties : `defi_m7_resultats.json`, `defi_m7_stationnarite.json`.
