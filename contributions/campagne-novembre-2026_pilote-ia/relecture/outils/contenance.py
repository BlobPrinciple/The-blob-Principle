#!/usr/bin/env python3
"""Quelle part d'un texte se retrouve dans V346 ? Comparaison par suites de 8 mots (insensible à la mise en lignes).
Usage : contenance.py <reference.txt> <texte.txt> [...]"""
import re, sys
K = 8
def mots(f):
    t = open(f, encoding='utf-8', errors='replace').read().replace('\x0c', ' ')
    t = re.sub(r'-\n\s*', '', t)
    return re.findall(r'\S+', t.lower())
ref = mots(sys.argv[1])
S = {hash(tuple(ref[i:i + K])) for i in range(len(ref) - K + 1)}
print(f"référence : {len(ref)} mots")
for f in sys.argv[2:]:
    w = mots(f); n = len(w) - K + 1
    vu = [hash(tuple(w[i:i + K])) in S for i in range(n)]
    couvert = [False] * len(w)
    for i, v in enumerate(vu):
        if v:
            for j in range(i, i + K): couvert[j] = True
    hors = sum(1 for c in couvert if not c)
    # plages hors référence d'au moins 40 mots
    plages = []; i = 0
    while i < len(w):
        if not couvert[i]:
            j = i
            while j < len(w) and not couvert[j]: j += 1
            if j - i >= 40: plages.append((i, j))
            i = j
        else: i += 1
    gros = sum(b - a for a, b in plages)
    print(f"{f.split('/')[-1]:<32} {len(w):>8} mots ; hors référence : {hors:>7} mots ({100*hors/len(w):5.1f} %) ; en plages de 40 mots ou plus : {gros:>7} mots, {len(plages)} plages")
