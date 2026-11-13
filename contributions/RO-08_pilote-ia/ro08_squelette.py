#!/usr/bin/env python3
"""RO-08 — le graphe du Blob peut-il être le 1-squelette d'une 3-variété fermée ?

Contribution du pilote IA du laboratoire (Claude, Anthropic), 13 novembre 2026.

Question. Le master V346 (CXL.2.4, p. 1195 imprimée) établit que le complexe de cliques
du Blob n'est pas une 3-pseudovariété. Cela ne dit rien d'un autre choix de faces :
pourrait-on garder les sommets et les arêtes du Blob et choisir d'autres triangles et
tétraèdres pour obtenir une triangulation fermée (voie la plus économe vers B) ?

Conditions nécessaires [T] (toute triangulation d'une 3-variété fermée, faces quelconques) :
  (C1) deg(v) >= 4 ;
  (C2) le link de v est une 2-sphère triangulée sur ses deg(v) voisins, donc possède
       3 deg(v) - 6 arêtes, toutes arêtes du graphe entre voisins de v :
       t_v := #arêtes entre voisins de v (= triangles du graphe en v) >= 3 deg(v) - 6 ;
  (C3) le link d'une arête uv est un cycle de longueur >= 3 formé de voisins communs :
       c_uv := #voisins communs >= 3.
  (Glob) somme de (C2) : n_tri / N >= kappa - 2 (kappa = degré moyen).
Une seule violation suffit à exclure toute triangulation fermée de 1-squelette G.
Pour une triangulation de drapeau (faces = cliques), (C2) devient l'égalité t_v = 3 deg(v) - 6
et (C1) deg(v) >= 6.

Protocole (fixé avant exécution) :
- moteur canonique corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py importé tel quel
  (kappa 6,6 ; beta 0,30 ; tau 0,50 ; pool_fac 1,6 ; therm_fac 120) ;
- N = 500, 1000, 2000, 4000 ; graines 0 à 3 ; témoins RGG (même |E|, sans viabilité) et ER ;
- contrôle positif : germe de Freudenthal–Kuhn de T^3 (L = 4, 5) : zéro violation attendue ;
- comptes pour tous les sommets et pour le « cœur » (sommets à plus de 2 r des faces du cube,
  pour écarter l'effet du bord du cube, V346 CXL.8) ;
- relaxation longue (therm_fac x 4) à N = 1000 pour la robustesse.
Implémentation : ensembles Python (indépendante de _tpv du moteur et du second script).
"""
import importlib.util, json, pathlib, sys, time, itertools
import numpy as np

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI.parent.parent / "corpus" / "03_scripts" / "SCRIPTS DIVERS BLOB" / "blob engine.py"
spec = importlib.util.spec_from_file_location("blob_engine", MOTEUR)
be = importlib.util.module_from_spec(spec); sys.modules["blob_engine"] = be; spec.loader.exec_module(be)


def adjacence(nbr, deg, N):
    return [set(int(x) for x in nbr[u, :deg[u]]) for u in range(N)]


def freudenthal(L):
    """Germe de Freudenthal–Kuhn de T^3 : x ~ y ssi y - x (mod L) est un vecteur 0/1 non nul ou son opposé."""
    idx = lambda a, b, c: ((a % L) * L + (b % L)) * L + (c % L)
    N = L ** 3; adj = [set() for _ in range(N)]
    dirs = [d for d in itertools.product((0, 1), repeat=3) if any(d)]
    for a, b, c in itertools.product(range(L), repeat=3):
        u = idx(a, b, c)
        for d in dirs:
            v = idx(a + d[0], b + d[1], c + d[2]); adj[u].add(v); adj[v].add(u)
    return adj


def bilan(adj, coeur=None):
    N = len(adj)
    d = np.array([len(a) for a in adj])
    t = np.array([sum(len(adj[a] & s) for a in s) // 2 for s in adj])
    c1 = d < 4
    c2 = t < 3 * d - 6
    drap = t != 3 * d - 6
    viol_e = 0; E = 0; sommet_e = np.zeros(N, bool)
    for u in range(N):
        for v in adj[u]:
            if v > u:
                E += 1
                if len(adj[u] & adj[v]) < 3:
                    viol_e += 1; sommet_e[u] = sommet_e[v] = True
    ntri = int(t.sum()) // 3
    bad = c1 | c2 | sommet_e
    out = {"N": N, "E": E, "kappa": 2 * E / N, "ntri_par_N": ntri / N,
           "seuil_global": 2 * E / N - 2, "global_ok": bool(ntri / N >= 2 * E / N - 2),
           "frac_C1": float(c1.mean()), "frac_C2": float(c2.mean()),
           "frac_aretes_C3": viol_e / E, "frac_sommets_viol": float(bad.mean()),
           "nb_sommets_viol": int(bad.sum()), "frac_drapeau_egalite_fausse": float(drap.mean()),
           "frac_deg_lt6": float((d < 6).mean()),
           "deficit_C2_total": int(np.maximum(0, 3 * d - 6 - t).sum())}
    if coeur is not None:
        out["coeur_n"] = int(coeur.sum())
        out["coeur_frac_sommets_viol"] = float(bad[coeur].mean())
        out["coeur_frac_C2"] = float(c2[coeur].mean())
        out["coeur_frac_C1"] = float(c1[coeur].mean())
    return out


def coeur_de(pts, N):
    r = (be.KAPPA / ((N - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    m = 2 * r
    return np.all((pts > m) & (pts < 1 - m), axis=1)


def main():
    res = {"controle_positif": {}, "blob": [], "rgg": [], "er": [], "blob_long": []}
    for L in (4, 5):
        res["controle_positif"][f"L{L}"] = bilan(freudenthal(L))
        print("Freudenthal", L, res["controle_positif"][f"L{L}"], flush=True)
    for N in (500, 1000, 2000, 4000):
        for s in range(4):
            t0 = time.time()
            pts, nbr, deg = be.build_blob(N, seed=s)
            co = coeur_de(pts, N)
            b = bilan(adjacence(nbr, deg, N), co); b["graine"] = s; res["blob"].append(b)
            pts, nbr, deg = be.build_rgg(N, seed=s)
            g = bilan(adjacence(nbr, deg, N), co); g["graine"] = s; res["rgg"].append(g)
            _, nbr, deg = be.build_er(N, seed=s)
            e = bilan(adjacence(nbr, deg, N)); e["graine"] = s; res["er"].append(e)
            print(f"N={N} s={s} ({time.time()-t0:.0f}s) BLOB viol={b['frac_sommets_viol']:.3f} "
                  f"coeur={b['coeur_frac_sommets_viol']:.3f} C2={b['frac_C2']:.3f} C3e={b['frac_aretes_C3']:.3f} "
                  f"ntri/N={b['ntri_par_N']:.2f}>= {b['seuil_global']:.2f} | RGG viol={g['frac_sommets_viol']:.3f} "
                  f"ntri/N={g['ntri_par_N']:.2f} | ER viol={e['frac_sommets_viol']:.3f}", flush=True)
            json.dump(res, open(ICI / "ro08_squelette.json", "w"), indent=1)
    for s in range(2):
        pts, nbr, deg = be.build_blob(1000, seed=s, therm_fac=4 * be.THERM_FAC)
        b = bilan(adjacence(nbr, deg, 1000), coeur_de(pts, 1000)); b["graine"] = s; b["therm_fac"] = 4 * be.THERM_FAC
        res["blob_long"].append(b); print("long", b, flush=True)
    json.dump(res, open(ICI / "ro08_squelette.json", "w"), indent=1)


if __name__ == "__main__":
    main()
