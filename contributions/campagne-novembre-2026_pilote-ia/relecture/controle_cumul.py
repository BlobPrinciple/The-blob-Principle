#!/usr/bin/env python3
"""RELECTURE INTEGRALE, 28 novembre 2026. Controle : les masters sont-ils cumulatifs ?
Pour chaque master du depot, les lignes de texte (25 caracteres au moins, espaces normalises) absentes mot pour mot de V346.
Usage : python3 controle_cumul.py <dossier des textes extraits par pdftotext>            Claude, pilote IA."""
import re, sys, collections, json
d = sys.argv[1]
def lignes(f):
    return [re.sub(r'\s+', ' ', l.replace('\x0c', ' ')).strip() for l in open(f'{d}/{f}', encoding='utf-8', errors='replace')]
def utiles(L): return [l for l in L if len(l) >= 25]
V346 = utiles(lignes('BLOB_PRINCIPLE_MASTER_V346_complet.txt')); S = set(V346)
out = dict(V346=dict(lignes_de_texte=len(V346), distinctes=len(S), repetees_a_l_identique=sum(n - 1 for n in collections.Counter(V346).values() if n > 1)))
for k in ('311', '315', '316', '319'):
    U = utiles(lignes(f'master_V{k}_complet.txt')); absent = [l for l in U if l not in S]
    out['V' + k] = dict(lignes_de_texte=len(U), absentes_mot_pour_mot_de_V346=len(absent), mots_absents=sum(len(a.split()) for a in absent))
S319 = set(utiles(lignes('master_V319_complet.txt'))); plus = [l for l in V346 if l not in S319]
out['V346_au_dela_de_V319'] = dict(lignes=len(plus), mots=sum(len(a.split()) for a in plus))
print(json.dumps(out, ensure_ascii=False, indent=1))
