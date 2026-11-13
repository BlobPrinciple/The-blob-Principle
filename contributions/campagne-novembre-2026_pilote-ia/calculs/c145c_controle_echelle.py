# Contrôle D refait : le théorème d'échelle [T-2] est exact en machine pour RK4 (pas et tolérances se mettent à l'échelle) ; DOP853 a une tolérance absolue fixe,
# donc ses pas diffèrent d'un D à l'autre et les événements tardifs, sensibles, peuvent différer. On vérifie l'exactitude avec RK4 et on compte l'accord de DOP853.
from c145c import *
n = 0; same = {'rk': 0, 'dop': 0}; w = {'rk': 0.0, 'dop': 0.0}; early = 0; ne = 0
for top, a_ in (('K4', 0.5), ('T5', 0.75)):
    for g0 in (0.0, 0.04):
        for src in 'SC':
            n += 1
            for sv in ('rk', 'dop'):
                a = run3(top, src, 0.3, '1', 'A2', a_, 1.0, g0, 3, solver=sv); b = run3(top, src, 1.2, '1', 'A2', a_, 4.0, g0, 3, solver=sv)
                eq = key3(a) == key3(b) and a['chocs'] == b['chocs'] and a['ncol'] == b['ncol']; same[sv] += eq
                d = max(abs(a['travail'] * 4 - b['travail']) / 4, abs(a['chaleur'] * 4 - b['chaleur']) / 4, abs((a['t1'] or 0) - (b['t1'] or 0)) if (a['t1'] is None) == (b['t1'] is None) else 9.0); w[sv] = max(w[sv], d)
                if sv == 'dop' and a['col1'] is not None and b['col1'] is not None: ne += 1; early += abs(a['col1'][0] - b['col1'][0]) < 1e-8 and a['col1'][1] == b['col1'][1]
print(f"RK4 : {same['rk']}/{n} paires identiques, écart maximal {w['rk']:.1e}")
print(f"DOP853 : {same['dop']}/{n} paires de même classement ; première collision identique (à 1e-8 T0) dans {early}/{ne}")
print('CONTROLE D : ' + ('PASSE' if same['rk'] == n and w['rk'] < 1e-12 and early == ne else 'ECHOUE'))
