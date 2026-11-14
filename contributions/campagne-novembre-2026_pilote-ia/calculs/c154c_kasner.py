#!/usr/bin/env python3
"""C-154c, controle exact d'un enonce de ChatGPT (C-153) : Kasner (2/3, 2/3, -1/3) a t = 1 : vide, K_ij, invariant de Kretschmann."""
import sympy as sp
t, x, y, z = sp.symbols('t x y z', positive=True); X = [t, x, y, z]; p = [sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(-1, 3)]
g = sp.diag(-1, t ** (2 * p[0]), t ** (2 * p[1]), t ** (2 * p[2])); gi = g.inv()
G = [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(4)) / 2 for c in range(4)] for b in range(4)] for a in range(4)]
def R(a, b, c, d): return sp.diff(G[a][b][d], X[c]) - sp.diff(G[a][b][c], X[d]) + sum(G[a][c][e] * G[e][b][d] - G[a][d][e] * G[e][b][c] for e in range(4))
Rl = [[[[sp.simplify(sum(g[a, e] * R(e, b, c, d) for e in range(4))) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
ric = sp.Matrix(4, 4, lambda b, d: sp.simplify(sum(R(a, b, a, d) for a in range(4))))
kr = sp.simplify(sum(Rl[a][b][c][d] * Rl[e][f][h][k] * gi[a, e] * gi[b, f] * gi[c, h] * gi[d, k] for a in range(4) for b in range(4) for c in range(4) for d in range(4) for e in range(4) for f in range(4) for h in range(4) for k in range(4) if Rl[a][b][c][d] != 0 and Rl[e][f][h][k] != 0))
K = [sp.simplify(-sp.diff(g[i, i], t) / 2 / g[i, i]).subs(t, 1) for i in (1, 2, 3)]
print('Ricci nul :', ric == sp.zeros(4, 4), '| Kretschmann(t) =', kr, '| a t=1 :', kr.subs(t, 1), '| K^i_i a t=1 :', K, '| somme p, somme p^2 :', sum(p), sum(q ** 2 for q in p))
