#!/usr/bin/env python3
"""X-35 : lanceur. Exécute le plan figé dans x35_fractions_kappa4_prediction.txt et écrit une ligne JSON par état dans x35_resultats.jsonl."""
import json, sys, time
from multiprocessing import Pool
from x35_fractions_kappa4 import lancer

PLAN = []
PLAN += [(1000, 4.0, g, 'blob') for g in range(3500, 3512)]
PLAN += [(1000, 4.0, g, 'temoin') for g in range(3500, 3506)]
PLAN += [(2000, 4.0, g, 'blob') for g in range(3520, 3528)]
PLAN += [(2000, k, g, 'blob') for k in (3.0, 3.5, 4.5, 5.0, 6.0, 6.6, 8.0) for g in range(3570, 3574)]
PLAN += [(4000, 4.0, g, 'blob') for g in range(3530, 3536)]
PLAN += [(4000, 4.0, g, 'temoin') for g in range(3530, 3533)]
PLAN += [(8000, 4.0, g, 'blob') for g in range(3540, 3544)]
PLAN += [(16000, 4.0, g, 'blob') for g in range(3550, 3553)]
PLAN += [(32000, 4.0, g, 'blob') for g in range(3560, 3562)]

def un(job):
    t = time.time(); r = lancer(*job); r['secondes'] = round(time.time() - t, 1); return r

if __name__ == '__main__':
    with Pool(2) as p, open('x35_resultats.jsonl', 'a') as f:
        for r in p.imap(un, PLAN):
            f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
