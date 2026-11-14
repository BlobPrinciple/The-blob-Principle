# [PASSATION C-146 / CAS-1 À CLAUDE — contre-audit demandé]

Rudolphe propose que l'effet Casimir intervienne **après** les premières annihilations, lorsque le bain et les liants apparaissent, sans gravitation primitive. Cette hypothèse est cohérente comme mécanisme post-bain, mais CAS-1 ne fournit ni l'origine des premières annihilations, ni l'existence d'un champ initial, ni une liaison durable. Les quatre voies historiques de construction C-1 ne doivent PAS être confondues avec les quatre orientations FF0/FF60/TF/TT étudiées ici.

**Préenregistrement figé AVANT calcul** : `C146_CAS1_PREENREGISTRE.md`, SHA-256 `cdd0ccd42b35152535d715ea31328d2022e5f17f8941b48b036d51a134c56f25`.

**Objet** : champ classique scalaire gaussien dans R³ posé, covariance exp(-r/ell), 4 ou 14 contraintes ponctuelles par tétraèdre. Interaction adimensionnée `u=.5 log det C_AB_total / (det C_A det C_B)`. Deux tetra ne se chevauchent pas (demi-espaces z≤0/z≥g). 96 cas = 2 maillages × 3 ell × 4 gaps × 4 orientations. **96 exécutés**.

**Prédictions** :
- P1 : 96/96 u≤0, dérivable exactement via complément de Schur.
- P2 : face-face alignées FF0 plus favorable que pointe-pointe TT pour 24/24 groupes.
- P3 : FF0 plus favorable que face tournée FF60 à ell=.25,g=.15 dans les deux maillages.
- P4 : blocs décorrélés u=0, permutations A/B et translations conformes.
- P5 : contribution irréductible à 3 contraintes sur une ligne = `-0.5 log(1-exp(-4d/ell))`, d=.3, ell=.5 : `+0.04754997526120135 kBT`.

**Précision** : max divergence 2 formules `9.33e-15`, invariance translation `6.22e-15`, minima matrices glob. `0.1032041`, 4 comparaisons mpmath 55 dps écart max `5.39e-16`. Une erreur d'export JSON booléen `numpy.bool` corrigée sans toucher au protocole ni aux calculs ; consignée.

**Exemple 14 points/objet, ell=.5,g=.3** : FF0 `-0.914205`, FF60 `-0.670031`, TF `-0.272575`, TT `-0.181965` (en kBT). Force normale FF0 = `-4.769955 kBT/a`, autres forces dans le CSV/JSON.

**Contre-audit demandé** :
1. Réimplémenter indépendamment la matrice de covariance, le comptage 4/14 points et les quatre orientations ; vérifier les 96 `u` individuels et les hypothèses P1–P5.
2. Examiner le risque de sélection artificielle par maillage (importance du point de face dans TF ; convergence 4→14 non suffisante pour paroi continue).
3. Réexaminer la justification thermodynamique du champ de bain classique *post-annihilation* : si état hors équilibre, le potentiel d'énergie libre n'est pas directement une loi de force.
4. Démontrer ou invalider la non-additivité analytique P5 et quantifier sa pertinence dans un **tissu** réel.
5. Proposer CAS-2 **avant calcul** : capture post-bain avec bilan énergie, dissipation, bruit et contacts, témoins et perturbations. Pas d'attribution de rôle à la gravitation primitive et pas de sélection favorable après résultat.

**Ne pas promouvoir** : ces calculs ne reproduisent ni une force électromagnétique de Casimir sur des parois idéales continues, ni l'émergence de la 3D, ni la première annihilation, ni des liants permanents, ni la TOE. TOE 0/7.
