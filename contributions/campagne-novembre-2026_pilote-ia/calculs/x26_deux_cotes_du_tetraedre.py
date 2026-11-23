#!/usr/bin/env python3
"""X-26 -- les deux cotes du tetraedre : lignees jumelles, miroir, rencontres, dans le tissu de contact de X-25.
Lectures C1, C2, C5 de X-25 (lien = contact ; constituants ronds sans chevauchement ; naissance dans la cellule, regle a la lettre : toutes les cellules de surface
enfantent ensemble, puis fermetures jusqu'a epuisement) et C6 : le depart est UNE cellule (n+1 constituants tous lies) dont les deux cotes sont libres.
Arithmetique exacte en entiers. Base du germe e_0 ... e_{n+1} ; cellule de depart e_0 ... e_n ; sphere miroir w = e_0 + ... + e_n - (n-1) e_{n+1}
(orthogonale a la cellule ; <w,w> = 4 au rang 2, 12 au rang 3) ; miroir R(x) = x - 2 <x,w> w / <w,w>.
Cote A : <u,w> < 0 ; cote B : <u,w> > 0 ; son propre reflet (M) : <u,w> = 0.
Prediction scellee : x26_deux_cotes_du_tetraedre_prediction.txt (SHA-256 1564ba2376f2b7300d3de9a57b1444d2156075d645e8f1f47354bdeb8362fc68).
Usage : python3 x26_deux_cotes_du_tetraedre.py [essai]     Claude, 23 novembre 2026."""
import itertools, json, os, sys, time
import numpy as np
from x25_cellule import germe, produit
from x25bis_naissances_et_fermetures import Tissu, autre_cote

ICI = os.path.dirname(os.path.abspath(__file__))


def miroir_de(n):
    w = tuple([1] * (n + 1) + [-(n - 1)])
    ww = produit(w, w)
    def R(x):
        s = produit(x, w); num = 2 * s
        assert num % ww == 0, (x, s)
        k = num // ww
        return tuple(a - k * b for a, b in zip(x, w))
    return w, ww, R


def tissu_a_deux_cotes(n):
    """Depart : une cellule ; palier 1 : les deux naissances jumelles."""
    T = Tissu(n); g0 = germe(n)
    cellule = frozenset(g0[:n + 1]); e_dernier = g0[n + 1]
    jumeau = autre_cote(cellule, e_dernier, n)
    for u in cellule: T.spheres[u] = 0
    T.spheres[e_dernier] = 1; T.spheres[jumeau] = 1
    k = T.ajoute(cellule | {jumeau}); assert k == 1                       # la cellule de depart devient interieure
    T.B = 2; T.C = 0; T.accole = {}
    return T, tuple(g0[:n + 1]), e_dernier, jumeau


def tous_les_contacts(L):
    """Toutes les paires : contacts (produit -1) et chevauchements (produit > -1)."""
    A = np.array(L, dtype=np.int64); m = len(L); assert np.abs(A).max() < 3 * 10 ** 8
    s = A.sum(axis=1); contacts = set(); chev = 0
    for a in range(0, m, 400):
        P = 2 * A[a:a + 400] @ A.T - np.outer(s[a:a + 400], s)
        for k in range(P.shape[0]): P[k, :a + k + 1] = -10 ** 18
        ii, jj = np.nonzero(P == -1)
        for i, j in zip(ii, jj): contacts.add((a + int(i), int(j)))
        chev += int((P > -1).sum())
    return contacts, chev


def liens_des_configurations(T, idx):
    liens = set()
    for D in T.confs:
        ids = sorted(idx[u] for u in D)
        for e in itertools.combinations(ids, 2): liens.add(e)
    return liens


def releve(T, n, g, cellule0, premiers_nes, w, ww, R, rang2=None, complet=True):
    L = list(T.spheres); m = len(L); idx = {u: i for i, u in enumerate(L)}
    sw = [produit(u, w) for u in L]
    cote = [0 if s == 0 else (-1 if s < 0 else 1) for s in sw]            # -1 : A ; +1 : B ; 0 : M
    nA, nB, nM = cote.count(-1), cote.count(1), cote.count(0)
    r = dict(palier=g, constituants=m, cote_A=nA, cote_B=nB, propre_reflet=nM, configurations=len(T.confs), cellules_de_surface=len(T.surface))
    # J1 : invariance par le miroir
    ens = set(L); images = [R(u) for u in L]
    r['conserve_par_le_miroir'] = all(v in ens for v in images)
    r['miroir_echange_A_et_B'] = all(cote[idx[v]] == -cote[i] for i, v in enumerate(images) if v in ens)
    r['fixes_par_le_miroir'] = sum(1 for u, v in zip(L, images) if u == v)
    # valeurs de <u,w>
    non_nuls = [abs(s) for s in sw if s != 0]
    r['min_abs_produit_avec_w_hors_M'] = min(non_nuls) if non_nuls else None
    r['pgcd_des_produits_avec_w'] = int(np.gcd.reduce(np.array([abs(s) for s in sw if s != 0], dtype=np.int64))) if non_nuls else None
    r['contact_avec_le_miroir'] = sum(1 for s in sw if s * s == ww)      # <u,w>^2 = <w,w> : tangent au miroir
    niveaux = {}
    if non_nuls:
        pas = r['pgcd_des_produits_avec_w']
        for s in sw: niveaux[abs(s) // pas] = niveaux.get(abs(s) // pas, 0) + 1
        r['effectifs_par_niveau'] = {str(k): v for k, v in sorted(niveaux.items())[:12]}; r['niveau_max'] = max(niveaux)
    # liens
    liens = liens_des_configurations(T, idx)
    if complet:
        contacts, chev = tous_les_contacts(L)
        r['contacts_toutes_paires'] = len(contacts); r['chevauchements'] = chev; r['contacts_hors_configurations'] = len(contacts - liens); r['liens_de_configuration_sans_contact'] = len(liens - contacts)
    r['liens'] = len(liens)
    deg = [0] * m
    for a, b in liens: deg[a] += 1; deg[b] += 1
    types = {}
    for a, b in liens:
        t = tuple(sorted((cote[a], cote[b]))); types[t] = types.get(t, 0) + 1
    nom = {-1: 'A', 0: 'M', 1: 'B'}
    r['liens_par_type'] = {nom[t[0]] + nom[t[1]]: v for t, v in sorted(types.items())}
    r['liens_entre_A_et_B'] = types.get((-1, 1), 0)
    # K17 : aucune configuration (donc aucune cellule) ne mele A et B
    r['configurations_melant_A_et_B'] = sum(1 for D in T.confs if {cote[idx[u]] for u in D} >= {-1, 1})
    # J8, J9 : degres
    ordre = sorted(range(m), key=lambda i: -deg[i])
    r['degres_cellule_de_depart'] = [deg[idx[u]] for u in cellule0]
    r['degres_premiers_nes'] = [deg[idx[u]] for u in premiers_nes]
    r['six_plus_grands_degres'] = [deg[i] for i in ordre[:8]]
    seuil4 = sorted(deg, reverse=True)[n]                                 # (n+1)-ieme plus grand degre
    r['cellule_de_depart_en_tete'] = all(deg[idx[u]] >= seuil4 for u in cellule0) and sorted(deg, reverse=True)[n] > sorted(deg, reverse=True)[n + 1] if m > n + 1 else None
    if m > n + 3:
        d_tri = sorted(deg, reverse=True)
        r['premiers_nes_cinquieme_et_sixieme'] = sorted(deg[idx[u]] for u in premiers_nes) == sorted(d_tri[n + 1:n + 3]) and d_tri[n + 2] > d_tri[n + 3]
    r['degre_moyen'] = 2 * len(liens) / m
    # M : les constituants qui sont leur propre reflet
    Ms = [u for u, c in zip(L, cote) if c == 0]
    r['M_derniere_coordonnee_nulle'] = all(u[n + 1] == 0 for u in Ms)
    r['M_paliers_de_naissance'] = {str(k): sum(1 for u in Ms if T.spheres[u] == k) for k in sorted({T.spheres[u] for u in Ms})}
    if n == 3:
        Mi = [idx[u] for u in Ms]; Mset = set(Mi)
        liensM = {(a, b) for a, b in liens if a in Mset and b in Mset}
        r['liens_entre_M'] = len(liensM)
        adjM = {i: set() for i in Mi}
        for a, b in liensM: adjM[a].add(b); adjM[b].add(a)
        k4 = [c for c in itertools.combinations(sorted(Mi), 4) if all(y in adjM[x] for x, y in itertools.combinations(c, 2))] if len(Mi) <= 60 else None
        if k4 is not None:
            r['cellules_de_quatre_M'] = len(k4)
            r['groupes_de_cinq_M_tous_lies'] = sum(1 for c in k4 for x in Mi if x > c[3] and all(x in adjM[y] for y in c))
            adj = {}
            for a, b in liens: adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
            un_A_un_B = 0; autres = {}
            for c in k4:
                com = set.intersection(*(adj[x] for x in c)); sig = tuple(sorted(cote[x] for x in com))
                if sig == (-1, 1): un_A_un_B += 1
                else: autres[str(sig)] = autres.get(str(sig), 0) + 1
            r['cellules_de_quatre_M_avec_un_cote_A_et_un_cote_B'] = un_A_un_B; r['cellules_de_quatre_M_autres'] = autres
        if rang2 is not None:
            # J6 : M au palier 2k+1 = tissu de rang 2 a la generation k
            k = (g - 1) // 2
            ens2 = {u for u, gen in rang2['spheres'].items() if gen <= k}
            M4 = {u[:4] for u in Ms}
            r['generation_de_rang_2_comparee'] = k; r['M_egale_tissu_de_rang_2'] = (M4 == ens2); r['effectif_du_tissu_de_rang_2'] = len(ens2)
            r['M_palier_egale_2k_plus_1'] = all((T.spheres[u] == 0 and rang2['spheres'][u[:4]] == 0) or T.spheres[u] == 2 * rang2['spheres'][u[:4]] + 1 for u in Ms if u[:4] in rang2['spheres'])
            liens2 = {frozenset((a, b)) for a, b in itertools.combinations(sorted(ens2), 2) if produit(a, b) == -1}
            liensM4 = {frozenset((L[a][:4], L[b][:4])) for a, b in liensM}
            r['liens_de_M_egaux_a_ceux_du_rang_2'] = (liensM4 == liens2); r['liens_du_tissu_de_rang_2'] = len(liens2)
    return r, dict(L=L, idx=idx, cote=cote, deg=deg, liens=liens)


def naissances_des_M(T, n, g, etat, R):
    """Chaque nouveau constituant qui est son propre reflet : ses liens au palier de sa naissance."""
    L, idx, cote, liens = etat['L'], etat['idx'], etat['cote'], etat['liens']
    adj = {}
    for a, b in liens: adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    out = {}
    for u in L:
        if cote[idx[u]] == 0 and T.spheres[u] == g:
            v = adj[idx[u]]; sig = tuple(sorted(cote[x] for x in v))
            jum = [L[x] for x in v if cote[x] != 0]
            miroirs = len(jum) == 2 and R(jum[0]) == jum[1]
            cle = '%d liens : %s%s' % (len(v), ''.join({-1: 'A', 0: 'M', 1: 'B'}[c] for c in sig), ' ; les deux voisins hors M sont images l\'un de l\'autre' if miroirs else '')
            out[cle] = out.get(cle, 0) + 1
    return out


def rang_deux_de_reference(G):
    """Tissu de rang 2 ne d'un germe de quatre, generations 0 a G (regle a la lettre)."""
    T2 = Tissu(2)
    for g in range(1, G + 1): T2.palier(g)
    return dict(spheres=dict(T2.spheres), effectifs=[sum(1 for v in T2.spheres.values() if v <= k) for k in range(G + 1)])


if __name__ == '__main__':
    essai = len(sys.argv) > 1 and sys.argv[1] == 'essai'
    t0 = time.time(); out = {}
    rang2 = rang_deux_de_reference(3); out['tissu_de_rang_2_de_reference'] = dict(effectifs_par_generation=rang2['effectifs'])
    print('rang 2 de reference, effectifs par generation :', rang2['effectifs'], flush=True)
    for n, G in ((2, 4), (3, 4)) if essai else ((2, 7), (3, 7)):
        w, ww, R = miroir_de(n)
        T, cellule0, e_dernier, jumeau = tissu_a_deux_cotes(n)
        assert all(produit(u, w) == 0 for u in cellule0) and R(e_dernier) == jumeau and R(jumeau) == e_dernier
        lignes = []
        r, etat = releve(T, n, 1, cellule0, (e_dernier, jumeau), w, ww, R, rang2 if n == 3 else None)
        r.update(naissances=2, produit_des_jumeaux=produit(e_dernier, jumeau), w=list(w), carre_de_w=ww); lignes.append(r)
        print('rang', n, json.dumps(r), flush=True)
        for g in range(2, G + 1):
            p = T.palier(g)
            complet = len(T.spheres) <= 16000
            r, etat = releve(T, n, g, cellule0, (e_dernier, jumeau), w, ww, R, rang2 if n == 3 else None, complet=complet)
            r.update(naissances=p['naissances'], cellules_au_meme_nouveau_ne=p['cellules_au_meme_nouveau_ne'], accolements=p['accolements'])
            f = p['accolements']
            r['fermetures'] = sum(v for k, v in f.items() if k.startswith('fermeture'))
            r['liens_poses_par_aucune_naissance'] = r['fermetures'] - p['cellules_au_meme_nouveau_ne']
            r['naissances_des_M'] = naissances_des_M(T, n, g, etat, R)
            r['croissance'] = r['constituants'] / lignes[-1]['constituants']
            r['croissance_du_degre_de_la_cellule_de_depart'] = r['degres_cellule_de_depart'][0] / lignes[-1]['degres_cellule_de_depart'][0]
            lignes.append(r)
            print('rang', n, json.dumps(r), flush=True)
        out['rang_%d' % n] = lignes
    out['duree_s'] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(ICI, 'x26_deux_cotes_du_tetraedre%s.json' % ('_essai' if essai else '')), 'w'), indent=1)
    print('duree', out['duree_s'], 's')
