import json, time
from multiprocessing import Pool
from x35b_tore import lancer
PLAN = [(2000, 4.0, g) for g in range(3580, 3584)] + [(8000, 4.0, g) for g in range(3584, 3587)] + [(16000, 4.0, g) for g in (3587, 3588)]
def un(j):
    t = time.time(); r = lancer(*j); r['secondes'] = round(time.time() - t, 1); return r
if __name__ == '__main__':
    with Pool(2) as p, open('x35b_resultats.jsonl', 'a') as f:
        for r in p.imap(un, PLAN): f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
