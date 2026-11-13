import numpy as np, itertools
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
cells=complex_from_max([(0,1,2,3)]); D,G,idx=ops(cells); g=1.5
pairs=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
ok=True; offmax=0
for s in itertools.product([1,-1],repeat=4):
    S=polar(cells,dict(enumerate(s))); H=D+g*S@G
    for sg in itertools.product([1,-1],repeat=3):   # orientations relatives dans chaque canal
        V=np.zeros((len(cells),3))
        for k,(a,b) in enumerate(pairs): V[idx[a],k]=1/np.sqrt(2); V[idx[b],k]=sg[k]/np.sqrt(2)
        M=V.T@H@V; target=-g/4*sum(s)*np.eye(3)
        offmax=max(offmax,abs(M-np.diag(np.diag(M))).max())
        if sg==(1,1,1) and not np.allclose(M,target): ok=False; print(s,np.round(M,3))
print("M = -(g/4)(somme sigma) I pour les 16 signes :",ok, "| couplage hors diagonale max (toutes orientations) :",offmax)
