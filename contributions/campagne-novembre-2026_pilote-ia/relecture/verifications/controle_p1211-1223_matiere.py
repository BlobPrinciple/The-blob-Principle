#!/usr/bin/env python3
"""Contrôle du pilote pour les pages 1211 à 1223 du master V346 (Parties CXXXIV à CXXXVII, 27 juin).
(1) Le secteur matière pose : quark = un tétraèdre à quatre faces libres ; amas ouverts (faces libres > 0, « massifs ») ;
    cavité fermée = cinq tétraèdres sur cinq sommets (bord du 4-simplexe), zéro face libre, « sans masse ».
    Question : dans le Blob simulé, quelle part des tétraèdres a quatre faces libres, combien de cliques à cinq sommets ?
    Moteurs de l'auteur : blob_colab_verrouillage.canonical (juin) et gap curl colab.py (30 mai).
(2) Groupes de symétrie des simplexes : ordre du plus grand quotient abélien et présence d'un sous-groupe normal propre
    autre que le groupe alterné, pour les simplexes à 3, 4, 5, 6 sommets (calcul direct sur les permutations).
(3) Niveau de bruit d'une moyenne de 729 phases Z3 tirées au hasard (T16 : |<P>| = 0,027 sur 729 boucles).
Usage : controle_p1211-1223_matiere.py "<blob colab verrouillage.py>" "<gap curl colab.py>"
"""
import sys, itertools
import numpy as np

def charge(chemin, marque):
    src = open(chemin, encoding='utf-8').read(); e = {}
    exec(compile(src[:src.index(marque)], 'moteur_de_l_auteur', 'exec'), e); return e

def bilan(nom, A, N):
    A = [set(A[v]) for v in range(N)]
    tris = [(i, j, k) for i in range(N) for j in A[i] if j > i for k in (A[i] & A[j]) if k > j]
    k4 = [(i, j, k, l) for (i, j, k) in tris for l in (A[i] & A[j] & A[k]) if l > k]
    mult = {}
    for q in k4:
        for f in itertools.combinations(q, 3):
            mult[f] = mult.get(f, 0) + 1
    libres = np.array([sum(1 for f in itertools.combinations(q, 3) if mult[f] == 1) for q in k4])
    k5 = sum(len([m for m in (A[i] & A[j] & A[k] & A[l]) if m > l]) for (i, j, k, l) in k4)
    dans_k5 = np.mean([1 if (A[i] & A[j] & A[k] & A[l]) else 0 for (i, j, k, l) in k4]) if k4 else float('nan')
    hist = [int(np.sum(libres == n)) for n in range(5)]
    print(f"{nom:<28} triangles {len(tris)}, tétraèdres {len(k4)}, cliques à 5 sommets {k5} ; tétraèdres selon leurs faces libres "
          f"(0,1,2,3,4) : {hist} ; part à 4 faces libres {hist[4]/max(len(k4),1):.1%} ; part contenue dans une clique à 5 : {dans_k5:.1%}")

print("(1) Tétraèdres du Blob simulé")
e = charge(sys.argv[1], '# ============================== SECTION A')
for seed in (1, 2):
    A, X, h = e['canonical'](1500, seed)
    bilan(f"moteur de juin, graine {seed}", A, 1500)
e = charge(sys.argv[2], '# --------------------- GAP CURL DE HODGE')
for seed in (1, 2):
    pts, adj0, pool, E0 = e['build_initial'](800, seed, 6.6)
    bilan(f"moteur du 30 mai, départ, g. {seed}", adj0, 800)
    bilan(f"moteur du 30 mai, Blob, g. {seed}", e['run_mcmc_canonical'](pts, adj0, pool, 800, E0, seed), 800)

print("(2) Groupe de symétrie du simplexe à n sommets (groupe symétrique S_n) : sous-groupes normaux")
def compose(p, q): return tuple(p[i] for i in q)
def inverse(p):
    r = [0] * len(p)
    for i, v in enumerate(p): r[v] = i
    return tuple(r)
def type_cyclique(p):
    vu, t = set(), []
    for i in range(len(p)):
        if i not in vu:
            n, j = 0, i
            while j not in vu:
                vu.add(j); j = p[j]; n += 1
            t.append(n)
    return tuple(sorted(t, reverse=True))
def engendre(gens, n):
    ident = tuple(range(n)); H = {ident}; front = [ident]
    while front:
        suivant = []
        for h in front:
            for g in gens:
                x = compose(h, g)
                if x not in H:
                    H.add(x); suivant.append(x)
        front = suivant
    return H
for n in (3, 4, 5, 6):
    G = list(itertools.permutations(range(n)))
    classes = {}
    for g in G:
        classes.setdefault(type_cyclique(g), []).append(g)      # dans S_n, une classe de conjugaison = un type cyclique
    ordres = sorted({len(engendre(c, n)) for t, c in classes.items() if t != tuple([1] * n)})
    print(f"  n = {n} (simplexe de dimension {n-1}) : ordre {len(G)} ; ordres des sous-groupes normaux engendrés par une classe de conjugaison : {ordres}")

print("(3) Module de la moyenne de 729 phases Z3 aléatoires")
rng = np.random.default_rng(0)
m = [abs(np.mean(np.exp(2j * np.pi * rng.integers(0, 3, 729) / 3))) for _ in range(2000)]
print(f"  moyenne {np.mean(m):.3f} ; intervalle à 90 % [{np.quantile(m, 0.05):.3f} ; {np.quantile(m, 0.95):.3f}] ; avec 80 phases : "
      f"{np.mean([abs(np.mean(np.exp(2j*np.pi*rng.integers(0,3,80)/3))) for _ in range(2000)]):.3f}")
