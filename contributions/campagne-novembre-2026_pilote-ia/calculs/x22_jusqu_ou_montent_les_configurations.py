#!/usr/bin/env python3
"""X-22 -- jusqu'ou montent les configurations ? Sur le moteur statique du corpus (blob engine.py, sans modification) et son temoin sans viabilite (build_rgg).
<< Etage k >> = groupe de k+1 constituants tous relies entre eux (ma lecture, declaree). Prediction scellee : x22_jusqu_ou_montent_les_configurations_prediction.txt.
Claude, 20 novembre 2026."""
import importlib.util, itertools, json, os
from collections import Counter
import numpy as np, networkx as nx
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(base, 'blob engine.py')); be = importlib.util.module_from_spec(spec); spec.loader.exec_module(be)
out = []
for N, seed in ((800, 0), (800, 1), (1600, 0), (3200, 0)):
    for nom, fab in (('blob', be.build_blob), ('rgg', be.build_rgg)):
        pts, nbr, deg = fab(N, seed); pts = np.asarray(pts)
        G = nx.Graph(); G.add_nodes_from(range(N))
        for u in range(N):
            for v in nbr[u, :deg[u]]: G.add_edge(u, int(v))
        haut = np.zeros(N, int); parEtage = Counter(); v4max = 0.0; n5 = 0
        for c in nx.find_cliques(G):
            k = len(c) - 1; parEtage[k] += 1
            for x in c: haut[x] = max(haut[x], k)
            if len(c) >= 5:                                   # volume a quatre dimensions des groupes de cinq (au plus 20 par groupe maximal)
                for q in itertools.islice(itertools.combinations(c, 5), 20):
                    M = pts[list(q[1:])] - pts[q[0]]          # 4 vecteurs de R^3
                    v4max = max(v4max, abs(np.linalg.det(M @ M.T)) ** 0.5 / 24); n5 += 1
        d = np.sort(np.array([G.degree(u) for u in range(N)]))[::-1]; L = d.sum() / 2
        part = {str(k): float((haut >= k).mean()) for k in (1, 2, 3, 4, 6, 8, 10, 12)}
        r = dict(modele=nom, N=N, graine=seed, liens=int(L), liens_par_constituant=float(L / N), plus_haut_etage=int(haut.max()),
                 part_des_constituants_a_l_etage_au_moins=part, part_ne_depassant_pas_l_etage_2=float((haut <= 2).mean()),
                 repartition_par_plus_haut_etage={str(k): int(v) for k, v in sorted(Counter(haut.tolist()).items())},
                 groupes_maximaux_par_etage={str(k): int(v) for k, v in sorted(parEtage.items())},
                 part_des_liens_portee_par_les_10pc_les_plus_relies=float(d[:N // 10].sum() / d.sum()), degre_max=int(d[0]),
                 liens_par_constituant_requis_par_etage={str(k): k / 2 for k in range(1, 18)},
                 groupes_de_cinq_testes=n5, plus_grand_volume_4D=float(v4max))
        out.append(r); print(json.dumps(r), flush=True); json.dump(out, open('x22_jusqu_ou_montent_les_configurations.json', 'w'), indent=1)
