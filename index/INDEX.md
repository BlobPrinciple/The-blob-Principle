# INDEX DU CORPUS — Blob Principle

*Établi le 24 September 2026.*

Deux fichiers d'index, à la racine du dossier :

- **`INDEX_CORPUS.csv`** — 10491 lignes, une par fichier. Colonnes : `source`, `version`, `nature`, `nom`, `chemin`, `octets`, `date`, `crc`. Ouvrable dans Numbers ou Excel : filtrable, triable, cherchable.
- **`INDEX.md`** — ce document : la carte des versions et le mode d'emploi.

Et deux documents de contexte : **`LEXIQUE.md`** pour le vocabulaire du corpus, **`LISEZ-MOI.md`** pour l'organisation et l'état des vérifications.

---

## Comment retrouver quelque chose

**Par version** — la carte plus bas donne, pour chacune des 219 versions repérées, où se trouve son master.

**Par nature** — filtrez la colonne `nature` du CSV :

| Nature | Fichiers | Ce que c'est |
|---|---:|---|
| `script` | 5 149 | Code Python de campagne |
| `donnees` | 1 741 | Sorties JSON |
| `verrou` | 650 | Tests numérotés de fermeture et leurs résultats |
| `master` | 619 | Le document principal  toutes versions |
| `texte` | 537 | Notes  audits  parties de manuscrit en .md |
| `pdf` | 394 | Rendus |
| `brique` | 338 | Unités de construction de preuve |
| `checkpoint` | 152 | États MCMC sauvegardés |
| `audit` | 140 | Auto-corrections AC-NN et rapports |
| `autre` | 136 | — |
| `palier` | 109 | Mesures à N fixé |
| `annexe` | 101 | Modules détachables |
| `livre` | 83 | Chapitres et volumes |
| `saut` | 74 | Avancées numérotées |
| `paper` | 59 | Articles courts |
| `manifeste` | 54 | Versions publiables courtes |

**Par mot** — le CSV se cherche au clavier. Le `LEXIQUE.md` explique ce que chaque terme du corpus désigne : verrou, brique, saut, palier, checkpoint, AC-NN, M2-W.

**Par contenu** — la colonne `crc` identifie un contenu indépendamment de son nom et de son emplacement. Deux lignes de même CRC sont le même fichier, au bit près. C'est l'outil de dédoublonnage et de contrôle d'intégrité.

---

## Les deux sources

**`disque`** — 3530 fichiers, directement lisibles dans les dossiers `00` à `10`.

**`archive-unifiee`** — 6961 entrées dans `92 ARCHIVE UNIFIEE/BLOB_ARCHIVE_UNIFIEE_2026-09-24.zip`. Cette archive de 560 Mo condense les 101 archives d'origine, qui pesaient 15,35 Go, **sans perdre un seul contenu** : 3 156 contenus distincts, comparés par CRC, intégrité confirmée.

**Les 101 archives d'origine restent dans `90 ARCHIVES ZIP`.** Rien n'a été supprimé.

---

## 46 versions n'existent QUE dans l'archive unifiée

Leur master n'est nulle part sur le disque. Pour les consulter, ouvrez l'archive.

V154, V164, V166, V167, V176, V180, V182, V183, V184, V189, V190, V196, V199, V204, V205, V206, V208, V210, V211, V212, V213, V214, V215, V221, V225, V228, V229, V234, V243, V256, V260, V265, V266, V273, V278, V279, V280, V283, V284, V285, V287, V288, V289, V290, V291, V292

---

## Carte des versions

| Version | Où | Exemple de chemin | Fichiers |
|---|---|---|---:|
| V67 | disque | `09 SAUVEGARDES/Archives Blob/blob v67 FULL MASTER.pdf` | 1 |
| V90 | disque | `09 SAUVEGARDES/Archives Blob/blob v90 MASTER.pdf` | 5 |
| V91 | disque | `10 DOCUMENTS EN VRAC/Masters et manuscrits/blob v91 MASTER.pdf` | 2 |
| V92 | disque | `02 VERSIONS (V92 a V197)/V142/archive_v142/donnees_json/verrou_1_1_HCP_connectome.json` | 18 |
| V99 | disque | `08 CAMPAGNES ET SAUTS/SAUT 9 et 10 et 11/Manifestes v99 et addendum v102/saut11_master` | 1 |
| V103 | disque | `09 SAUVEGARDES/Back up/blob v103 MASTER EXHAUSTIF.docx` | 4 |
| V107 | disque | `02 VERSIONS (V92 a V197)/V107/V107 exhaustive master.pdf` | 1 |
| V108 | disque | `02 VERSIONS (V92 a V197)/V108 autonomes/V108 master.pdf` | 6 |
| V109 | disque | `09 SAUVEGARDES/Manuscrits V109 a V135 — mai 2026/BlobPrinciple Master Autonome 17mai20` | 5 |
| V109plus | disque | `02 VERSIONS (V92 a V197)/V108 autonomes/Blob Principle V109plus master post cascade.pd` | 1 |
| V111 | disque | `08 CAMPAGNES ET SAUTS/Suite Cascade 17 mai/Suite blob graal 18 mai/BlobPrinciple Maste` | 2 |
| V112 | disque | `02 VERSIONS (V92 a V197)/V112/BlobPrinciple Master V112 18mai2026 VERROUILLE.pdf` | 2 |
| V113 | disque | `09 SAUVEGARDES/Manuscrits V109 a V135 — mai 2026/BlobPrinciple Master V113 18mai2026 V` | 2 |
| V114 | disque | `09 SAUVEGARDES/Manuscrits V109 a V135 — mai 2026/BlobPrinciple Master V114 LUCIDE 18ma` | 1 |
| V115 | disque | `09 SAUVEGARDES/Manuscrits V109 a V135 — mai 2026/BlobPrinciple Master V115 FINAL 18mai` | 1 |
| V117 | disque | `09 SAUVEGARDES/Manuscrits V109 a V135 — mai 2026/BlobPrinciple Master V117 DECOUVERTE ` | 1 |
| V120 | disque | `02 VERSIONS (V92 a V197)/V120/BlobPrinciple Master V120 19mai2026.pdf` | 1 |
| V121 | disque | `02 VERSIONS (V92 a V197)/V120/V121/BlobPrinciple Master V121 19mai2026.pdf` | 1 |
| V125 | disque | `02 VERSIONS (V92 a V197)/V125/BlobPrinciple Master V125 19mai2026.pdf` | 1 |
| V126 | disque | `02 VERSIONS (V92 a V197)/V126/BlobPrinciple Master V126 19mai2026.pdf` | 1 |
| V127 | disque | `02 VERSIONS (V92 a V197)/V127 finale/BlobPrinciple Master V127R AUTONOME 19mai2026.pdf` | 2 |
| V128 | disque | `02 VERSIONS (V92 a V197)/V128/BlobPrinciple Master V128R HONNETE 19mai2026.pdf` | 1 |
| V130 | disque | `09 SAUVEGARDES/Manuscrits V109 a V135 — mai 2026/BlobPrinciple Master V130 ULTIME 19ma` | 1 |
| V131 | disque | `09 SAUVEGARDES/Manuscrits V109 a V135 — mai 2026/BlobPrinciple Master V131 LesTroisCle` | 3 |
| V135 | disque | `09 SAUVEGARDES/Manuscrits V109 a V135 — mai 2026/BlobPrinciple Manuscrit V135 20mai202` | 2 |
| V137 | disque | `02 VERSIONS (V92 a V197)/V138/BlobPrinciple Master V137-IV COMPLET 21mai2026.pdf` | 4 |
| V137plus | disque | `02 VERSIONS (V92 a V197)/V138/BlobPrinciple Master V137plusplus COMPLET 21mai2026.pdf` | 1 |
| V138 | disque + archive | `02 VERSIONS (V92 a V197)/V138/BlobPrinciple Master V138 COMPLET 21mai2026.pdf` | 5 |
| V139 | disque + archive | `05 SCRIPTS/SCRIPTS DIVERS BLOB/BlobPrinciple Master V139 22mai2026.pdf` | 5 |
| V139plus | disque + archive | `02 VERSIONS (V92 a V197)/V139+/BlobPrinciple Master V139plus 22mai2026.pdf` | 5 |
| V140 | disque + archive | `02 VERSIONS (V92 a V197)/V140/BlobPrinciple Master V140 22mai2026.pdf` | 5 |
| V141 | disque + archive | `02 VERSIONS (V92 a V197)/V141/BlobPrinciple Master V141 23mai2026.pdf` | 7 |
| V141plus | disque + archive | `02 VERSIONS (V92 a V197)/V141/141+/BlobPrinciple Master V141plus 23mai2026.pdf` | 5 |
| V142 | disque + archive | `02 VERSIONS (V92 a V197)/V142/BlobPrinciple Master V142 23mai2026.pdf` | 7 |
| V144 | disque + archive | `02 VERSIONS (V92 a V197)/v143/BlobPrinciple Master V144 24mai2026.pdf` | 6 |
| V145 | disque + archive | `02 VERSIONS (V92 a V197)/V145/BlobPrinciple Master V145 24mai2026.pdf` | 5 |
| V146 | disque + archive | `02 VERSIONS (V92 a V197)/V146/BlobPrinciple Master V146 24mai2026.pdf` | 5 |
| V147 | disque + archive | `02 VERSIONS (V92 a V197)/V147/BlobPrinciple Master V147 24mai2026.pdf` | 5 |
| V150 | disque + archive | `02 VERSIONS (V92 a V197)/V150/BlobPrinciple Master V150 25mai2026.pdf` | 5 |
| V152 | disque + archive | `02 VERSIONS (V92 a V197)/V152/BlobPrinciple Master V152 25mai2026.pdf` | 17 |
| V153 | disque + archive | `02 VERSIONS (V92 a V197)/V153/BlobPrinciple Master V153 30mai2026.pdf` | 8 |
| V154 | **archive seule** | `v277_total/14_archive_v154/BlobPrinciple_Master_V154_2juin2026.md` | 6 |
| V155 | disque + archive | `02 VERSIONS (V92 a V197)/V155/BlobPrinciple Master V155 2juin2026.pdf` | 5 |
| V156 | disque + archive | `02 VERSIONS (V92 a V197)/V156/BlobPrinciple Master V156 2juin2026.pdf` | 4 |
| V157 | disque + archive | `02 VERSIONS (V92 a V197)/V157/BlobPrinciple Master V157 2juin2026.pdf` | 5 |
| V158 | disque + archive | `02 VERSIONS (V92 a V197)/V158/BlobPrinciple Master V158 3juin2026.pdf` | 2 |
| V159 | disque + archive | `02 VERSIONS (V92 a V197)/V159/BlobPrinciple Master V159 3juin2026.pdf` | 4 |
| V160 | disque + archive | `02 VERSIONS (V92 a V197)/V160/BlobPrinciple Master V160 3juin2026.pdf` | 3 |
| V161 | disque + archive | `02 VERSIONS (V92 a V197)/V161/BlobPrinciple Master V161 3juin2026.pdf` | 3 |
| V162 | disque + archive | `02 VERSIONS (V92 a V197)/V162/BlobPrinciple Master V162 3juin2026.pdf` | 3 |
| V163 | disque + archive | `02 VERSIONS (V92 a V197)/V163/BlobPrinciple Master V163 3juin2026.pdf` | 3 |
| V164 | **archive seule** | `v277_total/00_masters/BlobPrinciple_Master_V164_4juin2026.pdf` | 2 |
| V165 | disque + archive | `02 VERSIONS (V92 a V197)/V165/BlobPrinciple Master V165 4juin2026.pdf` | 3 |
| V166 | **archive seule** | `v277_total/00_masters/BlobPrinciple_Master_V166_4juin2026.pdf` | 2 |
| V167 | **archive seule** | `v277_total/00_masters/master_V167.md` | 2 |
| V168 | disque + archive | `02 VERSIONS (V92 a V197)/V168/BlobPrinciple Master V168 4juin2026.pdf` | 3 |
| V169 | disque + archive | `02 VERSIONS (V92 a V197)/V169/BlobPrinciple Master V169 4juin2026.pdf` | 3 |
| V170 | disque + archive | `02 VERSIONS (V92 a V197)/V170/BlobPrinciple Master V170 4juin2026.pdf` | 3 |
| V171 | disque + archive | `02 VERSIONS (V92 a V197)/V171/BlobPrinciple Master V171 4juin2026.pdf` | 3 |
| V172 | disque + archive | `02 VERSIONS (V92 a V197)/V172/BlobPrinciple Master V172 4juin2026.pdf` | 3 |
| V173 | disque + archive | `02 VERSIONS (V92 a V197)/V173/BlobPrinciple Master V173 4juin2026.pdf` | 3 |
| V174 | disque + archive | `02 VERSIONS (V92 a V197)/V174/BlobPrinciple Master V174 5juin2026.pdf` | 3 |
| V175 | disque + archive | `02 VERSIONS (V92 a V197)/V175/BlobPrinciple Master V175 5juin2026.pdf` | 3 |
| V176 | **archive seule** | `v277_total/00_masters/BlobPrinciple_Master_V176_5juin2026.pdf` | 2 |
| V177 | disque + archive | `02 VERSIONS (V92 a V197)/V177/BlobPrinciple Master V177 5juin2026.pdf` | 3 |
| V178 | disque + archive | `02 VERSIONS (V92 a V197)/V177/BlobPrinciple Master V178 5juin2026.pdf` | 4 |
| V179 | disque + archive | `02 VERSIONS (V92 a V197)/V178/BlobPrinciple Master V179 5juin2026.pdf` | 3 |
| V180 | **archive seule** | `v277_total/00_masters/BlobPrinciple_Master_V180_5juin2026.pdf` | 2 |
| V181 | disque + archive | `02 VERSIONS (V92 a V197)/V178/V181/BlobPrinciple Master V181 5juin2026.pdf` | 3 |
| V182 | **archive seule** | `v277_total/00_masters/master_V182.md` | 2 |
| V183 | **archive seule** | `v277_total/00_masters/BlobPrinciple_Master_V183_5juin2026.pdf` | 2 |
| V184 | **archive seule** | `v277_total/00_masters/BlobPrinciple_Master_V184_5juin2026.pdf` | 2 |
| V185 | disque + archive | `02 VERSIONS (V92 a V197)/V185/BlobPrinciple Master V185 5juin2026.pdf` | 3 |
| V186 | disque + archive | `02 VERSIONS (V92 a V197)/V186/BlobPrinciple Master V186 5juin2026.pdf` | 4 |
| V187 | disque + archive | `02 VERSIONS (V92 a V197)/V187/BlobPrinciple Master V187 6juin2026.pdf` | 3 |
| V188 | disque + archive | `02 VERSIONS (V92 a V197)/V189/master V188.pdf` | 2 |
| V189 | **archive seule** | `v277_total/00_masters/master_V189.md` | 1 |
| V190 | **archive seule** | `v277_total/00_masters/master_V190.md` | 1 |
| V191 | disque + archive | `02 VERSIONS (V92 a V197)/V191/master V191.pdf` | 2 |
| V192 | disque + archive | `02 VERSIONS (V92 a V197)/V192/master V192.pdf` | 2 |
| V193 | disque + archive | `02 VERSIONS (V92 a V197)/V193/master V193.pdf` | 2 |
| V194 | disque + archive | `02 VERSIONS (V92 a V197)/V194/master V194.pdf` | 2 |
| V195 | disque + archive | `02 VERSIONS (V92 a V197)/V195/master V195.pdf` | 2 |
| V196 | **archive seule** | `v277_total/00_masters/master_V196.md` | 1 |
| V197 | disque + archive | `02 VERSIONS (V92 a V197)/V197/master V197.pdf` | 2 |
| V198 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V198/master V198.pdf` | 2 |
| V199 | **archive seule** | `v277_total/00_masters/master_V199.md` | 1 |
| V200 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V200/master V200.pdf` | 3 |
| V201 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V201/master V201.pdf` | 3 |
| V202 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V202/master V202.pdf` | 3 |
| V203 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V203/master V203.pdf` | 3 |
| V204 | **archive seule** | `v277_total/00_masters/master_V204.md` | 2 |
| V205 | **archive seule** | `v277_total/00_masters/master_V205.pdf` | 2 |
| V206 | **archive seule** | `v277_total/00_masters/master_V206.pdf` | 2 |
| V207 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V207/master V207.pdf` | 3 |
| V208 | **archive seule** | `v277_total/00_masters/master_V208.md` | 2 |
| V209 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V209/master V209.pdf` | 3 |
| V210 | **archive seule** | `v277_total/00_masters/master_V210.pdf` | 2 |
| V211 | **archive seule** | `v277_total/00_masters/master_V211.md` | 2 |
| V212 | **archive seule** | `v277_total/00_masters/master_V212.md` | 2 |
| V213 | **archive seule** | `v277_total/00_masters/master_V213.pdf` | 2 |
| V214 | **archive seule** | `v277_total/00_masters/master_V214.md` | 2 |
| V215 | **archive seule** | `v277_total/00_masters/master_V215.pdf` | 2 |
| V216 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V216/master V216.pdf` | 3 |
| V217 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V217/master V217.pdf` | 3 |
| V218 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V218/master V218.pdf` | 3 |
| V219 | disque | `01 MASTERS (filiation PDF)/MASTERS/V219/Blob Master V219.pdf` | 1 |
| V220 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V220/Blob Master V220.pdf` | 4 |
| V221 | **archive seule** | `v277_total/00_masters/master_V221.md` | 2 |
| V222 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V222/Blob Master V222.pdf` | 3 |
| V223 | disque + archive | `05 SCRIPTS/SCRIPTS DIVERS BLOB/Blob Master V223.pdf` | 3 |
| V224 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V224/Blob Master V224.pdf` | 8 |
| V225 | **archive seule** | `v277_total/00_masters/master_V225_complet.md` | 9 |
| V226 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V226/Blob Master V226 complet.pdf` | 6 |
| V227 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V227/Blob Master V227 complet.pdf` | 4 |
| V228 | **archive seule** | `v277_total/_grave_v228/master_V228_complet_full.md` | 3 |
| V229 | **archive seule** | `v277_total/master_V229_complet_full.md` | 3 |
| V230 | disque + archive | `05 SCRIPTS/SCRIPTS DIVERS BLOB/Blob Master V230 complet.pdf` | 4 |
| V231 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V231/Blob Master V231 complet.pdf` | 9 |
| V232 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V232/Blob Master V232 complet.pdf` | 3 |
| V233 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V233/Blob Master V233 complet.pdf` | 3 |
| V234 | **archive seule** | `v277_total/Blob_Master_V234_complet.pdf` | 2 |
| V235 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V235/Blob Master V235 complet.pdf` | 3 |
| V236 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V236/LE BLOB V236 master complet.pdf` | 4 |
| V237 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V237/master V237 complet full.pdf` | 3 |
| V238 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V238/master V238 complet full.pdf` | 3 |
| V239 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V239/master V239 complet full.pdf` | 3 |
| V240 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V240/Blob Master V240 complet.pdf` | 4 |
| V241 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V241/Blob Master V241 complet.pdf` | 3 |
| V242 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V242/master V242 complet full.pdf` | 4 |
| V243 | **archive seule** | `v277_total/00_masters/master_V243_complet_full.pdf` | 3 |
| V244 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V244/master V244 complet full.pdf` | 4 |
| V245 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V245/master V245 complet full.pdf` | 4 |
| V246 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V246/master V246 complet full.pdf` | 4 |
| V247 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V247/master V247 complet full.pdf` | 4 |
| V248 | disque | `01 MASTERS (filiation PDF)/MASTERS/master V248 complet full.pdf` | 1 |
| V249 | disque | `01 MASTERS (filiation PDF)/MASTERS/V249/master V249 complet full.pdf` | 1 |
| V250 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V250/master V250 complet full.pdf` | 2 |
| V251 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V251/master V251 complet full.pdf` | 2 |
| V252 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V252/master V252 complet full.pdf` | 2 |
| V253 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V253/master V253 complet full.pdf` | 2 |
| V254 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V254/master V254 complet full.pdf` | 2 |
| V255 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V255/master V255 complet full.pdf` | 2 |
| V256 | **archive seule** | `v277_total/master_V256_complet_full.pdf` | 1 |
| V257 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V257/master V257 complet full.pdf` | 2 |
| V258 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V258/master V258 complet full.pdf` | 2 |
| V259 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V259/master V259 complet full.pdf` | 2 |
| V260 | **archive seule** | `v277_total/master_V260_complet_full.pdf` | 1 |
| V261 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V261/master V261 complet full.pdf` | 2 |
| V262 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V262/master V262 complet full.pdf` | 2 |
| V263 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V263/master V263 complet full.pdf` | 2 |
| V264 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V264/master V264 complet full.pdf` | 2 |
| V265 | **archive seule** | `v277_total/master_V265_complet_full.pdf` | 1 |
| V266 | **archive seule** | `v277_total/master_V266_complet_full.pdf` | 1 |
| V267 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V267/master V267 complet full.pdf` | 2 |
| V268 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V268/master V268 complet full.pdf` | 2 |
| V269 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/master V269 complet full.pdf` | 2 |
| V270 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V270/master V270 complet full.pdf` | 2 |
| V271 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V271/master V271 complet full.pdf` | 2 |
| V272 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V272/master V272 complet full.pdf` | 2 |
| V273 | **archive seule** | `v277_total/master_V273_complet_full.pdf` | 1 |
| V274 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V274/master V274 complet full.pdf` | 2 |
| V275 | disque | `01 MASTERS (filiation PDF)/MASTERS/V275/master V275 complet full.pdf` | 1 |
| V276 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V276/master V276 complet full.pdf` | 2 |
| V277 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V277/master V277 complet full.pdf` | 18 |
| V277bis | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V277 bis/master V277bis complet full.pdf` | 5 |
| V278 | **archive seule** | `v277_total/master_V278_body.md` | 3 |
| V279 | **archive seule** | `v277_total/master_V279_final.pdf` | 3 |
| V280 | **archive seule** | `v277_total/master_V280_final.pdf` | 3 |
| V281 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V281/master V281 complet full.pdf` | 4 |
| V282 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V282/master V282 complet full.pdf` | 4 |
| V283 | **archive seule** | `v277_total/tome_V283.md` | 3 |
| V284 | **archive seule** | `v277_total/V282_z2/tome_V284.md` | 3 |
| V285 | **archive seule** | `v277_total/tome_V285.md` | 3 |
| V287 | **archive seule** | `v277_total/tome_V287.md` | 3 |
| V288 | **archive seule** | `v277_total/master_V288_final.pdf` | 3 |
| V289 | **archive seule** | `v277_total/tome_V289.md` | 3 |
| V290 | **archive seule** | `v277_total/master_V290_final.pdf` | 3 |
| V291 | **archive seule** | `v277_total/tome_V291.md` | 3 |
| V292 | **archive seule** | `v277_total/master_V292_final.pdf` | 3 |
| V293 | disque + archive | `01 MASTERS (filiation PDF)/MASTERS/V293/tome V293.pdf` | 5 |
| V295 | disque | `01 MASTERS (filiation PDF)/MASTERS/V295/master V295 complet full.pdf` | 1 |
| V296 | disque | `01 MASTERS (filiation PDF)/MASTERS/V296/master V296 complet full.pdf` | 1 |
| V297 | disque | `01 MASTERS (filiation PDF)/MASTERS/V297/master V297 complet full.pdf` | 1 |
| V298 | disque | `01 MASTERS (filiation PDF)/MASTERS/V298/master V298 complet full.pdf` | 1 |
| V299 | disque | `01 MASTERS (filiation PDF)/MASTERS/V299/master V299 complet full.pdf` | 1 |
| V300 | disque | `01 MASTERS (filiation PDF)/MASTERS/V300/master V300 complet full.pdf` | 1 |
| V302 | disque | `01 MASTERS (filiation PDF)/MASTERS/V302/master V302 complet full.pdf` | 1 |
| V303 | disque | `01 MASTERS (filiation PDF)/MASTERS/V303/master V303 complet full.pdf` | 1 |
| V304 | disque | `01 MASTERS (filiation PDF)/MASTERS/V304/master V304 complet full.pdf` | 1 |
| V306 | disque | `01 MASTERS (filiation PDF)/MASTERS/V306/master V306 complet full.pdf` | 1 |
| V307 | disque | `01 MASTERS (filiation PDF)/MASTERS/V307/master V307 complet full.pdf` | 1 |
| V308 | disque | `01 MASTERS (filiation PDF)/MASTERS/V308/master V308 complet full.pdf` | 1 |
| V311 | disque | `04 PORTES ET AUDITS/RELEVE GO BLOB PORTES/V311/master V311 complet full.pdf` | 1 |
| V315 | disque | `04 PORTES ET AUDITS/RELEVE GO BLOB PORTES/V315/master V315 complet full.pdf` | 1 |
| V316 | disque | `04 PORTES ET AUDITS/RELEVE GO BLOB PORTES/master V316 complet full.pdf` | 1 |
| V319 | disque | `04 PORTES ET AUDITS/RELEVE GO BLOB PORTES/master V319 complet full.pdf` | 1 |
| V321 | disque | `01 MASTERS (filiation PDF)/MASTERS/V321/master V321 complet full.pdf` | 1 |
| V322 | disque | `01 MASTERS (filiation PDF)/MASTERS/V322/master V322 complet full.pdf` | 1 |
| V323 | disque | `01 MASTERS (filiation PDF)/MASTERS/V323/master V323 complet full.pdf` | 1 |
| V325 | disque | `01 MASTERS (filiation PDF)/MASTERS/V325/master V325 complet full.pdf` | 1 |
| V326 | disque | `01 MASTERS (filiation PDF)/MASTERS/V326/master V326 1 complet full.pdf` | 2 |
| V327 | disque | `01 MASTERS (filiation PDF)/MASTERS/V327/master V327 complet full.pdf` | 1 |
| V329 | disque | `01 MASTERS (filiation PDF)/MASTERS/V329/master V329 complet full.pdf` | 1 |
| V330 | disque | `01 MASTERS (filiation PDF)/MASTERS/master V330 complet full.pdf` | 1 |
| V331 | disque | `01 MASTERS (filiation PDF)/MASTERS/master V331 complet full.pdf` | 1 |
| V333 | disque | `01 MASTERS (filiation PDF)/MASTERS/master V333 complet full.pdf` | 1 |
| V334 | disque | `01 MASTERS (filiation PDF)/MASTERS/master V334 complet full.pdf` | 1 |
| V335 | disque | `01 MASTERS (filiation PDF)/master V335 complet full.pdf` | 1 |
| V338 | disque | `01 MASTERS (filiation PDF)/master_V338_complet_full.pdf` | 1 |
| V339 | disque | `01 MASTERS (filiation PDF)/master_V339_complet_full.pdf` | 1 |
| V340 | disque | `01 MASTERS (filiation PDF)/master_V340_complet_full.pdf` | 1 |
| V341 | disque | `01 MASTERS (filiation PDF)/master_V341_complet_full.pdf` | 1 |
| V342 | disque | `01 MASTERS (filiation PDF)/master_V342_complet_full.pdf` | 1 |
| V343 | disque | `01 MASTERS (filiation PDF)/master_V343_complet_full.pdf` | 1 |
| V344 | disque | `01 MASTERS (filiation PDF)/master_V344_complet_full.pdf` | 1 |
| V345 | disque | `01 MASTERS (filiation PDF)/master_V345_complet_full.pdf` | 1 |
| V346 | disque | `00 COURANT/master_V346_complet_full.pdf` | 1 |
| V347 | disque | `00 COURANT/BLOB_PRINCIPLE_MASTER_V347_1_ARMATURE_CANONIQUE.pdf` | 1 |

---

## Ce que l'index ne couvre pas

- Les **versions V294 à V346** n'ont jamais été archivées. Leurs masters PDF sont dans `01 MASTERS (filiation PDF)`, mais aucun jeu de scripts et de données ne leur correspond.
- Le **master courant est V346** — 1 918 pages, dans `00 COURANT`. V347.1 est une armature de 29 pages, pas un master.
- Les fichiers **`.pkl`** de la campagne D87 sont des binaires opaques : l'index donne leur taille et leur date, pas leur contenu.
