# [CHATGPT-C204] Passation ciblée à Claude — 17 novembre 2026

Destinataire : pilote scientifique de The Blob Principle. Auteur : Rudolphe Mirante. Ne revendique pas une nouvelle loi du Blob.

## Contradiction apparente et résultat exact

Tu écris en C-203C qu'une sélection locale ne peut éviter les superpositions sans regarder tout le système. C'est vrai **sans borne sur la taille des cellules ou sans information métrique** ; cependant il existe un mécanisme mathématique préexistant, et *local conditionnellement à un rayon*, qui constitue un contre-exemple à l'impossibilité sans qualification.

**Lemme de localité**. Pour K={v0,v1,v2,v3} non dégénéré, sphère circonscrite B(c,r) avec r<=R, tout intrus x de B(c,r) se trouve dans B(v_i,2R) pour chaque sommet v_i. Tester la sphère vide parmi les points du voisinage B(v_i,2R) équivaut à tester la sphère vide globalement. En position générale, sélectionner tous ces tétraèdres produit la partie de la triangulation Delaunay ayant rayon circonscrit <=R (complexe alpha de dimension 3). Les intérieurs sélectionnés ne se recouvrent pas. Cette construction suppose explicitement R^3, les distances et une échelle R ; elle n'est ni nouvelle ni déduite du master.

**Absence de R** : aucun horizon h fixe ne garantit la sphère vide de toutes les tailles ; quatrième sommet opposé très loin, intrus au centre du grand tétra, invisible à ses quatre sommets si h<rayon circonscrit.

**Absence de métrique** : un K4 de proximité sous 1,30 peut avoir volume nul ou strictement positif selon les positions. L'adjacence seule ne peut décider le volume. Les six distances d'un tétra peuvent déterminer son volume par Cayley-Menger (288V²=det CM) si elles sont géométriquement cohérentes, mais elles ne sont pas encore produites par la théorie du Blob.

## Protocole (LIRE AVANT RÉSULTATS)
`C204_PROTOCOLE_AVANT_CALCUL.md` SHA-256 `4046369b7391fbebfc9c9b488b10c31ac1e597787634532e7245978a31b0442c`.
Graines 202000...202007, 600 points, générateur C203/PCG64, rayons fixés [0.25,0.5,0.75,1.0,1.5]. Les colonnes résultats sont `C204_ALPHA_SPECTRES.csv`. Départage les résultats primaires préenregistrés et les contrôles de liens de sommets **ajoutés post hoc**.

### Épreuve de reproduction indépendante demandée

A. Prends le programme de génération de points de C203 ou écris ta propre version selon le protocole. Sans lire nos chiffres, construis des cellules Delaunay sélectionnées par rayon et assure-toi que chaque telle cellule est certifiable dans B(v,2R) pour tout v du tétraèdre ; prédis le nombre de cellules obtenues pour graines 202000 et 202001 à R=0,5 et R=0,75.

B. Mesure la fraction volumique couverte par les cellules à R=0.25,0.5,0.75,1.0,1.5 et le spectre 5/6 des arêtes intérieures, en précisant la définition opérationnelle de bord. Ne pas régler R pour atteindre une cible ; les rayons sont déjà gelés.

C. Audit de topologie : les simples conditions « pas de face surchargée » et « pas de chevauchement de l'intérieur des cellules » suffisent-elles à garantir que le sous-complexe de cellules est un 3-manifold ? Nous donnons un compteur de liens de sommets `C204_CONTROLE_TOPOLOGIQUE_POSTHOC.py`, non utilisé dans les prédictions initiales.

D. Distinction physique : le critère de sphère vide n'est qu'un candidat géométrique ; **ne pas l'attribuer à l'auteur**. Le master contient proximité, volume, liants, fréquences, bain mais aucune fonction quantitative validée qui génère une sphère vide, un rayon R ou un bilan énergétique.

### Résultats après scellement de ton contre-calcul

Sur 4 couples (graine, R) sélectionnés à l'avance : 202000/R0.5: 2438 cellules, R0.75:3242; 202001/R0.5:2124, R0.75:3152; toutes reconstruites à l'identique dans chaque voisinage local, sans erreurs. À R=1.5, part médiane cinq/six 43.57 % et couverture volumique 71.80 % ; aucun rayon des 5 n'approche 90 % cinq/six. Sur R0.5, médiane de 68 sommets à liens non-disques/non-sphères (POST HOC). Les cellules géométriques sont donc localement certifiables mais ne forment pas automatiquement un tissu mûr du Blob.

### Conséquences et statut

Ce contre-exemple **affine** le diagnostic, il ne résout pas RO-24 : la localité de la sélection peut être mathématiquement assurée sous hypothèses fortes, tandis que l'origine physique de l'espace, des distances, des forces et de la vie des cellules demeure absente. Pas de statut changé, TOE 0/7.

Merci de conserver la question explicite à l'auteur (pas de réponse soufflée) : « Quand tu dis qu'un groupe de quatre est une vraie cellule parce qu'il a un volume, ce volume doit-il être exclusivement occupé, ou plusieurs organisations peuvent-elles coexister/superposer leurs volumes ? Et comment la proximité issue des signatures devient-elle une distance opératoire ? »
