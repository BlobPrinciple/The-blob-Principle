import json, collections, numpy as np, math
R = json.load(open('c145b.json')); camp = collections.defaultdict(list)
for o in R: camp[o['camp']].append(o)
det = lambda o: o['verdict_ref'] != 'INDETERMINE'; PN = {1/8: '1/8', 1/4: '1/4', 1/2: '1/2'}
star = [{(min(v, w), max(v, w)) for w in range(4) if w != v} for v in range(4)]
def ej(d): L = {tuple(q) for q in d['liens']}; return [v for v in range(4) if star[v] <= L]
M = [o for o in camp['princ'] if o['reg'] == 'B0']
print('A. Liant nu, cœur dur 1/2 : P_any selon la géométrie (exacte / 8 perturbées), DOP853 brut (déterminés)')
for stop in ('A1', 'A2'):
    for src in 'SCF':
        v = [o for o in M if o['stop'] == stop and o['src'] == src]; e = [o for o in v if o['g'] == 0]; p = [o for o in v if o['g'] > 0]
        print(f"   {stop} {src} : exacte {sum(o['dop']['Pany'] for o in e)}/{len(e)} ({sum(o['dop']['Pany'] and det(o) for o in e)}) ; perturbées {sum(o['dop']['Pany'] for o in p)}/{len(p)} ({sum(o['dop']['Pany'] and det(o) for o in p)}) ; "
              f"P >= 1/4 : {sum(o['dop']['Pany'] for o in v if o['P'] > .2)}/{sum(o['P'] > .2 for o in v)} ({sum(o['dop']['Pany'] and det(o) for o in v if o['P'] > .2)} déterminés sur {sum(det(o) for o in v if o['P'] > .2)}) ; "
              f"groupe de première sortie à 3 liens : exacte {sum(len(o['dop']['groupe']) == 3 for o in e)}, perturbées {sum(len(o['dop']['groupe']) == 3 for o in p)}")
print('B. Forme des séparations durables (liant nu, cœur dur 1/2) : porteur entier éjecté ; lequel')
for stop in ('A1', 'A2'):
    for src in 'SCF':
        v = [o['dop'] for o in M if o['stop'] == stop and o['src'] == src and o['dop']['Pany']]; c = collections.Counter(tuple(ej(d)) for d in v)
        print(f"   {stop} {src} : {len(v)} durables ; porteurs éjectés {dict(c)} ; nombre de liens durablement sortis {dict(collections.Counter(len(d['liens']) for d in v))} ; P_first {sum(d['Pfirst'] for d in v)}")
print('C. Travail injecté (liant nu, cœur dur 1/2, P >= 1/4) : moyenne ; travail des trajectoires durables ; instant de l\'arrêt définitif A2')
for stop in ('A1', 'A2'):
    for src in 'SCF':
        v = [o['dop'] for o in M if o['stop'] == stop and o['src'] == src and o['P'] > .2]; d = [q for q in v if q['Pany']]; ts = [q['tstop'] for q in v if q['tstop'] is not None]
        print(f"   {stop} {src} : travail moyen {np.mean([q['travail'] for q in v]):.2f} ; durables {len(d)} : travail médian {np.median([q['travail'] for q in d]) if d else float('nan'):.2f} ; non durables : {np.median([q['travail'] for q in v if not q['Pany']]) if len(d) < len(v) else float('nan'):.2f} ; "
              f"chocs après la première sortie (A2) {np.mean([q['chocs'] for q in v]):.1f} délivrés ; arrêt définitif dans {len(ts)}/{len(v)}, médiane {np.median(ts) if ts else float('nan'):.1f} T0 ; fraction de fenêtre avec un lien sorti {np.mean([q['frac'] for q in v]):.2f}")
print('D. Collisions avant la première sortie (liant nu, cœur dur 1/2) :', sum(o['dop']['col1'] is not None and o['dop']['t1'] is not None and o['dop']['col1'][0] < o['dop']['t1'] for o in M), '/', sum(o['dop']['t1'] is not None for o in M), 'trajectoires avec sortie ; collisions par trajectoire, médiane', np.median([o['dop']['ncol'] for o in M]))
print('E. Collisions ambiguës :', [(o['camp'], o['reg'], o['src'], PN[o['P']], o['cad'], o['stop'], o['g'], [o[s]['ambigu'] for s in ('dop', 'rk1', 'rk2')]) for o in R if 'rk1' in o and any(o[s]['ambigu'] for s in ('dop', 'rk1', 'rk2'))])
print('F. Témoin à cœur mou, selon la géométrie')
for stop in ('A1', 'A2'):
    for src in 'SC':
        v = [o for o in camp['trav'] if o['stop'] == stop and o['src'] == src]; e = [o for o in v if o['g'] == 0]; p = [o for o in v if o['g'] > 0]
        print(f"   {stop} {src} : exacte P_any {sum(o['dop']['Pany'] for o in e)}/{len(e)} ; perturbées {sum(o['dop']['Pany'] for o in p)}/{len(p)} ({sum(o['dop']['Pany'] and det(o) for o in p)} dét.) ; groupes à 3 liens (perturbées) {sum(len(o['dop']['groupe']) == 3 for o in p)} ; porteur 0 éjecté {sum(0 in ej(o['dop']) for o in v)} ; r minimal médian {np.median([min(o['dop']['rmin']) for o in v]):.3f} ; premier passage sous 1/2 médian {np.median([o['dop']['tcoeur'] for o in v]):.2f} T0 ; t1 médian {np.median([o['dop']['t1'] for o in v]):.2f}")
print('G. Rayons 1/4 et 3/4, selon la géométrie (A1)')
for a in (0.25, 0.75):
    for src in 'SC':
        v = [o for o in camp['coeur'] if o['stop'] == 'A1' and o['src'] == src and o['a'] == a]; e = [o for o in v if o['g'] == 0]; p = [o for o in v if o['g'] > 0]
        print(f"   a={a} {src} : exacte P_any {sum(o['dop']['Pany'] for o in e)}/{len(e)} ; perturbées {sum(o['dop']['Pany'] for o in p)}/{len(p)} ({sum(o['dop']['Pany'] and det(o) for o in p)} dét.) ; collisions avant sortie {sum(o['dop']['col1'] is not None and o['dop']['col1'][0] < o['dop']['t1'] for o in v)}/{len(v)}")
print('H. Modes internes : sorties et P_any par géométrie exacte / perturbée')
for reg in ('H3', 'X3'):
    for stop in ('A1', 'A2'):
        v = [o for o in camp['modes'] if o['reg'] == reg and o['stop'] == stop]; print(f"   {reg} {stop} : sorties {sum(o['dop']['t1'] is not None for o in v)}/{len(v)} ; P_any {sum(o['dop']['Pany'] for o in v)} ({sum(o['dop']['Pany'] and det(o) for o in v)} dét.) ; énergie interne / travail à 24 T0 : {np.mean([o['dop']['points']['24']['interne']/max(o['dop']['travail'],1e-9) for o in v]):.2f} ; chaleur {np.mean([o['dop']['points']['24']['ext']/max(o['dop']['travail'],1e-9) for o in v]):.2f}")
v = [o for o in camp['princ'] if o['reg'] == 'Bg']; print('I. Bγ :', len(v), 'trajectoires, sorties', sum(o['dop']['t1'] is not None or o['rk1']['t1'] is not None or o['rk2']['t1'] is not None for o in v), '; chaleur / travail à 24 T0 :', round(float(np.mean([o['dop']['points']['24']['ext']/o['dop']['travail'] for o in v])), 3), '; indéterminés', sum(not det(o) for o in v))
print('J. Indéterminés (référence) par campagne et cause :', {k: (sum(not det(o) for o in camp[k]), len(camp[k])) for k in ('princ', 'modes', 'coeur', 'trav')}, '; liant nu principal par puissance :', {PN[P]: (sum(not det(o) for o in M if o['P'] == P), sum(o['P'] == P for o in M)) for P in (1/8, 1/4, 1/2)})
print('K. Fichiers :'); import subprocess; print(subprocess.run('sha256sum c145b.py c145pr2_prediction.txt c145pr2_declaration.txt c145b_controles.py c145b.json | cut -c1-16,65-', shell=True, capture_output=True, text=True).stdout)
