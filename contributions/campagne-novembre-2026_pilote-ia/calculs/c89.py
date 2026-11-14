# C-89 / PR-1 (ChatGPT) execute par Claude : realisation enchassee (metrique ambiante conservee), k=1, graines 0-7, 6 generations.
import numpy as np, random, itertools
exec(open('c86.py').read().split('rep=[]')[0])
X0={100:np.array([1,1,1.]),1:np.array([1,-1,-1.]),2:np.array([-1,1,-1.]),3:np.array([-1,-1,1.])}
vol=lambda T,X:np.linalg.det(np.array([X[T[i]]-X[T[0]] for i in (1,2,3)]))
statsA=[];statsC=[];statsD=[]
for seed in range(8):
    rng=random.Random(seed); X=dict(X0); T0=(100,1,2,3)   # orientation initiale : vol>0
    if vol(T0,X)<0: T0=(100,2,1,3)
    tets=[T0]; nv=200; signs=[]
    for gen in range(6):
        j=rng.randrange(len(tets)); T=tets.pop(j)
        al=np.array([rng.random()+1e-3 for _ in range(4)]); al/=al.sum()
        x=nv; nv+=1; X[x]=sum(al[i]*X[T[i]] for i in range(4))
        kids=[tuple(x if i==m else T[i] for i in range(4)) for m in range(4)]   # sommet ne insere a la place du sommet retire
        # A : volumes orientes et rapports
        for m,K in enumerate(kids): statsA.append((vol(K,X)>0, abs(vol(K,X)/vol(T,X)-al[m])))
        # identite des bords : somme des bords des enfants = bord du parent (chaines orientees)
        def bd(Tt):
            out={}
            for i in range(4):
                f=Tt[:i]+Tt[i+1:]; s_,sg=sgn_sort(f); out[s_]=out.get(s_,0)+(-1)**i*sg
            return out
        tot={}
        for K in kids:
            for f_,v in bd(K).items(): tot[f_]=tot.get(f_,0)+v
        tot={f_:v for f_,v in tot.items() if v!=0}; statsA.append((tot==bd(T),0.0))
        tets+=kids
    # C : axes des tetras contenant c, compares a l'axe initial
    n0=X[100]-sum(X0.values())/4; n0/=np.linalg.norm(n0); angs=[];nocont=0
    for T in tets:
        if 100 in T:
            b=sum(X[v] for v in T)/4; n=X[100]-b; n/=np.linalg.norm(n); angs.append(np.degrees(np.arccos(np.clip(n@n0,-1,1))))
        else: nocont+=1
    statsC.append((len(tets),nocont,max(angs),np.mean(angs)))
print('C-89A : volumes orientés >0 :',all(s[0] for s in statsA),'; max |V_i/V - alpha_i| :',max(s[1] for s in statsA),'; bords conservés : tous' if all(s[0] for s in statsA) else '')
print('C-89B : orientation ambiante identique pour tous les tétraèdres => p_sigma hérité (conditionnel à la métrique enchâssée)')
for i,(nt,nc,mx,mn) in enumerate(statsC): print(f'C-89C graine {i}: {nt} tétras, {nc} sans le contact (pas d\'axe), écart angulaire des axes au contact : moyen {mn:.1f}°, max {mx:.1f}°')
# D : survie du groupe G_H (automorphismes commutant avec P et Sigma) sous naissances jumelees signees
exec(open('c87.py').read().split('for k in (1,2):')[0])
for seed in range(4):
    row=[]
    for ngen in range(4):
        tp,tm,s,mir=grow2(1,ngen,seed); cells=R0(tp+tm,s); d,D,G,S,idx=ops_(cells,s,1.5)
        verts=sorted({v for c in cells for v in c}); cnt=0; has_tauP=False
        ch=sorted(v for v in verts if s[v]>0)
        for p in itertools.permutations(ch):
            perm={**{v:v for v in verts},**dict(zip(ch,p))}; perm.update({mir[u]:mir[perm[u]] for u in ch})
            if any(s[perm[v]]!=s[v] for v in verts): continue
            U=permop(cells,idx,perm)
            if U is None: continue
            cnt+=1
        row.append(cnt)
    print(f'C-89D graine {seed}: |G_H| (k=1) générations 0→3 : {row}')
