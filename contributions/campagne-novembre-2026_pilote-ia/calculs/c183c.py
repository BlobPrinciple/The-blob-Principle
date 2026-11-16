#!/usr/bin/env python3
"""C-183c -- contre-calcul independant du C-183 de ChatGPT (Claude, 16 novembre 2026) : croissance de polycubes sur une grille cubique DONNEE, decoupee en tetraedres de Freudenthal.
Ecrit d'apres son seul PROTOCOLE FIGE ; resultats, rapport et programme de ChatGPT non lus avant le scelle. Hypotheses d'auditeur de ChatGPT, pas des lois du Blob.
Usage : python3 c183c.py <bras A|B|C> <graine>  -> c183c_<bras>_<graine>.json ;  python3 c183c.py temoins -> c183c_temoins.json"""
import itertools, json, math, sys
import numpy as np

V6 = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
OCT = list(itertools.product((0, 1), repeat=3))


def _table():
    ok = []
    for m in range(256):
        occ = [o for i, o in enumerate(OCT) if m >> i & 1]; vide = [o for i, o in enumerate(OCT) if not m >> i & 1]
        def conn(L):
            if not L: return True
            vu = {L[0]}; pile = [L[0]]; S = set(L)
            while pile:
                x = pile.pop()
                for k in range(3):
                    y = list(x); y[k] ^= 1; y = tuple(y)
                    if y in S and y not in vu: vu.add(y); pile.append(y)
            return len(vu) == len(L)
        ok.append(conn(occ) and conn(vide))
    return ok
OKV = _table()


def sommet_ok(occ, v, plus=None):
    m = 0
    for i, o in enumerate(OCT):
        c = (v[0] - 1 + o[0], v[1] - 1 + o[1], v[2] - 1 + o[2])
        if c in occ or c == plus: m |= 1 << i
    return OKV[m], m


def arete_ok(occ, base, axe, plus=None):
    """arete partant du sommet base dans la direction axe : 4 cubes autour, en cycle."""
    u, w = [k for k in range(3) if k != axe]; cyc = []
    for du, dw in ((0, 0), (-1, 0), (-1, -1), (0, -1)):
        c = list(base); c[u] += du; c[w] += dw; c = tuple(c); cyc.append(c in occ or c == plus)
    return not (cyc == [True, False, True, False] or cyc == [False, True, False, True])


def admissible(occ, c):
    for o in OCT:
        if not sommet_ok(occ, (c[0] + o[0], c[1] + o[1], c[2] + o[2]), c)[0]: return False
    for axe in range(3):
        u, w = [k for k in range(3) if k != axe]
        for du, dw in ((0, 0), (1, 0), (0, 1), (1, 1)):
            b = list(c); b[u] += du; b[w] += dw
            if not arete_ok(occ, tuple(b), axe, c): return False
    return True


def etat(occ):
    a = sum(1 for c in occ for d in V6[::2] if (c[0] + d[0], c[1] + d[1], c[2] + d[2]) in occ); n = len(occ); F = 6 * n - 2 * a
    inter = sum(1 for c in occ if all((c[0] + d[0], c[1] + d[1], c[2] + d[2]) in occ for d in V6))
    S = set((c[0] + o[0], c[1] + o[1], c[2] + o[2]) for c in occ for o in OCT); si = 0; var = True
    for v in S:
        ok, m = sommet_ok(occ, v); si += m == 255; var &= ok
        for axe in range(3): var &= arete_ok(occ, v, axe)
    return dict(n=n, a=a, F=F, c=a - n + 1, F_sur_n=F / n, cubes_interieurs=inter, sommets_interieurs=si, variete_a_bord=bool(var), Nt=6 * n, Bt=2 * F, C_dual=6 * n - F + 1)


def tetraedres(occ):
    T = []
    for c in occ:
        for p in itertools.permutations(range(3)):
            v = [c]; x = list(c)
            for k in p: x[k] += 1; v.append(tuple(x))
            T.append(tuple(v))
    return T


def controle_tetra(occ):
    T = tetraedres(occ); F = {}; E = set(); vols = []
    for t in T:
        for f in itertools.combinations(sorted(t), 3): F[f] = F.get(f, 0) + 1
        for e in itertools.combinations(sorted(t), 2): E.add(e)
        a, b, c, d = (np.array(x, float) for x in t); vols.append(abs(np.dot(b - a, np.cross(c - a, d - a))) / 6)
    L = np.array([math.dist(a, b) for a, b in E])
    return dict(Nt=len(T), faces_max_incidence=max(F.values()), Bt=sum(1 for v in F.values() if v == 1), faces_interieures=sum(1 for v in F.values() if v == 2), volume_total=float(sum(vols)), volume_min=float(min(vols)), aretes=len(E),
                aretes_unite=int((abs(L - 1) < 1e-9).sum()), aretes_rac2=int((abs(L - math.sqrt(2)) < 1e-9).sum()), aretes_rac3=int((abs(L - math.sqrt(3)) < 1e-9).sum()), E_U=float((0.5 * (L - 1) ** 2).sum()))


def croissance(bras, seed, nmax=1000, jalons=(64, 216, 512, 1000)):
    rng = np.random.Generator(np.random.PCG64(seed)); occ = {(0, 0, 0)}; cand = {}
    def maj(c):
        if c in occ: cand.pop(c, None); return
        q = sum(1 for d in V6 if (c[0] + d[0], c[1] + d[1], c[2] + d[2]) in occ)
        if q == 0: cand.pop(c, None)
        else: cand[c] = (q, admissible(occ, c))
    for d in V6: maj(d)
    out = dict(bras=bras, graine=seed, jalons=[], histogramme_q={}, tetra={}); stop = None
    while len(occ) < nmax:
        L = sorted(c for c, (q, ad) in cand.items() if ad and (bras != 'A' or q == 1))
        if bras == 'C' and L: qm = max(cand[c][0] for c in L); L = [c for c in L if cand[c][0] == qm]
        if not L: stop = len(occ); break
        c = L[int(rng.integers(len(L)))]; q = cand[c][0]; out['histogramme_q'][q] = out['histogramme_q'].get(q, 0) + 1; occ.add(c)
        for dx, dy, dz in itertools.product((-1, 0, 1), repeat=3): maj((c[0] + dx, c[1] + dy, c[2] + dz))
        if len(occ) in jalons:
            e = etat(occ); e['candidats_admissibles'] = sum(1 for q_, ad in cand.values() if ad); e['candidats_rejetes'] = sum(1 for q_, ad in cand.values() if not ad); out['jalons'].append(e)
            if len(occ) in (64, 216) or (len(occ) == 1000 and seed == 18300): out['tetra'][len(occ)] = controle_tetra(occ)
    out['stop'] = stop; out['contacts_q_ge_2'] = sum(v for k, v in out['histogramme_q'].items() if k >= 2)
    if len(out['jalons']) == 4:
        x = np.log([j['n'] for j in out['jalons']]); y = np.log([j['F'] for j in out['jalons']]); out['beta'] = float(np.polyfit(x, y, 1)[0])
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'temoins':
        out = dict(boite=[], ligne=[])
        for Lc in (4, 6, 8, 10):
            occ = set(itertools.product(range(Lc), repeat=3)); e = etat(occ); e['tetra'] = controle_tetra(occ); out['boite'].append(e)
        for n in (64, 216, 512, 1000):
            occ = set((i, 0, 0) for i in range(n)); e = etat(occ); e['tetra'] = controle_tetra(occ) if n <= 216 else None; out['ligne'].append(e)
        for k in ('boite', 'ligne'):
            out['beta_' + k] = float(np.polyfit(np.log([e['n'] for e in out[k]]), np.log([e['F'] for e in out[k]]), 1)[0]); print(k, [(e['n'], e['F'], e['c'], e['cubes_interieurs'], e['sommets_interieurs'], e['variete_a_bord']) for e in out[k]], 'beta %.4f' % out['beta_' + k])
        print('boite tetra', [(e['tetra']['Nt'], e['tetra']['Bt'], e['tetra']['faces_max_incidence'], round(e['tetra']['volume_total'], 9), round(e['tetra']['E_U'], 4)) for e in out['boite']]); json.dump(out, open('c183c_temoins.json', 'w'))
    else:
        bras, seed = sys.argv[1], int(sys.argv[2]); r = croissance(bras, seed); json.dump(r, open(f'c183c_{bras}_{seed}.json', 'w'))
        print(bras, seed, 'stop', r['stop'], 'beta %.4f' % r.get('beta', float('nan')), 'F', [j['F'] for j in r['jalons']], 'c', [j['c'] for j in r['jalons']], 'int', [j['cubes_interieurs'] for j in r['jalons']], 'som', [j['sommets_interieurs'] for j in r['jalons']],
              'var', [j['variete_a_bord'] for j in r['jalons']], 'q', dict(sorted(r['histogramme_q'].items())), 'tetra', {k: (v['Nt'], v['Bt'], v['faces_max_incidence'], round(v['volume_total'], 9)) for k, v in r['tetra'].items()}, flush=True)
