#!/usr/bin/env python3
"""C-155c -- contre-calcul du C-155 de ChatGPT sur des complexes construits independamment (Claude, 14 novembre 2026)."""
import itertools, json, math
TH = math.acos(1 / 3); C = 6 * TH - 2 * math.pi; out = {}
def cyclique(n):                       # facettes du polytope cyclique C(n, 4) : condition de parite de Gale
    F = []
    for S in itertools.combinations(range(n), 4):
        s = set(S); ok = True
        for i in range(n):
            for j in range(i + 1, n):
                if i in s or j in s: continue
                if sum(1 for x in S if i < x < j) % 2: ok = False; break
            if not ok: break
        if ok: F.append(S)
    return F
def orthoplexe():
    return [tuple(sorted(2 * i + s[i] for i in range(4))) for s in itertools.product((0, 1), repeat=4)]
def comptes(T):
    k = {}
    for t in T:
        for e in itertools.combinations(sorted(t), 2): k[e] = k.get(e, 0) + 1
    faces = {}
    for t in T:
        for f in itertools.combinations(sorted(t), 3): faces[f] = faces.get(f, 0) + 1
    bord = set(e for f, c in faces.items() if c == 1 for e in itertools.combinations(f, 2))
    N0 = len(set(v for t in T for v in t))
    return k, bord, N0, len(faces)
def somme(T):
    k, bord, N0, N2 = comptes(T)
    return sum((math.pi if e in bord else 2 * math.pi) - c * TH for e, c in k.items())
def bissecte(T, e, m):
    a, b = e; new = []
    for t in T:
        if a in t and b in t:
            new.append(tuple(sorted(m if v == b else v for v in t))); new.append(tuple(sorted(m if v == a else v for v in t)))
        else: new.append(t)
    return new
W1 = {}
for nom, T in (('orthoplexe', orthoplexe()), ('cyclique_9', cyclique(9)), ('cyclique_11', cyclique(11)), ('cyclique_15', cyclique(15))):
    k, bord, N0, N2 = comptes(T)
    W1[nom] = dict(N0=N0, N1=len(k), N2=N2, N3=len(T), euler=N0 - len(k) + N2 - len(T), aretes_de_bord=len(bord), somme=somme(T), formule=2 * math.pi * N0 - C * len(T))
out['W1'] = W1
T = cyclique(9); k, _, _, _ = comptes(T); S0 = somme(T)
out['W2'] = dict(fils=len(k), degres=sorted(set(k.values())), ecart_max=max(abs(somme(bissecte(T, e, 99)) - S0 - (2 * math.pi - kk * C)) for e, kk in k.items()))
T = cyclique(15); S = somme(T); N0 = 15; choix = {}
for step in range(100):
    k, _, _, _ = comptes(T)
    e = min(sorted(k), key=lambda x: (round(abs(S + 2 * math.pi - k[x] * C), 12), x))
    choix[k[e]] = choix.get(k[e], 0) + 1; T = bissecte(T, e, N0); N0 += 1; S = somme(T)
k, _, _, _ = comptes(T)
out['W3'] = dict(choix=dict(sorted(choix.items())), N0=N0, N3=len(T), somme_finale=S, par_porteur=S / N0, depart_par_porteur=somme(cyclique(15)) / 15,
                 deficits_extremes_deg=[math.degrees(2 * math.pi - max(k.values()) * TH), math.degrees(2 * math.pi - min(k.values()) * TH)], degre_max=max(k.values()))
T1 = [(0, 1, 2, 3)]; out['W4'] = dict(tetraedre_seul=somme(T1), apres_bissection=somme(bissecte(T1, (0, 1), 4)), variation=somme(bissecte(T1, (0, 1), 4)) - somme(T1), formule=math.pi - C)
T2 = bissecte(T1, (0, 1), 4); T3 = bissecte(T2, (2, 3), 5)      # fil de bord a 2 cellules
out['W4']['k2'] = dict(variation=somme(T3) - somme(T2), formule=math.pi - 2 * C)
json.dump(out, open('c155c.json', 'w'), indent=1); print(json.dumps(out, indent=1))
