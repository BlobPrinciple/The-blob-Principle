#!/usr/bin/env python3
"""X-25 ter, premiere partie -- quelle regle du moteur complet de l'auteur le rend compatible avec la lecture de contact ? et la dimension des points y joue-t-elle ?
Les etats sont regeneres par les programmes de X-24 (x24bis_groupe_qui_se_defait.moteur : source de l'auteur avec les remplacements de texte declares la-bas) ;
les conditions (N1), (N2), (N3) du rang 3 sont celles de x25_moteurs_contact.py. Pour les points en dimension 2 : conditions du rang 2 en plus
(aucun groupe de cinq ; un triple tous lies a au plus deux voisins communs, non lies entre eux).
Prediction scellee : x25ter_moteur_et_contact_prediction.txt (SHA-256 5aece6706f9fe693c196a5817680082cca52f1d8471030acbe11d4832599345a).     Claude, 23 novembre 2026."""
import hashlib, json, os, sys, time
import x24_moteur_dimension as base
import x24bis_groupe_qui_se_defait as bis
from x25_moteurs_contact import epreuve

ICI = os.path.dirname(os.path.abspath(__file__))
QUATRE = bis.QUATRE_FORCES
VARIANTES = [  # (nom, groupe qui se defait (0 = aucun), kappa, forces, dimension des points)
    ("regle de l'auteur, quatre forces, kappa 4,6", 4, 4.6, QUATRE, 3), ("regle de l'auteur, quatre forces, kappa 8,6", 4, 8.6, QUATRE, 3),
    ("regle de l'auteur, quatre forces, points en dimension 2", 4, 6.6, QUATRE, 2), ("regle de l'auteur, quatre forces, points en dimension 4", 4, 6.6, QUATRE, 4),
    ("regle de l'auteur, quatre forces, points en dimension 5", 4, 6.6, QUATRE, 5),
    ("sans la regle (taux nul), sans force", 0, 6.6, (), 3), ("sans la regle (taux nul), quatre forces", 0, 6.6, QUATRE, 3),
    ("groupes de cinq qui se defont, sans force", 5, 6.6, (), 3), ("groupes de trois qui se defont, sans force", 3, 6.6, (), 3),
    ("regle de l'auteur, sans force", 4, 6.6, (), 3)]


def connues():
    s = set()
    def visite(o):
        if isinstance(o, dict):
            if 'empreinte_des_liens' in o: s.add(o['empreinte_des_liens'])
            for v in o.values(): visite(v)
        elif isinstance(o, list):
            for v in o: visite(v)
    for f in ('x24_moteur_dimension.json', 'x24bis_groupe_qui_se_defait.json', 'x24ter_quelle_force.json'):
        visite(json.load(open(os.path.join(ICI, f))))
    return s


def rang2(adj):
    n = len(adj); tri = 0; plus2 = 0; lies = 0
    for u in range(n):
        for v in (x for x in adj[u] if x > u):
            for w in (x for x in adj[u] & adj[v] if x > v):
                tri += 1; c = adj[u] & adj[v] & adj[w]
                if len(c) > 2: plus2 += 1
                elif len(c) == 2:
                    a, b = tuple(c); lies += b in adj[a]
    return dict(triples=tri, avec_plus_de_deux_voisins_communs=plus2, avec_deux_voisins_communs_lies_entre_eux=lies)


if __name__ == '__main__':
    t0 = time.time(); K = connues(); out = []
    for nom, n, kappa, forces, D in VARIANTES:
        for graine in (1, 2):
            M = bis.moteur(n, kappa, D)
            bl = M['Blob'](N0=300, seed=graine, forces=forces); tours = 0
            for cible in base.RELEVES:
                while bl.N < cible:
                    bl.step(0.12); tours += 1
                liens = base.liens_de(bl); emp = hashlib.sha256(json.dumps(liens).encode()).hexdigest()
                adj = [set(bl.adj[i]) for i in range(bl.N)]
                r = epreuve('%s, graine %d, %d constituants' % (nom, graine, bl.N), adj, dict(variante=nom, groupe=n, kappa=kappa, forces=len(forces), D=D, graine=graine, tours=tours,
                                                                                          empreinte_des_liens=emp, empreinte_deja_connue_de_X24=emp in K))
                if D == 2:
                    r['rang_2'] = rang2(adj); r['rang_2']['groupe_de_cinq_present'] = r['plus_grand_groupe_complet'] >= 5
                    r['rang_2_violee'] = bool(r['rang_2']['groupe_de_cinq_present'] or r['rang_2']['avec_plus_de_deux_voisins_communs'] or r['rang_2']['avec_deux_voisins_communs_lies_entre_eux'])
                out.append(r)
                print(json.dumps(dict(etat=r['etat'], voisins=round(r['voisins_moyens'], 2), connue=r['empreinte_deja_connue_de_X24'], plus_grand_groupe=r['plus_grand_groupe_complet'],
                                      groupes_de_5=r['groupes_de_5'], groupes_de_6=r['groupes_de_6'], triples=r['N2']['triples_tous_lies'], part_N2=r['N2']['part_satisfaisant_N2'],
                                      plus_de_six=r['N2']['avec_plus_de_six_voisins_communs'], N3_viole=r['N3']['liens_qui_violent_N3'], N1=r['N1_violee'], N2=r['N2_violee'], N3=r['N3_violee'],
                                      rang_2=r.get('rang_2'))), flush=True)
                json.dump(dict(etats=out, duree_s=round(time.time() - t0, 1)), open(os.path.join(ICI, 'x25ter_variantes.json'), 'w'), indent=1)
    print('duree', round(time.time() - t0, 1), 's')
