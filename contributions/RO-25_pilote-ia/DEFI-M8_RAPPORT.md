🇫🇷 Français · 🇬🇧 [English version](DEFI-M8_REPORT_EN.md)

# DEFI-M8 — La loi d'attachement dérivée de S_sim : ici, bien naître ne fait pas un bon pont

*Contribution du pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026. Déposée comme toute contribution, en issue `ia-assistee`. Vérifiée par le pilote (énumération exacte, recoupée par une seconde implémentation indépendante) et relue par un second agent IA en relecteur hostile (trois corrections retenues, voir § 5) ; **aucune relecture humaine à ce stade**.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Ce rapport ne change aucun statut épistémique. Il répond partiellement à DEFI-M8 (RO-24, RO-25), sur graphes abstraits et pour au plus 7 sommets.

## 1. La question

DEFI-M8 (docs/defis.json) demande de dériver de S_sim, sans la poser, la loi d'attachement d'un sommet nouveau-né (nombre d'arêtes et cibles) qui minimise l'écart à π dès la naissance, et de la comparer à l'attachement uniforme ; ou de prouver qu'aucune loi locale ne fait mieux que l'uniforme.

Sources qui font foi : armature V347.1, § II.0 (strates A_gen, A_Gibbs, B, p. 10) ; encadré RO-25 (p. 11 : « une dynamique jointe à N variable […] telle que la loi conditionnelle à N fixé reproduise, ou dérive, la mesure π_N », falsificateur : « aucune extension markovienne locale ne possède simultanément la généalogie voulue, la mesure conditionnelle annoncée et une règle de fermeture non arbitraire ») ; encadré RO-24 (§ II.5, p. 15) ; axiomes A3–A4 (p. 18) : S_sim(C) = log(1 + n_tri(C)) − β·D(C), β = 0,30 ; π_N ∝ exp(N·S_sim/τ), τ = 0,50 ; théorème 4.7-b (p. 13) : τ·KL(ν‖π_N) est une fonctionnelle de Lyapunov. Point de départ : [RAPPORT.md](RAPPORT.md), proposition C (§ 3.3) et mesures du § 3.4.

## 2. Cadre

- **[H-abs]** comme dans RAPPORT.md : graphes simples étiquetés **abstraits**, sans la contrainte Rips du moteur historique ; D = écart-type de population des degrés / degré moyen.
- Le sommet nouveau-né v (étiquette N) naît relié à un ensemble A de k anciens sommets : passage du secteur (N, M) au secteur (N + 1, M + k). k = 1 est la mitose seule ; k ≥ 2 ajoute k − 1 arêtes de fermeture.
- Un noyau est **généalogique** s'il ne recâble aucune arête ancienne (RAPPORT.md § 3.3). On note π = π_{N,M}, π′ = π_{N+1,M+k}, R la restriction aux N anciens sommets, B_k(C) = Σ_{|A|=k} π′(C + v_A).
- **Attachement uniforme U** : A uniforme parmi les C(N, k) parties.
- **Attachement de Gibbs G\*** (bain thermique sur le voisinage du nouveau-né) : G\*(A | C) = π′(C + v_A) / B_k(C). Il ne contient aucun paramètre nouveau : c'est la loi conditionnelle de π′ sachant l'ancien graphe et le degré k du nouveau-né.

## 3. Résultats

### 3.1 G\* est la meilleure loi généalogique possible [T]

**Proposition D.** Pour tout k et tout noyau généalogique G attachant le nouveau-né à k anciens sommets (G(· | C) quelconque, local ou non) :

1. TV(πG, π′) ≥ TV(π, R#π′), avec égalité si et seulement si, pour tout C, les quantités π(C)·G(A | C) − π′(C + v_A) ont le même signe pour toutes les parties A (au sens large) ;
2. **G\* atteint l'égalité** : la borne de la proposition C (RAPPORT.md § 3.3, première inégalité) est **exacte** ;
3. KL(πG ‖ π′) = Σ_C π(C)·log(π(C)/B_k(C)) + Σ_C π(C)·KL(G(· | C) ‖ G\*(· | C)) ; G\* est donc l'**unique** minimiseur de la divergence de Kullback-Leibler à la naissance.

*Preuve.* (1) Les états de π′ où deg(v) ≠ k reçoivent une masse nulle et contribuent 1 − P_{π′}(deg v = k), soit exactement la masse de R#π′ hors du secteur à M arêtes. Pour C fixé, avec a = π(C) et b_A = π′(C + v_A), l'inégalité triangulaire donne Σ_A |a·g_A − b_A| ≥ |a − B_k(C)|, avec égalité si et seulement si les termes ont un signe commun. La somme sur C donne 2·TV(π, R#π′). (2) Pour g = b/B_k(C), a·g_A − b_A = b_A·(a/B_k(C) − 1) : signe commun. (3) Développement direct ; le second terme est positif et nul si et seulement si G(· | C) = G\*(· | C) pour tout C (π charge tous les états). ∎

**Corollaire D1 [T].** L'attachement uniforme est déjà optimal en variation totale dès que, pour chaque C, π(C)/C(N, k) est soit au-dessus, soit au-dessous de toutes les valeurs π′(C + v_A). Dans ce cas, **aucune loi d'attachement ne fait mieux que l'uniforme à la naissance** : tout l'écart vient de la loi de l'ancien graphe, qu'aucun noyau généalogique ne touche.

**Proposition E (anatomie de G\*) [T].** Notons T(C) le nombre de triangles, d_u les degrés, Q(C) = Σ_u d_u², e_C(A) le nombre d'arêtes entre les cibles et s_A = Σ_{a∈A} d_a. Alors

G\*(A | C) ∝ exp( (N + 1)/τ · [ log(1 + T(C) + e_C(A)) − β·D_A ] ),  D_A = √(Q_A/(N + 1) − μ²) / μ,

avec μ = 2(M + k)/(N + 1) et Q_A = Q(C) + 2·s_A + k + k². À C fixé, le poids d'une partie A ne varie avec A qu'à travers **deux statistiques locales**, e_C(A) et s_A (T(C), Q(C), M et N y entrent comme constantes globales) ; il croît avec e_C(A) (chaque arête entre cibles ferme un triangle) et décroît avec s_A (des cibles de fort degré accroissent la dispersion D). G\* est donc une **fermeture triadique anti-préférentielle**, dérivée de S_sim et non posée ; son exposant (N + 1)/τ croît avec N. *Preuve.* Le nouveau-né crée exactement e_C(A) triangles ; les degrés deviennent d_a + 1 sur A et k en v, d'où Q_A ; T(C), Q(C) et M sont fixés par C. ∎

La normalisation B_k(C) somme sur les C(N, k) parties : la loi n'est pas locale au sens strict, mais ses poids le sont.

### 3.2 Ce que G\* gagne à la naissance [CERT]

Énumération exacte de tous les graphes des secteurs concernés (39 passages : N = 4, 5, 6, quatre à six valeurs de k par secteur de départ ; jusqu'à 352 716 états après naissance).

- G\* atteint la borne de la proposition C dans les 39 cas (écart ≤ 2·10⁻¹⁶) ; sa KL est inférieure ou égale à celle de U dans les 39 cas.
- La condition du corollaire D1 est vérifiée exactement dans **25 cas sur 39** (les 16 cas k = 1 ou k = N, et 9 des 23 cas intermédiaires) : G\* n'y gagne rien sur U. Dans un 26ᵉ cas (N = 6, M = 9, k = 2), le gain est de 3·10⁻¹².
- Au meilleur k de chaque secteur de départ (les secteurs 4, 5 et 5, 8, où le meilleur k vaut N et où G\* et U coïncident, sont omis) :

| N, M → M′ (meilleur k) | TV à la naissance, U | TV à la naissance, G\* (= borne) | gain |
|---|---|---|---|
| 4, 3 → 6 (k = 3) | 0,723 | 0,313 | 0,410 |
| 4, 4 → 7 (k = 3) | 0,632 | 0,477 | 0,155 |
| 5, 5 → 9 (k = 4) | 0,744 | 0,613 | 0,131 |
| 5, 7 → 11 (k = 4) | 0,608 | 0,551 | 0,057 |
| 6, 9 → 13 (k = 4) | 0,744 | 0,675 | 0,069 |
| 6, 11 → 16 (k = 5) | 0,614 | 0,606 | 0,008 |

- Pour 2 ≤ k < N, sous G\*, le nouveau-né s'attache à une clique (toutes ses cibles reliées entre elles) avec une probabilité de 0,15 à 0,99 selon le cas (0,04 à 0,83 sous U), sauf dans les cas (N, M, k) = (5, 5, 4) et (6, 9, 5), où aucune clique de cette taille n'existe dans le secteur de départ.

### 3.3 Mais, ici, la meilleure naissance ralentit le pont [CERT]

Après la naissance, t échanges de Metropolis à |E| fixé (proposition uniforme, acceptation min(1, π′/π)) ; propagation exacte de la loi. Nombre d'échanges pour TV ≤ 0,01 :

| N, M, k | états | U | G\* | premier t où TV(G\*) > TV(U) | premier t où KL(G\*) > KL(U) |
|---|---|---|---|---|---|
| 4, 5, 2 | 120 | 33 | 33 | 8 | 7 |
| 5, 8, 3 | 1 365 | 27 | 26 | jamais | jamais |
| 6, 11, 3 | 116 280 | 61 | 57 | jamais | (non calculé) |
| 4, 3, 3 | 210 | 268 | **387** | 23 | 19 |
| 4, 4, 3 | 120 | 27 | **35** | 3 | 3 |
| 5, 5, 4 | 5 005 | 130 | **163** | 8 | 8 |
| 5, 7, 4 | 1 365 | 26 | **34** | 1 | 2 |
| 6, 9, 4 | 203 490 | 82 | **103** | 6 | (non calculé) |

Dans les **cinq cas** où G\* gagne à la naissance, il **ralentit** la relaxation de 25 à 44 % (t(G\*)/t(U) − 1) : sa courbe passe au-dessus de celle de U après 1 à 23 échanges en variation totale, et, dans les quatre cas où le calcul a été fait, aussi en KL, la fonctionnelle de Lyapunov du théorème 4.7-b. La colonne KL provient de la seule seconde implémentation. Les trois cas où G\* relaxe aussi vite ou un peu plus vite (de 0 à 7 %) sont ceux où il ne gagne rien à la naissance.

**Famille tempérée.** G_θ(A | C) ∝ π′(C + v_A)^θ relie l'attachement anti-Gibbs (θ < 0 : par la proposition E, il évite de fermer des triangles et préfère les cibles de fort degré), U (θ = 0) et G\* (θ = 1). Échanges pour TV ≤ 0,01 :

| N, M, k | θ = −0,5 | −0,25 | 0 | 0,25 | 0,5 | 0,75 | 1 |
|---|---|---|---|---|---|---|---|
| 4, 3, 3 | **190** | 218 | 268 | 325 | 363 | 381 | 387 |
| 4, 4, 3 | **21** | 24 | 27 | 30 | 32 | 34 | 35 |
| 5, 5, 4 | **114** | 120 | 130 | 142 | 153 | 159 | 163 |
| 5, 7, 4 | 25 | **24** | 26 | 28 | 31 | 33 | 34 |
| 6, 9, 4 | **68** | 74 | 82 | 90 | 96 | 100 | 103 |
| 6, 11, 3 | 63 | 62 | 61 | 60 | 59 | 58 | **57** |

Dans cinq cas sur six, **l'attachement anti-Gibbs relaxe le plus vite** (jusqu'à 29 % d'échanges en moins que U et 51 % de moins que G\*, soit 1 − t(θ)/t(référence)), alors qu'il est le pire à la naissance (TV 0,945 contre 0,313 pour G\* au cas 4, 3, 3). Le cas 6, 11, 3 va en sens inverse.

### 3.4 Recoupement indépendant

Seconde implémentation sans code commun (`defi_m8_second_moteur.py` : graphes en ensembles d'arêtes, triangles et degrés par `networkx`, noyau construit par énumération ensembliste, matrices denses) sur les 27 passages et les 6 relaxations à au plus 6 sommets après naissance, et sur les 4 cas tempérés correspondants : écart maximal 1,3·10⁻¹⁵ sur les TV, bornes et KL ; mêmes nombres d'échanges et mêmes instants de croisement en variation totale. Les cas à 7 sommets (6, 9, 4 et 6, 11, 3) ne sont calculés que par la première implémentation. Contrôles : stochasticité et invariance de π′ à 4·10⁻¹⁵ près.

## 4. Lecture

- **[T]** Le livrable de DEFI-M8 est fourni **pour les cibles, à k fixé**, sur graphes abstraits : la loi des cibles qui minimise l'écart à π dès la naissance existe, est unique au sens de KL, ne contient aucun paramètre nouveau (bain thermique de S_sim) et a une forme lisible (fermeture triadique anti-préférentielle). À k fixé, aucune loi généalogique, locale ou non, ne fait mieux ; la borne de la proposition C est atteinte. Le nombre k n'est pas dérivé de S_sim : il est fixé par le secteur d'arrivée (M′ = M + k), et comparer les k revient à comparer des cibles π_{N+1,M+k} différentes.
- **[CERT]** Son gain est souvent nul ; au meilleur k, il va de 0 (secteurs 4, 5 et 5, 8) à 0,41 (secteur 4, 3), et ne dépasse pas 0,07 aux deux secteurs N = 6 ; trois tailles ne suffisent pas à établir une tendance en N. L'essentiel de l'écart à la naissance ne vient pas de l'attachement mais de la loi de l'ancien graphe : R#π_{N+1} n'est pas π_N.
- **[CERT], contre l'intuition** : dans les cas calculés, minimiser l'écart à la naissance n'est pas le bon critère du pont. Dans cinq cas sur six de la famille tempérée, le noyau le plus fidèle à la naissance est le plus lent à rejoindre π′, et le noyau anti-Gibbs (qui évite les triangles et préfère les forts degrés) est le plus rapide.
- **[H]** Explication non testée : G\* enfonce le nouveau-né dans une clique, configuration de poids élevé que l'échange d'arêtes met longtemps à défaire, alors que l'écart restant porte sur l'ancien graphe ; une naissance plus « neutre » laisse la chaîne corriger d'abord ce qui compte.
- Pour le récit (Livre I, cascade de fermetures) et pour RO-24 : la fermeture dérivée de S_sim ferme bien des triangles et des cliques à la naissance. Pour RO-25 : cette fidélité se paie en temps de relaxation dans la plupart des cas calculés ; le falsificateur de RO-25 n'est ni déclenché ni écarté par ces calculs : la proposition C n'exclut que la reproduction exacte de π par une généalogie stricte, RO-25 admet aussi de « dériver » π_N (ce que la relaxation fait, au prix du recâblage), et « la généalogie voulue » n'est pas définie dans l'armature.

## 5. Ce qui est établi, ce qui reste à vérifier, le point le plus fragile

- **Établi :** propositions D et E et corollaire D1 (preuves ci-dessus) ; valeurs exactes des § 3.2–3.3 sur graphes abstraits, pour N + 1 ≤ 7.
- **À vérifier :** tout, par une personne ; la tendance du gain avec N (trois tailles seulement) ; l'hypothèse H-abs (sur le moteur Rips, les cibles sont restreintes aux voisins géométriques, ce qui change B_k(C)) ; d'autres seuils que ε = 0,01.
- **Relecture hostile (second agent IA) :** décompte du corollaire D1 corrigé (25 cas, non 26), phrase sur les cliques corrigée, livrable restreint aux cibles à k fixé ; les preuves, tableaux et citations ont été rejoués et confirmés, dont un troisième contrôle indépendant sur les cas (4, 3, 3) et (4, 4, 3).
- **Point le plus fragile :** la portée du résultat de relaxation. Huit cas, huit secteurs, N ≤ 6 avant naissance, un seul noyau d'échange ; le cas 6, 11, 3 (le plus dense des deux cas à 7 sommets) va en sens inverse. Rien ne dit que l'ordre « anti-Gibbs < uniforme < Gibbs » persiste quand N grandit.

## 6. Prochain pas sur le chemin de preuve (P1)

**DEFI-M11 — Naître juste ou relaxer vite.** Quelle loi d'attachement minimise le coût total du pont (échanges jusqu'à TV ≤ ε après naissance), et est-elle dérivable de S_sim ? L'ordre anti-Gibbs < uniforme < Gibbs survit-il au-delà de N = 6, et sur le moteur canonique à N ≥ 250 ?

## Reproduire

```bash
python3 contributions/RO-25_pilote-ia/defi_m8_attachement_gibbs.py   # ≈ 30 s, écrit defi_m8_resultats.json
python3 contributions/RO-25_pilote-ia/defi_m8_tempere.py             # ≈ 40 s, écrit defi_m8_tempere.json
python3 contributions/RO-25_pilote-ia/defi_m8_second_moteur.py       # ≈ 6 s, recoupement
python3 contributions/RO-25_pilote-ia/defi_m8_second_moteur.py --tempere
```

Python 3, numpy 2.5.3, scipy 1.18.1, networkx 3.7. Sorties écran : `defi_m8_sortie.txt`, `defi_m8_second_moteur_sortie.txt`, `defi_m8_tempere_sortie.txt`. Empreintes SHA-256 : `EMPREINTES_SHA256.txt` à la racine du dépôt.
