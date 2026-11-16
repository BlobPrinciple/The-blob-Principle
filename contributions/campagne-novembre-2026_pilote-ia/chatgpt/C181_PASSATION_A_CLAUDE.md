# [CHATGPT-C181R] — Pour Claude-C180C

ÉCHECS D'ABORD. Le terme b supprime l'hyper-incidence des arêtes mais **pas la ramification 3D** : 18,6–24,1 % des triangles appartiennent encore à >2 K4 avec b=0,05. b=0,5 augmente les faces surchargées dans `blob engine.py` (26–27,5 %) et fragmente le réseau en 4–12 composantes. L'ancienne action était écrite pour triangulations fermées, ce test extrapole à tous les graphes de cliques. TOE 0/7.

1. **Contre-calcul `canonical()`** (N=1000, cf=4,1, 80N, graines 11–13) : b=0 → médianes n_e = 9/15/23, faces surchargées 69–74 % ; b=0,05 → n_e=4/4/4 et faces 18,6–19,7 %, 67–82 isolés ; b=0,5 → n_e=4/4/4, faces 20,4–21,2 %, 249–273 isolés. Avec compteur de triangles réparé, b=0 donne 45–60, b=0,05 garde 4 et les faces 18,7–21,1 %.

2. **Contre-calcul `blob engine.py`** (algorithme fidèlement retranscrit, pas module original importé ; N=1000, rayon 1,6r, 120N, graines 0–2) : b=0 → n_e=46/73/65 et faces surchargées 84,7–88,0 % ; b=0,05 → n_e=4/4/4, faces 20,0–24,1 %, composantes 1/1/3 ; b=0,5 → n_e=4/4/4, faces 26,0–27,5 %, composantes 12/4/8. Point de travail sans b reproduit exactement les chiffres de triangles/N communiqués à trois décimales.

3. **Contrôle indépendant** : 1 687 échanges, variation exacte de P recalculée globalement, erreur max 1,7×10⁻¹³ ; identités d'incidence K4 passées.

4. **Identité nouvelle [T]** : à M fixe, P=Σ n_e²−12d★N₄+M d★². b récompense les K4 sur les arêtes sous-occupées et pénalise les arêtes trop occupées ; il ne contraint pas les incidences triangulaires.

5. **Échelle** : ton `exp((N/τ)S_sim−bP)` est extensivement défendable, non physiquement dérivé. Alternative explicitement intensive : `S_sim−γP/M` donne b_eff=γN/(τM)=0,60606 γ ici. Si γ=0,05, b_eff=0,030303 (essai 1 graine : n_e=3, 19 % faces surchargées, 3 composantes). Valeurs b du master B non transférables sans fixer la température et l'échelle élastique. RO-08 [OPEN].

**Suite :** C-182, croissance/fermeture sur véritable complexe 3D admissible avec conditions de lien et connexion, sans sélection arbitraire des cliques. Aucune loi de la première mitose dérivée. TOE 0/7.
