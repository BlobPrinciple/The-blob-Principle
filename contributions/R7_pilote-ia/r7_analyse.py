# -*- coding: utf-8 -*-
"""DEFI-R7 — analyse : L(t, N) = 1/k1 (k1 : premier moment de l'excès S(k) − 1, k ≤ 20),
1/kmax, vides, S_max ; moyenne et erreur-type sur les graines ; L/r_N ; pente
d ln L / d ln t ; validation du moteur rogné contre les fichiers archivés de DEFI-R6 ;
seconde implémentation."""
import glob, json, math, os
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
R6 = os.path.join(ICI, "..", "R6_pilote-ia")
out = {}


def charge(motif):
    G = {}; meta = None  # fichiers d'une même série : graines disjointes
    for f in sorted(glob.glob(os.path.join(ICI, motif))):
        d = json.load(open(f)); meta = d
        G.update(d["graines"])
    return meta, G


def ms(x):
    x = np.asarray(x, float)
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(len(x))) if len(x) > 1 else float("nan")


print("== Validation : moteur A rogné contre l'archive DEFI-R6 (départ uniforme, N = 2 500) ==")
meta, G = charge("r7_N2500_rogne.json")
val = {}
for t, f in (("80", "r6_campagne_N2500_b80_initpoisson.json"), ("320", "r6_campagne_N2500_b320_initpoisson.json")):
    a = json.load(open(os.path.join(R6, f)))["graines"]
    va = ms([g["viab"]["vides"] for g in a.values()]); vb = ms([g["viab"]["traj"][t]["vides"] for g in G.values()])
    ka = [g["viab"]["kmax"] for g in a.values()]; kb = [g["viab"]["traj"][t]["kmax"] for g in G.values()]
    ma = ms([g["mobile"]["vides"] for g in a.values()]); mb = ms([g["mobile"]["traj"][t]["vides"] for g in G.values()])
    ecart = (vb[0] - va[0]) / math.hypot(va[1], vb[1])
    print(f"t={t}: vides viab archive {va[0]:.4f}±{va[1]:.4f}  A rogné {vb[0]:.4f}±{vb[1]:.4f} ({ecart:+.1f} σ) | "
          f"kmax archive {ka}  A {kb} | vides mobile {ma[0]:.4f} / {mb[0]:.4f}")
    val[t] = {"vides_archive": va, "vides_A_rogne": vb, "ecart_sigma": ecart, "kmax_archive": ka, "kmax_A": kb,
              "vides_mobile_archive": ma, "vides_mobile_A": mb}
out["validation_rogne"] = val

print("\n== Boîte périodique : L(t, N) ==")
camp = {}
for N in (2500, 5000, 10000):
    meta, G = charge(f"r7_N{N}.json")
    for suf in "abcd":
        m2, G2x = charge(f"r7_N{N}_{suf}.json")
        if G2x:
            assert m2["periodique"]
            meta = meta or m2
            G.update(G2x)
    if not G:
        continue
    r = meta["r_N"]; inst = meta["instants"]
    done = [t for t in inst if all(str(t) in g["viab"]["traj"] for g in G.values())]
    print(f"N = {N}, r_N = {r:.4f}, {len(G)} graines, 1/(2,9 r_N) = {1/(2.9*r):.2f}")
    print("  t     vides viab      vides mob   kmax(moy)  k1             L1/r_N        Smax")
    tab = {}
    for t in done:
        ts = str(t)
        vv = ms([g["viab"]["traj"][ts]["vides"] for g in G.values()])
        vm = ms([g["mobile"]["traj"][ts]["vides"] for g in G.values()])
        km = [g["viab"]["traj"][ts]["kmax"] for g in G.values()]
        k1 = ms([g["viab"]["traj"][ts]["k1"] for g in G.values()])
        L = ms([1 / g["viab"]["traj"][ts]["k1"] / r for g in G.values()])
        sm = ms([g["viab"]["traj"][ts]["Smax"] for g in G.values()])
        # robustesse : premier moment coupé à k·r_N ≤ 0,8 (même coupure en unités de r_N à tout N)
        # et sommet du pic interpolé par une parabole sur trois coquilles
        kc = int(0.8 / r)
        def k1c(S):
            S = np.asarray(S); k = np.arange(1, kc + 1); ex = np.clip(S[:kc] - 1, 0, None)
            return (k * ex).sum() / ex.sum()
        def kpic(S):
            S = np.asarray(S); i = int(np.argmax(S))
            if i == 0 or i == len(S) - 1:
                return float(i + 1)
            a, b, c = S[i - 1], S[i], S[i + 1]
            return i + 1 + 0.5 * (a - c) / (a - 2 * b + c)
        Lc = ms([1 / k1c(g["viab"]["traj"][ts]["S"]) / r for g in G.values()])
        Lp = ms([1 / kpic(g["viab"]["traj"][ts]["S"]) / r for g in G.values()])
        tab[ts + "_robustesse"] = {"coupure_k": kc, "L1c_sur_rN": Lc, "Lpic_sur_rN": Lp}
        tab[ts] = {"vides_viab": vv, "vides_mobile": vm, "kmax": km, "k1": k1, "L1_sur_rN": L, "Smax": sm}
        print(f"  {t:5d} {vv[0]:.3f}±{vv[1]:.3f}  {vm[0]:.3f}    {np.mean(km):4.2f} {sorted(km)}  {k1[0]:.2f}±{k1[1]:.2f}  "
              f"{L[0]:.2f}±{L[1]:.2f}  {sm[0]:.1f}±{sm[1]:.1f} | L1c/r {Lc[0]:.2f}±{Lc[1]:.2f} (k≤{kc}) Lpic/r {Lp[0]:.2f}±{Lp[1]:.2f}")
    # pente ln L1 contre ln t, par graine, sur t ≥ 80
    tt = [t for t in done if t >= 80]
    if len(tt) >= 3:
        pentes = []
        for g in G.values():
            y = np.log([1 / g["viab"]["traj"][str(t)]["k1"] for t in tt])
            pentes.append(np.polyfit(np.log(tt), y, 1)[0])
        p = ms(pentes)
        print(f"  pente d ln L1 / d ln t sur t = {tt[0]}..{tt[-1]} : {p[0]:.3f} ± {p[1]:.3f} (par graine)")
        tab["pente_lnL1_lnt"] = {"t": tt, "valeur": p}
        kc = int(0.8 / r); pc = []
        for g in G.values():
            y = []
            for t in tt:
                S = np.asarray(g["viab"]["traj"][str(t)]["S"]); k = np.arange(1, kc + 1); ex = np.clip(S[:kc] - 1, 0, None)
                y.append(np.log(ex.sum() / (k * ex).sum()))
            pc.append(np.polyfit(np.log(tt), y, 1)[0])
        pc = ms(pc)
        print(f"  pente d ln L1c / d ln t : {pc[0]:.3f} ± {pc[1]:.3f}")
        tab["pente_lnL1c_lnt"] = {"t": tt, "valeur": pc}
    acc = ms([g["viab"]["acceptees"] / g["viab"]["tentatives"] for g in G.values()])
    deb = sum(g["viab"]["debordements"] for g in G.values())
    tab["acceptation_viab"] = acc; tab["debordements"] = deb
    print(f"  acceptation viab {acc[0]:.3f} ; débordements de cellule {deb}")
    camp[str(N)] = {"r_N": r, "graines": len(G), "table": tab}
out["periodique"] = camp

print("\n== Seconde implémentation (force brute, S(k) exact), N = 2 500, périodique ==")
meta, G2 = charge("r7_second_N2500.json")
meta, GA = charge("r7_N2500.json")
sec = {}
if G2:
    for t in ("80", "320"):
        g2 = [g for g in G2.values() if t in g["traj"]]
        if not g2:
            continue
        vb = ms([g["traj"][t]["vides"] for g in g2]); va = ms([g["viab"]["traj"][t]["vides"] for g in GA.values()])
        kb = [g["traj"][t]["kmax"] for g in g2]; ka = [g["viab"]["traj"][t]["kmax"] for g in GA.values()]
        Sa = np.array([g["viab"]["traj"][t]["S"][:12] for g in GA.values()]); Sb = np.array([g["traj"][t]["S"] for g in g2])
        z = [(Sb[:, k].mean() - Sa[:, k].mean()) / math.hypot(Sa[:, k].std(ddof=1) / math.sqrt(len(Sa)),
             Sb[:, k].std(ddof=1) / math.sqrt(len(Sb)) if len(Sb) > 1 else 0) for k in range(6)]
        e = (vb[0] - va[0]) / math.hypot(va[1], vb[1] if not math.isnan(vb[1]) else 0)
        print(f"t={t} ({len(g2)} graines) : vides B {vb[0]:.4f}±{vb[1]:.4f} contre A {va[0]:.4f}±{va[1]:.4f} ({e:+.1f} σ) ; "
              f"kmax B {kb} A {sorted(ka)} ; S(k=1..6) B {np.round(Sb.mean(0)[:6],2).tolist()} A {np.round(Sa.mean(0)[:6],2).tolist()} ; "
              f"écarts {np.round(z,1).tolist()} σ")
        sec[t] = {"graines_B": len(g2), "vides_B": vb, "vides_A": va, "ecart_sigma": e, "kmax_B": kb, "kmax_A": ka,
                  "S_B": Sb.mean(0)[:6].tolist(), "S_A": Sa.mean(0)[:6].tolist(), "ecarts_S_sigma": z}
out["second_moteur"] = sec
json.dump(out, open(os.path.join(ICI, "r7_analyse_sortie.json"), "w"), indent=1)
