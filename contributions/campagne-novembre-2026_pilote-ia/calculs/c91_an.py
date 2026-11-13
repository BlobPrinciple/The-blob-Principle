import json, numpy as np
rng=np.random.default_rng(0)
def conc(d,L):
    s=[];n=len(d)
    for i in range(n):
        for j in range(i+1,n):
            a=(d[i]-d[j])*(L[i]-L[j])
            if abs(d[i]-d[j])>1e-12 and abs(L[i]-L[j])>1e-12: s.append(np.sign(a))
    return np.mean(s) if s else np.nan
for g in ('0.5','1.5','4.0'):
    R=json.load(open(f'c91_g{g}.json'))
    for pl in ('ref','ctl2','ctl3'):
        per=[]; states=[]; noninf=0
        for hist in R:
            cs=[]
            for rows in hist:
                if len(rows)<2: noninf+=1; continue
                d=np.array([r[pl] for r in rows]); L=np.array([r['L'] for r in rows]); states.append((d,L)); c=conc(d,L)
                if not np.isnan(c): cs.append(c)
            per.append(np.mean(cs) if cs else np.nan)
        per=np.array(per); obs=np.nanmean(per)
        # permutation : d permute dans chaque etat
        null=[]
        for b in range(500):
            vals=[]; k=0
            for hist in R:
                cs=[]
                for rows in hist:
                    if len(rows)<2: continue
                    d=np.array([r[pl] for r in rows]); L=np.array([r['L'] for r in rows]); c=conc(rng.permutation(d),L)
                    if not np.isnan(c): cs.append(c)
                vals.append(np.mean(cs) if cs else np.nan)
            null.append(np.nanmean(vals))
        null=np.array(null); p=(np.sum(null>=obs)+1)/(len(null)+1)
        boot=[np.nanmean(rng.choice(per[~np.isnan(per)],size=np.sum(~np.isnan(per)))) for _ in range(2000)]
        print(f"g={g} plan={pl}: concordance τ moyenne {obs:+.3f} ; IC95 histoires [{np.percentile(boot,2.5):+.3f}, {np.percentile(boot,97.5):+.3f}] ; nul {null.mean():+.3f}±{null.std():.3f} ; p={p:.4f} ; états non informatifs {noninf}")
