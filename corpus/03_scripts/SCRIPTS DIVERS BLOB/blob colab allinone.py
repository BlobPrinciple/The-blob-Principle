# ============================================================================
#  BLOB — SCAN COLAB TOUT-EN-UN  (colle TOUT, exécute : ça se lance seul)
#  A) FERMETURE r2/nT (secteur topologique, front V212) — grand N
#  B) SORKIN Λ ~ 1/√N — préfacteur √F + scaling σ²∝N^p + robustesse aux seuils
#  Écrit des JSON à chaque section (auditables). §C.3 : aucune cible posée.
#
#  Moteur CANONIQUE de référence (numpy) : |E|=N·κ/2 FIXE, secteur connexe,
#  τ_eff=τ/N, κ=6.6, β=0.30, τ=0.50. Lent à grand N → pour N≳4000, remplace
#  le CORPS de canonical() par ton blob_engine.py numba (même sortie A,X,h).
# ============================================================================
import numpy as np, time, json, os
from scipy.spatial import cKDTree

# ----------------------------- CONFIG -----------------------------
# Défauts Colab raisonnables (numpy). Monte si tu branches ton moteur numba.
A_N        = 1200                       # taille pour la fermeture r2/nT
A_KAPPAS   = (4.0, 6.6, 9.0, 12.0)      # balayage κ (≥3 pts obligatoire, V221)
A_SEEDS    = range(1, 4)                # 3 graines
B_NS       = (800, 1500, 2500)          # tailles pour Sorkin Λ
B_SEEDS    = range(1, 4)                # 3 graines
B_L        = 6                          # L^3 fenêtres pour le Fano spatial
OUTDIR     = os.getcwd()                # /content sur Colab
# ------------------------------------------------------------------

BETA, TAU = 0.30, 0.50

def canonical(N, seed, kappa=6.6, cand_factor=2.6, nsw_per_N=80):
    """RGG thermalisé, |E|=N·κ/2 FIXE (échanges d'arêtes), τ_eff=τ/N.
       Retourne (A:list[set], X:[N,3], h:float)."""
    rng = np.random.default_rng(seed); X = rng.random((N, 3))
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
        cv0 = np.sqrt(max(sumsq/N - mean*mean, 0)) / mean
        cv1 = np.sqrt(max(new_sumsq/N - mean*mean, 0)) / mean
        dS = np.log1p(new_ntri) - np.log1p(ntri) - BETA * (cv1 - cv0)
        if dS >= 0 or rng.random() < np.exp(min(dS/T, 30)):
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

def gf2_rank_d2(tris, eidx):
    basis = {}
    for (i, j, k) in tris:
        x = (1 << eidx[(i, j)]) | (1 << eidx[(i, k)]) | (1 << eidx[(j, k)])
        while x:
            p = x.bit_length() - 1
            if p in basis: x ^= basis[p]
            else: basis[p] = x; break
    return len(basis)

def num_components(A, N):
    par = list(range(N))
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i in range(N):
        for j in A[i]:
            if i < j:
                ri, rj = find(i), find(j)
                if ri != rj: par[ri] = rj
    return len({find(x) for x in range(N)})

def k4_centroids(A, X, tris):
    cents = []
    for (i, j, k) in tris:
        for l in (A[i] & A[j] & A[k]):
            if l > k: cents.append((X[i]+X[j]+X[k]+X[l]) / 4.0)
    return np.array(cents) if cents else np.zeros((0, 3))

def fano(P, L):
    if len(P) == 0: return float('nan')
    idx = np.clip((P * L).astype(int), 0, L-1)
    flat = idx[:, 0]*L*L + idx[:, 1]*L + idx[:, 2]
    c = np.bincount(flat, minlength=L**3).astype(float)
    return float(c.var() / c.mean())

# ============================== SECTION A ==============================
def section_A():
    print("="*64); print(f"SECTION A — fermeture r2/nT @ N={A_N} (GF(2), patience)"); print("="*64)
    out = {"N": A_N, "kappas": list(A_KAPPAS), "seeds": list(A_SEEDS),
           "per_seed": {}, "mean": {}, "cv_pct": {}}
    for k in A_KAPPAS:
        vals = []
        for s in A_SEEDS:
            A, X, h = canonical(A_N, s, k)
            edges, eidx, tris = edges_tris(A, A_N)
            vals.append(gf2_rank_d2(tris, eidx) / len(tris))
        vals = np.array(vals)
        out["per_seed"][str(k)] = vals.tolist()
        out["mean"][str(k)] = float(vals.mean())
        out["cv_pct"][str(k)] = float(vals.std()/vals.mean()*100)
        print(f"  κ={k:>4} : r2/nT = {vals.mean():.4f}  (CV {vals.std()/vals.mean()*100:.1f}%)")
    ms = [out["mean"][str(k)] for k in A_KAPPAS]
    out["spread_pct_over_kappa"] = float((max(ms)-min(ms))/np.mean(ms)*100)
    print(f"\n  variation sur κ : {out['spread_pct_over_kappa']:.1f}%  "
          f"(>5% = κ-paramètre, secteur topologique CLOS négatif ; <5% = rouvrir)")
    p = os.path.join(OUTDIR, "blob_sectionA_r2nT.json")
    json.dump(out, open(p, "w"), indent=2); print(f"  JSON → {p}")
    return out

# ============================== SECTION B ==============================
def section_B():
    print("="*64); print("SECTION B — Sorkin Λ : √F, scaling σ²∝N^p, robustesse seuils"); print("="*64)
    data = {N: {"fano_v": [], "fano_K4": [], "winvar_cells": []} for N in B_NS}
    thr_record = {}
    for N in B_NS:
        for s in B_SEEDS:
            A, X, h = canonical(N, s)               # UNE thermalisation, réutilisée
            edges, eidx, tris = edges_tris(A, N)
            cents = k4_centroids(A, X, tris)
            data[N]["fano_v"].append(fano(X, B_L))
            data[N]["fano_K4"].append(fano(cents, B_L))
            idx = np.clip((X * B_L).astype(int), 0, B_L-1)
            flat = idx[:, 0]*B_L*B_L + idx[:, 1]*B_L + idx[:, 2]
            data[N]["winvar_cells"].append(
                np.bincount(flat, minlength=B_L**3).astype(float).tolist())
            if N == B_NS[-1] and s == list(B_SEEDS)[0]:   # robustesse aux seuils
                f_all = fano(cents, B_L); n_all = len(cents)
                ic = np.clip((cents * B_L).astype(int), 0, B_L-1)
                fc = ic[:, 0]*B_L*B_L + ic[:, 1]*B_L + ic[:, 2]
                cnt = np.bincount(fc, minlength=B_L**3)
                thr = np.percentile(cnt[cnt > 0], 66) if (cnt > 0).any() else 0
                keep = np.array([cnt[f] >= thr for f in fc]) if n_all else np.array([])
                f_dense = fano(cents[keep], B_L) if keep.any() else float('nan')
                thr_record = {"def_tous_K4": {"F": f_all, "n": int(n_all)},
                              "def_amas_denses": {"F": f_dense, "n": int(keep.sum()) if n_all else 0}}
    out = {"Ns": list(B_NS), "seeds": list(B_SEEDS), "L": B_L,
           "fano_vertices": {}, "fano_K4": {}, "sqrtF_vertices": {}, "threshold": thr_record}
    print(f"\n  Fano spatial (L={B_L} ⇒ {B_L**3} fenêtres) :")
    print(f"  {'N':>6} | {'F_sommets (√F)':>18} | {'F_K4':>12}")
    Nl, Vl = [], []
    for N in B_NS:
        fv = np.array(data[N]["fano_v"]); fk = np.array(data[N]["fano_K4"])
        out["fano_vertices"][str(N)] = fv.tolist(); out["fano_K4"][str(N)] = fk.tolist()
        out["sqrtF_vertices"][str(N)] = float(np.sqrt(fv.mean()))
        print(f"  {N:>6} | {fv.mean():.3f} (√F={np.sqrt(fv.mean()):.3f}) | {fk.mean():.2f} ± {fk.std():.2f}")
        Nl.append(N); Vl.append(np.vstack(data[N]["winvar_cells"]).var())
    p_exp = float(np.polyfit(np.log(Nl), np.log(Vl), 1)[0])
    out["scaling_p"] = p_exp
    print(f"\n  scaling σ²(N) ∝ N^p : p = {p_exp:.3f}  (p≈1 ⇒ Poisson ⇒ Λ~1/√N ; p<1 ⇒ hyperuniforme)")
    if thr_record:
        print(f"\n  robustesse aux seuils (N={B_NS[-1]}) :")
        print(f"   tous K4     : F={thr_record['def_tous_K4']['F']:.2f} (n={thr_record['def_tous_K4']['n']})")
        print(f"   amas denses : F={thr_record['def_amas_denses']['F']:.2f} (n={thr_record['def_amas_denses']['n']})")
        print("   (F stable entre les deux ⇒ √F robuste aux seuils, réponse au point faible V169)")
    p = os.path.join(OUTDIR, "blob_sectionB_sorkin.json")
    json.dump(out, open(p, "w"), indent=2); print(f"\n  JSON → {p}")
    return out

# ============================== MAIN (se lance seul) ==============================
if __name__ == "__main__":
    t0 = time.time()
    rA = section_A()
    rB = section_B()
    print(f"\n[terminé en {time.time()-t0:.0f}s] — 2 JSON écrits dans {OUTDIR}")
    try:
        from google.colab import files
        files.download(os.path.join(OUTDIR, "blob_sectionA_r2nT.json"))
        files.download(os.path.join(OUTDIR, "blob_sectionB_sorkin.json"))
    except Exception:
        pass
