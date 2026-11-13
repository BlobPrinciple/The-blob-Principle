# Controle discriminant : subdivision stellaire d'un d-simplexe (d = 2,3,4,5), graphe des sommets, 32768 naissances, 4 graines.
# Si d_s suit d, le "3" est structurel ; sinon c'est une coincidence du graphe a moyeux.
exec(open('c113.py').read().split("if __name__")[0])
TS=(4,8,16,32,64,128)
def one(a):
    d,nb,seed=a; rng=random.Random(seed); S=[tuple(range(d+1))]; edges=list(itertools.combinations(range(d+1),2)); nv=d+1
    for n in range(nb):
        i=rng.randrange(len(S)); t=S[i]
        S[i]=tuple(nv if j==0 else t[j] for j in range(d+1))
        for k in range(1,d+1): S.append(tuple(nv if j==k else t[j] for j in range(d+1)))
        edges+=[(v,nv) for v in t]; nv+=1
    A=graph(nv,edges,0); st=np.random.default_rng(seed).choice(nv,300,replace=False); P,_=walk(A,st)
    return d,dsof(P),float(shortest_path(A,unweighted=True,indices=st[:20]).mean())
if __name__=='__main__':
    with Pool(2) as p: res=p.map(one,[(d,32768,s) for d in (2,3,4,5) for s in range(1100,1104)])
    for d in (2,3,4,5):
        rs=[x for x in res if x[0]==d]; print('d =',d,'d_s(4..128) =',np.round(np.mean([x[1] for x in rs],axis=0),2).tolist(),'distance moyenne =',round(np.mean([x[2] for x in rs]),2))
