#!/usr/bin/env python3
"""X-28 -- quelle propriete d'un tissu interdit une place admissible hors de l'empilement ? La regle a la lettre aux paliers 4 a 6.
Prediction scellee AVANT ce programme : x28_tissu_convexe_prediction.txt (SHA-256 c1576d634f56ee07ae24914e32a4f38f76db7cde54e29cb5165b2be08fb48bf5).
Outils importes tels quels : x27_mitose_avec_heritage (produit, Place, places_du_quadruple, descente, Tissu27) et le tissu de X-25 (regle a la lettre).

ENUMERATEUR NOUVEAU (clause N9). Pour un parent p et trois de ses voisins nes q, r, s, les boules liees aux quatre s'ecrivent
   x = alpha p + beta q + gamma r + delta s +/- lambda n,   n orthogonal aux quatre,
   beta = (b + c - a)/(2bc), gamma = (a + c - b)/(2ac), delta = (a + b - c)/(2ab), alpha = beta + gamma + delta - 1,
   a = nu(r,s), b = nu(q,s), c = nu(q,r), nu(u,v) = (1 - <u,v>)/2, lambda^2 <n,n> = 2 (beta + gamma + delta).
Filtre en nombres flottants (seuil 1e-6) contre les voisins du parent puis contre tout le tissu ; tout survivant est recalcule et controle
EXACTEMENT par places_du_quadruple et la methode _valide de X-27. Garde-fou : coordonnees de valeur absolue < 100 000.

Parties :
 paliers n [n_exact]  : regle a la lettre, paliers 0 a n ; places (parents a symetrie pres, completees par les 120 permutations), cotes libres,
                        convexite des tuiles, lemme du pont ; comparaison a l'outil de X-27 jusqu'au palier n_exact (defaut 3).
 file graine nb       : file d'attente avec l'outil de X-27 (toutes les places controlees a chaque naissance).
 partiel graine frac  : palier 4 plus une fraction tiree au hasard des naissances du palier 5 ; tous les parents.
 x27                  : le tissu du contre-exemple de X-27 et les trois places hors de l'empilement (clauses N5 et N8).
Usage : python3 x28_tissu_convexe.py paliers 5 | file 1 445 | partiel 1 0.5 | x27        Claude, 27 novembre 2026."""
import itertools, json, math, os, random, sys, time
from fractions import Fraction as F
import numpy as np
import x27_mitose_avec_heritage as m
from x25bis_naissances_et_fermetures import Tissu, autre_cote

ICI = os.path.dirname(os.path.abspath(__file__))
prod = m.prod
PERMS = list(itertools.permutations(range(5)))
COLS = [[c for c in range(5) if c != k] for k in range(5)]
SIG = np.array([(-1) ** k for k in range(5)], dtype=float)


def gram(Ai):
    s = Ai.sum(1); return 2 * Ai @ Ai.T - np.outer(s, s)


class Outil:
    """Un tissu S (liste de vecteurs entiers) : contacts exacts, tuiles nees (cinq tous lies), cellules, cotes libres, places admissibles."""

    def __init__(self, S):
        self.S = [tuple(int(v) for v in u) for u in S]; self.idx = {u: i for i, u in enumerate(self.S)}; n = len(self.S)
        self.Ai = np.array(self.S, dtype=np.int64); assert np.abs(self.Ai).max() < 100000, 'garde-fou : coordonnees trop grandes'
        self.Af = self.Ai.astype(float); self.sA = self.Af.sum(1); self.Gm = gram(self.Ai)
        d = np.diag(self.Gm); off = self.Gm[~np.eye(n, dtype=bool)]
        assert (d == 1).all() and (off <= -1).all(), 'le tissu se chevauche ou n est pas rond'
        self.adj = [set(np.nonzero(self.Gm[i] == -1)[0].tolist()) for i in range(n)]
        self.W = object.__new__(m.Tissu27); self.W.S = self.S; self.W.A = self.Af; self.W.sA = self.sA          # pour _valide et classe, tels quels

    # ---- tuiles et cellules
    def cliques(self):
        adj = self.adj; cel = []; tui = []
        for i in range(len(self.S)):
            Ni = {j for j in adj[i] if j > i}
            for j in sorted(Ni):
                Nij = {k for k in Ni & adj[j] if k > j}
                for k in sorted(Nij):
                    Nijk = {l for l in Nij & adj[k] if l > k}
                    for l in sorted(Nijk):
                        cel.append((i, j, k, l))
                        for q in sorted(x for x in Nijk & adj[l] if x > l): tui.append((i, j, k, l, q))
        self.cellules = cel; self.tuiles = tui
        self.tuiles_de = [[] for _ in self.S]
        for t, T in enumerate(tui):
            for i in T: self.tuiles_de[i].append(t)
        return cel, tui

    def cotes_libres(self):
        """Pour chaque cellule nee : ses cotes nes (constituants lies aux quatre) ; cote libre = somme de la cellule - cote ne, s'il n'est pas ne."""
        libres = set(); sans_cote_ne = 0; deux_cotes = 0; murs = []
        for C in self.cellules:
            nes = set.intersection(*(self.adj[i] for i in C))
            sC = tuple(sum(self.S[i][k] for i in C) for k in range(5))
            if not nes: sans_cote_ne += 1; continue
            if len(nes) == 2: deux_cotes += 1; continue
            t = self.S[next(iter(nes))]; t2 = tuple(sC[k] - t[k] for k in range(5))
            assert t2 not in self.idx
            libres.add(t2); murs.append((C, t, t2))
        self.libres = libres; self.murs = murs
        return libres, sans_cote_ne, deux_cotes

    def convexite(self):
        """Pour chaque cellule a un seul cote ne t (cote libre t') : un constituant ne u est au-dela du mur si <u, t - t'> < 0."""
        viol = 0; temoin = None
        for C, t, t2 in self.murs:
            d = np.array([a - b for a, b in zip(t, t2)], dtype=np.int64)
            v = 2 * self.Ai @ d - self.Ai.sum(1) * d.sum()
            if (v < 0).any():
                viol += 1
                if temoin is None:
                    j = int(np.nonzero(v < 0)[0][0]); temoin = dict(cellule=[list(self.S[i]) for i in C], cote_ne=list(t), cote_libre=list(t2), constituant_au_dela=list(self.S[j]), produit=int(v[j]))
        return dict(murs_de_surface=len(self.murs), murs_avec_un_constituant_au_dela=viol, convexe=(viol == 0), temoin=temoin)

    # ---- places admissibles d'un parent : filtre flottant sur tous les triplets de voisins, puis controle exact
    def survivants(self, p, tol=1e-6):
        N = np.array(sorted(self.adj[p]), dtype=np.int64); k = len(N)
        if k < 3: return [], 0
        nu = ((1 - self.Gm[np.ix_(N, N)]) // 2).astype(np.int64)
        V = self.Af[N]; sV = V.sum(1); gp = 2 * self.Af[p] - self.sA[p]; GV = 2 * V - sV[:, None]
        J, L = np.triu_indices(k, 1); debut = np.searchsorted(J, np.arange(k) + 1)
        forts = np.argsort(sV)[:min(k, 16)]                                    # les plus gros voisins d'abord : ils eliminent presque tout
        out = []; triplets = 0
        for i in range(k - 2):
            jj = J[debut[i]:]; ll = L[debut[i]:]
            if not len(jj): continue
            triplets += len(jj)
            a = nu[jj, ll]; b = nu[i, ll]; c = nu[i, jj]
            h = 2 * (a * b + b * c + c * a) - a * a - b * b - c * c
            ok = h >= 0
            if not ok.any(): continue
            jj, ll, a, b, c, h = jj[ok], ll[ok], a[ok].astype(float), b[ok].astype(float), c[ok].astype(float), h[ok].astype(float)
            be = (b + c - a) / (2 * b * c); ga = (a + c - b) / (2 * a * c); de = (a + b - c) / (2 * a * b); al = be + ga + de - 1
            x0 = al[:, None] * self.Af[p] + be[:, None] * V[i] + ga[:, None] * V[jj] + de[:, None] * V[ll]
            Mx = np.empty((len(jj), 4, 5)); Mx[:, 0] = gp; Mx[:, 1] = GV[i]; Mx[:, 2] = GV[jj]; Mx[:, 3] = GV[ll]
            n = np.stack([SIG[c_] * np.linalg.det(Mx[:, :, COLS[c_]]) for c_ in range(5)], axis=1)
            nn = 2 * (n * n).sum(1) - n.sum(1) ** 2
            bon = np.abs(nn) > 1e-9; r = np.where(bon, (h / (a * b * c)) / np.where(bon, nn, 1.0), -1.0); bon &= r >= 0
            if not bon.any(): continue
            jj, ll, x0, n, r = jj[bon], ll[bon], x0[bon], n[bon], r[bon]; lam = np.sqrt(r)
            for sg in (1.0, -1.0):
                x = x0 + sg * lam[:, None] * n; sx = x.sum(1)
                g = (2 * x @ V[forts].T - np.outer(sx, sV[forts]) <= -1 + tol).all(1)
                if not g.any(): continue
                xi, ji, li = x[g], jj[g], ll[g]; sxi = xi.sum(1)
                g2 = (2 * xi @ V.T - np.outer(sxi, sV) <= -1 + tol).all(1)
                if not g2.any(): continue
                xi, ji, li = xi[g2], ji[g2], li[g2]; sxi = xi.sum(1)
                g3 = (2 * xi @ self.Af.T - np.outer(sxi, self.sA) <= -1 + tol).all(1)
                for t in np.nonzero(g3)[0]: out.append((p, int(N[i]), int(N[ji[t]]), int(N[li[t]]), xi[t].copy()))
        return out, triplets

    def places_exactes(self, parents, journal=None):
        """Rend {cle: (Place, contacts)} pour les parents donnes. Controle exact de chaque survivant du filtre."""
        places = {}; triplets = 0; surv = 0
        for z, p in enumerate(parents):
            sv, t = self.survivants(p); triplets += t; surv += len(sv)
            for (p_, q, r, s, xf) in sv:
                quad = frozenset(self.S[i] for i in (p_, q, r, s)); pls = m.places_du_quadruple(quad)
                if not pls: continue
                pl = min(pls, key=lambda P: float(np.abs(P.xf - xf).max()))
                if float(np.abs(pl.xf - xf).max()) > 1e-6: continue
                if pl.cle in places: continue
                contacts = m.Tissu27._valide(self.W, pl)
                if contacts is None: continue
                assert {p_, q, r, s} <= contacts
                places[pl.cle] = (pl, contacts)
            if journal and (z % 20 == 0 or z == len(parents) - 1):
                print(json.dumps(dict(avance='%d/%d parents' % (z + 1, len(parents)), triplets=triplets, survivants=surv, places=len(places), t=round(time.time() - journal, 1))), flush=True)
        return places, triplets, surv

    def classe(self, pl): return m.Tissu27.classe(self.W, pl)

    def sans_cellule(self, contacts):
        c = sorted(contacts)
        return not any(all(b in self.adj[a] for a, b in itertools.combinations(t, 2)) for t in itertools.combinations(c, 4))

    # ---- lemme du pont (T2) eprouve sur les places trouvees
    def pont(self, places):
        """Pour chaque place, chaque parent possible p parmi ses contacts et chaque paire q, r de ses autres contacts lies a p :
        le milieu q + r + 2p est-il dans une tuile nee contenant p (coordonnees >= 0 hors de p) ? Si oui, T2 exige que q et r soient lies."""
        inv = {}
        def inverse(t):
            if t not in inv:
                B = np.array([self.S[i] for i in self.tuiles[t]], dtype=np.int64).T; Bi = np.rint(np.linalg.inv(B.astype(float))).astype(np.int64)
                assert (B @ Bi == np.eye(5, dtype=np.int64)).all(); inv[t] = Bi
            return inv[t]
        paires = dans = exceptions = liees_dans = non_liees = non_liees_hors = 0; ex = []
        for cle, (pl, contacts) in places.items():
            c = sorted(contacts)
            for p in c:
                vo = [u for u in c if u != p and u in self.adj[p]]
                for q, r in itertools.combinations(vo, 2):
                    paires += 1; lies = r in self.adj[q]; non_liees += (not lies)
                    z = self.Ai[q] + self.Ai[r] + 2 * self.Ai[p]; trouve = False
                    for t in self.tuiles_de[p]:
                        co = inverse(t) @ z; T = self.tuiles[t]
                        if all(co[k] >= 0 for k in range(5) if T[k] != p): trouve = True; break
                    if trouve:
                        dans += 1
                        if lies: liees_dans += 1
                        else:
                            exceptions += 1
                            if len(ex) < 5: ex.append(dict(place=str(cle), parent=list(self.S[p]), q=list(self.S[q]), r=list(self.S[r])))
                    elif not lies: non_liees_hors += 1
        return dict(paires_controlees=paires, paires_non_liees=non_liees, milieu_dans_une_tuile_nee=dans, dont_paires_liees=liees_dans,
                    exceptions_a_T2=exceptions, exemples=ex, paires_non_liees_dont_le_milieu_n_est_dans_aucune_tuile_nee=non_liees_hors)


def bilan(O, places):
    cl = {}; sc = 0; hors = []
    for cle, (pl, contacts) in places.items():
        k = O.classe(pl); cl[k] = cl.get(k, 0) + 1
        if O.sans_cellule(contacts): sc += 1
        if k != 'empilement' and len(hors) < 5:
            hors.append(dict(classe=k, place=[str(v) for v in pl.coords] if pl.coords is not None else [round(float(v), 9) for v in pl.xf], touche=[list(O.S[i]) for i in sorted(contacts)]))
    return cl, sc, hors


def partie_paliers(nmax, n_exact=3):
    T = Tissu(3); out = []
    for g in range(nmax + 1):
        if g: T.palier(g)
        t0 = time.time(); S = sorted(T.spheres); O = Outil(S); cel, tui = O.cliques(); libres, sans_cote, deux = O.cotes_libres()
        cotes_x25 = {autre_cote(c, o, 3) for c, o in T.surface.items()}
        reps = [i for i, u in enumerate(O.S) if u == tuple(sorted(u))]
        pl, triplets, surv = O.places_exactes(reps, journal=t0 if len(S) > 400 else None)
        toutes = set(); irr = 0
        for cle, (P, contacts) in pl.items():
            if P.coords is None: irr += 1; toutes.add(cle); continue
            for pe in PERMS: toutes.add(tuple(P.coords[k] for k in pe))
        cl, sc, hors = bilan(O, pl)
        r = dict(palier=g, constituants=len(S), parents_a_symetrie_pres=len(reps), tuiles_nees=len(tui), tuiles_du_tissu_de_X25=len(T.confs),
                 memes_tuiles=({frozenset(O.S[i] for i in t) for t in tui} == set(T.confs)), cellules_nees=len(cel), cellules_sans_cote_ne=sans_cote, cellules_a_deux_cotes_nes=deux,
                 triplets_examines=triplets, survivants_du_filtre=surv, places_des_parents_types=len(pl), par_classe_parents_types=cl, places_irrationnelles=irr,
                 places_admissibles=len(toutes), cotes_libres=len(libres), cotes_libres_des_cellules_de_surface_X25=len(cotes_x25), memes_cotes_libres=(libres == cotes_x25),
                 places_egales_aux_cotes_libres=(toutes == libres), places_hors_cotes=len(toutes - libres), cotes_non_admissibles=len(libres - toutes),
                 places_sans_cellule_parents_types=sc, exemples_hors_empilement=hors, convexite=O.convexite(), pont=O.pont(pl))
        if g <= n_exact:
            t1 = time.time(); W = m.Tissu27(S); r.update(outil_X27_places=len(W.places), meme_ensemble_que_l_outil_X27=(set(W.places) == toutes), outil_X27_duree_s=round(time.time() - t1, 1))
        r['duree_s'] = round(time.time() - t0, 1); out.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
        json.dump(out, open(os.path.join(ICI, 'x28_paliers_%d.json' % nmax), 'w'), indent=1, ensure_ascii=False)
        if g == 4: json.dump(sorted([list(u) for u in toutes]), open(os.path.join(ICI, 'x28_places_palier_4.json'), 'w'))
    return out


def partie_file(graine, naissances):
    rng = random.Random(graine); T = m.Tissu27(m.G5); t0 = time.time(); vue_a = {}; sans_cel_max = 0; sans_cel_vues = set()
    for k in range(naissances):
        cles = sorted((c for c in T.places if T.vues[c] == 'empilement'), key=repr)
        for c in cles:
            vue_a.setdefault(c, k)
            if c not in sans_cel_vues and T.sans_cellule(c): sans_cel_vues.add(c)
        plus_vieux = min(vue_a[c] for c in cles); choix = [c for c in cles if vue_a[c] == plus_vieux]
        T.naissance(rng.choice(choix))
        if (k + 1) in (5, 25, 115, 445) or (k + 1) % 50 == 0:
            b = m.bilan_des_vues(T.vues)
            print(json.dumps(dict(graine=graine, naissances=k + 1, places_presentes=len(T.places), places_rencontrees=len(T.vues), par_classe=b,
                                  hors_de_l_empilement=sum(v for c, v in b.items() if c != 'empilement'), places_sans_cellule_rencontrees=len(sans_cel_vues), t=round(time.time() - t0, 1))), flush=True)
    for c in T.places:
        if c not in sans_cel_vues and T.vues[c] == 'empilement' and T.sans_cellule(c): sans_cel_vues.add(c)
    b = m.bilan_des_vues(T.vues); S = sorted(T.S)
    r = dict(strategie='file d\'attente', graine=graine, naissances=len(T.S) - 5, quadruples_examines=len(T.quads), places_rencontrees=len(T.vues), par_classe=b,
             hors_de_l_empilement=sum(v for c, v in b.items() if c != 'empilement'), exemples_hors=T.hors[:5], places_sans_cellule_rencontrees=len(sans_cel_vues),
             places_a_la_fin=len(T.places), duree_s=round(time.time() - t0, 1))
    if naissances == 445:
        X = Tissu(3)
        for g in range(1, 5): X.palier(g)
        r['tissu_final_egal_au_palier_4'] = (S == sorted(X.spheres))
        f = os.path.join(ICI, 'x28_places_palier_4.json')
        if os.path.exists(f): r['places_finales_egales_a_celles_de_l_enumerateur'] = (sorted(list(c) for c in T.places) == json.load(open(f)))
        json.dump(sorted(list(c) for c in T.places), open(os.path.join(ICI, 'x28_file_%d_places_finales.json' % graine), 'w'))
    print(json.dumps(r, ensure_ascii=False), flush=True)
    return r


def partie_partiel(graine, frac):
    X = Tissu(3)
    for g in range(1, 5): X.palier(g)
    S4 = sorted(X.spheres); O4 = Outil(S4); O4.cliques(); libres, _, _ = O4.cotes_libres(); L = sorted(libres)
    rng = random.Random(graine); choisis = rng.sample(L, int(round(frac * len(L)))); t0 = time.time()
    O = Outil(S4 + sorted(choisis)); cel, tui = O.cliques(); lib, sans_cote, deux = O.cotes_libres()
    pl, triplets, surv = O.places_exactes(list(range(len(O.S))), journal=t0)
    cl, sc, hors = bilan(O, pl); cles = set(pl)
    r = dict(graine=graine, fraction=frac, constituants=len(O.S), naissances_du_palier_5_tirees=len(choisis), sur=len(L), tuiles_nees=len(tui), cellules_nees=len(cel), cellules_sans_cote_ne=sans_cote,
             triplets_examines=triplets, survivants_du_filtre=surv, places_admissibles=len(pl), par_classe=cl, hors_de_l_empilement=sum(v for c, v in cl.items() if c != 'empilement'),
             places_sans_cellule=sc, cotes_libres=len(lib), places_egales_aux_cotes_libres=(cles == lib), places_hors_cotes=len(cles - lib), cotes_non_admissibles=len(lib - cles),
             exemples_hors_empilement=hors, convexite=O.convexite(), pont=O.pont(pl), duree_s=round(time.time() - t0, 1))
    print(json.dumps(r, ensure_ascii=False), flush=True)
    return r


def partie_x27():
    c = json.load(open(os.path.join(ICI, 'x27_contre_exemple_court.json'))); t = json.load(open(os.path.join(ICI, 'x27_contre_exemple_toit.json')))
    out = {}
    # (1) le tissu de 22 constituants : convexite, places, pont
    S = list(m.G5) + [tuple(u) for u in c['liste_des_naissances']]; O = Outil(S); cel, tui = O.cliques(); lib, sans_cote, deux = O.cotes_libres()
    pl, triplets, surv = O.places_exactes(list(range(len(S)))); cl, sc, hors = bilan(O, pl); W = m.Tissu27(S)
    out['tissu_de_22'] = dict(tuiles_nees=len(tui), cellules_nees=len(cel), cellules_sans_cote_ne=sans_cote, places_admissibles=len(pl), par_classe=cl, places_sans_cellule=sc,
                              meme_ensemble_que_l_outil_X27=(set(pl) == set(W.places)), convexite=O.convexite(), pont=O.pont(pl), exemples_hors_empilement=hors)
    # (2) la place hors de l'empilement, parent e0 : paires de contacts, milieux
    x = tuple(F(v) for v in c['place_hors_empilement']); P_, cont = pl[x]; p = O.idx[(1, 0, 0, 0, 0)]; vo = [u for u in sorted(cont) if u != p and u in O.adj[p]]; det = []
    for q, r in itertools.combinations(vo, 2):
        z = O.Ai[q] + O.Ai[r] + 2 * O.Ai[p]; dedans = []
        for ti in O.tuiles_de[p]:
            B = np.array([O.S[i] for i in O.tuiles[ti]], dtype=np.int64).T; co = np.rint(np.linalg.solve(B.astype(float), z.astype(float))).astype(np.int64); assert (B @ co == z).all()
            if all(co[k] >= 0 for k in range(5) if O.tuiles[ti][k] != p): dedans.append(ti)
        det.append(dict(q=list(O.S[q]), r=list(O.S[r]), produit=int(O.Gm[q, r]), lies=(r in O.adj[q]), tuiles_nees_au_parent=len(O.tuiles_de[p]), tuiles_nees_contenant_le_milieu=len(dedans)))
    out['place_hors_empilement_parent_e0'] = dict(contacts=[list(O.S[i]) for i in sorted(cont)], paires=det)
    # (3) jumelles des trois places hors de l'empilement (clause N8)
    def jumelles(S_, xf):
        O_ = Outil(S_); res = []; touche = [i for i, u in enumerate(O_.S) if prod(xf, u) == -1]
        for p_ in touche:
            vo_ = [u for u in touche if u != p_ and u in O_.adj[p_]]
            for tr in itertools.combinations(vo_, 3):
                pls = m.places_du_quadruple(frozenset(O_.S[i] for i in (p_,) + tr))
                if len(pls) != 2: continue
                cs = [P.coords for P in pls]
                if xf not in cs: continue
                j = cs[1] if cs[0] == xf else cs[0]
                ent = j is not None and all(isinstance(v, int) for v in j)
                res.append(dict(parent=list(O_.S[p_]), voisins=[list(O_.S[i]) for i in tr], jumelle=[str(v) for v in j] if j is not None else None,
                                jumelle_dans_l_empilement=bool(ent and m.dans_l_empilement(j)), jumelle_nee=bool(ent and j in O_.idx)))
        return res
    N = [tuple(u) for u in t['liste_des_naissances']]; cas = []
    cas.append(('x_prime (17 naissances)', S, x))
    for h in t['outil_places_hors_empilement']:
        xf = tuple(F(v) for v in h['place']); cas.append(('place vue a %d constituants' % h['constituants'], list(m.G5) + N[:h['constituants'] - 5], xf))
    cas.append(('x du toit (26 naissances)', list(m.G5) + N, tuple(F(v, 3) for v in (8, 8, 7, -2, -2))))
    out['jumelles'] = []
    for nom, S_, xf in cas:
        j = jumelles(S_, xf)
        out['jumelles'].append(dict(place=nom, x=[str(v) for v in xf], quadruples=len(j), jumelles_dans_l_empilement=sum(1 for e in j if e['jumelle_dans_l_empilement']), detail=j[:6]))
    # (4) le tissu du toit (31 constituants)
    O2 = Outil(list(m.G5) + N); O2.cliques(); O2.cotes_libres(); pl2, _, _ = O2.places_exactes(list(range(len(O2.S)))); cl2, sc2, hors2 = bilan(O2, pl2)
    out['tissu_du_toit'] = dict(constituants=len(O2.S), places_admissibles=len(pl2), par_classe=cl2, places_sans_cellule=sc2, convexite=O2.convexite(), pont=O2.pont(pl2))
    print(json.dumps(out, ensure_ascii=False), flush=True); json.dump(out, open(os.path.join(ICI, 'x28_x27.json'), 'w'), indent=1, ensure_ascii=False)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'paliers': partie_paliers(int(a[1]), int(a[2]) if len(a) > 2 else 3)
    elif a[0] == 'file': partie_file(int(a[1]), int(a[2]))
    elif a[0] == 'partiel': partie_partiel(int(a[1]), float(a[2]))
    elif a[0] == 'x27': partie_x27()
