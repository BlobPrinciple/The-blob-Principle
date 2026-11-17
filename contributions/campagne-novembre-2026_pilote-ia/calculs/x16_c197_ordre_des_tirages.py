#!/usr/bin/env python3
"""X-16 [APRES COUP, non aveugle] -- l'ecart C-197c / C-197 (bras C, rupture) vient-il de l'ordre des tirages ? ChatGPT a repondu (passation C-200) : (a) dans la fermeture, le troisieme sommet est tire
HORS sommet de depart ; (b) en rupture, un nombre est tire pour CHAQUE arete, meme d'age 0. On refait le bras C avec ces deux conventions et on compare a ses nombres d'aretes et de triangles au pas 28
(lus dans C197_ETATS_BRUTS.csv). (Claude, 17 novembre 2026.) Usage : python3 x16_c197_ordre_des_tirages.py"""
import json
import numpy as np
from c197c import composantes, poches

SIEN_E = [458, 66, 4833, 1406, 449, 3063, 3073, 1074, 2760, 120, 1075, 2898]; SIEN_T = [204, 23, 2235, 676, 205, 1448, 1465, 494, 1289, 59, 520, 1396]; SIEN_C = [15, 6, 138, 41, 19, 109, 103, 44, 72, 1, 31, 92]
def simule(seed, hors_depart, tirage_pour_tous):
    p, q, eta = 0.28, 0.28, 0.16; rn = np.random.default_rng(seed); rc = np.random.default_rng(seed + 2000000); rr = np.random.default_rng(seed + 3000000); A = {0: set()}; ne = {}; N = 1
    def ajoute(u, w, t): A[u].add(w); A[w].add(u); ne[(min(u, w), max(u, w))] = t
    for t in range(1, 29):
        L = sorted(ne); tir = rr.random(len(L)) if tirage_pour_tous else None
        for i, (u, w) in enumerate(L):
            a = t - ne[(u, w)]
            if tirage_pour_tous: x = tir[i]
            elif a >= 1: x = rr.random()
            else: continue
            if a >= 1 and x < (0.055 if a < 6 else 0.14): A[u].discard(w); A[w].discard(u); del ne[(u, w)]
        nes = []; tn = rn.random(N)
        for v in range(N):
            if tn[v] < p: nes.append((N, v)); N += 1
        for c, v in nes: A[c] = set()
        for c, v in nes: ajoute(c, v, t)
        for c, v in nes:
            vo = sorted(A[v] - {c})
            if vo:
                for i in rc.choice(len(vo), size=min(4, len(vo)), replace=False):
                    if rc.random() < q and vo[i] not in A[c]: ajoute(c, vo[i], t)
        for u in range(N):
            if rc.random() < eta and A[u]:
                vo = sorted(A[u]); v = vo[int(rc.integers(len(vo)))]; vw = sorted(A[v] - {u}) if hors_depart else sorted(A[v])
                if vw:
                    w = vw[int(rc.integers(len(vw)))]
                    if w != u and w not in A[u]: ajoute(u, w, t)
    return sum(len(a) for a in A.values()) // 2, sum(len(A[u] & A[w]) for u in A for w in A[u] if w > u) // 3, len(composantes(A))

out = {}
for nom, (h, tt) in dict(mien=(False, False), a_seul=(True, False), b_seul=(False, True), a_et_b=(True, True)).items():
    R = [simule(s, h, tt) for s in range(197000, 197012)]; out[nom] = R
    print(nom, '| aretes', [r[0] for r in R], '| triangles mediane', np.median([r[1] for r in R]), '| composantes mediane', np.median([r[2] for r in R]), '| aretes identiques aux siennes :', sum(r[0] == e for r, e in zip(R, SIEN_E)), '/12 ; triangles identiques :', sum(r[1] == e for r, e in zip(R, SIEN_T)), '/12')
print('siens  | aretes', SIEN_E, '| triangles mediane', np.median(SIEN_T), '| composantes mediane', np.median(SIEN_C))
json.dump(dict(resultats=out, siens=dict(E=SIEN_E, T=SIEN_T, C=SIEN_C)), open('x16_c197_ordre_des_tirages.json', 'w'))
