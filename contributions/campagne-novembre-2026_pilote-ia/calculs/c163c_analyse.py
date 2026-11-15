#!/usr/bin/env python3
"""C-163c -- comparaison des executions (Claude, 15 novembre 2026). Invariant d'isometrie : liste triee de toutes les distances entre sommets.
Usage : python3 c163c_analyse.py <graine> <suffixe> <modes...>   (ex. 1320 _14 A B C)"""
import json, sys
import numpy as np
g, suf, modes = sys.argv[1], sys.argv[2], sys.argv[3:]
R = {m: json.load(open(f'c163c_{g}_{m}{suf}.json'))['etats'] for m in modes}
def dist(r):
    X = np.array(list(r['positions'].values())); i, j = np.triu_indices(len(X), 1); return np.sort(np.linalg.norm(X[i] - X[j], axis=1))
out = []
ref = modes[0]
for k in range(min(len(R[m]) for m in modes)):
    a = R[ref][k]; ligne = dict(n=a['n'], fil=a['fil_canonique'], E=a['E'], methode=a['methode'], egalites=a['egalites'], ecart_min=min([x for x in a['ecart_au_suivant'] if x is not None], default=None))
    for m in modes[1:]:
        b = R[m][k]
        ligne[m] = dict(meme_fil=a['fil_canonique'] == b['fil_canonique'], dE=abs(a['E'] - b['E']), methode=b['methode'],
                        dX=float(max(np.abs(np.array(a['positions'][c]) - np.array(b['positions'][c])).max() for c in a['positions'])),
                        ecart_isometrie=float(np.abs(dist(a) - dist(b)).max()))
    out.append(ligne)
    print(a['n'], a['fil_canonique'], a['methode'][:10], 'E %.9f' % a['E'], 'egal', a['egalites'], '|', ' | '.join(f"{m}: fil {'=' if ligne[m]['meme_fil'] else 'X'} dE {ligne[m]['dE']:.1e} dX {ligne[m]['dX']:.1e} iso {ligne[m]['ecart_isometrie']:.1e} {ligne[m]['methode'][:4]}" for m in modes[1:]))
json.dump(out, open(f'c163c_{g}_analyse{suf}.json', 'w'), indent=1)
