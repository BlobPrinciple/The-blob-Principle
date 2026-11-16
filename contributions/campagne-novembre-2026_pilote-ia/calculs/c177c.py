#!/usr/bin/env python3
"""C-177c -- energie d'un tissu = somme sur les fils interieurs de l'energie de couronne ? (Claude, 16 novembre 2026). Predictions : c177c_prediction.txt (ecrites avant).
Usage : python3 c177c.py G <debut> <fin> -> c177c_G_<debut>.json ; python3 c177c.py S -> c177c_synthese.json"""
import contextlib, glob, io, itertools, json, sys
import numpy as np
import c163c
from c120 import Mesh, SEEDS
from x11_additivite import Ecour

A_TEMOIN = 0.02086


def croissance(a, b):
    out = {}
    for seed in range(a, b):
        with contextlib.redirect_stdout(io.StringIO()): rows, statut = c163c.trajectoire(seed, 16, 'A')
        m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); L = []
        for r in rows:
            E = m.inc(); e = tuple(r['fil_canonique']); m.bisect(e, m=3 + r['n'], E=E); E = m.inc(); F = {}
            for t in m.T:
                for f in itertools.combinations(sorted(t), 3): F.setdefault(f, []).append(t)
            bord = set(x for f, v in F.items() if len(v) == 1 for x in itertools.combinations(f, 2))
            L.append(dict(n=r['n'], fil=list(e), E=r['E'], methode=r['methode'], min_V=r['min_V_sur_Vref'], N=len(m.T), n_int=sorted(len(v) for x, v in E.items() if x not in bord)))
        out[seed] = dict(statut=statut, etats=L); json.dump(out, open(f'c177c_G_{a}.json', 'w')); print(seed, statut, flush=True)


def synthese():
    H = {}
    for f in sorted(glob.glob('c177c_G_*.json')): H.update(json.load(open(f)))
    ec = {n: Ecour(n) for n in range(3, 16)}; T = [t for d in H.values() for t in d['etats']]; R = [t for t in T if len(t['n_int']) >= 2]
    P = np.array([sum(ec[k] for k in t['n_int']) for t in R]); E = np.array([t['E'] for t in R]); Q = A_TEMOIN * np.array([len(t['n_int']) for t in R]); tous = [k for t in T for k in t['n_int']]
    out = dict(graines=len(H), statuts=sorted(set(d['statut'] for d in H.values())), etats=len(T), retenus=len(R), A1_correlation=float(np.corrcoef(P, E)[0, 1]), A2_pente=float((P * E).sum() / (P * P).sum()), A3_mediane_E_sur_P=float(np.median(E / P)),
               A4_ecart_relatif_median=float(np.median(np.abs(E - P) / E)), A5_ecart_relatif_median_temoin=float(np.median(np.abs(E - Q) / E)), correlation_temoin=float(np.corrcoef(Q, E)[0, 1]), A6_histogramme={k: tous.count(k) for k in sorted(set(tous))},
               quantiles_E_sur_P=[float(x) for x in np.quantile(E / P, [0.1, 0.25, 0.75, 0.9])], a_16_naissances=[[s, float(sum(ec[k] for k in d['etats'][-1]['n_int'])), d['etats'][-1]['E']] for s, d in H.items() if len(d['etats']) == 16])
    print(json.dumps(out, indent=1)); json.dump(out, open('c177c_synthese.json', 'w'), indent=1)


if __name__ == '__main__':
    croissance(int(sys.argv[2]), int(sys.argv[3])) if sys.argv[1] == 'G' else synthese()
