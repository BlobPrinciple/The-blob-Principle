#!/usr/bin/env python3
"""Le point de travail du moteur canonique est-il stationnaire ?
Prolonge la chaîne de build_blob (120 N pas, soit ~36 balayages) jusqu'à 20 fois plus
longtemps, même moteur, mêmes paramètres, et suit n_tri/N, CV(degrés), Gini(masse)."""
import importlib.util, json, math, pathlib, sys, time
import numpy as np
ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI.parent.parent / "corpus" / "03_scripts" / "SCRIPTS DIVERS BLOB" / "blob engine.py"
spec = importlib.util.spec_from_file_location("blob_engine", MOTEUR)
be = importlib.util.module_from_spec(spec); sys.modules["blob_engine"] = be; spec.loader.exec_module(be)

def etat(nbr, deg, N):
    m = be.measure(nbr, deg, N)
    return {k: round(float(m[k]), 4) for k in ("n_tri_par_N", "CV", "Gini_masse") if k in m}

def run(N, seed, blocs, fac):
    pts, nbr, deg = be.build_blob(N, seed=seed)           # = 120 N pas
    eu, ev = [], []
    for u in range(N):
        for k in range(deg[u]):
            v = int(nbr[u, k])
            if v > u: eu.append(u); ev.append(v)
    eu = np.array(eu, np.int64); ev = np.array(ev, np.int64)
    r = (be.KAPPA / ((N - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    from scipy.spatial import cKDTree
    pool = cKDTree(pts).query_pairs(be.POOL_FAC * r, output_type='ndarray').astype(np.int64)
    pa = pool[:, 0].copy(); pb = pool[:, 1].copy()
    mean = 2.0 * len(eu) / N; nt = be._n_tri(nbr, deg, N)
    traj = [dict(pas_sur_N=be.THERM_FAC, **etat(nbr, deg, N))]
    for b in range(1, blocs + 1):
        nt = be._mcmc(nbr, deg, eu, ev, pa, pb, be.BETA, be.TAU / N, mean, nt,
                      fac * N, be.CAP, 7_000_000 + seed * 1000 + b)
        traj.append(dict(pas_sur_N=be.THERM_FAC + b * fac, **etat(nbr, deg, N)))
    return traj

if __name__ == "__main__":
    out = {}
    for N in (500, 1000, 2000):
        out[N] = [run(N, s, 10, 240) for s in range(3)]     # jusqu'à 120 + 2400 = 2520 N pas
        for s, tr in enumerate(out[N]):
            print(N, s, [(t["pas_sur_N"], t["n_tri_par_N"], t["CV"], t.get("Gini_masse")) for t in tr[::2] + [tr[-1]]], flush=True)
    (ICI / "defi_m7_stationnarite.json").write_text(json.dumps(out, indent=1))
