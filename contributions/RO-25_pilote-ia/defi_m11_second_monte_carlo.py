#!/usr/bin/env python3
"""DEFI-M11 — seconde implémentation indépendante du Monte-Carlo (Python pur, ensembles).

Pilote IA du laboratoire (Claude, Anthropic), 20 octobre 2026.
Aucun code commun avec defi_m11_monte_carlo.py : graphes en listes d'ensembles,
S_sim recalculé à partir des compteurs (triangles, somme des carrés des degrés),
générateur aléatoire de la bibliothèque standard (random.Random), naissance
uniforme (theta = 0) par tirage direct de k cibles distinctes.
Mesure le demi-temps de la moyenne des triangles du nouveau-né (secteur M = 2N − 2,
k = 4) pour N = 12, 16, 24, et la moyenne d'équilibre par une chaîne séparée.

Usage : python3 defi_m11_second_monte_carlo.py  ->  defi_m11_second_monte_carlo.json
"""
import json
import math
import pathlib
import random

ICI = pathlib.Path(__file__).resolve().parent
BETA, TAU = 0.30, 0.50


class Graphe:
    def __init__(self, n, aretes):
        self.n = n
        self.v = [set() for _ in range(n)]
        self.E = []
        self.tri = 0
        self.q = 0
        for a, b in aretes:
            self.ajouter(a, b)

    def ajouter(self, a, b):
        self.tri += len(self.v[a] & self.v[b])
        self.q += 2 * (len(self.v[a]) + len(self.v[b])) + 2
        self.v[a].add(b)
        self.v[b].add(a)
        self.E.append((a, b))

    def retirer(self, i):
        a, b = self.E[i]
        self.v[a].discard(b)
        self.v[b].discard(a)
        self.tri -= len(self.v[a] & self.v[b])
        self.q -= 2 * (len(self.v[a]) + len(self.v[b])) + 2
        self.E[i] = self.E[-1]
        self.E.pop()
        return a, b

    def S(self):
        m = len(self.E)
        mu = 2 * m / self.n
        return math.log(1 + self.tri) - BETA * math.sqrt(max(self.q / self.n - mu * mu, 0)) / mu

    def echange(self, rnd):
        n = self.n
        while True:
            x, y = rnd.randrange(n), rnd.randrange(n)
            if x != y and y not in self.v[x]:
                break
        i = rnd.randrange(len(self.E))
        s0 = self.S()
        a, b = self.retirer(i)
        self.ajouter(x, y)
        d = n * (self.S() - s0) / TAU
        if d >= 0 or rnd.random() < math.exp(d):
            return
        self.retirer(len(self.E) - 1)
        self.ajouter(a, b)

    def tri_sommet(self, s):
        vs = list(self.v[s])
        return sum(1 for i in range(len(vs)) for j in range(i + 1, len(vs)) if vs[j] in self.v[vs[i]])


def aleatoire(n, m, rnd):
    paires = [(a, b) for a in range(n) for b in range(a + 1, n)]
    return Graphe(n, rnd.sample(paires, m))


def main():
    out = []
    for n, R, bal in ((12, 400, 40), (16, 400, 60), (24, 300, 120)):
        m, k = 2 * n - 2, 4
        n1, m1 = n + 1, m + k
        rnd = random.Random(424242 + n)
        g = aleatoire(n, m, rnd)
        for _ in range(200 * m):
            g.echange(rnd)
        reperes = [0, 1, 2, 4, 8, 16, 32, 64, 120]
        reperes = [r for r in reperes if r <= bal]
        somme = [0.0] * len(reperes)
        for r in range(R):
            for _ in range(20 * m):
                g.echange(rnd)
            cibles = rnd.sample(range(n), k)
            h = Graphe(n1, list(g.E) + [(c, n) for c in cibles])
            t = 0
            for j, rep in enumerate(reperes):
                while t < rep * m1:
                    h.echange(rnd)
                    t += 1
                somme[j] += h.tri_sommet(n)
        moy = [s / R for s in somme]
        e = aleatoire(n1, m1, rnd)
        for _ in range(200 * m1):
            e.echange(rnd)
        acc = []
        for i in range(4000):
            for _ in range(m1 // 2):
                e.echange(rnd)
            acc.append(e.tri_sommet(i % n1))
        eq = sum(acc) / len(acc)
        ecart = [x - eq for x in moy]
        t_demi = None
        for j in range(1, len(reperes)):
            if abs(ecart[j]) <= abs(ecart[0]) / 2:
                t0, t1 = max(reperes[j - 1], 0.5), reperes[j]
                e0, e1 = abs(ecart[j - 1]), abs(ecart[j])
                f = (e0 - abs(ecart[0]) / 2) / (e0 - e1) if e0 != e1 else 1.0
                t_demi = math.exp(math.log(t0) + f * (math.log(t1) - math.log(t0)))
                break
        ligne = {"N": n, "R": R, "reperes_balayages": reperes, "T_v_moyen": moy, "T_v_equilibre": eq,
                 "t_demi_balayages": t_demi}
        out.append(ligne)
        print(n, "T_v", [round(x, 2) for x in moy], "éq", round(eq, 2), "t½", None if t_demi is None else round(t_demi, 1), flush=True)
    (ICI / "defi_m11_second_monte_carlo.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
