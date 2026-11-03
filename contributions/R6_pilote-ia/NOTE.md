🇫🇷 Français · 🇬🇧 [English version](NOTE_EN.md)

# DEFI-R6 — La toile sans viabilité : ce qui revient à la nucléation, à la mobilité et à la viabilité

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Note du pilote IA du laboratoire (Claude, Anthropic), session planifiée du 3 novembre 2026, par délégation de Rudolphe Mirante. Non relue par une personne.

## Objet

Le master V346 (XXV.2, p. 644–645 ; PDF 692–693) dit la structuration « nœuds + vides » de la toile cosmique simulée « propre à la viabilité », avec un rapport P_max/médiane qui « croît avec N » (≈ 630 à N = 5 000, ≈ 1 900 à N = 20 000) et des vides « croissants avec N et propres à la viabilité ». La note de DEFI-R5 (`contributions/R5_pilote-ia/NOTE.md`, E4) a montré que le témoin « mobilité sans viabilité » du fichier archivé reproduit l'essentiel de l'effet. DEFI-R6 demande ce qui, dans la toile, revient à la nucléation multi-sites, à la mobilité et à la viabilité.

Sources : `corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob_toile_results.json` (le fichier archivé, 4 bras, N = 1 000 à 20 000, 3 à 8 graines) ; `blob gravite colab.py` du même dossier (le moteur « à mobilité des positions » du 25 mai : `relax_positions`, `local_S`, κ = 6,6, β = 0,30, τ = 0,50 ; V346 XXV.1 p. 642). Le script producteur de la toile **manque au corpus** (NOTE R5, E4).

## Résultat en bref

1. **[T] + [M], fichier archivé.** La croissance de P_max/médiane avec N est la loi d'échelle cinématique d'une modulation de densité de forme fixe, pas une structure qui croît : l'amplitude relative P_max/N² est constante de N = 1 000 à 20 000 (pente log-log 0,01 ± 0,04 au Blob multi-sites, 0,04 ± 0,04 sans viabilité), et la médiane reste au bruit de grenaille (médiane/N ≈ 1,0 à 1,1 jusqu'à N = 15 000). Le fichier contient en revanche un signal propre à la viabilité, à petite échelle : de la puissance à k intermédiaire (k ≈ 6 à 12), absente ou bien plus faible sans viabilité, qui fait monter la médiane à N = 20 000.
2. **[M], campagne reconstruite à quatre bras (germes reconstruits, moteur archivé, 8 configurations de germes, N = 1 000 à 20 000).** À 5 et 20 balayages, la nucléation porte 89 à 99 % de l'amplitude à grande échelle ; [H] si l'archive avait une durée de cet ordre (ce qu'on ne peut établir sans son script), il en irait de même pour elle ; la mobilité sans viabilité l'érode (au plus 1 graine sur 8 en hausse, à toutes les tailles et durées) ; la viabilité l'accroît et creuse les vides (8 graines sur 8 partout). La part de la viabilité croît avec la durée : à N = 2 500, la nucléation ne porte plus que 70 % de l'amplitude à 80 balayages.
3. **[M], viabilité seule.** Depuis un départ uniforme, la viabilité seule crée des vides (+0,025 à 20 balayages, +0,074 à 80, +0,128 à 320, N = 2 500 ; +0,156 à 80 balayages, N = 5 000) et un pic de P(k) à k = 3 à 5, soit une longueur d'environ 3 fois le rayon de connexion r_N : une échelle du modèle, pas une échelle cosmique ; la mobilité sans viabilité ne fait rien de tel. L'amplitude atteinte (P_max/N² ≤ 0,011) reste au moins 14 fois plus faible que celle des germes.

**Verdict.** « Propre à la viabilité » ne tient pas pour le chiffre P_max/médiane du master : dans le fichier, cet effet (le mode k = 1 ou 2) est déjà présent sans viabilité, et dans la reconstruction il est posé par la nucléation. La viabilité a, elle, une action propre et mesurable, à petite échelle : elle condense et creuse des vides, y compris sans germes, cette action croît avec la durée de la dynamique, et on la voit aussi dans le fichier archivé (puissance à k intermédiaire). Cette condensation est en partie inscrite dans la règle locale du moteur (ln(1 + triangles) du seul sommet déplacé récompense la densité locale). « L'excès croît avec N » n'est pas un indice de structuration croissante. Aucun changement de statut.

## A. Relecture du fichier archivé

**Identité [T].** Pour N points tirés indépendamment selon une densité ρ sur [0,1]³ et A(k) = Σ_j exp(2πi k·x_j),

E |A(k)|² = Σ_j Σ_l E exp(2πi k·(x_j − x_l)) = N + N(N − 1) |ρ̂(k)|².

Preuve : les N termes diagonaux valent 1 ; les N(N − 1) termes croisés factorisent par indépendance en ρ̂(k)·ρ̂(k)* (avec affectation des points aux cellules de la grille, ρ̂ est celle de la loi des cellules ; l'identité est inchangée). Donc, pour une forme de densité qui ne dépend pas de N, P_max/médiane ≈ [1 + (N − 1)|ρ̂(k_max)|²] / [1 + (N − 1)|ρ̂(k_méd)|²] croît linéairement en N tant que la médiane reste au bruit de grenaille. Les configurations du Blob ne sont pas faites de tirages indépendants : l'identité est la référence, la constance mesurée ci-dessous est le fait.

**Mesure [M]** (`r6_archive.py`, sortie `r6_archive_sortie.txt`) :

| N | graines | P_max/médiane, multi-sites | P_max/N², multi-sites | P_max/N², sans viabilité | P_max/N², site unique | médiane/N, multi-sites |
|---|---|---|---|---|---|---|
| 1 000 | 8 | 131 ± 11 | 0,133 ± 0,011 | 0,117 ± 0,010 | 0,165 ± 0,002 | 1,02 |
| 2 500 | 8 | 335 ± 26 | 0,137 ± 0,011 | 0,126 ± 0,011 | 0,157 ± 0,002 | 1,02 |
| 5 000 | 6 | 662 ± 73 | 0,138 ± 0,015 | 0,129 ± 0,015 | 0,153 ± 0,001 | 1,04 |
| 10 000 | 5 | 1 329 ± 180 | 0,141 ± 0,018 | 0,134 ± 0,018 | 0,152 ± 0,001 | 1,06 |
| 15 000 | 4 | 2 032 ± 279 | 0,148 ± 0,021 | 0,141 ± 0,021 | 0,149 ± 0,001 | 1,09 |
| 20 000 | 3 | 2 060 ± 242 | 0,129 ± 0,015 | 0,124 ± 0,017 | 0,149 ± 0,001 | 1,26 |

(erreurs-types sur les graines). Pentes log-log sur toutes les graines : P_max/médiane 0,972 ± 0,039 (multi-sites), 1,039 ± 0,042 (sans viabilité), 0,926 ± 0,008 (site unique) ; P_max/N² 0,014 ± 0,037, 0,044 ± 0,042, −0,033 ± 0,004. Le pic est à k = 1 ou 2 (la plus grande échelle de la boîte) dans toutes les graines.

Conséquences pour XXV.2 :
- « L'excès croît avec N (≈ 630 à N = 5 000 → 1 900 à N = 20 000) » : c'est la normalisation par le bruit de grenaille. L'amplitude relative de la structure ne croît pas. [M]
- Le fléchissement à N = 20 000 vient de la médiane : sur les mêmes graines 0 à 2, on attendrait ≈ 2 410 par proportionnalité depuis N = 15 000 ; l'amplitude est la même (0,1295 contre 0,1294) et la médiane passe de 1,08·N à 1,26·N. Cette hausse n'existe qu'avec viabilité (multi-sites 1,26 ; site unique 1,25 ; témoin sans viabilité 1,02). [M]
- Signal propre à la viabilité (`r6_archive.py`, P(k)/N moyen) : à k = 10, 2,0 / 4,9 / 9,1 (multi-sites, N = 5 000 / 10 000 / 20 000) contre 1,0 / 1,2 / 1,8 sans viabilité ; à k = 8, 9,0 / 21 / 46 contre 2,2 / 4,7 / 13. Au site unique, une bosse se déplace vers les grands k quand N croît (parmi k = 6, 8, 10, 12, 15, maximum de P/N à k = 6 à N = 5 000 et à k = 10 à N = 20 000), à peu près comme 1/(2,9·r_N) (5,1 ; 8,0). [M] pour les valeurs ; [H] pour le lien avec l'échelle r_N, vue aussi en partie C.
- Estimateur : ce tableau prend la moyenne des rapports par graine (662 à N = 5 000 ; 2 060 à N = 20 000) ; le master et la note R5 prennent le rapport du spectre moyen (635 ; 1 879). [M]
- Les vides « résistent au remplissage » : pour une forme de densité fixe, la fraction de cellules vides décroît avec N de toute façon, d'autant plus lentement que la densité est concentrée ; le témoin sans viabilité décroît presque pareil (0,921 → 0,743). [M]
- Appariement par graine (mêmes clés de graine dans le fichier) : la viabilité ajoute à P_max/N² +0,016 ± 0,002 à N = 1 000, puis +0,011, +0,009, +0,007, +0,006, +0,005 ± 0,002 à N = 20 000, toutes les paires positives ; aux vides, +0,015 à +0,027 (toutes les paires positives, comme en E4). [M] Que les deux bras partagent la configuration initiale est une hypothèse : le script manque.

## B. Campagne reconstruite à quatre bras

**Protocole (reconstruit, déclaré comme tel).** Le script producteur manque ; le protocole suit V346 XXV.2 (« K = 8 germes d'âges variés », « positions mobiles sous Metropolis de viabilité ») et les conventions déduites du fichier archivé :
- mesures (`r6_mesures.py`) : vides = fraction des 20³ = 8 000 cellules vides (le Poisson archivé suit exp(−N/8 000) : 0,883 à N = 1 000, 0,083 à N = 20 000) ; P(k) = |FFT|² des comptes sur grille 64³, moyenne par coquille round(|k|) = 1 à 31 (le Poisson archivé vaut ≈ N à tout k) ; mon bras Poisson redonne 0,882 et médiane/N = 1,00 ;
- germes : 8 centres uniformes, âges a ~ U(0,2 ; 1), effectifs ∝ a³, nuages gaussiens d'écart-type 0,12·a, ramenés dans [0,1]³ par `np.clip` comme le moteur ; l'écart-type 0,12 a été choisi parce qu'il donne, figé, des vides proches de ceux du fichier à N = 1 000 (0,929 contre 0,921–0,937) ; le rognage place 24 % des points initiaux exactement sur une face (10 à 42 % selon la configuration, N = 2 500), nappes artificielles qui pèsent sur k = 1 et sur les vides ; le degré initial des germes (49 à 85) est loin de κ = 6,6 ;
- dynamique : `relax_positions` et `local_S` **importés tels quels** du fichier `blob gravite colab.py`, sur le graphe géométrique de rayon `rgg_radius(N, 6,6)` ; `sweeps` × ⌊N/4⌋ propositions ;
- bras appariés par graine (même configuration initiale) : **figé** (aucune dynamique), **mobile** (`viab=False`), **viab** (`viab=True`), **poisson** (uniforme figé) ;
- 8 configurations de germes (les mêmes à toutes les tailles N : « 8/8 » ne représente que 8 réalisations) ; N = 1 000, 2 500, 5 000, 10 000, 20 000 à 5 balayages ; 20 balayages à N = 2 500 et 5 000 ; 80 balayages à N = 2 500.

**Résultats [M]** (`r6_campagne.py`, `r6_analyse.py`, sortie `r6_analyse_sortie.txt`). Amplitude A = P_max/N² ; différences appariées, moyenne ± erreur-type, nombre de graines sur 8 où la différence est positive :

| N | balayages | A figé | A mobile | A viab | part de la nucléation | ΔA mobilité | ΔA viabilité | Δvides mobilité | Δvides viabilité |
|---|---|---|---|---|---|---|---|---|---|
| 1 000 | 5 | 0,150 | 0,146 | 0,156 | 0,96 | −0,0041 ± 0,0007 (0/8) | +0,0098 ± 0,0013 (8/8) | −0,0028 (0/8) | +0,0050 (8/8) |
| 2 500 | 5 | 0,149 | 0,147 | 0,153 | 0,97 | −0,0022 ± 0,0003 (0/8) | +0,0065 ± 0,0010 (8/8) | −0,0049 (0/8) | +0,0101 (8/8) |
| 5 000 | 5 | 0,150 | 0,149 | 0,154 | 0,98 | −0,0016 ± 0,0003 (0/8) | +0,0051 ± 0,0008 (8/8) | −0,0050 (0/8) | +0,0112 (8/8) |
| 10 000 | 5 | 0,151 | 0,150 | 0,153 | 0,99 | −0,0007 ± 0,0002 (1/8) | +0,0030 ± 0,0005 (8/8) | −0,0041 (0/8) | +0,0100 (8/8) |
| 20 000 | 5 | 0,151 | 0,150 | 0,152 | 0,99 | −0,0005 ± 0,0001 (1/8) | +0,0021 ± 0,0003 (8/8) | −0,0037 (0/8) | +0,0063 (8/8) |
| 2 500 | 20 | 0,149 | 0,140 | 0,167 | 0,89 | −0,0085 ± 0,0013 (0/8) | +0,026 ± 0,004 (8/8) | −0,017 (0/8) | +0,036 (8/8) |
| 5 000 | 20 | 0,150 | 0,144 | 0,163 | 0,92 | −0,0059 ± 0,0011 (0/8) | +0,019 ± 0,003 (8/8) | −0,017 (0/8) | +0,040 (8/8) |
| 2 500 | 80 | 0,149 | 0,118 | 0,210 | 0,70 | −0,031 ± 0,005 (0/8) | +0,092 ± 0,010 (8/8) | −0,047 (0/8) | +0,106 (8/8) |

« Part de la nucléation » = moyenne par graine de (A figé − A poisson)/(A viab − A poisson). « Viabilité » = viab − mobile, c'est-à-dire la comparaison que le fichier archivé permet ; viab − figé est aussi positif partout (8/8, sauf 7/8 aux vides à N = 1 000).

Lecture :
- La nucléation pose la structure à grande échelle ; à 5 balayages, la dynamique la modifie de moins de 4 % (1,6 % au plus à N ≥ 10 000, où le déplacement moyen d'un sommet n'est que 0,010 à 0,017). [M] Cette « part » mesure surtout le peu de dynamique écoulée : elle n'est pas une part causale, et elle ignore le terme de mobilité, négatif.
- La mobilité sans viabilité diffuse : elle érode l'amplitude (au plus 1 graine sur 8 en hausse) et remplit les vides (0 graine sur 8 en hausse), à toutes les tailles et durées. [M]
- La viabilité accentue : elle accroît l'amplitude et les vides, dans toutes les graines. Son effet croît avec la durée (×3 à ×4 de 5 à 20 balayages, ×14 de 5 à 80 balayages à N = 2 500 pour l'amplitude). [M]
- L'excès de vides du fichier archivé sur son témoin (+0,024 à N = 2 500 ; +0,027 à N = 5 000) se situe ici entre 5 et 20 balayages (+0,010 → +0,036 ; +0,011 → +0,040). [M] Si l'archive avait une durée de ce même ordre (ce qui n'est pas établi, le calage dépendant de s, du modèle de germes et du moteur), sa structure à grande échelle serait portée à 89 % au moins par la nucléation. [H]
- Les bras ne bougent pas autant : 55 à 61 % des sommets déplacés en viab contre 46 % en mobile à 5 balayages (relecture). [M]
- Bords : le moteur rogne les pas à [0,1] (boîte non périodique). Le contrôle n'a été fait que depuis un départ uniforme (partie C) ; pour les germes, il manque. [OPEN]

## C. La viabilité seule, sans germes

Même dynamique, configuration initiale uniforme (`--init poisson`) :

| N | balayages | vides figé | vides mobile | vides viab | A viab (A figé) | P_max/médiane viab | k du pic, viab (8 graines) |
|---|---|---|---|---|---|---|---|
| 2 500 | 20 | 0,733 | 0,732 | 0,757 | 0,0013 (0,0005) | 3,2 | 4–5 |
| 2 500 | 80 | 0,733 | 0,732 | 0,805 | 0,0044 (0,0005) | 10,7 | 4 |
| 2 500 | 320 | 0,733 | 0,732 | 0,860 | 0,0106 (0,0005) | 25,6 | 3–4 |
| 5 000 | 80 | 0,535 | 0,536 | 0,691 | 0,0022 (0,0002) | 10,7 | 5 |

- La viabilité seule condense : elle creuse des vides (8/8 graines partout) et fait naître un pic de P(k) à k = 3 à 5, absent des bras figé et mobile. [M]
- Ce pic suit le rayon de connexion : à 80 balayages, k = 4 à N = 2 500 et k = 5 à N = 5 000, rapport 1,25 pour r(2 500)/r(5 000) = 1,26 ; la longueur vaut environ 2,9·r_N dans les deux cas (relecture). C'est une échelle microscopique du modèle (rayon, pas de 0,3·r), non une échelle cosmique : elle ne contredit pas le constat du master, qui ne trouve aucune « longueur caractéristique » à grande échelle. [M] pour les positions, [H] pour l'interprétation. Le glissement avec le temps (k moyen ≈ 4,5 → 4 → 3,6 à N = 2 500, sur des coquilles entières) est mince. [M, faible]
- Bords : sans viabilité, 10 % des sommets finissent exactement sur une face (320 balayages, N = 2 500), artefact du rognage ; avec viabilité, la part à moins de r d'une face baisse (0,43 → 0,32) : la viabilité appauvrit les bords, effet de bord lui aussi. Le relecteur a vérifié, avec son propre code, que l'excès de vides subsiste sur les cellules intérieures (+0,064 contre +0,073 au total) et que le pic subsiste dans la sous-boîte [0,15 ; 0,85]³ ; contrôle non déposé ici, une boîte périodique reste à faire. [M] (relecture)
- Les amplitudes restent faibles : à 320 balayages, A = 0,011, soit 14 fois moins que les germes (0,15) ; P_max/médiane = 26 contre ≈ 250 à 440 pour les germes au même N. [M]

## Seconde implémentation

Partie A : toutes les cases du tableau, les pentes et les différences appariées ont été recalculées par le relecteur avec son propre code, concordantes.

Parties B et C : `r6_second_moteur.py` réécrit, sans code commun avec la partie B ni avec le moteur archivé, les germes, la dynamique (voisinage par cellules, viabilité locale recodée, générateur PCG64 sur d'autres graines) et les mesures (vides par cellules uniques, P(k) par `histogramdd` et `scipy.fft.fftn` complet, amplitude exacte des coquilles 1 et 2 par somme directe sur les points). Elle tire d'autres réalisations des germes : les niveaux absolus diffèrent (A figé 0,115 contre 0,150, dispersion des germes), les différences appariées se comparent. Sur 20 comparaisons (5 configurations × 4 différences : N = 1 000, 5 000, 10 000 à 5 balayages ; N = 2 500 à 20 balayages ; départ uniforme à 80 balayages), 17 concordent à moins de 2 erreurs combinées ; trois écarts entre 2,1 et 2,6 erreurs combinées : les deux différences de vides à N = 10 000 (même signe, même ordre) et la différence d'amplitude due à la mobilité depuis un départ uniforme (+2·10⁻⁵ contre −7·10⁻⁵, d'ordre 10⁻⁴ et proche de zéro dans les deux implémentations). Les signes de tous les effets non nuls et toutes les tendances sont reproduits, y compris le départ uniforme (vides 0,807 contre 0,805 ; pic à k = 3–4). Cette seconde implémentation vérifie le codage, pas le modèle : même règle, mêmes constantes, même s, même rognage.

## Ce que ceci change

- Au master, s'il est réédité : XXV.2 et XXV.3 ne peuvent dire « propre à la viabilité » la structuration mesurée par P_max/médiane ni dire que « l'excès croît avec N » au sens d'une structure croissante. Ce que les données soutiennent : une structure à grande échelle présente sans viabilité (posée par la nucléation dans la reconstruction), accentuée par la viabilité, érodée par la seule mobilité ; et une condensation propre à la viabilité, à l'échelle de quelques r_N, visible dans le fichier archivé comme sans germes.
- Rien au statut du programme ni à l'armature V347.1, qui ne reprend pas ces valeurs. Les portes physiques restent à 0/7.
- Défi dérivé : **DEFI-R7** — la condensation viable : échelle du modèle ou mûrissement sans fin ?

## Point le plus fragile

La partie B repose sur une **reconstruction** : le modèle de germes (forme gaussienne, âges, effectifs, rognage qui met 24 % des points sur les faces), la durée de dynamique et le choix du moteur de la gravité pour la toile sont des hypothèses ; la part de la nucléation dépend fortement de la durée (99 % à 5 balayages, 70 % à 80) et n'est pas une part causale. La partie A ne dépend pas de la reconstruction. La boîte n'est pas périodique, comme dans le moteur archivé.

## Reproduire

```
python3 contributions/R6_pilote-ia/r6_archive.py                     # partie A (1 s)
cd contributions/R6_pilote-ia
python3 r6_campagne.py --N 1000 --graines 0:8 --sortie r6_campagne_N1000.json   # idem N = 2500, 5000, 10000
python3 r6_campagne.py --N 20000 --graines 0:4 --sortie r6_campagne_N20000.json # et 4:8 → r6_campagne_N20000_b.json
python3 r6_campagne.py --N 2500 --graines 0:8 --balayages 20 --sortie r6_campagne_N2500_b20.json  # idem 5000 b20, 2500 b80
python3 r6_campagne.py --N 2500 --graines 0:8 --balayages 80 --init poisson --sortie r6_campagne_N2500_b80_initpoisson.json  # idem b20, b320 ; N = 5000 b80
python3 r6_second_moteur.py --N 5000 --graines 0:8 --sortie r6_second_N5000.json  # idem N = 1000, 10000 ; N = 2500 b20 ; --uniforme b80
python3 r6_analyse.py > r6_analyse_sortie.txt
```

Environ 2 h 30 de calcul sur 2 cœurs au total, dont 1 h pour N = 2 500 à 80 balayages (germes) et 1 h pour N = 20 000 ; numpy, scipy, sans numba. Les JSON de toutes les campagnes sont déposés.
