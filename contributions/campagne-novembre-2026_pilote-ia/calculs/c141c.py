# C-141c / PR-1 — SUBDIVISION DES ARETES PAR USURE. Protocole FIGE par ChatGPT (fil principal, 12 nov. 2026, 19 h 11 UTC,
#   sha256 38c46cde5ac3ebfbd0bfdf94e190562c3d72a44925512ad037595187a2c8933b), execute independamment par Claude.
# Regle : germe = tetraedre rempli (porteurs 0..3) ; file (0,1,2,3) ; une tentative retire le premier porteur v et le replace en fin ;
#   v piege (dans une cellule) : +1 d'usure sur chacun de ses liens ; lien admissible si usure >= soutien = max(1, nombre de triangles le contenant) ;
#   bras C (principal) : on n'evalue que les liens de v ; bras A (temoin) : tous les liens du graphe ; au plus UNE subdivision par tentative,
#   lien admissible lexicographiquement minimal ; subdivision de ab : C = N(a) & N(b) avant coupure ; ab supprime ; z lie a a, b et C ;
#   usure des nouveaux liens = 0 ; les autres gardent la leur ; z entre en fin de file.
# Temoins : T1 soutien = 1 partout ; T2 usure nulle ; T3 synchrone (ensemble maximal lexicographique de liens admissibles a etoiles fermees disjointes).
# PRECISIONS D'EXECUTION (Claude, declarees avant calcul) :
#  - "refus" = tentative d'un porteur piege (naissance libre bloquee), comptee avant toute subdivision ;
#  - "lien devenu admissible" = passage de usure < soutien a usure >= soutien lors d'un increment d'usure
#    (un soutien ne peut qu'augmenter : seuls les liens entre deux voisins communs gagnent un triangle) ;
#  - "ruptures differees" : bras C = liens admissibles de v non subdivises a la tentative, sommes ; bras A = taille du stock de liens admissibles en attente ;
#  - etoile fermee d'un lien ab (T3) = {a, b} U (N(a) & N(b)) ;
#  - controle exact des entourages : pour chaque porteur, l'entourage (complexe de cliques du graphe induit sur ses voisins) doit etre une surface
#    connexe dont chaque arete porte 1 ou 2 triangles et chaque sommet un cycle ou un chemin ; sphere si chi = 2 sans bord, disque si chi = 1 avec bord ;
#  - distance mediane = mediane des six distances entre fondateurs ; compteurs releves a chaque puissance de 2 du nombre de tentatives.
import sys, json, heapq, time
from collections import deque
from itertools import combinations
from statistics import median

def ek(a, b): return (a, b) if a < b else (b, a)

class Sim:
    def __init__(self, mode='C', support='topo', wear=True):
        self.N = {i: set(j for j in range(4) if j != i) for i in range(4)}
        self.w = {ek(a, b): 0 for a, b in combinations(range(4), 2)}
        self.queue = deque(range(4)); self.parent = {i: None for i in range(4)}; self.born = {i: 0 for i in range(4)}
        self.mode, self.support, self.wear = mode, support, wear
        self.n = self.births = self.refus = self.free = self.distant = self.became = self.deferred = 0
        self.heap = []; self.adm = set(); self.next = 4
    def sup(self, a, b):
        return 1 if self.support == 'one' else max(1, len(self.N[a] & self.N[b]))
    def trapped(self, v):
        Nv = self.N[v]
        for a in Nv:
            ca = Nv & self.N[a]
            for b in ca:
                if ca & self.N[b]: return True
        return False
    def subdivide(self, a, b, par):
        C = self.N[a] & self.N[b]; z = self.next; self.next += 1
        self.N[a].discard(b); self.N[b].discard(a); del self.w[ek(a, b)]
        self.N[z] = set()
        for x in (a, b, *C):
            self.N[z].add(x); self.N[x].add(z); self.w[ek(z, x)] = 0
        self.parent[z] = par; self.born[z] = self.n; self.queue.append(z); self.births += 1
        return z, C
    def attempt(self):
        v = self.queue.popleft(); self.queue.append(v); self.n += 1
        if not self.trapped(v):
            z = self.next; self.next += 1
            self.N[z] = {v}; self.N[v].add(z); self.w[ek(v, z)] = 0
            self.parent[z] = v; self.born[z] = self.n; self.queue.append(z); self.births += 1; self.free += 1
            return
        self.refus += 1; cand = []
        for x in sorted(self.N[v]):
            e = ek(v, x); s = self.sup(v, x); wb = self.w[e]
            if self.wear: self.w[e] = wb + 1
            if self.w[e] >= s:
                if wb < s: self.became += 1
                cand.append(e)
                if self.mode == 'A' and e not in self.adm:
                    self.adm.add(e); heapq.heappush(self.heap, e)
        if self.mode == 'C':
            if cand:
                e = min(cand); self.deferred += len(cand) - 1; self.subdivide(e[0], e[1], v)
        else:
            while self.heap and self.heap[0] not in self.adm: heapq.heappop(self.heap)
            if self.heap:
                e = heapq.heappop(self.heap); self.adm.discard(e); a, b = e
                if v in e: par = v
                else: par = a; self.distant += 1
                z, C = self.subdivide(a, b, par)
                for c in C:
                    for c2 in self.N[c] & C:
                        if c < c2 and (c, c2) in self.adm and self.w[(c, c2)] < self.sup(c, c2): self.adm.discard((c, c2))
            self.deferred = len(self.adm)

def link_kind(N, v):
    L = N[v]; adj = {a: N[a] & L for a in L}
    nV = len(L); nE = 0; nF3 = 0; bnd = 0
    for a in L:
        for b in adj[a]:
            if a < b:
                t = len(adj[a] & adj[b]); nE += 1; nF3 += t
                if t == 1: bnd += 1
                elif t != 2: return 'arete a %d triangles' % t
    if nF3 % 3: return 'incoherent'
    chi = nV - nE + nF3 // 3
    seen = set(); st = [next(iter(L))]
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x); st.extend(adj[x] - seen)
    if len(seen) != nV: return 'entourage non connexe'
    for a in L:
        sub = adj[a]; deg = [len(adj[b] & sub) for b in sub]
        ones = sum(1 for d in deg if d == 1)
        if any(d not in (1, 2) for d in deg) or ones not in (0, 2): return 'sommet singulier'
        s2 = set(); st = [next(iter(sub))]
        while st:
            x = st.pop()
            if x in s2: continue
            s2.add(x); st.extend((adj[x] & sub) - s2)
        if len(s2) != len(sub): return 'sommet singulier (non connexe)'
    if bnd == 0 and chi == 2: return 'sphere'
    if bnd > 0 and chi == 1: return 'disque'
    return 'autre (chi=%d, bord=%d)' % (chi, bnd)

def bfs(N, s):
    d = {s: 0}; q = deque([s])
    while q:
        x = q.popleft()
        for y in N[x]:
            if y not in d: d[y] = d[x] + 1; q.append(y)
    return d

def measure(N, born, links=True):
    V = len(N); E = sum(len(s) for s in N.values()) // 2
    F = 0; T4 = 0; inc = {0: 0, 1: 0, 2: 0, 3: 0}; k5 = 0
    for a in N:
        for b in N[a]:
            if a < b:
                ab = N[a] & N[b]
                for c in ab:
                    if b < c:
                        abc = ab & N[c]; F += 1; inc[min(len(abc), 3)] += 1
                        for d in abc:
                            if c < d:
                                T4 += 1
                                if abc & N[d]: k5 += 1
    comp = 0; seen = set()
    for s in N:
        if s not in seen:
            comp += 1; seen.update(bfs(N, s))
    deg = sorted(len(s) for s in N.values())
    top = sorted(N, key=lambda x: (-len(N[x]), x))[:10]
    dist = {}
    for i in range(4):
        d = bfs(N, i)
        for j in range(i + 1, 4): dist['%d-%d' % (i, j)] = d.get(j)
    out = dict(V=V, E=E, F=F, T=T4, chi=V - E + F - T4, composantes=comp, faces_0=inc[0], faces_1=inc[1], faces_2=inc[2], faces_3plus=inc[3],
               K5=k5 // 5 if k5 else 0, deg_max=deg[-1], deg_med=median(deg), deg_q95=deg[int(0.95 * (V - 1))],
               top10=[(x, len(N[x]), born[x]) for x in top], distances=dist, d_med=median(dist.values()),
               ratio=median(dist.values()) / V ** (1 / 3))
    if links:
        kinds = {}
        for v in N:
            k = link_kind(N, v); kinds[k] = kinds.get(k, 0) + 1
        out['entourages'] = kinds
    return out

CHECK = (256, 1024, 4096, 16384, 65536)

def run(mode='C', support='topo', wear=True, nmax=65536, links=True, verbose=True):
    S = Sim(mode, support, wear); res = dict(points={}, fenetres=[]); t0 = time.time(); prev = None; p2 = 1
    while S.n < nmax:
        S.attempt()
        if S.n == p2:
            cur = dict(n=S.n, V=len(S.N), became=S.became, deferred=S.deferred, distant=S.distant, births=S.births,
                       deg_max=max(len(s) for s in S.N.values()))
            if prev:
                dn = cur['n'] - prev['n']
                res['fenetres'].append(dict(de=prev['n'], a=cur['n'], r=(cur['V'] - prev['V']) / dn, devenues=cur['became'] - prev['became'],
                                            differees=(cur['deferred'] - prev['deferred']) if mode == 'C' else cur['deferred'],
                                            distantes=(cur['distant'] - prev['distant']) / max(1, cur['births'] - prev['births']),
                                            V=cur['V'], deg_max=cur['deg_max']))
            prev = cur; p2 *= 2
        if S.n in CHECK:
            m = measure(S.N, S.born, links); m.update(naissances=S.births, refus=S.refus, libres=S.free, distantes=S.distant,
                                                       non_pieges=sum(1 for v in S.N if not S.trapped(v)) if S.n <= 4096 or S.n == nmax else None)
            res['points'][S.n] = m
            if verbose:
                print(f"[{mode}/{support}/{'usure' if wear else 'sans usure'}] n={S.n} V={m['V']} E={m['E']} F={m['F']} T={m['T']} chi={m['chi']} comp={m['composantes']} "
                      f"faces(1,2,3+)={m['faces_1']},{m['faces_2']},{m['faces_3plus']} K5={m['K5']} deg max/med/q95={m['deg_max']}/{m['deg_med']}/{m['deg_q95']} "
                      f"dist={list(m['distances'].values())} ratio={m['ratio']:.3f} entourages={m.get('entourages')} ({time.time()-t0:.0f} s)", flush=True)
    res['sim'] = S
    return res

def run_sync(nmax=65536, links=True, verbose=True):
    N = {i: set(j for j in range(4) if j != i) for i in range(4)}; w = {ek(a, b): 0 for a, b in combinations(range(4), 2)}
    born = {i: 0 for i in range(4)}; nxt = 4; req = 0; gen = 0; res = dict(points={}, generations=[]); todo = list(CHECK); t0 = time.time()
    while req < nmax:
        gen += 1; carriers = list(N); req += len(carriers)
        for v in carriers:
            for x in N[v]: w[ek(v, x)] += 1
        adm = sorted(e for e in w if w[e] >= max(1, len(N[e[0]] & N[e[1]])))
        used = set(); chosen = []
        for a, b in adm:
            star = {a, b} | (N[a] & N[b])
            if not (star & used): chosen.append((a, b)); used |= star
        for a, b in chosen:
            C = N[a] & N[b]; z = nxt; nxt += 1
            N[a].discard(b); N[b].discard(a); del w[(a, b)]; N[z] = set()
            for x in (a, b, *C): N[z].add(x); N[x].add(z); w[ek(z, x)] = 0
            born[z] = gen
        res['generations'].append(dict(g=gen, demandes=req, V=len(N), admissibles=len(adm), subdivisees=len(chosen), deg_max=max(len(s) for s in N.values())))
        while todo and req >= todo[0]:
            m = measure(N, born, links); m.update(generation=gen, demandes=req); res['points'][todo.pop(0)] = m
            if verbose:
                print(f"[T3 synchrone] gen={gen} demandes={req} V={m['V']} T={m['T']} chi={m['chi']} comp={m['composantes']} faces(1,2,3+)={m['faces_1']},{m['faces_2']},{m['faces_3plus']} "
                      f"deg max/med/q95={m['deg_max']}/{m['deg_med']}/{m['deg_q95']} dist={list(m['distances'].values())} ratio={m['ratio']:.3f} entourages={m.get('entourages')} ({time.time()-t0:.0f} s)", flush=True)
    return res

if __name__ == '__main__':
    arm = sys.argv[1]; out = {}
    if arm == 'C': r = run('C')
    elif arm == 'A': r = run('A')
    elif arm == 'T1': r = run('C', support='one')
    elif arm == 'T2': r = run('C', wear=False)
    elif arm == 'T3': r = run_sync()
    r.pop('sim', None)
    json.dump(r, open(f'c141c_{arm}.json', 'w'), default=str)
    if 'fenetres' in r:
        for f in r['fenetres']: print('  fenetre', f)
    if 'generations' in r:
        for g in r['generations']: print('  generation', g)
