#!/usr/bin/env python3
"""Extrait en texte tous les PDF et DOCX du dépôt, et compte les mots par dossier et par type. Usage : extraire_tout.py <dépôt> <sortie>"""
import os, re, sys, subprocess, zipfile, hashlib, collections, json
depot, sortie = sys.argv[1], sys.argv[2]
tab = []; vus = {}
for racine, dirs, fichiers in os.walk(depot):
    if '.git' in racine.split(os.sep): continue
    for f in sorted(fichiers):
        p = os.path.join(racine, f); ext = f.rsplit('.', 1)[-1].lower() if '.' in f else ''
        rel = os.path.relpath(p, depot)
        if ext not in ('pdf', 'docx', 'md', 'txt', 'py', 'html', 'ipynb', 'cff', 'out', 'json', 'csv'): continue
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        double = vus.get(h); vus.setdefault(h, rel)
        cible = os.path.join(sortie, re.sub(r'[^A-Za-z0-9._-]+', '_', rel) + '.txt')
        try:
            if ext == 'pdf':
                if not os.path.exists(cible): subprocess.run(['pdftotext', p, cible], check=False, stderr=subprocess.DEVNULL)
                t = open(cible, encoding='utf-8', errors='replace').read() if os.path.exists(cible) else ''
            elif ext == 'docx':
                x = zipfile.ZipFile(p).read('word/document.xml').decode('utf-8', 'replace')
                x = re.sub(r'</w:p>', '\n', x); t = re.sub(r'<[^>]+>', '', x)
                open(cible, 'w').write(t)
            else:
                t = open(p, encoding='utf-8', errors='replace').read()
        except Exception as e:
            t = ''
        tab.append(dict(rel=rel, ext=ext, mots=len(t.split()), double_de=double, cible=cible if ext in ('pdf', 'docx') else p))
json.dump(tab, open(os.path.join(sortie, '_inventaire.json'), 'w'), ensure_ascii=False, indent=0)
agg = collections.defaultdict(lambda: collections.Counter())
for r in tab:
    if r['double_de']: continue
    parts = r['rel'].split(os.sep); d = os.sep.join(parts[:2]) if len(parts) > 2 else (parts[0] if len(parts) > 1 else '(racine)')
    agg[d][r['ext']] += r['mots']
print(f"{'dossier':<58} {'pdf':>9} {'docx':>8} {'md':>8} {'txt':>8} {'py':>8} {'html+ipynb':>10} | {'json/out/csv':>12}")
T = collections.Counter()
for d in sorted(agg):
    c = agg[d]; T.update(c)
    print(f"{d:<58} {c['pdf']:>9} {c['docx']:>8} {c['md']:>8} {c['txt']:>8} {c['py']:>8} {c['html']+c['ipynb']+c['cff']:>10} | {c['json']+c['out']+c['csv']:>12}")
print(f"{'TOTAL (hors doublons exacts)':<58} {T['pdf']:>9} {T['docx']:>8} {T['md']:>8} {T['txt']:>8} {T['py']:>8} {T['html']+T['ipynb']+T['cff']:>10} | {T['json']+T['out']+T['csv']:>12}")
print('doublons exacts :', sum(1 for r in tab if r['double_de']), 'fichiers')
