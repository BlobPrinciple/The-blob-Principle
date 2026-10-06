# THE BLOB PRINCIPLE — organisation du corpus

*Rangé le 24 septembre 2026. Archives vérifiées intégralement le même soir. Voir `LEXIQUE.md` pour le vocabulaire.*

---

## Où se trouve quoi

| Dossier | Fichiers | Volume | Contenu |
|---|---:|---:|---|
| `00 COURANT` | 3 | 0,01 Go | Master **V346** (1 918 p.), armature V347.1, section V345 |
| `01 MASTERS (filiation PDF)` | 110 | 0,56 Go | V248 → V346 |
| `02 VERSIONS (V92 a V197)` | 2 169 | 0,18 Go | 56 versions, scripts et données de campagne |
| `03 LIVRES` | 93 | 0,02 Go | *Le Blob Surnaturel*, *Du simplexe au complexe*, dossier Odile Jacob |
| `04 PORTES ET AUDITS` | 36 | 0,07 Go | Les 7 portes, théorèmes M2-W, scripts de vérification |
| `05 SCRIPTS` | 130 | 0,03 Go | Colab et simulations |
| `06 DONNEES` | 11 | 0,00 Go | Invariants 500k, universalité, paliers |
| `07 PARADIGMES TECHNOLOGIQUES` | 220 | 0,04 Go | HYDROSCOPE-IT, SILENTIA-PS, VIATRON-S, campagne D87 |
| `08 CAMPAGNES ET SAUTS` | 186 | 0,01 Go | Sauts 1 à 36, scaling V30, cascade, O2v4, ALPHA, BANC |
| `09 SAUVEGARDES` | 312 | 0,16 Go | Archives Blob, back-ups de mai, manuscrits V109–V135 |
| `10 DOCUMENTS EN VRAC` | 74 | 0,03 Go | Classés en onze rubriques |
| `90 ARCHIVES ZIP` | 101 | 15,35 Go | Les archives totales — **analysées, voir ci-dessous** |
| `91 CONTENUS UNIQUES (absents de V293)` | 156 | 0,06 Go | **Sauvetage** — ce que V293 ne contient pas |

---

## Vérification intégrale des archives — 24 septembre 2026

**Les 101 archives ont été téléchargées d'iCloud et ouvertes une par une.** Comparaison par **CRC**, pas par nom de fichier : chaque archive préfixe son contenu par son propre dossier racine, et **V157 change de structure** en imbriquant les archives antérieures. Une comparaison par chemin conclut faussement à l'absence de tout recouvrement.

### Les chiffres

- **392 450 entrées** dans les 101 archives, pour seulement **3 156 contenus distincts**. Facteur de redondance : **124**.
- **V293**, la plus récente et la plus grosse, contient **3 000 contenus sur 3 156 — 95,1 %**.
- **156 contenus ne sont dans aucune archive postérieure.** Ils pèsent 59,4 Mo décompressés.

### La loi, et son exception

Une archive V_n est intégralement contenue dans les archives postérieures, **sauf son propre master et son index** — chaque archive abandonne le master de la précédente. Vérifié sur V138⊂V142, V153⊂V157, V155⊂V157, V156⊂V157, V188⊂V191.

**L'exception :** entre V142 et V153, neuf fichiers disparaissent au-delà de cette règle — parties XV, XVII et XVIII du manuscrit, `consolidation_T.md`, `mitose.py`, les deux documents V139+. Tous retrouvés décompressés dans les dossiers de version. Aucune perte réelle, mais la preuve qu'une suppression en bloc en aurait causé une.

### Réponse : non, la dernière archive ne porte pas toute l'évolution

Les 156 contenus absents de V293 se répartissent ainsi :

| Nature | Nombre |
|---|---:|
| Scripts `.py` | 37 |
| **Masters du corpus** | **34** |
| Fichiers `.txt` | 31 |
| Textes `.md` | 27 |
| Données `.json` | 14 |
| `.pdf` | 8 |
| Autres | 5 |

Les 34 masters absents couvrent une plage continue : **V138, V139, V139plus, V140, V141, V141plus, V142, V144, V145, V146, V147, V150, V152** — sources `.md` et rendus `.pdf` — plus V159, V220, V224, V231 et V277.

**Et les archives s'arrêtent à V293, le 30 juillet.** Les cinquante-trois versions suivantes, V294 à V346, n'ont aucune archive.

### Le sauvetage

Les 156 contenus ont été extraits dans `91 CONTENUS UNIQUES (absents de V293)`, rangés par archive d'origine. **Vérification indépendante : les CRC ont été recalculés sur les fichiers écrits, pas repris de l'extraction.** V293 plus ces 156 fichiers redonnent exactement les 3 156 contenus de l'univers. **Contenus perdus : zéro.**

### Ce que la suppression libère

| | |
|---|---:|
| Archives actuelles | 15,35 Go |
| À conserver — V293 seule | 0,52 Go |
| Sauvetage ajouté | 0,06 Go |
| **Libérable** | **14,83 Go** (gain net 14,77 Go) |

Les cent archives autres que V293 sont, après ce sauvetage, **intégralement redondantes**.

---

## Deux points d'hygiène

**Le corpus vit dans iCloud.** Avant le 24 septembre, 3 224 fichiers sur 3 445 étaient déshydratés : une sauvegarde du Bureau n'aurait copié que des coquilles vides. Ils sont désormais sur le disque. **Faites une copie froide sur disque externe avant toute suppression.**

**Le Finder signale : « Impossible d'achever la synchronisation avec iCloud Drive. Réparez les autorisations pour… »** Le bouton « Réparer » n'a pas été actionné — c'est une modification d'autorisations système. Tant que la synchronisation ne s'achève pas, le rangement n'est pas garanti répercuté sur iCloud.

---

## Ce qui reste ouvert côté science

Le master V346 porte **quatre verdicts simultanés sur SUP-1**, du « frontière ouverte » en tête au « SUP-1 EST FERMÉ » de la partie CLXXVI datée du 18 juillet 2026. Le dernier fait foi ; rien ne le signale au lecteur qui commence page 1.

Quatre points d'audit attendent un feu vert :

1. (H1) pose un degré **borné** ; sa vérification fournit un degré en **O(log N)**.
2. L'ordre des limites n'est pas spécifié — à N fini, t → ∞ donne un exposant nul.
3. Le théorème vit sur un 3-tore ; le moteur v137 tourne sur un cube à bord.
4. L'étiquette (H1)–(H3) désigne quatre triplets différents dans le même document.
