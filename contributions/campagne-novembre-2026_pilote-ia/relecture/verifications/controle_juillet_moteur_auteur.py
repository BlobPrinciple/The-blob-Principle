#!/usr/bin/env python3
"""Contrôle indépendant de quatre mesures des 3, 4 et 5 juillet 2026 (master propre du 7 juillet, lignes 2524-2529,
3265-3278, 3381-3389, 3922-3960), absentes du PDF V346. Le moteur est celui de l'auteur, lu dans le dépôt et exécuté
tel quel : « blob suite AUTONOME colab.py », bloc moteur (build_initial, run_mcmc_canonical, find_all_K4, ...),
kappa = 6,6, beta = 0,30, tau = 0,50, réservoir de rayon 1,6 r, 130 N pas.

A. Matière et vide : les tétraèdres (K4) se concentrent-ils dans les cellules denses ?  (master : « les cellules denses,
   top 10 %, concentrent 94 % des K4 ; le fond clairsemé, 45 % du volume, en contient 0 % ; corrélation +0,87 »)
B. Trois étages : part des sommets dans un K4 / dans un triangle seulement / sur des arêtes seulement
   (master : environ 0,25 ; 0,44 ; 0,31)
C. Nombre de K4 du Blob rapporté à celui du graphe géométrique nu (master : 16 610 contre 1 901 à N = 1000, soit 9 fois)
D. Calcification : taux d'acceptation du retrait d'une arête selon le nombre de triangles qu'elle porte
   (master : 1,00 / 0,92 / 0,79 / 0,63 / 0,20 ; arêtes de K4 0,44 contre 0,92, rapport 2,10),
   et, ajout du pilote, variation moyenne de S (en unités de tau/N) sur les échanges acceptés, par classe de charge
   de l'arête retirée : un échange retire une arête et en pose une autre ; la variation est celle de l'échange entier.

Fidélité : la boucle instrumentée (D) est une copie ligne à ligne de run_mcmc_canonical ; on vérifie qu'avec la même
graine elle rend exactement le même graphe final que la fonction de l'auteur.
Usage : python3 -I controle_juillet_moteur_auteur.py "<chemin de blob suite AUTONOME colab.py>" [N graines...]
"""
import sys, math, itertools, time
from collections import Counter
import numpy as np

src = open(sys.argv[1], encoding='utf-8').read()
debut = src.index('# ------------------------------------------------------------------ PARAMÈTRES')
fin = src.index('class _B: pass')
M = {}
exec(compile("from scipy.spatial import KDTree\nimport numpy as np\nimport math, time, json\nfrom collections import deque\n"
             + src[debut:fin], 'moteur_de_l_auteur', 'exec'), M)
KAPPA = 6.6

def triangles(adj, N):
    out = []
    for i in range(N):
        for j in adj[i]:
            if j > i:
                for k in adj[i] & adj[j]:
                    if k > j: out.append((i, j, k))
    return out

def boucle_instrumentee(pts, adj_init, pool, N, E0, seed, burn_f=50, prod_f=80):
    """Copie de run_mcmc_canonical ; les relevés ne consomment aucun tirage."""
    TAU = M['TAU']; compute_S = M['compute_S']; still_connected = M['still_connected']; count_triangles = M['count_triangles']
    tau_eff = TAU / N
    rng = np.random.default_rng(seed + 200_000)
    adj = [set(a) for a in adj_init]
    edge_list = [(i, j) for i in range(N) for j in adj[i] if j > i]
    n_tri = count_triangles(adj, N)
    S_curr = compute_S(adj, n_tri, N)
    pool_arr = np.array(pool, dtype=np.int32); n_pool = len(pool_arr)
    prop = Counter(); acc = Counter(); cout = Counter(); propK = Counter(); accK = Counter()
    for step in range((burn_f + prod_f) * N):
        io = int(rng.integers(len(edge_list))); u, v = edge_list[io]
        e_in = None
        for _ in range(30):
            ii = int(rng.integers(n_pool)); a, b = int(pool_arr[ii, 0]), int(pool_arr[ii, 1])
            if b not in adj[a]: e_in = (a, b); break
        if e_in is None: continue
        a, b = e_in
        if len(adj[u]) <= 2 or len(adj[v]) <= 2:
            if not still_connected(adj, u, v, N): continue
        commun = adj[u] & adj[v]
        tl = len(commun)
        mesure = step >= burn_f * N
        if mesure:
            classe = tl if tl <= 2 else (3 if tl <= 4 else 5)
            dansK4 = any((y in adj[x]) for x, y in itertools.combinations(commun, 2))
            prop[classe] += 1; propK[dansK4] += 1
        adj[u].discard(v); adj[v].discard(u)
        adj[a].add(b); adj[b].add(a)
        tg = len(adj[a] & adj[b])
        nt = n_tri - tl + tg
        S_new = compute_S(adj, nt, N)
        if S_new - S_curr >= 0 or rng.random() < math.exp((S_new - S_curr) / tau_eff):
            if mesure:
                acc[classe] += 1; accK[dansK4] += 1; cout[classe] += (S_new - S_curr) / tau_eff
            n_tri = nt; S_curr = S_new; edge_list[io] = (a, b)
        else:
            adj[u].add(v); adj[v].add(u); adj[a].discard(b); adj[b].discard(a)
    return adj, prop, acc, cout, propK, accK

def concentration(adj, pts, N, g):
    """Cellules d'une grille g^3 rangées par degré moyen ; parts des K4 et des triangles (centre de gravité)."""
    cell = np.minimum((pts * g).astype(int), g - 1)
    idc = cell[:, 0] * g * g + cell[:, 1] * g + cell[:, 2]
    deg = np.array([len(a) for a in adj], float)
    npts = np.bincount(idc, minlength=g ** 3).astype(float)
    dmoy = np.bincount(idc, weights=deg, minlength=g ** 3) / np.maximum(npts, 1)
    k4 = M['find_all_K4'](adj, N); tri = triangles(adj, N)
    def par_cellule(simplexes):
        if not simplexes: return np.zeros(g ** 3)
        c = pts[np.array(simplexes)].mean(axis=1)
        cc = np.minimum((c * g).astype(int), g - 1)
        return np.bincount(cc[:, 0] * g * g + cc[:, 1] * g + cc[:, 2], minlength=g ** 3).astype(float)
    k4c, tric = par_cellule(k4), par_cellule(tri)
    ordre = np.argsort(-dmoy); n10 = max(1, int(round(0.10 * g ** 3)))
    haut = ordre[:n10]; bas = ordre[-int(round(0.45 * g ** 3)):]
    r = lambda x, sel: (x[sel].sum() / x.sum()) if x.sum() > 0 else float('nan')
    corr = np.corrcoef(dmoy, k4c)[0, 1] if k4c.std() > 0 else float('nan')
    cv = dmoy.std() / dmoy.mean()
    return dict(nK4=len(k4), ntri=len(tri), part_K4_haut=r(k4c, haut), part_tri_haut=r(tric, haut), part_K4_bas=r(k4c, bas),
                cellules_sans_K4=float((k4c == 0).mean()), corr=corr, cv_cellules=cv, k4=k4, tri=tri)

def etages(adj, N, k4, tri):
    dansK4 = set(v for q in k4 for v in q); dansT = set(v for t in tri for v in t)
    return len(dansK4) / N, len(dansT - dansK4) / N, (N - len(dansT | dansK4)) / N

def ligne(nom, c):
    print(f"   {nom:<34} K4 = {c['nK4']:>6} ; triangles = {c['ntri']:>6} ; top 10 % des cellules : {c['part_K4_haut']:.0%} des K4, "
          f"{c['part_tri_haut']:.0%} des triangles ; 45 % les moins denses : {c['part_K4_bas']:.1%} des K4 ; "
          f"cellules sans K4 : {c['cellules_sans_K4']:.0%} ; corrélation densité-K4 : {c['corr']:+.2f} ; dispersion des cellules : {c['cv_cellules']:.2f}")

def une_graine(N, seed):
    t0 = time.time()
    pts, adj0, pool, E0 = M['build_initial'](N, seed, KAPPA)
    g = max(3, int(round((N / 9.0) ** (1 / 3))))
    # témoins : graphe géométrique nu ; état de départ ; E0 arêtes tirées au hasard dans le réservoir
    from scipy.spatial import KDTree
    nu = [set() for _ in range(N)]
    for i, j in KDTree(pts).query_pairs(M['rips_radius'](N, KAPPA)): nu[i].add(j); nu[j].add(i)
    rng = np.random.default_rng(seed + 777)
    hasard = [set() for _ in range(N)]
    for k in rng.choice(len(pool), size=E0, replace=False):
        i, j = pool[int(k)]; hasard[i].add(j); hasard[j].add(i)
    blob = M['run_mcmc_canonical'](pts, adj0, pool, N, E0, seed)
    blob2, prop, acc, cout, propK, accK = boucle_instrumentee(pts, adj0, pool, N, E0, seed)
    identique = all(blob[i] == blob2[i] for i in range(N))
    print(f"N = {N}, graine {seed} : E0 = {E0} arêtes, réservoir {len(pool)} paires (degré de réservoir {2*len(pool)/N:.1f}), grille {g}^3 = {g**3} cellules ; "
          f"boucle instrumentée identique à celle de l'auteur : {identique} ; {time.time()-t0:.0f} s")
    res = {}
    for nom, a in (("graphe géométrique nu", nu), ("départ (aucun pas)", adj0), ("E0 arêtes au hasard du réservoir", hasard), ("Blob (130 N pas)", blob)):
        c = concentration(a, pts, N, g); ligne(nom, c); res[nom] = c
    cb = res["Blob (130 N pas)"]
    e = etages(blob, N, cb['k4'], cb['tri'])
    print(f"   B. étages du Blob : dans un K4 {e[0]:.2f} ; triangle seulement {e[1]:.2f} ; arêtes seulement {e[2]:.2f}"
          f"      (graphe nu : {'/'.join(f'{x:.2f}' for x in etages(nu, N, res['graphe géométrique nu']['k4'], res['graphe géométrique nu']['tri']))})")
    print(f"   C. K4 du Blob / K4 du graphe nu = {cb['nK4']} / {res['graphe géométrique nu']['nK4']} = {cb['nK4']/max(1,res['graphe géométrique nu']['nK4']):.1f}")
    print("   D. retrait d'une arête, par nombre de triangles portés (propositions, taux d'acceptation, variation moyenne de S des échanges acceptés en unités de tau/N) :")
    for cl, nom in ((0, '0'), (1, '1'), (2, '2'), (3, '3-4'), (5, '5+')):
        if prop[cl]:
            print(f"        charge {nom:<3} : {prop[cl]:>6} propositions ; taux {acc[cl]/prop[cl]:.4f} ; variation moyenne de S {cout[cl]/max(1,acc[cl]):+.3f}")
    if propK[True] and propK[False]:
        tK, tH = accK[True] / propK[True], accK[False] / propK[False]
        print(f"        arêtes dans un K4 : taux {tK:.4f} ({propK[True]} propositions) ; hors K4 : taux {tH:.4f} ({propK[False]}) ; rapport hors/dans = {tH/tK:.2f}")
    return e, cb, res

if __name__ == "__main__":
    plan = [(1000, (1, 2)), (2000, (1,))]
    if len(sys.argv) > 2:
        plan = [(int(sys.argv[2]), tuple(int(x) for x in sys.argv[3:]) or (1,))]
    for N, graines in plan:
        for s in graines:
            une_graine(N, s)
