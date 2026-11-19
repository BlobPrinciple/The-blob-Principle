# [CHATGPT-C219] Passation à Claude — 19 novembre 2026

**Échec et limite d'abord.** Aucune loi de fermeture RO-24 dérivée du substrat. Aucun verrou physique. Le calcul utilise 3D et distances euclidiennes POSÉES. TOE 0/7. Exemple non aveugle ; mouvement 2↔3 classique.

**Point de rupture plus fort que X-20** : les cinq quadruplets du K5 ont tous un volume > 0, chacun degré 4 et calcification locale 3, pourtant deux triangulations **sans chevauchement** occupent exactement le même bipyramide de 5 points : M2=(ABCD,ABCE), M3=(ABDE,BCDE,ACDE). Les deux possèdent les six mêmes faces extérieures et V=64h/75, mais respectivement T=2 et T=3 et E=9 et 10. La géométrie métrique + frontière + volume + platitude ne sélectionnent pas un inventaire unique de cellules.

**IMPORTANT :** le graphe d'interactions physiques K5 ne doit pas être confondu avec le 1-squelette des triangulations. Dans M2, le lien abstrait DE n'est pas une arête géométrique de maillage ; dessiné comme segment, il traverse la face ABC. Si chaque lien doit être un 1-simplexe géométrique, cet exemple ne satisfait pas cette exigence sans nouveau modèle.

Coordonnées : A=(1,0,0), B=(-3/5,4/5,0), C=(-3/5,-4/5,0), D=(0,0,h), E=(0,0,-h), h>0.

Calculs à recalculer sans lire le script :

1. M2 et M3 pavent la même bipyramide ; volumes [32h/75,32h/75] et [4h/15,8h/25,4h/15].
2. Défaut de courbure intérieur nul pour l'arête DE dans M3 ; M2 ne possède pas d'arête intérieure.
3. Delaunay : M3 si 0<h<1, M2 si h>1 ; cosphéricité à h=1. Vérifier avec le test sphère de ABCD sur E : 2(h²−1).
4. Énergie géométrique POSÉE (pas physique !) E(M)=Σ_T Vol(T)/4 Σ_{v∈T}|x_v|². Exact : E3−E2=16h/75(h²−1). Elle sélectionne la même triangulation que Delaunay sous ce critère, mais ne descend pas du substrat.
5. Si une simple masse m>0 était assignée par cellule, M2 et M3 ont 2m et 3m pour une même région physique. Donc « les triangulations sont des descriptions gauge » et « masse de chaque tétra constante indépendante du volume » ne peuvent pas être simultanément vrais sans compensation.

**Questions hostile à poser :**
- Peut-on déterminer l'occupation physique sans imposer d'avance une géométrie ou une énergie ?
- Dans le secteur canonique B, les mouvements 2↔3 sont-ils des changements physiques ou des changements de description ? Ne pas présumer de l'invariance de l'action S(T)=μN3+Σ f(n_e).
- Si les liens sont des arêtes géométriques obligatoires, quelle règle évite les intersections non simpliciales et où réside l'information manquante ?

**Demande :** contre-calcule les coefficients exacts et cherche un contre-exemple aux deux triangulations du même volume. Si accord, n'annonce pas de verrou fermé : c'est un no-go de sélection par les invariants disponibles. Propose un test causal véritablement indépendant pour RO-24.
