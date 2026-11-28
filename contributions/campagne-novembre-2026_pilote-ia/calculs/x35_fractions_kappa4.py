#!/usr/bin/env python3
"""X-35. Les fractions de phase à kappa0 = 4 (« voie cosmologique »), réécrites à partir de la définition du corpus.

Définition suivie : blob_v137_source.py de l'auteur (empreinte 42f31911...9df5), fonctions build_initial,
run_mcmc_canonical, neighbor_stability, link_topology, classify_phases. Ce programme ne l'importe pas : il en
réécrit la spécification avec le moteur à mise à jour incrémentale de X-34, pour pouvoir monter en taille.
Écarts connus avec le programme de l'auteur (aucun ne change la loi visée) :
  - tirage de l'arête absente : uniforme dans la liste des arêtes absentes de la réserve (l'auteur tire dans la
    réserve entière et rejette, 30 essais au plus) ;
  - garde de connexité : recherche en largeur depuis les deux bouts (même réponse, coût moindre) ;
  - suites de nombres aléatoires différentes : les trajectoires diffèrent, seules les statistiques se comparent.

Usage : x35_fractions_kappa4.py N kappa graine bras [beta] [tau]
        bras = blob (dynamique de viabilité) | temoin (mêmes échanges, tous acceptés, même nombre de pas)
Sortie : une ligne JSON.
"""
import sys, math, json
import numpy as np
from scipy.spatial import cKDTree
from x34_replication_blob_canonique import Graphe, cliques4

BURN, EVOL = 130, 30          # (50 + 80) N pas pour l'équilibre, 30 N pas pour l'état « évolué » (blob_v137_source.py)

def composante_max(adj, N):
    vu = np.zeros(N, bool); best = 0
    for s in range(N):
        if vu[s]: continue
        pile = [s]; vu[s] = True; t = 0
        while pile:
            x = pile.pop(); t += 1
            for y in adj[x]:
                if not vu[y]: vu[y] = True; pile.append(y)
        best = max(best, t)
    return best

def relies_sans(adj, u, v):
    """u et v restent-ils reliés si l'on ignore l'arête (u, v) ? Recherche depuis les deux bouts."""
    A = {u}; B = {v}; fa = [u]; fb = [v]
    while fa and fb:
        if len(fa) <= len(fb):
            nf = []
            for x in fa:
                for y in adj[x]:
                    if (x == u and y == v): continue
                    if y in B: return True
                    if y not in A: A.add(y); nf.append(y)
            fa = nf
        else:
            nf = []
            for x in fb:
                for y in adj[x]:
                    if (x == v and y == u): continue
                    if y in A: return True
                    if y not in B: B.add(y); nf.append(y)
            fb = nf
    return False

def construire(N, kappa, graine):
    r = (kappa / ((N - 1) * (4 / 3) * math.pi)) ** (1 / 3)
    E0 = max(N - 1, int(N * kappa / 2))
    pts = np.random.default_rng(graine).uniform(0.0, 1.0, (N, 3))
    arbre = cKDTree(pts)
    pool = [tuple(sorted(map(int, p))) for p in arbre.query_pairs(1.6 * r, output_type='ndarray')]
    init = [tuple(sorted(map(int, p))) for p in arbre.query_pairs(r, output_type='ndarray')]
    g = Graphe(N, pool, np.random.default_rng(graine + 50_000))
    for e in g.pool: g.absent[e] = len(g.labs); g.labs.append(e)
    for e in init: g.ajouter(e)
    essais = 0
    while len(g.liste) < E0 and g.labs:
        g.ajouter(g.labs[int(g.rng.integers(len(g.labs)))])
    while len(g.liste) > E0 and essais < 10 * E0:      # règle de l'auteur : on ne retire que si le graphe reste d'un seul tenant
        essais += 1
        e = g.liste[int(g.rng.integers(len(g.liste)))]
        g.retirer(e)
        if composante_max(g.adj, N) != N: g.ajouter(e)
    return g, E0, len(pool), len(init)

def pas(g, n_pas, beta, facteur, rng, tout_accepter):
    acc = 0; gardes = 0
    for _ in range(n_pas):
        e = g.liste[int(rng.integers(len(g.liste)))]
        f = g.labs[int(rng.integers(len(g.labs)))]
        u, v = e
        if len(g.adj[u]) <= 2 or len(g.adj[v]) <= 2:
            gardes += 1
            if not relies_sans(g.adj, u, v): continue
        S0 = g.S(beta)
        g.retirer(e); g.ajouter(f)
        if tout_accepter: acc += 1; continue
        dS = g.S(beta) - S0
        if dS >= 0 or rng.random() < math.exp(dS * facteur): acc += 1
        else: g.retirer(f); g.ajouter(e)
    return acc / n_pas, gardes / n_pas

def chi_du_lien(adj, v):
    nb = list(adj[v]); d = len(nb)
    la = {w: set() for w in nb}; n3 = 0
    for i, a in enumerate(nb):
        for b in nb[i + 1:]:
            if b in adj[a]: n3 += 1; la[a].add(b); la[b].add(a)
    n4 = 0
    for a in nb:
        l = list(la[a])
        for i, x in enumerate(l):
            for y in l[i + 1:]:
                if y in la[x]: n4 += 1
    return d - n3 + n4 // 3

def classer(adj_eq, adj_ev, N, K4, thetas):
    stab = np.array([1.0 if not (adj_eq[v] | adj_ev[v]) else len(adj_eq[v] & adj_ev[v]) / len(adj_eq[v] | adj_ev[v]) for v in range(N)])
    dans_tri = np.zeros(N, bool)
    for i in range(N):
        ni = adj_eq[i]
        for j in ni:
            if j > i and (ni & adj_eq[j]):
                dans_tri[i] = True; dans_tri[j] = True
                for k in ni & adj_eq[j]: dans_tri[k] = True
    dans_k4 = np.zeros(N, bool)
    for q in K4: dans_k4[list(q)] = True
    chi = {int(v): chi_du_lien(adj_eq, int(v)) for v in np.flatnonzero(dans_k4)}
    out = {'f_sans_triangle': float((~dans_tri).mean()), 'f_triangle_hors_k4': float((dans_tri & ~dans_k4).mean()),
           'f_k4': float(dans_k4.mean()), 'stabilite_moyenne': float(stab.mean()),
           'stabilite_moyenne_k4': float(stab[dans_k4].mean()) if dans_k4.any() else None, 'par_theta': {}}
    for th in thetas:
        ks = [v for v in chi if stab[v] > th]
        d = {'f_k4_stable': len(ks) / N}
        if ks:
            c = np.array([chi[v] for v in ks], float)
            nb_moy = int((c >= c.mean()).sum()); nb_med = int((c >= np.median(c)).sum())
            res = len(ks) - nb_moy
            fL = (int((~dans_tri).sum()) + res) / N; fDM = (int(dans_tri.sum()) - len(ks)) / N; fb = nb_moy / N
            d.update({'f_L': fL, 'f_DM': fDM, 'f_b': fb, 'p_chi': nb_moy / len(ks), 'chi_moyen': float(c.mean()),
                      # conventions de rechange, pour mesurer ce que chaque choix du classeur déplace
                      'alt_residu_en_DM': [int((~dans_tri).sum()) / N, (int(dans_tri.sum()) - nb_moy) / N, fb],
                      'alt_mediane': [(int((~dans_tri).sum()) + len(ks) - nb_med) / N, fDM, nb_med / N]})
        else:
            d.update({'f_L': float((~dans_tri).mean()), 'f_DM': float(dans_tri.mean()), 'f_b': 0.0})
        out['par_theta'][str(th)] = d
    return out

def lancer(N, kappa, graine, bras, beta=0.30, tau=0.50):
    g, E0, npool, ninit = construire(N, kappa, graine)
    lcc0 = composante_max(g.adj, N) / N
    out = {'N': N, 'kappa': kappa, 'graine': graine, 'bras': bras, 'beta': beta, 'tau': tau, 'E0': E0, 'aretes': len(g.liste),
           'degre_reserve': 2 * npool / N, 'aretes_rayon': ninit, 'lcc_initiale': lcc0}
    if lcc0 < 0.85: out['ecartee'] = True; return out
    libre = (bras == 'temoin')
    acc, gardes = pas(g, BURN * N, beta, N / tau, np.random.default_rng(graine + 200_000), libre)
    adj_eq = [set(a) for a in g.adj]
    K4 = cliques4(g)
    out.update({'acceptation': acc, 'part_gardes': gardes, 'tri_par_N': g.ntri / N, 'k4_par_N': len(K4) / N, 'cv_degres': g.cv(),
                'lcc_equilibre': composante_max(adj_eq, N) / N})
    pas(g, EVOL * N, beta, N / tau, np.random.default_rng(graine + 210_000), libre)
    out.update(classer(adj_eq, g.adj, N, K4, [0.338, 0.40, 0.45, 0.50, 0.55, 0.60]))
    return out

if __name__ == '__main__':
    N, kappa, graine, bras = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    beta = float(sys.argv[5]) if len(sys.argv) > 5 else 0.30
    tau = float(sys.argv[6]) if len(sys.argv) > 6 else 0.50
    print(json.dumps(lancer(N, kappa, graine, bras, beta, tau), ensure_ascii=False))
