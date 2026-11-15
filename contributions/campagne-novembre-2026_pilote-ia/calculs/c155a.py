#!/usr/bin/env python3
"""C-155A -- execution par Claude du protocole fige par ChatGPT (empreinte 661c3a95...babc) : croissance de C-132 bis (bras L, regle U,
temoin B apparie) sous interdit de recouvrement. Attendus : c155c_prediction.txt, partie 2 (ecrits avant).

ECARTS DECLARES AU PROTOCOLE (budget de calcul et faisabilite) :
 (0) A chaque naissance, la relaxation d'origine de C-132 est essayee d'abord ; son resultat est garde s'il est admissible (la trajectoire
     reste alors celle d'origine, au chiffre pres) ; sinon relaxation contrainte depuis l'etat d'insertion. Le resultat d'origine est
     aussi ecarte s'il laisse un volume sous 0,2 Vref, meme de 1e-9 (tolerance de son lagrangien augmente).
 (1) Les huit initialisations du protocole ne sont faites que lorsque la relaxation contrainte est necessaire.
 (2) Methode : minimisation de E + penalites quadratiques a marge sur (a) le degagement entre cellules et (b) le volume minimal, par
     L-BFGS, raideurs croissantes (1e2, 1e4, 1e6) ; l'etat final est ensuite CERTIFIE sans penalite : il n'est accepte que si tous les
     degagements sont strictement positifs et tous les volumes au-dessus de 0,2 Vref. L'energie rapportee est E seule. Un etat accepte est
     admissible ; ce n'est PAS un point KKT exact du probleme contraint (minimum approche par exces, biais de marge) : KKT = INCONCLUSIF.
 (3) Degagement signe entre deux cellules, selon leurs sommets communs : aucun -> axes separateurs des tetraedres ; un -> axes separateurs
     des deux cones de sommet commun ; deux -> separation angulaire des deux diedres autour de l'arete commune ; trois -> rien (orientation).
     Un degagement strictement positif certifie que l'intersection des deux cellules est exactement leur simplexe commun.
 (4) Controle independant : le test de recouvrement de c152c.py (axes separateurs bruts, profondeur > 1e-6), a tous les releves.
Usage : python3 c155a.py <graine> [nmax]"""
import itertools, json, math, random, sys
import numpy as np, scipy.optimize as so
from c120 import Mesh, SEEDS, vol6
from c152c import axes_separateurs
import c132_audit as c132

MARGE = 2e-4; EPSV = 0.2; MARGEV = 1e-3
EXPORT = True      # ajout du 15 novembre (C-156c) : export des coordonnees des etats acceptes ; rien d'autre n'est change
EDG = list(itertools.combinations(range(4), 2))


def _enveloppe(W, ax, tailles):
    """W (n, m, 3) : vecteurs unitaires (-rayons de A, rayons de B). Les deux cones sont separables ssi l'origine n'est pas interieure a
    l'enveloppe convexe de W. Rend : distance de l'origine a l'enveloppe (> 0) si separables, sinon la meilleure marge (< 0) sur les axes ax."""
    nrm = np.linalg.norm(ax, axis=2); ok = nrm > 1e-12
    u = ax / np.maximum(nrm, 1e-300)[:, :, None]
    pr = np.einsum('nmk,npk->nmp', u, W).min(2)
    sep = np.where(ok, pr, -np.inf).max(1)
    n, m = W.shape[:2]; d2 = (W ** 2).sum(2).min(1)                     # sous-ensembles a un point
    for t in tailles:
        for S in itertools.combinations(range(m), t):
            Ws = W[:, list(S)]; G = np.einsum('nik,njk->nij', Ws, Ws) + 1e-15 * np.eye(t)
            lam = np.linalg.solve(G, np.ones((n, t, 1)))[:, :, 0]; lam = lam / lam.sum(1, keepdims=True)
            p = np.einsum('ni,nik->nk', lam, Ws); val = (p ** 2).sum(1)
            d2 = np.where((lam >= -1e-12).all(1), np.minimum(d2, val), d2)
    return np.where(sep >= -1e-13, np.sqrt(d2), sep)


def degagement(P, kind):
    """P (n, 8, 3) : sommets de A puis de B, les sommets communs en tete des deux. kind = nombre de sommets communs (0, 1, 2)."""
    A, B = P[:, :4], P[:, 4:]
    if kind == 0:
        return -axes_separateurs(A, B)
    if kind == 1:
        RA = A[:, 1:] - A[:, :1]; RB = B[:, 1:] - A[:, :1]
        RA = RA / np.linalg.norm(RA, axis=2, keepdims=True); RB = RB / np.linalg.norm(RB, axis=2, keepdims=True)
        W = np.concatenate([-RA, RB], axis=1)
        ax = [sg * np.cross(W[:, i], W[:, j]) for i, j in itertools.combinations(range(6), 2) for sg in (1, -1)]
        return _enveloppe(W, np.stack(ax, 1), (2, 3))
    e = A[:, 1] - A[:, 0]; e = e / np.linalg.norm(e, axis=1, keepdims=True)
    def proj(Q):
        R = Q - A[:, :1]; R = R - np.einsum('npk,nk->np', R, e)[:, :, None] * e[:, None, :]
        return R / np.linalg.norm(R, axis=2, keepdims=True)
    W = np.concatenate([-proj(A[:, 2:]), proj(B[:, 2:])], axis=1)
    c = np.cross(e[:, None, :], W)
    return _enveloppe(W, np.concatenate([c, -c], axis=1), (2,))


class Tissu:
    def __init__(s, m):
        s.m = m; s.ids = sorted(m.X); s.pos = {v: i for i, v in enumerate(s.ids)}; s.TT = sorted(m.T)
        s.T = np.array([[s.pos[v] for v in t] for t in s.TT])
        ed = list(m.rest); s.I = np.array([s.pos[e[0]] for e in ed]); s.J = np.array([s.pos[e[1]] for e in ed]); s.R = np.array([m.rest[e] for e in ed])
        s.paires = {0: [], 1: [], 2: []}
        for i, j in itertools.combinations(range(len(s.TT)), 2):
            a, b = s.T[i], s.T[j]; com = [v for v in a if v in b]
            if len(com) == 3: continue
            s.paires[len(com)].append(com + [v for v in a if v not in com] + com + [v for v in b if v not in com])
        s.paires = {k: np.array(v, int).reshape(-1, 8) for k, v in s.paires.items()}

    def X0(s): return np.array([s.m.X[v] for v in s.ids])
    def volumes(s, X): a, b, c, d = (X[s.T[:, i]] for i in range(4)); return np.einsum('ij,ij->i', b - a, np.cross(c - a, d - a)) / 6
    def degagements(s, X): return {k: (degagement(X[p], k) if len(p) else np.zeros(0)) for k, p in s.paires.items()}
    def energie(s, X): L = np.linalg.norm(X[s.I] - X[s.J], axis=1); return 0.5 * ((L - s.R) ** 2).sum()

    def fonction(s, z, VR, mu):
        X = z.reshape(-1, 3); D = X[s.I] - X[s.J]; L = np.linalg.norm(D, axis=1); G = np.zeros_like(X); w = ((L - s.R) / L)[:, None] * D
        np.add.at(G, s.I, w); np.add.at(G, s.J, -w); F = 0.5 * ((L - s.R) ** 2).sum()
        a, b, c, d = (X[s.T[:, i]] for i in range(4)); V = np.einsum('ij,ij->i', b - a, np.cross(c - a, d - a)) / 6
        viol = np.maximum(0, EPSV * VR * (1 + MARGEV) - V) / VR
        if viol.any():
            F += mu * (viol ** 2).sum(); co = (-2 * mu * viol / VR / 6)[:, None]
            gb = np.cross(c - a, d - a) * co; gc = np.cross(d - a, b - a) * co; gd = np.cross(b - a, c - a) * co
            np.add.at(G, s.T[:, 1], gb); np.add.at(G, s.T[:, 2], gc); np.add.at(G, s.T[:, 3], gd); np.add.at(G, s.T[:, 0], -(gb + gc + gd))
        h = 1e-7
        for k, p in s.paires.items():
            if not len(p): continue
            cl = degagement(X[p], k); act = np.nonzero(cl < MARGE)[0]
            if not len(act): continue
            F += mu * ((MARGE - cl[act]) ** 2).sum()
            Pa = X[p[act]]                                             # (na, 8, 3)
            pert = np.repeat(Pa[:, None], 48, axis=1)                   # differences centrees sur 24 coordonnees
            for q in range(24):
                pert[:, 2 * q, q // 3, q % 3] += h; pert[:, 2 * q + 1, q // 3, q % 3] -= h
            # les sommets communs figurent deux fois (positions 0..k-1 et 4..4+k-1) : deplacer les deux copies ensemble
            for q in range(3 * k):
                pert[:, 2 * q, 4 + q // 3, q % 3] += h; pert[:, 2 * q + 1, 4 + q // 3, q % 3] -= h
            val = degagement(pert.reshape(-1, 8, 3), k).reshape(len(act), 48)
            dcl = (val[:, 0::2] - val[:, 1::2]) / (2 * h)               # (na, 24)
            coef = -2 * mu * (MARGE - cl[act])
            for q in range(24):
                if 12 <= q < 12 + 3 * k: continue                       # copie B des sommets communs : deja comptee
                np.add.at(G, (p[act][:, q // 3], q % 3), coef * dcl[:, q])
        return F, G.ravel()

    def admissible(s, X, VR):
        V = s.volumes(X); cl = s.degagements(X)
        return bool((V >= EPSV * VR).all() and all((not len(v)) or v.min() > 1e-10 for v in cl.values()))

    def relaxe(s, VR, graine, n):
        """Huit initialisations (protocole) : l'etat d'insertion et 7 perturbations admissibles (PCG64(graine*100000 + 100 n + i), amplitude RMS 0,01)."""
        base = s.X0(); essais = []
        for i in range(8):
            if i == 0: z0 = base.ravel()
            else:
                rng = np.random.Generator(np.random.PCG64(graine * 100000 + 100 * n + i)); Xp = base + 0.01 * rng.standard_normal(base.shape)
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
        if not bons:
            return None, 0.0, [{k: v for k, v in e.items() if k != 'X'} for e in essais]
        best = min(bons, key=lambda e: e['E'])
        for v in s.ids: s.m.X[v] = best['X'][s.pos[v]]
        return best['X'], best['gradient'], [{k: v for k, v in e.items() if k != 'X'} for e in essais]


def longest(m, t): return max(itertools.combinations(sorted(t), 2), key=lambda e: (round(m.length(e), 9), e))


def mesures(m, ts, VR, f0, V0):
    X = ts.X0(); V = ts.volumes(X); cl = ts.degagements(X); L = {e: m.length(e) for e in m.rest}
    q = [6 * math.sqrt(2) * v / max(L[e] for e in itertools.combinations(sorted(t), 2)) ** 3 for t, v in zip(ts.TT, V)]
    P = X[ts.T]; i, j = np.triu_indices(len(ts.TT), 1)
    brut = axes_separateurs(P[i], P[j]) if len(i) else np.zeros(0)
    f = [m.length(e) for e in itertools.combinations(range(4), 2)]
    mins = {k: (float(v.min()) if len(v) else None) for k, v in cl.items()}
    return dict(N0=len(m.X), N1=len(m.rest), N3=len(m.T), E=float(ts.energie(X)), min_V_sur_Vref=float((V / VR).min()), volume_min=float(V.min()),
                qmin=float(min(q)), q10=float(np.percentile(q, 10)), qmed=float(np.median(q)), somme_volumes=float(V.sum()), rapport_volume=float(V.sum() / V0),
                fondateurs_max=float(max(a / b for a, b in zip(f, f0))), fondateurs_moy=float(np.mean(f) / np.mean(f0)),
                degagement_min=mins, degagement_min_global=min(x for x in mins.values() if x is not None) if any(x is not None for x in mins.values()) else None,
                paires_actives=int(sum((v < 2 * MARGE).sum() for v in cl.values())), volumes_actifs=int((V < EPSV * VR * (1 + 2 * MARGEV)).sum()),
                recouvrements_controle_independant=int((brut > 1e-6).sum()), profondeur_max_controle=float(brut.max()) if len(brut) else 0.0)


def trajectoire(seed, nmax, law, replay=None):
    rng = random.Random(seed); m = Mesh(SEEDS['regulier'], 1.0, law, 'F'); Vref = {}
    f0 = [m.length(e) for e in itertools.combinations(range(4), 2)]; V0 = vol6(m.X, next(iter(m.T))) / 6
    rows = []; seq = []; statut = 'en cours'
    for n in range(1, nmax + 1):
        TT = sorted(m.T); E = m.inc()
        if replay is not None: e = replay[n - 1]
        else:
            vols = [vol6(m.X, t) for t in TT]; t = rng.choices(TT, weights=vols)[0]; steps = 0
            while True:
                e = longest(m, t); l = m.length(e); nxt = None
                for t2 in E[e]:
                    e2 = longest(m, t2)
                    if m.length(e2) > l + 1e-9: l = m.length(e2); nxt = t2
                if nxt is None or steps >= 200: break
                t = nxt; steps += 1
        deg = len(E[e]); bord = e in m._bedges(); Epre = m.energy()
        m.bisect(e, E=E); seq.append(e); Eins = m.energy()
        for t in m.T:
            if t not in Vref: Vref[t] = vol6(m.X, t) / 6
        for t in list(Vref):
            if t not in m.T: del Vref[t]
        ts = Tissu(m); VR = np.array([Vref[t] for t in ts.TT])
        avant = {v: m.X[v].copy() for v in m.X}
        gmax = 0.0; methode = 'aucune'; essais = []
        if law == 'U':
            # (l'export des etats est ajoute plus bas ; la dynamique est inchangee)
            # d'abord la relaxation D'ORIGINE de C-132 (ressorts + volume minimal) : si son resultat est admissible, c'est aussi un minimum
            # local du probleme contraint, et la trajectoire reste celle d'origine ; sinon, retour a l'etat d'insertion et relaxation contrainte.
            r0 = c132.relax(m, dict(Vref)); cl0 = ts.degagements(ts.X0()); gmax = r0['gmax']; methode = 'origine'
            if any(len(v) and v.min() <= 1e-10 for v in cl0.values()) or (ts.volumes(ts.X0()) < EPSV * VR).any():
                for v in avant: m.X[v] = avant[v].copy()
                X, gmax, essais = ts.relaxe(VR, seed, n); methode = 'contrainte'
                if X is None: methode = 'contrainte : aucun essai admissible, etat d insertion garde'
        r = mesures(m, ts, VR, f0, V0)
        r['export'] = dict(sommets=[int(v) for v in ts.ids], X=[[float(c) for c in m.X[v]] for v in ts.ids], cellules=[[int(v) for v in t] for t in ts.TT],
                           Vref=[float(x) for x in VR], fils=[[int(a), int(b)] for a, b in m.rest], repos=[float(m.rest[e_]) for e_ in m.rest])
        r.update(n=n, methode=methode, essais=essais, arete=list(e), degre_arete=deg, arete_de_bord=bool(bord), E_avant=Epre, E_insertion=Eins, gradient_penalise_max=gmax)
        admissible = (r['degagement_min_global'] is None or r['degagement_min_global'] > 1e-10) and r['min_V_sur_Vref'] >= EPSV and r['volume_min'] > 0 and r['recouvrements_controle_independant'] == 0
        r['admissible'] = bool(admissible); r['controle_energie'] = bool(r['E'] <= Eins + 1e-8)
        rows.append(r); print(law, seed, n, json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items() if k not in ('arete', 'essais', 'export')}), flush=True)
        if not admissible: statut = f'etat non admissible a la naissance {n}'; break
    else:
        statut = 'toutes les naissances admissibles'
    return rows, seq, statut


if __name__ == '__main__':
    seed = int(sys.argv[1]); nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 31
    rowsU, seq, stU = trajectoire(seed, nmax, 'U')
    rowsB, _, stB = trajectoire(seed, len(seq), 'B', replay=seq)
    json.dump(dict(graine=seed, U=dict(statut=stU, etats=rowsU), B=dict(statut=stB, etats=rowsB)), open(f'c155a_{seed}_etats.json' if EXPORT else f'c155a_{seed}.json', 'w'))
    print('STATUT', seed, 'U :', stU, '| B :', stB)
