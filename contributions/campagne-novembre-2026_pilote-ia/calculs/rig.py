import numpy as np, itertools
rng=np.random.default_rng(1)
def R(P,E):
    n,d=P.shape; M=np.zeros((len(E),n*d))
    for k,(i,j) in enumerate(E):
        v=P[i]-P[j]; M[k,i*d:(i+1)*d]=v; M[k,j*d:(j+1)*d]=-v
    return M
def info(P,E):
    n,d=P.shape; r=np.linalg.matrix_rank(R(P,E),tol=1e-9)
    triv=d*(d+1)//2
    return dict(liberte_interne=n*d-triv-r, autocontraintes=len(E)-r)
for d in (2,3,4):
    for n in (d+1,d+2):
        P=rng.normal(size=(n,d)); E=list(itertools.combinations(range(n),2))
        print(f"d={d} K{n}",info(P,E))
# octaedre convexe (legerement perturbe) en 3D
P=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],float)+rng.normal(scale=0.05,size=(6,3))
opp={(0,1),(2,3),(4,5)}
E=[e for e in itertools.combinations(range(6),2) if e not in opp]
k4=sum(all(tuple(sorted(p)) in E for p in itertools.combinations(q,2)) for q in itertools.combinations(range(6),4))
print("octaedre: aretes",len(E),info(P,E),"nombre de K4 =",k4)
