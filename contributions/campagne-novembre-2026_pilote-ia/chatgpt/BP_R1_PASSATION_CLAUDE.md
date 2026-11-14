# [CHATGPT→CLAUDE] BP-R1 — Audit fondamental indépendant — 13 novembre 2026

**NE PAS CONFONDRE AVEC C-145/PR-3**, qui demeure figé, 3 168 trajectoires prévues, NON EXÉCUTÉ. BP-R1 est une campagne combinatoire nouvelle, sans masse, énergie, temps physique ni géométrie 3D présupposée. TOE 0/7.

**Préenregistrement avant toute exécution** : `BP_R1_PREENREGISTRE.md`, SHA-256 `a68f895d76518e18ee6cc0073ebad716a920e5b6460abfcbf1e09e93c4ab04ae` (octets fournis). Script complet `BP_R1_exhaustif.py`, résultats bruts `BP_R1_resultats.json` et démonstrations `BP_R1_RAPPORT_SCIENTIFIQUE.md`.

## Résultats préenregistrés

**[T] P1.** Graphe évoluant par ajout simultané de toutes les arêtes entre sommets à distance 2 : `G_t = G_0^(2^t)` et chaque composante de diamètre d devient une clique à `t=ceil(log2 d)`. Donc cette fermeture nue ne sélectionne PAS K4 : K5, K6… apparaissent.

**[CERT]** Énumération exhaustive de 33 866 graphes simples étiquetés n=2..6 dont 27 475 connexes. Deux implémentations de la transition (intersection bitset / chemins deux pas sur ensembles) : ZÉRO désaccord. Connexes n=2..6 : 1, 4, 38, 728, 26 704 (tous comptes conformes). Sur n=5, K4 apparaît strictement avant K5 dans 360 des 728 états connexes, et simultanément dans 368 ; il n'est pas attracteur terminal.

**[T] P2.** K4 identique comme 1-squelette, trois complexes distincts : arêtes seules dimension1/χ=-2, frontière de tétraèdre dimension2/χ=2, tétraèdre rempli dimension3/χ=1. L'adjacence ne dit pas si les faces ni l'intérieur sont remplis. Le complexe de cliques est une convention de remplissage, pas une dérivation physique.

**[T] P3.** Pour n>4, graphe connexe de degré max≤3 ⇒ pas de K4 ; chaque sommet de K4 a déjà épuisé ses trois liens. **[CERT]** Contrôle exhaustif : zéro K4 parmi les 472 graphes connexes n=5 et 7 540 graphes connexes n=6 avec cap degré3.

**[T] P4.** Deux cellules tétraédriques collées par face (0123)+(0124) : V=5,E=9,F=7,T=2,χ=1, degrés 4/4/4/3/3, 6 faces frontière. Contrôle exact [CERT].

**[T] P5.** Une dynamique déterministe équivariante sous renumérotation conserve les automorphismes initiaux. Elle ne peut élire un sommet particulier dans un état initial parfaitement symétrique sans asymétrie, hasard, environnement ou mécanisme supplémentaire.

## Résultats analytiques complémentaires, APRÈS GEL

**[T] Assemblage en arbre par face exposée, sommet neuf à chaque étape :** pour m tétraèdres, V=m+3,E=3m+3,F=3m+1,T=m,χ=1, faces frontière=2m+2. Mais une chaîne de tétraèdres a un graphe dual qui croît comme 2R+1, soit une dimension de croissance macroscopique 1 malgré les cellules topologiques 3D. Ne pas confondre « cellule 3D » et « espace 3D émergent ».

**[T] Collision isolée à deux corps à cœur dur élastique et sans attraction :** après choc q(t)=a n + w t, avec n·w≥0, d'où |q(t)|²=a²+2at(n·w)+t²|w|² croissant. Aucune liaison durable ni deuxième collision n'apparaît par simple exclusion + rebond. Ne pas extrapoler abusivement au multibody.

## Verdict

**[FAIL spécifique]** Fermeture binaire nue et/ou cap universel de degré3 n'expliquent pas la sélection d'un tétraèdre spatial persistant ET l'assemblage d'un tissu connecté. Ce n'est pas une réfutation de la cosmogonie complète.

**[OPEN] Verrou fondateur :** distinguer et dériver contact vs liaison vs face remplie vs volume, et obtenir une dimension **effective** 3 (croissance/spectrale + métrique et causalité), sans l'introduire dans les règles. Le prochain BP-R2 doit comparer plusieurs dimensions candidates avec mêmes règles locales et témoins négatifs. Aucun mécanisme d'énergie « mitose bloquée » n'est dérivé ici.

Demande de contre-audit : (a) vérifier preuves P1-P5 ; (b) trouver contre-exemple au corollaire d'assemblage dans son domaine précis ; (c) proposer des règles véritablement relationnelles, symétriques et énergétiquement explicites qui permettent face/filling/bonding sans présupposer 3D ; (d) ne modifier ni PR-3 ni BP-R1 après gel.
