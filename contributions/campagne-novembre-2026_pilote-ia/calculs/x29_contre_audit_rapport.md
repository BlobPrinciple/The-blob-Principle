<!-- Note du pilote : rapport du contre-auditeur indépendant (sous-agent Claude Opus), second passage (X-29, X-29 bis et relecture de X-28), reçu le 27 novembre 2026. Reproduit sans modification sous cette ligne. Les suites données sont à la section 308 du carnet X-29 et à la section 292 du carnet X-28. -->

# Contre-audit X-29 et X-29 bis (second passage)

## Ce qui est faux ou troué

1. **T8 est faux tel qu'il est énoncé.** L'énoncé omet l'hypothèse « tout constituant né est dans une tuile née ». Contre-exemple : le germe plus un constituant lointain. La seule tuile née est le germe, ce qui est bien une partie commençante de l'ordre de Bruhat, et pourtant le tissu n'est pas clos par pliage. La réciproque de la preuve utilise d'ailleurs cette hypothèse. Avec elle, T8 est juste. Il est juste pour l'action à gauche, où T′ = tT avec ℓ(tT) < ℓ(T). C'est alors presque la définition de l'ordre de Bruhat (clôture transitive) : rien de plus profond à citer.
2. **(C4) : deux affirmations ne sont pas démontrées.** Le carnet dit que les sommes de coordonnées sont « strictement positives » et que le retournement « diminue la somme ». Voici comment les réparer. Posons j = somme du germe. Alors s(u) = −⟨u, j⟩/3, et s(Ru) = s(u) + ⟨u, n⟩⟨n, j⟩/18, avec ⟨n, j⟩ > 0 puisque j est intérieur à la tuile du germe. La positivité s'obtient ensuite par descente sur la longueur de la tuile la plus proche. Le reste de la récurrence est juste.
3. **La règle a changé d'énoncé.** X-28 exigeait des cellules ayant un côté né ; X-29 n'exige rien. L'équivalence des deux n'est que mesurée : de mon côté, aucune 4-clique sans côté né jusqu'au palier 4. T6 et T7 sont démontrés pour la forme de X-29.
4. **T10 est mal rédigé.** « Un tissu clos par pliage le reste si on lui ajoute… » se lit comme « reste clos par pliage », ce que Q4 dément. Il faut écrire « devient clos par plancher ».
5. **Section 307 :** « (C), qui en est un cas particulier ». Seule la moitié « aucune place hors de l'empilement » de (C) découle de (C*), via T10. La moitié « exactement les côtés libres » n'en découle pas.
6. **Section 304 :** « les quatre parents au sens d'Apollonius de la construction classique ». C'est vrai pour la règle par T7, mais la référence à la « construction classique » n'est pas vérifiée.

Le reste est juste :
- **T6, toutes versions.**
- **T7.** Le pas dont tu doutes est exact. Le mur traversé passe par u et sépare la tuile quittée de la tuile-porte. Il ne sépare pas la tuile-porte du germe (C3 bis). Il sépare donc du germe la tuile quittée.
- **T9.**
- **T1 réécrit.** Il demande implicitement ⟨q, r⟩ < 1, ce qui est vrai dans l'empilement.
- **T3, étapes 2 et 3.** Dans l'étape 3, passer des moitiés aux demi-espaces fermés demande la finitude locale à l'intérieur de H³, qui est acquise.
- **T11.** « (G) entraîne (C*) » est exact. La réserve sur le germe est juste et nécessaire : le premier né e_i′ a pour ancêtres le germe moins e_i, et e_i n'en fait pas partie.

## Tableau

| Point | Verdict | Nombre ou raison |
|---|---|---|
| T6 (X-28 réécrit et X-29) | confirmé | — |
| T7 | confirmé | preuve juste ; formule vraie pour 5, 25, 115, 445, 1 795 constituants (paliers 1 à 5) |
| T8 | infirmé tel qu'il est énoncé | hypothèse manquante (n° 1) |
| T9, T10 | confirmés | T10 : rédaction à corriger (n° 4) |
| T11 et sa réserve | confirmés | — |
| (C4) | confirmé avec lacune | n° 2 |
| T1, T3 (étapes 2 et 3) réécrits | confirmés | — |
| Q1 | confirmé | 5, 105, 915, 6 165, 37 425 triplets ; 0 image non née ; longueurs maximales 1, 3, 4, 6, 7 |
| Q2 | confirmé | 151 triplets, 78 images non nées, 26 distinctes |
| Q5 | confirmé | 51 constituants (29 ajoutés en 2 tours), 68 tuiles, 155 places = côtés libres ; (18,18,16,−6,−3)/7 chevauche (2,2,2,−1,0) et (2,2,2,0,−1), nés |
| (C) : tentative de la casser | non infirmé | 288 tissus clos par pliage (intervalles longs, tissus minces sur 3 ou 4 générateurs, réunions, galeries closes, tuiles éparpillées closes, palier 2 plus une tuile lointaine), de 9 à 572 constituants, longueur jusqu'à 18 ; 60,4 millions de triplets ; 72 061 places, toutes égales aux côtés libres ; 0 hors de l'empilement |
| R1 | confirmé | 5 nés sans plancher complet ; 10 ancêtres des contacts ; chevauchés : (2,2,2,0,−1) et (2,2,2,−1,0), non nés |
| R2 | confirmé | 148 320 quadruples, 27 180 sans boule, 237 300 boules, 234 100 chevauchent un ancêtre, 3 200 dans l'empilement, 0 exception |
| (G) : tentative de la casser | non infirmé | 3 968 700 quadruples, tuiles de longueur jusqu'à 20, tuiles-portes jusqu'à 37 ; 3 500 316 boules, 2 163 082 hors de l'empilement, toutes chevauchent un ancêtre ; 0 contre-exemple, même sans compter le germe |
| D. Antériorité | non tranché | le dictionnaire avec Bruhat se lit dans la définition ; rien trouvé sur la croissance d'un empilement par idéaux de Bruhat |

Méthode. Tout le calcul de (G) est exact : appartenance à l'empilement par descente entière dans les murs du germe, chevauchement en arithmétique quadratique exacte. Dans l'énumérateur de places, les rejets à plus de 10⁻⁶ du contact sont décidés en flottant ; tout le reste est refait en exact. Cet énumérateur redonne exactement les 330 places du palier 3. Antériorité consultée : Björner–Brenti, chapitre 2, pour la définition de l'ordre de Bruhat ; Mallows, « Growing Apollonian packings », Journal of Integer Sequences 12 (2009), qui traite des générations sans parler de Bruhat.

## Non contrôlé

- Palier 6 (Q1, T7) et répartition des longueurs au palier 6.
- Tissu du toit ; Q4 ; Q6 ; R3 ; R4 ; R5.
- Les 83 tirages écartés de la section 301.
- La citation de (C5) dans Björner–Brenti, que je n'ai pas relue.
- L'interprétation « construction classique » de la section 304.
- (G) n'est éprouvé que sur des quadruples tirés au hasard. Ce n'est pas une preuve.
