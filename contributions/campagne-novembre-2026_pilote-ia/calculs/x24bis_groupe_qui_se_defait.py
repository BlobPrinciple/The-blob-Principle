#!/usr/bin/env python3
"""X-24 bis -- quelle regle du moteur complet de l'auteur fait l'etage 3 ? Le groupe qui se defait.
VARIANTES D'AUDITEUR, DECLAREES : en plus des six remplacements de x24_moteur_dimension.py (ici D = 3, donc sans effet), trois remplacements de texte dans la
partie << cycle + faible >> du source de l'auteur : (7) recherche des groupes de n constituants tous lies (n = 3, 4, 5 ; n = 4 : fonction de l'auteur) ;
(8) tirage du lien retire parmi n constituants ; (9) taux 0,236 remplace par 0 pour << sans desintegration >> (n = 0).
Controle zero : n = 4, taux 0,236, sans force = moteur non modifie lance sans force.
Prediction scellee : x24bis_groupe_qui_se_defait_prediction.txt (SHA-256 d2e6d730301f0a0c766b7520c14d8b5dfde54597e4c13ffb8bfe3e0da0aaf598).
Usage : python3 x24bis_groupe_qui_se_defait.py controle | n kappa graine forces(0, 4 ou sans_<force>) [D]
Le mode sans_<force> sert X-24 ter (prediction x24ter_quelle_force_prediction.txt), ajoute apres l'execution de X-24 bis : le plan bis n'a pas change.     Claude, 22 novembre 2026.
Note ajoutee apres execution : les sorties ecrites une par execution ont ete regroupees dans x24bis_groupe_qui_se_defait.json et .out, et x24ter_quelle_force.json et .out."""
import hashlib, json, os, sys, time
import numpy as np
from x23_outils import analyse_exacte
import x24_moteur_dimension as base

ICI = os.path.dirname(os.path.abspath(__file__))
RELEVES = (600, 1000)
QUATRE_FORCES = ("grav", "em", "weak", "bord")


def groupes_de_trois(adj, N):
    out = []
    for i in range(N):
        for j in adj[i]:
            if j <= i: continue
            for k in adj[i] & adj[j]:
                if k > j: out.append((i, j, k))
    return out


def groupes_de_cinq(adj, N):
    out = []
    for i in range(N):
        Ni = adj[i]
        for j in Ni:
            if j <= i: continue
            cij = Ni & adj[j]
            for k in cij:
                if k <= j: continue
                cijk = cij & adj[k]
                for l in cijk:
                    if l <= k: continue
                    for m in cijk & adj[l]:
                        if m > l: out.append((i, j, k, l, m))
    return out


def moteur(n, kappa, D=3):
    """Source de l'auteur avec les six remplacements de base, puis les trois de ce complement, comptes un par un."""
    s = base.SOURCE

    def remplace(s, ancien, nouveau):
        assert s.count(ancien) == 1, (ancien, s.count(ancien))
        return s.replace(ancien, nouveau)
    s = remplace(s, 'BETA, TAU, KAPPA = 0.30, 0.50, 6.6', 'BETA, TAU, KAPPA = 0.30, 0.50, %r' % kappa)
    s = remplace(s, '(kappa/((N-1)*(4/3)*math.pi))**(1/3)', '(kappa/((N-1)*VOLD))**(1/DIM)')
    s = remplace(s, 'rng.uniform(0.0,1.0,(N,3))', 'rng.uniform(0.0,1.0,(N,DIM))')
    s = remplace(s, 'self.rng.normal(0,0.10,3)', 'self.rng.normal(0,0.10*ECH,DIM)')
    s = remplace(s, 'def vg(self,parent,newp,r=0.32):', 'def vg(self,parent,newp,r=0.32*ECH):')
    s = remplace(s, '>0.45: continue', '>0.45*ECH: continue')
    s = remplace(s, 'K4=find_all_K4(self.adj,self.N); cur=set(key(q) for q in K4)', 'K4=TROUVE(self.adj,self.N); cur=set(key(q) for q in K4)')
    s = remplace(s, 'i,j=self.rng.choice(4,2,replace=False)', 'i,j=self.rng.choice(TAILLE,2,replace=False)')
    s = remplace(s, 'p_eff=0.236*math.exp(-age/8)', 'p_eff=TAUX*math.exp(-age/8)')
    ech = 1.0 if D == 3 else base.rayon_de_depart(D, kappa) / base.rayon_de_depart(3, kappa)
    M = dict(DIM=D, VOLD=base.volume_boule(D), ECH=ech, TAILLE=(n if n else 4), TAUX=(0.236 if n else 0.0))
    exec(s, M)
    M['TROUVE'] = {0: M['find_all_K4'], 4: M['find_all_K4'], 3: groupes_de_trois, 5: groupes_de_cinq}[n]
    return M


def releve(bl, n, kappa, graine, forces, tours, D):
    N = bl.N
    liens = base.liens_de(bl)
    r = dict(groupe=n, kappa=kappa, graine=graine, forces=len(forces), D=D, tours=tours, N=N, liens=len(liens), voisins_moyens=2 * len(liens) / N, groupes_presents=len(bl._K4),
             empreinte_des_liens=hashlib.sha256(json.dumps(liens).encode()).hexdigest())
    for d in (2, 3, 4, 5, 6):
        t0 = time.time()
        rng = np.random.default_rng([graine, N, d, n, int(round(kappa * 10)), len(forces)])
        a = analyse_exacte(N, liens, d, rng)
        r['etage%d' % d] = {k: v for k, v in a.items() if not k.startswith('_')}
        r['etage%d' % d]['duree_s'] = round(time.time() - t0, 1)
    return r


def execution(n, kappa, graine, forces, D=3):
    M = moteur(n, kappa, D)
    bl = M['Blob'](N0=300, seed=graine, forces=forces)
    tours = 0; out = []
    for cible in RELEVES:
        while bl.N < cible:
            bl.step(0.12); tours += 1
        r = releve(bl, n, kappa, graine, forces, tours, D); out.append(r)
        print(json.dumps(r), flush=True)
    return out


def controle():
    """Q0 : n = 4, taux 0,236, sans force = moteur non modifie lance sans force."""
    from c204c import Blob as BlobAuteur
    res = []
    for graine in (1, 2):
        a = BlobAuteur(N0=300, seed=graine, forces=())
        b = moteur(4, 6.6)['Blob'](N0=300, seed=graine, forces=())
        for cible in RELEVES:
            while a.N < cible:
                a.step(0.12); b.step(0.12)
            la, lb = base.liens_de(a), base.liens_de(b)
            r = dict(graine=graine, N=a.N, liens=len(la), voisins_moyens=2 * len(la) / a.N, liens_identiques=la == lb)
            res.append(r); print(json.dumps(r), flush=True)
    return res


if __name__ == '__main__':
    if sys.argv[1] == 'controle':
        json.dump(controle(), open(os.path.join(ICI, 'x24bis_controle.json'), 'w'), indent=1)
    else:
        n, kappa, graine = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
        D = int(sys.argv[5]) if len(sys.argv) > 5 else 3
        if sys.argv[4].startswith('sans_'):          # X-24 ter : ablation simple d'une force, les trois autres actives
            forces = tuple(f for f in QUATRE_FORCES if f != sys.argv[4][5:]); assert len(forces) == 3
            nom = 'x24ter_%s_k%s_g%d.json' % (sys.argv[4], ('%.1f' % kappa).replace('.', 'p'), graine)
        else:
            nf = int(sys.argv[4]); forces = QUATRE_FORCES if nf else ()
            nom = 'x24bis_n%d_k%s_g%d_f%d%s.json' % (n, ('%.1f' % kappa).replace('.', 'p'), graine, nf, '' if D == 3 else '_D%d' % D)
        out = execution(n, kappa, graine, forces, D)
        json.dump(out, open(os.path.join(ICI, nom), 'w'), indent=1)
