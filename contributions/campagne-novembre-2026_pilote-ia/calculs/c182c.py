#!/usr/bin/env python3
"""C-182c -- contre-calcul independant du C-182 de ChatGPT (Claude, 16 novembre 2026). Ecrit d'apres son seul PROTOCOLE FIGE (lu) ; ses resultats, son rapport et son programme
n'ont pas ete lus avant le scelle de c182c_c183c_prediction.txt. H-FACE et bascule 2->3 sont des hypotheses d'auditeur de ChatGPT, pas des lois du Blob.
Usage : python3 c182c.py   -> c182c.json"""
import itertools, json, math
import numpy as np

VREF = math.sqrt(2) / 12; DS = 2 * math.pi / math.acos(1 / 3); H = math.sqrt(2 / 3)


def vol(X, t): a, b, c, d = (X[i] for i in t); return abs(np.dot(b - a, np.cross(c - a, d - a))) / 6


def chevauche(P, Q, tol=1e-9):
    """SAT : 8 normales de faces et 36 produits d'aretes ; True si les interieurs se penetrent."""
    axes = []
    for T in (P, Q):
        for i, j, k in itertools.combinations(range(4), 3): axes.append(np.cross(T[j] - T[i], T[k] - T[i]))
    eP = [P[j] - P[i] for i, j in itertools.combinations(range(4), 2)]; eQ = [Q[j] - Q[i] for i, j in itertools.combinations(range(4), 2)]
    axes += [np.cross(u, v) for u in eP for v in eQ]
    for ax in axes:
        n = np.linalg.norm(ax)
        if n < 1e-12: continue
        ax = ax / n; p = P @ ax; q = Q @ ax
        if p.max() <= q.min() + tol or q.max() <= p.min() + tol: return False
    return True


def faces(T):
    F = {}
    for t in T:
        for f in itertools.combinations(sorted(t), 3): F.setdefault(f, []).append(t)
    return F


def mesure(X, T):
    X = np.array(X); F = faces(T); Ni = sum(1 for v in F.values() if len(v) == 2); B = sum(1 for v in F.values() if len(v) == 1); surch = sum(1 for v in F.values() if len(v) > 2)
    E = {}
    for t in T:
        for e in itertools.combinations(sorted(t), 2): E[e] = E.get(e, 0) + 1
    bord = set(e for f, v in F.items() if len(v) == 1 for e in itertools.combinations(f, 2)); inte = [e for e in E if e not in bord]
    # connexite du dual
    adj = {t: set() for t in T}
    for v in F.values():
        if len(v) == 2: adj[v[0]].add(v[1]); adj[v[1]].add(v[0])
    vu = {T[0]}; pile = [T[0]]
    while pile:
        x = pile.pop()
        for y in adj[x]:
            if y not in vu: vu.add(y); pile.append(y)
    # lien de chaque arete : chemin ou cycle
    lien_ok = True
    for e in E:
        tt = [t for t in T if e[0] in t and e[1] in t]; deg = {}
        for a_, b_ in itertools.combinations(tt, 2):
            if len(set(a_) & set(b_)) == 3: deg[a_] = deg.get(a_, 0) + 1; deg[b_] = deg.get(b_, 0) + 1
        d = sorted(deg.get(t, 0) for t in tt)
        if not (len(tt) == 1 or d == [1, 1] + [2] * (len(tt) - 2) or (e not in bord and d == [2] * len(tt))): lien_ok = False
    return dict(Nv=len(set(i for t in T for i in t)), Ne=len(E), Nt=len(T), Ni=Ni, B=B, C_dual=Ni - len(T) + 1, faces_surchargees=surch, dual_connexe=len(vu) == len(T), liens_aretes_ok=lien_ok,
                V_sum_sur_Vref=float(sum(vol(X, t) for t in T) / VREF), V_min_sur_Vref=float(min(vol(X, t) for t in T) / VREF), E_U=float(sum(0.5 * (np.linalg.norm(X[a] - X[b]) - 1) ** 2 for a, b in E)),
                aretes_interieures=len(inte), n_e_interieures=sorted(E[e] for e in inte), P_int=float(sum((E[e] - DS) ** 2 for e in inte)), longueur_max=float(max(np.linalg.norm(X[a] - X[b]) for a, b in E)))


def rips(X, r):
    X = np.array(X); n = len(X); D = np.linalg.norm(X[:, None] - X[None], axis=2); A = [set(j for j in range(n) if j != i and D[i, j] <= r) for i in range(n)]
    tri = [(i, j, k) for i in range(n) for j in A[i] if j > i for k in A[i] & A[j] if k > j]; nb = [len(A[i] & A[j] & A[k]) for i, j, k in tri]
    k4 = sum(nb) // 4
    return dict(aretes=sum(len(a) for a in A) // 2, triangles=len(tri), K4=k4, part_triangles_dans_plus_de_2_K4=float(np.mean([x > 2 for x in nb])) if tri else 0.0, triangles_surcharges=int(sum(x > 2 for x in nb)))


def bascules_admissibles(X, T):
    X = np.array(X); F = faces(T); E = set(e for t in T for e in itertools.combinations(sorted(t), 2)); out = []
    for f, v in F.items():
        if len(v) != 2: continue
        p = (set(v[0]) - set(f)).pop(); q = (set(v[1]) - set(f)).pop()
        if (min(p, q), max(p, q)) in E: continue
        a, b, c = f; n = np.cross(X[b] - X[a], X[c] - X[a]); sp = np.dot(X[p] - X[a], n); sq = np.dot(X[q] - X[a], n)
        if sp * sq >= 0: continue
        s = sp / (sp - sq); M = X[p] + s * (X[q] - X[p])
        m = np.array([X[b] - X[a], X[c] - X[a], n]).T; uvw = np.linalg.solve(m, M - X[a]); l = (1 - uvw[0] - uvw[1], uvw[0], uvw[1])
        if min(l) <= 1e-8: continue
        nouv = [tuple(sorted(t)) for t in ((a, b, p, q), (b, c, p, q), (c, a, p, q))]; vs = [vol(X, t) for t in nouv]
        if min(vs) < 0.2 * VREF: continue
        if abs(sum(vs) - vol(X, v[0]) - vol(X, v[1])) > 1e-9 * (vol(X, v[0]) + vol(X, v[1])): continue
        out.append((round(float(np.linalg.norm(X[p] - X[q])), 10), min(p, q), max(p, q), f, v, nouv))
    return sorted(out, key=lambda z: z[:3])


def graine(seed, naissances=16):
    rng = np.random.Generator(np.random.PCG64(seed))
    X = [np.array([0., 0, 0]), np.array([1., 0, 0]), np.array([.5, math.sqrt(3) / 2, 0]), np.array([.5, math.sqrt(3) / 6, H])]
    S = [(0, 1, 2, 3)]; SF = [(0, 1, 2, 3)]; hist = []; stop = None; rejets = dict(sommet_proche=0, chevauchement=0)
    for m in range(1, naissances + 1):
        F = faces(S); bord = sorted(f for f, v in F.items() if len(v) == 1); ordre = rng.permutation(len(bord)); choisi = None
        for i in ordre:
            f = bord[i]; t = F[f][0]; d = (set(t) - set(f)).pop(); a, b, c = f; n = np.cross(X[b] - X[a], X[c] - X[a]); n /= np.linalg.norm(n)
            if np.dot(X[d] - X[a], n) > 0: n = -n
            q = (X[a] + X[b] + X[c]) / 3 + H * n
            if min(np.linalg.norm(q - x) for x in X) <= 1e-7: rejets['sommet_proche'] += 1; continue
            Q = np.array([X[a], X[b], X[c], q])
            if abs(np.dot(Q[1] - Q[0], np.cross(Q[2] - Q[0], Q[3] - Q[0]))) / 6 < 0.2 * VREF: continue
            if any(chevauche(np.array([X[i_] for i_ in t2]), Q) for t2 in S): rejets['chevauchement'] += 1; continue
            choisi = (f, q); break
        if choisi is None: stop = m; break
        f, q = choisi; iq = len(X); X.append(q); nt = tuple(sorted(f + (iq,))); S.append(nt); SF.append(nt)
        bf = set(g for g, v in faces(S).items() if len(v) == 1)
        adm = bascules_admissibles(X, SF); bascule = None
        if adm:
            L, p, q_, f2, v, nouv = adm[0]; EU0 = mesure(X, SF)['E_U']; SF = [t for t in SF if t not in v] + nouv; bascule = dict(arete=[p, q_], longueur=L, dE_U=mesure(X, SF)['E_U'] - EU0, candidats=len(adm))
            assert set(g for g, vv in faces(SF).items() if len(vv) == 1) == bf, 'FAIL apparence'
        hist.append(dict(naissance=m, bascule=bascule, S={k: v for k, v in mesure(X, S).items() if k != 'n_e_interieures'}, SF=mesure(X, SF)))
    chev_SF = sum(1 for t1, t2 in itertools.combinations(SF, 2) if chevauche(np.array([X[i] for i in t1]), np.array([X[i] for i in t2])))
    chev_S = sum(1 for t1, t2 in itertools.combinations(S, 2) if chevauche(np.array([X[i] for i in t1]), np.array([X[i] for i in t2])))
    return dict(graine=seed, naissances_reussies=len(hist), stop=stop, rejets=rejets, bascules=sum(1 for h in hist if h['bascule']), naissance_de_la_premiere_bascule=next((h['naissance'] for h in hist if h['bascule']), None),
                final_S=mesure(X, S), final_SF=mesure(X, SF), chevauchements_S=chev_S, chevauchements_SF=chev_SF, rips_1_01=rips(X, 1.01), rips_1_60=rips(X, 1.60), historique=hist)


if __name__ == '__main__':
    out = []
    for seed in range(18200, 18208):
        r = graine(seed); out.append(r); s, f = r['final_S'], r['final_SF']
        print(seed, 'naiss', r['naissances_reussies'], 'bascules', r['bascules'], 'premiere', r['naissance_de_la_premiere_bascule'], '| S Nv Ne Nt B C', s['Nv'], s['Ne'], s['Nt'], s['B'], s['C_dual'], 'V %.6f' % s['V_sum_sur_Vref'],
              '| SF Ne Nt B C', f['Ne'], f['Nt'], f['B'], f['C_dual'], 'V %.6f' % f['V_sum_sur_Vref'], 'Vmin %.3f' % f['V_min_sur_Vref'], 'E_U %.6f' % f['E_U'], 'surch', f['faces_surchargees'], 'liens', f['liens_aretes_ok'], f['dual_connexe'],
              'chev', r['chevauchements_S'], r['chevauchements_SF'], '| rips1.01 K4', r['rips_1_01']['K4'], 'surch', r['rips_1_01']['triangles_surcharges'], '| rips1.6 K4', r['rips_1_60']['K4'], 'surch', r['rips_1_60']['triangles_surcharges'], 'rejets', r['rejets'], flush=True)
        json.dump(out, open('c182c.json', 'w'))
