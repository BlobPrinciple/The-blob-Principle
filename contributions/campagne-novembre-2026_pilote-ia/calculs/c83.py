# C-83 (protocole Claude, audite et accepte par ChatGPT ; controles A,B,C ajoutes avant calcul).
# Etat initial : complexe apres 3 naissances jumelees (graine 0) ; ensuite uniquement 2<->3 en paires miroirs.
# Tirage uniforme parmi orbites admissibles ; N=10000 ; 64 graines ; g in {0.5,1.5} ; k in {2,3} ; a0 uniforme (racines des poids egaux) et a0=(1,2[,3]).
# Lyapunov : produit des M~_j = G(K_{j+1})^{1/2} M_j G(K_j)^{-1/2}, QR repete. Selection : max w > 1-1e-6 (premier passage, maintien final).
# Cache exact par complexe (espace d'etats fini) : pas d'approximation supplementaire.
import sys, json, random, numpy as np
exec(open('c82_marche.py').read().split("if __name__")[0])
from scipy.linalg import sqrtm
def key(tp): return tuple(sorted(tp))
KC={}; TC={}
def info(tp,tm,s,g,F):
    kk=key(tp)
    if kk not in KC:
        cells=R0(tp+tm,s); P,idx,Vs=basis(cells,s,g,F); G=Vs.T@Vs
        KC[kk]=(cells,P,idx,Vs,np.real(sqrtm(G)),np.real(np.linalg.inv(sqrtm(G))),round(np.trace(P)))
    return KC[kk]
def run(g,k,a0,seed,N,T0):
    tp,tm,s,mir,nv=T0; F=[100+i for i in range(k)]; rng=random.Random(seed)
    a=np.array(a0,float); Q=np.eye(k); lyap=np.zeros(k); snaps={}; first=None; blocks=0; visited=set(); preserve={}
    for n in range(1,N+1):
        mv=[m for m in moves(tp,s,F) if m[0]!='B']; rng.shuffle(mv); done=False
        I=info(tp,tm,s,g,F)
        for m in mv:
            st=apply(m,tp,tm,s,mir,nv); tk=(key(tp),key(st[0]))
            if tk not in TC:
                J=info(st[0],st[1],st[2],g,F)
                if J[6]!=k or any(len(c)>1 and pol(c,st[2])==0 for c in J[0]): TC[tk]=None
                else:
                    Phi=np.zeros((len(J[0]),k))
                    for c,i in I[2].items():
                        if c in J[2]: Phi[J[2][c]]+=I[3][i]
                    TC[tk]=np.linalg.lstsq(J[3],J[1]@Phi,rcond=None)[0]
            M=TC[tk]
            if M is None: continue
            J=info(st[0],st[1],st[2],g,F); Mt=J[4]@M@I[5]
            Q,R=np.linalg.qr(Mt@Q); lyap+=np.log(np.abs(np.diag(R)))
            a=M@a; a/=np.linalg.norm(a); tp,tm,s,mir,nv=st; done=True; visited.add(key(tp))
            off=np.abs(M)-np.diag(np.diag(np.abs(M))); preserve[m[0]]=max(preserve.get(m[0],0),off.max()); break
        if not done: blocks=n; break
        w=a**2
        if first is None and w.max()>1-1e-6: first=n
        if n in (100,1000,3000,10000): snaps[n]=dict(w=w.tolist(),chi=sorted((lyap/n).tolist(),reverse=True))
    return dict(snaps=snaps,first=first,final=(a**2).tolist(),blocks=blocks,nvis=len(visited),offmax=preserve)
#MAIN
if __name__=='__main__':
    g=float(sys.argv[1]); k=int(sys.argv[2]); a0=json.loads(sys.argv[3]); s0,s1=int(sys.argv[4]),int(sys.argv[5])
    tp,tm,s,mir=init(k); nv=200; rng=random.Random(0)
    for _ in range(3):
        m=('B',tp[rng.randrange(len(tp))]); tp,tm,s,mir,nv=apply(m,tp,tm,s,mir,nv)
    T0=(tp,tm,s,mir,nv)
    print('init: tetras',len(tp),'mouvements 2-3/3-2 dispo',len([m for m in moves(tp,s,[100+i for i in range(k)]) if m[0]!='B']),flush=True)
    res=[run(g,k,a0,sd,10000,T0) for sd in range(s0,s1)]
    json.dump(res,open(f'c83_g{g}_k{k}_{"".join(map(str,a0))}_{s0}.json','w')); print('done',len(KC),'complexes')
