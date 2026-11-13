# C-78 (preregistre) : apres fusion jumelle + R0, le noyau se concentre-t-il sur les sommets neutres (secteur F) quand g croit,
# et l'ecart spectral au reste croit-il comme g ? Mesures : poids de ker H sur F ; plus petite |valeur propre| non nulle.
exec(open('c76_naissances_signees.py').read().split('res={}')[0])
for k in (1,2,3):
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    cells=sorted(R0([tuple(sorted(ren[v] for v in (0,1,2,3))),tuple(sorted(ren[v] for v in (4,5,6,7)))],s),key=lambda c:(len(c),c))
    idx={c:i for i,c in enumerate(cells)}; n=len(cells); d=np.zeros((n,n))
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f and f in idx: d[idx[c],idx[f]]+=(-1)**j
    D=d+d.T; G=np.diag([(-1)**(len(c)-1) for c in cells]); S=np.diag([pol(c,s) for c in cells])
    F=[idx[(100+i,)] for i in range(k)]
    row=[]
    for g in (0.5,1.5,4.0,10.0,30.0):
        w,V=np.linalg.eigh(D+g*S@G); K=V[:,abs(w)<1e-9]
        poidsF=np.sum(K[F]**2)/K.shape[1]; gap=min(abs(w[abs(w)>1e-9]))
        row.append(f"g={g}: poids F {poidsF:.4f}, ecart {gap:.3f}")
    print(f"k={k} |", " ; ".join(row))
