# C-137c / PR-1 — SELECTION DES REGLES GENEALOGIQUES. Protocole FIGE par ChatGPT (fil principal, 12 nov. 2026, 16 h 36 UTC), execute par Claude.
# Famille exhaustive : cellule ordonnee (x0, x1, x2, x3) ; mot periodique de trois battements dans {1,2,3}^3 (27) ; au battement d, le fil (x0, x_d) se divise ;
#   filles de C-136c : (x0..x_{d-1}, z, x_{d+1}..) et (x1..x_d, z, x_{d+1}..) ; puis une permutation fixe des quatre positions pour chaque fille (24 x 24).
#   Total 15 552 regles. Temoin positif connu : mot (3,2,1), permutations identite.
# Phase 1 : toutes les regles jusqu'a la generation 6 ; rejet immediat, sans reparation, si : deux choix incompatibles autour d'un meme fil ; une face dans plus
#   de deux cellules ; cellule dupliquee ; complexe de cliques incoherent ; porteur disparu ; invariants d'une boule violes. Premiere generation d'echec publiee.
# Phase 2 : survivantes jusqu'a la generation 12 ; mesures aux generations 3, 6, 9, 12.  Phase 3 : temoins geometriques (Kuhn, Kuhn deforme, regulier).
# Phase 4 : construction ordonnee analogue en dimensions 2 et 4.
# PRECISIONS D'EXECUTION (Claude, declarees avant calcul) :
#  - naissances synchrones : toutes les cellules se divisent une fois par generation ; battement = mot[(g-1) mod 3] ;
#  - chaque porteur est NOMME par ses coordonnees barycentriques exactes par rapport aux quatre fondateurs (simple etiquette : aucune longueur n'entre dans la regle) ;
#  - deux regles sont dites equivalentes si leurs complexes coincident a une permutation des quatre fondateurs pres (forme canonique : minimum sur 24 permutations) ;
#  - invariants de boule controles : caracteristique d'Euler 1 ; bord = surface fermee de caracteristique 2 ; graphe dual connexe.
# PREDICTIONS ENREGISTREES AVANT CALCUL (Claude) :
#  P1. moins de 200 regles sur 15 552 survivent a la generation 6 ; elles forment au plus 5 classes de complexes, dont celle de la mitose reguliere (S1) ;
#  P2. toutes les cellules de toutes les survivantes ont H = +1 (theoreme de ChatGPT : un plus jeune sommet unique) ;
#  P3. phase 4 : la construction ordonnee fonctionne aussi en dimensions 2 et 4 ; elle ne selectionne donc pas la dimension 3 ;
#  P4. des regles a mot constant survivent (les permutations des filles peuvent coder le battement).
import itertools, sys, json, time
from fractions import Fraction as Fr
PERMS=list(itertools.permutations(range(4))); WORDS=list(itertools.product((1,2,3),repeat=3))
E=[tuple(Fr(int(i==j)) for j in range(4)) for i in range(4)]
def mid(a,b): return tuple((a[i]+b[i])/2 for i in range(4))
def step(cells,d,p1,p2):
    des=[frozenset((x[0],x[d])) for x in cells]; D=set(des)
    for x,e in zip(cells,des):
        for a,b in itertools.combinations(x,2):
            f=frozenset((a,b))
            if f in D and f!=e: return None
    new=[]
    for x in cells:
        z=mid(x[0],x[d]); c1=x[:d]+(z,)+x[d+1:]; c2=x[1:d+1]+(z,)+x[d+1:]
        new.append(tuple(c1[i] for i in p1)); new.append(tuple(c2[i] for i in p2))
    return new
def sane(cells):
    S=[frozenset(x) for x in cells]
    if len(set(S))!=len(S) or any(len(s)!=4 for s in S): return 'cellule dupliquée ou dégénérée'
    F={}
    for s in S:
        for f in itertools.combinations(sorted(s),3): F[f]=F.get(f,0)+1
    if max(F.values())>2: return 'face dans plus de deux cellules'
    return None
def run(word,p1,p2,gmax):
    cells=[tuple(E)]
    for g in range(1,gmax+1):
        cells=step(cells,word[(g-1)%3],p1,p2)
        if cells is None: return g,'choix incompatibles',None
        r=sane(cells)
        if r: return g,r,None
    return None,None,cells
if __name__=='__main__' and sys.argv[1]=='phase1':
    t=time.time(); fail={}; surv=[]
    for w in WORDS:
        for p1 in PERMS:
            for p2 in PERMS:
                g,why,cells=run(w,p1,p2,6)
                if g is None: surv.append((w,p1,p2))
                else: fail[(g,why)]=fail.get((g,why),0)+1
    print('Phase 1 :',len(surv),'survivantes sur',27*576,f'({time.time()-t:.0f} s)')
    for k in sorted(fail): print('   échec à la génération',k[0],':',k[1],':',fail[k])
    print('   témoin (3,2,1), identité, identité survivant :',((3,2,1),PERMS[0],PERMS[0]) in surv)
    bw={}
    for w,_,_ in surv: bw[w]=bw.get(w,0)+1
    print('   survivantes par mot :',{''.join(map(str,k)):v for k,v in sorted(bw.items())})
    json.dump([[list(w),list(p1),list(p2)] for w,p1,p2 in surv],open('c137c_survivantes6.json','w'))
