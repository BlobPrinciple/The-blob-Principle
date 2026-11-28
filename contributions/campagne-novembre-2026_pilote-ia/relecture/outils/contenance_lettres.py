#!/usr/bin/env python3
"""Pour chaque texte : part des phrases absentes de la référence V346, comparaison sur les seules LETTRES
(ligatures développées ; chiffres, espaces, ponctuation et numéros de page ignorés).
Phrase absente : moins de la moitié de ses fenêtres de 36 lettres se retrouve dans la référence.
Usage : contenance_lettres.py <ref> <inventaire.json> <filtre de chemin> [--exemples N]"""
import re, sys, json
L = 36
LIG = {'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl', 'œ': 'oe', 'æ': 'ae', '’': "'"}
def norm(s):
    s = s.lower()
    for a, b in LIG.items(): s = s.replace(a, b)
    return re.sub(r'[^a-zà-ÿ]', '', s)
def lire(f): return re.sub(r'-\n\s*', '', open(f, encoding='utf-8', errors='replace').read().replace('\x0c', ' '))
ref = norm(lire(sys.argv[1]))
S = {hash(ref[i:i + L]) for i in range(len(ref) - L + 1)}
inv = json.load(open(sys.argv[2])); filtre = sys.argv[3]
nex = int(sys.argv[5]) if len(sys.argv) > 5 else 0
for r in inv:
    if filtre not in r['rel'] or r['ext'] not in ('pdf', 'docx', 'md') or r['double_de'] or r['mots'] < 300: continue
    brut = lire(r['cible'])
    phrases = re.split(r'(?<=[.!?:;])\s+', re.sub(r'\s+', ' ', brut))
    mt = ma = 0; ex = []
    for p in phrases:
        n = norm(p)
        if len(n) < 50: continue
        m = len(p.split()); mt += m
        fen = [n[i:i + L] for i in range(0, len(n) - L + 1, 9)]
        if sum(hash(f) in S for f in fen) / len(fen) < 0.5:
            ma += m
            if sum(c.isalpha() for c in p) / len(p) > 0.76 and '$' not in p and '\\' not in p: ex.append(p)
    pm = sum(len(e.split()) for e in ex)
    print(f"{r['mots']:>8} mots | absents de V346 : {100*ma/max(mt,1):5.1f} % des phrases ({ma:>7} mots, dont prose {pm:>7}) | {r['rel'][-92:]}")
    for e in ex[:nex]: print('      ·', e[:260])
