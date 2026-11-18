#!/usr/bin/env python3
"""C-211c -- contre-calcul du << C-211 >> de ChatGPT (viabilite intemporelle) : noyau de viabilite d'un graphe de transitions, par mon propre programme,
sur des exemples de mon choix. Prediction scellee avant lecture des notes : c211c_prediction.txt. Claude, 18 novembre 2026. Usage : python3 c211c.py"""
import itertools, json, random

def noyau(succ, ordre=None):
    K = set(succ); etapes = 0; change = True
    while change:
        change = False; L = list(K) if ordre is None else [s for s in ordre if s in K]
        morts = [s for s in L if not (set(succ[s]) & K)]
        if ordre is None:
            if morts: K -= set(morts); etapes += 1; change = True
        else:
            if morts: K.discard(morts[0]); etapes += 1; change = True
    return K, etapes

def suite_infinie(succ, s):
    # un etat fini admet une suite infinie ssi il atteint un cycle
    vus = set(); pile = [s]; acc = set()
    while pile:
        u = pile.pop()
        if u in acc: continue
        acc.add(u); pile.extend(succ[u])
    def sur_cycle(u):
        pile = list(succ[u]); vus = set()
        while pile:
            v = pile.pop()
            if v == u: return True
            if v in vus: continue
            vus.add(v); pile.extend(succ[v])
        return False
    return any(sur_cycle(u) for u in acc)

out = {}
# 1. graphes aleatoires : unicite, independance de l'ordre, equivalence avec l'existence d'une suite infinie
rng = random.Random(211); ok_ordre = ok_equiv = 0; n_g = 300
for g in range(n_g):
    n = rng.randint(4, 14); succ = {i: [j for j in range(n) if rng.random() < 0.12] for i in range(n)}
    K, _ = noyau(succ); memes = True
    for _ in range(5):
        o = list(range(n)); rng.shuffle(o); K2, _ = noyau(succ, o); memes &= (K2 == K)
    ok_ordre += memes; ok_equiv += all((s in K) == suite_infinie(succ, s) for s in succ)
out['aleatoires'] = dict(graphes=n_g, noyau_independant_de_l_ordre=ok_ordre, noyau_egal_etats_a_suite_infinie=ok_equiv)
# 2. contre-exemples
out['etat_fixe_sans_mitose'] = sorted(noyau({'point': ['point']})[0])
out['cycle_sans_volume'] = sorted(noyau({'a': ['b'], 'b': ['c'], 'c': ['a'], 'd': ['a'], 'e': []})[0])
# 3. memes etats, deux jeux de transitions
etats = ['point', 'arete', 'triangle', 'tetraedre']
T1 = {'point': ['arete'], 'arete': ['triangle'], 'triangle': ['tetraedre'], 'tetraedre': ['tetraedre']}
T2 = {'point': ['arete'], 'arete': ['triangle', 'arete'], 'triangle': ['tetraedre'], 'tetraedre': []}
T3 = {'point': ['arete'], 'arete': ['triangle'], 'triangle': ['tetraedre'], 'tetraedre': []}
out['memes_etats_transitions_differentes'] = {k: sorted(noyau(T)[0]) for k, T in (('T1_tetraedre_stable', T1), ('T2_arete_stable_tetraedre_sans_suite', T2), ('T3_rien_ne_dure', T3))}
# 4. nombre d'etapes : chaine descendante de longueur N (le noyau est vide, il faut N etapes)
out['chaine_descendante'] = [dict(N=N, taille_noyau=len(noyau({i: ([i - 1] if i > 0 else []) for i in range(N)})[0]), etapes=noyau({i: ([i - 1] if i > 0 else []) for i in range(N)})[1]) for N in (10, 100, 1000)]
json.dump(out, open('c211c.json', 'w'), indent=1); print(json.dumps(out, indent=1))
