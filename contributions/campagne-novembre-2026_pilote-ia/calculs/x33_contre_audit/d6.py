"""D6 : variante plus libre a la generation 2. Chaque constituant ne (germe et palier 1) prend une fille non nee dont il est
un parent et dont le plancher est ne, toutes distinctes. Ensembles de dix naissances sans lien entre elles."""
import json, time, itertools
from alib import *
from rule import *

t0 = time.time()
P = Pack()
for v in GERM:
    P.gate_of(M[v], GERMSET - {v} | {M[v]})
born = sorted(set(GERM) | set(PAL1))
links, over, adj = adjacency(born)
cand = {}
for cl in cliques4(born, adj):
    C = frozenset(born[i] for i in cl)
    for x in cell_sides(C):
        if x in born: continue
        g = P.gate_of(x, C | {x})
        F = g - {x}
        if F <= set(born):
            cand[x] = F
C = sorted(cand)
X20 = set()
for v in GERM:
    for x, f in P.proper_daughters(M[v]): X20.add(x)
nC = len(C)
lk = {(i, j) for i, j in itertools.combinations(range(nC), 2) if ip(C[i], C[j]) == -1}
ov = sum(1 for i, j in itertools.combinations(range(nC), 2) if ip(C[i], C[j]) > -1)
nb = {i: set() for i in range(nC)}
for i, j in lk: nb[i].add(j); nb[j].add(i)


def matchable(sel):
    """Couplage parfait : chaque ne prend une candidate de sel dont il est parent."""
    match = {}
    def aug(p, seen):
        for k in sel:
            if p in cand[C[k]] and k not in seen:
                seen.add(k)
                if k not in match or aug(match[k], seen):
                    match[k] = p
                    return True
        return False
    return all(aug(p, set()) for p in born)


free = []
total = 0
matchable_any = 0
for sel in itertools.combinations(range(nC), 10):
    total += 1
    m = matchable(sel)
    if m: matchable_any += 1
    s = set(sel)
    if any(nb[i] & s for i in sel):
        continue
    free.append((sel, m))
free_m = [frozenset(C[i] for i in sel) for sel, m in free if m]
idx = {s: i for i, s in enumerate(free_m)}
seen = set(); classes = []
for i, s in enumerate(free_m):
    if i in seen: continue
    orb = set()
    for p in PERMS:
        t = frozenset(act(p, x) for x in s)
        assert t in idx
        orb.add(idx[t])
    seen |= orb; classes.append(len(orb))
# nombre de filles propres nees de chaque M_v dans ces ensembles
prof = {}
for s in free_m:
    k = tuple(sorted(sum(1 for x, f in P.proper_daughters(M[v]) if x in s) for v in GERM))
    prof[str(list(k))] = prof.get(str(list(k)), 0) + 1
print(json.dumps(dict(partie='D6', nes=len(born), candidates=nC, candidates_sont_les_vingt_X=(set(C) == X20), paires_liees=len(lk),
                      chevauchements_candidates=ov, ensembles_de_dix=total, avec_couplage_sans_condition=matchable_any,
                      sans_lien=len(free), sans_lien_et_couplage=len(free_m), classes_120=sorted(classes), nombre_de_classes=len(classes),
                      profils_filles_des_M=prof, duree_s=round(time.time() - t0, 1))))
