#!/usr/bin/env python3
"""X-2 [EXPLORATOIRE] -- Claude, 15 novembre 2026. Regime d'exploration : pas de prediction prealable, rien ici n'est acquis.
(a) Libre : croissance sans tension (on ne coupe que des fils propres a une cellule) ET sans chevauchement (on essaie les fils propres au hasard, on garde le premier
    dont l'etat relaxe est d'energie nulle et sans chevauchement). Jusqu'ou va-t-elle, et quelle forme prend le tissu ?
(b) Melange p : avec probabilite p un fil propre de la cellule tiree, sinon la regle N0 de x1_regles.py.
(c) D57 : dans la cellule tiree, le fil dont le nombre de cellules autour est le plus proche de 5,7 (a egalite, le plus long).
Usage : python3 x2_tension_nulle.py <sortie.json> <nb_graines> <nb_naissances> <regle> [...]   regles : Libre, Mel0.25, Mel0.5, Mel0.75, Mel0.9, D57"""
import itertools, json, random, sys
import numpy as np
import c132_audit as c132
from c155a import Tissu
from c120 import Mesh, SEEDS, vol6
from x1_regles import hessien, sortie_selle, choisir


def etat(m, Vref, V0):
    ts = Tissu(m); X = ts.X0(); VR = np.array([Vref[t] for t in ts.TT]); V = ts.volumes(X); cl = ts.degagements(X)
    dg = min((float(v.min()) for v in cl.values() if len(v)), default=1.0); proches = int(sum((v < 0.05).sum() for v in cl.values()))
    Einc = m.inc(); bord = m._bedges(); di = [len(v) for f, v in Einc.items() if f not in bord]; c = X.mean(0)
    return dict(E=float(m.energy()), vol=float(V.sum() / V0), N0=len(m.X), N1=len(m.rest), N3=len(m.T), degagement_min=dg, paires_proches=proches, min_V=float((V / VR).min()),
                cellules_par_fil=6 * len(m.T) / len(m.rest), fils_interieurs=len(di), cellules_par_fil_interieur=float(np.mean(di)) if di else None,
                rayon_giration=float(np.sqrt(((X - c) ** 2).sum(1).mean())), etendue=float(np.linalg.norm(X - c, axis=1).max()), Lmoy=float(np.mean([m.length(f) for f in m.rest])))


def croissance(seed, nmax, regle):
    rng = random.Random(seed); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); Vref = {}; V0 = vol6(m.X, next(iter(m.T))) / 6; rows = []; premier = None; statut = 'complet'; age = {e: 0 for e in m.rest}
    for n in range(1, nmax + 1):
        if regle == 'Libre':
            E = m.inc(); cand = [e for e, v in E.items() if len(v) == 1]; rng.shuffle(cand); ok = False; essais = 0
            for e in cand[:40]:
                essais += 1; m2 = m.copy(); V2 = dict(Vref); m2.bisect(e); c132.relax(m2, V2)
                if m2.energy() > 1e-12: continue
                ts = Tissu(m2); cl = ts.degagements(ts.X0())
                if min((float(v.min()) for v in cl.values() if len(v)), default=1.0) > 1e-9: m, Vref, ok = m2, V2, True; break
            if not ok: statut = f'bloque a la naissance {n} ({len(cand)} fils propres, {essais} essayes)'; break
            r = etat(m, Vref, V0); r.update(n=n, essais=essais, fils_propres=len(cand))
        else:
            E = m.inc()
            if regle.startswith('Mel'):
                p = float(regle[3:]); TT = sorted(m.T); t = rng.choices(TT, weights=[vol6(m.X, x) for x in TT])[0]
                pr = [e for e in itertools.combinations(sorted(t), 2) if len(E[e]) == 1]
                e = rng.choice(pr) if (pr and rng.random() < p) else choisir(m, rng, 'N0', age)[0]
            else:
                TT = sorted(m.T); t = rng.choices(TT, weights=[vol6(m.X, x) for x in TT])[0]
                e = min(itertools.combinations(sorted(t), 2), key=lambda f: (abs(len(E[f]) - 5.7), -m.length(f), rng.random()))
            deg = len(E[e]); m.bisect(e, E=E)
            for f in m.rest: age.setdefault(f, n)
            c132.relax(m, Vref); nesc = sortie_selle(m, Vref); r = etat(m, Vref, V0); r.update(n=n, deg_fil=deg, sorties=nesc)
            if r['degagement_min'] <= 1e-10 and premier is None: premier = n
        rows.append(r)
    return dict(graine=seed, regle=regle, statut=statut, premier_chevauchement=premier, etats=rows)


if __name__ == '__main__':
    sortie, ng, nmax, regles = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]; out = []
    for regle in regles:
        for seed in range(4000, 4000 + ng):
            r = croissance(seed, nmax, regle); out.append(r); f = r['etats'][-1]
            print(regle, seed, r['statut'], 'n', f['n'], 'chev', r['premier_chevauchement'], 'E %.4f' % f['E'], 'E/cell %.4f' % (f['E'] / f['N3']), 'vol %.2f' % f['vol'], 'c/fil %.3f' % f['cellules_par_fil'],
                  'c/fil int', f['cellules_par_fil_interieur'] and round(f['cellules_par_fil_interieur'], 3), 'Rg %.3f' % f['rayon_giration'], 'etendue %.2f' % f['etendue'], 'proches', f['paires_proches'], flush=True)
            json.dump(out, open(sortie, 'w'))
