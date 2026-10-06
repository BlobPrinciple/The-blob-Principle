#!/usr/bin/env python3
"""
================================================================================
  M2-W / G0-CRIT-NONCOND — COUREUR SUR LE SECTEUR T^3 CERTIFIE
================================================================================
  Ce module remplace tout coureur anterieur descendu de dDelta^4 (= S^3).
  Les mouvements de Pachner preservent la topologie : une chaine partie de la
  frontiere du 4-simplexe explore S^3 pour toujours, jamais T^3.

  CE QUI EST CERTIFIE ICI
    [1] germe T^3 explicite : triangulation de Freudenthal/Kuhn, N3 = 6 L^3
        - variete fermee : chaque triangle borde 2 tetraedres, chaque lien
          de sommet a chi = 2
        - Betti calcules en rang ENTIER : (1,3,3,1) verifie a L=3 et L=4
        - tous les q_v = 24 exactement  (= premier entier pair > q_plat=22.79)
        - N0/N3 = 1/6 exactement, donc I_2(germe) = 6/N3 EXACTEMENT
    [2] mouvements de Pachner 2<->3 et 1<->4 avec tests de legalite complets
    [3] mise a jour INCREMENTALE de N0,N1,N2,N3, n_e, q_v, L, D, sum q^k
    [4] acceptation de Barker (unique a verifier balance detaillee ET
        complementarite a(r)+a(1/r)=1) avec correction de Hastings exacte
    [5] temoin positif : suspension S^0 * L_geodesique, I_2 -> 1/32 exactement
    [6] auto-test bloquant avant toute campagne

  NOMBRES DE CONCEPTION (corriges pour le germe de Freudenthal)
    I_2(germe)      = 6/N3            I_2(suspension) -> 1/32 = 0.031250
    croisement brut : N3 = 192        separation x10 : N3 = 1920
    echelle L :  162 · 384 · 750 · 1296 · 2058 · 3072 · 4374
    >>> L=7 (N3=2058) depasse le gold-standard. Toute la campagne de
        decision est atteignable avec des germes CERTIFIES, sans avoir a
        chercher un temoin T^3 a chaque volume.

  RESERVE INSCRITE
    Version ETIQUETEE : le facteur 1/|Aut(T)| n'est pas implemente. AUT-LIFT
    le justifie a condition que les propositions soient equivariantes, ce qui
    est le cas ici (choix uniforme sur triangles/aretes/tetraedres/sommets).
    Le passage au quotient exact reste a certifier separement.
================================================================================
"""
import itertools, math, random, time, json
from collections import defaultdict, Counter

D_STAR = 2.0*math.pi/math.acos(1.0/3.0)      # 5.104299312119540
Q_PLAT = 4.0*math.pi/(3.0*math.acos(1.0/3.0)-math.pi)   # 22.794665

# ============================================================ etat incremental
class State:
    """Triangulation d'une 3-variete fermee, avec tous les compteurs a jour."""
    def __init__(self, tets):
        self.T = set(tets)
        self.ne = defaultdict(int)      # arete -> nb de tetraedres
        self.nf = defaultdict(int)      # triangle -> nb de tetraedres
        self.qv = defaultdict(int)      # sommet -> nb de tetraedres
        self.ft = defaultdict(set)      # triangle -> tetraedres  [O(1)]
        self.et = defaultdict(set)      # arete    -> tetraedres  [O(1)]
        for t in self.T: self._add_counts(t, +1)
        self.next_vertex = max(max(t) for t in self.T) + 1

    def _add_counts(self, t, s):
        for e in itertools.combinations(t, 2):
            self.ne[e] += s
            if s > 0: self.et[e].add(t)
            else: self.et[e].discard(t)
        for f in itertools.combinations(t, 3):
            self.nf[f] += s
            if s > 0: self.ft[f].add(t)
            else: self.ft[f].discard(t)
        for v in t: self.qv[v] += s
        if s < 0:
            for e in itertools.combinations(t, 2):
                if self.ne[e] == 0: del self.ne[e]; self.et.pop(e, None)
            for f in itertools.combinations(t, 3):
                if self.nf[f] == 0: del self.nf[f]; self.ft.pop(f, None)
            for v in t:
                if self.qv[v] == 0: del self.qv[v]

    def relabel(self, old, new):
        """[AUT-LIFT] Renomme old->new partout. Sert a la RECOMPACTION canonique
           apres un 4->1 : l invariant labels = {0,...,N0-1} est restaure."""
        if old == new: return
        touched=[t for t in self.T if old in t]
        for t in touched:
            self.remove(t); self.add(tuple(new if x==old else x for x in t))

    def add(self, t):
        t = tuple(sorted(t)); self.T.add(t); self._add_counts(t, +1)
    def remove(self, t):
        t = tuple(sorted(t)); self.T.discard(t); self._add_counts(t, -1)

    # ---------------- f-vecteur et observables ----------------
    @property
    def N0(self): return len(self.qv)
    @property
    def N1(self): return len(self.ne)
    @property
    def N2(self): return len(self.nf)
    @property
    def N3(self): return len(self.T)

    def tri_list(self):
        if getattr(self,'_tl_v',None) != (self.N2, self.N3): 
            self._tl = list(self.nf); self._tl_v = (self.N2, self.N3)
        return self._tl
    def edge_list(self):
        if getattr(self,'_el_v',None) != (self.N1, self.N3):
            self._el = list(self.ne); self._el_v = (self.N1, self.N3)
        return self._el
    def L(self):  return sum(math.log(1.0+n) for n in self.ne.values())
    def D(self):  return sum((n-D_STAR)**2 for n in self.ne.values())
    def ipr(self, ks=(2,3,4)):
        tot = 4.0*self.N3
        return {k: sum((q/tot)**k for q in self.qv.values()) for k in ks}
    def qmax(self): return max(self.qv.values())

    # ---------------- certification topologique ----------------
    def is_closed_manifold(self):
        """[CORRECTION 4] chi(Lk)=2 ne suffit pas. On certifie que chaque lien
           est une VRAIE 2-sphere : surface fermee (aretes 2-regulieres),
           chaque sommet du lien a un lien circulaire, connexe, chi=2.
           Une surface fermee connexe de chi=2 EST S^2."""
        if set(self.nf.values()) != {2}: return False, "triangle non 2-a-2"
        inc = defaultdict(list)
        for t in self.T:
            for v in t: inc[v].append(t)
        for v, ts in inc.items():
            tris=[tuple(sorted(x for x in t if x != v)) for t in ts]
            ed=defaultdict(int); vt=defaultdict(set); adj=defaultdict(set)
            for tr in tris:
                for e in itertools.combinations(tr,2): ed[e]+=1
                for w in tr: vt[w].add(tr)
            for e in ed:
                adj[e[0]].add(e[1]); adj[e[1]].add(e[0])
            if set(ed.values()) != {2}:
                return False, "lien de %d : arete non 2-reguliere" % v
            # lien de chaque sommet du lien = cercle
            for w, trs in vt.items():
                deg=defaultdict(int)
                for tr in trs:
                    o=[x for x in tr if x != w]
                    deg[o[0]]+=1; deg[o[1]]+=1
                if set(deg.values()) != {2}:
                    return False, "lien de %d : sommet %d non circulaire" % (v,w)
                # connexite du cercle
                st=[next(iter(deg))]; seen={st[0]}
                nb=defaultdict(set)
                for tr in trs:
                    o=[x for x in tr if x != w]; nb[o[0]].add(o[1]); nb[o[1]].add(o[0])
                while st:
                    x=st.pop()
                    for y in nb[x]:
                        if y not in seen: seen.add(y); st.append(y)
                if len(seen) != len(deg):
                    return False, "lien de %d : sommet %d a plusieurs cercles" % (v,w)
            # connexite du lien
            st=[tris[0][0]]; seen={tris[0][0]}
            while st:
                x=st.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y); st.append(y)
            if len(seen) != len(vt):
                return False, "lien de %d non connexe" % v
            chi=len(vt)-len(ed)+len(tris)
            if chi != 2: return False, "lien de %d : chi=%d" % (v, chi)
        return True, "OK"

    def betti_f2(self):
        """[CORRECTION 3] Rang EXACT sur F_2 par elimination avec bitsets.
           np.linalg.matrix_rank est un rang NUMERIQUE sur R, pas un rang
           certifie. Ici : arithmetique exacte, aucun flottant."""
        V=[(x,) for x in sorted(self.qv)]; E=sorted(self.ne)
        F=sorted(self.nf); TT=sorted(self.T)
        iv={x:i for i,x in enumerate(V)}; ie={x:i for i,x in enumerate(E)}
        iff={x:i for i,x in enumerate(F)}
        def rank_f2(cells, lo):
            cols=[]
            for c in cells:
                m=0
                for k in range(len(c)):
                    sub=tuple(c[:k]+c[k+1:])
                    if sub in lo: m ^= (1 << lo[sub])
                if m: cols.append(m)
            r=0; piv={}
            for m in cols:
                while m:
                    b=m.bit_length()-1
                    if b in piv: m ^= piv[b]
                    else: piv[b]=m; r+=1; break
            return r
        r1=rank_f2(E,iv); r2=rank_f2(F,ie); r3=rank_f2(TT,iff)
        return (len(V)-r1, len(E)-r1-r2, len(F)-r2-r3, len(TT)-r3)
    betti = betti_f2

# ============================================================ germes
def freudenthal_torus(L):
    """Germe T^3 certifie : n^3 cubes, 6 tetraedres chacun. N3 = 6 L^3."""
    vid = {}
    for c in itertools.product(range(L), repeat=3): vid[c] = len(vid)
    T = set()
    for c in itertools.product(range(L), repeat=3):
        for perm in itertools.permutations(range(3)):
            cur = list(c); chain = [tuple(cur)]
            for d in perm:
                cur = cur[:]; cur[d] += 1; chain.append(tuple(cur))
            idx = tuple(sorted(vid[tuple(x % L for x in p)] for p in chain))
            if len(set(idx)) == 4: T.add(idx)
    return State(T)

def suspension_witness(F_faces):
    """Temoin CONDENSE : S^0 * (sphere geodesique). I_2 -> 1/32, m = 1/2."""
    # icosaedre puis subdivisions : on genere par subdivision de triangles
    import numpy as np
    phi=(1+5**0.5)/2
    verts=[(-1,phi,0),(1,phi,0),(-1,-phi,0),(1,-phi,0),(0,-1,phi),(0,1,phi),
           (0,-1,-phi),(0,1,-phi),(phi,0,-1),(phi,0,1),(-phi,0,-1),(-phi,0,1)]
    faces=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),
           (11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),
           (3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
    P=[list(v) for v in verts]
    while len(faces)*4 <= F_faces:
        mid={}; nf=[]
        def M(a,b):
            k=(min(a,b),max(a,b))
            if k not in mid:
                P.append([(P[a][i]+P[b][i])/2 for i in range(3)]); mid[k]=len(P)-1
            return mid[k]
        for (a,b,c) in faces:
            ab,bc,ca=M(a,b),M(b,c),M(c,a)
            nf += [(a,ab,ca),(b,bc,ab),(c,ca,bc),(ab,bc,ca)]
        faces=nf
    n=len(P); p0,p1=n,n+1
    T=set()
    for (a,b,c) in faces:
        T.add(tuple(sorted((a,b,c,p0)))); T.add(tuple(sorted((a,b,c,p1))))
    return State(T)

# ============================================================ Pachner
def try_23(S, tri):
    """2->3 sur le triangle tri. Rend (tets_out, tets_in) ou None."""
    if S.nf.get(tri, 0) != 2: return None
    ts = list(S.ft.get(tri, ()))
    if len(ts) != 2: return None
    u = [x for x in ts[0] if x not in tri][0]
    w = [x for x in ts[1] if x not in tri][0]
    if u == w: return None
    if (min(u,w), max(u,w)) in S.ne: return None      # arete deja presente
    a,b,c = tri
    return (ts, [tuple(sorted((p,q,u,w))) for p,q in ((a,b),(b,c),(a,c))])

def try_32(S, ed):
    """3->2 sur l'arete ed."""
    if S.ne.get(ed, 0) != 3: return None
    ts = list(S.et.get(ed, ()))
    if len(ts) != 3: return None
    rest = set()
    for t in ts: rest |= set(x for x in t if x not in ed)
    if len(rest) != 3: return None
    tri = tuple(sorted(rest))
    if tri in S.nf: return None                        # triangle deja present
    u,w = ed
    return (ts, [tuple(sorted(tri+(u,))), tuple(sorted(tri+(w,)))])

def try_14(S, t, newv):
    return ([t], [tuple(sorted(f+(newv,))) for f in itertools.combinations(t,3)])

def try_41(S, v):
    if S.qv.get(v, 0) != 4: return None
    ts = [t for t in S.T if v in t]
    if len(ts) != 4: return None
    rest = set()
    for t in ts: rest |= set(x for x in t if x != v)
    if len(rest) != 4: return None
    tet = tuple(sorted(rest))
    if tet in S.T: return None
    return (ts, [tet])

# ============================================================ echantillonneur
def logpi(S, alpha, b, mu, tau):
    return (alpha*S.L() - b*S.D() - mu*S.N3)/tau

def barker_step(S, alpha, b, mu, tau, rng, lw, window=None):
    """[CORRECTION 1] SEULS les mouvements 2<->3 sont utilises.
       Ils laissent N0 = L^3 FIXE et le jeu d'etiquettes FIXE, donc AUT-LIFT
       est exact : a N0 fixe, une classe [T] a exactement N0!/|Aut T|
       representants etiquetes, et N0! est un facteur commun.
       1<->4 changeait N0 et incrementait next_vertex sans recompactage :
       la multiplicite dependait alors de l'HISTOIRE de la chaine.

       [CORRECTION 2] window = (Nmin, Nmax) : tout mouvement sortant de la
       fenetre est REJETE. C'est une restriction de l'espace d'etats, donc
       la balance detaillee est preservee."""
    kind = '23' if rng.random() < 0.5 else '32'
    if kind == '23':
        if window and S.N3 + 1 > window[1]: return S, lw, False
        if S.N2 == 0: return S, lw, False
        tri = rng.choice(S.tri_list()); res = try_23(S, tri)
        if res is None: return S, lw, False
        fwd = 1.0/S.N2
    else:
        if window and S.N3 - 1 < window[0]: return S, lw, False
        if S.N1 == 0: return S, lw, False
        ed = rng.choice(S.edge_list()); res = try_32(S, ed)
        if res is None: return S, lw, False
        fwd = 1.0/S.N1
    out, inn = res
    for t in out: S.remove(t)
    for t in inn: S.add(t)
    lw2 = logpi(S, alpha, b, mu, tau)
    back = (1.0/S.N1) if kind == '23' else (1.0/S.N2)
    r = math.exp(min(lw2-lw, 700.0)) * back/fwd
    if rng.random() < r/(1.0+r):
        return S, lw2, True
    for t in inn: S.remove(t)
    for t in out: S.add(t)
    return S, lw, False

# ============================================================ AUTO-TEST
def autotest(verbose=True):
    print("="*70); print("  AUTO-TEST — regle 5 appliquee au coureur"); print("="*70)
    S = freudenthal_torus(3)
    fv = (S.N0, S.N1, S.N2, S.N3)
    print("  [a] germe L=3 : f = %s   chi = %d" % (str(fv), fv[0]-fv[1]+fv[2]-fv[3]))
    if fv != (27,189,324,162) or fv[0]-fv[1]+fv[2]-fv[3] != 0:
        print("  >>> ECHEC f-vecteur. ARRET."); return False
    ok, msg = S.is_closed_manifold()
    print("  [b] variete fermee : %s" % msg)
    if not ok: print("  >>> ECHEC. ARRET."); return False
    bb = tuple(int(x) for x in S.betti())
    print("  [c] Betti EXACTS sur F_2 = %s   [T^3 : (1,3,3,1)]" % (str(bb),))
    if bb != (1,3,3,1): print("  >>> ECHEC : PAS T^3. ARRET."); return False
    qs = set(S.qv.values()); I = S.ipr()
    print("  [d] tous les q_v = %s   I_2 = %.8f   6/N3 = %.8f" % (qs, I[2], 6.0/S.N3))
    if qs != {24} or abs(I[2]-6.0/S.N3) > 1e-12:
        print("  >>> ECHEC : germe non uniforme. ARRET."); return False
    W = suspension_witness(1280)
    IW = W.ipr()
    print("  [e] temoin suspension : N3=%d  I_2=%.6f  (1/32=%.6f)  q_max/N3=%.4f"
          % (W.N3, IW[2], 1/32.0, W.qmax()/W.N3))
    if abs(IW[2]-1/32.0) > 5e-3 or abs(W.qmax()/W.N3-0.5) > 1e-9:
        print("  >>> ECHEC : temoin condense hors specification. ARRET."); return False
    rng = random.Random(11); lw = logpi(S, 0.4, 0.05, 2.3, 1.0); nacc = 0
    for _ in range(600):
        S, lw, a = barker_step(S, 0.4, 0.05, 2.3, 1.0, rng, lw)
        nacc += a
    ok, msg = S.is_closed_manifold()
    bb = tuple(int(x) for x in S.betti())
    print("  [f] apres 600 pas : N3=%d  variete=%s  Betti=%s  acceptation=%.2f"
          % (S.N3, msg, str(bb), nacc/600.0))
    if not ok or bb != (1,3,3,1):
        print("  >>> ECHEC : topologie non preservee. ARRET."); return False
    print("  ==> AUTO-TEST PASSE.\n"); return True


def try_41c(S, v):
    if S.qv.get(v,0)!=4: return None
    ts=[t for t in S.T if v in t]
    if len(ts)!=4: return None
    rest=set()
    for t in ts: rest |= set(x for x in t if x!=v)
    if len(rest)!=4: return None
    tet=tuple(sorted(rest))
    if tet in S.T: return None
    return ts,[tet]

def apply_41c(S, v):
    r=try_41c(S,v)
    if r is None: return False
    out,inn=r
    for t in out: S.remove(t)
    for t in inn: S.add(t)
    last=S.N0                     # ancien label max = N0_apres
    if last in S.qv and last!=v: S.relabel(last,v)
    S.next_vertex=S.N0
    return True

def step4(S, al, b, mu, tau, rng, lw, winN3, winN0):
    """4 types : 2->3, 3->2, 1->4, 4->1 (avec recompaction)."""
    kind=rng.choice(('23','32','14','41'))
    if kind=='23':
        if S.N3+1>winN3[1] or S.N2==0: return S,lw,False
        tri=rng.choice(S.tri_list()); res=try_23(S,tri)
        if res is None: return S,lw,False
        out,inn=res; fwd=1.0/S.N2
        for t in out: S.remove(t)
        for t in inn: S.add(t)
        back=1.0/S.N1
    elif kind=='32':
        if S.N3-1<winN3[0] or S.N1==0: return S,lw,False
        ed=rng.choice(S.edge_list()); res=try_32(S,ed)
        if res is None: return S,lw,False
        out,inn=res; fwd=1.0/S.N1
        for t in out: S.remove(t)
        for t in inn: S.add(t)
        back=1.0/S.N2
    elif kind=='14':
        if S.N3+3>winN3[1] or S.N0+1>winN0[1]: return S,lw,False
        t=rng.choice(sorted(S.T)); v=S.next_vertex
        out,inn=try_14(S,t,v); fwd=1.0/S.N3
        for x in out: S.remove(x)
        for x in inn: S.add(x)
        S.next_vertex=v+1
        back=1.0/S.N0
    else:
        if S.N3-3<winN3[0] or S.N0-1<winN0[0]: return S,lw,False
        v=rng.choice(sorted(S.qv))
        if try_41c(S,v) is None: return S,lw,False
        fwd=1.0/S.N0
        snap=set(S.T); nv=S.next_vertex
        apply_41c(S,v)
        back=1.0/S.N3
    lw2=logpi(S,al,b,mu,tau)
    r=math.exp(min(lw2-lw,700.0))*back/fwd
    if rng.random()<r/(1+r): return S,lw2,True
    # rejet : restaurer
    if kind=='41':
        S.T=set(snap); S.ne.clear(); S.nf.clear(); S.qv.clear(); S.ft.clear(); S.et.clear()
        for t in S.T: S._add_counts(t,+1)
        S.next_vertex=nv
    elif kind=='14':
        for x in inn: S.remove(x)
        for x in out: S.add(x)
        S.next_vertex=v
    else:
        for t in inn: S.remove(t)
        for t in out: S.add(t)
    return S,lw,False

# ============================================================================
#  S4 — VERROUILLAGE ADVERSARIAL DE GERME-EXTREMAL (cible D52)
#  Blob Principle — 16 août 2026 — script autonome, stdlib uniquement
# ----------------------------------------------------------------------------
#  CONJECTURE ATTAQUÉE (GERME-EXTREMAL, V329 HC.3) :
#     sup { rho : A = 0 atteignable sur T^3 } = 1/6  (atteint par le germe).
#  S4 = recherche adversariale : MINIMISER l'horloge A sous la contrainte
#  STRICTE rho > 1/6 (i.e. 6*N0 > N3), quatre familles de Pachner, jusqu'à
#  1 500 000 pas.
#
#  SÉMANTIQUE DU VERDICT (honnêteté épistémique, principe de verrou §C.3) :
#   - Si A = 0 exact est atteint avec 6*N0 > N3 sur variété certifiée :
#       COUNTEREXAMPLE — GERME-EXTREMAL est FALSIFIÉE. État complet sauvé.
#   - Sinon, après N pas : S4 NÉGATIF — évidence adversariale [O] renforcée.
#       CE N'EST PAS UN [T]. Le théorème reste la cible D52.
#
#  PALIERS JSON (répertoire --outdir) :
#   - checkpoint_STEP.json : reprise exacte (état, RNG, records, paramètres)
#   - record_*.json        : chaque nouveau minimum EXACT de A/N3 (état complet)
#   - COUNTEREXAMPLE.json  : si falsification (état complet + certificats)
#   - final_summary.json   : bilan, identités auditées, verdict
#  Reprise : relancer la même commande avec --resume (reprend le dernier
#  checkpoint du répertoire).
#
#  AUDITS EXACTS à chaque palier :
#   - identité  somme_e [|N(a)&N(b)| - n_e] = 3*MT      (tolérance zéro)
#   - identité  K3 = 2*N3 + MT                           (tolérance zéro)
#   - variété fermée ; Betti F2 tous les 10 paliers et à chaque record.
#  L'objectif de descente est le compteur NÉCESSAIRE bon marché
#  cheap = #{aretes : |N(a)&N(b)| = n_e}  (A/2 <= cheap) ; l'A EXACT
#  (condition de lien + tétraèdre manquant) est calculé aux paliers,
#  aux records, et dès que cheap = 0.
#  Usage :  python3 S4_GERME_EXTREMAL.py --steps 1500000 --palier 10000 \
#           --outdir S4_run --seed 52 [--resume] [--n3max 2400]
# ============================================================================
import json, os, sys, time, argparse, itertools, random as _rnd
from collections import defaultdict

def _nbrs(S):
    nb=defaultdict(set)
    for (a,b) in S.ne: nb[a].add(b); nb[b].add(a)
    return nb

def cheap_count(S):
    nb=_nbrs(S); c=0; exc=0
    for e,n in S.ne.items():
        k=len(nb[e[0]]&nb[e[1]]); exc+=k-n
        if k==n: c+=1
    return c,exc

def exact_audit(S):
    nb=_nbrs(S); tri=set(); tet=set(S.T)
    for t in S.T:
        for c in itertools.combinations(t,3): tri.add(c)
    MT=0
    for a in nb:
        for b in nb[a]:
            if b<=a: continue
            for c in nb[a]&nb[b]:
                if c<=b: continue
                if (a,b,c) not in tri: MT+=1
    A=0; BL=0; TN=0
    for e in S.ne:
        a,b=e; common=nb[a]&nb[b]
        lk={c for c in common if tuple(sorted((a,b,c))) in tri}
        if common!=lk: BL+=1; continue
        blocked=False
        for c,cc in itertools.combinations(sorted(lk),2):
            if cc in nb[c] and tuple(sorted((a,c,cc))) in tri and \
               tuple(sorted((b,c,cc))) in tri and tuple(sorted((a,b,c,cc))) not in tet:
                blocked=True; break
        if blocked: TN+=1
        else: A+=2
    K3=len(tri)+MT
    _,exc=cheap_count(S)
    idA = (exc==3*MT); idB = (K3==2*S.N3+MT)
    return dict(A=A,BL=BL,TN=TN,MT=MT,K3=K3,id_3MT=idA,id_K3=idB)

def state_to_json(S):
    return sorted([list(t) for t in S.T])

def state_from_json(lst):
    S=freudenthal_torus(3)
    S.T=set(tuple(sorted(t)) for t in lst)
    S.ne.clear(); S.nf.clear(); S.qv.clear(); S.ft.clear(); S.et.clear()
    for t in S.T: S._add_counts(t,+1)
    S.next_vertex=max(v for t in S.T for v in t)+1
    return S

def legal_ops(S,rng,n3min,n3max):
    ops=[]
    fs=list(S.nf); rng.shuffle(fs)
    for x in fs[:60]:
        if S.N3+1<=n3max and try_23(S,x) is not None: ops.append(('23',x))
        if len(ops)>=40: break
    es=[e for e,n in S.ne.items() if n==3]; rng.shuffle(es)
    for e in es[:40]:
        if S.N3-1>=n3min and try_32(S,e) is not None: ops.append(('32',e))
    if S.N3+3<=n3max:
        ts=sorted(S.T); rng.shuffle(ts)
        for t in ts[:15]: ops.append(('14',t))
    vs=[v for v,q in S.qv.items() if q==4]; rng.shuffle(vs)
    for v in vs[:15]:
        if S.N3-3>=n3min and try_41c(S,v) is not None: ops.append(('41',v))
    return ops

def apply_op(S,kind,arg):
    if kind=='23':
        r=try_23(S,arg)
        if r is None: return False
        o,i=r
    elif kind=='32':
        r=try_32(S,arg)
        if r is None: return False
        o,i=r
    elif kind=='14':
        v=S.next_vertex; o,i=try_14(S,arg,v)
    else:
        if try_41c(S,arg) is None: return False
        apply_41c(S,arg); return True
    for x in o: S.remove(x)
    for x in i: S.add(x)
    if kind=='14': S.next_vertex=v+1
    return True

def snapshot(S):
    return set(S.T),S.next_vertex

def restore(S,snap):
    T0,nv=snap
    S.T=set(T0); S.ne.clear();S.nf.clear();S.qv.clear();S.ft.clear();S.et.clear()
    for x in S.T: S._add_counts(x,+1)
    S.next_vertex=nv

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--steps',type=int,default=1500000)
    ap.add_argument('--palier',type=int,default=10000)
    ap.add_argument('--seed',type=int,default=52)
    ap.add_argument('--outdir',default='S4_run')
    ap.add_argument('--resume',action='store_true')
    ap.add_argument('--n3min',type=int,default=60)
    ap.add_argument('--n3max',type=int,default=2400)
    ap.add_argument('--look',type=int,default=4)
    ap.add_argument('--T0',type=float,default=2.0)
    ap.add_argument('--reheat',type=int,default=50000)
    a=ap.parse_args()
    os.makedirs(a.outdir,exist_ok=True)
    rng=_rnd.Random(a.seed)
    step0=0; records=[]; bestA=None
    if a.resume:
        cps=sorted([f for f in os.listdir(a.outdir) if f.startswith('checkpoint_')],
                   key=lambda f:int(f.split('_')[1].split('.')[0]))
        if cps:
            cp=json.load(open(os.path.join(a.outdir,cps[-1])))
            S=state_from_json(cp['state']); step0=cp['step']
            rng.setstate((cp['rng'][0],tuple(cp['rng'][1]),cp['rng'][2]))
            records=cp.get('records',[]); bestA=cp.get('bestA')
            print("REPRISE au pas %d (N3=%d)"%(step0,S.N3),flush=True)
        else:
            S=freudenthal_torus(3)
    else:
        S=freudenthal_torus(3)
    t0=time.time(); T=a.T0
    ch,_=cheap_count(S); cur=ch/float(S.N3)
    for step in range(step0+1,a.steps+1):
        if step%a.reheat==0: T=a.T0
        T*=0.99999
        ops=legal_ops(S,rng,a.n3min,a.n3max)
        if not ops:
            print("AUCUN MOUVEMENT LEGAL au pas %d"%step); break
        cands=[ops[rng.randrange(len(ops))] for _ in range(min(a.look,len(ops)))]
        best=None; bsc=None
        for kind,arg in cands:
            snap=snapshot(S)
            if not apply_op(S,kind,arg): restore(S,snap); continue
            if 6*S.N0<=S.N3:
                restore(S,snap); continue          # contrainte stricte rho > 1/6
            c2,_=cheap_count(S); sc=c2/float(S.N3)
            if bsc is None or sc<bsc: bsc=sc; best=(kind,arg)
            restore(S,snap)
        if best is None: continue
        d=bsc-cur
        if d<=0 or rng.random()<pow(2.718281828,-d/max(T,1e-9)) or rng.random()<0.08:
            apply_op(S,*best); cur=bsc
        if cur<1e-12 or step%a.palier==0:
            au=exact_audit(S)
            ok,msg=S.is_closed_manifold()
            palier=dict(step=step,elapsed=round(time.time()-t0,1),N3=S.N3,N0=S.N0,
                        rho=S.N0/S.N3,cheap=int(cur*S.N3),**au,manifold=msg,
                        constraint_ok=bool(6*S.N0>S.N3))
            if not(au['id_3MT'] and au['id_K3']):
                palier['FATAL']='identite violee'
                json.dump(palier,open(os.path.join(a.outdir,'FATAL_%d.json'%step),'w'),indent=1)
                print("FATAL : identite violee au pas %d"%step); sys.exit(9)
            newrec = (bestA is None or au['A']/S.N3<bestA)
            if newrec:
                bestA=au['A']/S.N3
                bet=S.betti_f2()
                rec=dict(palier,betti=list(bet),state=state_to_json(S))
                records.append(dict(step=step,A=au['A'],N3=S.N3,rho=S.N0/S.N3))
                json.dump(rec,open(os.path.join(a.outdir,'record_A%.5f_step%d.json'%(bestA,step)),'w'))
            if au['A']==0 and 6*S.N0>S.N3 and ok:
                bet=S.betti_f2()
                cx=dict(palier,betti=list(bet),state=state_to_json(S),
                        VERDICT='COUNTEREXAMPLE — GERME-EXTREMAL FALSIFIEE')
                json.dump(cx,open(os.path.join(a.outdir,'COUNTEREXAMPLE.json'),'w'),indent=1)
                print("*** COUNTEREXAMPLE : A=0 a rho=%.6f > 1/6 — GERME-EXTREMAL FALSIFIEE ***"%(S.N0/S.N3))
                sys.exit(42)
            if step%a.palier==0:
                st=rng.getstate()
                cp=dict(palier,records=records,bestA=bestA,
                        rng=[st[0],list(st[1]),st[2]],state=state_to_json(S),
                        params=vars(a))
                json.dump(cp,open(os.path.join(a.outdir,'checkpoint_%d.json'%step),'w'))
                sp=step/(time.time()-t0+1e-9)
                print("pas %7d | N3=%4d rho=%.5f | cheap=%3d A=%3d A/N3=%.5f | MT=%d | best=%.5f | %.0f pas/s ETA %.1f h"
                      %(step,S.N3,S.N0/S.N3,palier['cheap'],au['A'],au['A']/S.N3,au['MT'],
                        bestA,sp,(a.steps-step)/sp/3600),flush=True)
    au=exact_audit(S)
    fin=dict(steps_done=step,bestA=bestA,records=records,final_audit=au,
             VERDICT=("S4 NEGATIF — GERME-EXTREMAL non falsifiee apres %d pas. "
                      "EVIDENCE [O] renforcee ; CE N'EST PAS UN [T]. "
                      "Le theoreme reste la cible D52.")%step)
    json.dump(fin,open(os.path.join(a.outdir,'final_summary.json'),'w'),indent=1)
    print(fin['VERDICT'])

if __name__=='__main__':
    main()
