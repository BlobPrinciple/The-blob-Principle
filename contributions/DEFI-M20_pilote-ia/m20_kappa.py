#!/usr/bin/env python3
"""DEFI-M20 (RO-08), volet « κ ≥ 8 » — l'aristocratie et l'obstacle local survivent-ils à κ plus grand ?

Contribution du pilote IA du laboratoire (Claude, Anthropic), 27 novembre 2026.
Critère déposé avant la mesure : https://github.com/BlobPrinciple/The-blob-Principle/issues/56#issuecomment-7213958737

Variante : moteur canonique importé tel quel, build_blob(N, seed, kappa=κ), seuls κ changé
(β, τ, pool_fac, therm_fac canoniques). Témoin build_rgg au même κ.
Conditions locales nécessaires (voir contributions/RO-08_pilote-ia/NOTE.md) :
(C1) deg >= 4 ; (C2) t_v >= 3 deg - 6 ; (C3) >= 3 voisins communs par arête.
Grandeurs : V, G (Gini de t_v), A10 (part de Σ t_v au décile supérieur), Z (sans triangle).
Implémentation : ensembles Python (bilan) ; Gini par la formule triée du moteur.
"""
import importlib.util, json, pathlib, sys, time
import numpy as np

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI.parent.parent / "corpus" / "03_scripts" / "SCRIPTS DIVERS BLOB" / "blob engine.py"
spec = importlib.util.spec_from_file_location("blob_engine", MOTEUR)
be = importlib.util.module_from_spec(spec); sys.modules["blob_engine"] = be; spec.loader.exec_module(be)

KAPPAS = (6.6, 8.0, 10.0, 12.0, 14.0)
TAILLES = (1000, 2000, 4000)
GRAINES = range(4)


def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if x.sum() == 0:
        return 0.0
    c = np.arange(1, n + 1)
    return float(2 * np.sum(c * x) / (n * x.sum()) - (n + 1) / n)


def bilan(nbr, deg, N):
    adj = [set(int(x) for x in nbr[u, :deg[u]]) for u in range(N)]
    d = np.array([len(a) for a in adj])
    t = np.array([sum(len(adj[a] & s) for a in s) // 2 for s in adj])
    c1 = d < 4; c2 = t < 3 * d - 6
    se = np.zeros(N, bool); E = 0; ve = 0
    for u in range(N):
        for v in adj[u]:
            if v > u:
                E += 1
                if len(adj[u] & adj[v]) < 3:
                    ve += 1; se[u] = se[v] = True
    k = max(1, N // 10)
    ts = np.sort(t)[::-1]
    return {"N": N, "E": E, "kappa_mes": 2 * E / N, "deg_max": int(d.max()),
            "V": float((c1 | c2 | se).mean()), "C1": float(c1.mean()), "C2": float(c2.mean()),
            "C3_aretes": ve / E, "C3_sommets": float(se.mean()),
            "G": gini(t), "A10": float(ts[:k].sum() / max(t.sum(), 1)), "Z": float((t == 0).mean()),
            "ntri_par_N": float(t.sum() / 3 / N), "seuil_global": 2 * E / N - 2}


def main():
    res = []
    out = ICI / "m20_kappa.json"
    for kap in KAPPAS:
        for N in TAILLES:
            for s in GRAINES:
                t0 = time.time()
                _, nbr, deg = be.build_blob(N, seed=s, kappa=kap)
                b = bilan(nbr, deg, N); b.update(modele="blob", kappa=kap, graine=s)
                _, nbr, deg = be.build_rgg(N, seed=s, kappa=kap)
                g = bilan(nbr, deg, N); g.update(modele="rgg", kappa=kap, graine=s)
                res += [b, g]
                print(f"κ={kap} N={N} s={s} ({time.time()-t0:.0f}s) BLOB V={b['V']:.3f} G={b['G']:.3f} "
                      f"A10={b['A10']:.3f} Z={b['Z']:.3f} C3e={b['C3_aretes']:.3f} dmax={b['deg_max']} | "
                      f"RGG V={g['V']:.3f} G={g['G']:.3f} A10={g['A10']:.3f} Z={g['Z']:.3f}", flush=True)
                json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
