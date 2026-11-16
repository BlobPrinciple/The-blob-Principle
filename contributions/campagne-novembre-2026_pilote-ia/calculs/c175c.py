#!/usr/bin/env python3
"""C-175c -- topologie de la croissance canonique : chaine ou tissu ? (Claude, 16 novembre 2026). Predictions : c175c_prediction.txt (ecrites avant).
Usage : python3 c175c.py G <debut> <fin> -> c175c_G_<debut>.json ; python3 c175c.py S -> c175c_synthese.json"""
import contextlib, glob, io, itertools, json, sys
import numpy as np
import c163c
from c120 import Mesh, SEEDS

NB = 16


def topo(m):
    F = {}
    for t in m.T:
        for f in itertools.combinations(sorted(t), 3): F.setdefault(f, []).append(t)
    B = sum(len(v) == 1 for v in F.values()); N = len(m.T); C = (len(F) - B) - N + 1; E = m.inc(); bord = set(e for f, v in F.items() if len(v) == 1 for e in itertools.combinations(f, 2))
    return dict(N=N, B=B, C=C, fils_interieurs=len(set(E) - bord), identite=bool(B == 2 * N + 2 - 2 * C))


def croissance(a, b):
    out = {}
    for seed in range(a, b):
        with contextlib.redirect_stdout(io.StringIO()): rows, statut = c163c.trajectoire(seed, NB, 'A')
        m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); L = []
        for r in rows:
            E = m.inc(); e = tuple(r['fil_canonique']); k = len(E[e]); m.bisect(e, m=3 + r['n'], E=E); t = topo(m); t.update(n=r['n'], cellules_du_fil=k, E=r['E'], vol=r['rapport_volume']); L.append(t)
        out[seed] = dict(statut=statut, etats=L); json.dump(out, open(f'c175c_G_{a}.json', 'w')); print(seed, statut, [(t['N'], t['B'], t['C']) for t in L], flush=True)


def synthese():
    H = {}
    for f in sorted(glob.glob('c175c_G_*.json')): H.update(json.load(open(f)))
    out = dict(graines=len(H), statuts={s: d['statut'] for s, d in H.items()}, par_graine={}, par_naissance={})
    for s, d in H.items():
        L = d['etats']; f = L[-1]; out['par_graine'][s] = dict(naissances=len(L), N=f['N'], B=f['B'], C=f['C'], C_sur_N=f['C'] / f['N'], B_sur_N=f['B'] / f['N'], fils_interieurs=f['fils_interieurs'], partages=sum(t['cellules_du_fil'] > 1 for t in L),
                                                               premier_cycle=min((t['n'] for t in L if t['C'] > 0), default=None), identite=all(t['identite'] for t in L), vol=f['vol'])
    for n in range(1, NB + 1):
        S = [d['etats'][n - 1] for d in H.values() if len(d['etats']) >= n]
        if S: out['par_naissance'][n] = dict(graines=len(S), C_sur_N=float(np.mean([t['C'] / t['N'] for t in S])), B_sur_N=float(np.mean([t['B'] / t['N'] for t in S])), N=float(np.mean([t['N'] for t in S])), part_fil_partage=float(np.mean([t['cellules_du_fil'] > 1 for t in S])))
    tot = [t for d in H.values() for t in d['etats']]; out['part_fil_partage_totale'] = float(np.mean([t['cellules_du_fil'] > 1 for t in tot]))
    print(json.dumps(out, indent=1)); json.dump(out, open('c175c_synthese.json', 'w'), indent=1)


if __name__ == '__main__':
    croissance(int(sys.argv[2]), int(sys.argv[3])) if sys.argv[1] == 'G' else synthese()
