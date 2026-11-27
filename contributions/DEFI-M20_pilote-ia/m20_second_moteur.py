#!/usr/bin/env python3
"""DEFI-M20, volet « κ ≥ 8 » — seconde implémentation, sans code commun avec m20_kappa.py pour les mesures.

- Comptes par matrices creuses : t_v = ((A²)∘A)·1 / 2, voisins communs = (A²)_uv sur les arêtes.
- Gini par la différence absolue moyenne : G = Σ_ij |x_i − x_j| / (2 n² μ) (via tri et rangs, forme exacte).
- A10 par np.partition ; Z, C1, C2, C3 recalculés.
- Témoin RGG reconstruit sans le moteur (cKDTree.query_pairs, tri par longueur, |E| = round(N κ / 2))
  et comparé arête par arête au build_rgg du moteur.
Le graphe du Blob est régénéré par le moteur (déterministe à graine fixée) : la génération n'est pas
indépendante, seules les mesures le sont. Compare à m20_kappa.json sur N = 1 000 et 2 000.
"""
import importlib.util, json, pathlib, sys
import numpy as np, scipy.sparse as sp
from scipy.spatial import cKDTree

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI.parent.parent / "corpus" / "03_scripts" / "SCRIPTS DIVERS BLOB" / "blob engine.py"
spec = importlib.util.spec_from_file_location("blob_engine", MOTEUR)
be = importlib.util.module_from_spec(spec); sys.modules["blob_engine"] = be; spec.loader.exec_module(be)


def mat_de(nbr, deg, N):
    r = np.repeat(np.arange(N), deg); c = np.concatenate([nbr[u, :deg[u]] for u in range(N)])
    return sp.csr_matrix((np.ones(len(r), np.int64), (r, c)), shape=(N, N))


def mesures(A, coeur=None):
    N = A.shape[0]
    d = np.asarray(A.sum(1)).ravel()
    M = (A @ A).multiply(A).tocsr()
    t = np.asarray(M.sum(1)).ravel() // 2
    U = sp.triu(A, 1).tocoo(); E = U.nnz
    cu = np.asarray(M[U.row, U.col]).ravel()          # voisins communs par arête (0 inclus)
    bad_e = cu < 3
    se = np.zeros(N, bool); se[U.row[bad_e]] = True; se[U.col[bad_e]] = True
    x = np.sort(t.astype(float)); n = len(x); i = np.arange(n)
    G = float(np.sum((2 * i - n + 1) * x) / (n * n * x.mean())) if x.sum() else 0.0   # = Σ|xi-xj|/(2n²μ)
    k = max(1, N // 10)
    A10 = float(np.partition(t, N - k)[N - k:].sum() / t.sum())
    V = float(((d < 4) | (t < 3 * d - 6) | se).mean())
    bad = (d < 4) | (t < 3 * d - 6) | se
    Vc = float(bad[coeur].mean()) if coeur is not None else None
    return dict(V_coeur=Vc, n_coeur=int(coeur.sum()) if coeur is not None else None, V=V, C1=float((d < 4).mean()), C2=float((t < 3 * d - 6).mean()),
                C3_aretes=float(bad_e.mean()), G=G, A10=A10, Z=float((t == 0).mean()), E=E)


def rgg_propre(N, s, kap, pf=1.6):
    pts = np.random.default_rng(s).random((N, 3))
    r = (kap / ((N - 1) * (4 / 3) * np.pi)) ** (1 / 3)
    P = np.array(sorted(cKDTree(pts).query_pairs(pf * r)))
    L = np.linalg.norm(pts[P[:, 0]] - pts[P[:, 1]], axis=1)
    P = P[np.argsort(L, kind="stable")][:int(round(N * kap / 2))]
    A = sp.coo_matrix((np.ones(len(P), np.int64), (P[:, 0], P[:, 1])), shape=(N, N))
    return (A + A.T).tocsr()


def main():
    ref = {(r["modele"], r["kappa"], r["N"], r["graine"]): r for r in json.load(open(ICI / "m20_kappa.json"))}
    ecart = 0.0; n = 0; aretes_ok = True; out = []
    for kap in (6.6, 8.0, 10.0, 12.0, 14.0):
        for N in (1000, 2000):
            for s in range(4):
                pts, nbr, deg = be.build_blob(N, seed=s, kappa=kap)
                r0 = (kap / ((N - 1) * (4 / 3) * np.pi)) ** (1 / 3)   # supplément hors critère : cœur à 2 r des faces
                co = np.all((pts > 2 * r0) & (pts < 1 - 2 * r0), axis=1)
                b = mesures(mat_de(nbr, deg, N), co)
                _, nbr, deg = be.build_rgg(N, seed=s, kappa=kap)
                Am = mat_de(nbr, deg, N); Ap = rgg_propre(N, s, kap)
                same = (Am != Ap).nnz == 0; aretes_ok &= same
                g = mesures(Ap, co)
                for mod, m in (("blob", b), ("rgg", g)):
                    r = ref[(mod, kap, N, s)]
                    for q in ("V", "C1", "C2", "C3_aretes", "G", "A10", "Z"):
                        ecart = max(ecart, abs(m[q] - r[q])); n += 1
                out.append(dict(kappa=kap, N=N, graine=s, blob=b, rgg=g, rgg_aretes_identiques=bool(same)))
                print(f"κ={kap} N={N} s={s} blob G={b['G']:.4f} A10={b['A10']:.4f} V={b['V']:.4f} Vcoeur={b['V_coeur']:.3f} (n={b['n_coeur']}) | "
                      f"rgg G={g['G']:.4f} Vcoeur={g['V_coeur']:.3f} arêtes identiques={same}", flush=True)
    json.dump(out, open(ICI / "m20_second_moteur.json", "w"), indent=1)
    print(f"{n} comparaisons, écart maximal {ecart:.2e} ; RGG reconstruit identique : {aretes_ok}")
    print("ACCORD" if ecart < 1e-9 and aretes_ok else "DÉSACCORD")


if __name__ == "__main__":
    main()
