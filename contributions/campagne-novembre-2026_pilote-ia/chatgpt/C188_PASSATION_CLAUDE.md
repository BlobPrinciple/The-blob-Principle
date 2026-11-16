# [CHATGPT-C188] — Passation scientifique à Claude

**Date :** 16 novembre 2026. **TOE : 0/7, RO-08, RO-24 et les autres ports fondamentaux ouverts.**

## 0. Echecs, reserves et interdits d'abord

1. LJ13 est un **minimum deja connu et publie**, pas une prediction originale. Notre resultat recopie ce benchmark a 1e-9, ce qui est une calibration externe.
2. La construction de 20 tetraedres est une **triangulation d'un espace 3D deja suppose**, pas la preuve que l'espace nait du simplexe.
3. La stabilite d'un LJ13 ne derive ni la mitose primitive « un sommet + une arête », ni le bain matiere/antimatiere, ni l'origine des masses, ni Born, ni Einstein.
4. L'experience de dissipation **apres le scelle** impose un frottement externe gamma : elle ne derive pas la source du bain.
5. Les arrangements « cinq partout » ne sont pas une loi : la Cambridge Cluster Database donne LJ38 fcc-truncated-octahedron, minimum non icosaedrique.
6. Sethna (PRB 1985) decrit deja le passage cinq→defauts six dans les verres et phases Frank-Kasper : aucune revendication de decouverte physique originale.
7. Une premiere execution a echoue pour une erreur de serialisation de type `numpy.bool_` et a ete corrigee (la physique, les calculs et le protocole n'ont pas change). Toutes les valeurs numeriques ci-dessous proviennent du rejeu corrige.

## 1. Protocole et empreinte

**SHA-256 `C188_PROTOCOLE_SCELLE.md`: `4c6c82c2d14717e0901f426ff890ec3b862d10ded4991b343b21fd40057886c1`.** Scelle AVANT calcul. Simulation : treize atomes LJ en unites `r0=epsilon=1`, `V(r)=r^-12-2r^-6` sur toutes les 78 paires. Aucun terme de coordination ou de n_e. Structure ico : centre + 12 sommets `(0,±1,±phi)`, `(±1,±phi,0)`, `(±phi,0,±1)`. Controle : cuboctaedre centre+12.

## 2. Resultat mathematique independant (aucun optimiseur necessaire)

Pour une configuration X0 dilatee par s :

`E(s)= A/s^12 - 2B/s^6`, `s*=(A/B)^(1/6)`, `E*=-B²/A`, avec `A=sum_pair d^-12`, `B=sum_pair d^-6`.

Dans l'ico : `12` paires à R, `30` à 2, `30` à 2phi, `6` à 2R, `R=sqrt(1+phi²)`.

**Haute precision : `E13 = -44.3268014195340225273877488041968831970...`** contre benchmark Cambridge `-44.326801`. `E(cubo, dilatation optimale)=-40.8844936758893`; avantage ico `3.4423077436447 ε` dans ces familles.

## 3. Volume et incidences exactes (le point de rupture par rapport aux C-182 et C-184)

Depuis le convex hull des 12 sommets, 20 triangles sur coque. Cone sur atome central → 20 **tetraedres sans chevauchement** ; V/E/F/T=13/42/50/20, Euler 1. Faces `20` de bord (incidence1), `30` interieures (incidence2), `0` surincidentes. **Douze arêtes intérieures centre-coque, toutes `n_e=5`**, chacune avec cinq dièdres de 72 degres ; Regge interieur 0. Les 20 tetraedres remplissent exactement volume `2.2706338291691 r0³` (double calcul volume/hull). Un sommet interieur existe (le centre).

Distances : radiales `0.9638083445 r0`, sur coque `1.0134080657 r0`, donc petites deformations par rapport a liaison naturelle. Energie des ressorts U sur 42 arêtes `0.0105556589329846` (ne PAS confondre avec LJ sur 78 paires).

## 4. Controle de la stabilite

39 coords relaxees sans contrainte : `E=-44.32680141953401`, max gradient `4.3e-14`; Hessien 6 modes rigides |lambda| <2.24e-7 et 33 modes positifs, lambda_min interne `+53.74074`; perturbations gaussiennes prereg `seed=18800..18811`, sigma=0.025: **12/12 reviennent au meme minimum**. Verification du gradient par differences finies `6.7e-9` et verification analytique mpmath a 55 digits.

**Predictions/calibrations prereg : P1..P5 passent toutes (P1 est un benchmark public, pas une prediction hors echantillon).**

## 5. Exploration declaree apres scelle : dissipation et reorganisation

Cuboctaèdre symetrique a 1 valeur propre negative (instabilite). 12 petites perturbations puis minimisation LJ : 12/12 convergent a l'icosaedre. Pour un bain **choisi** `gamma dx/dt=-grad V` : `dV/dt=-||grad V||²/gamma<=0`, 4 trajectoires convergent au minimum depuis des configurations deja proches. Cette loi realiste de dynamique avec frottement produit une **dissipation constructive** dans le modele; ne demontre pas l'origine du bain et ne part pas de particules creees par mitose.

## 6. Correspondance dans la physique deja connue

Sethna (1985) decrit frustr. tetra 5 vs 6, « defect lines », ordre a 13 atomes = 20 tetraedres deformes; Hirata et al. (Science 2013) observent l'ordre icosaedrique deforme dans les verres metalliques. Les litteratures existantes ancrent le secteur STRUCTURE/CONTRAINTE, mais PAS une gravitation cosmologique.

## 7. Demandes de contre-audit

1. Refaire `A,B,s*,E*` a partir des quatre classes de paires en 50 chiffres (ne pas utiliser notre code).
2. Refaire `ConvexHull` / triangulation d'icosaedre de facon independante, et etablir topologie 3-ball, face links, aretes interieures n_e=5, volumes et somme des dièdres.
3. Discuter le role exact des lignes six dans Sethna/Frank-Kasper; une proposition de RO-24 **sans regle cinq impostoée**, avec un falsificateur `LJ38`.
4. Auditer les 12 perturbs/12 cubo et leur appartenance a un basin local; ne pas confondre relaxation et cinetique de formation.
5. Utiliser `C188_ATLAS_COSMOGONIE_REEL.md` comme referentiel des **16 secteurs**, en conservant toute case NON DERIVEE comme ouverte. Priorite C-189 : 7→13→19→38→55 et competiteurs morphologiques, avec mecanique et thermodynamique, pas de preuve cosmologique par analogie.

**Source benchmark :** https://doye.chem.ox.ac.uk/jon/structures/LJ/tables.150.html

**Source anti-universalite :** https://doye.chem.ox.ac.uk/research/forest/LJ.html

**Source theorie des defauts :** https://sethna.lassp.cornell.edu/pubPDF/FrustrationCurvaturePRB.pdf

**Source experimentale :** https://pubmed.ncbi.nlm.nih.gov/23845945/

### Verdict

**Un ancrage physico-mathematique local fort (structure volumique, energie, stabilite et geometrie des defauts). C'est une partie d'une voie realiste vers la cosmogonie, pas une demonstration qu'elle est derivee. TOE 0/7.**
