🇫🇷 Français · 🇬🇧 [English version](en/CONTRIBUTING.md)

# Contribuer au laboratoire du Blob Principle

Merci de vouloir éprouver le Blob Principle. Ce document fixe les règles, reprises de l'armature canonique V347.1 (Livre III, § III.2).

## 1. Avant tout

1. Lisez le [bloc de statut](ETAT_DU_PROGRAMME.md) : **TOE démontrée : NON**. Toute contribution qui le contredit sans preuve sera refusée.
2. Lisez l'[accord de contribution (CLA)](CLA.md). Toute contribution intégrée au corpus suppose son acceptation.
3. Identifiez la **recherche ouverte (RO)** que vous attaquez, ou ouvrez une *issue* « Critique » si vous contestez un résultat existant.

## 2. Types de contribution

| Type | Ce qu'il faut fournir |
|---|---|
| **Preuve** (vers [T]) | Énoncé complet, toutes les hypothèses déclarées, preuve, renvoi aux définitions de V347.1 / V346 |
| **Réfutation** (vers [R] ou [FAIL]) | Contre-exemple ou argument, reproductible ; une réfutation propre est un résultat complet |
| **Réplication / mesure** (vers [M] ou [CERT]) | Code, environnement, données ou générateur déterministe, **graines**, **empreintes SHA-256**, test négatif, séparation DEV / CONFIRMATORY / HELD-OUT |
| **Confirmatoire** | Tout ce qui précède **plus un second moteur indépendant** |
| **Critique méthodologique** | Point précis, page ou fichier visé, conséquence sur un statut |
| **Lecture, traduction, vulgarisation** | Signalements d'obscurités, propositions de clarification, traductions |

Toute contribution qui modifie un statut s'accompagne d'un **rapport de supersession** : quel énoncé, quel ancien statut, quel nouveau statut, pourquoi.

## 3. Étiquettes épistémiques

[T] théorème · [CERT] certificat fini · [M] mesure · [DEV] développement · [H] hypothèse · [OPEN] ouvert · [FAIL] échec · [R] rétracté · [EXT] validation externe · [ARCH] modèle archivé · [A] axiome · [DEF] définition · [METH] méthode.

Règles : les échecs sont montrés en premier ; rien de rétracté n'est ressuscité ; aucune identification à un objet physique (photon, graviton, Modèle Standard, ΛCDM…) n'est admise dans un énoncé formel avant le livre de confrontation.

## 4. Procédure

1. **Issue** — ouvrez une *issue* avec le modèle adapté (« Attaque d'une recherche ouverte », « Critique / réfutation », « Réplication », « Question »).
2. **Discussion** — l'auteur et la communauté examinent la démarche avant le travail lourd.
3. **Pull request** — déposez vos fichiers dans `contributions/RO-xx_votre-nom/` (ou `contributions/critique_votre-nom/`). Cochez l'acceptation du CLA dans la description.
4. **Revue** — revue contradictoire, sur le modèle du tribunal des huit relecteurs.
5. **Intégration** — l'auteur décide de l'intégration au corpus et de tout changement de statut. Le contributeur est inscrit dans [CONTRIBUTEURS.md](CONTRIBUTEURS.md) et cité dans le master qui intègre son apport.

## 5. Ce qui ne sera pas accepté

- La modification directe des fichiers du corpus d'origine (masters, livres) : ils sont figés et horodatés. Les apports vont dans `contributions/`.
- Une revendication sans reproductibilité, ou une promotion d'analogie en identité.
- Un code soumis à une licence incompatible, ou dont vous n'êtes pas l'auteur.
- Toute présentation d'une contribution comme une théorie distincte revendiquant la paternité du Blob Principle.

## 6. Conduite

Critiquez les idées, jamais les personnes. Voir [CODE_DE_CONDUITE.md](CODE_DE_CONDUITE.md).
