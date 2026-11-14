# C-74 (preregistre, fige avant calcul). Regle de rupture standard : rompre une arete supprime toutes les cellules qui la contiennent.
# Annihilation = fusion des contacts (i,i+4) -> porteur neutre n_i (C-73), puis branches testees (liste fermee) :
#  A : aucune rupture (rappel C-73)
#  B : rupture des aretes entre points de rencontre (n_i - n_j)  -> detachement mutuel des sites
#  C : B + rupture des aretes entre site et porteurs charges (detachement complet : le site devient isole)
#  D : contacts supprimes sans fusion (annihilation pure)
# Succes ℛ-1 : nombre de modes nuls = k (nombre de sites) pour k = 1,2,3 et g = 0.5/1.5/4. Comparaisons : 4 branches.
import itertools
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
def complexe(maxs,ruptures):
    cells=complex_from_max(maxs)
    return [c for c in cells if not any(set(e)<=set(c) for e in ruptures)]
def modes(cells,s,g):
    idx={c:i for i,c in enumerate(cells)}; n=len(cells); d=np.zeros((n,n))
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f and f in idx: d[idx[c],idx[f]]+=(-1)**j
    D=d+d.T; G=np.diag([(-1)**(len(c)-1) for c in cells]); S=polar(cells,s)
    return int(np.sum(abs(np.linalg.eigvalsh(D+g*S@G))<1e-9))
for k in (1,2,3):
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    fused=[tuple(sorted(ren[v] for v in t)) for t in [(0,1,2,3),(4,5,6,7)]]
    sites=[100+i for i in range(k)]; charges=[v for v in s if s[v]!=0]
    rB=[tuple(sorted(p)) for p in itertools.combinations(sites,2)]
    rC=rB+[tuple(sorted((a,b))) for a in sites for b in charges]
    branches={"A fusion seule":(fused,[]),"B sites detaches entre eux":(fused,rB),"C sites isoles":(fused,rC)}
    s8={**{i:1 for i in range(4)},**{i:-1 for i in range(4,8)}}
    for nom,(m,r) in branches.items():
        cells=complexe(m,r)
        # un site isole doit rester present comme 0-cellule
        for x in sites:
            if (x,) not in cells: cells.append((x,))
        print(f"k={k} {nom:28s}", [modes(sorted(cells,key=lambda c:(len(c),c)),s,g) for g in (0.5,1.5,4.0)])
    print(f"k={k} {'D contacts supprimes':28s}", [modes(complex_from_max([(0,1,2,3),(4,5,6,7)]),s8,g) for g in (0.5,1.5,4.0)])
