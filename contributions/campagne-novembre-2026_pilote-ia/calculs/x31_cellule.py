#!/usr/bin/env python3
"""X-31, LA PLACE EST LE COTE D'UNE CELLULE NEE ; LIEN AVEC LA DIVISION DE L'ARETE (rang 3).
Prediction scellee : x31_cellule_et_arete_prediction.txt (SHA-256 d0bf1d15...912efc), poussee avant ce calcul (commit 7f8c283).
 A1 n      : regle a la lettre, tissu S(n). Pour tout p ne et tout x de S(n+2) hors de S(n) lie a p : T20 (parent ou cousin).
 A2 a b    : tissus clos par plancher tires au hasard (tirage de R4 de X-29 bis, graines a..b) : T20 ; places = cotes non nes des cellules
             nees ; aucune cellule nee sans cote ne ; places dont le plancher n'est pas ne en entier.
 A3 n      : regle a la lettre, tissu S(n) : cellules nees sans cote ne ; le cote ne est-il du cote du germe ?
 B n       : B2 a B5 sur le palier n (6) : voisins communs des fils, liens entre constituants du meme palier, voisins d'un constituant du germe.
Outils du laboratoire : paliers et planchers (x29bis_plancher), places exactes (x29_pliage, x27). La tuile de la paire (p, x) est obtenue par
descente a partir d'une tuile contenant les deux, cherchee parmi T(x), T(p) et leurs voisines ; a defaut par parcours.   Claude, 27 novembre 2026."""
import itertools, json, random, sys, time
import numpy as np
import x29bis_plancher as Z
import x29_pliage as Y
from x29_pliage import GERME, GERME_ENS, autre

def T_de(A, u): return GERME_ENS if u in GERME_ENS else frozenset(A.pl[u] | {u})

def porte_de_paire(T, p, q):
    """A partir d'une tuile contenant p et q, la tuile contenant p et q la plus proche du germe."""
    T = set(T)
    while True:
        d = [v for v in T if v != p and v != q and sum(autre(T, v)) < sum(v)]
        if not d: return frozenset(T)
        v = min(d); T.remove(v); T.add(autre(T | {v}, v))

def tuile_des_deux(A, p, x, compte):
    """Une tuile de l'empilement contenant p et x (lies)."""
    Tp, Tx = T_de(A, p), T_de(A, x)
    if p in Tx: return Tx
    if x in Tp: return Tp
    for T, u, w in ((Tx, x, p), (Tp, p, x)):
        for v in T:
            if v == u: continue
            U = (T - {v}) | {autre(T, v)}
            if w in U: return U
    compte['tuile_cherchee_par_parcours'] += 1
    vus = {Tx}; couche = [Tx]
    for _ in range(8):
        suiv = []
        for T in couche:
            for v in T:
                if v == x: continue
                U = (T - {v}) | {autre(T, v)}
                if U in vus: continue
                if p in U: return U
                vus.add(U); suiv.append(U)
        couche = suiv
    raise RuntimeError('aucune tuile contenant la paire %s %s' % (p, x))

def gram(L1, L2):
    M1 = np.array(L1, dtype=np.int64); M2 = np.array(L2, dtype=np.int64)
    return 2 * M1 @ M2.T - np.outer(M1.sum(1), M2.sum(1))

def t20(A, nes, p, x, c, ex, S=None):
    """Classe la paire (p ne, x non ne, lies). Renvoie 'parent', 'cousin' ou 'exception'."""
    Tp, Tx = T_de(A, p), T_de(A, x)
    T0 = porte_de_paire(tuile_des_deux(A, p, x, c), p, x)
    if T0 == Tx and T0 != Tp: c['parent'] += 1; return 'parent'
    if T0 != Tp and T0 != Tx:
        abc = T0 - {p, x}; x2 = autre(T0, x)
        if Tp == abc | {p, x2} and abc <= nes and x2 in nes and Tx == abc | {x, autre(T0, p)}:
            c['cousin'] += 1; return 'cousin'
    c['exception'] += 1
    if len(ex) < 3: ex.append(dict(p=list(p), x=list(x), T0=sorted(map(list, T0)), T0_est_Tp=(T0 == Tp), T0_est_Tx=(T0 == Tx)))
    return 'exception'

def partie_A1(n):
    t0 = time.time(); S, tui, A = Z.palier(n + 2)
    nes = {u for u in S if S[u] <= n}; P = sorted(nes); X = sorted(u for u in S if S[u] > n)
    c = dict(paires=0, parent=0, cousin=0, exception=0, tuile_cherchee_par_parcours=0); ex = []; ex_cousin = []
    par = {(k, cas): 0 for k in (1, 2) for cas in ('parent', 'cousin', 'exception')}
    G = gram(P, X); I, J = np.nonzero(G == -1)
    for i, j in zip(I.tolist(), J.tolist()):
        p, x = P[i], X[j]; c['paires'] += 1; cas = t20(A, nes, p, x, c, ex); par[(S[x] - n, cas)] += 1
        if cas == 'cousin' and len(ex_cousin) < 2: ex_cousin.append(dict(p=list(p), palier_p=S[p], x=list(x), palier_x=S[x]))
    print(json.dumps(dict(partie='A1', n=n, nes=len(P), non_nes_examines=len(X), **c,
                          x_au_palier_suivant={cas: par[(1, cas)] for cas in ('parent', 'cousin', 'exception')},
                          x_deux_paliers_plus_loin={cas: par[(2, cas)] for cas in ('parent', 'cousin', 'exception')},
                          exemples_d_exception=ex, exemples_de_cousins=ex_cousin, duree_s=round(time.time() - t0, 1))), flush=True)

def cellules(L):
    """Toutes les cellules (quatre constituants tous lies) de la liste L, et pour chacune ses cotes presents dans L."""
    G = gram(L, L); V = [set(np.nonzero(G[i] == -1)[0].tolist()) for i in range(len(L))]
    for i in range(len(L)):
        Ni = {j for j in V[i] if j > i}
        for j in Ni:
            Nij = {k for k in Ni & V[j] if k > j}
            for k in Nij:
                for l in Nij & V[k]:
                    if l > k: yield (i, j, k, l), sorted(V[i] & V[j] & V[k] & V[l])

def partie_A3(n):
    t0 = time.time(); S, tui, A = Z.palier(n); L = sorted(S)
    c = dict(cellules=0, sans_cote_ne=0, un_cote_ne=0, deux_cotes_nes=0, cote_ne_pas_du_cote_du_germe=0); ex = []
    for (i, j, k, l), cotes in cellules(L):
        c['cellules'] += 1; C = [L[i], L[j], L[k], L[l]]
        if not cotes:
            c['sans_cote_ne'] += 1
            if len(ex) < 3: ex.append([list(u) for u in C])
        elif len(cotes) == 1:
            c['un_cote_ne'] += 1; u = L[cotes[0]]; u2 = tuple(sum(v[t] for v in C) - u[t] for t in range(5))
            if not sum(u) < sum(u2): c['cote_ne_pas_du_cote_du_germe'] += 1
        else: c['deux_cotes_nes'] += 1
    print(json.dumps(dict(partie='A3', palier=n, constituants=len(L), **c, exemples_sans_cote_ne=ex, duree_s=round(time.time() - t0, 1))), flush=True)

def partie_A2(a, b):
    S6, tui6, A = Z.palier(6); L5 = sorted(u for u in S6 if S6[u] <= 5 and u not in GERME_ENS); L6 = sorted(S6)
    tot = dict(tissus=0, constituants_min=10 ** 9, constituants_max=0, paires=0, parent=0, cousin=0, exception=0, tuile_cherchee_par_parcours=0,
               places=0, hors_de_l_empilement=0, tissus_ou_places_egalent_cotes_non_nes=0, cellules_sans_cote_ne=0, cellules_dont_le_seul_cote_ne_est_loin_du_germe=0,
               places_au_plancher_incomplet=0, tissus_avec_place_au_plancher_incomplet=0, non_clos_par_plancher=0)
    ex = []; ex_incomplet = []
    for graine in range(a, b + 1):
        rng = random.Random(graine); k = rng.randint(2, 8); tires = rng.sample(L5, k); S = set(GERME) | set(tires)
        for u in tires: S |= A.an[u]
        t0 = time.time(); nes = set(S); P = sorted(nes); X = [u for u in L6 if u not in nes]
        if any(not (A.pl[u] <= nes) for u in nes if u not in GERME_ENS): tot['non_clos_par_plancher'] += 1
        c = dict(paires=0, parent=0, cousin=0, exception=0, tuile_cherchee_par_parcours=0)
        G = gram(P, X); I, J = np.nonzero(G == -1)
        for i, j in zip(I.tolist(), J.tolist()): c['paires'] += 1; t20(A, nes, P[i], X[j], c, ex)
        O, tui = Y.outil(S); r, pl, lib = Y.places(O)
        # cellules nees : cote ne du cote du germe ?
        loin = 0; sans = 0
        for (i, j, kk, l), cotes in cellules(P):
            if not cotes: sans += 1
            elif len(cotes) == 1:
                C = [P[i], P[j], P[kk], P[l]]; u = P[cotes[0]]; u2 = tuple(sum(v[t] for v in C) - u[t] for t in range(5))
                if not sum(u) < sum(u2): loin += 1
        inc = 0
        for x in lib:
            x = tuple(int(t) for t in x)
            if x in S6 and not (A.pl[x] <= nes):
                inc += 1
                if len(ex_incomplet) < 2: ex_incomplet.append(dict(graine=graine, place=list(x), parents_non_nes=[list(v) for v in sorted(A.pl[x] - nes)]))
            elif x not in S6: raise RuntimeError('cote libre hors du palier 6')
        tot['tissus'] += 1; tot['constituants_min'] = min(tot['constituants_min'], len(P)); tot['constituants_max'] = max(tot['constituants_max'], len(P))
        for cle in c: tot[cle] += c[cle]
        tot['places'] += r['places_admissibles']; tot['hors_de_l_empilement'] += r['hors_de_l_empilement']
        tot['tissus_ou_places_egalent_cotes_non_nes'] += 1 if r['places_egales_aux_cotes_libres'] else 0
        tot['cellules_sans_cote_ne'] += sans; tot['cellules_dont_le_seul_cote_ne_est_loin_du_germe'] += loin
        tot['places_au_plancher_incomplet'] += inc; tot['tissus_avec_place_au_plancher_incomplet'] += 1 if inc else 0
        assert sans == r['cellules_sans_cote_ne'], 'desaccord avec l outil du laboratoire sur les cellules sans cote ne'
        print(json.dumps(dict(graine=graine, constituants=len(P), **c, places=r['places_admissibles'], hors=r['hors_de_l_empilement'],
                              places_egales_aux_cotes=r['places_egales_aux_cotes_libres'], cellules_sans_cote_ne=sans, plancher_incomplet=inc,
                              duree_s=round(time.time() - t0, 1))), flush=True)
    print(json.dumps(dict(bilan=True, partie='A2', graines=[a, b], **tot, exemples_d_exception=ex, exemples_plancher_incomplet=ex_incomplet)), flush=True)

def partie_B(n):
    t0 = time.time(); S, tui, A = Z.palier(n); L = sorted(S); idx = {u: i for i, u in enumerate(L)}; pal = np.array([S[u] for u in L])
    G = gram(L, L); V = [set(np.nonzero(G[i] == -1)[0].tolist()) for i in range(len(L))]
    # B2 : fils du germe
    b2 = {}
    for p, q in itertools.combinations(GERME, 2):
        com = V[idx[p]] & V[idx[q]]; b2['%s-%s' % (GERME.index(p), GERME.index(q))] = [sum(1 for k in com if pal[k] <= g) for g in range(n + 1)]
    # B3 : toutes les paires liees nees au palier n-1 au plus
    mx = 0; mx_ex = None; npaires = 0; histo = {}
    for i in range(len(L)):
        if pal[i] > n - 1: continue
        for j in V[i]:
            if j <= i or pal[j] > n - 1: continue
            npaires += 1; k = len(V[i] & V[j]); histo[k] = histo.get(k, 0) + 1
            if k > mx: mx = k; mx_ex = dict(p=list(L[i]), q=list(L[j]), paliers=[int(pal[i]), int(pal[j])])
    # B4 : paires liees de meme palier
    b4 = {g: dict(paires=0, cousins=0, autres=0) for g in range(1, n)}; c = dict(tuile_cherchee_par_parcours=0); ex = []
    for i in range(len(L)):
        for j in V[i]:
            if j <= i or pal[i] != pal[j] or pal[i] == 0 or pal[i] > n - 1: continue
            p, q = L[i], L[j]; g = int(pal[i]); b4[g]['paires'] += 1
            Tp, Tq = T_de(A, p), T_de(A, q); T0 = porte_de_paire(tuile_des_deux(A, p, q, c), p, q); abc = T0 - {p, q}
            if T0 != Tp and T0 != Tq and Tp == abc | {p, autre(T0, q)} and Tq == abc | {q, autre(T0, p)}: b4[g]['cousins'] += 1
            else:
                b4[g]['autres'] += 1
                if len(ex) < 3: ex.append(dict(p=list(p), q=list(q)))
    # B5 : voisins d'un constituant du germe, par palier
    b5 = [[sum(1 for k in V[idx[p]] if pal[k] <= g) for g in range(n + 1)] for p in GERME]
    print(json.dumps(dict(partie='B', palier=n, constituants=len(L), B2_voisins_communs_des_fils_du_germe=b2,
                          B3_paires_liees_nees_au_palier_precedent_au_plus=npaires, B3_plus_grand_nombre_de_voisins_communs=mx, B3_exemple=mx_ex,
                          B3_histogramme={str(k): histo[k] for k in sorted(histo)}, B4_paires_liees_de_meme_palier={str(g): b4[g] for g in b4},
                          B4_exemples_non_cousins=ex, B4_tuiles_cherchees_par_parcours=c['tuile_cherchee_par_parcours'],
                          B5_voisins_des_constituants_du_germe_par_palier=b5, duree_s=round(time.time() - t0, 1))), flush=True)

if __name__ == '__main__':
    quoi = sys.argv[1]
    if quoi == 'A1': partie_A1(int(sys.argv[2]))
    elif quoi == 'A2': partie_A2(int(sys.argv[2]), int(sys.argv[3]))
    elif quoi == 'A3': partie_A3(int(sys.argv[2]))
    elif quoi == 'B': partie_B(int(sys.argv[2]))
