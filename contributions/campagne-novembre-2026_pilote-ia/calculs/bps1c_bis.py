#!/usr/bin/env python3
"""BP-S1c bis -- complements APRES COUP (non preenregistres), declares comme tels.  (Claude, 13 novembre 2026)
(a) part exacte des octaedres parmi les premieres fermetures a six sommets, regime A (ChatGPT mesure 32 sur 512) ;
(b) chi2 d'ensemble des dix-huit comptes de ChatGPT contre les probabilites exactes ; tetraedres de A et C reunis ;
(c) seuil de cout avec cinq sites (cinetique et equilibre) ; (d) cadence de naissance rapportee au temps de fermeture.
Usage : python3 bps1c_bis.py   (ecrit bps1c_bis.json)
"""
import json, math, pathlib, sys
ICI = pathlib.Path(__file__).resolve().parent
src = (ICI / 'bps1c.py').read_text().split('# ------------------------------------------------------------------ X3, X7')[0]
_err = sys.stderr
exec(src)
from scipy.stats import chi2 as loi_chi2
b = {}
# (a) octaedres
s = S[6]
info, ordre, trans = G[6]
ouverts = [m for m in ordre if not info[m][2]]
def est_octa(m):
    cnt = [0] * 15
    for f in range(20):
        if m >> f & 1:
            for e in FE[f]:
                cnt[e] += 1
    return all(sum(1 for e, x in zip(EDGES, cnt) if x and v in e) == 4 for v in range(6))
octa_tr = []
for m in ouverts:
    for n in trans[m]:
        octa_tr.append(info[n][2] and info[n][3] == 6 and est_octa(n))
octa_tr = np.array(octa_tr)
k = taux(s, *REGIMES['A'])
R = np.bincount(s['src'], weights=k, minlength=s['n'])
dedans = s['dst'] >= 0
A = sp.identity(s['n'], format='csr') - sp.csr_matrix((k[dedans] / R[s['src'][dedans]], (s['src'][dedans], s['dst'][dedans])), shape=(s['n'], s['n']))
p_octa = float(spsolve(A.tocsc(), np.bincount(s['src'][octa_tr], weights=k[octa_tr] / R[s['src'][octa_tr]], minlength=s['n']))[0])
p6 = bilan['X2_exact']['A']['exact']['6']
n6 = 512
b['a_octaedres'] = dict(probabilite_exacte=p_octa, part_parmi_les_six_sommets=p_octa / p6, attendu_sur_512=n6 * p_octa / p6, chatgpt=32,
                        ecart_en_sigma=(32 - n6 * p_octa / p6) / math.sqrt(n6 * (p_octa / p6) * (1 - p_octa / p6)))
# (b) chi2 d'ensemble
c2 = 0.0
for nom, r in bilan['X2_exact'].items():
    for c, e in zip(r['chatgpt'], r['attendu_sur_1200']):
        c2 += (c - e) ** 2 / e
pA = bilan['X2_exact']['A']['exact']['4']
b['b_ensemble'] = dict(chi2=c2, degres_de_liberte=12, probabilite=float(loi_chi2.sf(c2, 12)),
                       tetraedres_A_et_C=dict(chatgpt=299 + 305, attendu=2400 * pA, ecart_en_sigma=(604 - 2400 * pA) / math.sqrt(2400 * pA * (1 - pA))))
# (c) seuil avec cinq sites
f45 = lambda e: (lambda p: p[4] - p[5])(premiere_fermeture(5, e, 0.4, 4, 1.0))
b['c_seuil_cinq_sites'] = dict(cinetique=brentq(f45, 0.0, 3.0, xtol=1e-6), equilibre=math.log(3) / 2,
                               rappel_six_sites=dict(cinetique=0.9221887, equilibre=math.log(6) / 2),
                               formule_equilibre_n_sites='ln(3 (n - 4)) / 2 contre les coques a cinq sommets')
(ICI / 'bps1c_bis.json').write_text(json.dumps(b, indent=1, ensure_ascii=False, default=float))
print(json.dumps(b, indent=1, ensure_ascii=False, default=float))
