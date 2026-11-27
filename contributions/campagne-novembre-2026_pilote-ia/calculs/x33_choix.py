#!/usr/bin/env python3
"""X-33, CE QUI FIXE LE CHOIX DE LA FILLE.
Prediction scellee : x33_ce_qui_fixe_le_choix_prediction.txt (SHA-256 b4b96d23...93bd548), poussee avant ce calcul (commit 1656860).
 D1 n         : clause D1 et T29 sur donnees. Regle a la lettre, palier n (5) : les paires de cousins, les murs de T'(x).
 D2           : clause D2. Generation 2 : les 6^5 tissus de la regle de T28, leurs liens de meme generation, les symetries du germe.
 D3 k         : clause D3. Generation 3 : les 3^10 tissus au-dessus du k-ieme des tissus sans lien de la generation 2 ('tous' : les 24).
 D4 g         : clause D4. La regle de T32 (chacune garde ses deux filles sans cousine possible), g generations, un tissu de chaque classe.
 D5 a b g     : clause D5. T30 et T31 sur les tirages de X-32 (graines a..b, g generations), rejoues a l'identique.
 D6           : clause D6. Variante plus libre, generation 2.
 hasard a b g : AJOUT NON SCELLE. Choix tires au hasard parmi ceux que la condition permet ; rien ne doit se bloquer.
 cellules g   : AJOUT NON SCELLE. Sous la regle de T32, les cellules du tissu a la generation g et leurs ages.
Outils du laboratoire : paliers et planchers (x29bis_plancher), descente vers la tuile-porte. Les filles propres sont recalculees par
descente, sans se servir de T27. Dans D4, << sans cousine possible >> est lu sur les donnees : aucune autre candidate de la generation
ne lui est liee ; la description annoncee (grand-mere, soeur non nee) est controlee a part.            Claude, 27 novembre 2026."""
import itertools, json, random, sys, time
import numpy as np
import x29bis_plancher as Z
from x29_pliage import GERME, GERME_ENS, autre

def prod(a, b): return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)
def T_de(A, u): return GERME_ENS if u in GERME_ENS else frozenset(A.pl[u] | {u})
def T_prime(T, x): return frozenset((T - {x}) | {autre(T, x)})
def separants(T, x):
    """Les parents f de x tels que le mur de T'(x) oppose a f separe T'(x) du germe."""
    T1 = T_prime(T, x); return [f for f in T if f != x and sum(autre(T1, f)) < sum(f)]

def filles_propres(T, c):
    """Les filles propres de c, de tuile-porte T : (fille, plancher, parent de c laisse de cote). Par descente, sans T27."""
    out = []
    for f in sorted(T):
        if f == c: continue
        x = autre(T, f); Tx = frozenset((T - {f}) | {x})
        if Z.porte(Tx, x) == Tx: out.append((x, Tx - {x}, f))
    return out

def gram(L1, L2):
    M1 = np.array(L1, dtype=np.int64); M2 = np.array(L2, dtype=np.int64)
    assert 12 * int(np.abs(M1).max()) * int(np.abs(M2).max()) < 2 ** 62, 'depassement possible en 64 bits'
    return 2 * M1 @ M2.T - np.outer(M1.sum(1), M2.sum(1))

PERMS = list(itertools.permutations(range(5)))
def signe(p): return (-1) ** sum(1 for i in range(5) for j in range(i) if p[j] > p[i])
def agit(p, u):
    """La symetrie du germe qui envoie le k-ieme constituant du germe sur le p[k]-ieme."""
    v = [0] * 5
    for k in range(5): v[p[k]] = u[k]
    return tuple(v)
def cycles(p):
    vu = set(); out = []
    for i in range(5):
        if i in vu: continue
        n = 0; j = i
        while j not in vu: vu.add(j); j = p[j]; n += 1
        out.append(n)
    return tuple(sorted(out))

# ---------------------------------------------------------------------------------------------------------------- D1
def partie_D1(n):
    t0 = time.time(); S, tui, A = Z.palier(n); L = sorted(S); N = len(L)
    c = dict(constituants=N, paires_liees=0, dans_le_germe=0, parent_et_enfant=0, cousins=0, cousins_hors_de_la_forme=0, cousins_mur_qui_ne_separe_pas=0,
             cousins_de_paliers_differents=0)
    voisins_cousins = {u: set() for u in L}
    for d in range(0, N, 600):
        G = gram(L[d:d + 600], L)
        for i, j in zip(*np.nonzero(G == -1)):
            i = int(i) + d; j = int(j)
            if j <= i: continue
            p, q = L[i], L[j]; c['paires_liees'] += 1
            if p in GERME_ENS and q in GERME_ENS: c['dans_le_germe'] += 1; continue
            if p in A.pl[q] or q in A.pl[p]: c['parent_et_enfant'] += 1; continue
            c['cousins'] += 1; voisins_cousins[p].add(q); voisins_cousins[q].add(p)
            if S[p] != S[q]: c['cousins_de_paliers_differents'] += 1
            for x, y in ((p, q), (q, p)):
                Tx = T_de(A, x); vs = [v for v in Tx if v != x and autre(Tx, v) == y]
                if len(vs) != 1: c['cousins_hors_de_la_forme'] += 1; continue
                if vs[0] not in separants(Tx, x): c['cousins_mur_qui_ne_separe_pas'] += 1
    # T29 sur donnees : pour chaque constituant hors du germe, les cousins annonces par les murs de T'(x)
    t = dict(constituants_hors_du_germe=0, par_nombre_de_murs_qui_separent={}, annonce_non_liee=0, annonce_parent_ou_enfant=0, cousin_des_donnees_non_annonce=0,
             annonces_hors_du_palier=0, zero_mur_mais_pas_du_palier_1=0, un_mur_mais_pas_de_mere_propre=0, deux_murs_mais_parents_non_cousins=0,
             deux_murs_et_une_mere_propre=0, plus_de_deux_murs=0)
    par_palier = {}
    for x in L:
        if x in GERME_ENS: continue
        t['constituants_hors_du_germe'] += 1; Tx = T_de(A, x); sep = separants(Tx, x); k = len(sep)
        t['par_nombre_de_murs_qui_separent'][k] = t['par_nombre_de_murs_qui_separent'].get(k, 0) + 1
        dd = par_palier.setdefault(S[x], {}); dd[k] = dd.get(k, 0) + 1
        annonces = set()
        for v in sep:
            y = autre(Tx, v); annonces.add(y)
            if prod(x, y) != -1: t['annonce_non_liee'] += 1
            Fy = A.pl[y] if y in S else Z.porte(frozenset((Tx - {v}) | {y}), y) - {y}
            if y not in S: t['annonces_hors_du_palier'] += 1
            if x in Fy or y in A.pl[x]: t['annonce_parent_ou_enfant'] += 1
        if not voisins_cousins[x] <= annonces: t['cousin_des_donnees_non_annonce'] += 1
        T1 = T_prime(Tx, x); meres = [f for f in Tx if f != x and f not in GERME_ENS and T_de(A, f) == T1]
        if k == 0 and T1 != GERME_ENS: t['zero_mur_mais_pas_du_palier_1'] += 1
        if k == 1 and meres != sep: t['un_mur_mais_pas_de_mere_propre'] += 1
        if k == 2:
            f1, f2 = sep
            if prod(f1, f2) != -1 or f1 in A.pl[f2] or f2 in A.pl[f1]: t['deux_murs_mais_parents_non_cousins'] += 1
            if meres: t['deux_murs_et_une_mere_propre'] += 1
        if k > 2: t['plus_de_deux_murs'] += 1
    t['par_nombre_de_murs_qui_separent'] = {str(k): v for k, v in sorted(t['par_nombre_de_murs_qui_separent'].items())}
    print(json.dumps(dict(partie='D1', palier=n, **c, T29_sur_donnees=t,
                          murs_qui_separent_par_palier={str(p): {str(k): v for k, v in sorted(par_palier[p].items())} for p in sorted(par_palier)},
                          duree_s=round(time.time() - t0, 1))), flush=True)

# ------------------------------------------------------------------------------------------------- generations 1 et 2
def depart():
    """Le palier 1 (M_v) et les vingt filles propres X(v, w), avec leurs tuiles-portes."""
    M = {}; T = {u: GERME_ENS for u in GERME}; X = {}
    for v in GERME:
        m = autre(GERME_ENS, v); Tm = frozenset((GERME_ENS - {v}) | {m}); assert Z.porte(Tm, m) == Tm; M[v] = m; T[m] = Tm
    for v in GERME:
        fp = filles_propres(T[M[v]], M[v]); assert len(fp) == 4 and all(f in GERME_ENS for _, _, f in fp)
        for x, pl, f in fp: X[(v, f)] = x; T[x] = frozenset(pl | {x})
    assert len(set(X.values())) == 20
    for p in PERMS:
        assert all(agit(p, M[v]) == M[agit(p, v)] for v in GERME) and all(agit(p, X[(v, w)]) == X[(agit(p, v), agit(p, w))] for v, w in X)
    return M, X, T

def tissus_generation_2():
    """Les 6^5 tissus de la regle a la generation 2 : pour chaque v, deux des quatre X(v, .). Rend aussi les paires liees parmi les vingt X."""
    M, X, T = depart(); cles = sorted(X); XL = [X[k] for k in cles]; G = gram(XL, XL)
    assert all(G[i, i] == 1 for i in range(20)); chev = int(((G > -1).sum() - 20) // 2)
    liees = [(cles[i], cles[j]) for i in range(20) for j in range(i + 1, 20) if G[i, j] == -1]
    tous = []
    for choix in itertools.product(*[list(itertools.combinations([w for w in GERME if w != v], 2)) for v in GERME]):
        tous.append(frozenset((v, w) for v, ws in zip(GERME, choix) for w in ws))
    return M, X, T, liees, chev, tous

def image_tournoi(p, t): return frozenset((agit(p, v), agit(p, w)) for v, w in t)

def partie_D2():
    t0 = time.time(); M, X, T, liees, chev, tous = tissus_generation_2()
    # les paires liees sont-elles les X(v, w), X(w, v) ?
    forme = sorted(liees) == sorted(((v, w), (w, v)) for v in GERME for w in GERME if v < w)
    # controle : aucun chevauchement parmi les trente constituants, les M_v ne sont pas lies entre eux
    tout = list(GERME) + [M[v] for v in GERME] + [X[k] for k in sorted(X)]; G = gram(tout, tout)
    chevauchements = int(((G > -1).sum() - 30) // 2); liens_M = int((G[5:10, 5:10] == -1).sum() // 2)
    distribution = {}; sans = []
    for t in tous:
        k = sum(1 for a, b in liees if a in t and b in t); distribution[k] = distribution.get(k, 0) + 1
        if k == 0: sans.append(t)
    ens = set(sans)
    def orbites(groupe):
        reste = set(sans); out = []
        while reste:
            t = min(reste, key=sorted); o = {image_tournoi(p, t) for p in groupe}; assert o <= ens; out.append(len(o)); reste -= o
        return sorted(out)
    pairs = [p for p in PERMS if signe(p) == 1]
    stab = []; types = set(); tous_pairs = True
    for t in sans:
        s = [p for p in PERMS if image_tournoi(p, t) == t]; stab.append(len(s))
        for p in s:
            types.add(cycles(p))
            if signe(p) != 1: tous_pairs = False
    reguliers = all(all(sum(1 for a, b in t if a == v) == 2 and sum(1 for a, b in t if b == v) == 2 for v in GERME) for t in sans)
    print(json.dumps(dict(partie='D2', tissus=len(tous), paires_liees_parmi_les_vingt=len(liees), paires_liees_de_la_forme_X_vw_X_wv=forme,
                          chevauchements_parmi_les_trente=chevauchements, liens_entre_constituants_du_palier_1=liens_M,
                          tissus_par_nombre_de_liens_de_meme_generation={str(k): distribution[k] for k in sorted(distribution)},
                          sans_lien=len(sans), sans_lien_tous_tournois_reguliers=reguliers,
                          classes_sous_les_120_symetries=orbites(PERMS), classes_sous_les_60_paires=orbites(pairs),
                          ordres_des_stabilisateurs=sorted(set(stab)), stabilisateurs_tous_pairs=tous_pairs,
                          types_de_cycles_dans_les_stabilisateurs=sorted(types), duree_s=round(time.time() - t0, 1))), flush=True)

def les_24():
    M, X, T, liees, chev, tous = tissus_generation_2()
    sans = sorted((t for t in tous if not any(a in t and b in t for a, b in liees)), key=sorted)
    return M, X, T, sans

def tissu_initial(M, X, T, t):
    """Germe, palier 1 et les dix X(v, w) du tournoi t. Rend nes (generation), tuiles-portes, meres propres."""
    nes = {u: 0 for u in GERME}; tu = {u: GERME_ENS for u in GERME}; mere = {}
    for v in GERME: nes[M[v]] = 1; tu[M[v]] = T[M[v]]
    for v, w in sorted(t): x = X[(v, w)]; nes[x] = 2; tu[x] = T[x]; mere[x] = M[v]
    return nes, tu, mere

# ---------------------------------------------------------------------------------------------------------------- D3
def partie_D3(arg):
    t0 = time.time(); M, X, T, sans = les_24(); indices = range(len(sans)) if arg == 'tous' else [int(arg)]
    for k in indices:
        nes, tu, mere = tissu_initial(M, X, T, sans[k]); meres = sorted(c for c in nes if nes[c] == 2)
        cand = []; trois = True
        for c in meres:
            fp = filles_propres(tu[c], c); trois = trois and len(fp) == 3
            for x, pl, f in fp: cand.append((c, x, pl, f))
        XL = [x for _, x, _, _ in cand]; assert len(set(XL)) == len(XL) and not set(XL) & set(nes)
        G = gram(XL, XL); n = len(XL); chev = int(((G > -1).sum() - n) // 2)
        liees = [(i, j) for i in range(n) for j in range(i + 1, n) if G[i, j] == -1]
        vieux = sorted(nes); Gv = gram(XL, vieux); chev += int((Gv > -1).sum())
        plancher_seul = all({vieux[j] for j in np.nonzero(Gv[i] == -1)[0]} == set(cand[i][2]) for i in range(n))
        # la description annoncee : la fille << a risque >> de c laisse de cote le parent que sa soeur nee a laisse de cote
        cote = {c: autre(tu[c], c) for c in meres}; soeur = {}
        for c in meres:
            s = [d for d in meres if d != c and mere[d] == mere[c]]; assert len(s) == 1; soeur[c] = s[0]
        risque = {i for i, (c, x, pl, f) in enumerate(cand) if f == cote[soeur[c]]}
        forme = sorted(liees) == sorted((i, j) for i in risque for j in risque if i < j and cand[j][0] == soeur[cand[i][0]]) and len(risque) == len(meres)
        par_mere = {c: [i for i in range(n) if cand[i][0] == c] for c in meres}
        distribution = {}; sans_lien_et_sans_risque = 0
        for lache in itertools.product(*[par_mere[c] for c in meres]):
            L = set(lache); k_liens = sum(1 for i, j in liees if i not in L and j not in L); distribution[k_liens] = distribution.get(k_liens, 0) + 1
            if k_liens == 0 and L == risque: sans_lien_et_sans_risque += 1
        print(json.dumps(dict(partie='D3', tissu_de_depart=k, meres=len(meres), chacune_trois_filles_propres=trois, candidates=n,
                              paires_liees_parmi_les_candidates=len(liees), paires_liees_de_la_forme_annoncee=forme, chevauchements=chev,
                              candidates_liees_aux_nes_par_leur_seul_plancher=plancher_seul, tissus=sum(distribution.values()),
                              tissus_par_nombre_de_liens_de_meme_generation={str(i): distribution[i] for i in sorted(distribution)},
                              sans_lien_ou_chaque_soeur_garde_ses_deux_filles_sans_cousine=sans_lien_et_sans_risque,
                              duree_s=round(time.time() - t0, 1))), flush=True)

# ---------------------------------------------------------------------------------------------------------------- D4
def soeurs_de(meres, mere):
    """Les meres vont par deux : deux filles propres nees de la meme mere propre."""
    groupe = {}; soeur = {}
    for m in meres: groupe.setdefault(mere[m], []).append(m)
    for q, ms in groupe.items():
        assert len(ms) == 2, 'un constituant n\'a pas exactement deux filles propres nees'
        soeur[ms[0]] = ms[1]; soeur[ms[1]] = ms[0]
    return soeur

def candidates_de(nes, tu, g):
    """Les filles propres des constituants nes a la generation g - 1 : (mere, fille, plancher, parent laisse de cote)."""
    cand = []; compte = {}
    for c in sorted(u for u in nes if nes[u] == g - 1):
        fp = filles_propres(tu[c], c); compte[len(fp)] = compte.get(len(fp), 0) + 1
        for x, pl, f in fp: cand.append((c, x, pl, f))
    return cand, compte

def liens_entre(XL):
    """Pour chaque candidate, les indices des autres candidates qui lui sont liees ; et le nombre de chevauchements."""
    n = len(XL); lie = [[] for _ in range(n)]; chev = 0
    for d in range(0, n, 800):
        G = gram(XL[d:d + 800], XL); lig = np.arange(G.shape[0]); assert (G[lig, d + lig] == 1).all(); G[lig, d + lig] = -2
        chev += int((G > -1).sum())
        for i, j in zip(*np.nonzero(G == -1)): lie[int(i) + d].append(int(j))
    return lie, chev // 2

def bilan_final(nes, tu, gmax):
    """A la derniere generation : liens, par sorte ; chevauchements ; voisins selon l'age."""
    L = sorted(nes); gen = np.array([nes[u] for u in L]); idx = {u: i for i, u in enumerate(L)}; N = len(L)
    b = dict(constituants=N, liens=0, liens_dans_le_germe=0, liens_de_parent_a_enfant=0, liens_de_meme_generation_hors_du_germe=0,
             liens_entre_generations_differentes_hors_parente=0, chevauchements=0, constituants_non_lies_a_tout_leur_plancher=0)
    deg = np.zeros(N, dtype=np.int64); meme = [0] * (gmax + 1)
    for d in range(0, N, 800):
        G = gram(L[d:d + 800], L); lig = np.arange(G.shape[0]); assert (G[lig, d + lig] == 1).all(); G[lig, d + lig] = -2
        b['chevauchements'] += int((G > -1).sum()); lie = (G == -1); deg[d:d + 800] = lie.sum(1)
        for i, j in zip(*np.nonzero(lie)):
            i = int(i) + d; j = int(j)
            if j <= i: continue
            b['liens'] += 1; p, q = L[i], L[j]
            if nes[p] == 0 and nes[q] == 0: b['liens_dans_le_germe'] += 1
            elif nes[p] == nes[q]: b['liens_de_meme_generation_hors_du_germe'] += 1; meme[nes[p]] += 1
            elif (p in tu[q] and nes[p] < nes[q]) or (q in tu[p] and nes[q] < nes[p]): b['liens_de_parent_a_enfant'] += 1
            else: b['liens_entre_generations_differentes_hors_parente'] += 1
    b['chevauchements'] //= 2
    for u in L:
        if nes[u] > 0 and not all(prod(u, f) == -1 for f in tu[u] if f != u): b['constituants_non_lies_a_tout_leur_plancher'] += 1
    par_age = {}
    for i, u in enumerate(L):
        a = gmax - nes[u]; e = par_age.setdefault(a, [0, 10 ** 9, 0, 0]); e[0] += 1; e[1] = min(e[1], int(deg[i])); e[2] = max(e[2], int(deg[i])); e[3] += int(deg[i])
    b['liens_de_meme_generation_par_generation'] = meme[1:]
    b['voisins_selon_l_age'] = {str(a): dict(constituants=par_age[a][0], au_moins=par_age[a][1], au_plus=par_age[a][2], en_moyenne=round(par_age[a][3] / par_age[a][0], 2)) for a in sorted(par_age)}
    return b

def regle_T32(M, X, T, t, gmax):
    """Chaque constituant ne a la generation g - 1 garde ses filles propres auxquelles aucune autre candidate n'est liee."""
    nes, tu, mere = tissu_initial(M, X, T, t); tailles = [5, 10, 20]
    c = dict(meres_sans_trois_filles_propres=0, meres_sans_deux_filles_sures_exactement=0, description_annoncee_en_defaut=0, chevauchements_entre_candidates=0)
    for g in range(3, gmax + 1):
        cand, compte = candidates_de(nes, tu, g); c['meres_sans_trois_filles_propres'] += sum(v for k, v in compte.items() if k != 3)
        XL = [x for _, x, _, _ in cand]; assert len(set(XL)) == len(XL) and not set(XL) & set(nes)
        lie, chev = liens_entre(XL); c['chevauchements_entre_candidates'] += chev
        par_mere = {}
        for i, (m, x, pl, f) in enumerate(cand): par_mere.setdefault(m, []).append(i)
        soeur = soeurs_de(par_mere, mere); nouvelles = []
        for m, ind in par_mere.items():
            sures = [i for i in ind if not lie[i]]
            if len(sures) != 2: c['meres_sans_deux_filles_sures_exactement'] += 1
            # description annoncee : la fille a risque laisse de cote le parent que la soeur nee de m a laisse de cote ;
            # les deux sures laissent de cote la grand-mere (a partir de la generation 3 de m) et le parent laisse par la soeur non nee
            q = mere[m]; cote_soeur = autre(tu[soeur[m]], soeur[m]); risque = [i for i in ind if cand[i][3] == cote_soeur]
            attendu = sorted(i for i in ind if i not in risque)
            if len(risque) != 1 or attendu != sorted(sures): c['description_annoncee_en_defaut'] += 1
            if len(risque) == 1 and len(lie[risque[0]]) == 1:
                j = lie[risque[0]][0]
                if not (cand[j][0] == soeur[m] and cand[j][3] == autre(tu[m], m)): c['description_annoncee_en_defaut'] += 1
            elif len(risque) == 1: c['description_annoncee_en_defaut'] += 1
            if nes[m] >= 3 and not any(cand[i][3] == mere[q] for i in sures): c['description_annoncee_en_defaut'] += 1
            for i in sures: nouvelles.append(cand[i])
        for m, x, pl, f in nouvelles: nes[x] = g; tu[x] = frozenset(pl | {x}); mere[x] = m
        tailles.append(len(nes))
    return nes, tu, mere, tailles, c

def partie_D4(gmax):
    t0 = time.time(); M, X, T, sans = les_24()
    # un tournoi circulant : v bat v + 1 et v + 2 ; son image par la transposition des deux premiers constituants du germe
    circ = frozenset((GERME[i], GERME[(i + d) % 5]) for i in range(5) for d in (1, 2)); assert circ in sans
    tau = (1, 0, 2, 3, 4); autre_classe = image_tournoi(tau, circ); assert autre_classe in sans
    pairs = [p for p in PERMS if signe(p) == 1]; meme_classe = any(image_tournoi(p, circ) == autre_classe for p in pairs)
    tissus = []
    for nom, t in (('A', circ), ('B', autre_classe)):
        t1 = time.time(); nes, tu, mere, tailles, c = regle_T32(M, X, T, t, gmax); b = bilan_final(nes, tu, gmax); E = frozenset(nes)
        stab = [p for p in PERMS if frozenset(agit(p, u) for u in E) == E]
        print(json.dumps(dict(partie='D4', tissu=nom, generations=gmax, tailles=tailles, tailles_attendues=[5 * 2 ** g for g in range(gmax + 1)], **c, **b,
                              liens_attendus=4 * len(nes) - 10, symetries_du_germe_qui_conservent_le_tissu=len(stab),
                              dont_impaires=sum(1 for p in stab if signe(p) == -1), types_de_cycles=sorted({cycles(p) for p in stab}),
                              plus_grande_coordonnee=max(max(abs(a) for a in u) for u in E), duree_s=round(time.time() - t1, 1))), flush=True)
        tissus.append(E)
    A_, B_ = tissus; vers = [p for p in PERMS if frozenset(agit(p, u) for u in A_) == B_]
    print(json.dumps(dict(partie='D4', bilan=True, depart_B_dans_la_meme_classe_paire_que_A=meme_classe, constituants_communs_a_A_et_B=len(A_ & B_),
                          symetries_qui_envoient_A_sur_B=len(vers), dont_paires=sum(1 for p in vers if signe(p) == 1),
                          dont_impaires=sum(1 for p in vers if signe(p) == -1), duree_s=round(time.time() - t0, 1))), flush=True)

# ---------------------------------------------------------------------------------------------------------------- D5
def tirage_X32(graine, gmax):
    """Le tirage de X-32 (x32_deux_filles.py, partie 'chaine'), rejoue a l'identique : memes appels au generateur, dans le meme ordre."""
    import x32_deux_filles as W
    rng = random.Random(graine); nes = {u: 0 for u in GERME}; T = {u: GERME_ENS for u in GERME}; mere = {}; derniere = {}
    while True:
        perm = list(GERME); rng.shuffle(perm)
        if all(u != v for u, v in zip(GERME, perm)): break
    for u, v in zip(GERME, perm):
        x = autre(GERME_ENS, v); nes[x] = 1; T[x] = (GERME_ENS - {v}) | {x}; mere[x] = u; derniere[u] = x
    for g in range(2, gmax + 1):
        pris = set(); nouvelles = []; premieres = [c for c in nes if nes[c] == g - 1]; anciennes = [p for p in nes if nes[p] < g - 1]
        for p in anciennes:
            c = derniere[p]; fp = W.filles_propres(T[c], c)
            choix = [(x, pl) for x, pl in fp if p in pl and x not in nes and x not in pris]
            x, pl = rng.choice(choix); pris.add(x); nouvelles.append((p, x, pl))
        for c in premieres:
            choix = [(x, pl) for x, pl in W.filles_propres(T[c], c) if x not in nes and x not in pris]
            x, pl = rng.choice(choix); pris.add(x); nouvelles.append((c, x, pl))
        for p, x, pl in nouvelles: nes[x] = g; T[x] = pl | {x}; mere[x] = p; derniere[p] = x
    return nes, {u: frozenset(T[u]) for u in T}, mere

def partie_D5(a, b, gmax):
    tot = dict(tirages=0, constituants_des_generations_1_a_avant_derniere=0, sans_deux_filles_propres_nees_exactement=0, fille_propre_nee_a_une_autre_generation=0,
               constituants_du_germe=0, filles_propres_nees_d_un_constituant_du_germe={}, nes_sans_mere_propre_nee_a_la_generation_precedente=0,
               mere_de_regle_differente_de_la_mere_propre=0, nees_depuis_la_generation_2=0, liens=0, liens_dans_le_germe=0, liens_de_parent_a_enfant=0,
               liens_de_meme_generation_hors_du_germe=0, liens_entre_generations_differentes_hors_parente=0, chevauchements=0)
    meme = [0] * (gmax + 1)
    for graine in range(a, b + 1):
        t0 = time.time(); nes, T, mere = tirage_X32(graine, gmax); tot['tirages'] += 1; propre = {}
        for c in nes:
            if nes[c] == gmax: continue
            fp = filles_propres(T[c], c); nees = [x for x, pl, f in fp if x in nes]
            if nes[c] == 0:
                tot['constituants_du_germe'] += 1; k = len(nees); d = tot['filles_propres_nees_d_un_constituant_du_germe']; d[k] = d.get(k, 0) + 1; continue
            tot['constituants_des_generations_1_a_avant_derniere'] += 1
            if len(nees) != 2: tot['sans_deux_filles_propres_nees_exactement'] += 1
            for x in nees:
                propre.setdefault(x, []).append(c)
                if nes[x] != nes[c] + 1: tot['fille_propre_nee_a_une_autre_generation'] += 1
        for x in nes:
            if nes[x] < 2: continue
            tot['nees_depuis_la_generation_2'] += 1; m = propre.get(x, [])
            if len(m) != 1 or nes[m[0]] != nes[x] - 1: tot['nes_sans_mere_propre_nee_a_la_generation_precedente'] += 1
            elif m[0] != mere[x]: tot['mere_de_regle_differente_de_la_mere_propre'] += 1
        bb = bilan_final(nes, T, gmax)
        for k in ('liens', 'liens_dans_le_germe', 'liens_de_parent_a_enfant', 'liens_de_meme_generation_hors_du_germe', 'liens_entre_generations_differentes_hors_parente', 'chevauchements'): tot[k] += bb[k]
        for g in range(1, gmax + 1): meme[g] += bb['liens_de_meme_generation_par_generation'][g - 1]
        print(json.dumps(dict(graine=graine, constituants=len(nes), liens_de_meme_generation=bb['liens_de_meme_generation_hors_du_germe'], duree_s=round(time.time() - t0, 1))), flush=True)
    tot['filles_propres_nees_d_un_constituant_du_germe'] = {str(k): v for k, v in sorted(tot['filles_propres_nees_d_un_constituant_du_germe'].items())}
    print(json.dumps(dict(bilan=True, partie='D5', graines=[a, b], generations=gmax, **tot, liens_de_meme_generation_cumules_sur_les_tirages=meme,
                          rappel_X32_meme_mesure=[0, 0, 55, 48, 89, 189, 403, 712, 1456, 2923, 5898])), flush=True)

# ---------------------------------------------------------------------------------------------------------------- D6
def couplage_parfait(adj, n):
    """Couplage biparti par chemins augmentants : adj[i] = indices de droite permis au i-ieme de gauche."""
    droite = {}
    def essaie(i, vu):
        for j in adj[i]:
            if j in vu: continue
            vu.add(j)
            if j not in droite or essaie(droite[j], vu): droite[j] = i; return True
        return False
    return all(essaie(i, set()) for i in range(n))

def partie_D6():
    t0 = time.time(); M, X, T = depart(); nes = list(GERME) + [M[v] for v in GERME]; ens = set(nes)
    # les candidates : constituants non nes dont le plancher est ne (cotes non nes des cellules nees, de tuile-porte voulue)
    cand = {}
    for quad in itertools.combinations(nes, 4):
        if any(prod(a, b) != -1 for a, b in itertools.combinations(quad, 2)): continue
        for u in nes:
            if u in quad or any(prod(u, a) != -1 for a in quad): continue
            x = tuple(sum(a[k] for a in quad) - u[k] for k in range(5))
            if x in ens: continue
            Tx = Z.porte(frozenset(quad) | {x}, x)
            if Tx - {x} <= ens: cand[x] = Tx - {x}
    CL = sorted(cand); n = len(CL); sont_les_X = set(CL) == set(X.values())
    G = gram(CL, CL); liees = [(i, j) for i in range(n) for j in range(i + 1, n) if G[i, j] == -1]
    inv = {X[k]: k for k in X}
    total = 0; avec_couplage = 0; sans_lien = 0; retenus = []
    for sous in itertools.combinations(range(n), 10):
        total += 1; s = set(sous)
        if any(i in s and j in s for i, j in liees): continue
        sans_lien += 1
        adj = [[k for k, i in enumerate(sous) if p in cand[CL[i]]] for p in nes]
        if couplage_parfait(adj, 10): avec_couplage += 1; retenus.append(frozenset(inv[CL[i]] for i in sous))
    ens_r = set(retenus); reste = set(retenus); classes = []
    while reste:
        t = min(reste, key=sorted); o = {image_tournoi(p, t) for p in PERMS}; assert o <= ens_r; classes.append(len(o)); reste -= o
    degres = {}
    for t in retenus:
        d = tuple(sorted(sum(1 for a, b in t if a == v) for v in GERME)); degres[d] = degres.get(d, 0) + 1
    # sans la condition : combien d'ensembles de dix candidates admettent un couplage
    libres = 0
    for sous in itertools.combinations(range(n), 10):
        adj = [[k for k, i in enumerate(sous) if p in cand[CL[i]]] for p in nes]
        if couplage_parfait(adj, 10): libres += 1
    print(json.dumps(dict(partie='D6', nes=len(nes), candidates=n, candidates_sont_les_vingt_X=sont_les_X, paires_liees_parmi_les_candidates=len(liees),
                          ensembles_de_dix=total, sans_lien_entre_elles=sans_lien, sans_lien_et_chacun_prend_une_fille=avec_couplage,
                          classes_sous_les_120_symetries=sorted(classes), nombre_de_classes=len(classes),
                          par_nombres_de_filles_des_cinq_du_palier_1={str(list(d)): v for d, v in sorted(degres.items())},
                          ensembles_de_dix_ou_chacun_prend_une_fille_sans_la_condition=libres, duree_s=round(time.time() - t0, 1))), flush=True)

# ------------------------------------------------------------------------------------------------------------ hasard
def partie_hasard(a, b, gmax):
    """AJOUT NON SCELLE. Generation 2 : un des 24 au hasard. Ensuite, par paire de soeurs, un des choix sans lien, au hasard."""
    M, X, T, sans = les_24(); tot = dict(tirages=0, paires_de_soeurs=0, choix_permis_par_paire={}, blocages=0)
    for graine in range(a, b + 1):
        t0 = time.time(); rng = random.Random(graine); nes, tu, mere = tissu_initial(M, X, T, rng.choice(sans)); tailles = [5, 10, 20]
        for g in range(3, gmax + 1):
            cand, compte = candidates_de(nes, tu, g); XL = [x for _, x, _, _ in cand]; lie, chev = liens_entre(XL); assert chev == 0
            par_mere = {}
            for i, (m, x, pl, f) in enumerate(cand): par_mere.setdefault(m, []).append(i)
            vues = set(); nouvelles = []; soeur = soeurs_de(par_mere, mere)
            for m in sorted(par_mere):
                if m in vues: continue
                s = soeur[m]; vues |= {m, s}; tot['paires_de_soeurs'] += 1
                permis = []
                for la in itertools.combinations(par_mere[m], 2):
                    for lb in itertools.combinations(par_mere[s], 2):
                        ch = set(la) | set(lb)
                        if not any(j in ch for i in ch for j in lie[i]): permis.append(ch)
                k = len(permis); tot['choix_permis_par_paire'][k] = tot['choix_permis_par_paire'].get(k, 0) + 1
                if not permis: tot['blocages'] += 1; continue
                for i in sorted(rng.choice(permis)): nouvelles.append(cand[i])
            for m, x, pl, f in nouvelles: nes[x] = g; tu[x] = frozenset(pl | {x}); mere[x] = m
            tailles.append(len(nes))
        bb = bilan_final(nes, tu, gmax); tot['tirages'] += 1
        print(json.dumps(dict(partie='hasard', graine=graine, tailles=tailles, liens=bb['liens'], liens_attendus=4 * len(nes) - 10,
                              liens_de_meme_generation_hors_du_germe=bb['liens_de_meme_generation_hors_du_germe'],
                              liens_entre_generations_differentes_hors_parente=bb['liens_entre_generations_differentes_hors_parente'],
                              chevauchements=bb['chevauchements'], duree_s=round(time.time() - t0, 1))), flush=True)
    tot['choix_permis_par_paire'] = {str(k): v for k, v in sorted(tot['choix_permis_par_paire'].items())}
    print(json.dumps(dict(bilan=True, partie='hasard', graines=[a, b], generations=gmax, **tot)), flush=True)

def partie_cellules(gmax):
    """AJOUT NON SCELLE. Toutes les cellules (quatre constituants tous lies) du tissu de la regle de T32, a la generation gmax."""
    from x31_cellule import cellules
    t0 = time.time(); M, X, T, sans = les_24(); circ = frozenset((GERME[i], GERME[(i + d) % 5]) for i in range(5) for d in (1, 2))
    nes, tu, mere, tailles, c = regle_T32(M, X, T, circ, gmax); L = sorted(nes)
    r = dict(cellules=0, cellules_du_germe=0, cellules_d_une_tuile_porte_qui_contiennent_son_constituant=0, cellules_avec_au_plus_un_constituant_du_germe=0,
             dont_quatre_ages_differents=0); cotes_nes = {}
    for (i, j, k, l), cotes in cellules(L):
        C = [L[i], L[j], L[k], L[l]]; r['cellules'] += 1; ng = sum(1 for u in C if u in GERME_ENS)
        if ng == 4: r['cellules_du_germe'] += 1
        if ng <= 1:
            r['cellules_avec_au_plus_un_constituant_du_germe'] += 1
            if len({nes[u] for u in C}) == 4: r['dont_quatre_ages_differents'] += 1
        y = max(C, key=lambda u: nes[u])
        if nes[y] > 0 and all(u in tu[y] for u in C): r['cellules_d_une_tuile_porte_qui_contiennent_son_constituant'] += 1
        cotes_nes[len(cotes)] = cotes_nes.get(len(cotes), 0) + 1
    print(json.dumps(dict(partie='cellules', generation=gmax, constituants=len(L), **r, cellules_attendues=5 + 4 * (len(L) - 5),
                          cellules_selon_le_nombre_de_cotes_nes={str(k): v for k, v in sorted(cotes_nes.items())}, duree_s=round(time.time() - t0, 1))), flush=True)

if __name__ == '__main__':
    p = sys.argv[1]
    if p == 'D1': partie_D1(int(sys.argv[2]))
    elif p == 'D2': partie_D2()
    elif p == 'D3': partie_D3(sys.argv[2])
    elif p == 'D4': partie_D4(int(sys.argv[2]))
    elif p == 'D5': partie_D5(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif p == 'D6': partie_D6()
    elif p == 'hasard': partie_hasard(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif p == 'cellules': partie_cellules(int(sys.argv[2]))
