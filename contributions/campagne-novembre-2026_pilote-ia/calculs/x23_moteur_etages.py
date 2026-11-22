#!/usr/bin/env python3
"""X-23, partie B -- l'ascenseur de rigidite dans le moteur de l'auteur (blob engine.py, importe sans modification).
Pour le Blob (build_blob), son terreau (build_rgg) et le temoin aleatoire (build_er), a kappa = 4 ; 5 ; 6 ; 6,6 ; 7 ; 8 ; 9 ; 10 :
a chaque etage d = 1 ... 5, mecanismes, auto-contraintes, plus grand amas rigide, part des constituants figes (dans un amas rigide d'au moins d+1 constituants).
Positions tirees au hasard dans R^d (aucune dimension posee) ; pour d = 3, aussi les positions reelles du moteur.
Prediction scellee : x23_regle_de_l_etage_prediction.txt (SHA-256 7c80008d46d64a9776a1a4c092cfb80c0e6bd1b83f9480f02ae7d266f00bb5a1). Claude, 22 novembre 2026."""
import importlib.util, json, os, sys, tempfile, time
os.environ.setdefault('NUMBA_CACHE_DIR', tempfile.mkdtemp(prefix='numba_x23_'))   # le cache de compilation ne doit pas etre ecrit dans le corpus
import numpy as np, networkx as nx
from scipy.stats import spearmanr
from x23_outils import analyse_exacte, positions_reelles_exactes, matrice_de_rigidite

ici = os.path.dirname(os.path.abspath(__file__))
base = os.path.join(ici, '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(base, 'blob engine.py'))
be = importlib.util.module_from_spec(spec)
sys.modules['blob_engine'] = be
spec.loader.exec_module(be)

KAPPAS = (6.6, 6, 7, 8, 5, 10, 4, 9)
ETAGES = (2, 3, 4, 5)
ID = {'blob': 1, 'rgg': 2, 'er': 3}


def liens_du_moteur(nbr, deg, N):
    s = set()
    for u in range(N):
        for v in nbr[u, :deg[u]]:
            v = int(v)
            if v != u:
                s.add((min(u, v), max(u, v)))
    return sorted(s)


def un_cas(modele, N, graine, kappa, etages=ETAGES):
    fab = {'blob': be.build_blob, 'rgg': be.build_rgg, 'er': be.build_er}[modele]
    pts, nbr, deg = fab(N, graine, kappa=kappa)
    liens = liens_du_moteur(nbr, deg, N)
    E = len(liens)
    G = nx.Graph(); G.add_nodes_from(range(N)); G.add_edges_from(liens)
    comps = [len(c) for c in nx.connected_components(G)]
    haut = np.zeros(N, int)
    for c in nx.find_cliques(G):
        for x in c:
            haut[x] = max(haut[x], len(c) - 1)
    r = dict(modele=modele, N=N, graine=graine, kappa=kappa, liens=E, liens_par_constituant=E / N, triangles_par_constituant=be._n_tri(nbr, deg, N) / N,
             part_par_cliques={str(k): float((haut >= k).mean()) for k in (1, 2, 3, 4, 5)}, plus_haut_etage_par_cliques=int(haut.max()))
    r['etage1'] = dict(mecanismes=len(comps) - 1, auto_contraintes=E - N + len(comps), part_plus_grand_amas=max(comps) / N, part_figee=float((np.array([G.degree(u) for u in range(N)]) >= 1).mean()))
    tpv = np.asarray(be._tpv(nbr, deg, N), float)
    for d in etages:
        t0 = time.time()
        rng = np.random.default_rng([graine, int(round(kappa * 10)), ID[modele], d, N])
        a = analyse_exacte(N, liens, d, rng)                       # positions entieres tirees au hasard, arithmetique exacte : aucun seuil
        ligne = {k: v for k, v in a.items() if not k.startswith('_')}
        ligne['maxwell_mecanismes_moins_auto_contraintes'] = d * N - d * (d + 1) // 2 - E
        ligne['part_par_cliques'] = float((haut >= d).mean())
        if d == 3 and pts is not None:
            pts = np.asarray(pts, float)
            b = analyse_exacte(N, liens, 3, rng, pos=positions_reelles_exactes(pts))   # rang exact AUX positions reelles du moteur
            ligne['positions_reelles'] = dict(mecanismes=b['mecanismes'], auto_contraintes=b['auto_contraintes'], part_plus_grand_amas=b['part_plus_grand_amas'],
                                              part_figee=b['part_figee'], memes_amas=bool((b['_meilleur'] == a['_meilleur']).all()))
            # poids : part redondante de chaque lien (levier), en virgule flottante sur les positions reelles, coupee au rang exact
            R = matrice_de_rigidite(N, liens, pts)
            Ug, sv, Vt = np.linalg.svd(R, full_matrices=False)
            rg = b['rang']
            red = 1.0 - (Ug[:, :rg] ** 2).sum(1)
            lib = 3.0 - (Vt[:rg].T.reshape(N, 3, rg) ** 2).sum(axis=(1, 2))
            poids = np.zeros(N)
            for (u, v), x in zip(liens, red):
                poids[u] += x / 2; poids[v] += x / 2
            ordre = np.argsort(-poids)
            ligne['poids'] = dict(somme=float(poids.sum()), valeurs_singulieres_autour_de_la_coupe=[float(sv[rg - 1] / sv[0]), float(sv[rg] / sv[0]) if rg < len(sv) else None],
                                  correlation_de_rangs_avec_la_masse_du_corpus=float(spearmanr(poids, tpv).statistic),
                                  part_portee_par_les_10pc_les_plus_charges=float(poids[ordre[:N // 10]].sum() / max(poids.sum(), 1e-300)),
                                  correlation_de_rangs_poids_liberte=float(spearmanr(poids, lib).statistic),
                                  part_des_liens_sans_redondance=float((red < 1e-6).mean()), part_des_liens_redondants_a_plus_de_90pc=float((red > 0.9).mean()),
                                  part_des_constituants_sans_poids=float((poids < 1e-6).mean()))
        ligne['duree_s'] = round(time.time() - t0, 1)
        r[f'etage{d}'] = ligne
    return r


if __name__ == '__main__':
    quoi = sys.argv[1] if len(sys.argv) > 1 else 'tout'
    fichier = os.path.join(ici, 'x23_moteur_etages.json' if quoi == 'tout' else f'x23_moteur_etages_{quoi}.json')
    out = []
    if quoi == 'essai':
        plan = [('blob', 800, 0, 6.6, ETAGES)]
    elif quoi == 'grand':
        plan = [(m, 1600, 0, 6.6, (2, 3, 4)) for m in ('blob', 'rgg')]
    else:
        plan = []
        for kappa in KAPPAS:
            for graine in (0, 1):
                for m in ('blob', 'rgg') + (('er',) if graine == 0 else ()):
                    plan.append((m, 800, graine, kappa, ETAGES))
    for m, N, g, kappa, etages in plan:
        t0 = time.time()
        r = un_cas(m, N, g, kappa, etages)
        r['duree_s'] = round(time.time() - t0, 1)
        out.append(r)
        print(json.dumps(r), flush=True)
        json.dump(out, open(fichier, 'w'), indent=1)
