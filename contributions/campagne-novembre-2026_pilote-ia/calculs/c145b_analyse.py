import json, collections, numpy as np, math, sys
R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'c145b.json')); T0 = 2 * math.pi / math.sqrt(2)
PN = {1 / 8: '1/8', 1 / 4: '1/4', 1 / 2: '1/2'}; CA = ['1/2', '4/5', '1', '6/5']; COUP = [(1 / 4, '1/2'), (1 / 4, '1'), (1 / 2, '1/2'), (1 / 2, '4/5')]
camp = collections.defaultdict(list)
for o in R: camp[o['camp']].append(o)
G = [o for o in R if o['camp'] in ('princ', 'modes', 'coeur', 'trav')]
ix = {(o['camp'], o['reg'], o['src'], o['P'], o['cad'], o['stop'], o['a'], o['g']): o for o in G}
det = lambda o: o['verdict_ref'] != 'INDETERMINE'
star = [{(min(v, w), max(v, w)) for w in range(4) if w != v} for v in range(4)]
def ejecte(d): L = {tuple(q) for q in d['liens']}; return any(s <= L for s in star)
print(len(R), 'calculs ;', {k: len(v) for k, v in camp.items()})
print('\n1. CLASSEMENTS ET CONTROLES')
for k in ('princ', 'modes', 'coeur', 'trav'):
    v = camp[k]
    if not v: continue
    print(f"   {k:<6} n={len(v):<5} strict {dict(collections.Counter(o['verdict'] for o in v))} | référence {dict(collections.Counter(o['verdict_ref'] for o in v))} | DOP853 brut {dict(collections.Counter(o['dop']['statut'] for o in v))}")
    print(f"          accord {sum(o['accord'] for o in v)}/{len(v)} ; bilans des trois sous 1e-6 : {sum(o['bilan_ok'] for o in v)} ; ambigus (un solveur au moins) : {sum(any(o[s]['ambigu'] for s in ('dop','rk1','rk2')) for o in v)} "
          f"{dict(collections.Counter(o[s]['ambigu'] for o in v for s in ('dop','rk1','rk2') if o[s]['ambigu']))}")
    print(f"          résidu max dop {max(o['dop']['residu_abs'] for o in v):.0e}, rk1 {max(o['rk1']['residu_abs'] for o in v):.0e}, rk2 {max(o['rk2']['residu_abs'] for o in v):.0e} ; quantité de mouvement {max(o['dop']['qmv'] for o in v):.0e} ; moment {max(o['dop']['mcin'] for o in v):.0e} ; "
          f"r minimal {min(min(o[s]['rmin']) for o in v for s in ('dop','rk1','rk2')):.10f} ; collisions (dop) {sum(o['dop']['ncol'] for o in v)}, simultanées {sum(o['dop']['nsimul'] for o in v)} ; variation d'énergie aux collisions {max(o[s]['dkcol'] for o in v for s in ('dop','rk1','rk2')):.0e}")
allg = [o for o in G]; print(f"   TOTAL 2 160 : {len(allg)} ; indéterminés en référence : {sum(not det(o) for o in allg)} ({100*sum(not det(o) for o in allg)/max(len(allg),1):.1f} %) ; à la lettre stricte : {sum(o['verdict']=='INDETERMINE' for o in allg)}")
def table(cp, regs, a=0.5, couples=None, srcs='SCF'):
    for reg in regs:
        for stop in ('A1', 'A2'):
            for src in srcs:
                v = [o for o in camp[cp] if o['reg'] == reg and o['stop'] == stop and o['src'] == src and o['a'] == a]
                if not v: continue
                ex = [o for o in v if o['dop']['t1'] is not None]; pa = [o for o in v if o['dop']['Pany']]; pf = [o for o in v if o['dop']['Pfirst']]
                print(f"   {reg} {stop} {src} a={a}: n={len(v):<4} sorties {len(ex):<4}({sum(det(o) for o in ex)})  P_any {len(pa):<4}({sum(det(o) for o in pa)})  P_first {len(pf):<4}({sum(det(o) for o in pf)})  porteur entier éjecté {sum(ejecte(o['dop']) for o in pa):<4} "
                      f"travail moyen {np.mean([o['dop']['travail'] for o in v]):.2f}  chocs sautés {np.mean([o['dop']['sautes'] for o in v]):.1f}  indéterminés {sum(not det(o) for o in v)}")
print('\n2. CAMPAGNE PRINCIPALE (a = 1/2) : sorties, P_any, P_first — DOP853 brut (déterminés en référence)')
table('princ', ('B0', 'Bg'))
print('   par puissance, liant nu :')
for stop in ('A1', 'A2'):
    for src in 'SCF':
        row = []
        for P in (1 / 8, 1 / 4, 1 / 2):
            v = [o for o in camp['princ'] if o['reg'] == 'B0' and o['stop'] == stop and o['src'] == src and o['P'] == P]; row.append(f"P={PN[P]}: sorties {sum(o['dop']['t1'] is not None for o in v)}/{len(v)}, P_any {sum(o['dop']['Pany'] for o in v)}({sum(o['dop']['Pany'] and det(o) for o in v)})")
        print(f'      {stop} {src} :', ' | '.join(row))
def candidats(cp, regs, a=0.5, couples=None):
    out = []
    confs = sorted({(o['reg'], o['P'], o['cad'], o['stop']) for o in camp[cp] if o['a'] == a and o['reg'] in regs}, key=lambda q: (q[0], q[3], q[1], CA.index(q[2])))
    for reg, P, c, stop in confs:
        if any((cp, reg, x, P, c, stop, a, g) not in ix for x in 'SC' for g in range(9)): continue
        S = [ix[(cp, reg, 'S', P, c, stop, a, g)] for g in range(9)]; C = [ix[(cp, reg, 'C', P, c, stop, a, g)] for g in range(9)]
        fort = sum(C[g]['dop']['Pany'] and not S[g]['dop']['Pany'] for g in range(1, 9)); fortd = sum(C[g]['dop']['Pany'] and not S[g]['dop']['Pany'] and det(C[g]) and det(S[g]) for g in range(1, 9))
        inv = sum(S[g]['dop']['Pany'] and not C[g]['dop']['Pany'] for g in range(1, 9)); invd = sum(S[g]['dop']['Pany'] and not C[g]['dop']['Pany'] and det(C[g]) and det(S[g]) for g in range(1, 9))
        tot = lambda g: C[g]['dop']['t1'] is not None and S[g]['dop']['t1'] is not None and C[g]['dop']['t1'] <= S[g]['dop']['t1'] - 0.5
        tard = lambda g: C[g]['dop']['t1'] is not None and S[g]['dop']['t1'] is not None and S[g]['dop']['t1'] <= C[g]['dop']['t1'] - 0.5
        f1 = sum(tot(g) for g in range(1, 9)); f1d = sum(tot(g) and det(C[g]) and det(S[g]) for g in range(1, 9)); f2 = sum(C[g]['dop']['t1'] is not None and S[g]['dop']['t1'] is None for g in range(1, 9))
        f3 = sum(tard(g) for g in range(1, 9)); f3d = sum(tard(g) and det(C[g]) and det(S[g]) for g in range(1, 9)); nd = sum(det(C[g]) and det(S[g]) for g in range(1, 9))
        out.append(dict(reg=reg, P=P, c=c, stop=stop, fort=fort, fortd=fortd, inv=inv, invd=invd, tot=f1, totd=f1d, cseul=f2, tard=f3, tardd=f3d, nd=nd,
                        sany=sum(q['dop']['Pany'] for q in S[1:]), cany=sum(q['dop']['Pany'] for q in C[1:]), sex=sum(q['dop']['t1'] is not None for q in S[1:]), cex=sum(q['dop']['t1'] is not None for q in C[1:]),
                        s0=S[0]['dop']['statut'], c0=C[0]['dop']['statut'], gs=collections.Counter(len(q['dop']['groupe']) for q in S[1:] if q['dop']['t1'] is not None), gc=collections.Counter(len(q['dop']['groupe']) for q in C[1:] if q['dop']['t1'] is not None),
                        ts=[q['dop']['t1'] for q in S], tc=[q['dop']['t1'] for q in C]))
    return out
def affiche(cd, titre):
    print(titre)
    for q in cd:
        if q['sex'] + q['cex'] == 0: continue
        sp = lambda t: (f"{min(x for x in t if x is not None):.2f}-{max(x for x in t if x is not None):.2f}" if any(x is not None for x in t) else '   -   ')
        print(f"   {q['reg']} {q['stop']} P={PN[q['P']]:<4} c={q['c']:<4}: sur 8 perturbations — S sort {q['sex']}, P_any {q['sany']} | C sort {q['cex']}, P_any {q['cany']} | C seul P_any {q['fort']}({q['fortd']}) | S seul P_any {q['inv']}({q['invd']}) | "
              f"C plus tôt de 0,5 T0 : {q['tot']}({q['totd']}) ; C plus tard : {q['tard']}({q['tardd']}) ; C sort sans S : {q['cseul']} | couples déterminés {q['nd']} | exact : S {q['s0']}, C {q['c0']} | t1 S {sp(q['ts'])} C {sp(q['tc'])} | groupes S {dict(q['gs'])} C {dict(q['gc'])}")
    print(f"   => CANDIDAT FORT (C seul P_any dans >= 6 perturbations) : {sum(q['fortd'] >= 6 for q in cd)} configurations en lecture déterminée, {sum(q['fort'] >= 6 for q in cd)} en DOP853 brut ; l'inverse (S seul P_any) : {sum(q['invd'] >= 6 for q in cd)} / {sum(q['inv'] >= 6 for q in cd)}")
    print(f"   => CANDIDAT FAIBLE (C plus tôt d'au moins 0,5 T0 dans >= 6 perturbations) : {sum(q['totd'] >= 6 for q in cd)} déterminées, {sum(q['tot'] >= 6 for q in cd)} brutes ; l'inverse (C plus tard) : {sum(q['tardd'] >= 6 for q in cd)} / {sum(q['tard'] >= 6 for q in cd)} ; sur {len(cd)} configurations")
cdp = candidats('princ', ('B0', 'Bg')); affiche(cdp, '\n3. S CONTRE C, CAMPAGNE PRINCIPALE, par configuration (DOP853 brut ; entre parenthèses, couples déterminés des deux côtés)')
print('\n4. CONCENTRATION A TRAVAIL EGAL (F_U moyen jusqu\'au dernier choc commun avant toute sortie), campagne principale et modes')
for cp, regs in (('princ', ('B0', 'Bg')), ('modes', ('H3', 'X3'))):
    for reg in regs:
        up = 0; n = 0; vs = []; vc = []; vf = []
        for o in camp[cp]:
            if o['reg'] != reg or o['src'] != 'S' or o['stop'] != 'A1': continue
            if any((cp, reg, x, o['P'], o['cad'], 'A1', o['a'], o['g']) not in ix for x in 'CF'): continue
            c_ = ix[(cp, reg, 'C', o['P'], o['cad'], 'A1', o['a'], o['g'])]; f_ = ix[(cp, reg, 'F', o['P'], o['cad'], 'A1', o['a'], o['g'])]; ps = o['dop']['parchoc']; pc = c_['dop']['parchoc']; pf = f_['dop']['parchoc']; k = min(len(ps), len(pc), len(pf)) - 1
            if k < 1: continue
            n += 1; fs = ps[k][2][0] / (ps[k][0] * T0); fc = pc[k][2][0] / (pc[k][0] * T0); ff = pf[k][2][0] / (pf[k][0] * T0); up += fc > fs; vs.append(fs); vc.append(fc); vf.append(ff)
        if n: print(f"   {reg} : S {np.mean(vs):.3f}  C {np.mean(vc):.3f}  F {np.mean(vf):.3f} ; C > S dans {up}/{n}")
print('\n5. CAMPAGNE MODES INTERNES (a = 1/2, quatre couples)'); table('modes', ('H3', 'X3')); cdm = candidats('modes', ('H3', 'X3')); affiche(cdm, '   S contre C :')
print('\n6. RAYON DU CŒUR (liant nu, quatre couples, S et C)')
for a in (0.25, 0.5, 0.75):
    if a == 0.5:
        for stop in ('A1', 'A2'):
            for src in 'SC':
                v = [o for o in camp['princ'] if o['reg'] == 'B0' and o['stop'] == stop and o['src'] == src and (o['P'], o['cad']) in COUP]
                print(f"   B0 {stop} {src} a=0.5: n={len(v):<4} sorties {sum(o['dop']['t1'] is not None for o in v):<4} P_any {sum(o['dop']['Pany'] for o in v):<4}({sum(o['dop']['Pany'] and det(o) for o in v)})  indéterminés {sum(not det(o) for o in v)}")
    else: table('coeur', ('B0',), a=a, srcs='SC')
for a in (0.25, 0.75): affiche(candidats('coeur', ('B0',), a=a), f'   S contre C, a = {a} :')
affiche([q for q in cdp if q['reg'] == 'B0' and (q['P'], q['c']) in COUP], '   S contre C, a = 0.5 (mêmes quatre couples) :')
print('\n7. TEMOIN DE TRAVERSEE (cœur mou ; passage sous r = 1/2 relevé)')
v = camp['trav']
if v:
    ex = [o for o in v if o['dop']['t1'] is not None]; cont = [o for o in ex if o['dop']['tcoeur'] is not None and o['dop']['tcoeur'] < o['dop']['t1']]
    print(f"   n={len(v)} ; passage sous 1/2 : {sum(o['dop']['tcoeur'] is not None for o in v)} ; sorties : {len(ex)} ; CONTAMINEES (passage avant la première sortie) : {len(cont)} ; r minimal < 0,01 (vraie traversée) : {sum(min(o['dop']['rmin']) < 0.01 for o in v)}")
    for stop in ('A1', 'A2'):
        for src in 'SC':
            w = [o for o in v if o['stop'] == stop and o['src'] == src]; h = [o for o in camp['princ'] if o['reg'] == 'B0' and o['stop'] == stop and o['src'] == src and (o['P'], o['cad']) in COUP]
            print(f"   {stop} {src} : cœur mou P_any {sum(o['dop']['Pany'] for o in w)}/{len(w)} (déterminés {sum(o['dop']['Pany'] and det(o) for o in w)}), sorties {sum(o['dop']['t1'] is not None for o in w)} | cœur dur a=1/2 P_any {sum(o['dop']['Pany'] for o in h)}/{len(h)}, sorties {sum(o['dop']['t1'] is not None for o in h)}")
print('\n8. SENSIBILITE : dispersion de l\'instant de première sortie sur les 9 géométries, par configuration (toutes campagnes à cœur dur)')
sp = []; mixed = 0; nconf = 0
for key in sorted({(o['camp'], o['reg'], o['src'], o['P'], o['cad'], o['stop'], o['a']) for o in G if o['camp'] != 'trav'}, key=str):
    if any(key + (g,) not in ix for g in range(9)): continue
    v = [ix[key + (g,)] for g in range(9)]; t = [o['dop']['t1'] for o in v if o['dop']['t1'] is not None]
    if not t: continue
    nconf += 1; sp.append((max(t) - min(t)) if len(t) == 9 else 99.0); pa = sum(o['dop']['Pany'] for o in v); mixed += 0 < pa < 9
print(f"   {nconf} configurations avec au moins une sortie ; dispersion > 0,5 T0 (ou sortie absente dans une partie des géométries) : {sum(q > 0.5 for q in sp)} ; < 0,01 T0 : {sum(q < 0.01 for q in sp)} ; P_any ni toujours ni jamais sur les 9 géométries : {mixed}")
print('\n9. TEMOINS D\'ETIQUETAGE ET COMPARATEUR A PRECISION ACCRUE (DOP853, géométrie exacte, liant nu)')
k2 = lambda d: (d['t1'] is not None, tuple(tuple(q) for q in d['groupe']), d['Pfirst'], d['Pany'])
for cp in ('etiq', 'fin'):
    v = camp[cp]; ok = 0
    for o in v:
        nom = ix.get(('princ', 'B0', o['src'], o['P'], o['cad'], o['stop'], 0.5, 0))
        if nom is None: continue
        same = k2(o['dop']) == k2(nom['dop']); ok += same
        if not same: print(f"      {cp} {o['src']} P={PN[o['P']]} c={o['cad']} {o['stop']} {o.get('perm','')} : {o['dop']['statut']} t1={o['dop']['t1'] and round(o['dop']['t1'],3)} {o['dop']['groupe']} {o['dop']['liens']} | nominal {nom['dop']['statut']} t1={nom['dop']['t1'] and round(nom['dop']['t1'],3)} {nom['dop']['groupe']} {nom['dop']['liens']} (réf {nom['verdict_ref']})")
    print(f"   {cp} : accord avec le calcul nominal {ok}/{len(v)}")
print('\n10. DUREE :', round(sum(o['duree'] for o in R)), 's de calcul')
