#!/usr/bin/env python3
"""C-231c et C-230c -- contre-calculs independants des notes C-230 et C-231 de ChatGPT. Tissus de d-simplexes empiles (N = 64, d = 1..12), deux regles de collage,
suppression aleatoire de liens ; puis deux controles de C-230 (etage a budget de liens fixe ; stabilite des orbites selon la dimension).
Prediction scellee : c231c_prediction.txt. Claude, 20 novembre 2026."""
import itertools, json
import numpy as np, networkx as nx
N = 64; out = dict(tissus=[], c230={})
def tissu(d, regle, rng):
    G = nx.complete_graph(d + 1); fac = [tuple(c) for c in itertools.combinations(range(d + 1), d)]
    for v in range(d + 1, N):
        i = rng.integers(len(fac)) if regle == 'hasard' else len(fac) - 1
        f = fac.pop(i); G.add_edges_from((v, u) for u in f)
        fac.extend(tuple(x for x in f if x != u) + (v,) for u in f)      # les d nouvelles facettes frontiere
    return G
for d in range(1, 13):
    for regle in ('hasard', 'derniere'):
        r = dict(d=d, regle=regle, M=None, M_formule=d * N - d * (d + 1) // 2, lam=[], diam=[], connexe={}, plus_grand={}, part_sommets_a_d_liens=[])
        acc = {p: [[], []] for p in (0.2, 0.4, 0.6)}
        for g in range(8):
            rng = np.random.default_rng([d, regle == 'hasard', g]); G = tissu(d, regle, rng)
            assert G.number_of_edges() == r['M_formule']; r['M'] = G.number_of_edges()
            r['lam'].append(nx.edge_connectivity(G)); r['diam'].append(nx.diameter(G)); r['part_sommets_a_d_liens'].append(sum(1 for _, k in G.degree() if k == d) / N)
            E = np.array(G.edges())
            for p in acc:
                for _ in range(120):
                    H = nx.Graph(); H.add_nodes_from(range(N)); H.add_edges_from(E[rng.random(len(E)) >= p])
                    c = max(len(x) for x in nx.connected_components(H)); acc[p][0].append(c == N); acc[p][1].append(c / N)
        for p in acc: r['connexe'][str(p)] = float(np.mean(acc[p][0])); r['plus_grand'][str(p)] = float(np.mean(acc[p][1]))
        r['lam'] = sorted(set(r['lam'])); r['diam'] = [min(r['diam']), max(r['diam'])]; r['part_sommets_a_d_liens'] = float(np.mean(r['part_sommets_a_d_liens']))
        out['tissus'].append(r); print(json.dumps(r), flush=True)
# P5 : d optimal pour gain = P(connexe) - eps * M, regle au hasard
opt = {}
for p in ('0.2', '0.4', '0.6'):
    for eps in (0.0002, 0.0005, 0.001, 0.002, 0.004, 0.008):
        T = [t for t in out['tissus'] if t['regle'] == 'hasard']; opt[f'p={p},eps={eps}'] = max(T, key=lambda t: t['connexe'][p] - eps * t['M'])['d']
out['d_optimal_selon_cout_pose'] = opt; print(json.dumps(opt))
# C-230c Q1 : 200 constituants, 400 liens
A = nx.complete_graph(21); A.add_edges_from((v, v - 1) for v in range(21, 200)); A.add_edges_from((v, v - 2) for v in range(23, 34)); 
B = nx.Graph(); B.add_nodes_from(range(200)); B.add_edges_from((i, (i + 1) % 200) for i in range(200)); B.add_edges_from((i, (i + 2) % 200) for i in range(200))
out['c230']['Q1'] = dict(A=dict(sommets=A.number_of_nodes(), liens=A.number_of_edges(), etage=max(len(c) for c in nx.find_cliques(A)) - 1),
                         B=dict(sommets=B.number_of_nodes(), liens=B.number_of_edges(), etage=max(len(c) for c in nx.find_cliques(B)) - 1))
# C-230c Q2 : force en r^-(d-1) ; potentiel effectif U = L^2/(2 r^2) + V(r) ; stabilite de l'orbite circulaire r = 1 : U''(1) avec L^2 fixe par U'(1) = 0
q2 = {}
for d in range(2, 8):
    # F = -1/r^(d-1) ; L^2 = r^3 * |F| en r = 1 = 1 ; U'' = 3 L^2 / r^4 + dF... : U''(1) = 3 - (d-1) = 4 - d
    h = 1e-4; V = (lambda r: np.log(r)) if d == 2 else (lambda r: -r ** (2 - d) / (d - 2)); U = lambda r: 0.5 / r ** 2 + V(r)
    q2[str(d)] = dict(U2_numerique=float((U(1 + h) - 2 * U(1) + U(1 - h)) / h ** 2), U2_exact=4 - d)
out['c230']['Q2'] = q2; print(json.dumps(out['c230']))
json.dump(out, open('c231c.json', 'w'), indent=1)
