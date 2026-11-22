#!/usr/bin/env python3
"""X-23 bis -- le seuil de gel de chaque etage dans le terreau du moteur, selon la taille, avec et sans bord.
Terreau = build_rgg du moteur de l'auteur (blob engine.py, sans modification) : les kappa*N/2 paires les plus courtes de N points du cube unite.
Temoin d'auditeur sans bord : memes points, distances periodiques, meme nombre de liens.
Arithmetique exacte modulo 2^31 - 1 (x23_outils). Prediction scellee : x23bis_seuil_de_gel_prediction.txt
(SHA-256 d72b06e75afecc656d463ec1d2957ddb5954321b12335ad4c71c9748a702a9ae). Claude, 22 novembre 2026."""
import importlib.util, json, os, sys, tempfile, time
os.environ.setdefault('NUMBA_CACHE_DIR', tempfile.mkdtemp(prefix='numba_x23_'))
import numpy as np
from scipy.spatial import cKDTree
import x23_outils as o

ici = os.path.dirname(os.path.abspath(__file__))
base = os.path.join(ici, '..', '..', '..', 'corpus', '03_scripts', 'SCRIPTS DIVERS BLOB')
spec = importlib.util.spec_from_file_location('blob_engine', os.path.join(base, 'blob engine.py'))
be = importlib.util.module_from_spec(spec)
sys.modules['blob_engine'] = be
spec.loader.exec_module(be)


def liens_du_moteur(nbr, deg, N):
    s = set()
    for u in range(N):
        for v in nbr[u, :deg[u]]:
            v = int(v)
            if v != u:
                s.add((min(u, v), max(u, v)))
    return sorted(s)


def terreau_sans_bord(N, graine, kappa):
    """Memes points que le moteur (meme generateur, meme graine) ; les kappa*N/2 paires les plus courtes au sens des distances periodiques."""
    rng = np.random.default_rng(graine)
    pts = rng.random((N, 3))
    E0 = int(round(N * kappa / 2))
    r = (kappa / ((N - 1) * (4.0 / 3.0) * np.pi)) ** (1.0 / 3.0)
    arbre = cKDTree(pts, boxsize=1.0)
    paires = arbre.query_pairs(1.25 * r, output_type='ndarray')
    d = pts[paires[:, 0]] - pts[paires[:, 1]]
    d -= np.round(d)
    dist = np.linalg.norm(d, axis=1)
    assert len(paires) >= E0
    ordre = np.argsort(dist)[:E0]
    return sorted((int(min(a, b)), int(max(a, b))) for a, b in paires[ordre])


def plus_grand_amas(Mb, d, rng, echantillon=64):
    """Taille du plus grand amas rigide seulement (plus rapide que la decomposition complete)."""
    n = Mb.shape[0]
    deg = Mb.sum(1) - 1
    meilleur = 1
    for i in np.argsort(-deg):
        if deg[i] + 1 <= meilleur:
            break
        reste = Mb[i].copy(); reste[i] = False
        while reste.sum() + 1 > meilleur:
            js = np.nonzero(reste)[0]
            if js.size == 0:
                break
            if js.size > echantillon:
                js = rng.choice(js, size=echantillon, replace=False)
            j = int(js[np.argmax((Mb[js] & Mb[i]).sum(1))])
            cadre = [int(i), j]
            commun = Mb[i] & Mb[j]
            while len(cadre) < d:
                c = commun.copy(); c[cadre] = False
                idx = np.nonzero(c)[0]
                if idx.size == 0:
                    break
                if idx.size > echantillon:
                    idx = rng.choice(idx, size=echantillon, replace=False)
                v = int(idx[np.argmax((Mb[idx] & commun).sum(1))])
                cadre.append(v); commun &= Mb[v]
            membres = np.nonzero(commun)[0]
            meilleur = max(meilleur, len(membres))
            reste[membres] = False
    return meilleur


def mesure(n, liens, d, rng):
    P = o.PREMIER
    pos = rng.integers(1, P, size=(n, d), dtype=np.int64)
    li = np.array([l[0] for l in liens] + [l[1] for l in liens]); co = np.array([l[1] for l in liens] + [l[0] for l in liens])
    A = o.csr_matrix((np.ones(len(li)), (li, co)), shape=(n, n))
    perm = np.asarray(o.reverse_cuthill_mckee(A, symmetric_mode=True))
    rang_de = np.empty(n, dtype=np.int64); rang_de[perm] = np.arange(n)
    ordre_liens = sorted(range(len(liens)), key=lambda e: min(rang_de[liens[e][0]], rang_de[liens[e][1]]))
    M = np.zeros((len(liens), d * n), dtype=np.int64)
    for r, e in enumerate(ordre_liens):
        a, b = liens[e]
        v = (pos[a] - pos[b]) % P
        ca, cb = rang_de[a], rang_de[b]
        M[r, d * ca:d * ca + d] = v
        M[r, d * cb:d * cb + d] = (P - v) % P
    rang, piv, dernier = o._echelonne(M, P)
    m, s = o.compte(n, len(liens), d, int(rang))
    Z = np.zeros((3, n, d), dtype=np.int64)
    for t in range(3):
        z = rng.integers(0, P, size=d * n, dtype=np.int64)
        Z[t] = o._vecteur_nul(M, piv, dernier, P, z).reshape(n, d)[rang_de]
    del M
    Mb = o._paires_rigides(pos, Z, P)
    g = plus_grand_amas(Mb, d, rng)
    return dict(mecanismes=int(m), auto_contraintes=int(s), part_plus_grand_amas=g / n)


PLAN = []
K3 = (5.4, 5.8, 6.2, 6.6, 7.0, 7.4, 7.8, 8.2, 8.6)
for N, graines in ((800, 8), (400, 8), (1600, 8), (3200, 4)):
    for k in K3:
        for g in range(graines):
            PLAN.append(('terreau', N, g, k, 3))
            if N >= 800:
                PLAN.append(('sans_bord', N, g, k, 3))
for N in (800, 1600):
    for g in range(4):
        for k in (3.6, 4.0, 4.4, 4.8, 5.2, 5.6, 6.0):
            PLAN.append(('terreau', N, g, k, 2))
            if N == 1600:
                PLAN.append(('sans_bord', N, g, k, 2))
        for k in (7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5):
            PLAN.append(('terreau', N, g, k, 4))
            if N == 1600:
                PLAN.append(('sans_bord', N, g, k, 4))
for k in (8.0, 10.0, 12.0, 14.0):
    for g in (0, 1):
        PLAN.append(('blob', 800, g, k, 3))

PLAN_TER = []
for N, graines in ((800, 16), (1600, 16), (3200, 8)):
    for g in range(graines):
        for k in (6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0):
            PLAN_TER.append(('terreau', N, g, k, 3))
            PLAN_TER.append(('sans_bord', N, g, k, 3))
for N in (800, 1600):
    for g in range(8):
        for k in (6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.0):
            PLAN_TER.append(('blob', N, g, k, 3))
        for k in (4.8, 5.0, 5.2, 5.4, 5.6, 5.8):
            PLAN_TER.append(('blob', N, g, k, 2))
        PLAN_TER.append(('blob', N, g, 6.6, 3))
for g in range(4):
    for k in (6.2, 6.4, 6.6, 6.8):
        PLAN_TER.append(('sans_bord', 4800, g, k, 3))

if __name__ == '__main__':
    # ordre : d'abord tout ce qui est petit, les N = 3200 a la fin
    ter = len(sys.argv) > 1 and sys.argv[1] == 'ter'
    if ter:
        PLAN = PLAN_TER
    PLAN.sort(key=lambda c: (c[1] > 3200, c[1] > 1600, c[1] > 800))
    fichier = os.path.join(ici, 'x23ter_seuil_fin.json' if ter else 'x23bis_seuil_de_gel.json')
    out = []
    for modele, N, g, kappa, d in PLAN:
        t0 = time.time()
        if modele == 'terreau':
            pts, nbr, deg = be.build_rgg(N, g, kappa=kappa)
            liens = liens_du_moteur(nbr, deg, N)
        elif modele == 'blob':
            pts, nbr, deg = be.build_blob(N, g, kappa=kappa)
            liens = liens_du_moteur(nbr, deg, N)
        else:
            liens = terreau_sans_bord(N, g, kappa)
        rng = np.random.default_rng([g, int(round(kappa * 10)), d, N, len(modele)])
        r = mesure(N, liens, d, rng)
        r.update(modele=modele, N=N, graine=g, kappa=kappa, etage=d, liens=len(liens), duree_s=round(time.time() - t0, 1))
        out.append(r)
        print(json.dumps(r), flush=True)
        if len(out) % 20 == 0:
            json.dump(out, open(fichier, 'w'), indent=0)
    json.dump(out, open(fichier, 'w'), indent=0)
