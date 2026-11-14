#!/usr/bin/env python3
"""C-145 / PR-3 -- differend K4, A1, S : mon programme a la tolerance de regroupement lue dans le code de ChatGPT (2e-8).
Ajout du 13 novembre 2026, apres lecture de pr3_independent.cpp (ligne 62 : r < a + 2e-8). Compare trajectoire par trajectoire."""
import json
import math
import pathlib
import sys
from multiprocessing import Pool

ICI = pathlib.Path(__file__).resolve().parent
sys.path[:0] = [str(ICI), str(ICI.parent)]
import c145c_tolerance as ct  # noqa: E402

if __name__ == '__main__':
    T0 = 2 * math.pi / math.sqrt(2)
    ref = {}
    for l in (ICI / 'chatgpt_pr3_K4_A1_S.txt').read_text().split():
        P, c, g, pany, t1, ncol, nimp = l.split(',')
        ref[(float(P), {'0.5': '1/2', '1': '1'}[c], int(g))] = (int(pany), float(t1) / T0, int(ncol))
    taches = [(2e-8, P, cad, g) for P in (0.25, 0.5) for cad in ('1/2', '1') for g in range(0, 9)]
    with Pool(2) as pool:
        res = pool.map(ct.une, taches, chunksize=2)
    memes_t1 = memes_issue = memes_col = 0
    lignes = []
    for x in res:
        cg = ref[(x['P'], x['cad'], x['g'])]
        ok_t = x['t1'] is not None and abs(x['t1'] - cg[1]) < 2e-3
        ok_i = (x['statut'] == 'PANY') == bool(cg[0])
        memes_t1 += ok_t
        memes_issue += ok_i
        memes_col += (x['ncol'] == cg[2])
        lignes.append(dict(P=x['P'], cad=x['cad'], g=x['g'], moi_t1=x['t1'], chatgpt_t1=cg[1], moi=x['statut'], chatgpt_durable=cg[0],
                           moi_collisions=x['ncol'], chatgpt_collisions=cg[2]))
    bilan = dict(tolerance=2e-8, n=len(res), memes_premieres_sorties_a_2e_3=memes_t1, memes_issues=memes_issue, memes_nombres_de_collisions=memes_col,
                 durables_moi=sum(x['statut'] == 'PANY' for x in res), durables_chatgpt=sum(v[0] for v in ref.values()), lignes=lignes)
    (ICI / 'c145c_tolerance_2e8.json').write_text(json.dumps(bilan, indent=1, default=str))
    print({k: v for k, v in bilan.items() if k != 'lignes'})
    for l in lignes:
        if not (abs((l['moi_t1'] or 0) - l['chatgpt_t1']) < 2e-3 and (l['moi'] == 'PANY') == bool(l['chatgpt_durable'])):
            print('  ecart', l)
