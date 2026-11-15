#!/usr/bin/env python3
"""C-164c -- test de la donnee de l'auteur << L'autonomie, je pense >> (Claude, 15 novembre 2026). Predictions : c164c_prediction.txt (ecrites avant).
Usage : python3 c164c.py H <debut> <fin>   branche horloges autonomes, graines debut..fin-1, 10 naissances -> c164c_H_<debut>.json (archives ensuite en .json.gz ; les decompresser pour la synthese)
        python3 c164c.py E                 branche << tous ensemble >> (decoupe rouge ; six bissections a la suite, 720 ordres) -> c164c_E.json
        python3 c164c.py S                 synthese -> c164c_synthese.json"""
import contextlib, glob, io, itertools, json, sys
import numpy as np
import c163c, c132_audit as c132
from c155a import Tissu, EPSV
from c120 import Mesh, SEEDS, vol6

NB = 10


def signature(X):
    X = np.asarray(X); i, j = np.triu_indices(len(X), 1); return np.sort(np.linalg.norm(X[i] - X[j], axis=1))


def classe(sig, liste, tol=1e-5):
    for k, s in enumerate(liste):
        if len(s) == len(sig) and np.abs(np.asarray(s) - sig).max() < tol: return k
    liste.append([float(x) for x in sig]); return len(liste) - 1


def branche_H(a, b):
    out = {}
    for seed in range(a, b):
        with contextlib.redirect_stdout(io.StringIO()):
            rows, statut = c163c.trajectoire(seed, NB, 'A')
        out[seed] = dict(statut=statut, etats=[dict(n=r['n'], E=r['E'], vol=r['rapport_volume'], fil=r['fil_canonique'], methode=r['methode'], egalites=r['egalites'], adm=r['admissible'],
                                                    sig=[float(x) for x in signature(list(r['positions'].values()))]) for r in rows])
        json.dump(out, open(f'c164c_H_{a}.json', 'w')); print('H', seed, statut, ['%.6f' % r['E'] for r in rows], flush=True)


AR = list(itertools.combinations(range(4), 2))


def forme(m, mid):
    """Triangulation en etiquettes independantes des numeros : fondateur i -> ('v', i) ; milieu -> ('m', paire)."""
    lab = {i: ('v', i) for i in range(4)}; lab.update({v: ('m', e) for e, v in mid.items()})
    return frozenset(frozenset(lab[v] for v in t) for t in m.T)


def transporte(F, p):
    def g(x): return ('v', p[x[1]]) if x[0] == 'v' else ('m', tuple(sorted((p[x[1][0]], p[x[1][1]]))))
    return frozenset(frozenset(g(x) for x in t) for t in F)


def canon(F):
    imgs = [transporte(F, p) for p in itertools.permutations(range(4))]
    cle = lambda G: sorted(sorted(map(str, t)) for t in G)
    return min(imgs, key=cle), sum(G == F for G in imgs)


def rouge(diag):
    m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); mid = {e: 4 + k for k, e in enumerate(AR)}
    for e, v in mid.items(): m.X[v] = (m.X[e[0]] + m.X[e[1]]) / 2
    M = lambda a, b: mid[tuple(sorted((a, b)))]
    T = [(a, *[M(a, b) for b in range(4) if b != a]) for a in range(4)]
    a, b = diag; c, d = [x for x in range(4) if x not in diag]; cyc = [M(a, c), M(b, c), M(b, d), M(a, d)]
    T += [(M(a, b), M(c, d), cyc[i], cyc[(i + 1) % 4]) for i in range(4)]
    m.T = set(t if vol6(m.X, t) > 0 else (t[1], t[0], t[2], t[3]) for t in T); m.nv = 10
    m.rest = {e: 1.0 for t in m.T for e in itertools.combinations(sorted(t), 2)}
    return m, mid


def suite(ordre):
    m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); mid = {}
    for e in ordre: mid[e] = m.bisect(e)
    return m, mid


def detend(m):
    Vref = {}; r0 = c132.relax(m, Vref); ts = Tissu(m); VR = np.array([Vref[t] for t in ts.TT]); methode = 'origine'
    cl = ts.degagements(ts.X0())
    if any(len(v) and v.min() <= 1e-10 for v in cl.values()) or (ts.volumes(ts.X0()) < EPSV * VR).any():
        m2 = None; methode = 'contrainte'
        X, g, essais = ts.relaxe(VR, 0, 0)
        if X is None: methode = 'aucun essai admissible'
    X = ts.X0(); cl = ts.degagements(X); V = ts.volumes(X)
    return dict(E=float(ts.energie(X)), methode=methode, admissible=bool(ts.admissible(X, VR)), min_V_sur_Vref=float((V / VR).min()), degagement_min=float(min(v.min() for v in cl.values() if len(v))),
                somme_volumes=float(V.sum()), N3=len(ts.TT), N1=len(m.rest), sig=[float(x) for x in signature(X)])


def branche_E():
    out = dict(rouge=[], suite=[]); V0 = None
    for diag in [(0, 1), (0, 2), (0, 3)]:
        m, mid = rouge(diag); F, sym = canon(forme(m, mid)); sig0 = signature(np.array([m.X[v] for v in sorted(m.X)]))
        if V0 is None: V0 = sum(vol6(m.X, t) for t in m.T) / 6
        r = detend(m); r.update(diagonale=list(diag), symetries=sym, forme=str(sorted(sorted(map(str, t)) for t in F))); out['rouge'].append(r)
        print('rouge', diag, 'symetries', sym, 'E %.9f' % r['E'], r['methode'], r['admissible'], 'vol x%.4f' % (r['somme_volumes'] / V0), flush=True)
    formes = {}
    for ordre in itertools.permutations(AR):
        m, mid = suite(ordre); F, sym = canon(forme(m, mid)); k = str(sorted(sorted(map(str, t)) for t in F))
        if k not in formes: formes[k] = dict(ordres=0, symetries=sym, exemple=[list(e) for e in ordre], N3=len(m.T))
        formes[k]['ordres'] += 1
    rk = set(r['forme'] for r in out['rouge'])
    for k, d in formes.items():
        m, mid = suite([tuple(e) for e in d['exemple']]); r = detend(m); r.update(d); r['est_rouge'] = k in rk; out['suite'].append(r)
        print('suite', d['exemple'], 'ordres', d['ordres'], 'symetries', d['symetries'], 'cellules', d['N3'], 'E %.9f' % r['E'], r['methode'], r['admissible'], 'vol x%.4f' % (r['somme_volumes'] / V0), 'rouge' if r['est_rouge'] else '', flush=True)
    out['V0'] = V0; json.dump(out, open('c164c_E.json', 'w'))


def synthese():
    H = {}
    for f in sorted(glob.glob('c164c_H_*.json')): H.update(json.load(open(f)))
    out = dict(graines=len(H), par_naissance={})
    cl = {n: [] for n in range(1, NB + 1)}; rep = {n: {} for n in range(1, NB + 1)}
    for seed, d in H.items():
        for r in d['etats']:
            k = classe(np.array(r['sig']), cl[r['n']]); rep[r['n']].setdefault(k, []).append((r['E'], r['vol'], r['adm'], max(r['egalites'])))
    for n in range(1, NB + 1):
        out['par_naissance'][n] = dict(graines=sum(len(v) for v in rep[n].values()), classes=len(cl[n]), effectifs=sorted((len(v) for v in rep[n].values()), reverse=True)[:8],
                                       E_min=min(x[0] for v in rep[n].values() for x in v), E_max=max(x[0] for v in rep[n].values() for x in v), vol_moy=float(np.mean([x[1] for v in rep[n].values() for x in v])),
                                       non_admissibles=sum(not x[2] for v in rep[n].values() for x in v), naissances_avec_egalite=sum(x[3] > 1 for v in rep[n].values() for x in v))
        print('H naissance', n, json.dumps(out['par_naissance'][n]))
    E = json.load(open('c164c_E.json')); out['E'] = []
    cE = []
    for genre in ('rouge', 'suite'):
        for r in E[genre]:
            k = classe(np.array(r['sig']), cE); dansH = any(len(s) == len(r['sig']) and np.abs(np.array(s) - np.array(r['sig'])).max() < 1e-5 for s in cl[6])
            d = dict(genre=genre, classe_E=k, E=r['E'], methode=r['methode'], admissible=r['admissible'], volume=r['somme_volumes'] / E['V0'], symetries=r['symetries'], cellules=r['N3'], ordres=r.get('ordres'), dans_les_classes_H_a_6=dansH)
            out['E'].append(d); print('E', json.dumps(d))
    json.dump(out, open('c164c_synthese.json', 'w'), indent=1)


if __name__ == '__main__':
    if sys.argv[1] == 'H': branche_H(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == 'E': branche_E()
    else: synthese()
