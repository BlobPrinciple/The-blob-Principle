<!-- Rapport du contre-auditeur indépendant de X-26, versé tel quel le 23 novembre 2026. -->

# Contre-audit X-26 — rapport

Code indépendant : `audit.py`, `t2.py`, `t3.py`, `t4.py` (entiers et fractions exacts ; boules en tuples, configurations en ensembles d'indices, fermeture par liste de travail). Le dépôt n'a été ouvert qu'après coup.

## 1. Verdicts

- **K14 — VRAI.** Le miroir fixe la cellule, échange les deux côtés et renverse l'orientation (réflexion de déterminant −1). Pour l'invariance à chaque palier, il faut ajouter à la preuve que la fermeture ne dépend pas de l'ordre (l'éligibilité est monotone, le point fixe est unique).
- **K15 — VRAI AVEC RÉSERVE.** L'identité clé est triviale : <u,w> = −2n·u_{n+1}. L'argument « ne traverse pas » est juste (|<u,ŵ>| ≥ √3 hors de M), mais il ne suffit pas pour exclure un lien A–B : il faut aussi écarter le cas d'une boule B *contenant* la boule du miroir. Cela exige la non-chevauchement global (avec e₀), qui est un théorème classique (Boyd 1973) et non un fait vérifié jusqu'au palier 7. Rang 2 : preuve courte disponible. Si u ∈ vect(e₀,e₁,e₂), avec p,q,r = −<u,eᵢ> ≥ 1, alors <u,u> = −(pq+qr+rp) < 0 ≠ 1.
- **K16 — VRAI AVEC RÉSERVE.**
  - (b) Le sens « tissu ⊆ M » se démontre par l'hexlet de Soddy : autour de m₁m₂m₃, l'anneau est m₀, a, a′, v, b′, b, avec v = −m₀ + 2Σmᵢ, obtenu en trois pas.
  - Le sens « M ⊆ tissu » n'est que constaté. Une preuve existe par maximalité de l'empilement de cercles (ensemble résiduel d'intérieur vide), à condition d'avoir la non-chevauchement.
  - (c) La relation « génération k ↔ palier 2k+1 » est constatée ; l'hexlet en donne une esquisse, sans preuve d'exactitude.
  - « Côté A et côté B » est démontré : cinq boules deux à deux tangentes ne tiennent pas dans w^⊥, de dimension 4, car det(2I−J)₅ = −48.
  - O(3,1) : vrai, mais c'est un fait général de Lorentz, étranger à l'empilement.
- **K17 — VRAI**, comme corollaire de K15 ; c'est aussi vérifié directement.
- **Q5 — OUI, preuve simple, sans recourir à la non-chevauchement.** Si v ∈ M naît de C, alors R(C) est de surface et a le même côté libre v. Si R(C) = C, les membres hors M de C vont par paires (a, Ra), or <a,Ra> = 1 − 6a₄² ≠ −1 ; donc C ⊂ M, et v ∈ M est impossible (argument du déterminant). Il y a donc au moins deux cellules. « Exactement deux » est seulement constaté.

## 2. Nombres recalculés (paliers 0→7)

| Grandeur | Recalcul | Écart |
|---|---|---|
| Rang 2 : effectifs | 3, 5, 11, 29, 83, 245, 731, 2189 ; M = 3 ; A–B = 0 ; min = 4 ; pgcd = 4 | aucun |
| Rang 3 : effectifs | 4, 6, 14, 42, 174, 666, 2646, 10746 | aucun |
| Naissances / doubles | 2, 8, 28, 132, 492, 1980, 8100 / 0, 0, 4, 0, 84, 288, 1044 | aucun |
| Liens hors naissance | **6**, 0, 12, 48, 132, 648, 2556 | palier 1 : convention (liens de la cellule de départ) |
| Liens | 14, 46, 174, 750, 2934, 11790, 47790 (contacts géométriques = liens de configuration, toutes paires) | aucun |
| M | 4, 4, 4, 8, 8, 20, 20, 56 ; pgcd = 6 ; A–B = 0 ; chevauchements = 0 (toutes paires jusqu'au palier 7) | aucun |
| Nés dans M | 4 + 12 + 36, tous issus de 2 cellules, 5 liens MMM+A+B, A et B images l'un de l'autre | aucun |
| Cellules M | 1, 1, 5, 5, 17, 17, 53, toutes structurelles, côtés A+B | aucun |
| Liens de e₀ / e₄ | 5, 11, 26, 74, 188, 488, 1304 / 4, 8, 20, 56, 140, 368, 980 ; e₀ strictement maximal ; moyenne au palier 6 = 8,9116 | aucun |
| Niveau 1 | 2, 10, 10, 34, 34, 106, 106 | voir erreur 2 |
| Rang 4 | 35 paires chevauchantes au palier 3 | conforme |

Le champ « fermetures » du .out (16, 48, 216…) compte aussi les doublons de naissance. Ce n'est pas une erreur, mais le libellé est ambigu.

## 3. Antériorité

- **Vérifié.**
  - Soddy, *Nature* 139 (1937) 77 : l'hexlet, mécanisme exact de K16.
  - Boyd, *Canad. J. Math.* 25 (1973) 303–322 : l'empilement osculateur en dimension 3.
  - Graham–Lagarias–Mallows–Wilks–Yan, *Discrete Comput. Geom.* 35 (2006) 37–72 : groupe d'Apollonius et groupe dual, dont les sphères duales comme w.
  - Kontorovich–Nakamura, *PNAS* 116(2) (2019) 436–441 : grappe et co-grappe, théorème de structure.
- K14 découle immédiatement de la théorie : R(D) = S₄(D), donc l'empilement est invariant.
- **Non trouvé.** Je n'ai pas trouvé de référence explicite pour l'énoncé « la section par une sphère duale est l'empilement apollonien de cercles ». C'est probablement du folklore ; ce n'est pas vérifié.

## 4. Erreurs, par gravité

1. **Moyenne.** La preuve du rang 3 « aucun lien A–B » est présentée comme arithmétique. Elle dépend en réalité de la non-chevauchement globale (cas d'emboîtement), qu'il faut citer.
2. **Moyenne.** « Niveau 1 = deux par cellule de M » est faux aux paliers pairs (2, 4, 6) : il y a alors 8, 24 et 72 constituants à 3 voisins M (les a′ de l'hexlet).
3. **Moyenne.** L'« observation non prédite » des niveaux entiers est une tautologie : |<u,w>|/6 = |u₄|, une coordonnée entière. Le pgcd 6 l'est aussi.
4. **Faible.** M ⊆ tissu et 2k+1 sont présentés comme démontrés alors qu'ils sont seulement constatés.
5. **Faible.** Convention du palier 1 pour les liens hors naissance.

## 5. Ce que cela ne donne pas

Aucune dynamique ni physique. A et B sont des copies isométriques exactes, sans propriété qui les distingue (ni charge, ni masse, ni asymétrie). La symétrie vient du choix symétrique du départ. Les lignées ne se touchent jamais : M ne les « fait pas se rencontrer », M est le lieu fixe du miroir. La lecture « matière/antimatière » reste une lecture. Au rang ≥ 4, tout s'effondre (chevauchement). Rien de cela ne s'étend au-delà d'une structure classique de l'empilement de Soddy.
