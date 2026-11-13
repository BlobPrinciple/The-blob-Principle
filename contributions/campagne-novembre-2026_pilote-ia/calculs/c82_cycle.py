# C-82(iii) : holonomie d'un cycle 3->2 puis 2->3 (retour exact au complexe de depart).
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
g=1.5
def transport(cells,s,cells2,sites):
    P,idx=kern(cells,s,g); P2,idx2=kern(cells2,s,g)
    Vs=np.array([P[:,idx[(c,)]] for c in sites]).T; Vs2=np.array([P2[:,idx2[(c,)]] for c in sites]).T
    Phi=np.zeros((len(cells2),len(sites)))
    for c,i in idx.items():
        if c in idx2: Phi[idx2[c]]+=Vs[i]
    return np.linalg.lstsq(Vs2,P2@Phi,rcond=None)[0]
for (k,seed,ngen,e) in [(2,3,4,(200,204)),(3,5,3,(200,202)),(3,3,4,(200,204))]:
    tp,tm,s,mir=grow(k,ngen,seed); sites=[100+i for i in range(k)]
    em=tuple(sorted(mir[v] for v in e))
    K=R0(tp+tm,s); Km=R0(move32(tp,e)+move32(tm,em),s)
    M1=transport(K,s,Km,sites); M2=transport(Km,s,K,sites); C=M2@M1
    ev=np.linalg.eigvals(C)
    w=np.ones(k)/k; c=np.sqrt(w); traj=[]
    for n in range(1,4001):
        c=C@c
        if n in (1,10,100,1000,4000): traj.append(np.round(c**2/np.sum(c**2),4).tolist())
    print(f"k={k} arete {e}: |M(2->3)-I|={np.max(abs(M2-np.eye(k))):.1e}  |cycle-I|={np.max(abs(C-np.eye(k))):.1e}  valeurs propres={np.round(ev,5)}")
    print("   poids sous n cycles (n=1,10,100,1000,4000):",traj)
