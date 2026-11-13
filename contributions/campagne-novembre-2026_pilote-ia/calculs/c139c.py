# C-139c — LE NON-CHEVAUCHEMENT ET DEUX MARQUES BINAIRES SUFFISENT-ILS A ARRETER LA MITOSE LIBRE AU TETRAEDRE ? (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Donnees de l'auteur : (15 h 43 UTC) "un simplexe ne peut pas chevaucher un simplexe quand il est cree" ; (17 h 42 UTC) les deux descendants sont lies et heritent
#   des liens du parent ("je pense que oui, a tester") ; la premiere fermeture bloque la mitose. Corpus : un porteur porte deux marques binaires (bit de lignee, signe de chiralite).
# AXIOME TESTE, affiche comme supplementaire (bras N2 du protocole C-138c de ChatGPT) :
#   (E) deux porteurs qui ont exactement les memes relations (meme voisinage ferme : "au meme endroit") doivent differer par leur signature ;
#   une naissance n'a lieu que si le nouveau-ne peut recevoir une signature libre a l'endroit ou il nait.
# (1) Mitose libre a heritage integral (loi F), k marques binaires, rythmes S et A (ancien d'abord, et au hasard) : taille a saturation.
#     PREDICTION : 2^k porteurs tous lies, quel que soit le rythme : k = 1 -> fil ; k = 2 -> tetraedre ; k = 3 -> 8 porteurs (dimension 7).
# (2) A saturation (k = 2), naissance sur un fil ab SANS couper le fil : cinq porteurs tous lies -> interdite par (E). AVEC coupure du fil : autorisee ?
#     PREDICTION : interdite sans coupure ; autorisee avec coupure, le nouveau-ne prenant la signature d'un de ses deux parents.
# (3) Tissu de la mitose reguliere (C-136c), generations 1 a 12 : tailles des groupes de porteurs "au meme endroit" (meme voisinage ferme).
#     PREDICTION : jamais plus de 4 ; aucun au-dela des premieres generations a l'interieur du tissu.
# (4) Existe-t-il une attribution des signatures (chaque nouveau-ne recoit celle d'un de ses deux parents) respectant (E) a chaque generation, jusqu'a g = 9 ?
#     PREDICTION : oui.
import itertools, random, sys
from fractions import Fraction as Fr
sys.setrecursionlimit(100000)
def freeF(k,tempo,seed=None):
    V=[0]; N={0:set()}; sig={0:0}; rng=random.Random(seed); queue=[0]; blocked=set()
    while True:
        cand=[v for v in V if v not in blocked]
        if not cand: break
        parents=list(cand) if tempo=='S' else ([queue.pop(0)] if seed is None else [rng.choice(cand)])
        if tempo=='A' and seed is None and parents[0] in blocked: continue
        progressed=False
        for p in parents:
            # le nouveau-ne aurait le voisinage ferme de p : signatures deja prises a cet endroit
            taken={sig[v] for v in V if (N[v]|{v})==(N[p]|{p})}
            free=[s for s in range(2**k) if s not in taken]
            if not free: blocked.add(p); continue
            c=len(V); V.append(c); N[c]=set(N[p])|{p}
            for q in N[c]: N[q].add(c)
            sig[c]=free[0]; progressed=True
            if tempo=='A' and seed is None: queue+=[p,c]
        if tempo=='A' and seed is None and not progressed and not queue: break
        if tempo=='A' and seed is None and not queue: queue=[v for v in V if v not in blocked]
    return len(V),all(len(N[v])==len(V)-1 for v in V),len(set(sig.values()))
print('(1) mitose libre, héritage intégral, exclusion (E) :')
for k in (1,2,3):
    r=[freeF(k,'S'),freeF(k,'A')]+[freeF(k,'A',seed=s) for s in range(1380,1388)]
    print(f'   k = {k} marque(s) : tailles à saturation {sorted(set(x[0] for x in r))} ; tous liés : {all(x[1] for x in r)} ; signatures distinctes {sorted(set(x[2] for x in r))}  (rythmes S, A ancien d\'abord, A au hasard × 8)')
# (2)
N={v:set(range(4))-{v} for v in range(4)}; sig={0:0,1:1,2:2,3:3}
z=4; Nz=set(range(4)); same=[v for v in range(4) if (N[v]|{v}|{z})==(Nz|{z})]
print('(2) tétraèdre saturé, naissance sur le fil 0-1 sans coupure : porteurs au même endroit que le nouveau-né :',same,'→ signatures prises',sorted(sig[v] for v in same),': naissance',('interdite' if len(same)>=4 else 'autorisée'))
N2={v:set(N[v]) for v in N}; N2[0].discard(1); N2[1].discard(0); N2[z]=set(range(4))
for v in range(4): N2[v].add(z)
same=[v for v in range(4) if (N2[v]|{v})==(N2[z]|{z})]
print('    avec coupure du fil 0-1 : au même endroit que le nouveau-né :',same,'→ signatures prises',sorted(sig[v] for v in same),'; libres :',sorted(set(range(4))-{sig[v] for v in same}),'= celles des deux parents ; 0 et 1 ont le même voisinage ouvert :',N2[0]==N2[1])
# (3) et (4) : tissu regulier
E4=[tuple(Fr(int(i==j)) for j in range(4)) for i in range(4)]
cells=[tuple(E4)]; parents_of={}; order=list(E4); gens=[]
for g in range(1,13):
    d=(3,2,1)[(g-1)%3]; new=[]
    for x in cells:
        zz=tuple((x[0][i]+x[d][i])/2 for i in range(4))
        if zz not in parents_of: parents_of[zz]=(x[0],x[d]); order.append(zz)
        new.append(x[:d]+(zz,)+x[d+1:]); new.append(x[1:d+1]+(zz,)+x[d+1:])
    cells=new; Nn={}
    for x in cells:
        for a,b in itertools.combinations(x,2): Nn.setdefault(a,set()).add(b); Nn.setdefault(b,set()).add(a)
    cl={}
    for v in Nn: cl.setdefault(frozenset(Nn[v]|{v}),[]).append(v)
    op={}
    for v in Nn: op.setdefault(frozenset(Nn[v]),[]).append(v)
    tw=[c for c in cl.values() if len(c)>1]; fw=[c for c in op.values() if len(c)>1]
    gens.append((g,len(order),tw,fw))
    print(f'(3) génération {g:2d} : {len(cells):4d} cellules ; groupes de porteurs au même endroit (voisinage fermé identique) : {len(tw)} (plus grand : {max((len(c) for c in tw),default=0)}) ; mêmes relations sans être liés : {len(fw)} (plus grand : {max((len(c) for c in fw),default=0)})',flush=True)
# (4) recherche d'une attribution : chaque nouveau-ne prend la signature d'un de ses deux parents ; (E) verifiee a chaque generation <= 9
cons=[]   # contraintes : (generation, groupe)
for g,nv,tw,fw in gens:
    if g<=9:
        for c in tw: cons.append(tuple(sorted(c,key=order.index)))
cons=sorted(set(cons),key=lambda c:max(order.index(v) for v in c)); born=[v for v in order[4:] if order.index(v)<gens[8][1]]
sigv={E4[i]:i for i in range(4)}
def ok(v):
    for c in cons:
        if v in c and all(u in sigv for u in c):
            s=[sigv[u] for u in c]
            if len(set(s))<len(s): return False
    return True
def dfs(i):
    if i==len(born): return True
    v=born[i]; a,b=parents_of[v]
    for s in dict.fromkeys((sigv[a],sigv[b])):
        sigv[v]=s
        if ok(v) and dfs(i+1): return True
        del sigv[v]
    return False
res=dfs(0); cnt={}
for v,s in sigv.items(): cnt[s]=cnt.get(s,0)+1
print(f'(4) attribution des signatures jusqu\'à la génération 9 ({len(born)} nouveau-nés, {len(cons)} contraintes d\'exclusion) : {"existe" if res else "impossible"} ; effectifs par signature : {dict(sorted(cnt.items()))}')
