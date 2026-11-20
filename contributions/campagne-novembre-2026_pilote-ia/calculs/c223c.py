#!/usr/bin/env python3
"""C-223c et C-228c -- contre-calculs des notes C-223 (625 genealogies de cinq constituants) et C-228 (quatre spins ; cout b|E| - a T ; CHSH) de ChatGPT.
Prediction scellee avant calcul : x21_orientation_et_recouvrement_prediction.txt. Ecrit sans ouvrir ses programmes. Claude, 20 novembre 2026."""
import itertools, json, math
from fractions import Fraction as F
import numpy as np
out = {}
# ---- C-223c
L = 'ABCDE'
def concorde(ordre):   # ordre : tuple des 5 etiquettes ; concordance ssi nombre impair de A, B, C entre D et E
    i, j = sorted((ordre.index('D'), ordre.index('E'))); return (j - i - 1) % 2 == 1
ordres = list(itertools.permutations(L)); base = F(sum(concorde(o) for o in ordres), len(ordres))
gen = []
for racine in L:
    autres = [x for x in L if x != racine]
    for par in itertools.product(L, repeat=4):
        p = dict(zip(autres, par))
        if any(p[x] == x for x in autres): continue
        ok = True
        for x in autres:      # chaque sommet doit remonter a la racine sans cycle
            y = x; vus = set()
            while y != racine:
                if y in vus: ok = False; break
                vus.add(y); y = p[y]
            if not ok: break
        if ok: gen.append((racine, p))
stats = []; comp = {o: 0 for o in ordres}
for racine, p in gen:
    ext = [o for o in ordres if o[0] == racine and all(o.index(p[x]) < o.index(x) for x in p)]
    for o in ext: comp[o] += 1
    stats.append((len(ext), sum(concorde(o) for o in ext)))
fr = [F(c, n) for n, c in stats]
out['C223c'] = dict(genealogies=len(gen), concordance_ordre_uniforme=str(base), genealogies_par_ordre=sorted(set(comp.values())), taux_agrege_pondere=str(F(sum(c for n, c in stats), sum(n for n, c in stats))),
                    minimum=str(min(fr)), maximum=str(max(fr)), a_zero=sum(f == 0 for f in fr), a_un=sum(f == 1 for f in fr), moyenne_non_ponderee=str(sum(fr) / len(fr)), moyenne_non_ponderee_decimale=float(sum(fr) / len(fr)))
# ---- C-228c : quatre spins 1/2
sx = np.array([[0, 1], [1, 0]], complex) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.array([[1, 0], [0, -1]], complex) / 2; I = np.eye(2)
def op(m, k): return np.kron(np.kron(np.kron(*[m if i == k else I for i in range(2)]), m if k == 2 else I), m if k == 3 else I)
S = [[op(m, k) for m in (sx, sy, sz)] for k in range(4)]
J2 = sum(sum(S[k][a] for k in range(4)) @ sum(S[k][a] for k in range(4)) for a in range(3))
w, V = np.linalg.eigh(J2); Z = V[:, np.abs(w) < 1e-9]
eps = lambda a, b, c: (a - b) * (b - c) * (c - a) / 2
chi = sum(eps(a, b, c) * S[0][a] @ S[1][b] @ S[2][c] for a in range(3) for b in range(3) for c in range(3) if eps(a, b, c))
vp = np.linalg.eigvalsh(Z.conj().T @ chi @ Z)
out['C228c_spins'] = dict(dimension_spin_total_nul=int(Z.shape[1]), valeurs_propres_triple_produit=[float(x) for x in vp], racine3_sur_4=math.sqrt(3) / 4)
# ---- cout b|E| - a T
res = {}
for N in (4, 5, 6):
    P = list(itertools.combinations(range(N), 2)); tri = list(itertools.combinations(range(N), 3)); idx = {e: i for i, e in enumerate(P)}
    tm = [sum(1 << idx[e] for e in itertools.combinations(t, 2)) for t in tri]
    E = np.array([bin(b).count('1') for b in range(1 << len(P))]); T = np.zeros(1 << len(P), int); B = np.arange(1 << len(P))
    for m in tm: T += ((B & m) == m)
    for nom, (a, b) in (('a_egal_b', (1, 1)), ('a_egal_2b', (2, 1)), ('a_egal_b_sur_2', (1, 2))):
        Fv = b * E - a * T; mn = Fv.min(); arg = np.nonzero(Fv == mn)[0]
        res[f'N{N}_{nom}'] = dict(minimum=int(mn), nombre_de_minimiseurs=int(len(arg)), aretes_des_minimiseurs=sorted(set(int(E[i]) for i in arg)), seuil_2_plus_3b_sur_a=2 + 3 * b / a)
out['C228c_cout'] = res
S_det = [abs(a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1) for a0 in (1, -1) for a1 in (1, -1) for b0 in (1, -1) for b1 in (1, -1)]
out['C228c_CHSH'] = dict(strategies=len(S_det), maximum_deterministe=max(S_det), quantique=2 * math.sqrt(2))
json.dump(out, open('c223c.json', 'w'), indent=1); print(json.dumps(out, indent=1))
