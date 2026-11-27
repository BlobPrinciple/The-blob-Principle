#!/usr/bin/env python3
"""EXPLORATION (hors protocole : ni prediction scellee, ni contre-audit) -- 26 novembre 2026, Claude.
Question : au rang 3, les voisins d'un constituant de l'empilement sont-ils les spheres de Ford des entiers d'Eisenstein (Northshield, arXiv:1503.00813) ?
Lecture : le constituant e0 du germe devient un plan ; ses voisins y posent chacun un point de contact w = (m + n*omega)/b, omega = exp(2 i pi/3),
avec b = y2 + y3 + y4 la courbure, m = y3 + y4, n = y4 (unite : le pas du reseau triangulaire des spheres egales).
Dictionnaire a eprouver : un vecteur entier y, rond (<y,y> = 1) et lie a e0 (<y,e0> = -1), est dans l'empilement
   si et seulement si   la fraction w, reduite en alpha/beta dans Z[omega], a pour denominateur un beta de norme b.
Tout est exact (entiers). L'appartenance a l'empilement est decidee par la descente (meme regle que x27, recrite ici)."""
import sys, time, json

def prod(a, b): return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)

def dans_l_empilement(x):
    y = list(x)
    for _ in range(100000):
        j = min(range(5), key=lambda k: y[k]); t = y[j]
        if t >= 0: break
        y = [(-t if k == j else y[k] + t) for k in range(5)]
        if sum(y) <= 0: return False
    return sorted(y) == [0, 0, 0, 0, 1]

# entiers d'Eisenstein a + b*omega, omega^2 = -1 - omega
def N(z): return z[0] * z[0] - z[0] * z[1] + z[1] * z[1]
def mul(z, w): return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0] - z[1] * w[1])
def conj(z): return (z[0] - z[1], -z[1])
def divmod_e(z, w):
    """Division euclidienne dans Z[omega] : z = q*w + r, N(r) < N(w)."""
    n = N(w); t = mul(z, conj(w))                       # z/w = t/n
    best = None
    for qa in (t[0] // n, t[0] // n + 1):
        for qb in (t[1] // n, t[1] // n + 1):
            q = (qa, qb); pq = mul(q, w); r = (z[0] - pq[0], z[1] - pq[1])
            if best is None or N(r) < N(best[1]): best = (q, r)
    assert N(best[1]) < n
    return best
def pgcd(z, w):
    while w != (0, 0): z, w = w, divmod_e(z, w)[1]
    return z

def main(smax):
    t0 = time.time(); R = (smax + 1) // 2 + 1
    vus = dans = ford = accord = 0; desaccords = []; par_b = {}
    for y2 in range(-R, R + 1):
        for y3 in range(-R, R + 1):
            for y4 in range(-R, R + 1):
                b = y2 + y3 + y4
                if b < 1: continue
                Q = y2 * y2 + y3 * y3 + y4 * y4
                if Q % b: continue
                c = Q // b
                if (c - b) % 2 or b + c - 1 > smax: continue
                y = ((b + c) // 2 - 1, (c - b) // 2, y2, y3, y4)
                assert prod(y, y) == 1 and prod(y, (1, 0, 0, 0, 0)) == -1
                vus += 1
                p = dans_l_empilement(y)
                g = pgcd((y3 + y4, y4), (b, 0)); f = (N(g) == b)        # N(beta) = b^2/N(g) = b
                dans += p; ford += f
                if p == f: accord += 1
                elif len(desaccords) < 10: desaccords.append([list(y), p, f])
                if p: par_b[b] = par_b.get(b, 0) + 1
    out = dict(somme_maximale=smax, vecteurs_entiers_ronds_lies_a_e0=vus, dans_l_empilement=dans, spheres_de_Ford_d_Eisenstein=ford, accords=accord,
               desaccords=desaccords, courbure_maximale_vue=max(par_b), duree_s=round(time.time() - t0, 1))
    print(json.dumps(out, ensure_ascii=False))

if __name__ == '__main__': main(int(sys.argv[1]))
