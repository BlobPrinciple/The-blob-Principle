#!/usr/bin/env python3
"""DEFI-M9 — le décile massif est-il fixé par la position ou figé par la dynamique ?

Contribution du pilote IA du laboratoire (Claude, Anthropic), 16 octobre 2026.

Contrôle ajouté après lecture des premiers résultats de naissance (DEFI-M9_RAPPORT.md §2),
puis complété, à la demande de la relecture hostile, par le témoin C et la mesure des bords.
Sur un même nuage de points (même graine de positions),
deux chaînes du moteur canonique, importé tel quel :
- chaîne A : départ canonique (les round(N kappa / 2) paires les plus courtes du réservoir) ;
- chaîne B : départ différent (autant de paires du réservoir tirées au hasard), autre graine
  de Metropolis ;
- chaîne C (témoin) : même départ que A, autre graine de Metropolis.
Chacune reçoit la thermalisation canonique (120 N pas) puis T = 4 096 balayages.
On compare le décile supérieur de masse (triangles incidents, ex aequo inclus) :
- persistance dans A entre la fin de la thermalisation et t = 4 096 balayages ;
- recouvrement entre A et B à t = 4 096 balayages.
Le recouvrement A-C mesure ce que partagent deux chaînes de même départ ; si A-B est nettement
plus bas que A-C, le décile garde la mémoire de l'état initial.
On relève aussi la part du décile à moins de r d'une face du cube (bords non périodiques) et le
recouvrement entre le décile de masse et le décile de degré de réservoir (fixé par la position).
Lecture : si le recouvrement A-B est proche de la persistance, l'aristocratie est fixée par
les positions (elle existe aussi à l'équilibre) ; s'il est proche de 0,1 (hasard) alors que
la persistance est élevée, elle est figée par la dynamique (mémoire de l'état initial).
"""
import importlib.util, json, pathlib, sys
import numpy as np

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI.parent.parent / "corpus" / "03_scripts" / "SCRIPTS DIVERS BLOB" / "blob engine.py"
spec = importlib.util.spec_from_file_location("blob_engine", MOTEUR)
be = importlib.util.module_from_spec(spec); sys.modules["blob_engine"] = be; spec.loader.exec_module(be)
T = 4096


def chaine(N, pool, edges, graine):
    eu = edges[:, 0].copy(); ev = edges[:, 1].copy()
    nbr, deg = be._build_nbr(eu.copy(), ev.copy(), N, be.CAP)
    pa = pool[:, 0].copy(); pb = pool[:, 1].copy()
    mean = 2.0 * len(eu) / N; nt = be._n_tri(nbr, deg, N)
    nt = be._mcmc(nbr, deg, eu, ev, pa, pb, be.BETA, be.TAU / N, mean, nt, be.THERM_FAC * N,
                  be.CAP, graine)
    m0 = be._tpv(nbr, deg, N).copy()
    nt = be._mcmc(nbr, deg, eu, ev, pa, pb, be.BETA, be.TAU / N, mean, nt, T * len(eu),
                  be.CAP, graine + 1)
    return m0, be._tpv(nbr, deg, N).copy(), nt / N


def haut(m):
    return m >= np.quantile(m, 0.9)


def main():
    plan = [(250, 3), (500, 4), (2000, 3)] if "--rapide" not in sys.argv else [(250, 1)]
    out = []
    for N, ng in plan:
        for g in range(ng):
            pts, edges, pool = be._rips(N, 300 + g, be.KAPPA, be.POOL_FAC)
            rng = np.random.default_rng(4_000 + g)
            edgesB = pool[rng.choice(len(pool), size=len(edges), replace=False)]
            a0, aT, ntA = chaine(N, pool, edges, 11_000 + g)
            b0, bT, ntB = chaine(N, pool, edgesB, 22_000 + g)
            c0, cT, ntC = chaine(N, pool, edges, 33_000 + g)
            hA0, hAT, hBT, hCT = haut(a0), haut(aT), haut(bT), haut(cT)
            r_ = (be.KAPPA / ((N - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
            bord = np.min(np.minimum(pts, 1 - pts), axis=1) < r_
            dpool = np.bincount(pool.ravel(), minlength=N); hP = haut(dpool)
            r = {"N": N, "graine": 300 + g,
                 "n_tri_par_N_A": round(float(ntA), 3), "n_tri_par_N_B": round(float(ntB), 3),
                 "persistance_A": round(float((hA0 & hAT).sum() / hA0.sum()), 4),
                 "recouvrement_A_B": round(float((hAT & hBT).sum() / hAT.sum()), 4),
                 "recouvrement_A_C": round(float((hAT & hCT).sum() / hAT.sum()), 4),
                 "part_bord_tous": round(float(bord.mean()), 4),
                 "part_bord_decile_A": round(float(bord[hAT].mean()), 4),
                 "recouvrement_masse_reservoir": round(float((hAT & hP).sum() / hAT.sum()), 4),
                 "part_haut_A": round(float(hAT.mean()), 4), "part_haut_B": round(float(hBT.mean()), 4)}
            out.append(r); print(r, flush=True)
    if "--rapide" not in sys.argv:
        (ICI / "defi_m9_deux_chaines.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
