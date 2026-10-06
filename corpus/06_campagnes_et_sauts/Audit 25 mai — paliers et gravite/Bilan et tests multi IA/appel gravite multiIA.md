# APPEL À CONTRIBUTIONS MULTI-IA — LA GRAVITÉ DYNAMIQUE DU BLOB PRINCIPLE

**À : DeepSeek, Grok, Gemini, OpenAI.** Vous avez déjà contribué aux frontières ouvertes du Blob Principle. Voici un appel ciblé sur **la nature de la gravité**, accompagné d’un bilan exhaustif de tests déjà réalisés (document joint « bilan_gravite.md »). Lisez-le : il contient ce qui marche, ce qui a échoué, et pourquoi. Méthode imposée (rappel) : falsifiable, testable en numpy/scipy/networkx, nul de contrôle systématique (RGG pur, RGG régularisé, mobilité sans viabilité), interdiction d’injecter le résultat cherché dans l’instrument, zéro complaisance, zéro p-hacking.

## L’état des lieux (résumé du bilan joint)

**Établi [M], propre à la viabilité :**

1. Gravité = poussée au volume : le Blob ferme les tétraèdres 2,5× plus que les nuls (deux nuls identiques).
1. **Rapport de force tétra-tétra** : sous la dynamique, deux tétraèdres montrent un profil attraction/répulsion fonction de la distance — répulsion à courte distance (+0,064), distance d’équilibre (~0,10), attraction à grande distance (−0,002). Les paires non-matière n’ont pas ce profil. Les trois nuls restent positifs partout (jamais d’attraction). C’est propre à la viabilité.

**Testé et NON concluant (voies fermées honnêtement) :**

- La force ne dépend PAS de la configuration (orientation, asymétrie de masse/taille) à distance fixe : elle est centrale/isotrope, pas magnétique.
- Courbure locale (déficit de Regge : artefact de recouvrement des K₄ ; Forman-Ricci à degré contrôlé : la signature courbure∝matière existe dans le RGG mais DISPARAÎT dans le Blob).
- Déformation du substrat par la masse : profil de densité plat (pas de puits visible) ; mesure du « vide entre deux masses » cassée par manque de résolution.
- **Onde gravitationnelle** : exposant de propagation ≈0,03 pour Blob ET nul (la perturbation se stabilise localement, ne se propage pas ; ni onde ∝t, ni diffusion ∝√t). Léger excès de cohérence de front (2,84 vs 2,51) mais marginal.

## LA QUESTION CENTRALE

Il existe un **résultat statique solide** (force attraction/répulsion entre tétraèdres, propre à la viabilité). La vision de l’auteur (R. Mirante) insiste sur une **dynamique** : la gravité comme énergie qui se propage (onde, par analogie avec les ondes gravitationnelles détectées), une masse qui « pousse » le substrat de dimension 0. Mais aucun test de propagation n’a capté d’onde propre à la viabilité.

**Comment réconcilier la force statique mesurée (réelle) avec une éventuelle dynamique propagative ?** Quatre hypothèses concurrentes, à départager :

- (H1) L’observable est mauvais : la mobilité des positions de sommets n’est pas le bon véhicule d’une onde ; il faut un autre observable (ex. propagation d’une perturbation de *viabilité* ou de *connectivité*, pas de position).
- (H2) La taille est trop petite : N≤1200 ne laisse pas de place à un front propagatif ; le grand N (Colab) révélerait une onde.
- (H3) Le mécanisme est statique par nature : le Blob réalise une gravité « de configuration d’équilibre » (la matière se place à distance viable) sans propagation — et c’est un résultat en soi, pas un échec.
- (H4) L’onde existe mais dans un autre canal : la perturbation se propagerait via la *topologie* (réarrangement d’arêtes/triangles de proche en proche) plutôt que via la géométrie des positions.

## CE QUE NOUS VOUS DEMANDONS

Pour la gravité du Blob, proposez :

1. **Un observable de propagation que nous n’avons pas testé.** Le bilan montre que la propagation par déplacement de positions ne donne rien (exposant ≈0). Existe-t-il un canal de propagation plus naturel — perturbation de viabilité locale, d’énergie de déformation, de connectivité, de courbure — qui pourrait révéler une onde si elle existe ? Donnez le protocole précis (quoi perturber, quoi mesurer, comment extraire une vitesse/exposant).
1. **Comment distinguer proprement onde de diffusion** dans un graphe combinatoire, avec un critère qui ne soit pas réfutable comme artefact. (Le critère exposant 1 vs 0,5 est-il le bon ? Y a-t-il mieux — relation de dispersion ω(k), réversibilité, transport balistique ?)
1. **Le bon véhicule physique :** dans un modèle où la « matière » est un tétraèdre et le « substrat » un nuage de points, qu’est-ce qui devrait osciller/se propager pour qu’on parle d’onde gravitationnelle ? La métrique (distances) ? La densité ? La courbure ? La viabilité ?
1. **Votre verdict honnête sur H1–H4 :** laquelle est la plus probable ? Et si vous pensez que (H3) est correcte — que la gravité du Blob est statique/configurationnelle et qu’il n’y a pas d’onde à trouver — dites-le franchement. Une gravité statique propre à la viabilité (déjà mesurée) est un résultat ; une onde forcée serait un faux.
1. **Le piège spécifique à éviter** pour votre proposition, et le **critère de succès/échec chiffré**.

Proposez des angles **différents et complémentaires**. L’objectif : soit trouver le bon observable qui révèle une dynamique propagative (si elle existe), soit conclure proprement que la gravité du Blob est de nature statique/configurationnelle. Les deux issues sont acceptables ; seul un faux positif ne l’est pas.