# C-88 / PR-1 (ChatGPT) execute par Claude. Cl3(C) fidele : e_i -> diag(s_i, -s_i). Tetraedre equilateral (C-58), k=1.
import numpy as np, itertools
exec(open('c86.py').read().split('rep=[]')[0])
s1=np.array([[0,1],[1,0]],complex); s2=np.array([[0,-1j],[1j,0]]); s3=np.diag([1,-1]).astype(complex)
E=[np.block([[m,np.zeros((2,2))],[np.zeros((2,2)),-m]]) for m in (s1,s2,s3)]; I4=np.eye(4)
ev=lambda v:sum(v[i]*E[i] for i in range(3)); om=E[0]@E[1]@E[2]
# sommets : c (contact) et a,b,d charges
X={'c':np.array([1,1,1.]),'a':np.array([1,-1,-1.]),'b':np.array([-1,1,-1.]),'d':np.array([-1,-1,1.])}
bary=sum(X.values())/4; n=(X['c']-bary)/np.linalg.norm(X['c']-bary)
def f(sig,nv,detO=1): return 0.5*(I4+sig*detO*1j*om)@(0.5*(I4+ev(nv)))
res={}
for sig in (1,-1):
    F=f(sig,n); res[f'f{sig}^2=f']=np.abs(F@F-F).max(); res[f'rang f{sig}']=np.linalg.matrix_rank(F)
    # dim de l'ideal a gauche Cl.f : rang de l'application x -> x f sur la base de Cl (16 mots)
    words=[I4]+[E[i] for i in range(3)]+[E[i]@E[j] for i,j in itertools.combinations(range(3),2)]+[om]
    res[f'dim Cl.f{sig}']=np.linalg.matrix_rank(np.array([(w@F).ravel() for w in words]))
# automorphismes du stabilisateur de c : matrices orthogonales permutant a,b,d
labs=['a','b','d']; out=[]
for p in itertools.permutations(labs):
    A=np.array([X[l] for l in labs]).T; B=np.array([X[l] for l in p]).T
    O=B@np.linalg.inv(A); det=round(np.linalg.det(O))
    for sig in (1,-1):
        img=f(sig,O@n,det)   # rho_O(f_sig)
        same=np.abs(img-f(sig,n)).max()<1e-12; swap=np.abs(img-f(-sig,n)).max()<1e-12
        out.append((p,det,sig,'f_sig' if same else ('f_-sig' if swap else 'autre')))
for o in out: print(o)
print(res)
# C-88B : epsilon_P depuis le miroir EXISTANT (permop de c86, signe sur la cellule maximale)
maxs,s,mirv,verts=build('C76',1); cells=R0(maxs,s); d,D,G,S,idx=ops_(cells,s,1.5); P=permop(cells,idx,mirv)
tplus=[c for c in cells if len(c)==4 and s[[v for v in c if v<100][0]]>0][0]; tminus=tuple(sorted(mirv[v] for v in tplus))
eps=P[idx[tminus],idx[tplus]]; print('cellule +',tplus,'-> cellule -',tminus,'; epsilon_P =',eps)
# transposition tau (echange de deux sommets charges dans les deux lignees) : signe sur la cellule maximale
ch=[v for v in tplus if v<100]; tau={**{v:v for v in verts},ch[0]:ch[1],ch[1]:ch[0],mirv[ch[0]]:mirv[ch[1]],mirv[ch[1]]:mirv[ch[0]]}
T=permop(cells,idx,tau); print('tau sur cellule + :',T[idx[tplus],idx[tplus]],'; sur cellule - :',T[idx[tminus],idx[tminus]])
# candidat : lignee sigma porte f_sigma (omega_sigma defini par la cellule maximale orientee de sa lignee)
# P : (lignee+, f_+) -> (lignee-, idempotent de signe eps*(+1)) ; tau P : signe eps*det(tau)
for name,sgn in (('P',eps),('tauP',eps*T[idx[tplus],idx[tplus]])):
    print(name,': f_+ (lignée +) -> idempotent de signe',int(sgn),'dans la lignée - ; candidat de la lignée - = f_- ->','PRÉSERVE le couple' if sgn==-1 else 'NE préserve PAS le couple')
# C-88C : relevements de la rotation de 120 deg autour de n
e1=np.cross(n,[1,0,0]); e1/=np.linalg.norm(e1); e2=np.cross(n,e1)
B12=ev(e1)@ev(e2); sgen=np.cos(np.pi/3)*I4-np.sin(np.pi/3)*B12   # exp(-pi/3 e1e2)
for nm,ss in (('s',sgen),('-s',-sgen)):
    c3=ss@ss@ss; print(nm,'^3 = ',('-1' if np.abs(c3+I4).max()<1e-12 else ('+1' if np.abs(c3-I4).max()<1e-12 else '?')),
          '; phases sur Cl.f+ :',np.round(np.angle(np.linalg.eigvals((ss@f(1,n))[np.ix_(*[np.where(np.abs(f(1,n)).sum(1)>1e-9)[0]]*2)]))/np.pi,4),'π')
# verification : s realise bien la rotation de 120 deg autour de n (s e_v s^-1 = e_{Rv})
R=lambda v: np.cos(2*np.pi/3)*v+np.sin(2*np.pi/3)*np.cross(n,v)+(1-np.cos(2*np.pi/3))*np.dot(n,v)*n
print('s e_a s^-1 = e_{R a} :',np.abs(sgen@ev(X['a'])@np.linalg.inv(sgen)-ev(R(X['a']))).max()<1e-12, '| R(a) parmi b,d :',[l for l in 'bd' if np.allclose(R(X['a']),X[l])])
