# [CHATGPT-C235] Passation contradictoire — audit historique des masters

**Objectif prioritaire : détecter les régressions historiques et invalider, si possible, le nouvel énoncé C-235-T1.**

**Sources effectivement dépouillées :** 65 PDF masters/armatures de la bibliothèque de l'auteur, textes de 82 144 pages et déduplication exacte en 9 133 contenus ; V153 30 mai 2026 p. 258–259 ; V293 p. 97–99, 1220–1222 ; V346 p. 642–644, 1165, 1268–1272, 1914–1918 ; V347.2 p. 17–18, 27–29 ; rapport C-59 déjà présent.

## Attaque A : théorème C-235-T1 (sans nouveau paramètre)

Action lue dans V278/V346 : S=α Σ_{e∈E} f(t_e) −β Σ_i(deg_i−deg_moy)^2, t_e = nombre de triangles contenant e. Si α>0, β≥0 et f est croissante avec f(n−2)>0, à nombre de liens libre et sans autre contrainte, K_n maximise S ; c'est le seul maximiseur pour n≥3.

**À réfuter :** fournir un graphe simple n≥3 dont le score est supérieur/égal à celui de K_n sans être K_n sous ces hypothèses. Contrôles livrés pour n=4,5,6, quatre fonctions, total 135 424 graphes évalués. La preuve analytique par bornes sur t_e et |E| est dans le rapport ; si une hypothèse manque, l'expliciter.

**Attention :** cette proposition NE CONTREDIT PAS les campagnes à nombre de liens fixé, ni une action munie d'un vrai coût de liaison ou d'un réservoir fini. Elle teste l'extension non justifiée de l'axiome local à la croissance.

## Attaque B : source historique

1. Existe-t-il une version antérieure à V153 (30 mai 2026), **dans les archives effectivement accessibles**, qui exprime déjà la cristallisation par paliers ? Fournir une page/texte, pas une citation de mémoire.
2. Identifier les premiers scripts et l'action exacte de la campagne V278/V293 : N et M sont-ils fixés dans toutes les branches ? Certaines récompenses incorporent-elles déjà un terme d'arête -c|E| que C-235 aurait omis ?
3. Déterminer si l'hystérésis anciennement mesurée survit sous finitesize scaling, multi-graines et même noyau Q_phys ; ne jamais reprendre « premier ordre prouvé » de manière inconditionnelle.
4. Déterminer quelles analyses V153 de viabilité, rigidité Hodge, d_s≈3, 4PCF et holographie ont été rétractées/supersédées depuis V347.2 ; une analogie physique ne vaut pas identité.

## Attaque C : mécanisme réel

- C59 : la transformation de Doob change des statistiques conditionnelles mais pas les affinités des cycles. Chercher un contre-exemple avec Q réversible et h>0 ; si aucun, maintenir RO-27.
- C59 : coût de la naissance 1↔4 non borné pour l'action B selon valence. Vérifier l'hypothèse que l'on peut augmenter arbitrairement la valence en gardant un secteur de triangulations admissible. Si ce point échoue, rétrograder la portée.
- Trouver une règle *non arbitraire* de ressources qui empêche les cliques et autorise des volumes physiques sans supposer d=3. Ne PAS réutiliser un des nombreux réglages du corpus comme constante fondamentale.

## Critères de retour

Renvoyer : (i) erreurs de transcription (pages et statut) ; (ii) contre-exemple théorème s'il existe ; (iii) faux acquis historiques ; (iv) plus ancien résultat déjà équivalent à C-235 ; (v) une seule recommandation d'expérience nouvelle avec un témoin négatif. **TOE 0/7 inchangé.**
