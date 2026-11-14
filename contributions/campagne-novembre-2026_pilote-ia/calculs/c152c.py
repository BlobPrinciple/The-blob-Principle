#!/usr/bin/env python3
"""C-152c -- Interpenetration des tissus de C-132 bis (Claude, 14 novembre 2026). Predictions : c152c_prediction.txt.
Trajectoires exactes du bras L de c132_audit.py, rejouees. Usage : python3 c152c.py [L|P]"""
import itertools, json, math, sys
import numpy as np
import c132_audit as c
from c120 import vol6

EDG = list(itertools.combinations(range(4), 2))


def axes_separateurs(A, B):
    """A, B : (n, 4, 3). Rend la profondeur de chevauchement (> 0 : interieurs communs), par paire."""
    ax = []
    for T in (A, B):
        for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
            ax.append(np.cross(T[:, j] - T[:, i], T[:, k] - T[:, i]))
    for i, j in EDG:
        for k, l in EDG:
            ax.append(np.cross(A[:, j] - A[:, i], B[:, l] - B[:, k]))
    prof = np.full(len(A), np.inf)
    for a in ax:
        nrm = np.linalg.norm(a, axis=1); ok = nrm > 1e-12
        u = a / np.maximum(nrm, 1e-300)[:, None]
        pa = np.einsum('nvk,nk->nv', A, u); pb = np.einsum('nvk,nk->nv', B, u)
        rec = np.minimum(pa.max(1), pb.max(1)) - np.maximum(pa.min(1), pb.min(1))
        prof = np.where(ok, np.minimum(prof, rec), prof)
    return prof


def analyse(m):
    ids = sorted(m.X); pos = {v: i for i, v in enumerate(ids)}; X = np.array([m.X[v] for v in ids]); TT = sorted(m.T)
    T = np.array([[pos[v] for v in t] for t in TT]); P = X[T]
    # T1 : sommets enfermes
    t1 = 0
    for t in range(len(TT)):
        M = np.vstack([P[t].T, np.ones(4)])
        lam = np.linalg.solve(M, np.vstack([X.T, np.ones(len(X))]))
        ins = (lam > 1e-7).all(0); ins[T[t]] = False; t1 += int(ins.sum())
    # T2 : paires en chevauchement
    I, J = np.triu_indices(len(TT), 1)
    prof = axes_separateurs(P[I], P[J])
    ch = prof > 1e-6
    partage = np.array([len(set(T[i]) & set(T[j])) for i, j in zip(I[ch], J[ch])]) if ch.any() else np.array([], int)
    # T3 : angles diedres autour des aretes
    inc = {}
    for k, t in enumerate(T):
        for a, b in EDG:
            e = tuple(sorted((t[a], t[b]))); o = [v for v in t if v not in e]
            inc.setdefault(e, []).append(o)
    faces = {}
    for t in T:
        for f in itertools.combinations(sorted(t), 3): faces[f] = faces.get(f, 0) + 1
    bord = set(e for f, n in faces.items() if n == 1 for e in itertools.combinations(f, 2))
    ecarts = []; multip = []
    for e, L in inc.items():
        if e in bord: continue
        u = X[e[1]] - X[e[0]]; u /= np.linalg.norm(u); s = 0.0
        for o1, o2 in L:
            a = X[o1] - X[e[0]]; b = X[o2] - X[e[0]]; a -= a.dot(u) * u; b -= b.dot(u) * u
            s += math.degrees(math.acos(max(-1, min(1, a.dot(b) / np.linalg.norm(a) / np.linalg.norm(b)))))
        ecarts.append(s - 360.0); multip.append(len(L))
    deg_arete = max(len(L) for L in inc.values())
    vols = np.array([vol6(m.X, t) / 6 for t in TT])
    return dict(cellules=len(TT), sommets_enfermes=t1, paires_en_chevauchement=int(ch.sum()), profondeur_max=float(prof.max()),
                chevauchements_par_sommets_partages={str(k): int((partage == k).sum()) for k in range(4)},
                aretes_interieures=len(ecarts), ecart_angle_max=float(max(map(abs, ecarts))) if ecarts else None,
                aretes_a_720=int(sum(abs(x - 360) < 1e-3 for x in ecarts)), aretes_hors_360=int(sum(abs(x) > 1e-4 for x in ecarts)),
                cellules_max_autour_d_une_arete=deg_arete, volume_min=float(vols.min()), somme_volumes=float(vols.sum()))


if __name__ == '__main__':
    # temoins
    reg = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(8)
    n = np.cross(reg[1] - reg[0], reg[2] - reg[0]); n /= np.linalg.norm(n); apex2 = reg[3] - 2 * np.dot(reg[3] - reg[0], n) * n
    A = np.array([reg]); miroir = np.array([[reg[0], reg[1], reg[2], apex2]]); meme = np.array([[reg[0], reg[1], reg[2], reg[3] + 0.05 * (reg[0] + reg[1] + reg[2]) / 3 - 0.05 * reg[3]]])
    out = dict(temoins=dict(colles_cotes_opposes=float(axes_separateurs(A, miroir)[0]), colles_meme_cote=float(axes_separateurs(A, meme)[0])))
    print(out['temoins'], flush=True)
    arm = sys.argv[1] if len(sys.argv) > 1 else 'L'
    orig = c.relax; st = {}
    def espion(m, Vref):
        r = orig(m, Vref); st['m'] = m; return r
    c.relax = espion
    for seed in (1320, 1321, 1322):
        rel = {}
        c.CHECK = tuple(range(1, 32)) + (63, 127)
        c.HOOK = lambda row: rel.__setitem__(row['n'], dict(E=row['E'], nact=row['nact'], **analyse(st['m'])))
        c.run(arm, seed, 127)
        out[str(seed)] = rel
        prem2 = next((k for k in sorted(rel) if rel[k]['paires_en_chevauchement']), None); prem1 = next((k for k in sorted(rel) if rel[k]['sommets_enfermes']), None)
        print(seed, 'premier chevauchement', prem2, 'premier sommet enferme', prem1, flush=True)
        for k in (1, 3, 7, 15, 31, 63, 127): print(seed, k, json.dumps(rel[k]), flush=True)
    json.dump(out, open(f'c152c_{arm}.json', 'w'), indent=1)
