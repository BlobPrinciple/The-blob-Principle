#!/usr/bin/env python3
"""X-24, partie A -- la regle de l'etage quand un lien est un contact (et non une distance tenue).
Realisation par contacts d'une coque de rang k : des calottes rondes de S^k, d'interieurs disjoints, tangentes exactement le long des liens.
Chaque calotte est un vecteur u de l'espace de Minkowski a (k+1)+1 dimensions, de carre <u,u> = 1 ; contact <=> <u_i,u_j> = -1 ; disjointes <=> <u_i,u_j> < -1.
Rang 2 : empilement de cercles calcule par la methode de Newton sur les sommes d'angles (fonctionnelle convexe de Colin de Verdiere), puis controles :
 N1 existence ; N2 unicite (deux faces exterieures) ; N3 signature (3,1) ; N4 rigidite (noyau de dimension 6) ; N5 polyedre de Koebe ; N6 rang 1 ; N7 rang >= 3.
Prediction scellee : x24_contact_et_porteur_de_l_etage_prediction.txt (SHA-256 d287d0a3fa12fc54313064f13cc957147229992665bee313d92c74e753b8bf95).
Usage : python3 x24_contacts.py [tout|essai]     Claude, 22 novembre 2026."""
import itertools, json, math, os, sys, time
import numpy as np
import mpmath as mp
from scipy.optimize import least_squares
from scipy.spatial import ConvexHull
from x23_outils import liens_des_cellules
from x23_coques import bord_du_simplexe, mitose_arete, est_fermee

ICI = os.path.dirname(os.path.abspath(__file__))
TAILLES = (4, 5, 6, 8, 12, 20, 40, 80, 150, 300)
GRAINES = (0, 1, 2, 3, 4, 5)
mp.mp.dps = 60


# ---------------------------------------------------------------- coques
def coques_par_mitose(k, tailles, graine):
    """Coque de rang k nee du bord du simplexe par mitose uniforme de l'arete ; etats releves aux tailles demandees."""
    rng = np.random.default_rng([24, k, graine])
    cellules, n = bord_du_simplexe(k)
    etats = {}
    while True:
        if n in tailles:
            assert est_fermee(cellules, k)
            etats[n] = [tuple(sorted(F)) for F in cellules]
        if n >= max(tailles):
            return etats
        liens = liens_des_cellules(cellules)
        a, b = liens[int(rng.integers(len(liens)))]
        cellules = mitose_arete(cellules, a, b, n); n += 1


def oriente(faces):
    """Oriente toutes les faces de facon coherente (deux faces voisines parcourent leur lien commun en sens opposes)."""
    faces = [tuple(f) for f in faces]
    par_lien = {}
    for i, f in enumerate(faces):
        for a, b in itertools.combinations(f, 2):
            par_lien.setdefault((min(a, b), max(a, b)), []).append(i)
    assert all(len(v) == 2 for v in par_lien.values())
    ori = {0: faces[0]}
    pile = [0]
    while pile:
        i = pile.pop(); f = ori[i]
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            for j in par_lien[(min(a, b), max(a, b))]:
                if j != i and j not in ori:
                    c = [x for x in faces[j] if x != a and x != b][0]
                    ori[j] = (b, a, c)
                    pile.append(j)
    assert len(ori) == len(faces)
    return [ori[i] for i in range(len(faces))]


# ---------------------------------------------------------------- empilement de cercles (rang 2)
def rayons(n, F, ext, tol=1e-13, itmax=400):
    """Rayons d'un empilement euclidien : les trois cercles de la face exterieure ont le rayon 1, la somme des angles vaut 2 pi autour des autres."""
    F = np.array(F)
    dedans = np.array([v for v in range(n) if v not in ext], dtype=int)
    if len(dedans) == 0:
        return np.ones(n), 0
    place = -np.ones(n, dtype=int); place[dedans] = np.arange(len(dedans))
    Vc = np.concatenate([F[:, 0], F[:, 1], F[:, 2]]); Ac = np.concatenate([F[:, 1], F[:, 2], F[:, 0]]); Bc = np.concatenate([F[:, 2], F[:, 0], F[:, 1]])

    def residu(u):
        r = np.exp(u); rv, ra, rb = r[Vc], r[Ac], r[Bc]
        th = np.zeros(n); np.add.at(th, Vc, 2 * np.arctan(np.sqrt(ra * rb / (rv * (rv + ra + rb)))))
        return (th - 2 * np.pi)[dedans]
    u = np.zeros(n)
    res = residu(u)
    for it in range(itmax):
        if np.abs(res).max() < tol:
            break
        r = np.exp(u); rv, ra, rb = r[Vc], r[Ac], r[Bc]
        rho = np.sqrt(rv * ra * rb / (rv + ra + rb))
        da, db = rho / (rv + ra), rho / (rv + rb)
        J = np.zeros((len(dedans), len(dedans)))
        m = place[Vc] >= 0
        np.add.at(J, (place[Vc][m], place[Vc][m]), -(da + db)[m])
        ma = m & (place[Ac] >= 0); np.add.at(J, (place[Vc][ma], place[Ac][ma]), da[ma])
        mb = m & (place[Bc] >= 0); np.add.at(J, (place[Vc][mb], place[Bc][mb]), db[mb])
        du = np.linalg.solve(J, -res)
        t = 1.0; n0 = np.linalg.norm(res)
        while True:
            u2 = u.copy(); u2[dedans] += t * du
            res2 = residu(u2)
            if np.linalg.norm(res2) <= (1 - 1e-4 * t) * n0 or t < 1e-12:
                break
            t /= 2
        u, res = u2, res2
    return np.exp(u), it


def rayons_mp(n, F, ext, r0):
    """Meme systeme, affine a 60 chiffres par la methode de Newton a partir de la solution flottante."""
    dedans = [v for v in range(n) if v not in ext]
    place = {v: i for i, v in enumerate(dedans)}
    u = [mp.log(mp.mpf(float(x))) for x in r0]
    for v in ext:
        u[v] = mp.mpf(0)
    coins = [(f[c], f[(c + 1) % 3], f[(c + 2) % 3]) for f in F for c in range(3)]
    for it in range(12):
        r = [mp.exp(x) for x in u]
        res = mp.matrix(len(dedans), 1); J = mp.matrix(len(dedans), len(dedans))
        for i in range(len(dedans)):
            res[i] = -2 * mp.pi
        for v, a, b in coins:
            if v not in place:
                continue
            i = place[v]; s = r[v] + r[a] + r[b]
            res[i] += 2 * mp.atan(mp.sqrt(r[a] * r[b] / (r[v] * s)))
            rho = mp.sqrt(r[v] * r[a] * r[b] / s)
            da, db = rho / (r[v] + r[a]), rho / (r[v] + r[b])
            J[i, i] -= da + db
            if a in place: J[i, place[a]] += da
            if b in place: J[i, place[b]] += db
        err = max(abs(res[i]) for i in range(len(dedans))) if dedans else mp.mpf(0)
        if err < mp.mpf(10) ** (-52):
            break
        du = mp.lu_solve(J, -res)
        for i, v in enumerate(dedans):
            u[v] += du[i]
    return [mp.exp(x) for x in u], float(err)


def disposition(n, F, ext, r, haute=False):
    """Centres (nombres complexes) : face exterieure posee dans le sens des aiguilles d'une montre, puis chaque face de proche en proche."""
    if haute:
        sq, at, ex, un = mp.sqrt, mp.atan, mp.exp, mp.mpc(0, 1)
    else:
        sq, at, ex, un = math.sqrt, math.atan, np.exp, 1j

    def angle(v, a, b):
        return 2 * at(sq(r[a] * r[b] / (r[v] * (r[v] + r[a] + r[b]))))
    P = [None] * n
    a, b, c = ext
    P[a] = 0 * un; P[b] = (r[a] + r[b]) + 0 * un
    P[c] = P[a] + (r[a] + r[c]) * ex(-un * angle(a, b, c))
    par_lien = {}
    for i, f in enumerate(F):
        for x, y in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            par_lien.setdefault((min(x, y), max(x, y)), []).append(i)
    fait = set(); file = [i for i, f in enumerate(F) if set(f) == set(ext)]
    assert len(file) == 1
    fait.add(file[0])
    while file:
        i = file.pop(0); f = F[i]
        for x, y in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            for j in par_lien[(min(x, y), max(x, y))]:
                if j in fait:
                    continue
                g = F[j]
                for t in range(3):
                    p, q, k = g[t], g[(t + 1) % 3], g[(t + 2) % 3]
                    if P[p] is not None and P[q] is not None:
                        if P[k] is None:
                            d = P[q] - P[p]
                            P[k] = P[p] + (r[p] + r[k]) * ex(un * angle(p, q, k)) * d / abs(d)
                        break
                fait.add(j); file.append(j)
    assert all(p is not None for p in P)
    return P


def gram(P, r, haute=False):
    """Produits inversifs <u_i,u_j> = (r_i^2 + r_j^2 - |c_i - c_j|^2) / (2 r_i r_j) : invariants de Mobius."""
    n = len(P)
    if haute:
        G = mp.matrix(n, n)
        for i in range(n):
            for j in range(n):
                G[i, j] = (r[i] ** 2 + r[j] ** 2 - abs(P[i] - P[j]) ** 2) / (2 * r[i] * r[j])
        return G
    P = np.array(P); r = np.array(r)
    return (r[:, None] ** 2 + r[None, :] ** 2 - np.abs(P[:, None] - P[None, :]) ** 2) / (2 * r[:, None] * r[None, :])


def vecteurs(P, r, haute=False):
    """Vecteurs de Minkowski (x, y, z ; t), signature (+,+,+,-), des cercles du plan."""
    out = []
    for p, rr in zip(P, r):
        x, y = (p.real, p.imag)
        q = x * x + y * y - rr * rr
        out.append([x / rr, y / rr, (q - 1) / (2 * rr), (q + 1) / (2 * rr)])
    return out


def rang_mp(M, seuil=mp.mpf(10) ** (-30)):
    """Rang par elimination a pivot total, en haute precision."""
    M = M.copy(); nl, nc = M.rows, M.cols
    grand = max(abs(M[i, j]) for i in range(nl) for j in range(nc))
    rang = 0; lignes = list(range(nl)); cols = list(range(nc))
    for etape in range(min(nl, nc)):
        best = mp.mpf(0); bi = bj = -1
        for i in range(etape, nl):
            for j in range(etape, nc):
                if abs(M[i, j]) > best:
                    best = abs(M[i, j]); bi, bj = i, j
        if best <= seuil * grand:
            break
        if bi != etape:
            for j in range(nc):
                M[etape, j], M[bi, j] = M[bi, j], M[etape, j]
        if bj != etape:
            for i in range(nl):
                M[i, etape], M[i, bj] = M[i, bj], M[i, etape]
        piv = M[etape, etape]
        for i in range(etape + 1, nl):
            f = M[i, etape] / piv
            if f != 0:
                for j in range(etape, nc):
                    M[i, j] -= f * M[etape, j]
        rang += 1
    return rang, float(best / grand) if grand else 0.0


def jacobien_contacts(U, liens, dim):
    """Jacobien de (<u_i,u_i> - 1 ; <u_i,u_j> + 1 sur les liens) ; dim = k+2 coordonnees par constituant, la derniere de genre temps."""
    n = len(U)
    J = mp.matrix(n + len(liens), dim * n)
    sg = [1] * (dim - 1) + [-1]
    for i in range(n):
        for a in range(dim):
            J[i, dim * i + a] = 2 * sg[a] * U[i][a]
    for e, (i, j) in enumerate(liens):
        for a in range(dim):
            J[n + e, dim * i + a] = sg[a] * U[j][a]
            J[n + e, dim * j + a] = sg[a] * U[i][a]
    return J


def champs_de_lorentz(U, dim):
    """Action des generateurs du groupe de Lorentz so(dim-1, 1) sur les vecteurs : X = eta A, A antisymetrique."""
    n = len(U); sg = [1] * (dim - 1) + [-1]
    champs = []
    for a, b in itertools.combinations(range(dim), 2):
        f = mp.matrix(dim * n, 1)
        for i in range(n):
            f[dim * i + a] += sg[a] * U[i][b]       # (eta A u)_a = eta_aa * u_b
            f[dim * i + b] -= sg[b] * U[i][a]
        champs.append(f)
    return champs


# ---------------------------------------------------------------- centrage et polyedre de Koebe
def centrage(U, liens):
    """Barycentre conforme des points de contact : le boost qui amene leur centre de gravite a l'origine (Springborn 2005)."""
    U = np.array(U, dtype=float)
    L = []
    for i, j in liens:
        l = U[i] + U[j]                      # vecteur de genre lumiere : le point de contact
        L.append(l / l[3])
    L = np.array(L)
    x = np.array([0.0, 0.0, 0.0, 1.0])
    for it in range(10000):
        w = -(L[:, :3] @ x[:3] - L[:, 3] * x[3])          # -<x, l> > 0
        y = (L / w[:, None]).sum(0)
        y = y / math.sqrt(y[3] ** 2 - (y[:3] ** 2).sum())
        if np.abs(y - x).max() < 1e-15 * max(1.0, abs(y[3])):
            x = y; break
        x = y
    v = x[:3] / x[3]; v2 = float(v @ v)                    # vitesse du boost
    g = 1 / math.sqrt(1 - v2)
    B = np.eye(4)
    if v2 > 0:
        B[:3, :3] += (g - 1) * np.outer(v, v) / v2
        B[:3, 3] = -g * v; B[3, :3] = -g * v; B[3, 3] = g
    return U @ B.T, float(math.atanh(math.sqrt(v2))), it, v


def boost_mp(Um, v):
    """Le meme boost, construit a 60 chiffres a partir de la vitesse flottante : transformation de Lorentz exacte, donc l'empilement reste un empilement."""
    v = [mp.mpf(float(x)) for x in v]; v2 = sum(x * x for x in v)
    if v2 == 0:
        return [list(u) for u in Um]
    g = 1 / mp.sqrt(1 - v2)
    out = []
    for u in Um:
        uv = sum(u[a] * v[a] for a in range(3))
        out.append([u[a] + (g - 1) * uv * v[a] / v2 - g * v[a] * u[3] for a in range(3)] + [g * (u[3] - uv)])
    return out


def koebe(U, liens, faces):
    """Polyedre de Koebe d'un empilement centre : sommets = poles des calottes."""
    U = np.asarray(U); n = len(U)
    assert (U[:, 3] > 0).all(), 'une calotte depasse l hemisphere apres centrage'
    S = U[:, :3] / U[:, 3:4]
    tang = 0.0
    for i, j in liens:
        d = S[j] - S[i]
        tang = max(tang, abs(np.linalg.norm(np.cross(S[i], d)) / np.linalg.norm(d) - 1.0))
    hull = ConvexHull(S)
    convexe = len(hull.vertices) == n and {tuple(sorted(int(x) for x in s)) for s in hull.simplices} == {tuple(sorted(f)) for f in faces}
    R = np.zeros((len(liens), 3 * n))
    for e, (i, j) in enumerate(liens):
        d = S[i] - S[j]; d = d / np.linalg.norm(d)
        R[e, 3 * i:3 * i + 3] = d; R[e, 3 * j:3 * j + 3] = -d
    sv = np.linalg.svd(R, compute_uv=False)
    return dict(ecart_de_tangence_des_aretes=float(tang), convexe_et_memes_faces=bool(convexe), plus_petite_valeur_singuliere=float(sv[-1]), plus_grande=float(sv[0]),
                rang_flottant=int((sv > 1e-9 * sv[0]).sum()), rang_attendu=3 * n - 6), S


def rang_koebe_mp(Ump, liens):
    """Rang de la matrice de rigidite du polyedre de Koebe a l'etage 3, a 60 chiffres (les poles sont pris tels quels : le rang est invariant projectif)."""
    n = len(Ump)
    S = [[u[a] / u[3] for a in range(3)] for u in Ump]
    R = mp.matrix(len(liens), 3 * n)
    for e, (i, j) in enumerate(liens):
        for a in range(3):
            R[e, 3 * i + a] = S[i][a] - S[j][a]; R[e, 3 * j + a] = S[j][a] - S[i][a]
    return rang_mp(R)


# ---------------------------------------------------------------- une coque de rang 2, tous controles
def face_eloignee(F, ext):
    for f in F:
        if not set(f) & set(ext):
            return f
    return next(f for f in F if set(f) != set(ext))


def etude_rang2(n, faces, haute):
    F = oriente(faces)
    liens = liens_des_cellules([frozenset(f) for f in faces])
    assert len(liens) == 3 * n - 6
    lien = set(liens)
    out = dict(V=n, liens=len(liens))
    ext1 = F[0]; ext2 = face_eloignee(F, ext1)
    Gs = []
    for num, ext in enumerate((ext1, ext2)):
        r, it = rayons(n, F, ext)
        P = disposition(n, F, ext, r)
        Pn = np.array(P)
        tang = max(abs(abs(Pn[i] - Pn[j]) - (r[i] + r[j])) / (r[i] + r[j]) for i, j in liens)
        G = gram(P, r)
        hors = np.array([[(min(i, j), max(i, j)) not in lien and i != j for j in range(n)] for i in range(n)])
        out['calcul%d' % (num + 1)] = dict(face_exterieure=list(ext), iterations=int(it), residu_de_tangence_relatif=float(tang), plus_grand_produit_hors_liens=float(G[hors].max()) if hors.any() else None,
                                           rapport_des_rayons=float(r.max() / r.min()))
        Gs.append(G)
        if num == 0:
            r1, P1 = r, P
    out['unicite_ecart_relatif_des_produits'] = float((np.abs(Gs[0] - Gs[1]) / (1 + np.abs(Gs[0]))).max())
    out['aucun_chevauchement'] = bool(out['calcul1']['plus_grand_produit_hors_liens'] is None or out['calcul1']['plus_grand_produit_hors_liens'] < -1)
    ev = np.linalg.eigvalsh(Gs[0]); ordre = np.argsort(-np.abs(ev)); quatre = ev[ordre[:4]]
    out['signature_flottante'] = dict(positives=int((quatre > 0).sum()), negatives=int((quatre < 0).sum()), cinquieme_sur_quatrieme=float(abs(ev[ordre[4]]) / abs(ev[ordre[3]])) if n > 4 else 0.0)
    # centrage et polyedre de Koebe (flottant)
    U = vecteurs(P1, r1)
    Uc, rapidite, itc, vit = centrage(U, liens)
    ko, S = koebe(Uc, liens, faces)
    ko['rapidite_du_centrage'] = rapidite
    out['koebe'] = ko
    out['rayon_angulaire_min_max_deg'] = [float(np.degrees(np.arctan(1 / np.abs(Uc[:, 3])).min())), float(np.degrees(np.arccos(np.clip(Uc[:, 3] / np.sqrt(1 + Uc[:, 3] ** 2), -1, 1)).max()))]
    # rigidite en flottant, variables (centre / rayon, log rayon) : jacobien de log(distance / somme des rayons) sur les liens
    Jf = np.zeros((len(liens), 3 * n)); Pn = np.array(P1)
    for e, (i, j) in enumerate(liens):
        d = Pn[i] - Pn[j]; dd = abs(d) ** 2; s = r1[i] + r1[j]
        Jf[e, 3 * i] = r1[i] * d.real / dd; Jf[e, 3 * i + 1] = r1[i] * d.imag / dd; Jf[e, 3 * i + 2] = -r1[i] / s
        Jf[e, 3 * j] = -r1[j] * d.real / dd; Jf[e, 3 * j + 1] = -r1[j] * d.imag / dd; Jf[e, 3 * j + 2] = -r1[j] / s
    sv = np.linalg.svd(Jf, compute_uv=False)
    out['rigidite_flottante'] = dict(lignes=len(liens), colonnes=3 * n, plus_petite_valeur_singuliere=float(sv[-1]), plus_grande=float(sv[0]), noyau=int(3 * n - (sv > 1e-10 * sv[0]).sum()))
    if haute:
        rm, err = rayons_mp(n, F, ext1, r1)
        Pm = disposition(n, F, ext1, rm, haute=True)
        tangm = max(abs(abs(Pm[i] - Pm[j]) - (rm[i] + rm[j])) / (rm[i] + rm[j]) for i, j in liens)
        Um = vecteurs(Pm, rm, haute=True)
        J = jacobien_contacts(Um, liens, 4)
        rg, dernier = rang_mp(J)
        champs = champs_de_lorentz(Um, 4)
        ecart = max(max(abs(x) for x in (J * f)) for f in champs)
        C = mp.matrix(4 * n, 6)
        for c, f in enumerate(champs):
            for i in range(4 * n):
                C[i, c] = f[i]
        rgc, _ = rang_mp(C)
        Gm = gram(Pm, rm, haute=True)
        E = mp.eigsy(Gm, eigvals_only=True)
        vals = sorted([E[i] for i in range(n)], key=lambda x: -abs(x))
        rk, _ = rang_koebe_mp(boost_mp(Um, vit), liens)
        out['haute_precision'] = dict(erreur_des_sommes_d_angles=err, residu_de_tangence_relatif=float(tangm), rang_du_jacobien=rg, lignes=n + len(liens), colonnes=4 * n, noyau=4 * n - rg,
                                      pivot_suivant_relatif=dernier, champs_de_lorentz_dans_le_noyau_ecart=float(ecart), rang_des_six_champs=rgc,
                                      valeurs_propres_positives=sum(1 for x in vals[:4] if x > 0), valeurs_propres_negatives=sum(1 for x in vals[:4] if x < 0),
                                      cinquieme_sur_quatrieme=float(abs(vals[4]) / abs(vals[3])) if n > 4 else 0.0, rang_de_rigidite_du_polyedre=rk, rang_attendu=3 * n - 6,
                                      produits_inversifs=[[float(Gm[i, j]) for j in range(n)] for i in range(n)] if n <= 12 else None)
    return out


# ---------------------------------------------------------------- rang 1 et rangs >= 3
def rang1(V, rng):
    """Polygone : V arcs qui se touchent bout a bout sur le cercle. Vecteurs de l'espace de Minkowski a 2+1 dimensions."""
    bouts = np.sort(rng.uniform(0, 2 * np.pi, V))
    U = []
    for i in range(V):
        a, b = bouts[i], bouts[(i + 1) % V] + (2 * np.pi if i == V - 1 else 0)
        c, h = (a + b) / 2, (b - a) / 2
        U.append([mp.cos(c) / mp.sin(h), mp.sin(c) / mp.sin(h), mp.cos(h) / mp.sin(h)])
    liens = sorted((min(i, (i + 1) % V), max(i, (i + 1) % V)) for i in range(V))
    sg = [1, 1, -1]
    res = max(abs(sum(sg[a] * U[i][a] * U[j][a] for a in range(3)) + 1) for i, j in liens)
    J = jacobien_contacts(U, liens, 3)
    rg, _ = rang_mp(J, seuil=mp.mpf(10) ** (-12))
    return dict(V=V, residu=float(res), rang=rg, colonnes=3 * V, noyau=3 * V - rg, attendu=max(V, 3))


def recherche(n, liens, dim, departs, graine, penalite=True):
    """Cherche n calottes de S^(dim-2) dont le graphe des contacts est exactement << liens >> : moindres carres, chevauchements comptes."""
    lien = set(liens); hors = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in lien]
    sg = np.array([1.0] * (dim - 1) + [-1.0])
    I = np.array([l[0] for l in liens]); Jx = np.array([l[1] for l in liens])
    Ih = np.array([l[0] for l in hors], dtype=int); Jh = np.array([l[1] for l in hors], dtype=int)

    def f(x):
        U = x.reshape(n, dim)
        a = (U * U * sg).sum(1) - 1
        b = (U[I] * U[Jx] * sg).sum(1) + 1
        if len(hors) and penalite:
            c = np.maximum(0.0, (U[Ih] * U[Jh] * sg).sum(1) + 1)
            return np.concatenate([a, b, c])
        return np.concatenate([a, b])
    rng = np.random.default_rng([24, 7, n, dim, graine])
    best = None; residus = []
    for d in range(departs):
        U0 = rng.normal(size=(n, dim)); U0[:, -1] *= 0.3
        q = (U0 * U0 * sg).sum(1)
        U0[q <= 0.05, -1] = 0.0
        U0 /= np.sqrt((U0 * U0 * sg).sum(1))[:, None]
        s = least_squares(f, U0.ravel(), method='trf', xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
        rr = float(np.linalg.norm(s.fun)); residus.append(rr)
        if best is None or rr < best[0]:
            best = (rr, s.x.reshape(n, dim).copy())
    return best, residus


def rang_superieur(k, departs):
    """Rang k >= 3 : K_(k+2), K_(k+3) moins un lien (une naissance), K_(k+4) moins deux liens disjoints (deux naissances, liens (1,2) puis (3,4))."""
    dim = k + 2; out = {}
    cas = {'depart': (k + 2, []), 'une_naissance': (k + 3, [(0, 1)]), 'deux_naissances': (k + 4, [(0, 1), (2, 3)])}
    for nom, (n, retire) in cas.items():
        liens = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in retire]
        (res, U), residus = recherche(n, liens, dim, departs, k)
        ligne = dict(constituants=n, liens=len(liens), compte_juste=dim * n - n - dim * (dim - 1) // 2, departs=departs, plus_petit_residu=res,
                     residu_median=float(np.median(residus)), departs_sous_1e_8=int(sum(1 for x in residus if x < 1e-8)))
        if res < 1e-9:
            Um = [[mp.mpf(float(x)) for x in u] for u in U]
            J = jacobien_contacts(Um, liens, dim)
            rg, _ = rang_mp(J, seuil=mp.mpf(10) ** (-9))
            ligne.update(rang_du_jacobien=rg, noyau=dim * n - rg, noyau_du_groupe=dim * (dim - 1) // 2)
        # meme recherche sans compter les chevauchements : montre les solutions degenerees (boules confondues)
        (res0, U0), _ = recherche(n, liens, dim, max(20, departs // 10), k + 100, penalite=False)
        ligne['plus_petit_residu_sans_compter_les_chevauchements'] = res0
        out[nom] = ligne
    return out


# ---------------------------------------------------------------- execution
def controle_300():
    """Ajout apres execution, declare : le seul calcul au-dessus du seuil 1e-9 de N1 (graine 0, 300 constituants, seconde face exterieure : 2,3e-9) est refait
    avec des rayons et une disposition a 60 chiffres, pour savoir si l'ecart vient de l'arithmetique flottante de la disposition de proche en proche."""
    n = 300; faces = coques_par_mitose(2, (n,), 0)[n]
    F = oriente(faces); liens = liens_des_cellules([frozenset(f) for f in faces])
    ext = face_eloignee(F, F[0])
    r, it = rayons(n, F, ext)
    P = np.array(disposition(n, F, ext, r))
    flottant = max(abs(abs(P[i] - P[j]) - (r[i] + r[j])) / (r[i] + r[j]) for i, j in liens)
    rm, err = rayons_mp(n, F, ext, r)
    Pm = disposition(n, F, ext, rm, haute=True)
    haute = max(abs(abs(Pm[i] - Pm[j]) - (rm[i] + rm[j])) / (rm[i] + rm[j]) for i, j in liens)
    ecart_rayons = max(abs(mp.mpf(float(r[i])) - rm[i]) / rm[i] for i in range(n))
    res = dict(graine=0, V=n, face_exterieure=list(ext), residu_flottant=float(flottant), residu_a_60_chiffres=float(haute), erreur_des_sommes_d_angles=err, ecart_relatif_des_rayons_flottants=float(ecart_rayons))
    print(json.dumps(res)); json.dump(res, open(os.path.join(ICI, 'x24_contacts_controle_300.json'), 'w'), indent=1)


if __name__ == '__main__':
    quoi = sys.argv[1] if len(sys.argv) > 1 else 'tout'
    if quoi == 'controle300':
        controle_300(); sys.exit(0)
    t0 = time.time(); sortie = dict(rang2=[], rang1=[], rangs_superieurs={})
    tailles = TAILLES if quoi == 'tout' else (4, 5, 6, 8, 12)
    graines = GRAINES if quoi == 'tout' else (0,)
    definitions = {}
    for g in graines:
        etats = coques_par_mitose(2, tailles, g)
        for n in tailles:
            definitions['rang2_graine%d_V%d' % (g, n)] = etats[n]
            r = etude_rang2(n, etats[n], haute=(n <= 40 and (g < 2 or n <= 12)))
            r['graine'] = g
            sortie['rang2'].append(r)
            hp = r.get('haute_precision', {})
            print('rang 2 | graine %d | V %3d | tangence %.1e ; %.1e | unicite %.1e | chevauchement %s | signature (%d,%d) | noyau flottant %d | Koebe convexe %s, tangence %.1e, rang %d/%d | haute precision : noyau %s, rigidite %s/%s'
                  % (g, n, r['calcul1']['residu_de_tangence_relatif'], r['calcul2']['residu_de_tangence_relatif'], r['unicite_ecart_relatif_des_produits'], not r['aucun_chevauchement'],
                     r['signature_flottante']['positives'], r['signature_flottante']['negatives'], r['rigidite_flottante']['noyau'], r['koebe']['convexe_et_memes_faces'], r['koebe']['ecart_de_tangence_des_aretes'],
                     r['koebe']['rang_flottant'], r['koebe']['rang_attendu'], hp.get('noyau'), hp.get('rang_de_rigidite_du_polyedre'), hp.get('rang_attendu')), flush=True)
    json.dump(definitions, open(os.path.join(ICI, 'x24_coques_definitions.json'), 'w'))
    rng = np.random.default_rng([24, 1])
    for V in range(3, 13):
        r = rang1(V, rng); sortie['rang1'].append(r)
        print('rang 1 | V %2d | residu %.1e | noyau %d (attendu %d)' % (V, r['residu'], r['noyau'], r['attendu']), flush=True)
    for k in ((3, 4, 5) if quoi == 'tout' else (3,)):
        sortie['rangs_superieurs'][str(k)] = rang_superieur(k, 200 if quoi == 'tout' else 30)
        for nom, l in sortie['rangs_superieurs'][str(k)].items():
            print('rang %d | %s | %d constituants, %d liens (compte juste : %d) | plus petit residu %.2e (median %.2e ; %d departs sous 1e-8) | noyau %s | sans compter les chevauchements : %.1e'
                  % (k, nom, l['constituants'], l['liens'], l['compte_juste'], l['plus_petit_residu'], l['residu_median'], l['departs_sous_1e_8'], l.get('noyau'), l['plus_petit_residu_sans_compter_les_chevauchements']), flush=True)
    sortie['duree_s'] = round(time.time() - t0, 1)
    json.dump(sortie, open(os.path.join(ICI, 'x24_contacts.json' if quoi == 'tout' else 'x24_contacts_essai.json'), 'w'), indent=1)
    print('duree', sortie['duree_s'], 's')
