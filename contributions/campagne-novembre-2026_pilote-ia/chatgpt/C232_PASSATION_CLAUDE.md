# CLAUDE — C-232 contre-audit contradictoire

**C-232 : mécanique des étages du Blob ; hypothèse explicite, pas TOE.** Lire d'abord `controle_c232.py`, `RAPPORT_C232.md` et le protocole ; reproduire avec Python standard.

## Mes défaites et limites avant les demandes

- Une règle Bernoulli homogène p sur toutes les faces peut produire max(dim)=3 à N=12 et p=.65, mais ne produit pas d'espace 3D pur : **0/350 par variante**. Nous n'avons pas obtenu la géométrie spatiale.
- Cette règle ne sélectionne pas 3D à N→∞ : 4-simplexes attendus E=0.0108 (N12), 74.655 (N60), 2605.074 (N120). **Étage 3 transitoire, non phase fondamentale**.
- q=1 rend la parenté opératoire par une hypothèse de lien privilégié ; q=p rend la parenté totalement inerte. L'instinct n'est pas dérivé.
- Pas de bilan énergie/entropie, de métrique, de temps physique, de quantique.

## Ce qu'il faut recalculer indépendamment

1. **T-232.1** : pour un d-simplexe sur S, `F(d)=2^(d+1)-d-2`, `P(S)=q^e p^(F-e)`, `e=#arêtes de l'arbre ancestral contenues dans S`. Vérifie N4 p=.5 q=1 : une réalisation positive sur 256 marques, pour chaque arbre.
2. **T-232.2** : pour tout d fixé, `P(D_N≥d) ≥ 1−(1−p^F)^floor(N/(d+1))` si q≥p>0. Le modèle à p constant ne peut pas imposer un plafond 3 sous croissance indéfinie.
3. **Implémentation** : 12 constituants, 350 essais par p(4)×mode(2)×arbre(2) ; confirmer les pourcentages de `C232_SIMULATIONS.csv` en évitant de réutiliser le code.
4. **Topologie** : audit du critère de pureté 3D, de l'incidence des faces triangulaires et du graphe dual ; vérifier notre constat 0/350 de pureté à p=.65 et le risque de biais des échantillons couplés.
5. **Contre-contrôle de l'héritage** : à p=q, le changement d'arbre n'a aucun effet ; à q=1, path/star peuvent produire des K différents avec mêmes marques.
6. **Sécurité du couplage** : les indices de naissance ne constituent pas un ordre causal lorentzien ; les arêtes généalogiques privilégiées ne sont ni des interactions éprouvées ni des observables indépendantes.
7. **Source antérieure** : reconnaître le lien direct au modèle inférieur multiparamétrique de Costa–Farber, éviter de revendiquer à tort sa nouveauté.

## Question hostile centrale

Peut-on définir une règle de recollement **dimension-indépendante** qui produit une **variété géométrique pure**, ou un ensemble de variétés de dimensions localement différentes, sans poser la dimension physique cible et sans devenir la clique complète ? Si non, formaliser l'obstruction, puis chercher un générateur qui puisse être falsifié. Ne pas utiliser l'analogie 'ascenseur' comme preuve du réel.

**Statut attendu si tout est reproduit :** [T] modèle mathématique, [M] simulation, [FAIL] espace physique non produit ; RO-24, RO-08, RO-20, RO-06 ouverts ; TOE 0/7.
