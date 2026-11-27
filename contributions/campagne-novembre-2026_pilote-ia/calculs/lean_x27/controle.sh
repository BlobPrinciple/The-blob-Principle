#!/bin/sh
# X-27 au noyau de Lean : rejoue tous les controles. Les outils de Lean 4.35.0 (lean, leanchecker, leanexport, nanoda_bin, con-ron, con-leche)
# doivent etre dans le PATH. Usage : sh controle.sh > controle.out 2>&1     Claude, 26 novembre 2026.
set -u
cd "$(dirname "$0")" || exit 1
export LEAN_PATH="$PWD"
echo "== outils"; lean --version; nanoda_bin --help 2>/dev/null | head -1
echo "== empreintes"; sha256sum Enonce.lean genere.py
echo "== 1. la preuve est regeneree, puis Lean compile l'enonce et la preuve"
python3 -I genere.py > Preuve.lean; sha256sum Preuve.lean
lean -o Enonce.olean Enonce.lean; echo "lean Enonce : code $?"
lean -o Preuve.olean Preuve.lean; echo "lean Preuve : code $?"
echo "== 2. mots interdits dans les deux fichiers (attendu : 0 partout)"
for m in sorry native_decide axiom unsafe implemented_by extern opaque; do echo "$m : $(grep -cw "$m" Enonce.lean) dans l'enonce, $(grep -w "$m" Preuve.lean | grep -vc '^/-\|^Fichier\|^le mot')" ; done
echo "== 3. rejeu par les verificateurs de Lean"
leanchecker Enonce Preuve; echo "leanchecker : code $?"
leanchecker-paranoid Enonce Preuve; echo "leanchecker-paranoid : code $?"
leanchecker --fresh Preuve; echo "leanchecker --fresh : code $?"
echo "== 4. export du theoreme et de tout ce dont il depend, puis trois noyaux independants"
leanexport Preuve -- X27.K20_est_fausse > k20.ndjson; echo "leanexport : code $? ; $(wc -l < k20.ndjson) lignes ; sha256 $(sha256sum k20.ndjson | cut -c1-64)"
cat > nanoda.json <<'FIN'
{ "export_file_path": "k20.ndjson", "use_stdin": false, "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true, "nat_extension": true, "string_extension": true,
  "pp_declars": ["X27.K20_est_fausse", "X27.EnonceK20Fausse"], "pp_to_stdout": true, "print_success_message": true }
FIN
nanoda_bin nanoda.json; echo "nanoda : code $?"
con-ron --jobs=2 k20.ndjson; echo "con-ron : code $?"
con-leche --jobs=2 k20.ndjson; echo "con-leche : code $?"
echo "== 5. essais de mutation : quatre versions faussees, Lean doit les refuser toutes (code 1) ; la version intacte doit passer (code 0)"
rm -rf mut; mkdir mut
essai() { nom=$1; fichier=$2; expr=$3; d=mut/$nom; mkdir -p "$d"; cp Enonce.lean Preuve.lean "$d"/
  ( cd "$d" && sed -i "$expr" "$fichier" && lean -o Enonce.olean Enonce.lean > e.out 2>&1; LEAN_PATH="$PWD" lean Preuve.lean > p.out 2>&1; c=$?
    echo "$nom : code $c ; $(grep -c 'error' p.out) erreurs ; fichier modifie : $(cmp -s "$fichier" ../../"$fichier" && echo non || echo oui)" ) }
essai M0_intacte Enonce.lean 's/zzz/zzz/'
essai M1_place_faussee Enonce.lean 's/def place : Boule := ⟨(18, 18, 16, -6, -3), 7⟩/def place : Boule := ⟨(18, 18, 16, -6, -4), 7⟩/'
essai M2_naissance_faussee Enonce.lean 's/(8, 2, 8, 2, -3), (9, 3, 9, 1, -3),$/(8, 2, 8, 2, -2), (9, 3, 9, 1, -3),/'
essai M3_place_de_l_empilement Enonce.lean 's/def place : Boule := ⟨(18, 18, 16, -6, -3), 7⟩/def place : Boule := ⟨(2, 2, 2, -1, 0), 1⟩/'
essai M4_temoin_fausse Preuve.lean '0,/(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (5, 3, 5, -1, -1), (6, 6, 3, -2, 0),$/s//(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (5, 3, 5, -1, -1), (9, 9, 3, -3, 1),/'
rm -rf mut k20.ndjson nanoda.json Enonce.olean Preuve.olean
