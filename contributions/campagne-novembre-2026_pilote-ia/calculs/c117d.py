# C-117 quater — POIDS METRIQUES DIAGONAUX (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Motif (C-125, ChatGPT) : avec les masses de Whitney, non diagonales, la polarite Sigma n'est plus auto-adjointe [T]. Or tout poids DIAGONAL
#   commute avec Sigma et Gamma : H = D + g Sigma Gamma reste auto-adjoint et les theoremes de modes proteges survivent.
# Question : des poids diagonaux suffisent-ils pour UNE seule vitesse sur la trame de la mitose (C~3), ou les etoiles circoncentriques degenerent ?
# Bras : L1 = masses de Whitney condensees par somme des lignes (a k = 0) ; L2 = diagonale de la masse de Whitney, renormalisee par degre pour
#   garder la meme trace que la masse complete. Trames : Kuhn (coordonnees cubiques) et C~3.
# CRITERE : poids strictement positifs, c_A = c_B = c_C a 1 % pres, isotropie < 1 % a |k| = 0,01, pas de birefringence.
# PREDICTION ENREGISTREE : L1 PASS sur les 0-formes (c_A = 1) mais FAIL global (les 1-formes condensees ne sont pas consistantes) ; L2 FAIL.
import itertools, numpy as np, scipy.linalg as sl
import importlib.util, sys
spec=importlib.util.spec_from_file_location('c117c','c117c.py'); 
src=open('c117c.py').read().split("for name in ('Kuhn','C3'):")[0]; ns={}; exec(src,ns); build=ns['build']
h=lambda M:np.sort(np.linalg.eigvalsh((M+M.conj().T)/2))
for name in ('Kuhn','C3'):
    S,dmat,mass=build(name); M0=[mass(p,np.zeros(3)).real for p in range(4)]
    for arm in ('L1','L2'):
        if arm=='L1': w=[M.sum(1) for M in M0]
        else: w=[np.diag(M)*np.trace(M)/np.trace(np.diag(np.diag(M))) for M in M0]; w=[np.diag(M)*M.sum()/np.diag(M).sum() for M in M0]
        pos=all((x>1e-14).all() for x in w)
        print(f'{name} {arm}: poids positifs={pos} ; poids distincts par degré : '+' | '.join(str(sorted(set(np.round(x,6)))) for x in w))
        if not pos: continue
        for eps in (0.1,0.01):
            rows=[]
            for dv in ((1,0,0),(1,1,0),(1,1,1),(1,2,3),(3,-1,2)):
                k=eps*np.array(dv,float)/np.linalg.norm(dv); q=eps**2; d0,d1,d2=dmat(1,k),dmat(2,k),dmat(3,k)
                A=h(np.diag(w[0]**-.5)@d0.conj().T@np.diag(w[1])@d0@np.diag(w[0]**-.5)); Bv=h(np.diag(w[1]**-.5)@d1.conj().T@np.diag(w[2])@d1@np.diag(w[1]**-.5)); C=h(np.diag(w[3]**.5)@d2@np.diag(1/w[2])@d2.conj().T@np.diag(w[3]**.5))
                nz=lambda v:[x for x in v if x>1e-6*q]; rows.append((nz(A)[0]/q,nz(Bv)[0]/q,nz(Bv)[1]/q,nz(C)[0]/q))
            r=np.array(rows)
            print(f'   |k|={eps}: c_A²={r[:,0].mean():.6f} (anis. {np.ptp(r[:,0])/r[:,0].mean():.1e}) c_B²={r[:,1].mean():.6f}/{r[:,2].mean():.6f} (anis. {np.ptp(r[:,1:3])/r[:,1:3].mean():.1e}) c_C²={r[:,3].mean():.6f} (anis. {np.ptp(r[:,3])/r[:,3].mean():.1e})')
