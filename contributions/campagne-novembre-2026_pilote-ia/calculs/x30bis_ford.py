#!/usr/bin/env python3
"""X-30 (seconde partie), MODELE DE FORD-EISENSTEIN. Prediction scellee : x30bis_demonstration_de_G1_prediction.txt
(SHA-256 28112142...58b6), poussee avant ce calcul (commit e3fb3fc). Programme independant de l'outil de X-27 : aucun import du laboratoire.

Vu d'un constituant p, ses voisins sont les spheres de Ford des entiers d'Eisenstein (fait classique C6). Un sommet alpha/beta (fraction
reduite de Z[omega]) est code par sa matrice hermitienne de rang 1 : (A, C, D) = (norme(alpha), alpha * conj(beta), norme(beta)), qui ne
depend pas de l'unite choisie. nu(u, v) = A_u D_v + D_u A_v - 2 Re(C_u conj(C_v)) = norme du determinant. Un tetraedre : quatre sommets de nu
deux a deux egal a 1. Retournement d'un sommet v dans la face opposee : M' = (somme des trois autres) - M_v.
Une boule x liee a p est une horoboule : diametre 1 posee en xi si elle touche le sommet a l'infini. xi = c0 + c1 * racine(rho), c0 et c1
dans Q(omega), rho rationnel ; nu(x, u) = P + Q racine(rho), compare exactement.

 V4 : q a l'infini, r et s de denominateur de norme 1, 3 ou 4 a distance au plus 3 : types et boules tangentes.
 V6 : cas critique (4,4,4), toutes les bases a distance au plus 7 ; puis tirage de 20 000 cas.
 temoin : controles du programme sur des cas dont la reponse est connue.
 exhaustif normes rayon_sommets rayon_bases : AJOUT NON SCELLE. Toutes les boules hors de l'empilement tangentes a l'infini et a deux sommets
   de la fenetre, toutes les bases a distance bornee : nombre de portes libres.
Usage : python3 x30bis_ford.py V4 | V6 [rayon] | tirage [n] [graine] | temoin | exhaustif nmax rs rb        Claude, 27 novembre 2026."""
import itertools, json, math, random, sys, time
from fractions import Fraction as F

# ---------- entiers d'Eisenstein a + b omega, codes (a, b) ; omega^2 = -1 - omega ----------
def e_add(x, y): return (x[0] + y[0], x[1] + y[1])
def e_sub(x, y): return (x[0] - y[0], x[1] - y[1])
def e_mul(x, y): return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0] - x[1] * y[1])
def e_conj(x): return (x[0] - x[1], -x[1])
def e_norme(x): return x[0] * x[0] - x[0] * x[1] + x[1] * x[1]
def e_re2(x): return 2 * x[0] - x[1]                                   # deux fois la partie reelle
def e_scal(k, x): return (k * x[0], k * x[1])
ZERO, UN, ZETA, I3 = (0, 0), (1, 0), (1, 1), (1, 2)                     # zeta = 1 + omega ; I3 = i racine(3) = 1 + 2 omega
UNITES = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]

def e_divmod(x, y):
    n = e_norme(y); t = e_mul(x, e_conj(y)); q = (round(F(t[0], n)), round(F(t[1], n)))
    return q, e_sub(x, e_mul(q, y))

def e_pgcd_etendu(x, y):
    """(g, s, t) avec s x + t y = g."""
    a, b = x, y; s0, s1, t0, t1 = UN, ZERO, ZERO, UN
    while b != ZERO:
        q, r = e_divmod(a, b); a, b = b, r
        s0, s1 = s1, e_sub(s0, e_mul(q, s1)); t0, t1 = t1, e_sub(t0, e_mul(q, t1))
    return a, s0, t0

# ---------- sommets ----------
def sommet(alpha, beta): return (e_norme(alpha), e_mul(alpha, e_conj(beta)), e_norme(beta))
INF, S0, S1, SZ = sommet(UN, ZERO), sommet(ZERO, UN), sommet(UN, UN), sommet(ZETA, UN)
BASE = tuple(sorted((INF, S0, S1, SZ)))

def nu(u, v): return u[0] * v[2] + u[2] * v[0] - e_re2(e_mul(u[1], e_conj(v[1])))

def retourne(T, v):
    a, b, c = [u for u in T if u != v]
    w = (a[0] + b[0] + c[0] - v[0], e_sub(e_add(e_add(a[1], b[1]), c[1]), v[1]), a[2] + b[2] + c[2] - v[2])
    return tuple(sorted((a, b, c, w)))

def cote(T, v, w):
    """> 0 : w du cote de v par rapport a la face opposee a v ; 0 : sur le plan ; < 0 : de l'autre cote."""
    return sum(nu(u, w) for u in T if u != v) - 2 * nu(v, w)

def separe(T, v, B):
    return any(cote(T, v, w) < 0 for w in B)

def tetraedre_contenant(alpha, beta):
    g, s, t = e_pgcd_etendu(alpha, beta)                               # s alpha + t beta = g, unite
    assert e_norme(g) == 1
    gam, dlt = e_sub(ZERO, t), s                                       # alpha dlt - beta gam = g
    u, e = (alpha, beta), (gam, dlt)
    T = [sommet(*u), sommet(*e), sommet(e_add(u[0], e[0]), e_add(u[1], e[1])),
         sommet(e_add(u[0], e_mul(ZETA, e[0])), e_add(u[1], e_mul(ZETA, e[1])))]
    assert all(nu(a, b) == 1 for a, b in itertools.combinations(T, 2))
    return tuple(sorted(T))

def porte(c_vec, B):
    """Le tetraedre contenant le sommet c le plus proche de B : aucun mur passant par c ne le separe de B. c_vec = (alpha, beta)."""
    T = tetraedre_contenant(*c_vec); c = sommet(*c_vec)
    for _ in range(100000):
        v = next((v for v in T if v != c and separe(T, v, B)), None)
        if v is None: return T
        T = retourne(T, v)
    raise RuntimeError('descente sans fin')

def boule(rayon, depart=BASE):
    vus = {depart: 0}; couche = [depart]
    for d in range(1, rayon + 1):
        suiv = []
        for T in couche:
            for v in T:
                U = retourne(T, v)
                if U not in vus: vus[U] = d; suiv.append(U)
        couche = suiv
    return vus

# ---------- reels P + Q racine(rho), complexes de Q(omega) a coefficients fractions ----------
def signe_surd(P, Q, rho):
    """Signe exact de P + Q racine(rho), rho >= 0 rationnel."""
    if Q == 0 or rho == 0: return (P > 0) - (P < 0)
    if P == 0: return (Q > 0) - (Q < 0)
    if (P > 0) == (Q > 0): return 1 if P > 0 else -1
    d = P * P - Q * Q * rho                                             # signes opposes : compare |P| et |Q| racine(rho)
    if d == 0: return 0
    return (1 if P > 0 else -1) if d > 0 else (1 if Q > 0 else -1)

class Horoboule:
    """Boule de diametre 1 posee en xi = c0 + c1 racine(rho) (elle touche le sommet a l'infini)."""
    def __init__(self, c0, c1, rho):
        r = None
        if rho >= 0:
            a, b = F(rho).numerator, F(rho).denominator; ra, rb = math.isqrt(a), math.isqrt(b)
            if ra * ra == a and rb * rb == b: r = F(ra, rb)
        if r is not None: c0 = (c0[0] + r * c1[0], c0[1] + r * c1[1]); c1 = (F(0), F(0)); rho = F(0)
        self.c0, self.c1, self.rho = (F(c0[0]), F(c0[1])), (F(c1[0]), F(c1[1])), F(rho)
        self.n0 = e_norme(self.c0) + self.rho * e_norme(self.c1); self.n1 = e_re2(e_mul(self.c0, e_conj(self.c1)))    # |xi|^2 = n0 + n1 racine(rho)
    def rationnelle(self): return self.rho == 0
    def dans_l_empilement(self): return self.rho == 0 and all(v.denominator == 1 for v in self.c0)
    def nu(self, u):
        """nu(x, u) = P + Q racine(rho) : renvoie (P, Q)."""
        A, C, D = u
        return (D * self.n0 - e_re2(e_mul(e_conj(self.c0), C)) + A, D * self.n1 - e_re2(e_mul(e_conj(self.c1), C)))
    def compare(self, u, K=1):
        """Signe exact de nu(x, u) - K. Chevauchement : < 0 pour K = 1."""
        P, Q = self.nu(u); return signe_surd(P - K, Q, self.rho)
    def flottant(self, u):
        P, Q = self.nu(u); return float(P) + float(Q) * math.sqrt(float(self.rho))

def boules_tangentes(r, s):
    """Les boules de diametre 1 (tangentes au sommet a l'infini) tangentes aux sommets r et s (denominateurs non nuls)."""
    zr = (F(r[1][0], r[2]), F(r[1][1], r[2])); zs = (F(s[1][0], s[2]), F(s[1][1], s[2])); hr, hs = F(1, r[2]), F(1, s[2])
    dz = e_sub(zs, zr); d2 = e_norme(dz)
    if d2 == 0: return []
    t = (d2 + hr - hs) / (2 * d2); E = hr - t * t * d2
    if E < 0: return []
    pied = (zr[0] + t * dz[0], zr[1] + t * dz[1]); c1 = e_mul(I3, dz); rho = E / (3 * d2)
    if E == 0: return [Horoboule(pied, (0, 0), 0)]
    return [Horoboule(pied, c1, rho), Horoboule(pied, e_scal(-1, c1), rho)]

# ---------- enumeration des sommets ----------
def sommets_fenetre(normes, rayon):
    """Sommets alpha/beta reduits, norme(beta) dans normes, |alpha/beta| <= rayon. Renvoie {cle: (alpha, beta)}."""
    out = {}; R = range(-12, 13)
    betas = [b for b in itertools.product(R, R) if e_norme(b) in normes]
    for beta in betas:
        nb = e_norme(beta); m = int(rayon * math.sqrt(nb)) + 2
        for alpha in itertools.product(range(-2 * m, 2 * m + 1), repeat=2):
            if e_norme(alpha) > rayon * rayon * nb: continue
            g, _, _ = e_pgcd_etendu(alpha, beta)
            if e_norme(g) != 1: continue
            out.setdefault(sommet(alpha, beta), (alpha, beta))
    return out

def type_de(q, r, s): return tuple(sorted((nu(q, r), nu(q, s), nu(r, s))))

# ---------- V4 ----------
def partie_V4():
    t0 = time.time(); S = sommets_fenetre({1, 3, 4}, 3); L = sorted(S)
    par_norme = {n: sum(1 for u in L if u[2] == n) for n in (1, 3, 4)}
    types = {}; ex = []; lies_aux_deux = dict(triplets=0, boules=0, hors=0)
    interdits = {(1, 3, 3), (1, 4, 4), (3, 3, 4), (3, 4, 4)}; viol = dict(a=0, b=0, c=0, d=0)
    for r, s in itertools.combinations(L, 2):
        n = nu(r, s)
        if n not in (1, 3, 4): continue
        ty = type_de(INF, r, s); B = boules_tangentes(r, s); dedans = sum(1 for x in B if x.dans_l_empilement()); hors = len(B) - dedans
        # un des trois lie aux deux autres ?
        k = [nu(INF, r), nu(INF, s), n]; lie2 = (k[0] == 1 and k[1] == 1) or (k[0] == 1 and k[2] == 1) or (k[1] == 1 and k[2] == 1)
        e = types.setdefault(ty, dict(triplets=0, sans_boule=0, boules=0, dans_l_empilement=0, hors=0, un_contact_lie_aux_deux_autres=0))
        e['triplets'] += 1; e['boules'] += len(B); e['dans_l_empilement'] += dedans; e['hors'] += hors; e['sans_boule'] += (len(B) == 0); e['un_contact_lie_aux_deux_autres'] += lie2
        if lie2: lies_aux_deux['triplets'] += 1; lies_aux_deux['boules'] += len(B); lies_aux_deux['hors'] += hors
        if ty in interdits: viol['a'] += 1
        if ty in ((3, 3, 3), (1, 3, 4)) and hors: viol['b'] += 1
        if ty == (4, 4, 4) and not (len(B) == 2 and dedans == 1): viol['c'] += 1
        if hors and not lie2 and ty != (4, 4, 4):
            viol['d'] += 1
            if len(ex) < 5: ex.append(dict(type=list(ty), r=[list(S[r][0]), list(S[r][1])], s=[list(S[s][0]), list(S[s][1])]))
    print(json.dumps(dict(partie='V4', sommets=len(L), par_norme_du_denominateur=par_norme,
                          types={str(k): v for k, v in sorted(types.items())}, un_contact_lie_aux_deux_autres=lies_aux_deux,
                          type_444_present=(types.get((4, 4, 4), {}).get('triplets', 0) > 0), violations=viol, exemples_de_violation=ex,
                          duree_s=round(time.time() - t0, 1))), flush=True)

# ---------- (H) : pour une boule x et trois contacts, une base B : une des trois portes est-elle chevauchee ? ----------
def portes_libres(x, contacts, B):
    """Pour chaque contact (alpha, beta) : sa porte par rapport a B, et True si x ne chevauche aucun de ses trois autres sommets."""
    out = []
    for cv in contacts:
        c = sommet(*cv); T = porte(cv, B); out.append((T, all(x.compare(u) >= 0 for u in T if u != c)))
    return out

def controle_T16(x, contacts, B, etat):
    """Pour chaque porte libre et chaque sommet w de B autre que le contact : nu(x, w) >= (3/4) nu(c, w), egalite seulement si x est dans l'empilement."""
    for cv, (T, libre) in zip(contacts, portes_libres(x, contacts, B)):
        if not libre: continue
        c = sommet(*cv)
        for w in B:
            if w == c: continue
            P, Q = x.nu(w); sg = signe_surd(P - F(3, 4) * nu(c, w), Q, x.rho); etat['t16_triplets'] += 1
            if sg < 0 or (sg == 0 and not x.dans_l_empilement()): etat['t16_exceptions'] += 1
            if sg == 0: etat['t16_egalites'] += 1

def partie_V6(rayon):
    t0 = time.time(); bases = boule(rayon)
    # triangle (a, b, c) = (zeta, 0, 1) ; x au milieu de bc ; r et s aux milieux de ab et ac
    x = Horoboule((F(1, 2), F(0)), (0, 0), 0); q, r, s = (UN, ZERO), (ZETA, (2, 0)), (e_add(UN, ZETA), (2, 0)); contacts = [q, r, s]
    cles = [sommet(*c) for c in contacts]
    assert all(x.compare(c) == 0 for c in cles) and not x.dans_l_empilement() and type_de(*cles) == (4, 4, 4)
    rep = {0: 0, 1: 0, 2: 0, 3: 0}; ex = []; etat = dict(t16_triplets=0, t16_exceptions=0, t16_egalites=0); par_distance = {}
    for B, d in bases.items():
        pl = portes_libres(x, contacts, B); k = sum(1 for _, libre in pl if libre); rep[k] += 1
        e = par_distance.setdefault(d, [0, 0]); e[0] += 1; e[1] += (k == 3)
        controle_T16(x, contacts, B, etat)
        if k == 3 and len(ex) < 3: ex.append([[u[0], list(u[1]), u[2]] for u in B])
    print(json.dumps(dict(partie='V6_cas_critique', rayon=rayon, bases=len(bases), bases_par_nombre_de_portes_libres=rep,
                          exceptions=rep[3], exemples=ex, par_distance={str(k): v for k, v in sorted(par_distance.items())}, **etat,
                          duree_s=round(time.time() - t0, 1))), flush=True)

def marche(pas, rng):
    T = BASE
    for _ in range(pas): T = retourne(T, rng.choice(T))
    return T

def partie_tirage(n, graine):
    t0 = time.time(); rng = random.Random(graine); S = sommets_fenetre(set(range(1, 14)), 2.5); L = sorted(S)
    rep = {0: 0, 1: 0, 2: 0, 3: 0}; ex = []; faits = 0; essais = 0; irr = 0; types = {}
    etat = dict(t16_triplets=0, t16_exceptions=0, t16_egalites=0)
    while faits < n:
        essais += 1; r, s = rng.sample(L, 2); Bx = [x for x in boules_tangentes(r, s) if not x.dans_l_empilement()]
        if not Bx: continue
        x = rng.choice(Bx); B = marche(rng.randint(1, 30), rng); contacts = [(UN, ZERO), S[r], S[s]]
        pl = portes_libres(x, contacts, B); k = sum(1 for _, libre in pl if libre); rep[k] += 1; faits += 1; irr += (not x.rationnelle())
        ty = type_de(INF, r, s); types[ty] = types.get(ty, 0) + 1
        controle_T16(x, contacts, B, etat)
        if k == 3 and len(ex) < 3: ex.append(dict(r=[list(S[r][0]), list(S[r][1])], s=[list(S[s][0]), list(S[s][1])], base=[[u[0], list(u[1]), u[2]] for u in B]))
    plus = sorted(types.items(), key=lambda kv: -kv[1])[:8]
    print(json.dumps(dict(partie='V6_tirage', graine=graine, cas=faits, essais=essais, sommets_disponibles=len(L), boules_irrationnelles=irr,
                          cas_par_nombre_de_portes_libres=rep, exceptions=rep[3], exemples=ex, types_les_plus_frequents={str(k): v for k, v in plus},
                          **etat, duree_s=round(time.time() - t0, 1))), flush=True)

def partie_exhaustif(nmax, rs, rb):
    t0 = time.time(); S = sommets_fenetre(set(range(1, nmax + 1)), rs); L = sorted(S); bases = boule(rb)
    rep = {0: 0, 1: 0, 2: 0, 3: 0}; ex = []; boules = 0; irr = 0; etat = dict(t16_triplets=0, t16_exceptions=0, t16_egalites=0); rapport_min = None
    for r, s in itertools.combinations(L, 2):
        for x in boules_tangentes(r, s):
            if x.dans_l_empilement(): continue
            boules += 1; irr += (not x.rationnelle()); contacts = [(UN, ZERO), S[r], S[s]]
            for B in bases:
                pl = portes_libres(x, contacts, B); k = sum(1 for _, libre in pl if libre); rep[k] += 1
                if k == 3 and len(ex) < 3: ex.append(dict(r=[list(S[r][0]), list(S[r][1])], s=[list(S[s][0]), list(S[s][1])], base=[[u[0], list(u[1]), u[2]] for u in B]))
                for cv, (T, libre) in zip(contacts, pl):
                    if not libre: continue
                    c = sommet(*cv)
                    for w in B:
                        if w == c: continue
                        P, Q = x.nu(w); k3 = F(3, 4) * nu(c, w); sg = signe_surd(P - k3, Q, x.rho); etat['t16_triplets'] += 1
                        if sg <= 0: etat['t16_exceptions'] += 1
                        v = x.flottant(w) / nu(c, w); rapport_min = v if rapport_min is None else min(rapport_min, v)
    print(json.dumps(dict(partie='exhaustif_non_scelle', norme_max=nmax, rayon_sommets=rs, rayon_bases=rb, sommets=len(L), bases=len(bases), boules_hors_de_l_empilement=boules,
                          irrationnelles=irr, couples_boule_base_par_nombre_de_portes_libres=rep, exceptions=rep[3], exemples=ex, **etat,
                          plus_petit_rapport_nu_x_w_sur_nu_c_w=rapport_min, duree_s=round(time.time() - t0, 1))), flush=True)

# ---------- temoins ----------
def partie_temoin():
    out = {}
    # 1. arithmetique : omega^3 = 1, zeta^6 = 1, norme multiplicative, pgcd etendu
    w = (0, 1); out['omega_cube'] = e_mul(w, e_mul(w, w)) == UN
    z = UN
    for _ in range(6): z = e_mul(z, ZETA)
    out['zeta_puissance_6'] = z == UN
    rng = random.Random(1); ok = True
    for _ in range(2000):
        a, b = (rng.randint(-30, 30), rng.randint(-30, 30)), (rng.randint(-30, 30), rng.randint(-30, 30))
        ok &= e_norme(e_mul(a, b)) == e_norme(a) * e_norme(b)
        if a != ZERO or b != ZERO:
            g, s, t = e_pgcd_etendu(a, b); ok &= e_add(e_mul(s, a), e_mul(t, b)) == g
    out['norme_et_pgcd'] = bool(ok)
    # 2. la base : quatre sommets lies deux a deux ; le retourne de l'infini est le centre du triangle, de denominateur de norme 3
    out['base_liee'] = all(nu(a, b) == 1 for a, b in itertools.combinations(BASE, 2))
    T = retourne(BASE, INF); g = [u for u in T if u not in BASE][0]; out['retourne_de_l_infini'] = [g[0], list(g[1]), g[2]]
    out['retourne_est_le_centre_du_triangle'] = (g == sommet(ZETA, (2, 1)))        # (1 + zeta)/3 = zeta/(2 + omega), denominateur de norme 3
    out['nu_entre_un_sommet_et_son_retourne'] = nu(INF, g)
    # 3. tout tetraedre a distance <= 5 de la base a ses sommets lies deux a deux ; croissance de la boule
    Bo = boule(5); out['tetraedres_a_distance_au_plus_5'] = len(Bo)
    out['croissance'] = [sum(1 for d in Bo.values() if d == k) for k in range(6)]
    out['tous_lies'] = all(nu(a, b) == 1 for T in Bo for a, b in itertools.combinations(T, 2))
    # 4. porte : la porte d'un sommet de B par rapport a B est B ; la porte par rapport a B est a la plus petite distance de B (controle par parcours)
    ok = True; ecarts = 0; S = sommets_fenetre({1, 3, 4, 7}, 1.5); dist_par_base = {}
    for B in list(Bo)[:40]:
        D = boule(6, B)
        for cle, cv in list(S.items())[:60]:
            T = porte(cv, B)
            cont = [d for U, d in D.items() if cle in U]
            if cont:
                dmin = min(cont)
                if T not in D or D[T] != dmin or sum(1 for U, d in D.items() if cle in U and d == dmin) != 1: ecarts += 1
    out['porte_egale_au_plus_proche_ecarts'] = ecarts
    # 5. temoin positif de (H) : boule DANS l'empilement, portes libres possibles ; temoin negatif : une boule hors de l'empilement tangente a deux contacts seulement
    x_in = Horoboule((F(2), F(1)), (0, 0), 0); out['boule_entiere_dans_l_empilement'] = x_in.dans_l_empilement()
    # boule de diametre 1 posee en un point entier : elle touche l'infini et ses six voisins du reseau
    vo = [sommet(e_add((2, 1), u), UN) for u in UNITES]; out['boule_entiere_touche_ses_six_voisins'] = all(x_in.compare(v) == 0 for v in vo)
    # temoin negatif : deux contacts seulement (l'infini et le sommet 0). Il doit exister des bases ou les DEUX portes sont libres :
    # l'enonce a besoin de trois voisins. xi = 1/4 + (i racine 3) racine(5/16), |xi|^2 = 1/16 + 15/16 = 1, hors du reseau.
    x2 = Horoboule((F(1, 4), F(0)), (F(1), F(2)), F(5, 16))
    c2 = [(UN, ZERO), (ZERO, UN)]; out['temoin_deux_contacts_tangence'] = [x2.compare(sommet(*c)) for c in c2]
    libres2 = 0
    for B in Bo:
        if all(l for _, l in portes_libres(x2, c2, B)): libres2 += 1
    out['temoin_deux_contacts_bases_ou_les_deux_portes_sont_libres'] = libres2
    print(json.dumps(dict(partie='temoin', **out)), flush=True)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'V4': partie_V4()
    elif a[0] == 'V6': partie_V6(int(a[1]) if len(a) > 1 else 7)
    elif a[0] == 'tirage': partie_tirage(int(a[1]) if len(a) > 1 else 20000, int(a[2]) if len(a) > 2 else 20261127)
    elif a[0] == 'temoin': partie_temoin()
    elif a[0] == 'exhaustif': partie_exhaustif(int(a[1]), float(a[2]), int(a[3]))
