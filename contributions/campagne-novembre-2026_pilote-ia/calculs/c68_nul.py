# C-68 preenregistre (fige AVANT calcul) :
# rencontre ++++ / ---- par k=3 aretes miroirs (0-4, 1-5, 2-6), g = 3/2 (valeur archivee).
# Sous-espace K = noyau de H. Operateurs testes, liste fermee : Sigma, Gamma, D^2, N (dimension de cellule).
# Pour chacun : O_K = P_K O P_K restreint a K (3x3), valeurs propres lambda, puis
#   r = e1^2/e2 (Koide exact : 6) en prenant lambda comme sqrt(m) (et |lambda| si signes mixtes).
# Succes si |r-6|/6 < 1e-3 pour un operateur, AVEC note de 4 comparaisons. Echec sinon.
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
s8={**{i:1 for i in range(4)},**{i:-1 for i in range(4,8)}}; m={i:(i+4)%8 for i in range(8)}
for k in (3,):
    maxs=[(0,1,2,3),(4,5,6,7)]+[(i,i+4) for i in range(k)]
    analyse(f"Rencontre par {k} aretes",maxs,s8,m)
    cells=complex_from_max(maxs); D,G,idx=ops(cells); S=polar(cells,s8); g=1.5
    H=D+g*S@G; w,V=np.linalg.eigh(H); K=V[:,abs(w)<1e-9]; print("dim noyau :",K.shape[1])
    N=np.diag([len(c)-1 for c in cells]).astype(float)
    for nom,O in [("Sigma",S),("Gamma",G),("D^2",D@D),("N",N)]:
        lam=np.linalg.eigvalsh(K.T@O@K)
        for lab,l in [("lambda",lam),("|lambda|",abs(lam))]:
            e1=l.sum(); e2=l[0]*l[1]+l[0]*l[2]+l[1]*l[2]
            r=e1**2/e2 if abs(e2)>1e-12 else float('inf')
            print(f"  {nom:5s} {lab:8s} valeurs={np.round(l,4)}  e1^2/e2={r:.5f}")
