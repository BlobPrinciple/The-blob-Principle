#!/usr/bin/env python3
"""Contrôle de la page 1582 de V346 (Tome V312, §FJ.3) : le témoin « réseau régulier (Freudenthal) ».

(1) Dual circumcentrique de la triangulation de Kuhn-Freudenthal : où sont les circumcentres ?
(2) Dimension spectrale exacte du laplacien scalaire du réseau cubique infini, pas a = 1 :
    P(t) = [exp(-2t) I_0(2t)]^3 par site, d_s(t) = -2 dlnP/dlnt = 12 t (1 - I_1(2t)/I_0(2t)),
    aux abscisses t/a^2 du tableau du master, puis son maximum.
Aucun moteur n'est requis : géométrie élémentaire et fonctions de Bessel."""
import itertools
import numpy as np
from scipy.special import ive


def circumcentre(p):
    a = 2.0 * (p[1:] - p[0])
    b = (p[1:] ** 2).sum(1) - (p[0] ** 2).sum()
    return np.linalg.solve(a, b)


print("(1) Les six tétraèdres de Kuhn du cube unité")
centres, aretes, faces = [], {}, {}
for perm in itertools.permutations(range(3)):
    v = [np.zeros(3)]
    for axe in perm:
        w = v[-1].copy()
        w[axe] = 1.0
        v.append(w)
    v = np.array(v)
    c = circumcentre(v)
    centres.append(c)
    print("    chemin", perm, "-> circumcentre", np.round(c, 12))
    for i, j in itertools.combinations(range(4), 2):
        cle = tuple(sorted((tuple(v[i]), tuple(v[j]))))
        aretes[cle] = int(np.count_nonzero(v[i] - v[j]))
    for tri in itertools.combinations(range(4), 3):
        cle = tuple(sorted(tuple(v[i]) for i in tri))
        faces[cle] = faces.get(cle, 0) + 1
centres = np.array(centres)
print("    écart maximal entre les six circumcentres :", float(np.abs(centres - centres[0]).max()))
n_axe = sum(1 for k in aretes.values() if k == 1)
n_face = sum(1 for k in aretes.values() if k == 2)
n_corps = sum(1 for k in aretes.values() if k == 3)
print(f"    arêtes du cube triangulé : {n_axe} d'axe, {n_face} diagonales de face, {n_corps} diagonale de corps")
internes = sum(1 for k in faces.values() if k == 2)
print(f"    triangles : {internes} internes (deux tétraèdres du même cube), {len(faces) - internes} sur les faces du cube")
print("    Conséquence : arête duale d'un triangle interne = distance entre deux circumcentres confondus = 0 ;")
print("    face duale d'une diagonale = polygone dont les sommets occupent au plus deux positions = aire 0 ;")
print("    seules les arêtes d'axe (carré dual d'aire a^2) et les triangles des faces (segment dual a) ont une étoile non nulle.")

print()
print("(2) Laplacien scalaire du réseau cubique infini : dimension spectrale exacte")
print("    t/a^2    d_s exact   « régulier » du master   « Blob » du master")
master_reg = {0.0063: 0.095, 0.0310: 0.428, 0.1021: 1.051, 0.3367: 1.127}
master_blob = {0.0063: 0.700, 0.0310: 1.400, 0.1021: 2.040, 0.3367: 2.848}


def ds(t):
    x = 2.0 * np.asarray(t, dtype=float)
    return 6.0 * x * (1.0 - ive(1, x) / ive(0, x))


for t in master_reg:
    print(f"    {t:6.4f}   {float(ds(t)):8.3f}   {master_reg[t]:12.3f}   {master_blob[t]:18.3f}")
grille = np.logspace(-3, 3, 600001)
val = ds(grille)
i = int(val.argmax())
print(f"    maximum : d_s = {val[i]:.3f} à t/a^2 = {grille[i]:.3f} ; d_s(10) = {float(ds(10.0)):.3f} ; d_s(100) = {float(ds(100.0)):.3f} ; limite 3")
