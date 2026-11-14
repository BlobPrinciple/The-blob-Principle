# C-119 — LA TENSION CHOISIT-ELLE LE FIL LE PLUS LONG ? (test propose par ChatGPT, execute par Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Tension historique du Blob (C-12, C-15, C-23, C-24) : ressorts de Hooke de longueur naturelle COMMUNE l0 sur les aretes.
# Trame : S1 (C-116) aux generations 12, 13, 14 (les trois classes de forme). Longueurs physiques = longueurs plongees / (plus courte arete), de sorte
#   que la plus courte arete vaut 1 ; alpha = l0 / (plus courte arete).
# Pour chaque cellule interieure et chacune de ses 6 aretes e, on calcule la variation d'energie DE(e) si un porteur nait au milieu de e
#   (toutes les cellules autour de e se divisent). Deux comptages : E1 = une fois par arete ; E2 = une fois par (cellule, arete) (comptage de ChatGPT).
# Questions : (a) l'arete qui minimise DE est-elle la plus longue de la cellule ? (b) DE est-elle negative (naissance spontanee) ?
# PREDICTIONS ENREGISTREES : E2 choisit la plus longue arete pour alpha < 1,4 (calcul a une cellule : seuil 1/0,708) ; pour alpha = 0 c'est un theoreme
#   (ChatGPT : DE = E(T) - 5/2 l^2). E1 : inconnu. Fenetre de naissance spontanee pour E2 a une cellule : 0,37 < alpha < 1,11.
import itertools, numpy as np, json
src=open('c116.py').read().split("if __name__")[0]
src=src.replace("    return finish(L,F,E,nv,seed,extra)\ndef run_S2","    return (L,F,E,nv,P)\ndef run_S2")
ns={}; exec(src,ns)
def dist(P,a,b): return float(np.linalg.norm(np.subtract(P[a],P[b])))
def analyse(target):
    L,F,E,nv,P=ns['run'](('S1',target,1500)); P=[np.array(p) for p in P]
    bnd=set(v for f,ts in F.items() if len(ts)==1 for v in f)
    lmin=min(dist(P,a,b) for a,b in E); ln={e:dist(P,*e)/lmin for e in E}
    def dE(e,alpha,mode):
        a,b=e; m=(P[a]+P[b])/2; l=ln[e]; ts=E[e]; h=lambda x:(x-alpha)**2
        link=set(v for t in ts for v in t if v!=a and v!=b); sp={x:float(np.linalg.norm(P[x]-m))/lmin for x in link}
        if mode==1: return 2*h(l/2)-h(l)+sum(h(s) for s in sp.values())
        tot=0
        for t in ts:
            x,y=[v for v in t if v!=a and v!=b]; o=[ln[tuple(sorted(p))] for p in ((a,x),(a,y),(b,x),(b,y))]; xy=ln[tuple(sorted((x,y)))]
            tot+=2*h(l/2)+sum(h(v) for v in o)+2*(h(sp[x])+h(sp[y]))+2*h(xy)-(h(l)+sum(h(v) for v in o)+h(xy))
        return tot
    cells=[t for t in L if not any(v in bnd for v in t)]
    out={}
    for mode in (1,2):
        for alpha in (0,0.25,0.5,0.75,1.0,1.25,1.5,2.0,3.0):
            ok=0; neg=0; vals=[]
            for t in cells:
                es=list(itertools.combinations(t,2)); d=[dE(e,alpha,mode) for e in es]; i=int(np.argmin(d)); lmax=max(ln[e] for e in es)
                ok+=ln[es[i]]>=lmax-1e-9; neg+=min(d)<0; vals.append(min(d))
            out[(mode,alpha)]=(ok/len(cells),neg/len(cells),float(np.mean(vals)))
    return len(L),len(cells),out
res={}
for target,g in ((4096,12),(8192,13),(16384,14)):
    n,nc,out=analyse(target); res[g]=out
    print(f'génération {g} : {n} cellules, {nc} intérieures')
    for mode in (1,2):
        print('  comptage',('par arête (E1)' if mode==1 else 'par cellule (E2)'))
        for alpha in (0,0.25,0.5,0.75,1.0,1.25,1.5,2.0,3.0):
            a,b,c=out[(mode,alpha)]; print(f'    alpha={alpha:<4}: plus longue arête choisie {100*a:5.1f} %  naissance spontanée {100*b:5.1f} %  ΔE moyen {c:+.3f}')
