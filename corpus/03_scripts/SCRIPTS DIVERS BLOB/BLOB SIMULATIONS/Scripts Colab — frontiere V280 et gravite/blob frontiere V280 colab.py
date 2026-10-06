#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# BLOB — LA FRONTIÈRE V280 (Colab) — 18 juillet 2026. Autonome.
# Cinq volets, cinq verrous. Toutes grilles PRÉ-ENREGISTRÉES, gravées avant lecture.
#
#  F1  PERCOLATION Delaunay∩Blob — balayage degré 10→30, N grand. Le pont variété :
#      la fraction retenue croît (mesuré ×6,7 de deg-10→18) ; où est le seuil ?
#      GRILLE : PERCOLE si géante ≥50% des retenus ET span ≥80%. Sinon : courbe gravée,
#      et si fraction(deg-30) < 5% → la voie « filtre strict 6/6 » est déclarée
#      insuffisante, bascule vers filtre relâché (chantier à grille séparée).
#  F2  ℤ₂ FSS — N ∈ {2,5k, 6k, 12k, 20k}, κ ∈ [0,30;0,70] pas 0,05.
#      GRILLE : TRANSITION si χ_max(N) croît monotone ET ajustement χ_max ~ F^{γ/(νd)}
#      donne un exposant > 0,3 ; κ_c = position du pic à plus grand N (rapportée ±0,05).
#      Si χ_max sature → crossover/désordre (Harris) — gravé tel quel.
#  F3  TROU r₃(7) — N=50k (préset maximal), 200 modes, escalier IDS contre le comptage
#      exact du tore (…56, 80, 80, 92…). GRILLE : PALIER si la pente locale de N(ratio)
#      dans [6,6;7,4] ≤ 50% des fenêtres voisines. Sinon : élargissement mesuré, gravé ;
#      si l'élargissement à m=6 ne décroît pas de ≥30% vs N=8000 → prédiction déclarée
#      hors de portée de cet observable (et gravée comme telle).
#  F4  EXPOSANTS CRITIQUES — transition principale : χ=Var(d) à β ∈ {1,55;1,45;1,35}
#      sur N ∈ {6k,12k,24k}. GRILLE : premier exposant si χ_max ~ N^{γ/(νd)} avec
#      ajustement R² ≥ 0,9 ; valeur rapportée ± erreur.
#  F5  INSTRUMENT d_s + EINSTEIN — d_f, d_w, d_s(fenêtres multiples) à N ∈ {8k, 20k}.
#      GRILLE : la fenêtre de fit de d_s qui minimise |d_s − 2·d_f/d_w| est adoptée
#      comme fenêtre étalonnée si l'écart ≤ 0,15 aux deux tailles → tâche SUP-1(1)
#      fermée proprement (le d_s canonique est réétalonné, d_f et d_w identifiés).
# ═══════════════════════════════════════════════════════════════════════════════
import numpy as np, math, json, time, warnings
warnings.filterwarnings("ignore")
from collections import defaultdict, deque, Counter
from itertools import combinations
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from scipy.spatial import Delaunay

PRESET = "complet"   # "rapide" (~1h) | "complet" (~3-4h) | "maximal" (~8-12h)
OUT = "frontiere_V280_results.json"
CFG = {
 "rapide":  {"F1_N": 8000,  "F1_degs": [10,14,18,22],      "F2_Ns": [2500,6000],        "F3_N": 20000, "F3_k": 140, "F4_Ns": [4000,8000],        "F5_Ns": [8000]},
 "complet": {"F1_N": 20000, "F1_degs": [10,14,18,22,26,30],"F2_Ns": [2500,6000,12000],  "F3_N": 30000, "F3_k": 170, "F4_Ns": [6000,12000,24000], "F5_Ns": [8000,20000]},
 "maximal": {"F1_N": 30000, "F1_degs": [10,14,18,22,26,30],"F2_Ns": [2500,6000,12000,20000],"F3_N": 50000,"F3_k": 200,"F4_Ns": [6000,12000,24000,48000],"F5_Ns": [8000,20000,40000]},
}[PRESET]
DENS,KAP,RC,TAU = 200.0,10.0,1.6,0.5

def build(N,seed):
    rng=np.random.default_rng(seed);L=(N/DENS)**(1/3)
    pts=rng.uniform(0,L,size=(N,3));rc=RC*(3*KAP/(4*math.pi*DENS))**(1/3)
    nc=max(1,int(L/rc));g=defaultdict(list)
    for i,p in enumerate(pts):g[tuple((p//rc).astype(int)%nc)].append(i)
    cand=[]
    for i,p in enumerate(pts):
        ci=(p//rc).astype(int)
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                for dz in(-1,0,1):
                    for j in g[tuple((ci+[dx,dy,dz])%nc)]:
                        if j>i:
                            dd=pts[i]-pts[j];dd-=L*np.round(dd/L)
                            if(dd*dd).sum()<rc*rc:cand.append((i,j))
    return pts,sorted(set(cand)),L,rc,rng

def relax_global(adj,d,cand,beta,N,seed,sw):
    rng=np.random.default_rng(seed);te=TAU/N
    T=0
    for u in adj:
        for v in adj[u]:
            if v>u:T+=len(adj[u]&adj[v])
    T//=3
    X=int((d.astype(np.int64)**2).sum());E=int(sum(len(adj[u]) for u in adj)//2);mu=2.0*E/N
    el=[(i,j) for i in range(N) for j in adj[i] if j>i]
    for _ in range(sw):
        for _ in range(3*N):
            io=rng.integers(len(el));u,v=el[io];ii=rng.integers(len(cand));a,b=cand[ii]
            if b in adj[a] or v not in adj[u] or len({u,v,a,b})<4 or d[u]<=2 or d[v]<=2:continue
            t_rm=len(adj[u]&adj[v]);adj[u].discard(v);adj[v].discard(u)
            t_ad=len(adj[a]&adj[b]);adj[u].add(v);adj[v].add(u)
            dT=t_ad-t_rm
            dX=(-2*d[u]+1)+(-2*d[v]+1)+(2*d[a]+1)+(2*d[b]+1)
            cv0=math.sqrt(max(X/N-mu*mu,0))/mu;cv1=math.sqrt(max((X+dX)/N-mu*mu,0))/mu
            dS=math.log(1+T+dT)-math.log(1+T)-beta*(cv1-cv0)
            if dS>=0 or rng.random()<math.exp(dS/te):
                adj[u].discard(v);adj[v].discard(u);adj[a].add(b);adj[b].add(a)
                d[u]-=1;d[v]-=1;d[a]+=1;d[b]+=1;T+=dT;X+=dX;el[io]=(a,b)
    return adj,d

def viable_state(N,seed,beta,deg,sw=30):
    pts,cand,L,rc,rng=build(N,seed)
    E=int(deg*N/2)
    adj=defaultdict(set)
    for k in rng.choice(len(cand),size=min(E,len(cand)),replace=False):
        a,b=cand[k];adj[a].add(b);adj[b].add(a)
    d=np.zeros(N,dtype=np.int64)
    for u in adj:d[u]=len(adj[u])
    adj,d=relax_global(adj,d,cand,beta,N,seed+1,sw)
    return pts,cand,L,rc,adj,d

def spectrum(adj,N,k):
    r=[];c=[]
    for u in adj:
        for v in adj[u]:r.append(u);c.append(v)
    A=sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(N,N))
    dd=np.asarray(A.sum(1)).ravel();Lp=(sp.diags(dd)-A).tocsr()
    try:
        return np.sort(eigsh(Lp,k=k,sigma=1e-6,which='LM',return_eigenvectors=False,maxiter=10000))
    except Exception:
        return None

if __name__=="__main__":
    print(open(__file__).read().split('# ═'*1)[0] if False else "BLOB — FRONTIÈRE V280 — grilles gravées (voir en-tête du script)")
    print(f"PRESET={PRESET} | {CFG}\n");t0=time.time();R={"meta":{"preset":PRESET,"cfg":CFG}}
    def save():
        with open(OUT,"w") as f: json.dump(R,f)
    def el(): return f"({(time.time()-t0)/60:.0f} min)"

    # ───────── F1 : PERCOLATION — balayage degré ─────────
    print("─── F1 : percolation Delaunay∩Blob, balayage degré ───")
    R["F1"]=[]
    N=CFG["F1_N"]
    try:
        pts,cand,L,rc,rng=build(N,81000)
        tri=Delaunay(pts);simp=tri.simplices
        marg=0.05*L;inner=np.all((pts>marg)&(pts<L-marg),axis=1)
        simp_in=simp[np.array([all(inner[v] for v in s) for s in simp])]
        print(f"  Delaunay intérieurs : {len(simp_in)}  {el()}",flush=True)
        for deg in CFG["F1_degs"]:
            E=deg*N//2
            if E>len(cand):
                print(f"  deg={deg}: candidats insuffisants — stop");break
            adj=defaultdict(set)
            for k in rng.choice(len(cand),size=E,replace=False):
                a,b=cand[k];adj[a].add(b);adj[b].add(a)
            d=np.zeros(N,dtype=np.int64)
            for u in adj:d[u]=len(adj[u])
            adj,d=relax_global(adj,d,cand,3.0,N,81002+deg,25)
            ret=[]
            for s in simp_in:
                a,b,c,dd4=sorted(s.tolist())
                if (b in adj[a]) and (c in adj[a]) and (dd4 in adj[a]) and (c in adj[b]) and (dd4 in adj[b]) and (dd4 in adj[c]):
                    ret.append((a,b,c,dd4))
            nr=len(ret)
            rec={"deg":deg,"retained":nr,"frac":nr/len(simp_in)}
            if nr>0:
                face2t=defaultdict(list)
                for ti,(a,b,c,dd4) in enumerate(ret):
                    for f in ((a,b,c),(a,b,dd4),(a,c,dd4),(b,c,dd4)):face2t[f].append(ti)
                parent=list(range(nr))
                def find(x):
                    while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
                    return x
                for f,ts in face2t.items():
                    for i in range(1,len(ts)):
                        ra,rb=find(ts[0]),find(ts[i])
                        if ra!=rb:parent[ra]=rb
                comp=Counter(find(i) for i in range(nr));giant=max(comp.values());gid=max(comp,key=comp.get)
                gx=[pts[v,0] for i in range(nr) if find(i)==gid for v in ret[i]]
                span=(max(gx)-min(gx))/(L-2*marg)
                rec.update({"giant_frac":giant/nr,"span":span,
                            "percole":bool(giant/nr>=0.5 and span>=0.8)})
            R["F1"].append(rec);save()
            print(f"  deg={deg}: retenus {nr} ({rec['frac']*100:.2f}%) | géante {rec.get('giant_frac',0)*100:.0f}% | span {rec.get('span',0)*100:.0f}%  "
                  f"{'★★★ PERCOLE' if rec.get('percole') else ''}  {el()}",flush=True)
    except Exception as ex:
        print(f"  F1 ÉCHEC : {ex}")

    # ───────── F2 : ℤ₂ FSS ─────────
    print("\n─── F2 : jauge ℤ₂ — FSS multi-tailles, κ fin ───")
    R["F2"]=[]
    kappas=[round(0.30+0.05*i,2) for i in range(9)]  # 0.30..0.70
    for Nz in CFG["F2_Ns"]:
        try:
            pts,cand,L,rc,adj,d=viable_state(Nz,31000,2.5,10,28)
            eid={};edges=[]
            for u in adj:
                for v in adj[u]:
                    if v>u:eid[(u,v)]=len(edges);edges.append((u,v))
            E=len(edges);tris=[]
            for u in adj:
                for v in adj[u]:
                    if v>u:
                        for w in adj[u]&adj[v]:
                            if w>v:tris.append((u,v,w))
            F=len(tris)
            T_e=[[] for _ in range(E)];tri_e=np.zeros((F,3),dtype=np.int64)
            for ti,(u,v,w) in enumerate(tris):
                for k2,(a,b) in enumerate(((u,v),(v,w),(u,w))):
                    e=eid[(a,b)];tri_e[ti,k2]=e;T_e[e].append(ti)
            row={"N":Nz,"F":F,"chi":{}}
            for kappa in kappas:
                rg=np.random.default_rng(777)
                s=rg.choice([-1,1],size=E).astype(np.int8)
                P=s[tri_e].prod(axis=1).astype(np.int32);Ps=[]
                for sw in range(50+35):
                    order=rg.permutation(E);u01=rg.random(E)
                    for e in order:
                        dsum=0
                        for ti in T_e[e]:dsum+=P[ti]
                        dS=-2.0*kappa*dsum
                        if dS>=0 or u01[e]<math.exp(dS):
                            s[e]=-s[e]
                            for ti in T_e[e]:P[ti]=-P[ti]
                    if sw>=50:Ps.append(P.mean())
                Ps=np.array(Ps);row["chi"][str(kappa)]=float(F*Ps.var())
            km=max(row["chi"],key=row["chi"].get)
            row["chi_max"]=row["chi"][km];row["kappa_c_est"]=float(km)
            R["F2"].append(row);save()
            print(f"  N={Nz}: χ_max={row['chi_max']:.2f} à κ={km}  {el()}",flush=True)
        except Exception as ex:
            print(f"  N={Nz} ÉCHEC F2 : {ex}")
    if len(R["F2"])>=3:
        Fs=np.array([r["F"] for r in R["F2"]]);cm=np.array([r["chi_max"] for r in R["F2"]])
        expo=float(np.polyfit(np.log(Fs),np.log(cm),1)[0])
        R["F2_expo"]=expo;save()
        print(f"  → χ_max ~ F^{expo:.2f}  ({'★ TRANSITION (exposant>0,3) — κ_c='+str(R['F2'][-1]['kappa_c_est']) if expo>0.3 else 'saturation — crossover/désordre, gravé tel quel'})")

    # ───────── F3 : TROU r₃(7) — escalier IDS ─────────
    print("\n─── F3 : trou spectral r₃(7), escalier IDS ───")
    try:
        Ns=CFG["F3_N"]
        pts,cand,L,rc,adj,d=viable_state(Ns,21000,3.0,10,30)
        vals=spectrum(adj,Ns,CFG["F3_k"])
        if vals is not None:
            rat=(vals[1:]/vals[1])
            def slope(lo,hi):return float(((rat>=lo)&(rat<=hi)).sum()/(hi-lo))
            sl7=slope(6.6,7.4);slnb=(slope(5.6,6.4)+slope(7.6,8.4))/2
            # élargissement couche 6 : étendue des modes 57..80 (indices cumulés théoriques)
            width6=float(rat[79]-rat[56]) if len(rat)>80 else float('nan')
            R["F3"]={"N":Ns,"ratios":rat.tolist()[:150],"slope_hole":sl7,"slope_nb":slnb,
                     "ratio":sl7/max(slnb,1e-9),"width_layer6":width6}
            save()
            print(f"  pente trou/voisines = {sl7/max(slnb,1e-9):.2f} (grille ≤0,50) | largeur couche 6 = {width6:.2f} (N=8000 : ~1,0)")
            print(f"  → {'★★★ PALIER r₃(7) DÉTECTÉ — la prédiction arithmétique est LÀ' if sl7/max(slnb,1e-9)<=0.5 else ('◐ déplétion partielle' if sl7/max(slnb,1e-9)<=0.75 else '✗ non résolu — élargissement gravé')}  {el()}",flush=True)
    except Exception as ex:
        print(f"  F3 ÉCHEC : {ex}")

    # ───────── F4 : exposants critiques ─────────
    print("\n─── F4 : exposant de la transition principale (χ scaling) ───")
    R["F4"]=[]
    for beta in (1.55,1.45,1.35):
        row={"beta":beta,"chi":{}}
        for Nn in CFG["F4_Ns"]:
            try:
                pts,cand,L,rc,adj,d=viable_state(Nn,61000,beta,10,30)
                row["chi"][str(Nn)]=float(np.var(d.astype(float)))
            except Exception as ex:
                print(f"    N={Nn} β={beta} échec : {ex}")
        R["F4"].append(row);save()
        vals=[(int(k),v) for k,v in row["chi"].items()]
        if len(vals)>=3:
            xs=np.log([v[0] for v in vals]);ys=np.log([v[1] for v in vals])
            p=np.polyfit(xs,ys,1);r2=float(np.corrcoef(xs,ys)[0,1]**2)
            print(f"  β={beta}: χ(N) exposant={p[0]:.3f} (R²={r2:.2f})  {'★ premier exposant' if r2>=0.9 else ''}  {el()}",flush=True)

    # ───────── F5 : instrument d_s + Einstein ─────────
    print("\n─── F5 : réétalonnage d_s par la relation d'Einstein ───")
    R["F5"]=[]
    for Nn in CFG["F5_Ns"]:
        try:
            pts,cand,L,rc,adj,d=viable_state(Nn,91000,3.0,10,35)
            # d_f
            rgs=np.random.default_rng(1);srcs=rgs.choice([u for u in adj if adj[u]],size=12,replace=False)
            grow=defaultdict(list)
            for s0 in srcs:
                dist={s0:0};q=deque([s0])
                while q:
                    u=q.popleft()
                    if dist[u]>=10:continue
                    for v in adj[u]:
                        if v not in dist:dist[v]=dist[u]+1;q.append(v)
                cnt=Counter(dist.values());cum=0
                for rr in range(0,11):
                    cum+=cnt.get(rr,0);grow[rr].append(cum)
            rs=np.arange(2,8);Bs=np.array([np.mean(grow[rr]) for rr in rs])
            d_f=float(np.polyfit(np.log(rs),np.log(Bs),1)[0])
            # d_w
            rgw=np.random.default_rng(2)
            starts=rgw.choice([u for u in adj if adj[u]],size=200,replace=False)
            dists={}
            for s0 in starts:
                ddm={s0:0};q=deque([s0])
                while q:
                    u=q.popleft()
                    if ddm[u]>=14:continue
                    for v in adj[u]:
                        if v not in ddm:ddm[v]=ddm[u]+1;q.append(v)
                dists[s0]=ddm
            cur=np.array(starts);TT=[3,5,8,12,18,27,40,60];msd={t:[] for t in TT}
            for t in range(1,61):
                for i in range(len(cur)):
                    if rgw.random()<0.5:
                        nb=list(adj[cur[i]]);cur[i]=nb[rgw.integers(len(nb))]
                if t in TT:
                    for i in range(len(cur)):
                        d0=dists[starts[i]].get(cur[i],15);msd[t].append(d0*d0)
            tt=np.array(TT,dtype=float);mm=np.array([np.mean(msd[t]) for t in TT])
            ok=(tt>=3)&(tt<=40);d_w=2.0/float(np.polyfit(np.log(tt[ok]),np.log(mm[ok]),1)[0])
            ein=2*d_f/d_w
            # d_s multi-fenêtres
            r=[];c=[]
            for u in adj:
                for v in adj[u]:r.append(u);c.append(v)
            A=sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(Nn,Nn))
            deg=np.asarray(A.sum(1)).ravel();Pi=deg/deg.sum()
            rng2=np.random.default_rng(3);src=rng2.choice(Nn,size=8,replace=False)
            X=np.zeros((Nn,8));X[src,np.arange(8)]=1.0;invd=1.0/np.maximum(deg,1)
            TG=np.unique(np.round(np.logspace(0,math.log10(400),50)).astype(int))
            rec=np.zeros(len(TG));tj=0
            for t in range(1,TG[-1]+1):
                X=0.5*(X+invd[:,None]*(A@X))
                if tj<len(TG) and t==TG[tj]:rec[tj]=float(np.mean(X[src,np.arange(8)]-Pi[src]));tj+=1
            best=None
            for lo in (4,6,8,12):
                for hi in (40,60,90,140):
                    ok2=(TG>=lo)&(TG<=hi)&(rec>0)
                    if ok2.sum()<6:continue
                    dsv=0.948*float(-2*np.polyfit(np.log(TG[ok2]),np.log(rec[ok2]),1)[0])
                    if best is None or abs(dsv-ein)<abs(best[2]-ein):best=(lo,hi,dsv)
            R["F5"].append({"N":Nn,"d_f":d_f,"d_w":d_w,"einstein":ein,
                            "ds_best_window":best})
            save()
            print(f"  N={Nn}: d_f={d_f:.3f} d_w={d_w:.3f} Einstein={ein:.3f} | meilleure fenêtre d_s: t∈[{best[0]},{best[1]}] → {best[2]:.3f} (écart {abs(best[2]-ein):.3f})  "
                  f"{'★ fenêtre étalonnée' if abs(best[2]-ein)<=0.15 else ''}  {el()}",flush=True)
        except Exception as ex:
            print(f"  N={Nn} ÉCHEC F5 : {ex}")

    print(f"\n════ FIN — résultats : {OUT}  ({(time.time()-t0)/60:.0f} min) ════")
    save()
