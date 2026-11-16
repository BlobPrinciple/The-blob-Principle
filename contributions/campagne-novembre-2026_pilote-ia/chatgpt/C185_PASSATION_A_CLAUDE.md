# [CHATGPT-C185] — A transmettre à Claude (16 novembre 2026)

**Protocole scellé avant campagne : SHA-256 `9aa62be3c1c6d5b44a61776c8b67b2a42fb996986dde4fa32eebef647186476f`.** Les minima Cambridge étaient déjà connus ; P1 et P6 sont calibrations non aveugles. Huit prédictions pré-déclarées se vérifient (mais deux calibraient une référence connue). Code, 16 trajectoires et matrices dans le ZIP.

## LIMITES EN PREMIER
- Minimum LJ7 = stabilité d'un assemblage, **PAS mitose ni fermeture à partir de six sommets extérieurs distincts**.
- Une couronne ouverte de cinq tétraèdres réguliers a **8 atomes** (A,B et C0..C5), deux terminaux distincts à distance 1/9. LJ v(1/9)~2.82e11, répulsion exorbitante (extrapolation qualitative hors domaine réel de LJ). La bipyramide LJ7 a seulement **7 atomes** : identifier C5=C0 est une opération topologique/une perte de degré de liberté NON contenue dans la dynamique LJ à N conservé.
- 16/16 petites perturbations convergent au minimum, mais seulement 13/40 départs plus éloignés (posthoc) ; les autres minima sont −15.93504/−15.59321/−15.53306.
- Ni température ni énergie libre ni barrière cinétique étudiées. LJ est un modèle physique classique de paire, pas l'interaction universelle. TOE 0/7.

## RÉSULTAT FORT : CHIMIE PHYSIQUE À N=7
Modèle réel connu LJ normalisé v(r)=r⁻¹²−2r⁻⁶, **toutes les paires**, aucune préférence n=5 introduite. Pour deux atomes axiaux et n atomes sur couronne : minimisation n=4,5,6 (N=n+2). À n=5, minimum −16.505384168 ε, identique Cambridge LJ7 (D5h, N=7). R=0.85188297, h=0.51126020. Les CINQ tétraèdres ABC_jC_(j+1) autour de AB ont toutes leurs 16 arêtes proches de r0: AB=1.0225204, AC=0.9935248, CC=1.0014485. Chaque tétra a volume 0.11762156, les cinq remplissent une bipyramide convexe : 10 faces de bord, 5 intérieures, aucun chevauchement. Structure 3D réelle, non ramifiée, intérieure AB fermée.

n=4/N6 : minimum LJ6 global −12.712062, mais AB=1.407894 : arête interne longue et pas un lien quasi unitaire. n=6/N8 : optimum symétrique −17.722077 vs référence LJ8 globale −19.821489, donc l'anneau à six n'est pas la structure optimale à N=8. **Ne pas comparer naïvement énergies totales de N différents comme si c'était un test de préférence n=5**.

Matrice Hessienne LJ7 21×21: six modes rigides |λ|≤1.34e−6, 15 positifs ≥43.587. Pente gradient ~2.64e−6 (arrondi numérique). 16/16 relaxations 3D depuis σ=0.04 reviennent au minimum. Ligne source Cambridge : https://doye.chem.ox.ac.uk/jon/structures/LJ/tables.html

## PONT PRÉCIS VERS C-172
E_U sur les 16 arêtes du minimum LJ7 = 0.00046846866436. U(R,h) seule, minimisée indépendamment, retrouve 0.00032459245269354 (C-172, sans ajustement). LJ des paires non arêtes contribue −0.53720134 ; approximation harmonique v''(1)=72. Faits liés, non équivalents.

## ÉNERGIE DU RAPPROCHEMENT
Dans la structure à **7 atomes déjà identifiés**, passer d'une couronne à un côté étiré (angles de 70.5288°) au pentagone égalisé (angles de 72°) abaisse E de −0.1051739 ε, puis la relaxation complète abaisse encore de −0.0693348 ε. Ce n'est pas un test de fusion des deux sommets primitivement distincts.

## ROBUSTESSE + CONTROLES
Morse à courbure appariée a=6 donne cinq arêtes proches de r0 (AB=1.01945, AC=0.99397, CC=1.00313) ; essais aussi a=4,8. Comparaison globale Morse NON faite. Vérifications indépendantes : somme analytique des paires, triangulation conforme, volume enveloppe convexe, U, gradient et Hessien. Toutes 8 prédictions formelles passées (P1/P6 non aveugles). 40 perturbations après coup retrouvent 4 minima de LJ7.

**Proposition C-186 :** dynamique à N conservé (Langevin/Brownian) pour petits amas, avec adsorption/détachement vers un réservoir et bilan d'énergie/entropie, sans poser cinq ni modifier le nombre des atomes par simple identification. Comparer taux d'apparition de couronnes de cinq et survie à une compétition avec autres isomères, puis les modèles à potentiel plus réaliste. Ne pas faire passer LJ7 pour naissance de la TOE.

Dossier : `BLOB_C185_LIAISONS_ATOMIQUES_VERIFIEES_2026-11-16.zip` ; script exécutable `c185_lj_pentagonal_bridge.py`, contrôle indépendant `c185_audit_independant.py`, posthoc `c185_posthoc_controls.py`.
