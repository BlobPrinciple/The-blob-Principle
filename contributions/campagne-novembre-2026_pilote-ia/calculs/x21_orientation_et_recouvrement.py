#!/usr/bin/env python3
"""X-21 -- << coherence d'orientation >> de deux groupes de quatre partageant une face, sur le moteur statique du corpus (blob engine.py, sans modification), avec la
convention << determinant a sommets ranges par numero >> (ma lecture, attestee comme proxy dans V346 p. 1074). Question : cette coherence mesure-t-elle autre chose que la
part des paires dont les deux tetraedres se chevauchent ? Prediction scellee : x21_orientation_et_recouvrement_prediction.txt. Claude, 20 novembre 2026."""
import importlib.util, itertools, json, os
import numpy as np
from scipy.spatial import Delaunay
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(base, 'blob engine.py')); be = importlib.util.module_from_spec(spec); spec.loader.exec_module(be)
def sg(pts, q):
    q = sorted(q); return np.sign(np.linalg.det(pts[q[1:]] - pts[q[0]]))
def cote(pts, f, x):
    return np.sign(np.linalg.det(np.array([pts[f[1]] - pts[f[0]], pts[f[2]] - pts[f[0]], pts[x] - pts[f[0]]])))
out = []
for N, seed in ((800, 0), (800, 1), (1600, 0)):
    for nom, fab in (('blob', be.build_blob), ('rgg', be.build_rgg)):
        pts, nbr, deg = fab(N, seed); pts = np.asarray(pts); A = [set(int(x) for x in nbr[u, :deg[u]]) for u in range(N)]
        D = {tuple(sorted(int(x) for x in t)) for t in Delaunay(pts).simplices}
        c = dict(opp=[0, 0], meme=[0, 0]); g = [0, 0, 0]   # [paires, concordantes] ; geometriques : [paires, concordantes, du meme cote]
        for u in range(N):
            for v in (x for x in A[u] if x > u):
                for w in (x for x in A[u] & A[v] if x > v):
                    f = (u, v, w); ap = sorted(A[u] & A[v] & A[w])
                    for a, b in itertools.combinations(ap, 2):
                        m = cote(pts, f, a) == cote(pts, f, b); ok = sg(pts, f + (a,)) == sg(pts, f + (b,))
                        k = 'meme' if m else 'opp'; c[k][0] += 1; c[k][1] += int(ok)
                        if tuple(sorted(f + (a,))) in D and tuple(sorted(f + (b,))) in D: g[0] += 1; g[1] += int(ok); g[2] += int(m)
        tot = c['opp'][0] + c['meme'][0]; pm = c['meme'][0] / tot; P = (c['opp'][1] + c['meme'][1]) / tot
        r = dict(modele=nom, N=N, graine=seed, paires=tot, part_du_meme_cote=pm, P_meme_signe=P, P_si_cotes_opposes=c['opp'][1] / c['opp'][0], P_si_meme_cote=c['meme'][1] / c['meme'][0],
                 formule_0_4_plus_0_2_part=0.4 + 0.2 * pm, paires_geometriques=g[0], P_geometriques=(g[1] / g[0] if g[0] else None), geometriques_du_meme_cote=g[2])
        out.append(r); print(json.dumps(r), flush=True); json.dump(out, open('x21_orientation_et_recouvrement.json', 'w'), indent=1)
