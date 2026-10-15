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
*État au 2026-10-15 — défis v1.1.*

| Défi | Étape du chemin de preuve | État | Dernier événement |
|---|---|---|---|
| DEFI-L1 | T | ouvert | — |
| DEFI-L2 | T | ouvert | — |
| DEFI-L3 | T | ouvert | — |
| DEFI-L4 | T | ouvert | — |
| DEFI-R1 | T | réplication obtenue | 2026-10-06 : SELFTEST : 4/4 sur machine tierce, numpy 2.5.3 |
| DEFI-R2 | P2 | ouvert | — |
| DEFI-R3 | T | ouvert | — |
| DEFI-R4 | P1 | ouvert | — |
| DEFI-R5 | T | ouvert | — |
| DEFI-M1 | P2 | ouvert | — |
| DEFI-M2 | P2 | ouvert | — |
| DEFI-M3 | P1 | ouvert | — |
| DEFI-M4 | P1 | ouvert | — |
| DEFI-M5 | P1 | ouvert | — |
| DEFI-M6 | P1 | ouvert | — |
| DEFI-G1 | P2 | ouvert | — |
| DEFI-G2 | P2 | ouvert | — |
| DEFI-G3 | P2 | ouvert | — |
| DEFI-G4 | P2 | ouvert | — |
| DEFI-T0 | T | ouvert | — |
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

## Niveau 1 — Codeur, étudiant, ingénieur

| Code | Défi | Point de départ | Critère de réussite |
|---|---|---|---|
| **DEFI-R1** | **Le réplicateur.** Exécutez l'auto-test du moteur C2-R sur votre machine. | `python3 corpus/07_complements/blob_c2r_autonome-2.py --selftest` (dépendance : numpy) | Rapport « Réplication » : machine, versions, sortie complète. Attendu : `SELFTEST : 4/4`. *Vérifié le 6 octobre 2026 sur une machine tierce (numpy 2.5.3) : 4/4.* |
| **DEFI-R2** | **L = 6.** Faites aboutir la campagne C2-R à L = 6, non concluante faute de calcul (environ 17 % du budget requis). | Même script, `--all` puis `--finalize` | Rapport avec R̂, ESS, MCSE et décision du contrat gelé. Relève **RO-12**. |
| **DEFI-R3** | **Le second moteur.** Réécrivez **indépendamment**, sans lire le code existant, l'échantillonneur de la fonctionnelle *S_sim(C) = log(1 + n_tri(C)) − βD(C)* et comparez vos invariants à ceux publiés. | Définitions de l'armature V347.1, II.0 et II.4 ; données `corpus/04_donnees/` | Écarts chiffrés avec barres d'erreur. Toute divergence est un résultat. |
| **DEFI-R4** | **La nucléation.** Le Blob peut-il naître du vide strict ? Aujourd'hui : 0/40 graines sous les deux moteurs canoniques. | Armature II.3, **RO-02** | Protocole **préenregistré** (publié avant exécution) sur ≥ 30 graines : P(Ω¹ \| Ω⁰) ≥ 0,9 depuis le vide strict, **ou** une borne négative propre. |
| **DEFI-R5** | **Le chasseur d'erreurs.** Trouvez une incohérence numérique entre un résultat publié (JSON) et le texte du master qui le cite. | `corpus/03_scripts/`, `corpus/06_campagnes_et_sauts/`, master V346 | Fichier, page, valeur citée, valeur réelle. |

## Niveau 2 — Mathématicien, physicien

| Code | Défi | Recherche ouverte | Ce qui compte comme réussite |
|---|---|---|---|
| **DEFI-M1** | **Les quatre points de SUP-1.** Degré borné contre O(log N), ordre des limites, 3-tore contre cube à bord, étiquettes (H1)–(H3) incohérentes. | [ETAT § 5](ETAT_DU_PROGRAMME.md) | Note de supersession qui tranche chacun des quatre points. |
| **DEFI-M2** | **La pince spectrale.** Le même objet peut-il satisfaire l'ellipticité uniforme exigée par Delmotte (INF-1) et le cadre non elliptique de SUP-1 ? | [Audit INF-1](corpus/02_portes_et_audits/audits_18-09-2026/) | Preuve que la pince se referme sur une classe explicite, **ou** obstruction démontrée. |
| **DEFI-M3** | **La fermeture.** La mitose seule ne produit jamais de triangle (no-go démontré). Proposez un générateur de fermeture **local** compatible avec la viabilité. | **RO-24** | Générateur explicite, ou preuve qu'aucun générateur local compatible n'existe (ce qui tuerait la cascade causale). |
| **DEFI-M4** | **Le bit σ₀.** Montrez que le choix de polarité à la première scission ne peut pas être dérivé de Ω⁰ et doit rester un axiome — ou dérivez-le. | **RO-03** | Théorème d'obstruction, ou mécanisme interne. |
| **DEFI-M5** | **La scission double.** Toute « scission en deux simplexes opposés » se réduit-elle à deux mitoses successives ? | **RO-04** | Réduction démontrée, ou nouvelle opération explicitée. |
| **DEFI-M6** | **Persister.** Donnez une définition de « persister » indépendante du simple fait que π > 0. | **RO-20** | Critère robuste, non arbitraire, calculable. |

## Niveau 3 — Spécialiste (porte G0)

| Code | Défi | Recherche ouverte |
|---|---|---|
| **DEFI-G1** | Marge locale uniforme sur le secteur typique de Gibbs (GEN-4 *typical-set*) | **RO-13** |
| **DEFI-G2** | Intertwiner MARKED ↔ CONNECTED dans une norme de Banach déclarée | **RO-14** |
| **DEFI-G3** | Convergence sous retrait du régulateur, limite projective | **RO-15** |
| **DEFI-G4** | Point fixe non trivial et universalité (C4, C5, C7) | **RO-16** |

## Le grand défi — le Tribunal ouvert

**DEFI-T0 — Cassez le Blob.** Trouvez une faille **fatale** : une contradiction interne, une hypothèse cachée qui fait tomber une branche entière, un résultat central non reproductible. Argumentez-la avec la rigueur d'un relecteur de revue.

Les réfutations retenues sont inscrites au **Mur des réfutateurs**, avec le nom de leur auteur, dans chaque version maîtresse qui en tient compte.

---

## Tableau d'honneur

| Date | Contributeur | Défi | Résultat | Effet sur le programme |
|---|---|---|---|---|
| 06/10/2026 | (vérification d'ouverture) | DEFI-R1 | `SELFTEST : 4/4` sur machine tierce, numpy 2.5.3 | Reproductibilité de l'auto-test confirmée |

## Mur des réfutateurs

*Vide à ce jour. Il n'attend que vous.*

---

### Ce que vous gagnez

- **Un crédit nominatif permanent** dans [CONTRIBUTEURS.md](CONTRIBUTEURS.md) et dans la version maîtresse qui intègre votre apport.
- **Une trace citable** : chaque version du dépôt reçoit un DOI Zenodo.
- La satisfaction d'avoir éprouvé une candidate à la théorie du tout — qu'elle tienne ou qu'elle tombe.
