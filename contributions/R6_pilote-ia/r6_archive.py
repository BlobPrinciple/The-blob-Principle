# -*- coding: utf-8 -*-
"""DEFI-R6 — partie A : relecture du fichier archivé blob_toile_results.json.

Question : la croissance de P_max/médiane avec N (master V346, XXV.2, p. 644–645)
traduit-elle une structure qui croît, ou seulement la loi d'échelle cinématique
d'une modulation de densité de forme fixe ?

Identité [T] : pour N points i.i.d. de densité ρ sur [0,1]^3,
  E |Σ_j exp(2πi k·x_j)|^2 = N + N(N−1) |ρ̂(k)|^2 .
Le bruit de grenaille vaut N ; une modulation de forme fixe donne un terme en N^2.
Donc P_max/médiane ≈ 1 + (N−1)|ρ̂|^2 croît linéairement en N sans que la structure
change. Le test : P_max/N^2 (amplitude relative) et médiane/N doivent être
constants en N si la structure est de forme fixe.

Sortie : r6_archive_sortie.json et impression texte.
"""
import json, sys, os, collections
import numpy as np
from scipy import stats

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, "..", "..", "corpus", "06_campagnes_et_sauts",
                   "Audit 25 mai — paliers et gravite", "blob_toile_results.json")


def main():
    d = json.load(open(SRC))
    par = collections.defaultdict(dict)  # (mode, N) -> {seed: entry}
    for cle, e in d.items():
        mode, n, s = cle.rsplit("_", 2)
        par[(mode, int(n[1:]))][int(s[1:])] = e
    modes = ["multi", "multi_noviab", "single", "poisson"]
    tailles = sorted({n for (_, n) in par})
    out = {"source": "corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob_toile_results.json",
           "par_bras": {}, "pentes_loglog": {}, "apparie_viab_moins_noviab": {}}
    print("mode N graines | Pmax/med | Pmax/N^2 | med/N | void")
    for m in modes:
        xs, ys, amp = [], [], []
        for n in tailles:
            es = par[(m, n)]
            pk = np.array([es[s]["pk"][1] for s in sorted(es)])
            r = pk.max(1) / np.median(pk, 1)
            a = pk.max(1) / n**2
            md = np.median(pk, 1) / n
            v = np.array([es[s]["void"] for s in sorted(es)])
            ng = len(es)
            def ms(x):
                return [float(x.mean()), float(x.std(ddof=1) / np.sqrt(len(x)))]
            out["par_bras"][f"{m}_N{n}"] = {"graines": ng, "Pmax_sur_mediane": ms(r),
                                           "Pmax_sur_N2": ms(a), "mediane_sur_N": ms(md),
                                           "vides": ms(v)}
            print(f"{m:13s} {n:6d} {ng} | {r.mean():8.1f} ± {r.std(ddof=1)/np.sqrt(ng):6.1f} | "
                  f"{a.mean():.4f} ± {a.std(ddof=1)/np.sqrt(ng):.4f} | {md.mean():.3f} | {v.mean():.3f}")
            xs += [np.log(n)] * ng; ys += list(np.log(r)); amp += list(np.log(a))
        if m != "poisson":
            sl = stats.linregress(xs, ys)
            sa = stats.linregress(xs, amp)
            out["pentes_loglog"][m] = {"pente_Pmax_sur_mediane": [sl.slope, sl.stderr],
                                       "pente_Pmax_sur_N2": [sa.slope, sa.stderr]}
            print(f"  pente log-log {m}: Pmax/med {sl.slope:.3f} ± {sl.stderr:.3f} ; "
                  f"Pmax/N^2 {sa.slope:.3f} ± {sa.stderr:.3f}")
    # appariement par graine viab - noviab (mêmes clés de graine)
    print("apparié multi − multi_noviab : ΔPmax/N^2, Δvides, paires où Δ>0")
    for n in tailles:
        a, b = par[("multi", n)], par[("multi_noviab", n)]
        com = sorted(set(a) & set(b))
        da = np.array([max(a[s]["pk"][1]) - max(b[s]["pk"][1]) for s in com]) / n**2
        dv = np.array([a[s]["void"] - b[s]["void"] for s in com])
        out["apparie_viab_moins_noviab"][f"N{n}"] = {
            "paires": len(com), "dPmax_sur_N2": [float(da.mean()), float(da.std(ddof=1) / np.sqrt(len(com)))],
            "dPmax_sur_N2_positifs": int((da > 0).sum()),
            "dvides": [float(dv.mean()), float(dv.std(ddof=1) / np.sqrt(len(com)))],
            "dvides_positifs": int((dv > 0).sum())}
        print(f"  N={n:6d} {len(com)} paires : {da.mean():+.4f} ± {da.std(ddof=1)/np.sqrt(len(com)):.4f} "
              f"({(da>0).sum()}/{len(com)}) ; vides {dv.mean():+.4f} ({(dv>0).sum()}/{len(com)})")
    # puissance à k intermédiaire (P(k)/N moyen sur les graines), signal propre à la viabilité
    out["P_sur_N_k_intermediaires"] = {}
    print("P(k)/N moyen aux k = 6, 8, 10, 12, 15 ; 1/(2,9 r_N)")
    for m in modes:
        for n in (1000, 5000, 10000, 20000):
            es = par[(m, n)]
            a = np.mean([np.array(es[s]["pk"][1]) / n for s in es], 0)
            r = (6.6 / ((n - 1) * 4 / 3 * np.pi)) ** (1 / 3)
            v = {str(k): float(a[k - 1]) for k in (6, 8, 10, 12, 15)}
            out["P_sur_N_k_intermediaires"][f"{m}_N{n}"] = v
            print(f"  {m:13s} {n:6d} " + " ".join(f"{v[k]:7.2f}" for k in v) + f" | {1/(2.9*r):.1f}")
    json.dump(out, open(os.path.join(ICI, "r6_archive_sortie.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
