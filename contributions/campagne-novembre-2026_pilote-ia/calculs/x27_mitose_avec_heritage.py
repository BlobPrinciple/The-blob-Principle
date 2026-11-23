#!/usr/bin/env python3
"""X-27 -- la mitose d'un constituant avec heritage, lue comme un contact (rang 3).
Lectures : C1 (un lien est un contact), C2 (constituants ronds, sans chevauchement), C7 (a chaque naissance la forme reste fixee par les contacts).
La naissance dans la cellule (C5 de X-25) n'est PAS posee. Parole de l'auteur prise comme regle : le nouveau-ne est lie a son parent et herite de liens du parent.
NAISSANCE HERITEE ET FIXEE : un nouveau-ne x, rond, qui touche son parent p et trois voisins q, r, s de p, les quatre etant independants, et qui ne chevauche rien.
PLACE ADMISSIBLE : une place ou une telle naissance est possible. PLACE SANS CELLULE : ses contacts ne contiennent aucun groupe de quatre tous lies.
Arithmetique exacte (entiers, fractions, et signe exact de p + q*racine(rho) pour les places irrationnelles).
Appartenance a l'empilement ne du germe : descente par les reflexions du groupe d'Apollonius (coordonnee negative -> reflexion), exacte pour les vecteurs entiers.
Parties : A (tous les tissus atteignables en d naissances), B (croissances longues : hasard, adverse, couche), C (regle a la lettre de X-25), E (liens des nouveau-nes).
Prediction scellee : x27_mitose_avec_heritage_prediction.txt (SHA-256 d0e1e54de989fa8f6022dcc3edceee900914133c1f8cabddc6136ea0feccb502).
Usage : python3 x27_mitose_avec_heritage.py A [d] | B strategie graine_debut graine_fin naissances | C [palier_max] | E | controle     Claude, 23 novembre 2026."""
import itertools, json, math, os, random, sys, time
from fractions import Fraction as F
import numpy as np
from x25_cellule import germe
from x25bis_naissances_et_fermetures import Tissu, autre_cote

ICI = os.path.dirname(os.path.abspath(__file__))
G5 = germe(3)


def prod(a, b):
    return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)


def det(m):
    """Determinant exact d'une matrice carree d'entiers ou de fractions (elimination en fractions)."""
    m = [[F(x) for x in r] for r in m]; n = len(m); d = F(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if m[r][c] != 0), None)
        if piv is None: return F(0)
        if piv != c: m[c], m[piv] = m[piv], m[c]; d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            if f != 0:
                for k in range(c, n): m[r][k] -= f * m[c][k]
    return d


def resout(mat, b):
    """Resolution exacte de mat * x = b (fractions) ; None si singuliere."""
    n = len(mat); a = [[F(x) for x in r] + [F(b[i])] for i, r in enumerate(mat)]
    for c in range(n):
        piv = next((r for r in range(c, n) if a[r][c] != 0), None)
        if piv is None: return None
        a[c], a[piv] = a[piv], a[c]
        p = a[c][c]; a[c] = [v / p for v in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c]; a[r] = [v - f * w for v, w in zip(a[r], a[c])]
    return [a[i][n] for i in range(n)]


def carre_parfait(q):
    """Racine exacte d'une fraction positive si elle est un carre, sinon None."""
    if q < 0: return None
    a, b = q.numerator, q.denominator; ra, rb = math.isqrt(a), math.isqrt(b)
    return F(ra, rb) if ra * ra == a and rb * rb == b else None


class Place:
    """x = base + signe * racine(rho) * n ; <x,s> = A + signe * racine(rho) * B."""
    __slots__ = ('base', 'n', 'rho', 'signe', 'coords', 'cle', 'xf')

    def __init__(self, base, n, rho, signe, quad):
        self.base, self.n, self.rho, self.signe = base, n, rho, signe
        r = carre_parfait(rho)
        if r is not None:
            c = tuple(b + signe * r * k for b, k in zip(base, n))
            self.coords = tuple(int(v) for v in c) if all(v.denominator == 1 for v in c) else c
            self.cle = self.coords
        else:
            self.coords = None; self.cle = ('irrationnelle', quad, signe)
        rf = math.sqrt(float(rho))
        self.xf = np.array([float(b) + signe * rf * k for b, k in zip(base, n)])

    def compare(self, s):
        """-1 : disjoint (<x,s> < -1) ; 0 : contact ; +1 : chevauchement. Exact."""
        if self.coords is not None:
            v = prod(self.coords, s) + 1
            return -1 if v < 0 else (0 if v == 0 else 1)
        L = -1 - prod(self.base, s); R = self.signe * prod(self.n, s)       # <x,s> + 1 = R * racine(rho) - L
        if R == 0: return -1 if L > 0 else (0 if L == 0 else 1)
        g = R * R * self.rho; L2 = L * L
        if R > 0:
            if L < 0: return 1
            return -1 if g < L2 else (0 if g == L2 else 1)
        if L >= 0: return -1
        return -1 if g > L2 else (0 if g == L2 else 1)


CACHE = {}


def places_du_quadruple(quad):
    """Les boules (deux au plus) qui touchent les quatre constituants du quadruple, s'ils sont independants."""
    if quad in CACHE: return CACHE[quad]
    u = sorted(quad); out = []
    M = [[prod(a, b) for b in u] for a in u]
    alpha = resout(M, [-1, -1, -1, -1])
    if alpha is not None:
        g = [tuple(2 * a[k] - sum(a) for k in range(5)) for a in u]                    # <n,u_i> = n . g_i
        n = tuple(int((-1) ** k * det([[r[c] for c in range(5) if c != k] for r in g])) for k in range(5))
        d = math.gcd(*n) if any(n) else 0
        if d:
            n = tuple(v // d for v in n); nu = prod(n, n)
            if nu != 0:
                rho = (1 + sum(alpha)) / nu
                if rho >= 0:
                    base = tuple(sum(alpha[i] * u[i][k] for i in range(4)) for k in range(5))
                    out = [Place(base, n, rho, 0, quad)] if rho == 0 else [Place(base, n, rho, +1, quad), Place(base, n, rho, -1, quad)]
    CACHE[quad] = out
    return out


def dans_l_empilement(x):
    """Descente : tant qu'une coordonnee est negative, reflexion dans la sphere duale correspondante. x dans l'empilement <=> on arrive a un constituant du germe."""
    if any(not isinstance(v, int) for v in x): return False
    y = list(x)
    for _ in range(100000):
        j = min(range(5), key=lambda k: y[k]); t = y[j]
        if t >= 0: break
        y = [(-t if k == j else y[k] + t) for k in range(5)]
        if sum(y) <= 0: return False
    return sorted(y) == [0, 0, 0, 0, 1]


class Tissu27:
    """Un tissu (liste de constituants entiers), ses contacts, et toutes ses places admissibles, tenues a jour a chaque naissance."""

    def __init__(self, S):
        self.S = []; self.adj = []; self.places = {}; self.quads = set(); self.A = None; self.hors = []
        self.vues = {}                                              # toute place admissible rencontree : cle -> classement
        for u in S: self._pose(u)
        for p in range(len(self.S)):
            for t in itertools.combinations(sorted(self.adj[p]), 3): self._quadruple((p,) + t)

    def _pose(self, u):
        i = len(self.S); self.S.append(u); self.adj.append(set())
        for j in range(i):
            v = prod(u, self.S[j])
            assert v <= -1, ('chevauchement dans le tissu', u, self.S[j], v)
            if v == -1: self.adj[i].add(j); self.adj[j].add(i)
        self.A = np.array(self.S, dtype=float); self.sA = self.A.sum(axis=1)
        return i

    def _valide(self, pl):
        """Contacts de la place avec le tissu, ou None si elle chevauche un constituant. Filtre flottant puis controle exact."""
        v = 2 * self.A @ pl.xf - self.sA * pl.xf.sum() + 1          # <x,s> + 1
        if (v > 1e-7).any(): return None
        contacts = set()
        for j in np.nonzero(v > -1e-7)[0]:
            c = pl.compare(self.S[int(j)])
            if c > 0: return None
            if c == 0: contacts.add(int(j))
        return contacts

    def _quadruple(self, idx):
        q = frozenset(idx)
        if q in self.quads: return
        self.quads.add(q)
        for pl in places_du_quadruple(frozenset(self.S[i] for i in q)):
            if pl.cle in self.places: continue
            contacts = self._valide(pl)
            if contacts is None: continue
            self.places[pl.cle] = (pl, contacts)
            if pl.cle not in self.vues:
                self.vues[pl.cle] = self.classe(pl)
                if self.vues[pl.cle] != 'empilement':
                    self.hors.append(dict(classe=self.vues[pl.cle], place=[str(v) for v in pl.coords] if pl.coords is not None else [round(float(v), 9) for v in pl.xf],
                                          touche=[list(self.S[i]) for i in sorted(contacts)], constituants=len(self.S)))

    def classe(self, pl):
        if pl.coords is None: return 'irrationnelle'
        if any(not isinstance(v, int) for v in pl.coords): return 'rationnelle non entiere'
        return 'empilement' if dans_l_empilement(pl.coords) else 'entiere hors empilement'

    def sans_cellule(self, cle):
        c = sorted(self.places[cle][1])
        return not any(all(b in self.adj[a] for a, b in itertools.combinations(t, 2)) for t in itertools.combinations(c, 4))

    def naissance(self, cle):
        pl, _ = self.places.pop(cle); assert isinstance(pl.coords, tuple) and all(isinstance(v, int) for v in pl.coords)
        y = self._pose(pl.coords)
        for k in list(self.places):                                 # les places deja connues : contact ou chevauchement avec le nouveau-ne
            p2, cont = self.places[k]; c = p2.compare(pl.coords)
            if c > 0: del self.places[k]
            elif c == 0: cont.add(y)
        for t in itertools.combinations(sorted(self.adj[y]), 3): self._quadruple((y,) + t)
        for p in self.adj[y]:
            for t in itertools.combinations(sorted(self.adj[p] - {y}), 2): self._quadruple((p, y) + t)
        return y


def bilan_des_vues(vues):
    r = {}
    for c in vues.values(): r[c] = r.get(c, 0) + 1
    return r


# ---------------------------------------------------------------- partie A : tous les tissus atteignables
def partie_A(dmax):
    t0 = time.time(); niveau = {frozenset(G5)}; out = []; hors = []
    for d in range(dmax + 1):
        suivant = set(); nb_places = 0; sans = 0; classes = {}; ambigus = 0
        for etat in niveau:
            T = Tissu27(sorted(etat))
            for cle, (pl, cont) in T.places.items():
                nb_places += 1; c = T.vues[cle]; classes[c] = classes.get(c, 0) + 1
                if T.sans_cellule(cle): sans += 1
                if c == 'empilement': suivant.add(etat | {pl.coords})
                elif len(hors) < 20: hors.append(dict(naissances=d, tissu=[list(u) for u in sorted(etat)], classe=c, place=[str(v) for v in pl.coords] if pl.coords is not None else [round(float(v), 9) for v in pl.xf], touche=[list(T.S[i]) for i in sorted(cont)]))
        r = dict(naissances=d, tissus=len(niveau), places_admissibles=nb_places, places_par_classe=classes, places_sans_cellule=sans, duree_s=round(time.time() - t0, 1))
        out.append(r); print(json.dumps(r), flush=True)
        niveau = suivant
    return dict(niveaux=out, places_hors_de_l_empilement=hors)


# ---------------------------------------------------------------- partie B : croissances longues
def partie_B(strategie, graine, naissances):
    rng = random.Random(graine); T = Tissu27(G5); t0 = time.time()
    jamais_sans = set(); nais_sans = 0; arret = None
    for k in range(naissances):
        cles = sorted((c for c in T.places if T.vues[c] == 'empilement'), key=repr)
        sans = [c for c in cles if T.sans_cellule(c)]
        jamais_sans.update(sans)
        if strategie == 'couche':
            choix = [c for c in cles if 0 in T.places[c][1] and 1 in T.places[c][1]]
            if not choix: arret = 'plus de place dans la couche'; break
            m = min(len(T.places[c][1]) for c in choix); choix = [c for c in choix if len(T.places[c][1]) == m]
        elif strategie == 'adverse' and sans: choix = sans
        else: choix = cles
        if not choix: arret = 'plus de place'; break
        c = rng.choice(choix)
        if c in sans: nais_sans += 1
        T.naissance(c)
    cles = [c for c in T.places if T.vues[c] == 'empilement']; jamais_sans.update(c for c in cles if T.sans_cellule(c))
    b = bilan_des_vues(T.vues)
    deg = sorted((len(a) for a in T.adj), reverse=True)
    return dict(strategie=strategie, graine=graine, naissances=len(T.S) - 5, constituants=len(T.S), liens=sum(deg) // 2, quadruples_examines=len(T.quads),
                places_admissibles_rencontrees=len(T.vues), par_classe=b, hors_de_l_empilement=sum(v for c, v in b.items() if c != 'empilement'),
                exemples_hors=T.hors[:5],
                places_sans_cellule_rencontrees=len(jamais_sans), naissances_dans_une_place_sans_cellule=nais_sans, plus_grands_degres=deg[:5], arret=arret, duree_s=round(time.time() - t0, 1))


# ---------------------------------------------------------------- partie C : regle a la lettre de X-25
def partie_C(gmax):
    out = []; T = Tissu(3)
    for g in range(gmax + 1):
        if g: T.palier(g)
        t0 = time.time(); S = sorted(T.spheres); W = Tissu27(S)
        cotes = {autre_cote(cel, occ, 3) for cel, occ in T.surface.items()}
        adm = set(W.places); classes = bilan_des_vues(W.vues)
        r = dict(palier=g, constituants=len(S), quadruples_examines=len(W.quads), places_admissibles=len(adm), par_classe=classes, cotes_libres_des_cellules_de_surface=len(cotes),
                 places_egales_aux_cotes_libres=(adm == cotes), places_hors_cotes=len(adm - cotes), cotes_non_admissibles=len(cotes - adm),
                 places_sans_cellule=sum(1 for c in adm if W.sans_cellule(c)), duree_s=round(time.time() - t0, 1))
        out.append(r); print(json.dumps(r), flush=True)
    return out


# ---------------------------------------------------------------- partie E : liens des nouveau-nes dans l'empilement, regle a la lettre
def partie_E(gmax=6):
    out = []; T = Tissu(3)
    for g in range(1, gmax + 1):
        T.palier(g)
        L = list(T.spheres); idx = {u: i for i, u in enumerate(L)}; nb = [0] * len(L); anciens = [0] * len(L); pal = [T.spheres[u] for u in L]; vus = set()
        for D in T.confs:
            ids = sorted(idx[u] for u in D)
            for a, b in itertools.combinations(ids, 2):
                if (a, b) in vus: continue
                vus.add((a, b)); nb[a] += 1; nb[b] += 1
                if pal[b] < pal[a]: anciens[a] += 1
                if pal[a] < pal[b]: anciens[b] += 1
        nes = [i for i in range(len(L)) if pal[i] == g]; h = {}
        for i in nes: h[nb[i]] = h.get(nb[i], 0) + 1
        r = dict(palier=g, naissances=len(nes), liens_moyens_a_la_fin_du_palier=sum(nb[i] for i in nes) / len(nes), dont_vers_plus_anciens=sum(anciens[i] for i in nes) / len(nes),
                 repartition={str(k): v for k, v in sorted(h.items())})
        out.append(r); print(json.dumps(r), flush=True)
    return out


def controle():
    """Controles de l'outil : le germe a cinq places (les cotes de ses cinq cellules) ; la descente reconnait tout l'empilement jusqu'au palier 5 et refuse des vecteurs entiers hors empilement."""
    T = Tissu27(G5); T3 = Tissu(3)
    for g in range(1, 6): T3.palier(g)
    tous = list(T3.spheres); ok = all(dans_l_empilement(u) for u in tous)
    faux = [(2, 1, 0, 0, 0), (3, 2, 0, 0, 0), (-2, 3, 2, 2, 2), (1, 1, 1, 1, -2)]
    tot_pos = sum(1 for u in tous if min(u) >= 0)
    return dict(places_du_germe=len(T.places), toutes_cotes_de_cellule=all(not T.sans_cellule(c) for c in T.places), classes=bilan_des_vues(T.vues),
                descente_reconnait_les_constituants_jusqu_au_palier_5=ok, effectif=len(tous), constituants_sans_coordonnee_negative=tot_pos,
                vecteurs_hors_empilement_refuses=[(list(v), prod(v, v), dans_l_empilement(v)) for v in faux])


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'controle': print(json.dumps(controle()))
    elif mode == 'A':
        d = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        r = partie_A(d); json.dump(r, open(os.path.join(ICI, 'x27_partie_A.json'), 'w'), indent=1)
    elif mode == 'B':
        strategie, g0, g1, nais = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]); out = []
        for graine in range(g0, g1 + 1):
            r = partie_B(strategie, graine, nais); out.append(r); print(json.dumps(r), flush=True)
        json.dump(out, open(os.path.join(ICI, 'x27_partie_B_%s_%d_%d.json' % (strategie, g0, g1)), 'w'), indent=1)
    elif mode == 'C':
        r = partie_C(int(sys.argv[2]) if len(sys.argv) > 2 else 3); json.dump(r, open(os.path.join(ICI, 'x27_partie_C.json'), 'w'), indent=1)
    elif mode == 'E':
        r = partie_E(); json.dump(r, open(os.path.join(ICI, 'x27_partie_E.json'), 'w'), indent=1)
