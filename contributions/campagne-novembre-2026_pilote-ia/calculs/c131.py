# C-131 — DISPERSION AU-DELA DE k^2 SUR LA TRAME DE LA MITOSE (protocole propose par ChatGPT dans C-130, execute par Claude, 12 nov. 2026).
# PROTOCOLE (fige par ChatGPT) : memes poids diagonaux que C-129, SANS reajustement ; developpement de Bloch jusqu'a l'ordre k^4 dans les directions
#   (1,0,0), (1,1,0), (1,1,1) et des directions generiques ; deux observables : (i) anisotropie directionnelle d'une meme branche,
#   (ii) separation entre branches de degres differents.
# Methode : lambda(k)/k^2 = c0 + beta k^2 + gamma k^4, ajuste sur |k| = 0.4, 0.2, 0.1, 0.05 ; puis beta(direction) = a + b * Somme k_i^4 (forme cubique).
# PREDICTION ENREGISTREE AVANT CALCUL (Claude) :
#   P1. beta != 0 dans chaque branche (correction de reseau) ;
#   P2. b != 0 : anisotropie a l'ordre k^4, de la forme cubique a + b Somme k_i^4 pour les branches scalaires A et C ;
#   P3. (a, b) differents d'une branche a l'autre : separation des branches a l'ordre k^4 ;
#   P4. les deux polarisations de la branche B sont degenerees selon (1,0,0) et (1,1,1), separees selon (1,1,0) et les directions generiques.
#   Donc : symetrie exacte a maille finie [FAIL attendu] ; correction relative en (k a)^2, qui s'annule a la limite continue.
import math, numpy as np
src=open('c117c.py').read().split("for name in ('Kuhn','C3'):")[0]; ns={}; exec(src,ns); S_,dmat,mass=ns['build']('C3')
M0=[mass(p,np.zeros(3)).real for p in range(4)]; w=[np.diag(M).copy() for M in M0]; h=lambda M:np.sort(np.linalg.eigvalsh((M+M.conj().T)/2))
def lam(w,k):
    q=k@k; d0,d1,d2=dmat(1,k),dmat(2,k),dmat(3,k)
    A=h(np.diag(w[0]**-.5)@d0.conj().T@np.diag(w[1])@d0@np.diag(w[0]**-.5)); Bv=h(np.diag(w[1]**-.5)@d1.conj().T@np.diag(w[2])@d1@np.diag(w[1]**-.5)); C=h(np.diag(w[3]**.5)@d2@np.diag(1/w[2])@d2.conj().T@np.diag(w[3]**.5))
    nz=lambda v:[x for x in v if x>1e-6*q]; return np.array([nz(A)[0]/q,nz(Bv)[0]/q,nz(Bv)[1]/q,nz(C)[0]/q])
# poids de C-129, a l'identique (meme calibrage, meme direction, meme |k|)
cA,cB,_,cC=lam(w,1e-3*np.array([1.,2.,3.])/np.sqrt(14)); l1=math.sqrt(cB/cA); c2=cA*l1; l3=c2/cC
w2=[w[0],w[1]*l1,w[2],w[3]*l3]; w2=[x/c2**(i) for i,x in enumerate(w2)]
dirs=[(1,0,0),(1,1,0),(1,1,1),(1,2,3),(3,-1,2),(2,1,0),(5,3,1),(1,1,2),(4,1,1),(2,3,6)]
ks=np.array([0.4,0.2,0.1,0.05]); names=['A (sommets)','B pol. 1','B pol. 2','C (volumes)']; res=[]
for dv in dirs:
    u=np.array(dv,float)/np.linalg.norm(dv); Y=np.array([lam(w2,kk*u) for kk in ks])        # (4 tailles, 4 branches)
    V=np.vstack([np.ones(4),ks**2,ks**4]).T; coef=np.linalg.lstsq(V,Y,rcond=None)[0]          # c0, beta, gamma
    res.append((dv,(u**4).sum(),coef))
print('direction      S4=Σk̂⁴ |', ' | '.join(f'{n:>22s}' for n in names)); print(' '*24+'|'+' | '.join(f'{"c0-1":>10s} {"beta":>11s}' for _ in names))
for dv,s4,c in res: print(f'{str(dv):14s} {s4:.4f}  | '+' | '.join(f'{c[0,i]-1:+10.1e} {c[1,i]:+11.6f}' for i in range(4)))
s4=np.array([r[1] for r in res]); B=np.array([r[2][1] for r in res])
print('\nAjustement beta = a + b·Σk̂⁴ sur les 10 directions :')
for i,n in enumerate(names):
    X=np.vstack([np.ones(len(s4)),s4]).T; (a,b),*_=np.linalg.lstsq(X,B[:,i],rcond=None); r=B[:,i]-X@np.array([a,b])
    print(f'  {n:12s}: a = {a:+.6f}  b = {b:+.6f}  résidu max = {abs(r).max():.1e}  étendue de beta = {np.ptp(B[:,i]):.6f}')
m=(B[:,1]+B[:,2])/2; X=np.vstack([np.ones(len(s4)),s4]).T; (a,b),*_=np.linalg.lstsq(X,m,rcond=None)
print(f'  B (moyenne des deux polarisations) : a = {a:+.6f}  b = {b:+.6f}  résidu max = {abs(m-X@np.array([a,b])).max():.1e}')
print('\nÉcart entre les deux polarisations de B (beta2 - beta1) par direction :')
for (dv,s,c) in res: print(f'  {str(dv):12s} {c[1,2]-c[1,1]:+.6f}')
print('\nSéparation des branches à l\'ordre k⁴ (beta moyenné sur les directions) :',' ; '.join(f'{n} {B[:,i].mean():+.6f}' for i,n in enumerate(names)))
print('Contrôle : réseau cubique à six voisins, lambda = 4 Σ sin²(k_i/2) : beta = -S4/12 → a = 0, b = -1/12 =',round(-1/12,6))
