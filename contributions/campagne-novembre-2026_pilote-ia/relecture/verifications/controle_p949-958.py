#!/usr/bin/env python3
"""Contrôles du pilote pour les pages 949-958 du master V346 (Parties LXXI et LXXII, 4 juin).

1. « Charge maximale » d'un tétraèdre (quatre faces d'holonomie 2) : fréquence, dépendance à la numérotation des sommets,
   corrélation entre deux tétraèdres qui partagent une face, une arête ou un sommet. Énumération exacte.
   Convention du master : une valeur de Z3 par arête, orientée du plus petit numéro vers le plus grand ;
   holonomie d'une face (a<b<c) = h(ab) + h(bc) - h(ac) modulo 3.
2. Facteur de Fano d'un comptage sur-poissonien après sélection d'une fraction q des éléments (loi de l'amincissement).
"""
import itertools
import numpy as np

def faces_hol(h, sommets):
    """h : dictionnaire arête (i<j) -> valeur ; renvoie l'holonomie des 4 faces du tétraèdre porté par `sommets` (triés)."""
    out = []
    for a, b, c in itertools.combinations(sorted(sommets), 3):
        out.append((h[(a, b)] + h[(b, c)] - h[(a, c)]) % 3)
    return out

def enumere(sommets_total, tetra1, tetra2=None):
    aretes = sorted({e for T in ([tetra1] + ([tetra2] if tetra2 else [])) for e in itertools.combinations(sorted(T), 2)})
    n1 = n12 = tot = 0
    for vals in itertools.product(range(3), repeat=len(aretes)):
        h = dict(zip(aretes, vals)); tot += 1
        m1 = all(f == 2 for f in faces_hol(h, tetra1))
        n1 += m1
        if tetra2 and m1 and all(f == 2 for f in faces_hol(h, tetra2)): n12 += 1
    return tot, n1, n12

tot, n1, _ = enumere(4, (0, 1, 2, 3))
print(f"1a. tétraèdre isolé : {n1} configurations sur {tot} à quatre faces d'holonomie 2  (1/27 = {1/27:.4f})")

# dépendance à la numérotation : on échange les numéros de deux sommets
aretes = list(itertools.combinations(range(4), 2)); reste = collections = None
compte = {}
for perm in [(1, 0, 2, 3), (0, 2, 1, 3), (0, 1, 3, 2), (3, 1, 2, 0), (1, 2, 3, 0)]:
    garde = 0; n = 0
    for vals in itertools.product(range(3), repeat=6):
        h = dict(zip(aretes, vals))
        if not all(f == 2 for f in faces_hol(h, (0, 1, 2, 3))): continue
        n += 1
        h2 = {}
        for (i, j), v in h.items():
            a, b = perm[i], perm[j]
            h2[(min(a, b), max(a, b))] = v if a < b else (-v) % 3      # même connexion, autre numérotation
        garde += all(f == 2 for f in faces_hol(h2, (0, 1, 2, 3)))
    compte[perm] = (garde, n)
for perm, (g, n) in compte.items():
    print(f"1b. renumérotation {perm} : {g} des {n} tétraèdres « maximaux » le restent")

for nom, t2 in (("une face", (0, 1, 2, 4)), ("une arête", (0, 1, 4, 5)), ("un sommet", (0, 4, 5, 6))):
    tot, n1, n12 = enumere(None, (0, 1, 2, 3), t2)
    print(f"1c. deux tétraèdres partageant {nom} : P(second maximal | premier maximal) = {n12}/{n1} = {n12/n1:.4f}")

rng = np.random.default_rng(3)
print("2. amincissement d'un comptage de moyenne 5 000 et de Fano 25 (binomiale négative), 200 000 tirages")
m, F = 5000, 25.0; p = 1 / F; r = m * p / (1 - p)
X = rng.negative_binomial(r, p, 200000)
for q in (1.0, 0.3, 0.15, 0.05, 0.02):
    Y = rng.binomial(X, q)
    print(f"   fraction gardée {q:>4} : Fano mesuré {Y.var()/Y.mean():6.2f} ; loi q·F + 1 - q = {q*F + 1 - q:6.2f}")
