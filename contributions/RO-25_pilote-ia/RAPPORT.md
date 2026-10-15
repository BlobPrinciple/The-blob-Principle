🇫🇷 Français · 🇬🇧 [English version](REPORT_EN.md)

# RO-25 / RO-24 — Le pont croissance → Gibbs : ce que la mitose seule ne peut pas porter

*Contribution du pilote IA du laboratoire (Claude, Anthropic), 15 octobre 2026. Déposée comme toute contribution, en issue `ia-assistee`. Vérifiée par le pilote lui-même (calcul exact, plus recoupement par une seconde implémentation indépendante, `networkx`) ; **aucune relecture humaine à ce stade**.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Ce rapport ne change aucun statut épistémique. Il précise une recherche ouverte (RO-25) et réfute une option proposée pour une autre (RO-24).

## 1. La question

L'armature V347.1 (§ II.0) sépare trois strates : **A_gen** (croissance généalogique par mitose μ, N variable), **A_Gibbs** [ARCH] (à N et |E| fixés, mesure π_N ∝ exp(N·S_sim/τ), échanges d'arêtes de Metropolis), **B** (triangulations de T³). Le pont A_gen → A_Gibbs est la recherche ouverte **RO-25** :

> *Une dynamique jointe à N variable, combinant mitose/fermeture et relaxation, telle que la loi conditionnelle à N fixé reproduise, ou dérive, la mesure π_N d'A_Gibbs.*

Pour la fermeture (**RO-24**, § II.5), l'armature propose comme *« option la plus économique à tester »* d'**intercaler la dynamique d'arêtes déjà existante d'A_Gibbs entre les événements de croissance**, plutôt que d'inventer une troisième loi.

Ce rapport teste ces deux énoncés.

## 2. Cadre et hypothèse déclarée

- S_sim(C) = log(1 + n_tri(C)) − β·D(C), D = écart-type des degrés / degré moyen (A3) ; π_{N,M}(C) ∝ exp(N·S_sim(C)/τ) (A4) ; β = 0,30, τ = 0,50 (valeurs ARCHIVE / PRODUCTION).
- μ ajoute un sommet feuille et **une** arête (§ II.3, théorème 5.2-a) ; μ⁻¹ est le collapse d'une feuille (théorème 3.4).
- L'échange d'arêtes d'A_Gibbs retire une arête et en ajoute une : il conserve N et |E| = M (§ II.0 ; script historique, V346 p. 291–292 imprimées, p. 339–340 du PDF).
- **[H-abs]** Les calculs portent sur des graphes **abstraits** étiquetés, sans la contrainte géométrique Rips (réservoir d'arêtes à distance < 1,5 r) du moteur historique. Les énoncés [T] des § 3.1 et 3.2 n'en dépendent pas ; les mesures exactes des § 3.3 et 3.4 en dépendent.

## 3. Résultats

### 3.1 Invariant de densité [T]

**Proposition A.** Sous toute composition de μ, μ⁻¹ et d'échanges à |E| fixé, la quantité **M − N est conservée**.

*Preuve.* μ : (N, M) ↦ (N + 1, M + 1) ; μ⁻¹ : (N, M) ↦ (N − 1, M − 1) ; un échange : (N, M) ↦ (N, M). ∎

**Corollaire A1 [T].** Depuis Ω⁰ (N = 1, M = 0), toute trajectoire vérifie **M = N − 1** : le degré moyen vaut 2 − 2/N < 2 pour toujours. Le régime de production d'A_Gibbs, où le degré moyen est de l'ordre de κ₀ (5,5 à 8 dans les balayages ; 6,6 « canonique » ; V346 p. 148 imprimée, p. 196 du PDF), est **inaccessible** : la loi conditionnelle à N fixé de cette dynamique est portée par le secteur M = N − 1, disjoint de celui de π_N. L'écart en variation totale vaut 1 dès que le secteur de π_N a un nombre d'arêtes différent de N − 1, c'est-à-dire pour tout degré moyen cible supérieur à 2.

**Corollaire A2 [T].** Pour atteindre asymptotiquement un degré moyen κ̄, il faut créer en moyenne **κ̄/2 − 1 arêtes de plus que la mitose par sommet né** (2,3 pour κ̄ = 6,6). Ces arêtes ne peuvent venir ni de μ ni de l'échange : un générateur qui change M − N est **nécessaire**.

*Vérification numérique [M] :* 200 trajectoires aléatoires de 400 pas (μ, μ⁻¹, échanges ; graine 20261015, N jusqu'à 172) : 0 violation de M = N − 1.

### 3.2 Au secteur M = N − 1, la sélection fragmente [T] + [CERT]

**Lemme B [T].** Un graphe à N sommets et N − 1 arêtes a c = 1 + β₁ composantes connexes (β₁ : nombre cyclomatique). Un triangle impose β₁ ≥ 1, donc **c ≥ 2** ; un tétraèdre K₄ (β₁(K₄) = 3) impose **c ≥ 4**. ∎

Autrement dit, sur le seul secteur que l'option économique peut atteindre, **tout triangle déconnecte le graphe**. Or la mesure π_{N,N−1} récompense les triangles :

| N | graphes (M = N − 1) | π(au moins un triangle) | π(graphe connexe) | E_π[n_tri] |
|---|---|---|---|---|
| 4 | 20 | 0,9757 | 0,0243 | 0,98 |
| 5 | 210 | 0,99688 | 2,9·10⁻³ | 1,00 |
| 6 | 3 003 | 0,99990 | 7,7·10⁻⁵ | 1,84 |
| 7 | 54 264 | 0,9999993 | 4,5·10⁻⁷ | 3,73 |

[CERT] énumération complète ; aucune exception au lemme B parmi les 57 497 graphes. Recoupé indépendamment (`networkx`) pour N = 5 et 6 : mêmes probabilités à 10⁻¹⁵ près.

**Conséquence.** L'option « mitose + échanges d'A_Gibbs intercalés » ne produit pas la cascade dans un porteur connexe : elle produit, sous le poids de viabilité, des **îlots triangulaires disjoints**. C'est le contraire du récit (Livre I, ch. 5). L'option la plus économique proposée pour RO-24 est donc **réfutée** pour le moteur à |E| fixé. Cela ne réfute pas RO-24 : cela dit que la fermeture doit **créer des arêtes**.

### 3.3 Obstruction généalogique [T] + [CERT]

Appelons **généalogique** un noyau de croissance G qui fait naître un sommet sans recâbler aucune arête ancienne (le sous-graphe induit sur les anciens sommets est conservé). C'est ce qu'exige une généalogie au sens fort.

**Proposition C [T].** Pour tout noyau généalogique G et tout M′ :

TV(π_{N,M} G, π_{N+1,M′}) ≥ TV(π_{N,M}, R#π_{N+1,M′}) ≥ 1 − P_{π_{N+1,M′}}(deg(sommet nouveau) = M′ − M) > 0,

où R est la restriction aux N anciens sommets. *Preuve.* R est déterministe et R#(π_{N,M}G) = π_{N,M} ; la variation totale décroît sous une application mesurable ; la masse dont la restriction n'a pas M arêtes est hors du support de π_{N,M}. La dernière inégalité est stricte car π_{N+1,M′} charge des graphes où le degré du nouveau sommet diffère (support plein, 0 < M′ < N(N+1)/2, N ≥ 2). ∎

**Aucune croissance purement généalogique ne reproduit exactement π.** Bornes exactes, minimisées sur le nombre k d'arêtes du nouveau sommet :

| N → N + 1 | M → M′ (meilleur k) | borne inférieure de TV |
|---|---|---|
| 4 → 5 | 3 → 6 (k = 3) | 0,313 |
| 4 → 5 | 4 → 7 (k = 3) | 0,477 |
| 5 → 6 | 5 → 9 (k = 4) | 0,613 |
| 5 → 6 | 7 → 11 (k = 4) | 0,551 |
| 6 → 7 | 9 → 13 (k = 4) | 0,675 |

[CERT] ; le cas 4 → 5 est recoupé par `networkx` (0,31306).

### 3.4 Ce qui marche : croissance avec fermeture, puis relaxation [T] + [CERT]

Soit le noyau « mitose + fermeture » : le sommet naît relié à k anciens sommets distincts tirés uniformément (k = 1 : μ seule ; k ≥ 2 : k − 1 arêtes de fermeture), suivi de t échanges de Metropolis à |E| fixé (proposition uniforme, donc symétrique, acceptation min(1, π′/π)).

**[T] (résultat classique des chaînes de Markov réversibles finies, appliqué ici).** Le noyau d'échange laisse π_{N,M} invariante (proposition symétrique, acceptation de Metropolis). Sur les graphes abstraits, il est irréductible (deux ensembles de M arêtes se relient par au plus M échanges, chacun réduisant leur différence symétrique) et apériodique (rejets de probabilité positive dès que π n'est pas uniforme) ; la loi après t échanges converge donc vers π_{N,M} quelle que soit la loi de départ. Le pont « dérive » donc π_N **dans la limite de séparation des échelles de temps**, avec un coût fini à N fini.

Mesures exactes (propagation de la loi, sans échantillonnage) :

| N, M après naissance | k | états | TV à t = 0 | t pour TV ≤ 0,1 | ≤ 0,01 | ≤ 0,001 | échanges par arête (TV ≤ 0,01) |
|---|---|---|---|---|---|---|---|
| 5, 7 | 2 | 120 | 0,865 | 9 | 33 | 61 | 4,7 |
| 6, 11 | 3 | 1 365 | 0,787 | 9 | 27 | 50 | 2,5 |
| 7, 14 | 3 | 116 280 | 0,853 | 19 | 61 | 117 | 4,4 |

Contrôles : stochasticité et invariance de π vérifiées à 10⁻¹⁴ près.

**Le prix [T, d'après la proposition C].** Cette convergence passe par le recâblage d'arêtes anciennes : la généalogie des **sommets** survit, celle des **arêtes** est effacée par la relaxation. Il faut choisir entre une généalogie stricte des arêtes et la mesure exacte π_N ; on ne peut pas avoir les deux.

## 4. Effet proposé sur le programme (aucun changement de statut)

- **RO-24 :** l'option « intercaler les échanges d'A_Gibbs » est réfutée pour le moteur à |E| fixé (§ 3.1–3.2). Toute fermeture viable doit créer des arêtes, au rythme d'environ κ̄/2 − 1 par naissance.
- **RO-25 :** « reproduire » exactement π_N par une croissance généalogique est impossible (§ 3.3) ; « dériver » π_N par croissance-avec-fermeture puis relaxation est possible à N fini (§ 3.4), au prix de la généalogie des arêtes. La recherche reste **ouverte** : le coût de relaxation quand N grandit n'est pas connu (les trois points mesurés ne dégagent aucune loi).

## 5. Ce qui est établi, ce qui reste à vérifier, le point le plus fragile

- **Établi :** propositions A, C et lemme B (preuves élémentaires ci-dessus) ; valeurs exactes des § 3.2–3.4 sur graphes abstraits.
- **À vérifier :** tout, par une personne ; la transposition au moteur Rips géométrique (hypothèse H-abs), où le réservoir d'arêtes est restreint ; le comportement du coût de relaxation au-delà de N = 7.
- **Point le plus fragile :** l'hypothèse H-abs. Le corpus mesure aussi une croissance « par paliers » (V346 p. 209 imprimée, p. 257 du PDF, `etape4_mitose_paliers.py`, nœud N3) où chaque nouveau sommet s'attache à une structure existante et qui produit des tétraèdres dans un espace connexe : ce modèle comporte déjà, de fait, une règle de fermeture à plusieurs arêtes, ce qui est cohérent avec le corollaire A2 mais n'a pas été rejoué ici.

## 6. Prochain pas sur le chemin de preuve (P1)

1. **DEFI-M7** — le coût du pont : le nombre d'échanges par arête nécessaire après une naissance reste-t-il borné quand N grandit, sur le moteur Rips ?
2. **DEFI-M8** — une fermeture non arbitraire : dériver de S_sim la loi d'attachement du nouveau sommet (k et cibles) qui minimise l'écart à π dès la naissance, plutôt que de la poser.

## Reproduire

```bash
python3 contributions/RO-25_pilote-ia/pont_croissance_gibbs.py            # 1 à 3 min, écrit resultats.json
python3 contributions/RO-25_pilote-ia/pont_croissance_gibbs.py --rapide   # sans le cas N = 7 de la partie D
```

Python 3.13, numpy 2.5.3, scipy 1.18.1. Empreintes SHA-256 : voir `EMPREINTES_SHA256.txt` à la racine du dépôt.
