#!/usr/bin/env python3
"""X-1 [EXPLORATOIRE] -- Claude, 15 novembre 2026. Regime d'exploration demande par l'auteur : pas de prediction prealable, rien ici n'est acquis.
Croissance (regle U, bissection, volume >= 0,2 Vref) avec sortie des points-selles, sous plusieurs regles locales de choix du fil (liste de ChatGPT, C-165).
Le chevauchement n'est PAS corrige : il est seulement releve (premiere naissance ou il apparait).
Usage : python3 x1_regles.py <sortie.json> <nb_graines> <nb_naissances> <regle> [<regle> ...]
Regles : N0 (cellule au volume, marche vers le fil le plus long, hasard entre fils egaux), N0_sans (meme chose, sans sortie des points-selles),
         Dmin, Dmax (fil le moins / le plus entoure), Jeune, Ancien, Emin (insertion la moins couteuse), N1 (un fil au hasard dans tout le tissu)."""
import itertools, json, random, sys
import numpy as np
import c132_audit as c132
from c155a import Tissu
from c120 import Mesh, SEEDS, vol6
TOL = 1e-7


def hessien(m):
    ids = sorted(m.X); pos = {v: i for i, v in enumerate(ids)}; n = len(ids); H = np.zeros((3 * n, 3 * n))
    for (a, b), R in m.rest.items():
        d = m.X[a] - m.X[b]; L = np.linalg.norm(d); u = d / L; K = np.outer(u, u) + (1 - R / L) * (np.eye(3) - np.outer(u, u)); i, j = 3 * pos[a], 3 * pos[b]
        H[i:i + 3, i:i + 3] += K; H[j:j + 3, j:j + 3] += K; H[i:i + 3, j:j + 3] -= K; H[j:j + 3, i:i + 3] -= K
    w, V = np.linalg.eigh(H); return w, V, ids


def sortie_selle(m, Vref):
    n = 0
    for _ in range(6):
        w, V, ids = hessien(m)
        if w[0] > -1e-6: break
        E0 = m.energy(); mode = V[:, 0].reshape(-1, 3); best = None
        for sg in (1, -1):
            m2 = m.copy()
            for v, x in zip(ids, mode): m2.X[v] = m2.X[v] + sg * 0.003 * x
            c132.relax(m2, dict(Vref)); E2 = m2.energy()
            if E2 < E0 - 1e-9 and (best is None or E2 < best[0]): best = (E2, m2)
        if best is None: break
        for v in ids: m.X[v] = best[1].X[v]
        n += 1
    return n


def choisir(m, rng, regle, age):
    E = m.inc()
    if regle == 'N1': return rng.choice(sorted(E)), E
    TT = sorted(m.T); t = rng.choices(TT, weights=[vol6(m.X, x) for x in TT])[0]
    def plus_long(t):
        ar = list(itertools.combinations(sorted(t), 2)); L = {e: m.length(e) for e in ar}; lm = max(L.values()); return [e for e in ar if L[e] >= lm - TOL], lm
    for _ in range(200):
        cand, l = plus_long(t); vois = [(plus_long(t2)[1], t2) for e in cand for t2 in E[e] if t2 != t]
        if not vois: break
        l2 = max(x for x, _ in vois)
        if l2 <= l + TOL: break
        t = rng.choice(sorted(set(t2 for x, t2 in vois if x >= l2 - TOL)))
    rng.shuffle(cand)
    if regle == 'Dmin': cand.sort(key=lambda e: len(E[e]))
    elif regle == 'Dmax': cand.sort(key=lambda e: -len(E[e]))
    elif regle == 'Jeune': cand.sort(key=lambda e: -age[e])
    elif regle == 'Ancien': cand.sort(key=lambda e: age[e])
    elif regle == 'Emin': cand.sort(key=lambda e: m.dE_insert(e, E))
    return cand[0], E


def croissance(seed, nmax, regle):
    rng = random.Random(seed); m = Mesh(SEEDS['regulier'], 1.0, 'U', 'F'); Vref = {}; V0 = vol6(m.X, next(iter(m.T))) / 6
    age = {e: 0 for e in m.rest}; rows = []; premier = None
    for n in range(1, nmax + 1):
        e, E = choisir(m, rng, regle.replace('_sans', ''), age); deg = len(E[e]); m.bisect(e, E=E)
        for f in m.rest: age.setdefault(f, n)
        for f in list(age):
            if f not in m.rest: del age[f]
        c132.relax(m, Vref); w0 = float(hessien(m)[0][0]); nesc = 0 if regle.endswith('_sans') else sortie_selle(m, Vref)
        ts = Tissu(m); X = ts.X0(); VR = np.array([Vref[t] for t in ts.TT]); V = ts.volumes(X); cl = ts.degagements(X)
        dg = min((float(v.min()) for v in cl.values() if len(v)), default=1.0)
        if dg <= 1e-10 and premier is None: premier = n
        Einc = m.inc(); bord = m._bedges(); di = [len(v) for f, v in Einc.items() if f not in bord]
        rows.append(dict(n=n, E=float(m.energy()), vol=float(V.sum() / V0), N0=len(m.X), N1=len(m.rest), N3=len(m.T), deg_fil=deg, selle_avant=w0 < -1e-6, sorties=nesc, vp_min=float(hessien(m)[0][0]),
                         degagement_min=dg, min_V=float((V / VR).min()), actifs=int((V < 0.2 * VR * (1 + 1e-6)).sum()), fils_interieurs=len(di), cellules_par_fil_interieur=float(np.mean(di)) if di else None,
                         cellules_par_fil=float(np.mean([len(v) for v in Einc.values()])), Lmoy=float(np.mean([m.length(f) for f in m.rest])), Lmax=float(max(m.length(f) for f in m.rest))))
    return dict(graine=seed, regle=regle, premier_chevauchement=premier, etats=rows)


if __name__ == '__main__':
    sortie, ng, nmax, regles = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]; out = []
    for regle in regles:
        for seed in range(3000, 3000 + ng):
            r = croissance(seed, nmax, regle); out.append(r); f = r['etats'][-1]
            print(regle, seed, 'chev', r['premier_chevauchement'], 'E %.4f' % f['E'], 'vol %.2f' % f['vol'], 'N3/N0 %.3f' % (f['N3'] / f['N0']), 'c/fil int', f['cellules_par_fil_interieur'] and round(f['cellules_par_fil_interieur'], 3),
                  'selles', sum(x['selle_avant'] for x in r['etats']), 'sorties', sum(x['sorties'] for x in r['etats']), 'actifs', f['actifs'], flush=True)
            json.dump(out, open(sortie, 'w'))
