#!/usr/bin/env python3
"""C-176c -- le terme b (n_e - d*)^2 de l'action du master et les ressorts de la regle U (Claude, 16 novembre 2026). Predictions : c176c_prediction.txt (ecrites avant)."""
import json, math
import mpmath as mp
mp.mp.dps = 40
TH = mp.acos(mp.mpf(1) / 3); DS = 2 * mp.pi / TH


def E(n, d=0):
    n = mp.mpf(n)
    f = lambda h, r: 0.5 * (h - 1) ** 2 + n * (mp.sqrt(r * r + h * h / 4) - 1) ** 2 + n / 2 * (2 * r * mp.sin(mp.pi / n) - 1 - d) ** 2
    g = lambda h, r: (mp.diff(f, (h, r), (1, 0)), mp.diff(f, (h, r), (0, 1)))
    h, r = mp.findroot(g, (mp.mpf(1), mp.sqrt(3) / 2), tol=1e-30, maxsteps=200)
    return f(h, r)


out = dict(d_etoile=str(DS), theta=str(TH))
# P1
out['P1'] = dict(E_en_d_etoile=str(E(DS)), ecart_des_deux_formes=str(abs(DS - mp.pi / mp.asin(1 / mp.sqrt(3)))), E_voisins=[[x, str(E(DS + x))] for x in (-0.5, -0.1, -0.01, 0.01, 0.1, 0.5)],
                 minimum_sur_grille=min((float(E(mp.mpf(k) / 100)), k / 100) for k in range(250, 1201)))
# P2
mprime = -mp.sqrt(3) * mp.cos(mp.pi / DS) * mp.pi / DS ** 2; A = DS / 2; g2 = mp.mpf(4) / 3; k = (3 * DS / 4) / (1 + DS / 8); c = mprime ** 2 * A * k / (k + A * g2)
df = {h: str((E(DS + mp.mpf(h)) + E(DS - mp.mpf(h)) - 2 * E(DS)) / (2 * mp.mpf(h) ** 2)) for h in ('1e-3', '1e-4')}
out['P2'] = dict(c_formule=str(c), c_differences_finies=df, ecart_relatif=str(abs(mp.mpf(df['1e-4']) - c) / c))
# P3 : troisieme derivee par differences centrees
h = mp.mpf('1e-2'); c3 = (E(DS + 2 * h) - 2 * E(DS + h) + 2 * E(DS - h) - E(DS - 2 * h)) / (2 * h ** 3) / 6; out['P3'] = dict(c3=str(c3))
# P4
out['P4'] = dict(c_sur_theta2=str(c / TH ** 2))
# P5
d5 = mp.sqrt(3) * mp.sin(mp.pi / 5) - 1; out['P5'] = dict(delta=str(d5), n0=str(mp.pi / mp.asin((1 + d5) / mp.sqrt(3))), E_a_5=str(E(5, d5)))
# comparaison aux couronnes entieres (connues)
ent = {3: 0.081681166378, 4: 0.030574477178, 5: 0.000324592453, 6: 0.026164940474, 7: 0.121380820374}
out['entiers'] = {n: dict(E=v, E_famille=float(E(n)), quadratique=float(c * (n - DS) ** 2), avec_cubique=float(c * (n - DS) ** 2 + c3 * (n - DS) ** 3), rapport_E_sur_x2=float(v / (n - DS) ** 2)) for n, v in ent.items()}
for k_, v in out.items(): print(k_, json.dumps(v) if isinstance(v, dict) else v)
json.dump(out, open('c176c.json', 'w'), indent=1)
