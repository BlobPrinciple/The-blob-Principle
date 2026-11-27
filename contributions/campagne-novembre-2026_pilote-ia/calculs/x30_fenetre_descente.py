#!/usr/bin/env python3
"""X-30 (premiere partie), LA FENETRE ET LA DESCENTE. Prediction scellee : x30_fenetre_prediction.txt (SHA-256 ae760b44...4325), poussee avant ce calcul.
 tout n [sym] : palier n, toutes les boules liees a un quadruple (parent + trois voisins nes).
   U1 (T13) : pour chaque contact hors germe dont la boule ne chevauche aucun parent, <x, n> >= 6, egalite seulement pour un retourne.
   U2 (T12) : boule rationnelle : la descente s'acheve si et seulement si la boule est dans l'empilement.
   U3 (G1)  : toute boule hors de l'empilement chevauche un PARENT de l'un de ses quatre contacts.
 Avec 'sym' : parents a symetrie pres, et U3 seulement.
Chevauchement : test exact de l'outil de X-27 ; un filtre flottant n'ecarte que les cas a plus de 1e-6 du contact.      Claude, 27 novembre 2026."""
import itertools, json, sys, time
from fractions import Fraction as F
import numpy as np
import x29bis_plancher as Z
from x29_pliage import GERME_ENS, m, prod

def descente(x):
    """True : s'acheve (et y final) ; False : quitte le cone (somme <= 0, elle ne fait que decroitre) ; None : indecis."""
    y = list(x)
    for _ in range(100000):
        j = min(range(5), key=lambda i: y[i]); t = y[j]
        if t >= 0: return True, sorted(y)
        y = [(-t if i == j else y[i] + t) for i in range(5)]
        if sum(y) <= 0: return False, None
    return None, None

def partie(n, sym):
    S, tui, A = Z.palier(n); L = sorted(S); idx = {u: i for i, u in enumerate(L)}; M = np.array(L, dtype=np.int64); s = M.sum(1)
    Gm = 2 * M @ M.T - np.outer(s, s); Gx = (2 * M - s[:, None]).astype(float)
    par = [np.array(sorted(idx[a] for a in A.pl[u]), dtype=np.int64) for u in L]
    gen = {}                                                    # ancetres par generation
    def generations(u):
        if u not in gen:
            g = {}; couche = set(A.pl[u]); k = 1; vus = set()
            while couche:
                for a in couche: g.setdefault(a, k)
                vus |= couche; couche = set().union(*(A.pl[a] for a in couche)) - vus; k += 1
            gen[u] = g
        return gen[u]
    parents = [i for i, u in enumerate(L) if (not sym) or u == tuple(sorted(u))]
    t0 = time.time(); c = dict(quadruples=0, boules=0, dans_l_empilement=0, hors=0, u1_paires=0, u1_exceptions=0, u1_egalites=0, u1_egalites_non_retournees=0, u1_paires_irrationnelles=0,
                               u2_rationnelles=0, u2_irrationnelles=0, u2_acheve_et_dans=0, u2_quitte_et_hors=0, u2_exceptions=0, u2_indecis=0,
                               u3_hors=0, u3_chevauche_un_parent=0, u3_exceptions=0)
    u1_min = None; ex1 = []; ex2 = []; ex3 = []; rep = {}
    for p in parents:
        vo = [int(j) for j in np.nonzero(Gm[p] == -1)[0]]
        for q, r, t in itertools.combinations(vo, 3):
            c['quadruples'] += 1; quad = (p, q, r, t)
            for P in m.places_du_quadruple(frozenset(L[i] for i in quad)):
                c['boules'] += 1; rat = P.coords is not None
                dedans = rat and all(isinstance(v, int) for v in P.coords) and m.dans_l_empilement(P.coords)
                c['dans_l_empilement' if dedans else 'hors'] += 1
                # parents chevauches, contact par contact
                chev = {}
                for w in quad:
                    if len(par[w]) == 0: chev[w] = False; continue
                    v = Gx[par[w]] @ P.xf
                    chev[w] = bool(v.max() > -1 + 1e-6) or any(P.compare(L[int(a)]) > 0 for a in par[w][v > -1 - 1e-6])
                if not sym:
                    for w in quad:                                # U1
                        if len(par[w]) == 0 or chev[w]: continue
                        u = L[w]; n_ = tuple(2 * u[k] - sum(L[int(a)][k] for a in par[w]) for k in range(5))
                        if rat:
                            val = prod(P.coords, n_); c['u1_paires'] += 1; u1_min = val if u1_min is None else min(u1_min, val)
                            if val < 6:
                                c['u1_exceptions'] += 1
                                if len(ex1) < 3: ex1.append(dict(boule=[str(z) for z in P.coords], contact=list(u), valeur=str(val)))
                            elif val == 6:
                                c['u1_egalites'] += 1; ret = [tuple(u[k] + sum(L[int(a)][k] for a in par[w]) - 2 * L[int(b)][k] for k in range(5)) for b in par[w]]
                                if tuple(P.coords) not in ret: c['u1_egalites_non_retournees'] += 1
                        else:
                            c['u1_paires_irrationnelles'] += 1
                            if float(np.dot(Gx[w] * 0 + np.array([2 * n_[k] - sum(n_) for k in range(5)], dtype=float), P.xf)) < 6 - 1e-9: c['u1_exceptions'] += 1
                    if rat:                                       # U2
                        c['u2_rationnelles'] += 1; fin, y = descente([F(z) for z in P.coords])
                        if fin is None: c['u2_indecis'] += 1
                        elif fin and dedans and y == [0, 0, 0, 0, 1]: c['u2_acheve_et_dans'] += 1
                        elif (fin is False) and not dedans: c['u2_quitte_et_hors'] += 1
                        else:
                            c['u2_exceptions'] += 1
                            if len(ex2) < 3: ex2.append(dict(boule=[str(z) for z in P.coords], acheve=fin, dans_l_empilement=dedans, fin=[str(z) for z in y] if y else None))
                    else: c['u2_irrationnelles'] += 1
                if not dedans:                                    # U3
                    c['u3_hors'] += 1
                    if any(chev.values()): c['u3_chevauche_un_parent'] += 1
                    else:
                        c['u3_exceptions'] += 1; g = {}
                        for w in quad:
                            for a, k in generations(L[w]).items(): g[a] = min(g.get(a, 99), k)
                        ch = sorted((k, a) for a, k in g.items() if P.compare(a) > 0); kmin = ch[0][0] if ch else 0; rep[kmin] = rep.get(kmin, 0) + 1
                        if len(ex3) < 3: ex3.append(dict(parent=list(L[p]), voisins=[list(L[i]) for i in (q, r, t)], boule=[str(z) for z in P.coords] if rat else [round(float(z), 9) for z in P.xf],
                                                         ancetres_chevauches=[dict(generation=k, ancetre=list(a)) for k, a in ch[:4]]))
        m.CACHE.clear()
    print(json.dumps(dict(palier=n, constituants=len(L), parents=len(parents), a_symetrie_pres=bool(sym), **c, u1_plus_petite_valeur=str(u1_min), u1_exemples=ex1, u2_exemples=ex2,
                          u3_generation_du_plus_proche_ancetre_chevauche=dict(sorted(rep.items())), u3_exemples=ex3, duree_s=round(time.time() - t0, 1))), flush=True)

if __name__ == '__main__':
    a = sys.argv[1:]; partie(int(a[1]), len(a) > 2 and a[2] == 'sym')
