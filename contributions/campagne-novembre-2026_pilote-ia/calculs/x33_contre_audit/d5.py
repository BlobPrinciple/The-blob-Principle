"""D5 / T30 / T31 point 2.
 brute2      : tous les deroulements jusqu'a la generation 2, 44 departs.
 brute3 k    : tous les deroulements jusqu'a la generation 3 au-dessus de k tissus de generation 2 (les 24 sans lien en partie).
 hasard a b g: tirages au hasard (graines a..b), g generations : T30 (a), groupes (reciproque pas a pas), T31 point 2 sur les liens."""
import json, sys, time, itertools, random
from alib import *
from rule import *


def groups(run):
    """Requerants groupes par le constituant dont ils demandent une fille propre."""
    G = {}
    for p in run.requesters():
        key = run.last.get(p, p)
        G.setdefault(key, []).append(p)
    return G


def group_outcomes(run, key, reqs):
    """Toutes les affectations injectives permises au sein du groupe : liste de (dict p->x)."""
    opts = [[x for x in run.options(p) if x not in run.gen] for p in reqs]
    out = []
    for combo in itertools.product(*opts):
        if len(set(combo)) == len(combo):
            out.append(dict(zip(reqs, combo)))
    return out


def check_disjoint(run, G):
    seen = {}
    for key, reqs in G.items():
        for p in reqs:
            for x in run.options(p):
                if x in seen and seen[x] != key:
                    return False
                seen[x] = key
    return True


mode = sys.argv[1]
t0 = time.time()
P = Pack()
for _v in GERM:
    P.gate_of(M[_v], GERMSET - {_v} | {M[_v]})
if mode == 'brute2':
    tissues = {}
    per_start = []
    disjoint_all = True
    runs = 0
    group_sizes = set()
    for sg in derangements():
        r = Run(P)
        r.step1(sg)
        G = groups(r)
        disjoint_all &= check_disjoint(r, G)
        group_sizes.add(tuple(sorted(len(v) for v in G.values())))
        outs = {k: group_outcomes(r, k, v) for k, v in G.items()}
        keys = sorted(outs)
        S = set()
        for combo in itertools.product(*[outs[k] for k in keys]):
            runs += 1
            born = frozenset(x for d in combo for x in d.values())
            S.add(born)
        per_start.append(S)
    union = set().union(*per_start)
    # ensemble annonce par T30 : chaque M_v garde deux de ses quatre filles propres
    ann = set()
    pdl = {v: [x for x, f in P.proper_daughters(M[v])] for v in GERM}
    for combo in itertools.product(*[list(itertools.combinations(pdl[v], 2)) for v in GERM]):
        ann.add(frozenset(x for pr in combo for x in pr))
    print(json.dumps(dict(partie='D5-brute2', departs=len(per_start), deroulements=runs, groupes_disjoints=disjoint_all,
                          tailles_des_groupes=sorted(group_sizes), tissus_par_depart=sorted(set(len(s) for s in per_start)),
                          tous_les_departs_memes_tissus=all(s == per_start[0] for s in per_start), tissus_obtenus=len(union),
                          tissus_annonces_T30=len(ann), egalite=(union == ann), duree_s=round(time.time() - t0, 1))))

elif mode == 'brute3':
    k = int(sys.argv[2])
    # tous les deroulements jusqu'a la generation 2, en gardant l'etat complet
    pdl = {v: [x for x, f in P.proper_daughters(M[v])] for v in GERM}
    rng = random.Random(33)
    allsets = []
    for combo in itertools.product(*[list(itertools.combinations(pdl[v], 2)) for v in GERM]):
        allsets.append(frozenset(x for pr in combo for x in pr))
    # tissus sans lien en tete, puis des tissus au hasard
    def nlinks(s):
        return sum(1 for a, b in itertools.combinations(s, 2) if ip(a, b) == -1)
    free = sorted([s for s in allsets if nlinks(s) == 0], key=sorted)
    others = [s for s in allsets if nlinks(s) > 0]
    rng.shuffle(others)
    targets = free[:k // 2] + others[:k - k // 2]
    tset = {s: i for i, s in enumerate(targets)}
    found = {i: set() for i in range(len(targets))}
    runs_to = {i: 0 for i in range(len(targets))}
    bad_group = 0
    nondisj = 0
    for sg in derangements():
        r = Run(P)
        r.step1(sg)
        G = groups(r)
        outs = {kk: group_outcomes(r, kk, v) for kk, v in G.items()}
        keys = sorted(outs)
        for combo in itertools.product(*[outs[kk] for kk in keys]):
            born = frozenset(x for d in combo for x in d.values())
            if born not in tset:
                continue
            i = tset[born]
            runs_to[i] += 1
            r2 = Run(P)
            r2.step1(sg)
            assign = {}
            for d in combo: assign.update(d)
            r2.step(assign)
            G3 = groups(r2)
            if not check_disjoint(r2, G3): nondisj += 1
            per = []
            for kk in sorted(G3):
                o = group_outcomes(r2, kk, G3[kk])
                kept = frozenset(frozenset(d.values()) for d in o)
                full = frozenset(frozenset(pr) for pr in itertools.combinations([x for x, f in P.proper_daughters(kk)], 2))
                if kept != full: bad_group += 1
                per.append(sorted(kept, key=sorted))
            # tissus de generation 3 atteints par ce deroulement : produit
            for c3 in itertools.product(*per):
                found[i].add(frozenset(x for pr in c3 for x in pr))
    # annonce de T30 : chaque X ne garde deux de ses trois filles propres
    ok = []
    for i, s in enumerate(targets):
        ann = set()
        lists = [list(itertools.combinations([x for x, f in P.proper_daughters(x0)], 2)) for x0 in sorted(s)]
        for c3 in itertools.product(*lists):
            ann.add(frozenset(x for pr in c3 for x in pr))
        ok.append(dict(tissu=i, sans_lien_gen2=(nlinks(s) == 0), deroulements_qui_y_menent=runs_to[i],
                       tissus_gen3_obtenus=len(found[i]), annonces=len(ann), egalite=(found[i] == ann)))
    print(json.dumps(dict(partie='D5-brute3', tissus_gen2=len(targets), groupes_non_disjoints=nondisj,
                          groupes_ou_une_paire_manque=bad_group, detail=ok, duree_s=round(time.time() - t0, 1))))

elif mode == 'hasard':
    a, b, g = map(int, sys.argv[2:5])
    tot = dict(tirages=0, blocages=0, constituants_gen_1_a_g_1=0, sans_deux_filles_propres_nees=0, fille_propre_nee_ailleurs=0,
               germe_filles_propres_nees={}, groupes_controles=0, groupes_non_disjoints=0, groupes_ou_une_paire_manque=0,
               nees_gen2plus_sans_mere_propre_unique_nee_a_h_1=0, liens=0, liens_germe=0, liens_parent_enfant=0,
               liens_meme_gen=0, liens_gen_diff_hors_parente=0, chevauchements=0, liens_meme_gen_hors_forme=0,
               liens_meme_gen_par_gen={}, mere_regle_differente_mere_propre=0)
    for seed in range(a, b + 1):
        rng = random.Random(seed)
        r = Run(P)
        ds = derangements()
        r.step1(rng.choice(ds))
        okrun = True
        for h in range(2, g + 1):
            G = groups(r)
            tot['groupes_controles'] += len(G)
            if not check_disjoint(r, G): tot['groupes_non_disjoints'] += 1
            # reciproque pas a pas : chaque groupe peut realiser toutes les paires de filles propres de sa cle
            if h <= 6:
                for kk, reqs in G.items():
                    o = group_outcomes(r, kk, reqs)
                    kept = frozenset(frozenset(d.values()) for d in o)
                    full = frozenset(frozenset(pr) for pr in itertools.combinations([x for x, f in P.proper_daughters(kk)], 2))
                    if kept != full: tot['groupes_ou_une_paire_manque'] += 1
            if not r.random_step(rng):
                tot['blocages'] += 1; okrun = False; break
        tot['tirages'] += 1
        if not okrun: continue
        born = set(r.gen)
        for c in born:
            pd = [x for x, f in P.proper_daughters(c)]
            nb = [x for x in pd if x in born]
            if c in GERMSET:
                k = str(len(nb)); tot['germe_filles_propres_nees'][k] = tot['germe_filles_propres_nees'].get(k, 0) + 1
                continue
            if r.gen[c] <= g - 1:
                tot['constituants_gen_1_a_g_1'] += 1
                if len(nb) != 2: tot['sans_deux_filles_propres_nees'] += 1
                if any(r.gen[x] != r.gen[c] + 1 for x in nb): tot['fille_propre_nee_ailleurs'] += 1
            if r.gen[c] >= 2:
                pm = proper_mother(P, c)
                if len(pm) != 1 or pm[0] not in born or r.gen[pm[0]] != r.gen[c] - 1:
                    tot['nees_gen2plus_sans_mere_propre_unique_nee_a_h_1'] += 1
                elif pm[0] != r.rmother[c]:
                    tot['mere_regle_differente_mere_propre'] += 1
        L = sorted(born)
        links, over, adj = adjacency(L)
        tot['liens'] += len(links); tot['chevauchements'] += over
        for i, j in links:
            p, q = L[i], L[j]
            if p in GERMSET and q in GERMSET: tot['liens_germe'] += 1; continue
            if p in P.floor(q) or q in P.floor(p): tot['liens_parent_enfant'] += 1; continue
            if r.gen[p] != r.gen[q]: tot['liens_gen_diff_hors_parente'] += 1; continue
            tot['liens_meme_gen'] += 1
            hh = str(r.gen[p]); tot['liens_meme_gen_par_gen'][hh] = tot['liens_meme_gen_par_gen'].get(hh, 0) + 1
            # forme annoncee
            cp = proper_mother(P, p); cq = proper_mother(P, q)
            good = False
            if r.gen[p] == 2:
                # X(v,w), X(w,v) : meres M_v, M_w ; p laisse de cote w, q laisse de cote v
                if len(cp) == 1 and len(cq) == 1:
                    vp = [v for v in GERM if M[v] == cp[0]]; vq = [v for v in GERM if M[v] == cq[0]]
                    if vp and vq:
                        good = (leaves_out(P, cp[0], p) == vq[0] and leaves_out(P, cq[0], q) == vp[0])
            elif len(cp) == 1 and len(cq) == 1:
                c, ch = cp[0], cq[0]
                qa = proper_mother(P, c); qb = proper_mother(P, ch)
                if c != ch and qa and qa == qb and len(qa) == 1 or (c != ch and c in PAL1 and False):
                    pass
                mc = qa[0] if len(qa) == 1 else None
                # soeurs : meme mere propre (pour c du palier 1 il n'y en a pas d'unique : alors c, ch filles propres du meme M ? impossible ici)
                if mc is not None and qb == qa:
                    a_ = leaves_out(P, mc, c); s_ = leaves_out(P, mc, ch)
                    good = (leaves_out(P, c, p) == s_ and leaves_out(P, ch, q) == a_)
            if not good: tot['liens_meme_gen_hors_forme'] += 1
    tot['duree_s'] = round(time.time() - t0, 1)
    tot.update(partie='D5-hasard', graines=[a, b], generations=g)
    print(json.dumps(tot))
