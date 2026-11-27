"""Contre-audit X-32, partie T27 : regle a la lettre, puis classement des cotes au-dela des cellules de T(q)."""
import json, sys, time
from commun import *

t0 = time.time()
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6   # on construit S(0..NMAX)
QMAX = NMAX - 1                                         # q jusqu'au palier QMAX

palier = {u: 0 for u in GERME}
tuile_naissance = {u: GERME_SET for u in GERME}
tailles = [5]
nb_cellules = []
for n in range(NMAX):
    L = sorted(palier)
    idx = {u: i for i, u in enumerate(L)}
    over, adj = gram_check(L)
    assert over == 0
    adjs = [set(int(j) for j in a) for a in adj]
    cells = []
    for a in range(len(L)):
        Na = [b for b in adjs[a] if b > a]
        for b in Na:
            Nab = [c for c in Na if c > b and c in adjs[b]]
            for c in Nab:
                for d in Nab:
                    if d > c and d in adjs[c]:
                        cells.append((a, b, c, d))
    nb_cellules.append(len(cells))
    new = {}
    for cl in cells:
        C = [L[i] for i in cl]
        for y in cotes_par_algebre(C):
            if y not in palier and y not in new:
                new[y] = frozenset(C) | {y}
    for y, T in new.items():
        palier[y] = n + 1; tuile_naissance[y] = T
    tailles.append(len(palier))

porte_cache = {}
def T_de(u):
    if u in GERME_SET: return GERME_SET
    if u not in porte_cache:
        porte_cache[u] = descente(tuile_naissance[u], u)[0]
    return porte_cache[u]

def porte_de(x, tuile):
    if x in GERME_SET: return GERME_SET
    return descente(tuile, x)[0]

res = dict(constituants=0, cellules=0, fille_propre=0, cousin=0, autre=0, desaccord_avec_le_mur=0,
           mur_du_plancher_separe=0)
murs = {}; par_palier = {}; meres = {}; sans_mere_sans_cousins = 0; mere_vs_murs_desaccord = 0
for q in sorted(palier):
    if palier[q] == 0 or palier[q] > QMAX: continue
    res['constituants'] += 1
    Tq = T_de(q); F = Tq - {q}
    q2 = autre_cote(list(F), q); T1 = F | {q2}
    if separe(T1, q2): res['mur_du_plancher_separe'] += 1
    nsep = sum(1 for f in F if separe(T1, f)); murs[nsep] = murs.get(nsep, 0) + 1
    nf = 0
    for f in F:
        res['cellules'] += 1
        Ci = Tq - {f}
        x = autre_cote(list(Ci), f)
        assert pr(x, q) == -1
        Gx = porte_de(x, Ci | {x})
        if Gx - {x} == Ci: cas = 'fille_propre'; nf += 1
        elif q not in Gx: cas = 'cousin'
        else: cas = 'autre'
        res[cas] += 1
        if (cas == 'fille_propre') != (not separe(T1, f)): res['desaccord_avec_le_mur'] += 1
    d = par_palier.setdefault(palier[q], {}); d[nf] = d.get(nf, 0) + 1
    if palier[q] >= 2:
        m = sum(1 for g in F if F <= T_de(g))   # g mere propre : le plancher de q est une cellule de T(g) contenant g
        meres[m] = meres.get(m, 0) + 1
        if (m == 1) != (nsep == 1) or (m == 0) != (nsep == 2): mere_vs_murs_desaccord += 1
        if m == 0:
            Fl = list(F)
            cousins = [(a, b) for i, a in enumerate(Fl) for b in Fl[i + 1:] if a not in T_de(b) and b not in T_de(a)]
            if not cousins: sans_mere_sans_cousins += 1

out = dict(partie='T27 (contre-audit)', tailles_regle_a_la_lettre=tailles, cellules_nees_par_palier=nb_cellules,
           q_jusqu_au_palier=QMAX, **res,
           murs_de_T_prime_qui_separent={str(k): murs[k] for k in sorted(murs)},
           filles_propres_par_palier={str(p): {str(k): v for k, v in sorted(par_palier[p].items())} for p in sorted(par_palier)},
           meres_propres_paliers_2_et_plus={str(k): v for k, v in sorted(meres.items())},
           desaccord_mere_propre_et_murs=mere_vs_murs_desaccord, sans_mere_propre_et_sans_parents_cousins=sans_mere_sans_cousins,
           duree_s=round(time.time() - t0, 1))
print(json.dumps(out, ensure_ascii=False))
