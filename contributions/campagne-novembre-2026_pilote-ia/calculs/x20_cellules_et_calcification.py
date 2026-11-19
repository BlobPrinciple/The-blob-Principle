#!/usr/bin/env python3
"""X-20 -- sur le moteur statique du corpus (blob engine.py, sans modification) : les K4 qui sont des cellules de Delaunay et ceux qui ne le sont pas se distinguent-ils par
l'accumulation de liens (calcification), le degre, le volume, la longueur des liens ? Prediction scellee : x20_cellules_et_calcification_prediction.txt.
Claude, 19 novembre 2026. Usage : python3 x20_cellules_et_calcification.py"""
import importlib.util, itertools, json, os
import numpy as np
from scipy.spatial import Delaunay
from scipy.stats import rankdata
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(base, 'blob engine.py')); be = importlib.util.module_from_spec(spec); spec.loader.exec_module(be)
def depasse(x, y):
    """Probabilite qu'un element de x depasse un element de y (ex aequo comptes pour moitie)."""
    r = rankdata(np.concatenate([x, y])); nx, ny = len(x), len(y); return float((r[:nx].sum() - nx * (nx + 1) / 2) / (nx * ny))
out = []
for N, seed in ((800, 0), (800, 1), (1600, 0)):
    pts, nbr, deg = be.build_blob(N, seed); pts = np.asarray(pts); A = [set(int(x) for x in nbr[u, :deg[u]]) for u in range(N)]
    D = {tuple(sorted(int(x) for x in t)) for t in Delaunay(pts).simplices}
    geo = []; rows = []
    for u in range(N):
        for v in (x for x in A[u] if x > u):
            C = sorted(w for w in A[u] & A[v] if w > v)
            for i, a in enumerate(C):
                for b in C[i + 1:]:
                    if b in A[a]:
                        q = (u, v, a, b); E = list(itertools.combinations(q, 2))
                        calc = np.mean([len(A[x] & A[y]) for x, y in E]); dg = np.mean([len(A[x]) for x in q])
                        vol = abs(np.linalg.det(pts[[v, a, b]] - pts[u])) / 6; lon = np.mean([np.linalg.norm(pts[x] - pts[y]) for x, y in E])
                        geo.append(q in D); rows.append((calc, dg, vol, lon))
    geo = np.array(geo); R = np.array(rows); g, ng = R[geo], R[~geo]
    r = dict(N=N, graine=seed, K4=int(len(geo)), geometriques=int(geo.sum()), part_geometrique=float(geo.mean()))
    for k, nom in enumerate(('calcification', 'degre', 'volume', 'longueur')):
        r[nom] = dict(moyenne_geometriques=float(g[:, k].mean()), moyenne_non_geometriques=float(ng[:, k].mean()), probabilite_non_geometrique_depasse=depasse(ng[:, k], g[:, k]))
    out.append(r); print(json.dumps(r), flush=True); json.dump(out, open('x20_cellules_et_calcification.json', 'w'), indent=1)
