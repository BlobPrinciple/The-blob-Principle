# C-118 — L'EXTINCTION DE C-97 SURVIT-ELLE A LA MITOSE DE L'ARETE ? (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Acquis [T, C-84] : (1 + 2 d/g^2)^-1 <= G <= (1 + 2 d/(g^2+k))^-1, ou G est le poids du mode protege sur le contact et d le degre du contact.
# Acquis [T, C-97] : sous naissances 1->4 uniformes, d ~ n^(2/3), donc G -> 0 (extinction).
# Complexe jumeau, k = 1 contact, g = 1,5. Bras E : mitose de l'arete par paliers (regle S1 de C-116), jumelee en miroir.
# Bras V : naissances 1->4 jumelees uniformes (enumerateur de C-80), 6 graines, memes nombres de cellules.
# PREDICTION ENREGISTREE : bras E : d borne, G borne inferieurement (pas d'extinction) ; bras V : G decroit. Bornes de Loewner respectees partout.
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
g=1.5; k=1
def twin_edge(gens):
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
    kuhn=[(0.,0.,0.),(1.,0.,0.),(1.,1.,0.),(1.,1.,1.)]; P={ren[v]:kuhn[v] for v in range(4)}
    tp={tuple(sorted(ren[v] for v in (0,1,2,3)))}; tm={tuple(sorted(ren[v] for v in (4,5,6,7)))}; nv=[200]; stamp={}; c=[0]
    def key(e):
        if e not in stamp: c[0]+=1; stamp[e]=c[0]
        p,q=P[e[0]],P[e[1]]; return (-sum((p[i]-q[i])**2 for i in range(3)),stamp[e])
    for e in [(0,3),(0,2),(1,3),(0,1),(1,2),(2,3)]: key(tuple(sorted((ren[e[0]],ren[e[1]]))))
    longest=lambda t:min(itertools.combinations(t,2),key=key)
    def bisect(e):
        a,b=e; m=nv[0]; mm=nv[0]+1; nv[0]+=2; P[m]=tuple((P[a][i]+P[b][i])/2 for i in range(3)); s[m]=1; s[mm]=-1; mir[m]=mm; mir[mm]=m
        for t in [t for t in tp if a in t and b in t]:
            o=tuple(v for v in t if v not in e); tp.discard(t); tp.add(tuple(sorted((a,m)+o))); tp.add(tuple(sorted((b,m)+o)))
            tmir=tuple(sorted(mir[x] for x in t)); om=tuple(mir[v] for v in o); tm.discard(tmir)
            tm.add(tuple(sorted((mir[a],mm)+om))); tm.add(tuple(sorted((mir[b],mm)+om)))
    def divide(t):
        while t in tp:
            cur=t
            while True:
                e=longest(cur); best=key(e); nxt=None
                for t2 in [x for x in tp if e[0] in x and e[1] in x]:
                    s2=key(longest(t2))
                    if s2<best: best=s2; nxt=t2
                if nxt is None: bisect(e); break
                cur=nxt
    out=[]
    for gen in range(gens+1):
        out.append((gen,sorted(tp),sorted(tm),dict(s)))
        for t in sorted(tp):
            if t in tp: divide(t)
    return out
def stats(tp,tm,s):
    cells=R0(tp+tm,s); Pk,idx=kern(cells,s,g); i=idx[(100,)]
    d=sum(1 for c in cells if len(c)==2 and 100 in c and s[[x for x in c if x!=100][0]]>0)
    return len(tp),round(float(np.trace(Pk)),6),d,Pk[i,i],1/(1+2*d/g**2),1/(1+2*d/(g**2+k))
print('Bras E (mitose de l\'arête, paliers) : génération, cellules par lignée, dim ker, degré du contact, G, borne inf, borne sup')
import sys
for gen,tp,tm,s in twin_edge(int(sys.argv[1])):
    n,tr,d,G,lo,hi=stats(tp,tm,s); print(f'  gen {gen}: N3={n} ker={tr} d={d} G={G:.5f} bornes [{lo:.5f}, {hi:.5f}] respectées={lo-1e-12<=G<=hi+1e-12}',flush=True)
print('Bras V (naissances 1->4 uniformes, 6 graines)')
for nb in (0,2,5,21,85):
    r=[stats(*grow(k,nb,seed)[:3]) for seed in range(6)]
    print(f'  naissances {nb}: N3={r[0][0]} ker={set(x[1] for x in r)} d moyen={np.mean([x[2] for x in r]):.1f} G moyen={np.mean([x[3] for x in r]):.5f} bornes respectées={all(x[4]-1e-12<=x[3]<=x[5]+1e-12 for x in r)}',flush=True)
