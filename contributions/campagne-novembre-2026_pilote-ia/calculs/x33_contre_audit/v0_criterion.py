"""V0 : le critere de descente (somme des coordonnees) contre une vraie distance BFS sur le graphe des tuiles, rayon R.
Et : la tuile-porte ne depend pas de l'ordre de descente."""
import json, random, sys, time
from alib import *

R = int(sys.argv[1])
t0 = time.time()
D = {GERMSET: 0}
front = [GERMSET]
for r in range(1, R + 1):
    nf = []
    for T in front:
        for u in T:
            T2 = flip(T, u)
            if T2 not in D:
                D[T2] = r
                nf.append(T2)
    front = nf
bad_crit = 0
bad_dist = 0
checked = 0
for T, d in D.items():
    if d == R:
        continue
    checked += 1
    for u in T:
        T2 = flip(T, u)
        closer = D[T2] == d - 1
        if closer != wall_separates(T, u):
            bad_crit += 1
        if D[T2] not in (d - 1, d + 1):
            bad_dist += 1
    if dist(T) != d:
        bad_dist += 1
# gate order independence
rng = random.Random(7)
gate_bad = 0
ntest = 0
for T, d in D.items():
    if d < 2:
        continue
    for u in T:
        g1 = gate(u, T, 'min'); g2 = gate(u, T, 'max'); g3 = gate(u, T, rng)
        ntest += 1
        if not (g1 == g2 == g3):
            gate_bad += 1
counts = {}
for d in D.values():
    counts[d] = counts.get(d, 0) + 1
print(json.dumps(dict(partie='V0', rayon=R, tuiles_par_distance=counts, tuiles_controlees=checked,
                      desaccords_critere_vs_BFS=bad_crit, desaccords_distance=bad_dist,
                      descentes_testees=ntest, portes_dependant_de_l_ordre=gate_bad, duree_s=round(time.time() - t0, 1))))
