#!/usr/bin/env python3
"""DEFI-M7 — coût du pont croissance -> Gibbs sur le moteur canonique (Rips 3D).

Contribution du pilote IA du laboratoire (Claude, Anthropic), 15 octobre 2026.

Question : après la naissance d'un sommet (mitose + arêtes de fermeture), combien
d'échanges de Metropolis par arête faut-il pour que le nouveau-né devienne
indiscernable d'un sommet typique ? Ce coût reste-t-il borné quand N grandit ?

Moteur : corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py, importé tel quel
(paramètres canoniques gelés : kappa = 6.6, beta = 0.30, tau = 0.50, pool_fac = 1.6,
tau_eff = tau/N, thermalisation 120 N pas).

Protocole (déclaré avant exécution) :
- pour chaque N0 et chaque graine : construire le Blob (build_blob) ;
- B naissances successives : nouveau point uniforme dans le cube ; il naît relié à ses
  k plus proches voisins (k choisi pour garder |E| = round(kappa (N+1) / 2), donc 3 ou 4 :
  1 arête de mitose + k - 1 arêtes de fermeture) ; ses paires à distance < pool_fac * r
  rejoignent le réservoir ; r reste celui de N0 ;
- après chaque naissance, on relève le degré et les triangles incidents du nouveau-né
  aux décalages t (en balayages : 1 balayage = |E| tentatives d'échange), et la moyenne
  de ces deux grandeurs sur tous les sommets ;
- t_relax(obs) = premier décalage où l'écart moyen nouveau-né − population est
  inférieur à 2 erreurs-types (sur toutes les naissances et graines).
Hypothèse [H-loc] : la loi d'attachement « k plus proches voisins » est un choix, pas une
dérivation (c'est l'objet de DEFI-M8).
"""
import importlib.util, json, math, pathlib, sys, time
import numpy as np
from scipy.spatial import cKDTree

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI.parent.parent / "corpus" / "03_scripts" / "SCRIPTS DIVERS BLOB" / "blob engine.py"
spec = importlib.util.spec_from_file_location("blob_engine", MOTEUR)
be = importlib.util.module_from_spec(spec); sys.modules["blob_engine"] = be; spec.loader.exec_module(be)

LAGS = [0, 0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]


def tri_inc(nbr, deg, u):
    c = 0; du = deg[u]
    s = set(int(x) for x in nbr[u, :du])
    for i in range(du):
        a = int(nbr[u, i])
        for m in range(deg[a]):
            if int(nbr[a, m]) in s:
                c += 1
    return c // 2


def run(N0, seed, B):
    pts, nbr, deg = be.build_blob(N0, seed=seed)
    r = (be.KAPPA / ((N0 - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    pool = cKDTree(pts).query_pairs(be.POOL_FAC * r, output_type='ndarray').astype(np.int64)
    rng = np.random.default_rng(10_000 + seed)
    N = N0
    rec = {"deg": [], "tri": [], "pop_deg": [], "pop_tri": []}
    call = 0
    for b in range(B):
        # arêtes actuelles
        eu, ev = [], []
        for u in range(N):
            for k in range(deg[u]):
                v = int(nbr[u, k])
                if v > u:
                    eu.append(u); ev.append(v)
        E = len(eu)
        k = int(round(be.KAPPA * (N + 1) / 2)) - E
        k = max(1, min(k, 8))
        p = rng.random(3)
        d = np.linalg.norm(pts - p, axis=1)
        voisins = np.argsort(d)[:k]
        newp = np.where(d < be.POOL_FAC * r)[0]
        pts = np.vstack([pts, p])
        for v in voisins:
            eu.append(int(v)); ev.append(N)
        pool = np.vstack([pool, np.stack([newp, np.full(len(newp), N)], 1)]) if len(newp) else pool
        N += 1
        eu = np.array(eu, np.int64); ev = np.array(ev, np.int64)
        nbr, deg = be._build_nbr(eu, ev, N, be.CAP)
        pa = pool[:, 0].copy(); pb = pool[:, 1].copy()
        E = len(eu); mean = 2.0 * E / N
        nt = be._n_tri(nbr, deg, N)
        dd, tt = [], []
        t_prev = 0.0
        for L in LAGS:
            steps = int(round((L - t_prev) * E))
            if steps > 0:
                call += 1
                nt = be._mcmc(nbr, deg, eu, ev, pa, pb, be.BETA, be.TAU / N, mean,
                              nt, steps, be.CAP, seed * 1_000_003 + call)
            t_prev = L
            dd.append(int(deg[N - 1])); tt.append(tri_inc(nbr, deg, N - 1))
        tpv = be._tpv(nbr, deg, N)
        rec["deg"].append(dd); rec["tri"].append(tt)
        rec["pop_deg"].append(float(deg.mean())); rec["pop_tri"].append(float(tpv.mean()))
    return rec


def analyse(recs):
    out = {}
    for obs, pop in (("deg", "pop_deg"), ("tri", "pop_tri")):
        X = np.array([row for r in recs for row in r[obs]], float)      # naissances x lags
        P = np.array([x for r in recs for x in r[pop]], float)
        diff = X - P[:, None]
        m = diff.mean(0); se = diff.std(0, ddof=1) / math.sqrt(len(diff))
        tr = None
        for L, mm, ss in zip(LAGS, m, se):
            if abs(mm) < 2 * ss:
                tr = L; break
        out[obs] = {"ecart_moyen": [round(float(x), 3) for x in m],
                    "erreur_type": [round(float(x), 3) for x in se],
                    "t_relax_balayages": tr,
                    "pop_moyenne": round(float(P.mean()), 3)}
    return out


def main():
    plan = [(250, 4, 25), (500, 4, 25), (1000, 4, 25), (2000, 4, 20), (4000, 3, 12)]
    if "--rapide" in sys.argv:
        plan = [(250, 2, 10), (1000, 2, 10)]
    res = {"protocole": "voir en-tête", "lags_balayages": LAGS, "N": {}}
    for N0, ns, B in plan:
        t0 = time.time()
        recs = [run(N0, s, B) for s in range(ns)]
        a = analyse(recs); a["graines"] = ns; a["naissances_par_graine"] = B
        a["secondes"] = round(time.time() - t0, 1)
        res["N"][str(N0)] = a
        print(N0, json.dumps(a, ensure_ascii=False), flush=True)
    (ICI / ("defi_m7_resultats_rapide.json" if "--rapide" in sys.argv else "defi_m7_resultats.json")).write_text(
        json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
