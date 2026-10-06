#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blob Principle — Campagne grand-N : flot de la dimension de marche d_w (verrou B / c emergent)
================================================================================================

OBJET. Mesurer d_w (dimension de marche) sur le graphe emergent du Blob, a N croissant
(10^3 -> 10^5), pour trancher : d_w_global -> 2 dans la limite continue ?
  - d_w = 2  -> diffusion normale / propagation balistique -> un c constant peut emerger (Lorentz IR, Horava).
  - d_w > 2  -> sous-diffusion -> cone "mou", pas de c constant universel.

ANCRAGE REEL. Reduction dimensionnelle UV->2 quasi-universelle en gravite quantique
(Carlip arXiv:1904.04379 ; Calcagni) ; emergence de Lorentz dans l'IR via flot RG (Horava arXiv:0901.3775) ;
lecture de d_w (Savo et al., PRA 90, 023839, 2014 : d_w=2 normal, >2 sous-diffusif).
Contrainte du reel : |c_photon - c_grav|/c < 1e-15 (GW170817).

METHODE. Module source CONSIGNE blob_v137_source.py (BETA=0.30, TAU=0.50, kappa=6.6) embarque VERBATIM.
Mesure de d_w = methode walk_dimension.py consignee : marche aleatoire, <r^2(sigma)> ~ sigma^(2/d_w),
r = distance geodesique (BFS). Implementation optimisee (1 BFS / source). MCMC a 25*N pas
(burn_f=10, prod_f=15) valide fidele au 130*N consigne sur une machine.

RESULTATS DEJA OBTENUS sur une seule machine (a confirmer/infirmer ici) :
    N      d_w_global
    800    2.90
    1500   2.81
    2500   2.66
    4000   2.58
    6000   2.56
-> decroit vers 2 mais RALENTIT : plateau ~2.5 vs convergence lente vers 2 non distinguables sous N~1e4.
Cette campagne pousse a N >= 1e4 (idealement 1e5) pour trancher.

FALSIFIABLE. d_w_global -> 2 a grand N  => c emergent dans l'IR (coherent avec le reel).
             d_w_global plafonne nettement > 2.2 => cone mou en IR, pas de c constant universel
             (le Blob serait alors un espace a diffusion anormale, famille des multigraphes CDT
              de Giasemidis-Wheater-Zohren arXiv:1202.6322 ; pas un echec, une nature).

USAGE.
    python3 blob_dw_campagne_grandN.py                      # N par defaut : 1000..16000
    python3 blob_dw_campagne_grandN.py --Ns 1000 4000 16000 64000
    python3 blob_dw_campagne_grandN.py --seeds 1 2 3 --burn 50 --prod 80   # fidelite maximale (lent)
    python3 blob_dw_campagne_grandN.py --nwalk 600 --out resultats_dw.json

Auteur : Rudolphe Mirante (Blob Principle). Co-redaction Claude (Anthropic) comme corde de rappel.
"""

import argparse, json, time, os
import numpy as np
from collections import deque

# ================================================================================
# MODULE SOURCE CONSIGNE blob_v137_source.py (VERBATIM)
# ================================================================================

"""
================================================================================
BLOB PRINCIPLE V137 — CODE SOURCE INTÉGRAL ET AUTONOME
================================================================================
Ce fichier est exécutable tel quel (Python 3, numpy, scipy).
Il contient TOUT le nécessaire pour reproduire et falsifier les résultats
du document master V137 :
  - construction du graphe géométrique (RGG 3D)
  - dynamique de viabilité canonique (E fixé) et grand-canonique (E libre)
  - classification des trois phases (Λ, matière noire, baryon) — définition exacte
  - mesure des fractions cosmologiques
  - mesure de la dimension de Hausdorff

Dépendances : numpy, scipy. Aucune autre.
Reproductibilité : tous les tirages sont indexés par 'seed'.

USAGE :
  python blob_v137_source.py            # lance la démonstration (fractions Planck)
================================================================================
"""
import numpy as np
import math, time, json
from collections import deque
from scipy.spatial import KDTree

# ------------------------------------------------------------------ PARAMÈTRES
BETA  = 0.30      # coefficient de désordre (A4)
TAU   = 0.50      # température combinatoire (A5), effective = TAU/N
THETA = 0.50      # seuil de stabilité temporelle (A6) = (kappa0-2)/kappa0
# kappa = E/N attendu ; kappa=4 => E0=2N => degré moyen <d>=4
# (rappel convention : <d> = 2*E/N)

# --------------------------------------------------------- CONSTRUCTION GRAPHE
def rips_radius(N, kappa, mult=1.0):
    """Rayon de portée pour obtenir E0 = N*kappa/2 arêtes en moyenne (A3)."""
    return mult * (kappa / ((N - 1) * (4/3) * math.pi)) ** (1/3)

def E0_target(N, kappa):
    return max(N - 1, int(N * kappa / 2))

def lcc_size(adj, N):
    """Taille de la plus grande composante connexe."""
    seen = [False]*N; best = 0
    for s in range(N):
        if not seen[s]:
            sz = 0; q = deque([s]); seen[s] = True
            while q:
                v = q.popleft(); sz += 1
                for w in adj[v]:
                    if not seen[w]: seen[w] = True; q.append(w)
            best = max(best, sz)
    return best

def build_initial(N, seed, kappa, pool_mult=1.6):
    """Construit le RGG 3D initial avec E0 arêtes et un pool d'arêtes candidates."""
    r = rips_radius(N, kappa); r_p = pool_mult * r
    E0 = E0_target(N, kappa)
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0.0, 1.0, (N, 3))
    tree = KDTree(pts)
    adj = [set() for _ in range(N)]
    for i, j in tree.query_pairs(r):
        adj[i].add(j); adj[j].add(i)
    pool = list(tree.query_pairs(r_p))
    rng2 = np.random.default_rng(seed + 50_000)
    K = sum(len(adj[i]) for i in range(N)) // 2
    att = 0; max_att = 10 * abs(E0 - K) + 5000
    while K != E0 and att < max_att:
        att += 1
        if K < E0:
            if not pool: break
            u, v = pool[rng2.integers(len(pool))]
            if v not in adj[u]: adj[u].add(v); adj[v].add(u); K += 1
        else:
            edges = [(i, j) for i in range(N) for j in adj[i] if j > i]
            if not edges: break
            u, v = edges[rng2.integers(len(edges))]
            adj[u].discard(v); adj[v].discard(u)
            if lcc_size(adj, N) == N: K -= 1
            else: adj[u].add(v); adj[v].add(u)
    return pts, adj, pool, E0

# ----------------------------------------------------------- VIABILITÉ (A4)
def count_triangles(adj, N):
    n = 0
    for i in range(N):
        for j in adj[i]:
            if j > i:
                n += len(adj[i] & adj[j] & set(k for k in adj[j] if k > j))
    return n

def compute_S(adj, n_tri, N, gamma=0.0):
    """Fonctionnelle de viabilité S = log(1+n_tri) - beta*D - gamma*E/N (A4)."""
    degs = np.array([len(adj[i]) for i in range(N)], float)
    D = degs.std() / (degs.mean() + 1e-8)
    E = degs.sum() / 2.0
    return math.log(1 + n_tri) - BETA * D - gamma * E / N

def still_connected(adj, u, v, N):
    """Vérifie que retirer l'arête (u,v) ne déconnecte pas le graphe."""
    seen = {u}; q = deque([u])
    while q:
        node = q.popleft()
        for w in adj[node]:
            if w in seen: continue
            if (node == u and w == v) or (node == v and w == u): continue
            seen.add(w); q.append(w)
            if w == v: return True
    return False

def run_mcmc_canonical(pts, adj_init, pool, N, E0, seed, burn_f=50, prod_f=80):
    """Dynamique de viabilité à E fixé (échange d'arêtes). A5."""
    tau_eff = TAU / N
    rng = np.random.default_rng(seed + 200_000)
    adj = [set(a) for a in adj_init]
    edge_list = [(i, j) for i in range(N) for j in adj[i] if j > i]
    if not edge_list or not pool: return adj
    n_tri = count_triangles(adj, N)
    S_curr = compute_S(adj, n_tri, N)
    pool_arr = np.array(pool, dtype=np.int32); n_pool = len(pool_arr)
    for step in range((burn_f + prod_f) * N):
        if not edge_list: break
        io = int(rng.integers(len(edge_list))); u, v = edge_list[io]
        e_in = None
        for _ in range(30):
            ii = int(rng.integers(n_pool)); a, b = int(pool_arr[ii,0]), int(pool_arr[ii,1])
            if b not in adj[a]: e_in = (a, b); break
        if e_in is None: continue
        a, b = e_in
        if len(adj[u]) <= 2 or len(adj[v]) <= 2:
            if not still_connected(adj, u, v, N): continue
        tl = len(adj[u] & adj[v])
        adj[u].discard(v); adj[v].discard(u)
        adj[a].add(b); adj[b].add(a)
        tg = len(adj[a] & adj[b])
        nt = n_tri - tl + tg
        S_new = compute_S(adj, nt, N)
        if S_new - S_curr >= 0 or rng.random() < math.exp((S_new - S_curr) / tau_eff):
            n_tri = nt; S_curr = S_new; edge_list[io] = (a, b)
        else:
            adj[u].add(v); adj[v].add(u); adj[a].discard(b); adj[b].discard(a)
    return adj

def run_mcmc_grand_canonical(pts, adj_init, pool, N, seed, gamma, burn_f=40, prod_f=60):
    """Dynamique de viabilité à E LIBRE (ajout/suppression). Densité émergente. A5+III."""
    tau_eff = TAU / N
    rng = np.random.default_rng(seed + 300_000)
    adj = [set(a) for a in adj_init]
    pool_arr = np.array(pool, dtype=np.int32) if pool else np.empty((0,2),dtype=np.int32)
    n_pool = len(pool_arr); n_tri = count_triangles(adj, N)
    S_curr = compute_S(adj, n_tri, N, gamma)
    for step in range((burn_f + prod_f) * N):
        move = rng.integers(3)
        if move == 1 and n_pool > 0:           # AJOUT
            ii = int(rng.integers(n_pool)); a, b = int(pool_arr[ii,0]), int(pool_arr[ii,1])
            if b in adj[a]: continue
            tg = len(adj[a] & adj[b]); adj[a].add(b); adj[b].add(a)
            S_new = compute_S(adj, n_tri + tg, N, gamma)
            if S_new - S_curr >= 0 or rng.random() < math.exp((S_new - S_curr)/tau_eff):
                n_tri += tg; S_curr = S_new
            else: adj[a].discard(b); adj[b].discard(a)
        elif move == 2:                          # SUPPRESSION
            edges = [(i,j) for i in range(N) for j in adj[i] if j > i]
            if not edges: continue
            u, v = edges[int(rng.integers(len(edges)))]
            if len(adj[u]) <= 1 or len(adj[v]) <= 1: continue
            tl = len(adj[u] & adj[v]); adj[u].discard(v); adj[v].discard(u)
            S_new = compute_S(adj, n_tri - tl, N, gamma)
            if S_new - S_curr >= 0 or rng.random() < math.exp((S_new - S_curr)/tau_eff):
                n_tri -= tl; S_curr = S_new
            else: adj[u].add(v); adj[v].add(u)
    return adj

# ------------------------------------------------------- TOPOLOGIE DU LINK
def link_topology(adj, v):
    """Renvoie (n_K3, n_K4, chi) pour le sommet v. Théorème T1."""
    nb = list(adj[v]); d = len(nb)
    if d == 0: return 0, 0, 0
    link_adj = {w: set() for w in nb}
    nK3 = 0
    for i, a in enumerate(nb):
        for b in nb[i+1:]:
            if b in adj[a]:
                nK3 += 1; link_adj[a].add(b); link_adj[b].add(a)
    nK4 = 0
    for a in nb:
        la = list(link_adj[a])
        for i, x in enumerate(la):
            for y in la[i+1:]:
                if y in link_adj[x]: nK4 += 1
    nK4 //= 3
    return nK3, nK4, d - nK3 + nK4

def find_all_K4(adj, N):
    out = []
    for i in range(N):
        Ni = adj[i]
        for j in Ni:
            if j <= i: continue
            cij = Ni & adj[j]
            for k in cij:
                if k <= j: continue
                for l in (cij & adj[k]):
                    if l > k: out.append((i, j, k, l))
    return out

def neighbor_stability(adj0, adj1, N):
    """Stabilité f(v) = Jaccard des voisinages entre deux états (A6)."""
    f = np.zeros(N)
    for v in range(N):
        n0, n1 = adj0[v], adj1[v]
        u = n0 | n1
        f[v] = 1.0 if len(u) == 0 else len(n0 & n1) / len(u)
    return f

# --------------------------------------------------- CLASSIFICATION (Déf IV.1)
def classify_phases(adj_eq, adj_evolved, N, theta=THETA):
    """
    Définition EXACTE des trois phases (Partie IV.1) :
      - Λ        : n_K3 = 0  (aucun triangle)  + résidus de cœurs sous le seuil chi
      - DM       : dans un triangle, hors cœur baryonique stable
      - baryon   : dans un K4 stable (f>theta) ET chi(link) >= <chi> intrinsèque
    Renvoie (f_L, f_DM, f_b).
    """
    f_stable = neighbor_stability(adj_eq, adj_evolved, N)
    V_stable = {v for v in range(N) if f_stable[v] > theta}
    # sommets dans un triangle
    V_in_tri = set()
    for i in range(N):
        ni = adj_eq[i]
        for j in ni:
            if j <= i: continue
            common = ni & adj_eq[j]
            if common:
                V_in_tri.add(i); V_in_tri.add(j)
                V_in_tri.update(k for k in common if k > j)
    V_isolated = set(range(N)) - V_in_tri
    # sommets dans un K4
    V_in_K4 = set()
    for K in find_all_K4(adj_eq, N):
        for v in K: V_in_K4.add(v)
    V_K4_stable = V_in_K4 & V_stable
    if not V_K4_stable:
        return len(V_isolated)/N, (len(V_in_tri))/N, 0.0
    # seuil intrinsèque chi >= <chi>
    chi_pv = {v: link_topology(adj_eq, v)[2] for v in V_K4_stable}
    chi_mean = np.mean(list(chi_pv.values()))
    V_b = {v for v, c in chi_pv.items() if c >= chi_mean}
    V_K4_residual = V_K4_stable - V_b           # cœurs sous le seuil -> Λ
    V_DM = V_in_tri - V_K4_stable
    V_L = V_isolated | V_K4_residual
    return len(V_L)/N, len(V_DM)/N, len(V_b)/N

# ------------------------------------------------------ DIMENSION DE HAUSDORFF
def hausdorff_dim(adj, N, n_src=10):
    """Dimension de Hausdorff par croissance de boules géodésiques."""
    rng = np.random.default_rng(7)
    nodes = [v for v in range(N) if adj[v]]
    if len(nodes) < 15: return None
    slopes = []
    for _ in range(n_src):
        src = nodes[rng.integers(len(nodes))]
        dist = {src: 0}; q = deque([src])
        while q:
            v = q.popleft()
            for w in adj[v]:
                if w not in dist: dist[w] = dist[v]+1; q.append(w)
        rmax = max(dist.values())
        if rmax < 3: continue
        rs = np.arange(1, int(rmax*0.7)+1)
        cnt = np.array([sum(1 for dd in dist.values() if dd <= r) for r in rs], float)
        m = cnt >= 3
        if m.sum() < 3: continue
        s = np.polyfit(np.log(rs[m]), np.log(cnt[m]), 1)[0]
        slopes.append(s)
    return (float(np.mean(slopes)), float(np.std(slopes))) if slopes else None

# ------------------------------------------------------------------- DÉMO
def demo_fractions(N=1000, n_seeds=10, kappa=4.0):
    """Reproduit les fractions cosmologiques (Partie IV-V)."""
    PLANCK = {'L': 0.6847, 'DM': 0.2645, 'b': 0.0490}
    res = []
    for seed in range(n_seeds):
        pts, adj0, pool, E0 = build_initial(N, seed, kappa)
        if lcc_size(adj0, N) / N < 0.85: continue
        adj_eq = run_mcmc_canonical(pts, adj0, pool, N, E0, seed)
        adj_ev = run_mcmc_canonical(pts, adj_eq, pool, N, E0, seed + 10_000, burn_f=0, prod_f=30)
        fL, fDM, fb = classify_phases(adj_eq, adj_ev, N)
        res.append((fL, fDM, fb))
    a = np.array(res)
    mL, mDM, mb = a.mean(0)
    chi2 = ((mL-PLANCK['L'])/PLANCK['L'])**2 + ((mDM-PLANCK['DM'])/PLANCK['DM'])**2 + ((mb-PLANCK['b'])/PLANCK['b'])**2
    print(f"Blob ({len(res)} seeds, N={N}, <d>={kappa}):")
    print(f"  Omega_L  = {mL:.4f} +/- {a[:,0].std():.4f}  (Planck {PLANCK['L']}, ecart {(mL-PLANCK['L'])/PLANCK['L']*100:+.1f}%)")
    print(f"  Omega_DM = {mDM:.4f} +/- {a[:,1].std():.4f}  (Planck {PLANCK['DM']}, ecart {(mDM-PLANCK['DM'])/PLANCK['DM']*100:+.1f}%)")
    print(f"  Omega_b  = {mb:.4f} +/- {a[:,2].std():.4f}  (Planck {PLANCK['b']}, ecart {(mb-PLANCK['b'])/PLANCK['b']*100:+.1f}%)")
    print(f"  Somme = {mL+mDM+mb:.4f} | chi2 = {chi2:.4f}")

if __name__ == "__main__":
    demo_fractions()


# ==================================================================================
#  MESURE d_w — methode walk_dimension.py consignee (implementation optimisee)
# ==================================================================================

def largest_cc(adj, N):
    seen = set(); best = []
    for s in range(N):
        if s in seen:
            continue
        c = []; st = [s]
        while st:
            x = st.pop()
            if x in seen:
                continue
            seen.add(x); c.append(x); st.extend(adj[x] - seen)
        if len(c) > len(best):
            best = c
    return best


def bfs_dist(adj_l, src):
    dist = {src: 0}; q = deque([src])
    while q:
        u = q.popleft()
        for w in adj_l[u]:
            if w not in dist:
                dist[w] = dist[u] + 1; q.append(w)
    return dist


def walk_profile(adj, N, n_walk=400, seed=0, sig_max=128):
    """ <r^2(sigma)> ~ sigma^(2/d_w), r = distance geodesique (BFS). Renvoie d_w global,
    le flot local d_w(sigma), sigma* (fenetre balistique d_w<2.3) et le diametre. """
    cc = largest_cc(adj, N); ccs = set(cc)
    if len(cc) < 150:
        return None
    adj_l = {v: list(adj[v] & ccs) for v in cc}
    rng = np.random.default_rng(seed)
    sigmas = [s for s in [2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128] if s <= sig_max]
    smax = max(sigmas)
    starts = rng.choice(cc, min(n_walk, len(cc)), replace=False)
    r2 = {s: [] for s in sigmas}
    diam = max(bfs_dist(adj_l, cc[int(rng.integers(len(cc)))]).values())
    for src in starts:
        dsrc = bfs_dist(adj_l, src); cur = src
        for step in range(1, smax + 1):
            nb = adj_l[cur]
            if not nb:
                break
            cur = nb[rng.integers(len(nb))]
            if step in r2:
                d = dsrc.get(cur)
                if d is not None:
                    r2[step].append(d * d)
    sg = []; r2m = []
    for s in sigmas:
        if len(r2[s]) > 25:
            sg.append(s); r2m.append(np.mean(r2[s]))
    sg = np.array(sg, float); r2m = np.array(r2m, float)
    gl = 2.0 / np.polyfit(np.log(sg), np.log(r2m), 1)[0]
    prof = []; ss = 0
    for i in range(len(sg) - 2):
        sl = np.polyfit(np.log(sg[i:i + 3]), np.log(r2m[i:i + 3]), 1)[0]
        dw = 2.0 / sl if sl > 0 else 99.0
        prof.append((float(sg[i + 1]), float(dw)))
        if dw < 2.3:
            ss = sg[i + 1]
    return dict(sg=sg.tolist(), r2m=r2m.tolist(), d_w_global=float(gl),
                sigma_star=float(ss), diam=float(diam), profile=prof)



# ==================================================================================
#  MCMC CONSIGNE + CHECKPOINT INTRA-BOUCLE (copie verbatim de la boucle + sauvegarde
#  periodique de l'etat ; reprise fidele validee identique au moteur consigne).
#  -> protege le calcul LE PLUS LONG (le MCMC lui-meme) a tres grand N.
# ==================================================================================
import math as _math

def run_mcmc_canonical_ckpt(pts, adj_init, pool, N, E0, seed, burn_f=50, prod_f=80,
                            ckpt_path=None, ckpt_every_steps=200_000):
    tau_eff = TAU / N
    total = (burn_f + prod_f) * N
    pool_arr = np.array(pool, dtype=np.int32); n_pool = len(pool_arr)
    start = 0; ck = None
    if ckpt_path and os.path.exists(ckpt_path):
        try:
            with open(ckpt_path) as f: ck = json.load(f)
            if ck.get("seed") == seed and ck.get("N") == N and ck.get("total") == total:
                adj = [set(x) for x in ck["adj"]]
                edge_list = [tuple(e) for e in ck["edge_list"]]
                n_tri = ck["n_tri"]; S_curr = ck["S_curr"]; start = ck["step"]
                rng = np.random.default_rng(); rng.bit_generator.state = ck["rng_state"]
                print(f"    [ckpt] reprise MCMC au step {start}/{total}", flush=True)
            else:
                ck = None
        except Exception as e:
            print(f"    [ckpt] illisible ({e}) -> redemarrage MCMC", flush=True); ck = None
    if start == 0:
        rng = np.random.default_rng(seed + 200_000)
        adj = [set(a) for a in adj_init]
        edge_list = [(i, j) for i in range(N) for j in adj[i] if j > i]
        if not edge_list or not pool: return adj
        n_tri = count_triangles(adj, N)
        S_curr = compute_S(adj, n_tri, N)

    def _save(step):
        if not ckpt_path: return
        tmp = ckpt_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(dict(seed=seed, N=N, total=total, step=step, n_tri=int(n_tri),
                           S_curr=float(S_curr), adj=[sorted(a) for a in adj],
                           edge_list=[list(e) for e in edge_list],
                           rng_state=rng.bit_generator.state), f)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, ckpt_path)

    for step in range(start, total):
        if not edge_list: break
        io = int(rng.integers(len(edge_list))); u, v = edge_list[io]
        e_in = None
        for _ in range(30):
            ii = int(rng.integers(n_pool)); a, bb = int(pool_arr[ii, 0]), int(pool_arr[ii, 1])
            if bb not in adj[a]: e_in = (a, bb); break
        if e_in is None:
            if ckpt_path and (step + 1) % ckpt_every_steps == 0: _save(step + 1)
            continue
        a, bb = e_in
        if len(adj[u]) <= 2 or len(adj[v]) <= 2:
            if not still_connected(adj, u, v, N):
                if ckpt_path and (step + 1) % ckpt_every_steps == 0: _save(step + 1)
                continue
        tl = len(adj[u] & adj[v])
        adj[u].discard(v); adj[v].discard(u)
        adj[a].add(bb); adj[bb].add(a)
        tg = len(adj[a] & adj[bb])
        nt = n_tri - tl + tg
        S_new = compute_S(adj, nt, N)
        if S_new - S_curr >= 0 or rng.random() < _math.exp((S_new - S_curr) / tau_eff):
            n_tri = nt; S_curr = S_new; edge_list[io] = (a, bb)
        else:
            adj[u].add(v); adj[v].add(u); adj[a].discard(bb); adj[bb].discard(a)
        if ckpt_path and (step + 1) % ckpt_every_steps == 0: _save(step + 1)
    if ckpt_path and os.path.exists(ckpt_path): os.remove(ckpt_path)
    return adj


# ==================================================================================
#  ORCHESTRATION ROBUSTE — sauvegarde par palier (chaque graine) + reprise + securite
# ==================================================================================

def _atomic_write_json(path, obj):
    """Ecriture atomique : on ecrit dans un .tmp puis on remplace -> jamais de JSON corrompu."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _load_state(path, meta):
    """Reprise : si le JSON existe, on recharge les (N,seed) deja calcules pour les sauter."""
    if os.path.exists(path):
        try:
            with open(path) as f:
                st = json.load(f)
            done = {(r["N"], r["seed"]) for r in st.get("per_seed", [])}
            print(f"[reprise] fichier existant detecte : {len(done)} couples (N,seed) deja faits, ils seront sautes.",
                  flush=True)
            st["meta"] = meta
            return st
        except Exception as e:
            bak = path + ".corrupt"
            os.replace(path, bak)
            print(f"[reprise] JSON illisible ({e}) -> sauvegarde en {bak}, on repart de zero.", flush=True)
    return {"meta": meta, "per_seed": [], "per_N": []}


def _recompute_per_N(per_seed):
    """Agrege les resultats par graine en moyennes/ecarts-types par N."""
    by = {}
    for r in per_seed:
        by.setdefault(r["N"], []).append(r)
    out = []
    for N in sorted(by):
        g = np.array([r["d_w_global"] for r in by[N]])
        ss = np.array([r["sigma_star"] for r in by[N]])
        dm = np.array([r["diam"] for r in by[N]])
        out.append(dict(N=int(N), d_w_global=float(g.mean()), d_w_std=float(g.std()),
                        sigma_star=float(ss.mean()), diam=float(dm.mean()), n_seeds=len(by[N])))
    return out


def campaign(Ns, seeds, burn_f, prod_f, n_walk, out_path, meta):
    state = _load_state(out_path, meta)
    done = {(r["N"], r["seed"]) for r in state["per_seed"]}
    for N in Ns:
        for seed in seeds:
            if (N, seed) in done:
                print(f"  N={N} seed={seed} : deja fait, saute.", flush=True)
                continue
            t0 = time.time()
            try:
                pts, a0, pool, E0 = build_initial(N, seed, 6.6)
                _ckpt = (out_path + f'.mcmc_N{N}_s{seed}.ckpt') if out_path else None
                adj = run_mcmc_canonical_ckpt(pts, a0, pool, N, E0, seed, burn_f=burn_f, prod_f=prod_f,
                                              ckpt_path=_ckpt, ckpt_every_steps=200_000)
                adj = [set(x) for x in adj]
                res = walk_profile(adj, N, n_walk=n_walk, seed=seed)
                if res is None:
                    print(f"  N={N} seed={seed} : composante connexe trop petite, ignore.", flush=True)
                    continue
                rec = dict(N=int(N), seed=int(seed), d_w_global=res["d_w_global"],
                           sigma_star=res["sigma_star"], diam=res["diam"],
                           profile=res["profile"], t_sec=round(time.time() - t0, 1))
                state["per_seed"].append(rec)
                state["per_N"] = _recompute_per_N(state["per_seed"])
                # --- SAUVEGARDE PAR PALIER : a CHAQUE graine terminee ---
                _atomic_write_json(out_path, state)
                print(f"  N={N} seed={seed}: d_w_glob={res['d_w_global']:.3f} "
                      f"sigma*={res['sigma_star']:.0f} diam={res['diam']:.0f} "
                      f"[{rec['t_sec']:.0f}s] -> sauvegarde OK", flush=True)
            except KeyboardInterrupt:
                print("\n[interruption manuelle] etat sauvegarde, on s'arrete proprement.", flush=True)
                _atomic_write_json(out_path, state)
                raise
            except Exception as e:
                # --- SECURITE : une graine qui plante ne tue pas la campagne ---
                err = dict(N=int(N), seed=int(seed), error=repr(e), t_sec=round(time.time() - t0, 1))
                state.setdefault("errors", []).append(err)
                _atomic_write_json(out_path, state)
                print(f"  N={N} seed={seed} : ERREUR {e!r} -> consignee, on continue.", flush=True)
                continue
        # bilan partiel apres chaque N
        pn = [r for r in state["per_N"] if r["N"] == N]
        if pn:
            r = pn[0]
            print(f"N={N}: d_w_global={r['d_w_global']:.3f} +/- {r['d_w_std']:.3f}  "
                  f"sigma*/diam={r['sigma_star']/r['diam']:.3f}  (n={r['n_seeds']})\n", flush=True)
    return state


def run(Ns=(1000, 2000, 4000, 8000, 16000), seeds=(1, 2, 3),
        burn=10, prod=15, nwalk=400, out='resultats_dw.json'):
    """Appel direct depuis une cellule de notebook (sans argparse) :
        from blob_dw_campagne_grandN import run
        run(Ns=[1000,2000,4000,8000,16000], seeds=[1,2,3], out='resultats_dw.json')
    Reprend automatiquement le fichier 'out' s'il existe (sauvegarde apres chaque graine)."""
    meta = dict(BETA=BETA, TAU=TAU, kappa=6.6, Ns=list(Ns), seeds=list(seeds),
                burn_f=burn, prod_f=prod, n_walk=nwalk,
                methode="walk_dimension.py consignee ; <r^2(sigma)>~sigma^(2/d_w) ; r=geodesique BFS")
    print("Campagne d_w(N) — Blob | BETA=%.2f TAU=%.2f kappa=6.6 | MCMC %d*N pas | seeds=%s | out=%s"
          % (BETA, TAU, burn + prod, list(seeds), out), flush=True)
    state = campaign(list(Ns), tuple(seeds), burn, prod, nwalk, out, meta)
    rows = state["per_N"]
    print("\n=== BILAN ===\nN        d_w_global    +/-      sigma*/diam   n")
    for r in rows:
        print(f"{r['N']:>6}    {r['d_w_global']:.3f}    {r['d_w_std']:.3f}    "
              f"{r['sigma_star']/r['diam']:.3f}    {r['n_seeds']}")
    if len(rows) >= 4:
        import numpy as _np
        Ns_ = _np.array([r['N'] for r in rows], float); dw_ = _np.array([r['d_w_global'] for r in rows])
        dinf = _np.polyfit(1.0/_np.log(Ns_), dw_, 1)[1]
        print(f"\nExtrapolation d_w(N->inf) via 1/logN : d_inf ~ {dinf:.2f}")
        print("  d_inf ~ 2 -> c emergent IR ; d_inf > 2.2 -> cone mou (diffusion anormale).")
    return state


def main():
    ap = argparse.ArgumentParser(description="Campagne grand-N du flot de la dimension de marche d_w (Blob).")
    ap.add_argument('--Ns', type=int, nargs='+', default=[1000, 2000, 4000, 8000, 16000],
                    help="liste des tailles N")
    ap.add_argument('--seeds', type=int, nargs='+', default=[1, 2, 3], help="graines")
    ap.add_argument('--burn', type=int, default=10, help="burn_f (defaut 10 ; 50 = fidelite max consignee)")
    ap.add_argument('--prod', type=int, default=15, help="prod_f (defaut 15 ; 80 = fidelite max consignee)")
    ap.add_argument('--nwalk', type=int, default=400, help="nombre de marcheurs par graine")
    ap.add_argument('--out', type=str, default='resultats_dw.json', help="fichier JSON de sortie (= reprise)")
    args, _unknown = ap.parse_known_args()  # tolere les args injectes par Jupyter/Colab (-f kernel.json)

    meta = dict(BETA=BETA, TAU=TAU, kappa=6.6, Ns=args.Ns, seeds=args.seeds,
                burn_f=args.burn, prod_f=args.prod, n_walk=args.nwalk,
                methode="walk_dimension.py consignee ; <r^2(sigma)>~sigma^(2/d_w) ; r=geodesique BFS")

    print("Campagne d_w(N) — Blob Principle | BETA=%.2f TAU=%.2f kappa=6.6" % (BETA, TAU))
    print("MCMC : %d*N pas (burn_f=%d, prod_f=%d) | seeds=%s | nwalk=%d"
          % (args.burn + args.prod, args.burn, args.prod, args.seeds, args.nwalk))
    print("Sortie + reprise : %s  (sauvegarde apres CHAQUE graine ; relancer la meme commande reprend ou ca s'est arrete)"
          % args.out)
    print("=" * 80, flush=True)

    state = campaign(args.Ns, tuple(args.seeds), args.burn, args.prod, args.nwalk, args.out, meta)
    rows = state["per_N"]

    print("\n=== BILAN ===")
    print("N        d_w_global    +/-      sigma*/diam   n")
    for r in rows:
        print(f"{r['N']:>6}    {r['d_w_global']:.3f}    {r['d_w_std']:.3f}    "
              f"{r['sigma_star']/r['diam']:.3f}    {r['n_seeds']}")

    if len(rows) >= 4:
        Ns_ = np.array([r['N'] for r in rows], float)
        dw_ = np.array([r['d_w_global'] for r in rows])
        dinf_log = np.polyfit(1.0 / np.log(Ns_), dw_, 1)[1]   # extrapolation N->inf via 1/logN
        print(f"\nExtrapolation d_w(N->inf) via 1/logN : d_inf ~ {dinf_log:.2f}")
        print("  d_inf ~ 2     -> c constant emergent dans l'IR (Lorentz IR, coherent avec le reel).")
        print("  d_inf > 2.2   -> cone mou en IR, pas de c constant universel (diffusion anormale).")

    if state.get("errors"):
        print(f"\n[!] {len(state['errors'])} erreur(s) consignee(s) dans le JSON (champ 'errors').")
    print(f"\nResultats dans {args.out} (per_seed = detail par graine ; per_N = agregats).")


if __name__ == '__main__':
    main()
