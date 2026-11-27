# DEFI-M20 (RO-08), volet « κ ≥ 8 » — l'aristocratie et l'obstacle local survivent à un degré moyen plus grand

> **Statut inchangé : TOE démontrée NON · portes physiques 0/7 · niveau 1.** Contribution du pilote IA du laboratoire (Claude, Anthropic), par délégation de Rudolphe Mirante, 27 novembre 2026. Défi : [DEFI-M20](https://github.com/BlobPrinciple/The-blob-Principle/issues/56), troisième livrable possible (« la mesure des conditions locales sous une variante de A_Gibbs à κ ≥ 8 »). Point de départ, non refait : `contributions/RO-08_pilote-ia/NOTE.md`.

## Objet

À κ = 6,6, la borne de Walkup exclut d'emblée que le graphe de A_Gibbs soit le 1-squelette d'une 3-variété fermée connexe (RO-08, NOTE.md, Résultat 1). Ce verrou est arithmétique : il tombe dès κ ≥ 8 − 20/N. Reste à savoir si l'obstacle **local** (aristocratie des triangles, violations des conditions de link) n'était qu'un effet du petit degré moyen. On change donc κ seul dans le moteur et on mesure.

**Critère et prédictions déposés publiquement avant la mesure** : [issue #56, commentaire du 27/11/2026](https://github.com/BlobPrinciple/The-blob-Principle/issues/56#issuecomment-7213958737).

## Résultat en bref

1. **[M] L'aristocratie est gardée à tous les κ testés (6,6 à 14), selon le critère déposé.** Gini des triangles par sommet : Blob 0,73 à 0,88 contre RGG 0,34 à 0,48 ; part des triangles portée par le décile supérieur : Blob 0,68 à 0,88 contre 0,23 à 0,32. Les écarts Blob − RGG valent au moins 0,37 (Gini) et 0,43 (décile) à chaque κ et chaque N, au moins quatre fois le seuil 0,10. L'aristocratie s'atténue lentement quand κ croît (Gini 0,877 → 0,747 à N = 4 000) et l'écart au témoin se resserre (A10 : 0,58 → 0,46 à N = 4 000, de κ = 6,6 à 14) ; rien n'est extrapolé au-delà de κ = 14.
2. **[M] L'obstacle local ne bouge pas avec κ ; sans viabilité, il recule.** Fraction des sommets violant (C1), (C2) ou (C3) : Blob 0,972 à 0,981 à tous les κ et N ; RGG 0,92 → 0,47 de κ = 6,6 à 14 (N = 4 000). Au niveau des sommets, (C3) porte à elle seule toutes les violations du Blob : dans les 15 lignes, la fraction des sommets touchant une arête à moins de 3 voisins communs est égale à V (97 à 98 %, à tous les κ, contre 45 % pour le RGG à κ = 14) ; (C2) vient en plus (0,78 → 0,91, en hausse avec κ ; RGG 0,78 → 0,24). Prédiction « obstacle subsistant » : vérifiée selon le critère ; « porté surtout par (C3) » : vérifiée qualitativement, hors critère chiffré.
3. **[M] À κ ≥ 12, la viabilité fait perdre des triangles par rapport à son propre état de départ ; dès κ = 10, la condition globale est parfois violée.** Le RGG est exactement l'état initial de la chaîne du Blob (mêmes points, mêmes arêtes, `_rips`). À N = 4 000 : n_tri/N = 5,23 (Blob) contre 3,60 (RGG) à κ = 6,6, 8,47 contre 8,32 à κ = 10, mais 10,36 contre 12,02 à κ = 12 et 12,04 contre 16,42 à κ = 14. La condition globale nécessaire n_tri/N ≥ κ − 2 (somme de (C2), [T]) est violée par 1 configuration du Blob sur 12 à κ = 10, 2 sur 12 à κ = 12 et 2 sur 12 à κ = 14. Cette exclusion par simple comptage est redondante (la condition globale est la somme de (C2), et toutes les configurations du Blob sont déjà exclues localement), mais elle montre que la viabilité ne crée même plus assez de triangles en tout.

**Verdict.** Relever κ lève le verrou arithmétique de Walkup mais pas l'obstacle : sous la variante à κ seul changé (β, τ, therm_fac canoniques), le graphe reste aristocratique et presque tous ses sommets restent incompatibles avec un link de 2-sphère. À état initial identique, c'est la chaîne de viabilité (dans ce réglage et à cette durée), non le petit degré, qui éloigne le graphe d'une triangulation ; le témoin sans viabilité s'en rapproche quand κ croît. RO-08 reste ouvert ; DEFI-M20 reste ouvert (algorithme de complétion et coût par sommet non traités). Aucun changement de statut.

## Variante et protocole

- Moteur canonique `corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py` importé tel quel ; `build_blob(N, seed, kappa=κ)` avec β = 0,30, τ = 0,50, pool_fac = 1,6, therm_fac = 120 inchangés (tableau `PARAMETRES CANONIQUES` du moteur). **Ce n'est pas A_Gibbs canonique** : c'est une variante à κ seul changé ; les arêtes initiales (les round(κN/2) paires les plus courtes du pool de rayon 1,6 r) et le pool suivent κ (`_rips`).
- Témoin `build_rgg` au même κ (même |E|, sans viabilité).
- κ ∈ {6,6 ; 8 ; 10 ; 12 ; 14} ; N ∈ {1 000 ; 2 000 ; 4 000} ; graines 0 à 3 ; 120 configurations.
- Conditions nécessaires [T] de RO-08 (NOTE.md, § Conditions nécessaires utilisées) : (C1) deg ≥ 4 ; (C2) t_v ≥ 3 deg − 6 ; (C3) au moins 3 voisins communs par arête ; (Glob) n_tri/N ≥ κ − 2.
- Grandeurs du critère : V (sommets en violation), G (Gini de t_v), A10 (part de Σ t_v au décile supérieur), Z (sommets sans triangle).
- κ = 14 est le degré moyen du germe de Freudenthal–Kuhn de T³, contrôle positif de RO-08 (zéro violation).

## Mesures (moyennes sur 4 graines)

| κ | N | Blob V | C1 | C2 | C3 (arêtes) | G | A10 | Z | n_tri/N (seuil κ − 2) | RGG V | RGG G | RGG A10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6,6 | 1 000 | 0,972 | 0,277 | 0,772 | 0,640 | 0,871 | 0,860 | 0,283 | 5,38 (4,60) | 0,906 | 0,478 | 0,316 |
| 6,6 | 2 000 | 0,975 | 0,274 | 0,772 | 0,645 | 0,865 | 0,852 | 0,291 | 5,04 (4,60) | 0,916 | 0,460 | 0,299 |
| 6,6 | 4 000 | 0,975 | 0,273 | 0,776 | 0,649 | 0,877 | 0,877 | 0,310 | 5,23 (4,60) | 0,920 | 0,461 | 0,302 |
| 8 | 1 000 | 0,972 | 0,167 | 0,832 | 0,627 | 0,852 | 0,834 | 0,185 | 6,90 (6,00) | 0,844 | 0,447 | 0,299 |
| 8 | 2 000 | 0,972 | 0,166 | 0,819 | 0,621 | 0,847 | 0,826 | 0,195 | 6,60 (6,00) | 0,864 | 0,426 | 0,279 |
| 8 | 4 000 | 0,978 | 0,156 | 0,843 | 0,647 | 0,859 | 0,853 | 0,199 | 6,60 (6,00) | 0,870 | 0,425 | 0,280 |
| 10 | 1 000 | 0,976 | 0,081 | 0,877 | 0,597 | 0,819 | 0,797 | 0,092 | 9,12 (8,00) | 0,731 | 0,407 | 0,274 |
| 10 | 2 000 | 0,979 | 0,078 | 0,871 | 0,599 | 0,814 | 0,786 | 0,100 | 8,52 (8,00) | 0,745 | 0,389 | 0,258 |
| 10 | 4 000 | 0,981 | 0,070 | 0,886 | 0,629 | 0,828 | 0,809 | 0,103 | 8,47 (8,00) | 0,759 | 0,388 | 0,260 |
| 12 | 1 000 | 0,976 | 0,042 | 0,898 | 0,538 | 0,778 | 0,736 | 0,050 | 11,27 (10,00) | 0,581 | 0,384 | 0,261 |
| 12 | 2 000 | 0,977 | 0,044 | 0,879 | 0,547 | 0,775 | 0,724 | 0,055 | 10,39 (10,00) | 0,603 | 0,365 | 0,246 |
| 12 | 4 000 | 0,980 | 0,036 | 0,899 | 0,584 | 0,790 | 0,757 | 0,053 | 10,36 (10,00) | 0,618 | 0,361 | 0,245 |
| 14 | 1 000 | 0,974 | 0,024 | 0,891 | 0,472 | 0,732 | 0,677 | 0,028 | 13,27 (12,00) | 0,446 | 0,362 | 0,247 |
| 14 | 2 000 | 0,975 | 0,023 | 0,891 | 0,503 | 0,737 | 0,681 | 0,029 | 12,36 (12,00) | 0,461 | 0,342 | 0,233 |
| 14 | 4 000 | 0,981 | 0,019 | 0,905 | 0,532 | 0,747 | 0,696 | 0,030 | 12,04 (12,00) | 0,472 | 0,340 | 0,234 |

Source : `m20_kappa.json`, `m20_analyse_sortie.txt`. Les valeurs à κ = 6,6 reproduisent celles de RO-08 (mêmes graines ; V = 0,975 à N = 1 000, graine 0, dans les deux).

Fraction des sommets touchant une arête (C3) à N = 4 000 : Blob 0,975 ; 0,978 ; 0,981 ; 0,980 ; 0,981 (κ = 6,6 à 14) ; RGG 0,895 ; 0,839 ; 0,722 ; 0,585 ; 0,446.

Condition globale par configuration (Blob) : violée à κ = 10 (N = 4 000 graine 2 : 7,95 < 8), à κ = 12 (N = 1 000 graine 0 : 9,89 < 10 ; N = 4 000 graine 2 : 9,76) et à κ = 14 (N = 2 000 graine 0 : 11,59 < 12 ; N = 4 000 graine 2 : 11,06)  ; jamais à κ ≤ 8. Le RGG la viole dans toutes ses configurations à κ = 6,6 et 8 (3,66 et 5,41 en moyenne sur 12 configurations), jamais à κ ≥ 10.

**Supplément hors critère (cœur du cube).** Sommets à plus de 2 r des faces, calculé par la seconde implémentation à N = 1 000 et 2 000 : le Blob y reste à 0,92 à 1,00 de sommets en violation ; le RGG y est violé à peu près autant que sur tout le cube (écart ≤ 0,04 dans les deux sens). L'effet n'est pas un effet de bord. À κ ≥ 12 et N = 1 000, le cœur ne compte que quelques dizaines de sommets.

## Recoupement

`m20_second_moteur.py` : mesures refaites sans code commun (matrices creuses ; décile par `np.partition` ; Gini par une forme par rangs, algébriquement identique à celle du moteur, donc code distinct mais non méthode indépendante) sur 40 configurations (κ, N, graine) à N = 1 000 et 2 000, pour les deux modèles, et témoin RGG reconstruit sans le moteur (`cKDTree.query_pairs`, tri par longueur) puis comparé arête par arête. **ACCORD** : 560 comparaisons (7 grandeurs × 2 modèles × 40 configurations), écart maximal 2,2·10⁻¹⁶ ; RGG reconstruit identique arête par arête dans les 40 configurations. La génération du Blob n'est pas indépendante (même moteur, déterministe à graine fixée) : seules les mesures le sont.

## Limites

- Variante, non moteur canonique : seul κ change ; β et τ ne sont pas recalibrés. À τ_eff = τ/N fixé, le poids d'un triangle dans S = ln(1 + n_tri) − β·CV vaut environ 1/n_tri ; rapporté à τ_eff, il vaut ≈ 2/(n_tri/N), soit ≈ 0,38 à κ = 6,6 et ≈ 0,17 à κ = 14, de plus en plus petit quand κ croît (aucun seuil franchi) ; [H] c'est l'explication probable du point 3 (la chaîne devient plus entropique), non testée ici.
- therm_fac = 120 donne 120·N essais pour κ·N/2 arêtes, soit environ 17 essais par arête à κ = 14 contre 36 à κ = 6,6 : l'équilibre est moins atteint à grand κ. Aucune relaxation longue n'a été faite à κ ≥ 8.
- Le plafond de degré CAP = 96 du moteur n'est pas atteint (degré maximal 76 sur les 120 configurations).
- Conditions nécessaires seulement : les franchir ne ferait pas une triangulation. Pour T³, la borne de Novik–Swartz (RO-08, NOTE.md, point 1) exige κ ≥ 8 + 40/N : κ = 8 exactement reste exclu globalement pour T³.
- 4 graines par point ; écart-type entre graines ≤ 0,01 pour V ; jusqu'à 0,04 (G) et 0,07 (A10) à N = 1 000, 0,01 à 0,04 à N = 4 000.

## Question ouverte

[OPEN] Existe-t-il un réglage (κ, β, τ) de la mesure de viabilité qui garde ses propriétés (aristocratie, toile, persistance) **et** satisfait les conditions locales de link, ou l'aristocratie est-elle incompatible par nature avec un 1-squelette de 3-variété ? Le coût en arêtes vers une triangulation de T³ (premier livrable de DEFI-M20) reste à mesurer.

## Reproduire

```
pip install numba   # le moteur l'utilise
python3 contributions/DEFI-M20_pilote-ia/m20_kappa.py          # ≈ 14 min sur 2 cœurs
python3 contributions/DEFI-M20_pilote-ia/m20_analyse.py
python3 contributions/DEFI-M20_pilote-ia/m20_second_moteur.py  # ≈ 4 min ; dernière ligne ACCORD
```

Fichiers : `m20_kappa.py`, `m20_second_moteur.py`, `m20_analyse.py`, `m20_kappa.json`, `m20_second_moteur.json` et les sorties `*_sortie.txt`.
