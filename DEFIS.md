🇫🇷 Français · 🇬🇧 [English version](en/CHALLENGES.md)

# Les défis du Blob — « Cassez le Blob »

> **TOE démontrée : NON.** Le Blob Principle ne demande pas à être cru. Il demande à être **éprouvé**.
> Chaque défi ci-dessous est un vrai problème ouvert du programme. Le réussir — y compris en **réfutant** une affirmation — fait avancer la science, et votre nom entre au [tableau d'honneur](#tableau-dhonneur).

**Règle d'or :** une réfutation propre vaut autant qu'une preuve. Le programme a déjà rétracté des dizaines de ses propres affirmations ; il vous invite à continuer.

Pour relever un défi : ouvrez une *issue* avec le modèle adapté, citez le code du défi (ex. `DEFI-R1`), puis déposez votre travail dans `contributions/`. Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Le fil conducteur : la cosmogonie du Blob, et comment la prouver

Tous les défis servent un seul but, déclaré par l'auteur : faire du Blob une candidate TOE forte, puis une TOE. Aujourd'hui, il est au niveau 1 (modèle mathématique reproductible) ; la distance à parcourir est connue et découpée en quatre étapes, détaillées dans [PILOTE_IA.md](PILOTE_IA.md#le-chemin-de-preuve) :

- **P1** — unifier la cosmogonie : une seule dynamique dérivée de Ω⁰ jusqu'au secteur G0 ;
- **P2** — fermer la porte G0 / continuum ;
- **P3** — franchir les portes physiques (0/7) par la confrontation au réel ;
- **P4** — validation externe (G6) ;
- **T** — transversal : lire, traduire, expliquer, répliquer, chasser les erreurs, tenter de casser le Blob.

**Les défis évoluent.** Chaque contribution retenue est inscrite au [journal des avancées](JOURNAL_DES_AVANCEES.md) ; un défi clos en ouvre au moins un autre, plus proche du fil conducteur ; une réfutation ouvre le défi « réparer ou abandonner » la branche touchée. Laissez le Blob plus éprouvé que vous ne l'avez trouvé.

### État des défis

<!-- ETAT-DEFIS:DEBUT (généré par outils/defis.py, ne pas modifier à la main) -->
*État au 2026-10-27 — défis v1.10.*

| Défi | Étape du chemin de preuve | État | Dernier événement |
|---|---|---|---|
| DEFI-L1 | T | ouvert | — |
| DEFI-L2 | T | ouvert | — |
| DEFI-L3 | T | ouvert | — |
| DEFI-L4 | T | ouvert | — |
| DEFI-L5 | T | ouvert | — |
| DEFI-R1 | T | réplication obtenue | 2026-10-06 : SELFTEST : 4/4 sur machine tierce, numpy 2.5.3 |
| DEFI-R2 | P2 | ouvert | — |
| DEFI-R3 | T | ouvert | 2026-10-15 : [T]+[M] le moteur archivé V109 (V346 p. 291–292) surcompte les triangles de +1,4 % à +2,7 % quand l'arête ajoutée touche l'arête retirée ; le moteur canonique actuel n'est pas concerné |
| DEFI-R4 | P1 | ouvert | — |
| DEFI-R5 | T | ouvert | 2026-10-23 : [M] six incohérences JSON ↔ master V346 : tableau M-7.1 (p. 173), ligne N = 1000 recopiée de N = 3000 (JSON : 2,847 ± 0,082, 5 graines) ; loi d'aire (p. 259–260) : « σ² ∝ V^≈1 » contre 3,23 au JSON, verdict dépendant de la fenêtre ; A1.5 (p. 560) : expression évaluée à 0,0982 au lieu de 0,00981, δ₀ = 0,252 [T] contre 0,159 [T*] au JSON ; toile cosmique (p. 644–645) : le témoin sans viabilité reproduit l'essentiel de l'effet « propre à la viabilité » ; ρ* « 4,8–5,0 stable » (p. 1203) contre 4,630 à N = 8 000 ; III.3.6 (p. 255) : écart-type et erreur-type mêlés ; quatre écarts mineurs |
| DEFI-R6 | T | ouvert | — |
| DEFI-M1 | P2 | ouvert | — |
| DEFI-M2 | P2 | ouvert | — |
| DEFI-M3 | P1 | ouvert | 2026-10-15 : [T] mitose + échanges à |E| fixé conservent M − N (degré moyen < 2 depuis Ω⁰) ; [CERT] à M = N − 1, π concentre sa masse sur des îlots triangulaires disjoints : l'« option la plus économique » de RO-24 est réfutée pour le moteur à |E| fixé |
| DEFI-M4 | P1 | ouvert | — |
| DEFI-M5 | P1 | ouvert | — |
| DEFI-M6 | P1 | ouvert | — |
| DEFI-M7 | P1 | ouvert | 2026-10-15 : [M] moteur canonique : degré du nouveau-né relaxé en 8 à 16 balayages, sans croissance de N = 250 à 4 000 ; coût d'une naissance proportionnel à N ; [OPEN] masse triangulaire du nouveau-né non tranchée (−3,0 ± 2,0 à 512 balayages) |
| DEFI-M8 | P1 | ouvert | 2026-10-20 : [T] à k fixé, l'attachement de Gibbs G*(A | C) ∝ π_{N+1,M+k}(C + v_A), dérivé de S_sim sans paramètre nouveau, atteint la borne de la proposition C et minimise de façon unique la KL à la naissance ; ses poids ne varient qu'avec les arêtes entre cibles et la somme de leurs degrés (fermeture triadique anti-préférentielle) ; [CERT] graphes abstraits, N + 1 ≤ 7, 39 passages : aucun gain sur l'uniforme dans 25 cas, gain au meilleur k de 0 à 0,41 ; dans les 5 cas où G* gagne, relaxation ralentie de 25 à 44 % ; l'attachement anti-Gibbs relaxe le plus vite dans 5 cas sur 6 ; k non dérivé |
| DEFI-M9 | P1 | ouvert | 2026-10-16 : [M] corps de la loi des masses du nouveau-né indiscernable de la population après 16 à 256 balayages (N = 250 à 2 000, 200 naissances par taille) ; [M] queue lente : 6 à 7 % des nouveau-nés dans le décile massif jusqu'à 1 024 balayages (10 % attendus), 8,5 % à 2 048 ; [M, partiel] décile massif largement partagé entre chaînes sur 9 nuages sur 10, et évitant les bords du cube ; [OPEN] rôle de l'âge |
| DEFI-M10 | P1 | ouvert | — |
| DEFI-M11 | P1 | ouvert | 2026-10-20 : [CERT] carte exacte, 102 cas à N + 1 ≤ 7 : là où G* gagne à la naissance, il ralentit la relaxation dans 50 cas sur 57 (45 sur 47 pour un gain ≥ 10⁻³), l'anti-Gibbs accélère dans 44 cas sur 57 ; [M] Monte-Carlo N = 8 à 64, M + k = 2(N + 1), k = 4 : observables globales indifférentes à la loi de naissance après quelques balayages ; demi-temps d'accession des triangles du nouveau-né au moins de l'ordre de N³ balayages (0,5 à N = 8, 442 à N = 64), peu sensible à la loi de naissance de la famille G_θ : 87 à 97 % de la masse triangulaire est portée par une aristocratie de sommets |
| DEFI-M12 | P1 | ouvert | 2026-10-27 : [M] graphes abstraits, degré moyen 4, mesure de l'armature (λ = n/τ), n = 17 à 193 : demi-temps d'autocorrélation poolée de T_v de 9,2 à 111 873 balayages, ni loi de puissance ni exponentielle en n : log t½ = 0,964·√n − 1,77 (exposant libre 0,507 ± 0,010), prédiction faite sur n ≤ 97 vérifiée à 2 % près à n = 129 et 193 ; méthode naissance de DEFI-M11 concordante à N = 96 et 128 ; [M] degré moyen 6 : sur-polynomial, plus rapide (exp(a·n^0,6) environ) ; [M] la lenteur suit λ : à λ fixé, t½ décroît avec n et l'aristocratie se dissout ; à n = 65, log t½ affine en λ ; [M] l'aristocratie est une clique dominante de taille ≈ n^0,47 portant 69 à 90 % des triangles ; [H] conséquence pour le pont : ≈ 0,17·exp(0,96·√n) balayages entre naissances si la loi se prolongeait |
| DEFI-M13 | P1 | ouvert | — |
| DEFI-G1 | P2 | ouvert | — |
| DEFI-G2 | P2 | ouvert | — |
| DEFI-G3 | P2 | ouvert | — |
| DEFI-G4 | P2 | ouvert | — |
| DEFI-T0 | T | ouvert | — |
| DEFI-D1 | T | ouvert | — |
| DEFI-D2 | T | ouvert | — |
<!-- ETAT-DEFIS:FIN -->

Source : [docs/defis.json](docs/defis.json), version lisible par machine.

---

## Niveau 0 — Curieux (aucune compétence technique requise)

| Code | Défi | Ce qu'il faut rendre |
|---|---|---|
| **DEFI-L1** | **Le lecteur.** Lisez l'[armature V347.1](corpus/00_master_courant/BLOB_PRINCIPLE_MASTER_V347_1_ARMATURE_CANONIQUE.pdf) (29 p.) et signalez le passage le moins clair. | Une *issue* « Question » : page, phrase, ce qui bloque. |
| **DEFI-L2** | **Le passeur.** Traduisez un chapitre du Livre I de l'armature (anglais, espagnol, arabe, chinois…) en respectant le [lexique verrouillé](index/LEXIQUE_FR-EN.md) — *viabilité* se dit *viability*, jamais *sustainability*. | La traduction dans `contributions/traduction_<langue>_<nom>/`. |
| **DEFI-L3** | **L'illustrateur.** Dessinez la cascade point → arête → triangle → tétraèdre, ou les trois temps du Blob, de façon fidèle au récit (I.1 à I.6). | Une image (PNG/SVG) et une phrase d'explication. |
| **DEFI-L4** | **Le vulgarisateur.** Expliquez le Blob en 60 secondes (texte, vidéo, BD), **avec le bloc de statut** : TOE démontrée : NON. | Le lien ou le fichier. |
| **DEFI-L5** | **Le Bâtisseur.** Sur la page [Fais naître ton univers](https://blobprinciple.github.io/The-blob-Principle/univers.html), obtenez à 80 sommets un univers d'un seul tenant et régulier (D < 0,50) avec **3 arêtes de fermeture seulement**. Aucun des 2 400 univers simulés par le laboratoire n'y parvient ; record à battre : D = 0,542 (graine 5215). | Un commentaire dans la [galerie des univers (#33)](https://github.com/BlobPrinciple/The-blob-Principle/issues/33) : lien, D, nombre de morceaux. Vérifiable avec `node outils/univers_batisseur.js`. |

## Niveau 1 — Codeur, étudiant, ingénieur

| Code | Défi | Point de départ | Critère de réussite |
|---|---|---|---|
| **DEFI-R1** | **Le réplicateur.** Exécutez l'auto-test du moteur C2-R sur votre machine. | `python3 corpus/07_complements/blob_c2r_autonome-2.py --selftest` (dépendance : numpy) | Rapport « Réplication » : machine, versions, sortie complète. Attendu : `SELFTEST : 4/4`. *Vérifié le 6 octobre 2026 sur une machine tierce (numpy 2.5.3) : 4/4.* |
| **DEFI-R2** | **L = 6.** Faites aboutir la campagne C2-R à L = 6, non concluante faute de calcul (environ 17 % du budget requis). | Même script, `--all` puis `--finalize` | Rapport avec R̂, ESS, MCSE et décision du contrat gelé. Relève **RO-12**. |
| **DEFI-R3** | **Le second moteur.** Réécrivez **indépendamment**, sans lire le code existant, l'échantillonneur de la fonctionnelle *S_sim(C) = log(1 + n_tri(C)) − βD(C)* et comparez vos invariants à ceux publiés. | Définitions de l'armature V347.1, II.0 et II.4 ; données `corpus/04_donnees/` | Écarts chiffrés avec barres d'erreur. Toute divergence est un résultat. |
| **DEFI-R4** | **La nucléation.** Le Blob peut-il naître du vide strict ? Aujourd'hui : 0/40 graines sous les deux moteurs canoniques. | Armature II.3, **RO-02** | Protocole **préenregistré** (publié avant exécution) sur ≥ 30 graines : P(Ω¹ \| Ω⁰) ≥ 0,9 depuis le vide strict, **ou** une borne négative propre. |
| **DEFI-R5** | **Le chasseur d'erreurs.** Trouvez une incohérence numérique entre un résultat publié (JSON) et le texte du master qui le cite. | `corpus/03_scripts/`, `corpus/06_campagnes_et_sauts/`, master V346 | Fichier, page, valeur citée, valeur réelle. |
| **DEFI-R6** | **La toile sans viabilité.** Le master V346 (XXV.2) dit la structuration « nœuds + vides » de la toile cosmique simulée « propre à la viabilité » ; le témoin « mobilité sans viabilité » du même fichier reproduit l'essentiel de l'effet, la viabilité n'ajoutant qu'un petit excès de vides ([note](contributions/R5_pilote-ia/NOTE.md), E4). Qu'est-ce qui sculpte les nœuds et les vides : la nucléation multi-sites, la mobilité ou la viabilité ? | `corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob_toile_results.json`, master V346 p. 644–646 | Campagne à quatre bras au moins (avec viabilité, mobile sans viabilité, multi-sites figé, Poisson), N ≥ 5 000 à deux tailles, 8 graines par bras, statistiques par graine, code et JSON publiés ; ou argument démontré. |

## Niveau 2 — Mathématicien, physicien

| Code | Défi | Recherche ouverte | Ce qui compte comme réussite |
|---|---|---|---|
| **DEFI-M1** | **Les quatre points de SUP-1.** Degré borné contre O(log N), ordre des limites, 3-tore contre cube à bord, étiquettes (H1)–(H3) incohérentes. | [ETAT § 5](ETAT_DU_PROGRAMME.md) | Note de supersession qui tranche chacun des quatre points. |
| **DEFI-M2** | **La pince spectrale.** Le même objet peut-il satisfaire l'ellipticité uniforme exigée par Delmotte (INF-1) et le cadre non elliptique de SUP-1 ? | [Audit INF-1](corpus/02_portes_et_audits/audits_18-09-2026/) | Preuve que la pince se referme sur une classe explicite, **ou** obstruction démontrée. |
| **DEFI-M3** | **La fermeture.** La mitose seule ne produit jamais de triangle (no-go démontré). Proposez un générateur de fermeture **local** compatible avec la viabilité. | **RO-24** | Générateur explicite, ou preuve qu'aucun générateur local compatible n'existe (ce qui tuerait la cascade causale). |
| **DEFI-M4** | **Le bit σ₀.** Montrez que le choix de polarité à la première scission ne peut pas être dérivé de Ω⁰ et doit rester un axiome — ou dérivez-le. | **RO-03** | Théorème d'obstruction, ou mécanisme interne. |
| **DEFI-M5** | **La scission double.** Toute « scission en deux simplexes opposés » se réduit-elle à deux mitoses successives ? | **RO-04** | Réduction démontrée, ou nouvelle opération explicitée. |
| **DEFI-M6** | **Persister.** Donnez une définition de « persister » indépendante du simple fait que π > 0. | **RO-20** | Critère robuste, non arbitraire, calculable. |
| **DEFI-M7** | **Le coût du pont.** Après la naissance d'un sommet avec ses arêtes de fermeture, combien d'échanges de Metropolis par arête faut-il pour revenir à π_N ? Sur graphes abstraits : 2,5 à 4,7 par arête (ε = 0,01, N = 5 à 7, [rapport](contributions/RO-25_pilote-ia/RAPPORT.md)). Ce coût reste-t-il borné quand N grandit, sur le moteur Rips ? | **RO-25** | Borne démontrée, ou mesure multi-graines avec barres d'erreur jusqu'à N ≥ 500, montrant un coût borné ou divergent. |
| **DEFI-M8** | **Une fermeture non arbitraire.** La mitose seule ne peut pas porter la cascade : il faut ≈ κ̄/2 − 1 arêtes de fermeture par naissance ([rapport](contributions/RO-25_pilote-ia/RAPPORT.md)). Dérivez de S_sim, sans la poser, la loi d'attachement du nouveau sommet qui minimise l'écart à π dès la naissance. | **RO-24**, **RO-25** | Loi dérivée et écart à la naissance comparé à l'attachement uniforme, ou preuve qu'aucune loi locale ne fait mieux. |
| **DEFI-M9** | **L'aristocratie des sommets massifs.** Sur le moteur canonique, le degré d'un nouveau-né rejoint la moyenne en 8 à 16 balayages, mais sa masse triangulaire reste en déficit ([rapport](contributions/RO-25_pilote-ia/DEFI-M7_RAPPORT.md)). Le nouveau-né atteint-il un jour la masse typique, ou la viabilité fige-t-elle une aristocratie de sommets massifs ? | **RO-25**, **RO-20** | Loi des triangles incidents du nouveau-né contre celle de la population, en variation totale, avec au moins 200 naissances par taille sur au moins trois tailles ; ou argument démontré. |
| **DEFI-M10** | **La lente accession au décile massif.** La loi des masses d'un nouveau-né rejoint celle de la population en 16 à 256 balayages, sauf la queue : 6 à 7 % des nouveau-nés sont dans le décile massif jusqu'à 1 024 balayages, contre 10 % attendus ([rapport](contributions/RO-25_pilote-ia/DEFI-M9_RAPPORT.md)). Combien de balayages pour atteindre 10 %, ce temps croît-il avec N, et le nouveau-né rejoint-il la masse d'équilibre de sa position ? | **RO-25**, **RO-20** | Part mesurée à ± 1 point (au moins 1 000 naissances par taille, deux tailles) jusqu'à au moins 16 384 balayages, comparée à la masse d'équilibre de la position (chaîne indépendante, de préférence en boîte périodique) ; ou borne démontrée. |
| **DEFI-M11** | **Naître juste ou relaxer vite.** L'attachement de Gibbs, dérivé de S_sim, minimise exactement l'écart à π à la naissance, mais ralentit de 25 à 44 % la relaxation dans les cinq cas où il gagne ; l'attachement anti-Gibbs relaxe le plus vite dans cinq cas sur six (graphes abstraits, N ≤ 6 ; [rapport](contributions/RO-25_pilote-ia/DEFI-M8_RAPPORT.md)). Quelle loi d'attachement minimise le coût total du pont, et est-elle dérivable de S_sim ? | **RO-25**, **RO-24** | Loi minimisant le temps de relaxation après naissance (borne démontrée, ou mesure exacte jusqu'à N + 1 ≥ 8 et multi-graines sur le moteur canonique à N ≥ 250), comparée à U, G\* et G_θ ; ou preuve que les deux critères coïncident asymptotiquement. |
| **DEFI-M12** | **La lenteur aristocratique.** Sur graphes abstraits à degré moyen 4, un nouveau-né met de plus en plus longtemps à acquérir sa masse triangulaire d'équilibre : demi-temps de 0,5 balayage à N = 8, 442 à N = 64, au moins de l'ordre de N³, peut-être exponentiel ; la masse est portée par une aristocratie de sommets ([rapport](contributions/RO-25_pilote-ia/DEFI-M11_RAPPORT.md)). Puissance ou exponentielle ? | **RO-25**, **RO-20** | Borne démontrée (trou spectral, goulot d'étranglement), ou mesure jusqu'à N ≥ 128 à deux densités au moins et sur le moteur canonique à N ≥ 250, avec barres d'erreur. |
| **DEFI-M13** | **La barrière de la clique dominante.** Sur graphes abstraits à degré moyen 4, sous la mesure de l'armature, le temps que met un sommet à changer de rang triangulaire croît comme exp(0,96·√n) de n = 17 à 193 (ni puissance ni exponentielle en n) ; la lenteur suit λ = n/τ et l'aristocratie est une clique dominante de taille ≈ √n ; à degré moyen 6, la croissance est plus rapide ([rapport](contributions/RO-25_pilote-ia/DEFI-M12_RAPPORT.md)). Pourquoi √n, et pourquoi pas à degré moyen 6 ? | **RO-25**, **RO-20** | Preuve ou réfutation d'une barrière exp(Θ(√n)) (goulot d'étranglement, conductance) et d'une clique de taille Θ(√n) ; explication de l'exposant ≈ 0,6 à degré moyen 6 ; ou même signature cherchée sur le moteur canonique à N ≥ 250. |

## Niveau 3 — Spécialiste (porte G0)

| Code | Défi | Recherche ouverte |
|---|---|---|
| **DEFI-G1** | Marge locale uniforme sur le secteur typique de Gibbs (GEN-4 *typical-set*) | **RO-13** |
| **DEFI-G2** | Intertwiner MARKED ↔ CONNECTED dans une norme de Banach déclarée | **RO-14** |
| **DEFI-G3** | Convergence sous retrait du régulateur, limite projective | **RO-15** |
| **DEFI-G4** | Point fixe non trivial et universalité (C4, C5, C7) | **RO-16** |

## Le procès des 22 paradoxes — le débat est ouvert

Le récit des livres *Du simplexe au complexe* donne une place à vingt-deux grands paradoxes. Combien tiennent face aux mathématiques ? Verdict provisoire : **classe A = 0**, B = 3, C = 14, D = 5. Dossier complet : [debats/PROCES_DES_PARADOXES.md](debats/PROCES_DES_PARADOXES.md) · [#32](https://github.com/BlobPrinciple/The-blob-Principle/issues/32).

| Code | Défi | Ce qu'il faut rendre |
|---|---|---|
| **DEFI-D1** | **Le juré** (niveau 0). Contestez le classement d'un paradoxe : trop sévère ou trop généreux. | Un commentaire dans [#32](https://github.com/BlobPrinciple/The-blob-Principle/issues/32) : numéro, classe proposée, argument, page citée. |
| **DEFI-D2** | **L'avocat** (niveau 2). Faites monter un paradoxe d'une classe — D → C : un mécanisme explicite ; C → B : un objet formel défini dans l'armature ; B → A : un énoncé [T] dans le secteur canonique — ou démontrez qu'il doit descendre. | Une note dans `contributions/` ; candidats les plus proches de la classe A : n° 5, 8 et 9 (**RO-03**, **RO-10**, **RO-26**). |

## Le grand défi — le Tribunal ouvert

**DEFI-T0 — Cassez le Blob.** Trouvez une faille **fatale** : une contradiction interne, une hypothèse cachée qui fait tomber une branche entière, un résultat central non reproductible. Argumentez-la avec la rigueur d'un relecteur de revue.

Les réfutations retenues sont inscrites au **Mur des réfutateurs**, avec le nom de leur auteur, dans chaque version maîtresse qui en tient compte.

---

## Tableau d'honneur

| Date | Contributeur | Défi | Résultat | Effet sur le programme |
|---|---|---|---|---|
| 06/10/2026 | (vérification d'ouverture) | DEFI-R1 | `SELFTEST : 4/4` sur machine tierce, numpy 2.5.3 | Reproductibilité de l'auto-test confirmée |
| 16/10/2026 | Pilote IA du laboratoire (Claude, Anthropic) — non relu par une personne | DEFI-M9 (RO-25) | [M] Le déficit de masse du nouveau-né se concentre dans la queue massive, rejointe lentement ; le décile massif est largement partagé entre chaînes indépendantes ([rapport](contributions/RO-25_pilote-ia/DEFI-M9_RAPPORT.md), [#19](https://github.com/BlobPrinciple/The-blob-Principle/issues/19)) | Résultat partiel ; défi dérivé DEFI-M10 ; statut inchangé |
| 20/10/2026 | Pilote IA du laboratoire (Claude, Anthropic) — non relu par une personne | DEFI-M8 (RO-24, RO-25) | [T] L'attachement de Gibbs dérivé de S_sim est la meilleure loi généalogique à la naissance (à k fixé) ; [CERT] il ralentit pourtant la relaxation dans les cinq cas où il gagne ([rapport](contributions/RO-25_pilote-ia/DEFI-M8_RAPPORT.md), [#35](https://github.com/BlobPrinciple/The-blob-Principle/issues/35)) | Résultat partiel ; défi dérivé DEFI-M11 ; statut inchangé |
| 20/10/2026 | Pilote IA du laboratoire (Claude, Anthropic) — non relu par une personne | DEFI-M11 (RO-25, RO-24) | [CERT] Bien naître ralentit le pont dans 50 cas exacts sur 57 ; [M] à grand N, l'accession du nouveau-né à la masse triangulaire d'équilibre prend au moins de l'ordre de N³ balayages, quelle que soit la loi de naissance testée ([rapport](contributions/RO-25_pilote-ia/DEFI-M11_RAPPORT.md), [#37](https://github.com/BlobPrinciple/The-blob-Principle/issues/37)) | Résultat partiel ; défi dérivé DEFI-M12 ; statut inchangé |
| 27/10/2026 | Pilote IA du laboratoire (Claude, Anthropic) — non relu par une personne | DEFI-M12 (RO-25, RO-20) | [M] La lenteur aristocratique n'est ni une loi de puissance ni une exponentielle en n : à degré moyen 4, t½ ≈ exp(0,96·√n) de n = 17 à 193, prédiction hors échantillon vérifiée ; elle suit le refroidissement λ = n/τ de la mesure et l'aristocratie est une clique dominante de taille ≈ √n ([rapport](contributions/RO-25_pilote-ia/DEFI-M12_RAPPORT.md), [#41](https://github.com/BlobPrinciple/The-blob-Principle/issues/41)) | Résultat partiel ; défi dérivé DEFI-M13 ; statut inchangé |

## Mur des réfutateurs

| Date | Réfutateur | Défi | Ce qui est réfuté | Effet sur le programme |
|---|---|---|---|---|
| 15/10/2026 | Pilote IA du laboratoire (Claude, Anthropic) — non relu par une personne | DEFI-M3 (RO-24) | L'« option la plus économique » proposée pour RO-24 : mitose et échanges à \|E\| fixé conservent M − N, et la sélection fragmente alors le graphe en îlots triangulaires disjoints ([rapport](contributions/RO-25_pilote-ia/RAPPORT.md)) | RO-24 reste ouvert ; toute fermeture doit créer des arêtes ; défis dérivés DEFI-M7 et DEFI-M8 ; aucun changement de statut |
| 15/10/2026 | Pilote IA du laboratoire (Claude, Anthropic) — non relu par une personne | DEFI-R3 | Le comptage incrémental des triangles du moteur archivé V109 (V346 p. 291–292) : surcompte de +1,4 % à +2,7 % ([note](contributions/R3_pilote-ia/NOTE.md)) | Script [ARCH] corrigé ; le moteur canonique n'est pas concerné ; statut inchangé |
| 23/10/2026 | Pilote IA du laboratoire (Claude, Anthropic) — non relu par une personne | DEFI-R5 | Six passages du master V346 contredits par les JSON qu'ils rapportent : ligne N = 1000 du tableau M-7.1 recopiée de N = 3000 ; « σ² ∝ V^≈1 » (fit enregistré : 3,23) ; borne de A1.5 évaluée dix fois trop haut ; toile « propre à la viabilité » alors que le témoin sans viabilité reproduit l'essentiel de l'effet ; ρ* « stable » ; deux métriques d'erreur mêlées ([note](contributions/R5_pilote-ia/NOTE.md), [#39](https://github.com/BlobPrinciple/The-blob-Principle/issues/39)) | Corrections à porter au master s'il est réédité ; armature V347.1 non touchée ; défi dérivé DEFI-R6 ; statut inchangé |

*La place suivante vous attend.*

---

### Ce que vous gagnez

- **Un crédit nominatif permanent** dans [CONTRIBUTEURS.md](CONTRIBUTEURS.md) et dans la version maîtresse qui intègre votre apport.
- **Une trace citable** : chaque version du dépôt reçoit un DOI Zenodo.
- La satisfaction d'avoir éprouvé une candidate à la théorie du tout — qu'elle tienne ou qu'elle tombe.
