# Noyau du contre-audit X-30bis. Ecrit a neuf, n'importe rien du laboratoire.
# Vecteurs : tuples de 5 entiers (ou Fractions) dans la base du germe.
from fractions import Fraction as F
from itertools import combinations
import random

def ip(u, v):
    return 2 * sum(a * b for a, b in zip(u, v)) - sum(u) * sum(v)

def nu(u, v):
    return F(1 - ip(u, v), 2)

def add(*vs):
    return tuple(sum(c) for c in zip(*vs))

def sub(u, v):
    return tuple(a - b for a, b in zip(u, v))

def scal(k, u):
    return tuple(k * a for a in u)

GERME = tuple(tuple(1 if i == j else 0 for j in range(5)) for i in range(5))

def flip(tile, j):
    """tuile voisine a travers le mur oppose au membre j (couleur j)"""
    autre = sub(add(*[tile[k] for k in range(5) if k != j]), tile[j])
    return tile[:j] + (autre,) + tile[j + 1:]

def coords(v, tile):
    """coordonnees de v dans la base de la tuile : <v, n_k>/6, n_k = 2 t_k - somme des autres"""
    S = add(*tile)
    out = []
    for k in range(5):
        n = sub(scal(3, tile[k]), S)  # 2 t_k - (S - t_k)
        out.append(F(ip(v, n), 6))
    return out

def membre(x):
    """x vecteur entier rond : est-il un constituant ? descente jusqu'au cone fondamental."""
    if any(F(c).denominator != 1 for c in x):
        return False
    y = [int(c) for c in x]
    if 2 * sum(c * c for c in y) - sum(y) ** 2 != 1:
        return False
    while True:
        if sum(y) <= 0:
            return False
        neg = [j for j in range(5) if y[j] < 0]
        if not neg:
            return sorted(y) == [0, 0, 0, 0, 1]
        j = neg[0]
        v = y[j]
        y = [(-v if k == j else y[k] + v) for k in range(5)]

def porte(u, tile, fixes=None):
    """descente gloutonne : retourne, tant que possible, un membre (autre que ceux de 'fixes')
    dont l'autre cote a une somme plus petite. Renvoie la tuile atteinte et le nombre de pas."""
    if fixes is None:
        fixes = [u]
    tile = tuple(tile)
    pas = 0
    while True:
        bouge = False
        for j in range(5):
            if tile[j] in fixes:
                continue
            t2 = flip(tile, j)
            if sum(t2[j]) < sum(tile[j]):
                tile = t2; pas += 1; bouge = True
                break
        if not bouge:
            return tile, pas

def longueur(tile):
    """longueur de Coxeter, par descente des sommes (tout membre dont l'autre cote est plus petit)"""
    n = 0
    t = tuple(tile)
    while t != GERME:
        for j in range(5):
            t2 = flip(t, j)
            if sum(t2[j]) < sum(t[j]):
                t = t2; n += 1; break
        else:
            raise RuntimeError("bloque hors du germe")
    return n

def marche(L, rng):
    """tuile tiree par une marche reduite (on ne revient pas en arriere en somme) de L pas croissants"""
    t = GERME
    for _ in range(L):
        js = [j for j in range(5) if sum(flip(t, j)[j]) > sum(t[j])]
        j = rng.choice(js)
        t = flip(t, j)
    return t

# --- arithmetique exacte dans Q(sqrt r) : nombres a + b*sqrt(r), r rationnel positif non carre ou carre
def signe_qr(a, b, r):
    """signe de a + b sqrt(r), r >= 0 rationnel"""
    a = F(a); b = F(b); r = F(r)
    if b == 0 or r == 0:
        return (a > 0) - (a < 0)
    sb = 1 if b > 0 else -1
    if a == 0:
        return sb
    sa = 1 if a > 0 else -1
    if sa == sb:
        return sa
    # signes opposes : comparer a^2 et b^2 r
    d = a * a - b * b * r
    if d == 0:
        return 0
    return sa if d > 0 else sb

def noyau_lineaire(rows):
    """base (une seule attendue) du noyau d'une matrice de Fractions, par Gauss"""
    m = [list(map(F, r)) for r in rows]
    nc = len(m[0])
    piv = []
    r = 0
    for c in range(nc):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c); r += 1
        if r == len(m):
            break
    libres = [c for c in range(nc) if c not in piv]
    base = []
    for fcol in libres:
        v = [F(0)] * nc
        v[fcol] = F(1)
        for i, c in enumerate(piv):
            v[c] = -m[i][fcol]
        base.append(v)
    return base

def gram_ligne(u):
    """ligne de la forme <u, .> : coefficients l_k tels que <u, v> = sum l_k v_k"""
    s = sum(u)
    return [2 * a - s for a in u]

def boules_liees(cs):
    """boules rondes liees aux quatre vecteurs cs (<x, c> = -1). Renvoie (x0, d, r) avec x = x0 + lam d,
    lam^2 = r, ou None si pas de solution reelle, ou 'degenere' si les quatre sont dependants."""
    rows = [gram_ligne(c) for c in cs]
    # resoudre rows . x = -1 : solution particuliere + noyau
    m = [list(map(F, r)) + [F(-1)] for r in rows]
    nc = 5
    piv = []; r = 0
    for c in range(nc):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        pv = m[r][c]; m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c); r += 1
        if r == len(m): break
    for i in range(r, len(m)):
        if m[i][nc] != 0:
            return None
    if len(piv) < 4:
        return 'degenere'
    libre = [c for c in range(nc) if c not in piv][0]
    x0 = [F(0)] * nc
    for i, c in enumerate(piv):
        x0[c] = m[i][nc]
    d = [F(0)] * nc; d[libre] = F(1)
    for i, c in enumerate(piv):
        d[c] = -m[i][libre]
    # <x0 + l d, x0 + l d> = 1 ; <x0, d> pas forcement nul
    A = ip(d, d); B = 2 * ip(x0, d); C = ip(x0, x0) - 1
    if A == 0:
        if B == 0:
            return None
        l = -C / B
        return [(tuple(a + l * b for a, b in zip(x0, d)), None, None)]
    # recentrer : l = -B/(2A) + mu, mu^2 = (B^2 - 4AC)/(4A^2)
    disc = (B * B - 4 * A * C) / (4 * A * A)
    if disc < 0:
        return None
    l0 = -B / (2 * A)
    xc = tuple(a + l0 * b for a, b in zip(x0, d))
    return [(xc, tuple(d), disc)]
