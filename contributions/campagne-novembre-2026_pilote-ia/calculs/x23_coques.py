#!/usr/bin/env python3
"""X-23, parties A et C -- la regle de l'etage sur les coques fermees.
Coque fermee de rang k = sphere simpliciale de dimension k. Mitose de l'arete (C-116) = le porteur nait sur un lien, chaque cellule qui porte ce lien se divise en deux.
On mesure, a chaque naissance, (mecanismes, auto-contraintes) aux etages d = 1 ... k+2, par deux lectures independantes du rang (flottant et exact modulo 2^31 - 1).
Prediction scellee : x23_regle_de_l_etage_prediction.txt (SHA-256 7c80008d46d64a9776a1a4c092cfb80c0e6bd1b83f9480f02ae7d266f00bb5a1). Claude, 22 novembre 2026."""
import itertools, json, sys, time
import numpy as np
from scipy.spatial import ConvexHull
from x23_outils import liens_des_cellules, etage, analyse_exacte

SORTIE = {}


def bord_du_simplexe(k):
    """Plus petite coque fermee de rang k : le bord du simplexe de dimension k+1 (k+2 sommets)."""
    return [frozenset(c) for c in itertools.combinations(range(k + 2), k + 1)], k + 2


def est_fermee(cellules, k):
    """Chaque face de dimension k-1 appartient a exactement deux cellules."""
    cpt = {}
    for F in cellules:
        for x in F:
            g = F - {x}
            cpt[g] = cpt.get(g, 0) + 1
    return all(v == 2 for v in cpt.values())


def autour(cellules, a, b):
    """Nombre de sommets qui entourent le lien (a, b) = sommets de son entourage."""
    s = set()
    for F in cellules:
        if a in F and b in F:
            s |= F
    return len(s) - 2


def mitose_arete(cellules, a, b, w):
    out = []
    for F in cellules:
        if a in F and b in F:
            out.append((F - {a}) | {w})
            out.append((F - {b}) | {w})
        else:
            out.append(F)
    return out


def naissance_en_volume(cellules, i, w):
    F = cellules[i]
    out = cellules[:i] + cellules[i + 1:]
    for x in F:
        out.append((F - {x}) | {w})
    return out


def retournement(cellules, rng):
    """Rang 2 seulement : retourne un lien (a, b) porte par les triangles (a, b, x) et (a, b, y) si (x, y) n'est pas deja un lien."""
    liens = liens_des_cellules(cellules)
    ens = set(liens)
    for _ in range(200):
        a, b = liens[rng.integers(len(liens))]
        tri = [F for F in cellules if a in F and b in F]
        if len(tri) != 2:
            continue
        (x,) = tuple(tri[0] - {a, b})
        (y,) = tuple(tri[1] - {a, b})
        if (min(x, y), max(x, y)) in ens:
            continue
        reste = [F for F in cellules if not (a in F and b in F)]
        return reste + [frozenset({a, x, y}), frozenset({b, x, y})]
    return cellules


def mesure(n, cellules, etages, rng, exact=True):
    liens = liens_des_cellules(cellules)
    out = {}
    for d in etages:
        if n < d + 1:
            continue
        r = etage(n, liens, d, rng, exact=exact)
        out[d] = r
    return liens, out


# ------------------------------------------------------------------ A2, A3, A4 : mitose de l'arete, rangs 1 a 4
def epreuve_mitose(k, naissances, graine, choix='uniforme'):
    rng = np.random.default_rng(1000 * k + graine)
    cellules, n = bord_du_simplexe(k)
    histo = []
    somme_exces = 0
    violations = []
    for t in range(naissances + 1):
        exact = (t % 5 == 0) or (t == naissances)
        liens, m = mesure(n, cellules, range(1, k + 3), rng, exact=exact)
        E = len(liens)
        assert est_fermee(cellules, k)
        ligne = dict(t=t, V=n, E=E, somme_des_exces=somme_exces)
        for d, r in m.items():
            ligne[f'etage{d}'] = [r['mecanismes'], r['auto_contraintes']]
            if exact and not r['accord']:
                violations.append(('rang exact different du rang flottant', k, t, d, r['rang'], r['rang_exact']))
        # emboitement A1 : rigide a l'etage d => rigide a l'etage d-1
        for d in sorted(m):
            if d - 1 in m and m[d]['mecanismes'] == 0 and m[d - 1]['mecanismes'] != 0:
                violations.append(('emboitement', k, t, d))
        # attendus
        if k == 1:
            att = {1: (0, 1), 2: (n - 3, 0)}
        elif k == 2:
            att = {2: (0, n - 3), 3: (0, 0), 4: (n - 4, 0)}
        else:
            att = {k + 1: (0, E - (k + 1) * n + (k + 1) * (k + 2) // 2)}
            if choix != 'en_volume' and E - (k + 1) * n + (k + 1) * (k + 2) // 2 != somme_exces:
                violations.append(('somme des exces', k, t, E, n, somme_exces))
        for d, (am, as_) in att.items():
            if d in m and (m[d]['mecanismes'], m[d]['auto_contraintes']) != (am, as_):
                violations.append(('attendu', k, t, d, (m[d]['mecanismes'], m[d]['auto_contraintes']), (am, as_)))
        histo.append(ligne)
        if t == naissances:
            break
        if choix == 'en_volume':
            i = int(rng.integers(len(cellules)))
            E_avant = E
            cellules = naissance_en_volume(cellules, i, n)
            n += 1
            continue
        if choix == 'uniforme':
            a, b = liens[rng.integers(len(liens))]
        else:
            ne = [autour(cellules, a, b) for a, b in liens]
            cible = min(ne) if choix == 'entourage_minimal' else max(ne)
            cands = [l for l, x in zip(liens, ne) if x == cible]
            a, b = cands[rng.integers(len(cands))]
        ne_ab = autour(cellules, a, b)
        cellules = mitose_arete(cellules, a, b, n)
        n += 1
        apport = len(liens_des_cellules(cellules)) - E
        if apport != 1 + ne_ab:
            violations.append(('apport', k, t, apport, ne_ab))
        somme_exces += ne_ab - k
    return histo, violations


def partie_A_mitose():
    res = {}
    plan = {1: 40, 2: 60, 3: 45, 4: 26}
    for k, T in plan.items():
        for choix in (['uniforme'] if k < 3 else ['uniforme', 'entourage_minimal', 'entourage_maximal']):
            for g in range(3):
                t0 = time.time()
                h, v = epreuve_mitose(k, T if choix == 'uniforme' else min(T, 30), g, choix)
                cle = f'rang{k}_{choix}_graine{g}'
                res[cle] = dict(violations=v, debut=h[0], fin=h[-1], trajectoire=[[x['t'], x['V'], x['E'], x.get(f'etage{k}'), x.get(f'etage{k+1}'), x.get(f'etage{k+2}')] for x in h])
                print(cle, 'violations', len(v), '| fin : V', h[-1]['V'], 'E', h[-1]['E'], {q: h[-1][q] for q in h[-1] if q.startswith('etage')}, f'{time.time()-t0:.0f}s', flush=True)
    return res


def partie_A_volume():
    res = {}
    for k in (1, 2, 3, 4):
        for g in range(2):
            h, v = epreuve_mitose(k, 30, 50 + g, 'en_volume')
            fin = h[-1]
            juste = all(x[f'etage{k+1}'] == [0, 0] for x in h)
            res[f'rang{k}_graine{g}'] = dict(juste_a_chaque_pas_a_l_etage_k_plus_1=juste, fin=fin, violations=v)
            print('naissance en volume, rang', k, 'graine', g, ': juste a chaque pas a l\'etage', k + 1, ':', juste, '| fin', {q: fin[q] for q in fin if q.startswith('etage')}, flush=True)
    return res


# ------------------------------------------------------------------ A6 : toutes les coques
def enveloppe(nb, dim, rng):
    """Enveloppe convexe de nb points tires sur la sphere unite de R^dim : une sphere simpliciale de rang dim-1."""
    x = rng.standard_normal((nb, dim))
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    h = ConvexHull(x)
    assert len(h.vertices) == nb
    return [frozenset(int(v) for v in s) for s in h.simplices]


def partie_A6():
    res = {}
    rng = np.random.default_rng(606)
    for nb in (12, 30, 80, 200):
        c = enveloppe(nb, 3, rng)
        assert est_fermee(c, 2)
        liens, m = mesure(nb, c, (2, 3, 4), rng)
        res[f'rang2_enveloppe_{nb}'] = dict(V=nb, E=len(liens), **{f'etage{d}': [r['mecanismes'], r['auto_contraintes'], r['accord']] for d, r in m.items()})
        print('enveloppe rang 2, V =', nb, 'E =', len(liens), {d: (r['mecanismes'], r['auto_contraintes'], r['accord']) for d, r in m.items()}, flush=True)
    # retournements d'aretes sur une coque de rang 2 nee par mitose
    cellules, n = bord_du_simplexe(2)
    for t in range(40):
        liens = liens_des_cellules(cellules)
        a, b = liens[rng.integers(len(liens))]
        cellules = mitose_arete(cellules, a, b, n); n += 1
    tous_justes = True
    for t in range(300):
        cellules = retournement(cellules, rng)
        if t % 20 == 19:
            assert est_fermee(cellules, 2)
            liens, m = mesure(n, cellules, (3,), rng, exact=(t % 100 == 99))
            tous_justes &= (m[3]['mecanismes'], m[3]['auto_contraintes']) == (0, 0)
    res['rang2_300_retournements'] = dict(V=n, juste_a_l_etage_3_a_chaque_controle=bool(tous_justes))
    print('rang 2, 300 retournements, V =', n, ': juste a l\'etage 3 a chaque controle :', tous_justes, flush=True)
    for nb in (12, 30, 60):
        c = enveloppe(nb, 4, rng)
        assert est_fermee(c, 3)
        liens, m = mesure(nb, c, (3, 4, 5, 6), rng)
        E = len(liens)
        res[f'rang3_enveloppe_{nb}'] = dict(V=nb, E=E, attendu_etage4=[0, E - 4 * nb + 10], **{f'etage{d}': [r['mecanismes'], r['auto_contraintes'], r['accord']] for d, r in m.items()})
        print('enveloppe rang 3, V =', nb, 'E =', E, 'attendu etage 4 :', (0, E - 4 * nb + 10), {d: (r['mecanismes'], r['auto_contraintes'], r['accord']) for d, r in m.items()}, flush=True)
    return res


# ------------------------------------------------------------------ A7 : budget de liens sous mitose uniforme (comptage seul, grandes tailles)
def budget(k, V_final, graine, releves):
    rng = np.random.default_rng(7000 + 10 * k + graine)
    cellules, n = bord_du_simplexe(k)
    cel = {i: F for i, F in enumerate(cellules)}
    prochain = len(cel)
    par_sommet = {}
    for i, F in cel.items():
        for x in F:
            par_sommet.setdefault(x, set()).add(i)
    liens = liens_des_cellules(cellules)
    pos_lien = {l: i for i, l in enumerate(liens)}
    out = []
    while True:
        if n in releves:
            E = len(liens)
            ech = [liens[i] for i in rng.integers(len(liens), size=min(4000, len(liens)))]
            moy = float(np.mean([len(set().union(*[cel[i] for i in (par_sommet[a] & par_sommet[b])])) - 2 for a, b in ech])) if k >= 2 else 0.0
            out.append(dict(V=n, E=E, liens_par_constituant=E / n, entourage_moyen=moy, cellules=len(cel)))
        if n >= V_final:
            break
        a, b = liens[rng.integers(len(liens))]
        ids = par_sommet[a] & par_sommet[b]
        entourage = set()
        w = n
        par_sommet[w] = set()
        for i in ids:
            F = cel.pop(i)
            entourage |= F
            for x in F:
                par_sommet[x].discard(i)
            for retire in (a, b):
                G = (F - {retire}) | {w}
                cel[prochain] = G
                for x in G:
                    par_sommet[x].add(prochain)
                prochain += 1
        entourage -= {a, b}
        # liens : (a, b) disparait ; (a, w), (b, w), (w, x) apparaissent
        i = pos_lien.pop((a, b))
        dernier = liens.pop()
        if i < len(liens):
            liens[i] = dernier
            pos_lien[dernier] = i
        for x in [a, b] + sorted(entourage):
            l = (x, w)
            pos_lien[l] = len(liens)
            liens.append(l)
        n += 1
    return out


def partie_A7():
    res = {}
    plan = {1: 20000, 2: 20000, 3: 20000, 4: 12000, 5: 3000}
    for k, Vf in plan.items():
        for g in range(2 if k < 5 else 3):
            t0 = time.time()
            rel = sorted({Vf // 8, Vf // 4, Vf // 2, Vf})
            r = budget(k, Vf, g, rel)
            res[f'rang{k}_graine{g}'] = r
            print('budget rang', k, 'graine', g, [(x['V'], round(x['liens_par_constituant'], 3), round(x['entourage_moyen'], 3)) for x in r], 'limite predite', k * (k + 1) // 2, f'{time.time()-t0:.0f}s', flush=True)
    return res


# ------------------------------------------------------------------ C : jusqu'ou tient un tissu ne par mitose de l'arete
def partie_C():
    res = {}
    for nom, depart in (('sphere_rang3', bord_du_simplexe(3)), ('boule_de_tetraedres', ([frozenset({0, 1, 2, 3})], 4))):
        for g in range(2):
            rng = np.random.default_rng(9000 + g + (0 if nom.startswith('s') else 50))
            cellules, n = depart
            cellules = list(cellules)
            while n < 300:
                liens = liens_des_cellules(cellules)
                a, b = liens[rng.integers(len(liens))]
                cellules = mitose_arete(cellules, a, b, n); n += 1
            liens = liens_des_cellules(cellules)
            E = len(liens)
            ligne = dict(V=n, E=E, liens_par_constituant=E / n, cellules=len(cellules))
            for d in (3, 4, 5, 6, 7):
                r = analyse_exacte(n, liens, d, rng)             # rang et amas en arithmetique exacte (la lecture flottante des amas s'est revelee non fiable)
                re = etage(n, liens, d, rng, exact=True)         # second tirage independant : rang flottant et rang exact
                ligne[f'etage{d}'] = dict(mecanismes=r['mecanismes'], auto_contraintes=r['auto_contraintes'], part_plus_grand_amas=r['part_plus_grand_amas'],
                                          part_figee=r['part_figee'], accord_rang_exact=bool(re['rang_exact'] == r['rang']), rang_flottant_identique=bool(re['rang'] == r['rang']),
                                          maxwell=d * n - d * (d + 1) // 2 - E)
            res[f'{nom}_graine{g}'] = ligne
            print(nom, 'graine', g, 'V', n, 'E', E, 'liens/constituant', round(E / n, 3), {d: (ligne[f'etage{d}']['mecanismes'], ligne[f'etage{d}']['auto_contraintes'], round(ligne[f'etage{d}']['part_plus_grand_amas'], 3), ligne[f'etage{d}']['accord_rang_exact']) for d in (3, 4, 5, 6, 7)}, flush=True)
    return res


if __name__ == '__main__':
    quoi = sys.argv[1:] or ['mitose', 'volume', 'A6', 'A7', 'C']
    fichier = 'x23_coques.json'
    try:
        SORTIE = json.load(open(fichier))
    except Exception:
        SORTIE = {}
    for q in quoi:
        t0 = time.time()
        print('=====', q, flush=True)
        SORTIE[q] = {'mitose': partie_A_mitose, 'volume': partie_A_volume, 'A6': partie_A6, 'A7': partie_A7, 'C': partie_C}[q]()
        json.dump(SORTIE, open(fichier, 'w'), indent=1, default=str)
        print(f'===== {q} termine en {time.time()-t0:.0f}s', flush=True)
