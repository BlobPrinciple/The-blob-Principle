"""Synthese : D3 sur les 24, formule de T32 point 3, et combinatoire des appariements de T32 point 4."""
import json, itertools
L = [json.loads(l) for l in open('d2d3.out')]
d3 = [r for r in L if r['partie'] == 'D3']
dists = set(json.dumps(r['par_nombre_de_liens_gen3']) for r in d3)
zero = sum(r['par_nombre_de_liens_gen3']['0'] for r in d3)
formule = {g: 24 * 5 ** (5 * (2 ** (g - 2) - 1)) for g in (2, 3, 4)}
# appariements : filles de c = {s*, r1, r2}, de chat = {a*, r1', r2'} ; s* et a* liees si gardees toutes deux
dc = ['s*', 'r1', 'r2']; dh = ['a*', 'r1p', 'r2p']
res = {}
for perm in itertools.permutations(dh):
    pi = dict(zip(dc, perm))
    ok = 0
    for x in dc:
        keep_c = set(dc) - {x}; keep_h = set(dh) - {pi[x]}
        if not ('s*' in keep_c and 'a*' in keep_h): ok += 1
    res['-'.join(f'{k}:{v}' for k, v in pi.items())] = ok
# facons permises par paire de soeurs (9 au total)
perm9 = sum(1 for kc in itertools.combinations(dc, 2) for kh in itertools.combinations(dh, 2) if not ('s*' in kc and 'a*' in kh))
print(json.dumps(dict(partie='synthese', tissus_D3=len(d3), distributions_D3_distinctes=len(dists), distribution=json.loads(dists.pop()),
      tous_cinq_liens_de_la_forme=all(r['de_la_forme_annoncee'] == 5 and r['paires_liees'] == 5 for r in d3),
      sans_lien_gen3_total=zero, formule_T32=formule, un_seul_sans_risque_par_tissu=all(r['sans_lien_et_aucune_fille_a_risque'] == 1 for r in d3),
      facons_permises_par_paire_sur_9=perm9, facons_identiques_permises_selon_l_appariement=res)))
