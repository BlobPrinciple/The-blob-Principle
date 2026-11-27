"""D2 (generation 2, 6^5 tissus, symetries) et D3 (generation 3, 3^10 au-dessus de chacun des tissus sans lien)."""
import json, sys, time, itertools
from alib import *
from rule import *

t0 = time.time()
P = Pack()
for v in GERM:
    P.gate_of(M[v], GERMSET - {v} | {M[v]})
X = {}
for v in GERM:
    pd = P.proper_daughters(M[v])
    assert len(pd) == 4
    for x, f in pd:
        assert x == other(P.T[M[v]], f)
        X[(v, f)] = x
        P.gate_of(x, flip(P.T[M[v]], f))
iv = {v: i for i, v in enumerate(GERM)}
Xs = list(X.values())
assert len(set(Xs)) == 20
lk = set()
for a, b in itertools.combinations(X, 2):
    if ip(X[a], X[b]) == -1:
        lk.add(frozenset((a, b)))
form = all(a[0] == b[1] and a[1] == b[0] for a, b in map(tuple, lk))
over20 = sum(1 for a, b in itertools.combinations(Xs, 2) if ip(a, b) > -1)
links_pal1 = sum(1 for a, b in itertools.combinations(PAL1, 2) if ip(a, b) == -1)
# liens des X avec germe et palier 1 hors plancher
extra = 0
for k, x in X.items():
    for u in list(GERM) + list(PAL1):
        if ip(x, u) == -1 and u not in P.floor(x):
            extra += 1
pairs = {v: list(itertools.combinations([w for w in GERM if w != v], 2)) for v in GERM}
dist_links = {}
free = []
for ch in itertools.product(range(6), repeat=5):
    born = []
    for v, c in zip(GERM, ch):
        for w in pairs[v][c]:
            born.append((v, w))
    nl = sum(1 for a, b in itertools.combinations(born, 2) if frozenset((a, b)) in lk)
    dist_links[nl] = dist_links.get(nl, 0) + 1
    if nl == 0:
        free.append(frozenset(born))
# tournois reguliers
def is_regular_tournament(B):
    beats = {}
    seen = set()
    for v, w in B:
        if frozenset((v, w)) in seen:
            return False
        seen.add(frozenset((v, w)))
        beats[v] = beats.get(v, 0) + 1
    return len(seen) == 10 and all(beats.get(v, 0) == 2 for v in GERM)
all_tourn = all(is_regular_tournament(B) for B in free)
# nombre total de tournois reguliers etiquetes sur 5 points (independant)
nreg = 0
E = list(itertools.combinations(range(5), 2))
for bits in range(1 << 10):
    sc = [0] * 5
    for k, (i, j) in enumerate(E):
        sc[i if bits >> k & 1 else j] += 1
    if all(s == 2 for s in sc):
        nreg += 1
# symetries : action sur les vecteurs
def img(p, B):
    return frozenset(act(p, X[k]) for k in B)
vecsets = [frozenset(X[k] for k in B) for B in free]
idx = {s: i for i, s in enumerate(vecsets)}
def classes(perms):
    seen = set(); out = []
    for i, s in enumerate(vecsets):
        if i in seen: continue
        orb = set()
        for p in perms:
            t = frozenset(act(p, x) for x in s)
            assert t in idx
            orb.add(idx[t])
        seen |= orb; out.append(len(orb))
    return sorted(out)
even = [p for p in PERMS if sign(p) == 1]
stab = []
for s in vecsets:
    st = [p for p in PERMS if frozenset(act(p, x) for x in s) == s]
    stab.append((len(st), all(sign(p) == 1 for p in st), sorted(set(cycle_type(p) for p in st))))
res2 = dict(partie='D2', X_distincts=20, paires_liees_parmi_les_vingt=len(lk), forme_X_vw_X_wv=form, chevauchements_parmi_les_vingt=over20,
            liens_entre_les_cinq_du_palier_1=links_pal1, liens_des_X_avec_germe_ou_palier1_hors_plancher=extra,
            tissus=sum(dist_links.values()), tissus_par_nombre_de_liens_gen2=dict(sorted(dist_links.items())), sans_lien=len(free),
            sans_lien_tous_tournois_reguliers=all_tourn, tournois_reguliers_etiquetes_sur_5=nreg,
            classes_120=classes(PERMS), classes_60_paires=classes(even),
            stabilisateurs=sorted(set((a, b, tuple(c)) for a, b, c in stab)), duree_s=round(time.time() - t0, 1))
print(json.dumps(res2), flush=True)

# ---------------- D3
def tissue_d3(B):
    """Au-dessus du tissu B de la generation 2 (ensemble de cles (v,w)) : filles propres des dix nees."""
    born = set(GERM) | set(PAL1) | {X[k] for k in B}
    cands = {}
    for k in B:
        x = X[k]
        pd = P.proper_daughters(x)
        cands[k] = pd
        for y, f in pd:
            P.gate_of(y, flip(P.T[x], f))
    return born, cands
for ti, B in enumerate(sorted(free, key=lambda B: sorted(B))):
    t1 = time.time()
    born, cands = tissue_d3(B)
    three = all(len(c) == 3 for c in cands.values())
    allc = [(k, y, f) for k in cands for y, f in cands[k]]
    assert len(set(y for _, y, _ in allc)) == 30
    clk = [(a, b) for a, b in itertools.combinations(range(30), 2) if ip(allc[a][1], allc[b][1]) == -1]
    cover = sum(1 for a, b in itertools.combinations(range(30), 2) if ip(allc[a][1], allc[b][1]) > -1)
    bover = sum(1 for _, y, _ in allc for u in born if ip(y, u) > -1)
    blink_extra = sum(1 for _, y, _ in allc for u in born if ip(y, u) == -1 and u not in P.floor(y))
    # forme annoncee (T31 point 4) : soeurs c=X(v,a), chat=X(v,s) ; c laisse de cote a, chat laisse de cote s ;
    # la fille de c qui laisse de cote s est liee a la fille de chat qui laisse de cote a
    good = 0
    for a, b in clk:
        (k1, y1, f1), (k2, y2, f2) = allc[a], allc[b]
        if k1[0] == k2[0] and k1 != k2 and f1 == k2[1] and f2 == k1[1]:
            good += 1
    keys = sorted(cands)
    choices = {k: list(itertools.combinations(range(3), 2)) for k in keys}
    pos = {}
    for i, (k, y, f) in enumerate(allc):
        pos[(k, cands[k].index((y, f)))] = i
    clkset = set(clk)
    dist3 = {}
    same_thing = 0
    zero_by_pair = {}
    for ch in itertools.product(range(3), repeat=10):
        sel = []
        for k, c in zip(keys, ch):
            for j in choices[k][c]:
                sel.append(pos[(k, j)])
        nl = sum(1 for a, b in itertools.combinations(sorted(sel), 2) if (a, b) in clkset)
        dist3[nl] = dist3.get(nl, 0) + 1
        if nl == 0:
            # chaque soeur garde ses deux filles sans cousine possible
            risky = set()
            for a, b in clk: risky |= {a, b}
            if not (set(sel) & risky):
                same_thing += 1
    print(json.dumps(dict(partie='D3', tissu_de_depart=ti, trois_filles_propres_chacune=three, candidates=30, paires_liees=len(clk),
                          de_la_forme_annoncee=good, chevauchements_candidates=cover, chevauchements_avec_nes=bover,
                          liens_avec_nes_hors_plancher=blink_extra, tissus=sum(dist3.values()),
                          par_nombre_de_liens_gen3=dict(sorted(dist3.items())),
                          sans_lien_et_aucune_fille_a_risque=same_thing, duree_s=round(time.time() - t1, 1))), flush=True)
