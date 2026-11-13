# C-117 — UNE SEULE VITESSE ? (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Fait acquis [T, C-63] : sur une lignee, H = D + g Sigma Gamma verifie H^2 = Delta + g^2, avec D = d + d^dagger.
# Si la trame est un espace 3D etendu, Delta doit donner E^2 = g^2 + c^2 k^2 avec UNE vitesse c pour tous les secteurs.
# Les valeurs propres non nulles de Delta vont par paires de degres : A = (0-formes, 1-formes longitudinales),
#   B = (1-formes transverses, 2-formes), C = (2-formes, 3-formes). Trois vitesses c_A, c_B, c_C.
# Trame : triangulation de Kuhn du tore (germe canonique du master, valence 36/7), analyse de Bloch exacte (maille : 1 sommet, 7 aretes, 12 faces, 6 tetras).
# Metrique de reference : celle ou la marche sur les sommets est isotrope (reseau cubique centre ; les 14 voisins a distances sqrt(3)/2 et 1).
# Bras 1 : D du master, produits scalaires NON ponderes (tous les poids = 1).
# Bras 2 : etoiles de Hodge metriques (dual circoncentrique / primal) de la geometrie cubique centree.
# CRITERE : isotropie (ecart relatif entre directions < 1 % a k -> 0) ET c_A = c_B = c_C a 1 % pres ET pas de birefringence dans B.
# PREDICTION ENREGISTREE : bras 1 FAIL (trois vitesses differentes) ; bras 2 PASS.
import itertools, numpy as np
E3=np.eye(3,dtype=int)
def shapes():
    S={0:[((0,0,0),)]}
    for p in (1,2,3):
        S[p]=[]
        for perm in itertools.permutations(range(3)):
            path=[np.zeros(3,int)]
            for a in perm: path.append(path[-1]+E3[a])
            for idx in itertools.combinations(range(4),p+1):
                v=[path[i] for i in idx]; sh=tuple(tuple(int(z) for z in x-v[0]) for x in v)
                if sh not in S[p]: S[p].append(sh)
    return S
S=shapes(); assert [len(S[p]) for p in range(4)]==[1,7,12,6]
def dmat(p,k):  # d_{p-1} : C^{p-1} -> C^p  (matrice |S_p| x |S_{p-1}|), cobord = transposee du bord
    M=np.zeros((len(S[p]),len(S[p-1])),complex)
    for i,sh in enumerate(S[p]):
        for j in range(p+1):
            f=[np.array(x) for q,x in enumerate(sh) if q!=j]; shift=f[0]; fs=tuple(tuple(int(z) for z in x-shift) for x in f)
            M[i,S[p-1].index(fs)]+=(-1)**j*np.exp(1j*np.dot(k,shift))
    return M
B=np.array([[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]).T   # colonnes = images de e1,e2,e3 (reseau cubique centre)
def geom():
    # etoiles de Hodge circoncentriques, calculees sur un patch (toutes les cellules touchant la maille 0)
    def cc(pts):
        pts=np.array(pts,float); A=2*(pts[1:]-pts[0]); b=(pts[1:]**2).sum(1)-(pts[0]**2).sum()
        if len(pts)==4: return np.linalg.solve(A,b)
        # circoncentre dans le plan affine
        x=np.linalg.lstsq(np.vstack([A,*np.atleast_2d(np.linalg.svd(A)[2][len(pts)-1:])]),np.concatenate([b,[np.dot(n,pts[0]) for n in np.atleast_2d(np.linalg.svd(A)[2][len(pts)-1:])]]),rcond=None)[0]
        return x
    pos=lambda v:B@np.array(v,float)
    tets=[(np.array(a),sh) for a in itertools.product(range(-2,3),repeat=3) for sh in S[3]]
    def vol(pts):
        pts=np.array(pts,float); M=pts[1:]-pts[0]
        return np.sqrt(abs(np.linalg.det(M@M.T)))/np.prod(range(1,len(pts)))
    star={0:[],1:[],2:[],3:[]}
    V3=vol([pos(x) for x in S[3][0]]); star[3]=[1/vol([pos(x) for x in sh]) for sh in S[3]]
    tl=[[tuple(int(z) for z in a+np.array(x)) for x in sh] for a,sh in tets]
    for sh in S[2]:
        f=set(sh); inc=[t for t in tl if f<=set(t)]; assert len(inc)==2
        c1,c2=[cc([pos(x) for x in t]) for t in inc]; star[2].append(np.linalg.norm(c1-c2)/vol([pos(x) for x in sh]))
    for sh in S[1]:
        e=set(sh); inc=[t for t in tl if e<=set(t)]; mid=(pos(sh[0])+pos(sh[1]))/2; area=0
        for t in inc:
            ct=cc([pos(x) for x in t])
            for o in [x for x in t if x not in e]:
                cf=cc([pos(x) for x in list(sh)+[o]]); area+=vol([mid,cf,ct])
        star[1].append(area/np.linalg.norm(pos(sh[1])-pos(sh[0])))
    star[0]=[abs(np.linalg.det(B))]
    return star,[len([t for t in tl if set(sh)<=set(t)]) for sh in S[1]]
star,val=geom()
print('valences des 7 arêtes :',val,' moyenne',np.mean(val),' (36/7 =',36/7,')')
print('longueurs des 7 arêtes :',[round(float(np.linalg.norm(B@np.array(sh[1]))),4) for sh in S[1]])
print('étoiles : *0',np.round(star[0],4),'*1',np.round(star[1],4),'*2',np.round(star[2],4),'*3',np.round(star[3],4))
def speeds(kc,weighted):
    k=B.T@kc   # phase = kc.(B n) = (B^T kc).n
    d0,d1,d2=dmat(1,k),dmat(2,k),dmat(3,k)
    w=[np.array(star[p]) if weighted else np.ones(len(S[p])) for p in range(4)]; q=np.dot(kc,kc)
    h=lambda M:np.sort(np.linalg.eigvalsh((M+M.conj().T)/2))
    A=h(np.diag(w[0]**-.5)@d0.conj().T@np.diag(w[1])@d0@np.diag(w[0]**-.5))
    Bv=h(np.diag(w[1]**-.5)@d1.conj().T@np.diag(w[2])@d1@np.diag(w[1]**-.5))
    C=h(np.diag(w[3]**.5)@d2@np.diag(1/w[2])@d2.conj().T@np.diag(w[3]**.5))
    return A[0]/q, Bv[1]/q, Bv[2]/q, C[0]/q, Bv[0]/q
dirs={'(1,0,0)':(1,0,0),'(1,1,0)':(1,1,0),'(1,1,1)':(1,1,1),'(1,2,3)':(1,2,3),'(3,-1,2)':(3,-1,2)}
for weighted in (False,True):
    print('\n=== bras',2 if weighted else 1,'(étoiles métriques)' if weighted else '(non pondéré, D du master)')
    for eps in (0.3,1e-1,1e-2):
        rows=[]
        for name,dv in dirs.items():
            kc=eps*np.array(dv,float)/np.linalg.norm(dv); rows.append(speeds(kc,weighted))
        rows=np.array(rows)
        print(f'|k|={eps:g}: c_A²={rows[:,0].mean():.6f} (anisotropie {np.ptp(rows[:,0])/rows[:,0].mean():.1e})  c_B²={rows[:,1].mean():.6f} / {rows[:,2].mean():.6f} (anis. {np.ptp(rows[:,1:3])/rows[:,1:3].mean():.1e})  c_C²={rows[:,3].mean():.6f} (anis. {np.ptp(rows[:,3])/rows[:,3].mean():.1e})')
