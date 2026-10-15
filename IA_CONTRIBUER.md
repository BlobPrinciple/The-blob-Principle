🇫🇷 Français · 🇬🇧 [English version](en/AI_CONTRIBUTING.md)

# Contribuer au Blob avec une IA

Le Blob Principle a été construit avec plusieurs IA utilisées comme contradicteurs, jamais comme oracles. Le laboratoire accueille donc volontiers les contributions faites avec une IA (ChatGPT, Claude, Gemini, Mistral, Llama, DeepSeek ou toute autre), à une condition : **une personne vérifie et signe ce qui est soumis.**

> **TOE démontrée : NON** · portes physiques 0/7 · 27 recherches ouvertes. Une IA qui « confirme » le Blob ne prouve rien ; une IA qui aide à trouver une erreur, une preuve ou une réfutation vérifiable fait avancer le programme.

## En trois étapes

1. **Choisissez un défi** dans [DEFIS.md](DEFIS.md) ou dans sa version lisible par machine, [docs/defis.json](https://blobprinciple.github.io/The-blob-Principle/defis.json).
2. **Donnez à votre IA la consigne ci-dessous**, avec le défi choisi.
3. **Vérifiez vous-même le résultat**, puis déposez-le avec le modèle d'issue « Contribution assistée par IA ».

## Consigne à copier dans votre IA

```text
Tu participes au laboratoire public du Blob Principle (auteur : Rudolphe Mirante,
DOI 10.5281/zenodo.23188586). Statut déclaré : théorie du tout démontrée NON,
portes physiques 0/7, niveau 1 (modèle mathématique reproductible).

Sources qui font foi :
- Armature V347.1 (anglais) : https://github.com/BlobPrinciple/The-blob-Principle/blob/main/corpus/00_master_courant/EN/armature_V347-1_EN.md
- État du programme : https://github.com/BlobPrinciple/The-blob-Principle/blob/main/ETAT_DU_PROGRAMME.md
- Défis : https://blobprinciple.github.io/The-blob-Principle/defis.json

Fil conducteur du laboratoire : la cosmogonie du Blob, et comment la prouver.

Défi traité : DEFI-__ (recopier son énoncé).

Règles :
1. Travaille uniquement à partir des sources ci-dessus ; cite la section ou la ligne
   pour chaque affirmation sur le corpus. Si tu ne trouves pas, dis-le.
2. Étiquette chaque énoncé : [T] démontré, [M] mesuré, [H] hypothèse, [OPEN] ouvert.
3. Donne tout ce qui permet à un tiers de vérifier : calculs complets, code exécutable,
   commande, sortie attendue.
4. Une réfutation propre vaut autant qu'une preuve. Ne cherche pas à confirmer le Blob :
   cherche ce qui est vrai.
5. Termine par : ce qui est établi, ce qui reste à vérifier, et le point le plus fragile
   de ta propre réponse.
6. Rédige ensuite le texte complet d'une issue « Contribution assistée par IA », prêt à
   coller, avec ces champs : code du défi, modèle utilisé, consigne donnée, résultat
   étiqueté, éléments vérifiables, point le plus fragile, « Vérifié par » (laissé vide :
   la personne le remplit après vérification). Donne le lien pour la déposer :
   https://github.com/BlobPrinciple/The-blob-Principle/issues/new?template=5_contribution-ia.md
7. Indique enfin le prochain pas utile sur le chemin de preuve (champ proof_path de defis.json).
```

## Chaque session compte, même la vôtre

Une conversation avec une IA ne laisse aucune trace dans le laboratoire : l'IA lit le dépôt, elle n'y écrit pas. Ce qu'elle trouve n'existe pour le programme qu'une fois déposé dans une *issue*. Les règles 6 et 7 de la consigne servent à cela : chaque session se termine par une contribution prête à déposer et par la direction à suivre ensuite.

Cela vaut pour tous, **auteur compris** : les sessions de Rudolphe Mirante passent par le même modèle d'*issue* et par la même vérification que celles de n'importe quel contributeur. C'est ce qui donne sa valeur à une avancée inscrite au [journal des avancées](JOURNAL_DES_AVANCEES.md).

Ne vous arrêtez pas à une réponse. Si votre session a fermé une question, elle en a ouvert une autre : notez-la dans votre *issue*. Le Blob avance par cette chaîne-là.

## Ce que doit contenir une contribution

- le **modèle** utilisé (nom et version) et la **consigne** donnée ;
- le **nom de la personne** qui a vérifié le résultat ;
- les **éléments vérifiables** : fichiers réellement présents, valeurs retrouvables dans le corpus (fichier et ligne), commande qui reproduit le résultat ;
- le **point le plus fragile** de la contribution.

Les envois générés en série sans ces éléments sont fermés sans examen sur le fond (voir [CONTRIBUTING.md](CONTRIBUTING.md#5-ce-qui-ne-sera-pas-accepté)).

## Ce qui se passe ensuite

Chaque contribution est relue, rejouée quand elle contient du calcul, puis classée : **retenue** (inscrite au [journal des avancées](JOURNAL_DES_AVANCEES.md) et au tableau d'honneur ou au mur des réfutateurs, au nom de la personne qui l'a signée), **à compléter**, ou **non retenue**, avec la raison. Ce travail de vérification et d'aiguillage est confié au [pilote IA du laboratoire](PILOTE_IA.md). Une contribution retenue fait évoluer les défis : le défi traité change d'état, et un défi dérivé, plus proche du fil conducteur, est ouvert. Seul l'auteur du programme décide de ce qui entre dans le corpus et de tout changement de statut ([GOUVERNANCE.md](GOUVERNANCE.md)). Une contribution ne transfère aucun droit sur le Blob Principle ([PATERNITE.md](PATERNITE.md), [CLA.md](CLA.md)).
