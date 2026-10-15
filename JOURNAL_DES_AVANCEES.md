🇫🇷 Français · 🇬🇧 [English version](en/ADVANCES_LOG.md)

# Journal des avancées

> **TOE démontrée : NON** · portes physiques 0/7 · niveau 1 (modèle mathématique reproductible).

Ce journal inscrit, dans l'ordre, chaque contribution **retenue** : vérifiée, rejouée quand elle contient du calcul, et validée par le [pilote](PILOTE_IA.md), qui en a reçu délégation de l'auteur le 15 octobre 2026. Une avancée peut être une preuve, une réfutation, une réplication indépendante ou une erreur trouvée dans le corpus. Une réfutation y a la même place qu'une preuve.

Les contributions faites avec une IA, y compris celles de l'auteur, suivent le même chemin : une *issue* au modèle « Contribution assistée par IA », puis la vérification et la décision du [pilote](PILOTE_IA.md), par délégation de l'auteur ([GOUVERNANCE.md](GOUVERNANCE.md)). Un changement de statut épistémique reste soumis aux seuils de Core 1.0 et l'auteur en est prévenu avant toute publication.

Chaque inscription met à jour l'historique du défi dans [docs/defis.json](docs/defis.json). Une avancée qui change un statut est publiée dans une nouvelle version du dépôt, archivée sur Zenodo.

## Avancées

| N° | Date | Défi / RO | Nature | Contributeur | Résultat vérifié | Effet sur le programme | Trace |
|---|---|---|---|---|---|---|---|
| 1 | 06/10/2026 | DEFI-R1 | Réplication | vérification d'ouverture | `SELFTEST : 4/4` sur machine tierce, numpy 2.5.3 | Reproductibilité de l'auto-test confirmée ; statut inchangé | [DEFIS.md](DEFIS.md#tableau-dhonneur) |
| 2 | 15/10/2026 | DEFI-M3 (RO-24), RO-25 | Réfutation + théorèmes | pilote IA du laboratoire (Claude, Anthropic) ; non relu par une personne | [T] M − N conservé par mitose et échanges à \|E\| fixé ; [CERT] fragmentation à M = N − 1 (P(connexe) = 4,5·10⁻⁷ à N = 7) ; [T] aucune croissance généalogique ne reproduit π (TV ≥ 0,31) ; [CERT] croissance avec fermeture puis relaxation : TV ≤ 0,01 après 2,5 à 4,7 échanges par arête | « Option la plus économique » de RO-24 réfutée pour le moteur à \|E\| fixé ; RO-24 et RO-25 restent ouverts ; défis DEFI-M7 et DEFI-M8 ouverts ; statut inchangé | [rapport](contributions/RO-25_pilote-ia/RAPPORT.md), [#16](https://github.com/BlobPrinciple/The-blob-Principle/issues/16) |

## Évolution des défis

| Date | Version | Changement |
|---|---|---|
| 06/10/2026 | 1.0 | Ouverture : 20 défis |
| 15/10/2026 | 1.1 | Ajout du fil conducteur, du chemin de preuve (P1 à P4, T), de l'état et de l'historique de chaque défi, et des règles d'évolution ; aucun changement de statut |
| 15/10/2026 | 1.2 | Délégation au pilote ; historique de DEFI-M3 ; ouverture de DEFI-M7 (coût du pont RO-25) et DEFI-M8 (fermeture dérivée de S_sim) ; aucun changement de statut |
