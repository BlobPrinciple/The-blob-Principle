"""Contre-audit X-32, variante libre (HORS de l'enonce T28).
Chaque constituant ne p prend pour fille n'importe quel constituant x non ne dont p est un parent et dont les quatre
parents sont nes ; filles distinctes. Couplage glouton au hasard ; si le glouton bloque, on cherche par chemins
augmentants s'il existe un couplage parfait, et on continue avec lui.
Usage : python3 libre.py GRAINE_DEBUT GRAINE_FIN GENERATIONS [hasard|adverse]"""
import json, random, sys, time
from collections import Counter
from commun import *


def candidats(gen):
    L = sorted(gen)
    over, adj = gram_check(L)
    assert over == 0
    adjs = [set(int(j) for j in a) for a in adj]
    cand = {}   # x -> plancher
    places = set()
    ncell = 0
    for a in range(len(L)):
        Na = [b for b in adjs[a] if b > a]
        for b in Na:
            Nab = [c for c in Na if c > b and c in adjs[b]]
            for c in Nab:
                for d in Nab:
                    if d > c and d in adjs[c]:
                        ncell += 1
                        C = frozenset((L[a], L[b], L[c], L[d]))
                        for y in cotes_par_algebre(list(C)):
                            if y in gen: continue
                            places.add(y)
                            if y not in cand and descente(C | {y}, y)[0] == C | {y}:
                                cand[y] = C
    return cand, len(places), ncell


def run(graine, gmax, strat='hasard'):
    rng = random.Random(graine); t0 = time.time()
    gen = {u: 0 for u in GERME}
    lignes = []
    for g in range(1, gmax + 1):
        cand, nplaces, ncell = candidats(gen)
        options = {p: [] for p in gen}
        for x, C in cand.items():
            for p in C: options[p].append(x)
        for p in options: options[p].sort()
        sans_option = sum(1 for p in options if not options[p])
        ordre = list(gen); rng.shuffle(ordre)
        if strat == 'adverse': ordre.sort(key=lambda p: -len(options[p]))
        prise = {}; fille = {}; bloques = 0
        for p in ordre:
            libres = [x for x in options[p] if x not in prise]
            if not libres: bloques += 1; continue
            if strat == 'adverse':   # prendre la fille la plus disputee (le plus de parents encore sans fille)
                x = max(libres, key=lambda y: (sum(1 for q in cand[y] if q not in fille and q != p), y))
            else:
                x = rng.choice(libres)
            prise[x] = p; fille[p] = x
        parfait = None
        if bloques:
            # completer par chemins augmentants
            def augmente(p, vu):
                for x in options[p]:
                    if x in vu: continue
                    vu.add(x)
                    if x not in prise or augmente(prise[x], vu):
                        prise[x] = p; fille[p] = x; return True
                return False
            sys.setrecursionlimit(100000)
            for p in ordre:
                if p not in fille: augmente(p, set())
            parfait = len(fille) == len(gen)
        lignes.append(dict(generation=g, constituants_avant=len(gen), cellules_nees=ncell, places_admissibles=nplaces,
                           filles_possibles=len(cand), constituants_sans_aucune_fille_possible=sans_option,
                           glouton_bloque_pour=bloques, couplage_parfait_trouve_apres_blocage=parfait))
        if len(fille) != len(gen):
            return dict(graine=graine, arret='aucun couplage parfait', par_generation=lignes, duree_s=round(time.time() - t0, 1))
        for p, x in fille.items():
            assert pr(p, x) == -1 and x not in gen
        for x in fille.values(): gen[x] = g
    L = sorted(gen); over, _ = gram_check(L)
    return dict(graine=graine, strategie=strat, tailles_finales=len(gen), chevauchements=over, par_generation=lignes, duree_s=round(time.time() - t0, 1))


if __name__ == '__main__':
    a, b, gmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    strat = sys.argv[4] if len(sys.argv) > 4 else 'hasard'
    for s in range(a, b + 1):
        print(json.dumps(run(s, gmax, strat), ensure_ascii=False), flush=True)
