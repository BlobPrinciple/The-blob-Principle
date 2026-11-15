#!/usr/bin/env python3
"""X-7 [EXPLORATOIRE] -- Claude, 15 novembre 2026. Regime d'exploration : pas de prediction prealable, rien ici n'est acquis.
Piste de ChatGPT (C-170) : la fermeture n'interdit pas la mitose, elle en augmente le cout et pourrait la detourner.
Alternance croissance / fermeture comme c169c.py, mais la naissance choisit, parmi les fils propres dont la division est sans chevauchement (au plus 30 essayes, tires
au hasard), celui dont l'etat relaxe a l'energie la plus basse (<< moindre cout >>), au lieu du premier venu (<< hasard >>).
Fermeture : les deux bouts d'un meme eventail ouvert (aucun nombre de cellules impose), non lies, a moins de 0,25.
Usage : python3 x7_moindre_cout.py <sortie.json> <hasard|cout> <nb_graines> <naissances> [refus]
Version 1 (sans 'refus') : la reunion la plus proche est faite sans controle ; elle reunit aussi des eventails de 2 ou 3 cellules ecrases par la tension, d'ou chevauchements
et blocage (sorties *_v1). Version 2 ('refus') : une reunion n'est gardee que si l'etat relaxe est sans chevauchement."""
import itertools, json, random, sys
from collections import Counter
import numpy as np
import c132_audit as c132
from c120 import Mesh, SEEDS
from c169c import degagement_min, reunir
REFUS = len(sys.argv) > 5 and sys.argv[5] == 'refus'


def bouts(m):
    b = {}
    for (u, v), cells in m.inc().items():
        g = {}
        for t in cells:
            x, y = [w for w in t if w not in (u, v)]; g.setdefault(x, set()).add(y); g.setdefault(y, set()).add(x)
        ext = [w for w, s in g.items() if len(s) == 1]
        if len(ext) == 2 and len(g) == len(cells) + 1: b[frozenset(ext)] = len(cells)
    return b


def croissance(seed, mode, nmax):
    rng = random.Random(seed); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); Vref = {}; statut = 'complet'; reunions = []; n = 0; dans_anneau = 0; couts = []
    for n in range(1, nmax + 1):
        E = m.inc(); bord = m._bedges(); cand = [e for e, v in E.items() if len(v) == 1]; rng.shuffle(cand); essais = []
        fils_int = set(f for f in E if f not in bord)
        for e in cand[:30]:
            m2 = m.copy(); V2 = dict(Vref); m2.bisect(e); c132.relax(m2, V2)
            if degagement_min(m2)[0] > 1e-9:
                t = E[e][0]; anneau = any(tuple(sorted(f)) in fils_int for f in itertools.combinations(sorted(t), 2))      # la cellule divisee touche-t-elle un fil interieur ?
                essais.append((m2.energy(), m2, V2, anneau))
                if mode == 'hasard': break
        if not essais: statut = f'bloque a la naissance {n}'; n -= 1; break
        E0 = m.energy(); e2, m, Vref, anneau = min(essais, key=lambda x: x[0]); dans_anneau += anneau; couts.append(e2 - E0)
        for _ in range(30):
            b = bouts(m); c = [(float(np.linalg.norm(m.X[x] - m.X[y])), x, y, k) for (x, y), k in ((tuple(p), k) for p, k in b.items()) if tuple(sorted((x, y))) not in m.rest]
            c = [z for z in c if z[0] < 0.25]
            if not c: break
            if REFUS:                                   # version 2 (apres coup, declaree) : une reunion n'est gardee que si l'etat relaxe est sans chevauchement
                fait = False
                for d, x, y, k in sorted(c):
                    m2 = m.copy(); V2 = dict(Vref); reunir(m2, V2, x, y); c132.relax(m2, V2)
                    if degagement_min(m2)[0] > 1e-9: m, Vref, fait = m2, V2, True; reunions.append(dict(n=n, d=d, cellules=k)); break
                if not fait: break
            else:
                d, x, y, k = min(c); reunir(m, Vref, x, y); c132.relax(m, Vref); reunions.append(dict(n=n, d=d, cellules=k))
    Einc = m.inc(); bord = m._bedges(); di = [len(v) for f, v in Einc.items() if f not in bord]; dg, chev = degagement_min(m)
    return dict(graine=seed, mode=mode, statut=statut, naissances=n, cellules=len(m.T), E=float(m.energy()), E_par_cellule=float(m.energy() / len(m.T)), reunions=len(reunions),
                tailles_reunies=dict(Counter(str(r['cellules']) for r in reunions)), anneaux={str(k): v for k, v in sorted(Counter(di).items())}, chevauchements=chev,
                divisions_touchant_un_anneau=dans_anneau, cout_moyen_naissance=float(np.mean(couts)) if couts else None)


if __name__ == '__main__':
    sortie, mode, ng, nmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); out = []
    for seed in range(8000, 8000 + ng):
        r = croissance(seed, mode, nmax); out.append(r); json.dump(out, open(sortie, 'w'))
        print(mode, seed, r['statut'], 'naissances', r['naissances'], 'cellules', r['cellules'], 'reunions', r['reunions'], r['tailles_reunies'], 'anneaux', r['anneaux'], 'E/cell %.5f' % r['E_par_cellule'],
              'divisions touchant un anneau', r['divisions_touchant_un_anneau'], 'chev', r['chevauchements'], flush=True)
