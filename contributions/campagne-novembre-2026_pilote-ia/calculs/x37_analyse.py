#!/usr/bin/env python3
"""X-37 -- analyse des series du protocole des deux horloges, selon les definitions scellees dans x37_deux_horloges_prediction.txt.
Usage : x37_analyse.py x37_series.jsonl [niveaux separes par des virgules] > x37_analyse.out      (Claude, 28 novembre 2026)"""
import sys, json, math
import numpy as np

NIVEAUX = tuple(int(x) for x in sys.argv[2].split(',')) if len(sys.argv) > 2 else (1000, 2000, 4000, 8000, 16000)
R = [json.loads(l) for l in open(sys.argv[1])]


def ms(x):
    x = np.array([v for v in x if v is not None and np.isfinite(v)], float)
    if len(x) == 0: return (float('nan'), float('nan'), 0)
    return (float(x.mean()), float(x.std(ddof=1) / math.sqrt(len(x))) if len(x) > 1 else float('nan'), len(x))


def f(t, d=4):
    m, s, n = t
    return f'{m:+.{d}f} +/- {s:.{d}f} (n={n})'


def indices(S):
    return [next((i for i, n in enumerate(S['N']) if n >= L), None) for L in NIVEAUX]


def pente(x, y):
    x = np.array(x, float); y = np.array(y, float)
    if len(x) < 2: return None, None
    a, b = np.polyfit(x, y, 1); p = a * x + b; sst = ((y - y.mean()) ** 2).sum()
    return float(a), float(1 - ((y - p) ** 2).sum() / sst) if sst > 0 else None


def bootstrap(num, den, rng, B=2000):
    """Rapport des sommes sur les graines, erreur type par reechantillonnage des graines."""
    num = np.array(num, float); den = np.array(den, float); n = len(num)
    tir = rng.integers(0, n, (B, n))
    return float(num.sum() / den.sum()), float((num[tir].sum(1) / den[tir].sum(1)).std(ddof=1))


def analyse(nom, runs, natif):
    rng = np.random.default_rng(3700)
    print(f'\n===== {nom} : {len(runs)} graines =====')
    I = [indices(r['series']) for r in runs]
    assert all(all(i is not None for i in ii) for ii in I), 'un niveau non atteint'
    def col(cle, j, dec=0): return [r['series'][cle][ii[j] - dec] for r, ii in zip(runs, I)]
    print('niveau | N lu | pas | liens/N | purs/N (rho) | triangles/N | K4/N | degre max | K4 nes | K4 disparus | mitoses')
    for j, L in enumerate(NIVEAUX):
        N = np.array(col('N', j), float)
        print(f'{L:6d} | {N.mean():7.0f} | {np.mean(col("t", j)):4.1f} | {np.mean(np.array(col("E", j)) / N):.4f} | {f(ms(np.array(col("liens_purs", j)) / N))} | '
              f'{np.mean(np.array(col("triangles", j)) / N):.4f} | {f(ms(np.array(col("k4", j)) / N), 5)} | {np.mean(col("degre_max", j)):.1f} | '
              f'{np.mean(col("k4_nes", j)):.1f} | {np.mean(col("k4_morts", j)):.1f} | {np.mean(col("mitoses", j)):.0f}')
    # croissance
    lam = []; r2 = []
    for r, ii in zip(runs, I):
        S = r['series']; a, q = pente(S['t'][ii[1]:ii[-1] + 1], np.log(S['N'][ii[1]:ii[-1] + 1])); lam.append(a); r2.append(q)
    print(f'croissance, ln N contre le pas entre les niveaux {NIVEAUX[1]} et {NIVEAUX[-1]} : pente {f(ms(lam))} ; R2 moyen {np.mean(r2):.5f}, minimum {min(r2):.5f}')
    # rho et w
    print("densite d'aretes pures : pente locale d ln rho / d ln N, puis w = -pente - 1")
    for j in range(len(NIVEAUX) - 1):
        p = [math.log((r['series']['liens_purs'][ii[j + 1]] / r['series']['N'][ii[j + 1]]) / (r['series']['liens_purs'][ii[j]] / r['series']['N'][ii[j]])) /
             math.log(r['series']['N'][ii[j + 1]] / r['series']['N'][ii[j]]) for r, ii in zip(runs, I)]
        m = ms(p); print(f'  {NIVEAUX[j]:6d} -> {NIVEAUX[j + 1]:6d} : pente {f(m)} ; w = {-m[0] - 1:+.4f}')
    # fermetures par mitose
    sortie = {}
    for cle, nomc in (('k4_nes', 'K4'), ('triangles_nes', 'triangles')):
        print(f'fermetures de {nomc} par mitose, r (rapport des sommes sur les graines, erreur type par reechantillonnage) :')
        rr = []
        for j, L in enumerate(NIVEAUX):
            v, e = bootstrap(col(cle, j), col('mitoses', j), rng); rr.append((v, e))
            nuls = sum(1 for x in col(cle, j) if x == 0)
            print(f'  {L:6d} : r = {v:.5f} +/- {e:.5f} ; graines a zero fermeture : {nuls}')
        print('  pentes locales de ln r contre ln N (rapports des sommes ; erreur type par reechantillonnage des graines) :')
        for j in range(len(NIVEAUX) - 1):
            a = np.array(col(cle, j), float); b = np.array(col(cle, j + 1), float); ma = np.array(col('mitoses', j), float); mb = np.array(col('mitoses', j + 1), float)
            Na = np.array(col('N', j), float); Nb = np.array(col('N', j + 1), float); n = len(a); tir = rng.integers(0, n, (2000, n))
            def pl(ix): return math.log((b[ix].sum() / mb[ix].sum()) / (a[ix].sum() / ma[ix].sum())) / math.log(Nb[ix].mean() / Na[ix].mean())
            v = pl(np.arange(n)); e = float(np.std([pl(t) for t in tir if a[t].sum() > 0 and b[t].sum() > 0], ddof=1))
            print(f'  {NIVEAUX[j]:6d} -> {NIVEAUX[j + 1]:6d} : pente {v:+.4f} +/- {e:.4f}   (g = {-v:+.4f})')
        pg = []
        for r, ii in zip(runs, I):
            S = r['series']; x = [math.log(S['N'][i]) for i in ii if S[cle][i] > 0 and S['mitoses'][i] > 0]; y = [math.log(S[cle][i] / S['mitoses'][i]) for i in ii if S[cle][i] > 0 and S['mitoses'][i] > 0]
            pg.append(pente(x, y)[0] if len(x) == len(ii) else None)
        m = ms(pg); print(f'  pente par graine sur les {len(NIVEAUX)} niveaux (graines sans zero) : {f(m)}   donc g = {-m[0]:+.4f}')
        sortie[nomc] = dict(r=rr, pente_par_graine=m)
    # horloges
    print('horloges de la matiere')
    for nomh in ('H1, compte cumule T', 'H2, somme de K4 nes / N', 'H3, somme de K4 nes / K4 presents'):
        ex = []; r2e = []; r2p = []; loc0 = []; loc1 = []
        for r, ii in zip(runs, I):
            S = r['series']; th = []; c = 0.0
            for i in range(len(S['N'])):
                if nomh.startswith('H1'): c += S['k4_nes'][i]
                elif nomh.startswith('H2'): c += S['k4_nes'][i] / S['N'][i]
                else: c += (S['k4_nes'][i] / S['k4'][i]) if S['k4'][i] > 0 else 0.0
                th.append(c)
            idx = [i for i in range(ii[1], ii[-1] + 1) if th[i] > 0]
            if len(idx) < 4: continue
            lnN = [math.log(S['N'][i]) for i in idx]; t = [th[i] for i in idx]; lt = [math.log(x) for x in t]
            a, q = pente(lt, lnN); ex.append(a); r2p.append(q); r2e.append(pente(t, lnN)[1])
            loc0.append((lnN[1] - lnN[0]) / (lt[1] - lt[0]) if lt[1] > lt[0] else None); loc1.append((lnN[-1] - lnN[-2]) / (lt[-1] - lt[-2]) if lt[-1] > lt[-2] else None)
        m = ms(ex)
        print(f'  {nomh} : d ln N / d ln temps = {f(m)} ; exposant de a = N^(1/3) : {m[0] / 3:+.4f} ; R2 loi de puissance {np.mean(r2p):.5f} ; R2 exponentielle {np.mean(r2e):.5f} ; '
              f'pente locale au debut {f(ms(loc0), 3)}, a la fin {f(ms(loc1), 3)}')
    if natif:
        print('acceptation de la mitose selon le type de lien (rapport des sommes sur les graines) :')
        for j, L in enumerate(NIVEAUX):
            ap = sum(col('acceptes_pure', j)) / sum(col('essais_pure', j)); am = sum(col('acceptes_matiere', j)) / sum(col('essais_matiere', j))
            part = sum(col('acceptes_pure', j)) / (sum(col('acceptes_pure', j)) + sum(col('acceptes_matiere', j)))
            tx = np.array(col('mitoses', j), float) / np.array(col('N', j, 1), float)
            pred = 0.5 * (np.array(col('acceptes_pure', j), float) / np.array(col('essais_pure', j), float)) * np.array(col('liens_purs', j, 1), float) / np.array(col('N', j, 1), float)
            print(f'  {L:6d} : arete pure {ap:.4f} ; arete prise dans un triangle {am:.4f} ; rapport {ap / am:.1f} ; part des mitoses sur aretes pures {part:.4f} ; '
                  f'taux de croissance du pas {tx.mean():.4f} ; 0,5 x acceptation x rho = {pred.mean():.4f} ; ecart relatif {f(ms((pred - tx) / tx))}')
    return sortie


N40 = sorted([r for r in R if r['bras'] == 'N' and r['n_init'] == 40], key=lambda r: r['graine'])
C40 = sorted([r for r in R if r['bras'] == 'C' and r['n_init'] == 40], key=lambda r: r['graine'])
N160 = sorted([r for r in R if r['bras'] == 'N' and r['n_init'] == 160], key=lambda r: r['graine'])
print('X-37, analyse. Series :', len(R), '; niveaux :', NIVEAUX)
a = analyse('BRAS N (mitose native, anneau de 40)', N40, True)
c = analyse('BRAS C (mitose + age + dissipation, anneau de 40)', C40, False) if C40 else None
if N160:
    b = analyse('CONTROLE (mitose native, anneau de 160)', N160, True)
    print('\ncontrole du depart : r(K4) au depart 160 moins r(K4) au depart 40, en erreurs types')
    for j, L in enumerate(NIVEAUX):
        (v1, e1), (v2, e2) = a['K4']['r'][j], b['K4']['r'][j]
        print(f'  {L:6d} : {v2:.5f} contre {v1:.5f} ; ecart {(v2 - v1) / math.hypot(e1, e2):+.2f} erreur type')
