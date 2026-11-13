# C-86D : verification independante de la symetrie SO(2) de ChatGPT ; C-87 exploratoire (extension naive apres naissance).
exec(open('c86.py').read().split('rep=[]')[0])
def Jop(cells,idx,Jv):  # Jv : dict u -> dict w -> coeff (action sur vecteurs de sommets)
    N=len(cells); M=np.zeros((N,N))
    for c in cells:
        for j,v in enumerate(c):
            for w,a in Jv.get(v,{}).items():
                nc=list(c); nc[j]=w
                if len(set(nc))<len(nc): continue
                img,sg=sgn_sort(nc)
                if img in idx: M[idx[img],idx[c]]+=sg*a
    return M
Jm=np.array([[0,1,-1],[-1,0,1],[1,-1,0]],float)
def Jdict(ch):
    d={}
    for i,u in enumerate(ch):
        for j,w in enumerate(ch):
            if Jm[j,i]!=0: d.setdefault(u,{})[w]=Jm[j,i]   # J e_u = sum_w J[w,u] e_w
    return d
for kind in ('C76',):
    maxs,s,mirv,verts=build(kind,1); cells=R0(maxs,s)
    for g in (0.5,1.5,4.0):
        d,D,G,S,idx=ops_(cells,s,g); H=D+g*S@G
        Jv={**Jdict([1,2,3]),**Jdict([mirv[1],mirv[2],mirv[3]])}
        J=Jop(cells,idx,Jv)
        print(kind,g,'|[J,D]|=',np.abs(J@D-D@J).max(),'|[J,SG]|=',np.abs(J@S@G-S@G@J).max(),'J^3+3J=',np.abs(J@J@J+3*J).max(),'J≠0:',np.abs(J).max())
        Q=-1j/np.sqrt(3)*J; ev=np.round(np.linalg.eigvals(Q).real,6); print('  spec Q',sorted(set(ev)))
        E2=g*g+4; Vl=[l for l in levels(H) if abs(l[0]-np.sqrt(E2))<1e-8][0][1]
        Qr=Vl.T@(-1j/np.sqrt(3)*J)@Vl; print('  niveau E²=g²+4 dim',Vl.shape[1],'décomposition Q:',{q:int(np.sum(np.abs(np.linalg.eigvalsh(Qr)-q)<1e-6)) for q in (-1,0,1)})
# C-87 exploratoire : apres une naissance jumelee, l'extension naive (J sur les anciens sommets charges, nouveau sommet fixe) commute-t-elle ?
maxs,s,mirv,verts=build('C76',1); tp=[maxs[0]]; tm=[maxs[1]]
t=tp[0]; a,b=200,201; s2=dict(s); s2[a]=1; s2[b]=-1
bb=lambda T,x:[tuple(sorted(tuple(y for i,y in enumerate(T) if i!=j)+(x,))) for j in range(4)]
cells2=R0(bb(tp[0],a)+bb(tm[0],b),s2); d2,D2,G2,S2,idx2=ops_(cells2,s2,1.5); H2=D2+1.5*S2@G2
mv2={**mirv,a:b,b:a}
Jv={**Jdict([1,2,3]),**Jdict([mv2[1],mv2[2],mv2[3]])}
J2=Jop(cells2,idx2,Jv); print('C-87 naïf (sommet né fixe): |[J,H\']|=',np.abs(J2@H2-H2@J2).max())
# commutant de H' : dimension (diagnostic) et existence d'un generateur antisymetrique extensible
e,V=np.linalg.eigh(H2); mult=[]; i=0
while i<len(e):
    j=i
    while j<len(e) and abs(e[j]-e[i])<1e-9: j+=1
    mult.append(j-i); i=j
print('C-87 multiplicités spectrales après naissance :',sorted(mult,reverse=True)[:8],'(avant :',sorted([l[1].shape[1] for l in levels(D+1.5*S@G)],reverse=True)[:8],')')
