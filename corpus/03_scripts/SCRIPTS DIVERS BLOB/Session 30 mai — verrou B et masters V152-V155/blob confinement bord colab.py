# =====================================================================================
# BLOB PRINCIPLE — P0-c : CONFINEMENT PAR ÉNERGIE DE BORD (formulation propre)
# Script autonome Colab. À lancer APRÈS blob_unification_spatiale_colab.py.
#
# LEÇON DE LA PARTIE XLIX : remplacer log par une puissance casse l'échelle de Metropolis
# (artefact). ICI on garde log(1+n_tri) INTACT et on ajoute SEULEMENT une énergie de bord :
#   S = log(1+n_tri) - beta*D - g * log(1 + nb_faces_exposees)
# Le terme de bord est en unité logarithmique => même échelle que le terme principal,
# donc tau_eff INCHANGÉ, pas d'artefact d'échelle. (faces exposées = q(f)=2-n_tet(f)=1)
#
# Mécanisme attendu : pénaliser les faces exposées favorise les assemblages FERMÉS
# (faces internes) = confinement. Test local (N~577) : ratio survie assemblé/isolé ~4,
# isolés fragilisés (quark libre instable), assemblés stables (hadron). À CONFIRMER ici
# au scaling + multi-seed avant inscription au master.
#
# Cibles : ratio = survie(K4 assemblé)/survie(K4 isolé). Mur initial (sans bord) = 1,13.
# Fidèle au moteur (BETA=0.30, TAU=0.50, kappa=6.6, mitose continue, cycle).
# Balaye g ∈ {0, 0.5, 1.0, 2.0}. Change SEED en tête pour multi-seed.
# JSON écrit à chaque palier : 1000, 2500, 5000, 10000 (et 15000/25000 si le temps suit).
# =====================================================================================
import numpy as np, math, time, json
from collections import deque
from scipy.spatial import KDTree

BETA, TAU, KAPPA = 0.30, 0.50, 6.6

def rips_radius(N, kappa, mult=1.0): return mult * (kappa / ((N - 1) * (4/3) * math.pi)) ** (1/3)
def E0_target(N, kappa): return max(N - 1, int(N * kappa / 2))
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
    return pts, adj, pool, E0
def count_triangles(adj, N):
    n=0
    for i in range(N):
        for j in adj[i]:
            if j>i: n+=len(adj[i]&adj[j]&set(k for k in adj[j] if k>j))
    return n
def find_all_K4(adj, N):
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
def still_connected(adj, u, v, N):
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
def faces_exposees_count(adj, K4):
    fc={}
    for q in K4:
        for f in [(q[0],q[1],q[2]),(q[0],q[1],q[3]),(q[0],q[2],q[3]),(q[1],q[2],q[3])]:
            fk=tuple(sorted(f)); fc[fk]=fc.get(fk,0)+1
    return sum(1 for c in fc.values() if c==1)

class Blob:
    def __init__(self, N0=120, seed=1, gbord=0.0):
        self.beta, self.tau, self.kappa = BETA, TAU, KAPPA
        self.gbord = gbord
        pts,a0,pool,E0 = build_initial(N0, seed, KAPPA)
        self.pts=[np.array(p) for p in pts]; self.adj=[set(x) for x in a0]; self.N=N0
        self.rng=np.random.default_rng(seed*13); self.sweep=0; self.survie={}
    def Sglob(self, K4=None):
        nt=count_triangles(self.adj,self.N)
        d=np.array([len(self.adj[i]) for i in range(self.N)],float)
        D=d.std()/d.mean() if d.mean()>0 else 0
        S=math.log(1+nt)-self.beta*D
        if self.gbord>0:
            if K4 is None: K4=find_all_K4(self.adj,self.N)
            S-=self.gbord*math.log(1+faces_exposees_count(self.adj,K4))
        return S
    def vg(self, parent, newp, r=0.32):
        cand=[parent]+list(self.adj[parent]); return [i for i in cand if np.linalg.norm(self.pts[i]-newp)<r]
    def step(self, growth=0.12):
        self.sweep+=1; S=self.Sglob(); tau_eff=self.tau/max(self.N,1)
        for _ in range(self.N):
            v=int(self.rng.integers(self.N))
            if not self.adj[v]: continue
            if self.rng.random()<0.5:
                bb=int(self.rng.integers(self.N))
                if bb==v or bb in self.adj[v] or np.linalg.norm(self.pts[v]-self.pts[bb])>0.45: continue
                self.adj[v].add(bb); self.adj[bb].add(v); S2=self.Sglob(); d=S2-S
                if d>=0 or self.rng.random()<math.exp(min(d/tau_eff,30)): S=S2
                else: self.adj[v].discard(bb); self.adj[bb].discard(v)
            else:
                w=int(list(self.adj[v])[int(self.rng.integers(len(self.adj[v])))])
                if len(self.adj[v])<=2 or len(self.adj[w])<=2:
                    if not still_connected(self.adj,v,w,self.N): continue
                self.adj[v].discard(w); self.adj[w].discard(v); S2=self.Sglob(); d=S2-S
                if d>=0 or self.rng.random()<math.exp(min(d/tau_eff,30)): S=S2
                else: self.adj[v].add(w); self.adj[w].add(v)
        n_mit=max(2,int(self.N*growth))
        for _ in range(n_mit):
            parent=int(self.rng.integers(self.N)); newp=self.pts[parent]+self.rng.normal(0,0.10,3)
            vois=self.vg(parent,newp); self.pts.append(newp); self.adj.append(set()); nid=self.N; self.N+=1
            if len(vois)<2: self.adj[nid].add(parent); self.adj[parent].add(nid)
            else:
                knn=sorted(vois,key=lambda i:np.linalg.norm(self.pts[i]-newp))[:int(self.kappa)]
                for w in knn: self.adj[nid].add(w); self.adj[w].add(nid)
        K4=find_all_K4(self.adj,self.N); cur=set(key(q) for q in K4)
        for k in cur: self.survie[k]=self.survie.get(k,0)+1
        S=self.Sglob(K4)
        for q in K4:
            k=key(q); age=self.survie.get(k,1); p_eff=0.236*math.exp(-age/8)
            if self.rng.random()<p_eff:
                i,j=self.rng.choice(4,2,replace=False); u,w=q[int(i)],q[int(j)]
                if w in self.adj[u] and len(self.adj[u])>2 and len(self.adj[w])>2 and still_connected(self.adj,u,w,self.N):
                    self.adj[u].discard(w); self.adj[w].discard(u); S2=self.Sglob(); d=S2-S
                    if d>=0 or self.rng.random()<math.exp(min(d/tau_eff,30)): S=S2
                    else: self.adj[u].add(w); self.adj[w].add(u)
        k4list=[set(q) for q in K4]; v2={}
        for i,q in enumerate(k4list):
            for vv in q: v2.setdefault(vv,[]).append(i)
        lie=[False]*len(K4)
        for vv,lst in v2.items():
            for a in range(len(lst)):
                for c in range(a+1,len(lst)):
                    if len(k4list[lst[a]]&k4list[lst[c]])>=3: lie[lst[a]]=True; lie[lst[c]]=True
        for k in list(self.survie):
            if k not in cur: del self.survie[k]
        self._K4=K4; self._lie=lie
    def ratio(self):
        K4=self._K4; lie=self._lie
        si=[self.survie[key(K4[i])] for i in range(len(K4)) if not lie[i] and key(K4[i]) in self.survie]
        sl=[self.survie[key(K4[i])] for i in range(len(K4)) if lie[i] and key(K4[i]) in self.survie]
        r=(np.mean(sl)/max(np.mean(si),0.01)) if si and sl else 0
        return float(r), (float(np.mean(si)) if si else 0), (float(np.mean(sl)) if sl else 0), len(si), len(sl)

# ===================================== RUN =====================================
PALIERS=[1000,2500,5000,10000,15000,25000]
G_VALUES=[0.0,0.5,1.0,2.0]   # balayage du couplage de bord
SEED=1                        # change pour multi-seed
T0=time.time()
print(f"P0-c CONFINEMENT PAR BORD — seed={SEED}, g={G_VALUES}, paliers={PALIERS}")
all_results={}
for g in G_VALUES:
    results=[]; bl=Blob(N0=120, seed=SEED, gbord=g); pi=0
    print(f"\n--- g_bord = {g} ---")
    print(f"  {'N':>7} {'nK4':>6} {'s_iso':>7} {'s_lie':>7} {'RATIO':>7} {'t(s)':>7}")
    while bl.N < PALIERS[-1] and time.time()-T0 < 16000:
        bl.step(0.12)
        if pi<len(PALIERS) and bl.N>=PALIERS[pi]:
            r,mi,ml,ni,nl=bl.ratio()
            snap={"g":g,"N":int(bl.N),"seed":SEED,"n_K4":len(bl._K4),
                  "survie_iso":mi,"survie_lie":ml,"ratio":r,"n_iso":ni,"n_lie":nl,
                  "sweep":bl.sweep,"elapsed_s":round(time.time()-T0,1)}
            results.append(snap)
            print(f"  {bl.N:>7} {len(bl._K4):>6} {mi:>7.2f} {ml:>7.2f} {r:>7.2f} {snap['elapsed_s']:>7.1f}")
            all_results[str(g)]=results
            with open(f"blob_confinement_bord_seed{SEED}.json","w") as f:
                json.dump(all_results,f,indent=2)
            pi+=1
            while pi<len(PALIERS) and PALIERS[pi]<=bl.N: pi+=1
print(f"\nTermine. JSON : blob_confinement_bord_seed{SEED}.json")
print("\n=== VERDICT ===")
print("Si le ratio (g>0) reste STABLE >2 (idealement ~4) a tous les paliers et > ratio(g=0) :")
print("  => confinement propre confirme au scaling (log intact, pas d'artefact). Inscriptible.")
print("Si le ratio s'effondre vers 1 a grand N, ou explose erratiquement : non confirme.")
print("Comparer aussi les seeds (relancer avec SEED=2,3).")
