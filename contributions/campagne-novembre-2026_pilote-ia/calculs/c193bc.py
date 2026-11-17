#!/usr/bin/env python3
"""C-193Bc -- contre-calcul independant du C-193B de ChatGPT (Claude, 17 novembre 2026), d'apres son seul PROTOCOLE SCELLE : identites d'Euler d'une boule et du tore triangules,
machine temoin << chemin puis fermeture de toutes les paires a distance 2 >> avec registre d'energie, relecture des etats a 13 porteurs de C-192. La machine est une hypothese d'AUDITEUR de ChatGPT,
pas la mitose du master. Predictions : c193bc_prediction.txt. Usage : python3 c193bc.py -> c193bc.json"""
import itertools, json, math
from collections import Counter
import numpy as np
import c189dc, c190c

def complexe(aretes, n):
    """cliques de 4 du graphe ; faces et nombre de tetraedres par face."""
    A = [set() for _ in range(n)]
    for i, j in aretes: A[i].add(j); A[j].add(i)
    T = [(i, j, k, l) for i in range(n) for j in A[i] if j > i for k in A[i] & A[j] if k > j for l in A[i] & A[j] & A[k] if l > k]
    F = Counter(f for t in T for f in itertools.combinations(t, 3))
    tri = sum(1 for i in range(n) for j in A[i] if j > i for k in A[i] & A[j] if k > j)
    return T, F, tri

def bilan_boule(V, E, T, F):
    Fb = sum(1 for v in F.values() if v == 1); return dict(V=V, E=E, T=len(T), F=len(F), Fb=Fb, surchargees=sum(1 for v in F.values() if v > 2), exces=E - (V - 1), T_plus_demi_Fb=len(T) + Fb / 2, identite=bool(E - (V - 1) == len(T) + Fb / 2), euler=V - E + len(F) - len(T))

def graphe_de_contacts(X, seuil):
    n = len(X); D = np.linalg.norm(X[:, None] - X[None], axis=2); return [(i, j) for i in range(n) for j in range(i + 1, n) if D[i, j] <= seuil]

def boule_empilee(rng, n):
    """depart : un tetraedre ; chaque etape colle un sommet neuf sur une face du bord : toujours une boule."""
    T = [(0, 1, 2, 3)]; out = []
    for v in range(4, n):
        F = Counter(f for t in T for f in itertools.combinations(sorted(t), 3)); bord = sorted(f for f, c in F.items() if c == 1); f = bord[int(rng.integers(len(bord)))]; T.append(tuple(sorted(f + (v,))))
        E = set(e for t in T for e in itertools.combinations(sorted(t), 2)); F = Counter(f for t in T for f in itertools.combinations(sorted(t), 3)); out.append(bilan_boule(v + 1, len(E), T, F))
    return out

def tore_plein(m=7):
    """prisme triangulaire x cercle (m tranches), chaque prisme coupe en 3 tetraedres (decoupe coherente par ordre des sommets) : faces dans 1 ou 2 tetraedres, mais pas une boule."""
    idx = lambda s, a: (s % m) * 3 + a; T = []
    for s in range(m):
        a = [idx(s, 0), idx(s, 1), idx(s, 2)]; b = [idx(s + 1, 0), idx(s + 1, 1), idx(s + 1, 2)]
        T += [(a[0], a[1], a[2], b[2]), (a[0], a[1], b[1], b[2]), (a[0], b[0], b[1], b[2])]
    T = [tuple(sorted(t)) for t in T]; E = set(e for t in T for e in itertools.combinations(t, 2)); F = Counter(f for t in T for f in itertools.combinations(t, 3)); return bilan_boule(3 * m, len(E), T, F)

def machine(N, fermeture=True):
    aretes = set(); B = 0; journal = []; actifs, dormants = 1, N - 1
    for v in range(1, N):
        aretes.add((v - 1, v)); B += 1; actifs += 1; dormants -= 1; journal.append(dict(etape='naissance', N=actifs, F=dormants, M=len(aretes), U=-len(aretes), B=B, E_tot=-len(aretes) + B))
    t = 0
    while fermeture and len(aretes) < N * (N - 1) // 2:
        A = [set() for _ in range(N)]
        for i, j in aretes: A[i].add(j); A[j].add(i)
        neuves = set((i, k) for i in range(N) for j in A[i] for k in A[j] if k > i and k not in A[i]); aretes |= neuves; B += len(neuves); t += 1
        T, F, tri = complexe(aretes, N); k = min(2 ** t, N - 1)
        journal.append(dict(etape='tour %d' % t, N=actifs, F=dormants, M=len(aretes), M_predit=k * N - k * (k + 1) // 2, neuves=len(neuves), U=-len(aretes), B=B, E_tot=-len(aretes) + B, tetraedres=len(T), triangles=tri, faces_surchargees=sum(1 for v in F.values() if v > 2),
                            faces_a_un=sum(1 for v in F.values() if v == 1), puissance_du_chemin=bool(aretes == set((i, j) for i in range(N) for j in range(i + 1, N) if j - i <= k))))
    T, F, tri = complexe(aretes, N)
    return dict(N=N, tours=t, tours_predits=(math.ceil(math.log2(N - 1)) if fermeture else 0), M_final=len(aretes), tetraedres_final=len(T), surchargees_final=sum(1 for v in F.values() if v > 2), journal=journal)

if __name__ == '__main__':
    out = {}
    # B1 : boules
    phi = (1 + 5 ** .5) / 2; ico = np.array([p for a in (1, -1) for b in (phi, -phi) for p in ((0, a, b), (a, b, 0), (b, 0, a))], float); ico /= np.linalg.norm(ico[0]); ico13 = np.vstack([[0, 0, 0], ico])
    bip = np.array([[0, 0, .5], [0, 0, -.5]] + [[.8507 * math.cos(2 * math.pi * k / 5), .8507 * math.sin(2 * math.pi * k / 5), 0] for k in range(5)])
    tet = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / 8 ** .5
    out['boules'] = {}
    for nom, X, s in (('tetraedre', tet, 1.01), ('bipyramide LJ7', bip, 1.10), ('icosaedre centre LJ13', ico13, 1.10)):
        E = graphe_de_contacts(X, s); T, F, _ = complexe(E, len(X)); out['boules'][nom] = bilan_boule(len(X), len(E), T, F); print('B1', nom, out['boules'][nom])
    rng = np.random.default_rng(193); emp = [b for _ in range(20) for b in boule_empilee(rng, 30)]; out['boules_empilees'] = dict(etats=len(emp), identite_vraie=sum(b['identite'] for b in emp), euler=sorted(set(b['euler'] for b in emp)))
    print('B1 boules empilees', out['boules_empilees']); out['tore_plein'] = tore_plein(); print('B1 reserve, tore plein', out['tore_plein'])
    # B2 : tore T^3
    out['tore'] = {}
    for nom, m in (('A15', c189dc.mesure(c189dc.A15, 1.30)), ('C15', c189dc.mesure(c189dc.C15, 1.30))):
        V, E, T = m['atomes_par_maille'], m['liens_par_maille'], m['tetraedres_par_maille']; out['tore'][nom] = dict(V=V, E=E, T=T, identite=bool(E == V + T)); print('B2', nom, out['tore'][nom])
    m = c190c.mesure(1.30); out['tore']['sigma'] = dict(V=30, E=m['liens'], T=m['tetraedres'], identite=bool(m['liens'] == 30 + m['tetraedres'])); print('B2 sigma', out['tore']['sigma'])
    # B3, B4 : machine
    out['machine'] = {}; out['temoin'] = {}
    for N in (4, 5, 6, 7, 13, 19):
        r = machine(N); out['machine'][N] = r; w = machine(N, False); out['temoin'][N] = dict(M=w['M_final'], tetraedres=w['tetraedres_final'], E_tot=[j['E_tot'] for j in w['journal']][-1])
        tours = [j for j in r['journal'] if j['etape'].startswith('tour')]
        print('B3 N', N, 'tours', r['tours'], 'predits', r['tours_predits'], '| aretes', [N - 1] + [j['M'] for j in tours], 'conformes', all(j['M'] == j['M_predit'] and j['puissance_du_chemin'] for j in tours), '| tetra', [j['tetraedres'] for j in tours],
              '| surchargees', [j['faces_surchargees'] for j in tours], '| faces a un seul tetra', [j['faces_a_un'] for j in tours], '| E_tot max', max(abs(j['E_tot']) for j in r['journal']), '| N+F', sorted(set(j['N'] + j['F'] for j in r['journal'])), '| temoin', out['temoin'][N])
    # B6, B7 : relecture de mes etats C-192Uc a 13 porteurs
    d = json.load(open('c192uc.json')); out['relecture'] = {}
    for bras in ('LJ', 'WCA'):
        L = [(r['graine'], r['etats']['13']) for r in d[bras]]; out['relecture'][bras] = [dict(graine=g, M=e['contacts'], g=e['contacts'] - e['contacts_non_genealogiques'], non_genealogiques=e['contacts_non_genealogiques'], deficit=42 - e['contacts'], tetraedres=e['tetraedres']) for g, e in L]
        print('B6', bras, 'M', [x['M'] for x in out['relecture'][bras]], 'g', [x['g'] for x in out['relecture'][bras]], 'M-g', [x['non_genealogiques'] for x in out['relecture'][bras]])
    import c192uc
    from c187c import lj
    ident = []
    for s in range(192000, 192016):
        rng = np.random.default_rng(s); X = np.array([[-0.5, 0, 0], [0.5, 0, 0]])
        for N in range(3, 14):
            p = int(rng.integers(0, N - 1))
            for _ in range(128):
                u = rng.normal(size=3); c = X[p] + 1.04 * u / np.linalg.norm(u); dd = np.linalg.norm(X - c, axis=1); dd[p] = 9
                if dd.min() >= 0.78: break
            X = c192uc.relaxe(lj, np.vstack([X, c]))[0]
        E = graphe_de_contacts(X, 1.30 + 1e-12); T, F, _ = complexe(E, 13); b = bilan_boule(13, len(E), T, F); b['graine'] = s; ident.append(b)
    out['identite_sur_C192'] = ident; print('B7 identite de la boule sur mes 16 etats LJ13 : vraie pour', sum(b['identite'] for b in ident), '/ 16 ; (E, T, Fb, exces, T+Fb/2) :', [(b['E'], b['T'], b['Fb'], b['exces'], b['T_plus_demi_Fb']) for b in ident])
    json.dump(out, open('c193bc.json', 'w'), indent=1)
