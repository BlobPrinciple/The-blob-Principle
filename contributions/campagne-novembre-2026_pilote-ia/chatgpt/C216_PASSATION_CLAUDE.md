# [GPT-C216] Passation pour contre-audit Claude — 19 novembre 2026

**TOE 0/7.** Aucune loi physique entièrement dérivée. Audit mathématique non aveugle, données publiques et résultats théoriques connus.

## Contre-attaques prioritaires

1. **T1 — fermeture :** construire les matrices de bord des complexes `∂Δ³` et `Δ³`. Vérifier qu'ils partagent exactement `∂₁` et `∂₂` mais ont respectivement `b₂=1` et `b₂=0`, et caractéristiques d'Euler 2 et 1. Réserve à conserver : coquille en R³ peut enclore un intérieur géométrique sans 3-cellule occupée dans le complexe ; ne pas confondre les deux concepts.
2. **T2–T4 — conservation/dissipation/DEC :** vérifier `1ᵀB=0`, `Ḟ=-(Bᵀq)ᵀG(Bᵀq)` et `∂₂∂₃=0`. Tous les `G`, `q`, `A` sont posés. Aucun lien dérivé à la physique quantique ou aux interactions du SM.
3. **T5 — obstruction de persistance absolue :** démontrer que pour toute chaîne finie irréductible et tout sous-ensemble propre `O`, `P(τ_{O^c}=∞)=0`. Dans l'exemple C-215, temps de première sortie : `25/2` et `15/2`, en accord avec les valeurs propres `9/10,3/5`. **Ne pas étendre sans précaution aux chaînes infinies ou non irréductibles.** La persistance des simplexes/lignées est distincte de celle d'une structure `O`.
4. **T6 — maximum d'entropie :** vérifier `p∝exp(-βE)` seulement avec énergie et moyenne contraintes ; cela n'impose pas un `Q_phys`.
5. **T7 — Regge :** ne pas confondre arêtes-charnières de 3D et triangles-charnières de 4D ; pas de GR dérivée du simple défaut angulaire.

## Point de rupture décisif

Une loi qui ne dépend que des liens et faces (2-squelette) ne peut distinguer `∂Δ³` du `Δ³` rempli, sans donnée de constitution en cellule. Ceci frappe RO-24 plus directement qu'une comparaison K₄/Delaunay. Inviter à construire un mécanisme **indépendamment motivé** qui produit des 3-cellules, avec mesure falsifiable. Tout le reste reste conditionnel.

## Exécution

`python3 c216_verification.py` (SymPy) -> `RESULTATS_EXACTS.json` ; asserts d'homologie, incidence, énergie et Markov. SHA-256 listés dans `EMPREINTES_SHA256.txt`. Aucun changement au dépôt GitHub.
