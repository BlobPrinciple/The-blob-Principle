#!/usr/bin/env python3
"""Rejeu de controle : chaque programme de la campagne qui a une sortie .out du meme nom est relance sans argument, dans une copie du dossier,
et sa sortie standard est comparee a la sortie conservee. Verdicts : IDENTIQUE, PROCHE (memes mots, nombres egaux a 1e-6 pres ou champs de duree),
DIFFERENT, ERREUR (code de retour non nul), DELAI (plus de DELAI secondes)."""
import json, os, re, subprocess, sys, time
ICI = os.getcwd(); DELAI = int(sys.argv[1]); part, nparts = int(sys.argv[2]), int(sys.argv[3])
progs = sorted(f for f in os.listdir('.') if f.endswith('.py') and os.path.exists(f[:-3] + '.out'))
progs = [p for i, p in enumerate(progs) if i % nparts == part]
num = re.compile(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?')
def proche(a, b):
    la, lb = a.split('\n'), b.split('\n')
    if len(la) != len(lb): return False, 'nombre de lignes %d contre %d' % (len(la), len(lb))
    ecart = 0.0
    for x, y in zip(la, lb):
        if x == y: continue
        if re.search(r'dur[ée]e|temps|secondes| s\b|elapsed|time', x, re.I): continue
        sx, sy = num.sub('#', x), num.sub('#', y)
        if sx != sy: return False, 'ligne differente : %r / %r' % (x[:90], y[:90])
        for u, v in zip(num.findall(x), num.findall(y)):
            u, v = float(u), float(v)
            if u != v:
                e = abs(u - v) / max(abs(u), abs(v), 1e-300); ecart = max(ecart, e)
                if e > 1e-6: return False, 'nombre different : %r / %r' % (x[:90], y[:90])
    return True, 'ecart relatif maximal %.1e' % ecart
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', NUMBA_CACHE_DIR=os.path.join(ICI, '..', '..', '..', '..', 'numba'), OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
res = []
for p in progs:
    ref = open(p[:-3] + '.out', encoding='utf-8', errors='replace').read()
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, p], capture_output=True, text=True, timeout=DELAI, env=env)
        d = time.time() - t0
        if r.returncode != 0:
            v, note = 'ERREUR', (r.stderr.strip().split('\n')[-1] if r.stderr.strip() else 'code %d' % r.returncode)[:160]
        elif r.stdout == ref: v, note = 'IDENTIQUE', ''
        else:
            ok, note = proche(r.stdout.rstrip('\n'), ref.rstrip('\n'))
            v = 'PROCHE' if ok else 'DIFFERENT'
    except subprocess.TimeoutExpired:
        d = time.time() - t0; v, note = 'DELAI', ''
    res.append(dict(programme=p, verdict=v, duree_s=round(d, 1), note=note, octets_reference=len(ref)))
    print(json.dumps(res[-1], ensure_ascii=False), flush=True)
json.dump(res, open(os.path.join(ICI, '..', '..', '..', '..', 'rejeu_%d.json' % part), 'w'), indent=1, ensure_ascii=False)
