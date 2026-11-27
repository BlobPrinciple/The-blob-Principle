# Noyau du contre-audit X-31. Ecrit a neuf ; n'importe rien du laboratoire.
# Rang r : vecteurs de longueur n = r + 2 (rang 3 : 5, rang 2 : 4), base = germe.
# <x,z> = 2 sum x_k z_k - (sum x)(sum z).
import itertools
from fractions import Fraction
from math import isqrt, gcd

def ip(x, z):
    return 2 * sum(a * b for a, b in zip(x, z)) - sum(x) * sum(z)

def add(*vs):
    return tuple(map(sum, zip(*vs)))

def germe(n):
    return [tuple(1 if i == j else 0 for j in range(n)) for i in range(n)]

def det(m):
    # determinant exact (entiers), elimination de Bareiss
    m = [list(r) for r in m]
    n = len(m); sign = 1; prev = 1
    for k in range(n - 1):
        if m[k][k] == 0:
            for i in range(k + 1, n):
                if m[i][k] != 0:
                    m[k], m[i] = m[i], m[k]; sign = -sign; break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
        prev = m[k][k]
    return sign * m[n - 1][n - 1]

def noyau_entier(rows):
    # rows : (n-1) lignes de longueur n ; vecteur du noyau par mineurs (produit vectoriel generalise)
    n = len(rows[0])
    k = []
    for j in range(n):
        sub = [[r[c] for c in range(n) if c != j] for r in rows]
        k.append((-1) ** j * det(sub))
    g = 0
    for c in k:
        g = gcd(g, abs(c))
    if g == 0:
        return None
    return tuple(c // g for c in k)

def formes(vs):
    # lignes de la forme : <v, .> = (2 v - s(v) 1) . y
    out = []
    for v in vs:
        s = sum(v)
        out.append([2 * a - s for a in v])
    return out

def cotes(cell):
    # les deux boules rondes liees a tous les membres d'une cellule (r+1 boules toutes liees)
    n = len(cell[0])
    k = noyau_entier(formes(cell))
    K = ip(k, k)
    if n == 5:
        # u = s/2 + t k, t^2 K = 3
        s = add(*cell)
        # n = lam k avec lam^2 K = 12 ; cotes = (s +- n)/2
        num = 12
        assert num % K == 0, (cell, K)
        lam = isqrt(num // K); assert lam * lam * K == num
        u = tuple((a + lam * b) // 2 for a, b in zip(s, k))
        v = tuple((a - lam * b) // 2 for a, b in zip(s, k))
    else:
        s = add(*cell)  # u = s + t k, t^2 K = 4
        assert 4 % K == 0, (cell, K)
        lam = isqrt(4 // K); assert lam * lam * K == 4
        u = tuple(a + lam * b for a, b in zip(s, k))
        v = tuple(a - lam * b for a, b in zip(s, k))
    for w in (u, v):
        assert ip(w, w) == 1 and all(ip(w, c) == -1 for c in cell), (cell, w)
    return u, v

def retourne(T, i):
    # retourner le membre i d'une tuile : rang 3 : v' = S - 2v ; rang 2 : v' = 2 S - 3 v
    n = len(T[0]); S = add(*T); v = T[i]
    if n == 5:
        return tuple(a - 2 * b for a, b in zip(S, v))
    return tuple(2 * a - 3 * b for a, b in zip(S, v))

def descente(T, fixes):
    # tant que possible, retourner un membre hors de 'fixes' dont l'autre cote a une somme plus petite
    T = list(T)
    while True:
        for i in range(len(T)):
            if T[i] in fixes:
                continue
            w = retourne(T, i)
            if sum(w) < sum(T[i]):
                T[i] = w
                break
        else:
            return frozenset(T)

def appartient(x):
    # reduction gloutonne par les retournements du germe : y_i < 0 -> s_i
    y = list(x); n = len(y); pas = 0
    while True:
        neg = [i for i in range(n) if y[i] < 0]
        if not neg:
            break
        i = neg[0]
        a = y[i]
        if n == 5:
            y = [(-a if j == i else y[j] + a) for j in range(n)]
        else:
            y = [(-a if j == i else y[j] + 2 * a) for j in range(n)]
        pas += 1
        if pas > 10000:
            return None
    return sum(y) == 1 and sorted(y) == [0] * (n - 1) + [1]
