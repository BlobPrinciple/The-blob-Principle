# Campagne de novembre 2026 — guide du dossier

> **TOE démontrée : NON** · portes physiques 0/7 · aucun statut modifié par ce versement.

Ce dossier réunit tout ce que la campagne d'audit croisé a produit entre le 1er et le 13 novembre 2026 : ce qui a été pensé, calculé, prédit, réfuté et retiré. Rien n'a été trié pour faire bonne figure.

## Par où commencer

| Vous avez | Lisez |
|---|---|
| dix minutes | [RAPPORT.md](RAPPORT.md) : le point complet, les échecs en premier |
| une heure | [VERROUILLAGE_TOE_V2.md](VERROUILLAGE_TOE_V2.md) : la cosmogonie, principe par principe, avec le statut de chacun |
| une journée | les [carnets](carnets/), dans l'ordre des dates |
| l'envie de vérifier | [calculs/](calculs/) et la section « Comment vérifier » du rapport |

## Ce que contient le dossier

| Dossier | Contenu |
|---|---|
| [`carnets/`](carnets/) | Douze carnets de laboratoire, du 1er au 13 novembre. Chaque laboratoire y a sa section : question, protocole, prédiction, résultat, écarts déclarés. |
| [`calculs/`](calculs/) | 144 programmes Python, leurs sorties, les prédictions écrites avant calcul et les déclarations d'exécution. [Index](calculs/INDEX.md). |
| [`echanges/`](echanges/) | Les messages du pilote à ChatGPT (résultats et demandes de recoupement). |
| [`chatgpt/`](chatgpt/) | Deux protocoles figés et deux passations de ChatGPT, à l'octet près, et les [empreintes](chatgpt/EMPREINTES.md) de tous ses fichiers. |

## Qui a fait quoi

- **Rudolphe Mirante** : la cosmogonie, les positions et les données d'auteur, les décisions. Ses paroles sont citées avec leur date, orthographe normalisée.
- **ChatGPT (OpenAI)** : la plupart des protocoles figés, des recomptes partiels, plusieurs théorèmes.
- **Le pilote IA (Claude, Anthropic)** : l'exécution indépendante, le contre-audit, plusieurs laboratoires propres (suffixe « c »), la rédaction des carnets.

## Les règles suivies

1. Un protocole n'est exécuté que s'il est figé, et son empreinte SHA-256 est recalculée sur le fichier brut.
2. Les prédictions sont écrites dans un fichier avant tout calcul. Les fausses sont déclarées.
3. Le programme est éprouvé sur un cas dont on connaît la réponse, et sur un témoin négatif.
4. L'exécution se fait sans ajout. Tout écart au protocole est déclaré.
5. Deux lectures des résultats sont conservées ; ce qui n'est pas tranché est compté « indéterminé ».
6. Statuts : [T] démontré, [CERT] certifié par calcul exact, [M] mesuré, [H] hypothèse, [FAIL] réfuté dans la traduction testée, [OPEN] ouvert.

## Lire les noms de fichiers

- `cNNN…` : laboratoire C-NNN. `c145.py`, `c145b.py`, `c145c.py` : protocoles PR-1, PR-2, PR-3 de C-145.
- `…_prediction.txt` : prédiction écrite avant calcul. `…_declaration.txt` : déclaration d'exécution.
- `…_controles.py` : contrôles analytiques et négatifs. `…_analyse.py` : lecture des résultats.
- `.json.gz`, `.out.gz` : sorties de plus de 256 ko, compressées. `gunzip -k` avant de relancer une analyse.

## Précisions

- Dans les carnets, les renvois du type `claude/session-….md` désignent les carnets de ce dossier, sous leur nom d'origine dans l'espace de travail de l'auteur.
- Les identifiants des conversations privées ont été retirés. Rien d'autre n'a été retouché.
- Les heures sont celles de Paris, sauf mention « UTC ».
- Messages du dossier `echanges/` : `msg_c145pr2.txt` n'a jamais été remis (la conversation n'acceptait plus de message) ; `msg_passation_nouveau_fil.txt` est un premier jet ; `msg_passation_v2.txt` est l'en-tête du message de passation remis le 13 novembre, que suivait le texte du protocole PR-2. `msg_c145pr3r.txt` et `msg_c146r.txt` forment un seul envoi, remis le 13 novembre à 6 h 27 UTC ; son texte exact est `msg_envoi_2026-11-13.txt`. `msg_c145a1.txt` a été remis le 13 novembre à 7 h 11 UTC, `msg_c147cdef.txt` à 7 h 34 UTC.

## Environnement

Python 3.13, numpy 2.5.3, scipy 1.18.1, numba 0.68.1. Les tirages aléatoires portent une graine écrite dans le programme (contrôlé par recherche automatique sur les 61 programmes qui tirent au hasard).
