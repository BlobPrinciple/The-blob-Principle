#!/usr/bin/env python3
"""X-29, LE PLIAGE VERS LE GERME. Prediction scellee : x29_pliage_prediction.txt (SHA-256 725060cd...041a), poussee avant ce calcul.
 paliers n   : regle a la lettre, paliers 0 a n. Q1 (a) clos par pliage pour tous les murs separant une tuile nee du germe ; (b) formule de T7.
 x27         : Q2 (les tissus de X-27 sont-ils clos par pliage ?) et Q5 (cloture par pliage du tissu de 22 constituants, ses places).
 hasard a b  : Q3 et Q4, graines a a b. Reunion de 1 a 3 intervalles inferieurs de Bruhat, toutes les places, puis moitie des cotes libres ajoutee.
 partiel     : Q6, les six tissus incomplets de la clause N7(b) de X-28.
 regle n     : AJOUT NON SCELLE. Le tissu du programme de X-25 suit-il l'enonce mathematique de la regle a la lettre, paliers 0 a n ?
 ecartes a b : AJOUT NON SCELLE. Les tirages que Q3 a ecartes (plus de 350 constituants), toutes les places, sans Q4.
Mur : normale n = (constituant loin) - (son autre cote), <n, n> = 12 ; image de v : v - <v, n> n / 6. Descente : on retourne un constituant dont
l'autre cote a une somme de coordonnees plus petite (le germe est alors de l'autre cote du mur).      Claude, 27 novembre 2026."""
import json, os, random, sys, time
import x28_tissu_convexe as X
from x25bis_naissances_et_fermetures import Tissu
import x27_mitose_avec_heritage as m

ICI = os.path.dirname(os.path.abspath(__file__))
GERME = tuple(m.G5); GERME_ENS = frozenset(GERME)

def prod(a, b): return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)

def autre(T, u):
    """L'autre cote de la cellule T - {u} : somme des quatre autres, moins u."""
    return tuple(sum(v[k] for v in T) - 2 * u[k] for k in range(5))

def descentes(T): return [u for u in T if sum(autre(T, u)) < sum(u)]

def murs_vers_le_germe(T):
    """Normales des murs traverses par une descente de la tuile T au germe : ce sont les murs qui separent T du germe."""
    T = set(T); murs = []
    while True:
        d = descentes(T)
        if not d: break
        u = min(d); u2 = autre(T, u); murs.append(tuple(a - b for a, b in zip(u, u2))); T.remove(u); T.add(u2)
    assert frozenset(T) == GERME_ENS, 'la descente ne finit pas au germe'
    return murs

def image(v, n):
    c = prod(v, n); assert c >= 0
    if c == 0: return None
    w = [c * b for b in n]; assert all(x % 6 == 0 for x in w)
    return tuple(a - x // 6 for a, x in zip(v, w))

def pliage(S, tuiles):
    """Pour chaque tuile nee, chaque mur qui la separe du germe, chaque constituant au-dela : l'image est-elle nee ?"""
    tri = ech = 0; manque = set(); ex = None
    for T in tuiles:
        for n in murs_vers_le_germe(T):
            for v in T:
                im = image(v, n)
                if im is None: continue
                tri += 1
                if im not in S:
                    ech += 1; manque.add(im)
                    if ex is None: ex = dict(tuile=sorted(map(list, T)), mur=list(n), constituant=list(v), image_non_nee=list(im))
    return tri, ech, manque, ex

def tuiles_par_voisinage(S):
    """Tuiles nees atteintes depuis le germe en ne traversant que des tuiles nees."""
    vus = {GERME_ENS}; pile = [GERME_ENS]
    while pile:
        T = pile.pop()
        for u in T:
            u2 = autre(T, u)
            if u2 in S:
                T2 = (T - {u}) | {u2}
                if T2 not in vus: vus.add(T2); pile.append(T2)
    return vus

def outil(S):
    O = X.Outil(sorted(S)); cel, tui = O.cliques()
    return O, [frozenset(O.S[i] for i in t) for t in O.tuiles]

def places(O):
    lib, sans_cote, deux = O.cotes_libres(); pl, tri, surv = O.places_exactes(list(range(len(O.S)))); cl, sc, hors = X.bilan(O, pl); cles = set(pl)
    return dict(places_admissibles=len(pl), par_classe=cl, hors_de_l_empilement=sum(v for c, v in cl.items() if c != 'empilement'), places_sans_cellule=sc,
                cotes_libres=len(lib), cellules_sans_cote_ne=sans_cote, places_egales_aux_cotes_libres=(cles == lib), places_hors_cotes=len(cles - lib),
                cotes_non_admissibles=len(lib - cles), exemples_hors_empilement=hors), pl, lib

def partie_paliers(nmax):
    T = Tissu(3)
    for g in range(nmax + 1):
        if g: T.palier(g)
        S = dict(T.spheres); t0 = time.time(); tui = tuiles_par_voisinage(S); tri, ech, manque, ex = pliage(S, tui)
        # T7 : tuile-porte de u = la tuile nee contenant u dont aucune descente n'est un autre constituant que u
        de = {}
        for Tu in tui:
            d = descentes(Tu)
            if len(d) == 1: de.setdefault(d[0], []).append(Tu)
        hors_germe = [u for u in S if u not in GERME_ENS]; sans_porte = plusieurs = faux = 0
        for u in hors_germe:
            L = de.get(u, [])
            if not L: sans_porte += 1; continue
            if len(L) > 1: plusieurs += 1
            if S[u] != 1 + max(S[v] for v in L[0] if v != u): faux += 1
        lon = {}
        for Tu in tui: k = len(murs_vers_le_germe(Tu)); lon[k] = lon.get(k, 0) + 1
        print(json.dumps(dict(palier=g, constituants=len(S), tuiles_nees_atteintes=len(tui), triplets_tuile_mur_constituant=tri, images_non_nees=ech, exemple=ex,
                              T7_constituants_hors_germe=len(hors_germe), T7_sans_tuile_porte_nee=sans_porte, T7_plusieurs_tuiles_portes=plusieurs, T7_formule_fausse=faux,
                              tuiles_par_longueur=dict(sorted(lon.items())), duree_s=round(time.time() - t0, 1))), flush=True)

def cloture(S):
    S = set(S); tours = 0
    while True:
        O, tui = outil(S); tri, ech, manque, ex = pliage(S, tui)
        if not manque: return S, tours
        S |= manque; tours += 1

def partie_x27():
    for nom, f in (('tissu_de_22', 'x27_contre_exemple_court.json'), ('tissu_du_toit', 'x27_contre_exemple_toit.json')):
        c = json.load(open(os.path.join(ICI, f))); S = set(GERME) | {tuple(u) for u in c['liste_des_naissances']}
        O, tui = outil(S); dans = set().union(*tui); tri, ech, manque, ex = pliage(S, tui)
        r = dict(tissu=nom, constituants=len(S), tuiles_nees=len(tui), constituants_hors_de_toute_tuile_nee=len(S - dans), triplets=tri, images_non_nees=ech,
                 images_distinctes_manquantes=len(manque), clos_par_pliage=(ech == 0 and not (S - dans)), exemple=ex)
        print(json.dumps(r), flush=True)
        if nom == 'tissu_de_22':
            t0 = time.time(); C, tours = cloture(S); O2, tui2 = outil(C); tri2, ech2, _, _ = pliage(C, tui2); b, pl, lib = places(O2)
            x = tuple(X.F(v) for v in c['place_hors_empilement']); jum = (2, 2, 2, -1, 0)
            print(json.dumps(dict(cloture_du_tissu_de_22=True, tours=tours, constituants=len(C), ajoutes=len(C) - len(S), tuiles_nees=len(tui2), images_non_nees=ech2,
                                  la_place_hors_empilement_est_encore_admissible=(x in pl), la_jumelle_2_2_2_m1_0_est_nee=(jum in C), **b, duree_s=round(time.time() - t0, 1))), flush=True)

def retourne(T, j):
    u2 = tuple(sum(T[i][k] for i in range(5)) - 2 * T[j][k] for k in range(5))
    return T[:j] + (u2,) + T[j + 1:]

def mot_au_hasard(rng, L):
    T = GERME; mot = []
    for _ in range(L):
        monte = [j for j in range(5) if sum(retourne(T, j)[j]) > sum(T[j])]
        j = rng.choice(monte); mot.append(j); T = retourne(T, j)
    return mot

def intervalle(mot):
    """Tous les sous-mots d'un mot reduit : l'intervalle inferieur de Bruhat [germe, w]."""
    A = {GERME}
    for j in mot: A |= {retourne(T, j) for T in A}
    return A

def partie_hasard(a, b):
    tot = dict(tissus=0, ecartes=0, hors=0, sans_cellule=0, places=0, differents_des_cotes=0, pliage_echecs=0, q4_hors=0, q4_places=0, q4_sans_cellule=0, q4_clos=0)
    for graine in range(a, b + 1):
        rng = random.Random(graine); k = rng.randint(1, 3); B = set(); mots = []
        for _ in range(k):
            mot = mot_au_hasard(rng, rng.randint(3, 12)); mots.append(mot); B |= intervalle(mot)
        S = {v for T in B for v in T}
        if len(S) > 350:
            tot['ecartes'] += 1; print(json.dumps(dict(graine=graine, mots=mots, constituants=len(S), ecarte=True)), flush=True); continue
        t0 = time.time(); O, tui = outil(S); tri, ech, _, ex = pliage(S, tui); r, pl, lib = places(O)
        tot['tissus'] += 1; tot['hors'] += r['hors_de_l_empilement']; tot['sans_cellule'] += r['places_sans_cellule']; tot['places'] += r['places_admissibles']
        tot['differents_des_cotes'] += 0 if r['places_egales_aux_cotes_libres'] else 1; tot['pliage_echecs'] += ech
        # Q4 : on ajoute une moitie tiree au hasard des cotes libres
        L = sorted(lib); S2 = S | set(rng.sample(L, len(L) // 2)); O2, tui2 = outil(S2); tri2, ech2, _, _ = pliage(S2, tui2); r2, pl2, lib2 = places(O2)
        tot['q4_hors'] += r2['hors_de_l_empilement']; tot['q4_places'] += r2['places_admissibles']; tot['q4_sans_cellule'] += r2['places_sans_cellule']; tot['q4_clos'] += 1 if ech2 == 0 else 0
        print(json.dumps(dict(graine=graine, longueurs=[len(w) for w in mots], tuiles_de_l_ideal=len(B), constituants=len(S), tuiles_nees=len(tui), images_non_nees=ech,
                              places=r['places_admissibles'], hors=r['hors_de_l_empilement'], sans_cellule=r['places_sans_cellule'], cotes_libres=r['cotes_libres'],
                              egales_aux_cotes=r['places_egales_aux_cotes_libres'], hors_cotes=r['places_hors_cotes'], cotes_non_admissibles=r['cotes_non_admissibles'],
                              cellules_sans_cote_ne=r['cellules_sans_cote_ne'], exemples=r['exemples_hors_empilement'][:2],
                              q4=dict(constituants=len(S2), images_non_nees=ech2, places=r2['places_admissibles'], hors=r2['hors_de_l_empilement'], sans_cellule=r2['places_sans_cellule'],
                                      egales_aux_cotes=r2['places_egales_aux_cotes_libres'], exemples=r2['exemples_hors_empilement'][:2]), duree_s=round(time.time() - t0, 1))), flush=True)
    print(json.dumps(dict(bilan=True, graines=[a, b], **tot)), flush=True)

def partie_ecartes(a, b):
    """AJOUT NON SCELLE, fait apres les six clauses : les tirages ecartes par la clause Q3 (plus de 350 constituants), sans la clause Q4."""
    tot = dict(tissus=0, hors=0, sans_cellule=0, places=0, differents_des_cotes=0, pliage_echecs=0)
    for graine in range(a, b + 1):
        rng = random.Random(graine); k = rng.randint(1, 3); B = set(); mots = []
        for _ in range(k):
            mot = mot_au_hasard(rng, rng.randint(3, 12)); mots.append(mot); B |= intervalle(mot)
        S = {v for T in B for v in T}
        if len(S) <= 350: continue
        t0 = time.time(); O, tui = outil(S); tri, ech, _, ex = pliage(S, tui); r, pl, lib = places(O)
        tot['tissus'] += 1; tot['hors'] += r['hors_de_l_empilement']; tot['sans_cellule'] += r['places_sans_cellule']; tot['places'] += r['places_admissibles']
        tot['differents_des_cotes'] += 0 if r['places_egales_aux_cotes_libres'] else 1; tot['pliage_echecs'] += ech
        print(json.dumps(dict(graine=graine, longueurs=[len(w) for w in mots], tuiles_de_l_ideal=len(B), constituants=len(S), tuiles_nees=len(tui), images_non_nees=ech,
                              places=r['places_admissibles'], hors=r['hors_de_l_empilement'], sans_cellule=r['places_sans_cellule'], cotes_libres=r['cotes_libres'],
                              egales_aux_cotes=r['places_egales_aux_cotes_libres'], cellules_sans_cote_ne=r['cellules_sans_cote_ne'], exemples=r['exemples_hors_empilement'][:2],
                              duree_s=round(time.time() - t0, 1))), flush=True)
    print(json.dumps(dict(bilan=True, graines=[a, b], **tot)), flush=True)

def partie_regle(nmax):
    """AJOUT NON SCELLE : le tissu du programme de X-25 suit-il l'enonce mathematique retenu ? Naissances du palier g+1 = cotes non nes des cellules des tuiles nees du palier g."""
    T = Tissu(3); S = dict(T.spheres)
    for g in range(nmax):
        tui = tuiles_par_voisinage(S); cotes = {autre(Tu, u) for Tu in tui for u in Tu} - set(S)
        T.palier(g + 1); S2 = dict(T.spheres); nes = set(S2) - set(S)
        print(json.dumps(dict(palier=g, cotes_non_nes_des_cellules=len(cotes), naissances_du_palier_suivant=len(nes), memes_ensembles=(cotes == nes))), flush=True); S = S2

def partie_partiel():
    T = Tissu(3)
    for g in range(1, 5): T.palier(g)
    S4 = sorted(T.spheres); O4 = X.Outil(S4); O4.cliques(); libres, _, _ = O4.cotes_libres(); L = sorted(libres)
    for graine in (1, 2):
        for frac in (0.25, 0.5, 0.75):
            rng = random.Random(graine); S = set(S4) | set(rng.sample(L, int(round(frac * len(L))))); O, tui = outil(S); tri, ech, manque, ex = pliage(S, tui)
            print(json.dumps(dict(graine=graine, fraction=frac, constituants=len(S), tuiles_nees=len(tui), triplets=tri, images_non_nees=ech,
                                  images_distinctes_manquantes=len(manque), clos_par_pliage=(ech == 0))), flush=True)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'paliers': partie_paliers(int(a[1]))
    elif a[0] == 'x27': partie_x27()
    elif a[0] == 'hasard': partie_hasard(int(a[1]), int(a[2]))
    elif a[0] == 'partiel': partie_partiel()
    elif a[0] == 'regle': partie_regle(int(a[1]))
    elif a[0] == 'ecartes': partie_ecartes(int(a[1]), int(a[2]))
