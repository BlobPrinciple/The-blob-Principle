#!/bin/sh
# X-30 (seconde partie), complements non scelles : cas d'egalite de T16, T17 sans hypothese de signe, arithmetique de T18.
# Rejoue tous les controles. Les outils de Lean 4.35.0 (lean, leanchecker, leanexport, nanoda_bin, con-ron, con-leche)
# doivent etre dans le PATH. Usage : sh controle_complements.sh > controle_complements.out 2>&1     Claude, 27 novembre 2026.
set -u
cd "$(dirname "$0")" || exit 1
export LEAN_PATH="$PWD"
B=TroisQuartsEtCone
F=Complements
T="X30bis.trois_quarts_egalite X30bis.cone_paire_complet X30bis.cone_triplet_complet X30bis.norme_pas_2 X30bis.norme_pas_5 X30bis.det_div3 X30bis.det_div4"
echo "== outils"; lean --version; nanoda_bin --help 2>/dev/null | head -1
echo "== empreintes"; sha256sum $B.lean $F.lean
echo "== 1. Lean compile les enonces et les preuves"
lean -o $B.olean $B.lean > /dev/null; echo "lean $B : code $?"
lean -o $F.olean $F.lean; echo "lean $F : code $?"
echo "== 2. mots interdits (attendu : 0 partout)"
for m in sorry native_decide axiom unsafe implemented_by extern opaque; do echo "$m : $(grep -cw "$m" $F.lean)"; done
echo "== 3. rejeu par les verificateurs de Lean"
leanchecker $F; echo "leanchecker : code $?"
leanchecker-paranoid $F; echo "leanchecker-paranoid : code $?"
echo "== 4. export des sept theoremes et de tout ce dont ils dependent, puis noyaux independants"
leanexport $F -- $T > c.ndjson; echo "leanexport : code $? ; $(wc -l < c.ndjson) lignes ; sha256 $(sha256sum c.ndjson | cut -c1-64)"
cat > nanoda.json <<'JSON'
{ "export_file_path": "c.ndjson", "use_stdin": false, "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true, "nat_extension": true, "string_extension": true,
  "pp_declars": ["X30bis.trois_quarts_egalite", "X30bis.cone_paire_complet", "X30bis.cone_triplet_complet", "X30bis.norme_pas_2", "X30bis.norme_pas_5", "X30bis.det_div3", "X30bis.det_div4"], "pp_to_stdout": true, "print_success_message": true }
JSON
nanoda_bin nanoda.json; echo "nanoda : code $?"
con-ron --jobs=2 c.ndjson; echo "con-ron : code $?"
con-leche --jobs=2 c.ndjson; echo "con-leche : code $?"
echo "== 5. enonces modifies : le script de preuve ne doit plus passer (code 1) ; l'enonce intact doit passer (code 0)"
rm -rf mut; mkdir mut
essai() { nom=$1; expr=$2; cp $F.lean mut/$nom.lean; sed -i "$expr" mut/$nom.lean; lean mut/$nom.lean > mut/$nom.out 2>&1; c=$?
  echo "$nom : code $c ; $(grep -c 'error' mut/$nom.out) erreurs ; fichier modifie : $(cmp -s $F.lean mut/$nom.lean && echo non || echo oui)"; }
essai N0_intact 's/zzz/zzz/'
essai N1_T16_egalite_xp_vaut_2 's/    xp = 1 ∧ xc = 1 ∧ ((x1 = 1 ∧ x2 = 1 ∧ x3 = -1)/    xp = 2 ∧ xc = 1 ∧ ((x1 = 1 ∧ x2 = 1 ∧ x3 = -1)/'
essai N2_T16_egalite_un_seul_cas 's/ ∨ (x1 = 1 ∧ x2 = -1 ∧ x3 = 1) ∨ (x1 = -1 ∧ x2 = 1 ∧ x3 = 1)) := by/) := by/'
essai N3_T17_produit_nul_permis 's/    (h : 0 < nu4 q1 q2 q3 q4 b1 b2 b3 b4) : 0 < b1+b2+b3+b4 := by/    (h : 0 ≤ nu4 q1 q2 q3 q4 b1 b2 b3 b4) : 0 < b1+b2+b3+b4 := by/'
essai N4_T18_norme_jamais_1_modulo_3 's/theorem norme_mod3 (z0 z1 : Int) : eN z0 z1 % 3 ≠ 2 := by/theorem norme_mod3 (z0 z1 : Int) : eN z0 z1 % 3 ≠ 1 := by/'
essai N5_T18_divisible_par_9 's/    eN (det0 a0 a1 b0 b1 c0 c1 d0 d1) (det1 a0 a1 b0 b1 c0 c1 d0 d1) % 3 = 0 := by/    eN (det0 a0 a1 b0 b1 c0 c1 d0 d1) (det1 a0 a1 b0 b1 c0 c1 d0 d1) % 9 = 0 := by/'
essai N6_T18_divisible_par_8 's/    eN (det0 a0 a1 b0 b1 c0 c1 d0 d1) (det1 a0 a1 b0 b1 c0 c1 d0 d1) % 4 = 0 := by/    eN (det0 a0 a1 b0 b1 c0 c1 d0 d1) (det1 a0 a1 b0 b1 c0 c1 d0 d1) % 8 = 0 := by/'
essai N7_T18_une_seule_norme_divisible_par_3 's/(hb : eN b0 b1 % 3 = 0) (hd : eN d0 d1 % 3 = 0) :/(hb : eN b0 b1 % 3 = 0) (hd : eN d0 d1 % 1 = 0) :/'
rm -rf mut c.ndjson nanoda.json $B.olean $F.olean
