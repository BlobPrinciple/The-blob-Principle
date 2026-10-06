# ============================================================================
#  BLOB — NOTEBOOK VERROUILLAGE  (colle TOUT, exécute : se lance seul)
#  Tests-de-mort / clôtures des items MESURABLES vivants. Écrit 3 JSON.
#  §C.3 : aucune valeur posée pour atteindre une cible ; on teste vers l'avant.
#
#  A) CLÔTURE r2/nT (secteur topologique)     [EXACT — GF(2)]
#  B) SORKIN √F : substrat Poisson + durcissement de seuil
#         · substrat (sommets)                [EXACT — confirme V200]
#         · durcissement calcification         [PROXY défendable de V170]
#  C) PARITÉ P + ⟨χ⟩ (asymétrie chirale)      [EXACT — déf. corpus l.386]
#
#  Moteur CANONIQUE numpy (|E| fixe, secteur connexe, τ_eff=τ/N). Lent à grand
#  N → pour N≳4000, remplace le CORPS de canonical() par ton blob_engine.py
#  numba (même sortie A, X, h) et monte les CONFIG.
# ============================================================================
import numpy as np, time, json, os
from scipy.spatial import cKDTree

# ----------------------------- CONFIG -----------------------------
KAPPAS   = (4.0, 6.6, 9.0, 12.0)     # balayage κ commun (≥3 pts, V221)
A_N      = 1000                      # clôture r2/nT
A_SEEDS  = range(1, 4)
B_NS     = (800, 1500, 2500)         # Sorkin substrat + scaling
B_SEEDS  = range(1, 4)
B_L      = 6                         # L^3 fenêtres
B_QS     = (40, 50, 60, 70, 80)      # quantiles de durcissement (V170)
C_N      = 1200                      # parité
C_SEEDS  = range(1, 4)
OUTDIR   = os.getcwd()
# ------------------------------------------------------------------

BETA, TAU = 0.30, 0.50

def canonical(N, seed, kappa=6.6, cand_factor=2.6, nsw_per_N=80):
    """RGG thermalisé, |E|=N·κ/2 FIXE (échanges d'arêtes). Retourne (A, X, h)."""
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

def fano(P, L):
    if len(P) == 0: return float('nan')
    idx = np.clip((P * L).astype(int), 0, L-1)
    flat = idx[:, 0]*L*L + idx[:, 1]*L + idx[:, 2]
    c = np.bincount(flat, minlength=L**3).astype(float)
    return float(c.var() / c.mean())

def enum_k4(A, X, tris):
    """Retourne (centroïdes [n,3], chiralités χ∈{-1,+1}, scores calcification)."""
    tri_deg = np.zeros(len(X), float)              # calcification ~ tri par sommet
    for (i, j, k) in tris:
        tri_deg[i] += 1; tri_deg[j] += 1; tri_deg[k] += 1
    cents, chis, calc = [], [], []
    for (i, j, k) in tris:
        for l in (A[i] & A[j] & A[k]):
            if l > k:                              # K4 = {i,j,k,l} dédupliqué
                v = np.linalg.det(np.array([X[j]-X[i], X[k]-X[i], X[l]-X[i]]))
                cents.append((X[i]+X[j]+X[k]+X[l]) / 4.0)
                chis.append(1.0 if v > 0 else -1.0)
                calc.append(tri_deg[i] + tri_deg[j] + tri_deg[k] + tri_deg[l])
    return (np.array(cents) if cents else np.zeros((0, 3)),
            np.array(chis), np.array(calc))

def parity_face(A, X, tris):
    """P = fraction de K4 face-adjacents (3 sommets communs) de MÊME chiralité.
       Méthode exacte : pour chaque triangle, les apex donnent des K4 partageant
       cette face ; on compte les paires de même signe de volume orienté."""
    same = tot = 0; chi_sum = 0.0; chi_n = 0
    for (i, j, k) in tris:
        apex = [l for l in (A[i] & A[j] & A[k])]
        if len(apex) < 1: continue
        signs = []
        for l in apex:
            v = np.linalg.det(np.array([X[j]-X[i], X[k]-X[i], X[l]-X[i]]))
            s = 1 if v > 0 else -1; signs.append(s)
            if l > k:                       # représentant CANONIQUE du K4 → χ global compté 1×
                chi_sum += s; chi_n += 1
        for a in range(len(signs)):
            for b in range(a+1, len(signs)):
                tot += 1
                if signs[a] == signs[b]: same += 1
    P = same / tot if tot else float('nan')
    chi = chi_sum / chi_n if chi_n else float('nan')
    return P, tot, chi

# ============================== SECTION A ==============================
def section_A():
    print("="*66); print(f"A — CLÔTURE r2/nT @ N={A_N}  [EXACT, GF(2)]"); print("="*66)
    out = {"statut": "EXACT", "N": A_N, "kappas": list(KAPPAS), "per_seed": {}, "mean": {}, "cv_pct": {}}
    for k in KAPPAS:
        vals = []
        for s in A_SEEDS:
            A, X, h = canonical(A_N, s, k)
            edges, eidx, tris = edges_tris(A, A_N)
            vals.append(gf2_rank_d2(tris, eidx) / len(tris))
        vals = np.array(vals)
        out["per_seed"][str(k)] = vals.tolist(); out["mean"][str(k)] = float(vals.mean())
        out["cv_pct"][str(k)] = float(vals.std()/vals.mean()*100)
        print(f"  κ={k:>4} : r2/nT = {vals.mean():.4f}  (CV {vals.std()/vals.mean()*100:.1f}%)")
    ms = [out["mean"][str(k)] for k in KAPPAS]
    out["spread_pct_over_kappa"] = float((max(ms)-min(ms))/np.mean(ms)*100)
    print(f"  → variation sur κ : {out['spread_pct_over_kappa']:.1f}%  "
          f"(>5% ⇒ κ-paramètre, secteur CLOS négatif)")
    json.dump(out, open(os.path.join(OUTDIR, "verrou_A_r2nT.json"), "w"), indent=2)
    print("  JSON → verrou_A_r2nT.json")
    return out

# ============================== SECTION B ==============================
def section_B():
    print("="*66); print("B — SORKIN √F : substrat [EXACT] + durcissement [PROXY V170]"); print("="*66)
    fv = {N: [] for N in B_NS}; cells = {N: [] for N in B_NS}
    harden = {q: [] for q in B_QS}
    for N in B_NS:
        for s in B_SEEDS:
            A, X, h = canonical(N, s)
            edges, eidx, tris = edges_tris(A, N)
            cents, chis, calc = enum_k4(A, X, tris)
            fv[N].append(fano(X, B_L))
            idx = np.clip((X * B_L).astype(int), 0, B_L-1)
            flat = idx[:, 0]*B_L*B_L + idx[:, 1]*B_L + idx[:, 2]
            cells[N].append(np.bincount(flat, minlength=B_L**3).astype(float).tolist())
            if N == B_NS[-1] and len(calc):       # durcissement au plus grand N
                for q in B_QS:
                    thr = np.percentile(calc, q)
                    keep = calc >= thr
                    harden[q].append(fano(cents[keep], B_L) if keep.sum() else float('nan'))
    out = {"statut_substrat": "EXACT", "statut_durcissement": "PROXY_calcification_de_V170",
           "Ns": list(B_NS), "L": B_L, "sqrtF_vertices": {}, "fano_K4_par_quantile": {}}
    print("  Substrat (sommets) — doit être Poisson (√F≈1) :")
    Nl, Vl = [], []
    for N in B_NS:
        a = np.array(fv[N]); out["sqrtF_vertices"][str(N)] = float(np.sqrt(a.mean()))
        print(f"    N={N:>6} : √F = {np.sqrt(a.mean()):.3f}")
        Nl.append(N); Vl.append(np.vstack(cells[N]).var())
    out["scaling_p"] = float(np.polyfit(np.log(Nl), np.log(Vl), 1)[0])
    print(f"    scaling σ²∝N^p : p = {out['scaling_p']:.3f}  (p≈1 ⇒ Λ~1/√N)")
    print(f"\n  Durcissement calcification (N={B_NS[-1]}) — PROXY V170, Fano doit ↓ vers ~1 :")
    for q in B_QS:
        a = np.array(harden[q]); out["fano_K4_par_quantile"][f"q{q}"] = float(np.nanmean(a))
        print(f"    q{q} : Fano K4 = {np.nanmean(a):.1f}")
    print("    (si Fano chute vers ~1 en durcissant ⇒ corrobore V170 ; sinon ⇒ proxy ≠ viabilité exacte)")
    json.dump(out, open(os.path.join(OUTDIR, "verrou_B_sorkin.json"), "w"), indent=2)
    print("  JSON → verrou_B_sorkin.json")
    return out

# ============================== SECTION C ==============================
def section_C():
    print("="*66); print(f"C — PARITÉ P + ⟨χ⟩ @ N={C_N}  [EXACT, déf. corpus l.386]"); print("="*66)
    out = {"statut": "EXACT", "N": C_N, "kappas": list(KAPPAS),
           "P_mean": {}, "P_sigma": {}, "chi_global_mean": {}, "n_pairs_mean": {}}
    for k in KAPPAS:
        Ps, chis, npairs = [], [], []
        for s in C_SEEDS:
            A, X, h = canonical(C_N, s, k)
            edges, eidx, tris = edges_tris(A, C_N)
            P, tot, chi = parity_face(A, X, tris)
            Ps.append(P); chis.append(chi); npairs.append(tot)
        Ps = np.array(Ps); npm = float(np.mean(npairs))
        sigma = (np.mean(Ps) - 0.5) / (0.5/np.sqrt(npm)) if npm > 0 else float('nan')
        out["P_mean"][str(k)] = float(np.mean(Ps)); out["P_sigma"][str(k)] = float(sigma)
        out["chi_global_mean"][str(k)] = float(np.mean(chis)); out["n_pairs_mean"][str(k)] = npm
        print(f"  κ={k:>4} : P = {np.mean(Ps):.4f}  ({sigma:+.1f}σ vs 0,5)   ⟨χ⟩ = {np.mean(chis):+.4f}")
    print("  → corpus : P≈0,516 (22,6σ à κ=6,6, N grand), ⟨χ⟩≈0 (no-go asymétrie nette)")
    print("    P>0,5 stable ⇒ corrèle la chiralité [M] confirmé ; ⟨χ⟩≈0 ⇒ pas d'excès net")
    json.dump(out, open(os.path.join(OUTDIR, "verrou_C_parite.json"), "w"), indent=2)
    print("  JSON → verrou_C_parite.json")
    return out

# ============================== MAIN (se lance seul) ==============================
if __name__ == "__main__":
    t0 = time.time()
    rA = section_A(); rB = section_B(); rC = section_C()
    print(f"\n[terminé en {time.time()-t0:.0f}s] — 3 JSON écrits dans {OUTDIR}")
    print("RAPPEL corde de rappel : ceci verrouille le MESURABLE (confirme ou réfute).")
    print("Le mur des valeurs, les générations, g*, la gravité [T] (analytique) ne sont")
    print("PAS verrouillables par simulation — ce sont des frontières prouvées/ouvertes.")
    try:
        from google.colab import files
        for f in ("verrou_A_r2nT.json", "verrou_B_sorkin.json", "verrou_C_parite.json"):
            files.download(os.path.join(OUTDIR, f))
    except Exception:
        pass
