#!/usr/bin/env python3
"""DEFI-M9 — l'aristocratie des sommets massifs (moteur canonique, Rips 3D).

Contribution du pilote IA du laboratoire (Claude, Anthropic), 16 octobre 2026.
Suite de DEFI-M7 (defi_m7_cout_du_pont.py), dont la loi de naissance est reprise telle quelle.

Question : un sommet nouveau-né atteint-il la loi des triangles incidents de la population,
ou reste-t-il durablement en déficit (aristocratie figée des sommets massifs) ?

Protocole (déclaré avant exécution) :
- moteur : corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py, importé tel quel,
  paramètres canoniques gelés (kappa 6.6, beta 0.30, tau 0.50, pool_fac 1.6, tau_eff = tau/N) ;
- naissance [H-loc] (hypothèse de localité, [H] au sens de l'armature) : point uniforme dans le cube, relié à ses k plus proches voisins,
  k choisi pour garder |E| = round(kappa (N+1)/2) ; paires à distance < pool_fac r ajoutées
  au réservoir ; r reste celui de N0 (identique à DEFI-M7) ;
- après chaque naissance, décalages t = 0, 16, 64, 256, 1024, 2048 balayages
  (1 balayage = |E| tentatives) ; à chaque décalage :
    * PIT du nouveau-né : u = (#{autres sommets de masse < x} + U #{= x}) / (N - 1),
      U uniforme (départage des ex aequo) ; à l'équilibre, u suit la loi uniforme ;
    * même PIT pour un sommet témoin tiré au hasard parmi les sommets d'origine
      (indice < N0), qui donne le plancher statistique à effectif égal ;
- par taille : 10 graines x 20 naissances = 200 naissances ;
- statistiques : moyenne de u (0,5 attendu), part de u > 0,9 (0,1 attendu),
  variation totale sur 10 classes de u contre l'uniforme, test de Kolmogorov-Smirnov ;
- contrôle de figement (ajouté après lecture des premiers résultats de naissance, voir
  DEFI-M9_RAPPORT.md §2), sur la chaîne stationnaire sans naissance : corrélation de rang
  (Spearman) entre la masse triangulaire de chaque sommet à t0 et à t0 + t, et corrélation
  de la masse avec le degré de réservoir (nombre de paires du réservoir incidentes,
  fixé par la position).
"""
import importlib.util, json, math, pathlib, sys, time
import numpy as np
from scipy import stats
from scipy.spatial import cKDTree

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI.parent.parent / "corpus" / "03_scripts" / "SCRIPTS DIVERS BLOB" / "blob engine.py"
spec = importlib.util.spec_from_file_location("blob_engine", MOTEUR)
be = importlib.util.module_from_spec(spec); sys.modules["blob_engine"] = be; spec.loader.exec_module(be)

LAGS = [0, 16, 64, 256, 1024, 2048]
LAGS_STAT = [16, 64, 256, 1024, 4096]


def pit(x, autres, rng):
    lt = np.count_nonzero(autres < x); eq = np.count_nonzero(autres == x)
    return (lt + rng.random() * eq) / len(autres)


def aretes(nbr, deg, N):
    eu, ev = [], []
    for u in range(N):
        for k in range(deg[u]):
            v = int(nbr[u, k])
            if v > u:
                eu.append(u); ev.append(v)
    return eu, ev


def run(N0, seed, B):
    pts, nbr, deg = be.build_blob(N0, seed=seed)
    r = (be.KAPPA / ((N0 - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    pool = cKDTree(pts).query_pairs(be.POOL_FAC * r, output_type='ndarray').astype(np.int64)
    rng = np.random.default_rng(20_000 + seed)
    N = N0; call = 0
    rec = {"u_nb": [], "u_ctl": [], "d_tri": [], "x_nb": []}
    for b in range(B):
        eu, ev = aretes(nbr, deg, N)
        k = int(round(be.KAPPA * (N + 1) / 2)) - len(eu)
        k = max(1, min(k, 8))
        p = rng.random(3)
        d = np.linalg.norm(pts - p, axis=1)
        voisins = np.argsort(d)[:k]
        newp = np.where(d < be.POOL_FAC * r)[0]
        pts = np.vstack([pts, p])
        for v in voisins:
            eu.append(int(v)); ev.append(N)
        if len(newp):
            pool = np.vstack([pool, np.stack([newp, np.full(len(newp), N)], 1)])
        N += 1
        eu = np.array(eu, np.int64); ev = np.array(ev, np.int64)
        nbr, deg = be._build_nbr(eu, ev, N, be.CAP)
        pa = pool[:, 0].copy(); pb = pool[:, 1].copy()
        E = len(eu); mean = 2.0 * E / N
        nt = be._n_tri(nbr, deg, N)
        ctl = int(rng.integers(0, N0))
        un, uc, dt, xn = [], [], [], []
        t_prev = 0
        for L in LAGS:
            steps = (L - t_prev) * E
            if steps > 0:
                call += 1
                nt = be._mcmc(nbr, deg, eu, ev, pa, pb, be.BETA, be.TAU / N, mean,
                              nt, steps, be.CAP, seed * 1_000_003 + call)
            t_prev = L
            tpv = be._tpv(nbr, deg, N)
            nb = N - 1
            autres_nb = np.delete(tpv, nb)
            autres_ctl = np.delete(tpv, [ctl, nb])
            un.append(pit(tpv[nb], autres_nb, rng))
            uc.append(pit(tpv[ctl], autres_ctl, rng))
            dt.append(float(tpv[nb] - autres_nb.mean()))
            xn.append(int(tpv[nb]))
        rec["u_nb"].append(un); rec["u_ctl"].append(uc); rec["d_tri"].append(dt); rec["x_nb"].append(xn)
    return rec


def tv10(u):
    h = np.histogram(u, bins=10, range=(0, 1))[0] / len(u)
    return 0.5 * float(np.abs(h - 0.1).sum())


def resume(u):
    u = np.asarray(u, float); n = len(u)
    return {"moy_u": round(float(u.mean()), 4),
            "et_moy_u": round(float(u.std(ddof=1) / math.sqrt(n)), 4),
            "part_u_sup_0.9": round(float((u > 0.9).mean()), 4),
            "part_u_inf_0.1": round(float((u < 0.1).mean()), 4),
            "TV10": round(tv10(u), 4),
            "KS_p": float("%.3g" % stats.kstest(u, "uniform").pvalue)}


def analyse(recs):
    U = np.array([x for r in recs for x in r["u_nb"]], float)
    C = np.array([x for r in recs for x in r["u_ctl"]], float)
    D = np.array([x for r in recs for x in r["d_tri"]], float)
    out = {"n_naissances": int(U.shape[0]), "lags_balayages": LAGS, "par_lag": []}
    for j, L in enumerate(LAGS):
        out["par_lag"].append({"t": L, "nouveau_ne": resume(U[:, j]), "temoin": resume(C[:, j]),
                               "ecart_tri_moy": round(float(D[:, j].mean()), 3),
                               "ecart_tri_et": round(float(D[:, j].std(ddof=1) / math.sqrt(len(D))), 3)})
    return out


def figement(N, seed):
    """Chaîne stationnaire sans naissance : la masse de chaque sommet est-elle figée ?"""
    pts, nbr, deg = be.build_blob(N, seed=seed)
    r = (be.KAPPA / ((N - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    pool = cKDTree(pts).query_pairs(be.POOL_FAC * r, output_type='ndarray').astype(np.int64)
    dpool = np.bincount(pool.ravel(), minlength=N)
    eu, ev = aretes(nbr, deg, N)
    eu = np.array(eu, np.int64); ev = np.array(ev, np.int64)
    pa = pool[:, 0].copy(); pb = pool[:, 1].copy()
    E = len(eu); mean = 2.0 * E / N; nt = be._n_tri(nbr, deg, N)
    t0 = be._tpv(nbr, deg, N).copy()
    haut0 = t0 >= np.quantile(t0, 0.9)          # décile supérieur, ex aequo inclus
    out = {"part_haut_decile_t0": round(float(haut0.mean()), 4), "rho_masse_reservoir_t0": round(float(stats.spearmanr(t0, dpool)[0]), 4), "lags": []}
    t_prev = 0
    for L in LAGS_STAT:
        nt = be._mcmc(nbr, deg, eu, ev, pa, pb, be.BETA, be.TAU / N, mean, nt,
                      (L - t_prev) * E, be.CAP, 777_000 + seed * 101 + L)
        t_prev = L
        tl = be._tpv(nbr, deg, N)
        out["lags"].append({"t": L,
                            "rho_masse_t0_t": round(float(stats.spearmanr(t0, tl)[0]), 4),
                            "rho_masse_reservoir": round(float(stats.spearmanr(tl, dpool)[0]), 4),
                            # part des sommets du décile supérieur à t0 qui y sont encore à t
                            "persistance_haut_decile": round(float((tl[haut0] >= np.quantile(tl, 0.9)).mean()), 4),
                            "part_haut_decile_t": round(float((tl >= np.quantile(tl, 0.9)).mean()), 4)})
    return out


def option(nom, defaut=None):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main():
    """Sans option : plan complet. Options (pour découper le calcul en morceaux) :
    --tailles 250,500  --graines 0:10  --sans-figement  --figement-seul  --sortie nom.json"""
    plan = [(250, 10, 20), (500, 10, 20), (1000, 10, 20), (2000, 10, 20)]
    stat_plan = [(500, 3), (2000, 3)]
    g0, g1 = (int(x) for x in option("--graines", "0:10").split(":"))
    if option("--tailles"):
        tailles = [int(x) for x in option("--tailles").split(",")]
        plan = [p for p in plan if p[0] in tailles]
    if "--figement-seul" in sys.argv:
        plan = []
    if "--sans-figement" in sys.argv:
        stat_plan = []
    sortie = option("--sortie", "defi_m9_resultats.json")
    if "--rapide" in sys.argv:
        plan = [(250, 2, 5)]; stat_plan = [(250, 1)]; sortie = "defi_m9_resultats_rapide.json"; g0, g1 = 0, 2
    res = {"protocole": "voir en-tête", "graines": [g0, g1], "N": {}, "figement": {}, "brut": {}}
    for N0, ns, B in plan:
        t0 = time.time()
        recs = [run(N0, s, B) for s in range(g0, g1)]
        a = analyse(recs); a["graines"] = g1 - g0; a["naissances_par_graine"] = B
        a["secondes"] = round(time.time() - t0, 1)
        res["N"][str(N0)] = a; res["brut"][str(N0)] = recs
        print(N0, json.dumps(a, ensure_ascii=False), flush=True)
    for N, ns in stat_plan:
        res["figement"][str(N)] = [figement(N, 50 + s) for s in range(ns)]
        print("figement", N, json.dumps(res["figement"][str(N)], ensure_ascii=False), flush=True)
    (ICI / sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
