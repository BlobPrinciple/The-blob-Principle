import json, collections, numpy as np, math, sys
R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'c145c.json')); camp = collections.defaultdict(list)
for o in R: camp[o['camp']].append(o)
calc = [o for o in R if 'bloque' not in o['dop']]; det = lambda o: o['verdict_ref'] != 'INDETERMINE'
PS = [1/128, 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1.0]; PN = {1/128: '1/128', 1/64: '1/64', 1/32: '1/32', 1/16: '1/16', 1/8: '1/8', 1/4: '1/4', 1/2: '1/2', 1.0: '1'}
ix = {(o['camp'], o['top'], o['src'], o['P'], o['cad'], o['stop'], o['a'], o['D'], o['g0'], o['g']): o for o in R}
print(len(R), 'trajectoires ;', {k: len(v) for k, v in camp.items()}, '; bloquées :', len(R) - len(calc))
print('\n1. CLASSEMENTS ET CONTROLES')
for k in 'ABC':
    v = [o for o in camp[k] if 'bloque' not in o['dop']]
    if not v: continue
    print(f"   {k} n={len(v):<5} référence {dict(collections.Counter(o['verdict_ref'] for o in v))} | strict {dict(collections.Counter(o['verdict'] for o in v))} | DOP853 brut {dict(collections.Counter(o['dop']['statut'] for o in v))}")
    print(f"       accord {sum(o['accord'] for o in v)}/{len(v)} ; bilans des trois sous 1e-6 : {sum(o['bilan_ok'] for o in v)} ; ambigus {dict(collections.Counter(o[s]['ambigu'] for o in v for s in ('dop','rk1','rk2') if o[s]['ambigu']))} ; "
          f"résidus max {max(o['dop']['residu_abs'] for o in v):.0e} {max(o['rk1']['residu_abs'] for o in v):.0e} {max(o['rk2']['residu_abs'] for o in v):.0e} ; moments {max(o['dop']['qmv'] for o in v):.0e} {max(o['dop']['mcin'] for o in v):.0e} ; "
          f"r minimal / a {min(o[s]['rmin'] / o['a'] for o in v for s in ('dop','rk1','rk2')):.10f} ; collisions {sum(o['dop']['ncol'] for o in v)} ; variation d'énergie {max(o[s]['dkcol'] for o in v for s in ('dop','rk1','rk2')):.0e}")
print(f"   TOTAL calculé {len(calc)} ; indéterminés (référence) {sum(not det(o) for o in calc)} ({100*sum(not det(o) for o in calc)/max(len(calc),1):.1f} %) ; stricts {sum(o['verdict']=='INDETERMINE' for o in calc)}")
A = camp['A']
print('\n2. [T-1] borne énergétique : trajectoires avec 24 P < D :', sum(24 * o['P'] < o['D'] for o in A), '; sorties relevées (trois intégrations) :', sum((o[s]['t1'] is not None) for o in A if 24 * o['P'] < o['D'] for s in ('dop', 'rk1', 'rk2')))
print('\n3. CAMPAGNE A : séparation durable P_any sous A2, par P/D — nombre de géométries perturbées sur 8 (exact entre crochets) ; « R » = réussite robuste (>= 6 sur 8 déterminées, P_any)')
def cell(D, g0, c, src, P):
    v = [ix[('A', 'K4', src, P, c, 'A2', 0.5, D, g0, g)] for g in range(9)]; pa = sum(o['dop']['Pany'] for o in v[1:]); pad = sum(o['dop']['Pany'] and det(o) for o in v[1:]); ex = sum(o['dop']['t1'] is not None for o in v[1:])
    return pa, pad, ex, v[0]['dop']['statut'], sum(det(o) for o in v[1:])
rob = collections.defaultdict(dict)
for g0 in (0.0, 0.04):
    print(f'   friction gamma0 = {g0}')
    for D in (0.5, 1.0, 2.0):
        for c in ('1/2', '1'):
            for src in 'SCF':
                row = []
                for P in PS:
                    if any(('A', 'K4', src, P, c, 'A2', 0.5, D, g0, g) not in ix for g in range(9)): row.append('  ?  '); continue
                    pa, pad, ex, s0, nd = cell(D, g0, c, src, P); rob[(g0, D, c, src)][P] = (pad >= 6, pa >= 6, ex, pa)
                    row.append(f"{pa}({pad}){'R' if pad >= 6 else ('r' if pa >= 6 else ' ')}/{ex}")
                print(f"      D={D:<4} c={c:<3} {src} : " + '  '.join(f"{PN[P]}:{x}" for P, x in zip(PS, row)))
print('   lecture : P_any brut (déterminés) R=robuste déterminé, r=robuste brut seulement / nombre de perturbations avec sortie')
print('   seuils (plus petit P/D avec réussite robuste déterminée ; brute) et monotonie au-dessus :')
for g0 in (0.0, 0.04):
    for src in 'SCF':
        out = []
        for D in (0.5, 1.0, 2.0):
            for c in ('1/2', '1'):
                d = rob.get((g0, D, c, src), {}); pr = [P / D for P in PS if P in d and d[P][0]]; pb = [P / D for P in PS if P in d and d[P][1]]
                mono = all(d[P][1] for P in PS if P in d and pb and P / D >= min(pb))
                out.append(f"D={D},c={c}: {min(pr) if pr else '-'} ; {min(pb) if pb else '-'}{'' if mono else ' (non monotone)'}")
        print(f"      gamma0={g0} {src} : " + ' | '.join(out))
print('\n4. [T-2] INVARIANCE D\'ECHELLE (campagne A), à P/D, friction, cadence, source et géométrie égaux')
def k3(d): return (d['t1'] is not None, tuple(tuple(q) for q in d['groupe']), d['Pfirst'], d['Pany'], d['chocs'], d['ncol'])
for (Da, Db, nom) in ((0.5, 2.0, 'D = 1/2 contre D = 2 (facteur 4, exact en machine)'), (0.5, 1.0, 'D = 1/2 contre D = 1'), (1.0, 2.0, 'D = 1 contre D = 2')):
    n = 0; same = {'rk2': 0, 'dop': 0}; t1d = 0.0; nd = 0; samed = 0
    for o in A:
        if o['D'] != Da: continue
        Pb = o['P'] * Db / Da; kb = ('A', 'K4', o['src'], Pb, o['cad'], 'A2', 0.5, Db, o['g0'], o['g'])
        if kb not in ix: continue
        b = ix[kb]; n += 1
        for s in same: same[s] += k3(o[s]) == k3(b[s])
        if det(o) and det(b): nd += 1; samed += (o['dop']['statut'] == b['dop']['statut'])
    print(f"   {nom} : {n} paires ; identiques (sorties, groupes, P_first, P_any, chocs, collisions) : RK4 fin {same['rk2']}, DOP853 {same['dop']} ; parmi {nd} paires déterminées des deux côtés, même classement : {samed}")
print('\n5. FOCALISATION C > S (campagnes A et B) : configurations où C a P_any et S non dans >= 6 perturbations sur 8')
def paire(cp, top, P, c, stop, a, D, g0):
    S = [ix.get((cp, top, 'S', P, c, stop, a, D, g0, g)) for g in range(9)]; C = [ix.get((cp, top, 'C', P, c, stop, a, D, g0, g)) for g in range(9)]
    if any(q is None or 'bloque' in q['dop'] for q in S + C): return None
    f = sum(C[g]['dop']['Pany'] and not S[g]['dop']['Pany'] for g in range(1, 9)); fd = sum(C[g]['dop']['Pany'] and not S[g]['dop']['Pany'] and det(C[g]) and det(S[g]) for g in range(1, 9))
    i = sum(S[g]['dop']['Pany'] and not C[g]['dop']['Pany'] for g in range(1, 9)); idd = sum(S[g]['dop']['Pany'] and not C[g]['dop']['Pany'] and det(C[g]) and det(S[g]) for g in range(1, 9))
    return f, fd, i, idd, sum(q['dop']['Pany'] for q in S[1:]), sum(q['dop']['Pany'] for q in C[1:]), S[0]['dop']['statut'], C[0]['dop']['statut']
confs = sorted({(o['camp'], o['top'], o['P'], o['cad'], o['stop'], o['a'], o['D'], o['g0']) for o in R if o['camp'] in 'AB'}, key=str); nf = [0, 0, 0, 0]; nc = 0
for cf in confs:
    q = paire(*cf)
    if q is None: continue
    nc += 1; nf[0] += q[1] >= 6; nf[1] += q[0] >= 6; nf[2] += q[3] >= 6; nf[3] += q[2] >= 6
    if q[0] >= 5 or q[2] >= 5: print(f"      {cf} : C seul {q[0]}({q[1]}) ; S seul {q[2]}({q[3]}) ; P_any S {q[4]}/8, C {q[5]}/8 ; exact S {q[6]}, C {q[7]}")
print(f"   {nc} configurations : C > S robuste : {nf[0]} déterminées, {nf[1]} brutes ; S > C robuste : {nf[2]} déterminées, {nf[3]} brutes")
print('   concentration F_U moyenne à travail égal (dernier choc commun avant toute sortie), campagne A, par friction :')
for g0 in (0.0, 0.04):
    vs = []; vc = []; vf = []; up = 0; n = 0
    for o in A:
        if o['src'] != 'S' or o['g0'] != g0 or 24 * o['P'] < o['D']: continue
        kc = ('A', 'K4', 'C', o['P'], o['cad'], 'A2', 0.5, o['D'], g0, o['g']); kf = ('A', 'K4', 'F', o['P'], o['cad'], 'A2', 0.5, o['D'], g0, o['g'])
        if kc not in ix or kf not in ix: continue
        ps = o['dop']['parchoc']; pc = ix[kc]['dop']['parchoc']; pf = ix[kf]['dop']['parchoc']; k = min(len(ps), len(pc), len(pf)) - 1
        if k < 1: continue
        n += 1; fs = ps[k][2] / (ps[k][0] * 2 * math.pi / math.sqrt(2 * o['D'])); fc = pc[k][2] / (pc[k][0] * 2 * math.pi / math.sqrt(2 * o['D'])); ff = pf[k][2] / (pf[k][0] * 2 * math.pi / math.sqrt(2 * o['D'])); vs.append(fs); vc.append(fc); vf.append(ff); up += fc > fs
    if n: print(f"      gamma0={g0} : S {np.mean(vs):.3f}  C {np.mean(vc):.3f}  F {np.mean(vf):.3f} ; C > S dans {up}/{n}")
print('\n6. CAMPAGNE B : rayon du cœur — P_any, exact sur 4 / perturbé sur 32, DOP853 brut (déterminés)')
for a in (0.25, 0.5, 0.75, 1.0):
    for stop in ('A1', 'A2'):
        row = []
        for src in 'SC':
            v = [o for o in camp['B'] if o['a'] == a and o['stop'] == stop and o['src'] == src]
            if not v: row.append(f'{src} ?'); continue
            if 'bloque' in v[0]['dop']: row.append(f'{src} : BLOQUE ({len(v)})'); continue
            e = [o for o in v if o['g'] == 0]; p = [o for o in v if o['g'] > 0]
            row.append(f"{src} : exact {sum(o['dop']['Pany'] for o in e)}/{len(e)} ; perturbé {sum(o['dop']['Pany'] for o in p)}/{len(p)} ({sum(o['dop']['Pany'] and det(o) for o in p)}) ; sorties {sum(o['dop']['t1'] is not None for o in v)}/{len(v)} ; indéterminés {sum(not det(o) for o in v)}")
        print(f'   a={a:<4} {stop} | ' + ' | '.join(row))
print('\n7. CAMPAGNE C : K4 seul contre tissu de deux tétraèdres (cœur 3/4)')
for top in ('K4', 'T5'):
    for stop in ('A1', 'A2'):
        for src in 'SC':
            v = [o for o in camp['C'] if o['top'] == top and o['stop'] == stop and o['src'] == src]
            if not v: continue
            d = [o['dop'] for o in v]; pa = [q for q in d if q['Pany']]
            print(f"   {top} {stop} {src} : n={len(v)} sorties {sum(q['t1'] is not None for q in d)} ; face primaire durablement lésée (P_any) {len(pa)} ({sum(o['dop']['Pany'] and det(o) for o in v)}) ; "
                  f"dont tissu resté connexe sur la fenêtre {sum(q['connexe_fenetre'] for q in pa)} ; connexe à tout instant {sum(q['connexe_toujours'] for q in d)} ; porteur sans lien sur la fenêtre {sum(bool(q['deg0']) for q in d)} "
                  f"{dict(collections.Counter(tuple(q['deg0']) for q in d if q['deg0']))} ; chevauchement des deux tétraèdres {sum(q['ovl'] is not None for q in d)} (médiane {np.median([q['ovl'] for q in d if q['ovl'] is not None]) if any(q['ovl'] is not None for q in d) else float('nan'):.2f} T0) ; travail {np.mean([q['travail'] for q in d]):.2f} ; indéterminés {sum(not det(o) for o in v)}")
print('   redondance matérielle (face primaire lésée ET tissu connexe sur la fenêtre, >= 6 perturbations sur 8), par couple :')
nr = [0, 0]
for P in (1/4, 1/2):
    for c in ('1/2', '1'):
        for src in 'SC':
            for stop in ('A1', 'A2'):
                v = [ix.get(('C', 'T5', src, P, c, stop, 0.75, 1.0, 0.0, g)) for g in range(9)]
                if any(q is None for q in v): continue
                r = sum(q['dop']['Pany'] and q['dop']['connexe_fenetre'] for q in v[1:]); rd = sum(q['dop']['Pany'] and q['dop']['connexe_fenetre'] and det(q) for q in v[1:]); nr[0] += rd >= 6; nr[1] += r >= 6
                print(f"      P={PN[P]} c={c} {src} {stop} : {r}({rd})/8 ; P_any {sum(q['dop']['Pany'] for q in v[1:])}/8 ; connexe {sum(q['dop']['connexe_fenetre'] for q in v[1:])}/8 ; chevauchement {sum(q['dop']['ovl'] is not None for q in v[1:])}/8")
print(f"   configurations avec redondance robuste : {nr[0]} déterminées, {nr[1]} brutes")
print('\n8. RECOUPEMENTS INTERNES (mêmes paramètres calculés dans deux campagnes : doivent coïncider exactement)')
n = 0; same = 0
for o in camp['C']:
    if o['top'] != 'K4': continue
    b = ix.get(('B', 'K4', o['src'], o['P'], o['cad'], o['stop'], 0.75, 1.0, 0.0, o['g']))
    if b is None: continue
    n += 1; same += all(o[s]['t1'] == b[s]['t1'] and o[s]['Pany'] == b[s]['Pany'] and o[s]['ncol'] == b[s]['ncol'] for s in ('dop', 'rk1', 'rk2'))
for o in camp['B']:
    if o['a'] != 0.5 or o['stop'] != 'A2': continue
    b = ix.get(('A', 'K4', o['src'], o['P'], o['cad'], 'A2', 0.5, 1.0, 0.0, o['g']))
    if b is None: continue
    n += 1; same += all(o[s]['t1'] == b[s]['t1'] and o[s]['Pany'] == b[s]['Pany'] and o[s]['ncol'] == b[s]['ncol'] for s in ('dop', 'rk1', 'rk2'))
print(f'   {same}/{n} identiques')
print('\n9. DUREE :', round(sum(o['duree'] for o in R)), 's')
