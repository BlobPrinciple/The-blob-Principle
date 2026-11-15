#!/usr/bin/env python3
"""C-172c -- certification sur etats neufs (Claude, 15 novembre 2026). Protocole et predictions : c172c_prediction.txt (ecrits avant)."""
import itertools, json, random
import numpy as np
import c132_audit as c132
from c120 import Mesh, SEEDS, vol6
from c169c import degagement_min
from c171c import anneau_isole
from x1_regles import hessien
out = dict(C=[], D=[], temoin=[])


def sauve(): json.dump(out, open('c172c.json', 'w'))


def anneaux(m):
    E = m.inc(); b = m._bedges(); return sorted(len(v) for f, v in E.items() if f not in b)


def divisions(nom, m, Vref, ring, cible):
    E = m.inc(); E0 = m.energy()
    for e in sorted(f for f, v in E.items() if len(v) == 1):
        t = E[e][0]; m2 = m.copy(); V2 = dict(Vref); m2.bisect(e); Eins = m2.energy(); c132.relax(m2, V2); dg, chev = degagement_min(m2)
        r = dict(etat=nom, fil=list(e), dans_anneau=bool(t in ring), cout_insertion=float(Eins - E0), cout_relaxe=float(m2.energy() - E0), admissible=bool(dg > 1e-9), chevauchements=chev,
                 vp_min=float(hessien(m2)[0][0]), anneaux_apres=anneaux(m2))
        cible.append(r); sauve(); print('  ', nom, e, 'anneau' if r['dans_anneau'] else 'dehors', 'insertion %.5f' % r['cout_insertion'], 'relaxe %+.9f' % r['cout_relaxe'], 'adm', r['admissible'], 'vp %.1e' % r['vp_min'], 'anneaux', r['anneaux_apres'], flush=True)


# PARTIE C
for k in (3, 4, 5, 6):
    m, V = anneau_isole(k); E = m.inc(); print('C : anneau de', k, '| E %.12f' % m.energy(), '| fils propres', sum(1 for v in E.values() if len(v) == 1), '| vp min %.1e' % hessien(m)[0][0], flush=True)
    divisions(f'C{k}', m, V, set(E[(0, 1)]), out['C'])
# PARTIE D
def colle(m, Vref, face, t):
    opp = [v for v in t if v not in face][0]; a, b, c = (m.X[v] for v in face); n = np.cross(b - a, c - a); n /= np.linalg.norm(n)
    p = m.X[opp] - 2 * np.dot(m.X[opp] - a, n) * n; w = m.nv; m.nv += 1; m.X[w] = p; t2 = tuple(face) + (w,)
    if vol6(m.X, t2) < 0: t2 = (t2[1], t2[0], t2[2], t2[3])
    m.T.add(t2); Vref[t2] = vol6(m.X, t2) / 6
    for v in face: m.rest[tuple(sorted((v, w)))] = 1.0
for seed in (9100, 9101, 9102):
    rng = random.Random(seed); m, V = anneau_isole(5); ring = set(m.T); E = m.inc()
    ext = sorted((f, t) for t in ring for f in itertools.combinations(sorted(t), 3) if not (0 in f and 1 in f)); f, t = rng.choice(ext); colle(m, V, f, t); c132.relax(m, V); nais = 0
    while nais < 15:
        E = m.inc(); cand = [e for e, v in E.items() if len(v) == 1 and v[0] not in ring]; rng.shuffle(cand); ok = False
        for e in cand:
            m2 = m.copy(); V2 = dict(V); m2.bisect(e); c132.relax(m2, V2)
            if degagement_min(m2)[0] > 1e-9: m, V, ok = m2, V2, True; break
        if not ok: break
        nais += 1
    print('D : graine', seed, '| cellules', len(m.T), '| naissances', nais, '| E %.12f' % m.energy(), '| anneaux', anneaux(m), '| vp min %.1e' % hessien(m)[0][0], flush=True)
    divisions(f'D{seed}', m, V, ring, out['D'])
# TEMOIN
rng = random.Random(9199); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); V = {}
for n in range(20):
    E = m.inc(); cand = [e for e, v in E.items() if len(v) == 1]; rng.shuffle(cand)
    for e in cand:
        m2 = m.copy(); V2 = dict(V); m2.bisect(e); c132.relax(m2, V2)
        if degagement_min(m2)[0] > 1e-9: m, V = m2, V2; break
print('TEMOIN : cellules', len(m.T), '| E %.2e' % m.energy(), '| anneaux', anneaux(m), flush=True); divisions('T', m, V, set(), out['temoin'])
