# C-94 (Claude, criteres figes AVANT calcul) : dynamique "trempe + dephasage" sans operateur nouveau.
# Naissance jumelee = inclusion S (soudaine) ; entre deux naissances, evolution e^{-iH't} pendant un temps d'attente inconnu
# => moyenne temporelle = dephasage complet entre niveaux d'energie distincts (hypothese declaree : attente >> 1/ecart, ecart >= g).
# On suit la matrice densite complete rho, SANS projection sur le noyau. Observables sur le bloc noyau, en coordonnees de sites :
#   A = V^+ rho V^+†  ;  poids w_i = A_ii / tr A ; coherence c_ij = |A_ij|/sqrt(A_ii A_jj).
# SUCCES (decoherence a poids de Born) : c_ij -> 0 ET w_i reste egal a |a_i|^2/sum|a|^2 (ecart < 0.02).
# ECHEC : coherence qui ne decroit pas, ou poids qui derivent.
import numpy as np, random, sys
exec(open('c80_2A.py').read().split('g=1.5; out=[]')[0])
def dephase(rho,Hm):
    e,U=np.linalg.eigh(Hm); r=U.T@rho@U; lab=np.cumsum(np.r_[0,np.diff(e)>1e-8]); mask=lab[:,None]==lab[None,:]
    return U@(r*mask)@U.T, e
def run(k,a0,seed,ngen,g=1.5):
    rng=random.Random(seed)
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
    tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]; F=[100+i for i in range(k)]; nv=200
    cells=R0(tp+tm,s); Hm,idx=H(cells,s,g); P,_=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
    psi=V@np.array(a0,float); psi/=np.linalg.norm(psi); rho=np.outer(psi,psi); out=[]
    for gen in range(ngen+1):
        Vp=np.linalg.pinv(V); A=Vp@rho@Vp.T; w=np.diag(A)/np.trace(A)
        coh=[abs(A[i,j])/np.sqrt(A[i,i]*A[j,j]) for i in range(k) for j in range(i+1,k)]
        out.append((gen,len(cells),np.trace(rho),np.trace(P@rho),w.copy(),max(coh)))
        if gen==ngen: break
        j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir)
        a,b=nv,nv+1; nv+=2; sg=pol(t,s) or 1; s[a]=sg; s[b]=-sg; mir[a]=b; mir[b]=a
        tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
        tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
        cells2=R0(tp+tm,s); H2,idx2=H(cells2,s,g); S=np.zeros((len(cells2),len(cells)))
        for c,i in idx.items():
            if c in idx2: S[idx2[c],i]=1
        rho=S@rho@S.T; rho,_=dephase(rho,H2)
        cells,idx=cells2,idx2; P,_=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T
    return out
if __name__=='__main__':
    for k,a0 in ((2,(1,2)),(2,(1,1)),(3,(1,2,3))):
        w0=np.array(a0,float)**2/np.sum(np.array(a0,float)**2)
        print(f'--- k={k}, a0={a0}, poids de Born initiaux {np.round(w0,4)}')
        allw=[];allc=[]
        for seed in range(6):
            o=run(k,a0,seed,7); allw.append([x[4] for x in o]); allc.append([x[5] for x in o])
            if seed==0:
                for x in o: print(f'  gén {x[0]} cellules {x[1]:4d} tr ρ={x[2]:.4f} occupation du noyau={x[3]:.4f} poids={np.round(x[4],4)} cohérence max={x[5]:.4f}')
        allw=np.array(allw); allc=np.array(allc)
        print('  moyenne sur 6 graines, génération 7 : poids',np.round(allw[:,-1].mean(0),4),'± ',np.round(allw[:,-1].std(0),4),'; cohérence',round(allc[:,-1].mean(),4),'(min',round(allc[:,-1].min(),4),'max',round(allc[:,-1].max(),4),')')
