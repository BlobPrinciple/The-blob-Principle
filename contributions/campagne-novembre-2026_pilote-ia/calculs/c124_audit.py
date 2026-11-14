# Contre-audit de C-124 (ChatGPT) par Claude, 12 nov. 2026.
# (1) Formule de Schur : G^-1 = I + (2/g^2) [L_FF - L_FI (L_II + g^2)^-1 L_IF], verifiee en fractions sur trois cas donnes par ChatGPT (k = 1, g = 3/2).
# (2) Extension : G_n sous S1 (C-116) pour k = 1, contact place en chacun des quatre sommets du germe, jusqu'a 262 144 cellules par lignee.
import itertools, sys, numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl
from fractions import Fraction as Fr
import sympy
def G_exact(edges,contact,g=Fr(3,2)):
    V=sorted(set(v for e in edges for v in e)); I=[v for v in V if v!=contact]; idx={v:i for i,v in enumerate(I)}
    L=sympy.zeros(len(I),len(I)); b=sympy.zeros(len(I),1); dF=0
    for a,c in edges:
        if contact in (a,c):
            o=c if a==contact else a; dF+=1; L[idx[o],idx[o]]+=1; b[idx[o]]-=1
        else:
            L[idx[a],idx[a]]+=1; L[idx[c],idx[c]]+=1; L[idx[a],idx[c]]-=1; L[idx[c],idx[a]]-=1
    x=(L+sympy.Rational(g.numerator,g.denominator)**2*sympy.eye(len(I))).solve(b)
    schur=dF-(b.T*x)[0]; return 1/(1+2/sympy.Rational(g.numerator,g.denominator)**2*schur)
K4=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
print('germe, contact 0 :',G_exact(K4,0),' (ChatGPT : 13/37)')
print('bissection de (0,1) :',G_exact([(0,4),(4,1),(4,2),(4,3),(0,2),(0,3),(1,2),(1,3),(2,3)],0),' (ChatGPT : 103/303)')
print('bissection de (1,2) :',G_exact([(1,4),(4,2),(4,0),(4,3),(0,1),(0,2),(0,3),(1,3),(2,3)],0),' (ChatGPT : 13/45)')
src=open('c116.py').read().split("if __name__")[0]
src=src.replace("    return finish(L,F,E,nv,seed,extra)\ndef run_S2","    return (L,F,E,nv,P)\ndef run_S2"); ns={}; exec(src,ns)
g2=2.25
print('\nS1, k = 1, g = 3/2 : G_n selon le sommet du germe choisi comme contact (degré du contact entre parenthèses)')
prev=None
for gen in range(0,19,3):
    L,F,E,nv,P=ns['run'](('S1',2**gen,1500)); ed=np.array(list(E.keys())); A=sp.csr_matrix((np.ones(len(ed)),(ed[:,0],ed[:,1])),shape=(nv,nv)); A=A+A.T; deg=np.array(A.sum(1)).ravel(); Lap=sp.diags(deg)-A
    row=[]
    for c in range(4):
        I=np.array([v for v in range(nv) if v!=c]); LII=Lap[I][:,I]+g2*sp.eye(len(I)); LIF=Lap[I][:,[c]].toarray().ravel()
        x=spl.spsolve(LII.tocsc(),LIF); schur=deg[c]-LIF@x; row.append((1/(1+2/g2*schur),int(deg[c])))
    print(f'  génération {gen:2d} ({2**gen:6d} cellules) : '+' ; '.join(f'{G:.6f} ({d})' for G,d in row)+('' if prev is None else '   écart au palier précédent : '+' ; '.join(f'{a[0]-b[0]:+.1e}' for a,b in zip(row,prev))),flush=True); prev=row
