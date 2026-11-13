# Contre-audit de C-130 (ChatGPT) par Claude, 12 nov. 2026. Arithmetique exacte (sympy).
import sympy as sp, itertools
R=sp.Rational
# --- 1D : arete de longueur 1 coupee en deux
W0=sp.diag(R(1,3),R(1,3)); W0p=sp.diag(R(1,6),R(1,3),R(1,6)); P0=sp.Matrix([[1,0],[R(1,2),R(1,2)],[0,1]])
d=sp.Matrix([[-1,1]]); dp=sp.Matrix([[-1,1,0],[0,-1,1]]); P1=sp.Matrix([[R(1,2)],[R(1,2)]])   # 1-cochaine : la valeur sur l'arete se partage
print('1D  d\'P0 = P1 d :',dp*P0==P1*d,' ; P0^T W0\' P0 =',(P0.T*W0p*P0).tolist(),' ≠ W0 :',P0.T*W0p*P0!=W0)
W1=sp.Matrix([[1]]); W1p=sp.diag(2,2)                                                           # masse de Whitney d'une 1-forme : 1/L
L0=W0.inv()*d.T*W1*d; L0p=W0p.inv()*dp.T*W1p*dp
print('    spectre grossier :',sorted(L0.eigenvals()),' ; spectre fin :',sorted(L0p.eigenvals()))
Q=P0.T*W0p*P0; Qs=sp.simplify((Q**R(-1,2))); U0=sp.simplify(P0*Qs*sp.sqrt(W0))
print('    isométrisé : U0^T W0\' U0 = W0 :',sp.simplify(U0.T*W0p*U0-W0)==sp.zeros(2,2),' ; d\'U0 = √2·P1 d :',sp.simplify(dp*U0-sp.sqrt(2)*P1*d)==sp.zeros(2,2),
      ' ; constantes conservées :',sp.simplify(U0*sp.Matrix([1,1])-sp.Matrix([1,1,1]))==sp.zeros(3,1))
# masses completes de Whitney, meme arete : le transport est isometrique
M0=sp.Matrix([[R(1,3),R(1,6)],[R(1,6),R(1,3)]]); M0p=sp.Matrix([[R(1,6),R(1,12),0],[R(1,12),R(1,3),R(1,12)],[0,R(1,12),R(1,6)]])
print('    masses complètes : P0^T M0\' P0 = M0 :',P0.T*M0p*P0==M0)
# --- 3D : tetraedre de Kuhn, bissection de l'arete la plus longue (0,3)
V=R(1,6); W=sp.diag(*[V/10]*4)                         # diagonale de la masse de Whitney des 0-formes : V/10 par sommet et par cellule
# sommets fins : 0,1,2,3,m ; cellules (0,1,2,m) et (m,1,2,3), volume 1/12 chacune
Wp=sp.diag(R(1,120),R(1,60),R(1,60),R(1,120),R(1,60)); P=sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[R(1,2),0,0,R(1,2)]])
Qd=P.T*Wp*P; print('3D  (P0^T W0\' P0)[0,3] =',Qd[0,3],' ; W0[0,3] =',W[0,3],' ; écart diagonal :',(Qd-W).diagonal().tolist())
# --- reseau cubique : ecart a l'ordre q^4 entre (q,0,0) et (q,q,q)/√3
q=sp.symbols('q',positive=True); lam=lambda k:4*sum(sp.sin(x/2)**2 for x in k)
print('cubique : λ(q,0,0) − λ(q/√3 ×3) =',sp.series(lam((q,0,0))-lam((q/sp.sqrt(3),)*3),q,0,7))
# --- reflexion de Rudolphe, calculs de ChatGPT : tetraedre regulier au repos, une arete se divise (regle U)
a=sp.symbols('a',positive=True); E=R(1,2)*(5*(a-1)**2+2*(a/2-1)**2+2*(sp.sqrt(3)*a/2-1)**2)
ast=sp.solve(sp.diff(E,a),a)[0]
print('tétraèdre : ΔE naissance =',sp.simplify(E.subs(a,1)),' ; dE/da(1) =',sp.simplify(sp.diff(E,a).subs(a,1)),' ; a* =',sp.simplify(ast),'=',sp.N(ast,8),' ; E(a*) =',sp.simplify(E.subs(a,ast)),'=',sp.N(E.subs(a,ast),8))
print('  détente libre : deux tétraèdres réguliers collés par une face, 9 fils au repos, E = 0 ; distance des anciennes extrémités = 2·hauteur =',sp.N(2*sp.sqrt(R(2,3)),6),'→ +',sp.N(100*(2*sp.sqrt(R(2,3))-1),4),'%')
