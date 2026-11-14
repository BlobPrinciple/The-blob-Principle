# C-116 bis (controle de tendance, declare apres lecture des resultats de C-116) : la regle asynchrone A4 passe le critere aux deux tailles,
# mais son deficit de distance par rapport a S1 passe de -18 % a -28 %. Question : la distance suit-elle encore N^(1/3) a 262 144 cellules ?
# Mesures (sans diffusion) : degre maximal, distance entre porteurs du germe, distance moyenne (sommets : 20 sources ; dual : 10 sources).
import sys, json, itertools, random, numpy as np
from scipy.sparse.csgraph import shortest_path
import c114
src=open('c116.py').read().split("if __name__")[0]
src=src.replace("    return finish(L,F,E,nv,seed,extra)\ndef run_S2","    return light(L,F,E,nv,seed,extra)\ndef run_S2")
def light(L,F,E,nv,seed,extra):
    V=c114.vgraph(nv,list(E.keys())); A=c114.dual(L,F); rng=np.random.default_rng(seed)
    dg=shortest_path(V,unweighted=True,indices=[0,1,2,3])[:,[0,1,2,3]]
    dv=shortest_path(V,unweighted=True,indices=rng.choice(nv,20,replace=False)); dd=shortest_path(A,unweighted=True,indices=rng.choice(len(L),10,replace=False))
    deg=np.array(V.sum(1)).ravel()
    out=dict(N3=len(L),nv=nv,germe=float(dg[np.triu_indices(4,1)].mean()),distv=float(dv.mean()),dist=float(dd.mean()),degmax=int(deg.max()),diamv=float(dv.max()),diamd=float(dd.max())); out.update(extra); return out
ns={'light':light}; exec(src,ns)
def job(a): return ns['run'](a)
if __name__=='__main__':
    from multiprocessing import Pool
    jobs=[('S1',262144,1500)]+[(a,262144,s) for a in ('A4','M1') for s in (1500,1501,1502)]
    with Pool(2) as p: res=p.map(job,jobs,chunksize=1)
    json.dump(res,open('c116b.json','w'))
    for a in ('S1','A4','M1'):
        rs=[x for x in res if x['arm']==a]; m=lambda k:np.mean([x[k] for x in rs])
        print(f'{a}: tétras={m("N3"):.0f} sommets={m("nv"):.0f} degré max={m("degmax"):.0f} germe={m("germe"):.1f} dist sommets={m("distv"):.1f} (diam {m("diamv"):.0f}) dist duale={m("dist"):.1f} (diam {m("diamd"):.0f})',flush=True)
