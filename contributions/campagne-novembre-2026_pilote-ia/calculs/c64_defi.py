import numpy as np, itertools
rng=np.random.default_rng(3)

def complex_from_max(maxs):
    S=set()
    for m in maxs:
        m=tuple(sorted(m))
        for k in range(1,len(m)+1):
            for c in itertools.combinations(m,k): S.add(c)
    return sorted(S,key=lambda c:(len(c),c))

def ops(cells,w=None):
    idx={c:i for i,c in enumerate(cells)}; n=len(cells); d=np.zeros((n,n))
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f: d[idx[c],idx[f]]+=(-1)**j*(1 if w is None else w[c])
    D=d+d.T; G=np.diag([(-1)**(len(c)-1) for c in cells]); return D,G,idx

def polar(cells,s):  # polarite d'une cellule = signe de la somme des polarites de ses sommets
    return np.diag([np.sign(sum(s[v] for v in c)) for c in cells])

def perm_op(cells,idx,p):
    n=len(cells); P=np.zeros((n,n))
    for c in cells:
        img=[p[v] for v in c]; srt=tuple(sorted(img))
        sign=np.linalg.det(np.eye(len(c))[[sorted(img).index(x) for x in img]])
        P[idx[srt],idx[c]]=sign
    return P

def analyse(nom,maxs,s,p,g=1.5,w=None):
    cells=complex_from_max(maxs); D,G,idx=ops(cells,w); S=polar(cells,s)
    H=D+g*S@G; ev=np.linalg.eigvalsh(H); z=int(np.sum(abs(ev)<1e-9))
    if p is None:
        print(f"{nom:42s} cellules={len(cells):3d} modes nuls={z}   (pas d'automorphisme miroir)"); return
    P=perm_op(cells,idx,p); C=G@P
    anti=np.allclose(C@H+H@C,0); L=round(np.trace(C))
    print(f"{nom:42s} cellules={len(cells):3d} C anticommute={anti}  |Lefschetz L(P)|={abs(L)}  modes nuls={z}")

K4=[(0,1,2,3)]; s4={0:1,1:1,2:-1,3:-1}
pair={0:2,1:3,2:0,3:1}           # (02)(13), permutation paire
cyc={0:2,2:1,1:3,3:0}            # 4-cycle, permutation impaire
bord=[(0,1,2),(0,1,3),(0,2,3),(1,2,3)]
print("--- 1. Le resultat de C-64 et sa vraie nature ---")
for g in (0.3,1.5,7.0): analyse(f"Tetraedre plein ++--, g={g}",K4,s4,pair,g)
analyse("Tetraedre plein, miroir par 4-cycle",K4,s4,cyc)
print("--- 2. Meme poche, topologie differente : surface du tetraedre (S2) ---")
analyse("Surface S2, miroir pair (02)(13)",bord,s4,pair)
analyse("Surface S2, miroir impair (4-cycle)",bord,s4,cyc)
print("--- 3. Les deux structures de C-64 ---")
analyse("Chaine 0-1-2-3, polarites + + - - (miroir)",[(0,1),(1,2),(2,3)],{0:1,1:1,2:-1,3:-1},{0:3,1:2,2:1,3:0})
analyse("Etoile centree sur +",[(0,1),(0,2),(0,3)],{0:1,1:1,2:-1,3:-1},None)
print("--- 4. Robustesse : liaisons de poids aleatoires compatibles avec le miroir ---")
cells=complex_from_max(K4); w={}
for c in cells:
    key=tuple(sorted(pair[v] for v in c))
    if key in w: w[c]=w[key]
    else: w[c]=rng.uniform(0.3,3)
analyse("Tetraedre plein, poids aleatoires symetriques",K4,s4,pair,w=w)
w2={c:rng.uniform(0.3,3) for c in cells}
analyse("Tetraedre plein, poids aleatoires non symetriques",K4,s4,None,w=w2)
print("--- 5. Bord du 4-simplexe (S3), 5 porteurs ++--0 ---")
S3=[tuple(x for x in range(5) if x!=i) for i in range(5)]
s5={0:1,1:1,2:-1,3:-1,4:0}
analyse("S3, miroir pair (02)(13)",S3,s5,{0:2,1:3,2:0,3:1,4:4})
analyse("S3, miroir impair (0213)",S3,s5,{0:2,2:1,1:3,3:0,4:4})
