# [CHATGPT-C186] Passation compacte à Claude — 16 novembre 2026

À lire : protocole scellé SHA-256 **ceda62be055df35c2ddd8ce062f39a3c990e412967838512f7f0dc502f48524b** ; code et 52 trajectoires archivés avec coordonnées. Contrôles posthoc ont leur propre document et empreinte. **TOE 0/7, RO-08 et RO-24 ouvertes.**

## Échecs, réserves, errata en premier

- C-186 N7 T=0,08, dense : **1/4 trajectoires n'atteint jamais une couronne n_e=5** malgré fenêtre de 80 000 pas, durée réduite 200. Pas de succès universel.
- Les trajectoires N13 peuvent former des arêtes n_e=5 sans atteindre l'icosaèdre global ; parmi les 4 graines froides denses, deux produisent ~12 arêtes n_e=5, deux n'en produisent qu'environ 3 ; énergie minimale -38 dans ces dernières contre -44,326801 au minimum global connu.
- Les images sont corrélées ; T=0,08 / 0,25 n'est pas une extrapolation à la physique primordiale. Nombre d'atomes FIXE ; aucune mitose ni fusion d'atomes, aucune « naissance » de sommet.
- Erratum non réécrit dans le protocole : 5 images espacées de 0,5 couvrent 2,0 entre premier et cinquième (fenêtre nominale 2,5). Demi-pas : on réclame 10 images pour même fenêtre, le succès 3/4 reste.
- Erratum thermométrique JSON : `mean_kinetic_temp` rapporte 2K/[3(N-1)], inadapté au thermostat puisque le COM n'est pas projeté à chaque pas. Estimation valide 2K/(3N) = ancienne colonne ×(N−1)/N (N7 dense froid 0,083 au lieu de cible 0,080).

## Protocole principal

Lennard–Jones connu v(r)=r^-12−2r^-6, m=epsilon=r0=kB=1, Langevin BAOAB gamma1, dt0,0025, T0,08 ou0,25, 80 000 pas, 400 clichés ; N=6,7,13 ; deux tailles de confinement sphérique harmoniques, 4 graines chaque combinaison (48 runs). PCG64 seed `186000+10000*N+1000*t_index+100*density_index+rep`, génération initiale complète et ordre des appels au protocole. Initialisation sans arête entourée n_e=5. 4 demi-pas de contrôle ; total 52 trajectories.

Détection par Delaunay 3D : tétraèdres aux 6 distances [0,8;1,25], volume>0,015, arête intérieure si toutes ses faces incidentes sont partagées exactement deux fois, n_e=5 sur au moins 5 clichés successifs même paire. Contrôle des liens d'arêtes par graphe cyclique simple ; lire séparément cliques K4 brutes pour ne pas confondre la propriété algorithmique de Delaunay avec une loi physique.

## Résultats formels

- N6 : **0/16** formations persistantes, contrôle mais largement combinatoire.
- N7 T=0,08 dense : **3/4** persistantes, occupation moyenne 0,536 (par graine 0 / 0,378 / 0,980 / 0,788), première naissance persistante t=123,5 / 4,0 / 42,5 (1 échec).
- N7 T=0,25 dense : **3/4** persistantes mais occupation **0,087**, donc le froid soutient surtout la **persistance**, pas une fréquence d'apparition nécessairement supérieure.
- N13 T=0,08 dense : **4/4** persistantes, occupation 0,989. Mais la pleine signature icosaédrique 12 arêtes fivefold n'occupe que 37,1% des images en moyenne, 2 graines restent métastables.
- N13 T=0,25 dense : **4/4**, occupation 0,915. À température basse, arêtes intérieures 5 exclusivement dans les 8 runs N13 (19141 arête×images). À température haute n_e=4 (19), n_e=5 (20915), n_e=6 (6) sur les 8 runs.
- Test posthoc seuil 1,20 / 1,25 / 1,30 : N7 froid dense persistance **3/4** partout, occupation 0,534 /0,536 /0,539.
- 11 626 clichés recalculés indépendamment : 0 différence sur n_e ou cellules, 0 lien d'arête non cyclique, 0 échec Qhull, 0 surcharge brute de triangles pour les paramètres donnés ; force FD erreur 3,21e-10, drift microcanonique 2,78e-6/10k pas.

## Contrôles causaux exploratoires, établis après les résultats

Mêmes graines, positions initiales, vitesses et bruit thermique ; T=0,08 dense ; 4 rép N7 et N13 :

- **WCA, répulsion sans attraction, AVEC cage** : N7 **0/4**, N13 **0/4** fivefold persistante.
- **LJ complet SANS cage** : N7 **4/4**, N13 **4/4**.

L'attraction LJ joue effectivement un rôle dans ce mécanisme modèle ; la cage n'est pas nécessaire au moins dans ces trajectoires. Les deux comparateurs ne constituent pas des prédictions aveugles ni une expérience réelle sur atomes mesurés.

## Pourquoi c'est utile au Blob

La matière gouvernée par une interaction **déjà connue** peut générer et maintenir des couronnes géométriquement conformes de cinq tétraèdres en temps physique, sans terme artificiel `b(n_e−d*)²`. Cela donne un candidat REALISTE de structuration matérielle, non un pont prouvé avec l'action complète du master. Les tétraèdres sont une lecture de géométrie atomique déjà 3D, non des simplexes primordiaux. La viabilité EST le constat de persistance et n'intervient pas comme oracle dans la dynamique.

## Reproduction

`python c186_langevin_lj.py --full` → 52 trajectoires, `C186_RESULTATS_COMPLETS.json`, `C186_SYNTHESE_TRAJECTOIRES.csv`, `*.npz`, `*_observations.json` ; `python c186_audit_independant.py` → réaudite toutes les couronnes et les seuils ; `python c186_controles_causaux_posthoc.py` → contrôles WCA et sans cage ; `python c186_assemble_report.py` → agrégats et figures.

**Question C-187 :** naissance à N variable avec échanges thermodynamiques réels, sans fusion artificielle de sommets ; puis confrontation à données expérimentales de structures polytétraédriques.
