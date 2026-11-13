# Contre-audit de C-120 (ChatGPT) par Claude, 12 nov. 2026. Trame S1 (C-116), generations 12, 13, 14 (les trois classes).
# (1) alpha d'equilibre sous relaxation homothetique, ressorts de longueur naturelle commune : alpha_eq = Somme L^2 / (Somme L * L_min).
# (2) seuil exact alpha* au-dela duquel la tension de Hooke ne choisit plus la plus longue arete (comptages par cellule et par arete).
# (3) fenetre de naissance spontanee (DE < 0 pour la bissection de la plus longue arete).
# (4) energie elastique par arete a l'equilibre : (K l0^2 / 2) * (1 - (moy L)^2 / moy L^2).
import itertools, numpy as np, math
src=open('c116.py').read().split("if __name__")[0]
src=src.replace("    return finish(L,F,E,nv,seed,extra)\ndef run_S2","    return (L,F,E,nv,P)\ndef run_S2")
ns={}; exec(src,ns)
print('valeur de ChatGPT (réseau régulier 3:3:1) : 12/(3+3√2+√3) =',12/(3+3*math.sqrt(2)+math.sqrt(3)))
for target,g in ((4096,12),(8192,13),(16384,14),(32768,15)):
    L,F,E,nv,P=ns['run'](('S1',target,1500)); P=[np.array(p) for p in P]
    bnd=set(v for f,ts in F.items() if len(ts)==1 for v in f)
    lmin=min(float(np.linalg.norm(P[a]-P[b])) for a,b in E); ln={e:float(np.linalg.norm(P[e[0]]-P[e[1]]))/lmin for e in E}
    inte=[e for e in E if e[0] not in bnd and e[1] not in bnd]
    Lall=np.array(list(ln.values())); Lint=np.array([ln[e] for e in inte])
    aeq=lambda v:(v**2).sum()/v.sum(); res=lambda v:1-v.mean()**2/(v**2).mean()
    from collections import Counter
    print(f'génération {g} : {len(L)} cellules ; longueurs² (arêtes intérieures) {sorted(Counter(np.round(Lint**2,6)).items())}')
    print(f'   alpha_eq toutes arêtes = {aeq(Lall):.5f} ; arêtes intérieures = {aeq(Lint):.5f} ; énergie résiduelle par arête (unités K l0²/2) = {res(Lint):.5f}')
    if g==15: continue
    def dE(e,alpha,mode):
        a,b=e; m=(P[a]+P[b])/2; l=ln[e]; ts=E[e]; h=lambda x:(x-alpha)**2
        link=set(v for t in ts for v in t if v!=a and v!=b); sp={x:float(np.linalg.norm(P[x]-m))/lmin for x in link}
        if mode==1: return 2*h(l/2)-h(l)+sum(h(s) for s in sp.values())
        tot=0
        for t in ts:
            x,y=[v for v in t if v!=a and v!=b]; o=[ln[tuple(sorted(p))] for p in ((a,x),(a,y),(b,x),(b,y))]; xy=ln[tuple(sorted((x,y)))]
            tot+=2*h(l/2)+2*(h(sp[x])+h(sp[y]))+h(xy)-h(l)
        return tot
    cell=next(t for t in L if not any(v in bnd for v in t) and all(not any(v in bnd for v in t2) for e in itertools.combinations(t,2) for t2 in E[e]))
    es=list(itertools.combinations(cell,2)); lmax=max(ln[e] for e in es); elong=[e for e in es if ln[e]>=lmax-1e-9][0]
    for mode in (2,1):
        choisi=lambda al:ln[es[int(np.argmin([dE(e,al,mode) for e in es]))]]>=lmax-1e-9
        grid=np.linspace(0,3,3001); ok=[choisi(a) for a in grid]; neg=[dE(elong,a,mode)<0 for a in grid]
        seg=lambda b:[(round(float(grid[i]),3),round(float(grid[j]),3)) for i,j in zip([i for i in range(len(b)) if b[i] and (i==0 or not b[i-1])],[i for i in range(len(b)) if b[i] and (i==len(b)-1 or not b[i+1])])]
        print(f'   comptage {"par cellule" if mode==2 else "par arête  "} : plus longue arête choisie pour alpha dans {seg(ok)} ; naissance spontanée pour alpha dans {seg(neg)} ; à alpha_eq={aeq(Lint):.3f} : choisie={choisi(aeq(Lint))}, ΔE={dE(elong,aeq(Lint),mode):+.3f}')
