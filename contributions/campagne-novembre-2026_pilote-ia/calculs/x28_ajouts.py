#!/usr/bin/env python3
"""X-28, AJOUTS NON PREDITS (faits apres les clauses scellees). Regle a la lettre, paliers 0 a n.
 contacts n : pour chaque place (parents a symetrie pres) : nombre de contacts ; pour chaque paire de contacts non lies : produit, et nombre de contacts
              lies aux deux. Motif attendu si la place est le dernier constituant manquant d'un anneau : produit -5 et au moins trois contacts communs.
 comble n   : on ajoute au tissu les places a cinq contacts (derniers membres manquants d'un anneau) ; ses tuiles sont-elles alors convexes ?
 pliage n   : lemme du pliage. Pour chaque cellule a un seul cote ne t (cote libre t') et chaque constituant ne u au-dela du mur (<u, t - t'> < 0) :
              l'image de u dans le mur, u - <u, t - t'> (t - t')/6, est-elle nee ? Et son palier est-il au plus celui de u ?
Usage : python3 x28_ajouts.py contacts 6 | pliage 6 | comble 5      Claude, 27 novembre 2026."""
import itertools, json, sys, time
import numpy as np
import x28_tissu_convexe as X
from x25bis_naissances_et_fermetures import Tissu

def paliers(nmax):
    T = Tissu(3); yield 0, T
    for g in range(1, nmax + 1): T.palier(g); yield g, T

def contacts(nmax):
    for g, T in paliers(nmax):
        S = sorted(T.spheres); O = X.Outil(S); O.cliques(); O.cotes_libres()
        reps = [i for i, u in enumerate(O.S) if u == tuple(sorted(u))]
        pl, _, _ = O.places_exactes(reps)
        nb = {}; prods = {}; communs = {}; cellules_par_place = {}
        for cle, (P, ct) in pl.items():
            c = sorted(ct); nb[len(c)] = nb.get(len(c), 0) + 1
            ncel = sum(1 for t in itertools.combinations(c, 4) if all(b in O.adj[a] for a, b in itertools.combinations(t, 2)))
            cellules_par_place[ncel] = cellules_par_place.get(ncel, 0) + 1
            for q, r in itertools.combinations(c, 2):
                if r in O.adj[q]: continue
                v = int(O.Gm[q, r]); prods[v] = prods.get(v, 0) + 1
                k = sum(1 for u in c if u not in (q, r) and u in O.adj[q] and u in O.adj[r]); communs[k] = communs.get(k, 0) + 1
        print(json.dumps(dict(palier=g, places_types=len(pl), nombre_de_contacts=nb, cellules_nees_parmi_les_contacts=cellules_par_place,
                              paires_non_liees_par_produit=prods, paires_non_liees_par_nombre_de_contacts_communs=communs)), flush=True)

def pliage(nmax):
    for g, T in paliers(nmax):
        S = sorted(T.spheres); O = X.Outil(S); O.cliques(); O.cotes_libres(); pal = np.array([T.spheres[u] for u in O.S])
        murs = au_dela = image_nee = palier_ok = non_entier = 0
        for C, t, t2 in O.murs:
            d = np.array([a - b for a, b in zip(t, t2)], dtype=np.int64); murs += 1
            v = 2 * O.Ai @ d - O.Ai.sum(1) * d.sum()
            for j in np.nonzero(v < 0)[0]:
                au_dela += 1
                if v[j] % 6: non_entier += 1; continue
                im = tuple(int(a) for a in (O.Ai[j] - (v[j] // 6) * d))
                if im in O.idx:
                    image_nee += 1
                    if pal[O.idx[im]] <= pal[j]: palier_ok += 1
        print(json.dumps(dict(palier=g, constituants=len(S), murs_de_surface=murs, constituants_au_dela_d_un_mur=au_dela, image_non_entiere=non_entier,
                              image_nee=image_nee, palier_de_l_image_au_plus_egal=palier_ok)), flush=True)

def comble(nmax):
    """Le tissu du palier n, auquel on ajoute les places a cinq contacts (derniers membres manquants d'un anneau) : ses tuiles sont-elles convexes ?"""
    for g, T in paliers(nmax):
        S = sorted(T.spheres); O = X.Outil(S); O.cliques(); O.cotes_libres()
        reps = [i for i, u in enumerate(O.S) if u == tuple(sorted(u))]
        pl, _, _ = O.places_exactes(reps); ajout = set()
        for cle, (P, ct) in pl.items():
            if len(ct) == 5:
                for pe in X.PERMS: ajout.add(tuple(P.coords[k] for k in pe))
        O2 = X.Outil(S + sorted(ajout)); O2.cliques(); O2.cotes_libres(); c = O2.convexite()
        print(json.dumps(dict(palier=g, constituants=len(S), derniers_membres_d_anneau_ajoutes=len(ajout), tuiles_nees_apres_ajout=len(O2.tuiles),
                              murs_de_surface=c['murs_de_surface'], murs_avec_un_constituant_au_dela=c['murs_avec_un_constituant_au_dela'], convexe=c['convexe'], temoin=c['temoin'])), flush=True)

if __name__ == '__main__':
    {'contacts': contacts, 'pliage': pliage, 'comble': comble}[sys.argv[1]](int(sys.argv[2]))
