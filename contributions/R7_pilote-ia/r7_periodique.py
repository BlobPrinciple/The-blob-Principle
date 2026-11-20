# -*- coding: utf-8 -*-
"""DEFI-R7 — la condensation viable en boîte périodique (implémentation A, numba).

Règle reprise du moteur de mobilité archivé (relax_positions, local_S, rgg_radius ;
corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob gravite colab.py,
V346 XXV.1 p. 642) : κ = 6,6, β = 0,30, τ = 0,50, σ = 0,3·r_N, N//4 tentatives par
balayage, un sommet isolé ne bouge pas, acceptation de Metropolis sur la seule
S locale du sommet déplacé : S(v) = ln(1 + triangles en v) − β·écart-type/moyenne
des degrés des voisins. Bras « mobile » : acceptation 1/2 sans viabilité.
Le graphe est le graphe géométrique (0 < d < r) des positions, recalculé à la volée
(il l'est aussi dans le moteur archivé, qui reconstruit les voisins à chaque pas).

Seule différence voulue : boîte périodique (distance d'image minimale, pas pris modulo 1)
au lieu du rognage np.clip. L'option --rogne rend le rognage pour valider ce moteur
contre les fichiers archivés de DEFI-R6 (départ uniforme, N = 2 500).

Usage : python3 r7_periodique.py --N 2500 --graines 0:8 --instants 0,20,40,80,160,320,640,1280 --sortie f.json [--rogne]
"""
import argparse, json, math, os, time
import numpy as np
import numba as nb

KAPPA, BETA, TAU = 6.6, 0.30, 0.50
CAP = 256


def rgg_radius(N, kappa=KAPPA):
    return (kappa / ((N - 1) * 4.0 / 3.0 * math.pi)) ** (1.0 / 3.0)


@nb.njit(cache=True)
def cellule(x, M):
    i = int(x[0] * M); j = int(x[1] * M); k = int(x[2] * M)
    if i >= M: i = M - 1
    if j >= M: j = M - 1
    if k >= M: k = M - 1
    return (i * M + j) * M + k


@nb.njit(cache=True)
def d2(a, b, per):
    s = 0.0
    for c in range(3):
        u = a[c] - b[c]
        if per:
            if u > 0.5: u -= 1.0
            elif u < -0.5: u += 1.0
        s += u * u
    return s


@nb.njit(cache=True)
def voisins(i, pos, cnt, mem, M, r2, per, out):
    x = pos[i]
    ci = int(x[0] * M); cj = int(x[1] * M); ck = int(x[2] * M)
    if ci >= M: ci = M - 1
    if cj >= M: cj = M - 1
    if ck >= M: ck = M - 1
    n = 0
    for di in range(-1, 2):
        a = ci + di
        if per: a %= M
        elif a < 0 or a >= M: continue
        for dj in range(-1, 2):
            b = cj + dj
            if per: b %= M
            elif b < 0 or b >= M: continue
            for dk in range(-1, 2):
                c = ck + dk
                if per: c %= M
                elif c < 0 or c >= M: continue
                cel = (a * M + b) * M + c
                for s in range(cnt[cel]):
                    j = mem[cel, s]
                    if j == i: continue
                    dd = d2(x, pos[j], per)
                    if dd < r2 and dd > 0.0:
                        out[n] = j; n += 1
    return n


@nb.njit(cache=True)
def S_locale(v, pos, cnt, mem, M, r2, per, buf, buf2):
    d = voisins(v, pos, cnt, mem, M, r2, per, buf)
    if d < 2:
        return 0.0
    tri = 0
    for a in range(d):
        for c in range(a + 1, d):
            dd = d2(pos[buf[a]], pos[buf[c]], per)
            if dd < r2 and dd > 0.0:
                tri += 1
    m = 0.0; q = 0.0
    for a in range(d):
        g = voisins(buf[a], pos, cnt, mem, M, r2, per, buf2)
        m += g; q += g * g
    m /= d; q /= d
    var = q - m * m
    if var < 0.0: var = 0.0
    cv = math.sqrt(var) / m if m > 0 else 0.0
    return math.log(1.0 + tri) - BETA * cv


@nb.njit(cache=True)
def retirer(i, pt_cel, pt_slot, cnt, mem):
    cel = pt_cel[i]; s = pt_slot[i]; last = cnt[cel] - 1
    j = mem[cel, last]
    mem[cel, s] = j; pt_slot[j] = s
    cnt[cel] = last


@nb.njit(cache=True)
def inserer(i, cel, pt_cel, pt_slot, cnt, mem):
    s = cnt[cel]
    if s >= mem.shape[1]:
        return False
    mem[cel, s] = i; pt_cel[i] = cel; pt_slot[i] = s; cnt[cel] = s + 1
    return True


@nb.njit(cache=True)
def balayer(pos, n_bal, r, M, viab, per, seed, cnt, mem, pt_cel, pt_slot, stats):
    np.random.seed(seed)
    N = pos.shape[0]; r2 = r * r; sigma = 0.3 * r
    buf = np.empty(N, np.int64); buf2 = np.empty(N, np.int64)
    old = np.empty(3)
    for _ in range(n_bal):
        for _ in range(N // 4):
            v = np.random.randint(N)
            if voisins(v, pos, cnt, mem, M, r2, per, buf) == 0:
                continue
            So = S_locale(v, pos, cnt, mem, M, r2, per, buf, buf2) if viab else 0.0
            for c in range(3):
                old[c] = pos[v, c]
            for c in range(3):
                y = pos[v, c] + np.random.normal(0.0, sigma)
                if per:
                    y = y - math.floor(y)
                    if y >= 1.0: y = 0.0
                else:
                    if y < 0.0: y = 0.0
                    elif y > 1.0: y = 1.0
                pos[v, c] = y
            oc = pt_cel[v]
            retirer(v, pt_cel, pt_slot, cnt, mem)
            if not inserer(v, cellule(pos[v], M), pt_cel, pt_slot, cnt, mem):
                stats[2] += 1  # débordement : refus forcé, compté
                for c in range(3):
                    pos[v, c] = old[c]
                inserer(v, oc, pt_cel, pt_slot, cnt, mem)
                continue
            if viab:
                dS = S_locale(v, pos, cnt, mem, M, r2, per, buf, buf2) - So
                acc = (dS >= 0.0) or (np.random.random() < math.exp(dS / TAU))
            else:
                acc = np.random.random() < 0.5
            stats[0] += 1
            if acc:
                stats[1] += 1
            else:
                retirer(v, pt_cel, pt_slot, cnt, mem)
                for c in range(3):
                    pos[v, c] = old[c]
                inserer(v, oc, pt_cel, pt_slot, cnt, mem)


def preparer(pos, r):
    M = max(3, int(1.0 / r))
    cnt = np.zeros(M ** 3, np.int64); mem = np.empty((M ** 3, CAP), np.int64)
    N = len(pos); pt_cel = np.empty(N, np.int64); pt_slot = np.empty(N, np.int64)
    for i in range(N):
        c = cellule(pos[i], M)
        assert inserer(i, c, pt_cel, pt_slot, cnt, mem)
    return M, cnt, mem, pt_cel, pt_slot


# ---------- mesures (grille périodique) ----------
NG_VIDE, NG_PK, KMAX = 20, 64, 31
_K = None


def _coquilles():
    global _K
    if _K is None:
        f = np.fft.fftfreq(NG_PK) * NG_PK
        kx, ky, kz = np.meshgrid(f, f, f[: NG_PK // 2 + 1], indexing="ij")
        km = np.rint(np.sqrt(kx ** 2 + ky ** 2 + kz ** 2)).astype(int)
        w = np.full(km.shape, 2.0); w[:, :, 0] = 1.0; w[:, :, -1] = 1.0
        _K = (km, w)
    return _K


def mesures(pts):
    n = len(pts)
    c = np.clip((pts * NG_VIDE).astype(int), 0, NG_VIDE - 1)
    occ = np.zeros((NG_VIDE,) * 3, bool); occ[c[:, 0], c[:, 1], c[:, 2]] = True
    g = np.zeros((NG_PK,) * 3)
    c = np.clip((pts * NG_PK).astype(int), 0, NG_PK - 1)
    np.add.at(g, (c[:, 0], c[:, 1], c[:, 2]), 1.0)
    p = np.abs(np.fft.rfftn(g)) ** 2
    km, w = _coquilles()
    S = np.array([(p[km == k] * w[km == k]).sum() / w[km == k].sum() / n for k in range(1, KMAX + 1)])
    k = np.arange(1, KMAX + 1)
    ex = np.clip(S[:20] - 1.0, 0, None)  # excès sur le bruit de grenaille (S = 1 pour l'uniforme)
    k1 = float((k[:20] * ex).sum() / ex.sum()) if ex.sum() > 0 else float("nan")
    return {"vides": float(1 - occ.mean()), "S": S.tolist(), "kmax": int(np.argmax(S) + 1),
            "Smax": float(S.max()), "k1": k1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--graines", default="0:8")
    ap.add_argument("--instants", default="0,20,40,80,160,320,640,1280")
    ap.add_argument("--bras", default="viab,mobile")
    ap.add_argument("--rogne", action="store_true")
    ap.add_argument("--sortie", required=True)
    a = ap.parse_args()
    g0, g1 = map(int, a.graines.split(":"))
    inst = [int(x) for x in a.instants.split(",")]
    per = not a.rogne
    r = rgg_radius(a.N)
    res = {"N": a.N, "r_N": r, "periodique": per, "instants": inst, "kappa": KAPPA, "beta": BETA,
           "tau": TAU, "graines": {}}
    if os.path.exists(a.sortie):
        res = json.load(open(a.sortie))
    for g in range(g0, g1):
        if str(g) in res["graines"]:
            continue
        e = {}
        for bras in a.bras.split(","):
            t = time.time()
            pos = np.random.default_rng(1000 + g).uniform(0, 1, (a.N, 3))
            M, cnt, mem, pc, ps = preparer(pos, r)
            stats = np.zeros(3, np.int64)
            traj = {}; fait = 0
            for k, ti in enumerate(inst):
                if ti > fait:
                    balayer(pos, ti - fait, r, M, bras == "viab", per, 97 * g + 13 * k + (0 if bras == "viab" else 50000),
                            cnt, mem, pc, ps, stats)
                    fait = ti
                traj[str(ti)] = mesures(pos)
            e[bras] = {"traj": traj, "tentatives": int(stats[0]), "acceptees": int(stats[1]),
                       "debordements": int(stats[2]), "secondes": time.time() - t}
            last = traj[str(inst[-1])]
            print(f"N={a.N} g={g} {bras} {time.time()-t:.0f}s acc {stats[1]/max(stats[0],1):.3f} "
                  f"debord {stats[2]} | vides {last['vides']:.3f} kmax {last['kmax']} k1 {last['k1']:.2f} Smax {last['Smax']:.2f}",
                  flush=True)
        res["graines"][str(g)] = e
        json.dump(res, open(a.sortie, "w"), indent=1)


if __name__ == "__main__":
    main()
