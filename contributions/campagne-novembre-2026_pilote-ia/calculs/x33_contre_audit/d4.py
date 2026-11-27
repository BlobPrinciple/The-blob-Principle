"""D4 : la regle << chacun garde ses deux filles propres auxquelles aucune autre candidate de la generation n'est liee >>,
depuis deux tournois en miroir ; et (mode hasard) choix au hasard sous la condition. Contre-exemple cherche a T32 point 3 :
un lien entre candidates dont les proprietaires ne sont pas soeurs."""
import json, sys, time, itertools, random
from alib import *
from rule import *

mode = sys.argv[1]
G_MAX = int(sys.argv[2])
t0 = time.time()
P = Pack()
for v in GERM:
    P.gate_of(M[v], GERMSET - {v} | {M[v]})


def Xvw(v, w):
    T = P.T[M[v]]
    x = other(T, w)
    P.gate_of(x, flip(T, w))
    return x


def grow(beats, choose, gmax, stats):
    gen = {u: 0 for u in GERM}
    for v in GERM: gen[M[v]] = 1
    for v, w in beats: gen[Xvw(v, w)] = 2
    for h in range(3, gmax + 1):
        owners = [c for c in gen if gen[c] == h - 1]
        cand = []
        for c in owners:
            for x, f in P.proper_daughters(c):
                P.gate_of(x, flip(P.T[c], f))
                cand.append((c, x, f))
        L = [x for _, x, _ in cand]
        assert len(set(L)) == len(L)
        lk, over, adj = adjacency(L)
        stats['chevauchements_entre_candidates'] += over
        mom = {c: proper_mother(P, c) for c in owners}
        for i, j in lk:
            ci, cj = cand[i][0], cand[j][0]
            if not (len(mom[ci]) == 1 and mom[ci] == mom[cj] and ci != cj):
                stats['liens_entre_candidates_de_non_soeurs'] += 1
        stats['liens_entre_candidates'] += len(lk)
        keep = choose(owners, cand, adj, mom)
        for x in keep:
            gen[x] = h
    return gen


def choose_safe(stats):
    def f(owners, cand, adj, mom):
        keep = []
        by = {}
        for i, (c, x, ff) in enumerate(cand):
            by.setdefault(c, []).append(i)
        for c in owners:
            ok = [i for i in by[c] if not adj[i]]
            if len(by[c]) != 3: stats['meres_sans_trois_filles_propres'] += 1
            if len(ok) != 2: stats['meres_sans_deux_filles_sures'] += 1
            keep += [cand[i][1] for i in ok]
        return keep
    return f


def choose_random(stats, rng):
    def f(owners, cand, adj, mom):
        by = {}
        for i, (c, x, ff) in enumerate(cand):
            by.setdefault(c, []).append(i)
        # paires de soeurs
        sis = {}
        for c in owners:
            sis.setdefault(mom[c][0], []).append(c)
        keep = []
        for q, cs in sis.items():
            assert len(cs) == 2
            a, b = cs
            ways = []
            for ka in itertools.combinations(by[a], 2):
                for kb in itertools.combinations(by[b], 2):
                    sel = set(ka) | set(kb)
                    if all(not (adj[i] & sel) for i in sel):
                        ways.append(sel)
            stats['facons_permises'][str(len(ways))] = stats['facons_permises'].get(str(len(ways)), 0) + 1
            if not ways:
                stats['blocages'] += 1; continue
            keep += [cand[i][1] for i in rng.choice(ways)]
        return keep
    return f


def analyse(gen, name):
    L = sorted(gen)
    links, over, adj = adjacency(L)
    r = dict(tissu=name, constituants=len(L), tailles=[sum(1 for u in gen if gen[u] <= h) for h in range(G_MAX + 1)],
             liens=len(links), chevauchements=over, liens_germe=0, liens_parent_enfant=0, liens_meme_gen_hors_germe=0, liens_autres=0)
    for i, j in links:
        p, q = L[i], L[j]
        if p in GERMSET and q in GERMSET: r['liens_germe'] += 1
        elif p in P.floor(q) or q in P.floor(p): r['liens_parent_enfant'] += 1
        elif gen[p] == gen[q]: r['liens_meme_gen_hors_germe'] += 1
        else: r['liens_autres'] += 1
    deg = {}
    for i, u in enumerate(L):
        deg.setdefault(gen[u], set()).add(len(adj[i]))
    r['voisins_selon_la_generation'] = {str(k): sorted(v) for k, v in sorted(deg.items())}
    S = frozenset(L)
    st = [p for p in PERMS if frozenset(act(p, u) for u in L) == S]
    r['symetries_du_germe_conservant'] = len(st)
    r['dont_impaires'] = sum(1 for p in st if sign(p) == -1)
    r['types_de_cycles'] = sorted(set(cycle_type(p) for p in st))
    r['plus_grande_coordonnee'] = max(abs(c) for u in L for c in u)
    return r, S, L, adj


if mode == 'regle':
    stats = dict(chevauchements_entre_candidates=0, liens_entre_candidates=0, liens_entre_candidates_de_non_soeurs=0,
                 meres_sans_trois_filles_propres=0, meres_sans_deux_filles_sures=0)
    A = [(GERM[i], GERM[(i + 1) % 5]) for i in range(5)] + [(GERM[i], GERM[(i + 2) % 5]) for i in range(5)]
    sw = (1, 0, 2, 3, 4)
    B = [(act(sw, v), act(sw, w)) for v, w in A]
    out = {}
    for name, beats in (('A', A), ('B', B)):
        gen = grow(beats, choose_safe(stats), G_MAX, stats)
        r, S, L, adj = analyse(gen, name)
        out[name] = (S, gen, L, adj)
        print(json.dumps(r), flush=True)
    SA, SB = out['A'][0], out['B'][0]
    maps = [p for p in PERMS if frozenset(act(p, u) for u in SA) == SB]
    print(json.dumps(dict(bilan=True, **stats, symetries_A_vers_B=len(maps), dont_paires=sum(1 for p in maps if sign(p) == 1),
                          communs_A_B=len(SA & SB), duree_s=round(time.time() - t0, 1))), flush=True)
    # cellules a la generation 8 (ou G_MAX si plus petit) dans A
    g8 = min(8, G_MAX)
    genA = out['A'][1]
    L = sorted(u for u in genA if genA[u] <= g8)
    links, over, adj = adjacency(L)
    cl = cliques4(L, adj)
    c_le1 = [c for c in cl if sum(1 for i in c if L[i] in GERMSET) <= 1]
    four = sum(1 for c in c_le1 if len(set(genA[L[i]] for i in c)) == 4)
    # chaque cellule est-elle une cellule de T(x) contenant x, x le plus jeune ?
    struct = 0
    for c in cl:
        us = [L[i] for i in c]
        if all(u in GERMSET for u in us): struct += 1; continue
        y = max(us, key=lambda u: genA[u])
        if set(us) - {y} <= P.floor(y): struct += 1
    print(json.dumps(dict(partie='cellules', generation=g8, constituants=len(L), cellules=len(cl), attendu=5 + 4 * (len(L) - 5),
                          cellules_au_plus_un_du_germe=len(c_le1), dont_quatre_ages=four, cellules_de_la_forme_annoncee=struct,
                          cellules_trois_ages_ou_moins_avec_deux_du_germe=sum(1 for c in cl if sum(1 for i in c if L[i] in GERMSET) >= 2 and len(set(genA[L[i]] for i in c)) < 4))), flush=True)
    # symetrie cachee : degres du germe uniques ?
    SAs, genA_, LA, adjA = out['A']
    degs = sorted(((len(adjA[i]), genA_[u]) for i, u in enumerate(LA)), reverse=True)[:7]
    print(json.dumps(dict(partie='degres_max_tissu_A', sept_plus_grands_degres_et_generation=degs)), flush=True)

elif mode == 'hasard':
    a, b = map(int, sys.argv[3:5])
    stats = dict(chevauchements_entre_candidates=0, liens_entre_candidates=0, liens_entre_candidates_de_non_soeurs=0,
                 facons_permises={}, blocages=0)
    # les 24 tournois reguliers
    E = list(itertools.combinations(range(5), 2))
    tours = []
    for bits in range(1 << 10):
        beats = [(GERM[i], GERM[j]) if bits >> k & 1 else (GERM[j], GERM[i]) for k, (i, j) in enumerate(E)]
        sc = {}
        for v, w in beats: sc[v] = sc.get(v, 0) + 1
        if all(sc.get(v, 0) == 2 for v in GERM): tours.append(beats)
    res = []
    for seed in range(a, b + 1):
        rng = random.Random(1000 + seed)
        gen = grow(rng.choice(tours), choose_random(stats, rng), G_MAX, stats)
        L = sorted(gen)
        links, over, adj = adjacency(L)
        nsame = sum(1 for i, j in links if gen[L[i]] == gen[L[j]] and not (L[i] in GERMSET and L[j] in GERMSET))
        res.append(dict(graine=seed, constituants=len(L), liens=len(links), meme_gen_hors_germe=nsame, chevauchements=over))
    print(json.dumps(dict(partie='D4-hasard', tournois_reguliers=len(tours), generations=G_MAX, tirages=res, **stats,
                          duree_s=round(time.time() - t0, 1))))
