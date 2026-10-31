#!/usr/bin/env python3
"""DEFI-M13 — temps de séjour dans l'aristocratie, mesuré sans biais, contre la barrière B.

Pilote IA du laboratoire (Claude, Anthropic), 30 octobre 2026.
Chaîne non biaisée (moteur de defi_m12_lenteur.py, même mesure : M = 2n, lam = n / tau),
départ « noyau planté », rodage. Tous les Delta balayages, T_v de tous les sommets.
Un sommet est « aristocrate » quand T_v ≥ T_haut, « roturier » quand T_v ≤ T_bas ; entre
les deux, il garde son dernier état (seuils à hystérésis, lus sur le profil P(T_v) de
defi_m13_profil.py : T_haut = moitié de T au minimum aristocratique, T_bas = 2).
Sortie = passage aristocrate → roturier. Temps de séjour moyen = temps total passé à l'état
« aristocrate » (sommets × balayages) / nombre de sorties. Si la lenteur est la traversée
activée du col de F(T) = −log P(T), log(séjour) doit suivre B à une constante près.
Usage : python3 defi_m13_sorties.py [--tailles 25,33,49,65,97,129,193] [--processus 2]
        [--sortie defi_m13_sorties.json]
"""
import json
import math
import pathlib
import sys
import time
from multiprocessing import Pool

import numpy as np

import defi_m12_lenteur as L

ICI = pathlib.Path(__file__).resolve().parent
# longueur de production en demi-temps t½ de DEFI-M12, Delta en fraction de t½
T_DEMI = {17: 9.2, 25: 21.5, 33: 43.3, 49: 146, 65: 389, 97: 2297, 129: 9760, 193: 111873}
LONGUEUR_T_DEMI = {17: 400, 25: 400, 33: 400, 49: 300, 65: 300, 97: 150, 129: 60, 193: 16}


def une(args):
    n, t_ari, graine = args
    m = 2 * n
    lam = n / L.TAU
    td = T_DEMI[n]
    delta = max(1, int(round(td / 40)))
    nrec = int(LONGUEUR_T_DEMI[n] * td / delta)
    rng = np.random.default_rng(graine)
    L.graine_numba(graine)
    adj, ar, deg, etat = L.depart(n, m, rng, True)
    L.balayer(adj, ar, deg, etat, n, int(max(400, 3 * td)) * m, lam)
    t_haut = max(3, t_ari // 2)
    t_bas = 2
    tv = np.zeros(n, dtype=np.int64)
    L.tri_tous(adj, n, tv)
    etat_v = np.where(tv >= t_haut, 1, 0)
    sorties = 0
    entrees = 0
    temps_ari = 0
    t0 = time.time()
    for i in range(nrec):
        L.balayer(adj, ar, deg, etat, n, delta * m, lam)
        L.tri_tous(adj, n, tv)
        nouveau = etat_v.copy()
        nouveau[tv >= t_haut] = 1
        nouveau[tv <= t_bas] = 0
        sorties += int(((etat_v == 1) & (nouveau == 0)).sum())
        entrees += int(((etat_v == 0) & (nouveau == 1)).sum())
        temps_ari += int(nouveau.sum()) * delta
        etat_v = nouveau
    sejour = temps_ari / sorties if sorties else None
    return {"n": n, "graine": graine, "delta": delta, "enregistrements": nrec, "balayages": nrec * delta,
            "t_haut": int(t_haut), "t_bas": t_bas, "sorties": sorties, "entrees": entrees,
            "aristocrates_moyen": temps_ari / (nrec * delta), "sejour_balayages": sejour, "duree_s": time.time() - t0}


def main():
    def opt(nom, defaut):
        return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut
    tailles = [int(x) for x in opt("--tailles", "25,33,49,65,97,129,193").split(",")]
    prof = json.loads((ICI / "defi_m13_profil_c2.json").read_text())["points"]
    taches = []
    for n in tailles:
        # T au minimum aristocratique : moyenne sur les répétitions du profil
        t_ari = int(round(np.mean([r["barriere"]["t_ari"] for r in prof if r["n"] == n and r["barriere"]["t_ari"] is not None])))
        for j in range(2):
            taches.append((n, t_ari, 4242 + 10 * n + j))
    res = []
    with Pool(int(opt("--processus", "2"))) as p:
        for r in p.imap_unordered(une, taches):
            res.append(r)
            print(r["n"], "sorties", r["sorties"], "entrées", r["entrees"], "aristocrates", round(r["aristocrates_moyen"], 2),
                  "séjour", None if r["sejour_balayages"] is None else round(r["sejour_balayages"], 1),
                  "%.0f s" % r["duree_s"], flush=True)
            (ICI / opt("--sortie", "defi_m13_sorties.json")).write_text(
                json.dumps({"cadre": __doc__.split("Usage")[0], "chaines": res}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
