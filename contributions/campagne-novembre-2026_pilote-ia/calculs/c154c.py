#!/usr/bin/env python3
"""C-154c -- (A) minimum de l'energie U de l'eventail a six cellules sous l'interdit de recouvrement ; (B) courbure de Regge de la trame
equilatere par comptage (Claude, 14 novembre 2026). Predictions : c154c_prediction.txt."""
import itertools, json, math
import numpy as np, scipy.optimize as so
from c149c import classes_de_palier, KUHN
from c152c import axes_separateurs
TH = math.acos(1 / 3); out = {}

# ---------------- (A) eventail : arete a-b, lien c0..c6
V = 9; a, b = 0, 1; cs = list(range(2, 9))
fils = [(a, b)] + [(a, c) for c in cs] + [(b, c) for c in cs] + [(cs[i], cs[i + 1]) for i in range(6)]
tets = [(a, b, cs[i], cs[i + 1]) for i in range(6)]
I = np.array([f[0] for f in fils]); J = np.array([f[1] for f in fils])
def energie(z):
    X = z.reshape(-1, 3); D = X[I] - X[J]; L = np.linalg.norm(D, axis=1); G = np.zeros_like(X); w = ((L - 1) / L)[:, None] * D
    np.add.at(G, I, w); np.add.at(G, J, -w); return 0.5 * ((L - 1) ** 2).sum(), G.ravel()
def angles(z):
    X = z.reshape(-1, 3); u = X[b] - X[a]; u = u / np.linalg.norm(u); res = []
    for i in range(6):
        p = X[cs[i]] - X[a]; q = X[cs[i + 1]] - X[a]; p = p - p.dot(u) * u; q = q - q.dot(u) * u
        res.append(math.atan2(np.dot(np.cross(p, q), u), p.dot(q)))        # angle oriente
    return np.array(res)
def depart(ang):
    X = np.zeros((V, 3)); X[a] = [0, 0, -0.5]; X[b] = [0, 0, 0.5]
    for i, c in enumerate(cs): X[c] = [0.9 * math.cos(i * ang), 0.9 * math.sin(i * ang), 0]
    return X.ravel()
def controle(z):
    X = z.reshape(-1, 3); P = np.array([X[list(t)] for t in tets]); i, j = np.triu_indices(6, 1)
    vol = [float(np.dot(X[t[1]] - X[t[0]], np.cross(X[t[2]] - X[t[0]], X[t[3]] - X[t[0]])) / 6) for t in tets]
    return dict(profondeur_max=float(axes_separateurs(P[i], P[j]).max()), volume_min=min(vol), volume_max=max(vol))
libre = so.minimize(energie, depart(math.radians(70)), jac=True, method='BFGS', options=dict(gtol=1e-12))
out['A4_sans_contrainte'] = dict(E=float(libre.fun), somme_angles_deg=float(math.degrees(angles(libre.x).sum())), **controle(libre.x))
meilleurs = []
for k, ang in enumerate((60, 58, 55, 50)):
    for marge in (0.0,):
        r = so.minimize(lambda z: energie(z)[0], depart(math.radians(ang)), jac=lambda z: energie(z)[1], method='SLSQP',
                        constraints=[dict(type='ineq', fun=lambda z: 2 * math.pi - angles(z).sum())], options=dict(ftol=1e-15, maxiter=2000))
        meilleurs.append((float(r.fun), r.x, ang))
E, z, ang = min(meilleurs, key=lambda t: t[0])
X = z.reshape(-1, 3)
out['A'] = dict(energies_par_depart=[round(m[0], 9) for m in meilleurs], E_min=E, somme_angles_deg=float(math.degrees(angles(z).sum())),
                angles_deg=[round(math.degrees(x), 4) for x in angles(z)], longueur_arete_centrale=float(np.linalg.norm(X[a] - X[b])),
                longueurs_min_max=[float(np.linalg.norm(X[I] - X[J], axis=1).min()), float(np.linalg.norm(X[I] - X[J], axis=1).max())], **controle(z))
# eventail a 59 degres par cellule, relaxe a angles fixes : comparaison indicative avec le 0,03366 de ChatGPT
r59 = so.minimize(lambda z: energie(z)[0], depart(math.radians(59)), jac=lambda z: energie(z)[1], method='SLSQP',
                  constraints=[dict(type='eq', fun=lambda z: angles(z) - math.radians(59))], options=dict(ftol=1e-15, maxiter=2000))
out['A_59_degres'] = dict(E=float(r59.fun), **controle(r59.x))

# ---------------- (B) comptage de Regge
def complexe(n, classes=None, dirs=None):
    idx = lambda p: (p[0] % n) * n * n + (p[1] % n) * n + (p[2] % n)
    vois = (lambda p: classes[tuple(q % 2 for q in p)]) if classes else (lambda p: [d for d in dirs] + [tuple(-c for c in d) for d in dirs])
    lie = lambda u, v: tuple(v[i] - u[i] for i in range(3)) in set(vois(u))
    cells = set()
    for p in itertools.product(range(n), repeat=3):
        for d1, d2, d3 in itertools.combinations(sorted(vois(p)), 3):
            q = [tuple(p[i] + d[i] for i in range(3)) for d in (d1, d2, d3)]
            if lie(q[0], q[1]) and lie(q[0], q[2]) and lie(q[1], q[2]):
                S = sorted([p] + q); o = tuple((S[0][i] // n) * n for i in range(3)); cells.add(tuple(tuple(s[i] - o[i] for i in range(3)) for s in S))
    return cells, idx
def regge(cells, idx, n, vraies_longueurs):
    par_arete = {}
    for c in cells:
        for (u, v) in itertools.combinations(c, 2):
            w = [x for x in c if x not in (u, v)]
            o = tuple((u[i] // n) * n for i in range(3)); key = (tuple(u[i] - o[i] for i in range(3)), tuple(v[i] - u[i] for i in range(3)))
            if vraies_longueurs:
                U, Vv, A, B = (np.array(x, float) for x in (u, v, w[0], w[1])); e = (Vv - U) / np.linalg.norm(Vv - U)
                p = A - U; q = B - U; p = p - p.dot(e) * e; q = q - q.dot(e) * e
                ang = math.acos(max(-1, min(1, p.dot(q) / np.linalg.norm(p) / np.linalg.norm(q))))
            else:
                ang = TH
            par_arete.setdefault(key, []).append(ang)
    N0 = n ** 3; N1 = len(par_arete); N3 = len(cells)
    faces = set()
    for c in cells:
        for f in itertools.combinations(c, 3):
            o = tuple((f[0][i] // n) * n for i in range(3)); faces.add(tuple(tuple(s[i] - o[i] for i in range(3)) for s in f))
    deficits = np.array([2 * math.pi - sum(v) for v in par_arete.values()]); k = np.array([len(v) for v in par_arete.values()])
    lon = np.array([round(sum(x * x for x in key[1])) for key in par_arete])
    return dict(N0=N0, N1=N1, N2=len(faces), N3=N3, euler=N0 - N1 + len(faces) - N3, cellules_par_porteur=N3 / N0, cellules_par_fil=float(k.mean()),
                somme_k_par_porteur=float(k.sum() / N0), repartition={f'longueur2={l}, k={kk}': int(((lon == l) & (k == kk)).sum()) for l in sorted(set(lon)) for kk in sorted(set(k[lon == l]))},
                deficits_deg=sorted(set(round(math.degrees(d), 3) for d in deficits)), somme_deficits_par_porteur=float(deficits.sum() / N0),
                formule=float((2 * math.pi * N1 - 6 * N3 * TH) / N0) if not vraies_longueurs else None, deficit_max_abs=float(np.abs(deficits).max()))
n = 6
cl = classes_de_palier(); cells, idx = complexe(n, classes=cl)
out['B3_trame_de_palier_equilatere'] = regge(cells, idx, n, False)
s = out['B3_trame_de_palier_equilatere']['somme_deficits_par_porteur']
out['B3_courbure'] = dict(R=2 * s / (6 * math.sqrt(2) / 12), rayon_hyperbolique=math.sqrt(6 / abs(2 * s / (6 * math.sqrt(2) / 12))))
out['B4'] = dict(rapport_plat=2 * math.pi / (6 * TH - 2 * math.pi), sphere_600=dict(deficit_deg=math.degrees(2 * math.pi - 5 * TH), total=720 * (2 * math.pi - 5 * TH)))
out['B6_trame_de_palier_vraies_longueurs'] = regge(cells, idx, n, True)
ck, ik = complexe(n, dirs=KUHN)
out['B6_Kuhn_vraies_longueurs'] = regge(ck, ik, n, True)
out['B6_Kuhn_equilatere'] = regge(ck, ik, n, False)
out['B6_bord_du_4_simplexe'] = dict(deficit_deg=math.degrees(2 * math.pi - 3 * TH), total=10 * (2 * math.pi - 3 * TH), formule=2 * math.pi * 10 - 30 * TH)
json.dump(out, open('c154c.json', 'w'), indent=1); print(json.dumps(out, indent=1))
