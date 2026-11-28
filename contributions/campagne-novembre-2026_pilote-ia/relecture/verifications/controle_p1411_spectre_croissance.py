#!/usr/bin/env python3
"""Contrôle du pilote pour les pages 1411-1412 du master V346 (Partie CCXIX, « le courant de l'inscription », 19 juillet).
Le master : la dynamique de croissance (ajout de sommets sans retrait, relaxation réversible entre deux ajouts) n'est pas
auto-adjointe [exact], « le spectre du générateur de l'inscription est donc complexe ».
Vérification : un générateur de Markov gradué par le nombre de sommets, dont chaque niveau est une relaxation réversible
et dont les seuls sauts entre niveaux montent, est triangulaire par blocs ; son spectre est la réunion des spectres des blocs
diagonaux, qui sont réels. Exemple numérique : 5 niveaux de 12 états, taux tirés au hasard, 200 tirages.
On mesure aussi le corrélateur antisymétrique D(k) = <a(t) b(t+k)> - <b(t) a(t+k)> en régime de croissance : il n'est pas nul.
"""
import numpy as np
rng = np.random.default_rng(3)

def generateur(niveaux=5, m=12):
    n = niveaux * m
    L = np.zeros((n, n))
    for a in range(niveaux):
        pi = rng.random(m) + 0.2
        Ssym = rng.random((m, m)); Ssym = (Ssym + Ssym.T) / 2          # taux réversibles : q(i,j) = Ssym(i,j) / pi(i)
        for i in range(m):
            for j in range(m):
                if i != j:
                    L[a*m+i, a*m+j] = Ssym[i, j] / pi[i]
        if a + 1 < niveaux:                                             # sauts de croissance, taux dépendant de l'état
            for i in range(m):
                for j in range(m):
                    L[a*m+i, (a+1)*m+j] = rng.random() * 0.3
    np.fill_diagonal(L, 0.0); np.fill_diagonal(L, -L.sum(axis=1))
    return L

pire = 0.0; asym = []
for _ in range(200):
    L = generateur()
    vp = np.linalg.eigvals(L)
    pire = max(pire, np.max(np.abs(vp.imag)))
    asym.append(np.max(np.abs(L - L.T)))
print(f"200 générateurs de croissance (non symétriques : écart maximal entre L et sa transposée {np.mean(asym):.2f} en moyenne)")
print(f"plus grande partie imaginaire d'une valeur propre, sur les 200 tirages : {pire:.2e}")

# corrélateur antisymétrique le long de trajectoires de croissance (deux observables fonctions de l'état)
L = generateur(niveaux=5, m=12); n = L.shape[0]
a_obs = rng.random(n); b_obs = rng.random(n)
taux = -np.diag(L); P = L / taux[:, None]; np.fill_diagonal(P, 0.0)
def trajectoire(pas=40):
    x = rng.integers(12); xs = [x]
    for _ in range(pas):
        if taux[x] <= 0 or P[x].sum() <= 0: xs.append(x); continue
        x = rng.choice(n, p=P[x] / P[x].sum()); xs.append(x)
    return np.array(xs)
R = 4000; D = np.zeros((R, 5))
for r in range(R):
    xs = trajectoire(); A = a_obs[xs]; B = b_obs[xs]
    for k in range(1, 6):
        D[r, k-1] = np.mean(A[:-k] * B[k:]) - np.mean(B[:-k] * A[k:])
moy = D.mean(axis=0); sem = D.std(axis=0, ddof=1) / np.sqrt(R)
print("corrélateur antisymétrique D(k), k = 1 à 5, sur 4 000 trajectoires de croissance :")
print("   moyenne      :", np.round(moy, 4))
print("   erreur type  :", np.round(sem, 4))
print("   moyenne / erreur :", np.round(moy / sem, 1))
