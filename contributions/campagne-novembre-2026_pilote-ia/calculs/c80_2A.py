# C-80.2A (Claude) : drift des poids de site sous les vrais transports de naissance jumelee signee.
# Complexe intact, R0 en lecture (noyau calcule sur R0(complexe)), g=1.5. Tirage uniforme du parent parmi les tetras +.
# Transport A_T = P0' . iota, deux variantes figees AVANT calcul :
#  (a) restriction : les coefficients sur les cellules persistantes sont gardes, la cellule t disparait ;
#  (b) subdivision : t -> somme signee des 4 nouveaux tetras (application de subdivision stellaire).
# Base de sites : v_i = P0 e_(c_i) (c_i = sommet de rencontre i). w_i = |c_i|^2/sum|c|^2 pour psi = sum c_i v_i.
import random, numpy as np, itertools
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
def pol(c,s): return np.sign(sum(s[v] for v in c))
def R0(maxs,s):
    cells=complex_from_max(maxs); bad=[c for c in cells if len(c)==2 and pol(c,s)==0]
    return sorted([c for c in cells if not any(set(e)<=set(c) for e in bad)],key=lambda c:(len(c),c))
def H(cells,s,g):
    idx={c:i for i,c in enumerate(cells)}; n=len(cells); d=np.zeros((n,n))
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f and f in idx: d[idx[c],idx[f]]+=(-1)**j
    D=d+d.T; G=np.diag([(-1)**(len(c)-1) for c in cells]); S=np.diag([pol(c,s) for c in cells])
    return D+g*S@G, idx
def kern(cells,s,g):
    M,idx=H(cells,s,g); e,V=np.linalg.eigh(M); K=V[:,abs(e)<1e-9]; return K@K.T, idx
def sgn_sort(t):
    t=list(t); sg=1
    for i in range(len(t)):
        for j in range(len(t)-1-i):
            if t[j]>t[j+1]: t[j],t[j+1]=t[j+1],t[j]; sg=-sg
    return tuple(t),sg
def coords(P,idx,sites,psi):
    Vs=np.array([P[:,idx[(c,)]] for c in sites]).T
    c,*_=np.linalg.lstsq(Vs,psi,rcond=None); res=np.linalg.norm(Vs@c-psi)
    w=c**2/np.sum(c**2); return w,res
g=1.5; out=[]
for k in (2,3):
  for seed in range(4):
    rng=random.Random(seed)
    ren={v:(100+v%4 if v%4<k else v) for v in range(8)}
    s={**{v:(1 if v<4 else -1) for v in range(8) if v%4>=k},**{100+i:0 for i in range(k)}}
    mir={**{v:(v+4)%8 for v in range(8) if v%4>=k},**{100+i:100+i for i in range(k)}}
    tp=[tuple(sorted(ren[v] for v in (0,1,2,3)))]; tm=[tuple(sorted(ren[v] for v in (4,5,6,7)))]
    sites=[100+i for i in range(k)]; nv=200
    w0=np.array([0.3,0.7]) if k==2 else np.array([0.2,0.3,0.5])
    for gen in range(3):
      cells=R0(tp+tm,s); P,idx=kern(cells,s,g)
      Vs=np.array([P[:,idx[(c,)]] for c in sites]).T
      psi=Vs@np.sqrt(w0)
      for var in 'ab':
        drs=[];ress=[];norms=[]
        for j in range(len(tp)):
          t=tp[j]; tmir=tuple(sorted(mir[x] for x in t)); a,b=nv,nv+1
          s2=dict(s); sg=pol(t,s) or 1; s2[a]=sg; s2[b]=-sg
          tp2=tp[:j]+tp[j+1:]+[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
          tm2=[x for x in tm if x!=tmir]+[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
          cells2=R0(tp2+tm2,s2); P2,idx2=kern(cells2,s2,g)
          phi=np.zeros(len(cells2))
          for c,i in idx.items():
            if c in idx2: phi[idx2[c]]+=psi[i]
            elif var=='b' and c in (t,tmir):
              nn=a if c==t else b
              for i3 in range(4):
                nc=list(c); nc[i3]=nn; nc,sg2=sgn_sort(nc)
                if nc in idx2: phi[idx2[nc]]+=sg2*psi[i]
          phi=P2@phi; norms.append(np.linalg.norm(phi)/np.linalg.norm(psi))
          w,res=coords(P2,idx2,sites,phi); drs.append(w-w0); ress.append(res/np.linalg.norm(phi))
        out.append((k,seed,gen,var,np.mean(drs,axis=0),max(ress),min(norms),max(norms),np.max(np.abs(drs))))
      # avance l'histoire (tirage uniforme)
      j=rng.randrange(len(tp)); t=tp.pop(j); tmir=tuple(sorted(mir[x] for x in t)); tm.remove(tmir)
      a,b=nv,nv+1; nv+=2; sg=pol(t,s) or 1; s[a]=sg; s[b]=-sg; mir[a]=b; mir[b]=a
      tp+=[tuple(sorted(tuple(x for i2,x in enumerate(t) if i2!=i)+(a,))) for i in range(4)]
      tm+=[tuple(sorted(tuple(x for i2,x in enumerate(tmir) if i2!=i)+(b,))) for i in range(4)]
np.set_printoptions(precision=5,suppress=False)
for o in out: print(o[:4],'delta=',o[4],'resid=%.1e'%o[5],'|A|∈[%.4f,%.4f]'%(o[6],o[7]),'max|Δw|=%.2e'%o[8])
