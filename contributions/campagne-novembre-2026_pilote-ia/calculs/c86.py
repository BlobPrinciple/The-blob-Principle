# C-86 / PR-1 (preenregistre par ChatGPT, execute par Claude). Aucun operateur nouveau.
import numpy as np, itertools
exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
def pol(c,s): return int(np.sign(sum(s[v] for v in c)))
def R0(maxs,s):
    cells=complex_from_max(maxs); bad=[c for c in cells if len(c)==2 and pol(c,s)==0]
    return sorted([c for c in cells if not any(set(e)<=set(c) for e in bad)],key=lambda c:(len(c),c))
def sgn_sort(t):
    t=list(t); sg=1
    for i in range(len(t)):
        for j in range(len(t)-1-i):
            if t[j]>t[j+1]: t[j],t[j+1]=t[j+1],t[j]; sg=-sg
    return tuple(t),sg
def build(kind,k):
    if kind=='C76': n=4; plus=[tuple(range(4))]; 
    else: n=5; plus=[tuple(x for x in range(5) if x!=i) for i in range(5)]
    ren=lambda v:(100+v%n if v%n<k else v)
    minus=[tuple(v+n for v in t) for t in plus]
    maxs=[tuple(sorted(ren(v) for v in t)) for t in plus+minus]
    verts=sorted({ren(v) for v in range(2*n)})
    s={v:(0 if v>=100 else (1 if v<n else -1)) for v in verts}
    mirv={v:(v if v>=100 else (v+n if v<n else v-n)) for v in verts}
    return maxs,s,mirv,verts
def ops_(cells,s,g):
    idx={c:i for i,c in enumerate(cells)}; N=len(cells); d=np.zeros((N,N))
    for c in cells:
        for j in range(len(c)):
            f=c[:j]+c[j+1:]
            if f and f in idx: d[idx[c],idx[f]]+=(-1)**j
    G=np.diag([(-1.0)**(len(c)-1) for c in cells]); S=np.diag([float(pol(c,s)) for c in cells])
    return d,d+d.T,G,S,idx
def permop(cells,idx,perm):
    U=np.zeros((len(cells),len(cells)))
    for c in cells:
        img,sg=sgn_sort([perm[v] for v in c])
        if img not in idx: return None
        U[idx[img],idx[c]]=sg
    return U
def levels(H,tol=1e-9):
    e,V=np.linalg.eigh(H); out=[]; i=0
    while i<len(e):
        j=i
        while j<len(e) and abs(e[j]-e[i])<tol: j+=1
        out.append((e[i],V[:,i:j])); i=j
    return out
rep=[]
for kind in ('C76','DD4'):
  for k in ((1,2,3) if kind=='C76' else (1,2,3)):
    maxs,s,mirv,verts=build(kind,k); cells=R0(maxs,s)
    n3=sum(len(c)==4 for c in cells)
    for g in (0.5,1.5,4.0):
      d,D,G,S,idx=ops_(cells,s,g); H=D+g*S@G; P=permop(cells,idx,mirv); C=G@P
      ctrl=dict(d2=np.abs(d@d).max(),herm=np.abs(H-H.T).max(),P2=np.abs(P@P-np.eye(len(cells))).max(),C2=np.abs(C@C-np.eye(len(cells))).max(),
                CH=np.abs(C@H+H@C).max(),HG=np.abs(H@G+G@H-2*g*S).max(),PHP=np.abs(P@H@P-H).max(),SH=np.abs(S@H-H@S).max())
      # C-86A : algebre engendree (mots de longueur <=3) par Sigma, Gamma, P, C, projecteurs de sites, Pi_F
      F=[c for c in cells if len(c)==1 and c[0]>=100]
      PiF=np.zeros_like(H)
      for c in F: PiF[idx[c],idx[c]]=1
      gens={'S':S,'G':G,'P':P,'C':C,'PiF':PiF,**{f'Pi{c[0]}':np.diag([1.0 if x==c else 0 for x in cells]) for c in F}}
      words={'I':np.eye(len(cells))}
      for L in (1,2,3):
        for w in itertools.product(gens,repeat=L):
          M=np.eye(len(cells))
          for x in w: M=M@gens[x]
          words['.'.join(w)]=M
      # base lineaire de l'espace engendre
      Wm=np.array([m.ravel() for m in words.values()]); U_,sv,Vt=np.linalg.svd(Wm,full_matrices=False); B=Vt[sv>1e-9]
      comm=np.array([(b.reshape(H.shape)@H-H@b.reshape(H.shape)).ravel() for b in B])
      _,sv2,Vt2=np.linalg.svd(comm.T,full_matrices=True); null=Vt2[np.sum(sv2>1e-8):]
      Qs=[sum(a*b for a,b in zip(v,B)).reshape(H.shape) for v in null]
      polyH=np.array([np.linalg.matrix_power(H,j).ravel() for j in range(len(cells))]); _,svp,Vp=np.linalg.svd(polyH,full_matrices=False); PB=Vp[svp>1e-9]
      nontriv=0; qspecs=[]
      for Q in Qs:
        r=Q.ravel()-PB.T@(PB@Q.ravel())
        if np.linalg.norm(r)>1e-7:
          nontriv+=1; qspecs.append(np.round(np.unique(np.round(np.linalg.eigvals(Q).real,6)),4).tolist())
      # C-86B : automorphismes (permutations des sommets) preservant les cellules, commutant avec le miroir, preservant Sigma
      auts=[]
      for p in itertools.permutations(verts):
        perm=dict(zip(verts,p))
        if any(perm[mirv[v]]!=mirv[perm[v]] for v in verts): continue
        if any(s[perm[v]]!=s[v] for v in verts): continue
        U=permop(cells,idx,perm)
        if U is None: continue
        auts.append((perm,U))
      homo=max(np.abs(U1@U2-permop(cells,idx,{v:p1[p2[v]] for v in verts})).max() for p1,U1 in auts for p2,U2 in auts)
      commH=max(np.abs(U@H-H@U).max() for _,U in auts)
      lev=levels(H); zero=[l for l in lev if abs(l[0])<1e-9]; pos=[l for l in lev if l[0]>1e-9][:3]
      def chars(Vb): return tuple(int(round(np.trace(Vb.T@U@Vb))) for _,U in auts)
      rep.append(dict(kind=kind,k=k,g=g,ncells=len(cells),n3=n3,ctrl={a:float(f'{b:.1e}') for a,b in ctrl.items()},
          nQ=len(Qs),nQ_nontriv=nontriv,qspec=qspecs[:4],naut=len(auts),homo=float(f'{homo:.1e}'),commH=float(f'{commH:.1e}'),
          ker=(zero[0][1].shape[1] if zero else 0, chars(zero[0][1]) if zero else None),
          pos=[(round(e,5),V.shape[1],chars(V)) for e,V in pos]))
for r in rep: print(r)
