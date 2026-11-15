#!/usr/bin/env python3
"""C-158c -- controle d'equilibre (fonction analyse de c156c.py, inchangee) sur les etats de c158c.py."""
import json
src = open('c156c.py').read().split("out = {}")[0]; exec(src)
out = {}
for sd in (1320, 1321, 1322):
    o = json.load(open(f'c158c_{sd}_etats.json')); rows = []
    for r in o['U']['etats']:
        k = analyse(r['export']); pol = [e for e in r['essais'] if e.get('i') == 'poli']
        k.update(n=r['n'], methode=r['methode'], poli=(pol[0]['statut'] if pol else None), verifie=bool(k['residu'] < 1e-5), qmin=r['qmin'], rapport_volume=r['rapport_volume'],
                 fondateurs_max=r['fondateurs_max'], recouvrements_controle_independant=r['recouvrements_controle_independant'], admissible=r['admissible']); rows.append(k)
    out[str(sd)] = dict(statut=o['U']['statut'], B_statut=o['B']['statut'], B_volume_final=o['B']['etats'][-1]['somme_volumes'], etats=rows)
    nv = [x['n'] for x in rows if not x['verifie']]
    print(sd, o['U']['statut'], '| verifies', sum(x['verifie'] for x in rows), '/', len(rows), '| non verifies', nv, '| polis gardes', sum(x['poli'] == 'garde' for x in rows), 'ecartes', sum(x['poli'] == 'ecarte' for x in rows))
    for n in (5, 11, 12, 15, 31):
        if n <= len(rows): x = rows[n - 1]; print('   n', n, 'E %.6f' % x['E'], 'residu %.1e' % x['residu'], 'qmin %.4f' % x['qmin'], 'vol x%.2f' % x['rapport_volume'], 'fond %.2f' % x['fondateurs_max'], 'contacts', x['contacts_actifs'], 'volumes', x['volumes_actifs'])
json.dump(out, open('c158c_kkt.json', 'w'), indent=1)
