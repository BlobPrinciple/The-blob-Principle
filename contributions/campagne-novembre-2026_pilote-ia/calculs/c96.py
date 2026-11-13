# C-96 / PR-1 (fige par ChatGPT, SHA f409a37f...) execute par Claude. Graines 200-263, 20 naissances, k=2,3.
import sys, json, numpy as np
exec(open('c94c.py').read().split("worst=0")[0])
g=float(sys.argv[1]); out={}
cinf=lambda k,g:(4/(g**4+6*g**2+4) if k==2 else 2/(g**4+5*g**2+2))
for k in (2,3):
    HIST=[]
    for seed in range(200,264):
        sn=chain(k,seed,20,g); X=sn[0][4].copy(); G0=X.T@X; rec=[]; idmax=0
        for n in range(1,len(sn)):
            X=Smat(sn[n-1],sn[n])@X; Vn=sn[n][4]; Gn=Vn.T@Vn; R=X-Vn
            idmax=max(idmax,np.abs(R.T@R-(G0-Gn)).max())
            C=R.T@R; d=np.sqrt(np.diag(C)); cm=max(abs(C[i,j])/(d[i]*d[j]) for i in range(k) for j in range(i+1,k))
            rec.append(cm)
        c00=max(abs(G0[i,j])/np.sqrt(G0[i,i]*G0[j,j]) for i in range(k) for j in range(i+1,k))
        HIST.append(dict(rec=rec,id=idmax,c0=c00))
    out[k]=HIST
json.dump(out,open(f'c96_g{g}.json','w')); print('fini',g)
