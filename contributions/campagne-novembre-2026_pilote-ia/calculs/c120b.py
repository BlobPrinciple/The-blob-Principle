# C-120 / PR-1, complements d'execution (Claude, 12 nov. 2026).
# (A) Detail de l'echec U/F a g = 5 : inversions ou non-convergence ?
# (B) Controle DECLARE "F + exclusion" : meme minimisation libre, avec une force numerique de non-inversion, declaree comme telle :
#     penalite w * Somme_t max(0, eps*Vbar - V_t)^2, eps = 0,05, w = 1e4 / Vbar^2, Vbar = volume moyen des cellules au depart de la relaxation.
#     Ce bras ne valide jamais le bras principal ; il dit seulement si un minimum sans cellule retournee existe et s'il s'etend.
# (C) Controle du classement d'aretes apres relaxation LOCALE (classes g = 12, 13, 14), loi U, etat de base = equilibre homothetique.
import sys, itertools, math, json, numpy as np, scipy.optimize as so
import c120
from c120 import Mesh, SEEDS, vol6, s1_events, relax16
def relax_excl(m,eps=0.05,jitter=0.0,seed=0):
    ids=sorted(m.X); pos={v:i for i,v in enumerate(ids)}; X0=np.array([m.X[v] for v in ids]); ed=list(m.rest); I=np.array([pos[e[0]] for e in ed]); J=np.array([pos[e[1]] for e in ed]); R=np.array([m.rest[e] for e in ed])
    T=np.array([[pos[v] for v in t] for t in m.T])
    def vols(X):
        a,b,c,d=(X[T[:,i]] for i in range(4)); return np.einsum('ij,ij->i',b-a,np.cross(c-a,d-a))/6
    Vbar=float(vols(X0).mean()); w=1e4/Vbar**2
    if jitter>0: X0=X0+jitter*np.mean(np.linalg.norm(X0[I]-X0[J],axis=1))*np.random.default_rng(seed).standard_normal(X0.shape)
    def fun(z):
        X=z.reshape(-1,3); D=X[I]-X[J]; L=np.linalg.norm(D,axis=1); G=np.zeros_like(X); wv=((L-R)/np.maximum(L,1e-300))[:,None]*D
        np.add.at(G,I,wv); np.add.at(G,J,-wv); E=0.5*((L-R)**2).sum()
        a,b,c,d=(X[T[:,i]] for i in range(4)); V=np.einsum('ij,ij->i',b-a,np.cross(c-a,d-a))/6; def_=np.maximum(0,eps*Vbar-V); pen=w*(def_**2).sum()
        if pen>0:
            k=(-2*w*def_/6)[:,None]; gb=np.cross(c-a,d-a)*k; gc=np.cross(d-a,b-a)*k; gd=np.cross(b-a,c-a)*k
            np.add.at(G,T[:,1],gb); np.add.at(G,T[:,2],gc); np.add.at(G,T[:,3],gd); np.add.at(G,T[:,0],-(gb+gc+gd))
        return E+pen,G.ravel()
    r=so.minimize(fun,X0.ravel(),jac=True,method='L-BFGS-B',options=dict(gtol=1e-10,ftol=1e-15,maxiter=100000,maxcor=40,maxfun=400000))
    Xn=r.x.reshape(-1,3)
    for v in ids: m.X[v]=Xn[pos[v]]
    V=vols(Xn); Eh=m.energy(); gmax=float(np.abs(r.jac).max())
    return dict(E=Eh,pen=float(r.fun-Eh),gmax=gmax,valid=bool(V.min()>0),conv=bool(gmax<=1e-8*max(1.0,float(r.fun))),nactive=int((V<eps*Vbar).sum()),Vmin=float(V.min()),Vbar=Vbar)
if sys.argv[1]=='A':
    gens=s1_events(6); m=Mesh(SEEDS['Kuhn'],1.0,'U','F')
    for g in range(0,6):
        if g>0:
            for a,b,mm in gens[g]: m.bisect((min(a,b),max(a,b)),m=mm)
        res=[]
        for i,sd in enumerate(range(1500,1516)):
            c=m.copy(); r=c.relax(jitter=0.0 if i==0 else 0.02,seed=sd); res.append((round(r['E'],6),r['valid'],r['conv'],sum(vol6(c.X,t)<=0 for t in c.T)))
        print('g =',g,'N3 =',len(m.T),': (énergie, sans inversion, convergé, cellules inversées) :',sorted(set(res)))
        ok=[x for x in res if x[1] and x[2]]
        if not ok: break
        vals,best=relax16(m); m=best[1]
if sys.argv[1]=='B':
    gens=s1_events(9); m=Mesh(SEEDS['Kuhn'],1.0,'U','F'); prev=None
    print('S1 forcé, loi U, frontière libre + exclusion déclarée (eps = 0,05)')
    for g in range(0,10):
        if g>0:
            for a,b,mm in gens[g]: m.bisect((min(a,b),max(a,b)),m=mm)
        best=None; allv=[]
        for i,sd in enumerate(range(1500,1516)):
            c=m.copy(); r=relax_excl(c,jitter=0.0 if i==0 else 0.02,seed=sd); allv.append((r['E']+r['pen'],r['valid'],r['conv']))
            if r['valid'] and (best is None or r['E']+r['pen']<best[0]-1e-12): best=(r['E']+r['pen'],c,r)
        if best is None: print('  g =',g,': aucun minimum sans inversion'); break
        m=best[1]; r=best[2]; mt=m.metrics()
        print(f"  g={g} N3={mt['N3']:4d} E_Hooke={r['E']:9.5f} pénalité={r['pen']:.2e} cellules au contact de la contrainte={r['nactive']} convergé={r['conv']} ({sum(v for _,v,_ in allv)}/16 sans inversion ; énergies {min(x for x,_,_ in allv):.5f}..{max(x for x,_,_ in allv):.5f}) E/arête={r['E']/mt['N1']:.5f} volume={mt['volume']:9.4f} diam={mt['diam']:7.3f} fondateurs moy={np.mean(mt['fondateurs']):7.3f} Lmin={mt['Lmin']:.3f} Lmax={mt['Lmax']:.3f} qmin={mt['qmin']:.4f} degmax={mt['degmax']} autoint={mt['autointersections']}",flush=True)
if sys.argv[1]=='C':
    src=open('c116.py').read().split("if __name__")[0]
    src=src.replace("    return finish(L,F,E,nv,seed,extra)\ndef run_S2","    return (L,F,E,nv,P)\ndef run_S2"); ns={}; exec(src,ns)
    for target,g in ((4096,12),(8192,13),(16384,14)):
        L,F,E,nv,P=ns['run'](('S1',target,1500)); P=np.array(P); bnd=set(v for f,ts in F.items() if len(ts)==1 for v in f)
        inte=[e for e in E if e[0] not in bnd and e[1] not in bnd]; Lr=np.array([np.linalg.norm(P[a]-P[b]) for a,b in inte]); a_eq=Lr.sum()/(Lr**2).sum()
        m=Mesh.__new__(Mesh); m.X={i:P[i]*a_eq for i in range(nv)}; m.T=set(t if vol6(m.X,t)>0 else (t[1],t[0],t[2],t[3]) for t in L); m.l0=1.0; m.law='U'; m.mode='F'; m.rest={e:1.0 for e in E}; m.nv=nv; m.fixed=set(); m.rejected=0
        inc=m.inc(); cell=next(t for t in L if not any(v in bnd for v in t) and all(not any(v in bnd for v in t2) for e in itertools.combinations(sorted(t),2) for t2 in E[e]))
        lmin=min(m.length(e) for e in E); print(f'génération {g} : alpha_eq = {1/lmin:.4f} ; cellule intérieure {cell}')
        rows=[]
        for e in itertools.combinations(sorted(cell),2):
            dEi=m.dE_insert(e,inc); k=m.copy(); patch=set(v for t in inc[e] for v in t); Eb=k.energy(); mm=k.bisect(e); r=k.relax(free=sorted(patch|{mm}))
            rows.append((m.length(e)/lmin,dEi,r['E']-Eb,r['valid'],r['conv']))
        lmax=max(x[0] for x in rows); i1=int(np.argmin([x[1] for x in rows])); i2=int(np.argmin([x[2] for x in rows]))
        for x in rows: print(f'   arête de longueur {x[0]:.4f} : ΔE_insertion = {x[1]:+.5f} ; ΔE après relaxation locale = {x[2]:+.5f} (sans inversion {x[3]}, convergé {x[4]})')
        print(f'   minimum à l\'insertion : longueur {rows[i1][0]:.4f} ({"la plus longue" if rows[i1][0]>=lmax-1e-9 else "PAS la plus longue"}) ; minimum après relaxation : longueur {rows[i2][0]:.4f} ({"la plus longue" if rows[i2][0]>=lmax-1e-9 else "PAS la plus longue"})',flush=True)
