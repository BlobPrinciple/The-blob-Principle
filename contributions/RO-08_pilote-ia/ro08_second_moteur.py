#!/usr/bin/env python3
"""RO-08 — seconde implémentation (matrices creuses), sans code commun avec ro08_squelette.py
pour les comptes : t_v = (A^3)_vv / 2, c_uv = (A^2)_uv sur les arêtes, degrés = somme des lignes.
Régénère les mêmes configurations (moteur canonique déterministe à graine fixée) et compare.
Ajoute la ventilation des violations par décile de masse triangulaire (aristocratie).
"""
import importlib.util, json, pathlib, sys
import numpy as np
import scipy.sparse as sp

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI.parent.parent / "corpus" / "03_scripts" / "SCRIPTS DIVERS BLOB" / "blob engine.py"
spec = importlib.util.spec_from_file_location("blob_engine", MOTEUR)
be = importlib.util.module_from_spec(spec); sys.modules["blob_engine"] = be; spec.loader.exec_module(be)


def matrice(nbr, deg, N):
    r = np.repeat(np.arange(N), deg)
    c = np.concatenate([nbr[u, :deg[u]] for u in range(N)])
    A = sp.csr_matrix((np.ones(len(r), np.int64), (r, c)), shape=(N, N))
    assert (A != A.T).nnz == 0 and A.diagonal().sum() == 0
    return A


def comptes(A):
    d = np.asarray(A.sum(1)).ravel()
    A2 = A @ A
    t = np.asarray(A2.multiply(A).sum(1)).ravel() // 2      # arêtes entre voisins
    C = sp.triu(A2.multiply(A), 1).tocoo()                  # voisins communs sur les arêtes (>0 seulement)
    E = sp.triu(A, 1).nnz
    ce_ge3 = C.data >= 3
    bad = np.zeros(A.shape[0], bool)
    # sommets touchés par une arête à c < 3 : toutes les arêtes moins celles à c >= 3
    U = sp.triu(A, 1).tocoo()
    ok = sp.csr_matrix((ce_ge3.astype(np.int64), (C.row, C.col)), shape=A.shape)
    okv = np.asarray(ok[U.row, U.col]).ravel() > 0
    bad[U.row[~okv]] = True; bad[U.col[~okv]] = True
    bad |= (d < 4) | (t < 3 * d - 6)
    return d, t, E, int((~okv).sum()), bad


def main():
    ref = json.load(open(ICI / "ro08_squelette.json"))
    out = {"comparaison": [], "deciles_blob": [], "deciles_rgg": []}
    ecart_max = 0.0
    for N in (500, 1000, 2000, 4000):
        for s in range(4):
            for nom, fab in (("blob", be.build_blob), ("rgg", be.build_rgg)):
                _, nbr, deg = fab(N, seed=s)
                d, t, E, ne, bad = comptes(matrice(nbr, deg, N))
                r = [x for x in ref[nom] if x["N"] == N and x["graine"] == s][0]
                mine = {"frac_sommets_viol": bad.mean(), "frac_aretes_C3": ne / E,
                        "frac_C2": (t < 3 * d - 6).mean(), "ntri_par_N": t.sum() / 3 / N,
                        "deficit_C2_total": np.maximum(0, 3 * d - 6 - t).sum()}
                for k, v in mine.items():
                    ecart_max = max(ecart_max, abs(float(v) - float(r[k])))
                out["comparaison"].append({"modele": nom, "N": N, "graine": s, **{k: float(v) for k, v in mine.items()}})
                if N == 4000:
                    rang = np.empty(N, np.int64); rang[np.lexsort((np.random.default_rng(s).random(N), t))] = np.arange(N); cls = rang * 10 // N  # déciles par rang, ex aequo départagés au hasard
                    lig = []
                    for c in range(10):
                        m = cls == c
                        lig.append({"decile": c, "n": int(m.sum()), "masse_moy": float(t[m].mean()) if m.any() else None,
                                    "deg_moy": float(d[m].mean()) if m.any() else None,
                                    "frac_C1": float((d[m] < 4).mean()) if m.any() else None,
                                    "frac_C2": float((t[m] < 3 * d[m] - 6).mean()) if m.any() else None,
                                    "frac_viol": float(bad[m].mean()) if m.any() else None})
                    out["deciles_" + nom].append({"graine": s, "frac_masse_nulle": float((t == 0).mean()), "deciles": lig})
    out["ecart_max_avec_premier_script"] = ecart_max
    print("écart maximal avec ro08_squelette.json :", ecart_max)
    for nom in ("blob", "rgg"):
        print(nom, "N=4000, déciles de masse (moyenne sur 4 graines) : décile, masse, degré, C1, C2, viol")
        for c in range(10):
            vals = [g["deciles"][c] for g in out["deciles_" + nom] if g["deciles"][c]["n"] > 0]
            f = lambda k: np.mean([v[k] for v in vals])
            print(f"  {c} {f('masse_moy'):7.1f} {f('deg_moy'):5.1f} {f('frac_C1'):.3f} {f('frac_C2'):.3f} {f('frac_viol'):.3f}")
    json.dump(out, open(ICI / "ro08_second_moteur.json", "w"), indent=1)
    print("ACCORD" if ecart_max < 1e-9 else "DÉSACCORD")


if __name__ == "__main__":
    main()
