# Audit INF-1 — hypothèses de Delmotte — VERSION 2
**Date :** 18 septembre 2026 — **remplace la version 1 du même jour**
**Statut :** hypothèses confirmées par **exposition de l'auteur lui-même**. Numérotation exacte de l'énoncé dans RMI 1999 toujours non vérifiée.

---

## 1. Source primaire trouvée

**Delmotte, T., *Harnack inequalities on graphs*, Séminaire de théorie spectrale et géométrie, tome 16 (1997-1998), p. 217-228.** Institut Fourier, Grenoble. Accès libre sur Numdam : https://www.numdam.org/item/TSG_1997-1998__16__217_0/

Delmotte y expose en anglais le résultat de l'article RMI, qu'il cite en référence [11] comme « to appear in Rev. Mat. Iberoamericana ». C'est donc l'auteur exposant son propre théorème, en accès libre. L'article RMI (p. 181-232) reste sous péage, mais son contenu d'hypothèses est désormais établi.

## 2. Hypothèses, telles qu'énoncées par l'auteur

**Définition 2.1 — condition A*(α).** Pour α > 0, le graphe pondéré (Γ, μ) satisfait A*(α) si : x ~ y ⟹ μ_xy ≥ α·m(x).
Conséquence tirée par l'auteur : le graphe est localement uniformément fini, avec **degré borné par 1/α**.

**Définition 2.3 — condition A(α).** A*(α) **plus une boucle en chaque sommet** (x ~ x). En particulier **p(x,x) ≥ α**.

**Théorème 2.4.** Sous A(α), les trois énoncés suivants sont équivalents :
(i) il existe C₁, C₂ > 0 tels que DV(C₁) et P(C₂) soient satisfaites ;
(ii) il existe C_H > 0 tel que HP(C_H) soit satisfaite ;
(iii) il existe c₁, C₁, C_r, c_r > 0 pour lesquels les estimées gaussiennes G soient satisfaites.

Définitions associées : DV(C₁) = V(x,2r) ≤ C₁·V(x,r) ; P(C₂) = inégalité de Poincaré L² sur les boules.

## 3. Correction de la version 1

La version 1 concluait à **une** hypothèse d'ellipticité. Il y en a **deux**. La condition de paresse p(x,x) ≥ α n'apparaissait dans aucune des sources secondaires consultées (Hua–Münch, Andres–Deuschel–Slowik). Elle était posée en [Q] ; elle est confirmée.

## 4. Point favorable au corpus

Delmotte justifie la boucle par un problème de parité : sur la marche standard sur ℤ, un entier impair n'est jamais atteint en temps pair, donc aucune borne inférieure n'est possible sans précaution. Il indique le contournement — appliquer le théorème à une sorte de graphe itéré deux fois — et précise que le résultat obtenu pour la marche d'origine, **surtout la borne inférieure, dépend de la présence de cycles de longueur impaire**.

Les graphes du corpus sont saturés de triangles (n_tri figure dans la fonctionnelle de viabilité). **L'obstruction de parité est donc vraisemblablement bénigne dans ce cadre.** Premier élément favorable de la série d'audits.

## 5. Points à vérifier côté corpus

1. **Degré uniformément borné.** A*(α) impose un degré ≤ 1/α. Si le degré croît avec la taille du graphe, Delmotte ne s'applique pas, indépendamment de tout le reste.
2. **Doublement de volume et Poincaré.** Ce sont les conditions à établir, le théorème étant une équivalence et non une source.
3. **Tension persistante avec SUP-1.** PRS opèrent sur un cadre non elliptique (conductances nulles sur les amas de percolation). A(α) exige μ_xy ≥ α·m(x) sur toute arête. Un même objet doit satisfaire les deux pour que la pince se referme. Non résolu.

## 6. Statut proposé

- Hypothèses de Delmotte : **établies** (source auteur, accès libre).
- Applicabilité au corpus : **[Q]** — conditionnée aux points 1 et 2 du §5.
- INF-1 comme [T] fermé : **toujours non justifié** en l'état.
