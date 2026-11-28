#!/usr/bin/env python3
"""X-37 -- le protocole des deux horloges de l'auteur (tome V305, 23 juillet 2026, EH.3 : << taux de fermeture des K4 contre compte de
mitoses, cinq tailles, vingt graines, cible etablie avant tir >>), execute sur ses propres operateurs de mitose du 27 mai 2026 :
<< native_1_mitose_viabilite.py >> (classe BlobNatif) et << mitose_cycle.py >> (classe BlobCosmogonie), charges sans modification,
empreintes SHA-256 verifiees. Ces deux fichiers ne sont pas au depot ; ils viennent de l'archive << BLOB MASTER V293 ARCHIVE TOTALE.zip >>
du dossier de l'auteur (scripts_fermeture_v151_v152).
Prediction scellee avant tout calcul : x37_deux_horloges_prediction.txt. Claude (pilote IA), 28 novembre 2026.

Usage : x37_deux_horloges.py <dossier des scripts de l'auteur> <bras : N ou C> <graine> <N_max> <n_init> <fichier de sortie .json>
Reprise : si <sortie>.pkl existe, le calcul reprend ou il s'etait arrete (etat complet, generateur aleatoire compris)."""
import sys, io, os, json, math, time, pickle, hashlib, contextlib

EMPREINTES = {'native_1_mitose_viabilite.py': 'c200317d3f453f1ceba5076231dc0d52067bafe68bb01ef6e19b413c95281ba7',
              'mitose_cycle.py': 'ef696e8e79ef403a7d3cc6b2177654d1a921dfd17f5af089f0bcf72590e8e029'}
PAS_MAX, K4_MAX = 80, 3_000_000


def charger(dossier):
    """Execute le texte de l'auteur tel quel (pour native_1 : jusqu'a la ligne qui lance sa demonstration, non comprise)."""
    esp = {}
    for nom, h in EMPREINTES.items():
        brut = open(os.path.join(dossier, nom), 'rb').read()
        assert hashlib.sha256(brut).hexdigest() == h, 'empreinte differente : ' + nom
        L = brut.decode('utf-8').split('\n')
        if nom.startswith('native_1'):
            fin = next(i for i, l in enumerate(L) if l.startswith('print("\\nMitose native'))
            L = L[:fin]
        e = {'__name__': 'auteur'}
        with contextlib.redirect_stdout(io.StringIO()):
            exec('\n'.join(L), e)
        esp[nom] = e
    return esp['native_1_mitose_viabilite.py'], esp['mitose_cycle.py']


def pas_natif_compte(bm, esp, p_attempt=0.5, p_triangle=0.12):
    """Copie mot pour mot de BlobNatif.step_natif, avec des compteurs passifs : aucun tirage aleatoire ajoute, retire ou deplace.
    L'identite des trajectoires avec la fonction de l'auteur est verifiee par equivalence() a chaque lancement."""
    exp, TAU = esp['math'].exp, esp['TAU']
    bm.t += 1
    c = dict(essais_pure=0, essais_matiere=0, acceptes_pure=0, acceptes_matiere=0, liens_de_structuration=0)
    eds = bm.edges()
    bm.rng.shuffle(eds)
    for (u, v) in eds:
        if v not in bm.adj[u]: continue
        if bm.rng.random() > p_attempt: continue
        vois = set([u, v]) | bm.adj[u] | bm.adj[v]
        S_before = bm.S_local(vois)
        pure = bm.is_pure(u, v)
        c['essais_pure' if pure else 'essais_matiere'] += 1
        m = bm.next_id
        bm.adj[m] = set()
        bm.adj[u].discard(v); bm.adj[v].discard(u)
        bm.adj[u].add(m); bm.adj[m].add(u); bm.adj[v].add(m); bm.adj[m].add(v)
        vois2 = vois | {m}
        S_after = bm.S_local(vois2)
        dS = S_after - S_before
        accept = (dS >= 0) or (bm.rng.random() < exp(dS / TAU))
        if accept:
            bm.next_id += 1
            c['acceptes_pure' if pure else 'acceptes_matiere'] += 1
        else:
            bm.adj[u].discard(m); bm.adj[v].discard(m); del bm.adj[m]
            bm.adj[u].add(v); bm.adj[v].add(u)
    for v in list(bm.adj.keys()):
        if bm.rng.random() < p_triangle and len(bm.adj[v]) >= 2:
            nb = list(bm.adj[v]); a, bb = bm.rng.choice(len(nb), 2, replace=False)
            if nb[bb] not in bm.adj[nb[a]]:
                bm.adj[nb[a]].add(nb[bb]); bm.adj[nb[bb]].add(nb[a]); c['liens_de_structuration'] += 1
    return c


def equivalence(esp):
    """Trois graines, huit pas : la copie instrumentee et la fonction de l'auteur donnent le meme graphe, lien pour lien, a chaque pas."""
    Cls = esp['BlobNatif']
    for graine in (0, 1, 2):
        a = Cls(n_init=40, seed=graine); b = Cls(n_init=40, seed=graine)
        for _ in range(8):
            np_, nm_ = a.step_natif(); c = pas_natif_compte(b, esp)
            assert a.adj == b.adj and a.next_id == b.next_id, 'trajectoires differentes'
            assert (np_, nm_) == (c['acceptes_pure'], c['acceptes_matiere']), 'compteurs differents'
    return True


def simplexes(adj):
    """Liens, liens purs (sans voisin commun : definition de l'auteur), triangles et K4, par enumeration."""
    tri = set(); k4 = set(); pures = 0; E = 0
    for u in adj:
        Au = adj[u]
        for v in Au:
            if v <= u: continue
            E += 1
            C = Au & adj[v]
            if not C:
                pures += 1; continue
            for k in C:
                if k > v:
                    tri.add((u, v, k))
                    for l in C & adj[k]:
                        if l > k: k4.add((u, v, k, l))
    return E, pures, tri, k4


CLES = ('t', 'N', 'E', 'liens_purs', 'triangles', 'k4', 'triangles_nes', 'triangles_morts', 'k4_nes', 'k4_morts', 'mitoses', 'degre_max',
        'essais_pure', 'essais_matiere', 'acceptes_pure', 'acceptes_matiere', 'liens_de_structuration')


def lancer(dossier, bras, graine, n_max, n_init, sortie, budget_s=1e9):
    t0 = time.time(); natif, cycle = charger(dossier)
    Cls = natif['BlobNatif'] if bras == 'N' else cycle['BlobCosmogonie']
    equiv = equivalence(natif) if bras == 'N' else None
    pkl = sortie + '.pkl'
    if os.path.exists(pkl):
        d, S, tri, k4, garde = pickle.load(open(pkl, 'rb')); bm = Cls.__new__(Cls); bm.__dict__.update(d)
    else:
        bm = Cls(n_init=n_init, seed=graine); S = {k: [] for k in CLES}; garde = None
        E, pures, tri, k4 = simplexes(bm.adj)
        for k, x in zip(CLES, (0, len(bm.adj), E, pures, len(tri), len(k4), 0, 0, 0, 0, 0, max(len(a) for a in bm.adj.values()), 0, 0, 0, 0, 0)): S[k].append(x)
    while S['N'][-1] < n_max and garde is None:
        if time.time() - t0 > budget_s:
            break
        avant = bm.next_id
        if bras == 'N':
            c = pas_natif_compte(bm, natif)
        else:
            bm.step(); c = {}
        E, pures, tri2, k42 = simplexes(bm.adj)
        ligne = dict(t=bm.t, N=len(bm.adj), E=E, liens_purs=pures, triangles=len(tri2), k4=len(k42), triangles_nes=len(tri2 - tri), triangles_morts=len(tri - tri2),
                     k4_nes=len(k42 - k4), k4_morts=len(k4 - k42), mitoses=bm.next_id - avant, degre_max=max(len(a) for a in bm.adj.values()))
        ligne.update(c)
        for k in CLES: S[k].append(ligne.get(k, 0))
        tri, k4 = tri2, k42
        if bm.t >= PAS_MAX: garde = 'nombre de pas maximal atteint'
        elif len(k4) > K4_MAX: garde = 'plus de trois millions de K4'
        pickle.dump((bm.__dict__, S, tri, k4, garde), open(pkl + '.tmp', 'wb')); os.replace(pkl + '.tmp', pkl)
    fini = S['N'][-1] >= n_max or garde is not None
    r = dict(bras=bras, graine=graine, n_init=n_init, N_max=n_max, fini=fini, garde=garde, equivalence_verifiee=equiv, series=S)
    json.dump(r, open(sortie, 'w'))
    return r


if __name__ == '__main__':
    dossier, bras, graine, n_max, n_init, sortie = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    budget = float(sys.argv[7]) if len(sys.argv) > 7 else 1e9
    r = lancer(dossier, bras, graine, n_max, n_init, sortie, budget)
    print(json.dumps(dict(bras=bras, graine=graine, fini=r['fini'], garde=r['garde'], pas=r['series']['t'][-1], N=r['series']['N'][-1], k4=r['series']['k4'][-1])))
