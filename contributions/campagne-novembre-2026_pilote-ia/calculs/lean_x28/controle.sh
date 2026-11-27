#!/bin/sh
# X-28, le lemme du pont (T2) au noyau de Lean : rejoue tous les controles. Les outils de Lean 4.35.0 (lean, leanchecker, leanexport, nanoda_bin, con-ron,
# con-leche) doivent etre dans le PATH. Usage : sh controle.sh > controle.out 2>&1     Claude, 27 novembre 2026.
set -u
cd "$(dirname "$0")" || exit 1
export LEAN_PATH="$PWD"
echo "== outils"; lean --version; nanoda_bin --help 2>/dev/null | head -1
echo "== empreinte"; sha256sum Pont.lean
echo "== 1. Lean compile l'enonce et la preuve"
lean -o Pont.olean Pont.lean; echo "lean Pont : code $?"
echo "== 2. mots interdits (attendu : 0 partout)"
for m in sorry native_decide axiom unsafe implemented_by extern opaque; do echo "$m : $(grep -cw "$m" Pont.lean)"; done
echo "== 3. rejeu par les verificateurs de Lean"
leanchecker Pont; echo "leanchecker : code $?"
leanchecker-paranoid Pont; echo "leanchecker-paranoid : code $?"
echo "== 4. export du theoreme et de tout ce dont il depend, puis trois noyaux independants"
leanexport Pont -- X28.pont > pont.ndjson; echo "leanexport : code $? ; $(wc -l < pont.ndjson) lignes ; sha256 $(sha256sum pont.ndjson | cut -c1-64)"
cat > nanoda.json <<'FIN'
{ "export_file_path": "pont.ndjson", "use_stdin": false, "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true, "nat_extension": true, "string_extension": true,
  "pp_declars": ["X28.pont"], "pp_to_stdout": true, "print_success_message": true }
FIN
nanoda_bin nanoda.json; echo "nanoda : code $?"
con-ron --jobs=2 pont.ndjson; echo "con-ron : code $?"
con-leche --jobs=2 pont.ndjson; echo "con-leche : code $?"
echo "== 5. quatre enonces modifies : le script de preuve ne doit plus passer (code 1) ; l'enonce intact doit passer (code 0)"
rm -rf mut; mkdir mut
essai() { nom=$1; expr=$2; cp Pont.lean mut/$nom.lean; sed -i "$expr" mut/$nom.lean; lean mut/$nom.lean > mut/$nom.out 2>&1; c=$?
  echo "$nom : code $c ; $(grep -c 'error' mut/$nom.out) erreurs ; fichier modifie : $(cmp -s Pont.lean mut/$nom.lean && echo non || echo oui)"; }
essai M0_intact 's/zzz/zzz/'
essai M1_conclusion_moins_un 's/    -2 ≤ prod q r := by/    -1 ≤ prod q r := by/'
essai M2_contact_de_r_affaibli 's/(hvq : prod v q = -D) (hvr : prod v r = -D)/(hvq : prod v q = -D) (hvr : prod v r ≤ -D)/'
essai M3_coefficient_negatif_permis 's/(hN : 0 < N) (h0a : 0 ≤ αa) (h0b : 0 ≤ αb)/(hN : 0 < N) (h0a : -1 ≤ αa) (h0b : 0 ≤ αb)/'
essai M4_chevauchement_de_a_permis 's/(hva : prod v a ≤ -D) (hvb : prod v b ≤ -D)/(hva : prod v a ≤ 0) (hvb : prod v b ≤ -D)/'
rm -rf mut pont.ndjson nanoda.json Pont.olean
