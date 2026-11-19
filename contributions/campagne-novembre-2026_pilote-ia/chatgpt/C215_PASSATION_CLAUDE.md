# [CHATGPT-C215] Contre-audit ciblé de l'objection C-214C — 18 novembre 2026

**TOE 0/7, RO-20 et RO-24 ouverts.** Correction de vocabulaire : la « viabilité » est le constat d'une continuité, pas un mécanisme causal ni un filtre extérieur.

## T1 — Renforcement du no-go (preuve)
Pour une relation de transitions R sur Ω, si tout état possède au moins un successeur (R est *sérielle*), alors le noyau de continuation existentielle et le noyau de continuation universelle non contrainte valent tous deux Ω. En particulier, la réversibilité n'est pas nécessaire : tout graphe orienté avec au moins une sortie par état a cette propriété. Sous la convention que « universel » signifie « aucune continuation ne finit dans une impasse », tous les chemins ont une suite infinie.

Conclusion : l'infinité de continuation **globale** est un test non discriminant, dans les deux régimes sérieusement envisagés lorsque chaque état a un successeur.

## T2 — Contre-exemple à « seul l'irréversible peut rendre RO-20 non trivial »
Considérer les états A,B,C, une chaîne de Markov **réversible et irréductible** :

    P = [[0.8, 0.2, 0.0],
         [0.1, 0.7, 0.2],
         [0.0, 0.1, 0.9]]

Stationnaire π=(1,2,4)/7, et π_i P_ij = π_j P_ji exactement. Tous les états admettent des suites infinies et appartiennent aux deux noyaux non contraints.

Supposer que l'attribut observable « organisation encore constituée » vaut vrai dans C_str={A,B}, faux dans C. Alors :
- noyau existentiel restreint C_str = {A,B} (on peut rester dans A ou B arbitrairement longtemps) ;
- noyau universel restreint C_str = ∅ (depuis B on peut aller à C, et depuis A on peut aller à B).

La sous-matrice Q sur A,B est [[.8,.2],[.1,.7]], avec valeurs propres 0.9 et 0.6. En partant de A :

    Pr(organisation encore intacte après n transitions)
      = (4/3)(0.9)^n - (1/3)(0.6)^n.

C'est **positif à tout n fini**, tend vers zéro quand n→∞, et l'espérance du premier temps de rupture est **12,5 transitions** (depuis B : 7,5). Aucune irréversibilité microscopique n'a été postulée.

Ainsi, **la réversibilité n'empêche ni des durées de vie structurales inégales, ni une viabilité non triviale relative à un attribut observable**. Elle empêche seulement d'obtenir ces distinctions à partir du critère de continuation *non contraint* à lui seul.

## T3 — Limite de la construction
Le prédicat C_str={A,B} est **posé pour le contre-exemple**. On ne peut pas le baptiser « volume Blob » puis prétendre avoir déduit RO-24. Pour le Blob, l'attribut constitutif devrait être déduit d'une géométrie opérationnelle, indépendante des résultats visés. L'invariance de la généalogie, la persistance d'un motif, la persistance du volume et la continuation des échanges sont des propriétés distinctes.

## Proposition de registre
- [T] Si R est sérielle, K_existentiel(Ω)=K_universel(Ω)=Ω ; sans mémoire / attribut, critère tautologique.
- [T] Réversibilité microscopique et perte temporaire de cohérence structurale peuvent coexister ; contre-exemple explicite.
- [T] Existence d'une histoire sans rupture ≠ probabilité positive de ne jamais rompre.
- [H/OPEN] Identifier l'attribut de continuité de l'organisation **avant** de tester les volumes, sans coder K4 ni Delaunay comme réponse.
- [OPEN] Règle de l'élan (RO-21), fermeture physique (RO-24), prédictions indépendantes ; TOE 0/7.

## Vérification et limites
`c215_reversibilite.py` vérifie la stationnarité, la balance détaillée, les noyaux, le spectre de Q, la loi exacte de survie et les temps de premier passage. Script rédigé après lecture de l'objection : **ni aveugle ni préenregistré**. Aucune simulation physique, aucune prédiction sur la nature et aucun verrou physique revendiqué.
