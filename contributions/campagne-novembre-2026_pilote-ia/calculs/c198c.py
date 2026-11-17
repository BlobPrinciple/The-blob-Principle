#!/usr/bin/env python3
"""C-198c -- contre-calcul independant du C-198 de ChatGPT (Claude, 17 novembre 2026), d'apres son seul PROTOCOLE : mouvements de Pachner 1->4, 4->1, 2->3, 3->2 dans une boule de bord fige
(le tetraedre de depart). Modele d'AUDITEUR ; dimension 3 et premier tetraedre donnes. Ajout : bras CIBLE (1->4 et 2->3 dans le rapport 1 : 2,70). Predictions : c198c_prediction.txt.
Usage : python3 c198c.py -> c198c.json"""
import itertools, json, random
from collections import Counter, defaultdict

fs = frozenset
class Boule:
    def __init__(s):
        s.T = {fs((0, 1, 2, 3))}; s.suiv = 4; s.reserve = []; s.recycles = 0
    def faces(s): return Counter(fs(f) for t in s.T for f in itertools.combinations(sorted(t), 3))
    def aretes(s): return Counter(fs(e) for t in s.T for e in itertools.combinations(sorted(t), 2))
    def sommets(s): return set(v for t in s.T for v in t)
    def cand14(s): return sorted(tuple(sorted(t)) for t in s.T)
    def cand41(s):
        inc = defaultdict(list)
        for t in s.T:
            for v in t: inc[v].append(t)
        out = []
        for v, L in inc.items():
            if v > 3 and len(L) == 4:
                base = fs(set().union(*L) - {v})
                if len(base) == 4 and base not in s.T and all(fs(set(f) | {v}) in s.T for f in itertools.combinations(sorted(base), 3)): out.append(v)
        return sorted(out)
    def cand23(s):
        F = defaultdict(list); A = s.aretes()
        for t in s.T:
            for f in itertools.combinations(sorted(t), 3): F[fs(f)].append(t)
        out = []
        for f, L in F.items():
            if len(L) == 2:
                u, = L[0] - f; v, = L[1] - f
                if fs((u, v)) not in A: out.append((tuple(sorted(f)), min(u, v), max(u, v)))
        return sorted(out)
    def cand32(s):
        A = defaultdict(list); F = s.faces(); bord = set(fs(f) for f in itertools.combinations(range(4), 2))
        for t in s.T:
            for e in itertools.combinations(sorted(t), 2): A[fs(e)].append(t)
        out = []
        for e, L in A.items():
            if len(L) == 3:
                opp = set().union(*L) - e
                if len(opp) == 3 and fs(opp) not in F and all(sum(1 for t in L if set(p) <= t) == 1 for p in itertools.combinations(sorted(opp), 2)):
                    # arete interieure : chaque face (e + x) est dans 2 des 3 tetraedres
                    if all(F[fs(set(e) | {x})] == 2 for x in opp): out.append((tuple(sorted(e)), tuple(sorted(opp))))
        return sorted(out)
    def f14(s, t, rng):
        if s.reserve: v = s.reserve.pop(rng.randrange(len(s.reserve))); s.recycles += 1
        else: v = s.suiv; s.suiv += 1
        s.T.remove(fs(t))
        for f in itertools.combinations(t, 3): s.T.add(fs(f + (v,)))
    def f41(s, v):
        L = [t for t in s.T if v in t]; base = fs(set().union(*L) - {v})
        for t in L: s.T.remove(t)
        s.T.add(base); s.reserve.append(v)
    def f23(s, c):
        f, u, v = c; s.T.remove(fs(f + (u,))); s.T.remove(fs(f + (v,)))
        for p in itertools.combinations(f, 2): s.T.add(fs(p + (u, v)))
    def f32(s, c):
        e, opp = c
        for p in itertools.combinations(opp, 2): s.T.remove(fs(p + e))
        s.T.add(fs(opp + (e[0],))); s.T.add(fs(opp + (e[1],)))
    def controle(s, complet=False):
        F = s.faces(); A = s.aretes(); V = s.sommets(); T = len(s.T); r = dict(V=len(V), E=len(A), F=len(F), T=T)
        r['chi'] = len(V) - len(A) + len(F) - T; r['faces_ok'] = all(c in (1, 2) for c in F.values()); r['bord_ok'] = set(f for f, c in F.items() if c == 1) == set(fs(f) for f in itertools.combinations(range(4), 3))
        r['identite'] = len(A) - (len(V) - 1) == T + 2; ok = r['chi'] == 1 and r['faces_ok'] and r['bord_ok'] and r['identite']
        if complet:
            for v in V:
                L = [t - {v} for t in s.T if v in t]; ea = Counter(fs(p) for t in L for p in itertools.combinations(sorted(t), 2)); sv = set(x for t in L for x in t); chi = len(sv) - len(ea) + len(L)
                adj = defaultdict(set)
                for p in ea: a, b = p; adj[a].add(b); adj[b].add(a)
                vu = {next(iter(sv))}; pile = list(vu)
                while pile:
                    x = pile.pop()
                    for y in adj[x]:
                        if y not in vu: vu.add(y); pile.append(y)
                bordv = v < 4; ok &= (len(vu) == len(sv)) and (chi == (1 if bordv else 2)) and all(c == 2 for c in ea.values()) if not bordv else (len(vu) == len(sv)) and chi == 1 and all(c in (1, 2) for c in ea.values())
            r['liens_ok'] = bool(ok); r['betti'] = s.betti(); ok &= r['betti'] == [1, 0, 0, 0]
        r['ok'] = bool(ok); return r
    def betti(s):
        def rang(lignes):
            base = {}; r = 0
            for x in lignes:
                while x:
                    h = x.bit_length() - 1
                    if h in base: x ^= base[h]
                    else: base[h] = x; r += 1; break
            return r
        V = sorted(s.sommets()); E = sorted(tuple(sorted(e)) for e in s.aretes()); F = sorted(tuple(sorted(f)) for f in s.faces()); T = sorted(tuple(sorted(t)) for t in s.T)
        iv = {v: i for i, v in enumerate(V)}; ie = {e: i for i, e in enumerate(E)}; i_f = {f: i for i, f in enumerate(F)}
        r1 = rang([(1 << iv[a]) | (1 << iv[b]) for a, b in E]); r2 = rang([sum(1 << ie[p] for p in itertools.combinations(f, 2)) for f in F]); r3 = rang([sum(1 << i_f[f] for f in itertools.combinations(t, 3)) for t in T])
        return [len(V) - r1, len(E) - r1 - r2, len(F) - r2 - r3, len(T) - r3]
    def spectre(s):
        F = s.faces(); inc = Counter(); bord = Counter()
        for t in s.T:
            for e in itertools.combinations(sorted(t), 2): inc[fs(e)] += 1
        interieur = [n for e, n in inc.items() if not (set(e) <= {0, 1, 2, 3})]; return Counter(interieur)
    def k4(s):
        A = defaultdict(set)
        for e in s.aretes(): a, b = e; A[a].add(b); A[b].add(a)
        return sum(1 for i in A for j in A[i] if j > i for k in A[i] & A[j] if k > j for l in A[i] & A[j] & A[k] if l > k)

def trajet(seed, types, poids, n):
    rng = random.Random(seed); B = Boule(); tent = Counter(); acc = Counter(); ok = True
    for i in range(1, n + 1):
        ty = rng.choices(types, weights=poids)[0]; tent[ty] += 1; c = getattr(B, 'cand' + ty)()
        if c:
            x = c[rng.randrange(len(c))]; acc[ty] += 1
            if ty == '14': B.f14(x, rng)
            else: getattr(B, 'f' + ty)(x)
            ok &= B.controle()['ok']
        if i % 20 == 0: ok &= B.controle(True)['ok']
    r = B.controle(True); sp = B.spectre(); r.update(ok_partout=bool(ok and r['ok']), tentes=dict(tent), acceptes=dict(acc), recycles=B.recycles, spectre={int(k): v for k, v in sorted(sp.items())}, moyenne=6 * r['T'] / r['E'], T_sur_V=r['T'] / r['V'], K4=B.k4()); return r

if __name__ == '__main__':
    BRAS = dict(GROW=(['14', '23', '32', '41'], [45, 30, 15, 10], 240, 198000), BALANCED=(['14', '23', '32', '41'], [28, 27, 25, 20], 240, 198000), ONLY14=(['14'], [1], 120, 198000), CIBLE=(['14', '23'], [1, 2.70], 400, 198100)); out = {}
    for nom, (ty, po, n, g0) in BRAS.items():
        R = [trajet(g0 + i, ty, po, n) for i in range(8)]; out[nom] = R; tot = Counter()
        for r in R:
            for k, v in r['spectre'].items(): tot[k] += v
        N = sum(tot.values()); te = Counter(); ac = Counter()
        for r in R: te.update(r['tentes']); ac.update(r['acceptes'])
        print(nom, '| controles', sum(r['ok_partout'] for r in R), '/ 8 | betti', sorted(set(tuple(r['betti']) for r in R)), '| V', [r['V'] for r in R], '| E', [r['E'] for r in R], '| F', sorted(set(r['F'] for r in R))[:3], '| T', [r['T'] for r in R], '| K4', [r['K4'] for r in R],
              '| moyenne 6T/E', ['%.3f' % r['moyenne'] for r in R], '| T/V', ['%.2f' % r['T_sur_V'] for r in R], '| acceptation', {k: '%d/%d' % (ac[k], te[k]) for k in ty}, '| recycles', [r['recycles'] for r in R],
              '| spectre interieur (parts)', {k: round(v / N, 3) for k, v in sorted(tot.items())}, '| part 5+6 %.3f' % ((tot[5] + tot[6]) / N), '| part > 6 %.3f' % (sum(v for k, v in tot.items() if k > 6) / N), '| max', max(tot), flush=True)
    json.dump(out, open('c198c.json', 'w'), indent=1)
