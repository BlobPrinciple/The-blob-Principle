#!/usr/bin/env python3
"""C-163c bis -- c163c.py avec deux seuils corriges (voir c163c_bis_prediction.txt) : tolerance declaree 1e-7 sur le volume minimal pour garder la
relaxation d'origine et pour l'admissibilite ; egalite de longueurs a 1e-7 ; quasi-egalites (ecart < 1e-5) signalees ; etats ecrits a chaque naissance.
C-163c -- tirage independant des numeros (Claude, 15 novembre 2026).
Croissance de c155a.py (regle U, interdit de chevauchement), ou le choix de la cellule et du fil ne depend plus de l'ordre des numeros :
course d'exponentielles (argmin Z_T / V_T), marques tirees d'une empreinte des sommets CANONIQUES ; egalites departagees par marque.
Usage : python3 c163c_bis.py <graine> <nmax> <A|B|C|B2>
 A : numeros d'origine.  B : fondateurs permutes, nouveaux sommets en descendant depuis 999, marques transportees.
 B2 : comme B avec une permutation impaire des fondateurs.  C : comme B, marques NON transportees (temoin negatif)."""
import hashlib, itertools, json, math, sys
import numpy as np, scipy.optimize as so
import c155a
from c155a import Tissu, mesures, EPSV
from c120 import Mesh, SEEDS, vol6
import c132_audit as c132

TOL = 1e-7; TOLV = 1e-7; QUASI = 1e-5


def marque(seed, n, genre, cles):
    h = hashlib.sha256(f"C163C|{seed}|{n}|{genre}|{','.join(map(str, sorted(cles)))}".encode()).hexdigest()
    return -math.log((int(h[:13], 16) + 0.5) / 16 ** 13)


class TissuCov(Tissu):
    def relaxe(s, VR, graine, n):
        """Comme c155a.Tissu.relaxe ; les perturbations sont tirees dans l'ordre des numeros canoniques."""
        base = s.X0(); essais = []
        rang = {v: r for r, v in enumerate(sorted(s.ids, key=lambda v: s.canon[v]))}; ordre = np.array([rang[v] for v in s.ids])
        for i in range(8):
            if i == 0: z0 = base.ravel()
            else:
                rng = np.random.Generator(np.random.PCG64(graine * 100000 + 100 * n + i)); Xp = base + 0.01 * rng.standard_normal(base.shape)[ordre]
                if not s.admissible(Xp, VR): essais.append(dict(i=i, statut='perturbation non admissible')); continue
                z0 = Xp.ravel()
            z = z0
            for mu in (1e2, 1e4, 1e6):
                r = so.minimize(s.fonction, z, args=(VR, mu), jac=True, method='L-BFGS-B', options=dict(gtol=1e-9, ftol=1e-15, maxiter=4000, maxfun=20000, maxcor=30)); z = r.x
            for _ in range(12):
                if np.abs(r.jac).max() < 1e-6: break
                r = so.minimize(s.fonction, z, args=(VR, 1e6), jac=True, method='L-BFGS-B', options=dict(gtol=1e-10, ftol=1e-16, maxiter=6000, maxfun=30000, maxcor=40)); z = r.x
            X = z.reshape(-1, 3); ok = s.admissible(X, VR)
            essais.append(dict(i=i, statut='admissible' if ok else 'non admissible', E=float(s.energie(X)), gradient=float(np.abs(r.jac).max()), X=X))
        bons = [e for e in essais if e['statut'] == 'admissible']
        if not bons: return None, 0.0, [{k: v for k, v in e.items() if k != 'X'} for e in essais]
        best = min(bons, key=lambda e: e['E'])
        for v in s.ids: s.m.X[v] = best['X'][s.pos[v]]
        return best['X'], best['gradient'], [{k: v for k, v in e.items() if k != 'X'} for e in essais]


def trajectoire(seed, nmax, mode):
    perm = {'A': (0, 1, 2, 3), 'B': (3, 0, 1, 2), 'C': (3, 0, 1, 2), 'B2': (1, 0, 3, 2)}[mode]        # numero local i <- sommet canonique perm[i]
    m = Mesh([SEEDS['regulier'][perm[i]] for i in range(4)], 1.0, 'U', 'F')
    canon = {i: perm[i] for i in range(4)}                    # numero local -> numero canonique
    cle = (lambda v: canon[v]) if mode != 'C' else (lambda v: v)
    Vref = {}; f0 = [m.length(e) for e in itertools.combinations(range(4), 2)]; V0 = vol6(m.X, next(iter(m.T))) / 6
    rows = []; statut = 'en cours'
    for n in range(1, nmax + 1):
        E = m.inc(); TT = list(m.T)
        mc = {t: marque(seed, n, 'T', [cle(v) for v in t]) for t in TT}
        me = {e: marque(seed, n, 'F', [cle(v) for v in e]) for e in E}
        def plus_long(t):
            ar = list(itertools.combinations(sorted(t), 2)); L = {e: m.length(e) for e in ar}; lmax = max(L.values())
            ex = [e for e in ar if L[e] >= lmax - TOL]; reste = [L[e] for e in ar if L[e] < lmax - TOL]
            return min(ex, key=lambda e: me[e]), lmax, len(ex), (lmax - max(reste)) if reste else None
        score = {t: mc[t] / (vol6(m.X, t) / 6) for t in TT}; ordre = sorted(TT, key=lambda t: score[t]); t = ordre[0]
        marge_cellule = (score[ordre[1]] / score[ordre[0]]) if len(ordre) > 1 else None
        steps = 0; egal = []; ecart = []
        while True:
            e, l, ne, gap = plus_long(t); egal.append(ne); ecart.append(gap)
            vois = [(plus_long(t2)[1], t2) for t2 in E[e] if t2 != t]
            if not vois or steps >= 200: break
            l2 = max(x for x, _ in vois)
            if l2 <= l + TOL: break
            t = min((t2 for x, t2 in vois if x >= l2 - TOL), key=lambda t2: mc[t2]); steps += 1
        deg = len(E[e]); Epre = m.energy()
        nouveau = (3 + n) if mode == 'A' else (1000 - n)
        m.bisect(e, m=nouveau, E=E); canon[nouveau] = 3 + n; Eins = m.energy()
        for t_ in m.T:
            if t_ not in Vref: Vref[t_] = vol6(m.X, t_) / 6
        for t_ in list(Vref):
            if t_ not in m.T: del Vref[t_]
        ts = TissuCov(m); ts.canon = dict(canon); VR = np.array([Vref[t_] for t_ in ts.TT])
        avant = {v: m.X[v].copy() for v in m.X}
        r0 = c132.relax(m, dict(Vref)); cl0 = ts.degagements(ts.X0()); gmax = r0['gmax']; methode = 'origine'; essais = []
        if any(len(v) and v.min() <= 1e-10 for v in cl0.values()) or (ts.volumes(ts.X0()) < EPSV * VR * (1 - TOLV)).any():
            for v in avant: m.X[v] = avant[v].copy()
            X, gmax, essais = ts.relaxe(VR, seed, n); methode = 'contrainte'
            if X is None: methode = 'contrainte : aucun essai admissible, etat d insertion garde'
        r = mesures(m, ts, VR, f0, V0)
        r.update(n=n, methode=methode, essais=essais, fil_canonique=sorted(canon[v] for v in e), degre_arete=deg, E_avant=Epre, E_insertion=Eins, gradient_max=gmax,
                 marge_cellule=marge_cellule, pas_de_marche=steps, egalites=egal, ecart_au_suivant=ecart,
                 positions={str(canon[v]): [float(c) for c in m.X[v]] for v in m.X})
        adm = (r['degagement_min_global'] is None or r['degagement_min_global'] > 1e-10) and r['min_V_sur_Vref'] >= EPSV * (1 - TOLV) and r['volume_min'] > 0 and r['recouvrements_controle_independant'] == 0
        r['admissible'] = bool(adm); r['quasi_egalite'] = bool(any(x is not None and x < QUASI for x in ecart)); rows.append(r)
        json.dump(dict(graine=seed, mode=mode, statut='en cours', etats=rows), open(f'c163c_bis_{seed}_{mode}.json', 'w'))
        print(mode, seed, n, r['fil_canonique'], 'deg', deg, methode, 'E %.9f' % r['E'], 'vol %.4f' % r['rapport_volume'], 'egal', egal, 'ecart', ['%.2e' % x if x is not None else None for x in ecart],
              'marge %.3f' % marge_cellule if marge_cellule else '', 'adm', adm, 'QUASI' if r['quasi_egalite'] else '', flush=True)
        if not adm: statut = f'etat non admissible a la naissance {n}'; break
    else: statut = 'toutes les naissances admissibles'
    return rows, statut


if __name__ == '__main__':
    seed, nmax, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rows, statut = trajectoire(seed, nmax, mode)
    json.dump(dict(graine=seed, mode=mode, statut=statut, etats=rows), open(f'c163c_bis_{seed}_{mode}.json', 'w'))
    print('STATUT', seed, mode, statut)
