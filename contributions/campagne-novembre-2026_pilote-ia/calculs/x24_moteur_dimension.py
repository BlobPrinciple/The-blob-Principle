#!/usr/bin/env python3
"""X-24, partie B -- ce qui porte l'etage dans le moteur complet de l'auteur (<< blob ablation labo colab.py >>, corpus).
VARIANTE D'AUDITEUR, DECLAREE : le source de l'auteur (lignes 1 a 228, empreinte verifiee) est execute apres remplacement de texte en six endroits :
la valeur de KAPPA ; la dimension D des points (tirage de depart et deplacement du nouveau-ne) ; le volume de la boule unite dans le rayon de depart ;
les trois longueurs absolues du source (0,10 ; 0,32 ; 0,45) multipliees par ECH = r_D / r_3. Rien d'autre n'est touche.
A D = 3 et kappa = 6,6 la variante doit redonner exactement les liens du moteur non modifie (controle zero, mode << controle >>).
Prediction scellee : x24_contact_et_porteur_de_l_etage_prediction.txt (SHA-256 d287d0a3fa12fc54313064f13cc957147229992665bee313d92c74e753b8bf95).
Usage : python3 x24_moteur_dimension.py controle | python3 x24_moteur_dimension.py D kappa graine     Claude, 22 novembre 2026.
Note ajoutee apres execution : les sorties ecrites une par execution ont ete regroupees, apres controle ligne a ligne, dans x24_moteur_dimension.json et .out."""
import hashlib, json, math, os, sys, time
import numpy as np
from x23_outils import analyse_exacte

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB', 'Session 30 mai — verrou B et masters V152-V155', 'blob ablation labo colab.py')
brut = open(SRC, 'rb').read()
assert hashlib.sha256(brut).hexdigest() == '9d36fc7a847f7ed92500b7e06a910f49ed12e2b769312e7fad28f2ce13416003'
LIGNES = brut.decode('utf-8').split('\n')
FIN = next(i for i, l in enumerate(LIGNES) if l.startswith('def mesure('))
SOURCE = '\n'.join(LIGNES[:FIN])
FORCES = ("grav", "em", "weak", "bord")
RELEVES = (600, 1000)      # premier depassement : 660 et 1037 constituants


def volume_boule(D):
    return (4 / 3) * math.pi if D == 3 else math.pi ** (D / 2) / math.gamma(D / 2 + 1)


def rayon_de_depart(D, kappa, N=300):
    return (kappa / ((N - 1) * volume_boule(D))) ** (1 / D)


def moteur(D, kappa):
    """Le source de l'auteur, avec six remplacements de texte comptes un par un."""
    s = SOURCE

    def remplace(s, ancien, nouveau):
        assert s.count(ancien) == 1, (ancien, s.count(ancien))
        return s.replace(ancien, nouveau)
    s = remplace(s, 'BETA, TAU, KAPPA = 0.30, 0.50, 6.6', 'BETA, TAU, KAPPA = 0.30, 0.50, %r' % kappa)
    s = remplace(s, '(kappa/((N-1)*(4/3)*math.pi))**(1/3)', '(kappa/((N-1)*VOLD))**(1/DIM)')
    s = remplace(s, 'rng.uniform(0.0,1.0,(N,3))', 'rng.uniform(0.0,1.0,(N,DIM))')
    s = remplace(s, 'self.rng.normal(0,0.10,3)', 'self.rng.normal(0,0.10*ECH,DIM)')
    s = remplace(s, 'def vg(self,parent,newp,r=0.32):', 'def vg(self,parent,newp,r=0.32*ECH):')
    s = remplace(s, '>0.45: continue', '>0.45*ECH: continue')
    ech = 1.0 if D == 3 else rayon_de_depart(D, kappa) / rayon_de_depart(3, kappa)
    M = dict(DIM=D, VOLD=volume_boule(D), ECH=ech)
    exec(s, M)
    return M, ech


def liens_de(bl):
    return sorted((i, j) for i in range(bl.N) for j in bl.adj[i] if j > i)


def releve(bl, D, kappa, graine, tours, etages=(2, 3, 4, 5)):
    N = bl.N
    liens = liens_de(bl)
    r = dict(D=D, kappa=kappa, graine=graine, tours=tours, N=N, liens=len(liens), voisins_moyens=2 * len(liens) / N, groupes_de_quatre=len(bl._K4) if hasattr(bl, '_K4') else None,
             empreinte_des_liens=hashlib.sha256(json.dumps(liens).encode()).hexdigest())
    for d in etages:
        t0 = time.time()
        rng = np.random.default_rng([graine, N, d, D, int(round(kappa * 10))])
        a = analyse_exacte(N, liens, d, rng)
        r['etage%d' % d] = {k: v for k, v in a.items() if not k.startswith('_')}
        r['etage%d' % d]['duree_s'] = round(time.time() - t0, 1)
    return r


def execution(D, kappa, graine):
    M, ech = moteur(D, kappa)
    bl = M['Blob'](N0=300, seed=graine, forces=FORCES)
    tours = 0
    out = []
    for cible in RELEVES:
        while bl.N < cible:
            bl.step(0.12); tours += 1
        r = releve(bl, D, kappa, graine, tours); r['ech'] = ech
        out.append(r)
        print(json.dumps(r), flush=True)
    return out


def controle():
    """B0 : a D = 3 et kappa = 6,6 la variante redonne exactement les liens du moteur non modifie."""
    from c204c import Blob as BlobAuteur
    res = []
    for graine in (1, 2):
        a = BlobAuteur(N0=300, seed=graine, forces=FORCES)
        M, ech = moteur(3, 6.6)
        b = M['Blob'](N0=300, seed=graine, forces=FORCES)
        assert ech == 1.0
        for cible in RELEVES:
            while a.N < cible:
                a.step(0.12); b.step(0.12)
            la, lb = liens_de(a), liens_de(b)
            pa = np.array(a.pts); pb = np.array(b.pts)
            r = dict(graine=graine, N=a.N, N_variante=b.N, liens=len(la), liens_identiques=la == lb, positions_identiques=bool(pa.shape == pb.shape and (pa == pb).all()),
                     empreinte_des_liens=hashlib.sha256(json.dumps(la).encode()).hexdigest())
            res.append(r); print(json.dumps(r), flush=True)
    return res


if __name__ == '__main__':
    if sys.argv[1] == 'controle':
        json.dump(controle(), open(os.path.join(ICI, 'x24_moteur_dimension_controle.json'), 'w'), indent=1)
    else:
        D, kappa, graine = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
        out = execution(D, kappa, graine)
        json.dump(out, open(os.path.join(ICI, 'x24_moteur_dimension_D%d_k%s_g%d.json' % (D, ('%.1f' % kappa).replace('.', 'p'), graine)), 'w'), indent=1)
