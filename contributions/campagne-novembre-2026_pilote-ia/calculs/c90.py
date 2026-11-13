# C-90 (protocole ChatGPT, 4 tests) execute par Claude, sur les histoires de C-89 (realisation enchassee, k=1, graines 0-7, 6 generations).
import numpy as np, random, itertools
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.diag([1,-1]).astype(complex)
Pi=lambda n:0.5*(np.eye(2)+n[0]*sx+n[1]*sy+n[2]*sz)
X0={100:np.array([1,1,1.]),1:np.array([1,-1,-1.]),2:np.array([-1,1,-1.]),3:np.array([-1,-1,1.])}
vol=lambda T,X:np.linalg.det(np.array([X[T[i]]-X[T[0]] for i in (1,2,3)]))
unit=lambda v:v/np.linalg.norm(v)
# controle exploratoire de ChatGPT : naissance au barycentre du tetra regulier
X=dict(X0); X[999]=sum(X0.values())/4; T=(100,1,2,3)
kids=[tuple(999 if i==m else T[i] for i in range(4)) for m in range(4)]
ns=[unit(X[T[m]]-sum(X[v] for v in kids[m])/4) for m in range(4)]
B=np.trace(Pi(ns[0])@Pi(ns[1])@Pi(ns[2])); print('exploratoire : n_i.n_j =',round(ns[0]@ns[1],6),' B_012 =',np.round(B,6),' i/(3√3) =',round(1/(3*np.sqrt(3)),6))
allph=[];sib=[];undef=0;tot=0;idem=[];mirr=[]
for seed in range(8):
    rng=random.Random(seed); X=dict(X0); T0=(100,1,2,3)
    axis={T0:unit(X[100]-sum(X0.values())/4)}   # axe initial : contact (C-88)
    tets=[T0]; nv=200
    for gen in range(6):
        j=rng.randrange(len(tets)); T=tets.pop(j)
        al=np.array([rng.random()+1e-3 for _ in range(4)]); al/=al.sum(); x=nv; nv+=1; X[x]=sum(al[i]*X[T[i]] for i in range(4))
        kids=[tuple(x if i==m else T[i] for i in range(4)) for m in range(4)]
        for m,K in enumerate(kids): axis[K]=unit(X[T[m]]-sum(X[v] for v in K)/4)   # C-90A : axe = sommet omis - barycentre de l'enfant
        tets+=kids
        b=np.trace(Pi(axis[kids[0]])@Pi(axis[kids[1]])@Pi(axis[kids[2]])); sib.append(np.angle(b) if abs(b)>1e-12 else np.nan)
    # C-90B : idempotence et rang des projecteurs
    for K in tets: P_=Pi(axis[K]); idem.append(max(np.abs(P_@P_-P_).max(),abs(np.trace(P_)-1)))
    # C-90A miroir : lignee miroir realisee par translation (epsilon_P=+1) -> axes identiques ; par reflexion -> axes reflechis
    R=np.diag([-1,1,1.]); 
    for K in tets:
        n=axis[K]; nr=unit(R@n)   # reflexion de l'axe
        mirr.append(abs(np.trace(Pi(n)@Pi(nr))))  # recouvrement des projecteurs miroir (1 si identiques)
    # C-90C : boucles autour des aretes interieures (cycle des tetras contenant l'arete, ordonnes par adjacence de faces)
    edges={}
    for K in tets:
        for e in itertools.combinations(sorted(K),2): edges.setdefault(e,[]).append(K)
    for e,ring in edges.items():
        if len(ring)<3: continue
        # ordonner le cycle : deux tetras sont voisins s'ils partagent une face contenant e
        order=[ring[0]]; rest=ring[1:]
        while rest:
            nxt=[K for K in rest if len(set(K)&set(order[-1]))==3]
            if not nxt: break
            order.append(nxt[0]); rest.remove(nxt[0])
        if rest or len(set(order[0])&set(order[-1]))!=3: continue   # arete de bord : pas de cycle ferme
        M=np.eye(2,dtype=complex)
        for K in order: M=M@Pi(axis[K])
        b=np.trace(M); tot+=1
        if abs(b)<1e-12: undef+=1
        else: allph.append(np.angle(b))
allph=np.array(allph); sib=np.array(sib)
print('C-90B : max |Π²-Π|, |trΠ-1| =',max(idem))
print('C-90A miroir par réflexion : recouvrement tr(Π_n Π_Rn) min =',round(min(mirr),4),'(1 = identique) ; par translation : identique')
print('C-90C fratries (3 premiers enfants de chaque naissance) : phases /π :',np.round(np.nanmin(sib)/np.pi,3),'à',np.round(np.nanmax(sib)/np.pi,3),'; |phase| > 0,01π :',np.mean(np.abs(sib)>0.01*np.pi))
print(f'C-90C/D boucles fermées autour d\'arêtes intérieures : {tot} boucles, {undef} indéfinies (trace nulle) ; phases non nulles (>0,01π) : {np.mean(np.abs(allph)>0.01*np.pi):.2f} ; |phase| moyenne {np.mean(np.abs(allph))/np.pi:.3f}π ; max {np.max(np.abs(allph))/np.pi:.3f}π')
print('signes : fratries >0 :',np.mean(sib>0),' ; boucles d\'arêtes >0 :',np.mean(allph>0),'<0 :',np.mean(allph<0))
