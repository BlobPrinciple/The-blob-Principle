# Suite de l'audit [T-2] : comparaison exacte (positions identiques ; vitesses de D = 2 égales au double de celles de D = 1/2, la multiplication par 2 étant exacte).
from c145c import *
def etats(D, P, cad, sub, g, nmax=30):
    cx = Ctx('K4', D, 0.0, 0.5); c = {'1/2': .5, '1': 1.}[cad]; T0 = cx.T0; s = np.zeros(cx.N); s[:12] = geometrie('K4', g).ravel(); r = np.empty(6); lensg(s, cx.BI, cx.BJ, r)
    side = np.ones((3, 10), np.int64); side[0, :6] = np.where(r >= R0, 1, -1); side[1, :6] = -1; ev = []; colls = []; st = dict(rmin=np.ones(6), ovl=-1.0, k=0, fprev=None, IFU=0.0); t = 0.0; out = []
    for j in range(nmax):
        tm = j * c * T0
        if tm > t + 1e-12: s = rk_adv3(cx, s, t, tm, sub, side, ev, st, colls); t = tm
        out.append((s[:12].copy(), s[12:24].copy(), len(colls), 'avant choc')); kick3(s, P * c, 4, v=0); out.append((s[:12].copy(), s[12:24].copy(), len(colls), 'après choc'))
    return out
for g in (0, 3):
    a = etats(0.5, 0.0625 * 0.5, '1', 1, g); b = etats(2.0, 0.0625 * 2.0, '1', 1, g)
    k = next((i for i, (x, y) in enumerate(zip(a, b)) if not (np.array_equal(x[0], y[0]) and np.array_equal(2 * x[1], y[1]))), None)
    print(f'géométrie {g} : premier état non identique : ' + ('aucun sur 30 chocs' if k is None else f"n° {k} ({a[k][3]} {k // 2}) ; collisions avant : {a[k][2]} / {b[k][2]} ; écart positions {np.abs(a[k][0]-b[k][0]).max():.1e}, vitesses {np.abs(2*a[k][1]-b[k][1]).max():.1e}"))
# le potentiel et le second membre sont-ils exactement covariants ? (force de D = 2 = 4 fois celle de D = 1/2, au bit près)
rng = np.random.default_rng(7); bad = 0
ca = Ctx('K4', 0.5, 0.0, 0.5); cb = Ctx('K4', 2.0, 0.0, 0.5)
for _ in range(2000):
    s = np.zeros(25); s[:12] = (P0 * rng.uniform(.7, 2.5) + rng.normal(0, .2, (4, 3))).ravel(); s[12:24] = rng.normal(0, 1, 12); s2 = s.copy(); s2[12:24] *= 2
    fa = ca.fun(0, s); fb = cb.fun(0, s2); bad += not (np.array_equal(2 * fa[:12], fb[:12]) and np.array_equal(4 * fa[12:24], fb[12:24]))
print('second membre : états non exactement covariants :', bad, '/ 2000')
import math; print('T0(1/2) == 2 T0(2) :', ca.T0 == 2 * cb.T0, '; pas RK :', ca.T0 / 1024 == 2 * (cb.T0 / 1024))
