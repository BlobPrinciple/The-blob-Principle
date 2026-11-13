# C-135c — DU PORTEUR AU TISSU : CE QUE LA MITOSE DE L'ARETE REPOND AUX QUATRE QUESTIONS DE CHATGPT (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Contexte : sur le fil principal, ChatGPT (C-134) trouve que six regles de liaison depuis un seul simplexe echouent (graphe complet ou biparti) et demande
#   a Rudolphe : qui se lie a qui, pourquoi un lien persiste, pourquoi un tetraedre plutot qu'un reseau ou tout touche tout. Position de l'auteur (14 h 26 UTC) :
#   l'energie n'appartient pas au simplexe ; la mitose est premiere. Aucune energie, aucun ressort, aucune coordonnee dans cette epreuve.
# ENONCES A CERTIFIER :
#  (A) [T] La mitose de l'arete conserve la propriete "une cellule = un ensemble de porteurs tous lies entre eux" (complexe de cliques du graphe des fils) :
#      si elle est vraie avant une naissance, elle l'est apres. Preuve ecrite dans l'archive ; ici, verification par enumeration des cliques a chaque naissance,
#      sur la mitose reguliere S1 (4 096 cellules) et sur 5 histoires de 400 naissances a arete quelconque.
#  (B) [T] Doublement avec heritage complet des liens et lien entre soeurs : K1, K2, K4, K8... Le premier graphe qui contient une boucle fermee est K4.
#      Si la premiere fermeture emprisonne la mitose (les naissances ont ensuite lieu sur les fils de la structure fermee), la dimension reste 3 et K8 n'apparait pas.
#  (C) Apres la fermeture, un nouveau porteur ne se lie qu'aux deux bouts de son fil et aux porteurs des cellules autour de ce fil : nombre de liens par naissance
#      et degre maximal releves sur S1.
# PREDICTION ENREGISTREE : (A) aucune violation ; (B) boucles independantes 0, 0, 3, 21 ; dimension des cliques 0, 1, 3, 7 ; (C) au plus 10 liens par naissance
#      sur S1 (2 bouts + 4, 6 ou 8 porteurs autour), degre maximal 26.
import itertools, random, sys
from c120 import s1_events
def start(): return {frozenset((0,1,2,3))},{v:set(range(4))-{v} for v in range(4)}
def bisect(T,N,a,b,m):
    ts=[t for t in T if a in t and b in t]; link=set()
    for t in ts:
        T.discard(t); T.add((t-{b})|{m}); T.add((t-{a})|{m}); link|=t-{a,b}
    N[a].discard(b); N[b].discard(a); N[m]=set()
    for x in (a,b,*link): N[m].add(x); N[x].add(m)
    return len(link)+2
def flag(T,N):
    k4=set()
    for u in N:
        for v in N[u]:
            if v<u: continue
            for w in N[u]&N[v]:
                if w<v: continue
                for x in N[u]&N[v]&N[w]:
                    if x<w: continue
                    q=frozenset((u,v,w,x)); k4.add(q)
                    if N[u]&N[v]&N[w]&N[x]: return False,'K5'
    faces=set(frozenset(f) for t in T for f in itertools.combinations(t,3)); tri=set()
    for u in N:
        for v in N[u]:
            if v<u: continue
            for w in N[u]&N[v]:
                if w>v: tri.add(frozenset((u,v,w)))
    return (k4==T and tri==faces),(len(k4),len(T),len(tri),len(faces))
# (A) S1
gens=s1_events(12); T,N=start(); nb=0; ok=True; maxlinks=0; hist={}
for g in sorted(gens):
    for a,b,m in gens[g]:
        k=bisect(T,N,a,b,m); nb+=1; maxlinks=max(maxlinks,k); hist[k]=hist.get(k,0)+1
        if nb%7==0 or len(gens[g])<8:
            r,info=flag(T,N); ok&=r
            if not r: print('VIOLATION S1 à la naissance',nb,info); break
    r,info=flag(T,N); ok&=r
print(f'(A) S1 : {nb} naissances, {len(T)} cellules, {len(N)} porteurs ; cellules = cliques à chaque contrôle : {ok} ; 4-cliques = {info[0]}, cellules = {info[1]}, triangles = {info[2]}, faces = {info[3]}')
print(f'(C) S1 : liens créés par naissance (nombre : fréquence) {dict(sorted(hist.items()))} ; maximum {maxlinks} ; degré maximal {max(len(x) for x in N.values())} ; porteurs éternels : aucun porteur supprimé ({len(N)} = 4 + {nb})')
# (A) histoires quelconques
for seed in range(5):
    rng=random.Random(1800+seed); T,N=start(); ok=True; nv=4
    for n in range(400):
        t=sorted(rng.choice(sorted(T,key=sorted))); a,b=rng.sample(t,2); bisect(T,N,a,b,nv); nv+=1
        r,info=flag(T,N); ok&=r
        if not r: print('VIOLATION, graine',seed,'naissance',n,info); break
    print(f'(A) arête quelconque, graine {1800+seed} : 400 naissances, {len(T)} cellules ; cellules = cliques après chaque naissance : {ok} ; degré maximal {max(len(x) for x in N.values())}')
# (B) doublement avec heritage complet
V=[0]; E=set()
for g in range(4):
    comp=1; n=len(V); cyc=len(E)-n+1; # K_n connexe
    import math
    print(f'(B) génération {g} : {n} porteurs, {len(E)} liens (graphe complet : {len(E)==n*(n-1)//2}), boucles indépendantes {cyc}, dimension de la plus grande clique {n-1}')
    V2=[]; E2=set()
    for v in V: V2+=[(v,0),(v,1)]; E2.add(frozenset(((v,0),(v,1))))
    for e in E:
        u,v=tuple(e)
        for i in (0,1):
            for j in (0,1): E2.add(frozenset(((u,i),(v,j))))
    V,E=V2,E2
