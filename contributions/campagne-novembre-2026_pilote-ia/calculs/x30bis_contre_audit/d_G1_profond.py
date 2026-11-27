# D. (G1) en profondeur, et E. le second point de T19 et T15 sur des paires profondes.
import sys, time
from math import isqrt
from noyau import *

t0 = time.time()
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 240
graine = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
SEUIL = int(sys.argv[3]) if len(sys.argv) > 3 else 13
rng = random.Random(graine)
germe = set(GERME)

def carre_rat(r):
    a, b = r.numerator, r.denominator
    ra, rb = isqrt(a), isqrt(b)
    return F(ra, rb) if ra * ra == a and rb * rb == b else None

stat = dict(essais_p=0, triplets=0, degeneres=0, sans_boule=0, boules=0, dans=0, hors=0, hors_irr=0,
            hors_sans_parent_chevauche=0, portes_libres={0: 0, 1: 0, 2: 0, 3: 0}, types_hors={},
            point2_test=0, point2_faux=0, T15_test=0, T15_faux=0, T16_test=0, T16_faux=0, Lmax=0)
exemples = []

def chevauche(xc, d, disc, sgn, f):
    a = ip(xc, f) + 1
    if d is None:
        return a > 0
    return signe_qr(a, sgn * ip(d, f), disc) > 0

def nuxw(xc, d, disc, sgn, w):
    """nu(x, w) = (1 - <xc,w> - sgn sqrt(disc) <d,w>)/2 : renvoie (a, b) avec nu = a + b sqrt(disc)"""
    if d is None:
        return (F(1 - ip(xc, w), 2), F(0))
    return (F(1 - ip(xc, w), 2), -F(sgn * ip(d, w), 2))

while time.time() - t0 < BUDGET:
    L = rng.randint(8, 30)
    T = marche(L, rng)
    stat['Lmax'] = max(stat['Lmax'], L)
    p = rng.choice(T)
    stat['essais_p'] += 1
    # residu de p : tuiles contenant p, a 3 pas
    res = {T: None}; front = [T]
    for _ in range(3):
        nf = []
        for t in front:
            for j in range(5):
                if t[j] == p: continue
                t2 = flip(t, j)
                if t2 not in res: res[t2] = None; nf.append(t2)
        front = nf
    tuile_de = {}
    for t in res:
        for u in t:
            if u != p and u not in tuile_de: tuile_de[u] = t
    vois = list(tuile_de)
    Tp, _ = porte(p, T)
    Fp = [u for u in Tp if u != p]
    porte_c = {}
    def T0(c):
        if c not in porte_c:
            g, _ = porte(p, tuile_de[c], fixes=[p, c])
            porte_c[c] = g
        return porte_c[c]
    parents = {}
    def par(u):
        if u in germe: return []
        if u not in parents:
            g, _ = porte(u, tuile_de[u] if u in tuile_de else T)
            parents[u] = [v for v in g if v != u]
        return parents[u]
    # E : second point et T15 sur quelques voisins c de p
    for c in rng.sample(vois, min(6, len(vois))):
        t0c = T0(c)
        G = [u for u in t0c if u not in (p, c)]
        Tc, _ = porte(c, tuile_de[c])
        stat['T15_test'] += 1
        if not (all(u in Tp for u in G) or all(u in Tc for u in G)): stat['T15_faux'] += 1
        for w in Tp:
            if w in (p, c): continue
            co = coords(w, t0c)
            stat['point2_test'] += 1
            if any(co[k] < 0 for k in range(5) if t0c[k] in G): stat['point2_faux'] += 1
    # triplets de voisins a petits nu
    Vs = rng.sample(vois, min(60, len(vois)))
    cand = []
    for q, r, s in combinations(Vs, 3):
        a, b, cc = nu(q, r), nu(q, s), nu(r, s)
        if max(a, b, cc) <= SEUIL:
            cand.append((q, r, s))
    rng.shuffle(cand)
    for q, r, s in cand[:150]:
        stat['triplets'] += 1
        sol = boules_liees((p, q, r, s))
        if sol == 'degenere': stat['degeneres'] += 1; continue
        if sol is None: stat['sans_boule'] += 1; continue
        xc, d, disc = sol[0]
        if d is None:
            liste = [(xc, None, None, 1)]
        else:
            liste = [(xc, d, disc, 1), (xc, d, disc, -1)]
        rc = carre_rat(disc) if d is not None else F(0)
        for (xc_, d_, disc_, sg) in liste:
            stat['boules'] += 1
            if rc is not None:
                x = tuple(a + sg * rc * b for a, b in zip(xc_, d_)) if d_ is not None else xc_
                if membre(x): stat['dans'] += 1; continue
            else:
                stat['hors_irr'] += 1
            stat['hors'] += 1
            ok = False
            for u in (p, q, r, s):
                for f in par(u):
                    if chevauche(xc_, d_, disc_, sg, f): ok = True; break
                if ok: break
            if not ok:
                stat['hors_sans_parent_chevauche'] += 1
                exemples.append((p, q, r, s, xc_, d_, disc_, sg))
            # portes libres (si p, c pas tous deux dans le germe)
            libres = 0; libres_c = []
            for cc_ in (q, r, s):
                if p in germe and cc_ in germe: continue
                G = [u for u in T0(cc_) if u not in (p, cc_)]
                if not any(chevauche(xc_, d_, disc_, sg, f) for f in G):
                    libres += 1; libres_c.append(cc_)
            stat['portes_libres'][libres] += 1
            ty = tuple(sorted(int(v) for v in (nu(q, r), nu(q, s), nu(r, s))))
            stat['types_hors'][ty] = stat['types_hors'].get(ty, 0) + 1
            # T16 sur les portes libres, w dans F(p)
            for cc_ in libres_c:
                for w in Fp:
                    if w == cc_: continue
                    a_, b_ = nuxw(xc_, d_, disc_, sg, w)
                    # nu(x,w) - 3/4 nu(c,w) >= 0 ?
                    stat['T16_test'] += 1
                    if signe_qr(a_ - F(3, 4) * nu(cc_, w), b_, disc_ if disc_ is not None else 0) < 0:
                        stat['T16_faux'] += 1

print("graine %d, budget %.0f s, temps %.1f s" % (graine, BUDGET, time.time() - t0))
for k, v in stat.items():
    if k == 'types_hors':
        v = dict(sorted(v.items())[:25])
    print("  %s : %s" % (k, v))
print("contre-exemples a (G1) :", len(exemples))
for e in exemples[:5]:
    print("   ", e)
