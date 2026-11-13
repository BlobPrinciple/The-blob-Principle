# C-140c / PR-1 — CYCLE STRUCTUREL : PIEGE, USURE, FRACTURE, LIBERATION, RENOUVELLEMENT. Protocole FIGE par ChatGPT (12 nov. 2026, 18 h 01 UTC), execute par Claude.
# Automate combinatoire, sans energie ni coefficient continu. Graphe des liens actifs ; registre de filiation permanent ; cellule = groupe de quatre porteurs tous lies (K4).
# Axiome T : tout porteur d'une cellule active est piege ; sa tentative de mitose est refusee et comptee.
# Loi W : chaque tentative refusee ajoute une unite d'usure a chaque lien actif du porteur ; un lien rompt quand son usure atteint son soutien = max(1, nombre de
#   triangles intacts qui le contiennent), soutien pris avant les ruptures de l'evenement ; ruptures simultanees, pas de cascade dans un meme evenement.
# Reprise : F (le nouveau-ne se lie au parent et a tous ses voisins) ; R (naissance sur le fil incident de plus petite paire d'identifiants : le fil est retire, le
#   nouveau-ne se lie aux deux bouts et a leurs voisins communs ; naissance pendante s'il n'y a aucun fil).
# Signatures : E0 (aucune) ; E2-L (deux bits herites strictement du parent ; naissance rejetee si (E) est violee) ; E2-F (plus petite signature admissible parmi quatre).
# Germe : K4. Ordonnancement principal : un porteur par evenement, file circulaire par anciennete, nouveau-nes en fin de file. Temoin synchrone.
# Temoins negatifs : W0 (pas d'usure), T0 (pas de piege), G0 (depart d'un seul porteur), Wmax (soutien = 1 pour tous les liens).
# PRECISIONS D'EXECUTION DECLAREES AVANT CALCUL (Claude) :
#  - duree : 256 tentatives par porteur initial (1 024 evenements depuis K4 ; 256 depuis un seul porteur) ; T0 avec F arrete a 64 evenements (graphe complet) ;
#  - la condition de rupture est evaluee sur tous les liens actifs a la fin de CHAQUE evenement (une baisse de soutien due a une rupture anterieure compte a l'evenement suivant) ;
#  - renouvellement complet = (1) une fracture detruit au moins une cellule, (2) une naissance a lieu ensuite, (3) une nouvelle cellule apparait qui contient un porteur
#    ne apres cette fracture ; le compteur repart alors ;
#  - controle d'etiquetage (bras R) : le depart du fil "de plus petite paire" utilise des etiquettes tirees au hasard a la naissance (3 graines) au lieu de l'ordre de naissance ;
#  - temoin synchrone : etat piege pris au debut du tour ; naissances dans l'ordre d'anciennete ; usures et ruptures appliquees en fin de tour ; arret a 1 024 tentatives ou 3 000 porteurs.
#  - J'ai suivi a la main les cinq premiers evenements du bras principal F avant d'ecrire le code (fracture au 2e evenement, naissance au 3e).
# PREDICTIONS ENREGISTREES AVANT CALCUL (Claude) :
#  P1. W0 : gel eternel (4 porteurs, aucune naissance).
#  P2. Bras principal W / F / E0 : au moins deux renouvellements complets (PASS combinatoire conditionnel) ; population croissante ; jamais cinq porteurs tous lies.
#  P3. Bras W / R / E0 : [T attendu] une naissance sur un fil ne cree jamais de cellule dans un graphe qui n'en a pas ; apres la premiere fracture, plus aucune cellule,
#      plus aucun piege : une naissance par evenement, tissu a deux dimensions. FAIL cycle (aucun renouvellement).
#  P4. E2-L avec F : toute naissance rejetee par (E) (le nouveau-ne est le jumeau de son parent, meme signature) : mort sans renaissance. E2-F avec F : cycle maintenu.
#  P5. Wmax : cycles plus courts, maintenus avec F. G0 / F : K1, K2, K3, K4 puis cycle ; G0 / R : chaine sans cellule.
#  P6. Interface 3H(z) : NON_COMPARABLE (ni metrique, ni horloge, ni regle de decalage spectral derivees).
import sys, random, itertools, collections, json, math
def simulate(rebirth='F',sig='E0',wear='W',trap=True,seed_graph='K4',maxev=None,sync=False,label_seed=None,cap=3000):
    n0=4 if seed_graph=='K4' else 1; N={v:set(range(n0))-{v} for v in range(n0)}; w={}
    for a,b in itertools.combinations(range(n0),2): w[(a,b)]=0
    orig=set(w); sg={v:v for v in range(n0)}; rng=random.Random(label_seed) if label_seed is not None else None; lab={v:(rng.random() if rng else v) for v in range(n0)}
    cells=set(); incell=collections.Counter(); born_ev={v:0 for v in range(n0)}; cell_birth={}; life=[]
    def add_cell(c,ev):
        if c not in cells:
            cells.add(c); cell_birth[c]=ev
            for v in c: incell[v]+=1
    def del_cell(c,ev):
        cells.discard(c); life.append(ev-cell_birth.pop(c))
        for v in c: incell[v]-=1
    def cells_at(z,ev):
        Nz=N[z]
        for x in Nz:
            for y in Nz&N[x]:
                if y<=x: continue
                for t in Nz&N[x]&N[y]:
                    if t>y: add_cell(frozenset((z,x,y,t)),ev)
    if n0==4: add_cell(frozenset(range(4)),0)
    key=lambda a,b:(a,b) if a<b else (b,a)
    def Eok():
        g={}
        for v in N: g.setdefault(frozenset(N[v]|{v}),[]).append(sg[v])
        return all(len(set(s))==len(s) for s in g.values())
    maxev=maxev or 256*n0; queue=collections.deque(range(n0)); st=dict(blocked=0,births=0,eblocked=0,fract=0,wearcum=0); marks={}; renew=0; phase=0; frac_id=None
    series={}; ev=0; omega5=False; rounds=0; hist=[]
    def do_birth(p,ev):
        nonlocal omega5
        z=len(N)
        if sig!='E0': snapN={v:set(s) for v,s in N.items()}; snapw=dict(w)
        removed=None
        if rebirth=='F' or not N[p]:
            nb=set(N[p])|{p}
        else:
            q=min(N[p],key=lambda q:tuple(sorted((lab[p],lab[q])))); removed=key(p,q); nb=(N[p]&N[q])|{p,q}
            N[p].discard(q); N[q].discard(p)
        N[z]=set(nb)
        for x in nb: N[x].add(z)
        lab[z]=rng.random() if rng else z
        ok=True
        if sig=='E2-L': sg[z]=sg[p]; ok=Eok()
        elif sig=='E2-F':
            ok=False
            for s_ in range(4):
                sg[z]=s_
                if Eok(): ok=True; break
        else: sg[z]=0
        if not ok:
            N.clear(); N.update(snapN); w.clear(); w.update(snapw); sg.pop(z,None); lab.pop(z,None); return None
        if removed is not None:
            w.pop(removed,None); orig.discard(removed)
            for c in [c for c in cells if removed[0] in c and removed[1] in c]: del_cell(c,ev)
        for x in nb: w[key(z,x)]=0
        born_ev[z]=ev; cells_at(z,ev)
        if not omega5:
            for c in list(cells):
                if z in c:
                    common=set.intersection(*(N[v] for v in c))
                    if common: omega5=True; break
        return z
    def ruptures(ev):
        nonlocal phase,frac_id,renew
        brk=[e for e,x in w.items() if (x>=1 if wear=='Wmax' else x>=max(1,len(N[e[0]]&N[e[1]])))] if wear!='W0' else []
        lost=0
        for a,b in brk:
            N[a].discard(b); N[b].discard(a); del w[(a,b)]; orig.discard((a,b)); st['fract']+=1
            for c in [c for c in cells if a in c and b in c]: del_cell(c,ev); lost+=1
        if brk and 'première fracture' not in marks: marks['première fracture']=ev
        if lost and 'première cellule perdue' not in marks: marks['première cellule perdue']=ev
        if lost and phase==0: phase=1; frac_id=len(N)
        if not orig and n0==4 and 'derniers liens d\'origine disparus' not in marks: marks['derniers liens d\'origine disparus']=ev
    def after_birth(z,ev):
        nonlocal phase,renew
        st['births']+=1
        if 'première fracture' in marks and 'première naissance après fracture' not in marks: marks['première naissance après fracture']=ev
        if any(z in c for c in cells) and z>=n0 and 'première cellule contenant un descendant' not in marks: marks['première cellule contenant un descendant']=ev
        if phase==1: phase=2
        if phase==2 and any(max(c)>=frac_id for c in cells if z in c): renew+=1; phase=0
    checkpoints={16,64,256,1024}
    def snapshot(ev):
        deg=[len(x) for x in N.values()]; fd=[]
        if n0==4:
            for s in range(4):
                d={s:0}; q=[s]
                for u in q:
                    for v in N[u]:
                        if v not in d: d[v]=d[u]+1; q.append(v)
                fd+=[d.get(t,-1) for t in range(s+1,4)]
        tri=sum(len(N[a]&N[b]) for a,b in w)//3
        series[ev]=dict(N=len(N),liens=len(w),triangles=tri,cellules=len(cells),pieges=sum(1 for v in N if incell[v]>0),degmax=max(deg),fondateurs=sorted(fd),**st)
    if not sync:
        while ev<maxev and len(N)<cap:
            ev+=1; p=queue.popleft()
            if trap and incell[p]>0:
                st['blocked']+=1
                if wear!='W0':
                    for q in N[p]: w[key(p,q)]+=1; st['wearcum']+=1
                queue.append(p)
            else:
                z=do_birth(p,ev); queue.append(p)
                if z is None: st['eblocked']+=1
                else: queue.append(z); after_birth(z,ev)
            ruptures(ev)
            if ev in checkpoints or ev==maxev: snapshot(ev)
            if ev%64==0: hist.append((ev,len(N),len(cells)))
    else:
        while ev<maxev and len(N)<cap:
            rounds+=1; present=sorted(N); T0={v for v in present if incell[v]>0} if trap else set(); inc=collections.Counter()
            for p in present:
                ev+=1
                if p in T0:
                    st['blocked']+=1
                    for q in N[p]: inc[key(p,q)]+=1
                else:
                    z=do_birth(p,ev)
                    if z is None: st['eblocked']+=1
                    else: after_birth(z,ev)
            if wear!='W0':
                for e,x in inc.items():
                    if e in w: w[e]+=x; st['wearcum']+=x
            ruptures(ev); hist.append((rounds,len(N),len(cells)))
        snapshot(ev)
    alive=len(cells); life_s=sorted(life)
    return dict(marks=marks,renouvellements=renew,series=series,omega5=omega5,cellules_creees=len(life)+alive,cellules_vivantes=alive,duree_mediane=(life_s[len(life_s)//2] if life_s else None),duree_max=(life_s[-1] if life_s else None),hist=hist,rounds=rounds,evenements=ev)
def show(name,r):
    s=r['series']; last=s[max(s)]
    print(f'{name:34s}: renouvellements {r["renouvellements"]:4d} ; repères {r["marks"]} ; cinq porteurs tous liés : {r["omega5"]}')
    print(f'{"":34s}  fin (événement {max(s)}) : {last["N"]} porteurs, {last["liens"]} liens, {last["triangles"]} triangles, {last["cellules"]} cellules, {last["pieges"]} piégés, degré max {last["degmax"]}, naissances {last["births"]}, refus par piège {last["blocked"]}, refus par (E) {last["eblocked"]}, ruptures {last["fract"]}, distances entre fondateurs {last["fondateurs"]} ; cellules créées {r["cellules_creees"]}, durée médiane {r["duree_mediane"]}, max {r["duree_max"]}',flush=True)
if __name__=='__main__':
    out={}
    def go(name,**kw): r=simulate(**kw); out[name]=r; show(name,r); return r
    print('— Bras principaux (file circulaire) —')
    for rb in 'FR':
        for sg_ in ('E0','E2-L','E2-F'): go(f'W / {rb} / {sg_}',rebirth=rb,sig=sg_)
    print('— Témoin synchrone —')
    for rb in 'FR': go(f'W / {rb} / E0 / synchrone',rebirth=rb,sync=True)
    print('— Témoins négatifs —')
    for rb in 'FR':
        go(f'W0 / {rb} (pas d\'usure)',rebirth=rb,wear='W0'); go(f'T0 / {rb} (pas de piège)',rebirth=rb,trap=False,maxev=64 if rb=='F' else None)
        go(f'G0 / {rb} (un seul porteur)',rebirth=rb,seed_graph='K1'); go(f'Wmax / {rb} (soutien 1)',rebirth=rb,wear='Wmax')
    print('— Contrôle d\'étiquetage, bras R —')
    for s_ in (1,2,3): go(f'W / R / E0 / étiquettes {s_}',rebirth='R',label_seed=s_)
    print('— Croissance du bras principal W / F / E0 : (événement, porteurs, cellules) —'); print('  ',out['W / F / E0']['hist'])
    print('— Témoin synchrone F : (tour, porteurs, cellules) —'); print('  ',out['W / F / E0 / synchrone']['hist'][:40])
    json.dump({k:{kk:vv for kk,vv in v.items()} for k,v in out.items()},open('c140c.json','w'),default=str)
