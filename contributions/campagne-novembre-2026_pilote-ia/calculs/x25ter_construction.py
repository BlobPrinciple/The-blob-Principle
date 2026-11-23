#!/usr/bin/env python3
"""X-25 ter, seconde partie -- CONSTRUCTION : des boules rondes de R^3, d'interieurs disjoints, dont les contacts sont exactement les liens du moteur complet de l'auteur.
Etats de reference : << blob ablation labo colab.py >>, quatre forces, kappa = 6,6, graines 1 et 2, releves a 660 et 1 037 constituants (etats de X-24 B, empreintes
controlees). Inconnues : un centre et un rayon par constituant. Depart : positions du moteur (mises a l'echelle), rayons par moindres carres sur les liens.
Minimisation (L-BFGS) de  somme_liens (d - r_i - r_j)^2 + mu x somme_non_lies max(0, (1+m)(r_i + r_j) - d)^2,  mu croissant, puis polissage de Gauss-Newton sur les
egalites des liens. Criteres ecrits avant calcul : lien : |d - r_i - r_j| <= 1e-9 (r_i + r_j) ; paire non liee : d - r_i - r_j >= 1e-6 (r_i + r_j) ; rayons > 0.
Controle separe : produit inversif p = (r_i^2 + r_j^2 - d^2) / (2 r_i r_j), -1 sur les liens, < -1 ailleurs.
Un echec de l'optimiseur ne refute rien. Prediction scellee : x25ter_moteur_et_contact_prediction.txt
(SHA-256 5aece6706f9fe693c196a5817680082cca52f1d8471030acbe11d4832599345a).
Usage : python3 x25ter_construction.py graine cible [marge]     Claude, 23 novembre 2026."""
import hashlib, json, os, sys, time
import numpy as np
from scipy.optimize import minimize
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsmr
import x24_moteur_dimension as base

ICI = os.path.dirname(os.path.abspath(__file__))


def etat(graine, cible):
    M, ech = base.moteur(3, 6.6)
    bl = M['Blob'](N0=300, seed=graine, forces=base.FORCES)
    while bl.N < cible: bl.step(0.12)
    liens = base.liens_de(bl)
    return np.array(bl.pts, float)[:bl.N], liens, hashlib.sha256(json.dumps(liens).encode()).hexdigest()


class Probleme:
    def __init__(self, X0, liens):
        self.N = N = len(X0)
        L = np.array(liens, int); self.I, self.J = L[:, 0], L[:, 1]
        lie = np.zeros((N, N), bool); lie[self.I, self.J] = True; lie[self.J, self.I] = True
        A, B = np.triu_indices(N, 1); garde = ~lie[A, B]; self.A, self.B = A[garde], B[garde]
        d = np.linalg.norm(X0[self.I] - X0[self.J], axis=1)
        self.X0 = X0 * (2.0 / np.median(d))                                  # longueur mediane des liens = 2

    def depart(self):
        N = self.N; X = self.X0.copy()
        d = np.linalg.norm(X[self.I] - X[self.J], axis=1); E = len(d)
        Jm = coo_matrix((np.ones(2 * E), (np.r_[np.arange(E), np.arange(E)], np.r_[self.I, self.J])), shape=(E, N)).tocsr()
        r = lsmr(Jm, d, atol=1e-12, btol=1e-12)[0]
        r = np.clip(r, 0.2, None)
        return np.r_[X.ravel(), np.log(r)]

    def energie(self, z, mu, m):
        N = self.N; X = z[:3 * N].reshape(N, 3); r = np.exp(z[3 * N:])
        D = X[self.I] - X[self.J]; d = np.sqrt((D * D).sum(1)); f = d - r[self.I] - r[self.J]
        e = (f * f).sum()
        gX = np.zeros((N, 3)); gr = np.zeros(N)
        c = (2 * f / d)[:, None] * D
        for k in range(3):
            gX[:, k] += np.bincount(self.I, c[:, k], N) - np.bincount(self.J, c[:, k], N)
        gr += -2 * (np.bincount(self.I, f, N) + np.bincount(self.J, f, N))
        D2 = X[self.A] - X[self.B]; d2 = np.sqrt((D2 * D2).sum(1)); g = (1 + m) * (r[self.A] + r[self.B]) - d2
        act = g > 0
        if act.any():
            a, b = self.A[act], self.B[act]; h = g[act]; e += mu * (h * h).sum()
            c2 = (2 * mu * h / d2[act])[:, None] * D2[act]
            for k in range(3):
                gX[:, k] += -np.bincount(a, c2[:, k], N) + np.bincount(b, c2[:, k], N)
            gr += 2 * mu * (1 + m) * (np.bincount(a, h, N) + np.bincount(b, h, N))
        return e, np.r_[gX.ravel(), gr * r]

    def mesures(self, z):
        N = self.N; X = z[:3 * N].reshape(N, 3); r = np.exp(z[3 * N:])
        d = np.linalg.norm(X[self.I] - X[self.J], axis=1); s = r[self.I] + r[self.J]
        d2 = np.linalg.norm(X[self.A] - X[self.B], axis=1); s2 = r[self.A] + r[self.B]
        p1 = (r[self.I] ** 2 + r[self.J] ** 2 - d ** 2) / (2 * r[self.I] * r[self.J]); p2 = (r[self.A] ** 2 + r[self.B] ** 2 - d2 ** 2) / (2 * r[self.A] * r[self.B])
        return dict(residu_relatif_max_sur_les_liens=float((np.abs(d - s) / s).max()), ecart_relatif_min_des_paires_non_liees=float(((d2 - s2) / s2).min()),
                    paires_non_liees_qui_se_chevauchent=int((d2 < s2).sum()), rayon_min=float(r.min()), rayon_max=float(r.max()),
                    produit_inversif_des_liens_ecart_max_a_moins_un=float(np.abs(p1 + 1).max()), produit_inversif_max_des_paires_non_liees=float(p2.max()))

    def polissage(self, z, tours=30):
        """Gauss-Newton de norme minimale sur les egalites des liens (les paires non liees ne sont que surveillees)."""
        N = self.N; E = len(self.I)
        for _ in range(tours):
            X = z[:3 * N].reshape(N, 3); r = np.exp(z[3 * N:])
            D = X[self.I] - X[self.J]; d = np.sqrt((D * D).sum(1)); f = d - r[self.I] - r[self.J]
            if np.abs(f).max() < 1e-14: break
            U = D / d[:, None]; e = np.arange(E)
            rows = np.r_[np.repeat(e, 3), np.repeat(e, 3), e, e]
            cols = np.r_[(3 * self.I[:, None] + np.arange(3)).ravel(), (3 * self.J[:, None] + np.arange(3)).ravel(), 3 * N + self.I, 3 * N + self.J]
            vals = np.r_[U.ravel(), (-U).ravel(), -r[self.I], -r[self.J]]
            Jm = coo_matrix((vals, (rows, cols)), shape=(E, 4 * N)).tocsr()
            dz = lsmr(Jm, -f, atol=1e-15, btol=1e-15, maxiter=20000)[0]
            z = z + dz
        return z

    def rang_des_liens(self, z):
        """Rang de la jacobienne des egalites des liens (plein rang = solution isolee a mouvements pres, existence exacte au voisinage)."""
        N = self.N; E = len(self.I); X = z[:3 * N].reshape(N, 3); r = np.exp(z[3 * N:])
        D = X[self.I] - X[self.J]; d = np.sqrt((D * D).sum(1)); U = D / d[:, None]
        Jd = np.zeros((E, 4 * N)); e = np.arange(E)
        for k in range(3):
            Jd[e, 3 * self.I + k] = U[:, k]; Jd[e, 3 * self.J + k] = -U[:, k]
        Jd[e, 3 * N + self.I] = -r[self.I]; Jd[e, 3 * N + self.J] = -r[self.J]
        sv = np.linalg.svd(Jd, compute_uv=False)
        return dict(liens=E, inconnues=4 * N, rang=int((sv > 1e-9 * sv[0]).sum()), plus_petite_valeur_singuliere=float(sv[min(E, 4 * N) - 1]), plus_grande=float(sv[0]))


def construit(graine, cible, marge=0.02, verbeux=True):
    t0 = time.time(); X0, liens, emp = etat(graine, cible)
    P = Probleme(X0, liens); z = P.depart(); hist = []
    for mu in (1.0, 10.0, 100.0, 1000.0):
        for essai in range(6):
            res = minimize(P.energie, z, args=(mu, marge), jac=True, method='L-BFGS-B', options=dict(maxiter=20000, maxfun=40000, ftol=1e-30, gtol=1e-14, maxcor=30))
            z = res.x
            if res.fun < 1e-16 or res.nit < 50: break
        mes = P.mesures(z); hist.append(dict(mu=mu, energie=float(res.fun), iterations=int(res.nit), **mes))
        if verbeux: print(json.dumps(hist[-1]), flush=True)
    z = P.polissage(z); mes = P.mesures(z)
    ok = mes['residu_relatif_max_sur_les_liens'] <= 1e-9 and mes['ecart_relatif_min_des_paires_non_liees'] >= 1e-6 and mes['rayon_min'] > 0
    r = dict(graine=graine, constituants=P.N, liens=len(liens), empreinte_des_liens=emp, marge=marge, etapes=hist, apres_polissage=mes, construction_trouvee=bool(ok), duree_s=round(time.time() - t0, 1))
    if ok and P.N <= 1100: r['jacobienne_des_liens'] = P.rang_des_liens(z)
    N = P.N
    np.savez_compressed(os.path.join(ICI, 'x25ter_construction_g%d_N%d.npz' % (graine, N)), centres=z[:3 * N].reshape(N, 3), rayons=np.exp(z[3 * N:]), liens=np.array(liens))
    return r


if __name__ == '__main__':
    graine, cible = int(sys.argv[1]), int(sys.argv[2]); marge = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
    r = construit(graine, cible, marge)
    print(json.dumps({k: v for k, v in r.items() if k != 'etapes'}), flush=True)
    json.dump(r, open(os.path.join(ICI, 'x25ter_construction_g%d_N%d.json' % (graine, r['constituants'])), 'w'), indent=1)
