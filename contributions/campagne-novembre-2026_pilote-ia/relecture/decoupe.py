#!/usr/bin/env python3
"""Decoupe un texte extrait par pdftotext en tranches de lecture qui suivent les pages, sans retirer un mot.
Usage : decoupe.py <texte> <dossier de sortie> <prefixe> <premiere page> <caracteres par tranche>"""
import re, sys, textwrap, collections, os
txt, sortie, prefixe, premiere, CIBLE = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
os.makedirs(sortie, exist_ok=True)
pages = open(txt, encoding='utf-8', errors='replace').read().split('\x0c')
if pages and not pages[-1].strip(): pages = pages[:-1]
def reflow(page):
    out = []
    for b in re.split(r'\n\s*\n', page):
        L = [l.strip() for l in b.split('\n') if l.strip()]
        if not L: continue
        cur = L[0]
        for prev, l in zip(L, L[1:]):
            if len(prev) >= 62: cur += ' ' + l
            else: out.append(cur); cur = l
        out.append(cur)
    res = []; court = []
    def vide():
        if court: res.extend(textwrap.wrap(' · '.join(court), 900, break_long_words=False, break_on_hyphens=False)); court.clear()
    for p in out:
        if len(p) <= 34: court.append(p)
        else: vide(); res.extend(textwrap.wrap(p, 900, break_long_words=False, break_on_hyphens=False))
    vide(); return res
chunks = []; cur = []; car = 0; debut = premiere
for i, pg in enumerate(pages, 1):
    if i < premiere: continue
    L = reflow(pg); c = sum(len(l) + 1 for l in L)
    if car and car + c > CIBLE: chunks.append((debut, i - 1, cur)); cur = []; car = 0; debut = i
    cur.append(f'=== p. {i} ==='); cur.extend(L); car += c
chunks.append((debut, len(pages), cur))
for k, (a, b, L) in enumerate(chunks, 1):
    open(f'{sortie}/{prefixe}{k:02d}_p{a:04d}-{b:04d}.txt', 'w').write('\n'.join(L) + '\n')
def mots(t): return collections.Counter(re.findall(r'\S+', t.replace('·', ' ')))
orig = mots(' '.join(pages[premiere - 1:])); nouv = collections.Counter()
for _, _, L in chunks: nouv += mots(' '.join(l for l in L if not l.startswith('=== p. ')))
print(f'{len(pages)} pages ; {len(chunks)} tranches ; mots absents des tranches : {sum((orig - nouv).values())}')
