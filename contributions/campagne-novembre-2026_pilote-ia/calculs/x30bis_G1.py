#!/usr/bin/env python3
"""X-30 (seconde partie), DEMONSTRATION DE (G1) : controles sur les paliers. Prediction scellee : x30bis_demonstration_de_G1_prediction.txt
(SHA-256 28112142...58b6), poussee avant ce calcul (commit e3fb3fc).
 V1 n  : T15 au palier n. Pour toute paire liee (p, q), T0 = la tuile contenant p et q la plus proche du germe ; ses trois autres constituants
         sont-ils tous dans T(p), ou tous dans T(q) ? Repartition des cas.
 V23 n : T16 et types au palier n. Pour chaque quadruple (p ; q, r, s), chaque boule x liee aux quatre, chaque contact c parmi q, r, s dont la
         porte vue de p n'est pas chevauchee, chaque w de F(p) autre que c : nu(x, w) >= (3/4) nu(c, w) ? Et les types (nu(q,r), nu(q,s), nu(r,s)).
 V5 n  : (C6) au palier n. Les voisins du premier constituant du germe, vus de lui et du deuxieme : points alpha/beta de Q(omega).
T(u) : tuile-porte de u (le germe pour un constituant du germe) ; F(u) = T(u) prive de u. Descente vers le germe : on retourne un constituant
dont l'autre cote a une somme de coordonnees plus petite (X-29). Comparaisons exactes : fractions, et signe exact de P + Q racine(rho).
Outils importes tels quels : x27 (places d'un quadruple), x29 (tissu, descente), x29 bis (planchers). Arithmetique d'Eisenstein : x30bis_ford.
Usage : python3 x30bis_G1.py V1 n | V23 n | V5 n        Claude, 27 novembre 2026."""
import itertools, json, math, sys, time
from fractions import Fraction as F
import numpy as np
import x29bis_plancher as Z
import x29_pliage as Y
from x29_pliage import GERME, GERME_ENS, autre, prod, m
import x30bis_ford as E

def T_de(A, u): return GERME_ENS if u in GERME_ENS else frozenset(A.pl[u] | {u})

def porte_de_paire(T, p, q):
    """A partir d'une tuile contenant p et q, la tuile contenant p et q la plus proche du germe."""
    T = set(T)
    while True:
        d = [v for v in T if v != p and v != q and sum(autre(T, v)) < sum(v)]
        if not d: return frozenset(T)
        v = min(d); T.remove(v); T.add(autre(T | {v}, v))

def tuile_contenant(A, p, q, par_paire, compte):
    """Une tuile de l'empilement contenant p et q (lies) : parmi les tuiles nees, sinon par parcours des tuiles contenant p a partir de T(p)."""
    k = (p, q) if p < q else (q, p)
    if k in par_paire: return par_paire[k]
    compte['paires_sans_tuile_nee'] += 1
    dep = T_de(A, p); vus = {dep}; couche = [dep]
    for _ in range(12):
        suiv = []
        for T in couche:
            for v in T:
                if v == p: continue
                U = (T - {v}) | {autre(T, v)}
                if U in vus: continue
                if q in U: return U
                vus.add(U); suiv.append(U)
        couche = suiv
    raise RuntimeError('aucune tuile contenant la paire %s %s' % (p, q))

def prepare(n):
    S, tui, A = Z.palier(n); L = sorted(S); idx = {u: i for i, u in enumerate(L)}; M = np.array(L, dtype=np.int64); s = M.sum(1)
    Gm = 2 * M @ M.T - np.outer(s, s); par_paire = {}
    for T in tui:
        for a, b in itertools.combinations(sorted(T), 2): par_paire.setdefault((a, b), T)
    return S, tui, A, L, idx, Gm, par_paire

def partie_V1(n):
    t0 = time.time(); S, tui, A, L, idx, Gm, par_paire = prepare(n)
    c = dict(paires_liees=0, exceptions=0, deux_dans_le_germe=0, T0_est_la_tuile_porte_de_l_un_seulement=0, T0_tuile_porte_d_aucun_des_deux=0,
             cousins_conformes=0, T0_tuile_porte_des_deux_hors_germe=0, paires_sans_tuile_nee=0, T0_non_nee=0)
    ex = []; ex_cousins = []; nes = set(S)
    I, J = np.nonzero(np.triu(Gm == -1, 1))
    for i, j in zip(I.tolist(), J.tolist()):
        p, q = L[i], L[j]; c['paires_liees'] += 1
        T0 = porte_de_paire(tuile_contenant(A, p, q, par_paire, c), p, q); abc = T0 - {p, q}; Tp, Tq = T_de(A, p), T_de(A, q)
        if not (T0 <= nes): c['T0_non_nee'] += 1
        if not (abc <= Tp or abc <= Tq):
            c['exceptions'] += 1
            if len(ex) < 3: ex.append(dict(p=list(p), q=list(q), T0=sorted(map(list, T0))))
        if p in GERME_ENS and q in GERME_ENS: c['deux_dans_le_germe'] += 1
        elif T0 == Tp and T0 == Tq: c['T0_tuile_porte_des_deux_hors_germe'] += 1
        elif T0 == Tp or T0 == Tq: c['T0_est_la_tuile_porte_de_l_un_seulement'] += 1
        else:
            c['T0_tuile_porte_d_aucun_des_deux'] += 1
            if Tp == (T0 - {q}) | {autre(T0, q)} and Tq == (T0 - {p}) | {autre(T0, p)}: c['cousins_conformes'] += 1
            if len(ex_cousins) < 2: ex_cousins.append(dict(p=list(p), q=list(q), paliers=[S[p], S[q]], T0=sorted(map(list, T0))))
    print(json.dumps(dict(partie='V1', palier=n, constituants=len(L), tuiles_nees=len(tui), **c, exemples_d_exception=ex, exemples_de_cousins=ex_cousins,
                          duree_s=round(time.time() - t0, 1))), flush=True)

def signe_produit(P, w, K):
    """Signe exact de <x, w> - K pour une place P de l'outil de X-27 (rationnelle ou non)."""
    if P.coords is not None:
        v = prod(P.coords, w) - K; return (v > 0) - (v < 0)
    return E.signe_surd(prod(P.base, w) - K, P.signe * prod(P.n, w), P.rho)

def partie_V23(n):
    t0 = time.time(); S, tui, A, L, idx, Gm, par_paire = prepare(n); N = len(L); cpt = dict(paires_sans_tuile_nee=0)
    nu_ = (1 - Gm) // 2
    # portes vues de p : pour chaque paire liee, T0 prive de p et q
    porte = {}
    I, J = np.nonzero(np.triu(Gm == -1, 1))
    for i, j in zip(I.tolist(), J.tolist()):
        p, q = L[i], L[j]; T0 = porte_de_paire(tuile_contenant(A, p, q, par_paire, cpt), p, q); porte[(i, j)] = porte[(j, i)] = (T0, tuple(sorted(T0 - {p, q})))
    Fp = [tuple(sorted(T_de(A, u) - {u})) for u in L]
    c = dict(quadruples=0, sans_boule=0, boules=0, dans_l_empilement=0, hors=0, irrationnelles=0,
             t16_triplets=0, t16_exceptions=0, t16_egalites=0, t16_egalites_hors_empilement=0, t16_triplets_hors_empilement=0, t16_triplets_irrationnels=0,
             t16_hypothese_secteur_violee=0, temoin_portes_chevauchees_triplets=0, temoin_portes_chevauchees_rapport_sous_trois_quarts=0,
             e_valeurs_2_5_6=0, v3a=0, v3b=0, v3c=0, v3d=0)
    types = {}; rapport_min = None; ex16 = []; exd = []; libres_hors = {0: 0, 1: 0, 2: 0, 3: 0}; libres_dedans = {0: 0, 1: 0, 2: 0, 3: 0}; valeurs_nu = {}
    interdits = {(1, 3, 3), (1, 4, 4), (3, 3, 4), (3, 4, 4)}
    for p in range(N):
        vo = [int(j) for j in np.nonzero(Gm[p] == -1)[0]]
        for a, b in itertools.combinations(vo, 2):
            v = int(nu_[a, b]); valeurs_nu[v] = valeurs_nu.get(v, 0) + 1
            if v in (2, 5, 6): c['e_valeurs_2_5_6'] += 1
        for q, r, t in itertools.combinations(vo, 3):
            c['quadruples'] += 1; k = (int(nu_[q, r]), int(nu_[q, t]), int(nu_[r, t])); ty = tuple(sorted(k))
            lie2 = (k[0] == 1 and k[1] == 1) or (k[0] == 1 and k[2] == 1) or (k[1] == 1 and k[2] == 1)
            Pl = m.places_du_quadruple(frozenset(L[i] for i in (p, q, r, t))); e = types.setdefault(ty, dict(quadruples=0, sans_boule=0, boules=0, dans_l_empilement=0, hors=0))
            e['quadruples'] += 1; e['boules'] += len(Pl); e['sans_boule'] += (len(Pl) == 0); c['sans_boule'] += (len(Pl) == 0)
            if ty in interdits: c['v3a'] += 1
            nd = 0
            for P in Pl:
                c['boules'] += 1; rat = P.coords is not None; c['irrationnelles'] += (not rat)
                dedans = rat and all(isinstance(v, int) for v in P.coords) and m.dans_l_empilement(P.coords); nd += dedans
                c['dans_l_empilement' if dedans else 'hors'] += 1; e['dans_l_empilement' if dedans else 'hors'] += 1
                if not dedans:
                    if ty in ((3, 3, 3), (1, 3, 4)): c['v3b'] += 1
                    if max(k) <= 5 and not lie2 and ty != (4, 4, 4):
                        c['v3d'] += 1
                        if len(exd) < 3: exd.append(dict(p=list(L[p]), voisins=[list(L[i]) for i in (q, r, t)], type=list(ty)))
                nl = 0
                for cc in (q, r, t):
                    T0, g3 = porte[(p, cc)]; libre = all(P.compare(u) <= 0 for u in g3); nl += libre
                    for w in Fp[p]:
                        if w == L[cc]: continue
                        ncw = (1 - prod(L[cc], w)) // 2; K = 1 - F(3, 2) * ncw; sg = signe_produit(P, w, K)          # nu(x,w) >= 3/4 nu(c,w)  <=>  <x,w> <= K
                        if not libre:
                            c['temoin_portes_chevauchees_triplets'] += 1; c['temoin_portes_chevauchees_rapport_sous_trois_quarts'] += (sg > 0); continue
                        c['t16_triplets'] += 1; c['t16_triplets_hors_empilement'] += (not dedans); c['t16_triplets_irrationnels'] += (not rat)
                        if any(prod(w, tuple(2 * u[i] - (sum(v[i] for v in T0) - u[i]) for i in range(5))) < 0 for u in g3): c['t16_hypothese_secteur_violee'] += 1
                        if sg == 0:
                            c['t16_egalites'] += 1; c['t16_egalites_hors_empilement'] += (not dedans)
                        if sg > 0 or (sg == 0 and not dedans):
                            c['t16_exceptions'] += 1
                            if len(ex16) < 3: ex16.append(dict(p=list(L[p]), c=list(L[cc]), w=list(w), boule=[str(z) for z in P.coords] if rat else [round(float(z), 9) for z in P.xf]))
                        if not dedans:
                            v = (1 - float(np.dot(np.array([2 * w[i] - sum(w) for i in range(5)], dtype=float), P.xf))) / 2 / ncw
                            rapport_min = v if rapport_min is None else min(rapport_min, v)
                (libres_dedans if dedans else libres_hors)[nl] += 1
            if ty == (4, 4, 4) and not (len(Pl) == 2 and nd == 1): c['v3c'] += 1
        m.CACHE.clear()
    print(json.dumps(dict(partie='V23', palier=n, constituants=N, paires_sans_tuile_nee=cpt['paires_sans_tuile_nee'], **c,
                          t16_plus_petit_rapport_hors_empilement=rapport_min, t16_exemples=ex16, v3d_exemples=exd,
                          types={str(k): v for k, v in sorted(types.items())}, type_444_present=(types.get((4, 4, 4), {}).get('quadruples', 0) > 0),
                          valeurs_de_nu_entre_voisins={str(k): v for k, v in sorted(valeurs_nu.items())},
                          boules_hors_par_nombre_de_portes_libres=libres_hors, boules_dedans_par_nombre_de_portes_libres=libres_dedans,
                          duree_s=round(time.time() - t0, 1))), flush=True)

def partie_V5(n):
    t0 = time.time(); T = Y.Tissu(3)
    for g in range(1, n + 1): T.palier(g)
    S = dict(T.spheres); p, q, e3, e4, e5 = GERME; vo = [u for u in S if prod(u, p) == -1 and u != q]
    c = dict(voisins=len(vo), exceptions=0, incoherents=0, par_norme={}); pos = {}; ex = []
    for u in vo:
        nq = F(1 - prod(q, u), 2); d3, d4, d5 = [F(1 - prod(u, e), 2) / nq for e in (e3, e4, e5)]        # carres des distances aux points 0, 1, zeta
        X = (d3 - d4 + 1) / 2; s3Y = d3 + 1 - X - d5                                                       # racine(3) * Y
        if X * X + s3Y * s3Y / 3 != d3: c['incoherents'] += 1; continue
        b = 2 * s3Y / 3; a = X + b / 2                                                                     # z = a + b omega
        D = math.lcm(a.denominator, b.denominator); num = (int(a * D), int(b * D)); g, _, _ = E.e_pgcd_etendu(num, (D, 0)); nb = F(D * D, E.e_norme(g))
        pos[u] = (a, b, nq); c['par_norme'][str(nq)] = c['par_norme'].get(str(nq), 0) + 1
        if nb != nq:
            c['exceptions'] += 1
            if len(ex) < 3: ex.append(dict(u=list(u), nu_q_u=str(nq), z=[str(a), str(b)], norme_du_denominateur_reduit=str(nb)))
    # nu(u, v) = |z_u - z_v|^2 nu(q,u) nu(q,v) pour toutes les paires : coherence du plongement
    paires = mauvaises = 0; Lv = sorted(pos)
    for u, v in itertools.combinations(Lv, 2):
        au, bu, nu_u = pos[u]; av, bv, nu_v = pos[v]; d2 = E.e_norme((au - av, bu - bv)); paires += 1
        if d2 * nu_u * nu_v != F(1 - prod(u, v), 2): mauvaises += 1
    c['par_norme'] = dict(sorted(c['par_norme'].items(), key=lambda kv: F(kv[0])))
    print(json.dumps(dict(partie='V5', palier=n, constituants=len(S), **c, exemples=ex, paires_controlees=paires, paires_incoherentes=mauvaises,
                          duree_s=round(time.time() - t0, 1))), flush=True)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'V1': partie_V1(int(a[1]))
    elif a[0] == 'V23': partie_V23(int(a[1]))
    elif a[0] == 'V5': partie_V5(int(a[1]))
