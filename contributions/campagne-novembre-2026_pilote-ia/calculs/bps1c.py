#!/usr/bin/env python3
"""BP-S1c -- Contre-audit exact de BP-S1 / TEST-1 (ChatGPT) et trois prolongements.  (Claude, 13 novembre 2026)

Attendus : bps1c_prediction.txt (ecrit avant tout programme).
Modele (protocole fige de ChatGPT, empreinte 31240c21...7881) : six sites etiquetes, triangle d'ancrage (0,1,2), etats = ensembles de faces
admissibles, E = eps F + gamma B - J [ferme], taux exp[-beta (0,3 + max(dE, 0))], arret a la premiere coque spherique fermee.
Ici : probabilites de premiere fermeture EXACTES (systeme lineaire), puis Monte-Carlo independant.
Usage : python3 bps1c.py   (ecrit bps1c.json)
"""
import itertools
import json
import math
import pathlib
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.optimize import brentq
from scipy.sparse.linalg import spsolve

ICI = pathlib.Path(__file__).resolve().parent
FACES = list(itertools.combinations(range(6), 3))
EDGES = list(itertools.combinations(range(6), 2))
EI = {e: i for i, e in enumerate(EDGES)}
FE = [[EI[p] for p in itertools.combinations(f, 2)] for f in FACES]
SEED = FACES.index((0, 1, 2))
bilan = {}
t0 = time.time()


def analyse(mask):
    """None si l'etat n'est pas admissible ; sinon (F, B, ferme, V)."""
    fs = [f for f in range(20) if mask >> f & 1]
    cnt = [0] * 15
    for f in fs:
        for e in FE[f]:
            cnt[e] += 1
    if max(cnt) > 2:
        return None
    # connexite des faces par aretes partagees
    vu = {fs[0]}
    pile = [fs[0]]
    while pile:
        f = pile.pop()
        for g in fs:
            if g not in vu and set(FE[f]) & set(FE[g]):
                vu.add(g)
                pile.append(g)
    if len(vu) != len(fs):
        return None
    # lien de chaque sommet occupe : connexe (chemin ou cycle)
    occ = set(v for f in fs for v in FACES[f])
    for v in occ:
        ar = [tuple(x for x in FACES[f] if x != v) for f in fs if v in FACES[f]]
        noeuds = set(x for a in ar for x in a)
        vus = {ar[0][0]}
        pile = [ar[0][0]]
        while pile:
            x = pile.pop()
            for a in ar:
                if x in a:
                    y = a[0] if a[1] == x else a[1]
                    if y not in vus:
                        vus.add(y)
                        pile.append(y)
        if vus != noeuds:
            return None
    B = sum(1 for c in cnt if c == 1)
    F, V, A = len(fs), len(occ), sum(1 for c in cnt if c > 0)
    if B == 0 and V - A + F != 2:
        return None                                   # fermeture non spherique : rejetee
    return F, B, B == 0, V


# ------------------------------------------------------------------ X1 : enumeration directe des 62 985 ensembles
autres = [f for f in range(20) if f != SEED]
compte, octa, total = {4: 0, 5: 0, 6: 0}, 0, 0
for k in (3, 5, 7):
    for c in itertools.combinations(autres, k):
        total += 1
        mask = 1 << SEED
        for f in c:
            mask |= 1 << f
        cnt = [0] * 15
        for f in (SEED,) + c:
            for e in FE[f]:
                cnt[e] += 1
        if any(x not in (0, 2) for x in cnt):
            continue
        r = analyse(mask)
        if r is not None and r[2]:
            compte[r[3]] += 1
            if r[3] == 6:
                deg = [sum(1 for e, x in zip(EDGES, cnt) if x and v in e) for v in range(6)]
                octa += deg == [4] * 6
bilan['X1_coques'] = dict(ensembles_examines=total, par_sommets=compte, octaedres=octa, autres_a_six=compte[6] - octa)


# ------------------------------------------------------------------ graphe des etats (pour un nombre de sites donne)
def graphe(nsites):
    permis = [f for f in range(20) if max(FACES[f]) < nsites]
    info = {1 << SEED: analyse(1 << SEED)}
    ordre = [1 << SEED]
    trans = {}
    i = 0
    while i < len(ordre):
        m = ordre[i]
        i += 1
        if info[m][2]:
            continue                                  # coque fermee : absorbante
        cnt = [0] * 15
        for f in range(20):
            if m >> f & 1:
                for e in FE[f]:
                    cnt[e] += 1
        vois = []
        for f in permis:
            if m >> f & 1:
                if f == SEED:
                    continue
                n = m & ~(1 << f)
            else:
                if not any(cnt[e] for e in FE[f]):
                    continue
                n = m | (1 << f)
            if n not in info:
                info[n] = analyse(n)
                if info[n] is not None:
                    ordre.append(n)
            if info[n] is not None:
                vois.append(n)
        trans[m] = vois
    return info, ordre, trans


G = {n: graphe(n) for n in (4, 5, 6)}
bilan['etats'] = {str(n): dict(admissibles=len(G[n][1]), ouverts=len(G[n][2]), fermes=len(G[n][1]) - len(G[n][2])) for n in G}
print('etats', bilan['etats'], f'{time.time() - t0:.1f} s', file=sys.stderr)


def systeme(nsites):
    info, ordre, trans = G[nsites]
    ouverts = [m for m in ordre if not info[m][2]]
    idx = {m: i for i, m in enumerate(ouverts)}
    src, dst, dF, dB, cible = [], [], [], [], []
    for m in ouverts:
        F, B, _, _ = info[m]
        for n in trans[m]:
            F2, B2, ferme, V = info[n]
            src.append(idx[m])
            dst.append(-1 if ferme else idx[n])
            dF.append(F2 - F)
            dB.append(B2 - B)
            cible.append(V if ferme else 0)
    return dict(n=len(ouverts), idx=idx, src=np.array(src), dst=np.array(dst), dF=np.array(dF), dB=np.array(dB), cible=np.array(cible))


S = {n: systeme(n) for n in (4, 5, 6)}


def taux(s, eps, gam, J, beta):
    dE = eps * s['dF'] + gam * s['dB'] - J * (s['cible'] > 0)
    return np.exp(-beta * (0.3 + np.maximum(dE, 0)))


def premiere_fermeture(nsites, eps, gam, J, beta):
    s = S[nsites]
    k = taux(s, eps, gam, J, beta)
    R = np.bincount(s['src'], weights=k, minlength=s['n'])
    dedans = s['dst'] >= 0
    A = sp.identity(s['n'], format='csr') - sp.csr_matrix((k[dedans] / R[s['src'][dedans]], (s['src'][dedans], s['dst'][dedans])),
                                                          shape=(s['n'], s['n']))
    out = {}
    for V in (4, 5, 6):
        sel = s['cible'] == V
        b = np.bincount(s['src'][sel], weights=k[sel] / R[s['src'][sel]], minlength=s['n'])
        out[V] = float(spsolve(A.tocsc(), b)[0]) if sel.any() else 0.0
    return out


REGIMES = {'A': (0.6, 0.4, 4, 1.0), 'B': (-0.6, 0.4, 4, 1.0), 'C': (0.6, 0.4, 0, 1.0), 'D': (0.6, 0.4, 4, 0.25), 'E': (-0.6, 0.4, 0, 1.0),
           'F': (0.6, 0.0, 4, 1.0)}
CHATGPT = {'A': (299, 389, 512), 'B': (52, 168, 980), 'C': (305, 395, 500), 'D': (84, 264, 852), 'E': (57, 134, 1009), 'F': (195, 424, 581)}

# ------------------------------------------------------------------ X2 : probabilites exactes contre les comptes de ChatGPT
x2 = {}
for nom, par in REGIMES.items():
    p = premiere_fermeture(6, *par)
    ec = [(c - 1200 * p[V]) / math.sqrt(1200 * p[V] * (1 - p[V])) for c, V in zip(CHATGPT[nom], (4, 5, 6))]
    x2[nom] = dict(exact={str(V): p[V] for V in p}, somme=sum(p.values()), attendu_sur_1200=[1200 * p[V] for V in (4, 5, 6)],
                   chatgpt=CHATGPT[nom], ecarts_en_sigma=ec)
bilan['X2_exact'] = x2
bilan['X2_identites'] = dict(A_moins_C=max(abs(x2['A']['exact'][v] - x2['C']['exact'][v]) for v in '456'),
                             B_moins_E=max(abs(x2['B']['exact'][v] - x2['E']['exact'][v]) for v in '456'),
                             ecart_max_en_sigma=max(abs(e) for r in x2.values() for e in r['ecarts_en_sigma']))
print('X2', f'{time.time() - t0:.1f} s', file=sys.stderr)

# ------------------------------------------------------------------ X3, X7 : Monte-Carlo independant (Gillespie, PCG64)
info6, ordre6, trans6 = G[6]
s6 = S[6]
debut = np.searchsorted(s6['src'], np.arange(s6['n'] + 1))            # transitions rangees par etat source
rng = np.random.default_rng(20261113)
x3 = {}
for nom, par in REGIMES.items():
    eps, gam, J, beta = par
    k = taux(s6, *par)
    r_face = math.exp(-beta * (0.3 + max(J - eps + 3 * gam, 0)))
    n = {4: 0, 5: 0, 6: 0}
    res = {4: 0, 5: 0, 6: 0}
    duree = {4: [], 5: [], 6: []}
    evts = []
    for _ in range(1200):
        i, ne = 0, 0
        while True:
            a, b_ = debut[i], debut[i + 1]
            kk = k[a:b_]
            j = a + int(np.searchsorted(np.cumsum(kk), rng.random() * kk.sum()))
            ne += 1
            if s6['dst'][j] < 0:
                V = int(s6['cible'][j])
                break
            i = int(s6['dst'][j])
        F = 2 * V - 4
        h = rng.exponential(1 / ((F - 1) * r_face))
        n[V] += 1
        res[V] += h >= 10
        duree[V].append(h)
        evts.append(ne)
    p = x2[nom]['exact']
    x3[nom] = dict(comptes=[n[4], n[5], n[6]], residents=[res[4], res[5], res[6]],
                   ecarts_en_sigma=[(n[V] - 1200 * p[str(V)]) / math.sqrt(1200 * p[str(V)] * (1 - p[str(V)])) for V in (4, 5, 6)],
                   evenements_moyens=float(np.mean(evts)), evenements_max=int(max(evts)),
                   duree_moyenne={str(V): float(np.mean(duree[V])) for V in (4, 5, 6)},
                   duree_theorique={str(V): 1 / ((2 * V - 5) * r_face) for V in (4, 5, 6)})
bilan['X3_monte_carlo'] = x3
bilan['X3_ecart_max_en_sigma'] = max(abs(e) for r in x3.values() for e in r['ecarts_en_sigma'])
# X7 : sorties d'une coque fermee, comptees sur la chaine elle-meme
sorties = {}
for m in ordre6:
    F, B, ferme, V = info6[m]
    if ferme:
        ok = sum(1 for f in range(20) if f != SEED and m >> f & 1 and analyse(m & ~(1 << f)) is not None)
        sorties.setdefault(V, set()).add((F, ok))
bilan['X7_faces_retirables_par_coque'] = {str(V): sorted(v) for V, v in sorties.items()}
print('X3', f'{time.time() - t0:.1f} s', file=sys.stderr)

# ------------------------------------------------------------------ X4 : seuil de cout
x4 = {}
for eps in np.round(np.arange(0.0, 3.01, 0.2), 2):
    p = premiere_fermeture(6, float(eps), 0.4, 4, 1.0)
    w = np.array([3 * math.exp(-4 * eps), 18 * math.exp(-6 * eps), 78 * math.exp(-8 * eps)])
    x4[f'{eps:.1f}'] = dict(premiere_fermeture=[p[4], p[5], p[6]], equilibre=list(w / w.sum()))
f45 = lambda e: (lambda p: p[4] - p[5])(premiere_fermeture(6, e, 0.4, 4, 1.0))
f46 = lambda e: (lambda p: p[4] - p[6])(premiere_fermeture(6, e, 0.4, 4, 1.0))
s45 = brentq(f45, 0.0, 3.0, xtol=1e-6) if f45(0.0) * f45(3.0) < 0 else None
s46 = brentq(f46, 0.0, 3.0, xtol=1e-6) if f46(0.0) * f46(3.0) < 0 else None
bilan['X4_seuil_de_cout'] = dict(balayage=x4, seuil_cinetique_4_contre_5=s45, seuil_cinetique_4_contre_6=s46,
                                 seuil_cinetique=None if s45 is None or s46 is None else max(s45, s46),
                                 seuil_d_equilibre_4_contre_5=math.log(6) / 2, seuil_d_equilibre_4_contre_6=math.log(26) / 4)

# ------------------------------------------------------------------ X5 : nombre de sites, regime A
bilan['X5_nombre_de_sites'] = {str(n): premiere_fermeture(n, *REGIMES['A']) for n in (4, 5, 6)}


# ------------------------------------------------------------------ X6 : naissances successives, regime A
def naissances(cb, par=REGIMES['A']):
    tailles = [S[n]['n'] for n in (4, 5, 6)]
    off = np.concatenate([[0], np.cumsum(tailles)])
    N = int(off[-1])
    lig, col, val = [], [], []
    R = np.zeros(N)
    sec = {V: np.zeros(N) for V in (4, 5, 6)}
    inv6 = {m: i for m, i in S[6]['idx'].items()}
    for a, n in enumerate((4, 5, 6)):
        s = S[n]
        k = taux(s, *par)
        np.add.at(R, off[a] + s['src'], k)
        dedans = s['dst'] >= 0
        lig.append(off[a] + s['src'][dedans])
        col.append(off[a] + s['dst'][dedans])
        val.append(k[dedans])
        for V in (4, 5, 6):
            sel = s['cible'] == V
            np.add.at(sec[V], off[a] + s['src'][sel], k[sel])
        if n < 6:                                                # naissance : meme ensemble de faces, un site de plus
            suiv = S[n + 1]['idx']
            ici = np.array([off[a] + i for m, i in s['idx'].items()])
            la = np.array([off[a + 1] + suiv[m] for m in s['idx']])
            lig.append(ici)
            col.append(la)
            val.append(np.full(len(ici), cb))
            R[ici] += cb
    lig, col, val = np.concatenate(lig), np.concatenate(col), np.concatenate(val)
    A = sp.identity(N, format='csc') - sp.csc_matrix((val / R[lig], (lig, col)), shape=(N, N))
    return {V: float(spsolve(A, sec[V] / R)[0]) for V in (4, 5, 6)}


bilan['X6_naissances_successives'] = {f'{cb:g}': naissances(cb) for cb in (0.001, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 100, 1e4)}
f9 = lambda lc: naissances(math.exp(lc))[4] - 0.9
f5 = lambda lc: naissances(math.exp(lc))[4] - 0.5
bilan['X6_cadences_seuils'] = dict(part_0_9=math.exp(brentq(f9, math.log(1e-4), math.log(1e3), xtol=1e-8)),
                                   part_0_5=math.exp(brentq(f5, math.log(1e-4), math.log(1e3), xtol=1e-8)))
# temps moyen de fermeture a quatre sites (pour situer la cadence) : resolution de R t = 1 + somme k t
s4 = S[4]
k4 = taux(s4, *REGIMES['A'])
R4 = np.bincount(s4['src'], weights=k4, minlength=s4['n'])
d4 = s4['dst'] >= 0
A4 = sp.diags(R4) - sp.csr_matrix((k4[d4], (s4['src'][d4], s4['dst'][d4])), shape=(s4['n'], s4['n']))
bilan['X6_temps_moyen_de_fermeture_a_quatre_sites'] = float(spsolve(A4.tocsc(), np.ones(s4['n']))[0])
print('duree', f'{time.time() - t0:.1f} s', file=sys.stderr)      # hors du fichier de sortie : il doit etre reproductible a l'octet

(ICI / 'bps1c.json').write_text(json.dumps(bilan, indent=1, ensure_ascii=False, default=float))
print(json.dumps(bilan, indent=1, ensure_ascii=False, default=float))
