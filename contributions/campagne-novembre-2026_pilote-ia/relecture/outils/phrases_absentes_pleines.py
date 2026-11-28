#!/usr/bin/env python3
"""Phrases de <texte> absentes de l'union des références, en entier, avec leur rang dans le texte.
Comparaison sur les caractères alphanumériques, fenêtres de 40 caractères, seuil : la moitié des fenêtres.
Les phrases voisines absentes sont regroupées en blocs ; chaque bloc est précédé de la dernière phrase présente (contexte).
Usage : phrases_absentes_pleines.py <texte> <ref> [<ref> ...]"""
import re, sys
L = 40
def norm(s): return re.sub(r'[^0-9a-zà-ÿ]', '', s.lower())
def lire(path):
    brut = open(path, encoding='utf-8', errors='replace').read().replace('\x0c', ' ')
    brut = brut.replace('ﬁ','fi').replace('ﬂ','fl').replace('ﬀ','ff').replace('ﬃ','ffi').replace('ﬄ','ffl')
    return re.sub(r'-\n\s*', '', brut)
texte, refs = sys.argv[1], sys.argv[2:]
S = set(); REFS = []
for r in refs:
    n = norm(lire(r)); REFS.append(n)
    S.update(hash(n[i:i + L]) for i in range(len(n) - L + 1))
phrases = re.split(r'(?<=[.!?:;])\s+', re.sub(r'\s+', ' ', lire(texte)))
etat = []
for p in phrases:
    n = norm(p)
    if len(n) < 12: etat.append(None); continue
    if len(n) < L: etat.append(any(n in r for r in REFS)); continue
    fen = [n[i:i + L] for i in range(0, len(n) - L + 1, 10)]
    etat.append(sum(hash(f) in S for f in fen) / len(fen) >= 0.5)
mots = 0; blocs = 0; i = 0
while i < len(phrases):
    if etat[i] is False:
        j = i
        while j < len(phrases) and etat[j] is not True: j += 1
        while j > i and etat[j - 1] is None: j -= 1
        k = i - 1
        while k >= 0 and etat[k] is None: k -= 1
        blocs += 1
        bloc = ' '.join(phrases[i:j]); mots += len(bloc.split())
        print(f"\n=== bloc {blocs} (phrases {i}–{j-1}) — après : « {phrases[k][-160:] if k >= 0 else ''} »")
        print(bloc)
        i = j
    else: i += 1
print(f"\n##### {blocs} blocs, {mots} mots absents")
