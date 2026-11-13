# C-137c / PR-1, phases 2 et 3 (protocole fige par ChatGPT ; precisions d'execution et predictions dans c137c.py).
import itertools, json, math, sys, time
from fractions import Fraction as Fr
from multiprocessing import Pool
from c137c import PERMS, E, step, sane, mid
EMB={'Kuhn':[(0,0,0),(1,0,0),(1,1,0),(1,1,1)],'deforme':[(0,0,0),(1,0,0),(1,1,0),(1,1,1.2)],'regulier':[(x/math.sqrt(8),y/math.sqrt(8),z/math.sqrt(8)) for x,y,z in ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))]}
def graph(cells):
    N={}
    for x in cells:
        for a,b in itertools.combinations(x,2): N.setdefault(a,set()).add(b); N.setdefault(b,set()).add(a)
    return N
def flag(S,N):
    k4=set()
    for u in N:
        for v in N[u]:
            if not u<v: continue
            cuv=N[u]&N[v]
            for w in cuv:
                if not v<w: continue
                for x in cuv&N[w]:
                    if w<x:
                        k4.add(frozenset((u,v,w,x)))
                        if cuv&N[w]&N[x]: return False
    return k4==S
def ball(S):
    F={}
    for s in S:
        for f in itertools.combinations(sorted(s),3): F.setdefault(f,[]).append(s)
    V=set(v for s in S for v in s); Ed=set(e for s in S for e in itertools.combinations(sorted(s),2))
    chi=len(V)-len(Ed)+len(F)-len(S); B=[f for f,l in F.items() if len(l)==1]; be={}
    for f in B:
        for e in itertools.combinations(f,2): be[e]=be.get(e,0)+1
    bv=set(v for f in B for v in f); chib=len(bv)-len(be)+len(B)
    # dual connexe
    adj={}
    for f,l in F.items():
        if len(l)==2: adj.setdefault(l[0],[]).append(l[1]); adj.setdefault(l[1],[]).append(l[0])
    s0=next(iter(S)); seen={s0}; st=[s0]
    while st:
        x=st.pop()
        for y in adj.get(x,()):
            if y not in seen: seen.add(y); st.append(y)
    return chi==1 and chib==2 and all(v==2 for v in be.values()) and len(seen)==len(S),(len(V),len(Ed),len(F),len(S))
def canon(cells):
    best=None
    for p in PERMS:
        h1=0; h2=0
        for x in cells:
            fs=frozenset(tuple(v[i] for i in p) for v in x); h=hash(fs); h1=(h1+h)&0xFFFFFFFFFFFFFFFF; h2=(h2+h*h)&0xFFFFFFFFFFFFFFFF
        k=(h1,h2)
        if best is None or k<best: best=k
    return best
def bfs(N,s):
    d={s:0}; q=[s]
    for u in q:
        for v in N[u]:
            if v not in d: d[v]=d[u]+1; q.append(v)
    return d
def work(rule):
    w,p1,p2=tuple(rule[0]),tuple(rule[1]),tuple(rule[2]); cells=[tuple(E)]; born={v:0 for v in E}; out=dict(rule=rule,echec=None,pal={}); links={}
    pos={k:{v:P[i] for i,v in enumerate(E)} for k,P in EMB.items()}; longest={k:[0,0] for k in EMB}; canons=[]
    for g in range(1,13):
        d=w[(g-1)%3]; N=graph(cells)
        for x in cells:
            a,b=x[0],x[d]
            for k in EMB:
                L=sorted((math.dist(pos[k][u],pos[k][v]) for u,v in itertools.combinations(x,2)),reverse=True); longest[k][1]+=1; longest[k][0]+=math.dist(pos[k][a],pos[k][b])>=L[0]-1e-12
        for e in set(frozenset((x[0],x[d])) for x in cells):
            a,b=tuple(e); n=2+len(N[a]&N[b]); links[n]=links.get(n,0)+1; z=mid(a,b)
            if z not in born:
                born[z]=g
                for k in EMB: pos[k][z]=tuple((pos[k][a][i]+pos[k][b][i])/2 for i in range(3))
        cells=step(cells,d,p1,p2)
        if cells is None: out['echec']=(g,'choix incompatibles'); return out
        r=sane(cells)
        if r: out['echec']=(g,r); return out
        if g%3==0:
            S=set(frozenset(x) for x in cells); N=graph(cells); okb,cnt=ball(S); deg=sorted(len(v) for v in N.values())
            if set(N)!=set(born): out['echec']=(g,'porteur disparu'); return out
            if not okb: out['echec']=(g,'invariants de boule'); return out
            fl=flag(S,N)
            if not fl: out['echec']=(g,'complexe de cliques incohérent'); return out
            cls={v:(born[v]-(g-3) if born[v]>g-3 else 0) for v in N}; same=sum(1 for a in N for b in N[a] if a<b and cls[a]==cls[b]); rainbow=all(sorted(cls[v] for v in x)==[0,1,2,3] for x in cells)
            Hs={}
            for x in cells:
                t=lambda i,j:max(born[x[i]],born[x[j]]); pr=(t(0,1)-t(2,3))*(t(0,2)-t(1,3))*(t(0,3)-t(1,2)); h=(pr>0)-(pr<0); Hs[h]=Hs.get(h,0)+1
            fd=sorted(bfs(N,E[i])[E[j]] for i,j in itertools.combinations(range(4),2))
            q={}
            for k in EMB:
                qs=[]
                for x in cells:
                    A=[pos[k][v] for v in x]; u=[A[1][i]-A[0][i] for i in range(3)]; v=[A[2][i]-A[0][i] for i in range(3)]; ww=[A[3][i]-A[0][i] for i in range(3)]
                    vol=abs(u[0]*(v[1]*ww[2]-v[2]*ww[1])-u[1]*(v[0]*ww[2]-v[2]*ww[0])+u[2]*(v[0]*ww[1]-v[1]*ww[0]))/6; dm=max(math.dist(a,b) for a,b in itertools.combinations(A,2)); qs.append(6*math.sqrt(2)*vol/dm**3)
                q[k]=(min(qs),len(set(round(z,6) for z in qs)))
            cz=canon(cells); canons.append(cz)
            out['pal'][g]=dict(comptes=cnt,degmax=deg[-1],degdist=[(d_,deg.count(d_)) for d_ in sorted(set(deg))],meme_classe=same,quatre_classes=rainbow,H=Hs,fondateurs=fd,qualite=q,canon=cz)
    out['liens']=sorted(links.items()); out['plus_long']={k:v[0]/v[1] for k,v in longest.items()}; out['signature']=tuple(canons)
    return out
if __name__=='__main__':
    rules=json.load(open('c137c_survivantes6.json')); t=time.time()
    with Pool(2) as p: res=p.map(work,rules,chunksize=4)
    json.dump(res,open('c137c_phase2.json','w'),default=str)
    ok=[r for r in res if r['echec'] is None]; ko=[r for r in res if r['echec'] is not None]
    print(f'Phase 2 : {len(ok)} règles conformes jusqu\'à la génération 12 sur {len(res)} ({time.time()-t:.0f} s)')
    fl={}
    for r in ko: fl[tuple(r['echec'])]=fl.get(tuple(r['echec']),0)+1
    for k in sorted(fl): print('   échec à la génération',k[0],':',k[1],':',fl[k])
    classes={}
    for r in ok: classes.setdefault(r['signature'],[]).append(r)
    print(f'   classes de complexes (à permutation des fondateurs près, aux quatre paliers) : {len(classes)}')
    ref=[r for r in ok if r['rule']==[[3,2,1],[0,1,2,3],[0,1,2,3]]]; refsig=ref[0]['signature'] if ref else None
    for i,(sig,rs) in enumerate(sorted(classes.items(),key=lambda kv:-len(kv[1]))):
        r=rs[0]; p12=r['pal'][12]; words=sorted(set(''.join(map(str,x['rule'][0])) for x in rs))
        print(f'   classe {i+1} : {len(rs)} règles ; contient le témoin (3,2,1) : {sig==refsig} ; mots : {words}')
        for g in (3,6,9,12):
            p=r['pal'][g]; print(f'      g={g:2d} : (porteurs, fils, faces, cellules) = {p["comptes"]} ; degré max {p["degmax"]} ; fils entre même classe d\'âge {p["meme_classe"]} ; quatre classes par cellule {p["quatre_classes"]} ; H {p["H"]} ; distances entre fondateurs {p["fondateurs"]}')
        print(f'      liens par naissance {r["liens"]} ; degrés à g=12 {p12["degdist"]}')
        for k in EMB:
            fr=sorted(set(round(x['plus_long'][k],4) for x in rs)); qm=sorted(set(round(x['pal'][12]['qualite'][k][0],4) for x in rs)); nc=sorted(set(x['pal'][12]['qualite'][k][1] for x in rs))
            print(f'      plongement {k:8s} : part des divisions sur le fil le plus long {fr[0]:.3f} à {fr[-1]:.3f} ; qualité minimale à g=12 {qm[0]:.4f} à {qm[-1]:.4f} ; formes distinctes {nc}')
