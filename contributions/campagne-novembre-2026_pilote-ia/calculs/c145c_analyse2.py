import json, collections, numpy as np, math
R = json.load(open('c145c.json')); ix = {(o['camp'], o['top'], o['src'], o['P'], o['cad'], o['stop'], o['a'], o['D'], o['g0'], o['g']): o for o in R}
A = [o for o in R if o['camp'] == 'A']; det = lambda o: o['verdict_ref'] != 'INDETERMINE'; PN = {1/128: '1/128', 1/64: '1/64', 1/32: '1/32', 1/16: '1/16', 1/8: '1/8', 1/4: '1/4', 1/2: '1/2', 1.0: '1'}
def k3(d): return (d['t1'] is not None, tuple(tuple(q) for q in d['groupe']), d['Pfirst'], d['Pany'], d['chocs'], d['ncol'])
print('A. [T-2] paires D = 1/2 / D = 2 non identiques en RK4 :')
for s in ('rk1', 'rk2'):
    for o in A:
        if o['D'] != 0.5: continue
        b = ix.get(('A', 'K4', o['src'], o['P'] * 4, o['cad'], 'A2', 0.5, 2.0, o['g0'], o['g']))
        if b is None or k3(o[s]) == k3(b[s]): continue
        x = o[s]; y = b[s]
        print(f"   {s} P/D={o['P']/0.5} c={o['cad']} {o['src']} g0={o['g0']} g={o['g']} : D=1/2 : {x['statut']} t1={x['t1']} gr={x['groupe']} chocs={x['chocs']} col={x['ncol']} amb={x['ambigu']} W={x['travail']} | D=2 : {y['statut']} t1={y['t1']} gr={y['groupe']} chocs={y['chocs']} col={y['ncol']} amb={y['ambigu']} W={y['travail']/4}")
print('B. friction : sorties et séparations durables par P/D (toutes sources, cadences, D ; perturbées + exactes), DOP853 brut')
for g0 in (0.0, 0.04):
    d = collections.defaultdict(lambda: [0, 0, 0, 0])
    for o in A:
        if o['g0'] != g0: continue
        q = d[o['P'] / o['D']]; q[0] += 1; q[1] += o['dop']['t1'] is not None; q[2] += o['dop']['Pany']; q[3] += o['dop']['Pany'] and det(o)
    print(f"   gamma0={g0} : " + ' | '.join(f"P/D={k:g}: n={v[0]}, sorties {v[1]}, P_any {v[2]} ({v[3]})" for k, v in sorted(d.items())))
print('C. friction : part du travail partie en chaleur à 24 T0, par P/D (trajectoires sans sortie) ; énergie restée dans le tétraèdre, en unités de D')
d = collections.defaultdict(list)
for o in A:
    if o['g0'] == 0.04 and o['dop']['t1'] is None and o['dop']['travail'] > 0: p = o['dop']['points']['24']; d[o['P'] / o['D']].append((p['ext'] / o['dop']['travail'], (p['cin'] + p['coh']) / o['D']))
print('   ' + ' | '.join(f"P/D={k:g}: chaleur {np.mean([q[0] for q in v]):.3f}, énergie stockée {np.mean([q[1] for q in v]):.2f} D (max {max(q[1] for q in v):.2f})" for k, v in sorted(d.items())))
print('D. friction, P/D = 2 (D = 1/2, P = 1) : détail par source et cadence')
for c in ('1/2', '1'):
    for src in 'SCF':
        v = [ix[('A', 'K4', src, 1.0, c, 'A2', 0.5, 0.5, 0.04, g)] for g in range(9)]
        print(f"   c={c} {src} : sorties {sum(o['dop']['t1'] is not None for o in v)}/9 ; P_any {sum(o['dop']['Pany'] for o in v)} ({sum(o['dop']['Pany'] and det(o) for o in v)}) ; t1 {min(o['dop']['t1'] for o in v if o['dop']['t1']):.2f}-{max(o['dop']['t1'] for o in v if o['dop']['t1']):.2f} ; travail moyen {np.mean([o['dop']['travail'] for o in v]):.2f} ; chaleur {np.mean([o['dop']['chaleur'] for o in v]):.2f} ; liens durables {collections.Counter(len(o['dop']['liens']) for o in v)}")
print('E. liant nu sous A2, par P/D : P_any toutes sources (perturbées), brut (déterminés) / 144')
d = collections.defaultdict(lambda: [0, 0, 0, 0])
for o in A:
    if o['g0'] != 0.0 or o['g'] == 0: continue
    q = d[o['P'] / o['D']]; q[0] += 1; q[1] += o['dop']['t1'] is not None; q[2] += o['dop']['Pany']; q[3] += o['dop']['Pany'] and det(o)
print('   ' + ' | '.join(f"P/D={k:g}: n={v[0]}, sorties {v[1]}, P_any {v[2]} ({v[3]})" for k, v in sorted(d.items())))
print('F. réussites robustes (>= 6 perturbations sur 8), par source, liant nu : brutes / déterminées, par P/D')
for src in 'SCF':
    d = collections.defaultdict(lambda: [0, 0, 0])
    for D in (0.5, 1.0, 2.0):
        for c in ('1/2', '1'):
            for P in PN:
                v = [ix[('A', 'K4', src, P, c, 'A2', 0.5, D, 0.0, g)] for g in range(1, 9)]; q = d[P / D]; q[0] += 1; q[1] += sum(o['dop']['Pany'] for o in v) >= 6; q[2] += sum(o['dop']['Pany'] and det(o) for o in v) >= 6
    print(f"   {src} : " + ' | '.join(f"{k:g}: {v[1]}/{v[0]} ({v[2]})" for k, v in sorted(d.items()) if k >= 0.125))
print('G. tissu : première sortie, travail, chevauchement — K4 seul contre tissu (A1, mêmes couples) ; instant médian de première sortie')
C = [o for o in R if o['camp'] == 'C']
for top in ('K4', 'T5'):
    v = [o['dop'] for o in C if o['top'] == top and o['stop'] == 'A1']; print(f"   {top} : t1 médian {np.median([q['t1'] for q in v if q['t1']]):.2f} T0 ; travail avant sortie {np.median([q['travail'] for q in v]):.2f} ; collisions médianes {np.median([q['ncol'] for q in v]):.0f}")
v = [o['dop'] for o in C if o['top'] == 'T5']; print('   chevauchement avant la première sortie :', sum(q['ovl'] is not None and (q['t1'] is None or q['ovl'] < q['t1']) for q in v), '/', len(v), '; instant min / max :', round(min(q['ovl'] for q in v), 2), round(max(q['ovl'] for q in v), 2))
print('   tissu sous A2 : porteurs sans lien sur la fenêtre :', collections.Counter(tuple(q['deg0']) for q in [o['dop'] for o in C if o['top'] == 'T5' and o['stop'] == 'A2']))
print('   tissu : liens du second tétraèdre (04, 14, 24) durablement sortis sans que la face primaire soit lésée :', sum((not q['Pany']) and any(l[1] == 4 for l in q['liens_tous']) for q in v), '/', len(v))
print('H. indéterminés (référence) :', {k: (sum(not det(o) for o in R if o['camp'] == k and 'bloque' not in o['dop']), sum(o['camp'] == k and 'bloque' not in o['dop'] for o in R)) for k in 'ABC'}, '; tissu seul :', sum(not det(o) for o in C if o['top'] == 'T5'), '/ 144')
print('I. collisions ambiguës :', [(o['camp'], o['top'], o['src'], PN[o['P']], o['cad'], o['stop'], o['a'], o['D'], o['g0'], o['g'], [o[s]['ambigu'] for s in ('dop', 'rk1', 'rk2')]) for o in R if 'rk1' in o and any(o[s]['ambigu'] for s in ('dop', 'rk1', 'rk2'))])
import subprocess; print(subprocess.run('sha256sum c145c.py c145pr3_prediction.txt c145pr3_declaration.txt c145pr3_spec.txt c145c_controles.py c145c.json | cut -c1-16,65-', shell=True, capture_output=True, text=True).stdout)
