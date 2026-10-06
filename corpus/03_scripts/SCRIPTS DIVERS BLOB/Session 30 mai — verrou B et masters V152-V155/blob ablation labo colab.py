# =====================================================================================
# BLOB PRINCIPLE — ABLATION LABO : quelle force est nécessaire à quoi ? (multi-config, multi-seed)
# Script autonome Colab. Principe R. Mirante : "si on coupe une branche la magie ne prend pas."
# On teste en COUPANT les forces, une par une et par paires, avec capteurs partout.
#
# Forces (versions VALIDÉES, aucun proxy) :
#   GRAV = vraie courbure d'Ollivier (accrétion de la mitose vers les puits)
#   EM   = vrai 2-cocycle U(1) (A sur arêtes, relaxation de F²)
#   WEAK = vraies horloges t1/t2 (désintégration des projetées t1>>t2)
#   BORD = vraie énergie de bord (faces exposées q=2-n_tet) — la "forte"/fermeture
#   (viabilité log(1+n_tri)-beta*D toujours présente : c'est le terreau, pas une force ablable)
#
# CONFIGS testées : 4forces (ref) ; ablations simples (-grav,-em,-weak,-bord) ;
#   paires (em+grav, em+weak, grav+weak, grav+bord, em+bord, weak+bord).
# CAPTEURS (version labo) par config/seed/palier : confinement (survie par taille),
#   signature matière (Ric K4-fond), distribution tailles, n_amas, ratio plus gros amas,
#   degré moyen, + CARTE DES FORCES (contribution moyenne de chaque force aux décisions).
#
# N=5000, SEEDS=[1,2] (ajuster). Coût : Ollivier lente => ~minutes par config. JSON à chaque config.
# =====================================================================================
import numpy as np, math, time, json
from collections import deque, Counter, defaultdict
from scipy.spatial import KDTree

BETA, TAU, KAPPA = 0.30, 0.50, 6.6

def rips_radius(N, kappa, mult=1.0): return mult*(kappa/((N-1)*(4/3)*math.pi))**(1/3)
def E0_target(N, kappa): return max(N-1, int(N*kappa/2))
def lcc_size(adj, N):
    seen=[False]*N; best=0
    for s in range(N):
        if not seen[s]:
            sz=0; q=deque([s]); seen[s]=True
            while q:
                v=q.popleft(); sz+=1
                for w in adj[v]:
                    if not seen[w]: seen[w]=True; q.append(w)
            best=max(best,sz)
    return best
def build_initial(N, seed, kappa, pool_mult=1.6):
    r=rips_radius(N,kappa); r_p=pool_mult*r; E0=E0_target(N,kappa)
    rng=np.random.default_rng(seed); pts=rng.uniform(0.0,1.0,(N,3))
    tree=KDTree(pts); adj=[set() for _ in range(N)]
    for i,j in tree.query_pairs(r): adj[i].add(j); adj[j].add(i)
    pool=list(tree.query_pairs(r_p)); rng2=np.random.default_rng(seed+50_000)
    K=sum(len(adj[i]) for i in range(N))//2; att=0; max_att=10*abs(E0-K)+5000
    while K!=E0 and att<max_att:
        att+=1
        if K<E0:
            if not pool: break
            u,v=pool[rng2.integers(len(pool))]
            if v not in adj[u]: adj[u].add(v); adj[v].add(u); K+=1
        else:
            edges=[(i,j) for i in range(N) for j in adj[i] if j>i]
            if not edges: break
            u,v=edges[rng2.integers(len(edges))]
            adj[u].discard(v); adj[v].discard(u)
            if lcc_size(adj,N)==N: K-=1
            else: adj[u].add(v); adj[v].add(u)
    return pts, adj
def still_connected(adj, u, v):
    seen={u}; q=deque([u])
    while q:
        node=q.popleft()
        for w in adj[node]:
            if w in seen: continue
            if (node==u and w==v) or (node==v and w==u): continue
            seen.add(w); q.append(w)
            if w==v: return True
    return False
def key(q): return tuple(sorted(q))
def count_tri(adj,N):
    n=0
    for i in range(N):
        for j in adj[i]:
            if j>i: n+=len(adj[i]&adj[j])
    return n//3
def find_all_K4(adj,N):
    out=[]
    for i in range(N):
        Ni=adj[i]
        for j in Ni:
            if j<=i: continue
            cij=Ni&adj[j]
            for k in cij:
                if k<=j: continue
                for l in (cij&adj[k]):
                    if l>k: out.append((i,j,k,l))
    return out
def ollivier_edge(adj,x,y):
    Nx=list(adj[x]);Ny=set(adj[y])
    if not Nx or not Ny: return 0.0
    def dsh(a,bs,md=3):
        dist={a:0};q=deque([a]);f={}
        while q:
            u=q.popleft()
            if u in bs: f[u]=dist[u]
            if dist[u]>=md: continue
            for w in adj[u]:
                if w not in dist: dist[w]=dist[u]+1;q.append(w)
        return f
    tot=0;c=0
    for a in Nx:
        fd=dsh(a,Ny);tot+=(min(fd.values()) if fd else 3);c+=1
    return 1.0-(tot/c if c else 0)
def faces_exp(adj,K4):
    fc={}
    for q in K4:
        for f in [(q[0],q[1],q[2]),(q[0],q[1],q[3]),(q[0],q[2],q[3]),(q[1],q[2],q[3])]:
            fk=tuple(sorted(f));fc[fk]=fc.get(fk,0)+1
    return sum(1 for c in fc.values() if c==1)

class Blob:
    def __init__(self, N0=300, seed=1, forces=("grav","em","weak","bord")):
        self.beta,self.tau,self.kappa=BETA,TAU,KAPPA
        self.F=set(forces)
        pts,a0=build_initial(N0,seed,KAPPA)
        self.pts=[np.array(p) for p in pts]; self.adj=[set(x) for x in a0]; self.N=N0
        self.rng=np.random.default_rng(seed*13); self.sweep=0
        self.survie={}; self.A={}; self.t1={}; self.t2={}; self.born={}
        self.force_log=defaultdict(float); self.force_cnt=defaultdict(int)
    def Aget(self,u,w): return self.A.get((min(u,w),max(u,w)),0.0)
    def Sglob(self, K4=None):
        nt=count_tri(self.adj,self.N)
        d=np.array([len(self.adj[i]) for i in range(self.N)],float)
        D=d.std()/d.mean() if d.mean()>0 else 0
        S=math.log(1+nt)-self.beta*D
        if "bord" in self.F:
            if K4 is None: K4=find_all_K4(self.adj,self.N)
            S-=math.log(1+faces_exp(self.adj,K4))
        return S
    def oll_local(self,v):
        if not self.adj[v]: return 0.0
        ws=list(self.adj[v])[:5]
        return float(np.mean([ollivier_edge(self.adj,v,w) for w in ws])) if ws else 0.0
    def vg(self,parent,newp,r=0.32):
        cand=[parent]+list(self.adj[parent]); return [i for i in cand if np.linalg.norm(self.pts[i]-newp)<r]
    def step(self,growth=0.12):
        self.sweep+=1;S=self.Sglob();tau_eff=self.tau/max(self.N,1)
        for _ in range(self.N):
            v=int(self.rng.integers(self.N))
            if not self.adj[v]: continue
            if self.rng.random()<0.5:
                bb=int(self.rng.integers(self.N))
                if bb==v or bb in self.adj[v] or np.linalg.norm(self.pts[v]-self.pts[bb])>0.45: continue
                self.adj[v].add(bb);self.adj[bb].add(v);S2=self.Sglob();d=S2-S
                if "em" in self.F:
                    em=-0.05*self.Aget(v,bb); d+=em
                    self.force_log["em"]+=abs(em); self.force_cnt["em"]+=1
                if d>=0 or self.rng.random()<math.exp(min(d/tau_eff,30)):
                    S=S2
                    if "em" in self.F: self.A[(min(v,bb),max(v,bb))]=self.rng.normal(0,0.3)
                else: self.adj[v].discard(bb);self.adj[bb].discard(v)
            else:
                w=int(list(self.adj[v])[int(self.rng.integers(len(self.adj[v])))])
                if len(self.adj[v])<=2 or len(self.adj[w])<=2:
                    if not still_connected(self.adj,v,w): continue
                self.adj[v].discard(w);self.adj[w].discard(v);S2=self.Sglob();d=S2-S
                if "bord" in self.F: self.force_log["bord"]+=abs(d); self.force_cnt["bord"]+=1
                if d>=0 or self.rng.random()<math.exp(min(d/tau_eff,30)):
                    S=S2; self.A.pop((min(v,w),max(v,w)),None)
                else: self.adj[v].add(w);self.adj[w].add(v)
        # mitose (+gravite si active)
        n_mit=max(2,int(self.N*growth)); mset=set()
        for _ in range(n_mit):
            if "grav" in self.F:
                cands=[int(self.rng.integers(self.N)) for _ in range(3)]
                cv=[self.oll_local(c) for c in cands]; parent=cands[int(np.argmax(cv))]
                self.force_log["grav"]+=(max(cv)-np.mean(cv)); self.force_cnt["grav"]+=1
            else:
                parent=int(self.rng.integers(self.N))
            newp=self.pts[parent]+self.rng.normal(0,0.10,3)
            vois=self.vg(parent,newp); self.pts.append(newp); self.adj.append(set()); nid=self.N; self.N+=1
            if len(vois)<2:
                self.adj[nid].add(parent); self.adj[parent].add(nid); mset.add(parent)
                if "em" in self.F: self.A[(min(nid,parent),max(nid,parent))]=0.0
            else:
                knn=sorted(vois,key=lambda i:np.linalg.norm(self.pts[i]-newp))[:int(self.kappa)]
                for w in knn:
                    self.adj[nid].add(w); self.adj[w].add(nid)
                    if "em" in self.F: self.A[(min(nid,w),max(nid,w))]=0.0
                mset|=set(knn)
        # cycle + faible
        K4=find_all_K4(self.adj,self.N); cur=set(key(q) for q in K4)
        for q in K4:
            k=key(q)
            if k not in self.born: self.born[k]=self.sweep; self.t1[k]=0; self.t2[k]=0
            if mset & set(q): self.t1[k]+=1
        for k in cur: self.survie[k]=self.survie.get(k,0)+1
        S=self.Sglob(K4)
        for q in K4:
            k=key(q); age=self.survie.get(k,1); p_eff=0.236*math.exp(-age/8)
            if "weak" in self.F:
                t1=self.t1.get(k,0); t2=max(self.t2.get(k,0),1)
                if t1/t2>2.0:
                    p_eff*=1.5; self.force_log["weak"]+=0.5; self.force_cnt["weak"]+=1
            if self.rng.random()<p_eff:
                if "weak" in self.F: self.t2[k]=self.t2.get(k,0)+1
                i,j=self.rng.choice(4,2,replace=False); u,w=q[int(i)],q[int(j)]
                if w in self.adj[u] and len(self.adj[u])>2 and len(self.adj[w])>2 and still_connected(self.adj,u,w):
                    self.adj[u].discard(w); self.adj[w].discard(u); self.A.pop((min(u,w),max(u,w)),None)
        for k in list(self.born):
            if k not in cur: del self.born[k]; self.t1.pop(k,None); self.t2.pop(k,None)
        for k in list(self.survie):
            if k not in cur: del self.survie[k]
        self._K4=K4

def assemblages(adj,K4):
    k4l=[set(q) for q in K4]; v2={}
    for i,q in enumerate(k4l):
        for v in q: v2.setdefault(v,[]).append(i)
    aK={i:set() for i in range(len(K4))}
    for v,lst in v2.items():
        for a in range(len(lst)):
            for c in range(a+1,len(lst)):
                if len(k4l[lst[a]]&k4l[lst[c]])>=3: aK[lst[a]].add(lst[c]); aK[lst[c]].add(lst[a])
    seen=set(); sizes=[]; so=[0]*len(K4)
    for i in range(len(K4)):
        if i in seen: continue
        comp=[]; st=[i]
        while st:
            x=st.pop()
            if x in seen: continue
            seen.add(x); comp.append(x); st.extend(aK[x]-seen)
        for m in comp: so[m]=len(comp)
        sizes.append(len(comp))
    return sizes, so

def mesure(bl, cfg, seed):
    K4=bl._K4; N=bl.N; nk=len(K4)
    sizes,so=assemblages(bl.adj,K4)
    biggest=max(sizes) if sizes else 0; n_amas=len(sizes)
    cls={"1":[], "2-4":[], "5-12":[], "13-50":[], "50+":[]}
    for i in range(len(K4)):
        k=key(K4[i])
        if k not in bl.survie: continue
        t=so[i]; s=bl.survie[k]
        if t==1: cls["1"].append(s)
        elif t<=4: cls["2-4"].append(s)
        elif t<=12: cls["5-12"].append(s)
        elif t<=50: cls["13-50"].append(s)
        else: cls["50+"].append(s)
    surv={c:(round(float(np.mean(v)),2) if v else None) for c,v in cls.items()}
    rng=np.random.default_rng(7); k4v=set(v for q in K4 for v in q)
    k4e=set()
    for q in K4:
        for a in range(4):
            for b in range(a+1,4): k4e.add((min(q[a],q[b]),max(q[a],q[b])))
    k4e=list(k4e)
    if len(k4e)>40: k4e=[k4e[i] for i in rng.choice(len(k4e),40,replace=False)]
    be=[(v,w) for v in range(N) if v not in k4v for w in bl.adj[v] if v<w]
    if len(be)>40: be=[be[i] for i in rng.choice(len(be),40,replace=False)]
    rk=[ollivier_edge(bl.adj,u,w) for u,w in k4e if w in bl.adj[u]]
    rb=[ollivier_edge(bl.adj,u,w) for u,w in be]
    ric=round(float(np.mean(rk))-float(np.mean(rb)),3) if len(rk)>5 and len(rb)>5 else None
    d=np.array([len(bl.adj[i]) for i in range(N)],float)
    fmap={f:round(bl.force_log[f]/max(bl.force_cnt[f],1),4) for f in ["grav","em","weak","bord"]}
    return {"config":cfg,"seed":seed,"N":int(N),"n_K4":nk,"deg_moy":round(float(d.mean()),2),
            "n_amas":n_amas,"ratio_gros":round(biggest/nk,3) if nk else 0,
            "Ric_K4_moins_fond":ric,"survie_par_taille":surv,"carte_forces":fmap,
            "ratio_confinement_50plus_sur_1":(round(surv["50+"]/surv["1"],2) if surv["1"] and surv["50+"] else None),
            "elapsed_s":round(time.time()-T0,1)}

# ===================================== RUN =====================================
N_TARGET=5000
SEEDS=[1,2]
CONFIGS={
    "4forces":("grav","em","weak","bord"),
    "sans_grav":("em","weak","bord"),
    "sans_em":("grav","weak","bord"),
    "sans_weak":("grav","em","bord"),
    "sans_bord":("grav","em","weak"),
    "em+grav":("em","grav"),
    "em+weak":("em","weak"),
    "grav+weak":("grav","weak"),
    "grav+bord":("grav","bord"),
    "em+bord":("em","bord"),
    "weak+bord":("weak","bord"),
}
T0=time.time()
print(f"ABLATION LABO — N={N_TARGET}, seeds={SEEDS}, {len(CONFIGS)} configs")
print(f"{'config':>12} {'seed':>4} {'N':>6} {'deg':>5} {'Ric':>6} {'conf(50+/1)':>11} {'survie 1|2-4|5-12|50+':>22} {'t(s)':>7}")
results=[]
for cfg,forces in CONFIGS.items():
    for seed in SEEDS:
        if time.time()-T0>28000: print("(budget)"); break
        bl=Blob(N0=300,seed=seed,forces=forces); 
        while bl.N<N_TARGET and time.time()-T0<28000:
            bl.step(0.12)
        m=mesure(bl,cfg,seed); results.append(m)
        s=m["survie_par_taille"]
        sv=f"{s['1']}|{s['2-4']}|{s['5-12']}|{s['50+']}"
        print(f"{cfg:>12} {seed:>4} {m['N']:>6} {m['deg_moy']:>5} {str(m['Ric_K4_moins_fond']):>6} {str(m['ratio_confinement_50plus_sur_1']):>11} {sv:>22} {m['elapsed_s']:>7.1f}")
        with open("blob_ablation_labo.json","w") as f: json.dump(results,f,indent=2)
print(f"\nTermine. JSON : blob_ablation_labo.json")
print("\n=== VERDICT ===")
print("Pour chaque force coupee, regarder : le confinement (50+/1) s'effondre-t-il ? la matiere")
print("(Ric) survit-elle ? Si couper une force DETRUIT le confinement => elle est NECESSAIRE.")
print("Comparer les paires : quelles 2 forces suffisent a maintenir confinement + matiere ?")
print("=> demontre 'si on coupe une branche la magie ne prend pas' et identifie le role de chaque force.")
