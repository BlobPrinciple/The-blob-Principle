#!/usr/bin/env python3
"""Contrôles du pilote pour les pages 966-976 du master V346 (Parties LXXV à LXXVIII, 4-5 juin).
Moteur : celui de l'auteur (gap curl colab.py : build_initial, run_mcmc_canonical), inchangé. N = 1 000, kappa = 6,6.

A. « Polarisation chirale » : deux tétraèdres qui partagent une face, « même chiralité » = même signe du volume orienté,
   sommets rangés par numéro croissant. Décomposition : même chiralité <=> (apex du même côté de la face) XOR (parités d'insertion différentes).
   Prédiction du pilote si les numéros sont sans lien avec la géométrie : P(même chiralité) = 0,4 + 0,2 P(même côté).
B. Ségrégation « énergie sombre / matière » par terciles de degré : arêtes pures incidentes / tétraèdres incidents.
C. Premier nombre de Betti des amas de matière (composantes du sous-graphe induit par les sommets de tétraèdres).
Usage : controle_p966-976.py "<chemin de gap curl colab.py>"
"""
import sys, itertools, collections
import numpy as np

src = open(sys.argv[1], encoding='utf-8').read()
espace = {}
exec(compile(src[:src.index('# --------------------- GAP CURL DE HODGE')], 'moteur_de_l_auteur', 'exec'), espace)
build_initial, run_mcmc_canonical = espace['build_initial'], espace['run_mcmc_canonical']

# parité d'insertion : énumération exacte sur 5 numéros en ordre aléatoire
eg = tot = 0
for perm in itertools.permutations(range(5)):
    a, b, c, d, e = perm
    rd = sum(x < d for x in (a, b, c)); re_ = sum(x < e for x in (a, b, c))
    eg += (rd - re_) % 2 == 0; tot += 1
print(f"A0. numéros aléatoires : P(parités d'insertion égales) = {eg}/{tot} = {eg/tot:.2f}  ->  P(même chiralité) = {1-eg/tot:.1f} + {2*eg/tot-1:.1f} P(même côté)")

def chir(P, t):
    a, b, c, d = sorted(t)
    return np.sign(np.linalg.det(np.array([P[b] - P[a], P[c] - P[a], P[d] - P[a]])))

def analyse(nom, pts, adj, N):
    # triangles et leurs apex
    meme_chi = meme_cote = n = 0; adj_meme = adj_opp = n_meme = n_opp = 0
    k4_par_sommet = np.zeros(N); pures = np.zeros(N)
    tri = set()
    for i in range(N):
        for j in adj[i]:
            if j <= i: continue
            cij = adj[i] & adj[j]
            if not cij: pures[i] += 1; pures[j] += 1
            for k in cij:
                if k > j: tri.add((i, j, k))
    k4 = set()
    for (i, j, k) in tri:
        apex = sorted(adj[i] & adj[j] & adj[k])
        for d in apex: k4.add(tuple(sorted((i, j, k, d))))
        if len(apex) < 2: continue
        nrm = np.cross(pts[j] - pts[i], pts[k] - pts[i])
        for d, e in itertools.combinations(apex, 2):
            sd = np.sign(np.dot(nrm, pts[d] - pts[i])); se = np.sign(np.dot(nrm, pts[e] - pts[i]))
            mc = sd == se; n += 1; meme_cote += mc
            meme_chi += chir(pts, (i, j, k, d)) == chir(pts, (i, j, k, e))
            lie = e in adj[d]
            if mc: n_meme += 1; adj_meme += lie
            else: n_opp += 1; adj_opp += lie
    for t in k4:
        for v in t: k4_par_sommet[v] += 1
    p = meme_cote / n
    print(f"A. {nom:<22} paires liées par une face : {n:>7} ; P(même côté) = {p:.3f} ; P(même chiralité) = {meme_chi/n:.4f} ; prédiction 0,4 + 0,2 p = {0.4+0.2*p:.4f} ; "
          f"apex reliés : {adj_meme/max(n_meme,1):.2f} (même côté) contre {adj_opp/max(n_opp,1):.2f} (côtés opposés)")
    deg = np.array([len(adj[i]) for i in range(N)]); q1, q2 = np.quantile(deg, [1/3, 2/3])
    vides = deg <= q1; noeuds = deg > q2
    rv = pures[vides].sum() / max(k4_par_sommet[vides].sum(), 1); rn = pures[noeuds].sum() / max(k4_par_sommet[noeuds].sum(), 1)
    print(f"B. {nom:<22} degré moyen vides {deg[vides].mean():.1f}, nœuds {deg[noeuds].mean():.1f} ; arêtes pures / tétraèdres : vides {rv:.3f}, nœuds {rn:.4f} ; contraste {rv/max(rn,1e-9):.0f}")
    # C. composantes du sous-graphe induit par les sommets de tétraèdres
    S = {v for t in k4 for v in t}; vu = set(); b1 = []
    for s in S:
        if s in vu: continue
        comp = [s]; vu.add(s); q = [s]
        while q:
            x = q.pop()
            for y in adj[x]:
                if y in S and y not in vu: vu.add(y); comp.append(y); q.append(y)
        cs = set(comp); E = sum(len(adj[x] & cs) for x in comp) // 2
        b1.append(E - len(comp) + 1)
    c = collections.Counter(b1)
    print(f"C. {nom:<22} tétraèdres {len(k4):>6} ; amas de matière {len(b1):>4} ; plus petit b1 = {min(b1)} ; b1 les plus fréquents : {c.most_common(3)}")

for seed in (1, 2):
    pts, adj0, pool, E0 = build_initial(1000, seed, 6.6)
    analyse(f"départ (graine {seed})", pts, adj0, 1000)
    analyse(f"Blob (graine {seed})", pts, run_mcmc_canonical(pts, adj0, pool, 1000, E0, seed), 1000)
