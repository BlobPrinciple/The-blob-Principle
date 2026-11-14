# Exploratoire (Claude) : feuilletage genealogique. Profondeur d'un sommet = generation de mitose (profondeur du tetra parent + 1).
# Un mouvement 2<->3 n'est autorise que si tous les sommets impliques ont des profondeurs dans une fenetre de largeur <= w.
exec(open('v1_b.py').read().split("R=int(sys.argv[1])")[0])
def growc(nb,R,seed,w):
    rng=random.Random(seed); L=[(0,1,2,3)]; pos={(0,1,2,3):0}; F={}; E={}; dep={0:0,1:0,2:0,3:0}
    def add(t):
        t=tuple(sorted(t)); pos[t]=len(L); L.append(t)
        for f in itertools.combinations(t,3): F.setdefault(f,set()).add(t)
        for e in itertools.combinations(t,2): E.setdefault(e,set()).add(t)
    def rem(t):
        i=pos.pop(t); last=L.pop()
        if last!=t: L[i]=last; pos[last]=i
        for f in itertools.combinations(t,3):
            F[f].discard(t)
            if not F[f]: del F[f]
        for e in itertools.combinations(t,2):
            E[e].discard(t)
            if not E[e]: del E[e]
    for f in itertools.combinations((0,1,2,3),3): F.setdefault(f,set()).add((0,1,2,3))
    for e in itertools.combinations((0,1,2,3),2): E.setdefault(e,set()).add((0,1,2,3))
    nv=4; acc=0
    for b in range(nb):
        t=L[rng.randrange(len(L))]; rem(t); dep[nv]=max(dep[v] for v in t)+1
        for m in range(4): add(tuple(nv if i==m else t[i] for i in range(4)))
        nv+=1
        for _ in range(R):
            t=L[rng.randrange(len(L))]
            if rng.random()<0.5:
                k=rng.randrange(4); f=tuple(v for i,v in enumerate(t) if i!=k); ts=F[f]
                if len(ts)!=2: continue
                t1,t2=tuple(ts); x=(set(t1)-set(f)).pop(); y=(set(t2)-set(f)).pop(); e=tuple(sorted((x,y)))
                vs=[dep[v] for v in f+(x,y)]
                if e in E or max(vs)-min(vs)>w: continue
                rem(t1); rem(t2)
                for pr in itertools.combinations(f,2): add(pr+(x,y))
                acc+=1
            else:
                e=tuple(sorted(rng.sample(t,2))); ts=E[e]
                if len(ts)!=3: continue
                link=sorted(set().union(*map(set,ts))-set(e))
                vs=[dep[v] for v in link+list(e)]
                if len(link)!=3 or tuple(link) in F or max(vs)-min(vs)>w: continue
                for tt in list(ts): rem(tt)
                add(tuple(link)+(e[0],)); add(tuple(link)+(e[1],)); acc+=1
    return L,F,acc
for w in (1,2,3):
    for nb in (320,1280):
        S=[];N=[];D=[];AC=[]
        for seed in range(3):
            L,F,acc=growc(nb,128,seed,w); A=dual(L,F); n=A.shape[0]; S.append(list(ds(A,ts=(8,16,32,64,128)).values())); N.append(n); AC.append(acc)
            d=shortest_path(A,unweighted=True,indices=np.random.default_rng(seed).choice(n,30,replace=False)); D.append(d[np.isfinite(d)].mean())
        print(f'fenêtre w={w} naissances={nb} tétras={int(np.mean(N))} mouvements acceptés={int(np.mean(AC))} distance={np.mean(D):.1f} d_s(8,16,32,64,128)={np.round(np.mean(S,axis=0),2).tolist()}',flush=True)
