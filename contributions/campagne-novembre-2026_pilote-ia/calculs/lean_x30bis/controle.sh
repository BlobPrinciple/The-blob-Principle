#!/bin/sh
# X-30 (seconde partie), T16 (les trois quarts) et T17 (le cone) au noyau de Lean : rejoue tous les controles. Les outils de Lean 4.35.0
# (lean, leanchecker, leanexport, nanoda_bin, con-ron, con-leche, lean4lean) doivent etre dans le PATH.
# Usage : sh controle.sh > controle.out 2>&1     Claude, 27 novembre 2026.
set -u
cd "$(dirname "$0")" || exit 1
export LEAN_PATH="$PWD"
F=TroisQuartsEtCone
echo "== outils"; lean --version; nanoda_bin --help 2>/dev/null | head -1
echo "== empreinte"; sha256sum $F.lean
echo "== 1. Lean compile les enonces et les preuves"
lean -o $F.olean $F.lean; echo "lean $F : code $?"
echo "== 2. mots interdits (attendu : 0 partout)"
for m in sorry native_decide axiom unsafe implemented_by extern opaque; do echo "$m : $(grep -cw "$m" $F.lean)"; done
echo "== 3. rejeu par les verificateurs de Lean"
leanchecker $F; echo "leanchecker : code $?"
leanchecker-paranoid $F; echo "leanchecker-paranoid : code $?"
echo "== 4. export des trois theoremes et de tout ce dont ils dependent, puis noyaux independants"
leanexport $F -- X30bis.trois_quarts X30bis.cone_paire X30bis.cone_triplet > g1.ndjson; echo "leanexport : code $? ; $(wc -l < g1.ndjson) lignes ; sha256 $(sha256sum g1.ndjson | cut -c1-64)"
cat > nanoda.json <<'FIN'
{ "export_file_path": "g1.ndjson", "use_stdin": false, "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true, "nat_extension": true, "string_extension": true,
  "pp_declars": ["X30bis.trois_quarts", "X30bis.cone_paire", "X30bis.cone_triplet"], "pp_to_stdout": true, "print_success_message": true }
FIN
nanoda_bin nanoda.json; echo "nanoda : code $?"
con-ron --jobs=2 g1.ndjson; echo "con-ron : code $?"
con-leche --jobs=2 g1.ndjson; echo "con-leche : code $?"
echo "== 5. enonces modifies : le script de preuve ne doit plus passer (code 1) ; l'enonce intact doit passer (code 0)"
rm -rf mut; mkdir mut
essai() { nom=$1; expr=$2; cp $F.lean mut/$nom.lean; sed -i "$expr" mut/$nom.lean; lean mut/$nom.lean > mut/$nom.out 2>&1; c=$?
  echo "$nom : code $c ; $(grep -c 'error' mut/$nom.out) erreurs ; fichier modifie : $(cmp -s $F.lean mut/$nom.lean && echo non || echo oui)"; }
essai M0_intact 's/zzz/zzz/'
essai M1_T16_conclusion_plus_un 's/      ≤ 1 + 3 \* (2 \* wc - (wp+wc+w1+w2+w3)) := by/      ≤ 3 * (2 * wc - (wp+wc+w1+w2+w3)) := by/'
essai M2_T16_chevauchement_de_f3_permis 's/(n3 : 2 \* x3 - (xp+xc+x1+x2+x3) ≤ -1)/(n3 : 2 * x3 - (xp+xc+x1+x2+x3) ≤ 0)/'
essai M3_T16_somme_nulle_permise 's/(g3 : 0 ≤ w3) (gp : 0 < w1+w2+w3) :/(g3 : 0 ≤ w3) (gp : 0 ≤ w1+w2+w3) :/'
essai M4_T16_hors_du_secteur 's/(g1 : 0 ≤ w1) (g2 : 0 ≤ w2) (g3 : 0 ≤ w3) (gp : 0 < w1+w2+w3) :/(g1 : 0 ≤ w1) (g2 : 0 ≤ w2) (g3 : -1 ≤ w3) (gp : 0 < w1+w2+w3) :/'
essai M5_T16_rondeur_de_x_affaiblie 's/(xp+xc+x1+x2+x3) \* (xp+xc+x1+x2+x3) = 1)/(xp+xc+x1+x2+x3) * (xp+xc+x1+x2+x3) ≤ 1)/'
essai M6_T17_paire_15_au_lieu_de_16 's/    3 \* nu4 q1 q2 q3 q4 r1 r2 r3 r4 < 16 := by/    3 * nu4 q1 q2 q3 q4 r1 r2 r3 r4 < 15 := by/'
essai M7_T17_triplet_11_au_lieu_de_12 's/s1 s2 s3 s4 < 12 := by/s1 s2 s3 s4 < 11 := by/'
essai M8_T17_w_pas_de_genre_lumiere 's/    (hs : nu4 s1 s2 s3 s4 s1 s2 s3 s4 = 0) (hw : nu4 w1 w2 w3 w4 w1 w2 w3 w4 = 0)/    (hs : nu4 s1 s2 s3 s4 s1 s2 s3 s4 = 0) (hw : nu4 w1 w2 w3 w4 w1 w2 w3 w4 = 1)/'
essai M9_T17_trois_quarts_remplace_par_deux_tiers 's/    (iq : 3 \* nu4 q1 q2 q3 q4 w1 w2 w3 w4 < 4 \* nu4 x1 x2 x3 x4 w1 w2 w3 w4)$/    (iq : 2 * nu4 q1 q2 q3 q4 w1 w2 w3 w4 < 3 * nu4 x1 x2 x3 x4 w1 w2 w3 w4)/'
rm -rf mut g1.ndjson nanoda.json $F.olean
