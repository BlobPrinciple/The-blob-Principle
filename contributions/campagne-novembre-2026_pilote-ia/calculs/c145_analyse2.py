import json, collections, numpy as np, math
R = json.load(open('c145.json')); G = [o for o in R if o['type'] == 'G']; PN = {0.0: '0', 1 / 48: '1/48', 1 / 16: '1/16', 1 / 8: '1/8', 1 / 4: '1/4', 1 / 2: '1/2'}
ix = {(o['regime'], o['source'], o['P'], o['cadence']): o for o in G}; CA = ['1/2', '4/5', '1', '6/5']; RG = ['B0', 'Bg', 'H3', 'X3']; PU = [1 / 16, 1 / 8, 1 / 4, 1 / 2]
print('A. Persistantes par source (DOP853 brut / référence) :', {s: (sum(o['dop']['statut'] == 'PERSISTANTE' for o in G if o['source'] == s), sum(o['verdict_ref'] == 'PERSISTANTE' for o in G if o['source'] == s)) for s in 'SCF'})
print('   Ruptures par source (brut / référence déterminée) :', {s: (sum(o['dop']['t1'] is not None for o in G if o['source'] == s), sum(o['dop']['t1'] is not None and o['verdict_ref'] != 'INDETERMINE' for o in G if o['source'] == s)) for s in 'SCF'})
print('   Ruptures par régime et source (brut) :', {r: {s: sum(o['dop']['t1'] is not None for o in G if o['source'] == s and o['regime'] == r) for s in 'SCF'} for r in RG})
print('B. Travail injecté avant la première rupture (DOP853), par source et régime : médiane [min ; max], n ; et travail par lien sorti')
for r in RG:
    for s in 'SCF':
        v = [(o['dop']['travail'], len(o['dop']['groupe'])) for o in G if o['source'] == s and o['regime'] == r and o['dop']['t1'] is not None]
        if v: print(f"   {r} {s} : {np.median([q[0] for q in v]):.2f} [{min(q[0] for q in v):.2f} ; {max(q[0] for q in v):.2f}], n={len(v)} ; par lien sorti {np.median([q[0]/q[1] for q in v]):.2f}")
v = [(o['dop']['travail'], len(o['dop']['groupe']), o['source']) for o in G if o['dop']['t1'] is not None and o['verdict_ref'] != 'INDETERMINE']
for s in 'SCF':
    w = [q for q in v if q[2] == s]; print(f"   déterminées, source {s} : n={len(w)}, travail médian {np.median([q[0] for q in w]):.2f} [{min(q[0] for q in w):.2f} ; {max(q[0] for q in w):.2f}], par lien {np.median([q[0]/q[1] for q in w]):.2f}")
print('C. Où va l\'énergie à 24 T0 quand rien ne rompt (parts du travail injecté : cinétique, cohésion, modes internes, chaleur évacuée), P = 1/2 et P = 1/4, moyenne sur cadences')
for P in (1 / 4, 1 / 2):
    for r in RG:
        for s in 'SCF':
            a = [ix[(r, s, P, c)]['dop'] for c in CA if ix[(r, s, P, c)]['dop']['t1'] is None]
            if a:
                q = [(d['points']['24']['cin'], d['points']['24']['coh'], d['points']['24']['interne'], d['points']['24']['ext'], d['travail']) for d in a]
                print(f"   P={PN[P]} {r} {s} (n={len(a)}) : cin {np.mean([x[0]/x[4] for x in q]):.2f}  coh {np.mean([x[1]/x[4] for x in q]):.2f}  interne {np.mean([x[2]/x[4] for x in q]):.2f}  chaleur {np.mean([x[3]/x[4] for x in q]):.2f}  (travail {np.mean([x[4] for x in q]):.1f})")
print('D. Cas déterminés où S et C rompent tous deux :')
for P in PU:
    for c in CA:
        for r in RG:
            s = ix[(r, 'S', P, c)]; cc = ix[(r, 'C', P, c)]; f = ix[(r, 'F', P, c)]
            if s['dop']['t1'] is not None and cc['dop']['t1'] is not None and s['verdict_ref'] != 'INDETERMINE' and cc['verdict_ref'] != 'INDETERMINE':
                print(f"   P={PN[P]} c={c} {r} : S t1={s['dop']['t1']:.2f} W={s['dop']['travail']:.2f} {len(s['dop']['groupe'])} liens {s['dop']['statut']} | C t1={cc['dop']['t1']:.2f} W={cc['dop']['travail']:.2f} {len(cc['dop']['groupe'])} lien {cc['dop']['statut']} | F t1={f['dop']['t1'] and round(f['dop']['t1'],2)} W={f['dop']['travail']:.2f} {f['dop']['statut']} (réf {f['verdict_ref']})")
print('E. Sous C : le lien de première rupture touche-t-il le dernier porteur sollicité ?', collections.Counter((o['dop']['demandeur'] in o['dop']['groupe'][0]) for o in G if o['source'] == 'C' and o['dop']['t1'] is not None))
print('   Sous S : groupes', collections.Counter(str(o['dop']['groupe']) for o in G if o['source'] == 'S' and o['dop']['t1'] is not None))
print('   Sous F : groupes', collections.Counter(str(o['dop']['groupe']) for o in G if o['source'] == 'F' and o['dop']['t1'] is not None))
print('F. Recaptures : parmi les ruptures transitoires (brut), nombre médian de sorties / recaptures du lien de première rupture ; ruptures après la fin de l\'injection (t1 > 24 T0) :', sum(o['dop']['t1'] is not None and o['dop']['t1'] > 24 for o in G))
print('G. Indéterminés de référence par source et régime :', {r: {s: sum(o['verdict_ref'] == 'INDETERMINE' for o in G if o['source'] == s and o['regime'] == r) for s in 'SCF'} for r in RG})
print('   bilan RK4 hors tolérance :', {s: sum((not o['bilan_ok']) for o in G if o['source'] == s) for s in 'SCF'}, '; dont avec traversée (rmin < 0,01 sur un solveur) :', sum((not o['bilan_ok']) and min(min(o[k]['rmin']) for k in ('dop', 'rk1', 'rk2')) < 0.01 for o in G), '/', sum(not o['bilan_ok'] for o in G))
print('   rmin des trajectoires au bilan RK4 hors tolérance :', sorted(round(min(min(o[k]['rmin']) for k in ('dop', 'rk1', 'rk2')), 4) for o in G if not o['bilan_ok']))
print('H. Durée totale de calcul (s) :', round(sum(o['duree'] for o in R)))
