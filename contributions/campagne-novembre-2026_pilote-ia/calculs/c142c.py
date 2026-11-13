# C-142c / PR-1 — DE L'IMPACT CONFINE A L'USURE DES LIANTS ET A LEUR CYCLE. Protocole FIGE par ChatGPT (12 nov. 2026, 20 h 11 UTC,
#   sha256 99ba38e6f1bd0e528c72fa98152ac6e7e86cdccc6e984b9ef1f12c7f026c7f06 ; branche laterale du fil), execute independamment par Claude.
# Regle : germe K4, file [0,1,2,3], enfant en queue apres le demandeur. Porteur v dans au moins un K4 : impulsion unite p_v = e_v - 1/n sur sa
#   composante ; L = laplacien (masses et raideurs 1) ; W0(e) = somme_{lambda>0} [b_e^T Pi_lambda p_v]^2 / lambda ; W1 = idem / sqrt(lambda).
#   FREQ : D_e += W1 ; STRAIN : D_e += W0 ; OFF : rien. Seuil s_e = max(1, nombre de triangles contenant e), sur le graphe AVANT changement.
#   Admissibles : D_e >= s_e ; priorite au plus grand D_e/s_e, puis identifiants croissants ; au plus une subdivision par tentative ; pas de cascade.
#   H4 : le premier se divise, les autres admissibles du meme instant cedent. H1(K) : le premier seulement ; il cede si la division porterait un degre > K
#   (extremites ou voisins communs), sinon il se divise. H2 : division seule, les liens nes d'un lien de rang r ont le rang r+1 et un dommage initial r+1.
#   H3 : le premier se divise s'il reste un voisin commun, sinon il cede. Tsplit : division seule. Tbreak : rupture seule. T141 : usure locale de C-141c.
#   Porteur libre (dans aucun K4 quand il devient demandeur) : pas d'impulsion, naissance immediate ; L-free : lien au seul parent ; F-free : lien au
#   parent et a tous ses voisins. Budget : 4 096 tentatives ou 256 porteurs. Points : 64, 256, 1 024, 4 096 tentatives ; passages a 32, 64, 128, 256.
# PRECISIONS D'EXECUTION (Claude, declarees avant calcul) :
#  - admissibilite evaluee sur TOUS les liens du graphe (le texte ne restreint pas) ; tolerance numerique 1e-9 sur D_e >= s_e et sur l'egalite des rapports ;
#  - valeurs propres regroupees en espaces propres a 1e-8 pres (somme coherente dans chaque espace degenere, comme l'exige le texte) ;
#  - H1 : degres apres division des deux extremites (inchanges) et de chaque voisin commun (+1) ; le nouveau-ne n'est pas soumis au plafond ;
#  - Tbreak : deux lectures executees, "tous les liens admissibles cedent" (Tbreak) et "le premier seulement" (Tbreak1) ;
#  - T141 : bras C de C-141c inchange (usure +1 sur les liens du porteur, evaluation locale, ordre des identifiants) ;
#  - etat piege / libre de chaque porteur releve apres chaque tentative ; un cycle complet = piege -> libre -> piege pour une meme identite ;
#  - caracteristique d'Euler calculee jusqu'aux groupes de cinq porteurs ; presence de groupes de six signalee ;
#  - "distances croissantes" : les six distances finies et strictement croissantes sur deux pas consecutifs de population (32-64-128 ou 64-128-256).
import sys, json, time, itertools
import numpy as np
from collections import deque, defaultdict
from statistics import median

EPS = 1e-9
def ek(a, b): return (a, b) if a < b else (b, a)

class Sim:
    def __init__(self, wear='FREQ', decide='H4', K=None, free='F'):
        self.N = {i: set(j for j in range(4) if j != i) for i in range(4)}
        self.D = {ek(a, b): 0.0 for a, b in itertools.combinations(range(4), 2)}
        self.rank = {e: 0 for e in self.D}
        self.queue = deque(range(4)); self.next = 4; self.n = 0
        self.wear, self.decide, self.K, self.free = wear, decide, K, free
        self.state = {i: True for i in range(4)}; self.hist = {i: [(0, True)] for i in range(4)}
        self.c = defaultdict(int); self.coexist = False; self.log = []
        self.share_by_dist = defaultdict(float); self.nonincident = 0.0; self.ndep = 0
    # ---------- structure
    def trapped(self, v):
        Nv = self.N[v]
        for a in Nv:
            ca = Nv & self.N[a]
            for b in ca:
                if ca & self.N[b]: return True
        return False
    def component(self, v):
        d = {v: 0}; q = deque([v])
        while q:
            x = q.popleft()
            for y in self.N[x]:
                if y not in d: d[y] = d[x] + 1; q.append(y)
        return d
    def refresh(self, touched):
        for x in touched:
            s = self.trapped(x)
            if x not in self.state: self.state[x] = s; self.hist[x] = [(self.n, s)]
            elif s != self.state[x]: self.state[x] = s; self.hist[x].append((self.n, s))
    def subdivide(self, a, b, r=0, d0=0.0):
        C = self.N[a] & self.N[b]; touched = self.N[a] | self.N[b] | {a, b}
        z = self.next; self.next += 1
        self.N[a].discard(b); self.N[b].discard(a); del self.D[ek(a, b)]; del self.rank[ek(a, b)]
        self.N[z] = set()
        for x in (a, b, *C):
            self.N[z].add(x); self.N[x].add(z); self.D[ek(z, x)] = d0; self.rank[ek(z, x)] = r
        self.queue.append(z); self.c['divisions'] += 1; touched.add(z); return z, touched
    def rupture(self, a, b):
        touched = self.N[a] | self.N[b] | {a, b}
        self.N[a].discard(b); self.N[b].discard(a); del self.D[ek(a, b)]; del self.rank[ek(a, b)]
        self.c['ruptures'] += 1; return touched
    # ---------- la cloche
    def spectral(self, v):
        dist = self.component(v); comp = sorted(dist); idx = {x: i for i, x in enumerate(comp)}; n = len(comp)
        L = np.zeros((n, n)); edges = []
        for x in comp:
            for y in self.N[x]:
                if x < y:
                    edges.append((x, y)); i, j = idx[x], idx[y]; L[i, i] += 1; L[j, j] += 1; L[i, j] -= 1; L[j, i] -= 1
        w, U = np.linalg.eigh(L); p = -np.ones(n) / n; p[idx[v]] += 1; c = U.T @ p
        ea = np.array([idx[a] for a, b in edges]); eb = np.array([idx[b] for a, b in edges])
        W0 = np.zeros(len(edges)); W1 = np.zeros(len(edges)); i = 0
        while i < n:
            j = i + 1
            while j < n and w[j] - w[j - 1] < 1e-8 * max(1.0, abs(w[j])): j += 1
            lam = float(w[i:j].mean())
            if lam > 1e-9:
                y = U[:, i:j] @ c[i:j]; d2 = (y[ea] - y[eb]) ** 2; W0 += d2 / lam; W1 += d2 / np.sqrt(lam)
            i = j
        return edges, W0, W1, dist
    # ---------- une tentative
    def attempt(self):
        v = self.queue.popleft(); self.queue.append(v); self.n += 1; touched = set()
        if not self.trapped(v):
            z = self.next; self.next += 1; nb = {v} | (set(self.N[v]) if self.free == 'F' else set())
            self.N[z] = set()
            for x in nb: self.N[z].add(x); self.N[x].add(z); self.D[ek(z, x)] = 0.0; self.rank[ek(z, x)] = 0
            self.queue.append(z); self.c['naissances_libres'] += 1; touched = nb | {z}
            if len(self.log) < 60: self.log.append((self.n, v, 'libre', z))
        else:
            self.c['refus'] += 1
            if self.decide == 'T141':
                cand = []
                for x in sorted(self.N[v]):
                    e = ek(v, x); self.D[e] += 1.0
                    if self.D[e] >= max(1, len(self.N[v] & self.N[x])): cand.append(e)
                if cand: z, touched = self.subdivide(*min(cand))
            elif self.wear != 'OFF':
                edges, W0, W1, dist = self.spectral(v); W = W1 if self.wear == 'FREQ' else W0; tot = float(W.sum())
                for e, x in zip(edges, W): self.D[e] += float(x)
                if tot > 0:
                    self.ndep += 1
                    for (a, b), x in zip(edges, W):
                        d = min(dist[a], dist[b]); self.share_by_dist[d] += float(x) / tot
                        if d > 0: self.nonincident += float(x) / tot
                adm = []
                for (a, b), d in self.D.items():
                    s = max(1, len(self.N[a] & self.N[b]))
                    if d >= s - EPS: adm.append((-round(d / s, 9), (a, b)))
                adm.sort(); adm = [e for _, e in adm]
                if adm:
                    a, b = adm[0]; dec = self.decide; ev = None
                    if dec in ('H4', 'Tsplit'): z, t = self.subdivide(a, b); touched |= t; ev = ('division', (a, b), z)
                    elif dec == 'H2':
                        r = self.rank[(a, b)] + 1; z, t = self.subdivide(a, b, r, float(r)); touched |= t; ev = ('division', (a, b), z)
                    elif dec == 'H1':
                        C = self.N[a] & self.N[b]
                        if max([len(self.N[a]), len(self.N[b])] + [len(self.N[x]) + 1 for x in C]) > self.K: touched |= self.rupture(a, b); ev = ('rupture', (a, b))
                        else: z, t = self.subdivide(a, b); touched |= t; ev = ('division', (a, b), z)
                    elif dec == 'H3':
                        if self.N[a] & self.N[b]: z, t = self.subdivide(a, b); touched |= t; ev = ('division', (a, b), z)
                        else: touched |= self.rupture(a, b); ev = ('rupture', (a, b))
                    elif dec in ('Tbreak', 'Tbreak1'): touched |= self.rupture(a, b); ev = ('rupture', (a, b))
                    others = []
                    if dec in ('H4', 'Tbreak'):
                        for (x, y) in adm[1:]:
                            if (x, y) in self.D: touched |= self.rupture(x, y); others.append((x, y))
                    if len(self.log) < 60: self.log.append((self.n, v, ev, others))
        self.refresh(touched)
        nt = sum(1 for s in self.state.values() if s)
        if 0 < nt < len(self.state): self.coexist = True

def bfs(N, s):
    d = {s: 0}; q = deque([s])
    while q:
        x = q.popleft()
        for y in N[x]:
            if y not in d: d[y] = d[x] + 1; q.append(y)
    return d

def measure(S):
    N = S.N; V = len(N); E = sum(len(s) for s in N.values()) // 2
    K3 = K4 = K5 = 0; over = 0; k6 = False
    for a in N:
        for b in N[a]:
            if a < b:
                ab = N[a] & N[b]
                for c in ab:
                    if b < c:
                        abc = ab & N[c]; K3 += 1
                        if len(abc) > 2: over += 1
                        for d in abc:
                            if c < d:
                                K4 += 1; abcd = abc & N[d]
                                for e in abcd:
                                    if d < e:
                                        K5 += 1
                                        if abcd & N[e]: k6 = True
    comp = 0; seen = set()
    for s in N:
        if s not in seen: comp += 1; seen.update(bfs(N, s))
    deg = sorted(len(s) for s in N.values()); dist = {}
    for i in range(4):
        d = bfs(N, i)
        for j in range(i + 1, 4): dist['%d-%d' % (i, j)] = d.get(j)
    return dict(n=S.n, V=V, E=E, K3=K3, K4=K4, K5=K5, K6=k6, chi=V - E + K3 - K4 + K5, composantes=comp, faces_plus_de_2=over,
                deg_max=deg[-1], deg_med=median(deg), deg_q95=deg[int(0.95 * (V - 1))], distances=dist,
                pieges=sum(1 for s in S.state.values() if s), libres=sum(1 for s in S.state.values() if not s),
                divisions=S.c['divisions'], ruptures=S.c['ruptures'], naissances_libres=S.c['naissances_libres'], refus=S.c['refus'])

def cycles(hist):
    """nombre de cycles complets piege -> libre -> piege ; un porteur ne libre n'a pas de cycle a son premier emprisonnement"""
    k = 0; freed = False; times = []
    for (t0, s0), (t1, s1) in zip(hist, hist[1:]):
        if s0 and not s1: freed = True; tl = t1
        elif (not s0) and s1 and freed: k += 1; times.append((tl, t1)); freed = False
    return k, times

def run_arm(spec):
    name, wear, decide, K, free = spec; t0 = time.time()
    S = Sim(wear, decide, K, free); pts = {}; passages = {}; todo = [32, 64, 128, 256]
    while S.n < 4096 and len(S.N) < 256:
        S.attempt()
        if S.n in (64, 256, 1024, 4096): pts[S.n] = measure(S)
        while todo and len(S.N) >= todo[0]: passages[todo.pop(0)] = measure(S)
    fin = measure(S)
    cyc = {v: cycles(h) for v, h in S.hist.items()}; kmax = max(k for k, _ in cyc.values()); with1 = [v for v, (k, _) in cyc.items() if k >= 1]
    firsts = sorted(set(t[0] for v in with1 for t in cyc[v][1][:1]))
    lib = [h[i + 1][0] for h in S.hist.values() for i in range(len(h) - 1) if h[i][1] and not h[i + 1][1]]
    ret = [t[1] for v in with1 for t in cyc[v][1][:1]]
    two = [cyc[v][1][1][1] for v in cyc if cyc[v][0] >= 2]
    allpts = list(pts.values()) + list(passages.values())
    conn = all(m['composantes'] == 1 for m in allpts) and fin['composantes'] == 1
    def incr(a, b):
        return a in passages and b in passages and all(passages[a]['distances'][k] is not None and passages[b]['distances'][k] is not None
                                                        and passages[b]['distances'][k] > passages[a]['distances'][k] for k in passages[a]['distances'])
    dist2 = (incr(32, 64) and incr(64, 128)) or (incr(64, 128) and incr(128, 256))
    degst = all(k in passages for k in (64, 128, 256)) and passages[128]['deg_max'] <= passages[64]['deg_max'] and passages[256]['deg_max'] <= passages[128]['deg_max']
    shifted = len(with1) >= 2 and len(set(tuple(cyc[v][1]) for v in with1)) >= 2 and S.coexist
    res = dict(bras=name, usure=wear, decision=decide, K=K, reprise=free, arret='256 porteurs' if len(S.N) >= 256 else '4 096 tentatives', tentatives=S.n,
               points=pts, passages=passages, fin=fin, cycles_max_par_identite=kmax, identites_avec_un_cycle=len(with1),
               identites_avec_deux_cycles=sum(1 for k, _ in cyc.values() if k >= 2), premiere_liberation=min(lib) if lib else None,
               premier_retour=min(ret) if ret else None, deuxieme_cycle=min(two) if two else None, coexistence=S.coexist,
               part_non_incidente=(S.nonincident / S.ndep) if S.ndep else None,
               part_par_distance={int(d): x / S.ndep for d, x in sorted(S.share_by_dist.items())} if S.ndep else None,
               crit=dict(deux_cycles=kmax >= 2, cycles_decales=shifted, connexe=conn, distances_croissantes=dist2, degre_stabilise=degst),
               journal=S.log[:40], duree=round(time.time() - t0, 1))
    res['PASS_complet'] = all(res['crit'].values())
    return res

def specs():
    out = [('T141', 'LOCAL', 'T141', None, 'F'), ('OFF', 'OFF', 'H4', None, 'F')]
    for wear in ('FREQ', 'STRAIN'):
        for free in ('F', 'L'):
            for dec, K in [('H4', None)] + [('H1', k) for k in (4, 8, 16, 32, 64)] + [('H2', None), ('H3', None), ('Tsplit', None), ('Tbreak', None), ('Tbreak1', None)]:
                out.append((f"{dec}{'' if K is None else K}/{wear}/{free}-free", wear, dec, K, free))
    return out

if __name__ == '__main__':
    from multiprocessing import Pool
    S = specs(); results = {}
    with Pool(2) as pool:
        for r in pool.imap_unordered(run_arm, S):
            results[r['bras']] = r; f = r['fin']; c = r['crit']
            print(f"{r['bras']:<24} arrêt={r['arret']:<16} n={r['tentatives']:<5} V={f['V']:<4} K4={f['K4']:<5} comp={f['composantes']:<3} deg max/med={f['deg_max']}/{f['deg_med']} "
                  f"div={f['divisions']} rupt={f['ruptures']} libres_nés={f['naissances_libres']} 1re lib={r['premiere_liberation']} retour={r['premier_retour']} 2e cycle={r['deuxieme_cycle']} "
                  f"cycles max={r['cycles_max_par_identite']} | 2cycles={c['deux_cycles']} décalés={c['cycles_decales']} connexe={c['connexe']} dist={c['distances_croissantes']} degré={c['degre_stabilise']} "
                  f"=> PASS={r['PASS_complet']} ({r['duree']} s)", flush=True)
            json.dump(results, open('c142c.json', 'w'), default=str)
    print('TERMINE', len(results), 'bras')
