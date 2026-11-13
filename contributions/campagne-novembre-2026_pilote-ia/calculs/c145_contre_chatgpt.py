# CONTRE-AUDIT du contrôle de ChatGPT (fil principal, 23 h 04 UTC) : cas B0, source C, P = 1/2, cadence 6/5 — sensibilité des séparations durables aux perturbations.
# Ce n'est pas un ajout à la grille de C-145 / PR-1 : c'est la vérification d'une affirmation de ChatGPT, avec mon code (c145.py), sans rien y changer.
import json, sys
from c145 import *
R = json.load(open('c145.json')); ix = {(o['regime'], o['source'], o['P'], o['cadence']): o for o in R if o['type'] == 'G'}
print('A. Mes valeurs pour les quatre triplets convergés (DOP853 ; écart maximal de t1 entre mes trois intégrations)')
for P, c in ((.25, '1/2'), (.25, '1'), (.5, '1/2'), (.5, '4/5')):
    for s in 'SC':
        o = ix[('B0', s, P, c)]; d = o['dop']; print(f"   P={P} c={c} {s} : t1 = {d['t1']:.9f} T0, groupe {d['groupe']}, durables {d['liens']}, écart entre solveurs {o['dt1']:.1e}")
o = ix[('B0', 'C', .5, '6/5')]
print('B. Cas P = 1/2, c = 6/5, B0, C dans mon exécution :'); 
for k in ('dop', 'rk1', 'rk2'): print(f"   {k} : {o[k]['statut']}, t1 = {o[k]['t1']:.9f}, groupe {o[k]['groupe']}, durables {o[k]['liens']}, résidu {o[k]['residu_abs']:.1e}, r final {[round(q,2) for q in o[k]['r_fin']]}")
print('   lecture stricte :', o['verdict'], '; référence :', o['verdict_ref'])
print('C. Même cas, sommet 1 déplacé le long de x (DOP853, mes tolérances)')
for eps in (0.0, 1e-10, -1e-10, 1e-8, -1e-8, 1e-6, -1e-6):
    d = run('B0', 'C', .5, '6/5', 'dop', perturb=eps); print(f"   perturbation {eps:+.0e} : {d['statut']:<11} t1 = {d['t1']:.9f}, groupe {d['groupe']}, durables {d['liens']}, résidu {d['residu_abs']:.1e}", flush=True)
print('D. Les trois autres cadences à P = 1/2 sous C dans B0, mêmes perturbations (durables ?)')
for c in ('1/2', '4/5', '1'):
    row = []
    for eps in (0.0, 1e-10, -1e-10, 1e-8, -1e-8):
        d = run('B0', 'C', .5, c, 'dop', perturb=eps); row.append(f"{d['statut'][:5]}{d['liens'] if d['liens'] else ''}@{d['t1']:.4f}")
    print(f'   c = {c} :', ' | '.join(row), flush=True)
print('E. Les quatre triplets convergés, source C, mêmes perturbations')
for P, c in ((.25, '1/2'), (.25, '1')):
    row = []
    for eps in (0.0, 1e-10, -1e-10, 1e-8, -1e-8):
        d = run('B0', 'C', P, c, 'dop', perturb=eps); row.append(f"{d['statut'][:5]}{d['liens'] if d['liens'] else ''}@{d['t1']:.4f}")
    print(f'   P = {P}, c = {c} :', ' | '.join(row), flush=True)
