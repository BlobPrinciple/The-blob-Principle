# C-120 / PR-1 — BOUCLE D'ETIREMENT-TENSION-MITOSE. Protocole FIGE par ChatGPT le 12 nov. 2026 (texte integral recu par l'API), execute par Claude.
# Energie : E = 1/2 Somme_e (|x_u - x_v| - r_e)^2, un ressort par arete distincte, K = 1. Lois : U (repos universel l0), B (repos a la naissance).
# Frontieres : F (libre), I (homothetique, a* = Somme r L / Somme L^2), X (bord fixe). Germes : Kuhn, Kuhn deforme (v3 = (1,1,6/5)), regulier d'arete 1.
# ECARTS DECLARES (budget de calcul et faisabilite) :
#  (1) Minimisation F et X : L-BFGS sans contrainte, puis controle des volumes orientes ; une solution a cellule inversee est rejetee et comptee.
#      Aucune force de contrainte numerique n'est ajoutee. Auto-intersections : test "aucun sommet strictement dans une cellule etrangere".
#  (2) DE_relax est calcule pour TOUTES les candidates tant que le maillage a au plus 64 aretes, et toujours pour l'evenement choisi ; au-dela,
#      seulement pour la candidate choisie.
#  (3) Les 16 initialisations (graines 1500-1515) sont faites pour les etats de germe et pour chaque generation du bras S1 force ; pas pour chaque candidate.
#  (4) Controle du classement (g = 12, 13, 14) : etat de base = equilibre homothetique de la trame de reference ; la relaxation apres naissance est LOCALE
#      (sommets du patch et nouveau sommet libres, le reste fixe).
import itertools, json, sys, math, numpy as np, scipy.optimize as so
def vol6(X,t): a,b,c,d=(X[v] for v in t); return float(np.dot(b-a,np.cross(c-a,d-a)))
class Mesh:
    def __init__(s,pts,l0,law,mode):
        s.X={i:np.array(p,float) for i,p in enumerate(pts)}; t=(0,1,2,3)
        if vol6(s.X,t)<0: t=(1,0,2,3)
        s.T={t}; s.l0=l0; s.law=law; s.mode=mode; s.rest={e:l0 for e in itertools.combinations(range(4),2)}; s.nv=4
        s.fixed=set(range(4)) if mode=='X' else set(); s.rejected=0
    def copy(s):
        m=Mesh.__new__(Mesh); m.X={k:v.copy() for k,v in s.X.items()}; m.T=set(s.T); m.l0=s.l0; m.law=s.law; m.mode=s.mode; m.rest=dict(s.rest); m.nv=s.nv; m.fixed=set(s.fixed); m.rejected=s.rejected; return m
    def inc(s):
        E={}
        for t in s.T:
            for e in itertools.combinations(sorted(t),2): E.setdefault(e,[]).append(t)
        return E
    def length(s,e): return float(np.linalg.norm(s.X[e[0]]-s.X[e[1]]))
    def energy(s): return 0.5*sum((s.length(e)-r)**2 for e,r in s.rest.items())
    def boundary_vertices(s):
        F={}
        for t in s.T:
            for f in itertools.combinations(sorted(t),3): F[f]=F.get(f,0)+1
        return set(v for f,c in F.items() if c==1 for v in f)
    def bisect(s,e,m=None,E=None):
        a,b=e; E=E or s.inc(); ts=E[e]; m=s.nv if m is None else m; s.nv=max(s.nv,m+1); s.X[m]=(s.X[a]+s.X[b])/2
        onb=(a in s.fixed and b in s.fixed and e in s._bedges()) if s.mode=='X' else False
        link=set()
        for t in ts:
            s.T.discard(t); s.T.add(tuple(m if v==b else v for v in t)); s.T.add(tuple(m if v==a else v for v in t)); link|=set(v for v in t if v!=a and v!=b)
        del s.rest[e]
        for ne in [tuple(sorted((a,m))),tuple(sorted((b,m)))]+[tuple(sorted((x,m))) for x in link]:
            s.rest[ne]=s.l0 if s.law=='U' else s.length(ne)
        if onb: s.fixed.add(m)
        return m
    def _bedges(s):
        F={}
        for t in s.T:
            for f in itertools.combinations(sorted(t),3): F[f]=F.get(f,0)+1
        return set(e for f,c in F.items() if c==1 for e in itertools.combinations(f,2))
    def dE_insert(s,e,E):
        a,b=e; m=(s.X[a]+s.X[b])/2; link=set(v for t in E[e] for v in t if v!=a and v!=b); L=s.length(e)
        if s.law=='B': return -0.5*(L-s.rest[e])**2
        return 0.5*(2*(L/2-s.l0)**2+sum((float(np.linalg.norm(s.X[x]-m))-s.l0)**2 for x in link))-0.5*(L-s.rest[e])**2
    def relax(s,jitter=0.0,seed=0,free=None):
        ids=sorted(s.X); pos={v:i for i,v in enumerate(ids)}; X0=np.array([s.X[v] for v in ids]); ed=list(s.rest); I=np.array([pos[e[0]] for e in ed]); J=np.array([pos[e[1]] for e in ed]); R=np.array([s.rest[e] for e in ed])
        if s.mode=='I':
            L=np.linalg.norm(X0[I]-X0[J],axis=1); a=float((R*L).sum()/(L**2).sum()); c=X0.mean(0); Xn=c+a*(X0-c)
            for v in ids: s.X[v]=Xn[pos[v]]
            return dict(E=s.energy(),gmax=0.0,ok=True,a=a)
        if free is None: free=[v for v in ids if v not in s.fixed]
        fi=np.array([pos[v] for v in free],int)
        if len(fi)==0: return dict(E=s.energy(),gmax=0.0,ok=True,a=1.0)
        if jitter>0:
            rng=np.random.default_rng(seed); X0=X0.copy(); X0[fi]+=jitter*np.mean(np.linalg.norm(X0[I]-X0[J],axis=1))*rng.standard_normal((len(fi),3))
        def fun(z):
            X=X0.copy(); X[fi]=z.reshape(-1,3); D=X[I]-X[J]; L=np.linalg.norm(D,axis=1); G=np.zeros_like(X); w=((L-R)/np.maximum(L,1e-300))[:,None]*D
            np.add.at(G,I,w); np.add.at(G,J,-w); return 0.5*((L-R)**2).sum(),G[fi].ravel()
        r=so.minimize(fun,X0[fi].ravel(),jac=True,method='L-BFGS-B',options=dict(gtol=1e-10,ftol=1e-15,maxiter=50000,maxcor=40,maxfun=200000))
        Xn=X0.copy(); Xn[fi]=r.x.reshape(-1,3); old={v:s.X[v] for v in ids}
        for v in ids: s.X[v]=Xn[pos[v]]
        vols=[vol6(s.X,t) for t in s.T]; valid=min(vols)>1e-12*max(1e-300,np.mean(np.abs(vols))); gmax=float(np.abs(r.jac).max())
        return dict(E=float(r.fun),gmax=gmax,ok=bool(valid and gmax<=1e-8*max(1.0,float(r.fun))),valid=bool(valid),conv=bool(gmax<=1e-8*max(1.0,float(r.fun))),old=old)
    def selfint(s):
        ids=sorted(s.X); P=np.array([s.X[v] for v in ids]); n=0
        for t in s.T:
            A=np.array([s.X[v] for v in t]); M=np.vstack([A.T,np.ones(4)])
            try: lam=np.linalg.solve(M,np.vstack([P.T,np.ones(len(P))]))
            except np.linalg.LinAlgError: continue
            ins=(lam>1e-7).all(0)
            for i in np.nonzero(ins)[0]:
                if ids[i] not in t: n+=1
        return n
    def metrics(s,E=None):
        E=E or s.inc(); L={e:s.length(e) for e in s.rest}; deg={}
        for a,b in s.rest: deg[a]=deg.get(a,0)+1; deg[b]=deg.get(b,0)+1
        vols=[vol6(s.X,t)/6 for t in s.T]; q=[]
        for t in s.T:
            dm=max(L[e] for e in itertools.combinations(sorted(t),2)); q.append(vol6(s.X,t)/6/dm**3)
        P=np.array(list(s.X.values())); F={}
        for t in s.T:
            for f in itertools.combinations(sorted(t),3): F[f]=F.get(f,0)+1
        fd=[float(np.linalg.norm(s.X[a]-s.X[b])) for a,b in itertools.combinations(range(4),2)]
        from scipy.spatial.distance import pdist
        return dict(N0=len(s.X),N1=len(s.rest),N2=len(F),N3=len(s.T),euler=len(s.X)-len(s.rest)+len(F)-len(s.T),conforme=max(F.values())<=2,volmin=float(min(vols)),inversions=int(sum(v<=0 for v in vols)),
            degmax=max(deg.values()),volume=float(sum(vols)),diam=float(pdist(P).max()),fondateurs=[round(x,6) for x in fd],Lmin=min(L.values()),Lmax=max(L.values()),Lmoy=float(np.mean(list(L.values()))),
            rmin=min(s.rest.values()),rmax=max(s.rest.values()),E=s.energy(),qmin=float(min(q)),autointersections=s.selfint() if len(s.T)<=600 else None)
SEEDS={'Kuhn':[(0,0,0),(1,0,0),(1,1,0),(1,1,1)],'deforme':[(0,0,0),(1,0,0),(1,1,0),(1,1,1.2)],'regulier':[(1/math.sqrt(8)*x,1/math.sqrt(8)*y,1/math.sqrt(8)*z) for x,y,z in ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))]}
def relax16(m):
    out=[]; best=None
    for i,sd in enumerate(range(1500,1516)):
        c=m.copy(); r=c.relax(jitter=0.0 if i==0 else 0.02,seed=sd); out.append((r['E'],r['ok']))
        if r['ok'] and (best is None or r['E']<best[0]-1e-13): best=(r['E'],c)
    return out,best
def autonome(seed,law,mode,l0,log=None):
    m=Mesh(SEEDS[seed],l0,law,mode); res=dict(seed=seed,law=law,mode=mode,l0=l0,events=[])
    if mode=='I': m.relax(); res['E0_16']=[m.energy()]
    else:
        vals,best=relax16(m); res['E0_16']=[round(v,12) for v,_ in vals]; res['E0_admissibles']=sum(ok for _,ok in vals)
        if best is None: res['arret']='INCONCLUSIF au germe'; return res
        m=best[1]
    res['germe']=m.metrics(); stop=None
    while len(m.T)<512:
        E=m.inc(); Eb=m.energy(); eps=1e-10*max(1.0,Eb); cand=[]
        for e in E:
            d=m.dE_insert(e,E); Lp={x:m.length(x) for t in E[e] for x in itertools.combinations(sorted(t),2)}
            longest_tets=all(m.length(e)>=max(m.length(x) for x in itertools.combinations(sorted(t),2))-1e-9 for t in E[e])
            cand.append(dict(e=e,dEi=d,longue_tetra=longest_tets,longue_patch=m.length(e)>=max(Lp.values())-1e-9))
        if len(E)<=64:
            for c in cand:
                k=m.copy(); k.bisect(c['e']); r=k.relax(); c['dEr']=(r['E']-Eb) if r['ok'] else None
        adm=[c for c in cand if c['dEi']<-eps]
        ev=dict(N3=len(m.T),E_avant=Eb,n_cand=len(cand),n_adm=len(adm),dEi_min=min(c['dEi'] for c in cand),dEi_longues=[round(c['dEi'],9) for c in cand if c['longue_tetra']][:6],
                barrieres=sum(1 for c in cand if c.get('dEr') is not None and c['dEr']<-eps and c['dEi']>=-eps),dEr_min=min([c['dEr'] for c in cand if c.get('dEr') is not None],default=None))
        if not adm: ev['choix']=None; res['events'].append(ev); stop='aucune naissance admissible'; break
        best=min(adm,key=lambda c:c['dEi']); ties=[c['e'] for c in adm if abs(c['dEi']-best['dEi'])<=1e-12*max(1,abs(best['dEi']))]
        m.bisect(best['e'],E=E); Ei=m.energy(); r=m.relax()
        ev.update(choix=best['e'],ex_aequo=len(ties),dEi=best['dEi'],longue_tetra=best['longue_tetra'],longue_patch=best['longue_patch'],E_insertion=Ei,E_relax=r['E'],ok=r['ok'])
        res['events'].append(ev)
        if not r['ok']: stop='relaxation non admissible ou non convergee'; break
    res['arret']=stop or 'seuil de 512 cellules atteint'; res['final']=m.metrics(); res['n_naissances']=sum(1 for e in res['events'] if e.get('choix') is not None)
    ch=[e for e in res['events'] if e.get('choix') is not None]; res['fraction_plus_longue_tetra']=float(np.mean([e['longue_tetra'] for e in ch])) if ch else None
    return res
def s1_sequence(gmax=9):
    src=open('c116.py').read().split("if __name__")[0]
    src=src.replace("        a,b=e; m=nv; nv+=1; nb+=1; ts=list(E[e]);","        a,b=e; m=nv; nv+=1; nb+=1; ts=list(E[e]); SEQ.append((a,b,m,len(L)));")
    ns={'SEQ':[]}; exec(src,ns); ns['run'](('S1',2**gmax,1500)) if False else None
    return ns
if __name__=='__main__':
    part=sys.argv[1]
    if part=='unit':
        m=Mesh(SEEDS['regulier'],1.0,'U','F'); vals,best=relax16(m); m=best[1]; E=m.inc()
        print('E0 (16 initialisations) : min',min(v for v,_ in vals),'max',max(v for v,_ in vals))
        print('DE_insert pour les 6 arêtes :',[round(m.dE_insert(e,E),12) for e in E],' attendu 2-√3 =',2-math.sqrt(3))
    if part=='auto':
        out=[]
        for seed in ('Kuhn','deforme','regulier'):
            for law in 'UB':
                for mode in 'FIX':
                    for l0 in (1.0,0.5,0.75,1.25):
                        r=autonome(seed,law,mode,l0); out.append(r); g=r.get('germe',{}); f=r.get('final',{})
                        e0=r['events'][0] if r['events'] else {}
                        print(f"{seed:8s} {law}/{mode} l0={l0:<4}: E0={g.get('E',float('nan')):.6f} naissances={r.get('n_naissances')} arrêt={r['arret']} | 1er évén.: dEi_min={e0.get('dEi_min',float('nan')):+.6f} admissibles={e0.get('n_adm')} barrières={e0.get('barrieres')} dEr_min={e0.get('dEr_min')} | final N3={f.get('N3')} vol={f.get('volume',float('nan')):.4f} diam={f.get('diam',float('nan')):.4f} qmin={f.get('qmin',float('nan')):.4f} degmax={f.get('degmax')} frac. plus longue={r.get('fraction_plus_longue_tetra')} E={f.get('E',float('nan')):.5f}",flush=True)
        json.dump(out,open('c120_auto.json','w'),default=str)
def s1_events(gmax=9):
    src=open('c116.py').read().split("if __name__")[0]
    src=src.replace("        a,b=e; m=nv; nv+=1; nb+=1; ts=list(E[e]);","        a,b=e; m=nv; nv+=1; nb+=1; ts=list(E[e]); SEQ.append((a,b,m,len(L)));")
    src=src.replace("    return finish(L,F,E,nv,seed,extra)\ndef run_S2","    return None\ndef run_S2")
    ns={'SEQ':[]}; exec(src,ns); ns['run'](('S1',2**gmax,1500)); gens={}
    for a,b,m,n3 in ns['SEQ']:
        g=int(math.floor(math.log2(n3)+1e-9))+1; gens.setdefault(g,[]).append((a,b,m))
    return gens
def s1_force(law,mode,l0=1.0,gmax=9):
    gens=s1_events(gmax); m=Mesh(SEEDS['Kuhn'],l0,law,mode); rows=[]
    for g in range(0,gmax+1):
        if g>0:
            for a,b,mm in gens[g]: m.bisect((min(a,b),max(a,b)),m=mm)
        Ei=m.energy()
        if mode=='I': r=m.relax(); vals=[(r['E'],True)]; ok=True
        else:
            vals,best=relax16(m); ok=best is not None
            if ok: m=best[1]
        if not ok: rows.append(dict(g=g,N3=len(m.T),statut='INCONCLUSIF',E16=[round(v,8) for v,_ in vals],admissibles=sum(o for _,o in vals))); break
        mt=m.metrics(); mt.update(g=g,E_insertion=Ei,E16min=min(v for v,_ in vals),E16max=max(v for v,_ in vals),admissibles=sum(o for _,o in vals),statut='ok'); rows.append(mt)
    return rows
if __name__=='__main__' and sys.argv[1]=='s1':
    out={}
    for law in 'UB':
        for mode in 'FIX':
            rows=s1_force(law,mode); out[law+mode]=rows; print(f'=== S1 forcé, loi {law}, frontière {mode}')
            for r in rows:
                if r['statut']!='ok': print(f"  g={r['g']} N3={r['N3']} INCONCLUSIF : {r['admissibles']}/16 minima admissibles ; énergies {min(r['E16']):.5f}..{max(r['E16']):.5f}"); continue
                print(f"  g={r['g']} N3={r['N3']:4d} E_ins={r['E_insertion']:9.4f} E_relax={r['E']:9.5f} (16 init. : {r['E16min']:.5f}..{r['E16max']:.5f}, {r['admissibles']}/16 adm.) E/arête={r['E']/r['N1']:.5f} volume={r['volume']:9.4f} diam={r['diam']:7.3f} fondateurs moy={np.mean(r['fondateurs']):7.3f} Lmin={r['Lmin']:.3f} Lmax={r['Lmax']:.3f} qmin={r['qmin']:.4f} degmax={r['degmax']} inv={r['inversions']} autoint={r['autointersections']}",flush=True)
    json.dump(out,open('c120_s1.json','w'),default=str)
