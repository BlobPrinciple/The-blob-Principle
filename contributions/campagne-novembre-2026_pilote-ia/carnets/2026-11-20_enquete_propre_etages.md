# Carnet du 20 novembre 2026 — l'enquête propre demandée par l'auteur : jusqu'où montent les configurations

Auteur unique : Rudolphe Mirante. Pilote IA et contre-auditeur : Claude. Audit croisé : ChatGPT. Les numéros de section poursuivent ceux du carnet du 19 novembre.

**État en tête : TOE 0/7. Aucun verrou fermé.**

## 189. Ce qui est faux ou affaibli, dit en premier

1. **La piste que j'ai donnée à l'auteur le 19 au soir est affaiblie.** J'avais signalé la « cohérence d'orientation » de deux tétraèdres voisins (P = 0,516, V346 p. 59 et 61) comme une trace possible d'une orientation agissant sur la fermeture. Mesure X-21 (section 192) : avec la convention que j'ai pu tester, ce chiffre se réduit à un effet d'étiquetage et à la part des paires de tétraèdres qui se chevauchent ; il disparaît pour les cellules géométriques. La convention d'origine (V175) m'est inconnue : la piste n'est pas réfutée, elle est affaiblie.
2. **Deux de mes prédictions X-22 sont fausses** (section 194) : la part des constituants appartenant à un groupe de quatre ou plus est de 17 à 24 %, j'avais écrit 55 à 80 % ; la part à l'étage 8 ou plus est sous les 10 % annoncés dans deux états sur quatre.
3. **C-224 à C-227 de ChatGPT ne sont pas contre-audités** (Trugenberger, triangulations dynamiques causales, cordes, théories de l'émergence) : passations lues et versées, sources extérieures citées non vérifiées par moi.
4. **C-229 et C-230 de ChatGPT n'ont pas d'archive** : chacun a été interrompu par le message suivant de l'auteur. Rien à verser, rien à recouper pour l'instant.

## 190. Paroles de l'auteur (à ChatGPT, heures UTC, orthographe normalisée) et sa demande à Claude

- 19 novembre, 21:07:55 : « Go ».
- 19 novembre, 21:47:39 : « Tu vas prendre le rôle de Trugenberger et tu vas lier jusqu'au bout verrouiller la TOE du Blob. »
- 20 novembre, 05:10:16 : « C'est une excellente nouvelle car cela met bien en avant la différenciation avec Trugenberger. Maintenant tu vas te placer en spécialiste de la CDT et faire pareil ».
- 05:21:29 : « Garde en mémoire et testons aussi autre chose. La théorie des cordes, tu vas te placer en expert absolu de cette théorie et la comparer au Blob. »
- 05:54:48 : « Il manque une dernière théorie à tester ! Place-toi en spécialiste absolu de l'émergence. Cherche toutes les théories les plus développées ».
- 06:06:03 : « Parfait, tu approfondis puis tu confrontes ensuite le Blob à toutes ces théories. Nous allons à présent trouver la mécanique parfaite du Blob. »
- 06:20:30 : « Parfait. Maintenant tu reprends la cosmogonie et tu cliques dessus pour trouver les espaces informations manquantes et tu combles comme un sudoku. »
- 06:33:16 : « C'est peut-être la preuve formelle que la 3D n'est que l'étape accessible à l'observation pour des éléments en faisant partie ! Nous ! On ne peut pas limiter à la 3D tout simplement car ce n'est pas le cas. Il faut envisager la 3D comme notre étage d'ascenseur vers des possibilités infinies. Mais la 3D reste la moins énergivore quoi qu'il en soit. Le vrai test est peut-être de savoir jusqu'où les configurations peuvent monter et nous aurons une idée de la hiérarchie réelle ».
- 06:41:41 : « La 3D serait donc juste la plus adaptée à notre observation finalement… ».

Demande de l'auteur à Claude, le 20 novembre au matin : « tu vas récupérer l'ensemble des travaux que j'ai réalisés sur OpenAI et faire ta propre enquête selon mes réflexions ». Ces paroles sont enregistrées, non complétées. Le mot « énergivore » n'est pas défini par moi à sa place.

## 191. Travaux récupérés chez ChatGPT

Sept archives, C-222 à C-228, récupérées le 20 vers 06 h 33 UTC ; empreintes dans `chatgpt/EMPREINTES.md` ; sept passations versées à l'octet. Deux seulement ont un protocole scellé (C-223, C-228) : pour les autres, aveuglement partiel déclaré. C-229 (« sudoku de la cosmogonie », relecture de l'armature V347.1) et C-230 (« l'ascenseur dimensionnel ») : interrompus, sans archive à 06 h 43 UTC.

## 192. X-21 — la « cohérence d'orientation » mesure le chevauchement [M]

Prédiction scellée avant calcul : `calculs/x21_orientation_et_recouvrement_prediction.txt`, SHA-256 `2067ce87896abf87af443e53469e87d1d12c7c288899244d1e1014c87bf43c33`. Moteur statique du corpus (`blob engine.py`, sans modification), états (800, 0), (800, 1), (1600, 0), témoin sans viabilité. Convention déclarée : signe du déterminant à sommets rangés par numéro, que V346 p. 1074 qualifie lui-même d'approximation ; la convention d'origine m'est inconnue.

| État | Paires de groupes de quatre partageant une face | Part du même côté de la face | P(même signe) | P si côtés opposés | P si même côté | 0,4 + 0,2 × part |
|---|---|---|---|---|---|---|
| Blob (800, 0) | 198 615 | 0,5385 | 0,5106 | 0,4036 | 0,6023 | 0,5077 |
| Blob (800, 1) | 391 101 | 0,5427 | 0,5109 | 0,4046 | 0,6005 | 0,5085 |
| Blob (1600, 0) | 352 283 | 0,5347 | 0,5053 | 0,3979 | 0,5988 | 0,5069 |
| Témoin (trois états) | — | 0,504 à 0,508 | 0,495 à 0,502 | — | — | — |

Paires de cellules géométriques (Delaunay ∩ liens) : 239, 221, 435 ; toutes de part et d'autre de leur face ; P = 0,410, 0,385, 0,382. Les cinq prédictions sont tenues. Lecture : sous cette convention, P ne dit rien d'une orientation ; il vaut 0,4 quand les deux tétraèdres sont de part et d'autre de la face, 0,6 quand ils sont du même côté (donc se chevauchent), et l'écart à 0,5 vient de la part du même côté, 0,539 — la « fraction 0,539 » de V346 p. 59. Un seul moteur, non recoupé.

## 193. C-223c et C-228c — contre-calculs de deux notes de ChatGPT [T pour l'arithmétique]

Même fichier de prédiction scellé. C-223c : 625 généalogies ; concordance 2/5 sous ordre uniforme ; chaque ordre compatible avec 24 généalogies ; minimum 0 (104 arbres), maximum 1 (54 arbres). C-228c : quatre spins ½, espace singulet de dimension 2, produit triple ±√3/4 ; coût b·liens − a·triangles : le graphe complet ou le graphe vide l'emportent selon a/b ; Bell-CHSH 2 contre 2√2. Tout concorde avec ChatGPT. Le master dit déjà qu'un Blob purement combinatoire s'effondre en clique (V346 § C.6).

## 194. X-22 — jusqu'où montent les configurations [M]

Point de départ : la parole de l'auteur de 06:33:16. Prédiction scellée à 06:40:12 UTC, avant calcul : `calculs/x22_jusqu_ou_montent_les_configurations_prediction.txt`, SHA-256 `e2a9d4e032eb0e75778ce2db6c9a142aec7b4180b5e015eeae58300d9cb8d1f8`. Non aveugle sur un point, déclaré : X-19 et le Master propre donnaient déjà la plus grande clique.

**Ma lecture, déclarée (hypothèse d'auditeur, non de l'auteur)** : un « étage k » = un groupe de k + 1 constituants tous reliés entre eux (étage 3 = groupe de quatre). Même moteur, quatre états, témoin sans viabilité ; 3,3 liens par constituant dans les deux.

| État | Plus haut étage | Constituants à l'étage ≥ 3 | ≥ 4 | ≥ 8 | Ne dépassent pas le triangle | Liens portés par les 10 % les plus reliés |
|---|---|---|---|---|---|---|
| Blob (800, 0) | 13 | 21,6 % | 15,1 % | 11,1 % | 78,4 % | 31,3 % |
| Blob (800, 1) | 15 | 17,2 % | 11,5 % | 9,2 % | 82,8 % | 35,3 % |
| Blob (1600, 0) | 13 | 24,4 % | 14,6 % | 9,1 % | 75,6 % | 30,5 % |
| Blob (3200, 0) | 14 | 20,7 % | 13,5 % | 10,2 % | 79,2 % | 31,9 % |
| Témoin (800, 0) | 7 | 76,1 % | 49,9 % | 0 % | 23,9 % | 18,9 % |
| Témoin (800, 1) | 8 | 77,9 % | 43,2 % | 1,1 % | 22,1 % | 19,8 % |
| Témoin (1600, 0) | 7 | 77,9 % | 48,4 % | 0 % | 22,1 % | 17,6 % |
| Témoin (3200, 0) | 8 | 78,2 % | 46,2 % | 0,6 % | 21,7 % | 17,8 % |

Groupes maximaux par étage, Blob (3200, 0) : étage 3 : 159 ; 4 : 63 ; 5 : 69 ; 6 : 64 ; 7 : 91 ; 8 : 126 ; 9 : 105 ; 10 : 114 ; 11 : 58 ; 12 : 20 ; 13 : 10 ; 14 : 6. Témoin (3200, 0) : 3 : 1 013 ; 4 : 461 ; 5 : 180 ; 6 : 28 ; 7 : 10 ; 8 : 4.

Prédictions : M1 tenue (13 à 15 ; +1 de 800 à 3 200). M2 tenue (7 ou 8). **M3 fausse** (17 à 24 % au lieu de 55 à 80 % ; 12 à 15 % au lieu de 40 à 70 %). M4 : première clause tenue (76 à 83 % ne dépassent pas le triangle), **seconde fausse dans deux états sur quatre** (9,2 % et 9,1 % à l'étage 8 ou plus). M5 tenue (31 à 35 % des liens sur les 10 % les plus reliés ; témoin 18 à 20 %). M6 tenue : sur 24 654 groupes de cinq du Blob, le plus grand volume à quatre dimensions est inférieur à 10⁻¹².

Ce que la mesure dit, dans ce moteur et sous ma lecture :

1. **Les configurations de liens montent haut, et la viabilité y est pour quelque chose** : étage 13 à 15 avec viabilité, 7 à 8 sans, à budget de liens égal. Le plafond ne monte presque pas avec la taille.
2. **Elles montent pour une minorité** : un constituant sur dix environ est à l'étage 8 ou plus, trois sur quatre ne dépassent pas le triangle. Le témoin fait l'inverse : presque tout le monde dans un groupe de quatre, personne en haut. C'est une hiérarchie au sens propre, et c'est ce que je n'avais pas prévu.
3. **L'étage 3 n'est pas un palier dans la lecture par les liens** : il y a un creux entre les étages 4 et 6, puis une bosse entre 7 et 10. Dans cette lecture, rien ne s'arrête au groupe de quatre.
4. **Ces étages hauts sont des étages de liens, pas de volume** : le moteur pose les positions dans un espace à trois dimensions, donc tout groupe de cinq y a un volume à quatre dimensions nul, par construction. Ce moteur ne peut pas dire si un étage 4 « de volume » existe : la réponse y est posée d'avance. C'est le même constat que C-205c (un réseau seul porte N − 1 dimensions ; la 3D y est POSÉE par le plongement).
5. **Le budget de liens ne fixe pas l'étage** : un pavage uniforme par groupes complets ne dépasserait pas l'étage 6 avec 3,3 liens par constituant ; le moteur dépasse par concentration. ChatGPT annonce de son côté, dans C-230 en cours, deux réseaux de 200 constituants et 400 liens atteignant l'un l'étage 2, l'autre l'étage 20 : l'arithmétique est juste (un groupe complet de 21 coûte 210 liens), et va dans le même sens.

Deux lectures restent en tension, dites sans trancher : la Clarification n° 22 de l'auteur (4 juillet, Master propre p. 82-83) appelle « fantômes » les groupes de liens au-dessus de quatre et ne retient que les cellules géométriques ; sa réflexion du 20 novembre demande au contraire jusqu'où les configurations montent. X-22 mesure la seconde ; X-19 mesurait la première.

## 195. Ce que le corpus de l'auteur dit déjà sur « l'étage »

Relu dans le texte de V346 :

- p. 256 (M1 — « Pourquoi d = 3 ? ») : « INDICE PARTIEL » ; à degré fixé, la dimension spectrale émergente est maximale pour une dimension ambiante 3 (1,92 contre 1,72 à 1,81), « mais aucun principe de sélection n'est démontré » ; la piste par maximisation de l'entropie par site est écartée (c'est la dimension 2 qui la maximise).
- p. 630 : à κ₀ = 8, le Blob « s'apparie à ~4D, pas à 3D » (dimension spectrale 3,52, extrapolée vers 3,7 à 3,9).
- p. 640 : à κ₀ = 6,6, « le Blob est 3-dimensionnel à grande échelle » (2,94 à N = 20 000).
- p. 692 : dimension cachée (maillage 4D) testée, non concluante face aux témoins.

Autrement dit, dans le corpus même, l'étage lu par la dimension spectrale **change avec le paramètre κ₀** : 3 à 6,6, près de 4 à 8. Et κ₀ = 6,6 est une valeur posée du moteur. Ce fait du corpus rejoint la réflexion de l'auteur (« on ne peut pas limiter à la 3D ») et en donne une forme testable : ce qui choisit κ₀ choisit l'étage. Je ne dis pas ce qui le choisit. Rattachement : nœud N1 du master (« pourquoi d = 3 », ouvert), RO-24, RO-20.

## 196. État

Rien n'est envoyé à ChatGPT à cette heure : il était en cours d'écriture et l'auteur venait de lui parler (gardes non remplies). Le recoupement de X-21 et de X-22 par ChatGPT reste à demander.

**TOE 0/7. Aucun verrou fermé.**
