"""Contre-audit X-32, partie T28 : la regle, ecrite independamment, avec plusieurs strategies de choix.
Usage : python3 t28.py STRATEGIE GRAINE_DEBUT GRAINE_FIN GENERATIONS [depart]
STRATEGIE : hasard | premier | dernier | priver_mere | priver_fille | adverse
depart : 'hasard' (derangement tire avec la graine) ou un entier 0..43 (indice du derangement dans l'ordre lexicographique)."""
import itertools, json, random, sys, time
from collections import Counter
from commun import *

DERANG = [p for p in itertools.permutations(range(5)) if all(p[i] != i for i in range(5))]
assert len(DERANG) == 44


TISSUS = []
def run(strategie, graine, gmax, depart):
    rng = random.Random(graine)
    t0 = time.time()
    gen = {u: 0 for u in GERME}
    porte = {u: GERME_SET for u in GERME}
    derniere = {}; choisi_par = {}
    err = Counter(); stats = Counter()
    fp_cache = {}

    def filles_propres(c):
        """Filles propres de c : x cote au-dela d'une cellule de T(c) contenant c, dont la tuile-porte (descente) est cette cellule + x."""
        if c in fp_cache: return fp_cache[c]
        T = porte[c]; out = []
        for f in T:
            if f == c: continue
            Ci = T - {f}; x = autre_cote(list(Ci), f)
            if descente(Ci | {x}, x)[0] == Ci | {x}: out.append((x, Ci))
        fp_cache[c] = out
        return out

    # generation 1
    perm = DERANG[rng.randrange(44)] if depart == 'hasard' else DERANG[int(depart)]
    demandes = []
    for i, u in enumerate(GERME):
        v = GERME[perm[i]]
        Ci = GERME_SET - {v}; x = autre_cote(list(Ci), v)
        demandes.append((u, [(x, Ci)]))
    tailles = [5]
    g = 1
    while True:
        # --- choix ---
        if strategie == 'hasard':
            ordre = demandes[:]; rng.shuffle(ordre)
        elif strategie in ('premier', 'dernier'):
            ordre = sorted(demandes, key=lambda d: d[0])
        elif strategie == 'priver_mere':      # les nouvelles-nees choisissent d'abord
            ordre = sorted(demandes, key=lambda d: (gen[d[0]] != g - 1, d[0]))
        elif strategie == 'priver_fille':     # les anciennes choisissent d'abord
            ordre = sorted(demandes, key=lambda d: (gen[d[0]] == g - 1, d[0]))
        elif strategie == 'adverse':          # les plus riches d'abord, et prendre ce qui prive le plus les autres
            ordre = sorted(demandes, key=lambda d: (-len(d[1]), d[0]))
        pris = set(); naissances = []
        restant = Counter(x for _, opts in demandes for x, _ in opts)
        for p, opts in ordre:
            for x, _ in opts: restant[x] -= 1
            libres = [(x, Ci) for x, Ci in sorted(opts) if x not in pris and x not in gen]
            if g >= 2:
                stats[('options_libres_au_moment_du_choix', 'nouvelle' if gen[p] == g - 1 else 'ancienne', len(libres))] += 1
            if not libres:
                err['blocage'] += 1; return dict(strategie=strategie, graine=graine, depart=depart, bloque_a_la_generation=g, erreurs=dict(err))
            if strategie == 'hasard': x, Ci = rng.choice(libres)
            elif strategie == 'dernier': x, Ci = libres[-1]
            elif strategie in ('priver_mere', 'priver_fille', 'adverse'):
                x, Ci = max(libres, key=lambda o: (restant[o[0]], o[0]))
            else: x, Ci = libres[0]
            pris.add(x); naissances.append((p, x, Ci))
        # --- controles de chaque naissance ---
        for p, x, Ci in naissances:
            if x in gen: err['deja_nee'] += 1
            if not all(v in gen for v in Ci): err['plancher_non_ne'] += 1
            if pr(x, p) != -1: err['non_liee_a_la_mere'] += 1
            if p not in Ci: err['mere_hors_du_plancher'] += 1
            Cl = list(Ci)
            if any(pr(Cl[i], Cl[j]) != -1 for i in range(4) for j in range(i + 1, 4)): err['plancher_pas_une_cellule'] += 1
            if pr(x, x) != 1 or any(pr(x, v) != -1 for v in Cl): err['pas_un_cote'] += 1
            if autre_cote(Cl, x) not in gen: err['autre_cote_non_ne'] += 1
            # tuile-porte recalculee par descente depuis une tuile eloignee
            t = list(Ci | {x})
            for _ in range(4):
                j = rng.choice([k for k in range(5) if t[k] != x]); S = add(*t); t[j] = tuple(S[k] - 2 * t[j][k] for k in range(5))
            G, pas = descente(t, x)
            if G != Ci | {x}: err['porte_differente_du_plancher_plus_x'] += 1
        if len(set(x for _, x, _ in naissances)) != len(naissances): err['doublon'] += 1
        for p, x, Ci in naissances:
            gen[x] = g; porte[x] = Ci | {x}; derniere[p] = x; choisi_par[x] = p
        # mere propre unique (x hors palier 1) ; nombre de filles propres
        if g >= 2:
            for p, x, Ci in naissances:
                m = sum(1 for v in Ci if Ci <= porte[v])
                stats[('meres_propres', m)] += 1
        tailles.append(len(gen)); TISSUS.append(dict(gen))
        if g == gmax: break
        g += 1
        # --- demandes de la generation g ---
        demandes = []; groupes = {}
        for p in gen:
            if gen[p] == g - 1:
                opts = filles_propres(p); demandes.append((p, opts)); groupes.setdefault(p, []).append(p)
                stats[('filles_propres_de_la_nouvelle', len(opts))] += 1
            elif gen[p] < g - 1:
                c = derniere[p]
                opts = [(x, Ci) for x, Ci in filles_propres(c) if p in Ci]
                demandes.append((p, opts)); groupes.setdefault(c, []).append(p)
                stats[('options_de_l_ancienne', len(opts))] += 1
        # disjonction des groupes
        vu = {}
        for c, ps in groupes.items():
            for x, _ in filles_propres(c):
                if x in vu and vu[x] != c: err['fille_propre_de_deux_constituants'] += 1
                vu[x] = c
            if len(ps) != 2: err['groupe_de_taille_differente_de_2'] += 1
    # --- controles finaux ---
    L = sorted(gen)
    over, adj = gram_check(L)
    gl = [gen[u] for u in L]
    meme = [0] * (gmax + 1)
    for i, a in enumerate(adj):
        for j in a:
            if j > i and gl[i] == gl[j]: meme[gl[i]] += 1
    deg_nouv = Counter(len(adj[i]) for i in range(len(L)) if gl[i] == gmax)
    # clos par plancher : chaque constituant hors du germe a ses quatre parents nes (porte par descente)
    non_clos = sum(1 for u in L if gen[u] > 0 and not all(v in gen for v in descente(porte[u], u)[0] - {u}))
    return dict(strategie=strategie, graine=graine, depart=depart if depart != 'hasard' else ('hasard', DERANG.index(perm)),
                tailles=tailles, distincts=len(set(L)) == len(L), chevauchements=over, non_clos_par_plancher=non_clos,
                erreurs=dict(err), liens_meme_generation=meme, voisins_des_nouvelles_nees=dict(sorted(deg_nouv.items())),
                stats={'|'.join(map(str, k)): v for k, v in sorted(stats.items(), key=str)}, duree_s=round(time.time() - t0, 1))


if __name__ == '__main__':
    strat, a, b, gmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    depart = sys.argv[5] if len(sys.argv) > 5 else 'hasard'
    for s in range(a, b + 1):
        print(json.dumps(run(strat, s, gmax, depart), ensure_ascii=False), flush=True)
