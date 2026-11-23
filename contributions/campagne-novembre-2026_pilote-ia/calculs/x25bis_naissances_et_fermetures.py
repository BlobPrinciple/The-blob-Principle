#!/usr/bin/env python3
"""X-25 bis -- naissances et fermetures : la surface du tissu de contact evolue-t-elle par les deux mouvements du secteur canonique (1 -> 4 et 2 -> 3) ?
Regle a la lettre (lectures C1, C2, C5 de X-25) : a chaque palier, (1) chaque cellule de surface enfante de son cote libre, toutes ensemble ; (2) toute configuration
dont les n+2 constituants existent et qui touche la surface par une cellule est accolee, jusqu'a epuisement. Arithmetique exacte en entiers (rangs 2 et 3).
Une configuration = n+2 constituants tous lies ; une cellule = n+1 d'entre eux ; la surface = les cellules contenues dans une seule configuration accolee.
Prediction scellee : x25bis_naissances_et_fermetures_prediction.txt (SHA-256 d9d8153a009e5c95aea33fece8936b4a552a20a6d5b0c5aaa04506ee141a47ce).
Usage : python3 x25bis_naissances_et_fermetures.py [essai]     Claude, 23 novembre 2026."""
import itertools, json, os, sys, time
import numpy as np
from x25_cellule import germe, produit

ICI = os.path.dirname(os.path.abspath(__file__))


def autre_cote(cellule, occupant, n):
    f = 2 // (n - 1); assert f * (n - 1) == 2                     # rangs 2 et 3 seulement : facteur entier
    s = [sum(c[k] for c in cellule) for k in range(n + 2)]
    return tuple(-occupant[k] + f * s[k] for k in range(n + 2))


class Tissu:
    def __init__(self, n):
        self.n = n; g0 = germe(n)
        self.spheres = {u: 0 for u in g0}
        self.confs = set(); self.surface = {}                     # cellule de surface (frozenset) -> occupant du cote deja accole
        self.accole = {}                                          # nombre de cellules de surface par lesquelles chaque configuration a ete accolee -> effectif
        self.B = 0; self.C = 0
        self.ajoute(frozenset(g0), germe_=True)

    def ajoute(self, D, germe_=False):
        if D in self.confs: return None
        self.confs.add(D); k = 0
        for x in D:
            cel = D - {x}
            if cel in self.surface: del self.surface[cel]; k += 1
            else: self.surface[cel] = x
        if not germe_: self.accole[k] = self.accole.get(k, 0) + 1
        return k

    def palier(self, g):
        n = self.n
        # (1) naissances, toutes ensemble, sur l'instantane de la surface
        instant = list(self.surface.items()); nes = []; nais = 0; meme_nouveau_ne = 0
        for cel, occ in instant:
            x = autre_cote(cel, occ, n)
            if x not in self.spheres: self.spheres[x] = g; nais += 1; nes.append((cel, x, True))
            else:
                if self.spheres[x] == g: meme_nouveau_ne += 1     # deux cellules de l'instantane ont le meme nouveau-ne
                nes.append((cel, x, False))
        types = {}
        for cel, x, neuf in nes:
            k = self.ajoute(cel | {x})
            if k is not None:
                cle = '%s:%d' % ('naissance' if neuf else 'fermeture', k); types[cle] = types.get(cle, 0) + 1
                if not neuf: self.C += 1
        self.B += nais
        # (2) fermetures jusqu'a epuisement
        ferm = 0
        while True:
            fait = False
            for cel, occ in list(self.surface.items()):
                if cel not in self.surface: continue
                x = autre_cote(cel, occ, n)
                if x in self.spheres:
                    k = self.ajoute(cel | {x})
                    if k is not None:
                        cle = 'fermeture:%d' % k; types[cle] = types.get(cle, 0) + 1; ferm += 1; self.C += 1; fait = True
            if not fait: break
        return dict(palier=g, naissances=nais, cellules_au_meme_nouveau_ne=meme_nouveau_ne, accolements=types)

    def controle(self, complet=True):
        """Surface : variete fermee ? contacts = liens de la surface ? groupes de n+1 tous lies aux deux cotes libres ?"""
        n = self.n; L = list(self.spheres); m = len(L); idx = {u: i for i, u in enumerate(L)}
        cells = [tuple(sorted(idx[u] for u in c)) for c in self.surface]
        faces = {}
        for c in cells:
            for f in itertools.combinations(c, n): faces[f] = faces.get(f, 0) + 1
        liens = set()
        for c in cells:
            for e in itertools.combinations(c, 2): liens.add(e)
        r = dict(constituants=m, liens_de_surface=len(liens), cellules_de_surface=len(cells), faces=len(faces), faces_hors_de_deux_cellules=sum(1 for v in faces.values() if v != 2),
                 naissances_cumulees=self.B, fermetures_cumulees=self.C)
        if n == 3:
            tri = len(faces); r['caracteristique_d_Euler'] = m - len(liens) + tri - len(cells)
            r['comptes_attendus'] = dict(constituants=5 + self.B, liens=10 + 4 * self.B + self.C, tetraedres=5 + 3 * self.B + self.C)
            r['tetraedres_par_lien'] = 6 * len(cells) / len(liens)
        else:
            r['caracteristique_d_Euler'] = m - len(liens) + len(cells)
        r['fermetures_sur_naissances'] = self.C / self.B if self.B else None
        if complet:
            # voisinage de chaque constituant
            par = {}
            for c in cells:
                for v in c: par.setdefault(v, []).append(tuple(x for x in c if x != v))
            mauvais = 0
            for v, lk in par.items():
                if n == 3:
                    V = {x for t in lk for x in t}; E = {e for t in lk for e in itertools.combinations(t, 2)}
                    chi = len(V) - len(E) + len(lk)
                    # connexite
                    adj = {}
                    for a, b in E: adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
                    vu = set(); pile = [next(iter(V))]
                    while pile:
                        a = pile.pop()
                        if a in vu: continue
                        vu.add(a); pile.extend(adj[a] - vu)
                    cnt = {}
                    for t in lk:
                        for e in itertools.combinations(t, 2): cnt[e] = cnt.get(e, 0) + 1
                    if chi != 2 or len(vu) != len(V) or any(c != 2 for c in cnt.values()): mauvais += 1
                else:
                    deg = {}
                    for a, b in lk: deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
                    if any(d != 2 for d in deg.values()): mauvais += 1
            r['constituants_dont_le_voisinage_n_est_pas_une_sphere'] = mauvais
            # contacts exacts
            A = np.array(L, dtype=np.int64); assert np.abs(A).max() < 3 * 10 ** 8
            s = A.sum(axis=1); contacts = set(); chev = 0
            for a in range(0, m, 400):
                P = 2 * A[a:a + 400] @ A.T - np.outer(s[a:a + 400], s)
                for k in range(P.shape[0]): P[k, :a + k + 1] = -10 ** 18
                ii, jj = np.nonzero(P == -1)
                for i, j in zip(ii, jj): contacts.add((a + int(i), int(j)))
                chev += int((P > -1).sum())
            r['contacts'] = len(contacts); r['contacts_hors_surface'] = len(contacts - liens); r['liens_de_surface_sans_contact'] = len(liens - contacts); r['chevauchements'] = chev
            # groupes de n+1 tous lies dont les deux cotes sont libres
            adjc = {}
            for a, b in contacts: adjc.setdefault(a, set()).add(b); adjc.setdefault(b, set()).add(a)
            libres2 = 0; groupes = 0
            def ext(R, cand):
                nonlocal libres2, groupes
                if len(R) == n + 1:
                    groupes += 1
                    com = set.intersection(*(adjc[v] for v in R))
                    if len(com) == 0: libres2 += 1
                    return
                for v in sorted(cand): ext(R + [v], {w for w in cand & adjc[v] if w > v})
            if m <= 3000:
                for u in sorted(adjc): ext([u], {w for w in adjc[u] if w > u})
                r['groupes_de_n_plus_1_tous_lies'] = groupes; r['dont_les_deux_cotes_libres'] = libres2
        return r


if __name__ == '__main__':
    essai = len(sys.argv) > 1 and sys.argv[1] == 'essai'
    t0 = time.time(); out = {}
    for n, G in ((2, 4), (3, 4)) if essai else ((2, 6), (3, 6)):
        T = Tissu(n); lignes = []
        c0 = T.controle(); c0['palier'] = 0; lignes.append(c0)
        for g in range(1, G + 1):
            p = T.palier(g)
            c = T.controle(complet=(len(T.spheres) <= 12000)); c.update(p); lignes.append(c)
            print('rang', n, json.dumps(c), flush=True)
        out['rang_%d' % n] = dict(paliers=lignes, accolements_cumules={str(k): v for k, v in sorted(T.accole.items())})
        print('rang', n, 'accolements cumules (nombre de cellules de surface par configuration accolee) :', out['rang_%d' % n]['accolements_cumules'], flush=True)
    out['duree_s'] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(ICI, 'x25bis_naissances_et_fermetures%s.json' % ('_essai' if essai else '')), 'w'), indent=1)
    print('duree', out['duree_s'], 's')
