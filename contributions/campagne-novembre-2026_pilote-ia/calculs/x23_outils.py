#!/usr/bin/env python3
"""X-23 -- outils communs : rigidite generique d'un reseau a l'etage d (dimension d), sans position posee.
Un reseau << tient l'etage d >> s'il est generiquement rigide en dimension d : on tire des positions au hasard dans R^d et on lit le rang de la matrice de rigidite.
Deux lectures independantes du rang : (1) valeurs propres de H = R^T R en virgule flottante ; (2) elimination de Gauss exacte modulo le nombre premier 2^31 - 1
sur des positions entieres tirees au hasard (une borne inferieure du rang generique, egale a lui avec une probabilite ecrasante).
Prediction scellee : x23_regle_de_l_etage_prediction.txt. Claude, 22 novembre 2026."""
import itertools
import numpy as np

PREMIER = 2147483647  # 2^31 - 1


def liens_des_cellules(cellules):
    """Liens (paires) portes par une liste de cellules (ensembles de sommets)."""
    E = set()
    for F in cellules:
        for a, b in itertools.combinations(sorted(F), 2):
            E.add((a, b))
    return sorted(E)


def matrice_de_rigidite(n, liens, pos):
    d = pos.shape[1]
    R = np.zeros((len(liens), d * n))
    for r, (a, b) in enumerate(liens):
        v = pos[a] - pos[b]
        R[r, d * a:d * a + d] = v
        R[r, d * b:d * b + d] = -v
    return R


def rang_exact(n, liens, d, rng):
    """Rang de la matrice de rigidite modulo 2^31 - 1, positions entieres aleatoires. Arithmetique entiere exacte (produits < 2^62)."""
    P = PREMIER
    pos = rng.integers(1, P, size=(n, d), dtype=np.int64)
    M = np.zeros((len(liens), d * n), dtype=np.int64)
    for r, (a, b) in enumerate(liens):
        v = (pos[a] - pos[b]) % P
        M[r, d * a:d * a + d] = v
        M[r, d * b:d * b + d] = (-v) % P
    rang = 0
    lignes, colonnes = M.shape
    for c in range(colonnes):
        if rang == lignes:
            break
        nz = np.nonzero(M[rang:, c])[0]
        if nz.size == 0:
            continue
        p = rang + int(nz[0])
        if p != rang:
            M[[rang, p]] = M[[p, rang]]
        inv = pow(int(M[rang, c]), P - 2, P)
        M[rang] = (M[rang] * inv) % P
        dessous = np.nonzero(M[rang + 1:, c])[0] + rang + 1
        if dessous.size:
            f = M[dessous, c][:, None]
            M[dessous] = (M[dessous] - f * M[rang][None, :]) % P
        rang += 1
    return rang


def compte(n, nb_liens, d, rang):
    """(mecanismes, auto-contraintes) a l'etage d. Convention du corpus (V346 p. 1096) : mecanismes = d*n - d(d+1)/2 - rang."""
    assert n >= d + 1, "il faut au moins d+1 constituants"
    return d * n - d * (d + 1) // 2 - rang, nb_liens - rang


def etage(n, liens, d, rng, exact=True, seuil=1e-9):
    """Rang flottant (positions normales) et, si demande, rang exact modulo p. Renvoie un dictionnaire."""
    pos = rng.standard_normal((n, d))
    R = matrice_de_rigidite(n, liens, pos)
    sv = np.linalg.svd(R, compute_uv=False) if R.size else np.zeros(0)
    rang = int((sv > seuil * sv[0]).sum()) if sv.size else 0
    ecart = None
    if 0 < rang < sv.size:
        ecart = float(sv[rang - 1] / max(sv[rang], 1e-300))
    m, s = compte(n, len(liens), d, rang)
    r = dict(d=d, rang=rang, mecanismes=m, auto_contraintes=s, ecart_spectral=ecart)
    if exact:
        re = rang_exact(n, liens, d, rng)
        r['rang_exact'] = re
        r['accord'] = bool(re == rang)
    return r


def analyse_complete(n, liens, pos, rng, sondes=12, seuil=1e-9, tol_paire=1e-7, leviers=False):
    """Spectre de H = R^T R, espace nul, paires mutuellement rigides (par sondes aleatoires de l'espace nul), amas rigides.
    Renvoie mecanismes, auto-contraintes, plus grand amas, taille du plus grand amas contenant chaque constituant, et (option) la part redondante de chaque lien."""
    d = pos.shape[1]
    R = matrice_de_rigidite(n, liens, pos)
    H = R.T @ R
    w, U = np.linalg.eigh(H)
    nul = w < seuil * w[-1]
    k0 = int(nul.sum())
    rang = d * n - k0
    m, s = compte(n, len(liens), d, rang)
    ecart = float(w[k0] / max(abs(w[k0 - 1]), 1e-300)) if 0 < k0 < len(w) else None
    res = dict(d=d, rang=rang, mecanismes=m, auto_contraintes=s, ecart_spectral=ecart)
    # paires rigides : (p_j - p_i).(z_j - z_i) = 0 pour tout mouvement z de l'espace nul ; on sonde par des combinaisons aleatoires
    U0 = U[:, :k0]
    G = rng.standard_normal((k0, sondes))
    Z = U0 @ G
    Z /= np.linalg.norm(Z, axis=0, keepdims=True)
    Q = np.zeros((n, n))
    for t in range(sondes):
        z = Z[:, t].reshape(n, d)
        sdiag = (pos * z).sum(1)
        croise = pos @ z.T
        T = sdiag[:, None] + sdiag[None, :] - croise - croise.T
        Q += T * T
    Q = np.sqrt(Q)
    echelle = np.sqrt((pos ** 2).sum(1).mean()) / np.sqrt(d * n)
    M = Q < tol_paire * echelle
    np.fill_diagonal(M, True)
    hors = Q[~M]
    dedans = Q[M & ~np.eye(n, dtype=bool)]
    res['marge_paires'] = [float(dedans.max() / echelle) if dedans.size else None, float(hors.min() / echelle) if hors.size else None]
    meilleur, tailles = amas_rigides(M, d, rng)
    res['plus_grand_amas'] = int(meilleur.max())
    res['part_plus_grand_amas'] = float(meilleur.max() / n)
    res['part_figee'] = float((meilleur >= d + 1).mean())
    res['nombre_amas_d_au_moins_d_plus_1'] = int(sum(1 for t in tailles if t >= d + 1))
    res['_meilleur'] = meilleur
    if leviers:
        Up = U[:, k0:]
        Y = R @ Up
        lev = (Y * Y / w[k0:][None, :]).sum(1)
        red = 1.0 - lev                                  # part redondante de chaque lien ; somme = auto-contraintes
        res['_redondance'] = red
        res['somme_redondance'] = float(red.sum())
        lib = (U0.reshape(n, d, k0) ** 2).sum(axis=(1, 2))   # part de liberte de chaque constituant ; somme = dimension de l'espace nul
        res['_liberte'] = lib
    return res


def amas_rigides(M, d, rng, echantillon=64):
    """Amas rigides = ensembles maximaux de constituants deux a deux rigides. Deux amas distincts partagent au plus d-1 constituants :
    d constituants deux a deux rigides (en position generale) fixent un amas unique = tous les constituants rigides avec chacun d'eux."""
    n = M.shape[0]
    meilleur = np.ones(n, dtype=int)
    couvert = np.eye(n, dtype=bool)
    tailles = []
    ordre = np.argsort(-M.sum(1))
    for i in ordre:
        reste = M[i] & ~couvert[i]
        while reste.any():
            js = np.nonzero(reste)[0]
            if js.size > echantillon:
                js = rng.choice(js, size=echantillon, replace=False)
            j = int(js[np.argmax((M[js] & M[i]).sum(1))])
            cadre = [int(i), j]
            commun = M[i] & M[j]
            while len(cadre) < d:
                c = commun.copy()
                c[cadre] = False
                idx = np.nonzero(c)[0]
                if idx.size == 0:
                    break
                if idx.size > echantillon:
                    idx = rng.choice(idx, size=echantillon, replace=False)
                v = int(idx[np.argmax((M[idx] & commun).sum(1))])
                cadre.append(v)
                commun &= M[v]
            membres = np.nonzero(commun)[0]
            sous = M[np.ix_(membres, membres)]
            while not sous.all():                          # garde-fou numerique : retirer le moins lie jusqu'a obtenir un ensemble deux a deux rigide
                pire = int(np.argmin(sous.sum(1)))
                if membres[pire] in cadre[:2]:
                    lignes = sous.sum(1).astype(float)
                    for q, mm in enumerate(membres):
                        if mm in cadre[:2]:
                            lignes[q] = np.inf
                    pire = int(np.argmin(lignes))
                membres = np.delete(membres, pire)
                sous = M[np.ix_(membres, membres)]
            couvert[np.ix_(membres, membres)] = True
            meilleur[membres] = np.maximum(meilleur[membres], len(membres))
            tailles.append(len(membres))
            reste = M[i] & ~couvert[i]
    return meilleur, tailles


# =====================================================================================================================
# LECTURE EXACTE (ajoutee apres le premier essai sur le moteur, 22 novembre) : en virgule flottante, le spectre de H n'a pas de trou net
# (plus petite valeur propre non nulle a un facteur 8 seulement de la plus grande << nulle >>) : ni le rang ni les amas ne sont fiables.
# Tout est donc refait en arithmetique entiere exacte modulo 2^31 - 1 : rang, vecteurs de l'espace nul, paires rigides. Aucun seuil.
# =====================================================================================================================
from numba import njit
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee


@njit(cache=False)
def _inverse(a, P):
    r = 1
    e = P - 2
    b = a % P
    while e > 0:
        if e & 1:
            r = (r * b) % P
        b = (b * b) % P
        e >>= 1
    return r


@njit(cache=False)
def _echelonne(M, P):
    """Forme echelonnee en place (pivots ramenes a 1, zeros sous les pivots). Renvoie le rang, les colonnes pivots et la derniere colonne non nulle de chaque ligne."""
    lignes, colonnes = M.shape
    dernier = np.zeros(lignes, np.int64)
    for i in range(lignes):
        l = -1
        for j in range(colonnes):
            if M[i, j] != 0:
                l = j
        dernier[i] = l
    piv = np.empty(lignes, np.int64)
    r = 0
    for c in range(colonnes):
        if r == lignes:
            break
        p = -1
        for i in range(r, lignes):
            if M[i, c] != 0:
                p = i
                break
        if p < 0:
            continue
        if p != r:
            for j in range(c, colonnes):
                t = M[r, j]; M[r, j] = M[p, j]; M[p, j] = t
            t = dernier[r]; dernier[r] = dernier[p]; dernier[p] = t
        inv = _inverse(M[r, c], P)
        lr = dernier[r]
        for j in range(c, lr + 1):
            M[r, j] = (M[r, j] * inv) % P
        for i in range(r + 1, lignes):
            f = M[i, c]
            if f != 0:
                g = P - f
                for j in range(c, lr + 1):
                    x = M[r, j]
                    if x != 0:
                        M[i, j] = (M[i, j] + g * x) % P
                if dernier[i] < lr:
                    dernier[i] = lr
        piv[r] = c
        r += 1
    return r, piv[:r].copy(), dernier


@njit(cache=False)
def _vecteur_nul(M, piv, dernier, P, z):
    """Un vecteur de l'espace nul : les colonnes libres gardent la valeur aleatoire recue dans z, les colonnes pivots sont resolues en remontant."""
    for r in range(piv.shape[0] - 1, -1, -1):
        c = piv[r]
        acc = 0
        for j in range(c + 1, dernier[r] + 1):
            x = M[r, j]
            if x != 0:
                acc = (acc + x * z[j]) % P
        z[c] = (P - acc) % P
    return z


@njit(cache=False)
def _paires_rigides(pos, Z, P):
    """M[i, j] vrai si (p_j - p_i).(z_j - z_i) = 0 modulo P pour chaque vecteur nul z fourni."""
    n, d = pos.shape
    S = Z.shape[0]
    Mb = np.ones((n, n), np.bool_)
    for i in range(n):
        for j in range(i + 1, n):
            ok = True
            for t in range(S):
                acc = 0
                for a in range(d):
                    dp = pos[j, a] - pos[i, a]
                    if dp < 0:
                        dp += P
                    dz = Z[t, j, a] - Z[t, i, a]
                    if dz < 0:
                        dz += P
                    acc = (acc + dp * dz) % P
                if acc != 0:
                    ok = False
                    break
            Mb[i, j] = ok
            Mb[j, i] = ok
    return Mb


def positions_reelles_exactes(pts):
    """Les positions du moteur sont des nombres flottants, donc des fractions dyadiques exactes : on les met au meme denominateur et on reduit modulo P.
    Le rang obtenu est celui de la matrice de rigidite AUX positions reelles (modulo P), sans tirage."""
    P = PREMIER
    pts = np.asarray(pts, float)
    fr = [[float(x).as_integer_ratio() for x in ligne] for ligne in pts]
    kmax = max(den.bit_length() - 1 for ligne in fr for _, den in ligne)
    out = np.zeros(pts.shape, dtype=np.int64)
    for i, ligne in enumerate(fr):
        for a, (num, den) in enumerate(ligne):
            k = den.bit_length() - 1
            out[i, a] = (num % P) * pow(2, kmax - k, P) % P
    return out


def analyse_exacte(n, liens, d, rng, pos=None, sondes=4, amas=True):
    """Rang exact modulo 2^31 - 1 a l'etage d ; paires rigides exactes ; amas rigides. pos = positions entieres (sinon tirees au hasard)."""
    P = PREMIER
    if pos is None:
        pos = rng.integers(1, P, size=(n, d), dtype=np.int64)
    pos = np.asarray(pos, dtype=np.int64) % P
    # ordre des sommets qui resserre la bande (Cuthill-McKee inverse) : ne change pas le rang, accelere l'elimination
    li = np.array([l[0] for l in liens] + [l[1] for l in liens]); co = np.array([l[1] for l in liens] + [l[0] for l in liens])
    A = csr_matrix((np.ones(len(li)), (li, co)), shape=(n, n))
    perm = np.asarray(reverse_cuthill_mckee(A, symmetric_mode=True))
    rang_de = np.empty(n, dtype=np.int64); rang_de[perm] = np.arange(n)
    ordre_liens = sorted(range(len(liens)), key=lambda e: min(rang_de[liens[e][0]], rang_de[liens[e][1]]))
    M = np.zeros((len(liens), d * n), dtype=np.int64)
    for r, e in enumerate(ordre_liens):
        a, b = liens[e]
        v = (pos[a] - pos[b]) % P
        ca, cb = rang_de[a], rang_de[b]
        M[r, d * ca:d * ca + d] = v
        M[r, d * cb:d * cb + d] = (P - v) % P
    rang, piv, dernier = _echelonne(M, P)
    m, s = compte(n, len(liens), d, int(rang))
    res = dict(d=d, rang=int(rang), mecanismes=int(m), auto_contraintes=int(s))
    if not amas:
        return res
    Z = np.zeros((sondes, n, d), dtype=np.int64)
    for t in range(sondes):
        z = rng.integers(0, P, size=d * n, dtype=np.int64)
        z = _vecteur_nul(M, piv, dernier, P, z)
        Z[t] = z.reshape(n, d)[rang_de]          # retour a la numerotation d'origine
    Mb = _paires_rigides(pos, Z, P)
    # controle interne : chaque lien du reseau doit etre une paire rigide (sinon le vecteur nul est faux)
    for a, b in liens:
        assert Mb[a, b], 'vecteur nul invalide'
    meilleur, tailles = amas_rigides(Mb, d, rng)
    res['plus_grand_amas'] = int(meilleur.max())
    res['part_plus_grand_amas'] = float(meilleur.max() / n)
    res['part_figee'] = float((meilleur >= d + 1).mean())
    res['nombre_amas_d_au_moins_d_plus_1'] = int(sum(1 for t in tailles if t >= d + 1))
    res['part_des_paires_rigides'] = float((Mb.sum() - n) / (n * (n - 1)))
    res['_meilleur'] = meilleur
    return res
