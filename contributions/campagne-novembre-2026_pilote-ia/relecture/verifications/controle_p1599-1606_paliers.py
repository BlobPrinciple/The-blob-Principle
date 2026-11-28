#!/usr/bin/env python3
"""Contrôle des pages 1598 à 1606 de V346 (Tomes V314 et V315) : dimension spectrale par degré de forme,
croisements deux à deux (« soudures »), ordre par i + j.

Implémentation indépendante : les sources des tomes de juillet ne sont pas au dépôt.
  - nuage de N points sur le tore T^3 = [0,1)^3 ; triangulation de Delaunay périodique (27 copies) ;
  - étoile de Hodge circumcentrique (dual de Voronoï) :
        *0 = volume de la cellule de Voronoï,   *1 = aire de la face duale / longueur de l'arête,
        *2 = longueur de l'arête duale / aire,  *3 = 1 / volume du tétraèdre ;
  - opérateurs de passage D_k = *_(k+1)^(1/2) d_k *_k^(-1/2) ; S_k = spectre non nul de D_k^T D_k.
Fait d'algèbre utilisé (décomposition de Hodge) : le spectre non nul du laplacien des k-formes est la
réunion S_(k-1) u S_k. Les quatre courbes par degré sont donc faites de trois spectres « de passage ».

Pourquoi l'ordre des croisements est forcé (3D). Notons Z_j(t) la trace de la chaleur du spectre de passage S_j
et e_j(t) sa valeur propre moyenne sous le poids de la chaleur. Aux nombres de Betti près :
    E_0 = e_0 ;  E_1 = moyenne pondérée de e_0 et e_1 ;  E_2 = moyenne pondérée de e_1 et e_2 ;  E_3 = e_2,
et la dimension spectrale du degré k vaut 2 t E_k. Si l'ordre passe de e_0 < e_1 < e_2 (ultraviolet) à
e_0 > e_1 > e_2 (infrarouge), avec e_0 = e_1 en t_a puis e_1 = e_2 en t_b > t_a, alors par valeurs intermédiaires :
    (0,1) en t_a  <  (0,2)  <  { (1,2), (0,3) }  <  (1,3)  <  (2,3) en t_b,
c'est-à-dire l'ordre par i + j ; si t_b < t_a, l'ordre exactement inverse. Le coefficient de Spearman avec i + j
vaut donc +0,9856 ou -0,9856 par construction. Seuls sont libres : l'existence de l'inversion, le signe, et l'écart
entre t_a et t_b (l'ouverture de l'escalier).

Usage : python3 -I -u controle_p1599-1606_paliers.py poisson|grille|grand
Sorties : controle_p1599-1606_paliers_poisson.out, _grille.out, _grand.out
"""
import itertools
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.optimize import brentq
from scipy.spatial import Delaunay
from scipy.stats import spearmanr

DECAL = np.array(list(itertools.product((-1.0, 0.0, 1.0), repeat=3)))


def circumcentres(x):
    a = 2.0 * (x[:, 1:, :] - x[:, 0:1, :])
    b = (x[:, 1:, :] ** 2).sum(2) - (x[:, 0:1, :] ** 2).sum(2)
    return np.linalg.solve(a, b[..., None])[..., 0]


def construire(p):
    """Complexe périodique et étoiles de Hodge. Retourne un dictionnaire de contrôles et les spectres de passage."""
    n = len(p)
    q = (p[None, :, :] + DECAL[:, None, :]).reshape(-1, 3)
    base = np.tile(np.arange(n), 27)
    tri = Delaunay(q)
    s, voisins = tri.simplices, tri.neighbors
    x = q[s]
    g = x.mean(1)
    proche = np.all((g > -0.6) & (g < 1.6), axis=1)
    cc = np.full((len(s), 3), np.nan)
    cc[proche] = circumcentres(x[proche])
    dans = np.nonzero(np.all((g >= 0.0) & (g < 1.0), axis=1))[0]

    autour = {}
    for i in np.nonzero(proche)[0]:
        v = s[i]
        for a in range(4):
            for b in range(a + 1, 4):
                cle = (v[a], v[b]) if v[a] < v[b] else (v[b], v[a])
                autour.setdefault(cle, []).append(i)

    tets, vol = [], []
    aretes, faces = {}, {}
    conflits = 0
    for i in dans:
        v = s[i]
        bv = base[v]
        if len(set(bv)) < 4:
            conflits += 1
        tets.append(tuple(sorted(bv)))
        vol.append(abs(np.linalg.det(q[v[1:]] - q[v[0]])) / 6.0)
        for a in range(4):
            for b in range(a + 1, 4):
                va, vb = (v[a], v[b]) if base[v[a]] < base[v[b]] else (v[b], v[a])
                cle = (base[va], base[vb])
                dep = q[vb] - q[va]
                if cle in aretes:
                    if np.abs(aretes[cle][2] - dep).max() > 1e-9:
                        conflits += 1
                    continue
                liste = autour[(va, vb) if va < vb else (vb, va)]
                c = cc[liste]
                lon = np.linalg.norm(dep)
                u = dep / lon
                e1 = np.cross(u, [1.0, 0.0, 0.0])
                if np.linalg.norm(e1) < 0.3:
                    e1 = np.cross(u, [0.0, 1.0, 0.0])
                e1 /= np.linalg.norm(e1)
                e2 = np.cross(u, e1)
                r = c - c.mean(0)
                xx, yy = r @ e1, r @ e2
                o = np.argsort(np.arctan2(yy, xx))
                xx, yy = xx[o], yy[o]
                aire = 0.5 * abs(np.sum(xx * np.roll(yy, -1) - np.roll(xx, -1) * yy))
                aretes[cle] = (lon, aire, dep)
        for a in range(4):
            f = [v[b] for b in range(4) if b != a]
            cle = tuple(sorted(base[f]))
            dual = np.linalg.norm(cc[i] - cc[voisins[i][a]])
            aire = 0.5 * np.linalg.norm(np.cross(q[f[1]] - q[f[0]], q[f[2]] - q[f[0]]))
            if cle in faces:
                if abs(faces[cle][1] - dual) > 1e-9:
                    conflits += 1
                continue
            faces[cle] = (aire, dual)

    la = sorted(aretes)
    lf = sorted(faces)
    lt = sorted(set(tets))
    ia = {c: k for k, c in enumerate(la)}
    i_f = {c: k for k, c in enumerate(lf)}
    ne, nf, nt = len(la), len(lf), len(lt)
    vol_de = dict(zip(tets, vol))

    lon = np.array([aretes[c][0] for c in la])
    aire_duale = np.array([aretes[c][1] for c in la])
    aire = np.array([faces[c][0] for c in lf])
    lon_duale = np.array([faces[c][1] for c in lf])
    volume = np.array([vol_de[c] for c in lt])
    e0 = np.zeros(n)
    for (a, b), l_, ad in zip(la, lon, aire_duale):
        e0[a] += l_ * ad / 6.0
        e0[b] += l_ * ad / 6.0
    e1_, e2_, e3_ = aire_duale / lon, lon_duale / aire, 1.0 / volume

    li, co, va_ = [], [], []
    for k, (a, b) in enumerate(la):
        li += [k, k]; co += [a, b]; va_ += [-1.0, 1.0]
    d0 = sp.csr_matrix((va_, (li, co)), shape=(ne, n))
    li, co, va_ = [], [], []
    for k, (a, b, c) in enumerate(lf):
        li += [k, k, k]; co += [ia[(b, c)], ia[(a, c)], ia[(a, b)]]; va_ += [1.0, -1.0, 1.0]
    d1 = sp.csr_matrix((va_, (li, co)), shape=(nf, ne))
    li, co, va_ = [], [], []
    for k, (a, b, c, d) in enumerate(lt):
        li += [k] * 4
        co += [i_f[(b, c, d)], i_f[(a, c, d)], i_f[(a, b, d)], i_f[(a, b, c)]]
        va_ += [1.0, -1.0, 1.0, -1.0]
    d2 = sp.csr_matrix((va_, (li, co)), shape=(nt, nf))

    ctrl = {
        "N": n, "E": ne, "F": nf, "T": nt, "Euler": n - ne + nf - nt, "conflits": conflits,
        "somme_voronoi": float(e0.sum()), "somme_tetra": float(volume.sum()),
        "somme_faces": float((aire * lon_duale).sum() / 3.0),
        "d1d0": float(abs(d1 @ d0).max()), "d2d1": float(abs(d2 @ d1).max()),
    }

    def racine(m):
        return sp.diags(np.sqrt(m))

    def inverse(m):
        return sp.diags(1.0 / np.sqrt(m))

    p0 = (racine(e1_) @ d0 @ inverse(e0)).toarray()
    p1 = (racine(e2_) @ d1 @ inverse(e1_)).toarray()
    p2 = (racine(e3_) @ d2 @ inverse(e2_)).toarray()
    v0 = np.linalg.eigvalsh(p0.T @ p0)
    v1 = np.linalg.eigvalsh(p1.T @ p1)
    v2 = np.linalg.eigvalsh(p2 @ p2.T)
    r0, r1, r2 = n - 1, ne - (n - 1) - 3, nt - 1
    ctrl["zeros"] = (float(v0[n - r0 - 1]), float(v1[ne - r1 - 1]), float(v2[nt - r2 - 1]))
    ctrl["lbar"] = float(lon.mean())
    if n <= 160:
        # décomposition de Hodge, vérifiée sur le laplacien complet des 1-formes et des 2-formes
        w1 = np.linalg.eigvalsh(p0 @ p0.T + p1.T @ p1)
        u1 = np.sort(np.concatenate([np.zeros(3), v0[-r0:], v1[-r1:]]))
        w2 = np.linalg.eigvalsh(p1 @ p1.T + p2.T @ p2)
        u2 = np.sort(np.concatenate([np.zeros(3), v1[-r1:], v2[-r2:]]))
        ctrl["hodge"] = (float(np.abs(w1[3:] - u1[3:]).max() / u1[-1]), float(np.abs(w2[3:] - u2[3:]).max() / u2[-1]),
                         len(w1) == len(u1), len(w2) == len(u2))
    spectres = (v0[-r0:], v1[-r1:], v2[-r2:])
    ctrl["bas"] = tuple(np.round(sp_[:7], 2) for sp_ in spectres)
    return ctrl, spectres


BETTI = (1.0, 3.0, 3.0, 1.0)


def moments(spectres, t):
    z = [np.exp(-t * v).sum() for v in spectres]
    m = [(v * np.exp(-t * v)).sum() for v in spectres]
    return z, m


def ds_par_degre(spectres, t):
    z, m = moments(spectres, t)
    num = (m[0], m[0] + m[1], m[1] + m[2], m[2])
    den = (BETTI[0] + z[0], BETTI[1] + z[0] + z[1], BETTI[2] + z[1] + z[2], BETTI[3] + z[2])
    total = 2.0 * t * 2.0 * sum(m) / (8.0 + 2.0 * sum(z))
    return [2.0 * t * a / b for a, b in zip(num, den)], total


def passages(spectres, t):
    z, m = moments(spectres, t)
    return [a / b for a, b in zip(m, z)]


def zeros_de(f, lo, hi, npts=500):
    xs = np.linspace(np.log(lo), np.log(hi), npts)
    vals = np.array([f(np.exp(u)) for u in xs])
    out = []
    for k in range(npts - 1):
        if vals[k] == 0.0 or vals[k] * vals[k + 1] < 0.0:
            out.append(float(np.exp(brentq(lambda u: f(np.exp(u)), xs[k], xs[k + 1]))))
    return out


PAIRES = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)]
ABSCISSES = (0.0024, 0.0075, 0.0235, 0.0742, 0.2336, 0.7359, 2.3180)
MASTER_300 = {0.0024: (0.06, 0.29, 0.44, 0.56), 0.0075: (0.18, 0.61, 0.85, 1.05), 0.0235: (0.52, 1.12, 1.44, 1.64),
              0.0742: (1.32, 1.76, 2.05, 2.17), 0.2336: (2.59, 2.58, 2.59, 2.63), 0.7359: (3.41, 3.26, 3.13, 3.06),
              2.3180: (1.83, 1.77, 1.73, 1.71)}
MASTER_450 = {(0, 1): 0.2521, (0, 2): 0.2560, (1, 2): 0.2611, (0, 3): 0.2626, (1, 3): 0.2722, (2, 3): 0.2988}


def analyser(spectres, n, fen=(0.08, 0.9)):
    a2 = n ** (-2.0 / 3.0)
    res = {}
    for i, j in PAIRES:
        z = zeros_de(lambda x: ds_par_degre(spectres, x * a2)[0][i] - ds_par_degre(spectres, x * a2)[0][j], *fen)
        res[(i, j)] = z
    elem = {}
    for (i, j), nom in (((0, 1), "passages 0 et 1"), ((0, 2), "passages 0 et 2"), ((1, 2), "passages 1 et 2")):
        elem[nom] = zeros_de(lambda x: passages(spectres, x * a2)[i] - passages(spectres, x * a2)[j], *fen)
    return res, elem


def nuage(mode, n, graine):
    rng = np.random.default_rng(graine)
    if mode == "poisson":
        return rng.random((n, 3))
    m = round(n ** (1.0 / 3.0))
    g = np.array(list(itertools.product(range(m), repeat=3)), float)
    return ((g + 0.5 + 0.15 * rng.uniform(-1.0, 1.0, g.shape)) / m) % 1.0


def campagne(mode, tailles):
    print(f"=== Substrat : {mode} ===")
    for n, graines in tailles:
        croix, elems, tables, tot, garde = [], [], [], [], []
        for gr in graines:
            t0 = time.time()
            p = nuage(mode, n, gr)
            ctrl, spectres = construire(p)
            nn = ctrl["N"]
            a2 = nn ** (-2.0 / 3.0)
            res, elem = analyser(spectres, nn)
            garde.append((spectres, nn, ctrl["lbar"]))
            croix.append(res)
            elems.append(elem)
            tables.append([ds_par_degre(spectres, x * a2)[0] for x in ABSCISSES])
            xs = np.exp(np.linspace(np.log(0.2), np.log(2.5), 400))
            tv = np.array([ds_par_degre(spectres, x * a2)[1] for x in xs])
            tot.append((float(tv.max()), float(xs[tv.argmax()])))
            print(f"  N={nn} graine={gr} : E={ctrl['E']} F={ctrl['F']} T={ctrl['T']} Euler={ctrl['Euler']} conflits={ctrl['conflits']} "
                  f"| somme Voronoï={ctrl['somme_voronoi']:.12f} tétra={ctrl['somme_tetra']:.12f} faces={ctrl['somme_faces']:.12f} "
                  f"| d1d0={ctrl['d1d0']:.0e} d2d1={ctrl['d2d1']:.0e} | plus grand « zéro » {max(ctrl['zeros']):.1e} "
                  f"| ({time.time() - t0:.0f} s)")
            print(f"      longueur moyenne d'arête <l> = {ctrl['lbar']:.5f} ; <l>^2 / a^2 = {ctrl['lbar'] ** 2 / a2:.4f} (a = N^(-1/3))")
            if "hodge" in ctrl:
                print(f"      décomposition de Hodge : spectre(Delta_1) contre S_0 u S_1 : écart relatif {ctrl['hodge'][0]:.1e} ; "
                      f"spectre(Delta_2) contre S_1 u S_2 : {ctrl['hodge'][1]:.1e} ; tailles égales : {ctrl['hodge'][2] and ctrl['hodge'][3]}")
            print(f"      bas des spectres de passage (attendu : (2 pi)^2 = 39,48 ; multiplicités 6, 12, 6) :")
            for k in range(3):
                print(f"        S_{k} : {ctrl['bas'][k]}")
            ordre = sorted((v[0], pq) for pq, v in res.items() if len(v) == 1)
            if len(ordre) == 6:
                rho = spearmanr([i + j for _, (i, j) in ordre], [v for v, _ in ordre]).statistic
                print("      croisements :", "  ".join(f"({i},{j})@{v:.4f}" for v, (i, j) in ordre), f"| Spearman(i+j) = {rho:+.4f}")
            else:
                print("      croisements (nombre par paire) :", {pq: [round(u, 4) for u in v] for pq, v in res.items()})
            print("      coïncidences des passages :", {k: [round(u, 4) for u in v] for k, v in elem.items()})
            pa = [passages(spectres, x * a2) for x in (0.05, 0.25, 0.30, 0.8)]
            print("      e_0, e_1, e_2 (x a^2) à t/a^2 = 0,05 ; 0,25 ; 0,30 ; 0,8 :",
                  " | ".join(" ".join(f"{u * a2:.3f}" for u in row) for row in pa))
        tb = np.array(tables)
        print(f"  --- N={n}, {len(graines)} graines : dimension spectrale par degré (moyenne ; écart-type entre graines)")
        for k, x in enumerate(ABSCISSES):
            ligne = "  ".join(f"{tb[:, k, d].mean():.3f}±{tb[:, k, d].std(ddof=1) if len(graines) > 1 else 0:.3f}" for d in range(4))
            ref = MASTER_300[x] if (mode == "poisson" and n == 300) else None
            print(f"      t/a^2={x:6.4f} : {ligne}" + (f"   | master N=300 : {ref}" if ref else ""))
        if mode == "poisson" and n == 300:
            def table(c):
                return np.mean([[ds_par_degre(sp_, c * x * nn_ ** (-2.0 / 3.0))[0] for x in ABSCISSES] for sp_, nn_, _ in garde], axis=0)
            ref = np.array([MASTER_300[x] for x in ABSCISSES])
            cs = np.linspace(0.8, 2.6, 361)
            cout = [float(np.mean((np.log(table(c)) - np.log(ref)) ** 2)) for c in cs]
            cbest = float(cs[int(np.argmin(cout))])
            tb2 = table(cbest)
            print(f"  --- Unité de la maille du master : une seule constante c ajustée sur ses 28 valeurs (t_master/a_master^2 = t N^(2/3) / c)")
            print(f"      meilleur c = {cbest:.3f} ; écart quadratique moyen en log = {np.sqrt(min(cout)):.4f} ; <l>^2/a^2 moyen = {np.mean([l_ ** 2 * nn_ ** (2.0 / 3.0) for _, nn_, l_ in garde]):.4f}")
            for k, x in enumerate(ABSCISSES):
                print(f"      t/a^2={x:6.4f} : pilote " + " ".join(f"{u:.3f}" for u in tb2[k]) + "  | master " + " ".join(f"{u:.2f}" for u in ref[k]))
        print(f"  --- N={n} : positions des croisements (moyenne ; écart-type entre graines ; graines où le croisement est unique)")
        for pq in PAIRES:
            v = [c[pq][0] for c in croix if len(c[pq]) == 1]
            if v:
                ref = f"   | master N=450 : {MASTER_450[pq]}" if (mode == "poisson" and n == 450) else ""
                print(f"      {pq} somme {sum(pq)} : {np.mean(v):.4f} ± {np.std(v, ddof=1) if len(v) > 1 else 0:.4f}  ({len(v)}/{len(croix)}){ref}")
            else:
                print(f"      {pq} : pas de croisement unique dans la fenêtre")
        for nom in elems[0]:
            v = [e[nom][0] for e in elems if len(e[nom]) == 1]
            if v:
                print(f"      coïncidence des {nom} : {np.mean(v):.4f} ± {np.std(v, ddof=1) if len(v) > 1 else 0:.4f}  ({len(v)}/{len(elems)})")
        print(f"  --- N={n} : maximum de la dimension spectrale totale (tous degrés) : "
              + " ; ".join(f"{m:.3f} à t/a^2={x:.3f}" for m, x in tot))


if __name__ == "__main__":
    quoi = sys.argv[1] if len(sys.argv) > 1 else "poisson"
    if quoi == "poisson":
        campagne("poisson", [(150, (11, 12, 13, 14)), (300, (21, 22, 23, 24)), (450, (31, 32, 33))])
    elif quoi == "grille":
        campagne("grille", [(216, (41, 42, 43)), (343, (51, 52, 53))])
    elif quoi == "grand":
        campagne("poisson", [(1000, (61,))])
    elif quoi == "essai":
        campagne("poisson", [(150, (11,))])
