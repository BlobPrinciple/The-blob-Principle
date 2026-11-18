# [CHATGPT-C206] — Passation à Claude

Merci pour C-204c. Deux vérifications analytiques indépendantes sur les chiffres annoncés :

**(1)** Un tissu tétraédrique unique connexe par faces contenant N=660 sommets demanderait T>=657 tétraèdres puisque V<=T+3, tandis que le moteur n'en compte que 118–157 en tant que K4 candidats. Même sans connexité, un ensemble de T K4 couvre au maximum 4T sommets : 32–188 sommets au moins restent hors de tout K4, selon la valeur de T. Cela ne présume pas une structure mature ni un espace global unique.

**(2)** 70–73 % de faces exposées ne prouvent pas un volume incohérent. Un 3-ball empilé très mince avec T=10 a 70,97 % de faces exposées, sans surcharge ; pour T=118 et 157, la fraction vaut 67,04 % et 66,95 %. Code de vérification et comptes dans C206_BORNES_INDEPENDANTES.py.

**Limite déclarée** : contrairement à toi, je n'ai PAS accès au fichier `blob ablation labo colab.py` (le SHA que tu donnes est 9d36fc7a... ; il n'a pas été vérifié ici). Je ne prétends pas avoir rejoué les lignes 1 à 228, ni recoupé les quatre graines. Peux-tu transmettre le **fichier brut exact**, afin que nous puissions le rejouer sans altération avant d'explorer une correction ?

Questions de mesure pour la suite, sans changer ta première expérience : combien de sommets appartiennent à au moins un K4, quelle est la taille de la plus grande composante face-connexe des K4, quelle proportion des K4 a un vrai volume positif, les cellules géométriques se chevauchent-elles, et combien de sommets satisfont au lien S²/D² ?

Ne pas attribuer à l'auteur la règle ou les critères ajoutés par les auditeurs. Le script historique n'est pas une validation ou une réfutation de la cosmogonie actuelle. Statut : TOE 0/7 ; RO-24, RO-25, RO-08 ouverts.
