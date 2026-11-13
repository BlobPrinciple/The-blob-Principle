# C-129 — LA POLARITE AUTO-ADJOINTE DANS UNE METRIQUE (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Verrou pose par ChatGPT (C-125, R5) : avec les masses de Whitney (non diagonales), Sigma n'est pas auto-adjointe [T].
# Proposition testee : des poids metriques DIAGONAUX (un poids positif par cellule, symetriques par le miroir). Alors
#   D_w = W^(1/2) d W^(-1/2) + transposee est symetrique, Sigma et Gamma (diagonales) commutent avec W : H_w = D_w + g Sigma Gamma est auto-adjoint.
# (A) Jumeaux : pour k = 1, 2, 3, g = 3/2, poids aleatoires (log-uniformes sur [1/4, 4]) symetriques par le miroir, 20 tirages, avant et apres
#     4 generations de mitose de l'arete jumelee (k = 1) : dim ker H_w = k ? P0 Sigma P0 = 0 ? {C, H_w} = 0 ?
#     PREDICTION : oui partout (le theoreme de Lefschetz ne depend que de la symetrie des poids).
# (B) Trame de la mitose (C~3) : existe-t-il des poids diagonaux positifs donnant UNE vitesse ? Construction : diagonale de la masse de Whitney,
#     puis un facteur par degre regle sur c_A = c_B = c_C (trois rapports libres pour trois vitesses : toujours soluble si chaque secteur est isotrope).
#     PREDICTION : PASS (vitesse unique, isotropie par symetrie cubique, pas de birefringence).
import itertools, sys, numpy as np
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
g=1.5
def Hw(cells,s,w):
    idx={c:i for i,c in enumerate(cells)}; n=len(cells); d=np.zeros((n,n))
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f: d[idx[c],idx[f]]+=(-1)**j*math.sqrt(w[c]/w[f])
    D=d+d.T; G=np.diag([(-1)**(len(c)-1) for c in cells]); S=np.diag([float(pol(c,s)) for c in cells]); return D+g*S@G,G,S,idx
import math
def test(tp,tm,s,mir,rng):
    cells=R0(tp+tm,s); mc=lambda c:tuple(sorted(mir[v] for v in c)); w={}
    for c in cells:
        if c not in w: x=float(np.exp(rng.uniform(-math.log(4),math.log(4)))); w[c]=x; w[mc(c)]=x
    M,G,S,idx=Hw(cells,s,w); e,V=np.linalg.eigh(M); K=V[:,abs(e)<1e-9]; P0=K@K.T
    Pm=np.zeros_like(M)
    for c in cells:
        img=[mir[v] for v in c]; srt=tuple(sorted(img)); perm=[img.index(v) for v in srt]; sign=1
        for a in range(len(perm)):
            for b in range(a+1,len(perm)): sign*=-1 if perm[a]>perm[b] else 1
        Pm[idx[srt],idx[c]]=sign
    C=G@Pm
    return K.shape[1],float(abs(P0@S@P0).max()),float(abs(C@M+M@C).max()),float(np.sort(abs(e))[K.shape[1]]) if K.shape[1]<len(e) else None
if sys.argv[1]=='A':
    rng=np.random.default_rng(1700)
    for k in (1,2,3):
        tp,tm,s,mir=grow(k,0,0); r=[test(tp,tm,s,mir,rng) for _ in range(20)]
        print(f'k={k}, germe jumeau, 20 tirages de poids : dim ker = {set(x[0] for x in r)} ; max |P0 Σ P0| = {max(x[1] for x in r):.1e} ; max |{{C,H}}| = {max(x[2] for x in r):.1e} ; écart spectral min = {min(x[3] for x in r):.3f}')
    for k in (1,2,3):
        r=[]
        for seed in range(5):
            tp,tm,s,mir=grow(k,6,seed); r+=[test(tp,tm,s,mir,rng) for _ in range(4)]
        print(f'k={k}, après 6 naissances jumelées 1→4 (5 histoires × 4 tirages) : dim ker = {set(x[0] for x in r)} ; max |P0 Σ P0| = {max(x[1] for x in r):.1e} ; max |{{C,H}}| = {max(x[2] for x in r):.1e} ; écart spectral min = {min(x[3] for x in r):.3f}')
    src=open('c118.py').read().split("def stats(tp,tm,s):")[0].split("exec(open('c81_32.py').read().split('g=1.5; F=')[0])")[1]
    src=src.replace("out.append((gen,sorted(tp),sorted(tm),dict(s)))","out.append((gen,sorted(tp),sorted(tm),dict(s),dict(mir)))"); exec(src)
    for gen,tp,tm,s,mir in twin_edge(5):
        r=[test(tp,tm,s,mir,rng) for _ in range(6)]
        print(f'k=1, mitose de l\'arête jumelée, génération {gen} ({len(tp)} cellules par lignée), 6 tirages : dim ker = {set(x[0] for x in r)} ; max |P0 Σ P0| = {max(x[1] for x in r):.1e} ; max |{{C,H}}| = {max(x[2] for x in r):.1e} ; écart spectral min = {min(x[3] for x in r):.3f}',flush=True)
if sys.argv[1]=='B':
    src=open('c117c.py').read().split("for name in ('Kuhn','C3'):")[0]; ns={}; exec(src,ns); S_,dmat,mass=ns['build']('C3')
    M0=[mass(p,np.zeros(3)).real for p in range(4)]; w=[np.diag(M).copy() for M in M0]; h=lambda M:np.sort(np.linalg.eigvalsh((M+M.conj().T)/2))
    def speeds(w,k):
        q=k@k; d0,d1,d2=dmat(1,k),dmat(2,k),dmat(3,k)
        A=h(np.diag(w[0]**-.5)@d0.conj().T@np.diag(w[1])@d0@np.diag(w[0]**-.5)); Bv=h(np.diag(w[1]**-.5)@d1.conj().T@np.diag(w[2])@d1@np.diag(w[1]**-.5)); C=h(np.diag(w[3]**.5)@d2@np.diag(1/w[2])@d2.conj().T@np.diag(w[3]**.5))
        nz=lambda v:[x for x in v if x>1e-6*q]; return nz(A)[0]/q,nz(Bv)[0]/q,nz(Bv)[1]/q,nz(C)[0]/q
    cA,cB,_,cC=speeds(w,1e-3*np.array([1.,2.,3.])/np.sqrt(14)); l1=math.sqrt(cB/cA); c2=cA*l1; l3=c2/cC
    w2=[w[0],w[1]*l1,w[2],w[3]*l3]; w2=[x/c2**(i) for i,x in enumerate(w2)]   # normalisation : c = 1
    print('facteurs par degré appliqués à la diagonale de Whitney : arêtes ×',round(l1,6),' tétraèdres ×',round(l3,6))
    print('poids distincts (sommets | arêtes | faces | tétraèdres) :',' | '.join(str(sorted(set(np.round(x,5)))) for x in w2))
    for eps in (0.3,0.1,0.01):
        rows=np.array([speeds(w2,eps*np.array(dv,float)/np.linalg.norm(dv)) for dv in ((1,0,0),(1,1,0),(1,1,1),(1,2,3),(3,-1,2))])
        print(f'   |k|={eps}: c_A²={rows[:,0].mean():.6f} c_B²={rows[:,1].mean():.6f}/{rows[:,2].mean():.6f} c_C²={rows[:,3].mean():.6f} ; anisotropie max={max(np.ptp(rows[:,i])/rows[:,i].mean() for i in range(4)):.1e}')
