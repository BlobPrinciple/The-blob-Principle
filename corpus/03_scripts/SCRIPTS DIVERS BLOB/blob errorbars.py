"""
================================================================================
 BLOB — BARRES D'ERREUR sur d_w a grand N  (multi-graines)
================================================================================
 Le balayage single-seed a atteint le plancher de bruit : la baisse de d_w par
 decade (~0.05-0.10) est devenue comparable a la dispersion graine-a-graine, donc
 on ne peut plus distinguer "recouvrement lent vers 2" de "plateau a ~2.5".
 Ce script mesure d_w avec un ECART-TYPE en relancant plusieurs GRAINES par N,
 a une echelle relative fixe (0.15*diam), pour trancher.

 Lecture :
   - si d_w(N) DECROIT de plus de ~2*sigma entre deux tailles -> trend reel
     (recouvrement si ca continue vers 2, anomalie si ca se fige a ~2.5) ;
   - si les d_w(N) se chevauchent dans leurs barres d'erreur -> bruit, il faut
     plus de graines ou un N bien plus grand.

 Reutilise le moteur deja valide (blob_dimensions_grandN.py doit etre dans le
 meme dossier).

 Usage Colab :
   !pip -q install numba
   %run blob_errorbars.py

 Cout : ~ (temps d'un run a ce N) * N_SEEDS * len(N_LIST). Commencer petit.
================================================================================
"""
import time, json
import numpy as np
import blob_dimensions_grandN as B   # moteur valide (build, mcmc, mesures)

# =============================== CONFIG =======================================
N_LIST    = [250_000]   # tailles a tester (commencer par 250k, le moins cher)
N_SEEDS   = 8           # graines par taille (>=6 pour un ecart-type fiable)
REL_SCALE = 0.15        # echelle relative ou lire d_w (le creux diffusif)
# Astuce : pour 500k mettre N_SEEDS=4-5 ; 1M est tres cher (eviter le multi-seed).
# ==============================================================================


def one_seed_dw(N, seed):
    """Un graphe thermalise (graine donnee) -> d_w, d_f, d_s a 0.15*diam."""
    tau_eff = B.TAU / N
    edges, pool, r = B.build_geometric(N, B.KAPPA, B.POOL_FAC, seed)
    nbr, deg = B.build_nbr_arrays(edges, N, B.CAP)
    eu = edges[:, 0].copy(); ev = edges[:, 1].copy()
    pa = np.ascontiguousarray(pool[:, 0]); pb = np.ascontiguousarray(pool[:, 1])
    mean = 2.0 * len(edges) / N
    nt = B.n_triangles(nbr, deg, N)
    total = B.THERM_FAC * N
    chunk = max(1, total // B.N_CHUNKS)
    for c in range(B.N_CHUNKS):
        nt = B.mcmc_chunk(nbr, deg, eu, ev, pa, pb,
                          B.BETA, tau_eff, mean, nt, chunk, B.CAP, seed * 1000 + 1 + c)
    mask, gc = B.giant_component_mask(nbr, deg, N)
    gcn = np.where(mask)[0]
    rng = np.random.default_rng(seed * 7 + 99)
    diam = 0
    for s in rng.choice(gcn, min(5, gc), replace=False):
        diam = max(diam, int(B.bfs_dist(nbr, deg, s, N)[mask].max()))
    T = int(min(B.T_CAP, max(200, 3.0 * diam * diam)))
    maxr = min(diam, 60)
    # d_w, d_s a 0.15*diam
    starts = rng.choice(gcn, min(B.N_START, gc), replace=False)
    tt, P, MSD = B.measure_walk(nbr, deg, N, starts, T)
    dw = 2.0 / B.running_slope(tt, MSD)
    ds = -2.0 * B.running_slope(tt, P)
    rt = np.sqrt(np.maximum(MSD, 1e-12))
    rstar = REL_SCALE * diam
    i = int(np.nanargmin(np.abs(rt - rstar)))
    dwx, dsx = float(dw[i]), float(ds[i])
    # d_f a la meme echelle
    src = rng.choice(gcn, min(B.N_SRC_DF, gc), replace=False)
    Vr = B.measure_df(nbr, deg, N, src, maxr)
    dfr = np.concatenate([[np.nan], B.running_slope(np.arange(1, maxr + 1), Vr[1:])])
    ri = int(round(rstar))
    dfx = float(dfr[ri]) if ri < len(dfr) and np.isfinite(dfr[ri]) else np.nan
    return dwx, dfx, dsx, diam


def main():
    print(f"==== BARRES D'ERREUR d_w ====  N_LIST={N_LIST}  graines={N_SEEDS}  "
          f"echelle=0.15*diam\n", flush=True)
    allres = {}
    for N in N_LIST:
        dws, dfs, dss = [], [], []
        t0 = time.time()
        for s in range(N_SEEDS):
            ts = time.time()
            dw, df, ds, diam = one_seed_dw(N, s)
            dws.append(dw); dfs.append(df); dss.append(ds)
            print(f"  N={N:,} graine {s+1}/{N_SEEDS} : d_w={dw:.3f}  d_f={df:.2f}  "
                  f"d_s={ds:.2f}  (diam={diam}, {time.time()-ts:.0f}s)", flush=True)
        v = np.array(dws)
        mu, sg = float(v.mean()), float(v.std(ddof=1)) if len(v) > 1 else 0.0
        sem = sg / np.sqrt(len(v)) if len(v) > 1 else 0.0
        print(f"\n  >>> N={N:,} : d_w = {mu:.3f} +/- {sg:.3f} (ecart-type)  "
              f"[+/- {sem:.3f} sur la moyenne, n={len(v)}]")
        print(f"      d_f = {np.nanmean(dfs):.2f}   d_s = {np.nanmean(dss):.2f}   "
              f"[{time.time()-t0:.0f}s total]\n", flush=True)
        allres[N] = dict(d_w_seeds=dws, d_f_seeds=dfs, d_s_seeds=dss,
                         d_w_mean=mu, d_w_std=sg, d_w_sem=sem,
                         d_f_mean=float(np.nanmean(dfs)), d_s_mean=float(np.nanmean(dss)))
        json.dump(allres, open("blob_errorbars.json", "w"), indent=2)

    # ---- comparaison si plusieurs N ----
    if len(allres) >= 2:
        print("================ COMPARAISON ================")
        Ns = sorted(allres)
        for k in range(len(Ns) - 1):
            a, b = allres[Ns[k]], allres[Ns[k + 1]]
            d = a["d_w_mean"] - b["d_w_mean"]
            s = np.sqrt(a["d_w_sem"] ** 2 + b["d_w_sem"] ** 2)
            sig = d / s if s > 0 else float('inf')
            verdict = ("BAISSE significative" if sig > 2 else
                       "compatible avec un PLATEAU (pas de baisse a 2sigma)")
            print(f"  {Ns[k]:,} -> {Ns[k+1]:,} : d_w {a['d_w_mean']:.3f} -> "
                  f"{b['d_w_mean']:.3f}  (Delta={d:+.3f}, {sig:.1f}sigma) : {verdict}")
        print("\n  BAISSE significative qui continue -> RECOUVREMENT (d_w->2).")
        print("  PLATEAU dans les barres d'erreur      -> ANOMALIE douce reelle (d_w->~2.5).")
    else:
        print("Mettre au moins 2 tailles dans N_LIST pour comparer (ex: [250000, 500000]).")


if __name__ == "__main__":
    main()
