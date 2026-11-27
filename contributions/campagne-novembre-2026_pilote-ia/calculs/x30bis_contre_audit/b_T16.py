# B. T16 sur tirages : tuile = germe, p = e1, c = e2, f = e3, e4, e5.
import sys, time, math
from noyau import *

t0 = time.time()
rng = random.Random(16)
p, c = GERME[0], GERME[1]
fs = GERME[2:]

def boule_x(a):
    a = [F(v) for v in a]
    assert sum(a) == 1
    b = (sum(v * v for v in a) - 1) / 2
    if any(b - v < 0 for v in a):
        return None
    x = (b, b, a[0], a[1], a[2])
    assert ip(x, x) == 1 and ip(x, p) == -1 and ip(x, c) == -1 and all(nu(x, f) >= 1 for f in fs)
    return x

def boule_w(phi):
    phi = [F(v) for v in phi]
    Phi = sum(phi)
    g = (sum(v * v for v in phi) - Phi * Phi) / (2 * Phi)
    w = (g + Phi - 1, g, phi[0], phi[1], phi[2])
    assert ip(w, w) == 1 and ip(w, p) == -1 and nu(c, w) == Phi
    return w

# constituants lies a p, de coordonnees >= 0 sur f, nu(c, w) > 0 : parcours du residu de p
res = {GERME}; front = [GERME]
for l in range(7):
    nf = []
    for t in front:
        for j in range(1, 5):
            t2 = flip(t, j)
            if t2 not in res: res.add(t2); nf.append(t2)
    front = nf
vois = set()
for t in res:
    for u in t:
        if u != p: vois.add(u)
Wc = [w for w in vois if all(v >= 0 for v in w[2:]) and nu(c, w) > 0]
print("voisins de p trouves : %d ; dans le secteur (w constituants) : %d" % (len(vois), len(Wc)))

def tirage_a():
    while True:
        den = rng.choice([1, 2, 3, 5, 7, 12, 30, 97])
        a1 = F(rng.randint(-6 * den, 6 * den), den); a2 = F(rng.randint(-6 * den, 6 * den), den)
        x = boule_x((a1, a2, 1 - a1 - a2))
        if x is not None: return x

viol = 0; egal = 0; egal_hors = 0; n = 0; minhors = None; nx = 0; nxhors = 0
for it in range(6000):
    x = tirage_a(); nx += 1
    dedans = membre(x)
    if not dedans: nxhors += 1
    Ws = list(rng.sample(Wc, 40))
    for _ in range(20):
        den = rng.choice([1, 2, 5, 11])
        phi = [F(rng.randint(0, 8 * den), den) for _ in range(3)]
        if rng.random() < 0.3: phi[rng.randrange(3)] = F(0)
        if sum(phi) == 0: continue
        Ws.append(boule_w(phi))
    for w in Ws:
        n += 1
        L, R = nu(x, w), F(3, 4) * nu(c, w)
        if L < R: viol += 1
        if L == R:
            egal += 1
            if not dedans: egal_hors += 1
        if not dedans and w in Wc:
            r = L / nu(c, w)
            if minhors is None or r < minhors: minhors = r
print("tirages x : %d (hors empilement : %d) ; couples (x, w) : %d ; violations : %d ; egalites : %d dont x hors : %d"
      % (nx, nxhors, n, viol, egal, egal_hors))
print("plus petit rapport nu(x,w)/nu(c,w), x hors empilement, w constituant : %s = %.6f" % (minhors, float(minhors)))

# approche de 3/4 : x voisin du retourne de f3, w constituant au milieu de l'arete f1 f2 (vu de p et c)
w = (2, -1, 2, 2, 0)
print("w = (2,-1,2,2,0) constituant :", membre(w), " nu(c,w) =", nu(c, w), " coords >= 0 sur f :", all(v >= 0 for v in w[2:]))
flip3 = (1, 1, 1, 1, -1)
print("retourne de f3 :", membre(flip3), " rapport :", nu(flip3, w) / nu(c, w))
for k in [10, 100, 1000, 10 ** 4, 10 ** 6]:
    e = F(1, k)
    x = boule_x((1 + e, 1 + e, -1 - 2 * e))
    print("  eps = 1/%d : x hors empilement : %s ; rapport = %s ~ %.8f ; ecart a 3/4 = %.3e"
          % (k, not membre(x), nu(x, w) / nu(c, w), float(nu(x, w) / nu(c, w)), float(nu(x, w) / nu(c, w) - F(3, 4))))

# boules irrationnelles (flottants, marge 1e-9) : a quelconque reel sur le plan sum a = 1
viol_f = 0; nf = 0
for it in range(20000):
    a1 = rng.uniform(-6, 6); a2 = rng.uniform(-6, 6); a = [a1, a2, 1 - a1 - a2]
    b = (sum(v * v for v in a) - 1) / 2
    if any(b - v < 0 for v in a): continue
    x = (b, b, *a)
    for _ in range(10):
        phi = [rng.uniform(0, 8) for _ in range(3)]
        Phi = sum(phi); g = (sum(v * v for v in phi) - Phi * Phi) / (2 * Phi)
        w = (g + Phi - 1, g, *phi)
        nf += 1
        if (1 - ip(x, w)) / 2 < 0.75 * Phi - 1e-9: viol_f += 1
print("flottants : %d couples, %d violations" % (nf, viol_f))
print("temps %.1f s" % (time.time() - t0))
