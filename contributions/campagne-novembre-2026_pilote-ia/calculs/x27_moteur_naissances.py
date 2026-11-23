#!/usr/bin/env python3
"""X-27, partie D -- le moteur complet de l'auteur pratique-t-il la naissance que les contacts seuls permettent ?
A chaque mitose du moteur (<< blob ablation labo colab.py >>, quatre forces, kappa = 6,6), releve du parent, des constituants auxquels le nouveau-ne est lie,
et des liens entre ces constituants a cet instant. Puis, par naissance :
 - etoile : le nouveau-ne est lie a son parent et a trois voisins du parent au moins (forme, en liens, d'une naissance heritee et fixee) ;
 - cellule : il est lie aux quatre membres d'un groupe de quatre tous lies (naissance dans une cellule, au sens des liens) ;
 - cinq : il est lie aux cinq membres d'un groupe de cinq tous lies (interdit a un tissu de contact de rang 3 : cela ferait six constituants tous lies).
INSTRUMENTATION DECLAREE : le source de l'auteur (lignes avant << def mesure( >>, empreinte verifiee par x24_moteur_dimension.py) est execute apres deux remplacements
de texte comptes qui AJOUTENT un enregistrement (aucun tirage au hasard, aucun etat modifie) :
 (1) apres << mset|=set(knn) >> : parent, constituants lies, liens entre eux, nombre de constituants lies qui sont le parent ou un voisin du parent ;
 (2) dans la branche << moins de deux voisins >> : parent seul.
Note ajoutee apres la premiere execution : le quatrieme champ (parent ou voisin du parent) manquait ; sans lui le controle M8 ne pouvait pas etre fait pour les
naissances ou le parent lui-meme n'est pas parmi les liens (1 a 2 %). Ajoute, puis reexecute ; les autres nombres sont inchanges.
Controle zero : empreintes des liens des quatre etats de reference de X-24 B (660 et 1 037 constituants, graines 1 et 2).
Prediction scellee : x27_mitose_avec_heritage_prediction.txt (SHA-256 d0e1e54de989fa8f6022dcc3edceee900914133c1f8cabddc6136ea0feccb502).     Claude, 23 novembre 2026."""
import hashlib, itertools, json, os, time
import x24_moteur_dimension as base

ICI = os.path.dirname(os.path.abspath(__file__))
EMPREINTES_X24 = {(1, 660): '3b85f7c1f30035fd', (1, 1037): 'c0e1a4275f32ff9d', (2, 660): 'c7f34aa111a149dc', (2, 1037): '3b663cb72881cbcf'}


def moteur():
    s = base.SOURCE
    def remplace(s, ancien, nouveau):
        assert s.count(ancien) == 1, (ancien, s.count(ancien))
        return s.replace(ancien, nouveau)
    s = remplace(s, 'mset|=set(knn)', 'mset|=set(knn); self._naiss.append((int(parent), tuple(int(a) for a in knn), tuple((int(a),int(b)) for a in knn for b in knn if a<b and b in self.adj[a]), sum(1 for a in knn if a==parent or a in self.adj[parent])))')
    s = remplace(s, 'self.adj[nid].add(parent); self.adj[parent].add(nid); mset.add(parent)', 'self.adj[nid].add(parent); self.adj[parent].add(nid); mset.add(parent); self._naiss.append((int(parent), (int(parent),), (), 1))')
    M = {}; exec(s, M); return M


def plus_grand_groupe(lies, liens):
    """Taille du plus grand groupe de constituants tous lies parmi ceux auxquels le nouveau-ne est lie."""
    E = set(liens)
    for k in range(len(lies), 1, -1):
        for t in itertools.combinations(sorted(lies), k):
            if all((a, b) in E for a, b in itertools.combinations(t, 2)): return k
    return 1 if lies else 0


def bilan(naiss):
    n = len(naiss); par_k = {}; par_w = {}; etoile = cellule = cinq = parent_dedans = herite = 0; croise = {}
    for parent, lies, liens, du_parent in naiss:
        k = len(lies); E = set(liens); w = plus_grand_groupe(lies, liens)
        par_k[k] = par_k.get(k, 0) + 1; par_w[w] = par_w.get(w, 0) + 1; croise[(k, w)] = croise.get((k, w), 0) + 1
        dedans = parent in lies; parent_dedans += dedans
        voisins_du_parent = [a for a in lies if a != parent and ((min(a, parent), max(a, parent)) in E)]
        herite += (du_parent == k)
        etoile += (dedans and len(voisins_du_parent) >= 3)
        cellule += (w >= 4); cinq += (w >= 5)
    return dict(naissances=n, par_nombre_de_liens={str(k): v for k, v in sorted(par_k.items())}, par_plus_grand_groupe_tous_lies={str(k): v for k, v in sorted(par_w.items())},
                par_liens_et_plus_grand_groupe={'%d liens, groupe de %d' % kw: v for kw, v in sorted(croise.items())},
                part_parent_parmi_les_liens=parent_dedans / n, part_tous_les_liens_au_parent_ou_a_ses_voisins=herite / n,
                part_etoile=etoile / n, part_dans_une_cellule=cellule / n, part_liee_a_cinq_tous_lies=cinq / n, liens_moyens=sum(len(l[1]) for l in naiss) / n)


if __name__ == '__main__':
    t0 = time.time(); out = []
    for graine in (1, 2):
        M = moteur(); bl = M['Blob'](N0=300, seed=graine, forces=base.FORCES); bl._naiss = []
        for cible in base.RELEVES:
            while bl.N < cible: bl.step(0.12)
            liens = base.liens_de(bl); emp = hashlib.sha256(json.dumps(liens).encode()).hexdigest()
            r = dict(graine=graine, constituants=bl.N, empreinte_des_liens=emp, empreinte_de_X24_retrouvee=emp.startswith(EMPREINTES_X24[(graine, bl.N)]), **bilan(bl._naiss))
            out.append(r); print(json.dumps(r), flush=True)
    json.dump(dict(etats=out, duree_s=round(time.time() - t0, 1)), open(os.path.join(ICI, 'x27_moteur_naissances.json'), 'w'), indent=1)
    print('duree', round(time.time() - t0, 1), 's')
