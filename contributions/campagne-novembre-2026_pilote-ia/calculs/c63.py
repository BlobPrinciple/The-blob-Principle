import numpy as np, itertools, math
V=list(range(4)); cells=[c for k in range(1,5) for c in itertools.combinations(V,k)]
idx={c:i for i,c in enumerate(cells)}; n=len(cells)
d=np.zeros((n,n))
for c in cells:
    if len(c)<4:
        for v in V:
            if v not in c:
                s=tuple(sorted(c+(v,))); pos=s.index(v)
                d[idx[s],idx[c]]+=(-1)**pos
D=d+d.T; G=np.diag([(-1)**(len(c)-1) for c in cells])
H=D+1.5*G
ev=np.round(np.linalg.eigvalsh(H),6)
print('cellules',n,' D G + G D = 0 :',np.allclose(D@G+G@D,0),' H^2 = Delta + g^2 :',np.allclose(H@H,D@D+2.25*np.eye(n)))
print('valeurs propres H+ :',{v:list(ev).count(v) for v in sorted(set(ev))})
print('indice gradue = chi =',4-6+4-1)
print('C-62 (sqrt2-1)/4 =',(math.sqrt(2)-1)/4)
print('C-61 (576/625)=(24/25)^2 ; E[K_100]=',100/2+(1-math.exp(-200))/4)
