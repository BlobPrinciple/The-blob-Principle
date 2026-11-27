# A. Paliers par la regle a la lettre ; T15 sur toutes les paires liees ; controle independant par parcours en largeur des tuiles.
import sys, time
from noyau import *

t0 = time.time()
NP = int(sys.argv[1]) if len(sys.argv) > 1 else 4

def cotes(cell):
    rows = [gram_ligne(c) for c in cell]
    ker = noyau_lineaire(rows)
    assert len(ker) == 1
    n0 = ker[0]
    nn = ip(n0, n0)
    k2 = F(12) / nn
    # racine rationnelle
    from math import isqrt
    a, b = k2.numerator, k2.denominator
    ra, rb = isqrt(a), isqrt(b)
    assert ra * ra == a and rb * rb == b, "normale non rationnelle"
    n = tuple(F(ra, rb) * c for c in n0)
    s = add(*cell)
    t1 = tuple((x + y) / 2 for x, y in zip(s, n)); t2 = tuple((x - y) / 2 for x, y in zip(s, n))
    out = []
    for t in (t1, t2):
        assert all(c.denominator == 1 for c in t)
        t = tuple(int(c) for c in t)
        assert ip(t, t) == 1 and all(ip(t, c) == -1 for c in cell)
        out.append(t)
    return out

S = set(GERME)
palier = {u: 0 for u in GERME}
tailles = [len(S)]
for n in range(NP):
    L = sorted(S)
    voisins = {u: set() for u in L}
    for u, v in combinations(L, 2):
        if ip(u, v) == -1:
            voisins[u].add(v); voisins[v].add(u)
    nouveaux = set()
    idx = {u: i for i, u in enumerate(L)}
    for a in L:
        Na = sorted((v for v in voisins[a] if idx[v] > idx[a]), key=idx.get)
        for b in Na:
            Nab = [v for v in Na if idx[v] > idx[b] and v in voisins[b]]
            for c in Nab:
                Nabc = [v for v in Nab if idx[v] > idx[c] and v in voisins[c]]
                for d in Nabc:
                    for t in cotes((a, b, c, d)):
                        if t not in S:
                            nouveaux.add(t)
    for t in nouveaux:
        palier[t] = n + 1
    S |= nouveaux
    tailles.append(len(S))
print("tailles des paliers S(0..%d) :" % NP, tailles, " (%.1f s)" % (time.time() - t0))

# Tuiles-portes par descente gloutonne ; tuile de depart : celle de la cellule de naissance n'est pas gardee,
# on la retrouve : pour u, une tuile contenant u = parcours en largeur des tuiles.
# Parcours en largeur des tuiles jusqu'a la longueur LMAX (longueur exacte = distance dans le graphe des tuiles).
LMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 9
dist = {GERME: 0}
front = [GERME]
for l in range(1, LMAX + 1):
    nf = []
    for t in front:
        for j in range(5):
            t2 = flip(t, j)
            if t2 not in dist:
                dist[t2] = l; nf.append(t2)
    front = nf
print("tuiles de longueur <= %d : %d (%.1f s)" % (LMAX, len(dist), time.time() - t0))

# controle : la longueur par descente des sommes = distance du parcours
mauv = sum(1 for t, l in dist.items() if longueur(t) != l)
print("controle longueur (descente des sommes) = distance du parcours : %d desaccords" % mauv)

# minima : par constituant et par paire
best1 = {}; best2 = {}
for t, l in dist.items():
    for u in t:
        b = best1.get(u)
        if b is None or l < b[0]: best1[u] = [l, t, 1]
        elif l == b[0]: b[2] += 1
    for u, v in combinations(t, 2):
        k = (u, v) if u < v else (v, u)
        b = best2.get(k)
        if b is None or l < b[0]: best2[k] = [l, t, 1]
        elif l == b[0]: b[2] += 1

manque1 = [u for u in S if u not in best1]
print("constituants de S(%d) absents du parcours : %d" % (NP, len(manque1)))
# il faut aussi que la longueur minimale soit atteinte : si u apparait, sa porte (plus courte) apparait aussi.
nonuniq1 = sum(1 for u in S if u in best1 and best1[u][2] != 1)
print("portes non uniques : %d" % nonuniq1)
# accord avec la descente gloutonne du carnet
desacc = 0
for u in S:
    if u in best1:
        g, _ = porte(u, best1[u][1])
        # partir d'une autre tuile contenant u : la plus longue connue
    # (on teste aussi depuis une tuile quelconque ci-dessous)
for u in S:
    if u not in best1: continue
    # une tuile contenant u, prise loin : on remonte la plus longue tuile du parcours contenant u
    pass

Lst = sorted(S)
paires = [(u, v) for u, v in combinations(Lst, 2) if ip(u, v) == -1]
print("paires liees dans S(%d) : %d" % (NP, len(paires)))
cas = {'germe': 0, 'T0=T(p)': 0, 'T0=T(q)': 0, 'T0=T(p)=T(q)': 0, 'aucune, forme annoncee': 0, 'aucune, autre forme': 0,
       'T15 faux': 0, 'paire absente': 0, 'T0 non unique': 0, 'glouton != parcours': 0}
germe = set(GERME)
for p, q in paires:
    k = (p, q) if p < q else (q, p)
    if k not in best2:
        cas['paire absente'] += 1; continue
    l0, T0, nb = best2[k]
    if nb != 1: cas['T0 non unique'] += 1
    # T0 par glouton depuis une tuile quelconque contenant p,q : depuis T0 lui-meme c'est trivial ;
    # on part de T0 retourne loin (marche dans le residu) puis on redescend
    Tp = best1[p][1]; Tq = best1[q][1]
    autres = [u for u in T0 if u not in (p, q)]
    inp = all(u in Tp for u in autres); inq = all(u in Tq for u in autres)
    if not (inp or inq): cas['T15 faux'] += 1
    if p in germe and q in germe: cas['germe'] += 1
    sp, sq = (set(T0) == set(Tp)), (set(T0) == set(Tq))
    if sp and sq: cas['T0=T(p)=T(q)'] += 1
    elif sp: cas['T0=T(p)'] += 1
    elif sq: cas['T0=T(q)'] += 1
    else:
        ok = False
        for (x, y, Tx) in ((p, q, Tp), (q, p, Tq)):
            # T(x) = {x, y', a, b, c} avec y' l'autre cote de la cellule {x, a, b, c}
            yp = sub(add(x, *autres), y)
            if set(Tx) == set([x, yp] + autres): ok = True
        cas['aucune, forme annoncee' if ok else 'aucune, autre forme'] += 1
    if p in germe and q not in germe and set(T0) != set(Tq): cas['T15 faux'] += 1
    if q in germe and p not in germe and set(T0) != set(Tp): cas['T15 faux'] += 1
print(cas)

# glouton (definition du carnet) contre parcours, pour les portes et pour T0, depuis des tuiles eloignees
rng = random.Random(1)
dg = 0; dg2 = 0; ess = 0
for u in Lst:
    if u not in best1: continue
    T = best1[u][1]
    for _ in range(3):
        # s'eloigner dans le residu de u
        t = T
        for __ in range(rng.randint(1, 6)):
            j = rng.choice([j for j in range(5) if t[j] != u]); t = flip(t, j)
        g, _ = porte(u, t)
        ess += 1
        if set(g) != set(best1[u][1]): dg += 1
for p, q in paires[:4000]:
    k = (p, q) if p < q else (q, p)
    if k not in best2: continue
    T = best2[k][1]
    t = T
    for __ in range(rng.randint(1, 6)):
        j = rng.choice([j for j in range(5) if t[j] not in (p, q)]); t = flip(t, j)
    g, _ = porte(p, t, fixes=[p, q])
    if set(g) != set(T): dg2 += 1
print("glouton du carnet vs parcours : portes %d desaccords sur %d essais ; T0 %d desaccords sur %d" % (dg, ess, dg2, min(4000, len(paires))))
print("temps total %.1f s" % (time.time() - t0))
