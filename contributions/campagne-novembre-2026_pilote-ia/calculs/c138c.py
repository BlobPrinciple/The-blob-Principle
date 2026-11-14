# C-138c / PR-1 — LA PREMIERE FERMETURE DEPUIS LE SIMPLEXE PRIMORDIAL. Protocole FIGE par ChatGPT (12 nov. 2026, empreinte 497b0019...), execute par Claude.
# Etat : graphe simple G = (V, E) + registre de filiation. Fermeture : premier etat complet ou mu(G) = |E| - |V| + c(G) > 0.
# Naissance : le porteur qui mitose garde son identite et engendre un nouveau porteur.
# Rythmes : S (tous les porteurs se divisent a chaque generation) ; A (un porteur par evenement : le plus ancien d'abord ; controle : parent tire au hasard, graines 1380-1387).
# Lois de liaison : F heritage integral (descendants lies ; le nouveau porteur recoit toutes les relations du parent ; toutes les combinaisons si les deux bouts se divisent) ;
#   L soeurs seulement ; M heritage partiel (chaque ancienne relation va a UN seul descendant a chaque bout) ; R remplacement (l'ancienne arete uv devient u'v, uv' ou u'v').
# Emprisonnement : N0 aucun (bras principal). N1 (memoire seule) est identique a N0 pour le graphe. N2 : tout interdit doit etre affiche comme axiome supplementaire.
# Tailles : N = 2, 4, ..., 256. Releves a la premiere fermeture et a chaque taille.
# PRECISIONS D'EXECUTION DECLAREES AVANT CALCUL (Claude) :
#  - A, "le plus ancien d'abord" : file circulaire dans l'ordre des naissances (chaque porteur se divise a son tour ; le nouveau-ne passe en fin de file) ;
#  - M : les anciennes relations du parent, rangees par identifiant de naissance de l'autre bout, restent au parent (rang pair) ou passent au nouveau-ne (rang impair) ;
#    temoin miroir : parite inverse. En rythme S, la regle s'applique a chaque bout sur les listes d'avant la generation ;
#  - A s'arrete a la taille 256 ; F est arrete a 64 porteurs pour le comptage des cliques (graphe complet : valeurs exactes par formule).
# PREDICTIONS ENREGISTREES AVANT CALCUL (Claude) :
#  P1 [T attendu]. L, M et R ne ferment jamais : chaque naissance ajoute un porteur et un lien, donc |E| - |V| est constant et mu = 0 pour toujours.
#     Une premiere fermeture exige qu'une relation soit tenue par les DEUX descendants a la fois.
#  P2. F : graphes complets ; fermeture a 4 porteurs (S) ou 3 (A) ; K5 des 5 porteurs (A) ou 8 (S) ; distances bloquees a 1 : surconnexion, FAIL comme explication suffisante.
#  P3. R : chemin (distance maximale N - 1 en S) ; extension sans fermeture. L : arbre, distances en log N (S).
#  P4. Verdict du protocole : OPEN — aucun bras ne donne a la fois fermeture, localite et extension.
import itertools, random, sys, math
def mu(V,E):
    par={v:v for v in V}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for a,b in E: par[f(a)]=f(b)
    c=len(set(f(v) for v in V)); return len(E)-len(V)+c,c
def adj(V,E):
    N={v:set() for v in V}
    for a,b in E: N[a].add(b); N[b].add(a)
    return N
def cliques(N,kmax=5):
    cnt={3:0,4:0,5:0}; om=1 if not any(N.values()) else 2
    for u in N:
        for v in N[u]:
            if v<=u: continue
            c2=N[u]&N[v]
            for w in c2:
                if w<=v: continue
                cnt[3]+=1; om=max(om,3); c3=c2&N[w]
                for x in c3:
                    if x<=w: continue
                    cnt[4]+=1; om=max(om,4)
                    for y in c3&N[x]:
                        if y>x: cnt[5]+=1; om=max(om,5)
    return cnt,om
def diam(N):
    best=0; tot=0; n=0
    for s in list(N)[:64]:
        d={s:0}; q=[s]
        for u in q:
            for v in N[u]:
                if v not in d: d[v]=d[u]+1; q.append(v)
        best=max(best,max(d.values())); tot+=sum(d.values()); n+=len(d)-1
    return best,tot/max(1,n)
def divide(V,E,parents,law,mirror=False):
    # parents : liste des porteurs qui se divisent en meme temps
    N=adj(V,E); child={}; nid=len(V)
    for p in parents: child[p]=nid; nid+=1
    newE=set()
    def side(u,v):   # descendant de u qui recoit l'ancienne relation uv (loi M)
        if u not in child: return u
        r=sorted(N[u]).index(v); return u if (r%2==0)!=mirror else child[u]
    for a,b in E:
        if law=='F':
            for x in ([a,child[a]] if a in child else [a]):
                for y in ([b,child[b]] if b in child else [b]): newE.add((min(x,y),max(x,y)))
        elif law=='L': newE.add((a,b))
        elif law=='M': x,y=side(a,b),side(b,a); newE.add((min(x,y),max(x,y)))
        elif law=='R': x,y=child.get(a,a),child.get(b,b); newE.add((min(x,y),max(x,y)))
    for p,c in child.items(): newE.add((p,c))
    return V+list(child.values()),newE
def run(tempo,law,seed=None,mirror=False,nmax=256):
    V=[0]; E=set(); rng=random.Random(seed) if seed is not None else None; queue=[0]; first=None; rows={}; sizes={2,4,8,16,32,64,128,256}
    while len(V)<nmax and not (law=='F' and len(V)>=64):
        if tempo=='S': parents=list(V)
        elif rng is None: p=queue.pop(0); parents=[p]
        else: parents=[rng.choice(V)]
        V,E=divide(V,E,parents,law,mirror)
        if tempo=='A' and rng is None: queue+= [parents[0],V[-1]]
        m,c=mu(V,E)
        if first is None and m>0:
            N=adj(V,E); cnt,om=cliques(N); first=dict(N=len(V),E=len(E),mu=m,omega=om,K3=cnt[3],K4=cnt[4],K5=cnt[5])
        if len(V) in sizes:
            N=adj(V,E); cnt,om=cliques(N) if len(V)<=64 or law!='F' else ({3:None,4:None,5:None},len(V)); d,dm=diam(N); deg=[len(x) for x in N.values()]
            rows[len(V)]=dict(E=len(E),mu=m,c=c,degmax=max(deg),omega=om,K3=cnt[3],K4=cnt[4],K5=cnt[5],diam=d,dmoy=round(dm,2))
    return first,rows
if __name__=='__main__':
    for law in 'FLMR':
        for tempo in 'SA':
            first,rows=run(tempo,law); last=max(rows)
            print(f'{law}/{tempo} : première fermeture = {first} ; '+' | '.join(f'N={n}: liens {r["E"]}, μ {r["mu"]}, degré max {r["degmax"]}, plus grand groupe tous liés {r["omega"]}, K3/K4/K5 {r["K3"]}/{r["K4"]}/{r["K5"]}, distance max {r["diam"]} (moy. {r["dmoy"]})' for n,r in rows.items() if n in (4,8,64,256)),flush=True)
        if law=='M':
            for tempo in 'SA':
                first,rows=run(tempo,law,mirror=True); r=rows[max(rows)]; print(f'M miroir/{tempo} : première fermeture = {first} ; N={max(rows)}: liens {r["E"]}, μ {r["mu"]}, degré max {r["degmax"]}, distance max {r["diam"]} (moy. {r["dmoy"]})')
        res=[run('A',law,seed=s) for s in range(1380,1388)]
        print(f'{law}/A au hasard (8 graines) : premières fermetures N = {[f["N"] if f else None for f,_ in res]} ; à la plus grande taille : μ = {sorted(set(r[max(r)]["mu"] for _,r in res))}, degré max {min(r[max(r)]["degmax"] for _,r in res)} à {max(r[max(r)]["degmax"] for _,r in res)}, distance max {min(r[max(r)]["diam"] for _,r in res)} à {max(r[max(r)]["diam"] for _,r in res)}',flush=True)
