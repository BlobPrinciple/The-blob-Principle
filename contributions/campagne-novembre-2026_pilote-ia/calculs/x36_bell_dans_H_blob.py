#!/usr/bin/env python3
"""X-36. Le test de Bell que le corpus de mars annonçait (« Cryptographie : non-clonage dans H_Blob, test Bell simulation ») et que
le 4 juillet a fait sur des grandeurs qui commutent.

Objet, tel que le pose l'appendice A du master v90 (30 mars 2026) : espace H_Blob = L2(Omega, pi) ; hamiltonien
H = I - D^{1/2} P D^{-1/2}, où P est la matrice de transition de la chaîne (échange d'une arête, Metropolis) et D = diag(pi) ;
état fondamental psi0 = sqrt(pi) (théorème T4).

Ici : petit Blob énuméré exactement (N points, toutes les paires sont des liens possibles, E liens, graphes connexes),
S = log(1 + triangles) - beta * (écart-type / moyenne des degrés), pi proportionnelle à exp(S * N / tau).
On coupe les liens possibles en deux régions (A : liens touchant les points 0 ou 1 ; B : les autres), on écrit psi0 comme une
matrice M[a, b], et on cherche la plus grande valeur de Bell (CHSH) pour des grandeurs à valeurs +1/-1 propres à chaque région :
  - borne de Gisin, calculée sur les deux plus grands coefficients de Schmidt (valeur atteinte, pas une estimation) ;
  - montée alternée (« see-saw ») sur les quatre grandeurs, depuis 40 départs au hasard ;
  - plafond pour les grandeurs qui se lisent sur la configuration (diagonales) : montée alternée restreinte aux diagonales.
Témoins : mesure uniforme à E fixé (aucune viabilite) ; mesure produit (liens indépendants, sans contrainte).

Usage : x36_bell_dans_H_blob.py N E [beta] [tau]
"""
import sys, itertools, math, json
import numpy as np

def graphes(N, E):
    paires = list(itertools.combinations(range(N), 2))
    out = []
    for c in itertools.combinations(range(len(paires)), E):
        adj = [set() for _ in range(N)]
        for i in c:
            u, v = paires[i]; adj[u].add(v); adj[v].add(u)
        vu = {0}; pile = [0]
        while pile:
            x = pile.pop()
            for y in adj[x]:
                if y not in vu: vu.add(y); pile.append(y)
        if len(vu) == N: out.append((frozenset(c), adj))
    return paires, out

def score(adj, N, beta):
    tri = sum(len(adj[u] & adj[v]) for u in range(N) for v in adj[u] if v > u) // 3
    d = np.array([len(a) for a in adj], float)
    return math.log(1 + tri) - beta * d.std() / d.mean()

def signe(X):
    w, V = np.linalg.eigh((X + X.T) / 2)
    return (V * np.where(w >= 0, 1.0, -1.0)) @ V.T

def chsh(M, A1, A2, B1, B2):
    return float(np.trace(M.T @ A1 @ M @ (B1 + B2)) + np.trace(M.T @ A2 @ M @ (B1 - B2)))

def montee(M, rng, diagonale=False, departs=40, tours=300):
    na, nb = M.shape; best = -9
    for _ in range(departs):
        if diagonale:
            B1 = np.diag(rng.choice([-1.0, 1.0], nb)); B2 = np.diag(rng.choice([-1.0, 1.0], nb))
        else:
            B1 = signe(rng.normal(size=(nb, nb))); B2 = signe(rng.normal(size=(nb, nb)))
        v = -9
        for _ in range(tours):
            X1 = M @ (B1 + B2) @ M.T; X2 = M @ (B1 - B2) @ M.T
            A1, A2 = (np.diag(np.sign(np.diag(X1)) + (np.diag(X1) == 0)), np.diag(np.sign(np.diag(X2)) + (np.diag(X2) == 0))) if diagonale else (signe(X1), signe(X2))
            Y1 = M.T @ (A1 + A2) @ M; Y2 = M.T @ (A1 - A2) @ M
            B1, B2 = (np.diag(np.sign(np.diag(Y1)) + (np.diag(Y1) == 0)), np.diag(np.sign(np.diag(Y2)) + (np.diag(Y2) == 0))) if diagonale else (signe(Y1), signe(Y2))
            nv = chsh(M, A1, A2, B1, B2)
            if nv - v < 1e-13: break
            v = nv
        best = max(best, v)
    return best

def analyse(M, rng):
    s = np.linalg.svd(M, compute_uv=False); lam = s ** 2; lam = lam / lam.sum()
    p = lam[0] + lam[1]; C = 2 * math.sqrt(lam[0] * lam[1]) / p if p > 0 else 0.0
    return {'rang_de_Schmidt': int((lam > 1e-12).sum()), 'entropie_d_intrication_bits': float(-(lam[lam > 1e-15] * np.log2(lam[lam > 1e-15])).sum()),
            'chsh_gisin': 2 * ((1 - p) + p * math.sqrt(1 + C * C)), 'chsh_montee': montee(M, rng),
            'chsh_grandeurs_lues_sur_la_configuration': montee(M, rng, diagonale=True)}

def matrice(paires, etats, poids, N):
    ia = [i for i, (u, v) in enumerate(paires) if u in (0, 1) or v in (0, 1)]; ib = [i for i in range(len(paires)) if i not in ia]
    ca = {}; cb = {}; cells = []
    for c, w in zip(etats, poids):
        a = frozenset(i for i in c if i in ia); b = frozenset(i for i in c if i in ib)
        cells.append((ca.setdefault(a, len(ca)), cb.setdefault(b, len(cb)), math.sqrt(w)))
    M = np.zeros((len(ca), len(cb)))
    for i, j, x in cells: M[i, j] = x
    return M / np.linalg.norm(M), len(ia), len(ib)

def lancer(N, E, beta=0.30, tau=0.50):
    rng = np.random.default_rng(3600 + 10 * N + E)
    paires, G = graphes(N, E); n = len(G)
    idx = {c: i for i, (c, _) in enumerate(G)}
    S = np.array([score(adj, N, beta) for _, adj in G])
    w = np.exp((S - S.max()) * N / tau); pi = w / w.sum()
    # chaîne : choisir un lien présent et un lien absent au hasard, échanger si le graphe reste connexe, accepter par Metropolis
    P = np.zeros((n, n)); npaires = len(paires)
    for i, (c, _) in enumerate(G):
        for e in c:
            for f in range(npaires):
                if f in c: continue
                j = idx.get((c - {e}) | {f})
                if j is None: continue
                P[i, j] += min(1.0, pi[j] / pi[i]) / (E * (npaires - E))
        P[i, i] = 1.0 - P[i].sum()
    bilan = float(np.abs(pi[:, None] * P - (pi[:, None] * P).T).max())
    r = np.sqrt(pi); H = np.eye(n) - (r[:, None] * P) / r[None, :]
    vp = np.linalg.eigvalsh((H + H.T) / 2)
    out = {'N': N, 'E': E, 'beta': beta, 'tau': tau, 'graphes_connexes': n, 'bilan_detaille_max': bilan,
           'residu_H_psi0': float(np.linalg.norm(H @ r)), 'asymetrie_H': float(np.abs(H - H.T).max()),
           'plus_petite_valeur_propre': float(vp[0]), 'trou_spectral': float(vp[1]), 'poids_de_l_etat_le_plus_probable': float(pi.max())}
    etats = [c for c, _ in G]
    M, na, nb = matrice(paires, etats, pi, N); out['liens_region_A'] = na; out['liens_region_B'] = nb
    out['blob'] = analyse(M, rng)
    M0, _, _ = matrice(paires, etats, np.ones(n) / n, N); out['temoin_uniforme_a_E_fixe'] = analyse(M0, rng)
    # témoin produit : chaque lien présent avec la probabilité E / nombre de paires, indépendamment, sans contrainte
    q = E / npaires
    tous = [frozenset(c) for k in range(npaires + 1) for c in itertools.combinations(range(npaires), k)]
    Mp, _, _ = matrice(paires, tous, [q ** len(c) * (1 - q) ** (npaires - len(c)) for c in tous], N); out['temoin_produit'] = analyse(Mp, rng)
    return out

if __name__ == '__main__':
    N, E = int(sys.argv[1]), int(sys.argv[2])
    beta = float(sys.argv[3]) if len(sys.argv) > 3 else 0.30
    tau = float(sys.argv[4]) if len(sys.argv) > 4 else 0.50
    print(json.dumps(lancer(N, E, beta, tau), ensure_ascii=False, indent=1))
