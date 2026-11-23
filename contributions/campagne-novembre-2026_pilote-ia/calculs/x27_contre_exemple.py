#!/usr/bin/env python3
"""X-27, CONTRE-EXEMPLE A K20 -- trouve par le raisonnement APRES les essais predits (aucun essai predit ne l'avait vu), puis verifie ici en arithmetique exacte.
K20 disait : quel que soit l'ordre des naissances, toute place admissible appartient a l'empilement. C'est FAUX.

L'IDEE. Deux constituants lies p et q de l'empilement. La boule x = (q - 2p)/3 touche p au meme point que q, mais elle est plus grosse que q : elle contient q.
Elle chevauche q et toute la couche des constituants lies a la fois a p et a q. Elle TOUCHE les constituants loges sous cette couche, contre p, dans le creux
de trois constituants de la couche (un par creux). Si un tissu contient p et trois de ces constituants-la, SANS contenir q ni aucun constituant de la couche,
alors x est une place admissible (elle touche son parent p et trois voisins de p, elle ne chevauche rien) et x n'est PAS dans l'empilement.
Un tel tissu existe : il suffit de ne jamais faire naitre les gros, et de passer d'un creux a l'autre par les petits. Toutes ses naissances sont des naissances
dans la cellule (la plus stricte des naissances heritees et fixees).

ICI : germe e0..e4 ; p = e0 ; q = (10, 8, 7, -2, -2), constituant de l'empilement (controle par la descente) ; x = (8, 8, 7, -2, -2)/3.
Parties :
 toit      : recherche des chemins (tuiles de cinq constituants tous lies, contenant p, que x ne chevauche pas), rejeu des naissances dans Tissu27 (l'outil des
             parties A, B, C, importe tel quel), et controle direct, independant de Tissu27, que x est une place admissible hors de l'empilement.
 court     : le plus petit contre-exemple trouve. On s'arrete a la premiere place hors de l'empilement que l'outil voit pendant le rejeu (une AUTRE boule que x,
             non cherchee), on retire les naissances dont on peut se passer, puis controle direct et controle de geometrie ordinaire (deux plans, des spheres).
 symetrie d: TOUS les tissus atteignables en d naissances, a la symetrie du germe pres (120 permutations) : borne inferieure du nombre de naissances d'un contre-exemple.
Usage : python3 x27_contre_exemple.py toit | court | symetrie d [budget_s]
Meme outil que x27_mitose_avec_heritage.py.     Claude, 23 novembre 2026."""
import collections, itertools, json, os, sys, time
from fractions import Fraction as F
import x27_mitose_avec_heritage as m

ICI = os.path.dirname(os.path.abspath(__file__))
prod = m.prod
G5 = tuple(m.G5)
P_ = (1, 0, 0, 0, 0)                      # le parent p
Q_ = (10, 8, 7, -2, -2)                   # le constituant q, lie a p, qui ne doit jamais naitre
X3 = (8, 8, 7, -2, -2)                    # 3 fois la boule x = (q - 2p)/3
X_ = tuple(F(v, 3) for v in X3)


def retournements(D):
    """Les cinq naissances dans la cellule possibles a partir d'une tuile (cinq constituants tous lies) : l'autre cote de chacune de ses cinq cellules."""
    for i in range(5):
        yield i, tuple(sum(D[j][k] for j in range(5) if j != i) - D[i][k] for k in range(5))


def taille(u):
    """Pour un voisin u de p : (1 - <q,u>)/2. Vaut 1 pour la couche liee a p et a q, 3 pour les constituants que x touche ; x chevauche u des que taille < 3."""
    return (1 - prod(Q_, u)) // 2


def chemins(pmax=18, tmax=25):
    """Parcours en largeur des tuiles contenant p, atteintes depuis le germe par naissances dans la cellule, sans jamais faire naitre un constituant que x chevauche.
    Rend, pour chaque constituant touche par x ainsi atteint, la suite des naissances qui y mene."""
    G = tuple(sorted(G5)); vus = {frozenset(G): (None, None)}; file = collections.deque([(G, 0)]); contacts = {}
    while file:
        D, d = file.popleft()
        if d >= pmax: continue
        for i, nv in retournements(D):
            if D[i] == P_: continue
            v = prod(X3, nv)
            if v > -3 or taille(nv) > tmax: continue                      # v > -3 : x chevaucherait le nouveau-ne
            E = tuple(sorted(D[:i] + D[i + 1:] + (nv,))); fe = frozenset(E)
            if fe in vus: continue
            vus[fe] = (frozenset(D), nv); file.append((E, d + 1))
            if v == -3 and nv not in contacts: contacts[nv] = fe
    out = {}
    for c, fe in contacts.items():
        ch = []; f = fe
        while vus[f][0] is not None: ch.append(vus[f][1]); f = vus[f][0]
        out[c] = ch[::-1]
    return len(vus), out


def rejoue(naissances, verbeux=True):
    """Rejoue les naissances dans Tissu27. A chaque naissance : la place doit etre une place admissible DE L'EMPILEMENT, connue de l'outil a cet instant ;
    on note si elle est le cote d'une cellule, et le moment ou l'outil voit apparaitre une place admissible hors de l'empilement."""
    T = m.Tissu27(list(G5)); journal = []; premiere_hors = None
    for k, u in enumerate(naissances, 1):
        assert u in T.places and T.vues[u] == 'empilement', ('pas une place admissible de l\'empilement', k, u)
        assert prod(X3, u) <= -3, ('x chevaucherait', u)
        cont = sorted(T.places[u][1]); cellule = not T.sans_cellule(u)
        T.naissance(u)
        if premiere_hors is None and T.hors: premiere_hors = k
        journal.append(dict(rang=k, nouveau_ne=list(u), touche=len(cont), cote_d_une_cellule=cellule, x_touche_le_nouveau_ne=(prod(X3, u) == -3), places_hors_empilement_vues=len(T.hors)))
        if verbeux: print(json.dumps(journal[-1]), flush=True)
    return T, journal, premiere_hors


def controle_direct(S, x=None):
    """Independant de Tissu27 : la boule x (fractions) est-elle une place admissible du tissu S, hors de l'empilement ? Tout en entiers et fractions."""
    x = X_ if x is None else tuple(F(v) for v in x)
    norme = prod(x, x)
    produits = {u: prod(x, u) for u in S}
    chevauche = [list(u) for u, v in produits.items() if v > -1]
    touche = [u for u, v in produits.items() if v == -1]
    etoiles = []
    for p in touche:
        voisins = [u for u in touche if u != p and prod(p, u) == -1]
        for t in itertools.combinations(voisins, 3):
            quad = (p,) + t
            gram = [[prod(a, b) for b in quad] for a in quad]
            if m.det(gram) != 0: etoiles.append(dict(parent=list(p), voisins_du_parent=[list(u) for u in t], determinant_de_gram=str(m.det(gram)),
                                                     liens_entre_les_trois_voisins=sum(1 for a, b in itertools.combinations(t, 2) if prod(a, b) == -1)))
    entiere = all(v.denominator == 1 for v in x)
    return dict(x=[str(v) for v in x], norme_de_x=str(norme), x_a_des_coordonnees_entieres=entiere,
                x_dans_l_empilement=(entiere and m.dans_l_empilement(tuple(int(v) for v in x))),
                constituants=len(S), constituants_chevauches_par_x=chevauche, constituants_touches_par_x=[list(u) for u in touche],
                produit_le_plus_proche_du_contact_parmi_les_autres=str(max((v for v in produits.values() if v != -1), default=None)),
                etoiles_parent_et_trois_voisins_independants=etoiles, x_est_une_place_admissible=(norme == 1 and not chevauche and bool(etoiles)))


def controle_euclidien(S, x):
    """Controle de geometrie ordinaire, sans le produit de Lorentz : le germe est realise par deux plans paralleles (e0 : z <= -1 ; e1 : z >= 1) et trois spheres
    de rayon 1 posees entre eux, toutes liees. Chaque constituant et la boule x deviennent une sphere de l'espace ordinaire (centre, rayon) ; on controle les
    distances entre centres. Nombres flottants : ce controle garde contre une erreur de signe ou d'orientation, l'exactitude vient du controle direct."""
    import math
    r3 = 2 / math.sqrt(3)
    def sph(c): return (c[0], c[1], c[2], (c[0] ** 2 + c[1] ** 2 + c[2] ** 2 - 2) / 2, (c[0] ** 2 + c[1] ** 2 + c[2] ** 2) / 2)      # sphere de rayon 1 centree en c
    W = [(0.0, 0.0, -1.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0, 1.0)] + [sph((r3 * math.cos(a), r3 * math.sin(a), 0.0)) for a in (0, 2 * math.pi / 3, 4 * math.pi / 3)]
    def L(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3] - a[4] * b[4]
    gram_ok = all(abs(L(W[i], W[j]) - (1 if i == j else -1)) < 1e-12 for i in range(5) for j in range(5))
    def image(u): return tuple(sum(float(u[k]) * W[k][c] for k in range(5)) for c in range(5))
    def boule(u):
        w = image(u); courb = w[4] - w[3]
        return None if abs(courb) < 1e-12 else ((w[0] / courb, w[1] / courb, w[2] / courb), 1 / courb)
    B = {u: boule(u) for u in S}; bx = boule(x)
    spheres = {u: b for u, b in B.items() if b is not None}
    pire = min(math.dist(a[0], b[0]) - a[1] - b[1] for (u, a), (v, b) in itertools.combinations(spheres.items(), 2))
    entre_plans = all(b[1] > 0 and abs(b[0][2]) + b[1] <= 1 + 1e-9 for b in spheres.values())
    ecarts = {u: math.dist(bx[0], b[0]) - bx[1] - b[1] for u, b in spheres.items()}
    return dict(germe_realise=gram_ok, plans=[list(u) for u, b in B.items() if b is None], spheres=len(spheres), toutes_entre_les_deux_plans=entre_plans,
                plus_petit_ecart_entre_deux_constituants=abs(round(pire, 9)) if abs(pire) < 1e-9 else round(pire, 9),
                x_centre=[round(v, 9) for v in bx[0]], x_rayon=round(bx[1], 12), x_touche_les_deux_plans=(abs(bx[0][2]) < 1e-9 and abs(bx[1] - 1) < 1e-9),
                x_touche=[list(u) for u, e in ecarts.items() if abs(e) < 1e-9], x_chevauche=[list(u) for u, e in ecarts.items() if e < -1e-9],
                plus_petit_ecart_de_x_aux_autres=round(min(e for e in ecarts.values() if abs(e) >= 1e-9), 9),
                positions={'x': [round(bx[0][0], 6), round(bx[0][1], 6), round(bx[0][2], 6), round(bx[1], 6)],
                           'constituants': [[list(u)] + [round(v, 6) for v in b[0]] + [round(b[1], 6)] for u, b in spheres.items()]})


def reduit(naissances, cle):
    """Retire, de la fin vers le debut, toute naissance dont on peut se passer : le rejeu doit rester valide et la place cle doit rester admissible a la fin."""
    L = list(naissances)
    for u in reversed(list(naissances)):
        essai = [v for v in L if v != u]
        T = m.Tissu27(list(G5)); ok = True
        for v in essai:
            if v not in T.places or T.vues[v] != 'empilement': ok = False; break
            T.naissance(v)
        if ok and cle in T.places: L = essai
    return L


def cle_fractions(place):
    return tuple(F(v) for v in place)


def partie_toit():
    r = dict(p=list(P_), q=list(Q_), q_dans_l_empilement=m.dans_l_empilement(Q_), norme_de_q=prod(Q_, Q_), p_et_q_lies=(prod(P_, Q_) == -1),
             x=[str(v) for v in X_], trois_x=list(X3), norme_de_trois_x=prod(X3, X3),
             trois_fois_x_avec_le_germe=[prod(X3, g) for g in G5], trois_fois_x_avec_q=prod(X3, Q_))
    print(json.dumps(r), flush=True)
    n, ch = chemins()
    touches_lies_a_p = sorted((len(c), u) for u, c in ch.items() if prod(u, P_) == -1)
    r.update(tuiles_parcourues=n, constituants_touches_par_x_atteints=[dict(constituant=list(u), naissances=k) for k, u in touches_lies_a_p])
    naissances = []
    for k, u in touches_lies_a_p[:2]:
        for v in ch[u]:
            if v not in naissances: naissances.append(v)
    T, journal, premiere = rejoue(naissances)
    r.update(naissances=len(naissances), liste_des_naissances=[list(u) for u in naissances], toutes_cote_d_une_cellule=all(j['cote_d_une_cellule'] for j in journal), journal=journal,
             rang_de_la_premiere_place_hors_empilement_vue_par_l_outil=premiere,
             outil_x_est_une_place=(X_ in T.places), outil_classement_de_x=T.vues.get(X_),
             outil_contacts_de_x=[list(T.S[i]) for i in sorted(T.places[X_][1])] if X_ in T.places else None,
             outil_places_hors_empilement=T.hors, outil_places_admissibles_a_la_fin=len(T.places), outil_bilan_des_places_vues=m.bilan_des_vues(T.vues),
             controle_direct_de_x=controle_direct(list(T.S)),
             controle_direct_des_places_hors_empilement=[controle_direct([tuple(u) for u in T.S[:h['constituants']]], cle_fractions(h['place'])) for h in T.hors],
             plus_grande_coordonnee=max(max(abs(v) for v in u) for u in T.S), liens=sum(len(a) for a in T.adj) // 2)
    print(json.dumps({k: v for k, v in r.items() if k != 'journal'}), flush=True)
    json.dump(r, open(os.path.join(ICI, 'x27_contre_exemple_toit.json'), 'w'), indent=1)
    return r


def partie_court():
    """Le plus petit contre-exemple trouve : on s'arrete a la premiere place hors de l'empilement que l'outil voit, puis on retire les naissances inutiles."""
    n, ch = chemins()
    touches_lies_a_p = sorted((len(c), u) for u, c in ch.items() if prod(u, P_) == -1)
    naissances = []
    for k, u in touches_lies_a_p[:2]:
        for v in ch[u]:
            if v not in naissances: naissances.append(v)
    T, journal, premiere = rejoue(naissances, verbeux=False)
    naissances = naissances[:premiere]
    T, journal, premiere = rejoue(naissances, verbeux=False)
    cle = cle_fractions(T.hors[0]['place']); assert cle in T.places
    avant = len(naissances); naissances = reduit(naissances, cle)
    T, journal, premiere = rejoue(naissances)
    assert cle in T.places and T.vues[cle] != 'empilement'
    S = [tuple(u) for u in T.S]
    cotes_libres = sorted(k for k in T.places if T.vues[k] == 'empilement' and not T.sans_cellule(k) and prod(cle, k) > -1)
    r = dict(naissances_avant_reduction=avant, naissances=len(naissances), liste_des_naissances=[list(u) for u in naissances],
             toutes_cote_d_une_cellule=all(j['cote_d_une_cellule'] for j in journal), journal=journal, constituants=len(S), liens=sum(len(a) for a in T.adj) // 2,
             place_hors_empilement=[str(v) for v in cle], outil_classement=T.vues[cle], outil_contacts=[list(T.S[i]) for i in sorted(T.places[cle][1])],
             outil_places_admissibles_a_la_fin=len(T.places), outil_bilan_des_places_vues=m.bilan_des_vues(T.vues),
             cotes_libres_de_cellule_que_la_place_chevauche=[list(k) for k in cotes_libres],
             controle_direct=controle_direct(S, cle), controle_euclidien=controle_euclidien(S, cle))
    print(json.dumps({k: v for k, v in r.items() if k not in ('journal', 'controle_euclidien')}), flush=True)
    print(json.dumps({k: v for k, v in r['controle_euclidien'].items() if k != 'positions'}), flush=True)
    json.dump(r, open(os.path.join(ICI, 'x27_contre_exemple_court.json'), 'w'), indent=1)
    return r


# ---------------------------------------------------------------- tous les tissus, a la symetrie du germe pres
PERMS = list(itertools.permutations(range(5)))


def canon(etat):
    """Forme canonique d'un ensemble de constituants nes (hors germe) sous les 120 permutations des coordonnees (elles fixent le germe)."""
    return min(tuple(sorted(tuple(u[s] for s in p) for u in etat)) for p in PERMS)


def partie_symetrie(dmax, budget_s=3000):
    t0 = time.time(); niveau = {()}; out = []; hors = []
    for d in range(dmax + 1):
        suivant = set(); nb_places = 0; classes = {}; faits = 0
        for etat in niveau:
            if time.time() - t0 > budget_s: break
            if len(m.CACHE) > 1500000: m.CACHE.clear()
            T = m.Tissu27(list(G5) + list(etat)); faits += 1
            for cle, (pl, cont) in T.places.items():
                nb_places += 1; c = T.vues[cle]; classes[c] = classes.get(c, 0) + 1
                if c == 'empilement':
                    if d < dmax: suivant.add(canon(etat + (pl.coords,)))
                elif len(hors) < 20: hors.append(dict(naissances=d, tissu=[list(u) for u in etat], classe=c, place=[str(v) for v in pl.coords] if pl.coords is not None else [round(float(v), 9) for v in pl.xf], touche=[list(T.S[i]) for i in sorted(cont)]))
        r = dict(naissances=d, tissus_a_symetrie_pres=len(niveau), tissus_examines=faits, complet=(faits == len(niveau)), places_admissibles=nb_places, places_par_classe=classes, duree_s=round(time.time() - t0, 1))
        out.append(r); print(json.dumps(r), flush=True)
        if faits < len(niveau): break
        niveau = suivant
    res = dict(niveaux=out, places_hors_de_l_empilement=hors)
    json.dump(res, open(os.path.join(ICI, 'x27_contre_exemple_symetrie_%d.json' % dmax), 'w'), indent=1)
    return res


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'toit': partie_toit()
    elif mode == 'court': partie_court()
    elif mode == 'symetrie': partie_symetrie(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 3000)
