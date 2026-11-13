# Contrôle ANALYTIQUE (aucune simulation de C-142) : « l'impact et la cloche » sur les deux premières structures de C-141c.
# Modèle scalaire minimal, déclaré : masses et raideurs égales à 1, déplacement u, L = laplacien du graphe des liens.
# Impulsion unité sur le porteur v ; réponse u(t) = somme sur les valeurs propres non nulles de P_lambda(delta_v) sin(w t)/w, w = sqrt(lambda).
# Étirement moyen d'un lien e = (a, b) : S_e(v) = 1/2 * somme_lambda [ (P_lambda delta_v)(a) - (P_lambda delta_v)(b) ]^2 / lambda   (exact, sympy).
import sympy as sp, itertools
def etude(nom, edges, n):
    L = sp.zeros(n, n)
    for a, b in edges:
        L[a, a] += 1; L[b, b] += 1; L[a, b] -= 1; L[b, a] -= 1
    vals = L.eigenvects()
    print(nom, ': valeurs propres', {sp.nsimplify(v): m for v, m, _ in vals})
    for v in range(n):
        S = {e: sp.Integer(0) for e in edges}
        d = sp.Matrix([1 if i == v else 0 for i in range(n)])
        for lam, m, vecs in vals:
            if lam == 0: continue
            Q = sp.Matrix.hstack(*vecs); P = Q * (Q.T * Q).inv() * Q.T; p = P * d
            for (a, b) in edges: S[(a, b)] += sp.Rational(1, 2) * (p[a] - p[b]) ** 2 / lam
        tot = sum(S.values()); inc = sum(s for e, s in S.items() if v in e)
        print(f'  impulsion sur {v} : part de l\'étirement portée par ses propres liens = {sp.nsimplify(sp.simplify(inc / tot))} ≈ {float(inc / tot):.4f} ;',
              'par lien :', {e: round(float(s / tot), 4) for e, s in S.items()})
K4 = list(itertools.combinations(range(4), 2))
etude('Tétraèdre seul', K4, 4)
deux = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4), (3, 4)]
etude('Deux cellules (après la première division de C-141c)', deux, 5)
