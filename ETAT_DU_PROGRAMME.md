🇫🇷 Français · 🇬🇧 [English version](en/PROGRAMME_STATUS.md)

# État du programme — octobre 2026

*Note d'état rédigée pour l'ouverture du laboratoire public (version 1.0 du dépôt, 6 octobre 2026). Elle s'appuie exclusivement sur l'armature canonique V347.1 (9 septembre 2026) et sur l'audit d'organisation du corpus (24 septembre 2026), tous deux publiés ici. En cas de divergence, l'armature V347.1 fait foi.*

> **TOE démontrée : NON.** Programme de recherche spéculatif formalisé, candidat à évaluation externe.
> Portes G0–G5 : ouvertes · G6 : externe · Portes physiques : 0/7.
> Niveau actuel selon le propre barème du corpus (Core 1.0 §7–§10) : **niveau 1 — modèle mathématique reproductible**. Les étiquettes « candidate de gravité quantique » ou « candidate TOE crédible » ne sont pas utilisables avant les seuils supérieurs. Le Blob Principle se présente donc ici comme **candidate déclarée et humble**, au tout premier palier, qui demande à être éprouvée.

---

## 1. La règle de lecture

Le corpus applique à lui-même une discipline que ce laboratoire reprend telle quelle :

- **Étiquettes épistémiques** — [T] théorème · [CERT] certificat fini · [M] mesure · [DEV] développement · [H] hypothèse · [OPEN] obligation ouverte · [FAIL] échec · [R] rétracté · [EXT] validation externe · [ARCH] résultat d'un modèle archivé · [A] axiome · [DEF] définition · [METH] règle méthodologique · [R-ALG] erreur algébrique héritée, corrigée.
- **Les échecs sont montrés en premier** et ne sont jamais reformulés pour paraître des succès.
- **Aucune résurrection** : un résultat [R] ou [FAIL] peut être raconté comme provenance, il ne redevient jamais vrai par répétition.
- **Aucun [T] historique n'entre sans recalcul direct.** L'armature V347.1 a déjà trouvé trois classes d'erreurs qui avaient traversé des centaines de pages ; elle suppose que d'autres existent jusqu'à preuve du contraire.
- **Rasoir d'Ockham** : trois chemins de validation indépendants (analytique, multi-graines avec barres d'erreur, validation croisée par trois algorithmes).
- **Tribunal de huit relecteurs hostiles** (probabiliste, physicien théoricien, philosophe des sciences, cosmologiste observationnel, topologue, théoricien de l'information, statisticien bayésien, expérimentateur).

## 2. Le cadre en une page

Le Blob Principle se lit en **miroir** : un *récit* cosmogonique (Livre I) et son *jumeau mathématique* (Livre II), l'écart entre les deux étant consigné comme **résidu** — PORTÉ (le formalisme dit ce que dit le récit), AFFAIBLI (il en dit moins), CORRIGÉ (il le contredit et le récit cède), ABSENT (aucun objet n'existe encore).

Formellement, le corpus contient trois strates qu'il faut distinguer :

| Strate | Objets | Dynamique | Rôle |
|---|---|---|---|
| **A_gen** | complexes simpliciaux abstraits, lignée σ, mitose μ, N variable | croissance généalogique partielle | origine / cascade |
| **A_Gibbs** [ARCH] | graphe Rips/flag à N fixé, fonctionnelle *S_sim(C) = log(1 + n_tri(C)) − βD(C)* | échange d'arêtes + mesure de Gibbs | sélection historique |
| **B** (B_shell, B_full) | triangulations finies de T³, action *S(T) = μN₃ + Σₑ f(nₑ)* | Pachner 2↔3 (et 1↔4) | secteur canonique G0 |

Les deux ponts A_gen → A_Gibbs (RO-25) et A_Gibbs → B (RO-08) **ne sont pas construits** : la cosmogonie et le secteur canonique forment aujourd'hui une généalogie de modèles, pas encore une dynamique unique dérivée de bout en bout.

## 3. Ce qui tient (extraits, avec statut)

Liste non exhaustive ; chaque énoncé renvoie à l'armature V347.1, qui renvoie elle-même aux pages du master V346.

- **Objet initial Ω⁰** : initialité catégorielle, trivialité homologique, absence de structure brisable [T].
- **Mitose simpliciale μ** : bien définie, unique de Ω⁰ vers Ω¹, combinatoirement réversible [T].
- **Lignée σ** : neutralité globale sous hérédité et cardinalités égales [T, trivial] ; la sélection par *S_sim* ne crée ni n'efface la lignée [T, structurel][ARCH] ; mesure de deux domaines cohérents (~94 %) sur le régime de cascade [M][ARCH].
- **Lyapunov KL** du sampler historique : *ℒ[ν] = τ KL(ν‖π_N)* décroît sous tout noyau laissant π_N invariante [T][ARCH] — propriété mathématique, qui ne fait pas du sampler une dynamique physique.
- **Branche R-TRUE / pull-back / MARKED** (secteur canonique) : la plus certifiée du corpus ; transmission d'information sous changement d'échelle PORTÉE ; marge locale positive mesurée sur six configurations à R = 3 et R = 4 [M] ; **no-go d'uniformité ponctuelle** démontré [T].
- **Dimension 3** : le master V346 la revendique par deux routes, spectrale et géométrique (plateau mesuré de dimension spectrale proche de 3). Ces revendications historiques ne sont pas encore retranscrites dans V347 et restent soumises à la règle « aucun [T] historique sans recalcul » ; le maillon SUP-1 est à lire avec la précaution du § 5.

## 4. Ce qui a été corrigé, rétracté ou a échoué

Montré ici en clair, parce que c'est ce qui rend le programme scientifique :

- **[FAIL] Q-TIME** : la mesure stationnaire ne fixe ni le générateur physique, ni son spectre, ni une horloge ; il faut séparer Q_samp et Q_phys (RO-06).
- **[T] NO-GO μ-seule** : la mitose seule ne produit ni cycle, ni triangle, ni tétraèdre ; un mécanisme de fermeture est nécessaire (RO-24). L'écriture « μ∘μ∘μ : Ω⁰ → Ω² » est rétractée [R].
- **[T]/[R] Correction ∂Δ²/Δ²** : le bord du triangle porte la boucle, le triangle rempli est contractile.
- **[R] Seuil dissipatif universel à Ω³** : non démontré ; des configurations de dimension ≤ 2 peuvent avoir D > 0 (RO-23).
- **[R-ALG] Signe de l'énergie libre** hérité de V346 : corrigé par *ℒ = τ KL*.
- **τ_c ≈ 0,40** : valide seulement dans une tranche paramétrique ; toute prétention universelle est retirée.
- **Chiralité** : la viabilité est aveugle à la parité ; l'orientation est héritée de la généalogie, pas fabriquée par la sélection (résidu CORRIGÉ).
- **Nucléation depuis le vide strict** : 0/40 graines sous les deux moteurs canoniques ; la mesure initiale « P = 1,00 » reposait sur un germe non vide (RO-02).
- **Correspondances cosmologiques historiques** (dérivations de Hubble, Ω_DM/Ω_b, quatrième lepton, etc.) : [R]/[FAIL], exclues de toute revendication.
- **Méthode D102** (activité pondérée absolue) : morte ; concordance Γ_min/s retirée.

## 5. Précaution de lecture du master V346

L'audit du 24 septembre 2026 relève que le master V346 porte **quatre verdicts successifs sur SUP-1**, de « frontière ouverte » en tête du document à « SUP-1 EST FERMÉ » dans la partie CLXXVI (18 juillet 2026). **Le plus récent fait foi**, mais rien ne le signale au lecteur qui commence page 1. Quatre points d'audit restent ouverts sur ce verdict :

1. l'hypothèse (H1) pose un degré **borné**, alors que sa vérification fournit un degré en **O(log N)** ;
2. l'ordre des limites n'est pas spécifié — à N fini, t → ∞ donne un exposant nul ;
3. le théorème vit sur un **3-tore**, alors que le moteur v137 tourne sur un **cube à bord** ;
4. l'étiquette (H1)–(H3) désigne **quatre triplets différents** dans le même document.

Ces quatre points sont une **porte d'entrée idéale pour un premier contributeur**.

### La « pince spectrale » ne se referme pas en l'état

L'audit du 18 septembre 2026 ([audits_18-09-2026/](corpus/02_portes_et_audits/audits_18-09-2026/)) établit, à partir de l'exposé de Delmotte lui-même (Séminaire de théorie spectrale et géométrie, Institut Fourier, 1997–1998, en accès libre sur Numdam), que le théorème invoqué pour fermer **INF-1** exige deux hypothèses : une ellipticité uniforme A*(α), qui impose un **degré borné par 1/α**, et une boucle en chaque sommet, p(x,x) ≥ α. Conséquences :

- **INF-1 comme [T] fermé n'est pas justifié en l'état** ; son applicabilité au corpus est une question ouverte [Q], conditionnée au degré uniformément borné, au doublement de volume et à l'inégalité de Poincaré.
- Le corpus contient une contradiction interne : une section ferme INF-1 par Delmotte, tandis que les annexes V232 et V236 retirent Delmotte (non-régularité d'Ahlfors mesurée, d_w ≈ 2,84). Le théorème étant une équivalence, les deux positions ne peuvent coexister.
- **Tension avec SUP-1** : SUP-1 s'appuie sur un cadre non elliptique (Procaccia–Rosenthal–Sapozhnikov), INF-1 exige l'ellipticité uniforme. Un même objet doit satisfaire les deux pour que la pince spectrale se referme : **non résolu**.
- Point favorable : l'obstruction de parité que la boucle sert à contourner est vraisemblablement bénigne ici, les graphes du corpus étant saturés de triangles.

### Échantillonnage C2-R (RO-12)

L = 4 validé (R̂ < 1,002 ; ESS > 3 300). L = 5 validé (R̂ = 1,003 ; ESS = 800 ; quatre départs surdispersés). **L = 6 non concluant** (budget de calcul à environ 17 % du requis). L = 7 hors champ. Un contributeur disposant de puissance de calcul peut faire avancer directement ce point.

## 6. Le registre des 27 recherches ouvertes

Chaque recherche ouverte (RO) possède un critère de clôture, un falsificateur ou une borne de revendication. **Une contribution qui fait passer un résidu de PORTÉ à CORRIGÉ est un résultat scientifique complet.**

### Bande A — porte G0 / continuum (bloque directement G0)

| RO | Objet et pièce manquante | Clôture / falsificateur |
|---|---|---|
| RO-12 | C2-R confirmatoire : réplication indépendante, tailles tenues | F-G0-1 |
| RO-13 | GEN-4 *typical-set* : marge locale uniforme sur secteur typique | F-G0-2 |
| RO-14 | MARKED ↔ CONNECTED : intertwiner en norme déclarée | F-G0-3 |
| RO-15 | Cutoff / limite projective : convergence sous retrait du régulateur | F-G0-4 |
| RO-16 | C4/C5/C7 : défaut, point fixe non trivial, universalité | F-G0-5 |
| RO-18 | Fenêtre finie → limite thermodynamique | borne de revendication |

### Bande B — intégrité du miroir causal (récit et formalisme peuvent-ils devenir une seule théorie ?)

| RO | Objet et pièce manquante | Clôture / falsificateur |
|---|---|---|
| RO-20 | Définir « persister » indépendamment de π > 0 | critère robuste, non arbitraire |
| RO-21 | Accessibilité globale / irréductibilité | composantes exactes ou preuve |
| RO-22 | Amélioration générationnelle | test de monotonie / non-monotonie |
| RO-23 | Seuil dissipatif général | dissipation physique positive avant Ω³ tue la version forte |
| RO-24 | Générateur de fermeture | aucune fermeture locale compatible tue la cascade causale |
| RO-25 | Pont croissance → Gibbs | aucune extension jointe compatible |
| RO-08 | Pont A_Gibbs → B | topologie non contrôlable |
| RO-26 | Espace d'états jumeau global | incompatibilité dynamique / RG |
| RO-06 | Q_samp ≠ Q_phys | aucun générateur physique admissible |
| RO-05 | Lignée σ sur T³ | incompatibilité avec quotient / Pachner |
| RO-10 | Opération de réduction ℛ (le bain) | incompatibilité dynamique |
| RO-09 | Couplage lignée–structure | terme impair forcé nul |
| RO-17 | Dissipation / rigidité sur T³ | non-reproduction sous action canonique |
| RO-07 | Articulation t₁ / t₂ | diagnostics historiques non reproduits |
| RO-27 | Comptabilité entropique locale | absence de production locale cohérente |

### Bande C — fondations et bornes de revendication

| RO | Objet et pièce manquante | Clôture / falsificateur |
|---|---|---|
| RO-02 | Nucléation Ω⁰ → Ω¹ + convention frontière de D | protocole robuste (≥ 30 graines, P ≥ 0,9 depuis le vide strict) ou borne négative |
| RO-04 | Deux simplexes simultanés | réduction à des opérations existantes ou nouvelle opération explicitée |
| RO-03 | Dérivation du bit σ₀ | clôture en axiome si obstruction depuis Ω⁰ |
| RO-11 | Rapport η | interdit avant bain formel et dérivation Core |
| RO-19 | Topologie imposée (T³) | borne de revendication |
| RO-01 | Premier mouvement | hors cadre par l'axiome A2 |

## 7. Feuille de route du laboratoire

1. **Ouverture** (octobre 2026) — publication du corpus, DOI Zenodo, appel à collaboration.
2. **Réplications** — RO-12 (C2-R confirmatoire) et RO-02 (nucléation) sont accessibles avec les scripts publiés.
3. **Audit SUP-1** — clore les quatre points du § 5 et publier une note de supersession.
4. **MASTER V347 complet** — dépouillement de V346 selon le protocole de l'armature (ordre de risque causal), puis gel par empreinte SHA-256.
5. **Livre différé de confrontation** — seulement après le gel, sous les quatre verdicts : identité, compatibilité, analogie, échec.

*Une nouvelle version maîtresse n'est produite que lorsqu'un résultat [T] nouveau ou la fermeture d'une porte le justifie — jamais pour un résultat négatif ou une campagne de contrôle.*
