# ======================================================================
#  BLOB — SCAN COLAB  (à coller dans Google Colab, cellules # %%)
#  A) FERMETURE r2/nT  (secteur topologique, front V212) — grand N
#  B) SORKIN Λ ~ 1/√N  — resserrage du préfacteur √F + robustesse aux seuils
#
#  Discipline : moteur CANONIQUE (|E| fixé, secteur connexe, τ_eff=τ/N,
#  κ=6.6, β=0.30, τ=0.50). §C.3 : on ne pose aucune cible ; on lit le verdict.
#  NOTE : le moteur ci-dessous est une référence numpy CORRECTE mais lente
#  à grand N. Pour N≳5000, remplace `canonical()` par TON blob_engine.py
#  (numba, vérifié bit-pour-bit) en gardant la même sortie (A:list[set], X).
# ======================================================================

# %% [CELL 1] — moteur canonique de référence + utilitaires
import numpy as np, time
from scipy.spatial import cKDTree

BETA, TAU = 0.30, 0.50

def canonical(N, seed, kappa=6.6, cand_factor=2.6, nsw_per_N=80):
    """RGG thermalisé, |E|=N*kappa/2 FIXE (échanges d'arêtes), τ_eff=τ/N.
       Retourne (A:list[set], X:np.ndarray[N,3], h:float)."""
    rng = np.random.default_rng(seed)
    X = rng.random((N, 3))
    r_cand = (kappa * cand_factor / (N * 4.18879))**(1/3.0)
    cand = cKDTree(X).query_pairs(r_cand, output_type='ndarray'); M = len(cand)
    E0 = min(int(round(N * kappa / 2.0)), M)
    sel = rng.choice(M, size=E0, replace=False)
    pres = np.zeros(M, bool); pres[sel] = True
    A = [set() for _ in range(N)]
    for k in sel:
        a, b = int(cand[k, 0]), int(cand[k, 1]); A[a].add(b); A[b].add(a)
    deg = np.array([len(s) for s in A], float)
    ntri = float(sum(len(A[i] & A[j]) for i in range(N) for j in A[i] if i < j))
    sumsq = float((deg**2).sum()); mean = 2.0 * E0 / N
    plist = list(sel); T = TAU / N
    for _ in range(nsw_per_N * N):
        ri = rng.integers(len(plist)); e = plist[ri]
        a, b = int(cand[e, 0]), int(cand[e, 1]); f = -1
        for _t in range(25):
            g = int(rng.integers(M))
            if not pres[g]:
                c, d = int(cand[g, 0]), int(cand[g, 1])
                if len({a, b, c, d}) == 4: f = g; break
        if f < 0: continue
        c, d = int(cand[f, 0]), int(cand[f, 1])
        dn = -len(A[a] & A[b]) + len(A[c] & A[d]); new_ntri = ntri + dn
        new_sumsq = sumsq + 2.0 * (deg[c] + deg[d] - deg[a] - deg[b]) + 4.0
        cv0 = np.sqrt(max(sumsq / N - mean*mean, 0)) / mean
        cv1 = np.sqrt(max(new_sumsq / N - mean*mean, 0)) / mean
        dS = np.log1p(new_ntri) - np.log1p(ntri) - BETA * (cv1 - cv0)
        if dS >= 0 or rng.random() < np.exp(min(dS / T, 30)):
            A[a].discard(b); A[b].discard(a); A[c].add(d); A[d].add(c)
            deg[a]-=1; deg[b]-=1; deg[c]+=1; deg[d]+=1
            ntri = new_ntri; sumsq = new_sumsq
            pres[e] = False; pres[f] = True; plist[ri] = f
    return A, X, (kappa / (N * 4.18879))**(1/3.0)

def edges_tris(A, N):
    edges = []; eidx = {}
    for i in range(N):
        for j in A[i]:
            if i < j: eidx[(i, j)] = len(edges); edges.append((i, j))
    tris = []
    for i in range(N):
        nb = sorted(x for x in A[i] if x > i)
        for a in range(len(nb)):
            j = nb[a]; Aj = A[j]
            for b in range(a+1, len(nb)):
                k = nb[b]
                if k in Aj: tris.append((i, j, k))
    return edges, eidx, tris

def k4_centroids(A, X, tris):
    """centroïdes des 4-cliques (matière)."""
    cents = []
    for (i, j, k) in tris:
        for l in (A[i] & A[j] & A[k]):
            if l > k:
                cents.append((X[i]+X[j]+X[k]+X[l]) / 4.0)
    return np.array(cents) if cents else np.zeros((0, 3))

print("Cellule 1 OK — moteur canonique + utilitaires chargés.")

# %% [CELL 2] — SECTION A : FERMETURE r2/nT (topologique, grand N)
# r2/nT = fraction de triangles homologiquement indépendants (rang GF(2) de d2 / nT).
# In-container (N≤1500) il s'est révélé κ-DÉPENDANT (~28% sur κ∈{4..12}) et corrélé
# à V_K4 (-0.60). Ici on CONFIRME à plus grand N : si la variation sur κ tient,
# le secteur topologique est CLOS négatif (4e secteur sans second invariant).
def gf2_rank_d2(tris, eidx):
    basis = {}
    for (i, j, k) in tris:
        x = (1 << eidx[(i, j)]) | (1 << eidx[(i, k)]) | (1 << eidx[(j, k)])
        while x:
            p = x.bit_length() - 1
            if p in basis: x ^= basis[p]
            else: basis[p] = x; break
    return len(basis)

def r2_over_nT(N, seed, kappa):
    A, X, h = canonical(N, seed, kappa)
    edges, eidx, tris = edges_tris(A, N)
    r2 = gf2_rank_d2(tris, eidx)
    return r2 / len(tris)

def section_A(N=2000, kappas=(4.0, 6.6, 9.0, 12.0), seeds=range(1, 4)):
    print("="*66); print(f"SECTION A — fermeture r2/nT @ N={N} (GF(2) lent : sois patient)"); print("="*66)
    means = []
    for k in kappas:
        vals = [r2_over_nT(N, s, k) for s in seeds]
        m, cv = np.mean(vals), np.std(vals)/np.mean(vals)*100
        means.append(m); print(f"  κ={k:>4} : r2/nT = {m:.4f}  (CV {cv:.1f}%)")
    spread = (max(means)-min(means))/np.mean(means)*100
    print(f"\n  variation sur κ : {spread:.1f}%  →  >5% = κ-paramètre (mort confirmée) ;"
          f"  <5% = surprise, rouvrir.")
    return means

# Lance (décommente) :  section_A(N=2000)

# %% [CELL 3] — SECTION B : SORKIN Λ ~ 1/√N  (le travail vivant)
# Λ ~ √F / √N, F = facteur de Fano SPATIAL (variance de nombre en fenêtres fixes).
# Objectifs : (1) F_substrat (sommets) ≈ 1 (Poisson) — le préfacteur √F ;
#             (2) σ²(N) ∝ N^p, p→1 (⇒ σ∝√N) ; (3) robustesse aux seuils (point faible V169).
def fano_windows(P, L):
    """P:[n,3] points dans [0,1]^3 ; L^3 fenêtres. Retourne F=Var/mean, mean."""
    if len(P) == 0: return np.nan, 0.0
    idx = np.clip((P * L).astype(int), 0, L-1)
    flat = idx[:, 0]*L*L + idx[:, 1]*L + idx[:, 2]
    counts = np.bincount(flat, minlength=L**3).astype(float)
    return counts.var() / counts.mean(), counts.mean()

def section_B(Ns=(1500, 3000, 6000), seeds=range(1, 5), L=6):
    print("="*66); print("SECTION B — Sorkin Λ : variance de nombre, préfacteur √F, scaling"); print("="*66)
    # (1) préfacteur √F sur le substrat (sommets) + F matière (K4), multi-N multi-graines
    print(f"\n  Fano SPATIAL (L={L} ⇒ {L**3} fenêtres) :")
    print(f"  {'N':>6} | {'F_sommets (√F)':>16} | {'F_K4 (matière)':>14}")
    rows = {}
    for N in Ns:
        Fv, FK = [], []
        for s in seeds:
            A, X, h = canonical(N, s)
            _, _, tris = edges_tris(A, N)
            cents = k4_centroids(A, X, tris)
            fv, _ = fano_windows(X, L); fk, _ = fano_windows(cents, L)
            Fv.append(fv); FK.append(fk)
        rows[N] = (np.mean(Fv), np.std(Fv), np.mean(FK), np.std(FK))
        print(f"  {N:>6} | {np.mean(Fv):.3f} (√F={np.sqrt(np.mean(Fv)):.3f}) | {np.mean(FK):.2f} ± {np.std(FK):.2f}")
    # (2) scaling σ²(N) ∝ N^p : variance du comptage dans UNE fenêtre fixe (1/L de la boîte)
    print(f"\n  Scaling σ²(N) du nombre de sommets dans une fenêtre fixe (fraction 1/{L**3}) :")
    Nl, Vl = [], []
    for N in Ns:
        cs = []
        for s in seeds:
            A, X, h = canonical(N, s)
            idx = np.clip((X * L).astype(int), 0, L-1)
            flat = idx[:, 0]*L*L + idx[:, 1]*L + idx[:, 2]
            cs.append(np.bincount(flat, minlength=L**3).astype(float))
        cs = np.vstack(cs); Nl.append(N); Vl.append(cs.var())
    p = np.polyfit(np.log(Nl), np.log(Vl), 1)[0]
    print(f"   exposant p = {p:.3f}   (p≈1 ⇒ σ∝√N, Poisson ; p<1 ⇒ hyperuniforme)")
    # (3) robustesse aux seuils : F_K4 selon la définition de la matière (point faible V169)
    print(f"\n  Robustesse aux seuils (N={Ns[-1]}, def. matière variée) :")
    N = Ns[-1]; A, X, h = canonical(N, 1); _, _, tris = edges_tris(A, N)
    cents_all = k4_centroids(A, X, tris)
    # def alternative : K4 dont les 6 arêtes sont "courtes" (sous la médiane) = plus stricte
    print(f"   def. 'tous K4'        : F = {fano_windows(cents_all, L)[0]:.2f}  (n={len(cents_all)})")
    if len(cents_all) > 50:
        # sous-échantillon dense (centroïdes dans le tiers le plus peuplé) = seuil + strict
        idx = np.clip((cents_all * L).astype(int), 0, L-1)
        flat = idx[:, 0]*L*L + idx[:, 1]*L + idx[:, 2]
        cnt = np.bincount(flat, minlength=L**3)
        thr = np.percentile(cnt[cnt > 0], 66)
        keep = np.array([cnt[f] >= thr for f in flat])
        print(f"   def. 'amas denses'    : F = {fano_windows(cents_all[keep], L)[0]:.2f}  (n={keep.sum()})")
    print("\n  LECTURE : √F_sommets stable multi-N ⇒ préfacteur de Λ durci ;")
    print("            p≈1 ⇒ substrat Poisson confirmé (⇒ Λ~1/√N, V200) ;")
    print("            F_K4 stable malgré le changement de def. ⇒ robustesse aux seuils (réponse à V169).")

# Lance (décommente) :  section_B(Ns=(1500, 3000, 6000))

print("Notebook prêt. Décommente section_A(...) puis section_B(...) selon le temps Colab.")
