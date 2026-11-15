#!/usr/bin/env python3
"""C-160c -- evaluation des etats 1 a 40 : P-marge (fonction analyse de c156c.py, inchangee) et P-original (reactions permises seulement
pour les volumes a 0,2 Vref a 1e-8 pres ; aucun contact actif). Compare aussi les etats 1 a 31 a ceux de C-158c (rejeu)."""
import gzip, json
import numpy as np, scipy.optimize as so
src = open('c156c.py').read().split("out = {}")[0]; exec(src)
def original(ex):
    ids = ex['sommets']; pos = {v: i for i, v in enumerate(ids)}; X = np.array(ex['X']); T = np.array([[pos[v] for v in t] for t in ex['cellules']])
    VR = np.array(ex['Vref']); I = np.array([pos[a] for a, b in ex['fils']]); J = np.array([pos[b] for a, b in ex['fils']]); R = np.array(ex['repos'])
    D = X[I] - X[J]; L = np.linalg.norm(D, axis=1); G = np.zeros_like(X); w = ((L - R) / L)[:, None] * D; np.add.at(G, I, w); np.add.at(G, J, -w)
    a, b, c, d = (X[T[:, i]] for i in range(4)); V = np.einsum('ij,ij->i', b - a, np.cross(c - a, d - a)) / 6; cols = []
    for t in np.nonzero(V <= 0.2 * VR * (1 + 1e-8))[0]:
        g = np.zeros_like(X); gb = np.cross(c[t] - a[t], d[t] - a[t]) / 6; gc = np.cross(d[t] - a[t], b[t] - a[t]) / 6; gd = np.cross(b[t] - a[t], c[t] - a[t]) / 6
        g[T[t, 1]] += gb; g[T[t, 2]] += gc; g[T[t, 3]] += gd; g[T[t, 0]] -= gb + gc + gd; cols.append(g.ravel())
    if cols:
        A = np.array(cols).T; mu, _ = so.nnls(A, G.ravel()); res = G.ravel() - A @ mu
    else: res = G.ravel()
    return float(np.abs(res).max())
out = {}
for sd in (1320, 1321, 1322):
    o = json.load(gzip.open(f'c160c_{sd}_etats.json.gz')); ref = json.load(gzip.open(f'c158c_{sd}_etats.json.gz')); rows = []
    for i, r in enumerate(o['U']['etats']):
        k = analyse(r['export']); k.update(n=r['n'], methode=r['methode'], marge_stationnaire=bool(k['residu'] < 1e-5), residu_original=original(r['export']), qmin=r['qmin'], q10=r['q10'],
                 rapport_volume=r['rapport_volume'], fondateurs_max=r['fondateurs_max'], recouvrements=r['recouvrements_controle_independant'], admissible=r['admissible'], degre_arete=r['degre_arete'],
                 ecart_au_rejeu=(abs(r['E'] - ref['U']['etats'][i]['E']) if i < 31 else None)); k['original_stationnaire'] = bool(k['residu_original'] < 1e-5); rows.append(k)
    out[str(sd)] = dict(statut=o['U']['statut'], B_volume_final=o['B']['etats'][-1]['somme_volumes'], B_recouvrements=sum(x['recouvrements_controle_independant'] for x in o['B']['etats']), etats=rows)
    print(sd, o['U']['statut'], '| ecart rejeu max 1-31 :', max(x['ecart_au_rejeu'] for x in rows[:31]), '| P-marge stationnaires 1-31 :', sum(x['marge_stationnaire'] for x in rows[:31]), '; 32-40 :', sum(x['marge_stationnaire'] for x in rows[31:]), '/', len(rows[31:]),
          '| P-original 1-31 :', sum(x['original_stationnaire'] for x in rows[:31]), '; 32-40 :', sum(x['original_stationnaire'] for x in rows[31:]), '| recouvrements :', sum(x['recouvrements'] for x in rows))
    for x in rows[31:]: print('   n', x['n'], 'E %.4f' % x['E'], 'marge %.1e' % x['residu'], 'orig %.1e' % x['residu_original'], 'qmin %.4f' % x['qmin'], 'q10 %.3f' % x['q10'], 'vol x%.1f' % x['rapport_volume'], 'k', x['degre_arete'], 'contacts', x['contacts_actifs'], 'volumes', x['volumes_actifs'])
    sous = [x['n'] for x in rows if x['qmin'] < 0.01]; print('   naissances sous 0,01 :', sous)
json.dump(out, open('c160c_kkt.json', 'w'), indent=1)
