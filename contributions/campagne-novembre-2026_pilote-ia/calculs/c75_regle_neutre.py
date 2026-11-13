# C-75 (preregistre avant calcul) : regle de rupture fondee sur la polarite, sans choix d'aretes.
# R0a : apres fusion (C-73), toute cellule de dimension >= 1 de polarite nulle (Sigma = 0) n'est portee par aucune lignee -> rompue.
# R0b : idem, mais la rupture ne vise que les aretes de polarite nulle (et les cellules qui les contiennent).
# Mesures : modes nuls ; nombre de composantes connexes ; sites detaches. Succes : k modes pour k = 1..4, g = 0.5/1.5/4, sans choix.
import itertools
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
def build(k):
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    maxs=[tuple(sorted(ren[v] for v in t)) for t in [(0,1,2,3),(4,5,6,7)]]
    return complex_from_max(maxs),s
def pol(c,s): return np.sign(sum(s[v] for v in c))
def modes(cells,s,g):
    cells=sorted(cells,key=lambda c:(len(c),c)); idx={c:i for i,c in enumerate(cells)}; n=len(cells); d=np.zeros((n,n))
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f and f in idx: d[idx[c],idx[f]]+=(-1)**j
    D=d+d.T; G=np.diag([(-1)**(len(c)-1) for c in cells]); S=np.diag([pol(c,s) for c in cells])
    return int(np.sum(abs(np.linalg.eigvalsh(D+g*S@G))<1e-9))
def comps(cells):
    import networkx as nx
    G=nx.Graph(); [G.add_node(c[0]) for c in cells if len(c)==1]; [G.add_edge(*c) for c in cells if len(c)==2]
    return nx.number_connected_components(G)
for k in (1,2,3,4):
    cells,s=build(k)
    ra=[c for c in cells if len(c)==1 or pol(c,s)!=0]
    ra=[c for c in ra if all((f in ra) for j in range(len(c)) for f in [c[:j]+c[j+1:]] if f)]
    bad=[c for c in cells if len(c)==2 and pol(c,s)==0]
    rb=[c for c in cells if not any(set(e)<=set(c) for e in bad)]
    print(f"k={k} | R0a modes {[modes(ra,s,g) for g in (0.5,1.5,4.0)]} comp {comps(ra)} | R0b modes {[modes(rb,s,g) for g in (0.5,1.5,4.0)]} comp {comps(rb)} | aretes neutres rompues {len(bad)}")
