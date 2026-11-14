exec(open('v1_audit.py').read().split("if __name__")[0])
from scipy.sparse.csgraph import shortest_path
import sys
R=int(sys.argv[1])
print('témoin cubique L=12,16,20 : distance moyenne',[round(float(np.mean(shortest_path(cubic(L),unweighted=True,indices=[0]))),2) for L in (12,16,20)])
rows=[]
for nb in (80,160,320,640,1280):
    D=[];N=[];S=[]
    for seed in range(3):
        L,F,acc=grow(nb,R,seed); A=dual(L,F); n=A.shape[0]
        src=np.random.default_rng(seed).choice(n,min(40,n),replace=False)
        d=shortest_path(A,unweighted=True,indices=src); D.append(d[np.isfinite(d)].mean()); N.append(n)
        S.append(list(ds(A,ts=(8,16,32,64,128)).values()))
    rows.append((nb,np.mean(N),np.mean(D),np.mean(S,axis=0)))
    print(f'R={R} naissances={nb} tétras={int(np.mean(N))} distance moyenne={np.mean(D):.2f} d_s(t=8,16,32,64,128)={np.round(np.mean(S,axis=0),2).tolist()}',flush=True)
N=np.array([r[1] for r in rows]); D=np.array([r[2] for r in rows])
for i in range(len(rows)-1):
    print(f'  dimension de Hausdorff locale entre {rows[i][0]} et {rows[i+1][0]} naissances : d_H = {np.log(N[i+1]/N[i])/np.log(D[i+1]/D[i]):.2f}')
