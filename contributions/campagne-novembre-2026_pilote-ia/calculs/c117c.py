# C-117 ter (declare) : bras pondere sur la trame limite de S1 (C~3), ou les etoiles circoncentriques degenerent.
# Produits scalaires de Whitney (elements finis de plus bas degre) : matrices de masse M_p assemblees par maille de Bloch.
# Controle : meme calcul sur Kuhn (coordonnees cubiques), qui doit redonner c = 1 dans la metrique cubique.
# PREDICTION ENREGISTREE : c_A = c_B = c_C = 1 sur les deux trames, isotropie en O(k^2).
import itertools, numpy as np, scipy.linalg as sl
from fractions import Fraction as Fr
def lattice(name):
    S={p:[] for p in range(4)}; seen={p:set() for p in range(4)}; tets=[]
    fl=lambda w:tuple(min(x[i] for x in w).__floor__() for i in range(3))
    if name=='C3':
        H=Fr(1,2)
        gen=[]
        for perm in itertools.permutations(range(3)):
            for sg in itertools.product((1,-1),repeat=3):
                ctr=(H,H,H); v=[ctr]; cur=list(ctr)
                for a in perm: cur=list(cur); cur[a]+=sg[a]*H; v.append(tuple(cur))
                gen.append(tuple(v[::-1]))
    else:
        gen=[]
        for perm in itertools.permutations(range(3)):
            v=[(Fr(0),Fr(0),Fr(0))]; cur=[Fr(0)]*3
            for a in perm: cur=list(cur); cur[a]+=1; v.append(tuple(cur))
            gen.append(tuple(v))
    for T in gen:
        a=fl(T); T=tuple(tuple(x[i]-a[i] for i in range(3)) for x in T); tets.append(T)
        for p in range(4):
            for idx in itertools.combinations(range(4),p+1):
                w=[T[i] for i in idx]; a=fl(w); key=tuple(tuple(x[i]-a[i] for i in range(3)) for x in w)
                if key not in seen[p]: seen[p].add(key); S[p].append(key)
    return S,tets,fl
def build(name):
    S,tets,fl=lattice(name); IDX={p:{s:i for i,s in enumerate(S[p])} for p in range(4)}
    def canon(w):
        a=fl(w); return IDX[len(w)-1][tuple(tuple(x[i]-a[i] for i in range(3)) for x in w)],np.array([float(z) for z in a])
    def dmat(p,k):
        M=np.zeros((len(S[p]),len(S[p-1])),complex)
        for i,sh in enumerate(S[p]):
            for j in range(p+1):
                c,a=canon([x for q,x in enumerate(sh) if q!=j]); M[i,c]+=(-1)**j*np.exp(1j*np.dot(k,a))
        return M
    # matrices de masse elementaires
    elem=[]
    for T in tets:
        P=np.array([[float(z) for z in x] for x in T]); A=np.hstack([np.ones((4,1)),P]); inv=np.linalg.inv(A); grad=inv[1:,:].T   # grad[i] = gradient de lambda_i
        V=abs(np.linalg.det(A))/6; I=V*(np.ones((4,4))+np.eye(4))/20; G=grad@grad.T
        m={0:{},1:{},2:{},3:{}}
        for i in range(4):
            for j in range(4): m[0][((i,),(j,))]=I[i,j]
        E1=list(itertools.combinations(range(4),2))
        for (i,j) in E1:
            for (k_,l) in E1: m[1][((i,j),(k_,l))]=I[i,k_]*G[j,l]-I[i,l]*G[j,k_]-I[j,k_]*G[i,l]+I[j,l]*G[i,k_]
        F2=list(itertools.combinations(range(4),3))
        def comps(f):
            a,b,c=f; return [(a,np.cross(grad[b],grad[c])),(b,np.cross(grad[c],grad[a])),(c,np.cross(grad[a],grad[b]))]
        for f in F2:
            for f2 in F2: m[2][(f,f2)]=4*sum(I[a,a2]*np.dot(C,C2) for a,C in comps(f) for a2,C2 in comps(f2))
        m[3][((0,1,2,3),(0,1,2,3))]=1/V
        elem.append((T,m))
    def mass(p,k):
        M=np.zeros((len(S[p]),len(S[p])),complex)
        for T,m in elem:
            for (s,t),val in m[p].items():
                cs,as_=canon([T[i] for i in s]); ct,at=canon([T[i] for i in t]); M[cs,ct]+=val*np.exp(1j*np.dot(k,at-as_))
        return M
    return S,dmat,mass
for name in ('Kuhn','C3'):
    S,dmat,mass=build(name); print(name,'maille',[len(S[p]) for p in range(4)])
    for eps in (0.1,0.01):
        rows=[]
        for dv in ((1,0,0),(1,1,0),(1,1,1),(1,2,3),(3,-1,2)):
            k=eps*np.array(dv,float)/np.linalg.norm(dv); q=eps**2
            d0,d1,d2=dmat(1,k),dmat(2,k),dmat(3,k); M0,M1,M2,M3=(mass(p,k) for p in range(4))
            A=np.sort(sl.eigh(d0.conj().T@M1@d0,M0,eigvals_only=True)); Bv=np.sort(sl.eigh(d1.conj().T@M2@d1,M1,eigvals_only=True))
            C=np.sort(np.linalg.eigvals(d2@np.linalg.inv(M2)@d2.conj().T@M3).real)
            nz=lambda v:[x for x in v if x>1e-6*q]
            rows.append((nz(A)[0]/q,nz(Bv)[0]/q,nz(Bv)[1]/q,nz(C)[0]/q))
        r=np.array(rows)
        print(f'  |k|={eps}: c_A²={r[:,0].mean():.6f} (anis. {np.ptp(r[:,0])/r[:,0].mean():.1e}) c_B²={r[:,1].mean():.6f}/{r[:,2].mean():.6f} (anis. {np.ptp(r[:,1:3])/r[:,1:3].mean():.1e}) c_C²={r[:,3].mean():.6f} (anis. {np.ptp(r[:,3])/r[:,3].mean():.1e})')
