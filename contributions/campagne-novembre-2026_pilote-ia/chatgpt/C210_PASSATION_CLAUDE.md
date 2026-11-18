# [CHATGPT-C210] Passation de contre-audit pour Claude

**Ne pas attribuer à l'auteur les modèles auxiliaires utilisés dans les preuves. Statut TOE 0/7.**

**Lecture prioritaire :** `RAPPORT_C210.md` puis `verification.py`.

**T1** : vérifier charge additive `q -> 2q`, condition d'isolation, borne `N <= (E+C)/epsilon`; identifier toute contre-hypothèse inutile.

**T2** : vérifier le témoin à 4 porteurs (arbre K4=0, fermeture K4=1, mêmes lignées et mêmes positions), volume `1/6`, conservation des flux antisymétriques et exemple du bilan avec bain. La preuve répond à *la question de nécessité logique* de RO-24, pas à sa clôture physique.

**T3** : vérifier théorème d'équivariance `F_t(gx)=gF_t(x)` sous unicité et symétrie initiale exacte. Chercher notamment si la constitution d'un *ensemble* de directions tétraédriques rompt SO(3) et quelles exceptions permettent la genèse.

**T4** : vérifier contre-modèle de Markov `(1,2)` versus `(10,20)`, même mesure stationnaire mais cinétique différente; vérifier que le rapport de balance détaillée ne fixe pas le préfacteur.

**T5** : vérifier la portée exacte du non-clonage : état quantique arbitraire et inconnu, pas transmission d'une disposition, d'un code classique ou d'une étiquette orthogonale.

**Objection centrale sollicitée :** fournir la plus petite hypothèse supplémentaire qui puisse rendre la fermeture volumique une conséquence (plutôt qu'une opération ajoutée), et montrer qu'elle n'encode pas la réponse. Si aucune n'est déductible, confirmer explicitement le no-go sans proposer un objectif numérique arbitraire.

**Ne pas présenter ces théorèmes classiques comme des découvertes de nouvelles lois physiques.** Aucune publication GitHub demandée ni effectuée.
