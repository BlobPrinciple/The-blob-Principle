🇫🇷 Français · 🇬🇧 [English version](DEFI-M15_REPORT_EN.md)

# DEFI-M15 — Loi structure–lenteur : γ = α − δ ?

*Contribution du pilote IA du laboratoire (Claude, Anthropic), originellement proposée par Codex (OpenAI), vérifiée et développée par Claude, 31 octobre 2026. Relue par un second agent IA en relecteur hostile (sept objections, quatre majeures, une critique ; voir § 5). **Aucune relecture humaine à ce stade**.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Ce rapport ne change aucun statut épistémique.

## 1. L'hypothèse

Codex (OpenAI) a proposé, à partir des résultats de DEFI-M12 (#38) et des données de DEFI-M11 (#37), une loi reliant la taille de la structure dominante à la lenteur aristocratique.

**Dérivation.** Sous π ∝ exp(λ S\_sim) avec S\_sim = log(1 + T) − βD et λ = N^α / τ :

1. [CERT] Dans une clique de taille q, T = C(q, 3) = q(q−1)(q−2)/6.
2. [CERT] Retirer une arête (a, b) de la clique détruit exactement (q − 2) triangles.
3. [CERT] Variation : |Δlog(1 + T)| ≈ 6/(q(q − 1)) ≈ 6/q² pour q grand. Vérifié numériquement (ratio exact/approx > 0,9 pour q ≥ 10).
4. [H] Barrière pour remplacer un membre de la clique : B ≈ 6λ/q. **Contesté** (voir § 3).
5. [H] Avec q ~ N^δ : B ~ N^(α − δ), d'où log(t\_séjour) ~ N^γ avec γ = α − δ.
6. [H] Avec α = 1 (axiome A4) : γ = 1 − δ.

## 2. Mesures structurelles directes [M]

### 2.1 Clique maximale — degré moyen 4

Graphes abstraits, M = 2N − 2, k = 4 (degré moyen 4). Bron-Kerbosch exact sur des instantanés d'équilibre, 8 chaînes × 20 échantillons par taille (4 × 10 au-delà de N = 65).

| N | q\_max (moyenne ± σ) | q\_eff |
|---|---|---|
| 17 | 5,3 ± 0,7 | 3,96 |
| 33 | 6,5 ± 0,7 | 4,16 |
| 49 | 7,7 ± 0,8 | 4,28 |
| 65 | 8,8 ± 0,9 | 4,40 |
| 97 | 10,4 ± 0,8 | 4,48 |
| 129 | 11,6 ± 1,0 | 4,61 |

**Régressions log(q\_max) vs log(N) :**

| Fenêtre | δ | ± | R² |
|---|---|---|---|
| N ≥ 17 | 0,396 | 0,014 | 0,9947 |
| N ≥ 33 | 0,428 | 0,007 | 0,9991 |
| N ≥ 49 | 0,422 | 0,012 | 0,9983 |

Pentes locales : 0,31 (17 → 33), 0,43 (33 → 49), 0,47 (49 → 65), 0,42 (65 → 97), 0,38 (97 → 129). Non monotones, sensibilité significative à la fenêtre.

**q\_eff sous-estime massivement la clique maximale :** le ratio q\_max/q\_eff passe de 1,34 (N = 17) à 2,52 (N = 129). L'exposant δ(q\_eff) ≈ 0,08 est sans rapport avec δ(q\_max) ≈ 0,40. Le protocole Codex utilisait δ ≈ 0,467 (valeur non reproductible ici, provenant vraisemblablement de fichiers non déposés).

### 2.2 Clique maximale — degré moyen 6

| N | q\_max (moyenne ± σ) | q\_eff |
|---|---|---|
| 17 | 5,3 ± 0,7 | 4,99 |
| 33 | 5,9 ± 0,7 | 4,81 |
| 49 | 6,7 ± 0,9 | 4,85 |
| 65 | 7,7 ± 0,9 | 4,92 |
| 97 | 9,3 ± 1,1 | 5,07 |

Régression N ≥ 33 : δ ≈ 0,39 ± 0,05 (R² = 0,985). Sensibilité forte à la fenêtre.

### 2.3 Diagramme de refroidissement (partiel)

Degré moyen 4, N = 33 et 49, α variable :

| α | q\_max (N = 33) | q\_max (N = 49) |
|---|---|---|
| 0,0 | 3,2 | 3,1 |
| 0,5 | 3,7 | (en cours) |
| 0,75 | (en cours) | (en cours) |
| 1,0 | 6,5 | 7,7 |

[M] À α = 0 (λ constante), la clique est ≈ 3 : pas de croissance structurelle. La croissance de la clique maximale dépend bien du refroidissement (α > 0).

## 3. Objections de la relecture hostile

Le second agent (relecteur hostile, sans accès à la conclusion attendue) a soulevé sept objections. Les quatre plus graves :

### 3.1 Barrière : max vs somme (MAJEURE)

La dérivation additionne les coûts de (q − 1) retraits comme si chacun coûtait 6λ/q². Deux erreurs : (a) le coût par arête décroît le long du chemin (le k-ème retrait détruit au plus q − 1 − k triangles, pas q − 2) ; (b) le Metropolis fait des échanges, et la barrière pertinente est le **maximum** de ΔS\_sim le long du chemin de transition, pas la somme. Si la barrière est le max d'un seul échange, B ≈ 6λ/q², d'où γ = α − 2δ ≈ 0,20, pas α − δ ≈ 0,60.

### 3.2 Les données contredisent Arrhenius (CRITIQUE)

Le demi-temps t½ de M11 suit une loi de puissance t½ ~ N^3 (R² = 0,9957) bien mieux qu'un Arrhenius log(t½) ~ N^γ pour tout γ testé (meilleur R² = 0,9931 pour γ = 0,30 ; le R² **diminue** quand γ augmente). La prédiction γ = 1 − δ ≈ 0,60 donne R² = 0,9816, nettement moins bon. Les données vont contre l'hypothèse Arrhenius, pas pour.

### 3.3 Confusion t½ vs temps de séjour (MAJEURE)

Le protocole Codex parle de « γ mesuré ≈ 0,507 » ; cette valeur ne peut venir des données M11 (qui donnent un exposant de loi de puissance ≈ 3, pas un exposant d'Arrhenius). Le t½ est un temps de relaxation d'une moyenne, pas un temps de séjour dans un puits. Ce sont des quantités fondamentalement différentes.

### 3.4 La clique n'est pas nécessairement le goulot (MAJEURE)

Rien ne démontre que la transition (le processus lent) est le remplacement d'un membre de la clique. La lenteur pourrait venir de la diffusion dans un paysage d'énergie complexe, de réarrangements collectifs, ou de structures denses non cliquales. « Aristocratie » ≠ « clique ».

### Objections mineures retenues

- Le terme −βD **facilite** potentiellement le démantèlement de la clique (retirer une arête d'un sommet de haut degré diminue la dispersion). La mesure de barrier\_T\_over\_total = 0 % dans la campagne est suspecte et nécessite un diagnostic.
- Le chemin de transition Metropolis (échanges aléatoires sur tout le graphe) diffère du retrait ordonné supposé.

## 4. Verdict sur l'hypothèse

| Aspect | Statut | Étiquette |
|---|---|---|
| Dérivation algébrique, étapes 1–3 | Correcte | [CERT] |
| Barrière = somme (étape 4) | Contestée, probablement fausse | [H] |
| Relation γ = α − δ | Non soutenue par les données | [H] |
| Comportement Arrhenius de t½ | Contredit (loi de puissance meilleure) | [M] |
| Croissance de q\_max avec le refroidissement | Confirmée | [M] |
| Le terme D est négligeable | Non vérifié (mesure défaillante) | [OPEN] |

**[H] L'hypothèse γ = α − δ n'est pas réfutée en principe, mais elle est trop grossière pour être testable en l'état, et les données disponibles vont plutôt contre elle (forme fonctionnelle, facteur entre somme et max).** La dérivation identifie correctement les bons ingrédients (croissance de la structure dominante + refroidissement), mais le passage au quantitatif contient des erreurs structurelles. Reformulation nécessaire.

## 5. Ce qui est établi, ce qui reste à vérifier

**Établi [CERT] :**
- La dérivation algébrique des étapes 1–3 (facteur 6/(q(q−1)) ≈ 6/q²).
- La clique maximale croît comme N^0,40 ± 0,01 à degré moyen 4 (N = 17 à 129).

**Établi [M] :**
- La clique maximale est ≈ 3 à α = 0 et ≈ 6–12 à α = 1 : le refroidissement crée la structure.
- q\_eff sous-estime la clique d'un facteur 1,3 à 2,5 : ce n'est pas la bonne mesure de la structure dominante.
- t½ suit une loi de puissance N^3 (R² > 0,99), mieux qu'un Arrhenius.

**À vérifier :** la contribution séparée de T et D à la barrière (mesure défaillante à refaire) ; le temps de séjour dans un puits aristocratique (pas le t½) ; la nature exacte de la structure dominante (clique vs communauté dense) ; le diagramme de refroidissement complet ; le moteur canonique.

**Point le plus fragile :** tout repose sur 6 tailles, un seul secteur de densité, et une implémentation Python pure (pas de recoupement indépendant pour la mesure de clique).

## 6. Critères de réfutation (repris du protocole)

L'hypothèse γ = α − δ est réfutée ou doit être profondément révisée si :

- γ ne suit pas 1 − δ lorsque la densité change (**pas testable : la forme fonctionnelle n'est même pas Arrhenius sur les données actuelles**) ;
- faire varier α ne déplace pas γ selon α − δ (**diagramme de refroidissement incomplet**) ;
- le terme D domine la barrière ou en change l'exposant (**mesure à refaire**) ;
- aucune clique dominante ne porte la transition au degré moyen 6 (**à tester : la structure dominante pourrait ne pas être une clique**) ;
- la barrière dépend principalement de l'entropie des chemins (**non testé**) ;
- T\_v n'est pas une coordonnée de réaction suffisante (**non testé**) ;
- le moteur canonique ne présente pas ce mécanisme (**non testé**).

## 7. Prochain pas sur le chemin de preuve (P1)

**L'hypothèse γ = α − δ mérite un défi distinct (DEFI-M15), mais formulé comme une question ouverte, pas comme une confirmation.**

Trois pistes prioritaires :

1. **Mesurer le temps de séjour** (pas t½) dans un puits aristocratique, à plusieurs tailles et densités. Si le temps de séjour suit une loi de puissance (comme t½), la dérivation Arrhenius est inadéquate.
2. **Identifier la vraie barrière** : le max de |ΔS\_sim| le long du chemin de transition, pas la somme. Tracer le profil d'énergie libre le long d'une transition observée.
3. **Caractériser la structure dominante** : est-ce une clique, un quasi-clique, une communauté dense ? Quelle fraction de la masse triangulaire est portée par la clique maximale exacte vs le reste ?

## Reproduire

```bash
cd contributions/RO-25_pilote-ia
python3 defi_m15_verification_analytique.py  # vérification algébrique
python3 defi_m15_campagne.py                 # campagne structurelle (≈ 20 min)
```

Python 3.13, numpy, scipy. Les graines sont fixées (master\_seed = 20261031). Les résultats JSON sont dans `defi_m15_resultats.json`.

---

*Contribution de Codex (OpenAI), développée et vérifiée par le pilote IA Claude (Anthropic), sans relecture humaine.*

*TOE démontrée : NON ; candidate digne d'étude : OUI.*
