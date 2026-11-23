#!/usr/bin/env python3
"""X-25, partie B -- les moteurs de l'auteur sont-ils compatibles avec << un lien est un contact entre constituants ronds qui ne se chevauchent pas >>, en dimension 3 ?
Conditions necessaires eprouvees sur les liens seuls (aucune position n'est utilisee) :
 (N1) aucun groupe de six constituants tous lies (au plus cinq boules deux a deux tangentes dans S^3) ;
 (N2) trois constituants tous lies ont au plus six voisins communs, et chacun de ces voisins est lie a au plus deux des autres (anneau) ;
 (N3) deux constituants lies : chaque voisin commun est lie a au plus six autres voisins communs (disques egaux dans un plan).
Etats : moteur complet de l'auteur (<< blob ablation labo colab.py >>, quatre forces, kappa = 6,6, graines 1 et 2, releves a 660 et 1 037 constituants : etats de
X-24 B, empreintes des liens controlees) ; moteur statique (<< blob engine.py >>, build_blob et temoin build_rgg, 800 constituants, graines 0 et 1 : etats de X-21).
Aucune ligne des sources de l'auteur n'est modifiee. Prediction scellee : x25_naissance_dans_la_cellule_prediction.txt
(SHA-256 fab572629dd8c725d1af724ebdf4168a2b73d4577bb0d8db6aabb6384908a709).     Claude, 23 novembre 2026."""
import hashlib, importlib.util, itertools, json, os, sys, time
import numpy as np
import x24_moteur_dimension as base

ICI = os.path.dirname(os.path.abspath(__file__))
EMPREINTES_X24 = {(1, 660): '3b85f7c1f30035fd', (1, 1037): 'c0e1a4275f32ff9d', (2, 660): 'c7f34aa111a149dc', (2, 1037): '3b663cb72881cbcf'}


def cliques_max(adj):
    """Bron-Kerbosch avec pivot ; rend le nombre de groupes complets maximaux par taille et la plus grande taille."""
    tailles = {}
    def bk(R, P, X):
        if not P and not X:
            tailles[len(R)] = tailles.get(len(R), 0) + 1; return
        u = max(P | X, key=lambda v: len(adj[v] & P))
        for v in list(P - adj[u]):
            bk(R | {v}, P & adj[v], X & adj[v]); P.remove(v); X.add(v)
    bk(set(), set(range(len(adj))), set())
    return tailles


def groupes_de_k(adj, k):
    """Nombre de groupes de k constituants tous lies (comptage direct par extension ordonnee)."""
    n = len(adj); total = 0
    def ext(cand, taille):
        nonlocal total
        if taille == k: total += 1; return
        for v in sorted(cand):
            ext({w for w in cand & adj[v] if w > v}, taille + 1)
    for u in range(n): ext({w for w in adj[u] if w > u}, 1)
    return total


def epreuve(nom, adj, extra=None):
    n = len(adj); t0 = time.time()
    liens = sum(len(a) for a in adj) // 2
    r = dict(etat=nom, constituants=n, liens=liens, voisins_moyens=2 * liens / n)
    if extra: r.update(extra)
    cm = cliques_max(adj); r['groupes_complets_maximaux_par_taille'] = {str(k): v for k, v in sorted(cm.items())}; r['plus_grand_groupe_complet'] = max(cm)
    for k in (4, 5, 6):
        r['groupes_de_%d' % k] = groupes_de_k(adj, k) if max(cm) <= 20 else None
    # (N2) triples tous lies
    tri = 0; plus6 = 0; clause2 = 0; ok2 = 0; hist = {}
    for u in range(n):
        for v in (x for x in adj[u] if x > u):
            for w in (x for x in adj[u] & adj[v] if x > v):
                tri += 1
                c = adj[u] & adj[v] & adj[w]; hist[len(c)] = hist.get(len(c), 0) + 1
                a = len(c) > 6
                b = any(len(adj[x] & c) > 2 for x in c)
                plus6 += a; clause2 += b; ok2 += (not a and not b)
    r['N2'] = dict(triples_tous_lies=tri, avec_plus_de_six_voisins_communs=plus6, avec_un_voisin_commun_lie_a_plus_de_deux_autres=clause2, satisfaisant_N2=ok2,
                   part_satisfaisant_N2=(ok2 / tri if tri else None), part_avec_plus_de_six=(plus6 / tri if tri else None),
                   voisins_communs_d_un_triple={str(k): v for k, v in sorted(hist.items())})
    # (N3) liens
    viol3 = 0; pire = 0
    for u in range(n):
        for v in (x for x in adj[u] if x > u):
            c = adj[u] & adj[v]
            m = max((len(adj[x] & c) for x in c), default=0); pire = max(pire, m); viol3 += m > 6
    r['N3'] = dict(liens=liens, liens_qui_violent_N3=viol3, part_qui_viole=viol3 / liens, plus_grand_nombre_de_voisins_communs_lies_a_un_meme_voisin_commun=pire)
    r['N1_violee'] = r['plus_grand_groupe_complet'] >= 6
    r['N2_violee'] = (plus6 + clause2) > 0
    r['N3_violee'] = viol3 > 0
    r['duree_s'] = round(time.time() - t0, 1)
    return r


def moteur_complet():
    out = []
    for graine in (1, 2):
        M, ech = base.moteur(3, 6.6)
        bl = M['Blob'](N0=300, seed=graine, forces=base.FORCES)
        tours = 0
        for cible in base.RELEVES:
            while bl.N < cible:
                bl.step(0.12); tours += 1
            liens = base.liens_de(bl)
            emp = hashlib.sha256(json.dumps(liens).encode()).hexdigest()
            adj = [set(a) for a in bl.adj[:bl.N]] if not isinstance(bl.adj, dict) else [set(bl.adj[i]) for i in range(bl.N)]
            r = epreuve('moteur complet, graine %d, %d constituants' % (graine, bl.N), adj,
                        dict(graine=graine, tours=tours, empreinte_des_liens=emp, empreinte_de_X24_retrouvee=emp.startswith(EMPREINTES_X24.get((graine, bl.N), '?'))))
            out.append(r); print(json.dumps(r), flush=True)
    return out


def moteur_statique():
    racine = os.path.join(ICI, '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
    spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(racine, 'blob engine.py')); be = importlib.util.module_from_spec(spec); spec.loader.exec_module(be)
    out = []
    for N, graine in ((800, 0), (800, 1)):
        for nom, fab in (('moteur statique (build_blob)', be.build_blob), ('temoin sans viabilite (build_rgg)', be.build_rgg)):
            pts, nbr, deg = fab(N, graine)
            adj = [set(int(x) for x in nbr[u, :deg[u]]) for u in range(N)]
            r = epreuve('%s, graine %d, %d constituants' % (nom, graine, N), adj, dict(graine=graine))
            out.append(r); print(json.dumps(r), flush=True)
    return out


if __name__ == '__main__':
    t0 = time.time()
    res = dict(moteur_complet=moteur_complet(), moteur_statique=moteur_statique())
    res['duree_s'] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(ICI, 'x25_moteurs_contact.json'), 'w'), indent=1)
    print('duree', res['duree_s'], 's')
