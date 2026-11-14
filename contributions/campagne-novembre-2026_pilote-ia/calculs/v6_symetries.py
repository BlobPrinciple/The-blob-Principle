# V6 (aveugle) : symetries de la rencontre a k contacts et representation portee par les modes proteges.
import itertools
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
s8={**{i:1 for i in range(4)},**{i:-1 for i in range(4,8)}}
for k in (2,3,4):
    maxs=[(0,1,2,3),(4,5,6,7)]+[(i,i+4) for i in range(k)]
    cells=complex_from_max(maxs); D,G,idx=ops(cells); S=polar(cells,s8)
    for g in (1.5,):
        H=D+g*S@G; w,V=np.linalg.eigh(H); P0=V[:,abs(w)<1e-9]@V[:,abs(w)<1e-9].T
        cset=set(cells); grp=[]
        # automorphismes conservant la polarite : permutation pi de {0..3} preservant l'ensemble des contacts, appliquee aux deux tetras
        for pi in itertools.permutations(range(4)):
            if set(pi[i] for i in range(k))!=set(range(k)): continue
            p={i:pi[i] for i in range(4)}; p.update({i+4:pi[i]+4 for i in range(4)})
            U=perm_op(cells,idx,p)
            if not np.allclose(U@H@U.T,H): continue
            grp.append((pi,np.trace(P0@U)))
        chars={}
        for pi,ch in grp:
            # type de cycle sur les contacts
            cyc=tuple(sorted(len(c) for c in __import__('sympy').combinatorics.Permutation(list(pi[:k])).cyclic_form)) if False else None
            fixed=sum(1 for i in range(k) if pi[i]==i)
            chars.setdefault(fixed,set()).add(round(ch,6))
        print(f"k={k}: |groupe conservant polarite et H| = {len(grp)} ; caractere sur le noyau selon nb de contacts fixes : {chars}")
