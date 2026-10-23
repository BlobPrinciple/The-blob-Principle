🇫🇷 Français · 🇬🇧 [English version](NOTE_EN.md)

# DEFI-R5 — Six incohérences entre des JSON du corpus et le master V346

*Pilote IA du laboratoire (Claude, Anthropic), 23 octobre 2026. Recherche répartie sur quatre agents IA ; les valeurs retenues sont recalculées par deux implémentations indépendantes ; relecture hostile en deux passes par un agent IA distinct, dont les objections bloquantes ont été intégrées. Non relu par une personne.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Aucun changement de statut. Aucune des valeurs en cause n'est reprise par l'armature V347.1, qui fait foi (sa recherche ouverte RO-08 renvoie à la plage V346 PDF 1243–1274, qui contient le passage de E5, sans en reprendre la valeur ρ*).

## Méthode

Texte du master V346 (1 918 p.) extrait par `pdftotext -layout`. Pages en numéro imprimé, page du PDF entre parenthèses (décalage de 48, sauf les tomes paginés à part comme V292). Le corpus compte 176 fichiers JSON (165 noms distincts). Les 169 JSON lisibles ont été confrontés aux passages qui rapportent la même campagne : par le nom du fichier quand le master le donne, sinon par le contenu (script, N, graines, date, valeurs). Chaque grandeur dérivée annoncée par le texte (moyenne, rapport, σ, pente, arithmétique) a été recalculée depuis le JSON. Les arrondis et les conventions d'écart-type (ddof 0 ou 1) qui ne changent aucune conclusion ne sont pas retenus.

## Incohérences retenues

**E1 — Tableau M-7.1 « Convergence d_s → 3 », p. 173 (PDF 221).**
- Cité : N = 1000, 20 graines, 3.045 ± 0.026, écart 1,5 % ; lignes N = 260 et N = 400.
- JSON : `06_campagnes_et_sauts/SAUT 9 et 10 et 11/Manifestes v99 et addendum v102/EXPECTED_OUTPUT_v93_updated 2.json`, `ds_N1000` = 2,847 ± 0,082, 5 graines, écart 5,1 % ; `ds_N3000` = 3,045 ± 0,026, 20 graines ; aucune entrée N = 260 ni N = 400.
- La ligne N = 1000 recopie la ligne N = 3000 (valeurs citées). Le master donne lui-même les valeurs du JSON p. 225 (PDF 273, M-13.1 « V2 corrigée ») et déclare p. 224–225 (PDF 272–273) que la valeur N = 400 « n'existe pas » ; le tableau M-7.1 la garde (3.180 ± 0.036). De N = 300 à 1 000, le JSON ne croît pas (2,908 ; 2,887 ; 2,847, écarts inférieurs aux barres) avant 3,045 à N = 3 000 : le tableau M-7.1, qui conclut à une « confirmation [M] que d_s converge vers 3 », ne repose pas sur ces données.

**E2 — Test loi d'aire, III.5.1, p. 259–260 (PDF 307–308) ; tableau VII.1.3, p. 329 (PDF 377).**
- Cité : σ²(n_K4) ∝ V^≈1,0 « régime intermédiaire », verdict « extensif, thermique standard » ; σ² vs A ≈ 1.
- JSON : `06_campagnes_et_sauts/Test O2v4 projection 3D à 2D trou noir/loi aire results.json`, `fits` : σ² ∝ V^3,230 (R² 0,789), σ² ∝ A^7,462 (R² 0,929). Le master imprime lui-même ce JSON p. 322–323 (PDF 370–371).
- La règle du script imprimé (p. 303–304, PDF 351–352 : `alpha < 0.78` loi d'aire, `alpha > 1.2` super-extensif) classe 3,23 « super-extensif ». On ne retrouve ≈ 1 qu'en écartant les deux premières classes, fenêtre non déclarée (classes 3 à 6 : 0,980 ; 3 à 7 : 0,923) ; les classes 4 à 6 donnent 0,774, sous le seuil de la loi d'aire. Selon la fenêtre, l'exposant va de 0,77 (classes 4 à 6) à 7,97 (classes 1 à 3), 3,23 sur l'ensemble : ni la qualification « extensif » ni l'absence de loi d'aire ne sont établies par ces données. σ² ∝ A^≈1 n'est retrouvé par aucune fenêtre de trois classes ou plus (la plus proche : 1,74).

**E3 — Annexe A1.5, cascades 2 et 3, p. 559–560 (PDF 607–608), statut [T].**
- Cité : « (0,30 × 0,2 × 8 × 0,414)/(2 × 0,125 × 81) = 0,0982 » ; « avec D_min^obs = 0,35 : Nβ|ΔD| ≤ 0,035 » ; « δ₀ ≥ 0,350 − 0,098 = 0,252 > 0 ».
- Calcul : l'expression imprimée vaut 0,00981 ; avec D_min = 0,35, 0,00350. Les deux évaluations imprimées valent dix fois l'expression. Le relecteur n'a trouvé dans le master aucune définition des constantes qui rende 0,0982 juste (il faudrait c₇ = 2 au lieu de 0,2).
- JSON : `06_campagnes_et_sauts/BLOB SCALING V30 DU 23 AVRIL 2026/EXPECTED_OUTPUT_v93_updated.json` (version « v93-consolidated-April2026 », que l'annexe, « reproduite de v105 », ne cite pas) : `delta0_analytic` = 0,159 [T*], `delta0_measured` = 0,274 [M].
- Portée : l'erreur d'évaluation est interne au master et certaine. Si l'expression est juste, la borne devient δ₀ ≥ 0,340, plus forte que 0,252 ; le [T] n'est fragilisé que si c'est l'expression qui est fausse. Le désaccord avec le JSON oppose deux versions du calcul (0,252 [T] contre 0,159 [T*]). Le signe δ₀ > 0 tient dans tous les cas. La valeur 0,252 est reprise à l'étape 2 du théorème LIT (A1.4, p. 559, PDF 607).

**E4 — Toile cosmique, XXV.2, p. 644–645 (PDF 692–693).**
- Cité : « structuration à grande échelle propre à la viabilité », P_max/médiane ≈ 1900 (Blob) contre 1,2 (Poisson) ; « grands vides, croissants avec N et propres à la viabilité » ; « jusqu'à 6 seeds ».
- JSON : `06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob_toile_results.json`. Les valeurs Blob et Poisson du texte concordent. Le témoin « mobilité sans viabilité », annoncé au protocole et présent dans le fichier, n'est pas rapporté :

| N | P_max/médiane Blob | sans viabilité | site unique | vides Blob | sans viabilité | excès de vides apparié |
|---|---|---|---|---|---|---|
| 5 000 | 635 | 619 | 739 | 0,861 | 0,834 | +0,027 (6/6) |
| 10 000 | 1 296 | 1 263 | 1 458 | 0,808 | 0,785 | +0,024 (5/5) |
| 20 000 | 1 879 | 2 277 | 2 380 | 0,763 | 0,743 | +0,020 (3/3) |

- L'essentiel de l'effet « nœuds + vides » subsiste sans viabilité. La viabilité n'ajoute qu'un excès de vides petit et de même signe dans toutes les paires de graines (+0,015 à +0,027 de N = 1 000 à 20 000) ; pour P_max/médiane, le Blob dépasse le témoin de 13 % à N = 1 000 et de 3 à 5 % de N = 2 500 à 10 000, puis le témoin dépasse le Blob à N = 15 000 (+4 %) et 20 000 (+21 %). « Propre à la viabilité » ne tient pas ; le fichier, sans témoin multi-sites figé, ne permet pas de séparer la nucléation de la mobilité. La synthèse XXV.3 (p. 645–646) est concernée. Mineur : le fichier a 8 graines à N = 1 000 et 2 500.

**E5 — CXL.7.2, p. 1203 (PDF 1251).**
- Cité : « ρ* ≈ 4,8–5,0 stable », sous « Non-variété confirmée à N=8000 ».
- JSON : `04_donnees/DERNIER JSON/palier_1000-2.json`, `palier_2000-2.json`, `palier_4000.json`, `palier_8000.json` (une campagne, 4 graines ; κ = 6,6 et date du 2 juillet 2026 selon `env-2.json` du même dossier) : ρ* = 4,993 ; 4,800 ; 4,803 ; 4,630 pour N = 1 000, 2 000, 4 000, 8 000 ; à N = 8 000, aucune des 4 graines n'atteint 4,8 (4,565 à 4,690). `03_scripts/SCRIPTS DIVERS BLOB/Grand N — paliers 32000/palier_32000.json`, campagne distincte à 8 graines : 4,421.
- Le master recale lui-même la constante sur ρ = 4,42 p. 1214 (PDF 1262) et y déclare « périmé » le calcul fait avec ρ = 4,9.

**E6 — Effondrement local, III.3.6, p. 255 (PDF 303).**
- Cité : « ⟨d_H^loc⟩ = 1.87 ± 0.24, statistiquement compatible avec 2 (la valeur exacte 2.00 est dans la barre d'erreur 1σ) » ; « l'effet dépasse 40σ ».
- JSON : `06_campagnes_et_sauts/Test O2v4 projection 3D à 2D trou noir/local collapse results.json`, `stats.dense` : 1,8685 ± 0,2418, écart-type sur n = 515 sommets.
- Deux métriques dans le même paragraphe : les t de Welch du texte (−25,33 ; −44,37) se recalculent (−25,36 ; −44,40) avec l'erreur-type par sommet, à laquelle 2 est à 12,3 erreurs-types. Les 515 sommets viennent de 5 graines : les erreurs-types par sommet sont des pseudo-répliques, et « compatible avec 2 à 1σ » et « 40σ » ne sont pas calculables à l'échelle des graines depuis le JSON, qui ne donne pas la classe dense par graine. La hiérarchie des moyennes Dense < Bulk < Void tient.

## Écarts mineurs

- **m1** — M-3.2, p. 136 (PDF 184) : « facteur 2.25× à 3.25× » ; les rapports Blob/nul du tableau vont de 2,51 (N = 300) à 3,25 (N = 3 000) : 2,25 est le gain (+225 %) lu comme un rapport. Le « 36.8σ » de N = 3 000 correspond à n = 4, le `SNR = 41` du JSON à n = 5 ; aucun n n'est documenté.
- **m2** — Même tableau, ligne N = 10 000 (49 204 ± 5 050 contre 17 510 ± 249, [M]) : le manifeste `EXPECTED_OUTPUT_v93_updated 2.json` porte `tri_ratio_N10000` = null, « PENDING » ; aucun JSON trouvé dans le corpus ne contient cette mesure.
- **m3** — Test B, cascade triangle → tétraèdre, p. 261 (PDF 309) : « 5 seeds » ; `scout results.json` et le script imprimé p. 305 : 4 graines, 56 points. b = 2,041 et R² = 0,534 concordent.
- **m4** — Tome V292, PARTIE CCI, volet C, p. 5 du tome (PDF 1375) : « Écart final : 0,004 ». `03_scripts/simulations/blob_total_V286_results.json` et la table imprimée donnent 0,014 au niveau final (0,331 contre 0,345) ; 0,004 est le critère du script, l'écart des moyennes des niveaux 1 à 3 (0,0042). Intitulé trompeur, conclusion inchangée.

## Concordances vérifiées

Rejoués par le pilote, concordants aux arrondis près : `invariants_500k.json` et `banc_*.json` (§122.6, p. 1063) ; `alpha_v2_*.json` (§122.1, p. 1059 : les 12 pentes recalculées depuis les points, α = 0,126 ± 0,008 en moyenne pondérée, 1,3σ et 0,4σ) ; `courbures_KL.json` (§123.1, p. 1065 : pentes pondérées −0,032 ± 0,011 et −0,012 ± 0,013) ; `queue_mort.json` et `rondeur_v2.json` (§124.1–§124.2, p. 1072–1073 : 7,1σ, 7,1σ, 10,6σ ; pentes et différences) ; `campagne_blob_ir.json` (annexe du 21 juin, p. 1134–1135 : moyennes et écarts des cinq paliers de la phase 1) ; `blob_paliers_N*.json` (PARTIE XX, p. 614–616 : séparations 8,3σ à 5,6σ et 1,8σ à 9,9σ). Ces contrôles ont été confirmés par le relecteur.

Signalés concordants par les agents de recherche, non rejoués par le pilote : `alpha_C*.json` (§121.2), `calibration ds results.json`, `dh ds convergence.json`, les JSON de verrouillage et de briques (PARTIE VII), `blob_dims_N*.json`, `blob_hierarchie_seed1.json`, `frontiere_V280_results.json`, les autres volets de `blob_total_V286_results.json`.

## Constats d'intégrité, hors du défi

- `blob_paliers_GLOBAL.json`, cité comme donnée de la PARTIE XX, ne contient que le palier N = 1 000 (les fichiers par palier, qui concordent, contiennent le reste).
- `campagne_blob_ir.json`, cité comme source, ne contient que la phase 1 (N ≤ 100 000) ; la phase 2 (250 000 à 2 000 000) n'y figure pas.
- Sept fichiers sont tronqués (JSON invalide) : `palier_N100_modeblob_seed1.json`, `palier_N100_modeblob_seed1-2.json`, `palier_N200_modeblob_seed1.json`, `palier_N1000_modeblob_seed1.json` (« Sauts 2 a 35 »), `palier_N100_modeblob_seed1.json` et `palier_N200_modeblob_seed1.json` (« Manifestes v99 et addendum v102 »), `saut9_N2000_seed1.json`.
- Dans `SAUT 35V3/`, tous les instantanés ont E = 0 et n_tri = 0 (`first_edge_step` nul), alors que le `saut35v3_RAPPORT.json` homonyme du dossier « Sauts 2 a 35 » rapporte des milliers de tétraèdres. Aucun de ces fichiers n'est cité par le master.

## Ce que cela change

Rien au statut du programme ni à l'armature V347.1. Deux corrections de fond sont à porter au master s'il est réédité : E1 (le tableau M-7.1 doit reprendre les valeurs de M-13.1) et E4 (la structuration « nœuds + vides » ne peut être dite propre à la viabilité ; seuls de petits excès — vides, et P(k) à petit N — le sont dans ces données). [OPEN] Un témoin multi-sites figé et des statistiques par graine diraient ce qui, dans la toile, revient à la nucléation, à la mobilité et à la viabilité.

## Reproduire

```
python3 contributions/R5_pilote-ia/r5_audit.py          # implémentation A (numpy) : r5_audit_sortie.json
python3 contributions/R5_pilote-ia/r5_audit_second.py   # implémentation B (Python pur, fractions, scipy) : contrôle des valeurs de cette note
```

Quelques secondes. Sorties de référence : `r5_audit_sortie.txt` ; `ACCORD COMPLET` en dernière ligne de `r5_audit_second_sortie.txt`. Les codes E1 à E6 et m1 à m4 sont ceux de cette note.
