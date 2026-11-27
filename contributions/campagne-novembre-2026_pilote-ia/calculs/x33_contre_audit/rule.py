"""La regle de T28, mise en oeuvre a neuf, et outils de controle de tissus."""
import itertools, random
from alib import *

M = {v: other(GERMSET, v) for v in GERM}          # M_v : cote au-dela de la cellule du germe qui ne contient pas v
PAL1 = frozenset(M.values())


class Run:
    def __init__(self, P=None):
        self.P = P or Pack()
        self.gen = {u: 0 for u in GERM}
        self.last = {}          # derniere fille (regle)
        self.rmother = {}       # mere au sens de la regle
        self.h = 0

    def options(self, p):
        """Filles permises a p a la generation suivante (h >= 1 deja faite)."""
        P = self.P
        if p not in self.last:
            if self.h == 0:
                raise ValueError
            return [x for x, f in P.proper_daughters(p)]
        d = self.last[p]
        Td = P.T[d]
        return [x for x, f in P.proper_daughters(d) if p in Td and p != f]

    def step1(self, derangement):
        """derangement : dict u -> v (v != u) ; la fille de u est M_v."""
        for u, v in derangement.items():
            assert u != v
            x = M[v]
            self.P.gate_of(x, GERMSET - {v} | {x})
            self.gen[x] = 1
            self.last[u] = x
            self.rmother[x] = u
        assert len(set(derangement.values())) == 5
        self.h = 1

    def requesters(self):
        return sorted(self.gen)

    def step(self, assign):
        """assign : dict p -> fille. Controle complet de la regle."""
        born = set(self.gen)
        reqs = self.requesters()
        assert set(assign) == set(reqs)
        vals = list(assign.values())
        assert len(set(vals)) == len(vals), 'meme fille deux fois'
        for p, x in assign.items():
            assert x in self.options(p), 'fille non permise'
            assert x not in born, 'fille deja nee'
        self.h += 1
        for p, x in assign.items():
            self.gen[x] = self.h
            self.last[p] = x
            self.rmother[x] = p

    def random_step(self, rng):
        reqs = self.requesters()
        rng.shuffle(reqs)
        used = set()
        assign = {}
        for p in reqs:
            opts = [x for x in self.options(p) if x not in used and x not in self.gen]
            if not opts:
                return False
            x = rng.choice(opts)
            assign[p] = x
            used.add(x)
        self.step(assign)
        return True


def derangements():
    out = []
    for p in itertools.permutations(range(5)):
        if all(p[i] != i for i in range(5)):
            out.append({GERM[i]: GERM[p[i]] for i in range(5)})
    return out


def proper_mother(P, x):
    """Meres propres de x (par definition, sans T27)."""
    if x in GERMSET:
        return []
    F = P.floor(x)
    return [f for f in F if F <= P.T[f]]


def leaves_out(P, c, x):
    """Le parent de c (ou membre du germe) que la fille propre x de c laisse de cote."""
    Tc = P.T[c]
    fs = [f for f in Tc if f != c and other(Tc, f) == x]
    assert len(fs) == 1
    return fs[0]
