# Relecture hostile — Hypothèse γ = α − δ

*Relecteur : second agent IA (Claude, Anthropic), 31 octobre 2026. Aucune relecture humaine.*

> **Mandat :** chercher les erreurs, pas les confirmations.

---

## Objection 1 — L'étape 5 est FAUSSE en tant que barrière d'énergie libre

**Gravité : MAJEURE (invalide la conclusion quantitative).**

La dérivation additionne les coûts de (q−1) retraits d'arêtes successifs comme si chacun coûtait 6λ/q². C'est incorrect pour deux raisons :

### 1a. Le coût par arête n'est pas constant le long du chemin

Après avoir retiré k arêtes du sommet v dans la clique, la clique résiduelle autour de v a la taille q−1 côtés mais v n'en fait déjà plus partie pour k liaisons. Le nombre de triangles détruits par le retrait de la (k+1)-ème arête n'est plus (q−2) mais décroît. Concrètement :

- Le 1er retrait détruit (q−2) triangles (tous les voisins communs dans la clique).
- Le 2ème retrait détruit au plus (q−3) triangles (un voisin commun de moins).
- Le k-ème retrait détruit au plus (q−1−k) triangles.

La somme correcte des triangles détruits est :
∑_{k=0}^{q-2} (q−2−k) = C(q−1, 2) = (q−1)(q−2)/2

Et la barrière totale (contribution triangulaire) est :
B ≈ λ · ∑_{k=0}^{q-2} (q−2−k)/(T − triangles déjà retirés)

Ceci n'est **pas** égal à (q−1)·6λ/q². La somme dépend du chemin et T diminue à chaque étape.

### 1b. Le Metropolis fait des ÉCHANGES, pas des retraits

Le moteur ne retire pas une arête sans compensation. Il échange : il retire une arête ET en ajoute une autre simultanément. L'arête ajoutée peut elle-même créer des triangles, ce qui réduit le coût net de l'échange. La dérivation traite le retrait comme s'il se faisait dans le vide, sans considérer que l'arête ajoutée compense partiellement.

De plus, le Metropolis accepte ou rejette l'échange entier en une étape. La barrière pertinente n'est pas la somme des coûts par arête, mais le **maximum** de ΔS_sim le long du chemin de transition le plus favorable (col de l'énergie libre), ce qui est typiquement bien inférieur à la somme.

**Correction nécessaire :** La barrière devrait être estimée comme un max le long du chemin, pas comme une somme. Si la barrière est le max d'un seul échange défavorable, alors B ≈ λ·(q−2)/T ≈ 6λ/q², et NON 6λ/q. Cela change l'exposant : B ~ λ/q² ~ N^(α−2δ), donc γ = α − 2δ, pas α − δ.

---

## Objection 2 — q_eff et clique maximale mesurent des choses différentes, et ni l'un ni l'autre n'est nécessairement pertinent

**Gravité : MAJEURE (invalide l'estimation de δ).**

- **q_eff** est défini par inversion de C(q−1, 2) = ⟨T_v⟩, soit q_eff = (1+√(1+8⟨T_v⟩))/2. C'est la taille de la clique qui donnerait au sommet moyen son nombre moyen de triangles. C'est une fiction : le sommet moyen n'est PAS dans une clique, et la distribution de T_v est très asymétrique (87–97 % de la masse portée par une minorité de sommets). q_eff ≈ 4 ne mesure pas la taille de la structure dominante ; il mesure la racine cubique de la masse triangulaire moyenne diluée par tous les sommets.

- **La clique maximale** (q_max ≈ 10 à n=97) est une grandeur entière qui saute par paliers. Son exposant δ ≈ 0.50 est bien plus élevé que δ(q_eff) ≈ 0.08. Or c'est la clique maximale qui porte la barrière dans le raisonnement (on parle du coût de remplacer un membre de LA clique dominante).

- **Mais la clique maximale n'est pas non plus le bon objet.** La structure dominante dans un graphe d'Erdős-Rényi à densité modérée n'est pas nécessairement une clique au sens strict. Des structures quasi-cliques (denses mais pas complètes) ou des structures communautaires peuvent porter une fraction importante de la masse triangulaire sans être des cliques exactes.

**Conclusion :** δ dépend fondamentalement de ce qu'on mesure. Le raisonnement exige que la structure dominante soit une clique, ce qui est une hypothèse non vérifiée.

---

## Objection 3 — Confusion entre temps de relaxation et temps de séjour

**Gravité : MAJEURE (les données ne testent pas l'hypothèse).**

Le protocole source (Codex) parle de « γ mesuré ≈ 0.507 ± 0.010 » au degré moyen 4. Cette valeur ne peut venir des données M11 existantes, qui mesurent un **exposant de loi de puissance** de t½ (t½ ~ N^3), pas un exposant d'Arrhenius.

- Si t½ ~ N^p avec p ≈ 3, alors log(t½) ~ p·log(N), qui est logarithmique en N.
- Si t_séjour ~ exp(c·N^γ), alors log(t_séjour) ~ N^γ, qui est polynomial en N.

Ces deux comportements sont incommensurables. Le fait que la loi de puissance ajuste bien les données M11 (R² > 0.99) **contredit** plutôt qu'il ne soutient l'hypothèse Arrhenius, puisqu'un comportement Arrhenius avec γ > 0 donnerait un R² plus faible en ajustement de loi de puissance aux grandes tailles (la courbure dans un log-log apparaîtrait).

Le test correct : tracer log(t½) vs N^γ pour différents γ et chercher la meilleure linéarité. Le vérificateur a fait ce test et trouve que R² **diminue** quand γ augmente (de 0.9863 pour γ=0.5 à 0.9546 pour γ=1.0), ce qui va CONTRE l'hypothèse d'un comportement Arrhenius.

---

## Objection 4 — Le terme −βD ne peut pas être ignoré a priori

**Gravité : MODÉRÉE (pourrait changer l'exposant ou dominer).**

Quand on retire une arête du sommet v dans une clique :
- Le degré de v diminue de 1.
- Le degré du partenaire diminue de 1.
- L'arête ajoutée en échange augmente les degrés de deux autres sommets.

La variation de D = σ(deg)/μ(deg) dépend de la position de v dans la distribution des degrés. Dans un graphe où la clique dominante a des sommets de degré ≈ q (plus élevé que la moyenne ≈ 4), retirer une arête de la clique **diminue** la dispersion des degrés, ce qui **augmente** S_sim (terme −βD moins négatif). Cela veut dire que la contribution D **facilite** le démantèlement de la clique, contrairement à la contribution T qui le freine.

Si la contribution D domine, la barrière pourrait être plus basse que prévu, voire négative (pas de barrière du tout).

Les nouvelles mesures montrent `barrier_T_over_total = 0%` pour tous les points, ce qui est suspect — soit la mesure est erronée (on ne mesure que les swaps rejetés, pas le coût le long d'un chemin de transition), soit D domine effectivement. Dans les deux cas, l'hypothèse « la barrière est portée par T » est directement contredite.

---

## Objection 5 — L'additivité de la barrière suppose un chemin ordonné qui n'est pas celui du Metropolis

**Gravité : MODÉRÉE.**

Le raisonnement suppose implicitement que la transition se fait par un chemin ordonné : d'abord retirer toutes les arêtes du sommet sortant, puis ajouter celles du remplaçant. Le Metropolis ne suit pas ce chemin : il fait des échanges aléatoires sur tout le graphe. Le sommet sortant peut perdre une arête de la clique parce qu'un échange ailleurs dans le graphe a déplacé cette arête, pas parce que le Metropolis « cible » ce sommet.

Le chemin de transition réel dans l'espace des configurations est un problème de passage de col en dimension élevée, et la barrière le long du chemin optimal (le col) peut être très différente de la somme des coûts élémentaires.

---

## Objection 6 — Les données contredisent l'hypothèse

**Gravité : CRITIQUE.**

Avec les nouvelles mesures de clique maximale :

| n | q_max |
|---|---|
| 17 | 5.3 |
| 33 | 6.5 |
| 49 | 7.7 |
| 65 | 8.8 |
| 97 | 10.4 |
| 129 | 11.6 |

Régression log(q_max) vs log(n) : δ ≈ 0.39 (n ≥ 17).

Prédiction γ = 1 − δ ≈ 0.61 (version barrière = somme) ou γ = 1 − 2δ ≈ 0.22 (version barrière = max).

Or t½ ~ N^3 (loi de puissance), et log(t½) vs N^0.61 donne R² = 0.9816, INFÉRIEUR au R² de la simple loi de puissance (0.9957). L'ajustement Arrhenius est MOINS bon que la loi de puissance.

---

## Objection 7 — L'hypothèse cachée la plus grave : la clique est LE goulot

**Gravité : MAJEURE.**

Rien ne démontre que la transition (le processus lent) est le remplacement d'un membre de la clique. D'autres mécanismes sont possibles :

- La lenteur pourrait venir de la **diffusion** du sommet à travers un paysage d'énergie complexe, sans qu'une clique soit impliquée.
- Plusieurs structures pourraient coexister et le goulot pourrait être entre elles, pas à l'intérieur.
- Le mode lent pourrait être un phénomène collectif (réarrangement global) plutôt que le remplacement d'un sommet dans une clique.

Le rapport M11 montre que 87–97 % de la masse triangulaire est portée par une aristocratie, mais « aristocratie » ≠ « clique ». Les sommets aristocratiques pourraient être reliés entre eux par des chemins denses sans former une clique.

---

## Résumé des objections

| # | Objection | Gravité | Effet sur γ = α − δ |
|---|---|---|---|
| 1 | Barrière ≠ somme des coûts ; max vs somme change l'exposant | MAJEURE | Pourrait être γ = α − 2δ ou autre |
| 2 | δ dépend de ce qu'on mesure ; q_eff et q_max donnent des δ très différents | MAJEURE | δ indéterminé |
| 3 | t½ suit une loi de puissance, pas Arrhenius | MAJEURE | L'hypothèse est contredite par la forme fonctionnelle |
| 4 | Le terme D facilite peut-être le démantèlement ; T/total = 0% dans les mesures | MODÉRÉE | La barrière pourrait ne pas exister |
| 5 | Le chemin de transition Metropolis ≠ retrait ordonné | MODÉRÉE | La barrière est surestimée |
| 6 | L'ajustement Arrhenius est moins bon que la loi de puissance | CRITIQUE | Les données contredisent l'hypothèse |
| 7 | Rien ne prouve que la clique est le goulot | MAJEURE | Le mécanisme est hypothétique |

## Verdict du relecteur

La dérivation algébrique (étapes 1–3) est correcte. Les étapes 4–7 contiennent des erreurs et des hypothèses non justifiées :

1. La barrière n'est pas la somme mais le max le long du chemin (erreur de structure).
2. Le δ pertinent est indéterminé (q_eff ≈ 0.08 vs q_max ≈ 0.39–0.50).
3. Les données M11 suivent une loi de puissance, pas un comportement Arrhenius.
4. L'ajustement Arrhenius est systématiquement moins bon que la loi de puissance.

**L'hypothèse γ = α − δ n'est pas soutenue par les données disponibles.** Cela ne signifie pas qu'elle est fausse en principe, mais que la dérivation est trop grossière pour être testable, et que les données actuelles vont plutôt contre elle qu'en sa faveur.

**Recommandation :** si un défi DEFI-M15 est créé, il doit être formulé comme « l'hypothèse γ = α − δ survit-elle à un test correct ? » et non comme « confirmer γ = α − δ ». Les critères de réfutation du protocole (§ 6) sont corrects et devraient être mis en avant.

---

*Statut : TOE démontrée : NON ; candidate digne d'étude : OUI.*
