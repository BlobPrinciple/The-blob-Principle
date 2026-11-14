# PONT ENTRE LES DEUX BRANCHES — contrôle analytique et numérique (aucun protocole exécuté ici).
# Modèle scalaire amorti : q'' + gamma L q' + L q = 0, q(0) = 0, q'(0) = p_v (impulsion unité du porteur bloqué), amortisseur sur chaque lien.
# Chaleur déposée dans le lien e : Q_e = gamma * intégrale de (b_e . q')^2 dt.
# Énoncé à contrôler : somme des Q_e = (1 - 1/n)/2 (exact) ; Q_e -> W0(e)/2 quand l'amortissement est faible (écart d'ordre gamma^2).
import numpy as np, itertools, random
from scipy.linalg import solve_continuous_lyapunov
def heat(edges, n, v, gamma):
    L = np.zeros((n, n))
    for a, b in edges: L[a, a] += 1; L[b, b] += 1; L[a, b] -= 1; L[b, a] -= 1
    w, U = np.linalg.eigh(L); keep = w > 1e-9; U = U[:, keep]; w = w[keep]; m = len(w)
    p = -np.ones(n) / n; p[v] += 1; c = U.T @ p
    A = np.block([[np.zeros((m, m)), np.eye(m)], [-np.diag(w), -gamma * np.diag(w)]]); z0 = np.concatenate([np.zeros(m), c])
    X = solve_continuous_lyapunov(A, -np.outer(z0, z0)); Xvv = X[m:, m:]          # intégrale de z z^T
    Q = np.array([gamma * (U[a] - U[b]) @ Xvv @ (U[a] - U[b]) for a, b in edges])
    # W0 avec somme cohérente par espace propre
    W0 = np.zeros(len(edges)); i = 0
    while i < m:
        j = i + 1
        while j < m and w[j] - w[j - 1] < 1e-8: j += 1
        y = U[:, i:j] @ c[i:j]; W0 += np.array([(y[a] - y[b]) ** 2 for a, b in edges]) / w[i:j].mean(); i = j
    return Q, W0
K5m = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4), (3, 4)]
random.seed(3); n = 14; G = set()
for i in range(1, n): G.add((random.randrange(i), i))
while len(G) < 30:
    a, b = sorted(random.sample(range(n), 2)); G.add((a, b))
G = sorted(G)
for nom, E, n_, v in (('tétraèdre', list(itertools.combinations(range(4), 2)), 4, 0), ('deux cellules', K5m, 5, 0), ('graphe aléatoire, 14 porteurs, 30 liens', G, n, 5)):
    for gamma in (0.01, 0.04, 0.12, 0.5):
        Q, W0 = heat(E, n_, v, gamma)
        print(f'{nom:<40} gamma={gamma:<5} somme Q = {Q.sum():.6f} (attendu {(1-1/n_)/2:.6f}) ; écart max |Q_e - W0/2| = {np.abs(Q-W0/2).max():.2e} ; écart relatif max = {np.abs(Q-W0/2).max()/ (W0.max()/2):.2e}')
