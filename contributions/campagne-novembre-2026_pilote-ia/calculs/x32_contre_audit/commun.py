"""Outils propres au contre-audit X-32 (aucun import du laboratoire).
Vecteurs : tuples de 5 entiers Python (arithmetique exacte). Germe = base canonique.
<x,z> = 2 sum x_k z_k - (sum x)(sum z)."""
from math import gcd, isqrt
from fractions import Fraction
import numpy as np

GERME = tuple(tuple(1 if i == j else 0 for j in range(5)) for i in range(5))
GERME_SET = frozenset(GERME)


def pr(a, b):
    return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def autre_cote(cellule, u):
    """Autre cote de la cellule (4 constituants) dont u est un cote : u + u' = somme de la cellule."""
    return sub(add(*cellule), u)


def det(M):
    """Determinant entier exact (Bareiss)."""
    M = [list(r) for r in M]
    n = len(M); sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            for i in range(k + 1, n):
                if M[i][k] != 0:
                    M[k], M[i] = M[i], M[k]; sign = -sign; break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[-1][-1]


def cotes_par_algebre(cell):
    """Les deux boules rondes liees aux quatre membres d'une cellule, calculees par algebre lineaire exacte
    (sans connaitre aucun cote) : y = s/2 +- lam n/2, n vecteur nul G-orthogonal, lam^2 = 12/<n,n>."""
    rows = [tuple(2 * a[k] - sum(a) for k in range(5)) for a in cell]
    n = []
    for j in range(5):
        minor = [[r[k] for k in range(5) if k != j] for r in rows]
        n.append((-1) ** j * det(minor))
    g = 0
    for v in n: g = gcd(g, v)
    n = [v // g for v in n]
    nn = pr(n, n)
    assert nn > 0
    q = Fraction(12, nn)
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    assert a * a == q.numerator and b * b == q.denominator, 'lambda non rationnel'
    lam = Fraction(a, b)
    s = add(*cell)
    out = []
    for e in (1, -1):
        y = [Fraction(s[k], 2) + e * lam * n[k] / 2 for k in range(5)]
        assert all(v.denominator == 1 for v in y), 'cote non entier'
        y = tuple(int(v) for v in y)
        assert pr(y, y) == 1 and all(pr(y, c) == -1 for c in cell)
        out.append(y)
    return out


def descente(tuile, u):
    """Tuile-porte de u par descente : tant que possible, retourner un constituant v != u dont l'autre cote
    (de la cellule tuile - {v}) a une somme plus petite que celle de v. Retourne (frozenset tuile, nombre de pas)."""
    t = list(tuile)
    assert u in t
    pas = 0
    while True:
        S = add(*t)
        moved = False
        for j, v in enumerate(t):
            if v == u: continue
            w = tuple(S[k] - 2 * v[k] for k in range(5))
            if sum(w) < sum(v):
                t[j] = w; pas += 1; moved = True; break
        if not moved:
            return frozenset(t), pas


def separe(tuile, v):
    """Le mur de la tuile opposee a v separe-t-il la tuile du germe ? (autre cote plus petit en somme)"""
    w = autre_cote([x for x in tuile if x != v], v)
    return sum(w) < sum(v)


def gram_check(vecs, chunk=1024):
    """Retourne (nombre de paires distinctes avec produit > -1, matrice de liens sous forme de liste d'adjacence)."""
    M = np.array(vecs, dtype=np.int64)
    assert np.abs(M).max() < 10 ** 7
    s = M.sum(1)
    over = 0
    adj = [None] * len(vecs)
    for d in range(0, len(vecs), chunk):
        G = 2 * M[d:d + chunk] @ M.T - np.outer(s[d:d + chunk], s)
        lig = np.arange(G.shape[0])
        assert (G[lig, d + lig] == 1).all()
        G[lig, d + lig] = -10
        over += int((G > -1).sum())
        for i in range(G.shape[0]):
            adj[d + i] = np.nonzero(G[i] == -1)[0]
    return over // 2, adj
