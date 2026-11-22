#!/usr/bin/env python3
"""X-24 quater -- une naissance change-t-elle la forme par contacts partout, ou seulement pres d'elle ?
Coque reguliere nee par mitose synchrone (analogue a deux dimensions de C-116) : tetraedre creux, deux naissances (octaedre), puis g paliers ou chaque cellule
se divise une fois par le lien oppose a son porteur le plus recent : 8 x 2^g cellules, 4 x 2^g + 2 constituants.
Invariant local d'un lien (p, q) : J = - <u_x, u_y>, x et y etant les deux constituants qui font face au lien (invariant de Mobius).
On compare J avant et apres une naissance de plus, lien par lien, selon la distance (en liens) au lien divise.
Prediction scellee : x24quater_localite_d_une_naissance_prediction.txt (SHA-256 9da00ca928a3a531b3da531775f1fd837ab55f95bdb827e05d81f8e6748f580a).
Usage : python3 x24quater_localite_d_une_naissance.py [essai]     Claude, 22 novembre 2026."""
import json, os, sys, time
from collections import deque
import numpy as np
from x23_outils import liens_des_cellules
from x23_coques import mitose_arete, est_fermee
from x24_contacts import oriente, rayons, disposition

ICI = os.path.dirname(os.path.abspath(__file__))


def coque_reguliere(g):
    """Octaedre (ne du tetraedre creux par deux mitoses), puis g paliers de division synchrone. Renvoie (constituants, cellules)."""
    eq = [2, 3, 4, 5]
    tri = []                                   # (v0, v1, v2) : lien de division (v0, v1), porteur le plus recent v2
    for i in range(4):
        a, b = eq[i], eq[(i + 1) % 4]
        tri.append((a, b, 0)); tri.append((a, b, 1))
    n = 6
    for palier in range(g):
        milieu = {}; usage = {}; nouv = []
        for v0, v1, v2 in tri:
            e = (min(v0, v1), max(v0, v1))
            if e not in milieu:
                milieu[e] = n; n += 1
            usage[e] = usage.get(e, 0) + 1
            m = milieu[e]
            nouv.append((v2, v0, m)); nouv.append((v1, v2, m))
        assert all(c == 2 for c in usage.values()), 'un lien de division n est pas partage par deux cellules exactement'
        tri = nouv
    cellules = [frozenset(t) for t in tri]
    assert est_fermee(cellules, 2) and len(cellules) == 8 * 2 ** g and n == 4 * 2 ** g + 2
    return n, cellules


def forme(n, cellules, ext):
    """Empilement de cercles (flottant) ; renvoie rayons, centres et residu de tangence relatif."""
    F = oriente([tuple(sorted(c)) for c in cellules])
    ext_o = next(f for f in F if set(f) == set(ext))
    r, it = rayons(n, F, ext_o)
    P = np.array(disposition(n, F, ext_o, r))
    liens = liens_des_cellules(cellules)
    tang = max(abs(abs(P[i] - P[j]) - (r[i] + r[j])) / (r[i] + r[j]) for i, j in liens)
    return r, P, float(tang), liens


def invariants(cellules, r, P):
    """Pour chaque lien, J = - <u_x, u_y> des deux constituants qui lui font face."""
    face = {}
    for c in cellules:
        c = sorted(c)
        for a, b, x in ((c[0], c[1], c[2]), (c[0], c[2], c[1]), (c[1], c[2], c[0])):
            face.setdefault((a, b), []).append(x)
    J = {}
    for e, xs in face.items():
        x, y = xs
        J[e] = (-(r[x] ** 2 + r[y] ** 2 - abs(P[x] - P[y]) ** 2) / (2 * r[x] * r[y]), tuple(sorted(xs)))
    return J


def distances(n, liens, sources):
    vois = [[] for _ in range(n)]
    for a, b in liens:
        vois[a].append(b); vois[b].append(a)
    d = -np.ones(n, dtype=int); file = deque()
    for s in sources:
        d[s] = 0; file.append(s)
    while file:
        u = file.popleft()
        for v in vois[u]:
            if d[v] < 0:
                d[v] = d[u] + 1; file.append(v)
    return d


def epreuve(g, nb_naissances, graine):
    n, cellules = coque_reguliere(g)
    liens = liens_des_cellules(cellules)
    ext = tuple(sorted(next(c for c in cellules if 1 in c)))          # face exterieure du calcul : une cellule au pole sud
    d_ext = distances(n, liens, ext)
    r0, P0, tang0, _ = forme(n, cellules, ext)
    J0 = invariants(cellules, r0, P0)
    rng = np.random.default_rng([24, 4, g, graine])
    loin = [e for e in liens if min(d_ext[e[0]], d_ext[e[1]]) >= 0.6 * d_ext.max()]
    out = dict(g=g, constituants=n, cellules=len(cellules), residu_de_tangence_avant=tang0, diametre_depuis_la_face_exterieure=int(d_ext.max()), naissances=[])
    for essai in range(nb_naissances):
        a, b = loin[int(rng.integers(len(loin)))]
        cel1 = mitose_arete(cellules, a, b, n)
        r1, P1, tang1, _ = forme(n + 1, cel1, ext)
        J1 = invariants(cel1, r1, P1)
        dist = distances(n, liens, (a, b))
        par_d = {}
        for e, (j0, opp0) in J0.items():
            if e in J1 and J1[e][1] == opp0:                      # meme entourage avant et apres
                d = int(min(dist[e[0]], dist[e[1]]))
                par_d.setdefault(d, []).append(abs(J1[e][0] - j0) / j0)
        lignes = []
        for d in sorted(par_d):
            v = np.array(par_d[d])
            lignes.append(dict(d=d, liens=len(v), mediane=float(np.median(v)), minimum=float(v.min()), maximum=float(v.max())))
        # ajustements de d = 2 a d = 12 (ou la distance maximale)
        sel = [l for l in lignes if 2 <= l['d'] <= 12 and l['mediane'] > 0]
        x = np.array([l['d'] for l in sel], float); y = np.log(np.array([l['mediane'] for l in sel]))
        ajust = {}
        if len(sel) >= 4:
            p1 = np.polyfit(np.log(x), y, 1); res1 = float(np.sqrt(np.mean((np.polyval(p1, np.log(x)) - y) ** 2)))
            p2 = np.polyfit(x, y, 1); res2 = float(np.sqrt(np.mean((np.polyval(p2, x) - y) ** 2)))
            ajust = dict(exposant_loi_de_puissance=float(-p1[0]), residu_log_log=res1, taux_exponentiel_par_lien=float(-p2[0]), residu_semi_log=res2)
        ligne = dict(lien_divise=[int(a), int(b)], distance_a_la_face_exterieure=int(min(d_ext[a], d_ext[b])), residu_de_tangence_apres=tang1, par_distance=lignes, ajustements=ajust)
        out['naissances'].append(ligne)
        print(json.dumps(dict(g=g, lien=[int(a), int(b)], residus=[tang0, tang1], ajustements=ajust)), flush=True)
        for l in lignes:
            print('   d = %2d | %4d liens | mediane %.3e | min %.3e | max %.3e' % (l['d'], l['liens'], l['mediane'], l['minimum'], l['maximum']), flush=True)
    return out


def bruit(g):
    """Ajout apres execution, declare : niveau de bruit du calcul. La meme coque, sans naissance de plus, calculee depuis deux faces exterieures differentes :
    l'ecart relatif des invariants J, qui devrait etre nul, mesure l'erreur d'arrondi, rangee par distance a la premiere face exterieure."""
    n, cellules = coque_reguliere(g)
    liens = liens_des_cellules(cellules)
    ext1 = tuple(sorted(next(c for c in cellules if 1 in c))); ext2 = tuple(sorted(next(c for c in cellules if 0 in c)))
    r1, P1, t1, _ = forme(n, cellules, ext1); r2, P2, t2, _ = forme(n, cellules, ext2)
    J1 = invariants(cellules, r1, P1); J2 = invariants(cellules, r2, P2)
    d_ext = distances(n, liens, ext1)
    par = {}
    for e in J1:
        par.setdefault(int(min(d_ext[e[0]], d_ext[e[1]])), []).append(abs(J1[e][0] - J2[e][0]) / J1[e][0])
    lignes = [dict(distance_a_la_face_exterieure=d, liens=len(v), mediane=float(np.median(v)), maximum=float(np.max(v))) for d, v in sorted(par.items())]
    tous = np.concatenate([np.array(v) for v in par.values()])
    res = dict(g=g, constituants=n, residus_de_tangence=[t1, t2], bruit_median=float(np.median(tous)), bruit_au_95e_centile=float(np.percentile(tous, 95)), bruit_maximal=float(tous.max()), par_distance=lignes)
    print(json.dumps({k: v for k, v in res.items() if k != 'par_distance'}))
    for l in lignes:
        print('   distance a la face exterieure %2d | %4d liens | mediane %.2e | max %.2e' % (l['distance_a_la_face_exterieure'], l['liens'], l['mediane'], l['maximum']))
    return res


if __name__ == '__main__':
    essai = len(sys.argv) > 1 and sys.argv[1] == 'essai'
    t0 = time.time()
    if len(sys.argv) > 1 and sys.argv[1] == 'bruit':
        json.dump([bruit(6), bruit(8)], open(os.path.join(ICI, 'x24quater_bruit.json'), 'w'), indent=1); sys.exit(0)
    if essai:                                   # mise au point : la coque et sa forme seulement, aucune naissance de plus
        for g in (2, 4):
            n, cellules = coque_reguliere(g)
            ext = tuple(sorted(next(c for c in cellules if 1 in c)))
            r, P, tang, liens = forme(n, cellules, ext)
            print('g', g, 'constituants', n, 'cellules', len(cellules), 'residu de tangence', tang, 'rapport des rayons', float(r.max() / r.min()))
        sys.exit(0)
    sortie = [epreuve(6, 3, 0), epreuve(8, 3, 0)]
    json.dump(dict(epreuves=sortie, duree_s=round(time.time() - t0, 1)), open(os.path.join(ICI, 'x24quater_localite_d_une_naissance.json'), 'w'), indent=1)
    print('duree', round(time.time() - t0, 1), 's')
