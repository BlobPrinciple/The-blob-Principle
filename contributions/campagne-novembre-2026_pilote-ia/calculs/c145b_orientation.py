# CONTRE-AUDIT d'un désaccord (ChatGPT, 13 nov., nouvelle conversation) : PR-2, liant nu, cœur dur 1/2, arrêt A1, source S, géométries perturbées :
# 0 séparation durable sur 96 chez moi, 14 sur 96 chez lui (non convergé). PR-2 ne fixe pas l'orientation du tétraèdre dans le repère des perturbations.
# Vérification avec mon code, sans rien y changer : mêmes 12 couples (P, c), mêmes 8 perturbations, tétraèdre tourné (3 rotations tirées une fois, graine 2026).
# Ce n'est pas un ajout à la grille de PR-2 : c'est le contrôle d'une explication possible du désaccord. DOP853 seul.
import numpy as np, sys, json
from multiprocessing import Pool
from c145b import *
rng = np.random.default_rng(2026)
def rot():
    q = rng.normal(size=4); q /= np.linalg.norm(q); a, b, c, d = q
    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)], [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)], [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]])
ROT = [np.eye(3)] + [rot() for _ in range(3)]
def job(a):
    k, src, P, c, g = a; R = ROT[k]; x = (P0 - P0.mean(0)) @ R.T
    if g: x = x + (1 if g % 2 == 1 else -1) * 1e-8 * delta((g + 1) // 2)
    d = run2('B0', src, P, c, stop='A1', x0=x); return (k, src, P, c, g, d['Pany'], d['t1'], len(d['groupe']), d['ambigu'])
if __name__ == '__main__':
    run2('B0', 'S', 0.3, '4/5', solver='rk', tend=2)
    J = [(k, src, P, c, g) for k in range(4) for src in 'SC' for P in (1/8, 1/4, 1/2) for c in ('1/2', '4/5', '1', '6/5') for g in range(9)]
    with Pool(2) as p: res = p.map(job, J, chunksize=8)
    json.dump(res, open('c145b_orientation.json', 'w'))
    for k in range(4):
        for src in 'SC':
            v = [r for r in res if r[0] == k and r[1] == src]; e = [r for r in v if r[4] == 0]; pp = [r for r in v if r[4] > 0]
            print(f"orientation {k} ({'protocole (la mienne)' if k == 0 else 'tournée'}) {src} : exacte P_any {sum(r[5] for r in e)}/12 ; perturbées {sum(r[5] for r in pp)}/96 ; groupes à 3 liens (perturbées) {sum(r[7] == 3 for r in pp)} ; ambigus {sum(r[8] is not None for r in v)}")
    print('TERMINE')
