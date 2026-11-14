# Controle exploratoire hors protocole : lignee isolee, bras A, graphe des sommets, tailles plus grandes ; d_s et distance moyenne.
exec(open('c113.py').read().split("if __name__")[0])
TS=(4,8,16,32,64,128,256)
def one(a):
    nb,seed=a; nv,edges=lineage(nb,seed,'A'); A=graph(nv,edges,0); rng=np.random.default_rng(seed)
    st=rng.choice(nv,300,replace=False); P,_=walk(A,st,tmax=385)
    d=shortest_path(A,unweighted=True,indices=st[:30]); deg=np.array(A.sum(1)).ravel()
    return nb,dsof(P),float(d.mean()),int(deg.max()),float(deg.mean())
if __name__=='__main__':
    with Pool(2) as p: res=p.map(one,[(nb,s) for nb in (2048,8192,32768) for s in range(1000,1006)])
    prev=None
    for nb in (2048,8192,32768):
        rs=[x for x in res if x[0]==nb]; dm=np.mean([x[2] for x in rs])
        print(nb,'d_s(4..256)=',np.round(np.mean([x[1] for x in rs],axis=0),2).tolist(),'distance=',round(dm,2),'degré max=',np.mean([x[3] for x in rs]),'moyen=',round(np.mean([x[4] for x in rs]),2), '' if prev is None else f'd_H local={np.log(nb/prev[0])/np.log(dm/prev[1]):.1f}')
        prev=(nb,dm)
