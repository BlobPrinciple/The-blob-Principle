#!/usr/bin/env python3
"""Contrôle d'arithmétique des pages 1900 (V344, « bande de construction maximale ») et 1911 (V345).

Sur une 3-variété fermée (caractéristique d'Euler nulle), N1 = N0 + N3 et la somme des degrés d'arêtes
vaut 6 N3 : la coordination moyenne est donc <n_e> = 6x/(1+x) avec x = N3/N0, fonction du seul volume.
On vérifie que la colonne <n_e> du tableau de la page 1900 est exactement cette fonction de la colonne <N3>/N0,
puis les constantes d*, x_plat, (6 - d*)^2 et d*^2 - 30 écrites pages 1887 et 1911.
"""
import math
table = [(0.0, 27.84, 5.792), (2.0, 12.09, 5.541), (2.3, 6.35, 5.182), (3.0, 4.20, 4.846)]
print("mu    <N3>/N0   <n_e> du master   6x/(1+x)   écart")
for mu, x, ne in table:
    print(f"{mu:3.1f}   {x:6.2f}    {ne:6.3f}            {6*x/(1+x):6.3f}    {6*x/(1+x)-ne:+.3f}")
ds = 2 * math.pi / math.acos(1 / 3)
print(f"d* = {ds:.6f} ; x_plat = d*/(6-d*) = {ds/(6-ds):.6f} (master : 5,698666)")
print(f"(6-d*)^2 = {(6-ds)**2:.15f} (master : 0,802279722269528) ; d*^2-30 = {ds*ds-30:.15f} (master : -3,946128532295987)")
print(f"densité du germe de Freudenthal : x = 6, coordination moyenne 6*6/7 = {36/7:.6f}")
