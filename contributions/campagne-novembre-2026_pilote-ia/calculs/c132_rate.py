# C-132 bis, extension declaree : taux de reussite du critere fige a 15 naissances sur 20 graines (1320-1339), bras P (protocole) et L (regle de la cosmogonie).
import c132_audit as A, numpy as np
for arm in ('P','L'):
    ok=0; q=[]; v=[]; g=[]; f=[]
    for seed in range(1320,1340):
        rows,_=A.run(arm,seed,15); r=rows[-1]
        if r['statut']!='ok': continue
        p=(r['inv']==0 and r['qmin']>=0.01 and r['fmax']>1.05 and r['Vratio']>1); ok+=p; q.append(r['qmin']); v.append(r['Vratio']); g.append(r['gmax']); f.append(r['fmax'])
    print(f'{arm} : critère figé satisfait pour {ok}/20 graines ; qmin médian {np.median(q):.4f} (min {min(q):.4f}, max {max(q):.4f}) ; V/V0 moyen {np.mean(v):.1f} (de {min(v):.1f} à {max(v):.1f}) ; distance max entre fondateurs × {np.mean(f):.2f} ; résidu d\'optimalité max {max(g):.1e}',flush=True)
