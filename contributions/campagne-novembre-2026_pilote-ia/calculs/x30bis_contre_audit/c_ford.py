# C. Modele de Ford sur Z[omega] (T18, C6), et (C6) sur les donnees (voisins de e1 vus de e1 et e2).
import time
from fractions import Fraction as F
from itertools import combinations
from noyau import ip, nu, GERME, flip
t0 = time.time()

def n2(s, t):  # |s + t w|^2
    return s * s - s * t + t * t

def mul(x, y):
    a, b = x; c, d = y
    # (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2 , w^2 = -1 - w
    return (a * c - b * d, a * d + b * c - b * d)

def conj(x):
    a, b = x
    return (a - b, -b)

def N(x):
    return n2(*x)

R = 3
# denominateurs (a unite pres) : 1 ; 1 - w ; 2  ; plus 7 : 3 + w (norme 9-3+1=7)
betas = {1: [(1, 0)], 3: [(1, -1)], 4: [(2, 0)], 7: [(3, 1), (2, -1)]}
pts = {}
for nb, bel in betas.items():
  for be in bel:
    for a in range(-4 * nb - 8, 4 * nb + 9):
        for b in range(-4 * nb - 8, 4 * nb + 9):
            al = (a, b)
            # alpha / beta = alpha * conj(beta) / N(beta)
            num = mul(al, conj(be))
            z = (F(num[0], nb), F(num[1], nb))
            if n2(*z) > R * R: continue
            # reduite : beta ne divise pas alpha (beta premier ou unite)
            if nb > 1 and num[0] % nb == 0 and num[1] % nb == 0: continue
            if z in pts and pts[z] != nb: raise SystemExit("conflit")
            pts[z] = nb
print("sommets de denominateur de norme 1, 3, 4, 7 a distance <= %d : %d" % (R, len(pts)), {k: sum(1 for v in pts.values() if v == k) for k in betas})

def nuz(z1, n1, z2, n2_):
    return n2(z1[0] - z2[0], z1[1] - z2[1]) * n1 * n2_

# (i) valeurs de nu selon les types
nom = {1: 'reseau', 3: 'centre', 4: 'milieu', 7: 'norme7'}
vals = {}
P = list(pts.items())
for (z1, a), (z2, b) in combinations(P, 2):
    k = tuple(sorted((a, b)))
    vals.setdefault(k, set()).add(nuz(z1, a, z2, b))
eis = set(n2(s, t) for s in range(-90, 91) for t in range(-90, 91))
for k in sorted(vals):
    v = sorted(vals[k])
    print("  %s-%s : nu = %s ... ; toutes des normes d'Eisenstein : %s ; carres de distance : %s"
          % (nom[k[0]], nom[k[1]], [int(x) for x in v[:7]], all(x in eis for x in v), [str(x / (k[0] * k[1])) for x in v[:5]]))
small = sorted(set(x for k in vals for x in vals[k] if x < F(16, 3)))
print("valeurs de nu < 16/3 entre deux voisins (tous types, normes <= 7) :", [str(x) for x in small])

# (ii) triplets (inf, r, s), r, s de norme 1, 3, 4, nu(r, s) dans {1, 3, 4}
lat = [z for z, n in pts.items() if n == 1]
types = {}
def intersections(z1, r1, z2, r2):
    """nombre de points communs des cercles |xi - z1|^2 = r1, |xi - z2|^2 = r2 (r carres de rayons)"""
    d = n2(z1[0] - z2[0], z1[1] - z2[1])
    # deux cercles de rayons a, b, distance D : 2 points si (a-b)^2 < D^2 < (a+b)^2, en carres :
    # D^2 < (a+b)^2  <=>  D^2 - a^2 - b^2 < 2ab  ; on compare au carre avec signes
    A = d - r1 - r2  # D^2 - a^2 - b^2
    # (a+b)^2 > D^2 <=> 2ab > A ; (a-b)^2 < D^2 <=> -2ab < A ; donc |A| < 2ab <=> A^2 < 4 r1 r2
    if d == 0: return 0 if r1 != r2 else -1
    if A * A < 4 * r1 * r2: return 2
    if A * A == 4 * r1 * r2: return 1
    return 0
inter = [z for z, n in pts.items() if n in (1, 3, 4) and n2(*z) <= 4]
autres = [z for z, n in pts.items() if n in (1, 3, 4)]
for z1 in inter:
    for z2 in autres:
        if z2 <= z1 and n2(*z2) <= 4: continue
        a, b = pts[z1], pts[z2]
        v = nuz(z1, a, z2, b)
        if v not in (1, 3, 4): continue
        t = (a, b, int(v))
        lie2 = (a == 1 and b == 1) or (a == 1 and v == 1) or (b == 1 and v == 1)
        typ = tuple(sorted(t))
        key = (typ, 'un lie aux deux autres' if lie2 else 'aucun')
        ni = intersections(z1, F(1, a), z2, F(1, b))
        # boules unite (liees au plan p et au plan inf) tangentes a r et s posees en des points du reseau
        sols = [l for l in lat if n2(l[0] - z1[0], l[1] - z1[1]) * a == 1 and n2(l[0] - z2[0], l[1] - z2[1]) * b == 1]
        st = types.setdefault(key, [0, 0, 0, 0])
        st[0] += 1; st[1] += ni; st[2] += len(sols); st[3] += (len(sols) < ni)
for k in sorted(types):
    print("  type %s, %s : %d triplets ; boules tangentes : %d ; dont sur le reseau (constituants) : %d ; triplets avec une boule hors reseau : %d"
          % (k[0], k[1], *types[k]))

# (iii) (C6) sur les donnees : voisins de e1, vus de e1 et e2 ; f = e3, e4, e5 en 0, 1, 1 + w
p, c = GERME[0], GERME[1]; f0, f1, f2 = GERME[2], GERME[3], GERME[4]
res = {GERME}; front = [GERME]
for l in range(8):
    nf = []
    for t in front:
        for j in range(1, 5):
            t2 = flip(t, j)
            if t2 not in res: res.add(t2); nf.append(t2)
    front = nf
vois = sorted(set(u for t in res for u in t if u != p))
place = {}
bad = 0
for u in vois:
    if u == c: continue
    Nu = nu(c, u)
    d0, d1, d2 = nu(f0, u) / Nu, nu(f1, u) / Nu, nu(f2, u) / Nu
    # -2s + t = d1 - d0 - 1 ; -s - t = d2 - d0 - 1
    A, B = d1 - d0 - 1, d2 - d0 - 1
    s = -(A + B) / 3; t = A + 2 * s
    if n2(s, t) != d0: bad += 1; continue
    # reduite alpha/beta avec N(beta) = Nu : il existe beta de norme Nu avec beta z entier et (alpha, beta) premiers entre eux
    if Nu.denominator != 1: bad += 1; continue
    place[u] = ((s, t), int(Nu))
print("(C6) donnees : %d voisins de e1 (residu, 8 pas) ; incoherences de trilateration : %d" % (len(vois), bad))
# denominateur : le plus petit entier D avec D z dans Z[w] ; pour une fraction reduite alpha/beta, z = alpha conj(beta)/N(beta)
# test : il existe beta de norme Nu tel que beta * z soit entier d'Eisenstein et pgcd(beta z, beta) = 1 (norme : on verifie
# que z n'est pas de denominateur plus petit : aucun beta' de norme < Nu divisant ne rend beta' z entier).
def eis_de_norme(n):
    return [(a, b) for a in range(-12, 13) for b in range(-12, 13) if n2(a, b) == n]
cache = {}
def denom_min(z):
    for n in range(1, 200):
        if n not in cache: cache[n] = eis_de_norme(n)
        for be in cache[n]:
            # beta * z, z = s + t w
            x = mul(be, (z[0], z[1]))  # fonctionne avec Fractions
            if x[0].denominator == 1 and x[1].denominator == 1:
                return n
    return None
mauvais = sum(1 for u, (z, n) in place.items() if denom_min(z) != n)
print("   norme du plus petit denominateur = nu(e2, u) : %d exceptions sur %d ; normes de %d a %d"
      % (mauvais, len(place), min(n for _, n in place.values()), max(n for _, n in place.values())))
L = list(place.items()); exc = 0; np_ = 0
for (u, (zu, nu_)), (v, (zv, nv)) in combinations(L, 2):
    np_ += 1
    if nu(u, v) != n2(zu[0] - zv[0], zu[1] - zv[1]) * nu_ * nv: exc += 1
print("   paires : %d ; exceptions a nu(u,v) = |zu - zv|^2 nu(c,u) nu(c,v) : %d" % (np_, exc))
print("temps %.1f s" % (time.time() - t0))
