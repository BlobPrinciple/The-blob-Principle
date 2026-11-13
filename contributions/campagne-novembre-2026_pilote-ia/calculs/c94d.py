# Audit de C-94 (ChatGPT) : (a) H^2 = D^2 + g^2 sur C=-1 ; (b) non-retour a n pas avec evolution UNITAIRE a temps aleatoires (sans dephasage)
exec(open('c94c.py').read().split("worst=0")[0])
exec(open('c86.py').read().split('rep=[]')[0].split("exec(open('c64_defi.py')")[0]) if False else None
from scipy.linalg import expm
# (a) sur les complexes de croissance
mxa=0
for k in (1,2,3):
  for seed in range(4):
    sn=chain(k,seed,4)
    # reconstruire P (miroir) et Gamma pour chaque instantane
    for cells,idx,Hm,P,V in sn:
      pass
print('(a) voir plus bas')
# reconstruction de C : on refait la croissance avec le miroir explicite
def chain2(k,seed,ngen,g=1.5):
    rng=random.Random(seed)
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
    tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]; F=[100+i for i in range(k)]; nv=200; out=[]
    for gen in range(ngen+1):
        cells=R0(tp+tm,s); idx={c:i for i,c in enumerate(cells)}; N=len(cells); d=np.zeros((N,N))
        for c in cells:
            for j in range(len(c)):
                f=c[:j]+c[j+1:]
                if f and f in idx: d[idx[c],idx[f]]+=(-1)**j
        D=d+d.T; G=np.diag([(-1.0)**(len(c)-1) for c in cells]); Sg=np.diag([float(pol(c,s)) for c in cells]); Hm=D+g*Sg@G
        Pm=np.zeros((N,N))
        for c in cells:
            img=[mir[v] for v in c]; srt=sorted(img); sg=1
            l=list(img)
            for i in range(len(l)):
                for j in range(len(l)-1-i):
                    if l[j]>l[j+1]: l[j],l[j+1]=l[j+1],l[j]; sg=-sg
            Pm[idx[tuple(srt)],idx[c]]=sg
        out.append((cells,idx,Hm,D,G@Pm,F))
        j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir)
        a,b=nv,nv+1; nv+=2; sg=pol(t,s) or 1; s[a]=sg; s[b]=-sg; mir[a]=b; mir[b]=a
        tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
        tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
    return out
g=1.5; mxa=0; mxb=0; occ=[]
for k in (1,2,3):
  for seed in range(4):
    sn=chain2(k,seed,6)
    for cells,idx,Hm,D,C,F in sn:
      N=len(cells); Qm=(np.eye(N)-C)/2   # projecteur sur C=-1
      mxa=max(mxa,np.abs(Qm@(Hm@Hm-D@D-g*g*np.eye(N))@Qm).max())
    # (b) evolution unitaire a temps aleatoires, n naissances, sans dephasage
    rng=np.random.default_rng(seed)
    cells,idx,Hm,D,C,F=sn[0]; e,U=np.linalg.eigh(Hm); K=U[:,abs(e)<1e-9]; psi=K@rng.normal(size=K.shape[1]); psi/=np.linalg.norm(psi)
    for n in range(1,len(sn)):
        psi=expm(-1j*Hm*rng.uniform(0.3,7))@psi
        c2,i2,H2,D2,C2,F2=sn[n]; S=np.zeros((len(c2),len(cells)))
        for c,i in idx.items():
            if c in i2: S[i2[c],i]=1
        e2,U2=np.linalg.eigh(H2); K2=U2[:,abs(e2)<1e-9]
        # partie de psi hors noyau AVANT la naissance : son image ne doit pas toucher le nouveau noyau
        Kold=np.linalg.eigh(Hm)[1][:,abs(np.linalg.eigh(Hm)[0])<1e-9]
        out_part=psi-Kold@(Kold.conj().T@psi)
        mxb=max(mxb,np.linalg.norm(K2.conj().T@(S@out_part)))
        psi=S@psi; cells,idx,Hm,D,C,F=c2,i2,H2,D2,C2,F2
print('(a) max |Q(H²−D²−g²)Q| sur C=−1 :',mxa)
print('(b) non-retour à n pas, évolution unitaire à temps aléatoires : max |P_new S (partie hors noyau)| =',mxb)
