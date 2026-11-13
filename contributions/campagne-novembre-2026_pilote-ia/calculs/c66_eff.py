import numpy as np, itertools
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
cells=complex_from_max([(0,1,2,3)]); D,G,idx=ops(cells); g=1.5
E=[i for i,c in enumerate(cells) if len(c)==2]; R=[i for i,c in enumerate(cells) if len(c)!=2]
pairs=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
for s in [(1,1,1,1),(1,1,-1,-1),(1,1,1,-1)]:
    S=polar(cells,dict(enumerate(s))); H=D+g*S@G
    for z in (0.0,0.7):
        A=H[np.ix_(R,R)]-z*np.eye(len(R))
        Heff=H[np.ix_(E,E)]+H[np.ix_(E,R)]@np.linalg.solve(-A,H[np.ix_(R,E)])
        V=np.zeros((len(E),3)); Ei={cells[i]:k for k,i in enumerate(E)}
        for k,(a,b) in enumerate(pairs): V[Ei[a],k]=V[Ei[b],k]=1/np.sqrt(2)
        M=V.T@Heff@V
        print(s,"z=",z,"M_eff=\n",np.round(M,4),"\n  reel symetrique:",np.allclose(M,M.T) and np.isrealobj(M))
