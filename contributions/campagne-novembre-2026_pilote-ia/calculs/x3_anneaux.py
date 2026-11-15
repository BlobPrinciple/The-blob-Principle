#!/usr/bin/env python3
"""X-3 [EXPLORATOIRE] -- Claude, 15 novembre 2026. Regime d'exploration : pas de prediction prealable, rien ici n'est acquis.
Fermeture des anneaux par contact dans une croissance sans tension.
1. Arbre de tetraedres reguliers par la regle << libre >> de x2 (fil propre, refus du chevauchement), N naissances.
2. Tours de fermeture : deux sommets non lies a moins de FUSION sont confondus ; deux sommets non lies a moins de RC recoivent un lien de longueur naturelle 1
   (RC = 1,15 : portee de contact de BP-S2) ; tout quadruplet de sommets mutuellement lies qui n'est pas deja une cellule devient une cellule (volume de reference =
   son volume du moment) ; relaxation (ressorts + volume minimal) ; on recommence jusqu'a ce que plus rien ne change.
Usage : python3 x3_anneaux.py <sortie.json> <nb_graines> <naissances> <RC> [<RC> ...]"""
import itertools, json, random, sys
from collections import Counter
import numpy as np
import c132_audit as c132
from c155a import Tissu
from c120 import Mesh, SEEDS, vol6
FUSION = 0.25


def arbre(seed, nmax):
    rng = random.Random(seed); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); Vref = {}
    for n in range(1, nmax + 1):
        E = m.inc(); cand = [e for e, v in E.items() if len(v) == 1]; rng.shuffle(cand); ok = False
        for e in cand[:60]:
            m2 = m.copy(); V2 = dict(Vref); m2.bisect(e); c132.relax(m2, V2)
            if m2.energy() > 1e-12: continue
            ts = Tissu(m2); cl = ts.degagements(ts.X0())
            if min((float(v.min()) for v in cl.values() if len(v)), default=1.0) > 1e-9: m, Vref, ok = m2, V2, True; break
        if not ok: break
    return m, Vref


def mesure(m, Vref):
    ts = Tissu(m); X = ts.X0(); VR = np.array([Vref[t] for t in ts.TT]); V = ts.volumes(X); cl = ts.degagements(X)
    Einc = m.inc(); bord = m._bedges(); di = [len(v) for f, v in Einc.items() if f not in bord]; c = X.mean(0); L = np.array([m.length(f) for f in m.rest])
    return dict(E=float(m.energy()), N0=len(m.X), N1=len(m.rest), N3=len(m.T), E_par_cellule=float(m.energy() / len(m.T)), volume=float(V.sum()), min_V=float((V / VR).min()),
                chevauchements=int(sum((v <= 1e-10).sum() for v in cl.values())), fils_interieurs=len(di), cellules_par_fil_interieur=float(np.mean(di)) if di else None,
                anneaux={str(k): v for k, v in sorted(Counter(di).items())}, cellules_par_fil=6 * len(m.T) / len(m.rest), fils_sans_cellule=sum(1 for f in m.rest if f not in Einc),
                rayon_giration=float(np.sqrt(((X - c) ** 2).sum(1).mean())), Lmin=float(L.min()), Lmax=float(L.max()), ecart_type_L=float(L.std()))


def fermeture(m, Vref, RC, tours=25):
    hist = []
    for tour in range(tours):
        ids = sorted(m.X); X = np.array([m.X[v] for v in ids]); D = np.linalg.norm(X[:, None] - X[None], axis=2); nf = nl = nc = 0
        lies = lambda a, b: tuple(sorted((a, b))) in m.rest
        # fusions (une a la fois, la plus proche)
        pr = [(D[i, j], ids[i], ids[j]) for i in range(len(ids)) for j in range(i + 1, len(ids)) if D[i, j] < FUSION and not lies(ids[i], ids[j])]
        if pr:
            _, a, b = min(pr); m.X[a] = (m.X[a] + m.X[b]) / 2; del m.X[b]; nf = 1
            rest = {}
            for (u, v), r in m.rest.items():
                u2, v2 = (a if u == b else u), (a if v == b else v)
                if u2 != v2: rest[tuple(sorted((u2, v2)))] = r
            m.rest = rest; T2 = set(); V2 = {}
            for t in m.T:
                t2 = tuple(a if v == b else v for v in t)
                if len(set(t2)) == 4: T2.add(t2); V2[t2] = Vref[t]
            m.T = T2; Vref.clear(); Vref.update(V2)
        else:
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    if D[i, j] <= RC and not lies(ids[i], ids[j]): m.rest[(ids[i], ids[j])] = 1.0; nl += 1
        # nouvelles cellules : quadruplets mutuellement lies
        vois = {v: set() for v in m.X}
        for u, v in m.rest: vois[u].add(v); vois[v].add(u)
        exist = set(frozenset(t) for t in m.T)
        for u, v in list(m.rest):
            com = sorted(vois[u] & vois[v])
            for w, z in itertools.combinations(com, 2):
                if z in vois[w]:
                    q = frozenset((u, v, w, z))
                    if q not in exist:
                        t = tuple(sorted(q)); vol = vol6(m.X, t)
                        if abs(vol) / 6 < 1e-3: continue
                        if vol < 0: t = (t[1], t[0], t[2], t[3])
                        m.T.add(t); Vref[t] = vol6(m.X, t) / 6; exist.add(q); nc += 1
        if nf == 0 and nl == 0 and nc == 0: break
        c132.relax(m, Vref); r = mesure(m, Vref); r.update(tour=tour + 1, fusions=nf, liens_ajoutes=nl, cellules_ajoutees=nc); hist.append(r)
    return hist


if __name__ == '__main__':
    sortie, ng, nmax, rcs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), [float(x) for x in sys.argv[4:]]; out = []
    for seed in range(5000, 5000 + ng):
        m0, V0 = arbre(seed, nmax); dep = mesure(m0, V0)
        for RC in rcs:
            m = m0.copy(); Vref = dict(V0); h = fermeture(m, Vref, RC); f = h[-1] if h else dep
            out.append(dict(graine=seed, RC=RC, naissances=nmax, depart=dep, tours=h))
            print(seed, 'RC', RC, 'arbre : cellules', dep['N3'], '| tours', len(h), 'fusions', sum(x['fusions'] for x in h), 'liens', sum(x['liens_ajoutes'] for x in h), 'cellules +', sum(x['cellules_ajoutees'] for x in h),
                  '| E %.4f' % f['E'], 'E/cell %.5f' % f['E_par_cellule'], 'N3', f['N3'], 'fils int', f['fils_interieurs'], 'c/fil int', f['cellules_par_fil_interieur'] and round(f['cellules_par_fil_interieur'], 3),
                  'anneaux', f['anneaux'], 'chev', f['chevauchements'], 'minV %.3f' % f['min_V'], 'L %.3f-%.3f' % (f['Lmin'], f['Lmax']), flush=True)
            json.dump(out, open(sortie, 'w'))
