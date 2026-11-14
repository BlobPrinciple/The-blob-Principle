# C-136c — UNE LOI DES LIENS SANS LONGUEUR, SANS ENERGIE, SANS COORDONNEE : LA SIGNATURE CHRONOLOGIQUE (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Question posee par ChatGPT (C-136, fil principal, 16 h 09 UTC) a la demande de Rudolphe ("que faut-il pour correspondre, et qu'avons-nous qui y ressemble ?") :
#   peut-on construire une regle de correspondance a partir de la seule filiation, sans coordonnees, sans energie, sans bain, sans choisir un nombre de voisins ?
# Regle testee (bissection genealogique, Maubach 1995, connue en analyse numerique) : chaque cellule garde l'ORDRE D'ARRIVEE de ses quatre porteurs (x0, x1, x2, x3)
#   et un battement d (3, 2, 1, puis 3...). Le fil qui se divise est x0-x_d. Le nouveau porteur z y nait. Les deux cellules filles sont
#   (x0, .., x_{d-1}, z, x_{d+1}, ..) et (x1, .., x_d, z, x_{d+1}, ..), battement suivant. Aucune longueur n'entre dans la regle.
# (a) Comparaison, generation par generation jusqu'a 4 096 cellules, avec la mitose reguliere S1 de C-116 (qui, elle, choisit le fil le plus LONG a l'aide de
#     coordonnees). Les coordonnees ne servent ici qu'a comparer. PREDICTION : memes cellules a chaque generation ; conformite sans propagation.
# (b) Classes d'age aux paliers (toutes les trois generations) : aines, puis porteurs nes au 1er, 2e, 3e battement du dernier palier.
#     PREDICTION : aucun fil ne relie deux porteurs de la meme classe ; chaque cellule contient exactement un porteur de chaque classe.
# (c) Controles : chaque face appartient a au plus deux cellules ; cellules = groupes de porteurs tous lies (C-135c) ; degre maximal.
import itertools
from fractions import Fraction as Fr
P={0:(Fr(0),Fr(0),Fr(0)),1:(Fr(1),Fr(0),Fr(0)),2:(Fr(1),Fr(1),Fr(0)),3:(Fr(1),Fr(1),Fr(1))}; born={0:0,1:0,2:0,3:0}
mid={}
def midpoint(a,b,g):
    k=frozenset((a,b))
    if k not in mid:
        m=len(P); mid[k]=m; P[m]=tuple((P[a][i]+P[b][i])/2 for i in range(3)); born[m]=g
    return mid[k]
d2=lambda a,b:sum((P[a][i]-P[b][i])**2 for i in range(3))
gen_cells=[((0,1,2,3),3)]          # regle genealogique : (ordre d'arrivee, battement)
geo=[frozenset((0,1,2,3))]         # regle metrique : fil le plus long
for g in range(1,13):
    new=[]; cut=set()
    for x,d in gen_cells:
        z=midpoint(x[0],x[d],g); cut.add(frozenset((x[0],x[d]))); nd=d-1 if d>1 else 3
        new.append((x[:d]+(z,)+x[d+1:],nd)); new.append((x[1:d+1]+(z,)+x[d+1:],nd))
    gen_cells=new; S=set(frozenset(x) for x,_ in new)
    conf=all(not(e<=t) for t in S for e in cut if len(e&t)==2) if g<=9 else None      # aucun fil divise ne subsiste dans une cellule
    newg=[]; uniq=True
    for t in geo:
        es=sorted(((d2(a,b),a,b) for a,b in itertools.combinations(sorted(t),2)),reverse=True); uniq&=es[0][0]>es[1][0]; _,a,b=es[0]; z=midpoint(a,b,g)
        newg.append((t-{b})|{z}); newg.append((t-{a})|{z})
    geo=newg; G=set(geo)
    F={}
    for t in S:
        for f in itertools.combinations(sorted(t),3): F[f]=F.get(f,0)+1
    N={}
    for t in S:
        for a,b in itertools.combinations(t,2): N.setdefault(a,set()).add(b); N.setdefault(b,set()).add(a)
    line=f'génération {g:2d} : {len(S):4d} cellules, {len(N):3d} porteurs ; règle généalogique = fil le plus long : {S==G} (fil le plus long unique : {uniq}) ; conforme : {conf} ; faces dans plus de deux cellules : {sum(v>2 for v in F.values())} ; degré max {max(len(v) for v in N.values())}'
    if g%3==0:
        cls={v:(born[v]-(g-3) if born[v]>g-3 else 0) for v in N}
        same=sum(1 for a in N for b in N[a] if a<b and cls[a]==cls[b]); rainbow=all(sorted(cls[v] for v in t)==[0,1,2,3] for t in S)
        cnt=[sum(1 for v in N if cls[v]==k) for k in range(4)]
        line+=f' | PALIER : fils entre porteurs de même classe d\'âge = {same} ; chaque cellule a les quatre classes : {rainbow} ; effectifs (aînés, 1er, 2e, 3e battement) = {cnt}'
    print(line,flush=True)
# cellules = cliques, au dernier palier
k4=set()
for u in N:
    for v in N[u]:
        if v<u: continue
        for w in N[u]&N[v]:
            if w<v: continue
            for x in N[u]&N[v]&N[w]:
                if x>w: k4.add(frozenset((u,v,w,x)))
print('contrôle final : groupes de quatre porteurs tous liés =',len(k4),'; cellules =',len(S),'; identiques :',k4==S)
