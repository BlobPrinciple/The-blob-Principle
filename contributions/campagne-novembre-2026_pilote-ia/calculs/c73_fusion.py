# C-73 (preregistre) : annihilation = fusion de chaque contact (i, i+4) en UN porteur neutre n_i (polarite 0),
# fixe par le miroir. Aucun parametre nouveau. Test : modes nuls apres fusion = chi(Fix P) = k ? pour g = 0.5, 1.5, 4.
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
for k in (1,2,3):
    ren={}; s={}; p={}
    for v in range(8):
        i=v%4
        if i<k: ren[v]=100+i; s[100+i]=0; p[100+i]=100+i
        else: ren[v]=v; s[v]=1 if v<4 else -1
    for v in range(8):
        if v%4>=k: p[ren[v]]=ren[(v+4)%8]
    maxs=[tuple(sorted(ren[v] for v in t)) for t in [(0,1,2,3),(4,5,6,7)]]
    for g in (0.5,1.5,4.0):
        cells=complex_from_max(maxs); D,G,idx=ops(cells); S=polar(cells,s)
        H=D+g*S@G; ev=np.linalg.eigvalsh(H); z=int(np.sum(abs(ev)<1e-9))
        P=perm_op(cells,idx,p); L=round(np.trace(G@P)); anti=np.allclose((G@P)@H+H@(G@P),0)
        print(f"k={k} g={g}: apres fusion modes nuls={z}  L(P)={L}  C anticommute={anti}")
