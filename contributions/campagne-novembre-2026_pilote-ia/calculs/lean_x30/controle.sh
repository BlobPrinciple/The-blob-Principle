#!/bin/sh
# X-30, le lemme de la fenetre (T13) au noyau de Lean : rejoue tous les controles. Les outils de Lean 4.35.0 (lean, leanchecker, leanexport, nanoda_bin,
# con-ron, con-leche) doivent etre dans le PATH. Usage : sh controle.sh > controle.out 2>&1     Claude, 27 novembre 2026.
set -u
cd "$(dirname "$0")" || exit 1
export LEAN_PATH="$PWD"
echo "== outils"; lean --version; nanoda_bin --help 2>/dev/null | head -1
echo "== empreinte"; sha256sum Fenetre.lean
echo "== 1. Lean compile l'enonce et la preuve"
lean -o Fenetre.olean Fenetre.lean; echo "lean Fenetre : code $?"
echo "== 2. mots interdits (attendu : 0 partout)"
for m in sorry native_decide axiom unsafe implemented_by extern opaque; do echo "$m : $(grep -cw "$m" Fenetre.lean)"; done
echo "== 3. rejeu par les verificateurs de Lean"
leanchecker Fenetre; echo "leanchecker : code $?"
leanchecker-paranoid Fenetre; echo "leanchecker-paranoid : code $?"
echo "== 4. export du theoreme et de tout ce dont il depend, puis trois noyaux independants"
leanexport Fenetre -- X30.fenetre > fenetre.ndjson; echo "leanexport : code $? ; $(wc -l < fenetre.ndjson) lignes ; sha256 $(sha256sum fenetre.ndjson | cut -c1-64)"
cat > nanoda.json <<'FIN'
{ "export_file_path": "fenetre.ndjson", "use_stdin": false, "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true, "nat_extension": true, "string_extension": true,
  "pp_declars": ["X30.fenetre"], "pp_to_stdout": true, "print_success_message": true }
FIN
nanoda_bin nanoda.json; echo "nanoda : code $?"
con-ron --jobs=2 fenetre.ndjson; echo "con-ron : code $?"
con-leche --jobs=2 fenetre.ndjson; echo "con-leche : code $?"
echo "== 5. quatre enonces modifies : le script de preuve ne doit plus passer (code 1) ; l'enonce intact doit passer (code 0)"
rm -rf mut; mkdir mut
essai() { nom=$1; expr=$2; cp Fenetre.lean mut/$nom.lean; sed -i "$expr" mut/$nom.lean; lean mut/$nom.lean > mut/$nom.out 2>&1; c=$?
  echo "$nom : code $c ; $(grep -c 'error' mut/$nom.out) erreurs ; fichier modifie : $(cmp -s Fenetre.lean mut/$nom.lean && echo non || echo oui)"; }
essai M0_intact 's/zzz/zzz/'
essai M1_conclusion_plus_un 's/    2 \* D ≤ a1+a2+a3+a4 := by/    2 * D + 1 ≤ a1+a2+a3+a4 := by/'
essai M2_chevauchement_de_f4_permis 's/(h4 : a4 ≤ a1+a2+a3+a4-D)/(h4 : a4 ≤ a1+a2+a3+a4)/'
essai M3_denominateur_nul_permis 's/(hD : 0 < D)/(hD : 0 ≤ D)/'
essai M4_rondeur_affaiblie 's/(hn : a1\*a1 + a2\*a2 + a3\*a3 + a4\*a4 = (a1+a2+a3+a4) \* (a1+a2+a3+a4))/(hn : a1*a1 + a2*a2 + a3*a3 + a4*a4 ≤ (a1+a2+a3+a4) * (a1+a2+a3+a4))/'
rm -rf mut fenetre.ndjson nanoda.json Fenetre.olean
