"""Agrege les sorties t28_*.out."""
import json, glob, sys
from collections import Counter
for f in sorted([g for g in glob.glob('/home/claude/audit_x32/t28_*.out') if 'bilan' not in g]):
    runs = [json.loads(l) for l in open(f) if l.startswith('{')]
    tail = Counter(); err = Counter(); bloque = 0; over = 0; nonclos = 0; dist = 0; stats = Counter(); meme = None; vois = Counter()
    for r in runs:
        if 'bloque_a_la_generation' in r: bloque += 1; continue
        tail[tuple(r['tailles'])] += 1
        for k, v in r['erreurs'].items(): err[k] += v
        over += r['chevauchements']; nonclos += r['non_clos_par_plancher']; dist += (not r['distincts'])
        for k, v in r['stats'].items(): stats[k] += v
        m = r['liens_meme_generation']; meme = m if meme is None else [a + b for a, b in zip(meme, m)]
        for k, v in r['voisins_des_nouvelles_nees'].items(): vois[k] += v
    print(json.dumps(dict(fichier=f.split('/')[-1], lancements=len(runs), bloques=bloque, tailles={str(list(k)): v for k, v in tail.items()},
                          erreurs=dict(err), chevauchements=over, non_clos_par_plancher=nonclos, avec_doublons=dist,
                          liens_meme_generation_cumules=meme, voisins_des_nouvelles_nees_gen_finale=dict(vois), stats=dict(sorted(stats.items()))),
                     ensure_ascii=False))
