#!/usr/bin/env python3
"""C-171R-c -- contre-calcul du C-171 de ChatGPT depuis son instantane M30 (Claude, 15 novembre 2026). Predictions : c171r_prediction.txt (ecrites avant le calcul)."""
import itertools, json, math
import numpy as np
import c132_audit as c132
from c120 import Mesh, SEEDS, vol6
from c169c import degagement_min
from x1_regles import hessien
d = json.load(open('c171r_etat_m30_chatgpt.json')); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F')
m.X = {int(k): np.array(v) for k, v in d['vertices'].items()}; m.T = set(tuple(t) if vol6(m.X, tuple(t)) > 0 else (t[1], t[0], t[2], t[3]) for t in d['tetrahedra']); m.nv = max(m.X) + 1
m.rest = {e: 1.0 for t in m.T for e in itertools.combinations(sorted(t), 2)}; VREG = 1 / (6 * math.sqrt(2)); Vref = {t: 1.5 * VREG for t in m.T}
E0 = m.energy(); w = hessien(m)[0]; E = m.inc(); bord = m._bedges(); inter = [f for f in E if f not in bord]; ring = set(E[tuple(d['central_edge'])])
faces = lambda t: set(itertools.combinations(sorted(t), 3)); fr = set(f for t in ring for f in faces(t)); dg0, ch0 = degagement_min(m)
out = dict(etat=dict(sommets=len(m.X), cellules=len(m.T), fils=len(m.rest), E=E0, ecart_a_son_energie=abs(E0 - 0.00032459245571509827), vp_min=float(w[0]), fils_interieurs=[(list(f), len(E[f])) for f in inter],
                     degagement_min=dg0, chevauchements=ch0, volume_min_sur_Vreg=float(min(vol6(m.X, t) / 6 / VREG for t in m.T))), divisions=[])
print('ETAT', json.dumps(out['etat']), flush=True)
A = [(0, 9), (2, 6), (6, 10), (9, 10)]; C2 = [(16, 19), (22, 27), (13, 14), (24, 29), (29, 32), (26, 28)]
for e in sorted(f for f, v in E.items() if len(v) == 1):
    t = E[e][0]; cat = 'A' if t in ring else ('C1' if faces(t) & fr else 'C2')
    m2 = m.copy(); V2 = dict(Vref); m2.bisect(e)
    for t2 in m2.T: V2.setdefault(t2, 1.5 * VREG)
    V2 = {t2: V2[t2] for t2 in m2.T}; Eins = m2.energy(); c132.relax(m2, V2); E2 = m2.inc(); b2 = m2._bedges(); dg, chev = degagement_min(m2)
    r = dict(fil=list(e), categorie=cat, teste_par_chatgpt=('A' if e in A else 'C2' if e in C2 else None), cout_insertion=float(Eins - E0), cout_relaxe=float(m2.energy() - E0), admissible=bool(dg > 1e-9), chevauchements=chev,
             vp_min=float(hessien(m2)[0][0]), anneaux_apres=sorted(len(v) for f, v in E2.items() if f not in b2))
    out['divisions'].append(r); json.dump(out, open('c171r_c.json', 'w'))
    print(e, cat, r['teste_par_chatgpt'] or '-', 'insertion %.5f' % r['cout_insertion'], 'relaxe %.9f' % r['cout_relaxe'], 'adm', r['admissible'], 'chev', chev, 'vp %.1e' % r['vp_min'], 'anneaux', r['anneaux_apres'], flush=True)
