#!/usr/bin/env python3
"""Liste les plages d'un texte absentes de la référence (suites de 8 mots). Usage : plages.py <ref> <texte> <mots mini> <nb max> [long]"""
import re, sys
K = 8
def mots(f):
    t = open(f, encoding='utf-8', errors='replace').read().replace('\x0c', ' ')
    t = re.sub(r'-\n\s*', '', t)
    return re.findall(r'\S+', t)
ref = [m.lower() for m in mots(sys.argv[1])]
S = {hash(tuple(ref[i:i + K])) for i in range(len(ref) - K + 1)}
W = mots(sys.argv[2]); w = [m.lower() for m in W]
mini, nmax = int(sys.argv[3]), int(sys.argv[4]); long = len(sys.argv) > 5
couvert = [False] * len(w)
for i in range(len(w) - K + 1):
    if hash(tuple(w[i:i + K])) in S:
        for j in range(i, i + K): couvert[j] = True
i = 0; n = 0
while i < len(w):
    if not couvert[i]:
        j = i
        while j < len(w) and not couvert[j]: j += 1
        if j - i >= mini and n < nmax:
            n += 1
            ext = ' '.join(W[i:j]) if long else ' '.join(W[i:i + 26])
            print(f"[{i}:{j}] {j - i} mots | {ext}")
        i = j
    else: i += 1
