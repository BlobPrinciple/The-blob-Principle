# PASSATION — [CHATGPT-C226] Confrontation cordes / Blob, 20 novembre 2026

TOE 0/7. Objets posés dans ce contrôle : surfaces fermées orientables équilatérales, champ scalaire sur les sommets, constante T, réseau cyclique avec lois de tension, CFT standard avec c_ghost connu. Ce sont des **bancs d'essai**, pas une dynamique déduite du substrat.

## Mes faiblesses d'abord
1. Aucune loi de fermeture du Blob n'est dérivée.
2. La métrique de la feuille d'univers est posée, donc l'émergence de l'espace-temps n'est pas expliquée.
3. La quantification complète de la corde n'est pas reproduite : pas de Virasoro, ghost BRST, invariance modulaire, graviton, ni supercorde générée.
4. Le protocole a été écrit dans la même session que l'exécution, sans scellé antérieur aux hypothèses ; pas d'aveugle et pas de réplication externe.
5. Le couplage dilaton et g_s ne sont pas des conséquences de la topologie seule ; ils ont été posés pour réaliser le poids g_s^{-chi}.

## Claims à contre-recalculer
- T1 : topologie des surfaces : `∂Δ³`=(4,6,4), χ=2, Σδ=4π; `∂octaèdre`=(6,12,8), χ=2, Σδ=4π ; tore périodique 4×4=(16,48,32), χ=0, Σδ=0.
- T2 : sur triangulation équilatérale fermée, `Σδ=2πχ`; démonstration par `3F=2E`.
- T3 : énergie de Dirichlet scalaire sur surface équilatérale `S=T/(4√3) Σ_faces Σ_edges_in_face (ΔX)² = T/(2√3) Σ_edges (ΔX)²`; tester par gradients.
- T4 : exemples : `S_∂Δ³=√3 T/2` avec X=(0,1,0,0) ; `S_tore=224√3 T/3` avec X_i=(i²+3i) mod7.
- T5 : mode de boucle, `ω_k=(N/π)sin(πk/N)→k`, pour L=2π, c=1 ; `spec Lap(K4)={0,4,4,4}`.
- T6 : central charges conventionnels c=D−26 et c=3D/2−15 donnent 26 et 10. **Vérification d'identité conditionnelle et non dérivation depuis le Blob.**
- T7 : le seul secteur A_gen à graphe arborescent ne porte aucune surface fermée à triangles, donc ne construit pas de worldsheet simpliciale par mitose seule.

## Attaque principale demandée
Peut-on produire un exemple de règle de naissance/fermeture **strictement issue des axiomes actuels**, sans seuil géométrique caché, qui constitue une surface simpliciale fermée portant un champ et un couplage nécessaires ? Sinon confirmer RO-24 ouvert. Peut-on montrer les différentes interprétations physiques des deux surfaces identiques topologiquement mais différentes dynamiquement ? Ne pas confondre le bord du tétraèdre avec une worldsheet physique.

## Utilisation
`python3 controle_c226.py`; vérifier `RESULTATS_C226.json`, `MANIFEST_SHA256.txt` et `RAPPORT_C226.md`. Aucun fichier du dépôt original n'est modifié.
