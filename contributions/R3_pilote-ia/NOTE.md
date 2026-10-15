🇫🇷 Français · 🇬🇧 [English version](NOTE_EN.md)

# DEFI-R3 — Erreur de comptage des triangles dans le moteur archivé « V109 »

*Pilote IA du laboratoire (Claude, Anthropic), 15 octobre 2026. Trouvée en réécrivant l'échantillonneur pour DEFI-M7. Non relue par une personne.*

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1. Aucun changement de statut.

## Constat

Le moteur MCMC « V109 » imprimé dans le master V346 (p. 291–292 imprimées, p. 339–340 du PDF) met à jour le nombre de triangles par `n_tri_new = n_tri - common_rm + common_add`, où `common_add` est calculé sur le graphe **avant** le retrait de l'arête (u, v). Rien n'interdit que l'arête ajoutée partage une extrémité avec l'arête retirée.

**[T]** Si l'arête ajoutée est (u, w) et que v est voisin de w, le triangle {u, v, w} est compté dans `common_add` alors que l'arête (u, v) vient de disparaître. L'erreur est toujours un excès : le compteur suivi dérive vers le haut, et l'acceptation de Metropolis s'appuie sur ce compteur faux, donc la chaîne n'échantillonne pas exactement π.

**[M]** Listage exécuté tel quel (N = 300 et 500, 3 graines chacun, 20 000 et 50 000 pas) : n_tri suivi supérieur au recomptage de 1,4 % à 2,7 %, dans les 6 cas.

## Portée

- Le moteur canonique actuel (`blob engine.py`) n'est **pas** concerné : il exclut les paires candidates qui touchent u ou v.
- Les résultats produits avec V109 sont déjà classés [ARCH] ; cette erreur s'ajoute aux raisons de ne pas les transporter sans recalcul.

## Reproduire

`python3 contributions/R3_pilote-ia/verif_v109_n_tri.py` (pdftotext requis ; quelques secondes).
