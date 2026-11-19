# [CHATGPT-C217] À contre-vérifier par Claude

Statut : TOE 0/7, aucun verrou physique ferme.

**Rectifications approuvées :** les donnees 92/99/100 % du V346 sont d'origine auteur (modele pose), non reproduites ici; pas de moteurs reconstitues de memoire. « Le tetraedre nait creux puis se calcifie » est une description de l'auteur, et pas un axiome topologique automatiquement interprete.

**[T] Deux complexes sous quatre sommets :** `∂Δ³` et `Δ³` ont le meme 2-squelette (4,6,4), mais respectivement 0/1 trois-simplexe, b2=1/0, chi=2/1. Matrices de bord (F2) rang 3,3,0 versus 3,3,1. Aucun lien interne ne peut etre ajoute a K4. Une convention flag force le 3-simplexe dès que K4 est present. K5 force un 4-simplexe dans le complexe flag, sans interdire pour autant K5 comme graphe de liens physiques 3D.

**Portée strictement locale :** avec nouveaux sommets/liens externes, le remplissage peut se faire par triangulation plus fine; aucun no-go general d'accretion des liens n'est revendique. Les Betti globaux peuvent varier differemment.

**Question centrale d'attribution :** « creux » signifie-t-il (A) region 3D peu dense, (B) coquille topologique avant activation de cellule 3D, ou (C) cavite dans un tissu volumique ? Ne pas attribuer une réponse sans confirmation. Les trois interpretations peuvent coexister mais leur correspondance doit etre formalisee.

**RO-24 :** dans chacun des trois cas, une loi qui fait emerger les cellules geometriques admissibles manque. Proposer un test mesure distincte du nombre de liens, de la topologie des cellules et de la masse/calcification, predite et scellee en amont. L'inspection publique du moteur ne permet pas de certifier le mecanisme dynamique historique manquant. Aucune loi physique derivee de ce resultat.

Reproduction : `python3 verif_homologie.py`. Auditer aussi le statut local versus global des homologies et la contrainte de conservation pendant la naissance.
