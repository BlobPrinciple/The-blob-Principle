# [CHATGPT-C213] — passation pour contre-audit Claude

**18 novembre 2026**. Protocole ecrit avant calcul : `C213_PROTOCOLE_AVANT_CALCUL.md` (SHA-256 `6b6c98d9a4ebf8760651d1981e78e1479324ee95e47273c27384d6164a29cc05`). Les calculs et l'archive sont scelles apres execution, non contre-audites de facon aveugle par un tiers.

## Mes limites avant mes resultats

L'auteur a dit : la viabilite examine toutes les possibilites hors du temps et retient ce qui tient/continue. **Je ne lui attribue pas** la matrice Q, l'usage de probabilites, le h-transform, les taux, l'existence d'une mesure sur les histoires ou une loi de l'elan. L'article scientifique d'origine sur le Q-process predate le Blob. **TOE 0/7, aucun verrou ferme**.

## Test hostile requis

Ecrire ta propre preuve et/ou un programme sans lire `C213_CONTRE_CALCUL.py`, pour cinq affirmations ; lire seulement le protocole.

1. Un etat s avec s->s de probabilite 1/2, et s->mort de probabilite 1/2, a une *histoire logique* infinie, mais sa probabilite de survie infinie vaut 0.
2. Q fixe = [[1/4,1/4],[1/4,1/2]], probabilites d'echec complementaires. Verifier `P_i(X1=j | tau>n)=Qij*(Q^(n-1)1)_j/(Q^n1)_i`; limite Q*=Qij*h_j/(lambda*h_i), lambda=(3+sqrt(5))/8, h=(1,phi). Valeurs A->B .6180339887499, B->A .2360679774998.
3. Sur ce Q symetrique, Q* est reversible ; distribution stationnaire proportionnelle a h^2 ; aucun courant net permanent, donc pas de fleche du temps tiree de l'experience.
4. **No-go universel :** pour une *quelconque* matrice stochastique P (meme non irreductible) et c in (0,1), poser Q=cP, echec=1-c. Alors conditionner sur la survie a n donne exactement P, pour tout horizon n>=1. Prouver sans supposer Perron simple. Cela signifie que la viabilite seule peut accompagner n'importe quelle loi P et n'en selectionne aucune.
5. Le support des histoires binaires ne fixe pas leur mesure : Bernoulli p dans (0,1) ont meme support mais frequencies typiques p differentes.

## Question au corpus, sans souffler la solution

Sans inventer de source d'energie, de force de viabilite, de taux ni de geometrie, existe-t-il un **axiome de l'elan** deja ecrit dans le master qui elimine effectivement l'arbitraire de P et implique une contrainte de fermeture des volumes ? Si absent, le dire. Distinguer le recit du master (hors preuve) de l'armature formelle V347.1.

## Controle important

Ne jamais traduire `P(tau=inf)=0` en `aucune histoire infinie n'existe` ; et ne jamais lire le Q-process, defini comme une limite de conditionnements, comme une preuve que l'histoire conditionnee existe avec probabilite positive dans le processus original.

Sources : dossier `C213_RAPPORT_SCIENTIFIQUE.md`, `C213_RESULTATS.json`, code et CSV ; aucune modification du depot GitHub.
