#!/usr/bin/env python3
"""X-25 quinquies -- quelle naissance le moteur complet de l'auteur pratique-t-il ? Comptage, a chaque mitose, des constituants auxquels le nouveau-ne est lie.
INSTRUMENTATION DECLAREE : le source de l'auteur (<< blob ablation labo colab.py >>, lignes avant << def mesure( >>, empreinte verifiee par x24_moteur_dimension.py)
est execute apres deux remplacements de texte comptes qui AJOUTENT un enregistrement (aucun tirage au hasard, aucun etat modifie) :
 (1) apres << mset|=set(knn) >> : nombre de constituants lies au nouveau-ne, nombre de liens entre eux, presence du parent ;
 (2) dans la branche << moins de deux voisins >> : (1, 0, 1).
Controle zero : empreintes des liens des quatre etats de reference de X-24 B.
Prediction scellee : x25quinquies_quelle_naissance_prediction.txt (SHA-256 e6ec214a1455e1f9bc372662817955ad2feb4a0ab42d7cfdc5529a3d82693f83).     Claude, 23 novembre 2026."""
import hashlib, json, os, time
import x24_moteur_dimension as base

ICI = os.path.dirname(os.path.abspath(__file__))
EMPREINTES_X24 = {(1, 660): '3b85f7c1f30035fd', (1, 1037): 'c0e1a4275f32ff9d', (2, 660): 'c7f34aa111a149dc', (2, 1037): '3b663cb72881cbcf'}


def moteur():
    s = base.SOURCE
    def remplace(s, ancien, nouveau):
        assert s.count(ancien) == 1, (ancien, s.count(ancien))
        return s.replace(ancien, nouveau)
    s = remplace(s, 'mset|=set(knn)', 'mset|=set(knn); self._naiss.append((len(knn), sum(1 for a in knn for b in knn if a<b and b in self.adj[a]), int(parent in knn)))')
    s = remplace(s, 'self.adj[nid].add(parent); self.adj[parent].add(nid); mset.add(parent)', 'self.adj[nid].add(parent); self.adj[parent].add(nid); mset.add(parent); self._naiss.append((1, 0, 1))')
    M = {}; exec(s, M); return M


def bilan(naiss):
    n = len(naiss); par_k = {}; complets = {}
    for k, m, p in naiss:
        par_k[k] = par_k.get(k, 0) + 1
        if m == k * (k - 1) // 2: complets[k] = complets.get(k, 0) + 1
    c3 = sum(v for k, v in complets.items() if k >= 3)
    return dict(naissances=n, par_nombre_de_constituants_lies={str(k): v for k, v in sorted(par_k.items())}, groupes_complets_par_taille={str(k): v for k, v in sorted(complets.items())},
                part_a_cinq_ou_six=sum(v for k, v in par_k.items() if k >= 5) / n, part_dans_un_groupe_complet_d_au_moins_trois=c3 / n, part_dans_un_groupe_complet_de_quatre=complets.get(4, 0) / n,
                part_avec_le_parent=sum(p for _, _, p in naiss) / n, liens_moyens_par_naissance=sum(k for k, _, _ in naiss) / n,
                part_des_paires_liees_parmi_les_constituants_lies=sum(m for _, m, _ in naiss) / max(1, sum(k * (k - 1) // 2 for k, _, _ in naiss)))


if __name__ == '__main__':
    t0 = time.time(); out = []
    for graine in (1, 2):
        M = moteur(); bl = M['Blob'](N0=300, seed=graine, forces=base.FORCES); bl._naiss = []
        for cible in base.RELEVES:
            while bl.N < cible: bl.step(0.12)
            liens = base.liens_de(bl); emp = hashlib.sha256(json.dumps(liens).encode()).hexdigest()
            r = dict(graine=graine, constituants=bl.N, empreinte_des_liens=emp, empreinte_de_X24_retrouvee=emp.startswith(EMPREINTES_X24[(graine, bl.N)]), **bilan(bl._naiss))
            out.append(r); print(json.dumps(r), flush=True)
    json.dump(dict(etats=out, duree_s=round(time.time() - t0, 1)), open(os.path.join(ICI, 'x25quinquies_quelle_naissance.json'), 'w'), indent=1)
    print('duree', round(time.time() - t0, 1), 's')
