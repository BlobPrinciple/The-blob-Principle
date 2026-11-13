# Exploratoire hors grille (declare) : zone de transition, chaines longues. 324 sommets, graines 610-612, 1500 balayages.
import sys,json
exec(open('c111.py').read().split("if __name__")[0])
from multiprocessing import Pool
if __name__=='__main__':
    LAM=[0.7,0.8,0.85,0.9,0.95,1.0,1.1]
    with Pool(2) as p: res=p.map(run,[(320,l,s,1500) for l in LAM for s in (610,611,612)])
    json.dump(res,open('c111b.json','w'))
    for lam in LAM:
        rs=[r for r in res if r['lam']==lam]; N0=rs[0]['N0']
        q=lambda r,a,b:np.mean(r['n3'][int(a*len(r['n3'])):int(b*len(r['n3']))])/N0
        print(f'λ={lam}: N3/N0 par quart de la fenêtre de mesure = {[round(np.mean([q(r,a,a+0.25) for r in rs]),3) for a in (0,0.25,0.5,0.75)]} ; par graine (fin) {[round(q(r,0.75,1),2) for r in rs]} ; distance={np.mean([r["dist"] for r in rs]):.1f} ; d_s(8..128)={np.round(np.mean([r["ds"] for r in rs],axis=0),2).tolist()}')
