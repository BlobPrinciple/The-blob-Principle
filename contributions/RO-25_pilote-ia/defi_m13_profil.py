#!/usr/bin/env python3
"""DEFI-M13 — profil d'énergie libre le long de T_v : la barrière de l'aristocratie, mesurée.

Pilote IA du laboratoire (Claude, Anthropic), 30 octobre 2026.

Cadre de DEFI-M8, M11, M12 (H-abs : graphes abstraits étiquetés, beta = 0,30, tau = 0,50 ;
pi ∝ exp(lam · S_sim), S_sim = log(1 + n_tri) − beta · D ; D = écart-type de population des
degrés / degré moyen ; échanges de Metropolis à |E| fixé, proposition uniforme ; noyau de
defi_m12_lenteur.balayer, auquel on ajoute un biais w(T_0) sur le nombre de triangles du
sommet marqué 0).

But : mesurer la loi d'équilibre exacte P(T_v) du nombre de triangles d'un sommet (sommets
échangeables : P est la même pour tout v) jusque dans ses creux, par échantillonnage
multicanonique (Wang–Landau sur T_0, puis production à biais fixé et repondération).
F(T) = −log P(T) est le profil d'énergie libre le long de l'observable dont DEFI-M12 a
mesuré le demi-temps d'autocorrélation. Barrière de sortie de l'aristocratie :
B_sortie = F(col) − F(minimum aristocratique), col = maximum de F entre le minimum roturier
et le minimum aristocratique. Si la lenteur de DEFI-M12 est une traversée activée de ce col,
log t½ doit suivre B_sortie à une constante près (pente 1).

Contrôle sans biais : aux petites tailles, P(T) est aussi estimé par l'histogramme direct
d'une chaîne non biaisée (tous les sommets), à comparer.

Usage : python3 defi_m13_profil.py [--points c2:17,c2:25,...] [--repetitions 3]
        [--processus 2] [--sortie defi_m13_profil.json]
Point « reg:n[:lam] » ; reg ∈ {c2, c3} (M = 2n ou 3n) ; lam par défaut n / tau.
"""
import json
import math
import pathlib
import sys
import time
from multiprocessing import Pool

import numpy as np
from numba import njit

import defi_m12_lenteur as L

ICI = pathlib.Path(__file__).resolve().parent
BETA, TAU = L.BETA, L.TAU
F_FINAL = 1e-5      # facteur de modification final de Wang–Landau
PLATITUDE = 0.7     # min H > 0,7 × moyenne sur tout le support
PROD = 5000         # balayages par bloc de production (8 blocs)


@njit(cache=True)
def ssim(ntri, Q, M, n):
    mu = 2.0 * M / n
    var = Q / n - mu * mu
    if var < 0.0:
        var = 0.0
    return math.log(1.0 + ntri) - BETA * math.sqrt(var) / mu


@njit(cache=True)
def communs(adj, n, u, v):
    c = 0
    for w in range(n):
        if adj[u, w] and adj[v, w]:
            c += 1
    return c


@njit(cache=True)
def t0_de(adj, n):
    t = 0
    for a in range(1, n):
        if adj[0, a]:
            for b in range(a + 1, n):
                if adj[0, b] and adj[a, b]:
                    t += 1
    return t


@njit(cache=True)
def balayer_biais(adj, aretes, deg, etat, n, nsteps, lam, w, H, f, tcap, vu):
    """Noyau de defi_m12_lenteur.balayer + biais exp(w[T_0]).
    etat = [n_tri, Σd², T_0]. Si f > 0 : Wang–Landau (w[T_0] −= f à chaque pas) ; vu marque
    les cases déjà rencontrées.
    H : histogramme de T_0 (un comptage par pas). Les états T_0 > tcap sont refusés."""
    M = aretes.shape[0]
    acc = 0
    for s in range(nsteps):
        i = np.random.randint(M)
        u, v = aretes[i, 0], aretes[i, 1]
        while True:
            x = np.random.randint(n)
            y = np.random.randint(n)
            if x != y and not adj[x, y]:
                break
        if x > y:
            x, y = y, x
        cuv = communs(adj, n, u, v)
        t0 = int(etat[2])
        if u == 0 or v == 0:
            t0 -= cuv
        elif adj[0, u] and adj[0, v]:
            t0 -= 1
        adj[u, v] = False
        adj[v, u] = False
        cxy = communs(adj, n, x, y)
        if x == 0 or y == 0:
            t0 += cxy
        elif adj[0, x] and adj[0, y]:
            t0 += 1
        ntri2 = etat[0] - cuv + cxy
        Q2 = etat[1]
        deg[u] -= 1
        Q2 += deg[u] ** 2 - (deg[u] + 1) ** 2
        deg[v] -= 1
        Q2 += deg[v] ** 2 - (deg[v] + 1) ** 2
        deg[x] += 1
        Q2 += deg[x] ** 2 - (deg[x] - 1) ** 2
        deg[y] += 1
        Q2 += deg[y] ** 2 - (deg[y] - 1) ** 2
        ok = False
        if t0 <= tcap:
            if f > 0.0 and H[t0] == 0 and vu[t0] == 0:
                # case jamais visitée : biais hérité de la case courante (évite les pièges de Wang–Landau)
                w[t0] = w[int(etat[2])]
                vu[t0] = 1
            dS = lam * (ssim(ntri2, Q2, M, n) - ssim(etat[0], etat[1], M, n)) + w[t0] - w[int(etat[2])]
            ok = dS >= 0.0 or np.random.random() < math.exp(dS)
        if ok:
            adj[x, y] = True
            adj[y, x] = True
            aretes[i, 0] = x
            aretes[i, 1] = y
            etat[0] = ntri2
            etat[1] = Q2
            etat[2] = t0
            acc += 1
        else:
            adj[u, v] = True
            adj[v, u] = True
            deg[u] += 1
            deg[v] += 1
            deg[x] -= 1
            deg[y] -= 1
        k = int(etat[2])
        H[k] += 1
        if f > 0.0:
            w[k] -= f
            vu[k] = 1
    return acc


def un_point(args):
    reg, n, lam, graine = args
    c = 3 if reg == "c3" else 2
    m = c * n
    rng = np.random.default_rng(graine)
    L.graine_numba(graine)
    graine_numba_ici(graine)
    t_debut = time.time()
    adj, ar, deg, etat2 = L.depart(n, m, rng, True)
    etat = np.array([etat2[0], etat2[1], 0.0])
    # sommet 0 : le placer dans le noyau planté (échangeabilité : sans effet sur P à l'équilibre)
    etat[2] = t0_de(adj, n)
    # support : T_v maximal observé dans une chaîne non biaisée issue du noyau planté, + 15 %
    tv = np.zeros(n, dtype=np.int64)
    tmax_obs = 0
    wz = np.zeros(100000)
    Hz = np.zeros(100000)
    vz = np.zeros(100000, dtype=np.int64)
    balayer_biais(adj, ar, deg, etat, n, 400 * m, lam, wz, Hz, 0.0, 99999, vz)
    for i in range(100):
        balayer_biais(adj, ar, deg, etat, n, 10 * m, lam, wz, Hz, 0.0, 99999, vz)
        L.tri_tous(adj, n, tv)
        tmax_obs = max(tmax_obs, int(tv.max()))
    tcap = int(1.15 * tmax_obs) + 2
    w = np.zeros(tcap + 1)
    H = np.zeros(tcap + 1)
    vu = np.zeros(tcap + 1, dtype=np.int64)
    if etat[2] > tcap:
        raise RuntimeError("T_0 initial au-dessus du support")
    # Wang–Landau : platitude exigée sur tout le support [0, tcap]
    f = 1.0
    pas = 20 * m
    etapes = 0
    platitude_manquee = 0
    while f > F_FINAL:
        H[:] = 0
        k = 0
        while True:
            balayer_biais(adj, ar, deg, etat, n, pas, lam, w, H, f, tcap, vu)
            k += 1
            if k >= 20 and H.min() > PLATITUDE * H.mean():
                break
            if k > 20000:
                platitude_manquee += 1
                break
        etapes += k
        f /= 2.0
    w_wl = w.copy()
    # production à biais fixé
    Hp = np.zeros(tcap + 1)
    nprod = 0
    blocs = []
    for bloc in range(8):
        Hb = np.zeros(tcap + 1)
        balayer_biais(adj, ar, deg, etat, n, PROD * m, lam, w, Hb, 0.0, tcap, vu)
        Hp += Hb
        blocs.append(Hb.tolist())
        nprod += PROD
    vis = Hp > 0
    logP = np.full(tcap + 1, np.nan)
    logP[vis] = np.log(Hp[vis]) - w[vis]
    logP -= np.nanmax(logP)
    # contrôle exact de l'état
    A = adj.astype(np.int64)
    assert abs(etat[0] - np.trace(A @ A @ A) / 6) < 0.5
    assert abs(etat[2] - t0_de(adj, n)) < 0.5
    # histogramme direct non biaisé (tous les sommets), pour contrôle
    Hd = np.zeros(tcap + 1)
    out = np.zeros(n, dtype=np.int64)
    w0 = np.zeros(tcap + 1)
    Hjunk = np.zeros(tcap + 1)
    balayer_biais(adj, ar, deg, etat, n, 1000 * m, lam, w0, Hjunk, 0.0, tcap, vu)
    for i in range(2000):
        balayer_biais(adj, ar, deg, etat, n, 5 * m, lam, w0, Hjunk, 0.0, tcap, vu)
        L.tri_tous(adj, n, out)
        for t in out:
            if t <= tcap:
                Hd[t] += 1
    return {"reglage": reg, "n": n, "M": m, "lam": lam, "graine": graine, "tcap": tcap, "tmax_obs": tmax_obs,
            "platitude_manquee": platitude_manquee, "platitude_production": float(Hp.min() / Hp.mean()),
            "H_blocs": blocs,
            "etapes_wl": etapes, "balayages_production": nprod, "logP": [None if not np.isfinite(x) else float(x) for x in logP],
            "H_production": Hp.tolist(), "w": w_wl.tolist(), "H_direct": Hd.tolist(),
            "duree_s": time.time() - t_debut}


@njit(cache=True)
def graine_numba_ici(g):
    np.random.seed(g)


def profil_barriere(logP, tcap_min=3):
    """F = −log P. Minimum roturier (T ≤ T_col), minimum aristocratique, col entre les deux.
    Recherche : minimum aristocratique = argmin F sur la moitié haute du support ; col =
    argmax F entre le minimum roturier global des petites valeurs et lui."""
    F = np.array([np.nan if x is None else -x for x in logP])
    ok = np.where(np.isfinite(F))[0]
    tmax = ok.max()
    # lissage minimal : aucun (valeurs entières de T) ; on travaille sur F brut
    haut = ok[ok >= tmax // 2]
    t_ari = int(haut[np.argmin(F[haut])])
    bas = ok[ok <= t_ari]
    # minimum roturier : argmin F sur T ≤ T_ari / 3
    tiers = bas[bas <= t_ari // 3]
    t_rot = int(tiers[np.argmin(F[tiers])])
    milieu = ok[(ok > t_rot) & (ok < t_ari)]
    t_col = int(milieu[np.argmax(F[milieu])]) if len(milieu) else t_ari
    return {"t_rot": t_rot, "t_col": t_col, "t_ari": t_ari, "F_rot": float(F[t_rot]), "F_col": float(F[t_col]),
            "F_ari": float(F[t_ari]), "B_sortie": float(F[t_col] - F[t_ari]), "B_entree": float(F[t_col] - F[t_rot]),
            "P_ari_masse": None}


def main():
    def opt(nom, defaut):
        return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut
    pts = opt("--points", "c2:17,c2:25,c2:33,c2:49,c2:65,c2:97,c2:129,c2:193").split(",")
    sortie = opt("--sortie", "defi_m13_profil.json")
    taches = []
    for j, p in enumerate(pts):
        champs = p.split(":")
        reg, n = champs[0], int(champs[1])
        lam = float(champs[2]) if len(champs) > 2 else n / TAU
        for j in range(int(opt("--repetitions", "3"))):
            taches.append((reg, n, lam, 20261030 + 1000 * n + int(lam) + (7 if reg == "c3" else 0) + 100003 * j))
    res = []
    with Pool(int(opt("--processus", "2"))) as pool:
        for r in pool.imap_unordered(un_point, taches):
            try:
                b = profil_barriere(r["logP"])
            except ValueError:
                b = {"B_sortie": float("nan"), "B_entree": float("nan"), "t_rot": None, "t_col": None, "t_ari": None}
            r["barriere"] = b
            res.append(r)
            print(r["reglage"], r["n"], "λ", r["lam"], "B_sortie %.2f B_entree %.2f" % (b["B_sortie"], b["B_entree"]),
                  "T rot/col/ari", b["t_rot"], b["t_col"], b["t_ari"], "WL", r["etapes_wl"], "%.0f s" % r["duree_s"], flush=True)
            (ICI / sortie).write_text(json.dumps({"cadre": __doc__.split("Usage")[0], "points": res}, ensure_ascii=False))


if __name__ == "__main__":
    main()
