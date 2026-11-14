# C-117 bis (controle exploratoire) : memes trois vitesses NON ponderees sur la trame limite de S1 (C-116),
# c'est-a-dire le complexe de Coxeter C~3 = subdivision barycentrique du reseau cubique (maille : 8 sommets, 56 aretes, 96 faces, 48 tetras).
import itertools, numpy as np
from fractions import Fraction as Fr
H=Fr(1,2)
def cells():
    S={p:[] for p in range(4)}; seen={p:set() for p in range(4)}
    for c in itertools.product(range(-1,2),repeat=3):
        for perm in itertools.permutations(range(3)):
            for sg in itertools.product((1,-1),repeat=3):
                ctr=tuple(Fr(x)+H for x in c); v=[ctr]
                cur=list(ctr)
                for a in perm: cur=list(cur); cur[a]+=sg[a]*H; v.append(tuple(cur))
                v=v[::-1]   # ordre : sommet du cube, milieu d'arete, centre de face, centre du cube
                for p in range(4):
                    for idx in itertools.combinations(range(4),p+1):
                        w=[v[i] for i in idx]; a=tuple(min(x[i] for x in w).__floor__() for i in range(3))
                        if a!=(0,0,0): continue
                        key=tuple(w)
                        if key not in seen[p]: seen[p].add(key); S[p].append(key)
    return S
S=cells(); print('maille :',[len(S[p]) for p in range(4)])
IDX={p:{s:i for i,s in enumerate(S[p])} for p in range(4)}
def dmat(p,k):
    M=np.zeros((len(S[p]),len(S[p-1])),complex)
    for i,sh in enumerate(S[p]):
        for j in range(p+1):
            f=[x for q,x in enumerate(sh) if q!=j]; a=tuple(min(x[i2] for x in f).__floor__() for i2 in range(3))
            fs=tuple(tuple(x[i2]-a[i2] for i2 in range(3)) for x in f)
            M[i,IDX[p-1][fs]]+=(-1)**j*np.exp(1j*np.dot(k,[float(z) for z in a]))
    return M
h=lambda M:np.sort(np.linalg.eigvalsh((M+M.conj().T)/2))
for eps in (0.1,0.01):
    rows=[]
    for dv in ((1,0,0),(1,1,0),(1,1,1),(1,2,3),(3,-1,2)):
        k=eps*np.array(dv,float)/np.linalg.norm(dv); q=eps**2
        d0,d1,d2=dmat(1,k),dmat(2,k),dmat(3,k)
        assert np.allclose(d1@d0,0) and np.allclose(d2@d1,0)
        A=h(d0.conj().T@d0); Bv=h(d1.conj().T@d1); C=h(d2@d2.conj().T)
        nz=lambda v:[x for x in v if x>1e-7*q]
        rows.append((nz(A)[0]/q,nz(Bv)[0]/q,nz(Bv)[1]/q,nz(C)[0]/q,len(A)-len(nz(A)),len(Bv)-len(nz(Bv)),len(C)-len(nz(C))))
    r=np.array(rows)
    print(f'|k|={eps}: c_A²={r[:,0].mean():.6f} (anis. {np.ptp(r[:,0])/r[:,0].mean():.1e}) c_B²={r[:,1].mean():.6f}/{r[:,2].mean():.6f} (anis. {np.ptp(r[:,1:3])/r[:,1:3].mean():.1e}) c_C²={r[:,3].mean():.6f} (anis. {np.ptp(r[:,3])/r[:,3].mean():.1e}) noyaux={r[0,4:].astype(int).tolist()}')
