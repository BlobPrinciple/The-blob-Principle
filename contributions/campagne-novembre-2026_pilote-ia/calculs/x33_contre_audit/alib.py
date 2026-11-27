"""Bibliotheque du contre-audit X-33, ecrite a neuf (aucun import des programmes du laboratoire).
Conventions : R^5, germe e_1..e_5, <x,z> = 2 sum x_k z_k - (sum x)(sum z)."""
import itertools
from fractions import Fraction
from math import isqrt
import numpy as np

GERM = tuple(tuple(1 if i == k else 0 for i in range(5)) for k in range(5))
GERMSET = frozenset(GERM)


def ip(a, b):
    return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)


def other(T, u):
    """Autre cote de la cellule T - {u} : somme(T) - 2u."""
    return tuple(sum(v[k] for v in T) - 2 * u[k] for k in range(5))


def flip(T, u):
    return frozenset((set(T) - {u}) | {other(T, u)})


def wall_separates(T, u):
    """Le mur de T oppose a u separe T du germe (critere du laboratoire : somme de l'autre cote < somme de u)."""
    return sum(other(T, u)) < sum(u)


def gate(u, T, order='min'):
    """Tuile-porte de u, par descente depuis une tuile T contenant u."""
    T = set(T)
    assert u in T
    while True:
        d = [v for v in T if v != u and wall_separates(T, v)]
        if not d:
            return frozenset(T)
        if order == 'min':
            v = min(d)
        elif order == 'max':
            v = max(d)
        else:
            v = order.choice(sorted(d))
        w = other(T, v)
        T.remove(v)
        T.add(w)


def dist(T):
    """Distance de la tuile au germe : nombre de retournements de descente."""
    T = set(T)
    n = 0
    while True:
        d = [v for v in T if wall_separates(T, v)]
        if not d:
            assert frozenset(T) == GERMSET, T
            return n
        v = min(d)
        w = other(T, v)
        T.remove(v)
        T.add(w)
        n += 1


class Pack:
    """Memoire des tuiles-portes."""

    def __init__(self):
        self.T = {u: GERMSET for u in GERM}

    def gate_of(self, u, T=None):
        if u not in self.T:
            assert T is not None
            self.T[u] = gate(u, T)
        return self.T[u]

    def floor(self, u):
        return self.T[u] - {u} if u not in GERMSET else frozenset()

    def Tp(self, u):
        return flip(self.T[u], u)

    def proper_daughters(self, q):
        """Liste (x, f) : x fille propre de q laissant de cote f (parent de q, ou membre du germe si q est dans le germe).
        Par definition : le plancher de x (recalcule par descente) est une cellule de T(q) contenant q."""
        Tq = self.T[q]
        out = []
        for f in sorted(Tq):
            if f == q:
                continue
            x = other(Tq, f)
            Tx = flip(Tq, f)
            g = self.gate_of(x, Tx)
            if g == Tx:
                out.append((x, f))
        return out

    def separating_parents(self, x):
        """Parents f de x tels que le mur de T'(x) oppose a f separe T'(x) du germe."""
        T1 = self.Tp(x)
        return [f for f in self.floor(x) if wall_separates(T1, f)]


def gram(L1, L2):
    A = np.array(L1, dtype=np.int64)
    B = np.array(L2, dtype=np.int64)
    m = max(int(np.abs(A).max()), int(np.abs(B).max()))
    assert 12 * m * m < 2 ** 62
    return 2 * A @ B.T - np.outer(A.sum(1), B.sum(1))


def links_and_overlaps(L):
    """Paires (i<j) liees, et nombre de paires qui se chevauchent (<x,z> > -1), sur toutes les paires de L."""
    links = []
    over = 0
    n = len(L)
    step = 1000
    for d in range(0, n, step):
        G = gram(L[d:d + step], L)
        for i, j in zip(*np.nonzero(G == -1)):
            i = int(i) + d
            j = int(j)
            if j > i:
                links.append((i, j))
        I, J = np.nonzero(G > -1)
        for i, j in zip(I, J):
            i = int(i) + d
            j = int(j)
            if j > i:
                over += 1
    return links, over


def det_int(M):
    M = [list(map(Fraction, r)) for r in M]
    n = len(M)
    d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n):
                M[r][k] -= f * M[c][k]
    assert d.denominator == 1
    return int(d)


def cell_sides(C):
    """Les deux cotes de la cellule C (4 constituants tous lies), calcules sans tuile connue."""
    C = list(C)
    rows = [[2 * c[k] - sum(c) for k in range(5)] for c in C]  # <x, c> = row . x
    kv = []
    for j in range(5):
        sub = [[r[k] for k in range(5) if k != j] for r in rows]
        kv.append((-1) ** j * det_int(sub))
    kk = ip(kv, kv)
    s = [sum(c[k] for c in C) for k in range(5)]
    # u = (s + lam k)/2, lam^2 <k,k> = 12
    assert kk > 0
    num, den = 12, kk
    lam = Fraction(isqrt(num * den), den)
    assert lam * lam == Fraction(num, den), (C, kv)
    out = []
    for sg in (1, -1):
        u = [Fraction(s[k]) + sg * lam * kv[k] for k in range(5)]
        u = [x / 2 for x in u]
        assert all(x.denominator == 1 for x in u)
        u = tuple(int(x) for x in u)
        assert ip(u, u) == 1 and all(ip(u, c) == -1 for c in C)
        out.append(u)
    return out


def cliques4(L, adj):
    """Cliques a 4 sommets ; adj : liste d'ensembles d'indices."""
    out = []
    n = len(L)
    for a in range(n):
        Na = {b for b in adj[a] if b > a}
        for b in Na:
            Nab = {c for c in Na & adj[b] if c > b}
            for c in Nab:
                for d in Nab & adj[c]:
                    if d > c:
                        out.append((a, b, c, d))
    return out


def adjacency(L):
    links, over = links_and_overlaps(L)
    adj = [set() for _ in L]
    for i, j in links:
        adj[i].add(j)
        adj[j].add(i)
    return links, over, adj


PERMS = list(itertools.permutations(range(5)))


def sign(p):
    return (-1) ** sum(1 for i in range(5) for j in range(i + 1, 5) if p[i] > p[j])


def act(p, u):
    """Envoie e_k sur e_{p[k]}."""
    v = [0] * 5
    for k in range(5):
        v[p[k]] = u[k]
    return tuple(v)


def cycle_type(p):
    seen = set()
    out = []
    for i in range(5):
        if i in seen:
            continue
        n = 0
        j = i
        while j not in seen:
            seen.add(j)
            j = p[j]
            n += 1
        out.append(n)
    return tuple(sorted(out))
