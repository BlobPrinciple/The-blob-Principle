#!/bin/bash
# X-25, scan des masters, etape 0 : extraction du texte de tous les PDF et DOCX du depot (corpus, livres, docs), un fichier texte par source dans ./txt,
# pages separees par le saut de page de pdftotext. A lancer depuis un dossier de travail HORS du depot : ./x25_scan_0_extraction.sh <racine du depot>
# Les identifiants S001, S002, ... suivent l'ordre alphabetique des chemins ; les etapes 1 a 3 (x25_scan_1_blocs.py, _2_phrases.py, _3_verrous.py),
# copiees dans le meme dossier de travail, s'y referent. Claude, 23 novembre 2026.
R="$1"; OUT=./txt; mkdir -p "$OUT"; : > table.tsv; i=0
find "$R/corpus" "$R/livres" "$R/docs" -type f \( -iname '*.pdf' -o -iname '*.docx' \) | LC_ALL=C sort | while IFS= read -r f; do
  i=$((i+1)); id=$(printf "S%03d" $i); rel="${f#$R/}"
  if [[ "${f,,}" == *.pdf ]]; then
    pdftotext -layout "$f" "$OUT/$id.txt" 2>/dev/null; p=$(pdfinfo "$f" 2>/dev/null | awk '/^Pages:/{print $2}')
  else
    python3 - "$f" "$OUT/$id.txt" <<'PY'
import sys, zipfile, re, html
x = zipfile.ZipFile(sys.argv[1]).read('word/document.xml').decode('utf-8', 'replace')
x = re.sub(r'</w:p>', '\n', x); x = re.sub(r'<w:tab/>', '\t', x); x = re.sub(r'<[^>]+>', '', x)
open(sys.argv[2], 'w').write(html.unescape(x))
PY
    p=docx
  fi
  printf "%s\t%s\t%s\t%s\t%s\n" "$id" "$p" "$(wc -c < "$OUT/$id.txt")" "$(sha256sum "$f" | cut -c1-16)" "$rel" >> table.tsv
done
