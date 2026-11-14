#!/usr/bin/env python3
"""C-147c ter -- reponses aux demandes de contre-audit de ChatGPT (13 novembre 2026, 7 h 18 UTC) : flux integre a travers
des coquilles, dependance a la taille du domaine, exposant a plus grande distance. Vraie trame de palier, part egale sur tous les fils.

Observable : u(x), quantite de la grandeur conservee portee par le porteur x a l'etat permanent ; equation : pour tout porteur
interieur, somme sur ses fils de (u(x) - u(voisin)) = source(x) ; u = 0 au bord. C'est le potentiel ; le flux sur un fil est u(x) - u(y).

Attendu, ecrit avant execution : (1) flux sortant de toute coquille cubique entourant la source = 1 a 1e-8 pres ;
(2) a 97^3 porteurs, exposant a 8 mailles entre 0,97 et 1,03 dans les trois directions, amplitude 4 pi A entre 0,2475 et 0,2525 ;
(3) entre 65^3 et 97^3, l'amplitude a 4 mailles varie de moins de 2 %.
Usage : python3 c147c_ter.py   (c147c_bis.py dans le meme repertoire)"""
import json
import math
import pathlib

import numpy as np
import scipy.sparse as sp

ICI = pathlib.Path(__file__).resolve().parent
exec((ICI / 'c147c_bis.py').read_text().split('# B1 : transmission egale sur tous les fils')[0])   # trame, aretes(), resous()

res = {}
for n in (33, 65, 97):
    a, b, d, grille, idx = aretes(n)
    N = n ** 3
    L = sp.coo_matrix((np.concatenate([-np.ones(len(a)), -np.ones(len(a))]), (np.concatenate([a, b]), np.concatenate([b, a]))), shape=(N, N)).tocsr()
    L = L + sp.diags(np.asarray(-L.sum(axis=1)).ravel())
    dedans = np.all((grille > 0) & (grille < n - 1), axis=1)
    c = n // 2                                   # 16, 32, 48 : classe (0,0,0), porteur a 26 fils
    rhs = np.zeros(N)
    rhs[idx[c, c, c]] = 1.0
    u = np.zeros(N)
    u[dedans] = resous(L[dedans][:, dedans], rhs[dedans])
    u3 = u.reshape(n, n, n)
    cheb = np.abs(grille - c).max(axis=1)
    flux = {}
    for R in (2, 4, 8, 12, 16, 24, 40):
        if R >= c:
            continue
        ina, inb = cheb[a] <= R, cheb[b] <= R
        flux[str(R)] = float((u[a][ina & ~inb] - u[b][ina & ~inb]).sum() + (u[b][inb & ~ina] - u[a][inb & ~ina]).sum())
    dirs = {'axe': (1, 0, 0), '(1,-1,0)': (1, -1, 0), '(1,1,1)': (1, 1, 1)}
    mes = {}
    for nom, v in dirs.items():
        Lv = math.sqrt(sum(x * x for x in v))
        v = np.array(v)
        for r0 in (4, 8):
            k = max(2, round(r0 / Lv))
            k += k % 2
            if 4 * k >= c:
                continue
            s = np.array([u3[tuple(c + j * v)] for j in range(0, 4 * k + 1)])
            mes[f'{nom} r={k * Lv:.1f}'] = dict(exposant=math.log2((s[k] - s[2 * k]) / (s[2 * k] - s[4 * k])),
                                              quatre_pi_A=4 * math.pi * 2 * k * Lv * (s[k] - s[2 * k]))
    res[f'{n}^3'] = dict(porteurs=N, fils=int(len(a)), flux_sortant=flux, mesures=mes)
(ICI / 'c147c_ter.json').write_text(json.dumps(res, indent=1))
for k, v in res.items():
    print(k, 'fils', v['fils'], 'flux', {R: round(f, 10) for R, f in v['flux_sortant'].items()})
    for m, w in v['mesures'].items():
        print('    ', m, 'p=%.4f 4piA=%.4f' % (w['exposant'], w['quatre_pi_A']))
