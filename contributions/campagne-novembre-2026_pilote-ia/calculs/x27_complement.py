#!/usr/bin/env python3
"""X-27, complement ajoute apres les premieres executions (non predit) :
 (1) un exemple explicite de place sans cellule (croissance dans une couche, graine 1), avec ses contacts et leurs produits mutuels ;
 (2) combien de quadruples (parent et trois voisins) offrent DEUX places admissibles a la fois : les contacts ne designent alors pas une place unique ;
 (3) croissance MIXTE, ajoutee parce que l'ordre adverse de la prediction s'est revele vide (aucune place sans cellule n'apparait en ordre tire au hasard, donc
     l'ordre adverse y est identique a l'ordre au hasard) : 25 naissances dans une couche, la place la moins attachee d'abord (ce qui fait naitre des places sans
     cellule et y fait naitre), puis 45 naissances en ordre adverse sans contrainte ; toutes les places admissibles sont controlees a chaque naissance.
 (4) RECHERCHE CIBLEE d'un contre-exemple a K20. Univers : l'empilement jusqu'au palier g (regle a la lettre). Pour chaque quadruple (parent et trois voisins) de
     l'univers et chacune de ses solutions x qui n'est PAS dans l'empilement : x chevauche certains constituants de l'univers (ensemble O) ; si O ne contient aucun
     constituant du germe, on fait croitre un tissu depuis le germe en prenant toutes les places admissibles de l'univers hors de O, jusqu'a epuisement ; si les
     quatre contacts de x finissent tous dans ce tissu, x y est une place admissible hors de l'empilement : contre-exemple. Recherche, non preuve (l'univers est borne).
Usage : python3 x27_complement.py | python3 x27_complement.py mixte graine_debut graine_fin | python3 x27_complement.py cible g [budget_s]
Meme outil que x27_mitose_avec_heritage.py, importe tel quel.     Claude, 23 novembre 2026."""
import json, os, random
import x27_mitose_avec_heritage as m
from x25bis_naissances_et_fermetures import Tissu

ICI = os.path.dirname(os.path.abspath(__file__))


def quadruples_a_deux_places(T):
    """Par quadruple examine : nombre de places admissibles parmi ses (au plus deux) solutions."""
    h = {0: 0, 1: 0, 2: 0}; cellules2 = 0
    for q in T.quads:
        sols = m.places_du_quadruple(frozenset(T.S[i] for i in q))
        k = sum(1 for pl in sols if pl.cle in T.places); h[k] += 1
        if k == 2:
            ids = sorted(q)
            if all(b in T.adj[a] for i, a in enumerate(ids) for b in ids[i + 1:]): cellules2 += 1
    return dict(quadruples=len(T.quads), sans_place=h[0], une_place=h[1], deux_places=h[2], dont_cellules_aux_deux_cotes_libres=cellules2)


def exemple_sans_cellule(graine=1, naissances=40):
    rng = random.Random(graine); T = m.Tissu27(m.G5)
    for k in range(naissances):
        cles = sorted((c for c in T.places if T.vues[c] == 'empilement'), key=repr)
        sans = [c for c in cles if T.sans_cellule(c)]
        if sans:
            c = sans[0]; pl, cont = T.places[c]; cont = sorted(cont)
            return dict(naissances_avant=k, constituants=len(T.S), place=list(c), dans_l_empilement=m.dans_l_empilement(c), touche=[list(T.S[i]) for i in cont],
                        produits_entre_les_constituants_touches=[[m.prod(T.S[a], T.S[b]) for b in cont] for a in cont],
                        produits_de_la_place_avec_le_tissu=sorted(m.prod(c, s) for s in T.S)[-6:])
        choix = [c for c in cles if 0 in T.places[c][1] and 1 in T.places[c][1]]
        mn = min(len(T.places[c][1]) for c in choix); choix = [c for c in choix if len(T.places[c][1]) == mn]
        T.naissance(rng.choice(choix))
    return None


def etat_final(strategie, graine, naissances):
    """Rejoue une croissance de la partie B (meme tirage) et rend le tissu final."""
    rng = random.Random(graine); T = m.Tissu27(m.G5)
    for k in range(naissances):
        cles = sorted((c for c in T.places if T.vues[c] == 'empilement'), key=repr)
        sans = [c for c in cles if T.sans_cellule(c)]
        if strategie == 'couche':
            choix = [c for c in cles if 0 in T.places[c][1] and 1 in T.places[c][1]]
            mn = min(len(T.places[c][1]) for c in choix); choix = [c for c in choix if len(T.places[c][1]) == mn]
        elif strategie == 'adverse' and sans: choix = sans
        else: choix = cles
        T.naissance(rng.choice(choix))
    return T


def mixte(graine, n_couche=25, n_libre=45):
    import time
    rng = random.Random(graine); T = m.Tissu27(m.G5); t0 = time.time(); jamais_sans = set(); nais_sans = 0
    for k in range(n_couche + n_libre):
        cles = sorted((c for c in T.places if T.vues[c] == 'empilement'), key=repr)
        sans = [c for c in cles if T.sans_cellule(c)]; jamais_sans.update(sans)
        if k < n_couche:
            choix = [c for c in cles if 0 in T.places[c][1] and 1 in T.places[c][1]]
            mn = min(len(T.places[c][1]) for c in choix); choix = [c for c in choix if len(T.places[c][1]) == mn]
        else: choix = sans if sans else cles
        c = rng.choice(choix); nais_sans += c in sans
        T.naissance(c)
    b = m.bilan_des_vues(T.vues)
    return dict(strategie='mixte', graine=graine, naissances=len(T.S) - 5, quadruples_examines=len(T.quads), places_admissibles_rencontrees=len(T.vues), par_classe=b,
                hors_de_l_empilement=sum(v for c, v in b.items() if c != 'empilement'), exemples_hors=T.hors[:5], places_sans_cellule_rencontrees=len(jamais_sans),
                naissances_dans_une_place_sans_cellule=nais_sans, deux_places=quadruples_a_deux_places(T), duree_s=round(time.time() - t0, 1))


def recherche_ciblee(g, budget_s=1500):
    import time
    import numpy as np
    t0 = time.time(); T3 = Tissu(3)
    for k in range(1, g + 1): T3.palier(k)
    U = sorted(T3.spheres); rang = {u: i for i, u in enumerate(U)}; germe = {rang[u] for u in m.G5}
    W = m.Tissu27(U); assert W.S == U
    A = np.array(U, dtype=float); sA = A.sum(axis=1)
    aretes = []; sols_de = []                                  # hyperaretes : quadruple (indices) -> solutions qui sont dans l'univers
    cibles = {}                                                # places hors empilement : cle -> (place, indice d'hyperarete)
    n_sol = n_dans = 0
    for q in W.quads:
        quad = frozenset(W.S[i] for i in q); e = len(aretes); aretes.append(tuple(sorted(q))); dedans = []
        for pl in m.places_du_quadruple(quad):
            n_sol += 1
            if pl.coords is not None and all(isinstance(v, int) for v in pl.coords) and m.dans_l_empilement(pl.coords):
                n_dans += 1
                if pl.coords in rang: dedans.append(rang[pl.coords])
            elif pl.cle not in cibles: cibles[pl.cle] = (pl, e)
        sols_de.append(dedans)
    par_membre = [[] for _ in U]
    for e, q in enumerate(aretes):
        for i in q: par_membre[i].append(e)
    par_O = {}; touche_germe = 0
    for cle, (pl, e) in cibles.items():
        v = 2 * A @ pl.xf - sA * pl.xf.sum() + 1
        O = set(int(i) for i in np.nonzero(v > 1e-7)[0])
        for i in np.nonzero(np.abs(v) <= 1e-7)[0]:
            if pl.compare(U[int(i)]) > 0: O.add(int(i))
        if O & germe: touche_germe += 1; continue
        par_O.setdefault(frozenset(O), []).append((pl, e))
    r = dict(palier=g, univers=len(U), quadruples=len(aretes), solutions=n_sol, solutions_dans_l_empilement=n_dans, places_hors_empilement_distinctes=len(cibles),
             dont_chevauchent_le_germe=touche_germe, a_tester=len(cibles) - touche_germe, ensembles_O_distincts=len(par_O), duree_preparation_s=round(time.time() - t0, 1))
    print(json.dumps(r), flush=True)
    contre = []; testes = 0; fermetures = 0; tailles = []
    for O, liste in sorted(par_O.items(), key=lambda kv: (len(kv[0]), sorted(kv[0]))):
        if time.time() - t0 > budget_s: break
        gen = set(germe); reste = [4] * len(aretes); pile = list(germe)
        while pile:                                            # fermeture : un constituant de l'univers, hors de O, nait des que les quatre membres d'un de ses quadruples existent
            i = pile.pop()
            for e in par_membre[i]:
                reste[e] -= 1
                if reste[e] == 0:
                    for y in sols_de[e]:
                        if y not in gen and y not in O: gen.add(y); pile.append(y)
        fermetures += 1; tailles.append(len(gen))
        for pl, e in liste:
            testes += 1
            if all(i in gen for i in aretes[e]):
                contre.append(dict(place=[str(v) for v in pl.coords] if pl.coords is not None else [round(float(v), 9) for v in pl.xf], contacts=[list(U[i]) for i in aretes[e]],
                                   chevauche=[list(U[i]) for i in sorted(O)], tissu=len(gen)))
    r.update(places_testees=testes, fermetures_calculees=fermetures, ensembles_O_restants=len(par_O) - fermetures, contre_exemples=len(contre), exemples=contre[:5],
             taille_du_tissu_atteint_min_mediane_max=[min(tailles), sorted(tailles)[len(tailles) // 2], max(tailles)] if tailles else None, duree_s=round(time.time() - t0, 1))
    return r


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cible':
        g = int(sys.argv[2]); budget = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
        r = recherche_ciblee(g, budget); print(json.dumps(r), flush=True)
        json.dump(r, open(os.path.join(ICI, 'x27_complement_cible_%d.json' % g), 'w'), indent=1)
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'mixte':
        g0, g1 = int(sys.argv[2]), int(sys.argv[3]); res = []
        for g in range(g0, g1 + 1):
            r = mixte(g); res.append(r); print(json.dumps(r), flush=True)
        json.dump(res, open(os.path.join(ICI, 'x27_complement_mixte_%d_%d.json' % (g0, g1)), 'w'), indent=1)
        sys.exit(0)
    out = dict(exemple_de_place_sans_cellule=exemple_sans_cellule())
    print(json.dumps(out['exemple_de_place_sans_cellule']), flush=True)
    deux = []
    T3 = Tissu(3)
    for g in range(0, 3):
        if g: T3.palier(g)
        r = dict(tissu='regle a la lettre, palier %d' % g, **quadruples_a_deux_places(m.Tissu27(sorted(T3.spheres)))); deux.append(r); print(json.dumps(r), flush=True)
    for strategie, graine, nais in (('hasard', 1, 70), ('hasard', 2, 70), ('couche', 1, 40), ('couche', 2, 40)):
        T = etat_final(strategie, graine, nais)
        r = dict(tissu='%s, graine %d, %d naissances' % (strategie, graine, nais), constituants=len(T.S), **quadruples_a_deux_places(T)); deux.append(r); print(json.dumps(r), flush=True)
    out['quadruples_offrant_deux_places'] = deux
    json.dump(out, open(os.path.join(ICI, 'x27_complement.json'), 'w'), indent=1)
