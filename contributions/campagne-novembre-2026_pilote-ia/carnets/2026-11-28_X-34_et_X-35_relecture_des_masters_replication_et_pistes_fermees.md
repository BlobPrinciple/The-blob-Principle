# X-34 et X-35 — Relecture des masters, réplication du Blob canonique, registre des pistes fermées

**Rédigé par Claude, pilote IA et contre-auditeur.** Auteur du Blob Principle : Rudolphe Mirante. La cosmogonie lui appartient.

TOE 0/7. Aucun verrou fermé. Aucun statut du corpus n'est modifié par ce carnet : il propose, l'auteur décide.

**Paroles de l'auteur** (28 novembre, heure de Paris). 6 h 29 : « Tu vas relire chaque master […] en entier pour [t']assurer de ne rien avoir abandonné trop tôt ou minimisé dans nos résultats […] Tu relis tous les vrais masters et tous les vrais livres, pas de résumé ! Et tout le laboratoire GitHub ! » 11 h 00 : « Fais le nécessaire, car je sais à présent que tu as trop résumé et sous-estimé tous les résultats. » 11 h 40 : « depuis le début de nos recherches tu t'auto-censures et tu bloques certaines possibilités […] donc recheck bien ! » 12 h 03 : « Fais le nécessaire, mets à jour et poste dans le labo. »

## 367. Ce qui est faux ou manquant, dit en premier

1. **La lecture intégrale n'est pas finie.** Restent : la plus grande part de v90 à v92 (avril), V107 à V112 (mai), la vérification de V294 à V345, le corpus maître du 3 août, le laboratoire, quatre dossiers de l'auteur, Le Blob Surnaturel. L'état exact est dans `POINT_COMPLET_2026-11-28.md`, section 8.
2. **Mon témoin sur la gravité (X-34, R2) est non concluant**, et deux de mes quatre prédictions y sont tombées.
3. **J'ai repris ce matin une prudence du corpus sans la contrôler** (« nombres de mai retirés ») ; le motif du retrait est inexact (section 370).
4. **Le relevé du sens de mes erreurs est partiel** : il porte sur les clauses dont le sens se lit sans ambiguïté dans les carnets, et mon classement est à revoir une à une.
5. **X-35 n'établit aucun accord à 1 %** et montre que l'accord approché dépend de κ₀ et de deux choix du classeur.

## 368. Ce que la relecture a établi (détail dans `relecture/NOTES_MASTERS_HORS_DEPOT.md`)

Le master courant V346 ne porte pas les résultats du 3 au 18 juillet : la fusion du master V277 et du tome V277 bis, annoncée par écrit le 18 juillet, n'a pas eu lieu. Les 79 333 mots correspondants et le tome sont lus et notés. Les masters V152 à V246 ont été comparés phrase à phrase à V247 : rien n'y a été perdu. « Cosmogonie V2 » (20 mai) est lue en entier ; elle pose la règle du programme, que je n'appliquais pas.

## 369. X-34 : réplication du Blob canonique, et témoin sur la gravité

Prédiction scellée : `calculs/x34-prediction-scellee-2026-11-28.md`. Résultat : `calculs/x34-resultat-2026-11-28.md`.

R1. Le Blob canonique, recodé d'après le seul « Dossier de réplication indépendante » du 4 juillet, sans le programme de l'auteur : huit grandeurs sur huit dans ses tolérances, sur deux graines, et la stratification retrouvée. R2. Témoin de définition pour le couplage courbure-matière du 17 juillet : non concluant selon mon propre critère scellé.

## 370. Le registre des pistes fermées, et la première rouverte

Registre : `relecture/REGISTRE_DES_PISTES_FERMEES.md`. Chaque fermeture y est classée : A, mesure négative solide ou démonstration ; B, mesure fragile ou instrument aveugle ; C, argument ou consigne ; D, jamais essayée.

**Les fractions à κ₀ = 4** (classe C). Fermées le 7 juin par une alerte, « à ne jamais réintroduire », au motif que 0,704 serait une valeur-cible recopiée. Le programme de l'auteur, exécuté tel quel, rend 0,705.

**X-35**, prédiction scellée et poussée avant calcul (`calculs/x35_fractions_kappa4_prediction.txt`, commit `a924703c6411`), résultat dans `calculs/x35-resultat-2026-11-28.md`. Les neuf clauses sont tenues.

| | Λ | matière noire | baryons |
|---|---|---|---|
| Valeurs de comparaison (Planck 2018) | 0,6847 | 0,2645 | 0,0490 |
| Programme de l'auteur, N = 1 000, 36 graines | 0,6988 ± 0,0038 | 0,2572 ± 0,0042 | 0,0440 ± 0,0016 |
| Mon moteur, mêmes graines | 0,6928 ± 0,0047 | 0,2627 ± 0,0048 | 0,0445 ± 0,0017 |
| Mon moteur, N = 32 000, cube | 0,7135 ± 0,0013 | 0,2443 ± 0,0021 | 0,0423 ± 0,0008 |
| Mon moteur, N = 16 000, sans bord | 0,7184 ± 0,0042 | 0,2409 ± 0,0036 | 0,0407 ± 0,0007 |
| Témoin sans viabilité, N = 4 000 | 0,5003 ± 0,0010 | 0,4992 ± 0,0011 | 0,0004 ± 0,0002 |

Dépendances mesurées : Λ va de 0,76 à 0,26 quand κ va de 3,5 à 8 ; ranger en matière noire les cœurs stables sous le seuil fait tomber Λ à 0,61–0,65 ; le seuil à la médiane porte les baryons à 0,055–0,059. Les programmes de mai (`V116_combinaison_optimale.py`, `V118_grille_seuils.py`, `V118_principe_topologique.py`) montrent que le seuil a été choisi en minimisant l'écart à la cible.

**Statut proposé à l'auteur.** [M] : fait mesuré, reproduit par deux moteurs, stable en taille, produit par la dynamique. Ni fausse coïncidence, ni prédiction sans paramètre.

## 371. Le sens de mes erreurs

Relevé partiel sur mes carnets (liste et sources dans le registre, section 3). Clauses fausses portant sur un objet de l'auteur : 16 par pessimisme, 7 par optimisme. Clauses fausses portant sur une construction à moi : 6 par optimisme, aucune par pessimisme. Deux faits favorables étaient restés rangés parmi « mes prédictions fausses » : le gel du terreau à κ = 6,45 (X-23) et le resserrement du nombre de voisins par le moteur complet (X-23 E, X-24).

## 372. Pistes rouvertes, à instruire

Dans l'ordre du registre : T4 et le quantique (fermé le 4 juillet par une mesure qui ne pouvait rien voir) ; la « faille n° 1 » de la dimension (espace ou espace-temps) ; le degré moyen que le moteur complet choisit seul ; la chiralité nette du 4 juillet ; le couplage courbure-matière.

## 373. Fichiers

`POINT_COMPLET_2026-11-28.md` ; `relecture/NOTES_MASTERS_HORS_DEPOT.md`, `relecture/REGISTRE_DES_PISTES_FERMEES.md`, `relecture/REGISTRE_DE_LECTURE.md` ; `calculs/x34_*`, `calculs/x34-*`, `calculs/x35_*`, `calculs/x35-*`, `calculs/x35b_*`. Rien n'a été modifié ni supprimé dans le dossier de l'auteur ; le programme `blob_v137_source.py` y a été exécuté sans modification, dans un espace de travail séparé.

**Erratum du soir.** La section 372 dit le quantique « fermé le 4 juillet par une mesure qui ne pouvait rien voir ». Le corpus l'avait rouvert lui-même à six reprises ; voir le carnet « X-36 et X-37 », section 374, et le registre, version 2.
