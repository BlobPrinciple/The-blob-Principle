#!/usr/bin/env python3
"""C-169c -- alternance croissance / fermeture, deux regles de reunion (Claude, 15 novembre 2026). Protocole et predictions : c169c_prediction.txt (ecrits avant).
Usage : python3 c169c.py <sortie.json> <regle> [<regle> ...]     regles : T, D0.12, D0.25, D0.5, D0.99, AUCUNE"""
import itertools, json, random, sys
from collections import Counter
import numpy as np
import c132_audit as c132
from c155a import Tissu
from c120 import Mesh, SEEDS, vol6
GRAINES = range(7000, 7004); NAISSANCES = 30


def degagement_min(m):
    ts = Tissu(m); cl = ts.degagements(ts.X0()); return min((float(v.min()) for v in cl.values() if len(v)), default=1.0), int(sum((v <= 1e-10).sum() for v in cl.values()))


def eventail(m, E, vois, a, b):
    """Critere de T : a et b non lies ont deux voisins communs u, v lies entre eux, le fil (u, v) portant exactement cinq cellules."""
    com = sorted(vois[a] & vois[b])
    return any(len(E.get(tuple(sorted((u, v))), ())) == 5 for u, v in itertools.combinations(com, 2) if tuple(sorted((u, v))) in m.rest)


def candidat(m, regle):
    ids = sorted(m.X); X = np.array([m.X[v] for v in ids]); D = np.linalg.norm(X[:, None] - X[None], axis=2); E = m.inc()
    vois = {v: set() for v in ids}
    for u, v in m.rest: vois[u].add(v); vois[v].add(u)
    r = 0.5 if regle == 'T' else float(regle[1:]); best = None
    for i, j in zip(*np.nonzero(np.triu(D < r, 1))):
        a, b = ids[i], ids[j]
        if b in vois[a]: continue
        ev = eventail(m, E, vois, a, b)
        if regle == 'T' and not ev: continue
        if best is None or D[i, j] < best[0]: best = (float(D[i, j]), a, b, ev)
    return best


def reunir(m, Vref, a, b):
    m.X[a] = (m.X[a] + m.X[b]) / 2; del m.X[b]; rest = {}
    for (u, v), r in m.rest.items():
        u2, v2 = (a if u == b else u), (a if v == b else v)
        if u2 != v2: rest[tuple(sorted((u2, v2)))] = r
    m.rest = rest; T2 = {}; perdues = 0
    for t in m.T:
        t2 = tuple(a if v == b else v for v in t)
        if len(set(t2)) < 4 or frozenset(t2) in T2: perdues += 1; continue
        T2[frozenset(t2)] = (t2, Vref[t])
    m.T = set(t for t, _ in T2.values()); Vref.clear(); Vref.update({t: v for t, v in T2.values()}); return perdues


def croissance(seed, regle):
    rng = random.Random(seed); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); Vref = {}; reunions = []; statut = 'complet'; n = 0
    for n in range(1, NAISSANCES + 1):
        E = m.inc(); cand = [e for e, v in E.items() if len(v) == 1]; rng.shuffle(cand); ok = False
        for e in cand[:60]:
            m2 = m.copy(); V2 = dict(Vref); m2.bisect(e); c132.relax(m2, V2)
            if degagement_min(m2)[0] > 1e-9: m, Vref, ok = m2, V2, True; break
        if not ok: statut = f'bloque a la naissance {n}'; n -= 1; break
        if regle != 'AUCUNE':
            for _ in range(30):
                c = candidat(m, regle)
                if c is None: break
                d, a, b, ev = c; perdues = reunir(m, Vref, a, b); c132.relax(m, Vref); reunions.append(dict(n=n, d=d, eventail=bool(ev), cellules_perdues=perdues))
    Einc = m.inc(); bord = m._bedges(); di = [len(v) for f, v in Einc.items() if f not in bord]; dg, chev = degagement_min(m)
    return dict(graine=seed, regle=regle, statut=statut, naissances=n, cellules=len(m.T), sommets=len(m.X), E=float(m.energy()), E_par_cellule=float(m.energy() / len(m.T)), reunions=len(reunions),
                hors_eventail=sum(not r['eventail'] for r in reunions), cellules_perdues=sum(r['cellules_perdues'] for r in reunions), chevauchements=chev, degagement_min=dg,
                fils_interieurs=len(di), anneaux={str(k): v for k, v in sorted(Counter(di).items())}, part_cinq=(Counter(di)[5] / len(di)) if di else None, detail=reunions)


if __name__ == '__main__':
    sortie, regles = sys.argv[1], sys.argv[2:]; out = []
    for regle in regles:
        for seed in GRAINES:
            r = croissance(seed, regle); out.append(r); json.dump(out, open(sortie, 'w'))
            print(regle, seed, r['statut'], 'naissances', r['naissances'], 'cellules', r['cellules'], 'reunions', r['reunions'], 'hors eventail', r['hors_eventail'], 'perdues', r['cellules_perdues'], 'chev', r['chevauchements'],
                  'E/cell %.5f' % r['E_par_cellule'], 'fils int', r['fils_interieurs'], 'anneaux', r['anneaux'], flush=True)
