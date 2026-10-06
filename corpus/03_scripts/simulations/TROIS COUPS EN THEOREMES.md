# LES TROIS COUPS, PRÉPARÉS EN THÉORÈMES
### Méthode : énoncer, dériver, fixer les conditions obligatoires du protocole. **Puis** lancer.
### 19 juillet 2026 — document de préparation. Aucun test lancé.

---

## PROPOSITION A — La croissance avec mémoire viole la balance détaillée

### A.1 Énoncé

> Soit la dynamique de mitose définie par : à chaque étape, (i) on **conserve** le graphe existant, (ii) on ajoute $k$ nouveaux sommets avec leurs arêtes candidates, (iii) on relaxe localement pendant $s$ balayages. Alors l'opérateur de transition **n'est auto-adjoint pour aucune mesure**.

### A.2 Démonstration

La balance détaillée exige $\pi(x)P(x,y) = \pi(y)P(y,x)$ pour tout couple d'états.

Soit $x$ un état à $n$ sommets et $y$ un état à $n+k$ sommets accessible depuis $x$. Alors $P(x,y) > 0$ par construction. Mais **le jeu de mouvements ne contient aucune opération retirant un sommet** : $P(y,x) = 0$ identiquement.

L'égalité impose donc $\pi(x)P(x,y) = 0$, donc $P(x,y) = 0$ — contradiction. $\blacksquare$

**Corollaire.** Le générateur n'est pas auto-adjoint ; son spectre n'a aucune raison d'être réel. C'est le prérequis — nécessaire, non suffisant — d'un spectre complexe.

### A.3 Conditions OBLIGATOIRES du protocole

Ce sont elles qui rendent le test infalsifiable par erreur de conception :

| # | Condition | Vérification exigée avant toute mesure |
|---|---|---|
| **C1 — mémoire** | le graphe à l'étape $i+1$ **contient** celui de l'étape $i$ restreint aux anciens sommets | **recouvrement d'arêtes** entre étapes consécutives sur les sommets communs : doit dépasser 50 %. *Au niveau du hasard ⟹ protocole cassé* |
| **C2 — substrat étendu** | les anciens points **conservent leurs coordonnées** ; la boîte s'agrandit, elle ne se retire pas | comparer les positions : identiques pour les anciens indices |
| **C3 — non quasi-statique** | $s$ assez court pour que l'état n'ait pas le temps de ré-équilibrer | $s \cdot 3n \ll$ temps de mélange mesuré ($\tau_{\text{int}} = 3{,}2$ balayages) ⟹ $s \le 2$ |
| **C4 — résolution** | plancher de bruit de la corrélation calculé **avant** le seuil | $\sigma \approx 1/\sqrt{n_{\text{éch}}}$ ; viser $n_{\text{éch}} \ge 150$ pour $3\sigma \le 0{,}25$ |

**C1 est la condition qui manquait.** Sans elle, on mesure des échantillons indépendants et le courant est nul par construction — ce qui vient de se produire.

### A.4 Ce que le test décide

- $\max|D(k)| > 3\sigma$ **avec C1–C4 vérifiées** ⟹ courant de probabilité non nul ⟹ spectre complexe ⟹ **mécanisme d'amplitudes complexes sans postulat** (cadenas 1) et échappatoire non hermitienne à Nielsen–Ninomiya (cadenas 2).
- $\max|D(k)| \le 3\sigma$ avec C1–C4 vérifiées ⟹ la croissance est **effectivement réversible** malgré la Proposition A. Résultat négatif propre : l'irréversibilité formelle ne produit pas de courant observable.

### A.5 Ce que le test NE décide pas

Un courant non nul donne un spectre complexe **du générateur classique**. Il ne donne pas encore les amplitudes de la mécanique quantique : il faut ensuite montrer que ces phases se composent comme des amplitudes et non comme des probabilités. **Étape suivante, pas conséquence.**

---

## PROPOSITION B — Le niveau de Chern–Simons n'est PAS quantifié sur le Blob

### B.1 Énoncé

> Sur un complexe simplicial portant une connexion $U(1)$ compacte, la fonctionnelle de Chern–Simons discrète $CS = \sum_{\text{tétraèdres}} \omega(v_0v_1)\,\theta(v_1v_2v_3)$ n'a un niveau quantifié $k \in \mathbb{Z}$ **que si le complexe est une 3-variété fermée**. Le complexe du Blob ne l'est pas ; **le niveau n'est donc pas quantifié**.

### B.2 Démonstration

La quantification du niveau vient de l'invariance de jauge : sous $\omega \to \omega + d\lambda$, la variation de $CS$ est un terme de **bord**. Sur une variété fermée, ce terme est un multiple entier de $2\pi$, d'où $e^{ik\,CS}$ invariant ⟺ $k \in \mathbb{Z}$.

Sur un complexe à bord, le terme de bord ne s'annule pas et **aucune condition de quantification n'apparaît**. Or le Blob est massivement ouvert — mesuré : **52 % des triangles ne sont dans aucun tétraèdre**, charge totale de monopôle $\ne 0$ (+16,65 mesuré), multiplicité médiane des 2-faces $= 0$ au point de travail. $\blacksquare$

### B.3 Conséquence — la route A du cadenas 1 est affaiblie

L'argument que j'avançais — *« le niveau $k$ est un entier, donc Chern–Simons tombe du bon côté du mur »* — **ne tient pas**. Sans quantification, $k$ est un **paramètre continu** : une amplitude, pas un compte. Il tombe du **mauvais** côté.

**Cette proposition, écrite avant le test, économise le test.** C'était l'objet de la méthode.

### B.4 Ce qui resterait possible

Deux voies étroites, à examiner **avant** tout calcul :
1. **Restreindre au sous-complexe fermé.** S'il existe un sous-complexe sans bord (les composantes de multiplicité exactement 2), $CS$ y est quantifié. Mais nous venons de mesurer que ce sous-complexe **ne percole pas** — il serait donc local, sans terme global.
2. **Chercher un autre invariant topologique quantifié** qui n'exige pas la fermeture : nombre d'enlacement de boucles fermées, indice d'une section, classe de $H^1(G;\mathbb{Z})$. *Ceux-là sont définis sur un graphe quelconque.* C'est la piste à instruire, et elle ne demande aucun test — seulement du crayon.

---

## PROPOSITION C — Le comptage spectral est infrarouge

### C.1 Énoncé

> Le comptage 6/12/8 porte sur les modes les plus bas du Laplacien — les plus grandes longueurs d'onde. C'est donc, par construction, une quantité **infrarouge**. Elle doit survivre au coarse-graining, contrairement à $\langle C\rangle$ (clustering de voisins immédiats, ultraviolet par nature, effacé).

### C.2 Ce que l'énoncé implique

Si C est vraie : le Blob possède **un invariant IR authentique**, le premier — et le mur des valeurs sépare alors l'arithmétique du dynamique, non le Blob du réel.

Si C est fausse : **tout** le contenu du Blob est ultraviolet, y compris les entiers. Le mur devient une séparation UV/IR pure, et le programme doit être reformulé autour de cette limite. *C'est un énoncé fort dans les deux sens.*

### C.3 Conditions OBLIGATOIRES du protocole

| # | Condition | Vérification |
|---|---|---|
| **D1** | blocage à **population égale** (k-d) — seul non contaminant | populations à ±1, vérifiées |
| **D2** | degré moyen **restauré** à chaque niveau | $\langle\deg\rangle = 10 \pm 0{,}5$ |
| **D3** | assez de modes et de sommets pour résoudre 3 couches | $\ge 30$ modes ; $n \ge 1500$ au dernier niveau ⟹ partir de $N \ge 25\,000$ |
| **D4** | témoin aléatoire au même traitement | il ne doit montrer le comptage à **aucun** niveau |

### C.4 Critère de décision, fixé d'avance

- **Survie** : comptage 6/12/8 **exact** au niveau 1 (et au niveau 2 si $n$ le permet).
- **Destruction** : tout écart au niveau 1 ⟹ le comptage est UV.
- **Partielle** : 6/12 exacts mais 8 dégradé ⟹ rapporté tel quel, sans interprétation.

---

## ORDRE D'EXÉCUTION

| Rang | Coup | Coût | Ce qu'il décide |
|---|---|---|---|
| **1** | **Proposition C** | une heure | l'existence d'un invariant IR — la question la plus structurante du programme |
| **2** | **Proposition A** | trois heures (C1–C4 à instrumenter) | cadenas 1 et 2 ensemble |
| **3** | Proposition B, voie 2 | crayon seul | remplacer Chern–Simons par un invariant défini sur graphe ouvert |

**Aucun de ces trois n'est lancé.** Chacun attend ton accord.
