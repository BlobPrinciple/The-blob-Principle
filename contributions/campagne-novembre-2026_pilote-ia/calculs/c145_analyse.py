import json, collections, numpy as np, math
R = json.load(open('c145.json')); G = [o for o in R if o['type'] == 'G']; Wt = [o for o in R if o['type'] == 'W']; Lb = [o for o in R if o['type'] == 'L']
T0 = 2 * math.pi / math.sqrt(2); PU = [0.0, 1 / 48, 1 / 16, 1 / 8, 1 / 4, 1 / 2]; PN = {0.0: '0', 1 / 48: '1/48', 1 / 16: '1/16', 1 / 8: '1/8', 1 / 4: '1/4', 1 / 2: '1/2'}; CA = ['1/2', '4/5', '1', '6/5']; RG = ['B0', 'Bg', 'H3', 'X3']
ix = {(o['regime'], o['source'], o['P'], o['cadence']): o for o in G}
def key(d): return (d['t1'] is not None, tuple(tuple(q) for q in d['groupe']), d['chocs'], d['statut'], tuple(tuple(q) for q in d['liens']))
print(len(G), 'trajectoires de grille,', len(Wt), 'témoins perturbés,', len(Lb), 'permutations')
print('\n1. CLASSEMENTS')
for nm, f in (('lettre stricte', lambda o: o['verdict']), ('référence', lambda o: o['verdict_ref']), ('DOP853 brut', lambda o: o['dop']['statut']), ('RK4 T0/1024 brut', lambda o: o['rk1']['statut']), ('RK4 T0/2048 brut', lambda o: o['rk2']['statut'])):
    print(f'   {nm:<18}', dict(collections.Counter(f(o) for o in G)))
print('   accord des trois intégrations :', sum(o['accord'] for o in G), '/ 288 ; bilan des trois sous 1e-6 :', sum(o['bilan_ok'] for o in G), '; bilan DOP853 sous 1e-6 :', sum(o['bilan_dop'] for o in G))
for s in ('dop', 'rk1', 'rk2'): print(f'   {s} : résidu absolu max {max(o[s]["residu_abs"] for o in G):.1e}, relatif max {max(o[s]["residu_rel"] for o in G):.1e}, quantité de mouvement max {max(o[s]["qmv"] for o in G):.1e}, moment cinétique max {max(o[s]["mcin"] for o in G):.1e}')
print('   causes d\'indétermination (lettre stricte) :', dict(collections.Counter(('désaccord' if not o['accord'] else '') + ('+bilan RK4' if not o['bilan_ok'] else '') for o in G if o['verdict'] == 'INDETERMINE')))
print('   indéterminés de référence par source :', dict(collections.Counter(o['source'] for o in G if o['verdict_ref'] == 'INDETERMINE')), '; par régime :', dict(collections.Counter(o['regime'] for o in G if o['verdict_ref'] == 'INDETERMINE')), '; par puissance :', dict(collections.Counter(PN[o['P']] for o in G if o['verdict_ref'] == 'INDETERMINE')))
print('\n2. SEUIL T-1 (P = 0 et 1/48) : sorties relevées, tous solveurs :', sum((o[s]['t1'] is not None) for o in G if o['P'] < 0.03 for s in ('dop', 'rk1', 'rk2')), 'sur', 3 * sum(o['P'] < 0.03 for o in G))
print('\n3. PREMIERES RUPTURES (DOP853 brut ; entre parenthèses : confirmées en lecture de référence), par puissance : nombre de cadences sur 4')
for src in 'SCF':
    print(f'   source {src}')
    for reg in RG:
        row = []
        for P in PU[2:]:
            a = [ix[(reg, src, P, c)] for c in CA]; row.append(f"{sum(o['dop']['t1'] is not None for o in a)}({sum(o['dop']['t1'] is not None and o['verdict_ref'] != 'INDETERMINE' for o in a)})")
        per = []
        for P in PU[2:]:
            a = [ix[(reg, src, P, c)] for c in CA]; per.append(f"{sum(o['dop']['statut'] == 'PERSISTANTE' for o in a)}({sum(o['verdict_ref'] == 'PERSISTANTE' for o in a)})")
        print(f'      {reg} : ruptures  P=1/16 {row[0]}  1/8 {row[1]}  1/4 {row[2]}  1/2 {row[3]}   | séparations persistantes  {per[0]}  {per[1]}  {per[2]}  {per[3]}')
print('\n4. DETAIL DES RUPTURES (DOP853) : P, cadence, régime, source, instant, groupe, chocs, travail, statut, lecture de référence, écart de t1 entre solveurs, rmin')
for P in PU[2:]:
    for c in CA:
        for reg in RG:
            for src in 'SCF':
                o = ix[(reg, src, P, c)]; d = o['dop']
                if d['t1'] is not None or o['rk2']['t1'] is not None:
                    print(f"   {PN[P]:<5} {c:<4} {reg} {src}  t1={('%.3f' % d['t1']) if d['t1'] is not None else '  -  ':<7} {str(d['groupe']):<26} chocs={d['chocs']:<3} W={d['travail']:<6.3f} {d['statut']:<11} réf={o['verdict_ref']:<11} strict={o['verdict']:<11} dt1={o['dt1']:.1e} rk2={o['rk2']['statut'][:5]} t1rk2={o['rk2']['t1'] and round(o['rk2']['t1'],3)} rmin={min(d['rmin']):.0e}")
print('\n5. S CONTRE C, à puissance, cadence et matériau fixés (64 triplets, P >= 1/16)')
cat = collections.Counter(); catref = collections.Counter(); lst = []
for P in PU[2:]:
    for c in CA:
        for reg in RG:
            s = ix[(reg, 'S', P, c)]; cc = ix[(reg, 'C', P, c)]; a = s['dop']['t1'] is not None; b = cc['dop']['t1'] is not None
            k = 'les deux' if a and b else ('S seule' if a else ('C seule' if b else 'aucune')); cat[k] += 1
            det = s['verdict_ref'] != 'INDETERMINE' and cc['verdict_ref'] != 'INDETERMINE'; catref[k if det else 'indéterminé'] += 1; lst.append((P, c, reg, k, det, s, cc))
print('   DOP853 brut :', dict(cat)); print('   lecture de référence (les deux trajectoires déterminées) :', dict(catref))
for P, c, reg, k, det, s, cc in lst:
    if k in ('S seule', 'C seule'): print(f"   {k} : P={PN[P]} c={c} {reg} ; réf S={s['verdict_ref']} C={cc['verdict_ref']} ; strict S={s['verdict']} C={cc['verdict']} ; t1 S={s['dop']['t1'] and round(s['dop']['t1'],3)} C={cc['dop']['t1'] and round(cc['dop']['t1'],3)} ; rk2 S={s['rk2']['t1'] and round(s['rk2']['t1'],3)} C={cc['rk2']['t1'] and round(cc['rk2']['t1'],3)}")
b2 = [(P, c, reg, det, s, cc) for P, c, reg, k, det, s, cc in lst if k == 'les deux']
print(f"   quand les deux rompent ({len(b2)} triplets) : C avant S dans {sum(cc['dop']['t1'] < s['dop']['t1'] for *_, s, cc in b2)} ; parmi les {sum(det for _,_,_,det,_,_ in b2)} déterminés : C avant S dans {sum(cc['dop']['t1'] < s['dop']['t1'] for _,_,_,det,s,cc in b2 if det)}")
print(f"      travail injecté avant rupture, médiane : S {np.median([s['dop']['travail'] for *_, s, cc in b2]):.3f}, C {np.median([cc['dop']['travail'] for *_, s, cc in b2]):.3f} ; C < S dans {sum(cc['dop']['travail'] < s['dop']['travail'] for *_, s, cc in b2)}")
print(f"      taille du groupe de première rupture : S {dict(collections.Counter(len(s['dop']['groupe']) for *_, s, cc in b2))}, C {dict(collections.Counter(len(cc['dop']['groupe']) for *_, s, cc in b2))}")
print('\n6. CONCENTRATION AVANT RUPTURE (DOP853) : part moyenne du lien le plus chargé F_U, et rapport des intégrales (énergie du lien le plus chargé / énergie de cohésion totale)')
def conc(o):
    d = o['dop']
    if d['t1'] is not None: a = d['avant']; t = a['t'] * T0; I = a['I']; mx = a['mx']
    else: a = d['points']['24']['cumul']; t = 24 * T0; I = a['I']; mx = a['mx']
    return (I[0] / t if t > 0 else 0.0, I[1] / I[2] if I[2] > 0 else 0.0, mx[0], mx[1], mx[2])
def common(o1, o2):
    """mêmes mesures sur la fenêtre commune [0, k T0], k = plus grand point de contrôle antérieur aux deux ruptures"""
    tt = [d['dop']['t1'] for d in (o1, o2) if d['dop']['t1'] is not None]; lim = min(tt) if tt else 24; ks = [k for k in (1, 4, 8, 12, 16, 20, 24) if k <= lim]
    if not ks: return None
    k = str(max(ks)); out = []
    for o in (o1, o2): I = o['dop']['points'][k]['cumul']['I']; out.append((I[0] / (int(k) * T0), I[1] / I[2] if I[2] > 0 else 0.0))
    return int(k), out
for src in 'SCF':
    v = [conc(ix[(reg, src, P, c)]) for P in PU[2:] for c in CA for reg in RG]
    print(f"   source {src} : F_U moyen {np.mean([q[0] for q in v]):.3f} (médiane {np.median([q[0] for q in v]):.3f}) ; rapport des intégrales {np.mean([q[1] for q in v]):.3f} (médiane {np.median([q[1] for q in v]):.3f})")
    for reg in RG:
        v = [conc(ix[(reg, src, P, c)]) for P in PU[2:] for c in CA]; print(f"        {reg} : F_U {np.mean([q[0] for q in v]):.3f} ; rapport {np.mean([q[1] for q in v]):.3f}")
up = 0; n = 0; upw = 0; rows = []
for P, c, reg, k, det, s, cc in lst:
    r = common(s, cc)
    if r is None: continue
    n += 1; up += r[1][1][0] > r[1][0][0]; upw += r[1][1][1] > r[1][0][1]; rows.append((P, c, reg, k, det, r))
print(f"   fenêtre commune S/C ({n} triplets) : F_U moyen plus élevé sous C dans {up} ; rapport des intégrales plus élevé sous C dans {upw}")
print(f"      moyennes sur fenêtre commune : F_U  S {np.mean([r[1][0][0] for *_, r in rows]):.3f}  C {np.mean([r[1][1][0] for *_, r in rows]):.3f} ; rapport  S {np.mean([r[1][0][1] for *_, r in rows]):.3f}  C {np.mean([r[1][1][1] for *_, r in rows]):.3f}")
for reg in RG:
    rr = [r for P, c, rg, k, det, r in rows if rg == reg]; print(f"        {reg} : F_U  S {np.mean([r[1][0][0] for r in rr]):.3f}  C {np.mean([r[1][1][0] for r in rr]):.3f} ; rapport  S {np.mean([r[1][0][1] for r in rr]):.3f}  C {np.mean([r[1][1][1] for r in rr]):.3f} ; C > S (rapport) dans {sum(r[1][1][1] > r[1][0][1] for r in rr)}/{len(rr)}")
print('\n7. F CONTRE S (borne construite)')
catf = collections.Counter(); catfr = collections.Counter()
for P in PU[2:]:
    for c in CA:
        for reg in RG:
            s = ix[(reg, 'S', P, c)]; f = ix[(reg, 'F', P, c)]; a = s['dop']['t1'] is not None; b = f['dop']['t1'] is not None
            k = 'les deux' if a and b else ('S seule' if a else ('F seule' if b else 'aucune')); catf[k] += 1; catfr[k if (s['verdict_ref'] != 'INDETERMINE' and f['verdict_ref'] != 'INDETERMINE') else 'indéterminé'] += 1
print('   DOP853 brut :', dict(catf), '; référence :', dict(catfr))
for src in 'SCF':
    for reg in RG:
        pm = [PN[P] for P in PU[2:] if any(ix[(reg, src, P, c)]['dop']['t1'] is not None for c in CA)]; print(f"   plus faible puissance avec rupture, {src} {reg} : {pm[0] if pm else 'aucune'}", end=' ;')
    print()
print('\n8. TRAVERSEES (distance minimale d\'un lien sous 0,01, DOP853) :', {src: sum(min(ix[(reg, src, P, c)]['dop']['rmin']) < 0.01 for P in PU for c in CA for reg in RG) for src in 'SCF'}, 'sur 96 par source')
print('   dont parmi les trajectoires avec rupture :', {src: sum(min(o['dop']['rmin']) < 0.01 for o in G if o['source'] == src and o['dop']['t1'] is not None) for src in 'SCF'})
print('\n9. TEMOINS PERTURBES (DOP853, +/- 1e-8) contre trajectoire nominale DOP853')
agree = 0; rows = collections.defaultdict(list)
for o in Wt:
    nom = ix[(o['regime'], o['source'], o['P'], o['cadence'])]; rows[(o['regime'], o['source'], o['P'], o['cadence'])].append(o)
for kk, ws in sorted(rows.items(), key=lambda q: (q[0][2], q[0][3], q[0][0], q[0][1])):
    nom = ix[kk]; same = all(key(w['dop']) == key(nom['dop']) for w in ws); agree += same
    print(f"   {kk[0]} {kk[1]} P={PN[kk[2]]} c={kk[3]:<4}: nominal {nom['dop']['statut']:<11} t1={nom['dop']['t1'] and round(nom['dop']['t1'],3)} {nom['dop']['groupe']} | +: {ws[0]['dop']['statut']:<11} t1={ws[0]['dop']['t1'] and round(ws[0]['dop']['t1'],3)} {ws[0]['dop']['groupe']} | -: {ws[1]['dop']['statut']:<11} t1={ws[1]['dop']['t1'] and round(ws[1]['dop']['t1'],3)} {ws[1]['dop']['groupe']} | {'ACCORD' if same else 'DESACCORD'} | réf nominale {nom['verdict_ref']}")
print(f'   accord complet : {agree}/24')
print('\n10. PERMUTATION D\'ETIQUETTES (2,0,3,1)')
for o in Lb:
    nom = ix[(o['regime'], o['source'], o['P'], o['cadence'])]; pm = o['perm']; EDGE = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]; order = [EDGE.index(tuple(sorted((pm[a], pm[b])))) for a, b in EDGE]
    dv = {k: float(np.abs(np.array(nom['dop']['points'][k]['r']) - np.array(o['dop']['points'][k]['r'])[order]).max()) for k in ('1', '4', '8', '16', '24', '28')}
    print(f"   {o['regime']} {o['source']} P={PN[o['P']]} c={o['cadence']:<4}: {'ACCORD' if key(o['dop']) == key(nom['dop']) else 'DESACCORD'} ; écart des distances : " + ' ; '.join(f'{k} T0 {v:.0e}' for k, v in dv.items()))
