#!/usr/bin/env python3
"""X-19 -- contre-verification de la << Clarification n 22 >> du Master propre du 7 juillet 2026 (p. 82) : complexe de Rips (cliques) contre
complexe geometrique restreint (Delaunay inter aretes du Blob), sur le moteur statique du corpus << blob engine.py >> importe sans modification.
Prediction scellee avant calcul : x19_clarification22_prediction.txt. Non aveugle (chiffres du corpus lus). Claude, 18 novembre 2026.
Usage : python3 x19_clarification22.py"""
import importlib.util, itertools, json, os
from collections import defaultdict
import numpy as np, networkx as nx
from scipy.spatial import Delaunay

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(base, 'blob engine.py')); be = importlib.util.module_from_spec(spec); spec.loader.exec_module(be)

def mesure(pts, nbr, deg, N):
    A = [set(int(x) for x in nbr[u, :deg[u]]) for u in range(N)]
    EB = {(u, v) for u in range(N) for v in A[u] if u < v}
    tet = np.sort(Delaunay(np.asarray(pts)).simplices, axis=1)
    ED = set(); FD = set()
    for t in tet:
        t = [int(x) for x in t]
        ED.update(itertools.combinations(t, 2)); FD.update(itertools.combinations(t, 3))
    E = EB & ED
    F = {f for f in FD if all(e in EB for e in itertools.combinations(f, 2))}
    T = [tuple(int(x) for x in t) for t in tet if all(e in EB for e in itertools.combinations([int(x) for x in t], 2))]
    ntf = defaultdict(int)
    for t in T:
        for f in itertools.combinations(t, 3): ntf[f] += 1
    niv = np.zeros(N, int)
    for e in E:
        for u in e: niv[u] = max(niv[u], 1)
    for f in F:
        for u in f: niv[u] = max(niv[u], 2)
    for t in T:
        for u in t: niv[u] = 3
    # anneaux fermes autour d'une arete restreinte
    te = defaultdict(list)
    for t in T:
        for e in itertools.combinations(t, 2): te[e].append(t)
    anneaux = defaultdict(int)
    for e, L in te.items():
        n = len(L); cf = defaultdict(int)
        for t in L:
            for f in itertools.combinations(t, 3):
                if e[0] in f and e[1] in f: cf[f] += 1
        if len(cf) == n and all(c == 2 for c in cf.values()): anneaux[n] += 1
    G = nx.Graph(); G.add_nodes_from(range(N)); G.add_edges_from(EB)
    k4 = 0; cmax = 0; hist = defaultdict(int)
    for c in nx.find_cliques(G): cmax = max(cmax, len(c)); hist[len(c)] += 1
    for (u, v) in EB:
        C = sorted(w for w in A[u] & A[v] if w > v)
        for i, a in enumerate(C):
            for b in C[i + 1:]:
                if b in A[a]: k4 += 1
    grandes = sum(c for s, c in hist.items() if s > 4); tot4 = sum(c for s, c in hist.items() if s >= 4)
    nE, nF, nT = len(E), len(F), len(T)
    return dict(N=N, aretes_blob=len(EB), degre_moyen=2 * len(EB) / N, part_non_geometrique=1 - nE / len(EB), E_sur_V=nE / N, F_sur_V=nF / N, T_sur_V=nT / N,
                chi_sur_V=(N - nE + nF - nT) / N, tiers=dict(aucun=float((niv == 0).mean()), arete=float((niv == 1).mean()), triangle=float((niv == 2).mean()), tetraedre=float((niv == 3).mean())),
                triangles_nus=sum(1 for f in F if ntf[f] == 0) / max(nF, 1), triangles_a_deux=sum(1 for f in F if ntf[f] == 2) / max(nF, 1),
                K4_cliques_sur_N=k4 / N, tetra_Delaunay_sur_N=len(tet) / N, K4_sur_tetra_Delaunay=k4 / len(tet), plus_grande_clique=cmax,
                part_cliques_maximales_au_dessus_de_4_parmi_celles_de_taille_au_moins_4=grandes / max(tot4, 1),
                anneaux_fermes={str(k): v for k, v in sorted(anneaux.items())}, part_aretes_anneau_5_ou_6=(anneaux[5] + anneaux[6]) / max(nE, 1))

if __name__ == '__main__':
    out = []
    for N, seed in ((800, 0), (800, 1), (1600, 0)):
        for nom, f in (('blob', be.build_blob), ('rgg', be.build_rgg)):
            pts, nbr, deg = f(N, seed); r = mesure(pts, nbr, deg, N); r.update(modele=nom, graine=seed); out.append(r); print(json.dumps(r), flush=True)
            json.dump(out, open('x19_clarification22.json', 'w'), indent=1)
