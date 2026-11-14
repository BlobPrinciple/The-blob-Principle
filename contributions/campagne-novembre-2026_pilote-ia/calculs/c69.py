import numpy as np, itertools
from scipy.linalg import expm
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
s8={**{i:1 for i in range(4)},**{i:-1 for i in range(4,8)}}; mir={i:(i+4)%8 for i in range(8)}
maxs=[(0,1,2,3),(4,5,6,7),(0,4),(1,5),(2,6)]
cells=complex_from_max(maxs); idx={c:i for i,c in enumerate(cells)}; n=len(cells)
chrono={(0,4):4.0,(1,5):2.0,(2,6):1.0}
G=np.diag([(-1)**(len(c)-1) for c in cells]).astype(complex); S=polar(cells,s8).astype(complex)
Nop=np.diag([len(c)-1 for c in cells]).astype(complex); g=1.5
for var,ph in [("A reel",1.0),("B phase i",1j)]:
    d=np.zeros((n,n),complex)
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f: d[idx[c],idx[f]]+=(-1)**j*(chrono[c]*ph if c in chrono else 1)
    D=d+d.conj().T; H=D+g*S@G
    w,V=np.linalg.eigh(H); K=V[:,abs(w)<1e-9]
    P=perm_op(cells,idx,mir); L=round(np.trace(G@P).real)
    print(f"--- Variante {var} : modes nuls={K.shape[1]}, L(P)={L}, anticommute={np.allclose((G@P)@H+H@(G@P),0)}")
    if K.shape[1]!=3: continue
    for nom,O in [("D^2",D@D),("exp(-D^2)",expm(-D@D)),("Gamma",G),("N",Nop)]:
        l=np.sort(abs(np.linalg.eigvalsh(K.conj().T@O@K)))
        e1=l.sum(); e2=l[0]*l[1]+l[0]*l[2]+l[1]*l[2]; r=e1**2/e2
        rat=(l[1]/l[0])**2 if l[0]>1e-12 else np.inf; rat2=(l[2]/l[1])**2
        print(f"  {nom:10s} sqrt(m)~{np.round(l,4)}  e1^2/e2={r:.4f}  ecart={abs(r-6)/6:.2e}  m2/m1={rat:.3f}  m3/m2={rat2:.3f}")
