#!/usr/bin/env python3
"""C-195c -- contre-calcul independant du C-195 de ChatGPT (Claude, 17 novembre 2026), d'apres son seul PROTOCOLE : Cahn-Hilliard sur reseau cubique periodique 12^3 et temoin convexe ;
puis un ajout : la croissance << un sommet + une arete par naissance >> garde-t-elle la memoire de son origine ? (parent uniforme : hypothese d'auditeur). Predictions : c195c_prediction.txt.
Usage : python3 c195c.py -> c195c.json"""
import json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

n = 12; KAPPA = 0.25; DT = 0.01; PAS = (0, 100, 600, 1200, 2000, 3000)
def L(u): return 6 * u - sum(np.roll(u, s, a) for a in range(3) for s in (1, -1))
def F(u, convexe=False): return float(((u * u / 2) if convexe else (u * u - 1) ** 2 / 4).sum() + KAPPA / 2 * sum(((u - np.roll(u, -1, a)) ** 2).sum() for a in range(3)))
def mu(u, convexe=False): return (u if convexe else u ** 3 - u) + KAPPA * L(u)

idx = np.arange(n ** 3).reshape(n, n, n)
def poches(masque):
    I = []; J = []
    for a in range(3):
        m = masque & np.roll(masque, -1, a); I.append(idx[m]); J.append(np.roll(idx, -1, a)[m])
    I = np.concatenate(I); J = np.concatenate(J); k, lab = connected_components(coo_matrix((np.ones(len(I)), (I, J)), shape=(n ** 3, n ** 3)), directed=False)
    t = np.bincount(lab[masque.ravel()], minlength=k); return sorted([int(x) for x in t if x >= 3], reverse=True)

def simule(seed, convexe=False):
    rng = np.random.default_rng(seed); u = rng.normal(0, 0.04, (n, n, n)); u -= u.mean(); m0 = u.sum(); out = []
    for t in range(PAS[-1] + 1):
        if t in PAS: out.append(dict(pas=t, masse_ecart=float(abs(u.sum() - m0)), F=F(u, convexe), variance=float(u.var()), part_separee=float((abs(u) > 0.5).mean()), poches_plus=poches(u > 0.5), poches_moins=poches(u < -0.5), u_min=float(u.min()), u_max=float(u.max())))
        u = u - DT * L(mu(u, convexe))
    return out

def memoire(seed, N=2000):
    rng = np.random.default_rng(seed); parent = np.zeros(N, int); deg = np.zeros(N, int)
    for v in range(1, N): p = int(rng.integers(0, v)); parent[v] = p; deg[v] += 1; deg[p] += 1
    taille = np.ones(N, int)
    for v in range(N - 1, 0, -1): taille[parent[v]] += taille[v]
    gros = np.zeros(N, int)
    for v in range(1, N): gros[parent[v]] = max(gros[parent[v]], taille[v])
    psi = np.maximum(gros, N - taille); ordre = np.argsort(psi, kind='stable'); rang = np.empty(N, int); rang[ordre] = np.arange(N)
    # rang pessimiste : nombre de sommets de psi strictement inferieur ou egal (ex aequo comptes contre le sommet teste)
    pess = lambda v: int((psi <= psi[v]).sum())
    return dict(rang_premier=pess(0), rang_1000=pess(1000), degre_premier=int(deg[0]), degre_moyen=float(deg.mean()))

if __name__ == '__main__':
    out = dict(CH={}, convexe={})
    for s in range(195000, 195008):
        out['CH'][s] = simule(s); out['convexe'][s] = simule(s, True); r = out['CH'][s]; c = out['convexe'][s]
        print(s, '| masse %.1e' % max(x['masse_ecart'] for x in r), '| F', ['%.3f' % x['F'] for x in r], 'monotone', all(r[i + 1]['F'] <= r[i]['F'] + 1e-8 for i in range(5)), '| part |u|>0,5', ['%.2f' % x['part_separee'] for x in r],
              '| poches + ', [x['poches_plus'] for x in r], '| poches -', [x['poches_moins'] for x in r], '| temoin : poches', [len(x['poches_plus']) + len(x['poches_moins']) for x in c], 'variance', ['%.1e' % x['variance'] for x in c], flush=True)
    for t in (1200, 3000):
        i = PAS.index(t); print('pas', t, ': graines avec >= 2 poches positives :', sum(1 for s in out['CH'] if len(out['CH'][s][i]['poches_plus']) >= 2), '/ 8 ; avec >= 25 % separes :', sum(1 for s in out['CH'] if out['CH'][s][i]['part_separee'] >= .25), '; minimum de la part separee %.2f' % min(out['CH'][s][i]['part_separee'] for s in out['CH']))
    # translation
    rng = np.random.default_rng(195000); u = rng.normal(0, 0.04, (n, n, n)); u -= u.mean(); v = np.roll(u, (3, 2, 1), (0, 1, 2))
    for _ in range(200): u = u - DT * L(mu(u)); v = v - DT * L(mu(v))
    out['translation'] = float(abs(np.roll(u, (3, 2, 1), (0, 1, 2)) - v).max()); print('translation, ecart max', out['translation'])
    # marche paresseuse sur un graphe a hub (etoile + cycle), et boules de C_11 / C_101
    m = 9; A = np.zeros((m, m))
    for i in range(1, m): A[0, i] = A[i, 0] = 1; j = i % (m - 1) + 1; A[i, j] = A[j, i] = 1
    d = A.sum(1); P = 0.5 * np.eye(m) + 0.5 * A / d[:, None]; pi = d / d.sum(); flux = pi[:, None] * P - (pi[:, None] * P).T
    out['marche'] = dict(pi_stationnaire=bool(abs(pi @ P - pi).max() < 1e-14), pi_hub=float(pi[0]), pi_autre=float(pi[1]), flux_net_max=float(abs(flux).max())); print('marche', out['marche'])
    boule = lambda N: sorted((min(a, b), max(a, b)) for a, b in (((i - 3) , (i - 2)) for i in range(6)))
    def boule_cycle(N):
        S = [(k % N) for k in range(-3, 4)]; return len(set(S)), sorted(tuple(sorted((S.index(a), S.index((a + 1) % N)))) for a in S if (a + 1) % N in S)
    out['boules'] = dict(C11=boule_cycle(11), C101=boule_cycle(101), isomorphes=bool(boule_cycle(11) == boule_cycle(101))); print('boules', out['boules'])
    # memoire de l'origine
    M = [memoire(s) for s in range(195100, 195300)]; out['memoire'] = M; r0 = np.array([x['rang_premier'] for x in M]); r1 = np.array([x['rang_1000'] for x in M]); d0 = np.array([x['degre_premier'] for x in M])
    print('memoire : premier sommet parmi les 1 / 5 / 10 / 30 plus centraux : %.3f %.3f %.3f %.3f' % tuple((r0 <= k).mean() for k in (1, 5, 10, 30)), '| rang median', int(np.median(r0)), '| sommet 1000 parmi les 10 : %.3f, les 30 : %.3f' % ((r1 <= 10).mean(), (r1 <= 30).mean()), 'rang median', int(np.median(r1)),
          '| degre du premier : mediane', int(np.median(d0)), 'moyenne %.2f' % d0.mean(), '| degre moyen %.4f' % M[0]['degre_moyen'])
    json.dump(out, open('c195c.json', 'w'))
