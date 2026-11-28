# Registre de lecture — relecture intégrale demandée le 28 novembre 2026

**Rédigé par Claude, pilote IA.** Auteur du Blob Principle : Rudolphe Mirante.

Parole de l'auteur (28 novembre, 6 h 29) : « Tu vas relire chaque master, les 347, en entier, pour t'assurer de ne rien avoir abandonné trop tôt ou minimisé dans nos résultats, puis les trois versions de la cosmogonie, et ensuite tu refais un point complet, car je sais à présent que tu as sous-exploité tout le travail réalisé et minimisé la force de ma cosmogonie ! Tu relis tous les vrais masters et tous les vrais livres, pas de résumé ! Et tout le laboratoire GitHub ! »

## Correction d'inventaire (28 novembre, en cours de lecture)

**Mon premier inventaire était faux.** Je n'avais compté que les dossiers `00_master_courant` et `01_masters_jalons`, et j'avais écrit « le dépôt ne contient que 7 masters ». Le relevé complet, fait par programme (`outils/extraire_tout.py`, sortie `outils/volume_du_depot.out`), donne ceci.

| Document | Dossier | Mots | Texte absent de V346 |
|---|---|---|---|
| Manifestes v93.5, v96, v99.1, addendum v102, article v30 | `corpus/06` | ≈ 20 000 | distincts, à lire |
| Master V111 (18 mai) | `corpus/06` | 72 896 | ≈ 500 mots de prose |
| Master V139 (22 mai) | `corpus/03` | 128 680 | ≈ 1 240 mots de prose |
| Master V152 (25 mai) | `corpus/03` | 202 816 | ≈ 1 410 mots de prose |
| Master V152 (29 mai) | `corpus/03` | 206 268 | ≈ 1 400 mots de prose |
| Master V155 (2 juin) | `corpus/03` | 231 923 | ≈ 1 490 mots de prose |
| Master V223 | `corpus/03` | 320 383 | ≈ 3 150 mots de prose |
| Master V230 complet | `corpus/03` | 343 262 | ≈ 1 540 mots de prose |
| Masters V311, V315, V316, V319 | `corpus/01` | 442 579 à 465 514 | 0 |
| Section V345 | `corpus/00` | 2 232 | 0 |
| **Master V346 complet** | `corpus/00` | 576 681 | — |
| Armature V347.1 | `corpus/00` | 14 135 | distincte, à lire |
| « Blob MASTER PROPRE LIVRE » | `corpus/03` | 53 070 | distinct, à lire |
| Corpus maître unique G0 (3 août, 5 442 pages) | `corpus/02` | 1 260 330 | incorpore V319 et 218 fichiers de données et de code ; ≈ 63 000 mots de phrases hors V346, à lire |

Le dépôt contient donc **13 masters et 4 manifestes**, non 7. L'index du corpus en répertorie 220 (V67 à V347) ; les autres restent hors du dépôt.

**Contrôle de contenance** (`outils/contenance_lettres.py`, sortie `outils/contenance_dans_V346.out`) : chaque phrase est comparée à V346 sur ses seules lettres, ce qui neutralise la mise en lignes, les numéros de page et les ligatures. Résultat : V311 à V319 et V345 sont dans V346 à 100 %. Pour V111 à V230, ce qui n'est pas retrouvé est fait de formules et de tableaux composés autrement, plus **260 phrases de prose distinctes, ≈ 4 700 mots**, rassemblées pour être lues. Exemple vérifié à la main : V139 écrit « inscrire cette tentative comme un échec définitif » ; V346 écrit « comme une voie exploratoire non concluante ». V346 est donc cumulatif, à des reformulations près, que je lirai.

**Volume du dépôt, doublons exacts retirés** (mots) : PDF 6 123 000, dont ≈ 3 700 000 de masters contenus dans V346 ; Word 596 000 (mêmes textes que les PDF des livres, pour l'essentiel) ; Markdown 706 000 ; texte 143 000 ; code 389 000 ; données (JSON, sorties, CSV) 2 221 000 unités, inventoriées et non lues ligne à ligne. **Prose restant à lire après V346 : de l'ordre de 1,9 million de mots.** Mon estimation précédente (livres 465 000, laboratoire 270 000) était trop basse d'un facteur 2 à 3 : elle omettait `corpus/02` à `corpus/07`, les cinq tomes du Blob Surnaturel et les contributions antérieures.

## Ce qui manque encore

1. Les masters hors du dépôt (index : 220 ; dépôt : 13 et 4 manifestes). La demande d'accès au dossier du Mac de l'auteur a été refusée par le garde-fou de la session ; je ne la contourne pas. Sur Zenodo ne figurent que les versions du dépôt.
2. Les sources que le master cite et que je n'ai trouvées dans aucun fichier du dépôt à ce stade : v91, v92 et v105 (« Paper A ») ; l'archive « BlobPrinciple_V138_archive_complete.zip ». Conséquence : les démonstrations de T7.3 (T28) et T7.4 (T29), dites « reproduites en annexe A1 », ne sont pas dans l'annexe A1 du master. À rechercher dans le livre annexe et les manifestes pendant leur lecture.
3. Une lecture n'est déclarée faite que page par page, ci-dessous. Rien n'est conclu d'un document tant que sa ligne n'est pas complète.

## Ordre de lecture

1. Master V346, pages restantes.
2. Les 260 phrases des masters antérieurs absentes de V346 ; « MASTER PROPRE LIVRE » ; armature V347.1 ; manifestes v93.5 à v102 et article v30.
3. Les livres : Du simplexe au complexe (Livre 1, révision du 17 mai, Livres 2 et 3, livre annexe), édition 2026, Le Blob Surnaturel (V1, cinq tomes de V2, V3).
4. Le laboratoire : `corpus/02` à `corpus/07` (portes, audits, scripts, sauts, protocoles), contributions R3 à RO-25, campagne de novembre, documents de la racine, débats, index.
5. Le point complet, écrit seulement quand la lecture qui le porte est finie.

## État de la lecture

| Document | Pages | Lu | Notes |
|---|---|---|---|
| Master V346 complet | 1 918 | 1 à 1 891 | `NOTES_V346.md` |
