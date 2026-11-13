# Contre-audit des trois affirmations de ChatGPT sur le fil principal (20 h 16 UTC) — calculs indépendants
import numpy as np, itertools
from scipy.integrate import quad
# 1. Tétraèdre régulier en 3D, 4 masses unité, 6 ressorts unité : spectre des petites vibrations
P = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float); H = np.zeros((12, 12))
for i, j in itertools.combinations(range(4), 2):
    u = (P[i] - P[j]) / np.linalg.norm(P[i] - P[j]); B = np.outer(u, u)
    H[3*i:3*i+3, 3*i:3*i+3] += B; H[3*j:3*j+3, 3*j:3*j+3] += B; H[3*i:3*i+3, 3*j:3*j+3] -= B; H[3*j:3*j+3, 3*i:3*i+3] -= B
w, U = np.linalg.eigh(H); print('valeurs propres (omega^2) :', np.round(w, 6))
nz = w > 1e-9; print('fréquences relatives des 6 modes non rigides :', np.round(np.sqrt(w[nz] / w[nz].min()), 6))
# 2. Impulsion égale et opposée sur deux sommets, le long de leur arête : partage de l'énergie cinétique initiale entre familles
u = (P[0] - P[1]) / np.linalg.norm(P[0] - P[1]); p = np.zeros(12); p[0:3] = u; p[3:6] = -u
c = U.T @ p; tot = (c ** 2).sum()
for lam in sorted(set(np.round(w, 6))):
    sel = np.abs(w - lam) < 1e-6; print(f'   omega^2 = {lam:.3f} : part de l\'énergie = {(c[sel]**2).sum()/tot:.6f}')
# 3. Morse U = D (1 - exp(-a x))^2, masse 1 : fréquence propre en fonction de l'énergie interne
D, a = 1.0, 1.0; w0 = a * np.sqrt(2 * D)
for E in (0.1, 0.2775, 0.5, 0.9):
    x1 = -np.log(1 + np.sqrt(E / D)) / a; x2 = -np.log(1 - np.sqrt(E / D)) / a
    f = lambda th: 1.0  # changement de variable x = xm + r sin(th) pour lever les singularités aux points de rebroussement
    xm, r = (x1 + x2) / 2, (x2 - x1) / 2
    g = lambda th: r * np.cos(th) / np.sqrt(2 * (E - D * (1 - np.exp(-a * (xm + r * np.sin(th)))) ** 2))
    T = 2 * quad(g, -np.pi / 2, np.pi / 2, limit=200)[0]
    print(f'   E/D = {E:.4f} : omega/omega0 intégré = {2*np.pi/T/w0:.5f} ; formule sqrt(1 - E/D) = {np.sqrt(1-E/D):.5f}')
