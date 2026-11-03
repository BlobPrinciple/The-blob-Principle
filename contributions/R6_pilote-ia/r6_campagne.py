# -*- coding: utf-8 -*-
"""DEFI-R6 — partie B : campagne à quatre bras sur conditions initiales reconstruites.

Bras (même configuration initiale par graine, donc différences appariées) :
  figé     : germes multi-sites, aucune dynamique ;
  mobile   : germes, relax_positions(viab=False) du moteur archivé ;
  viab     : germes, relax_positions(viab=True) du moteur archivé ;
  poisson  : uniforme figé.
Le moteur de mobilité (relax_positions, local_S, rgg_radius, κ = 6,6, β = 0,30,
τ = 0,50) est importé tel quel de
corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob gravite colab.py
(le moteur « à mobilité des positions » du 25 mai, V346 XXV.1 p. 642).

Usage : python3 r6_campagne.py --N 5000 --graines 0:8 --balayages 5 [--init poisson] --sortie f.json
"""
import argparse, importlib.util, json, os, time
import numpy as np
from scipy.spatial import cKDTree
import r6_mesures as M

ICI = os.path.dirname(os.path.abspath(__file__))
MOTEUR = os.path.join(ICI, "..", "..", "corpus", "06_campagnes_et_sauts",
                      "Audit 25 mai — paliers et gravite", "blob gravite colab.py")
spec = importlib.util.spec_from_file_location("moteur_gravite", MOTEUR)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)


def rgg(pts, N):
    r = G.rgg_radius(N, G.KAPPA)
    adj = [set() for _ in range(N)]
    for i, j in cKDTree(pts).query_pairs(r, output_type="ndarray"):
        adj[i].add(int(j)); adj[j].add(int(i))
    return adj, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--graines", default="0:8")
    ap.add_argument("--balayages", type=int, default=5)
    ap.add_argument("--s", type=float, default=0.12)
    ap.add_argument("--init", default="germes", choices=["germes", "poisson"],
                    help="poisson : la configuration initiale des bras figé/mobile/viab est uniforme")
    ap.add_argument("--sortie", required=True)
    a = ap.parse_args()
    g0, g1 = map(int, a.graines.split(":"))
    res = {"N": a.N, "balayages": a.balayages, "s": a.s, "K": 8, "init": a.init, "graines": {}}
    if os.path.exists(a.sortie):
        res = json.load(open(a.sortie))
    for g in range(g0, g1):
        if str(g) in res["graines"]:
            continue
        t = time.time()
        rng = np.random.default_rng(1000 + g)
        p0 = M.germes(a.N, rng, s=a.s) if a.init == "germes" else M.poisson(a.N, rng)
        e = {"fige": M.resume(p0)}
        e["fige"]["fraction_a_moins_de_r_d_une_face"] = float(((p0 < G.rgg_radius(a.N, G.KAPPA)) | (p0 > 1 - G.rgg_radius(a.N, G.KAPPA))).any(1).mean())
        adj0, r = rgg(p0, a.N)
        e["degre_moyen_initial"] = float(np.mean([len(x) for x in adj0]))
        for nom, viab in (("mobile", False), ("viab", True)):
            pts, adj = G.relax_positions(p0.copy(), [set(x) for x in adj0], a.N, r, seed=g,
                                         viab=viab, sweeps=a.balayages)
            e[nom] = M.resume(pts)
            e[nom]["deplacement_moyen"] = float(np.linalg.norm(pts - p0, axis=1).mean())
            e[nom]["fraction_deplaces"] = float((np.linalg.norm(pts - p0, axis=1) > 0).mean())
            # contrôle de bord : le moteur archivé rogne les pas à [0,1] (np.clip), boîte non périodique
            e[nom]["fraction_sur_une_face"] = float(((pts == 0) | (pts == 1)).any(1).mean())
            e[nom]["fraction_a_moins_de_r_d_une_face"] = float(((pts < r) | (pts > 1 - r)).any(1).mean())
        e["poisson"] = M.resume(M.poisson(a.N, np.random.default_rng(5000 + g)))
        e["secondes"] = time.time() - t
        res["graines"][str(g)] = e
        json.dump(res, open(a.sortie, "w"), indent=1)
        print(f"N={a.N} g={g} {e['secondes']:.0f}s amp figé {e['fige']['Pmax_sur_N2']:.4f} "
              f"mobile {e['mobile']['Pmax_sur_N2']:.4f} viab {e['viab']['Pmax_sur_N2']:.4f} | vides "
              f"{e['fige']['vides']:.4f} {e['mobile']['vides']:.4f} {e['viab']['vides']:.4f} | "
              f"dépl. {e['mobile']['deplacement_moyen']:.4f} {e['viab']['deplacement_moyen']:.4f}", flush=True)


if __name__ == "__main__":
    main()
