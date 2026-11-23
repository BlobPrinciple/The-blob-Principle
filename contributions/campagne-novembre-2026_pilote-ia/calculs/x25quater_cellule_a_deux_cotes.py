#!/usr/bin/env python3
"""X-25 quater -- deux conditions necessaires de plus pour << lien = contact de constituants ronds >> en dimension 3, sur les liens seuls :
 (N4) un groupe de quatre constituants tous lies a au plus deux voisins communs (une cellule a deux cotes) ;
 (N7) a et b lies, x et y deux de leurs voisins communs : au plus deux constituants lies a la fois a a, b, x et y.
Etats : les quatre etats de reference du moteur complet (X-24 B), puis, a titre de temoin, les etats << sans la regle >> et le moteur statique.
Prediction scellee : x25quater_cellule_a_deux_cotes_prediction.txt (SHA-256 d18deb259740972243894ec2a1a3eb4fcbfc97fc24bcd106254a493ea11734a7).     Claude, 23 novembre 2026."""
import hashlib, importlib.util, itertools, json, os, time
import x24_moteur_dimension as base
import x24bis_groupe_qui_se_defait as bis

ICI = os.path.dirname(os.path.abspath(__file__))


def conditions(adj):
    n = len(adj); k4 = 0; n4 = 0; pire4 = 0; quad = 0; n7 = 0; pire7 = 0
    for u in range(n):
        for v in (x for x in adj[u] if x > u):
            cuv = adj[u] & adj[v]
            for w in (x for x in cuv if x > v):
                for z in (x for x in cuv & adj[w] if x > w):
                    k4 += 1; c = len(adj[u] & adj[v] & adj[w] & adj[z]); pire4 = max(pire4, c); n4 += c > 2
            for x, y in itertools.combinations(sorted(cuv), 2):
                quad += 1; c = len(cuv & adj[x] & adj[y]); pire7 = max(pire7, c); n7 += c > 2
    return dict(groupes_de_quatre=k4, N4_groupes_de_quatre_a_plus_de_deux_voisins_communs=n4, N4_pire=pire4, N7_quadruplets_eprouves=quad, N7_violations=n7, N7_pire=pire7,
                N4_violee=n4 > 0, N7_violee=n7 > 0)


if __name__ == '__main__':
    t0 = time.time(); out = []
    for nom, groupe, forces in (("moteur complet, regle de l'auteur, quatre forces", 4, bis.QUATRE_FORCES), ("temoin : sans la regle (taux nul), quatre forces", 0, bis.QUATRE_FORCES)):
        for graine in (1, 2):
            M = bis.moteur(groupe, 6.6, 3); bl = M['Blob'](N0=300, seed=graine, forces=forces)
            for cible in base.RELEVES:
                while bl.N < cible: bl.step(0.12)
                liens = base.liens_de(bl); adj = [set(bl.adj[i]) for i in range(bl.N)]
                r = dict(etat='%s, graine %d, %d constituants' % (nom, graine, bl.N), empreinte_des_liens=hashlib.sha256(json.dumps(liens).encode()).hexdigest(), **conditions(adj))
                out.append(r); print(json.dumps(r), flush=True)
    racine = os.path.join(ICI, '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
    spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(racine, 'blob engine.py')); be = importlib.util.module_from_spec(spec); spec.loader.exec_module(be)
    for graine in (0, 1):
        pts, nbr, deg = be.build_blob(800, graine); adj = [set(int(x) for x in nbr[u, :deg[u]]) for u in range(800)]
        r = dict(etat='temoin : moteur statique, graine %d, 800 constituants' % graine, **conditions(adj)); out.append(r); print(json.dumps(r), flush=True)
    json.dump(dict(etats=out, duree_s=round(time.time() - t0, 1)), open(os.path.join(ICI, 'x25quater_cellule_a_deux_cotes.json'), 'w'), indent=1)
    print('duree', round(time.time() - t0, 1), 's')
