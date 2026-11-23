#!/usr/bin/env python3
"""X-27 -- figure du plus petit contre-exemple trouve a K20 (17 naissances). Vue de dessus de la couche comprise entre les constituants e0 et e1 du germe,
realises par deux plans paralleles (controle de geometrie ordinaire de x27_contre_exemple.py). Chaque constituant est une sphere : on dessine son contour vu
de dessus. Lit x27_contre_exemple_court.json. Usage : python3 x27_contre_exemple_figure.py sortie.png     Claude, 23 novembre 2026."""
import json, os, sys
from fractions import Fraction as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import x27_contre_exemple as c

ICI = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(ICI, 'x27_contre_exemple_court.json')))
naissances = [tuple(u) for u in r['liste_des_naissances']]; rang = {u: k for k, u in enumerate(naissances, 1)}
x = tuple(F(v) for v in r['place_hors_empilement'])
libres = [tuple(u) for u in r['cotes_libres_de_cellule_que_la_place_chevauche']]
S = list(c.G5) + naissances
pos = c.controle_euclidien(S + libres, x)['positions']
P = {tuple(e[0]): e[1:] for e in pos['constituants']}

fig, ax = plt.subplots(figsize=(12, 8.4), dpi=200)
bleu, gris, vert, rouge = '#2a78d6', '#8a8a86', '#1baa6b', '#e34948'
for u in libres:
    cx, cy, cz, ray = P[u]
    ax.add_patch(Circle((cx, cy), ray, fill=False, ec='#333333', lw=1.6, ls=(0, (5, 4)), zorder=2))
cx, cy, cz, ray = pos['x']
ax.add_patch(Circle((cx, cy), ray, fc=rouge, ec=rouge, alpha=0.30, lw=0, zorder=3)); ax.add_patch(Circle((cx, cy), ray, fill=False, ec=rouge, lw=2.4, zorder=6))
for u in S:
    if u not in P: continue                                   # e0 et e1 sont les deux plans
    cx, cy, cz, ray = P[u]; grand = abs(ray - 1) < 1e-6
    coul = gris if u in c.G5 else (bleu if grand else vert)
    ax.add_patch(Circle((cx, cy), ray, fc=coul, ec=coul, alpha=0.16 if grand else 0.55, lw=0, zorder=1 if grand else 4))
    ax.add_patch(Circle((cx, cy), ray, fill=False, ec=coul, lw=1.8 if grand else 1.0, zorder=5))
    if u in rang and (grand or ray > 0.2): ax.text(cx, cy, str(rang[u]), ha='center', va='center', fontsize=12 if grand else 7.5, color='#1a1a1a', zorder=7, fontweight='bold')
    elif u in c.G5: ax.text(cx, cy, 'germe', ha='center', va='center', fontsize=11, color='#3a3a3a', zorder=7)
xs = [v[0] for v in P.values()] + [pos['x'][0]]; ys = [v[1] for v in P.values()] + [pos['x'][1]]
xd = max(xs) + 1.35
ax.annotate('place admissible\nhors de l\'empilement', xy=(pos['x'][0] + 0.72, pos['x'][1] + 0.1), xytext=(xd, pos['x'][1] + 0.35), ha='left', va='center', fontsize=11, color='#a01f1f',
            fontweight='bold', arrowprops=dict(arrowstyle='-', color='#a01f1f', lw=1.1), zorder=9)
for u in libres:
    cx, cy, cz, ray = P[u]; haut = cy > 0
    ax.text(cx + (0.22 if haut else 0.0), cy + (0.45 if haut else -0.5), 'côté libre,\njamais occupé', ha='center', va='center', fontsize=8.8, color='#333333', zorder=9)
ax.set_xlim(min(xs) - 1.2, xd + 3.3); ax.set_ylim(min(ys) - 1.2, max(ys) + 1.2); ax.set_aspect('equal'); ax.axis('off')
import matplotlib.lines as ml
leg = [ml.Line2D([], [], marker='o', ls='', mfc='#dcdcda', mec=gris, ms=13, label='germe (ses deux autres constituants sont les deux plans, dessus et dessous)'),
       ml.Line2D([], [], marker='o', ls='', mfc='#cfe0f5', mec=bleu, ms=13, label='né dans une cellule, touche les deux plans (le nombre est le rang de naissance)'),
       ml.Line2D([], [], marker='o', ls='', mfc=vert, mec=vert, ms=8, label='né dans une cellule, petit, posé sur le plan du dessous (naissances 2 à 10)'),
       ml.Line2D([], [], marker='o', ls='', mfc='none', mec='#333333', ms=13, label='côté libre d\'une cellule, que ce tissu n\'a jamais occupé'),
       ml.Line2D([], [], marker='o', ls='', mfc='#f3c1c0', mec=rouge, ms=13, label='la place hors de l\'empilement : elle touche les deux plans, le 17 et le 10, et ne chevauche rien')]
ax.legend(handles=leg, loc='upper center', bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=10, ncol=1)
ax.set_title('Après 17 naissances, toutes dans la cellule, une place admissible existe hors de l\'empilement\n(vue de dessus de la couche comprise entre deux constituants du germe)', fontsize=13, pad=10)
fig.savefig(sys.argv[1], bbox_inches='tight', facecolor='white')
print('figure', sys.argv[1], 'x', pos['x'], 'libres', [(u, P[u]) for u in libres])
