#!/usr/bin/env python3
"""X-29 bis, NUL NE NAIT AVANT SON PLANCHER. Prediction scellee : x29bis_plancher_prediction.txt (SHA-256 99ee80f1...6c38), poussee avant ce calcul.
 x27        : R1. Les tissus de X-27 sont-ils clos par plancher ? La place hors de l'empilement chevauche-t-elle un ancetre de ses contacts ?
 G n [sym]  : R2, R3. Enonce (G) sur le palier n : toute boule liee a un parent et a trois de ses voisins nes, si elle ne chevauche aucun ancetre
              des quatre, est dans l'empilement. Avec 'sym' : parents a symetrie pres.
 hasard a b : R4. Germe plus ancetres de 2 a 8 constituants tires dans le palier 5 ; toutes les places.
 partiel    : R5. Les six tissus incomplets de X-28 sont-ils clos par plancher ?
Plancher de u : les quatre autres constituants de sa tuile-porte (on retourne, a partir d'une tuile contenant u, tout constituant autre que u dont
l'autre cote a une somme de coordonnees plus petite).      Claude, 27 novembre 2026."""
import itertools, json, os, random, sys, time
import numpy as np
import x29_pliage as Y
from x29_pliage import autre, GERME, GERME_ENS, Tissu, m, X

ICI = os.path.dirname(os.path.abspath(__file__))

def porte(T, u):
    T = set(T)
    while True:
        d = [v for v in T if v != u and sum(autre(T, v)) < sum(v)]
        if not d: return frozenset(T)
        v = min(d); T.remove(v); T.add(autre(T | {v}, v))

class Ancetres:
    """Planchers et ancetres, de proche en proche. tuile_de[u] : une tuile de l'empilement contenant u."""
    def __init__(self): self.pl = {u: frozenset() for u in GERME}; self.an = {u: frozenset() for u in GERME}; self.tu = {u: GERME_ENS for u in GERME}
    def plancher(self, u, T=None):
        if u not in self.pl:
            Gt = porte(T if T is not None else self.tu[u], u); f = Gt - {u}; self.pl[u] = f; self.tu[u] = Gt
            for v in f: self.tu.setdefault(v, Gt)
        return self.pl[u]
    def ancetres(self, u, T=None):
        if u not in self.an:
            f = self.plancher(u, T); a = set(f)
            for v in f: a |= self.ancetres(v)
            self.an[u] = frozenset(a)
        return self.an[u]

def palier(n):
    T = Tissu(3)
    for g in range(1, n + 1): T.palier(g)
    S = dict(T.spheres); tui = Y.tuiles_par_voisinage(S); A = Ancetres()
    une = {}
    for Tu in tui:
        for u in Tu: une.setdefault(u, Tu)
    for u in sorted(S, key=lambda v: S[v]): A.ancetres(u, une[u])
    return S, tui, A

def clos_par_plancher(S, A, une):
    manque = {}
    for u in S:
        if u in GERME_ENS: continue
        f = A.plancher(u, une.get(u)) - set(S)
        if f: manque[u] = f
    return manque

def partie_x27():
    for nom, f in (('tissu_de_22', 'x27_contre_exemple_court.json'), ('tissu_du_toit', 'x27_contre_exemple_toit.json')):
        c = json.load(open(os.path.join(ICI, f))); S = set(GERME) | {tuple(u) for u in c['liste_des_naissances']}; O, tui = Y.outil(S); A = Ancetres(); une = {}
        for Tu in tui:
            for u in Tu: une.setdefault(u, Tu)
        manque = clos_par_plancher(S, A, une); absents = set().union(*manque.values()) if manque else set()
        r = dict(tissu=nom, constituants=len(S), nes_dont_le_plancher_n_est_pas_ne=len(manque), constituants_de_plancher_absents=len(absents), clos_par_plancher=(not manque),
                 exemple=[dict(ne=list(u), plancher_non_ne=sorted(map(list, v))) for u, v in sorted(manque.items())[:2]])
        if nom == 'tissu_de_22':
            x = tuple(X.F(v) for v in c['place_hors_empilement']); contacts = [u for u in S if Y.prod(x, u) == -1]; anc = set()
            for u in contacts: anc |= A.ancetres(u, une[u])
            chev = sorted(a for a in anc if Y.prod(x, a) > -1)
            r.update(place=[str(v) for v in x], contacts=sorted(map(list, contacts)), ancetres_des_contacts=len(anc), ancetres_chevauches=[list(a) for a in chev],
                     ancetres_chevauches_nes=[list(a) for a in chev if a in S], la_jumelle_est_un_ancetre=((2, 2, 2, -1, 0) in anc),
                     la_jumelle_est_chevauchee=(Y.prod(x, (2, 2, 2, -1, 0)) > -1))
        print(json.dumps(r), flush=True)

def partie_G(n, sym):
    S, tui, A = palier(n); L = sorted(S); idx = {u: i for i, u in enumerate(L)}; M = np.array(L, dtype=np.int64); s = M.sum(1)
    Gm = 2 * M @ M.T - np.outer(s, s); Gx = (2 * M - s[:, None]).astype(float)                    # <x, a> = Gx[a] . x
    anc = [np.array(sorted(idx[a] for a in A.an[u]), dtype=np.int64) for u in L]
    parents = [i for i, u in enumerate(L) if (not sym) or u == tuple(sorted(u))]
    t0 = time.time(); quad = dep = boules = chev = libres_dedans = irr_libres = nviol = 0; viol = []
    for p in parents:
        vo = [int(j) for j in np.nonzero(Gm[p] == -1)[0]]
        for q, r, t in itertools.combinations(vo, 3):
            quad += 1; pls = m.places_du_quadruple(frozenset((L[p], L[q], L[r], L[t])))
            if not pls: dep += 1; continue
            ai = np.unique(np.concatenate((anc[p], anc[q], anc[r], anc[t])))
            for P in pls:
                boules += 1
                if len(ai):                                   # sans ancetre (quadruple du germe) : rien a chevaucher
                    v = Gx[ai] @ P.xf
                    if v.max() > -1 + 1e-6: chev += 1; continue
                    if any(P.compare(L[int(a)]) > 0 for a in ai[v > -1 - 1e-6]): chev += 1; continue
                if P.coords is not None and m.dans_l_empilement(P.coords): libres_dedans += 1; continue
                nviol += 1
                if P.coords is None: irr_libres += 1
                if len(viol) < 5:
                    viol.append(dict(parent=list(L[p]), voisins=[list(L[q]), list(L[r]), list(L[t])], boule=[str(c) for c in P.coords] if P.coords is not None else [round(float(c), 9) for c in P.xf],
                                     ancetres=[list(L[a]) for a in ai]))
        m.CACHE.clear()
    ex = viol
    print(json.dumps(dict(palier=n, constituants=len(L), parents=len(parents), a_symetrie_pres=bool(sym), quadruples=quad, quadruples_dependants_ou_sans_boule=dep, boules_liees_aux_quatre=boules,
                          chevauchent_un_ancetre=chev, sans_ancetre_chevauche_et_dans_l_empilement=libres_dedans, sans_ancetre_chevauche_et_HORS_de_l_empilement=nviol,
                          dont_irrationnelles=irr_libres, exemples=ex, plus_grand_nombre_d_ancetres=max(len(a) for a in anc), duree_s=round(time.time() - t0, 1))), flush=True)

def partie_hasard(a, b):
    S5, tui5, A = palier(5); L5 = sorted(u for u in S5 if u not in GERME_ENS)
    tot = dict(tissus=0, hors=0, sans_cellule=0, places=0, clos_par_pliage=0, places_egales_aux_cotes=0)
    for graine in range(a, b + 1):
        rng = random.Random(graine); k = rng.randint(2, 8); tires = rng.sample(L5, k); S = set(GERME) | set(tires)
        for u in tires: S |= A.an[u]
        t0 = time.time(); O, tui = Y.outil(S); tri, ech, _, _ = Y.pliage(S, tui); r, pl, lib = Y.places(O)
        tot['tissus'] += 1; tot['hors'] += r['hors_de_l_empilement']; tot['sans_cellule'] += r['places_sans_cellule']; tot['places'] += r['places_admissibles']
        tot['clos_par_pliage'] += 1 if ech == 0 else 0; tot['places_egales_aux_cotes'] += 1 if r['places_egales_aux_cotes_libres'] else 0
        print(json.dumps(dict(graine=graine, tires=k, paliers_des_tires=sorted(S5[u] for u in tires), constituants=len(S), tuiles_nees=len(tui), images_non_nees=ech, places=r['places_admissibles'],
                              hors=r['hors_de_l_empilement'], sans_cellule=r['places_sans_cellule'], cotes_libres=r['cotes_libres'], egales_aux_cotes=r['places_egales_aux_cotes_libres'],
                              hors_cotes=r['places_hors_cotes'], cellules_sans_cote_ne=r['cellules_sans_cote_ne'], exemples=r['exemples_hors_empilement'][:2], duree_s=round(time.time() - t0, 1))), flush=True)
    print(json.dumps(dict(bilan=True, graines=[a, b], **tot)), flush=True)

def partie_partiel():
    S5, tui5, A = palier(5); T = Tissu(3)
    for g in range(1, 5): T.palier(g)
    S4 = sorted(T.spheres); O4 = X.Outil(S4); O4.cliques(); libres, _, _ = O4.cotes_libres(); Lb = sorted(libres)
    for graine in (1, 2):
        for frac in (0.25, 0.5, 0.75):
            rng = random.Random(graine); S = set(S4) | set(rng.sample(Lb, int(round(frac * len(Lb))))); manque = {u for u in S if not A.pl[u] <= S}
            print(json.dumps(dict(graine=graine, fraction=frac, constituants=len(S), nes_dont_le_plancher_n_est_pas_ne=len(manque), clos_par_plancher=(not manque))), flush=True)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'x27': partie_x27()
    elif a[0] == 'G': partie_G(int(a[1]), len(a) > 2 and a[2] == 'sym')
    elif a[0] == 'hasard': partie_hasard(int(a[1]), int(a[2]))
    elif a[0] == 'partiel': partie_partiel()
