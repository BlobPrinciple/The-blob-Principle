#!/usr/bin/env python3
"""X-25, partie A -- la naissance dans la cellule sous la lecture de contact, en arithmetique exacte (entiers et fractions).
Lectures posees : C1 un lien est un contact ; C2 un constituant est une boule ronde de S^n ; C5 une cellule est un groupe de n+1 constituants tous lies et le
nouveau-ne, qui les touche tous, nait du cote libre. Germe : n+2 constituants tous lies.
Ecriture : chaque constituant est un vecteur u de R^(n+1,1), <u,u> = 1, donne par ses coordonnees dans la base du germe (matrice de Gram 2I - J) ;
<a,b> = 2 somme(a_i b_i) - somme(a) somme(b). Contact : -1. Separes : < -1. Chevauchement : > -1 (hors le meme constituant).
Naissance : dans une configuration de n+2 constituants tous lies, l'occupant u0 d'un cote de la cellule est remplace par u' = -u0 + (2/(n-1)) x somme de la cellule.
Prediction scellee : x25_naissance_dans_la_cellule_prediction.txt (SHA-256 fab572629dd8c725d1af724ebdf4168a2b73d4577bb0d8db6aabb6384908a709).
Usage : python3 x25_cellule.py [essai]     Claude, 23 novembre 2026."""
import itertools, json, math, os, sys, time
from fractions import Fraction as F
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))


def produit(a, b):
    return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)


def germe(n):
    N = n + 2
    return tuple(tuple(1 if i == j else 0 for j in range(N)) for i in range(N))


def naissance(conf, i, n):
    """Remplace l'element i de la configuration (tuple de n+2 vecteurs) par l'autre constituant qui touche les n+1 autres."""
    f = F(2, n - 1)
    if f.denominator == 1: f = int(f)
    N = n + 2
    s = [sum(conf[j][k] for j in range(N) if j != i) for k in range(N)]
    return tuple(-conf[i][k] + f * s[k] for k in range(N))


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
def paliers(n, G):
    """Naissances synchrones : a chaque palier, tous les cotes libres de toutes les cellules connues sont remplis. Rend constituants, paliers, cellules de naissance."""
    g0 = germe(n)
    spheres = {u: 0 for u in g0}                      # constituant -> palier de naissance
    berceau = {u: set() for u in g0}                  # constituant -> cellules (frozenset) ou il est ne, au palier de sa naissance
    confs = {frozenset(g0)}
    front = [frozenset(g0)]
    histoire = [dict(palier=0, constituants=len(spheres), configurations=1, naissances=0, coincidences=0)]
    for g in range(1, G + 1):
        nouveau = []; nais = 0; coinc = 0
        for D in front:
            Dl = sorted(D)
            for i in range(n + 2):
                x = naissance(Dl, i, n)
                cellule = frozenset(Dl[:i] + Dl[i + 1:])
                if x not in spheres:
                    spheres[x] = g; berceau[x] = {cellule}; nais += 1
                elif spheres[x] == g:
                    berceau[x].add(cellule)             # ne au meme palier par une autre cellule
                D2 = cellule | {x}
                if D2 not in confs:
                    confs.add(D2); nouveau.append(D2)
                    if spheres[x] < g: coinc += 1       # cote libre deja occupe par un constituant plus ancien : fermeture, pas de naissance
        front = nouveau
        histoire.append(dict(palier=g, constituants=len(spheres), configurations=len(confs), naissances=nais, coincidences=coinc))
    return spheres, berceau, confs, histoire


def bilan_des_paires(n, spheres, berceau):
    """Produits deux a deux, exacts. Entiers 64 bits pour n = 2, 3 (controle de depassement), fractions sinon."""
    L = list(spheres)
    m = len(L)
    seed = set(germe(n))
    naiss = set()
    for x, cells in berceau.items():
        for c in cells:
            for y in c: naiss.add(frozenset((x, y)))
    res = dict(constituants=m, contacts=0, contacts_du_germe=0, contacts_de_naissance=0, contacts_de_fermeture=0, chevauchements=0, produit_max_hors_identite=None, exemples=[])
    if n in (2, 3):
        A = np.array(L, dtype=np.int64); assert np.abs(A).max() < 3 * 10 ** 8, 'depassement possible'
        s = A.sum(axis=1)
        pmax = None
        for a in range(0, m, 400):
            P = 2 * A[a:a + 400] @ A.T - np.outer(s[a:a + 400], s)
            for k in range(P.shape[0]): P[k, :a + k + 1] = -10 ** 18          # paires (i < j) seulement
            mx = int(P.max()); pmax = mx if pmax is None else max(pmax, mx)
            ii, jj = np.nonzero(P == -1)
            for i, j in zip(ii, jj):
                x, y = L[a + i], L[j]
                res['contacts'] += 1
                if x in seed and y in seed: res['contacts_du_germe'] += 1
                elif frozenset((x, y)) in naiss: res['contacts_de_naissance'] += 1
                else:
                    res['contacts_de_fermeture'] += 1
                    if len(res['exemples']) < 3: res['exemples'].append(dict(fermeture=[list(x), list(y)], paliers=[spheres[x], spheres[y]]))
            ii, jj = np.nonzero(P > -1)
            res['chevauchements'] += len(ii)
        res['produit_max_hors_identite'] = str(pmax)
    else:
        pmax = None
        for i in range(m):
            for j in range(i + 1, m):
                p = produit(L[i], L[j]); pmax = p if pmax is None else max(pmax, p)
                if p == -1:
                    res['contacts'] += 1
                    x, y = L[i], L[j]
                    if x in seed and y in seed: res['contacts_du_germe'] += 1
                    elif frozenset((x, y)) in naiss: res['contacts_de_naissance'] += 1
                    else: res['contacts_de_fermeture'] += 1
                elif p > -1:
                    res['chevauchements'] += 1
                    if len(res['exemples']) < 3: res['exemples'].append(dict(chevauchement=[[str(v) for v in L[i]], [str(v) for v in L[j]]], produit=str(p), paliers=[spheres[L[i]], spheres[L[j]]]))
        res['produit_max_hors_identite'] = str(pmax)
    return res


def anneaux(n, spheres, palier_max):
    """Pour chaque groupe de n constituants tous lies nes au plus tard au palier palier_max : nombre de constituants qui les touchent tous (taille de l'anneau)."""
    L = list(spheres)
    vieux = [u for u in L if spheres[u] <= palier_max]
    tailles = {}
    for K in itertools.combinations(vieux, n):
        if any(produit(a, b) != -1 for a, b in itertools.combinations(K, 2)): continue
        t = sum(1 for x in L if all(produit(x, k) == -1 for k in K))
        tailles[t] = tailles.get(t, 0) + 1
    return {str(k): v for k, v in sorted(tailles.items())}


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
def anneau_exact(n, pas):
    """Anneau autour des n constituants du germe d'indices 2..n+1 : s_0 = u_0, s_1 = u_1, puis chaque naissance remplace l'avant-dernier. Produits <s_0, s_k> exacts."""
    conf = list(germe(n)); s = [conf[0], conf[1]]
    out = []
    i = 0
    for k in range(2, pas + 1):
        x = naissance(conf, i, n); conf[i] = x; s.append(x); i = 1 - i
        out.append(dict(pas=k, naissance=k - 1, produit_avec_s0=str(produit(s[0], x)), produit_avec_s1=str(produit(s[1], x)), produit_avec_le_precedent=str(produit(s[k - 1], x)),
                        formule=str(formule_anneau(n, k))))
    return out


def formule_anneau(n, k):
    """1 - (2(n-1)/(n-2)) (1 - cos(k theta)), cos(theta) = 1/(n-1), par le polynome de Tchebychev, en fractions."""
    if n == 2: return None
    c = F(1, n - 1); t0, t1 = F(1), c
    for _ in range(k - 1): t0, t1 = t1, 2 * c * t1 - t0
    ck = t1 if k >= 1 else t0
    return 1 - F(2 * (n - 1), n - 2) * (1 - ck)


def premier_chevauchement(n, kmax):
    """Recherche exhaustive : toutes les suites d'au plus kmax naissances (une naissance = un cote libre d'une cellule d'une configuration connue).
    Rend le plus petit nombre de naissances apres lequel deux constituants se chevauchent, avec un temoin ; verifie qu'aucun contact n'apparait hors naissance avant."""
    g0 = germe(n)
    etats = {(frozenset(g0), frozenset([frozenset(g0)]))}
    bilan = []
    for k in range(1, kmax + 1):
        suivants = set(); temoin = None; nb_chev = 0; fermetures = 0
        for S, C in etats:
            for D in C:
                Dl = sorted(D)
                for i in range(n + 2):
                    x = naissance(Dl, i, n)
                    if x in S: continue
                    S2 = S | {x}; C2 = C | {frozenset(Dl[:i] + Dl[i + 1:]) | {x}}
                    if (S2, C2) in suivants: continue
                    suivants.add((S2, C2))
                    cel = set(Dl[:i] + Dl[i + 1:])
                    for y in S:
                        p = produit(x, y)
                        if p > -1:
                            nb_chev += 1
                            if temoin is None or p > F(temoin['produit']): temoin = dict(produit=str(p), nouveau_ne=[str(v) for v in x], autre=[str(v) for v in y])
                        elif p == -1 and y not in cel: fermetures += 1
        bilan.append(dict(naissances=k, etats=len(suivants), etats_ou_paires_qui_chevauchent=nb_chev, contacts_hors_naissance=fermetures, temoin=temoin))
        if nb_chev: break
        etats = suivants
    return bilan


def murs(n):
    """Les 2(n+2) murs : constituants du germe u_i et spheres duales d_i des cellules (d_i orthogonal aux u_j, j != i). Produits normalises (carres pour l'irrationnel)."""
    N = n + 2
    Ginv = [[F(1, 2) * ((1 if i == j else 0) - F(1, n)) for j in range(N)] for i in range(N)]
    dd = Ginv[0][0]; dij = Ginv[0][1]
    return dict(duale_duale=str(dij / dd), duale_et_son_occupant_au_carre=str(F(1) / dd), duale_et_constituant_de_sa_cellule='0', constituant_constituant='-1',
                cosh_tau_au_carre=str(F(2 * n, n - 1)), cosh_tau=math.sqrt(2 * n / (n - 1)), tau=math.acosh(math.sqrt(2 * n / (n - 1))),
                angle_entre_duales_en_degres=math.degrees(math.acos(1 / (n - 1))) if n > 2 else 0.0, tours_pour_fermer=(2 * math.pi / math.acos(1 / (n - 1)) if n > 2 else None))


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
def bol_d_entiers(B):
    """n = 3, empilement de Soddy de courbures de germe (-1, 2, 2, 3, 3) : tous les constituants de courbure <= B. Courbure = produit scalaire des coordonnees avec le germe."""
    b0 = (-1, 2, 2, 3, 3)
    assert sum(b0) ** 2 == 3 * sum(x * x for x in b0)
    courb = lambda u: sum(c * b for c, b in zip(u, b0))
    g0 = germe(3)
    vus = {frozenset(g0)}; pile = [tuple(g0)]; spheres = {u: courb(u) for u in g0}
    while pile:
        D = pile.pop()
        for i in range(5):
            x = naissance(D, i, 3); bx = courb(x)
            if bx > B or bx < courb(D[i]): continue           # on ne remonte pas ; les echanges a courbure egale sont permis (germe symetrique)
            D2 = D[:i] + (x,) + D[i + 1:]; f = frozenset(D2)
            if f in vus: continue
            vus.add(f); spheres[x] = bx; pile.append(D2)
    return spheres


def exposant(B):
    sp = bol_d_entiers(B)
    c = np.array(sorted(v for v in sp.values() if v > 0))
    lignes = []
    x = 8
    while x <= B:
        lignes.append(dict(courbure_max=x, constituants=int((c <= x).sum()))); x *= 2
    xs = np.log([l['courbure_max'] for l in lignes]); ys = np.log([l['constituants'] for l in lignes])
    pentes = [float((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])) for i in range(len(xs) - 1)]
    k = [i for i, l in enumerate(lignes) if l['courbure_max'] >= 32]
    p = np.polyfit(xs[k], ys[k], 1)
    return dict(borne=B, constituants=len(sp), comptage=lignes, pentes_successives=pentes, exposant_ajuste_de_32_a_la_borne=float(p[0]), valeur_de_la_litterature=2.473946)


def temps(n, spheres):
    """Lecture lorentzienne, germe symetrique : coordonnee de temps de de Sitter x0 = cot(r) x somme des coordonnees, avec cos(2r) = -1/(n+1) pour le germe
    (n+2 boules egales, deux a deux tangentes). Temps propre tau = asinh(x0). Rend, par palier, le minimum, la mediane et le maximum de tau."""
    c2 = -1.0 / (n + 1); r = 0.5 * math.acos(c2); cot = 1.0 / math.tan(r)
    par = {}
    for u, g in spheres.items(): par.setdefault(g, []).append(math.asinh(cot * float(sum(u))))
    return [dict(palier=g, constituants=len(v), tau_min=min(v), tau_mediane=float(np.median(v)), tau_max=max(v)) for g, v in sorted(par.items())], cot


if __name__ == '__main__':
    essai = len(sys.argv) > 1 and sys.argv[1] == 'essai'
    t0 = time.time(); out = {}
    profondeur = {2: 4, 3: 4, 4: 3, 5: 3} if essai else {2: 8, 3: 7, 4: 4, 5: 4, 6: 3, 7: 3, 8: 3}
    for n, G in profondeur.items():
        sp, ber, confs, hist = paliers(n, G)
        b = bilan_des_paires(n, sp, ber)
        r = dict(rang=n, paliers=hist, paires=b, murs=murs(n), anneau=anneau_exact(n, 8), anneaux_autour_des_groupes_de_n_des_paliers_0_et_1=anneaux(n, sp, 1) if len(sp) < 30000 else None)
        if n >= 4: r['premier_chevauchement'] = premier_chevauchement(n, 4)
        if n in (2, 3): r['temps_de_de_sitter_par_palier'], r['cot_r_du_germe'] = temps(n, sp)
        out['rang_%d' % n] = r
        print('rang', n, '| paliers', [(h['palier'], h['constituants']) for h in hist], '| contacts', b['contacts'], 'dont fermeture', b['contacts_de_fermeture'],
              '| chevauchements', b['chevauchements'], '| produit max', b['produit_max_hors_identite'], '| anneaux', r['anneaux_autour_des_groupes_de_n_des_paliers_0_et_1'], flush=True)
        print('   anneau :', [(a['pas'], a['produit_avec_s0']) for a in r['anneau']], flush=True)
        if n >= 4: print('   premier chevauchement :', [(p['naissances'], p['etats'], p['etats_ou_paires_qui_chevauchent'], p['contacts_hors_naissance'], (p['temoin'] or {}).get('produit')) for p in r['premier_chevauchement']], flush=True)
        print('   murs :', {k: v for k, v in r['murs'].items()}, flush=True)
    if not essai:
        out['exposant_rang_3'] = exposant(128)
        print('exposant :', json.dumps(out['exposant_rang_3']), flush=True)
    out['duree_s'] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(ICI, 'x25_cellule%s.json' % ('_essai' if essai else '')), 'w'), indent=1)
    print('duree', out['duree_s'], 's')
