#!/usr/bin/env python3
"""Phrases d'un texte absentes de la référence, comparaison sur les seuls caractères alphanumériques
(insensible à la mise en lignes, aux espaces et à la ponctuation). Une phrase est dite absente si moins de
la moitié de ses fenêtres de 40 caractères se retrouve dans la référence.
Usage : phrases_absentes.py <ref> <texte> <nombre d'exemples>"""
import re, sys
L = 40
def norm(s): return re.sub(r'[^0-9a-zà-ÿ]', '', s.lower())
ref = norm(open(sys.argv[1], encoding='utf-8', errors='replace').read())
S = {hash(ref[i:i + L]) for i in range(len(ref) - L + 1)}
brut = open(sys.argv[2], encoding='utf-8', errors='replace').read().replace('\x0c', ' ')
brut = re.sub(r'-\n\s*', '', brut)
phrases = re.split(r'(?<=[.!?:;])\s+', re.sub(r'\s+', ' ', brut))
tot = abs_ = mots_tot = mots_abs = 0; ex = []
for p in phrases:
    n = norm(p)
    if len(n) < 60: continue
    tot += 1; m = len(p.split()); mots_tot += m
    fen = [n[i:i + L] for i in range(0, len(n) - L + 1, 10)]
    pres = sum(hash(f) in S for f in fen) / len(fen)
    if pres < 0.5:
        abs_ += 1; mots_abs += m
        lettres = sum(c.isalpha() for c in p) / max(len(p), 1)
        if lettres > 0.78 and '$' not in p and '\\' not in p: ex.append(p)
print(f"{sys.argv[2].split('/')[-1]} : {tot} phrases de 60 caractères ou plus ({mots_tot} mots) ; absentes : {abs_} ({mots_abs} mots) ; dont en prose courante : {len(ex)} ({sum(len(e.split()) for e in ex)} mots)")
for e in ex[:int(sys.argv[3])]: print('   ·', e[:300])
