#!/usr/bin/env python3
"""X-32, LE PARENT DEVIENT DEUX FILLES, AU RANG 3.
Prediction scellee : x32_deux_filles_prediction.txt (SHA-256 707c45ef...3535321), poussee avant ce calcul (commit 682fb1f).
 T27 n          : clauses C1 et C2. Regle a la lettre, constituants hors du germe jusqu'au palier n - 1, cotes au-dela pris dans le palier n (6).
 chaine a b g   : clauses C3 et C4. La regle de T28, graines a..b, g generations ; mesures sans prediction.
Outils du laboratoire : paliers et planchers (x29bis_plancher), descente vers la tuile-porte. Dans la partie 'chaine', la tuile-porte de chaque
nouvelle-nee est recalculee par descente, sans se servir de T27.     Claude, 27 novembre 2026."""
import itertools, json, random, sys, time
import numpy as np
import x29bis_plancher as Z
from x29_pliage import GERME, GERME_ENS, autre

def prod(a, b): return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)

def T_de(A, u): return GERME_ENS if u in GERME_ENS else frozenset(A.pl[u] | {u})

def partie_T27(n):
    t0 = time.time(); S, tui, A = Z.palier(n)
    c = dict(constituants=0, cellules=0, filles_propres=0, cousins=0, ni_l_un_ni_l_autre=0, desaccord_avec_le_mur=0, cote_hors_du_palier=0)
    par_palier = {}; murs = {}; ex = []
    for q in sorted(S):
        if q in GERME_ENS or S[q] > n - 1: continue
        c['constituants'] += 1; Tq = T_de(A, q); F = Tq - {q}; q2 = autre(Tq, q); T1 = F | {q2}; nf = 0
        nsep = sum(1 for f in F if sum(autre(T1, f)) < sum(f)); murs[nsep] = murs.get(nsep, 0) + 1
        assert not sum(autre(T1, q2)) < sum(q2), 'le mur du plancher separerait T\'(q) du germe'
        for f in F:
            c['cellules'] += 1; x = autre(Tq, f); Tx = (Tq - {f}) | {x}; separe = sum(autre(T1, f)) < sum(f)
            if x not in S: c['cote_hors_du_palier'] += 1; continue
            if T_de(A, x) == Tx: cas = 'fille'; c['filles_propres'] += 1; nf += 1
            elif T_de(A, x) == (Tx - {q}) | {autre(Tx, q)} and T_de(A, x) != Tx: cas = 'cousin'; c['cousins'] += 1
            else: cas = 'autre'; c['ni_l_un_ni_l_autre'] += 1
            if (cas == 'fille') != (not separe):
                c['desaccord_avec_le_mur'] += 1
                if len(ex) < 3: ex.append(dict(q=list(q), f=list(f), x=list(x), cas=cas, separe=separe))
        d = par_palier.setdefault(S[q], {}); d[nf] = d.get(nf, 0) + 1
    print(json.dumps(dict(partie='T27', palier=n, **c, murs_de_T_prime_qui_separent={str(k): murs[k] for k in sorted(murs)},
                          filles_propres_par_palier={str(p): {str(k): par_palier[p][k] for k in sorted(par_palier[p])} for p in sorted(par_palier)},
                          exemples_de_desaccord=ex, duree_s=round(time.time() - t0, 1))), flush=True)

def filles_propres(T, c):
    """Les filles propres de c, de tuile-porte T : (fille, plancher). Recalcule par descente, sans se servir de T27."""
    out = []
    for f in T:
        if f == c: continue
        x = autre(T, f); Tx = (T - {f}) | {x}
        if Z.porte(Tx, x) == Tx: out.append((x, Tx - {x}))
    return out

def partie_chaine(a, b, gmax):
    tot = dict(tirages=0, echecs_de_la_regle=0, doublons=0, non_clos_par_plancher=0, naissance_non_liee_a_la_mere=0, chevauchements=0,
               moins_de_deux_filles_possibles=0, filles_propres_de_la_derniere_fille={}, tailles=None)
    mes = dict(liens_de_meme_generation=[0] * (gmax + 1), plus_grand_palier=[0] * (gmax + 1))
    deg_age = {}; libres = {}
    for graine in range(a, b + 1):
        t0 = time.time(); rng = random.Random(graine)
        nes = {u: 0 for u in GERME}; T = {u: GERME_ENS for u in GERME}; pal = {u: 0 for u in GERME}; mere = {}; derniere = {}
        tailles = [5]
        # generation 1 : derangement du germe
        while True:
            perm = list(GERME); rng.shuffle(perm)
            if all(u != v for u, v in zip(GERME, perm)): break
        nouvelles = []
        for u, v in zip(GERME, perm):
            x = autre(GERME_ENS, v); Tx = (GERME_ENS - {v}) | {x}
            assert Z.porte(Tx, x) == Tx and prod(x, u) == -1
            nouvelles.append((u, x, Tx))
        for u, x, Tx in nouvelles:
            if x in nes: tot['doublons'] += 1
            nes[x] = 1; T[x] = Tx; pal[x] = 1; mere[x] = u; derniere[u] = x
        tailles.append(len(nes)); ok = True
        for g in range(2, gmax + 1):
            pris = set(); nouvelles = []; premieres = [c for c in nes if nes[c] == g - 1]; anciennes = [p for p in nes if nes[p] < g - 1]
            for p in anciennes:
                c = derniere[p]; fp = filles_propres(T[c], c); k = len(fp); tot['filles_propres_de_la_derniere_fille'][k] = tot['filles_propres_de_la_derniere_fille'].get(k, 0) + 1
                choix = [(x, pl) for x, pl in fp if p in pl and x not in nes and x not in pris]
                if len(choix) < 2: tot['moins_de_deux_filles_possibles'] += 1
                if not choix: tot['echecs_de_la_regle'] += 1; ok = False; break
                x, pl = rng.choice(choix); pris.add(x); nouvelles.append((p, x, pl))
            if not ok: break
            for c in premieres:
                choix = [(x, pl) for x, pl in filles_propres(T[c], c) if x not in nes and x not in pris]
                if len(choix) < 2: tot['moins_de_deux_filles_possibles'] += 1
                if not choix: tot['echecs_de_la_regle'] += 1; ok = False; break
                x, pl = rng.choice(choix); pris.add(x); nouvelles.append((c, x, pl))
            if not ok: break
            for p, x, pl in nouvelles:
                if not all(v in nes and nes[v] <= g - 1 for v in pl): tot['non_clos_par_plancher'] += 1
                if prod(x, p) != -1 or p not in pl: tot['naissance_non_liee_a_la_mere'] += 1
            for p, x, pl in nouvelles:
                if x in nes: tot['doublons'] += 1
                nes[x] = g; T[x] = pl | {x}; pal[x] = 1 + max(pal[v] for v in pl); mere[x] = p; derniere[p] = x
            tailles.append(len(nes))
        tot['tirages'] += 1
        if tot['tailles'] is None: tot['tailles'] = tailles
        elif tot['tailles'] != tailles: tot['tailles'] = 'differentes selon les tirages'
        if not ok: continue
        # controle a la derniere generation : aucun chevauchement ; mesures
        L = sorted(nes); gen = np.array([nes[u] for u in L]); M = np.array(L, dtype=np.int64); s = M.sum(1); deg = np.zeros(len(L), dtype=np.int64); meme = np.zeros(gmax + 1, dtype=np.int64)
        for d in range(0, len(L), 1000):
            G = 2 * M[d:d + 1000] @ M.T - np.outer(s[d:d + 1000], s); lig = np.arange(G.shape[0]); assert (G[lig, d + lig] == 1).all()
            G[lig, d + lig] = -1; tot['chevauchements'] += int((G > -1).sum()); lie = (G == -1); lie[lig, d + lig] = False
            deg[d:d + 1000] = lie.sum(1)
            for g in range(1, gmax + 1):
                sel = np.nonzero(gen[d:d + 1000] == g)[0]
                if len(sel): meme[g] += int(lie[sel][:, gen == g].sum())
        for g in range(gmax + 1): mes['liens_de_meme_generation'][g] += int(meme[g]) // 2; mes['plus_grand_palier'][g] = max(mes['plus_grand_palier'][g], max(pal[u] for u in L if nes[u] == g))
        for i, u in enumerate(L):
            age = gmax - nes[u]; d_ = deg_age.setdefault(age, [0, 0, 10 ** 9, 0]); d_[0] += 1; d_[1] += int(deg[i]); d_[2] = min(d_[2], int(deg[i])); d_[3] = max(d_[3], int(deg[i]))
        print(json.dumps(dict(graine=graine, generations=gmax, tailles=tailles, duree_s=round(time.time() - t0, 1))), flush=True)
    voisins = {str(age): dict(constituants=deg_age[age][0], voisins_en_moyenne=round(deg_age[age][1] / deg_age[age][0], 2), au_moins=deg_age[age][2], au_plus=deg_age[age][3]) for age in sorted(deg_age)}
    print(json.dumps(dict(bilan=True, partie='chaine', graines=[a, b], generations=gmax, **{k: (tot[k] if k != 'filles_propres_de_la_derniere_fille' else {str(i): tot[k][i] for i in sorted(tot[k])}) for k in tot},
                          mesures_sans_prediction=dict(liens_de_meme_generation_cumules_sur_les_tirages=mes['liens_de_meme_generation'], plus_grand_palier_par_generation=mes['plus_grand_palier'],
                                                       voisins_selon_l_age_a_la_derniere_generation=voisins))), flush=True)

def partie_libres(a, b, gmax):
    """Mesure sans prediction : a chaque generation, nombre de places admissibles (cotes non nes des cellules nees) et part laissee libre."""
    from x31_cellule import cellules
    for graine in range(a, b + 1):
        rng = random.Random(graine); nes = {u: 0 for u in GERME}; T = {u: GERME_ENS for u in GERME}; derniere = {}; lignes = []
        while True:
            perm = list(GERME); rng.shuffle(perm)
            if all(u != v for u, v in zip(GERME, perm)): break
        def compte(g):
            L = sorted(nes); ens = set(L); places = set(); plancher_ne = 0
            for (i, j, k, l), cotes in cellules(L):
                if len(cotes) == 1:
                    C = [L[i], L[j], L[k], L[l]]; u = L[cotes[0]]; places.add(tuple(sum(v[t] for v in C) - u[t] for t in range(5)))
            return dict(generation=g, constituants=len(L), places_admissibles=len(places))
        lignes.append(compte(0))
        for u, v in zip(GERME, perm):
            x = autre(GERME_ENS, v); nes[x] = 1; T[x] = (GERME_ENS - {v}) | {x}; derniere[u] = x
        lignes.append(compte(1))
        for g in range(2, gmax + 1):
            pris = set(); nouvelles = []
            for p in [p for p in nes if nes[p] < g - 1]:
                c = derniere[p]; x, pl = rng.choice([(x, pl) for x, pl in filles_propres(T[c], c) if p in pl and x not in nes and x not in pris]); pris.add(x); nouvelles.append((p, x, pl))
            for c in [c for c in nes if nes[c] == g - 1]:
                x, pl = rng.choice([(x, pl) for x, pl in filles_propres(T[c], c) if x not in nes and x not in pris]); pris.add(x); nouvelles.append((c, x, pl))
            for p, x, pl in nouvelles: nes[x] = g; T[x] = pl | {x}; derniere[p] = x
            lignes.append(compte(g))
        print(json.dumps(dict(partie='libres', graine=graine, par_generation=lignes)), flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'T27': partie_T27(int(sys.argv[2]))
    elif sys.argv[1] == 'chaine': partie_chaine(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif sys.argv[1] == 'libres': partie_libres(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
